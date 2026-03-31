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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class RunnerResult:
    candidate_id: str
    backend: str
    outcome: CandidateOutcome


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
    (candidates_dir / candidate_id / "traces" / "run.json").write_text(
        json.dumps(trace_payload, indent=2, sort_keys=True) + "\n",
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
    monotonic_start = time.monotonic()
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
    stdout_text = stdout_path.read_text(encoding="utf-8")
    stderr_text = stderr_path.read_text(encoding="utf-8")
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
