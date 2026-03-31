#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path


def ssh_bin() -> str:
    return os.environ.get("HARNESS_LAB_SSH_BIN", "ssh").strip() or "ssh"


def scp_bin() -> str:
    return os.environ.get("HARNESS_LAB_SCP_BIN", "scp").strip() or "scp"


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def scp_to_remote(local_path: Path, remote_target: str) -> None:
    run([scp_bin(), str(local_path), remote_target])


def scp_from_remote(remote_source: str, local_path: Path) -> None:
    local_path.parent.mkdir(parents=True, exist_ok=True)
    run([scp_bin(), remote_source, str(local_path)])


def ssh(host: str, command: str) -> subprocess.CompletedProcess[str]:
    return run([ssh_bin(), host, command])


def main() -> None:
    candidate_id = require_env("HARNESS_LAB_CANDIDATE_ID")
    candidate_dir = Path(require_env("HARNESS_LAB_CANDIDATE_DIR"))
    result_path = Path(require_env("HARNESS_LAB_RESULT_PATH"))
    trace_dir = Path(require_env("HARNESS_LAB_TRACE_DIR"))
    dataset_id = os.environ.get("HARNESS_LAB_DATASET_ID", "").strip()

    remote_host = require_env("HARNESS_LAB_REMOTE_HOST")
    remote_command = require_env("HARNESS_LAB_REMOTE_BACKEND_COMMAND")
    remote_root = os.environ.get("HARNESS_LAB_REMOTE_WORKSPACE_ROOT", "/tmp/harness-lab").strip()
    remote_dataset_path = os.environ.get("HARNESS_LAB_REMOTE_DATASET_PATH", "").strip()
    remote_candidate_dir = f"{remote_root.rstrip('/')}/{candidate_id}"
    remote_result_path = f"{remote_candidate_dir}/backend_result.json"
    remote_stdout_path = f"{remote_candidate_dir}/remote_stdout.log"
    remote_stderr_path = f"{remote_candidate_dir}/remote_stderr.log"

    proposal_path = candidate_dir / "proposal.json"
    diagnosis_path = candidate_dir / "diagnosis" / "summary.json"
    plan_path = Path(require_env("HARNESS_LAB_PLAN_PATH"))

    ssh(remote_host, f"mkdir -p {shlex.quote(remote_candidate_dir)}/diagnosis {shlex.quote(remote_candidate_dir)}/execution")
    scp_to_remote(proposal_path, f"{remote_host}:{remote_candidate_dir}/proposal.json")
    scp_to_remote(diagnosis_path, f"{remote_host}:{remote_candidate_dir}/diagnosis/summary.json")
    scp_to_remote(plan_path, f"{remote_host}:{remote_candidate_dir}/execution/plan.json")

    remote_exports = {
        "HARNESS_LAB_CANDIDATE_ID": candidate_id,
        "HARNESS_LAB_CANDIDATE_DIR": remote_candidate_dir,
        "HARNESS_LAB_PLAN_PATH": f"{remote_candidate_dir}/execution/plan.json",
        "HARNESS_LAB_PROPOSAL_PATH": f"{remote_candidate_dir}/proposal.json",
        "HARNESS_LAB_DIAGNOSIS_PATH": f"{remote_candidate_dir}/diagnosis/summary.json",
        "HARNESS_LAB_RESULT_PATH": remote_result_path,
        "HARNESS_LAB_DATASET_ID": dataset_id,
        "HARNESS_LAB_DATASET_PATH": remote_dataset_path,
    }
    export_clause = " ".join(
        f"{key}={shlex.quote(value)}"
        for key, value in remote_exports.items()
        if value
    )
    remote_shell = (
        f"cd {shlex.quote(remote_candidate_dir)} && "
        f"env {export_clause} bash -lc {shlex.quote(remote_command)} "
        f"> {shlex.quote(remote_stdout_path)} 2> {shlex.quote(remote_stderr_path)}"
    )
    ssh(remote_host, remote_shell)

    scp_from_remote(f"{remote_host}:{remote_result_path}", result_path)
    scp_from_remote(f"{remote_host}:{remote_stdout_path}", trace_dir / "remote_stdout.log")
    scp_from_remote(f"{remote_host}:{remote_stderr_path}", trace_dir / "remote_stderr.log")

    trace_dir.mkdir(parents=True, exist_ok=True)
    (trace_dir / "remote_backend.json").write_text(
        json.dumps(
            {
                "candidate_id": candidate_id,
                "remote_host": remote_host,
                "remote_candidate_dir": remote_candidate_dir,
                "remote_result_path": remote_result_path,
                "remote_stdout_path": remote_stdout_path,
                "remote_stderr_path": remote_stderr_path,
                "remote_command": remote_command,
                "dataset_id": dataset_id,
                "remote_dataset_path": remote_dataset_path,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"remote backend completed for {candidate_id} on {remote_host}")


if __name__ == "__main__":
    main()
