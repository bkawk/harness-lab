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
    smoke = {"val_score": 0.295, "boundary_f1": 0.22}
    allowed, reasons = should_run_full_audit(benchmark, smoke, cfg)
    assert allowed is True
    assert reasons == []


def test_smoke_gate_blocks_full_audit_for_transfer_collapse():
    cfg = ScienceConfig()
    benchmark = {"val_score": 0.31, "boundary_f1": 0.24}
    smoke = {"val_score": 0.25, "boundary_f1": 0.2}
    allowed, reasons = should_run_full_audit(benchmark, smoke, cfg)
    assert allowed is False
    assert "smoke_transfer_gap_too_wide" in reasons


def test_smoke_block_classifies_promising_candidate_as_audit_blocked():
    outcome_label, failure_modes = classify_smoke_block(
        {"val_score": 0.28, "boundary_f1": 0.22},
        {"val_score": 0.22, "boundary_f1": 0.17},
        12,
        ["smoke_transfer_gap_too_wide"],
    )
    assert outcome_label == "audit_blocked"
    assert failure_modes[0] == "transfer_smoke_failed"


def test_derive_config_supports_eval_reserve_override(monkeypatch):
    monkeypatch.setenv("HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS", "600")
    monkeypatch.setenv("HARNESS_LAB_SCIENCE_EVAL_RESERVE_SECONDS", "120")
    cfg = derive_config("cand_0099", {"target": {}, "changes": []}, {})
    assert cfg.time_budget_seconds == 600
    assert cfg.eval_reserve_seconds == 120
