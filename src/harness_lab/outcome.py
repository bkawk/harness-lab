from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.memory import read_json
from harness_lab.workspace import write_json

VALID_OUTCOME_STATUS = {"pending", "complete", "keeper_pending_review"}


@dataclass(frozen=True)
class CandidateOutcome:
    candidate_id: str
    status: str
    outcome_label: str
    benchmark: dict
    audit: dict
    observed_failure_modes: tuple[str, ...]
    evidence: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "status": self.status,
            "outcome_label": self.outcome_label,
            "benchmark": self.benchmark,
            "audit": self.audit,
            "observed_failure_modes": list(self.observed_failure_modes),
            "evidence": list(self.evidence),
        }


MAX_KEEPER_CHANGED_FILES = 10


def _proposal_backend_lever_count(proposal: dict) -> int:
    backend_levers = proposal.get("backend_levers", {})
    if not isinstance(backend_levers, dict):
        return 0
    total = 0
    for module_values in backend_levers.values():
        if isinstance(module_values, dict):
            total += len(module_values)
    return total


def _proposal_is_bounded_lever_candidate(proposal: dict) -> bool:
    changes = proposal.get("changes", [])
    if not isinstance(changes, list) or not changes:
        return False
    lever_count = _proposal_backend_lever_count(proposal)
    if lever_count <= 0 or lever_count > 4:
        return False
    return all(str(item.get("kind", "")).strip() == "backend_lever" for item in changes if isinstance(item, dict))


def validate_keeper_candidate(candidates_dir: Path, candidate_id: str) -> dict:
    """Gate keeper candidates through a minimal-change review before acceptance."""
    candidate_dir = candidates_dir / candidate_id
    outcome = read_json(candidate_dir / "outcome" / "result.json")
    proposal = read_json(candidate_dir / "proposal.json") if (candidate_dir / "proposal.json").exists() else {}
    diagnosis = read_json(candidate_dir / "diagnosis" / "summary.json") if (candidate_dir / "diagnosis" / "summary.json").exists() else {}
    patch_summary = read_json(candidate_dir / "patches" / "summary.json") if (candidate_dir / "patches" / "summary.json").exists() else {}

    changed_file_count = int(patch_summary.get("changed_file_count", 0) or 0)
    bounded_lever_candidate = _proposal_is_bounded_lever_candidate(proposal)
    lever_count = _proposal_backend_lever_count(proposal)
    severity = str(diagnosis.get("severity", "unknown"))
    parent_id = proposal.get("parent_id") or outcome.get("parent_id")
    parent_failures = set()
    if parent_id:
        parent_diagnosis_path = candidates_dir / str(parent_id) / "diagnosis" / "summary.json"
        if parent_diagnosis_path.exists():
            parent_diag = read_json(parent_diagnosis_path)
            parent_failures = {str(f) for f in parent_diag.get("failure_modes", []) if str(f).strip()}

    current_failures = {str(f) for f in outcome.get("observed_failure_modes", []) if str(f).strip()}

    checks = []

    # Check 1: has actual changes
    has_changes = changed_file_count > 0 or lever_count > 0
    checks.append(
        {
            "check": "has_changes",
            "passed": has_changes,
            "detail": f"changed_file_count={changed_file_count}, backend_lever_count={lever_count}",
        }
    )

    # Check 2: not too many changes
    bounded_changes = changed_file_count <= MAX_KEEPER_CHANGED_FILES or bounded_lever_candidate
    checks.append(
        {
            "check": "bounded_changes",
            "passed": bounded_changes,
            "detail": (
                f"max={MAX_KEEPER_CHANGED_FILES}, changed_file_count={changed_file_count}"
                if not bounded_lever_candidate
                else f"lever_based_candidate={lever_count} levers"
            ),
        }
    )

    # Check 3: no critical severity
    not_critical = severity != "critical"
    checks.append({"check": "not_critical_severity", "passed": not_critical, "detail": f"severity={severity}"})

    # Check 4: failure modes improved vs parent
    if parent_failures and current_failures:
        improved = current_failures != parent_failures
    else:
        improved = True
    checks.append({"check": "failure_modes_improved", "passed": improved, "detail": f"parent_failures={len(parent_failures)}, current={len(current_failures)}"})

    approved = all(c["passed"] for c in checks)
    rejection_reason = None
    if not approved:
        failed = [c["check"] for c in checks if not c["passed"]]
        rejection_reason = f"Keeper review failed: {', '.join(failed)}"

    result = {
        "candidate_id": candidate_id,
        "approved": approved,
        "checks": checks,
        "rejection_reason": rejection_reason,
    }

    # Write the review artifact
    review_path = candidate_dir / "outcome" / "keeper_review.json"
    from harness_lab.workspace import write_json as _write_json
    _write_json(review_path, result)

    return result


def outcome_path_for_candidate(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id / "outcome" / "result.json"


def update_outcome_for_candidate(
    candidates_dir: Path,
    candidate_id: str,
    *,
    status: str | None = None,
    outcome_label: str | None = None,
    benchmark_score: float | None = None,
    benchmark_summary: str | None = None,
    audit_score: float | None = None,
    audit_summary: str | None = None,
    observed_failure_modes: list[str] | None = None,
    evidence: list[str] | None = None,
) -> CandidateOutcome:
    path = outcome_path_for_candidate(candidates_dir, candidate_id)
    if not path.exists():
        raise FileNotFoundError(f"Outcome file not found: {path}")

    payload = read_json(path)
    next_status = status if status is not None else str(payload.get("status", "pending"))
    if next_status not in VALID_OUTCOME_STATUS:
        raise ValueError(f"Unsupported outcome status: {next_status}")

    current_benchmark = dict(payload.get("benchmark", {}))
    current_audit = dict(payload.get("audit", {}))
    if benchmark_score is not None:
        current_benchmark["score"] = benchmark_score
    if benchmark_summary is not None:
        current_benchmark["summary"] = benchmark_summary
    if audit_score is not None:
        current_audit["score"] = audit_score
    if audit_summary is not None:
        current_audit["summary"] = audit_summary

    updated = CandidateOutcome(
        candidate_id=str(payload.get("candidate_id", candidate_id)),
        status=next_status,
        outcome_label=outcome_label if outcome_label is not None else str(payload.get("outcome_label", "")),
        benchmark=current_benchmark,
        audit=current_audit,
        observed_failure_modes=tuple(
            str(item) for item in (observed_failure_modes if observed_failure_modes is not None else payload.get("observed_failure_modes", []))
        ),
        evidence=tuple(str(item) for item in (evidence if evidence is not None else payload.get("evidence", []))),
    )

    output = dict(payload)
    output.update(updated.to_dict())
    write_json(path, output)
    return updated
