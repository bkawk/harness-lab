from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("harness_lab.diagnosis")

from harness_lab.llm import run_claude_json
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


def _safe_read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = read_json(path)
    return payload if isinstance(payload, dict) else {}


def _safe_read_text(path: Path, limit: int = 4000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[-limit:]


def _heuristic_reconciled_fields(diagnosis: dict, outcome: dict, target: dict) -> dict:
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

    return {
        "status": "complete" if str(outcome.get("status", "")) == "complete" else str(diagnosis.get("status", "in_progress")),
        "summary": summary,
        "severity": severity,
        "mechanism": mechanism,
        "failure_modes": observed_failure_modes or list(diagnosis.get("failure_modes", [])),
        "evidence": evidence or list(diagnosis.get("evidence", [])),
        "counterfactuals": [str(item) for item in counterfactuals if str(item).strip()],
    }


def _llm_diagnosis_prompt(candidate_id: str, proposal: dict, outcome: dict, heuristic_fields: dict, traces: dict, parent_diagnosis: dict | None = None) -> str:
    payload = {
        "candidate_id": candidate_id,
        "proposal": {
            "rationale": proposal.get("rationale", ""),
            "target": proposal.get("target", {}),
            "changes": proposal.get("changes", [])[:8],
        },
        "outcome": outcome,
        "heuristic_fallback": heuristic_fields,
        "traces": traces,
    }
    if parent_diagnosis:
        payload["parent_diagnosis"] = {
            "summary": parent_diagnosis.get("summary", ""),
            "severity": parent_diagnosis.get("severity", ""),
            "mechanism": parent_diagnosis.get("mechanism", ""),
            "failure_modes": parent_diagnosis.get("failure_modes", []),
            "counterfactuals": parent_diagnosis.get("counterfactuals", [])[:5],
        }
    return (
        "You are reconciling a harness-lab diagnosis from outcome evidence.\n"
        "Return only JSON with keys: summary, severity, mechanism, failure_modes, evidence, counterfactuals.\n"
        "severity must be one of: unknown, low, medium, high, critical.\n"
        "failure_modes, evidence, and counterfactuals must be arrays of strings.\n"
        "Keep the diagnosis grounded in the provided proposal, outcome, and traces.\n"
        "If parent_diagnosis is provided, compare this candidate's outcome against the parent "
        "and note whether it improved, regressed, or showed the same failure modes.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _normalize_llm_diagnosis_payload(payload: dict, fallback: dict) -> dict | None:
    if not isinstance(payload, dict):
        return None
    summary = str(payload.get("summary", "")).strip()
    severity = str(payload.get("severity", fallback.get("severity", "unknown"))).strip()
    if severity not in VALID_SEVERITY:
        severity = str(fallback.get("severity", "unknown"))
    mechanism = str(payload.get("mechanism", fallback.get("mechanism", ""))).strip()
    failure_modes = [str(item).strip() for item in payload.get("failure_modes", []) if str(item).strip()]
    evidence = [str(item).strip() for item in payload.get("evidence", []) if str(item).strip()]
    counterfactuals = [str(item).strip() for item in payload.get("counterfactuals", []) if str(item).strip()]
    if not summary:
        return None
    return {
        "status": fallback.get("status", "complete"),
        "summary": summary,
        "severity": severity,
        "mechanism": mechanism or str(fallback.get("mechanism", "")).strip(),
        "failure_modes": failure_modes or list(fallback.get("failure_modes", [])),
        "evidence": evidence or list(fallback.get("evidence", [])),
        "counterfactuals": counterfactuals or list(fallback.get("counterfactuals", [])),
    }


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
    heuristic_fields = _heuristic_reconciled_fields(diagnosis, outcome, target)

    llm_fields = heuristic_fields
    if str(os.environ.get("HARNESS_LAB_LLM_DIAGNOSIS_ENABLED", "")).strip().lower() in {"1", "true", "yes"}:
        candidate_dir = candidates_dir / candidate_id
        traces = {
            "science_metrics": _safe_read_json(candidate_dir / "traces" / "science_metrics.json"),
            "science_progress": _safe_read_json(candidate_dir / "traces" / "science_progress.json"),
            "backend_result": _safe_read_json(candidate_dir / "traces" / "backend_result.json"),
            "science_debug_summary": _safe_read_json(candidates_dir.parent / "memory" / "science_debug_summary.json"),
            "runner_stdout_tail": _safe_read_text(candidate_dir / "traces" / "runner_stdout.log"),
            "runner_stderr_tail": _safe_read_text(candidate_dir / "traces" / "runner_stderr.log"),
        }
        parent_id = proposal.get("parent_id") or diagnosis.get("parent_id")
        parent_diag = None
        if parent_id:
            parent_diag_path = candidates_dir / str(parent_id) / "diagnosis" / "summary.json"
            if parent_diag_path.exists():
                parent_diag = read_json(parent_diag_path)
        payload = run_claude_json(
            _llm_diagnosis_prompt(candidate_id, proposal, outcome, heuristic_fields, traces, parent_diagnosis=parent_diag),
            cwd=candidate_dir,
        )
        normalized = _normalize_llm_diagnosis_payload(payload or {}, heuristic_fields)
        if normalized:
            log.info("diagnosis authored by claude for %s", candidate_id)
            llm_fields = normalized
        else:
            log.warning("diagnosis: claude fallback to heuristic for %s (payload=%s)", candidate_id, "empty" if not payload else "invalid")

    return update_diagnosis(
        candidates_dir,
        candidate_id,
        status=str(llm_fields.get("status", heuristic_fields["status"])),
        summary=str(llm_fields.get("summary", heuristic_fields["summary"])),
        severity=str(llm_fields.get("severity", heuristic_fields["severity"])),
        mechanism=str(llm_fields.get("mechanism", heuristic_fields["mechanism"])),
        failure_modes=list(llm_fields.get("failure_modes", heuristic_fields["failure_modes"])),
        evidence=list(llm_fields.get("evidence", heuristic_fields["evidence"])),
        counterfactuals=list(llm_fields.get("counterfactuals", heuristic_fields["counterfactuals"])),
    )
