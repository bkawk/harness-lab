from __future__ import annotations

from harness_lab.science_backend import (
    ScienceConfig,
    classify_smoke_block,
    derive_config,
    should_run_full_audit,
)


def test_smoke_gate_allows_full_audit_for_stable_transfer():
    cfg = ScienceConfig()
    benchmark = {"val_score": 0.31, "boundary_f1": 0.24}
    smoke = {
        "transfer_smoke": {"val_score": 0.295, "boundary_f1": 0.22},
        "boundary_smoke": {"val_score": 0.29, "boundary_f1": 0.2},
    }
    allowed, reasons = should_run_full_audit(benchmark, smoke, cfg)
    assert allowed is True
    assert reasons == []


def test_smoke_gate_blocks_full_audit_for_transfer_collapse():
    cfg = ScienceConfig()
    benchmark = {"val_score": 0.31, "boundary_f1": 0.24}
    smoke = {
        "transfer_smoke": {"val_score": 0.25, "boundary_f1": 0.2},
        "boundary_smoke": {"val_score": 0.29, "boundary_f1": 0.2},
    }
    allowed, reasons = should_run_full_audit(benchmark, smoke, cfg)
    assert allowed is False
    assert "transfer_smoke:gap_too_wide" in reasons


def test_smoke_gate_blocks_boundary_specific_collapse():
    cfg = ScienceConfig()
    benchmark = {"val_score": 0.31, "boundary_f1": 0.24}
    smoke = {
        "transfer_smoke": {"val_score": 0.30, "boundary_f1": 0.2},
        "boundary_smoke": {"val_score": 0.29, "boundary_f1": 0.08},
    }
    allowed, reasons = should_run_full_audit(benchmark, smoke, cfg)
    assert allowed is False
    assert "boundary_smoke:boundary_f1_too_low" in reasons


def test_smoke_block_classifies_promising_candidate_as_audit_blocked():
    outcome_label, failure_modes = classify_smoke_block(
        {"val_score": 0.28, "boundary_f1": 0.22},
        {"transfer_smoke": {"val_score": 0.22, "boundary_f1": 0.17}},
        12,
        ["transfer_smoke:gap_too_wide"],
    )
    assert outcome_label == "audit_blocked"
    assert failure_modes[0] == "transfer_smoke_gap_too_wide"


def test_smoke_block_surfaces_boundary_specific_primary_failure():
    outcome_label, failure_modes = classify_smoke_block(
        {"val_score": 0.31, "boundary_f1": 0.24},
        {
            "transfer_smoke": {"val_score": 0.30, "boundary_f1": 0.2},
            "boundary_smoke": {"val_score": 0.29, "boundary_f1": 0.08},
        },
        12,
        ["boundary_smoke:boundary_f1_too_low"],
    )
    assert outcome_label == "audit_blocked"
    assert failure_modes[0] == "boundary_transfer_weak"


def test_smoke_block_marks_severe_boundary_transfer_as_dead_end():
    outcome_label, failure_modes = classify_smoke_block(
        {"val_score": 0.31, "boundary_f1": 0.24},
        {
            "transfer_smoke": {"val_score": 0.29, "boundary_f1": 0.19},
            "boundary_smoke": {"val_score": 0.22, "boundary_f1": 0.08},
        },
        12,
        ["boundary_smoke:gap_too_wide", "boundary_smoke:boundary_f1_too_low"],
    )
    assert outcome_label == "dead_end"
    assert failure_modes[0] == "boundary_transfer_weak"


def test_smoke_block_marks_multi_slice_gap_failures_as_dead_end():
    outcome_label, failure_modes = classify_smoke_block(
        {"val_score": 0.32, "boundary_f1": 0.24},
        {
            "transfer_smoke": {"val_score": 0.25, "boundary_f1": 0.2},
            "hard_transfer_smoke": {"val_score": 0.24, "boundary_f1": 0.19},
        },
        12,
        ["transfer_smoke:gap_too_wide", "hard_transfer_smoke:gap_too_wide"],
    )
    assert outcome_label == "dead_end"
    assert failure_modes[0] == "hard_transfer_regression"


def test_derive_config_supports_eval_reserve_override(monkeypatch):
    monkeypatch.setenv("HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS", "600")
    monkeypatch.setenv("HARNESS_LAB_SCIENCE_EVAL_RESERVE_SECONDS", "120")
    cfg = derive_config("cand_0099", {"target": {}, "changes": []}, {})
    assert cfg.time_budget_seconds == 600
    assert cfg.eval_reserve_seconds == 120
