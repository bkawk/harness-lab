from __future__ import annotations

from harness_lab.bootstrap import build_decision_bundle
from harness_lab.workspace import create_candidate_workspace, write_json


def _make_candidate(candidates_dir, cid, *, status="complete", label="keeper", bench=0.3, audit=0.31, parent_id=None, mechanism="fusion_changed", failures=None):
    ws = create_candidate_workspace(candidates_dir, cid, parent_id=parent_id)
    write_json(
        ws.proposal_path,
        {
            "candidate_id": cid,
            "parent_id": parent_id,
            "status": "candidate",
            "target": {
                "harness_component": mechanism,
                "expected_failure_mode": "",
                "novelty_basis": f"novelty for {cid}",
            },
            "rationale": f"rationale for {cid}",
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
            "mechanism": mechanism,
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
            "benchmark": {"score": bench, "summary": f"bench {cid}" if bench is not None else ""},
            "audit": {"score": audit, "summary": f"audit {cid}" if audit is not None else ""},
            "observed_failure_modes": list(failures or []),
            "evidence": [],
        },
    )
    return ws


def test_decision_bundle_separates_scored_pending_and_stalled(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    _make_candidate(candidates_dir, "cand_0001", label="keeper", bench=0.31, audit=0.30, mechanism="fusion_changed")
    _make_candidate(candidates_dir, "cand_0002", status="pending", label="", bench=None, audit=None, mechanism="budget_policy_changed")
    _make_candidate(candidates_dir, "cand_0003", label="stalled", bench=None, audit=None, mechanism="loss_recipe_changed", failures=["stale_process"])
    create_candidate_workspace(candidates_dir, "cand_0004", parent_id="cand_0001")
    write_json(
        candidates_dir / "cand_0004" / "traces" / "science_progress.json",
        {
            "phase": "training",
            "updated_at": "2026-03-31T16:37:13+00:00",
            "steps": 200,
            "elapsed_seconds": 23.511,
            "remaining_seconds": 576.489,
            "peak_vram_mb": 1141,
        },
    )

    write_json(memory_dir / "candidate_index.json", {"candidate_count": 0, "candidates": []})
    write_json(memory_dir / "science_summary.json", {"leaders": {}, "recent_trend": {}, "trend_summary": ""})
    write_json(
        memory_dir / "science_debug_summary.json",
        {
            "summary": "Recent candidates are training up to the wall-clock limit without writing result artifacts.",
            "likely_issue": "training_consumes_wall_clock_before_eval",
            "recommended_fix": "Reserve evaluation time.",
            "findings": ["training reached the wall-clock limit before scoring"],
        },
    )
    monkeypatch.setattr("harness_lab.bootstrap.read_hindsight", lambda memory_dir: {"summary": "", "hindsight_findings": [], "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": [], "throughput_summary": {}, "process_classification_counts": {}})
    monkeypatch.setattr("harness_lab.bootstrap.read_policy", lambda memory_dir: {"summary": ""})
    monkeypatch.setattr("harness_lab.bootstrap.read_budget", lambda memory_dir: {"summary": "", "mechanism_budgets": []})
    monkeypatch.setattr("harness_lab.bootstrap.read_diversity", lambda memory_dir: {"summary": ""})
    monkeypatch.setattr("harness_lab.bootstrap.read_backend_profile", lambda memory_dir: {"summary": ""})
    monkeypatch.setattr("harness_lab.bootstrap.read_hardware_profile", lambda memory_dir: {"environment_hint": "linux_or_remote"})
    monkeypatch.setattr("harness_lab.bootstrap.read_external_review", lambda memory_dir: {"status": "idle", "lab_advice": [], "human_advice": []})
    monkeypatch.setattr("harness_lab.bootstrap.get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"} if dataset_id else None)

    bundle = build_decision_bundle(candidates_dir, memory_dir, "cand_0004", parent_id="cand_0001", dataset_id="abc_boundary512", synthesis={"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001", "reasons": ["base"], "total_score": 10}]})
    assert bundle["top_parent_id"] == "cand_0001"
    assert any(item["candidate_id"] == "cand_0001" for item in bundle["recent_scored_candidates"])
    assert any(item["candidate_id"] == "cand_0002" for item in bundle["pending_candidates"])
    assert any(item["candidate_id"] == "cand_0003" for item in bundle["stalled_candidates"])
    assert bundle["science_progress"]["phase"] == "training"
    assert bundle["science_progress"]["steps"] == 200
    assert bundle["science_debug_summary"]["likely_issue"] == "training_consumes_wall_clock_before_eval"
