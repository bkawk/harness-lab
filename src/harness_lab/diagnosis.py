from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.memory import read_json
from harness_lab.workspace import write_json

VALID_DIAGNOSIS_STATUS = {"empty", "in_progress", "complete"}
VALID_SEVERITY = {"unknown", "low", "medium", "high", "critical"}


@dataclass(frozen=True)
class DiagnosisUpdate:
    candidate_id: str
    status: str
    summary: str
    severity: str
    mechanism: str
    failure_modes: tuple[str, ...]
    evidence: tuple[str, ...]
    counterfactuals: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "status": self.status,
            "summary": self.summary,
            "severity": self.severity,
            "mechanism": self.mechanism,
            "failure_modes": list(self.failure_modes),
            "evidence": list(self.evidence),
            "counterfactuals": list(self.counterfactuals),
        }


def diagnosis_path_for_candidate(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id / "diagnosis" / "summary.json"


def update_diagnosis(
    candidates_dir: Path,
    candidate_id: str,
    *,
    status: str | None = None,
    summary: str | None = None,
    severity: str | None = None,
    mechanism: str | None = None,
    failure_modes: list[str] | None = None,
    evidence: list[str] | None = None,
    counterfactuals: list[str] | None = None,
) -> DiagnosisUpdate:
    path = diagnosis_path_for_candidate(candidates_dir, candidate_id)
    if not path.exists():
        raise FileNotFoundError(f"Diagnosis file not found: {path}")

    payload = read_json(path)
    next_status = status if status is not None else str(payload.get("status", "empty"))
    next_summary = summary if summary is not None else str(payload.get("summary", ""))
    next_severity = severity if severity is not None else str(payload.get("severity", "unknown"))
    next_mechanism = mechanism if mechanism is not None else str(payload.get("mechanism", ""))
    next_failure_modes = tuple(failure_modes if failure_modes is not None else payload.get("failure_modes", []))
    next_evidence = tuple(evidence if evidence is not None else payload.get("evidence", []))
    next_counterfactuals = tuple(counterfactuals if counterfactuals is not None else payload.get("counterfactuals", []))

    if next_status not in VALID_DIAGNOSIS_STATUS:
        raise ValueError(f"Unsupported diagnosis status: {next_status}")
    if next_severity not in VALID_SEVERITY:
        raise ValueError(f"Unsupported severity: {next_severity}")

    updated = DiagnosisUpdate(
        candidate_id=str(payload.get("candidate_id", candidate_id)),
        status=next_status,
        summary=next_summary,
        severity=next_severity,
        mechanism=next_mechanism,
        failure_modes=tuple(str(item) for item in next_failure_modes),
        evidence=tuple(str(item) for item in next_evidence),
        counterfactuals=tuple(str(item) for item in next_counterfactuals),
    )
    output_payload = dict(payload)
    output_payload.update(updated.to_dict())
    write_json(path, output_payload)
    return updated


def reconcile_diagnosis_from_outcome(candidates_dir: Path, candidate_id: str) -> DiagnosisUpdate:
    diagnosis_path = diagnosis_path_for_candidate(candidates_dir, candidate_id)
    outcome_path = candidates_dir / candidate_id / "outcome" / "result.json"
    proposal_path = candidates_dir / candidate_id / "proposal.json"
    if not diagnosis_path.exists():
        raise FileNotFoundError(f"Diagnosis file not found: {diagnosis_path}")
    if not outcome_path.exists():
        raise FileNotFoundError(f"Outcome file not found: {outcome_path}")

    diagnosis = read_json(diagnosis_path)
    outcome = read_json(outcome_path)
    proposal = read_json(proposal_path) if proposal_path.exists() else {}
    target = proposal.get("target", {})

    outcome_label = str(outcome.get("outcome_label", "")).strip()
    benchmark = outcome.get("benchmark", {})
    audit = outcome.get("audit", {})
    observed_failure_modes = [str(item).strip() for item in outcome.get("observed_failure_modes", []) if str(item).strip()]
    evidence = [str(item).strip() for item in outcome.get("evidence", []) if str(item).strip()]
    benchmark_summary = str(benchmark.get("summary", "")).strip()
    audit_summary = str(audit.get("summary", "")).strip()

    severity = "medium"
    if outcome_label in {"train_error", "audit_blocked"}:
        severity = "high"
    elif outcome_label in {"keeper", "improved"}:
        severity = "low"

    mechanism = (
        str(target.get("harness_component", "")).strip()
        or str(diagnosis.get("mechanism", "")).strip()
    )

    summary_parts = []
    if outcome_label:
        summary_parts.append(f"Outcome {outcome_label}.")
    if benchmark_summary:
        summary_parts.append(benchmark_summary)
    if audit_summary:
        summary_parts.append(audit_summary)
    summary = " ".join(summary_parts).strip() or str(diagnosis.get("summary", "")).strip()

    counterfactuals = list(diagnosis.get("counterfactuals", []))
    if outcome_label in {"dead_end", "audit_blocked", "train_error"} and mechanism:
        counterfactuals = counterfactuals or [f"Revise {mechanism} with a smaller or better-instrumented follow-up."]

    return update_diagnosis(
        candidates_dir,
        candidate_id,
        status="complete" if str(outcome.get("status", "")) == "complete" else str(diagnosis.get("status", "in_progress")),
        summary=summary,
        severity=severity,
        mechanism=mechanism,
        failure_modes=observed_failure_modes or list(diagnosis.get("failure_modes", [])),
        evidence=evidence or list(diagnosis.get("evidence", [])),
        counterfactuals=[str(item) for item in counterfactuals if str(item).strip()],
    )
