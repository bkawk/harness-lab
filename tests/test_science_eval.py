from harness_lab.science_eval import classify_outcome


def test_classify_outcome_marks_keeper_for_strong_transfer():
    outcome_label, failure_modes = classify_outcome(
        {"val_score": 0.31, "boundary_f1": 0.20},
        {"val_score": 0.295, "boundary_f1": 0.22},
        steps=10,
    )

    assert outcome_label == "keeper"
    assert failure_modes == []


def test_classify_outcome_adds_boundary_and_audit_specific_failure_reasons():
    outcome_label, failure_modes = classify_outcome(
        {"val_score": 0.36, "boundary_f1": 0.39},
        {"val_score": 0.27, "boundary_f1": 0.27},
        steps=10,
    )

    assert outcome_label == "audit_blocked"
    assert failure_modes[0] == "transfer_collapse"
    assert "audit_score_below_keeper_band" in failure_modes
    assert "boundary_transfer_regression" in failure_modes
    assert "audit_boundary_f1_weak" in failure_modes
