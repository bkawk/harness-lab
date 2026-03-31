from __future__ import annotations

import json
import math
import time
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import torch

from harness_lab.science_config import ScienceConfig, apply_oom_backoff, derive_config
from harness_lab.science_data import (
    PackedShardDataset,
    evaluate_model,
    get_dataset_spec,
    load_metadata,
    make_dataloader,
    make_transfer_eval_splits,
    move_batch_to_device,
)
from harness_lab.science_eval import classify_outcome, classify_smoke_block, should_run_full_audit
from harness_lab.science_loss import compute_loss
from harness_lab.science_model import CompactPointModel


@dataclass(frozen=True)
class ScienceRunResult:
    config: dict[str, object]
    benchmark_metrics: dict[str, float]
    smoke_metrics: dict[str, float]
    audit_metrics: dict[str, float]
    training_seconds: float
    steps: int
    peak_vram_mb: int
    device: str
    train_loss: float
    outcome_label: str
    observed_failure_modes: list[str]
    benchmark_summary: str
    audit_summary: str
    evidence: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_science_progress(trace_dir: Path, phase: str, **payload: object) -> None:
    trace_dir.mkdir(parents=True, exist_ok=True)
    progress = {
        "updated_at": utc_now(),
        "phase": phase,
        **payload,
    }
    (trace_dir / "science_progress.json").write_text(
        json.dumps(progress, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    details = " ".join(f"{key}={value}" for key, value in payload.items())
    if details:
        print(f"science-progress: {phase} {details}", flush=True)
    else:
        print(f"science-progress: {phase}", flush=True)


def get_device() -> torch.device:
    import os

    requested = os.environ.get("HARNESS_LAB_SCIENCE_DEVICE", "").strip()
    if requested:
        return torch.device(requested)
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def peak_vram_mb(device: torch.device) -> int:
    if device.type == "cuda":
        return int(torch.cuda.max_memory_allocated(device) / (1024 * 1024))
    return 0


def run_science_backend(
    *,
    candidate_id: str,
    dataset_root: Path,
    proposal: dict,
    diagnosis: dict,
    trace_dir: Path,
) -> ScienceRunResult:
    torch.manual_seed(1337 + _deterministic_index(candidate_id, 1000))
    if hasattr(torch, "set_float32_matmul_precision"):
        torch.set_float32_matmul_precision("high")

    trace_dir.mkdir(parents=True, exist_ok=True)
    write_science_progress(trace_dir, "initializing", candidate_id=candidate_id)
    cfg = derive_config(candidate_id, proposal, diagnosis)
    metadata = load_metadata(dataset_root)
    spec = get_dataset_spec(dataset_root)
    device = get_device()
    import os

    oom_retry = str(os.environ.get("HARNESS_LAB_SCIENCE_OOM_RETRY", "1")).strip().lower() in {"1", "true", "yes"}
    if device.type == "cuda" and oom_retry:
        free_bytes, total_bytes = torch.cuda.mem_get_info(device)
        free_gb = free_bytes / (1024**3)
        total_gb = total_bytes / (1024**3)
        if free_gb < 2.0:
            cfg = apply_oom_backoff(cfg, free_gb=free_gb)
            write_science_progress(
                trace_dir,
                "oom_backoff_applied",
                candidate_id=candidate_id,
                free_gb=round(free_gb, 3),
                total_gb=round(total_gb, 3),
                batch_size=cfg.batch_size,
                eval_batch_size=cfg.eval_batch_size,
                hidden_dim=cfg.hidden_dim,
                global_dim=cfg.global_dim,
                instance_dim=cfg.instance_dim,
                k_neighbors=cfg.k_neighbors,
                instance_loss_weight=cfg.instance_loss_weight,
            )
    write_science_progress(
        trace_dir,
        "config_ready",
        candidate_id=candidate_id,
        time_budget_seconds=cfg.time_budget_seconds,
        eval_reserve_seconds=cfg.eval_reserve_seconds,
        total_wall_clock_budget_seconds=cfg.time_budget_seconds + cfg.eval_reserve_seconds,
        batch_size=cfg.batch_size,
        eval_batch_size=cfg.eval_batch_size,
        hidden_dim=cfg.hidden_dim,
        global_dim=cfg.global_dim,
        k_neighbors=cfg.k_neighbors,
    )
    param_scale = torch.tensor(spec.param_scale, dtype=torch.float32, device=device)
    num_classes = len(spec.class_names)
    write_science_progress(
        trace_dir,
        "dataset_loaded",
        candidate_id=candidate_id,
        device=device.type,
        train_splits=len(metadata.get("splits", {}).get("train", [])),
        val_splits=len(metadata.get("splits", {}).get("val", [])),
        num_classes=num_classes,
    )

    train_dataset = PackedShardDataset(dataset_root, "train")
    benchmark_dataset, smoke_datasets, audit_dataset = make_transfer_eval_splits(dataset_root)
    train_loader = make_dataloader(train_dataset, cfg.batch_size, shuffle=True, drop_last=True)
    benchmark_loader = make_dataloader(benchmark_dataset, cfg.eval_batch_size, shuffle=False)
    smoke_loaders = {
        name: make_dataloader(dataset, cfg.eval_batch_size, shuffle=False)
        for name, dataset in smoke_datasets.items()
    }
    audit_loader = make_dataloader(audit_dataset, cfg.eval_batch_size, shuffle=False)
    write_science_progress(
        trace_dir,
        "dataloaders_ready",
        candidate_id=candidate_id,
        train_samples=len(train_dataset),
        benchmark_samples=len(benchmark_dataset),
        smoke_samples=sum(len(dataset) for dataset in smoke_datasets.values()),
        smoke_slice_counts={name: len(dataset) for name, dataset in smoke_datasets.items()},
        audit_samples=len(audit_dataset),
    )

    model = CompactPointModel(
        num_classes=num_classes,
        param_dim=spec.param_dim,
        hidden_dim=cfg.hidden_dim,
        global_dim=cfg.global_dim,
        instance_dim=cfg.instance_dim,
        k_neighbors=cfg.k_neighbors,
        instance_modulation_scale=cfg.instance_modulation_scale,
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    write_science_progress(
        trace_dir,
        "model_ready",
        candidate_id=candidate_id,
        device=device.type,
        parameter_count=sum(param.numel() for param in model.parameters()),
    )

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)

    train_iter = iter(train_loader)
    start = time.time()
    train_deadline = start + cfg.time_budget_seconds
    steps = 0
    last_stats = {"loss": math.nan, "cls_loss": math.nan, "param_loss": math.nan, "boundary_loss": math.nan, "instance_loss": math.nan}
    last_progress_emit = start
    write_science_progress(
        trace_dir,
        "training_started",
        candidate_id=candidate_id,
        train_budget_seconds=cfg.time_budget_seconds,
        eval_reserve_seconds=cfg.eval_reserve_seconds,
        total_wall_clock_budget_seconds=cfg.time_budget_seconds + cfg.eval_reserve_seconds,
    )

    while time.time() < train_deadline:
        try:
            batch = next(train_iter)
        except StopIteration:
            train_iter = iter(train_loader)
            batch = next(train_iter)
        batch = move_batch_to_device(batch, device)
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits, param_pred, boundary_logits, instance_embed = model(batch["points"], batch["normals"])
        loss, last_stats = compute_loss(
            logits,
            param_pred,
            boundary_logits,
            instance_embed,
            batch,
            param_scale=param_scale,
            cfg=cfg,
        )
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        optimizer.step()
        steps += 1
        now = time.time()
        if steps == 1 or steps % cfg.log_interval == 0 or (now - last_progress_emit) >= 30.0:
            elapsed = now - start
            write_science_progress(
                trace_dir,
                "training",
                candidate_id=candidate_id,
                steps=steps,
                elapsed_seconds=round(elapsed, 3),
                remaining_seconds=max(0.0, round(train_deadline - now, 3)),
                loss=round(float(last_stats["loss"]), 6),
                cls_loss=round(float(last_stats["cls_loss"]), 6),
                param_loss=round(float(last_stats["param_loss"]), 6),
                boundary_loss=round(float(last_stats["boundary_loss"]), 6),
                instance_loss=round(float(last_stats["instance_loss"]), 6),
                peak_vram_mb=peak_vram_mb(device),
            )
            last_progress_emit = now

    training_seconds = time.time() - start
    write_science_progress(
        trace_dir,
        "training_complete",
        candidate_id=candidate_id,
        steps=steps,
        training_seconds=round(training_seconds, 3),
        eval_reserve_seconds=cfg.eval_reserve_seconds,
        peak_vram_mb=peak_vram_mb(device),
    )
    write_science_progress(trace_dir, "benchmark_eval_started", candidate_id=candidate_id, steps=steps)
    benchmark_metrics = evaluate_model(model, benchmark_loader, device, param_scale=param_scale, num_classes=num_classes)
    write_science_progress(
        trace_dir,
        "benchmark_eval_complete",
        candidate_id=candidate_id,
        benchmark_score=round(float(benchmark_metrics["val_score"]), 6),
        benchmark_boundary_f1=round(float(benchmark_metrics.get("boundary_f1", 0.0)), 6),
    )
    smoke_metrics_by_name: dict[str, dict[str, float]] = {}
    for smoke_name, smoke_loader in smoke_loaders.items():
        write_science_progress(trace_dir, "smoke_eval_started", candidate_id=candidate_id, smoke_name=smoke_name)
        smoke_metrics_by_name[smoke_name] = evaluate_model(model, smoke_loader, device, param_scale=param_scale, num_classes=num_classes)
        write_science_progress(
            trace_dir,
            "smoke_eval_complete",
            candidate_id=candidate_id,
            smoke_name=smoke_name,
            smoke_score=round(float(smoke_metrics_by_name[smoke_name]["val_score"]), 6),
            smoke_boundary_f1=round(float(smoke_metrics_by_name[smoke_name].get("boundary_f1", 0.0)), 6),
        )
    primary_smoke_metrics = smoke_metrics_by_name.get("transfer_smoke") or next(iter(smoke_metrics_by_name.values()))
    full_audit_completed, smoke_failure_reasons = should_run_full_audit(benchmark_metrics, smoke_metrics_by_name, cfg)
    if full_audit_completed:
        write_science_progress(trace_dir, "audit_eval_started", candidate_id=candidate_id)
        audit_metrics = evaluate_model(model, audit_loader, device, param_scale=param_scale, num_classes=num_classes)
        write_science_progress(
            trace_dir,
            "audit_eval_complete",
            candidate_id=candidate_id,
            audit_score=round(float(audit_metrics["val_score"]), 6),
            audit_boundary_f1=round(float(audit_metrics.get("boundary_f1", 0.0)), 6),
        )
        outcome_label, observed_failure_modes = classify_outcome(benchmark_metrics, audit_metrics, steps)
    else:
        audit_metrics = dict(primary_smoke_metrics)
        audit_metrics["audit_skipped_after_smoke"] = True
        audit_metrics["smoke_failure_reasons"] = list(smoke_failure_reasons)
        audit_metrics["smoke_metrics_by_name"] = smoke_metrics_by_name
        write_science_progress(
            trace_dir,
            "audit_skipped_after_smoke",
            candidate_id=candidate_id,
            smoke_failure_reasons=",".join(smoke_failure_reasons),
        )
        outcome_label, observed_failure_modes = classify_smoke_block(benchmark_metrics, smoke_metrics_by_name, steps, smoke_failure_reasons)

    benchmark_summary = (
        f"Real science backend trained {candidate_id} for {training_seconds:.1f}s on {metadata['splits']['train'][0]['path'].split('/')[0] if metadata.get('splits') else 'train'} "
        f"and scored {benchmark_metrics['val_score']:.6f} on the benchmark validation slice."
    )
    if full_audit_completed:
        audit_summary = (
            f"Audit slice score was {audit_metrics['val_score']:.6f} with macro_iou {audit_metrics['macro_iou']:.6f} "
            f"and param_score {audit_metrics['param_score']:.6f}."
        )
    else:
        audit_summary = (
            f"Transfer smoke score was {primary_smoke_metrics['val_score']:.6f}; full audit was skipped after smoke gate "
            f"({', '.join(smoke_failure_reasons)})."
        )
    evidence = [
        "backend:science",
        f"science:device:{device.type}",
        f"science:steps:{steps}",
        f"science:train_seconds:{training_seconds:.1f}",
        f"science:benchmark:{benchmark_metrics['val_score']:.6f}",
        f"science:smoke:{primary_smoke_metrics['val_score']:.6f}",
        f"science:audit:{audit_metrics['val_score']:.6f}",
        f"science:full_audit_completed:{str(full_audit_completed).lower()}",
        f"science:transfer_gap:{(benchmark_metrics['val_score'] - audit_metrics['val_score']):.6f}",
        f"science:smoke_gap:{(benchmark_metrics['val_score'] - primary_smoke_metrics['val_score']):.6f}",
        f"science:benchmark_boundary_f1:{benchmark_metrics.get('boundary_f1', 0.0):.6f}",
        f"science:smoke_boundary_f1:{primary_smoke_metrics.get('boundary_f1', 0.0):.6f}",
        f"science:audit_boundary_f1:{audit_metrics.get('boundary_f1', 0.0):.6f}",
        f"science:train_samples:{len(train_dataset)}",
        f"science:val_benchmark_samples:{len(benchmark_dataset)}",
        f"science:val_smoke_samples:{sum(len(dataset) for dataset in smoke_datasets.values())}",
        f"science:val_audit_samples:{len(audit_dataset)}",
    ]

    (trace_dir / "science_config.json").write_text(json.dumps(asdict(cfg), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (trace_dir / "science_metrics.json").write_text(
        json.dumps(
            {
                "benchmark_metrics": benchmark_metrics,
                "smoke_metrics": primary_smoke_metrics,
                "smoke_metrics_by_name": smoke_metrics_by_name,
                "audit_metrics": audit_metrics,
                "full_audit_completed": full_audit_completed,
                "smoke_failure_reasons": smoke_failure_reasons,
                "benchmark_audit_gap": float(benchmark_metrics["val_score"] - audit_metrics["val_score"]),
                "benchmark_smoke_gap": float(benchmark_metrics["val_score"] - primary_smoke_metrics["val_score"]),
                "training_seconds": training_seconds,
                "steps": steps,
                "peak_vram_mb": peak_vram_mb(device),
                "device": device.type,
                "last_train_stats": last_stats,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    write_science_progress(
        trace_dir,
        "result_ready",
        candidate_id=candidate_id,
        outcome_label=outcome_label,
        benchmark_score=round(float(benchmark_metrics["val_score"]), 6),
        audit_score=round(float(audit_metrics["val_score"]), 6),
    )

    return ScienceRunResult(
        config=asdict(cfg),
        benchmark_metrics=benchmark_metrics,
        smoke_metrics=primary_smoke_metrics,
        audit_metrics=audit_metrics,
        training_seconds=training_seconds,
        steps=steps,
        peak_vram_mb=peak_vram_mb(device),
        device=device.type,
        train_loss=float(last_stats["loss"]),
        outcome_label=outcome_label,
        observed_failure_modes=observed_failure_modes,
        benchmark_summary=benchmark_summary,
        audit_summary=audit_summary,
        evidence=evidence,
    )
