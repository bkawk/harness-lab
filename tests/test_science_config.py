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
