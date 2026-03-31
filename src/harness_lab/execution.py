from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.datasets import get_dataset_record
from harness_lab.hardware import read_hardware_profile
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


def plan_execution_for_candidate(candidates_dir: Path, candidate_id: str) -> ExecutionPlan:
    proposal = _load_proposal(candidates_dir, candidate_id)
    diagnosis = _load_diagnosis(candidates_dir, candidate_id)
    path = execution_plan_path_for_candidate(candidates_dir, candidate_id)
    existing = read_json(path)

    target = proposal.get("target", {})
    changes = proposal.get("changes", [])
    failure_modes = [str(item) for item in diagnosis.get("failure_modes", []) if str(item).strip()]
    mechanism = str(target.get("harness_component", "")).strip() or str(diagnosis.get("mechanism", "")).strip()
    expected_failure_mode = str(target.get("expected_failure_mode", "")).strip()
    rationale = str(proposal.get("rationale", "")).strip() or str(diagnosis.get("summary", "")).strip()
    hardware_profile = read_hardware_profile(candidates_dir.parent / "memory")
    dataset_id = str(proposal.get("dataset_id", "")).strip()
    dataset_record = get_dataset_record(candidates_dir.parent / "memory", dataset_id) if dataset_id else None
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

    trace_capture = (
        "proposal_application",
        "benchmark_trace",
        "benchmark_metrics",
        "diagnosis_notes",
    )
    if audit_required:
        trace_capture += ("audit_trace", "audit_metrics")

    plan = ExecutionPlan(
        candidate_id=candidate_id,
        status="planned",
        benchmark={
            "objective": rationale or "Evaluate the drafted harness change against the diagnosed parent failure.",
            "steps": benchmark_steps,
            "success_signals": success_signals,
        },
        audit={
            "required": audit_required,
            "steps": audit_steps,
            "failure_signals": failure_signals,
        },
        trace_capture=trace_capture,
        rationale=rationale,
    )

    output = dict(existing)
    output.update(plan.to_dict())
    output["hardware_context"] = hardware_profile
    output["dataset_context"] = dataset_record or ({"dataset_id": dataset_id, "status": "missing"} if dataset_id else {})
    write_json(path, output)
    return plan
