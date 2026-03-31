from harness_lab.science_eval import classify_outcome


def test_classify_outcome_marks_keeper_for_strong_transfer():
    outcome_label, failure_modes = classify_outcome(
        {"val_score": 0.31, "boundary_f1": 0.20},
        {"val_score": 0.295, "boundary_f1": 0.22},
        steps=10,
    )

    assert outcome_label == "keeper"
    assert failure_modes == []
