from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class CandidateWorkspace:
    candidate_id: str
    root: Path
    parent_id: str | None
    created_at: str

    @property
    def source_dir(self) -> Path:
        return self.root / "source"

    @property
    def patches_dir(self) -> Path:
        return self.root / "patches"

    @property
    def traces_dir(self) -> Path:
        return self.root / "traces"

    @property
    def benchmark_dir(self) -> Path:
        return self.root / "benchmark"

    @property
    def execution_dir(self) -> Path:
        return self.root / "execution"

    @property
    def audit_dir(self) -> Path:
        return self.root / "audit"

    @property
    def outcome_dir(self) -> Path:
        return self.root / "outcome"

    @property
    def diagnosis_dir(self) -> Path:
        return self.root / "diagnosis"

    @property
    def memory_dir(self) -> Path:
        return self.root / "memory"

    @property
    def preflight_dir(self) -> Path:
        return self.root / "preflight"

    @property
    def proposal_path(self) -> Path:
        return self.root / "proposal.json"

    @property
    def diagnosis_path(self) -> Path:
        return self.root / "diagnosis" / "summary.json"

    @property
    def execution_plan_path(self) -> Path:
        return self.root / "execution" / "plan.json"

    @property
    def outcome_path(self) -> Path:
        return self.root / "outcome" / "result.json"

    @property
    def manifest_path(self) -> Path:
        return self.root / "workspace.json"


def create_candidate_workspace(base_dir: Path, candidate_id: str, parent_id: str | None = None) -> CandidateWorkspace:
    root = base_dir / candidate_id
    workspace = CandidateWorkspace(
        candidate_id=candidate_id,
        root=root,
        parent_id=parent_id,
        created_at=utc_now(),
    )
    if root.exists():
        raise FileExistsError(f"Candidate workspace already exists: {root}")

    for path in (
        workspace.source_dir,
        workspace.patches_dir,
        workspace.traces_dir,
        workspace.benchmark_dir,
        workspace.execution_dir,
        workspace.audit_dir,
        workspace.outcome_dir,
        workspace.diagnosis_dir,
        workspace.memory_dir,
        workspace.preflight_dir,
    ):
        path.mkdir(parents=True, exist_ok=True)

    write_json(
        workspace.manifest_path,
        {
            "candidate_id": workspace.candidate_id,
            "parent_id": workspace.parent_id,
            "created_at": workspace.created_at,
            "paths": {
                "source": str(workspace.source_dir.relative_to(root)),
                "patches": str(workspace.patches_dir.relative_to(root)),
                "traces": str(workspace.traces_dir.relative_to(root)),
                "benchmark": str(workspace.benchmark_dir.relative_to(root)),
                "execution": str(workspace.execution_dir.relative_to(root)),
                "audit": str(workspace.audit_dir.relative_to(root)),
                "outcome": str(workspace.outcome_dir.relative_to(root)),
                "diagnosis": str(workspace.diagnosis_dir.relative_to(root)),
                "memory": str(workspace.memory_dir.relative_to(root)),
                "preflight": str(workspace.preflight_dir.relative_to(root)),
            },
        },
    )
    write_json(
        workspace.proposal_path,
        {
            "candidate_id": workspace.candidate_id,
            "parent_id": workspace.parent_id,
            "created_at": workspace.created_at,
            "status": "draft",
            "target": {
                "harness_component": "",
                "expected_failure_mode": "",
                "novelty_basis": "",
            },
            "rationale": "",
            "changes": [],
        },
    )
    write_json(
        workspace.execution_plan_path,
        {
            "candidate_id": workspace.candidate_id,
            "created_at": workspace.created_at,
            "status": "draft",
            "benchmark": {
                "objective": "",
                "steps": [],
                "success_signals": [],
            },
            "audit": {
                "required": False,
                "steps": [],
                "failure_signals": [],
            },
            "trace_capture": [],
        },
    )
    write_json(
        workspace.outcome_path,
        {
            "candidate_id": workspace.candidate_id,
            "created_at": workspace.created_at,
            "status": "pending",
            "outcome_label": "",
            "benchmark": {
                "score": None,
                "summary": "",
            },
            "audit": {
                "score": None,
                "summary": "",
            },
            "observed_failure_modes": [],
            "evidence": [],
        },
    )
    write_json(
        workspace.diagnosis_path,
        {
            "candidate_id": workspace.candidate_id,
            "created_at": workspace.created_at,
            "status": "empty",
            "summary": "",
            "severity": "unknown",
            "mechanism": "",
            "failure_modes": [],
            "evidence": [],
            "counterfactuals": [],
        },
    )
    return workspace


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
