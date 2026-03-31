from harness_lab.memory import build_backend_module_summary
from harness_lab.workspace import write_json


def _candidate(tmp_path, candidate_id: str, *, outcome_label: str, benchmark: float | None, audit: float | None, modules: list[str]) -> None:
    candidate_root = tmp_path / candidate_id
    (candidate_root / "diagnosis").mkdir(parents=True)
    (candidate_root / "outcome").mkdir(parents=True)
    (candidate_root / "patches").mkdir(parents=True)
    (candidate_root / "source").mkdir(parents=True)
    (candidate_root / "traces").mkdir(parents=True)
    write_json(candidate_root / "workspace.json", {"candidate_id": candidate_id, "created_at": f"2026-03-31T00:00:0{candidate_id[-1]}+00:00", "parent_id": None})
    write_json(candidate_root / "proposal.json", {"status": "drafted", "target": {"harness_component": "initial_harness", "expected_failure_mode": "transfer", "novelty_basis": "module_split"}})
    write_json(candidate_root / "diagnosis" / "summary.json", {"status": "complete", "summary": "", "severity": "medium", "mechanism": "initial_harness", "failure_modes": []})
    write_json(candidate_root / "outcome" / "result.json", {"status": "complete", "outcome_label": outcome_label, "benchmark": {"score": benchmark, "summary": ""}, "audit": {"score": audit, "summary": ""}, "observed_failure_modes": [], "evidence": []})
    write_json(candidate_root / "source" / "manifest.json", {"commit": "abc", "branch": "main", "tracked_file_count": 1})
    write_json(candidate_root / "patches" / "summary.json", {"changed_file_count": len(modules), "backend_fingerprints": [], "backend_modules_touched": modules})


def test_build_backend_module_summary_groups_by_module(tmp_path):
    _candidate(tmp_path, "cand_0001", outcome_label="keeper", benchmark=0.31, audit=0.30, modules=["science_model"])
    _candidate(tmp_path, "cand_0002", outcome_label="audit_blocked", benchmark=0.33, audit=0.27, modules=["science_model", "science_loss"])

    payload = build_backend_module_summary(tmp_path)

    assert payload["module_count"] == 2
    assert payload["backend_module_counts"] == {"science_loss": 1, "science_model": 2}
    top = payload["modules"][0]
    assert top["module"] == "science_model"
    assert top["attempts"] == 2
    assert top["keeper_count"] == 1
    assert top["audit_blocked_count"] == 1
