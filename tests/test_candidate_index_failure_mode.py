from __future__ import annotations

from harness_lab.memory import build_candidate_index
from harness_lab.workspace import create_candidate_workspace, write_json


def test_candidate_index_prefers_diagnosed_failure_mode_over_proposal_target(tmp_path):
    candidates_dir = tmp_path / "candidates"
    ws = create_candidate_workspace(candidates_dir, "cand_0001")
    write_json(
        ws.proposal_path,
        {
            "candidate_id": "cand_0001",
            "status": "candidate",
            "target": {
                "harness_component": "science_model",
                "expected_failure_mode": "transfer_smoke_failed",
                "novelty_basis": "test",
            },
            "rationale": "test",
            "changes": [],
            "backend_levers": {},
        },
    )
    write_json(
        ws.diagnosis_path,
        {
            "candidate_id": "cand_0001",
            "status": "complete",
            "summary": "test",
            "severity": "high",
            "mechanism": "science_model",
            "failure_modes": ["hard_transfer_regression", "boundary_smoke:gap_too_wide"],
            "evidence": [],
            "counterfactuals": [],
        },
    )
    write_json(
        ws.outcome_path,
        {
            "candidate_id": "cand_0001",
            "status": "complete",
            "outcome_label": "audit_blocked",
            "benchmark": {"score": 0.39, "summary": ""},
            "audit": {"score": 0.35, "summary": ""},
            "observed_failure_modes": ["hard_transfer_regression", "boundary_smoke:gap_too_wide"],
            "evidence": [],
        },
    )

    payload = build_candidate_index(candidates_dir)
    summary = payload["candidates"][0]

    assert summary["expected_failure_mode"] == "hard_transfer_regression"
    assert summary["failure_modes"][0] == "hard_transfer_regression"
