from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.budget import read_budget
from harness_lab.datasets import choose_best_prepared_dataset, get_dataset_record
from harness_lab.diversity import read_diversity
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight
from harness_lab.memory import build_candidate_index, read_json
from harness_lab.policy import read_policy
from harness_lab.synthesis import synthesize_parent_candidates
from harness_lab.workspace import create_candidate_workspace, write_json


@dataclass(frozen=True)
class DraftProposal:
    candidate_id: str
    parent_id: str | None
    dataset_id: str
    status: str
    rationale: str
    target: dict
    changes: tuple[dict, ...]
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
            "memory_context": self.memory_context,
        }


def _candidate_root(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id


def _load_diagnosis(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(_candidate_root(candidates_dir, candidate_id) / "diagnosis" / "summary.json")


def _load_workspace(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(_candidate_root(candidates_dir, candidate_id) / "workspace.json")


def _load_existing_proposal(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(_candidate_root(candidates_dir, candidate_id) / "proposal.json")


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
    synthesis = synthesize_parent_candidates(candidates_dir)
    dataset_id = choose_dataset_id(candidates_dir)
    dataset_record = get_dataset_record(memory_dir, dataset_id) if dataset_id else None
    chosen_parent, branching_mode = _choose_parent_for_branching(index, synthesis, budget, diversity)
    chosen_parent = parent_id or chosen_parent
    candidate_root = _candidate_root(candidates_dir, candidate_id)
    if not candidate_root.exists():
        create_candidate_workspace(candidates_dir, candidate_id, chosen_parent)

    if chosen_parent is None:
        mechanism = "initial_harness"
        rationale = (
            f"Initial real backend candidate on dataset {dataset_id}."
            if dataset_id
            else "Initial real backend candidate with no prior parent available."
        )
        changes = (
            _policy_change_items(policy, mechanism)
            + _budget_change_items(budget, mechanism)
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
        draft = DraftProposal(
            candidate_id=candidate_id,
            parent_id=None,
            dataset_id=dataset_id,
            status="candidate",
            rationale=rationale,
            target={
                "harness_component": mechanism,
                "expected_failure_mode": "",
                "novelty_basis": "genesis real-backend baseline with no prior candidate lineage",
            },
            changes=changes,
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
                "branching_mode": "genesis",
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
        _proposal_change_items(parent_diagnosis, parent_summary)
        + _hindsight_change_items(hindsight, mechanism)
        + _policy_change_items(policy, mechanism)
        + _budget_change_items(budget, mechanism)
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
    draft = DraftProposal(
        candidate_id=candidate_id,
        parent_id=chosen_parent,
        dataset_id=dataset_id,
        status="candidate",
        rationale=rationale,
        target={
            "harness_component": mechanism or str(parent_summary.get("harness_component", "")).strip(),
            "expected_failure_mode": failure_modes[0] if failure_modes else str(parent_summary.get("expected_failure_mode", "")).strip(),
            "novelty_basis": _novelty_basis_from_memory(index, parent_summary, parent_diagnosis),
        },
        changes=changes,
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
            },
            "policy_context": policy,
            "budget_context": budget,
            "diversity_context": diversity,
            "dataset_context": dataset_record or ({"dataset_id": dataset_id, "status": "missing"} if dataset_id else {}),
            "branching_mode": branching_mode,
            "parent_selection": synthesis.get("ranked_parents", [])[:3],
        },
    )

    existing = _load_existing_proposal(candidates_dir, candidate_id)
    output = dict(existing)
    output.update(draft.to_dict())
    write_json(candidate_root / "proposal.json", output)
    return draft
