from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("harness_lab.proposal")

from harness_lab.bootstrap import _backend_lever_catalog, write_bootstrap_snapshot, write_decision_bundle
from harness_lab.budget import read_budget
from harness_lab.datasets import choose_best_prepared_dataset, get_dataset_record
from harness_lab.diversity import read_diversity
from harness_lab.external_review import read_external_review
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight
from harness_lab.llm import run_claude_json
from harness_lab.memory import build_candidate_index, read_json
from harness_lab.policy import read_policy
from harness_lab.synthesis import synthesize_parent_candidates
from harness_lab.workspace import create_candidate_workspace, write_json


ALLOWED_BACKEND_MODULES = {"science_model", "science_loss", "science_eval", "science_config", "science_train"}


@dataclass(frozen=True)
class DraftProposal:
    candidate_id: str
    parent_id: str | None
    dataset_id: str
    status: str
    rationale: str
    target: dict
    changes: tuple[dict, ...]
    backend_levers: dict
    no_lever_reason: str
    llm_backend_lever_retry_used: bool
    memory_context: dict

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "parent_id": self.parent_id,
            "dataset_id": self.dataset_id,
            "status": self.status,
            "rationale": self.rationale,
            "target": self.target,
            "changes": list(self.changes),
            "backend_levers": self.backend_levers,
            "no_lever_reason": self.no_lever_reason,
            "llm_backend_lever_retry_used": self.llm_backend_lever_retry_used,
            "memory_context": self.memory_context,
        }


