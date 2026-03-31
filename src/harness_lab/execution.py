from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("harness_lab.execution")

from harness_lab.datasets import get_dataset_record
from harness_lab.hardware import read_hardware_profile
from harness_lab.llm import run_claude_json
from harness_lab.memory import read_json
from harness_lab.workspace import write_json


@dataclass(frozen=True)
class ExecutionPlan:
    candidate_id: str
    status: str
    benchmark: dict
    audit: dict
    trace_capture: tuple[str, ...]
    rationale: str

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "status": self.status,
            "benchmark": self.benchmark,
            "audit": self.audit,
            "trace_capture": list(self.trace_capture),
            "rationale": self.rationale,
        }


def execution_plan_path_for_candidate(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id / "execution" / "plan.json"


def _load_proposal(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(candidates_dir / candidate_id / "proposal.json")


def _load_diagnosis(candidates_dir: Path, candidate_id: str) -> dict:
    return read_json(candidates_dir / candidate_id / "diagnosis" / "summary.json")


def _heuristic_execution_fields(
    proposal: dict,
    diagnosis: dict,
    hardware_profile: dict,
    dataset_record: dict | None,
    dataset_id: str,
) -> dict:
    target = proposal.get("target", {})
    changes = proposal.get("changes", [])
    failure_modes = [str(item) for item in diagnosis.get("failure_modes", []) if str(item).strip()]
    mechanism = str(target.get("harness_component", "")).strip() or str(diagnosis.get("mechanism", "")).strip()
    expected_failure_mode = str(target.get("expected_failure_mode", "")).strip()
    rationale = str(proposal.get("rationale", "")).strip() or str(diagnosis.get("summary", "")).strip()
    environment_hint = str(hardware_profile.get("environment_hint", "")).strip()
    cpu_count = hardware_profile.get("cpu_count")
    memory_gb = hardware_profile.get("memory_gb_estimate")

    benchmark_steps = [
        f"Apply proposed change to {mechanism or 'the harness under test'}.",
        "Run the local benchmark trace and capture raw logs under traces/.",
    ]
    if environment_hint:
        benchmark_steps.append(f"Adapt execution assumptions for environment: {environment_hint}.")
    if isinstance(cpu_count, int) and cpu_count > 0 and cpu_count <= 4:
        benchmark_steps.append("Keep the benchmark compact because CPU headroom is limited.")
    if isinstance(memory_gb, (int, float)) and memory_gb <= 8:
        benchmark_steps.append("Prefer low-memory evaluation settings on this machine.")
    if changes:
        benchmark_steps.extend([f"Exercise change: {item.get('summary', '')}" for item in changes[:3]])
    if dataset_record:
        benchmark_steps.append(f"Use dataset {dataset_record['dataset_id']} from {dataset_record['source']}.")
    elif dataset_id:
        benchmark_steps.append(f"Dataset {dataset_id} is expected but not yet attached.")

    success_signals = []
    if expected_failure_mode:
        success_signals.append(f"No recurrence of {expected_failure_mode} in benchmark traces.")
    if failure_modes:
        success_signals.append(f"Reduced evidence of {failure_modes[0]} relative to the parent candidate.")
    success_signals.append("Benchmark outputs produce a causal trace worth preserving in diagnosis.")

    audit_required = bool(expected_failure_mode or failure_modes)
    audit_steps = []
    failure_signals = []
    if audit_required:
        audit_steps.append("Run the audit path after benchmark if the candidate produces a plausible improvement.")
        audit_steps.append("Preserve audit outputs and compare them against the diagnosed parent failure.")
        failure_signals.append("Audit reproduces the same failure mode as the parent candidate.")
        failure_signals.append("Audit adds a new high-severity failure without offsetting benchmark evidence.")

    trace_capture = [
        "proposal_application",
        "benchmark_trace",
        "benchmark_metrics",
        "diagnosis_notes",
    ]
    if audit_required:
        trace_capture.extend(["audit_trace", "audit_metrics"])

    return {
        "rationale": rationale,
        "benchmark": {
            "objective": rationale or "Evaluate the drafted harness change against the diagnosed parent failure.",
            "steps": benchmark_steps,
            "success_signals": success_signals,
        },
        "audit": {
            "required": audit_required,
            "steps": audit_steps,
            "failure_signals": failure_signals,
        },
        "trace_capture": trace_capture,
    }


def _llm_execution_prompt(candidate_id: str, proposal: dict, diagnosis: dict, bootstrap_snapshot: dict, heuristic_fields: dict) -> str:
    payload = {
        "candidate_id": candidate_id,
        "proposal": {
            "rationale": proposal.get("rationale", ""),
            "target": proposal.get("target", {}),
            "changes": proposal.get("changes", [])[:8],
        },
        "diagnosis": {
            "summary": diagnosis.get("summary", ""),
            "severity": diagnosis.get("severity", ""),
            "mechanism": diagnosis.get("mechanism", ""),
            "failure_modes": diagnosis.get("failure_modes", []),
            "counterfactuals": diagnosis.get("counterfactuals", [])[:5],
        },
        "bootstrap_snapshot": bootstrap_snapshot,
        "heuristic_fallback": heuristic_fields,
    }
    return (
        "You are writing a bounded harness-lab execution plan.\n"
        "Return only JSON with keys: rationale, benchmark, audit, trace_capture.\n"
        "benchmark must contain objective, steps, success_signals.\n"
        "audit must contain required, steps, failure_signals.\n"
        "trace_capture must be an array of short strings.\n"
        "Keep the plan concrete and grounded in the supplied proposal and diagnosis.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _normalize_llm_execution_payload(payload: dict, fallback: dict) -> dict | None:
    if not isinstance(payload, dict):
        return None
    rationale = str(payload.get("rationale", "")).strip()
    benchmark = payload.get("benchmark", {})
    audit = payload.get("audit", {})
    trace_capture = payload.get("trace_capture", [])
    if not isinstance(benchmark, dict) or not isinstance(audit, dict) or not isinstance(trace_capture, list):
        return None
    objective = str(benchmark.get("objective", "")).strip()
    steps = [str(item).strip() for item in benchmark.get("steps", []) if str(item).strip()]
    success_signals = [str(item).strip() for item in benchmark.get("success_signals", []) if str(item).strip()]
    audit_required = bool(audit.get("required", False))
    audit_steps = [str(item).strip() for item in audit.get("steps", []) if str(item).strip()]
    failure_signals = [str(item).strip() for item in audit.get("failure_signals", []) if str(item).strip()]
    traces = [str(item).strip() for item in trace_capture if str(item).strip()]
    if not objective or not steps or not success_signals or not traces:
        return None
    return {
        "rationale": rationale or str(fallback.get("rationale", "")).strip(),
        "benchmark": {
            "objective": objective,
            "steps": steps[:8],
            "success_signals": success_signals[:6],
        },
        "audit": {
            "required": audit_required,
            "steps": audit_steps[:6],
            "failure_signals": failure_signals[:6],
        },
        "trace_capture": traces[:8],
    }


def plan_execution_for_candidate(candidates_dir: Path, candidate_id: str) -> ExecutionPlan:
    proposal = _load_proposal(candidates_dir, candidate_id)
    diagnosis = _load_diagnosis(candidates_dir, candidate_id)
    path = execution_plan_path_for_candidate(candidates_dir, candidate_id)
    existing = read_json(path)
    hardware_profile = read_hardware_profile(candidates_dir.parent / "memory")
    dataset_id = str(proposal.get("dataset_id", "")).strip()
    dataset_record = get_dataset_record(candidates_dir.parent / "memory", dataset_id) if dataset_id else None
    heuristic_fields = _heuristic_execution_fields(proposal, diagnosis, hardware_profile, dataset_record, dataset_id)
    fields = heuristic_fields
    if str(os.environ.get("HARNESS_LAB_LLM_EXECUTION_ENABLED", "")).strip().lower() in {"1", "true", "yes"}:
        candidate_dir = candidates_dir / candidate_id
        bootstrap_snapshot = {}
        bootstrap_path = candidate_dir / "memory" / "bootstrap_snapshot.json"
        if bootstrap_path.exists():
            bootstrap_snapshot = read_json(bootstrap_path)
        payload = run_claude_json(
            _llm_execution_prompt(candidate_id, proposal, diagnosis, bootstrap_snapshot, heuristic_fields),
            cwd=candidate_dir,
        )
        normalized = _normalize_llm_execution_payload(payload or {}, heuristic_fields)
        if normalized:
            log.info("execution plan authored by claude for %s", candidate_id)
            fields = normalized
        else:
            log.warning("execution: claude fallback to heuristic for %s (payload=%s)", candidate_id, "empty" if not payload else "invalid")

    plan = ExecutionPlan(
        candidate_id=candidate_id,
        status="planned",
        benchmark=fields["benchmark"],
        audit=fields["audit"],
        trace_capture=tuple(fields["trace_capture"]),
        rationale=fields["rationale"],
    )

    output = dict(existing)
    output.update(plan.to_dict())
    output["hardware_context"] = hardware_profile
    output["dataset_context"] = dataset_record or ({"dataset_id": dataset_id, "status": "missing"} if dataset_id else {})
    write_json(path, output)
    return plan
