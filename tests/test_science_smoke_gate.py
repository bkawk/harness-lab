from __future__ import annotations

from harness_lab.science_backend import (
    ScienceConfig,
    classify_smoke_block,
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

