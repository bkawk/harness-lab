from __future__ import annotations

import os
from dataclasses import asdict
from dataclasses import dataclass


@dataclass(frozen=True)
class ScienceConfig:
    batch_size: int = 2
    eval_batch_size: int = 2
    lr: float = 3e-4
    weight_decay: float = 1e-4
    hidden_dim: int = 128
    global_dim: int = 192
    param_loss_weight: float = 0.2
    boundary_loss_weight: float = 0.1
    instance_loss_weight: float = 0.05
    grad_clip: float = 1.0
    log_interval: int = 20
    k_neighbors: int = 8
    instance_dim: int = 16
    instance_margin: float = 0.35
    instance_modulation_scale: float = 0.1
    time_budget_seconds: int = 600
    eval_reserve_seconds: int = 120
    transfer_smoke_min_score: float = 0.24
    transfer_smoke_max_gap: float = 0.03
    transfer_smoke_min_boundary_f1: float = 0.12


def _proposal_signature(proposal: dict) -> str:
    target = proposal.get("target", {})
    changes = proposal.get("changes", [])
    bits = [
        str(target.get("harness_component", "")).strip(),
        str(target.get("expected_failure_mode", "")).strip(),
        str(target.get("novelty_basis", "")).strip(),
        *(str(item.get("kind", "")).strip() for item in changes),
        *(str(item.get("summary", "")).strip() for item in changes[:4]),
    ]
    return "|".join(bit for bit in bits if bit)


def _deterministic_index(text: str, modulo: int) -> int:
    total = sum(ord(ch) for ch in text)
    return total % modulo if modulo > 0 else 0


def deterministic_index(text: str, modulo: int) -> int:
    return _deterministic_index(text, modulo)


def _clamp_int(value: object, minimum: int, maximum: int) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return max(minimum, min(maximum, int(value)))


def _clamp_float(value: object, minimum: float, maximum: float) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return max(minimum, min(maximum, float(value)))


def _apply_backend_levers(cfg: ScienceConfig, proposal: dict) -> ScienceConfig:
    lever_groups = proposal.get("backend_levers", {})
    if not isinstance(lever_groups, dict):
        return cfg
    values = asdict(cfg)
    applied = False
    int_specs = {
        "hidden_dim": (64, 192),
        "global_dim": (96, 320),
        "instance_dim": (8, 32),
        "k_neighbors": (4, 16),
        "batch_size": (1, 4),
        "eval_batch_size": (1, 4),
        "log_interval": (5, 100),
        "time_budget_seconds": (300, 900),
        "eval_reserve_seconds": (60, 240),
    }
    float_specs = {
        "instance_modulation_scale": (0.0, 0.25),
        "param_loss_weight": (0.05, 0.5),
        "boundary_loss_weight": (0.01, 0.3),
        "instance_loss_weight": (0.0, 0.15),
        "instance_margin": (0.1, 0.6),
        "transfer_smoke_min_score": (0.15, 0.35),
        "transfer_smoke_max_gap": (0.01, 0.08),
        "transfer_smoke_min_boundary_f1": (0.05, 0.25),
        "lr": (1e-4, 6e-4),
        "weight_decay": (1e-5, 5e-4),
        "grad_clip": (0.5, 2.0),
    }
    for module_name in ("science_model", "science_loss", "science_eval", "science_config", "science_train"):
        module_levers = lever_groups.get(module_name, {})
        if not isinstance(module_levers, dict):
            continue
        for field, raw in module_levers.items():
            if field in int_specs:
                value = _clamp_int(raw, *int_specs[field])
            elif field in float_specs:
                value = _clamp_float(raw, *float_specs[field])
            else:
                value = None
            if value is None:
                continue
            values[field] = value
            applied = True
    return ScienceConfig(**values) if applied else cfg


