from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from harness_lab.datasets import get_dataset_record
from harness_lab.backend import DEFAULT_COMMAND_BACKEND
from harness_lab.execution import plan_execution_for_candidate
from harness_lab.hardware import read_hardware_profile
from harness_lab.memory import read_json
from harness_lab.outcome import CandidateOutcome, update_outcome_for_candidate
from harness_lab.simulator import simulate_candidate_outcome

STALE_TIMEOUT_DEFAULT = 600  # seconds before a command backend process is killed
EARLY_CRASH_THRESHOLD = 5.0  # seconds — anything shorter is "crashed_early"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class RunnerResult:
    candidate_id: str
    backend: str
    outcome: CandidateOutcome


def build_environment_preflight(
    repo_dir: Path,
    candidates_dir: Path,
    candidate_id: str,
    dataset_id: str,
    dataset_record: dict | None,
    hardware_profile: dict,
    backend_command: list[str],
) -> dict:
    """Gather a compact preflight summary of toolchain, dataset readiness, and backend path."""
    dataset_status = "not_configured"
    dataset_path = ""
    if dataset_record:
        dataset_status = str(dataset_record.get("status", "unknown"))
        dataset_path = str(dataset_record.get("local_path", ""))
    return {
        "candidate_id": candidate_id,
        "python_version": sys.version.split()[0],
        "working_directory": str(repo_dir),
        "backend_command": backend_command,
        "dataset_id": dataset_id,
        "dataset_status": dataset_status,
        "dataset_path": dataset_path,
        "hostname": str(hardware_profile.get("hostname", "")),
        "environment_hint": str(hardware_profile.get("environment_hint", "")),
        "cpu_count": hardware_profile.get("cpu_count"),
        "memory_gb_estimate": hardware_profile.get("memory_gb_estimate"),
    }


def classify_process_behavior(
    duration_seconds: float,
    returncode: int,
    poll_interval_seconds: float,
    stale_timeout: float,
) -> dict:
    """Classify how a command backend process behaved based on its runtime profile."""
    if returncode != 0 and duration_seconds < EARLY_CRASH_THRESHOLD:
        classification = "crashed_early"
    elif duration_seconds >= stale_timeout:
        classification = "stalled"
    elif duration_seconds < poll_interval_seconds * 2:
        classification = "completed_quickly"
    elif duration_seconds > stale_timeout * 0.5:
        classification = "slow_completion"
    else:
        classification = "normal_completion"
    return {
        "classification": classification,
        "duration_seconds": round(duration_seconds, 3),
        "returncode": returncode,
        "poll_count_estimate": max(1, int(duration_seconds / max(poll_interval_seconds, 0.01))),
    }


def compute_throughput_accounting(
    duration_seconds: float,
    poll_interval_seconds: float,
    stale_timeout: float,
) -> dict:
    """Compute wall-clock throughput accounting for a command run."""
    early = duration_seconds < stale_timeout * 0.5
    saved = max(0.0, stale_timeout - duration_seconds) if early else 0.0
    return {
        "wall_clock_seconds": round(duration_seconds, 3),
        "poll_interval_seconds": poll_interval_seconds,
        "stale_timeout_seconds": stale_timeout,
        "estimated_idle_polls": max(0, int(duration_seconds / max(poll_interval_seconds, 0.01)) - 1),
        "early_completion_detected": early,
        "time_saved_estimate_seconds": round(saved, 3),
    }


def build_preflight_bundle(
    candidates_dir: Path,
    memory_dir: Path,
    candidate_id: str,
) -> dict:
    """Package the most relevant files for a candidate into one place before execution."""
    candidate_dir = candidates_dir / candidate_id

    def _safe_read(path: Path) -> dict:
        if path.exists():
            return read_json(path)
        return {}

    bootstrap = _safe_read(candidate_dir / "memory" / "bootstrap_snapshot.json")
    execution_plan = _safe_read(candidate_dir / "execution" / "plan.json")
    proposal = _safe_read(candidate_dir / "proposal.json")
    diagnosis = _safe_read(candidate_dir / "diagnosis" / "summary.json")
    backend_profile = _safe_read(memory_dir / "backend_profile.json")
    dataset_registry = _safe_read(memory_dir / "datasets.json")

    ready = bool(
        proposal.get("status") not in {"", "draft"} or execution_plan.get("status") not in {"", "draft"}
    )

    return {
        "candidate_id": candidate_id,
        "preflight_ready": ready,
        "bootstrap_snapshot": bootstrap,
        "execution_plan": execution_plan,
        "proposal": proposal,
        "diagnosis": diagnosis,
        "backend_profile": backend_profile,
        "dataset_readiness": {
            "dataset_count": len(dataset_registry.get("datasets", [])),
            "ready_datasets": [
                d.get("dataset_id", "") for d in dataset_registry.get("datasets", []) if d.get("status") == "ready"
            ],
        },
    }


