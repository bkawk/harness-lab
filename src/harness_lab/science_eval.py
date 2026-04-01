from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harness_lab.science_config import ScienceConfig


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _smoke_primary_failure(smoke_failure_reasons: list[str]) -> str:
    if any(reason.startswith("boundary_smoke:boundary_f1_too_low") for reason in smoke_failure_reasons):
        return "boundary_transfer_weak"
    if any(reason.startswith("hard_transfer_smoke:gap_too_wide") for reason in smoke_failure_reasons):
        return "hard_transfer_regression"
    if any(reason.startswith("boundary_smoke:gap_too_wide") for reason in smoke_failure_reasons):
        return "boundary_transfer_regression"
    if any(reason.startswith("transfer_smoke:gap_too_wide") for reason in smoke_failure_reasons):
        return "transfer_smoke_gap_too_wide"
    if any(reason.endswith(":score_below_floor") for reason in smoke_failure_reasons):
        return "transfer_smoke_score_below_floor"
    return "transfer_smoke_failed"


def _count_smoke_gap_failures(smoke_failure_reasons: list[str]) -> int:
    return sum(1 for reason in smoke_failure_reasons if reason.endswith(":gap_too_wide"))


def _should_hard_fail_after_smoke(
    benchmark_metrics: dict[str, float],
    smoke_metrics_by_name: dict[str, dict[str, float]],
    smoke_failure_reasons: list[str],
) -> bool:
    benchmark = float(benchmark_metrics["val_score"])
    primary_smoke = smoke_metrics_by_name.get("transfer_smoke") or next(iter(smoke_metrics_by_name.values()))
    smoke = float(primary_smoke["val_score"])
    gap = benchmark - smoke
    boundary_metrics = smoke_metrics_by_name.get("boundary_smoke", {})
    boundary_f1 = float(boundary_metrics.get("boundary_f1", 1.0))

    if "hard_transfer_smoke:gap_too_wide" in smoke_failure_reasons:
        return True
    if "boundary_smoke:gap_too_wide" in smoke_failure_reasons and (
        "boundary_smoke:boundary_f1_too_low" in smoke_failure_reasons or boundary_f1 < 0.15
    ):
        return True
    if _count_smoke_gap_failures(smoke_failure_reasons) >= 2:
        return True
    if gap >= 0.07:
        return True
    return False


def classify_outcome(benchmark_metrics: dict[str, float], audit_metrics: dict[str, float], steps: int) -> tuple[str, list[str]]:
    benchmark = float(benchmark_metrics["val_score"])
    audit = float(audit_metrics["val_score"])
    gap = benchmark - audit
    benchmark_boundary_f1 = float(benchmark_metrics.get("boundary_f1", 0.0))
    audit_boundary_f1 = float(audit_metrics.get("boundary_f1", benchmark_boundary_f1))
    boundary_gap = benchmark_boundary_f1 - audit_boundary_f1
    if steps < 2:
        return "train_error", ["undertrained"]
    if benchmark >= 0.30 and audit >= benchmark - 0.025:
        return "keeper", []
    if audit >= 0.28 and audit >= benchmark + 0.01:
        return "improved", ["transfer_win"]
    if benchmark >= 0.24:
        reasons: list[str] = []
        if gap > 0.04:
            _append_unique(reasons, "transfer_collapse")
        elif gap > 0.02:
            _append_unique(reasons, "transfer_regression")
        else:
            _append_unique(reasons, "local_only_gain")
        if audit < 0.28:
            _append_unique(reasons, "audit_score_below_keeper_band")
        if boundary_gap > 0.05:
            _append_unique(reasons, "boundary_transfer_regression")
        if audit_boundary_f1 < 0.28:
            _append_unique(reasons, "audit_boundary_f1_weak")
        return "audit_blocked", reasons
    if audit_boundary_f1 < 0.15:
        return "dead_end", ["weak_boundary_f1", "audit_boundary_f1_weak"]
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
    primary_failure = _smoke_primary_failure(smoke_failure_reasons)
    severe_smoke_failure = _should_hard_fail_after_smoke(
        benchmark_metrics,
        smoke_metrics_by_name,
        smoke_failure_reasons,
    )
    if benchmark >= 0.24:
        if severe_smoke_failure:
            return "dead_end", [primary_failure, *smoke_failure_reasons]
        return "audit_blocked", [primary_failure, *smoke_failure_reasons]
    if any(float(metrics.get("boundary_f1", 0.0)) < 0.15 for metrics in smoke_metrics_by_name.values()):
        return "dead_end", ["weak_boundary_f1", primary_failure, *smoke_failure_reasons]
    if smoke < 0.20:
        return "dead_end", ["smoke_no_gain", primary_failure, *smoke_failure_reasons]
    return "audit_blocked", [primary_failure, *smoke_failure_reasons]
