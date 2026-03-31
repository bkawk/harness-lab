from harness_lab.human_feedback import build_human_feedback
from harness_lab.memory import build_science_debug_summary
from harness_lab.workspace import write_json


def _candidate(tmp_path, candidate_id: str, *, peak_vram_mb: int, benchmark: float, audit: float):
    candidate_root = tmp_path / candidate_id
    (candidate_root / "diagnosis").mkdir(parents=True)
    (candidate_root / "outcome").mkdir(parents=True)
    (candidate_root / "patches").mkdir(parents=True)
    (candidate_root / "source").mkdir(parents=True)
    (candidate_root / "traces").mkdir(parents=True)
    write_json(candidate_root / "workspace.json", {"candidate_id": candidate_id, "created_at": f"2026-03-31T00:00:0{candidate_id[-1]}+00:00", "parent_id": None})
    write_json(candidate_root / "proposal.json", {"status": "candidate", "target": {"harness_component": "initial_harness"}})
    write_json(candidate_root / "diagnosis" / "summary.json", {"status": "complete", "summary": "", "severity": "medium", "mechanism": "initial_harness", "failure_modes": []})
    write_json(candidate_root / "outcome" / "result.json", {"status": "complete", "outcome_label": "audit_blocked", "benchmark": {"score": benchmark, "summary": ""}, "audit": {"score": audit, "summary": ""}, "observed_failure_modes": [], "evidence": []})
    write_json(candidate_root / "source" / "manifest.json", {"commit": "abc", "branch": "main", "tracked_file_count": 1})
    write_json(candidate_root / "patches" / "summary.json", {"changed_file_count": 1, "backend_fingerprints": [], "backend_modules_touched": ["science_model"]})
    write_json(candidate_root / "traces" / "science_metrics.json", {"peak_vram_mb": peak_vram_mb, "device": "cuda"})


def test_build_science_debug_summary_detects_vram_headroom(tmp_path):
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir.mkdir(parents=True)
    memory_dir.mkdir(parents=True)
    write_json(memory_dir / "hardware_profile.json", {"gpu_memory_total_gb": 8.0})
    _candidate(candidates_dir, "cand_0001", peak_vram_mb=580, benchmark=0.31, audit=0.29)
    _candidate(candidates_dir, "cand_0002", peak_vram_mb=600, benchmark=0.30, audit=0.28)

    payload = build_science_debug_summary(candidates_dir)

    assert payload["likely_issue"] == "vram_headroom"
    assert payload["vram"]["avg_peak_vram_ratio"] < 0.2


def test_human_feedback_surfaces_vram_headroom(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(memory_dir / "external_review.json", {"human_advice": []})
    write_json(memory_dir / "hindsight.json", {"top_outcomes": [], "top_failure_modes": [], "summary": ""})
    write_json(memory_dir / "policy.json", {"summary": ""})
    write_json(memory_dir / "science_summary.json", {"leaders": {}})
    write_json(memory_dir / "human_feedback_responses.json", {"responses": []})
    write_json(
        memory_dir / "science_debug_summary.json",
        {
            "counts": {"completed_with_scores": 3},
            "vram": {"avg_peak_vram_mb": 590.0, "avg_peak_vram_ratio": 0.072},
        },
    )

    payload = build_human_feedback(memory_dir)

    assert any(item["kind"] == "vram_headroom" for item in payload["items"])
