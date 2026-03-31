"""Tests for the meta-harness imports in runner.py: environment preflight,
process classification, throughput accounting, and preflight bundle."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_lab.runner import (
    EARLY_CRASH_THRESHOLD,
    STALE_TIMEOUT_DEFAULT,
    build_environment_preflight,
    build_preflight_bundle,
    classify_process_behavior,
    compute_throughput_accounting,
)
from harness_lab.workspace import create_candidate_workspace


# ---------------------------------------------------------------------------
# build_environment_preflight
# ---------------------------------------------------------------------------

class TestBuildEnvironmentPreflight:
    def test_basic_fields(self, tmp_path):
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        candidates_dir = tmp_path / "candidates"
        candidates_dir.mkdir()
        hw = {"hostname": "lab-box", "environment_hint": "linux_or_remote", "cpu_count": 8, "memory_gb_estimate": 32.0}
        result = build_environment_preflight(
            repo_dir, candidates_dir, "cand_0001",
            "abc_v1", {"status": "ready", "local_path": "/data/abc"}, hw,
            ["bash", "-lc", "python3 run.py"],
        )
        assert result["candidate_id"] == "cand_0001"
        assert result["dataset_id"] == "abc_v1"
        assert result["dataset_status"] == "ready"
        assert result["dataset_path"] == "/data/abc"
        assert result["hostname"] == "lab-box"
        assert result["cpu_count"] == 8
        assert "python_version" in result
        assert result["backend_command"] == ["bash", "-lc", "python3 run.py"]

    def test_no_dataset(self, tmp_path):
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        result = build_environment_preflight(
            repo_dir, tmp_path, "cand_0002",
            "", None, {},
            ["bash", "-lc", "true"],
        )
        assert result["dataset_status"] == "not_configured"
        assert result["dataset_path"] == ""


# ---------------------------------------------------------------------------
# classify_process_behavior
# ---------------------------------------------------------------------------

class TestClassifyProcessBehavior:
    def test_completed_quickly(self):
        result = classify_process_behavior(
            duration_seconds=0.5, returncode=0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["classification"] == "completed_quickly"

    def test_normal_completion(self):
        result = classify_process_behavior(
            duration_seconds=30.0, returncode=0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["classification"] == "normal_completion"

    def test_slow_completion(self):
        result = classify_process_behavior(
            duration_seconds=350.0, returncode=0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["classification"] == "slow_completion"

    def test_crashed_early(self):
        result = classify_process_behavior(
            duration_seconds=2.0, returncode=1, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["classification"] == "crashed_early"
        assert result["returncode"] == 1

    def test_stalled(self):
        result = classify_process_behavior(
            duration_seconds=601.0, returncode=0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["classification"] == "stalled"

    def test_poll_count_estimate(self):
        result = classify_process_behavior(
            duration_seconds=10.0, returncode=0, poll_interval_seconds=2.0, stale_timeout=600,
        )
        assert result["poll_count_estimate"] == 5

    def test_duration_recorded(self):
        result = classify_process_behavior(
            duration_seconds=12.345, returncode=0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["duration_seconds"] == 12.345


# ---------------------------------------------------------------------------
# compute_throughput_accounting
# ---------------------------------------------------------------------------

class TestComputeThroughputAccounting:
    def test_early_completion(self):
        result = compute_throughput_accounting(
            duration_seconds=50.0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["early_completion_detected"] is True
        assert result["time_saved_estimate_seconds"] == 550.0
        assert result["wall_clock_seconds"] == 50.0

    def test_no_early_completion(self):
        result = compute_throughput_accounting(
            duration_seconds=400.0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["early_completion_detected"] is False
        assert result["time_saved_estimate_seconds"] == 0.0

    def test_idle_polls(self):
        result = compute_throughput_accounting(
            duration_seconds=10.0, poll_interval_seconds=2.0, stale_timeout=600,
        )
        assert result["estimated_idle_polls"] == 4  # 10/2 - 1

    def test_zero_duration(self):
        result = compute_throughput_accounting(
            duration_seconds=0.0, poll_interval_seconds=1.0, stale_timeout=600,
        )
        assert result["early_completion_detected"] is True
        assert result["time_saved_estimate_seconds"] == 600.0


# ---------------------------------------------------------------------------
# build_preflight_bundle
# ---------------------------------------------------------------------------

class TestBuildPreflightBundle:
    def _setup_candidate(self, tmp_path):
        candidates_dir = tmp_path / "candidates"
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        ws = create_candidate_workspace(candidates_dir, "cand_0001")
        # Write a minimal dataset registry
        (memory_dir / "datasets.json").write_text(
            json.dumps({"datasets": [{"dataset_id": "abc_v1", "status": "ready"}]}) + "\n"
        )
        return candidates_dir, memory_dir

    def test_basic_bundle(self, tmp_path):
        candidates_dir, memory_dir = self._setup_candidate(tmp_path)
        bundle = build_preflight_bundle(candidates_dir, memory_dir, "cand_0001")
        assert bundle["candidate_id"] == "cand_0001"
        assert "proposal" in bundle
        assert "execution_plan" in bundle
        assert "diagnosis" in bundle
        assert "dataset_readiness" in bundle
        assert "abc_v1" in bundle["dataset_readiness"]["ready_datasets"]

    def test_preflight_ready_flag_draft(self, tmp_path):
        candidates_dir, memory_dir = self._setup_candidate(tmp_path)
        bundle = build_preflight_bundle(candidates_dir, memory_dir, "cand_0001")
        # Fresh workspace has draft proposal and draft plan, so preflight_ready should be False
        assert bundle["preflight_ready"] is False

    def test_missing_memory_files(self, tmp_path):
        candidates_dir, memory_dir = self._setup_candidate(tmp_path)
        # Remove datasets.json
        (memory_dir / "datasets.json").unlink()
        bundle = build_preflight_bundle(candidates_dir, memory_dir, "cand_0001")
        assert bundle["dataset_readiness"]["dataset_count"] == 0