def derive_config(candidate_id: str, proposal: dict, diagnosis: dict) -> ScienceConfig:
    signature = f"{candidate_id}|{_proposal_signature(proposal)}|{diagnosis.get('summary', '')}"
    lr_choices = [2.0e-4, 3.0e-4, 4.0e-4]
    hidden_choices = [96, 128, 160]
    global_choices = [128, 192, 256]
    instance_choices = [12, 16, 24]
    modulation_choices = [0.05, 0.1, 0.15]
    boundary_choices = [0.05, 0.1, 0.15]
    instance_loss_choices = [0.02, 0.05, 0.08]
    neighbor_choices = [6, 8, 10]
    budget_choices = [540, 600, 660]

    cfg = ScienceConfig(
        lr=lr_choices[_deterministic_index(signature + "lr", len(lr_choices))],
        hidden_dim=hidden_choices[_deterministic_index(signature + "hidden", len(hidden_choices))],
        global_dim=global_choices[_deterministic_index(signature + "global", len(global_choices))],
        k_neighbors=neighbor_choices[_deterministic_index(signature + "neighbors", len(neighbor_choices))],
        instance_dim=instance_choices[_deterministic_index(signature + "instance_dim", len(instance_choices))],
        instance_modulation_scale=modulation_choices[_deterministic_index(signature + "instance_mod", len(modulation_choices))],
        boundary_loss_weight=boundary_choices[_deterministic_index(signature + "boundary", len(boundary_choices))],
        instance_loss_weight=instance_loss_choices[_deterministic_index(signature + "instance_loss", len(instance_loss_choices))],
        time_budget_seconds=budget_choices[_deterministic_index(signature + "budget", len(budget_choices))],
    )

    mechanism = str(proposal.get("target", {}).get("harness_component", "")).strip().lower()
    expected_failure = str(proposal.get("target", {}).get("expected_failure_mode", "")).strip().lower()
    change_kinds = {str(item.get("kind", "")).strip().lower() for item in proposal.get("changes", [])}
    boundary_expected = "boundary" in expected_failure
    hard_transfer_expected = "hard_transfer" in expected_failure

    if "transfer" in expected_failure or "audit" in expected_failure or "transfer" in mechanism or boundary_expected:
        transfer_updates = {
            **asdict(cfg),
            "lr": min(cfg.lr, 2.5e-4),
            "weight_decay": 2e-4,
        }
        if hard_transfer_expected:
            transfer_updates["boundary_loss_weight"] = max(cfg.boundary_loss_weight, 0.12)
            transfer_updates["instance_loss_weight"] = max(cfg.instance_loss_weight, 0.06)
            transfer_updates["instance_margin"] = max(cfg.instance_margin, 0.38)
            transfer_updates["k_neighbors"] = max(cfg.k_neighbors, 8)
        elif boundary_expected:
            transfer_updates["boundary_loss_weight"] = max(cfg.boundary_loss_weight, 0.12)
            transfer_updates["instance_loss_weight"] = max(cfg.instance_loss_weight, 0.06)
            transfer_updates["k_neighbors"] = max(cfg.k_neighbors, 8)
        else:
            transfer_updates["instance_loss_weight"] = min(cfg.instance_loss_weight, 0.04)
        cfg = ScienceConfig(**transfer_updates)
    if "budget_guardrail" in change_kinds or "diversity_warning" in change_kinds:
        cfg = ScienceConfig(
            **{
                **asdict(cfg),
                "hidden_dim": min(cfg.hidden_dim, 128),
                "global_dim": min(cfg.global_dim, 192),
                "k_neighbors": min(cfg.k_neighbors, 8),
            }
        )
    if "exploration_jump" in change_kinds:
        cfg = ScienceConfig(
            **{
                **asdict(cfg),
                "instance_dim": max(cfg.instance_dim, 16),
                "instance_loss_weight": min(0.1, cfg.instance_loss_weight + 0.02),
                "instance_modulation_scale": max(cfg.instance_modulation_scale, 0.1),
                "k_neighbors": max(cfg.k_neighbors, 8),
            }
        )
    cfg = _apply_backend_levers(cfg, proposal)
    override = os.environ.get("HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS", "").strip()
    if override:
        cfg = ScienceConfig(**{**asdict(cfg), "time_budget_seconds": int(float(override))})
    eval_reserve_override = os.environ.get("HARNESS_LAB_SCIENCE_EVAL_RESERVE_SECONDS", "").strip()
    if eval_reserve_override:
        cfg = ScienceConfig(**{**asdict(cfg), "eval_reserve_seconds": int(float(eval_reserve_override))})
    return cfg


def apply_oom_backoff(cfg: ScienceConfig, *, free_gb: float) -> ScienceConfig:
    if free_gb >= 2.0:
        return cfg
    return ScienceConfig(
        **{
            **asdict(cfg),
            "batch_size": 1,
            "eval_batch_size": 1,
            "hidden_dim": min(cfg.hidden_dim, 96),
            "global_dim": min(cfg.global_dim, 128),
            "instance_dim": min(cfg.instance_dim, 12),
            "k_neighbors": min(cfg.k_neighbors, 6),
            "instance_loss_weight": min(cfg.instance_loss_weight, 0.02),
        }
    )
