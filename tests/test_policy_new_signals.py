"""Tests for Import 2 & 5: process classification and throughput signals in policy."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_lab.policy import build_policy
from harness_lab.workspace import write_json


def _setup_policy_env(tmp_path, *, hindsight_overrides=None, index_overrides=None):
    """Set up minimal memory directory for policy building."""
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    index = {"candidate_count": 5, "candidates": [], **(index_overrides or {})}
    write_json(memory_dir / "candidate_index.json", index)

    hindsight = {
        "candidate_count": 5,
        "summary": "",
        "hindsight_findings": [],
        "policy_adjustments": [],
        "top_outcomes": [],
        "top_failure_modes": [],
        "over_explored_mechanisms": [],
        "under_explored_promising_mechanisms": [],
        "over_explored_backend_fingerprints": [],
        "under_explored_backend_fingerprints": [],
        "mechanism_stats": [],
        "backend_fingerprint_stats": [],
        "process_classification_counts": {},
        "throughput_summary": {},
        **(hindsight_overrides or {}),
    }
    write_json(memory_dir / "hindsight.json", hindsight)

    return candidates_dir, memory_dir


class TestPolicyProcessClassification:
    def test_stale_process_pressure(self, tmp_path):
        candidates_dir, memory_dir = _setup_policy_env(
            tmp_path,
            hindsight_overrides={"process_classification_counts": {"stalled": 3}},
        )
        policy = build_policy(candidates_dir, memory_dir)
        assert "policy:stale_process_pressure" in policy["evidence"]
        assert policy["selection_mode"] == "stabilize"
        assert policy["cooldown_multiplier"] >= 2.0

    def test_crash_pressure(self, tmp_path):
        candidates_dir, memory_dir = _setup_policy_env(
            tmp_path,
            hindsight_overrides={"process_classification_counts": {"crashed_early": 2}},
        )
        policy = build_policy(candidates_dir, memory_dir)
        assert "policy:crash_pressure" in policy["evidence"]
        assert policy["cooldown_multiplier"] >= 1.5

    def test_no_pressure_without_issues(self, tmp_path):
        candidates_dir, memory_dir = _setup_policy_env(tmp_path)
        policy = build_policy(candidates_dir, memory_dir)
        assert "policy:stale_process_pressure" not in policy["evidence"]
        assert "policy:crash_pressure" not in policy["evidence"]


class TestPolicyThroughput:
    def test_efficient_polling_signal(self, tmp_path):
        candidates_dir, memory_dir = _setup_policy_env(
            tmp_path,
            hindsight_overrides={"throughput_summary": {"avg_time_saved": 120, "avg_wall_clock": 200}},
        )
        policy = build_policy(candidates_dir, memory_dir)
        assert "policy:efficient_polling" in policy["evidence"]

    def test_low_savings_signal(self, tmp_path):
        candidates_dir, memory_dir = _setup_policy_env(
            tmp_path,
            hindsight_overrides={"throughput_summary": {"avg_time_saved": 5, "avg_wall_clock": 500}},
        )
        policy = build_policy(candidates_dir, memory_dir)
        assert "policy:low_polling_savings" in policy["evidence"]