def _candidate_root(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id


def _load_diagnosis(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(_candidate_root(candidates_dir, candidate_id) / "diagnosis" / "summary.json")


def _load_workspace(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(_candidate_root(candidates_dir, candidate_id) / "workspace.json")


def _load_existing_proposal(candidates_dir: Path, candidate_id: str) -> dict:
    path = _candidate_root(candidates_dir, candidate_id) / "proposal.json"
    if not path.exists():
        return {}
    return read_json(path)


def choose_dataset_id(candidates_dir: Path) -> str:
    memory_dir = candidates_dir.parent / "memory"
    best = choose_best_prepared_dataset(memory_dir)
    return str(best.get("dataset_id", "")) if best else ""


def choose_parent_candidate(candidates_dir: Path) -> str | None:
    synthesis = synthesize_parent_candidates(candidates_dir)
    return synthesis.get("top_parent_id")


def _candidate_summary_map(index: dict) -> dict[str, dict]:
    return {
        str(item.get("candidate_id", "")): item
        for item in index.get("candidates", [])
        if str(item.get("candidate_id", "")).strip()
    }


def _novelty_basis_from_memory(index: dict, parent_summary: dict, parent_diagnosis: dict) -> str:
    parent_failure_modes = [str(item).strip() for item in parent_diagnosis.get("failure_modes", []) if str(item).strip()]
    parent_failure = parent_failure_modes[0] if parent_failure_modes else str(parent_summary.get("expected_failure_mode", "")).strip()
    if parent_failure:
        mechanism = (
            str(parent_diagnosis.get("mechanism", "")).strip()
            or str(parent_summary.get("diagnosis_mechanism", "")).strip()
            or str(parent_summary.get("harness_component", "")).strip()
        )
        if mechanism:
            return f"counteracts repeated {parent_failure} around {mechanism}"
        return f"counteracts repeated {parent_failure}"

    repeated_failures = sorted(index.get("failure_mode_counts", {}).items(), key=lambda item: (-item[1], item[0]))
    dominant_components = sorted(index.get("harness_component_counts", {}).items(), key=lambda item: (-item[1], item[0]))
    failure_label = repeated_failures[0][0] if repeated_failures else parent_summary.get("expected_failure_mode", "")
    dominant_component = dominant_components[0][0] if dominant_components else parent_summary.get("harness_component", "")
    if failure_label and dominant_component:
        return f"counteracts repeated {failure_label} around {dominant_component}"
    if failure_label:
        return f"counteracts repeated {failure_label}"
    if dominant_component:
        return f"explores a new angle around {dominant_component}"
    return "first structured proposal from indexed diagnosis memory"


def _proposal_change_items(parent_diagnosis: dict, parent_summary: dict) -> tuple[dict, ...]:
    counterfactuals = [str(item) for item in parent_diagnosis.get("counterfactuals", []) if str(item).strip()]
    summary = str(parent_diagnosis.get("summary", "")).strip()
    mechanism = str(parent_diagnosis.get("mechanism", "")).strip() or str(parent_summary.get("diagnosis_mechanism", "")).strip()
    expected_failure_mode = str(parent_summary.get("expected_failure_mode", "")).strip()

    changes: list[dict] = []
    for counterfactual in counterfactuals[:3]:
        changes.append(
            {
                "kind": "counterfactual",
                "mechanism": mechanism,
                "summary": counterfactual,
            }
        )
    if not changes and summary:
        changes.append(
            {
                "kind": "diagnosis_response",
                "mechanism": mechanism,
                "summary": f"Address diagnosed issue: {summary}",
            }
        )
    if expected_failure_mode:
        changes.append(
            {
                "kind": "guardrail",
                "mechanism": mechanism,
                "summary": f"Reduce recurrence of {expected_failure_mode}",
            }
        )
    return tuple(changes)


def _hardware_guardrail_items(hardware_profile: dict) -> tuple[dict, ...]:
    environment_hint = str(hardware_profile.get("environment_hint", "")).strip()
    cpu_count = hardware_profile.get("cpu_count")
    memory_gb = hardware_profile.get("memory_gb_estimate")
    items: list[dict] = []
    if environment_hint == "local_macos":
        items.append(
            {
                "kind": "hardware_guardrail",
                "mechanism": "execution_policy",
                "summary": "Prefer compact local experiments on macOS before scaling up.",
            }
        )
    if isinstance(cpu_count, int) and cpu_count > 0 and cpu_count <= 4:
        items.append(
            {
                "kind": "hardware_guardrail",
                "mechanism": "execution_policy",
                "summary": "Keep candidate evaluation lightweight because CPU headroom is limited.",
            }
        )
    if isinstance(memory_gb, (int, float)) and memory_gb <= 8:
        items.append(
            {
                "kind": "hardware_guardrail",
                "mechanism": "memory_policy",
                "summary": "Avoid memory-heavy candidate shapes on this machine.",
            }
        )
    return tuple(items)


def _hindsight_change_items(hindsight: dict, mechanism: str) -> tuple[dict, ...]:
    items: list[dict] = []
    mechanism = mechanism.strip()
    over_explored = {
        str(item.get("mechanism", "")).strip()
        for item in hindsight.get("over_explored_mechanisms", [])
        if str(item.get("mechanism", "")).strip()
    }
    under_explored = {
        str(item.get("mechanism", "")).strip()
        for item in hindsight.get("under_explored_promising_mechanisms", [])
        if str(item.get("mechanism", "")).strip()
    }
    over_backend = {
        str(item.get("fingerprint", "")).strip()
        for item in hindsight.get("over_explored_backend_fingerprints", [])
        if str(item.get("fingerprint", "")).strip()
    }
    under_backend = {
        str(item.get("fingerprint", "")).strip()
        for item in hindsight.get("under_explored_backend_fingerprints", [])
        if str(item.get("fingerprint", "")).strip()
    }
    if mechanism and mechanism in over_explored:
        items.append(
            {
                "kind": "hindsight_guardrail",
                "mechanism": mechanism,
                "summary": f"Use a smaller or more novel follow-up because `{mechanism}` looks over-explored in hindsight.",
            }
        )
    if mechanism and mechanism in under_explored:
        items.append(
            {
                "kind": "hindsight_priority",
                "mechanism": mechanism,
                "summary": f"Lean into `{mechanism}` because hindsight says it was under-explored relative to its evidence.",
            }
        )
    for fingerprint in sorted(under_backend)[:2]:
        items.append(
            {
                "kind": "backend_hindsight_priority",
                "mechanism": fingerprint,
                "summary": f"Bias toward backend change type `{fingerprint}` because hindsight says it is promising and under-explored.",
            }
        )
    for fingerprint in sorted(over_backend)[:2]:
        items.append(
            {
                "kind": "backend_hindsight_guardrail",
                "mechanism": fingerprint,
                "summary": f"Use caution around backend change type `{fingerprint}` because hindsight says it has been over-explored.",
            }
        )
    for adjustment in hindsight.get("policy_adjustments", [])[:2]:
        items.append(
            {
                "kind": "hindsight_policy",
                "mechanism": mechanism or "policy",
                "summary": str(adjustment),
            }
        )
    return tuple(items)


def _policy_change_items(policy: dict, mechanism: str) -> tuple[dict, ...]:
    items: list[dict] = []
    summary = str(policy.get("summary", "")).strip()
    selection_mode = str(policy.get("selection_mode", "")).strip()
    preferred_backend = str(policy.get("preferred_runner_backend", "")).strip()
    if summary:
        items.append(
            {
                "kind": "policy_summary",
                "mechanism": mechanism or "policy",
                "summary": summary,
            }
        )
    if selection_mode:
        items.append(
            {
                "kind": "policy_mode",
                "mechanism": mechanism or "policy",
                "summary": f"Selection mode is `{selection_mode}` for this step.",
            }
        )
    if preferred_backend:
        items.append(
            {
                "kind": "policy_backend",
                "mechanism": mechanism or "execution_policy",
                "summary": f"Preferred runner backend is `{preferred_backend}`.",
            }
        )
    return tuple(items)


def _budget_change_items(budget: dict, mechanism: str) -> tuple[dict, ...]:
    items: list[dict] = []
    mechanism = mechanism.strip()
    for entry in budget.get("mechanism_budgets", []):
        if str(entry.get("mechanism", "")).strip() != mechanism:
            continue
        remaining = int(entry.get("remaining_followups", 0) or 0)
        if bool(entry.get("exhausted")):
            items.append(
                {
                    "kind": "budget_guardrail",
                    "mechanism": mechanism,
                    "summary": f"`{mechanism}` exhausted its follow-up budget, so this step should broaden the search or shrink the change.",
                }
            )
        else:
            items.append(
                {
                    "kind": "budget_headroom",
                    "mechanism": mechanism,
                    "summary": f"`{mechanism}` has {remaining} follow-up slots remaining in the current budget.",
                }
            )
        break
    if str(budget.get("exploration_mode", "")) == "force_broad_exploration":
        items.append(
            {
                "kind": "budget_exploration_mode",
                "mechanism": mechanism or "policy",
                "summary": "Budget says to force broader exploration instead of repeating exhausted mechanisms.",
            }
        )
    return tuple(items)


def _external_review_change_items(review: dict) -> tuple[dict, ...]:
    if not bool(review.get("review_requested")) and str(review.get("status", "")) != "reviewed":
        return ()
    items: list[dict] = []
    for item in review.get("lab_advice", [])[:3]:
        summary = str(item.get("summary", "")).strip()
        kind = str(item.get("kind", "external_review")).strip() or "external_review"
        if summary:
            items.append(
                {
                    "kind": f"external_review_{kind}",
                    "mechanism": "external_review",
                    "summary": summary,
                }
            )
    return tuple(items)


def _diversity_change_items(diversity: dict, chosen_mechanism: str, latest_mechanism: str) -> tuple[dict, ...]:
    if not bool(diversity.get("novelty_step_recommended")):
        return ()
    streak = int(diversity.get("current_mechanism_streak", 0) or 0)
    if chosen_mechanism and chosen_mechanism != latest_mechanism:
        return (
            {
                "kind": "diversity_novelty_step",
                "mechanism": chosen_mechanism,
                "summary": f"Recent mechanism streak reached {streak}, so this proposal takes a novelty step toward `{chosen_mechanism}`.",
            },
        )
    return (
        {
            "kind": "diversity_warning",
            "mechanism": chosen_mechanism or latest_mechanism or "policy",
            "summary": f"Recent mechanism streak reached {streak}; a more novel branch is recommended soon.",
        },
    )


def _choose_parent_for_branching(index: dict, synthesis: dict, budget: dict, diversity: dict) -> tuple[str | None, str]:
    ranked = list(synthesis.get("ranked_parents", []))
    if not ranked:
        return synthesis.get("top_parent_id"), "default"

    summary_map = _candidate_summary_map(index)
    latest_summary = index.get("candidates", [])[-1] if index.get("candidates") else {}
    latest_mechanism = str(latest_summary.get("diagnosis_mechanism") or latest_summary.get("harness_component") or "").strip()
    budget_mode = str(budget.get("exploration_mode", "balanced")).strip()
    novelty_recommended = bool(diversity.get("novelty_step_recommended"))
    exhausted = {
        str(item.get("mechanism", "")).strip()
        for item in budget.get("mechanism_budgets", [])
        if bool(item.get("exhausted")) and str(item.get("mechanism", "")).strip()
    }

    if budget_mode == "force_broad_exploration" or novelty_recommended:
        for item in ranked:
            candidate_id = str(item.get("candidate_id", "")).strip()
            mechanism = str(summary_map.get(candidate_id, {}).get("diagnosis_mechanism") or summary_map.get(candidate_id, {}).get("harness_component") or "").strip()
            if mechanism and mechanism != latest_mechanism and mechanism not in exhausted:
                return candidate_id, "force_broad_exploration"
        for item in ranked:
            candidate_id = str(item.get("candidate_id", "")).strip()
            mechanism = str(summary_map.get(candidate_id, {}).get("diagnosis_mechanism") or summary_map.get(candidate_id, {}).get("harness_component") or "").strip()
            if mechanism and mechanism not in exhausted:
                return candidate_id, "force_broad_exploration_fallback"

    if budget_mode == "focus_promising":
        return str(ranked[0].get("candidate_id") or synthesis.get("top_parent_id")), "focus_promising"

    return str(ranked[0].get("candidate_id") or synthesis.get("top_parent_id")), "default"


def _branching_mode_change_items(branching_mode: str, chosen_mechanism: str, latest_mechanism: str) -> tuple[dict, ...]:
    if branching_mode == "force_broad_exploration" and chosen_mechanism and chosen_mechanism != latest_mechanism:
        return (
            {
                "kind": "exploration_jump",
                "mechanism": chosen_mechanism,
                "summary": f"Branch deliberately toward `{chosen_mechanism}` instead of repeating the most recent mechanism `{latest_mechanism}`.",
            },
        )
    if branching_mode == "focus_promising":
        return (
            {
                "kind": "exploration_focus",
                "mechanism": chosen_mechanism or latest_mechanism or "policy",
                "summary": "Stay close to the strongest promising mechanism while there is still budget headroom.",
            },
        )
    return ()


def _llm_fallback_changes(fallback_changes: tuple[dict, ...], mutation_brief: dict) -> tuple[dict, ...]:
    target_module = str(mutation_brief.get("target_module", "")).strip()
    if target_module not in ALLOWED_BACKEND_MODULES:
        return fallback_changes
    suppressed_kinds = {
        "budget_guardrail",
        "budget_exploration_mode",
        "diversity_novelty_step",
        "diversity_warning",
        "exploration_jump",
    }
    filtered: list[dict] = []
    for item in fallback_changes:
        kind = str(item.get("kind", "")).strip()
        mechanism = str(item.get("mechanism", "")).strip()
        if kind in suppressed_kinds and mechanism not in {"", target_module}:
            continue
        if kind in suppressed_kinds:
            continue
        filtered.append(item)
    return tuple(filtered)


def _llm_proposal_prompt(
    *,
    bootstrap_snapshot: dict,
    decision_bundle: dict,
    mutation_brief: dict,
    parent_diagnosis: dict,
    parent_summary: dict,
    branching_mode: str,
    fallback_target: dict,
    fallback_changes: tuple[dict, ...],
    fallback_rationale: str,
) -> str:
    payload = {
        "bootstrap_snapshot": bootstrap_snapshot,
        "decision_bundle": decision_bundle,
        "parent_diagnosis": {
            "summary": parent_diagnosis.get("summary", ""),
            "mechanism": parent_diagnosis.get("mechanism", ""),
            "failure_modes": parent_diagnosis.get("failure_modes", []),
            "counterfactuals": parent_diagnosis.get("counterfactuals", [])[:5],
        },
        "parent_summary": {
            "candidate_id": parent_summary.get("candidate_id", ""),
            "diagnosis_mechanism": parent_summary.get("diagnosis_mechanism", ""),
            "expected_failure_mode": parent_summary.get("expected_failure_mode", ""),
            "backend_fingerprints": parent_summary.get("backend_fingerprints", []),
            "benchmark_score": parent_summary.get("benchmark_score"),
            "audit_score": parent_summary.get("audit_score"),
        },
        "branching_mode": branching_mode,
        "mutation_brief": mutation_brief,
        "fallback_draft": {
            "rationale": fallback_rationale,
            "target": fallback_target,
            "changes": list(_llm_fallback_changes(fallback_changes, mutation_brief)),
        },
    }
    return (
        "You are authoring a bounded harness-lab proposal.\n"
        "Return only JSON with keys: rationale, target, changes, backend_levers, no_lever_reason.\n"
        "target must be an object with keys: harness_component, expected_failure_mode, novelty_basis.\n"
        "changes must be an array of objects with keys: kind, mechanism, summary.\n"
        "backend_levers is optional. If present, it must be an object keyed by module name from: science_model, science_loss, science_eval, science_config, science_train.\n"
        "Each module value must be an object of scalar numeric lever values only.\n"
        "no_lever_reason is optional, but if target.harness_component is one of those backend modules and backend_levers is empty, provide a short evidence-based reason.\n"
        "When the proposal targets one of those backend modules, prefer using backend_levers over vague prose changes.\n"
        "If target.harness_component is one of those backend modules, returning empty backend_levers is discouraged.\n"
        "Prefer at least one small conservative lever move for the target module unless there is a strong evidence-based reason to avoid it.\n"
        "Only choose lever names and ranges that appear in the supplied backend_lever_catalog.\n"
        "If the mutation brief says wait, keep the move small: use at most two conservative lever nudges for the target module.\n"
        "When waiting, prefer defaults or nearby heuristic choices over aggressive jumps, and do not set levers for non-target modules.\n"
        "Good examples: science_model -> {hidden_dim: 160}; science_model -> {k_neighbors: 10}; science_eval -> {transfer_smoke_max_gap: 0.025}.\n"
        "Bad examples: setting many levers at once, changing non-target modules, or making large jumps far outside nearby defaults and choices.\n"
        "Keep the proposal concrete, short, and grounded in the supplied evidence.\n"
        "Do not mutate files or mention implementation details outside the proposal JSON.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _mutation_brief_state(memory_dir: Path) -> dict:
    brief_path = memory_dir / "mutation_brief.json"
    if not brief_path.exists():
        return {}
    brief = read_json(brief_path)
    if not isinstance(brief, dict):
        return {}
    target_module = str(brief.get("target_module", "")).strip()
    if target_module and target_module not in ALLOWED_BACKEND_MODULES:
        target_module = ""
    return {
        "recommended_action": str(brief.get("recommended_action", "")).strip() or "wait",
        "target_module": target_module,
        "summary": str(brief.get("summary", "")).strip(),
    }


def _mutation_brief_target_module(memory_dir: Path) -> str:
    return str(_mutation_brief_state(memory_dir).get("target_module", ""))


def _mutation_brief_change_items(target_module: str) -> tuple[dict, ...]:
    if not target_module:
        return ()
    return (
        {
            "kind": "mutation_brief_focus",
            "mechanism": target_module,
            "summary": f"Follow the current mutation brief by focusing this proposal on {target_module}.",
        },
    )


def _normalize_backend_levers(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}
    normalized: dict[str, dict[str, float | int]] = {}
    for module_name, lever_map in payload.items():
        module_key = str(module_name).strip()
        if module_key not in ALLOWED_BACKEND_MODULES or not isinstance(lever_map, dict):
            continue
        clean: dict[str, float | int] = {}
        for lever_name, value in lever_map.items():
            if isinstance(value, bool):
                continue
            if isinstance(value, int):
                clean[str(lever_name).strip()] = value
            elif isinstance(value, float):
                clean[str(lever_name).strip()] = float(value)
        if clean:
            normalized[module_key] = clean
    return normalized


def _soft_wait_backend_levers(backend_levers: dict, mutation_brief: dict) -> dict:
    if not backend_levers:
        return {}
    if str(mutation_brief.get("recommended_action", "")).strip() != "wait":
        return backend_levers
    target_module = str(mutation_brief.get("target_module", "")).strip()
    if target_module not in ALLOWED_BACKEND_MODULES:
        return {}
    module_levers = backend_levers.get(target_module, {})
    if not isinstance(module_levers, dict) or not module_levers:
        return {}
    catalog = _backend_lever_catalog().get(target_module, {})
    limited: dict[str, float | int] = {}
    for lever_name, value in module_levers.items():
        if lever_name not in catalog:
            continue
        limited[lever_name] = value
        if len(limited) >= 2:
            break
    return {target_module: limited} if limited else {}


def _normalize_llm_proposal_payload(payload: dict, fallback_target: dict, fallback_changes: tuple[dict, ...], fallback_rationale: str) -> tuple[str, dict, tuple[dict, ...], dict, str] | None:
    if not isinstance(payload, dict):
        return None
    rationale = str(payload.get("rationale", "")).strip()
    target_payload = payload.get("target", {})
    if not isinstance(target_payload, dict):
        target_payload = {}
    target = {
        "harness_component": str(target_payload.get("harness_component", fallback_target.get("harness_component", ""))).strip(),
        "expected_failure_mode": str(target_payload.get("expected_failure_mode", fallback_target.get("expected_failure_mode", ""))).strip(),
        "novelty_basis": str(target_payload.get("novelty_basis", fallback_target.get("novelty_basis", ""))).strip(),
    }
    changes: list[dict] = []
    for item in payload.get("changes", []):
        if not isinstance(item, dict):
            continue
        summary = str(item.get("summary", "")).strip()
        if not summary:
            continue
        kind = str(item.get("kind", "llm_proposal")).strip() or "llm_proposal"
        mechanism = str(item.get("mechanism", target["harness_component"])).strip() or target["harness_component"]
        changes.append({"kind": kind, "mechanism": mechanism, "summary": summary})
    if not rationale:
        return None
    if not target["harness_component"]:
        target["harness_component"] = str(fallback_target.get("harness_component", "")).strip()
    if not target["novelty_basis"]:
        target["novelty_basis"] = str(fallback_target.get("novelty_basis", "")).strip()
    if not changes:
        changes = list(fallback_changes)
    backend_levers = _normalize_backend_levers(payload.get("backend_levers", {}))
    no_lever_reason = str(payload.get("no_lever_reason", "")).strip()
    return rationale, target, tuple(changes[:8]), backend_levers, no_lever_reason


def _targeted_module_without_levers(target: dict, backend_levers: dict) -> str:
    module_name = str(target.get("harness_component", "")).strip()
    if module_name not in ALLOWED_BACKEND_MODULES:
        return ""
    module_values = backend_levers.get(module_name, {}) if isinstance(backend_levers, dict) else {}
    if isinstance(module_values, dict) and module_values:
        return ""
    return module_name


def _has_good_no_lever_reason(no_lever_reason: str) -> bool:
    return len(no_lever_reason.strip()) >= 24


def _llm_lever_retry_prompt(*, target_module: str) -> str:
    return (
        f"You targeted `{target_module}` but returned empty backend_levers.\n"
        "Choose one small conservative lever move for that target module using only the supplied catalog, "
        "or return a concrete evidence-based `no_lever_reason` explaining why even a small bounded nudge is unsafe or unhelpful right now.\n"
        "Do not leave both `backend_levers` and `no_lever_reason` empty."
    )


def _maybe_llm_author_proposal(
    *,
    candidate_root: Path,
    bootstrap_snapshot: dict,
    decision_bundle: dict,
    mutation_brief: dict,
    parent_diagnosis: dict,
    parent_summary: dict,
    branching_mode: str,
    fallback_target: dict,
    fallback_changes: tuple[dict, ...],
    fallback_rationale: str,
    fallback_backend_levers: dict,
) -> tuple[str, dict, tuple[dict, ...], dict, str, bool]:
    if str(os.environ.get("HARNESS_LAB_LLM_PROPOSAL_ENABLED", "")).strip().lower() not in {"1", "true", "yes"}:
        return fallback_rationale, fallback_target, fallback_changes, fallback_backend_levers, "", False
    payload = run_claude_json(
        _llm_proposal_prompt(
            bootstrap_snapshot=bootstrap_snapshot,
            decision_bundle=decision_bundle,
            mutation_brief=mutation_brief,
            parent_diagnosis=parent_diagnosis,
            parent_summary=parent_summary,
            branching_mode=branching_mode,
            fallback_target=fallback_target,
            fallback_changes=fallback_changes,
            fallback_rationale=fallback_rationale,
        ),
        cwd=candidate_root,
    )
    normalized = _normalize_llm_proposal_payload(payload or {}, fallback_target, fallback_changes, fallback_rationale)
    if not normalized:
        log.warning("proposal: claude fallback to heuristic (payload=%s)", "empty" if not payload else "invalid")
        return fallback_rationale, fallback_target, fallback_changes, fallback_backend_levers, "", False
    rationale, target, changes, backend_levers, no_lever_reason = normalized
    targeted_module = _targeted_module_without_levers(target, backend_levers)
    retry_used = False
    if targeted_module and not _has_good_no_lever_reason(no_lever_reason):
        retry_used = True
        retry_payload = run_claude_json(
            _llm_proposal_prompt(
                bootstrap_snapshot=bootstrap_snapshot,
                decision_bundle=decision_bundle,
                mutation_brief=mutation_brief,
                parent_diagnosis=parent_diagnosis,
                parent_summary=parent_summary,
                branching_mode=branching_mode,
                fallback_target=target,
                fallback_changes=changes,
                fallback_rationale=rationale,
            )
            + "\n\n"
            + _llm_lever_retry_prompt(target_module=targeted_module),
            cwd=candidate_root,
        )
        retry_normalized = _normalize_llm_proposal_payload(retry_payload or {}, target, changes, rationale)
        if retry_normalized:
            rationale, target, changes, backend_levers, no_lever_reason = retry_normalized
    backend_levers = _soft_wait_backend_levers(backend_levers, mutation_brief)
    log.info("proposal authored by claude")
    return rationale, target, changes, backend_levers, no_lever_reason, retry_used


def draft_proposal_for_candidate(
    candidates_dir: Path,
    candidate_id: str,
    *,
    parent_id: str | None = None,
) -> DraftProposal:
    index = build_candidate_index(candidates_dir)
    memory_dir = candidates_dir.parent / "memory"
    hardware_profile = read_hardware_profile(memory_dir)
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    budget = read_budget(memory_dir)
    diversity = read_diversity(memory_dir)
    external_review = read_external_review(memory_dir)
    synthesis = synthesize_parent_candidates(candidates_dir)
    dataset_id = choose_dataset_id(candidates_dir)
    dataset_record = get_dataset_record(memory_dir, dataset_id) if dataset_id else None
    chosen_parent, branching_mode = _choose_parent_for_branching(index, synthesis, budget, diversity)
    chosen_parent = parent_id or chosen_parent
    candidate_root = _candidate_root(candidates_dir, candidate_id)
    if not candidate_root.exists():
        create_candidate_workspace(candidates_dir, candidate_id, chosen_parent)
    decision_bundle_path = write_decision_bundle(
        candidates_dir,
        memory_dir,
        candidate_id,
        parent_id=chosen_parent,
        dataset_id=dataset_id,
        synthesis=synthesis,
    )
    bootstrap_path = write_bootstrap_snapshot(
        candidates_dir,
        memory_dir,
        candidate_id,
        parent_id=chosen_parent,
        dataset_id=dataset_id,
        synthesis=synthesis,
    )
    bootstrap_snapshot = read_json(bootstrap_path)
    decision_bundle = read_json(decision_bundle_path)
    mutation_brief = _mutation_brief_state(memory_dir)
    mutation_brief_target = str(mutation_brief.get("target_module", ""))

    if chosen_parent is None:
        mechanism = mutation_brief_target or "initial_harness"
        rationale = (
            f"Initial real backend candidate on dataset {dataset_id}."
            if dataset_id
            else "Initial real backend candidate with no prior parent available."
        )
        changes = (
            _mutation_brief_change_items(mutation_brief_target)
            + _policy_change_items(policy, mechanism)
            + _budget_change_items(budget, mechanism)
            + _external_review_change_items(external_review)
            + _hardware_guardrail_items(hardware_profile)
        )
        if str(policy.get("selection_mode", "")).strip() == "novelty_cycle_priority":
            changes += (
                {
                    "kind": "exploration_jump",
                    "mechanism": mechanism,
                    "summary": "Begin with a deliberately simple but real backend baseline before branching into richer candidate families.",
                },
            )
        target = {
            "harness_component": mechanism,
            "expected_failure_mode": "",
            "novelty_basis": "genesis real-backend baseline with no prior candidate lineage",
        }
        rationale, target, changes, backend_levers, no_lever_reason, llm_backend_lever_retry_used = _maybe_llm_author_proposal(
            candidate_root=candidate_root,
            bootstrap_snapshot=bootstrap_snapshot,
            parent_diagnosis={},
            parent_summary={},
            branching_mode="genesis",
            decision_bundle=decision_bundle,
            mutation_brief=mutation_brief,
            fallback_target=target,
            fallback_changes=changes,
            fallback_rationale=rationale,
            fallback_backend_levers={},
        )
        draft = DraftProposal(
            candidate_id=candidate_id,
            parent_id=None,
            dataset_id=dataset_id,
            status="candidate",
            rationale=rationale,
            target=target,
            changes=changes,
            backend_levers=backend_levers,
            no_lever_reason=no_lever_reason,
            llm_backend_lever_retry_used=llm_backend_lever_retry_used,
            memory_context={
                "parent_created_at": "",
                "reference_candidate_ids": [],
                "indexed_candidate_count": int(index.get("candidate_count", 0)),
                "failure_mode_counts": index.get("failure_mode_counts", {}),
                "dataset_context": dataset_record or {},
                "hardware_context": hardware_profile,
                "hindsight_summary": hindsight.get("summary", ""),
                "policy_context": policy,
                "budget_context": budget,
                "diversity_context": diversity,
                "external_review_context": external_review,
                "bootstrap_snapshot_path": str(bootstrap_path.relative_to(candidate_root)),
                "decision_bundle_path": str(decision_bundle_path.relative_to(candidate_root)),
                "branching_mode": "genesis",
                "mutation_brief_target": mutation_brief_target,
            },
        )
        write_json(candidate_root / "proposal.json", draft.to_dict())
        return draft

    parent_diagnosis = _load_diagnosis(candidates_dir, chosen_parent)
    parent_workspace = _load_workspace(candidates_dir, chosen_parent)
    parent_summary = next(
        (item for item in index["candidates"] if item["candidate_id"] == chosen_parent),
        {
            "candidate_id": chosen_parent,
            "diagnosis_mechanism": parent_diagnosis.get("mechanism", ""),
            "expected_failure_mode": "",
            "harness_component": "",
        },
    )
    mechanism = str(parent_diagnosis.get("mechanism", "")).strip() or str(parent_summary.get("diagnosis_mechanism", "")).strip()
    latest_summary = index.get("candidates", [])[-1] if index.get("candidates") else {}
    latest_mechanism = str(latest_summary.get("diagnosis_mechanism") or latest_summary.get("harness_component") or "").strip()
    changes = (
        _mutation_brief_change_items(mutation_brief_target)
        + _proposal_change_items(parent_diagnosis, parent_summary)
        + _hindsight_change_items(hindsight, mechanism)
        + _policy_change_items(policy, mechanism)
        + _budget_change_items(budget, mechanism)
        + _external_review_change_items(external_review)
        + _branching_mode_change_items(branching_mode, mechanism, latest_mechanism)
        + _diversity_change_items(diversity, mechanism, latest_mechanism)
        + _hardware_guardrail_items(hardware_profile)
    )
    failure_modes = [str(item) for item in parent_diagnosis.get("failure_modes", []) if str(item).strip()]
    counterfactuals = [str(item) for item in parent_diagnosis.get("counterfactuals", []) if str(item).strip()]

    rationale = str(parent_diagnosis.get("summary", "")).strip() or (f"Follow up on {chosen_parent} using indexed diagnosis memory.")
    if branching_mode == "force_broad_exploration":
        rationale = f"{rationale} Budget forced a broader jump away from the most recent exhausted line."
    elif branching_mode == "focus_promising":
        rationale = f"{rationale} Budget says to stay close to the most promising active line."
    target = {
        "harness_component": mutation_brief_target or mechanism or str(parent_summary.get("harness_component", "")).strip(),
        "expected_failure_mode": failure_modes[0] if failure_modes else str(parent_summary.get("expected_failure_mode", "")).strip(),
        "novelty_basis": _novelty_basis_from_memory(index, parent_summary, parent_diagnosis),
    }
    rationale, target, changes, backend_levers, no_lever_reason, llm_backend_lever_retry_used = _maybe_llm_author_proposal(
        candidate_root=candidate_root,
        bootstrap_snapshot=bootstrap_snapshot,
        mutation_brief=mutation_brief,
        parent_diagnosis=parent_diagnosis,
        parent_summary=parent_summary,
        branching_mode=branching_mode,
        decision_bundle=decision_bundle,
        fallback_target=target,
        fallback_changes=changes,
        fallback_rationale=rationale,
        fallback_backend_levers={},
    )
    draft = DraftProposal(
        candidate_id=candidate_id,
        parent_id=chosen_parent,
        dataset_id=dataset_id,
        status="candidate",
        rationale=rationale,
        target=target,
        changes=changes,
        backend_levers=backend_levers,
        no_lever_reason=no_lever_reason,
        llm_backend_lever_retry_used=llm_backend_lever_retry_used,
        memory_context={
            "parent_created_at": str(parent_workspace.get("created_at", "")),
            "reference_candidate_ids": [chosen_parent],
            "parent_failure_modes": failure_modes,
            "counterfactual_seeds": counterfactuals[:3],
            "hardware_context": hardware_profile,
            "hindsight_context": {
                "summary": hindsight.get("summary", ""),
                "policy_adjustments": hindsight.get("policy_adjustments", [])[:3],
                "over_explored_mechanisms": hindsight.get("over_explored_mechanisms", [])[:3],
                "under_explored_promising_mechanisms": hindsight.get("under_explored_promising_mechanisms", [])[:3],
                "over_explored_backend_fingerprints": hindsight.get("over_explored_backend_fingerprints", [])[:3],
                "under_explored_backend_fingerprints": hindsight.get("under_explored_backend_fingerprints", [])[:3],
            },
            "policy_context": policy,
            "budget_context": budget,
            "diversity_context": diversity,
            "external_review_context": {
                "status": external_review.get("status", ""),
                "trigger_reason": external_review.get("trigger_reason", ""),
                "reviewer": external_review.get("reviewer", ""),
                "lab_advice": external_review.get("lab_advice", [])[:3],
                "human_advice": external_review.get("human_advice", [])[:3],
            },
            "dataset_context": dataset_record or ({"dataset_id": dataset_id, "status": "missing"} if dataset_id else {}),
            "bootstrap_snapshot_path": str(bootstrap_path.relative_to(candidate_root)),
            "decision_bundle_path": str(decision_bundle_path.relative_to(candidate_root)),
            "branching_mode": branching_mode,
            "parent_selection": synthesis.get("ranked_parents", [])[:3],
            "mutation_brief_target": mutation_brief_target,
        },
    )

    existing = _load_existing_proposal(candidates_dir, candidate_id)
    output = dict(existing)
    output.update(draft.to_dict())
    write_json(candidate_root / "proposal.json", output)
    return draft
