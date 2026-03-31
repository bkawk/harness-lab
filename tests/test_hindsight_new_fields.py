"""Tests for Import 2 & 5: process classification and throughput aggregation in hindsight."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_lab.hindsight import build_hindsight
from harness_lab.workspace import create_candidate_workspace, write_json


def _make_candidate(candidates_dir, cid, *, outcome_label="dead_end", mechanism="encoder", evidence=None):
    """Create a minimal candidate workspace with given outcome."""
    ws = create_candidate_workspace(candidates_dir, cid)
    write_json(ws.outcome_path, {
        "candidate_id": cid,
        "status": "complete",
        "outcome_label": outcome_label,
        "benchmark": {"score": 0.5, "summary": "ok"},
        "audit": {"score": 0.4, "summary": "ok"},
        "observed_failure_modes": [],
        "evidence": list(evidence or []),
    })
    write_json(ws.diagnosis_path, {
        "candidate_id": cid,
        "status": "complete",
        "summary": "test",
        "severity": "medium",
        "mechanism": mechanism,
        "failure_modes": [],
        "evidence": [],
        "counterfactuals": [],
    })
    return ws


class TestHindsightProcessClassification:
    def test_counts_process_classifications(self, tmp_path):
        candidates_dir = tmp_path / "candidates"
        ws1 = _make_candidate(candidates_dir, "cand_0001")
        ws2 = _make_candidate(candidates_dir, "cand_0002")
        ws3 = _make_candidate(candidates_dir, "cand_0003")

        # Write process classification into run.json traces
        (ws1.traces_dir / "run.json").write_text(json.dumps({
            "process_classification": {"classification": "completed_quickly"},
        }))
        (ws2.traces_dir / "run.json").write_text(json.dumps({
            "process_classification": {"classification": "stalled"},
        }))
        (ws3.traces_dir / "run.json").write_text(json.dumps({
            "process_classification": {"classification": "stalled"},
        }))

        result = build_hindsight(candidates_dir)
        counts = result["process_classification_counts"]
        assert counts["completed_quickly"] == 1
        assert counts["stalled"] == 2

    def test_empty_when_no_classifications(self, tmp_path):
        candidates_dir = tmp_path / "candidates"
        _make_candidate(candidates_dir, "cand_0001")
        result = build_hindsight(candidates_dir)
        assert result["process_classification_counts"] == {}


class TestHindsightThroughputSummary:
    def test_aggregates_throughput_files(self, tmp_path):
        candidates_dir = tmp_path / "candidates"
        ws1 = _make_candidate(candidates_dir, "cand_0001")
        ws2 = _make_candidate(candidates_dir, "cand_0002")

        # Write throughput traces
        (ws1.traces_dir / "throughput.json").write_text(json.dumps({
            "wall_clock_seconds": 50.0,
            "poll_interval_seconds": 1.0,
            "stale_timeout_seconds": 600,
            "estimated_idle_polls": 49,
            "early_completion_detected": True,
            "time_saved_estimate_seconds": 550.0,
        }))
        (ws2.traces_dir / "throughput.json").write_text(json.dumps({
            "wall_clock_seconds": 400.0,
            "poll_interval_seconds": 1.0,
            "stale_timeout_seconds": 600,
            "estimated_idle_polls": 399,
            "early_completion_detected": False,
            "time_saved_estimate_seconds": 0.0,
        }))

        result = build_hindsight(candidates_dir)
        ts = result["throughput_summary"]
        assert ts["total_runs"] == 2
        assert ts["avg_wall_clock"] == 225.0
        assert ts["avg_time_saved"] == 275.0
        assert ts["total_time_saved"] == 550.0
        assert ts["early_completion_count"] == 1

    def test_zero_throughput(self, tmp_path):
        candidates_dir = tmp_path / "candidates"
        _make_candidate(candidates_dir, "cand_0001")
        result = build_hindsight(candidates_dir)
        ts = result["throughput_summary"]
        assert ts["total_runs"] == 0
        assert ts["avg_wall_clock"] == 0
