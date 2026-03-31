from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.budget import read_budget, write_budget
from harness_lab.diversity import write_diversity
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight, write_hindsight
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
    policy_text = " ".join(str(item) for item in hindsight.get("policy_adjustments", []))

    cooldown_multiplier = float(policy.get("cooldown_multiplier", 1.0) or 1.0)
    underexplored_bonus = int(policy.get("underexplored_bonus", 20) or 20)
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
