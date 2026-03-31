"""Tests for Import 5: throughput-adjusted budgets."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_lab.budget import build_budget
from harness_lab.workspace import write_json


def _setup_budget_env(tmp_path, *, hindsight_overrides=None, policy_overrides=None):
    """Set up minimal memory directory for budget building."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

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
        "mechanism_stats": [
            {
                "mechanism": "encoder",
                "attempts": 3,
                "positive_count": 1,
                "negative_count": 1,
                "avg_benchmark_score": 0.5,
                "outcome_counts": {"keeper": 1, "dead_end": 1, "improved": 0},
            }
        ],
        "backend_fingerprint_stats": [],
        "process_classification_counts": {},
        "throughput_summary": {},
        **(hindsight_overrides or {}),
    }
    write_json(memory_dir / "hindsight.json", hindsight)

    policy = {
        "summary": "test",
        "selection_mode": "balanced",
        "cooldown_multiplier": 1.0,
        "underexplored_bonus": 20,
        "backend_fingerprint_bonus": 10,
        "backend_fingerprint_cooldown": 12,
        "preferred_runner_backend": "simulated",
        "publish_every_cycles": 1,
        "novelty_cycle_priority": "normal",
        "policy_adjustments": [],
        "evidence": [],
        **(policy_overrides or {}),
    }
    write_json(memory_dir / "policy.json", policy)

    return memory_dir


class TestBudgetThroughputAdjustment:
    def test_extra_followups_when_mostly_early(self, tmp_path):
        memory_dir = _setup_budget_env(
            tmp_path,
            hindsight_overrides={
                "throughput_summary": {"total_runs": 4, "early_completion_count": 3},
            },
        )
        budget = build_budget(memory_dir)
        encoder_budget = next(b for b in budget["mechanism_budgets"] if b["mechanism"] == "encoder")
        # With throughput bonus, allowed_followups should be 1 more than baseline
        # Baseline: balanced=2, positive_count>0=+1 => 3. With throughput: 4.
        assert encoder_budget["allowed_followups"] == 4

    def test_no_extra_followups_when_few_early(self, tmp_path):
        memory_dir = _setup_budget_env(
            tmp_path,
            hindsight_overrides={
                "throughput_summary": {"total_runs": 4, "early_completion_count": 1},
            },
        )
        budget = build_budget(memory_dir)
        encoder_budget = next(b for b in budget["mechanism_budgets"] if b["mechanism"] == "encoder")
        # 1/4 < 0.5 so no bonus. Baseline: 2 + 1 (positive) = 3.
        assert encoder_budget["allowed_followups"] == 3

    def test_no_throughput_data(self, tmp_path):
        memory_dir = _setup_budget_env(tmp_path)
        budget = build_budget(memory_dir)
        encoder_budget = next(b for b in budget["mechanism_budgets"] if b["mechanism"] == "encoder")
        assert encoder_budget["allowed_followups"] == 3  # baseline
