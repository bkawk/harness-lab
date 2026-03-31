from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from harness_lab.budget import read_budget, write_budget
from harness_lab.diversity import write_diversity
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight, write_hindsight
from harness_lab.llm import run_claude_json
from harness_lab.memory import build_candidate_index, write_candidate_index, write_science_summary
from harness_lab.policy import read_policy, write_policy
from harness_lab.workspace import write_json

SEVERITY_SCORES = {
    "unknown": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


@dataclass(frozen=True)
class ParentCandidateScore:
    candidate_id: str
    total_score: int
    reasons: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "total_score": self.total_score,
            "reasons": list(self.reasons),
        }


def _llm_parent_prompt(index: dict, ranked: list[ParentCandidateScore], hindsight: dict, policy: dict, budget: dict, hardware_profile: dict) -> str:
    summary_map = {
        str(item.get("candidate_id", "")): item
        for item in index.get("candidates", [])
        if str(item.get("candidate_id", "")).strip()
    }
    compact_ranked = []
    for item in ranked[:8]:
        summary = summary_map.get(item.candidate_id, {})
        compact_ranked.append(
            {
                "candidate_id": item.candidate_id,
                "heuristic_score": item.total_score,
                "heuristic_reasons": list(item.reasons),
                "outcome_label": summary.get("outcome_label", ""),
                "diagnosis_mechanism": summary.get("diagnosis_mechanism", ""),
                "failure_modes": summary.get("failure_modes", []),
                "backend_fingerprints": summary.get("backend_fingerprints", []),
                "benchmark_score": summary.get("benchmark_score"),
                "audit_score": summary.get("audit_score"),
            }
        )
    payload = {
        "candidate_count": index.get("candidate_count", 0),
        "ranked_candidates": compact_ranked,
        "hindsight_summary": hindsight.get("summary", ""),
        "policy_summary": policy.get("summary", ""),
        "budget_summary": budget.get("summary", ""),
        "hardware_summary": {
            "environment_hint": hardware_profile.get("environment_hint", ""),
            "cpu_count": hardware_profile.get("cpu_count"),
            "memory_gb_estimate": hardware_profile.get("memory_gb_estimate"),
        },
    }
    return (
        "You are choosing the next parent candidate for harness-lab.\n"
        "Return only JSON with keys: top_parent_id, reasoning, candidate_adjustments.\n"
        "top_parent_id must be one of the provided candidate ids.\n"
        "candidate_adjustments must be an array of objects with keys: candidate_id, score_delta, reason.\n"
        "Keep the result grounded in the supplied candidate evidence.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _apply_llm_parent_selection(
    index: dict,
    ranked: list[ParentCandidateScore],
    hindsight: dict,
    policy: dict,
    budget: dict,
    hardware_profile: dict,
    *,
    cwd: Path,
) -> tuple[list[ParentCandidateScore], dict]:
    if str(os.environ.get("HARNESS_LAB_LLM_PARENT_SELECTION_ENABLED", "")).strip().lower() not in {"1", "true", "yes"}:
        return ranked, {}
    if not ranked:
        return ranked, {}
    payload = run_claude_json(
        _llm_parent_prompt(index, ranked, hindsight, policy, budget, hardware_profile),
        cwd=cwd,
    )
    if not isinstance(payload, dict):
        return ranked, {}
    top_parent_id = str(payload.get("top_parent_id", "")).strip()
    valid_ids = {item.candidate_id for item in ranked}
    if top_parent_id not in valid_ids:
        return ranked, {}

    adjustments: dict[str, tuple[int, str]] = {}
    for item in payload.get("candidate_adjustments", []):
        if not isinstance(item, dict):
            continue
        candidate_id = str(item.get("candidate_id", "")).strip()
        if candidate_id not in valid_ids:
            continue
        try:
            score_delta = int(item.get("score_delta", 0) or 0)
        except (TypeError, ValueError):
            score_delta = 0
        reason = str(item.get("reason", "")).strip()
        adjustments[candidate_id] = (score_delta, reason)

    revised: list[ParentCandidateScore] = []
    for item in ranked:
        delta, reason = adjustments.get(item.candidate_id, (0, ""))
        reasons = list(item.reasons)
        total = item.total_score + delta
        if delta:
            reasons.append(f"llm_parent_delta={delta}")
        if reason:
            reasons.append(f"llm_parent_reason:{reason}")
        if item.candidate_id == top_parent_id:
            total += 1000
            reasons.append("llm_parent_selected=1000")
        revised.append(
            ParentCandidateScore(
                candidate_id=item.candidate_id,
                total_score=total,
                reasons=tuple(reasons),
            )
        )
    revised.sort(key=lambda item: (-item.total_score, item.candidate_id))
    return revised, {
        "reviewer": "claude",
        "top_parent_id": top_parent_id,
        "reasoning": str(payload.get("reasoning", "")).strip(),
        "candidate_adjustments": [
            {
                "candidate_id": candidate_id,
                "score_delta": delta,
                "reason": reason,
            }
            for candidate_id, (delta, reason) in adjustments.items()
        ],
    }


