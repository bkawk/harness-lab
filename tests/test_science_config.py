from harness_lab.science_config import ScienceConfig, apply_oom_backoff, derive_config


def test_derive_config_supports_eval_reserve_override(monkeypatch):
    monkeypatch.setenv("HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS", "600")
    monkeypatch.setenv("HARNESS_LAB_SCIENCE_EVAL_RESERVE_SECONDS", "120")

    cfg = derive_config("cand_0099", {"target": {}, "changes": []}, {})

    assert cfg.time_budget_seconds == 600
    assert cfg.eval_reserve_seconds == 120


def test_apply_oom_backoff_reduces_pressure():
    cfg = ScienceConfig(batch_size=2, eval_batch_size=2, hidden_dim=160, global_dim=256, instance_dim=24, k_neighbors=10, instance_loss_weight=0.08)

    reduced = apply_oom_backoff(cfg, free_gb=1.5)

    assert reduced.batch_size == 1
    assert reduced.eval_batch_size == 1
    assert reduced.hidden_dim <= cfg.hidden_dim
    assert reduced.global_dim <= cfg.global_dim
    assert reduced.instance_dim <= cfg.instance_dim
    assert reduced.k_neighbors <= cfg.k_neighbors
    assert reduced.instance_loss_weight <= cfg.instance_loss_weight


def test_derive_config_applies_bounded_backend_levers():
    cfg = derive_config(
        "cand_0100",
        {
            "target": {},
            "changes": [],
            "backend_levers": {
                "science_model": {"hidden_dim": 999, "k_neighbors": 12},
                "science_loss": {"instance_loss_weight": 0.12},
                "science_eval": {"transfer_smoke_max_gap": 0.02},
                "science_train": {"batch_size": 3},
            },
        },
        {},
    )

    assert cfg.hidden_dim == 192
    assert cfg.k_neighbors == 12
    assert cfg.instance_loss_weight == 0.12
    assert cfg.transfer_smoke_max_gap == 0.02
    assert cfg.batch_size == 3


def test_derive_config_strengthens_boundary_transfer_seed_defaults():
    cfg = derive_config(
        "cand_0101",
        {
            "target": {
                "harness_component": "science_loss",
                "expected_failure_mode": "boundary_smoke:gap_too_wide",
            },
            "changes": [],
        },
        {},
    )

    assert cfg.boundary_loss_weight >= 0.12
    assert cfg.instance_loss_weight >= 0.06
    assert cfg.k_neighbors >= 8


def test_derive_config_strengthens_hard_transfer_seed_defaults():
    cfg = derive_config(
        "cand_0102",
        {
            "target": {
                "harness_component": "science_loss",
                "expected_failure_mode": "hard_transfer_regression",
            },
            "changes": [],
        },
        {},
    )

    assert cfg.boundary_loss_weight >= 0.12
    assert cfg.instance_loss_weight >= 0.06
    assert cfg.instance_margin >= 0.38
    assert cfg.k_neighbors >= 8
