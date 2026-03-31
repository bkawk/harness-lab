from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harness_lab.science_backend import ScienceConfig


def classify_outcome(benchmark_metrics: dict[str, float], audit_metrics: dict[str, float], steps: int) -> tuple[str, list[str]]:
    benchmark = float(benchmark_metrics["val_score"])
    audit = float(audit_metrics["val_score"])
    gap = benchmark - audit
    boundary_f1 = float(audit_metrics.get("boundary_f1", benchmark_metrics.get("boundary_f1", 0.0)))
    if steps < 2:
        return "train_error", ["undertrained"]
    if benchmark >= 0.30 and audit >= benchmark - 0.025:
        return "keeper", []
    if audit >= 0.28 and audit >= benchmark + 0.01:
        return "improved", ["transfer_win"]
    if benchmark >= 0.24:
        if gap > 0.04:
            return "audit_blocked", ["transfer_collapse"]
        if gap > 0.02:
            return "audit_blocked", ["transfer_regression"]
        return "audit_blocked", ["local_only_gain"]
    if boundary_f1 < 0.15:
        return "dead_end", ["weak_boundary_f1"]
    return "dead_end", ["no_gain"]


def should_run_full_audit(
    benchmark_metrics: dict[str, float],
    smoke_metrics_by_name: dict[str, dict[str, float]],
    cfg: ScienceConfig,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    benchmark = float(benchmark_metrics["val_score"])
    if benchmark < cfg.transfer_smoke_min_score:
        reasons.append("benchmark_below_smoke_floor")
    for smoke_name, smoke_metrics in smoke_metrics_by_name.items():
        smoke = float(smoke_metrics["val_score"])
        gap = benchmark - smoke
        boundary_f1 = float(smoke_metrics.get("boundary_f1", 0.0))
        if smoke < cfg.transfer_smoke_min_score:
            reasons.append(f"{smoke_name}:score_below_floor")
        if gap > cfg.transfer_smoke_max_gap:
            reasons.append(f"{smoke_name}:gap_too_wide")
        if boundary_f1 < cfg.transfer_smoke_min_boundary_f1:
            reasons.append(f"{smoke_name}:boundary_f1_too_low")
    return (len(reasons) == 0, reasons)


def classify_smoke_block(
    benchmark_metrics: dict[str, float],
    smoke_metrics_by_name: dict[str, dict[str, float]],
    steps: int,
    smoke_failure_reasons: list[str],
) -> tuple[str, list[str]]:
    if steps < 2:
        return "train_error", ["undertrained"]
    benchmark = float(benchmark_metrics["val_score"])
    primary_smoke = smoke_metrics_by_name.get("transfer_smoke") or next(iter(smoke_metrics_by_name.values()))
    smoke = float(primary_smoke["val_score"])
    if benchmark >= 0.24:
        return "audit_blocked", ["transfer_smoke_failed", *smoke_failure_reasons]
    if any(float(metrics.get("boundary_f1", 0.0)) < 0.15 for metrics in smoke_metrics_by_name.values()):
        return "dead_end", ["weak_boundary_f1", *smoke_failure_reasons]
    if smoke < 0.20:
        return "dead_end", ["smoke_no_gain", *smoke_failure_reasons]
    return "audit_blocked", ["transfer_smoke_failed", *smoke_failure_reasons]
