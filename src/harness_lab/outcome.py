from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.memory import read_json
from harness_lab.workspace import write_json

VALID_OUTCOME_STATUS = {"pending", "complete"}


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