def _dataset_context(candidates_dir: Path, candidate_id: str) -> tuple[str, dict | None]:
    proposal = read_json(candidates_dir / candidate_id / "proposal.json")
    dataset_id = str(proposal.get("dataset_id", "")).strip()
    if not dataset_id:
        return "", None
    dataset_record = get_dataset_record(candidates_dir.parent / "memory", dataset_id)
    if not dataset_record or dataset_record.get("status") != "ready":
        raise ValueError(f"Candidate {candidate_id} expects dataset {dataset_id}, but it is not ready in the registry.")
    return dataset_id, dataset_record


def _trace_paths(candidates_dir: Path, candidate_id: str) -> tuple[Path, Path, Path, Path]:
    trace_dir = candidates_dir / candidate_id / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = trace_dir / "runner_stdout.log"
    stderr_path = trace_dir / "runner_stderr.log"
    trace_path = trace_dir / "run.json"
    result_path = trace_dir / "backend_result.json"
    return stdout_path, stderr_path, trace_path, result_path


def _live_status_path(candidates_dir: Path, candidate_id: str) -> Path:
    trace_dir = candidates_dir / candidate_id / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    return trace_dir / "live_command.json"


def _write_live_status(
    *,
    candidates_dir: Path,
    candidate_id: str,
    backend: str,
    command: list[str],
    started_at: str,
    status: str,
    pid: int | None,
    poll_interval_seconds: float,
    last_poll_at: str,
    finished_at: str | None = None,
    returncode: int | None = None,
) -> None:
    payload = {
        "candidate_id": candidate_id,
        "backend": backend,
        "command": command,
        "started_at": started_at,
        "status": status,
        "pid": pid,
        "poll_interval_seconds": poll_interval_seconds,
        "last_poll_at": last_poll_at,
    }
    if finished_at is not None:
        payload["finished_at"] = finished_at
    if returncode is not None:
        payload["returncode"] = returncode
    _live_status_path(candidates_dir, candidate_id).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_trace(
    *,
    candidates_dir: Path,
    candidate_id: str,
    backend: str,
    repo_dir: Path,
    command: list[str],
    started_at: str,
    finished_at: str,
    returncode: int,
    duration_seconds: float,
    poll_interval_seconds: float | None,
    stdout_path: Path,
    stderr_path: Path,
    outcome: CandidateOutcome,
    result_path: Path | None = None,
    environment_preflight: dict | None = None,
    process_classification: dict | None = None,
    throughput_accounting: dict | None = None,
) -> None:
    trace_payload = {
        "candidate_id": candidate_id,
        "backend": backend,
        "started_at": started_at,
        "finished_at": finished_at,
        "command": command,
        "cwd": str(repo_dir),
        "returncode": returncode,
        "duration_seconds": round(duration_seconds, 3),
        "stdout_path": str(stdout_path.relative_to(candidates_dir / candidate_id)),
        "stderr_path": str(stderr_path.relative_to(candidates_dir / candidate_id)),
        "outcome": asdict(outcome),
    }
    if poll_interval_seconds is not None:
        trace_payload["poll_interval_seconds"] = poll_interval_seconds
    if result_path is not None:
        trace_payload["backend_result_path"] = str(result_path.relative_to(candidates_dir / candidate_id))
    if environment_preflight is not None:
        trace_payload["environment_preflight"] = environment_preflight
    if process_classification is not None:
        trace_payload["process_classification"] = process_classification
    if throughput_accounting is not None:
        trace_payload["throughput_accounting"] = throughput_accounting
    trace_dir = candidates_dir / candidate_id / "traces"
    (trace_dir / "run.json").write_text(
        json.dumps(trace_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if environment_preflight is not None:
        (trace_dir / "environment_preflight.json").write_text(
            json.dumps(environment_preflight, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if throughput_accounting is not None:
        (trace_dir / "throughput.json").write_text(
            json.dumps(throughput_accounting, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _run_simulated_backend(
    repo_dir: Path,
    candidates_dir: Path,
    candidate_id: str,
    hardware_profile: dict,
    started_at: str,
) -> RunnerResult:
    stdout_path, stderr_path, _, _ = _trace_paths(candidates_dir, candidate_id)
    command = [
        sys.executable,
        str(repo_dir / "scripts" / "simulate_outcome.py"),
        candidate_id,
        "--candidates-dir",
        str(candidates_dir),
        "--write",
    ]
    result = subprocess.run(
        command,
        cwd=repo_dir,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONPATH": str(repo_dir / "src")
            if not os.environ.get("PYTHONPATH")
            else f"{repo_dir / 'src'}:{os.environ['PYTHONPATH']}",
        },
    )
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Simulated runner failed for {candidate_id}: {result.stderr.strip()}")
    simulated = simulate_candidate_outcome(candidates_dir, candidate_id)
    evidence = list(simulated.evidence)
    if hardware_profile.get("hostname"):
        evidence.append(f"hardware:host:{hardware_profile['hostname']}")
    if hardware_profile.get("environment_hint"):
        evidence.append(f"hardware:env:{hardware_profile['environment_hint']}")
    evidence.extend(
        [
            f"trace:stdout:{stdout_path.name}",
            f"trace:stderr:{stderr_path.name}",
            "trace:backend:simulated",
        ]
    )
    outcome = update_outcome_for_candidate(
        candidates_dir,
        candidate_id,
        status="complete",
        outcome_label=simulated.outcome_label,
        benchmark_score=simulated.benchmark_score,
        benchmark_summary=simulated.benchmark_summary,
        audit_score=simulated.audit_score,
        audit_summary=simulated.audit_summary,
        observed_failure_modes=list(simulated.observed_failure_modes),
        evidence=evidence,
    )
    _write_trace(
        candidates_dir=candidates_dir,
        candidate_id=candidate_id,
        backend="simulated",
        repo_dir=repo_dir,
        command=command,
        started_at=started_at,
        finished_at=utc_now(),
        returncode=result.returncode,
        duration_seconds=0.0,
        poll_interval_seconds=None,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        outcome=outcome,
    )
    return RunnerResult(candidate_id=candidate_id, backend="simulated", outcome=outcome)


def _backend_command(repo_dir: Path) -> list[str]:
    command = os.environ.get("HARNESS_LAB_BACKEND_COMMAND", "").strip() or DEFAULT_COMMAND_BACKEND
    return ["bash", "-lc", command]


def _parse_command_backend_result(result_path: Path) -> dict:
    if not result_path.exists():
        raise RuntimeError(
            f"Command backend did not write result JSON to {result_path}. "
            "Expected fields: outcome_label, benchmark_score, benchmark_summary, "
            "audit_score, audit_summary, observed_failure_modes, evidence."
        )
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    required = ("outcome_label", "benchmark_summary", "audit_summary")
    missing = [field for field in required if field not in payload]
    if missing:
        raise RuntimeError(f"Command backend result is missing required fields: {', '.join(missing)}")
    return payload


def _run_command_backend(
    repo_dir: Path,
    candidates_dir: Path,
    candidate_id: str,
    hardware_profile: dict,
    dataset_id: str,
    dataset_record: dict | None,
    started_at: str,
) -> RunnerResult:
    stdout_path, stderr_path, _, result_path = _trace_paths(candidates_dir, candidate_id)
    command = _backend_command(repo_dir)
    candidate_dir = candidates_dir / candidate_id
    plan_path = candidate_dir / "execution" / "plan.json"
    proposal_path = candidate_dir / "proposal.json"
    diagnosis_path = candidate_dir / "diagnosis" / "summary.json"
    outcome_path = candidate_dir / "outcome" / "result.json"
    memory_dir = candidates_dir.parent / "memory"

    # --- Import 1: environment preflight ---
    env_preflight = build_environment_preflight(
        repo_dir, candidates_dir, candidate_id,
        dataset_id, dataset_record, hardware_profile, command,
    )

    # --- Import 6: preflight bundle ---
    preflight_dir = candidate_dir / "preflight"
    preflight_dir.mkdir(parents=True, exist_ok=True)
    bundle = build_preflight_bundle(candidates_dir, memory_dir, candidate_id)
    bundle["environment_preflight"] = env_preflight
    (preflight_dir / "bundle.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )

    env = {
        **os.environ,
        "PYTHONPATH": str(repo_dir / "src")
        if not os.environ.get("PYTHONPATH")
        else f"{repo_dir / 'src'}:{os.environ['PYTHONPATH']}",
        "HARNESS_LAB_REPO_DIR": str(repo_dir),
        "HARNESS_LAB_CANDIDATES_DIR": str(candidates_dir),
        "HARNESS_LAB_CANDIDATE_ID": candidate_id,
        "HARNESS_LAB_CANDIDATE_DIR": str(candidate_dir),
        "HARNESS_LAB_PLAN_PATH": str(plan_path),
        "HARNESS_LAB_PROPOSAL_PATH": str(proposal_path),
        "HARNESS_LAB_DIAGNOSIS_PATH": str(diagnosis_path),
        "HARNESS_LAB_OUTCOME_PATH": str(outcome_path),
        "HARNESS_LAB_RESULT_PATH": str(result_path),
        "HARNESS_LAB_TRACE_DIR": str(candidate_dir / "traces"),
        "HARNESS_LAB_DATASET_ID": dataset_id,
        "HARNESS_LAB_DATASET_PATH": str(dataset_record.get("local_path", "")) if dataset_record else "",
        "HARNESS_LAB_PREFLIGHT_BUNDLE_PATH": str(preflight_dir / "bundle.json"),
    }
    if hardware_profile.get("environment_hint"):
        env["HARNESS_LAB_HARDWARE_ENVIRONMENT"] = str(hardware_profile["environment_hint"])
    if hardware_profile.get("hostname"):
        env["HARNESS_LAB_HOSTNAME"] = str(hardware_profile["hostname"])

    result = subprocess.run(
        ["bash", "-lc", "true"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )
    poll_interval_seconds = float(os.environ.get("HARNESS_LAB_RUNNER_POLL_SECONDS", "1.0") or 1.0)
    stale_timeout = float(os.environ.get("HARNESS_LAB_RUNNER_STALE_SECONDS", str(STALE_TIMEOUT_DEFAULT)) or STALE_TIMEOUT_DEFAULT)
    monotonic_start = time.monotonic()
    was_stalled = False
    with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open("w", encoding="utf-8") as stderr_file:
        process = subprocess.Popen(
            command,
            cwd=repo_dir,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            env=env,
        )
        _write_live_status(
            candidates_dir=candidates_dir,
            candidate_id=candidate_id,
            backend="command",
            command=command,
            started_at=started_at,
            status="running",
            pid=process.pid,
            poll_interval_seconds=poll_interval_seconds,
            last_poll_at=started_at,
        )
        while True:
            returncode = process.poll()
            now = utc_now()
            if returncode is not None:
                _write_live_status(
                    candidates_dir=candidates_dir,
                    candidate_id=candidate_id,
                    backend="command",
                    command=command,
                    started_at=started_at,
                    status="finished",
                    pid=process.pid,
                    poll_interval_seconds=poll_interval_seconds,
                    last_poll_at=now,
                    finished_at=now,
                    returncode=returncode,
                )
                break
            # --- Import 2: stale-process detection ---
            elapsed = time.monotonic() - monotonic_start
            if elapsed >= stale_timeout:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                returncode = process.returncode
                was_stalled = True
                _write_live_status(
                    candidates_dir=candidates_dir,
                    candidate_id=candidate_id,
                    backend="command",
                    command=command,
                    started_at=started_at,
                    status="stalled",
                    pid=process.pid,
                    poll_interval_seconds=poll_interval_seconds,
                    last_poll_at=now,
                    finished_at=now,
                    returncode=returncode,
                )
                break
            _write_live_status(
                candidates_dir=candidates_dir,
                candidate_id=candidate_id,
                backend="command",
                command=command,
                started_at=started_at,
                status="running",
                pid=process.pid,
                poll_interval_seconds=poll_interval_seconds,
                last_poll_at=now,
            )
            time.sleep(max(0.1, poll_interval_seconds))

    duration_seconds = time.monotonic() - monotonic_start

    # --- Import 2: process classification ---
    proc_class = classify_process_behavior(
        duration_seconds, returncode, poll_interval_seconds, stale_timeout,
    )
    if was_stalled:
        proc_class["classification"] = "stalled"

    # --- Import 5: throughput accounting ---
    throughput = compute_throughput_accounting(
        duration_seconds, poll_interval_seconds, stale_timeout,
    )

    stdout_text = stdout_path.read_text(encoding="utf-8")
    stderr_text = stderr_path.read_text(encoding="utf-8")

    if was_stalled:
        # Stalled processes get a structured outcome instead of raising
        outcome = update_outcome_for_candidate(
            candidates_dir,
            candidate_id,
            status="complete",
            outcome_label="stalled",
            benchmark_summary="Process exceeded stale timeout and was terminated.",
            audit_summary="",
            observed_failure_modes=["stale_process"],
            evidence=[
                f"trace:stdout:{stdout_path.name}",
                f"trace:stderr:{stderr_path.name}",
                "trace:backend:command",
                f"process:classification:{proc_class['classification']}",
                f"process:duration:{proc_class['duration_seconds']}",
            ],
        )
        _write_trace(
            candidates_dir=candidates_dir,
            candidate_id=candidate_id,
            backend="command",
            repo_dir=repo_dir,
            command=command,
            started_at=started_at,
            finished_at=utc_now(),
            returncode=returncode,
            duration_seconds=duration_seconds,
            poll_interval_seconds=poll_interval_seconds,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            outcome=outcome,
            result_path=None,
            environment_preflight=env_preflight,
            process_classification=proc_class,
            throughput_accounting=throughput,
        )
        return RunnerResult(candidate_id=candidate_id, backend="command", outcome=outcome)

    if returncode != 0:
        raise RuntimeError(f"Command runner failed for {candidate_id}: {stderr_text.strip() or stdout_text.strip()}")

    payload = _parse_command_backend_result(result_path)
    evidence = [str(item) for item in payload.get("evidence", []) if str(item).strip()]
    if hardware_profile.get("hostname"):
        evidence.append(f"hardware:host:{hardware_profile['hostname']}")
    if hardware_profile.get("environment_hint"):
        evidence.append(f"hardware:env:{hardware_profile['environment_hint']}")
    evidence.extend(
        [
            f"trace:stdout:{stdout_path.name}",
            f"trace:stderr:{stderr_path.name}",
            f"trace:backend_result:{result_path.name}",
            "trace:backend:command",
            f"process:classification:{proc_class['classification']}",
            f"process:duration:{proc_class['duration_seconds']}",
            f"trace:environment_preflight:environment_preflight.json",
        ]
    )
    outcome = update_outcome_for_candidate(
        candidates_dir,
        candidate_id,
        status="complete",
        outcome_label=str(payload.get("outcome_label", "")),
        benchmark_score=payload.get("benchmark_score"),
        benchmark_summary=str(payload.get("benchmark_summary", "")),
        audit_score=payload.get("audit_score"),
        audit_summary=str(payload.get("audit_summary", "")),
        observed_failure_modes=[str(item) for item in payload.get("observed_failure_modes", []) if str(item).strip()],
        evidence=evidence,
    )
    _write_trace(
        candidates_dir=candidates_dir,
        candidate_id=candidate_id,
        backend="command",
        repo_dir=repo_dir,
        command=command,
        started_at=started_at,
        finished_at=utc_now(),
        returncode=returncode,
        duration_seconds=duration_seconds,
        poll_interval_seconds=poll_interval_seconds,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        outcome=outcome,
        result_path=result_path,
        environment_preflight=env_preflight,
        process_classification=proc_class,
        throughput_accounting=throughput,
    )
    return RunnerResult(candidate_id=candidate_id, backend="command", outcome=outcome)


def run_candidate(
    repo_dir: Path,
    candidates_dir: Path,
    candidate_id: str,
    *,
    backend: str = "simulated",
) -> RunnerResult:
    if backend not in {"simulated", "command"}:
        raise ValueError(f"Unsupported runner backend: {backend}")

    dataset_id, dataset_record = _dataset_context(candidates_dir, candidate_id)
    plan_execution_for_candidate(candidates_dir, candidate_id)
    hardware_profile = read_hardware_profile(candidates_dir.parent / "memory")
    started_at = utc_now()

    if backend == "simulated":
        return _run_simulated_backend(repo_dir, candidates_dir, candidate_id, hardware_profile, started_at)
    return _run_command_backend(
        repo_dir,
        candidates_dir,
        candidate_id,
        hardware_profile,
        dataset_id,
        dataset_record,
        started_at,
    )