def score_parent_candidate(summary: dict) -> ParentCandidateScore:
    score = 0
    reasons: list[str] = []

    if summary.get("proposal_status") == "draft" and summary.get("diagnosis_status") == "empty":
        return ParentCandidateScore(
            candidate_id=str(summary["candidate_id"]),
            total_score=-100,
            reasons=("exclude_empty_draft=-100",),
        )

    if summary.get("diagnosis_status") == "complete":
        score += 40
        reasons.append("diagnosis_complete=40")
    elif summary.get("diagnosis_status") == "in_progress":
        score += 10
        reasons.append("diagnosis_in_progress=10")

    severity = str(summary.get("diagnosis_severity", "unknown"))
    severity_score = SEVERITY_SCORES.get(severity, 0) * 10
    if severity_score:
        score += severity_score
        reasons.append(f"severity_{severity}={severity_score}")

    failure_modes = summary.get("failure_modes", [])
    failure_mode_score = min(len(failure_modes), 3) * 5
    if failure_mode_score:
        score += failure_mode_score
        reasons.append(f"failure_modes={failure_mode_score}")

    if summary.get("diagnosis_summary"):
        score += 10
        reasons.append("causal_summary=10")

    if summary.get("diagnosis_mechanism"):
        score += 10
        reasons.append("mechanism_present=10")

    if summary.get("parent_id"):
        score += 5
        reasons.append("lineage_context=5")

    return ParentCandidateScore(
        candidate_id=str(summary["candidate_id"]),
        total_score=score,
        reasons=tuple(reasons),
    )


def _apply_hardware_preference(score: ParentCandidateScore, summary: dict, hardware_profile: dict) -> ParentCandidateScore:
    total = score.total_score
    reasons = list(score.reasons)
    environment_hint = str(hardware_profile.get("environment_hint", "")).strip()
    cpu_count = hardware_profile.get("cpu_count")
    memory_gb = hardware_profile.get("memory_gb_estimate")

    constrained = (
        environment_hint == "local_macos"
        or (isinstance(cpu_count, int) and cpu_count > 0 and cpu_count <= 4)
        or (isinstance(memory_gb, (int, float)) and memory_gb <= 8)
    )

    if constrained:
        if summary.get("outcome_label") == "dead_end":
            total -= 10
            reasons.append("constrained_penalty_dead_end=-10")
        if summary.get("hardware_environment") == environment_hint and summary.get("outcome_label") == "keeper":
            total += 10
            reasons.append("constrained_reward_same_env_keeper=10")
    else:
        if summary.get("outcome_label") == "audit_blocked":
            total += 8
            reasons.append("roomier_reward_audit_blocked=8")
        if summary.get("diagnosis_severity") == "high":
            total += 5
            reasons.append("roomier_reward_harder_case=5")

    return ParentCandidateScore(
        candidate_id=score.candidate_id,
        total_score=total,
        reasons=tuple(reasons),
    )


