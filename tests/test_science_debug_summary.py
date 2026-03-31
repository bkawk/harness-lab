from __future__ import annotations

from harness_lab.memory import build_science_debug_summary
from harness_lab.workspace import create_candidate_workspace, write_json


def _make_candidate(candidates_dir, cid, *, status="complete", label="stalled", failures=None):
    ws = create_candidate_workspace(candidates_dir, cid)
    write_json(
        ws.proposal_path,
        {
            "candidate_id": cid,
            "status": "candidate",
            "target": {"harness_component": "fusion_changed", "expected_failure_mode": "", "novelty_basis": ""},
            "changes": [],
        },
    )
    write_json(
        ws.diagnosis_path,
        {
            "candidate_id": cid,
            "status": "complete",
            "summary": f"diagnosis for {cid}",
            "severity": "medium",
            "mechanism": "fusion_changed",
            "failure_modes": list(failures or []),
            "evidence": [],
            "counterfactuals": [],
        },
    )
    write_json(
        ws.outcome_path,
        {
            "candidate_id": cid,
            "status": status,
            "outcome_label": label,
            "benchmark": {"score": None, "summary": ""},
            "audit": {"score": None, "summary": ""},
            "observed_failure_modes": list(failures or []),
            "evidence": [],
        },
    )
    return ws


def test_science_debug_summary_detects_train_to_wall_without_results(tmp_path):
    candidates_dir = tmp_path / "candidates"
    for idx in range(2):
        cid = f"cand_{idx+1:04d}"
        ws = _make_candidate(candidates_dir, cid, failures=["stale_timeout"])
        write_json(
            ws.traces_dir / "run.json",
            {"process_classification": {"classification": "stale_timeout"}, "duration_seconds": 720.0},
        )
        write_json(
            ws.traces_dir / "science_progress.json",
            {
                "phase": "training",
                "elapsed_seconds": 598.5,
                "steps": 22000,
                "peak_vram_mb": 600,
            },
        )
    payload = build_science_debug_summary(candidates_dir, recent_window=4)
    assert payload["likely_issue"] == "training_consumes_wall_clock_before_eval"
    assert payload["counts"]["full_budget_training_without_result"] == 2
    assert any("never wrote result artifacts" in finding for finding in payload["findings"])
