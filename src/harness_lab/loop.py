from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.diagnosis import reconcile_diagnosis_from_outcome
from harness_lab.evidence import capture_candidate_evidence
from harness_lab.execution import plan_execution_for_candidate
from harness_lab.hardware import refresh_hardware_profile
from harness_lab.outcome import validate_keeper_candidate, update_outcome_for_candidate as _update_outcome
from harness_lab.proposal import draft_proposal_for_candidate
from harness_lab.runner import run_candidate
from harness_lab.synthesis import refresh_memory_artifacts


@dataclass(frozen=True)
class LoopResult:
    candidate_id: str
    parent_id: str | None
    proposal_status: str
    execution_status: str
    outcome_status: str
    diagnosis_status: str
    top_parent_id: str | None


def advance_candidate_loop(
    repo_dir: Path,
    candidates_dir: Path,
    memory_dir: Path,
    candidate_id: str,
    *,
    parent_id: str | None = None,
    outcome_label: str = "simulated_pending",
    benchmark_score: float | None = None,
    benchmark_summary: str | None = None,
    audit_score: float | None = None,
    audit_summary: str | None = None,
    observed_failure_modes: list[str] | None = None,
    evidence: list[str] | None = None,
    finalize_outcome: bool = False,
    simulate_outcome: bool = False,
    runner_backend: str = "simulated",
) -> LoopResult:
    memory_dir.mkdir(parents=True, exist_ok=True)
    refresh_hardware_profile(memory_dir)
    proposal = draft_proposal_for_candidate(candidates_dir, candidate_id, parent_id=parent_id)
    capture_candidate_evidence(repo_dir, candidates_dir, candidate_id, proposal.parent_id)
    plan = plan_execution_for_candidate(candidates_dir, candidate_id)

    outcome_status = "pending"
    diagnosis_status = "in_progress"
    if finalize_outcome:
        if simulate_outcome:
            outcome = run_candidate(repo_dir, candidates_dir, candidate_id, backend=runner_backend).outcome
        else:
            outcome = _update_outcome(
                candidates_dir,
                candidate_id,
                status="complete",
                outcome_label=outcome_label,
                benchmark_score=benchmark_score,
                benchmark_summary=benchmark_summary,
                audit_score=audit_score,
                audit_summary=audit_summary,
                observed_failure_modes=observed_failure_modes,
                evidence=evidence,
            )
        diagnosis = reconcile_diagnosis_from_outcome(candidates_dir, candidate_id)

        # --- Import 3: keeper completion discipline ---
        if outcome.outcome_label == "keeper":
            review = validate_keeper_candidate(candidates_dir, candidate_id)
            if not review["approved"]:
                outcome = _update_outcome(
                    candidates_dir,
                    candidate_id,
                    status="complete",
                    outcome_label="dead_end",
                    evidence=list(outcome.evidence) + [f"completion_discipline:rejected:{review['rejection_reason']}"],
                )
                diagnosis = reconcile_diagnosis_from_outcome(candidates_dir, candidate_id)

        outcome_status = outcome.status
        diagnosis_status = diagnosis.status

    synthesis = refresh_memory_artifacts(candidates_dir, memory_dir)
    return LoopResult(
        candidate_id=candidate_id,
        parent_id=proposal.parent_id,
        proposal_status=proposal.status,
        execution_status=plan.status,
        outcome_status=outcome_status,
        diagnosis_status=diagnosis_status,
        top_parent_id=synthesis.get("top_parent_id"),
    )