def _apply_hindsight_preference(score: ParentCandidateScore, summary: dict, hindsight: dict, policy: dict, budget: dict) -> ParentCandidateScore:
    total = score.total_score
    reasons = list(score.reasons)
    mechanism = str(summary.get("diagnosis_mechanism") or summary.get("harness_component") or "").strip()
    if not mechanism:
        return score

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
    policy_text = " ".join(str(item) for item in hindsight.get("policy_adjustments", []))
    backend_fingerprints = {
        str(item).strip()
        for item in summary.get("backend_fingerprints", [])
        if str(item).strip()
    }

    cooldown_multiplier = float(policy.get("cooldown_multiplier", 1.0) or 1.0)
    underexplored_bonus = int(policy.get("underexplored_bonus", 20) or 20)
    backend_fingerprint_bonus = int(policy.get("backend_fingerprint_bonus", 10) or 10)
    backend_fingerprint_cooldown = int(policy.get("backend_fingerprint_cooldown", 12) or 12)
    budget_items = {
        str(item.get("mechanism", "")).strip(): item
        for item in budget.get("mechanism_budgets", [])
        if str(item.get("mechanism", "")).strip()
    }

    if mechanism in over_explored:
        penalty = int(round(20 * cooldown_multiplier))
        total -= penalty
        reasons.append(f"hindsight_over_explored=-{penalty}")
    if mechanism in under_explored:
        total += underexplored_bonus
        reasons.append(f"hindsight_under_explored={underexplored_bonus}")
    matched_under_backend = sorted(backend_fingerprints & under_backend)
    if matched_under_backend:
        bonus = backend_fingerprint_bonus * len(matched_under_backend)
        total += bonus
        reasons.append(f"backend_fingerprint_under_explored={bonus}")
    matched_over_backend = sorted(backend_fingerprints & over_backend)
    if matched_over_backend:
        penalty = backend_fingerprint_cooldown * len(matched_over_backend)
        total -= penalty
        reasons.append(f"backend_fingerprint_over_explored=-{penalty}")
    if "transfer stability" in policy_text.lower() and summary.get("outcome_label") == "audit_blocked":
        total += 12
        reasons.append("hindsight_transfer_stability=12")
    if "train_error" in policy_text and summary.get("outcome_label") == "train_error":
        total -= 12
        reasons.append("hindsight_train_error_cooldown=-12")
    mechanism_budget = budget_items.get(mechanism)
    if mechanism_budget:
        remaining = int(mechanism_budget.get("remaining_followups", 0) or 0)
        if bool(mechanism_budget.get("exhausted")):
            total -= 40
            reasons.append("budget_exhausted=-40")
        elif remaining >= 2:
            total += 8
            reasons.append("budget_headroom=8")
    if str(budget.get("exploration_mode", "")) == "force_broad_exploration" and mechanism in over_explored:
        total -= 15
        reasons.append("budget_force_broad_exploration=-15")

    return ParentCandidateScore(
        candidate_id=score.candidate_id,
        total_score=total,
        reasons=tuple(reasons),
    )


def synthesize_parent_candidates(candidates_dir: Path, output_path: Path | None = None) -> dict:
    index = build_candidate_index(candidates_dir)
    memory_dir = candidates_dir.parent / "memory"
    hardware_profile = read_hardware_profile(memory_dir)
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    budget = read_budget(memory_dir)
    ranked = [
        _apply_hindsight_preference(
            _apply_hardware_preference(score_parent_candidate(summary), summary, hardware_profile),
            summary,
            hindsight,
            policy,
            budget,
        )
        for summary in index["candidates"]
    ]
    ranked.sort(key=lambda item: (-item.total_score, item.candidate_id))
    ranked, llm_parent_selection = _apply_llm_parent_selection(
        index,
        ranked,
        hindsight,
        policy,
        budget,
        hardware_profile,
        cwd=candidates_dir.parent.parent,
    )
    viable = [item for item in ranked if item.total_score >= 0]

    payload = {
        "candidate_count": index["candidate_count"],
        "hardware_context": hardware_profile,
        "hindsight_summary": hindsight.get("summary", ""),
        "policy_summary": policy.get("summary", ""),
        "budget_summary": budget.get("summary", ""),
        "top_parent_id": viable[0].candidate_id if viable else None,
        "ranked_parents": [item.to_dict() for item in viable],
        "excluded_candidates": [item.to_dict() for item in ranked if item.total_score < 0],
        "failure_mode_counts": index["failure_mode_counts"],
        "diagnosis_mechanism_counts": index["diagnosis_mechanism_counts"],
        "diagnosis_severity_counts": index["diagnosis_severity_counts"],
        "llm_parent_selection": llm_parent_selection,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(output_path, payload)
    return payload


def refresh_memory_artifacts(candidates_dir: Path, memory_dir: Path) -> dict:
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_candidate_index(candidates_dir, memory_dir / "candidate_index.json")
    write_science_summary(candidates_dir, memory_dir / "science_summary.json")
    write_hindsight(candidates_dir, memory_dir / "hindsight.json")
    write_policy(candidates_dir, memory_dir, memory_dir / "policy.json")
    write_budget(memory_dir, memory_dir / "budget.json")
    write_diversity(candidates_dir, memory_dir / "diversity.json")
    synthesize_payload = synthesize_parent_candidates(candidates_dir, memory_dir / "parent_synthesis.json")
    return synthesize_payload
