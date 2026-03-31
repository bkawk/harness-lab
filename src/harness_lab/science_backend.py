from __future__ import annotations

import json
import time
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
from harness_lab.science_model import CompactPointModel
from harness_lab.science_eval import classify_outcome, classify_smoke_block, should_run_full_audit
from harness_lab.science_train import ScienceRunResult, run_training_cycle, write_science_progress


def get_device() -> torch.device:
    import os

    requested = os.environ.get("HARNESS_LAB_SCIENCE_DEVICE", "").strip()
    if requested:
        return torch.device(requested)
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


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
    return run_training_cycle(
        candidate_id=candidate_id,
        trace_dir=trace_dir,
        model=model,
        optimizer=optimizer,
        train_loader=train_loader,
        benchmark_loader=benchmark_loader,
        smoke_loaders=smoke_loaders,
        audit_loader=audit_loader,
        cfg=cfg,
        param_scale=param_scale,
        num_classes=num_classes,
        device=device,
        metadata=metadata,
        train_dataset=train_dataset,
        benchmark_dataset=benchmark_dataset,
        smoke_datasets=smoke_datasets,
        audit_dataset=audit_dataset,
    )
