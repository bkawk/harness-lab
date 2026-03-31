from __future__ import annotations

import json
import math
import os
import time
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import torch

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

    if "transfer" in expected_failure or "audit" in expected_failure or "transfer" in mechanism:
        cfg = ScienceConfig(
            **{**asdict(cfg), "lr": min(cfg.lr, 2.5e-4), "weight_decay": 2e-4, "instance_loss_weight": min(cfg.instance_loss_weight, 0.04)}
        )
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
    override = os.environ.get("HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS", "").strip()
    if override:
        cfg = ScienceConfig(**{**asdict(cfg), "time_budget_seconds": int(float(override))})
    eval_reserve_override = os.environ.get("HARNESS_LAB_SCIENCE_EVAL_RESERVE_SECONDS", "").strip()
    if eval_reserve_override:
        cfg = ScienceConfig(**{**asdict(cfg), "eval_reserve_seconds": int(float(eval_reserve_override))})
    return cfg


def get_device() -> torch.device:
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
    oom_retry = str(os.environ.get("HARNESS_LAB_SCIENCE_OOM_RETRY", "1")).strip().lower() in {"1", "true", "yes"}
    if device.type == "cuda" and oom_retry:
        free_bytes, total_bytes = torch.cuda.mem_get_info(device)
        free_gb = free_bytes / (1024**3)
        total_gb = total_bytes / (1024**3)
        if free_gb < 2.0:
            cfg = ScienceConfig(
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
