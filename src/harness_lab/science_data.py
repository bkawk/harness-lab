from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, Subset


@dataclass(frozen=True)
class DatasetSpec:
    class_names: tuple[str, ...]
    num_points: int
    param_dim: int
    param_scale: tuple[float, ...]


def shards_dir(dataset_root: Path) -> Path:
    return dataset_root / "shards"


def load_metadata(dataset_root: Path) -> dict[str, object]:
    path = shards_dir(dataset_root) / "metadata.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing shard metadata at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def get_dataset_spec(dataset_root: Path) -> DatasetSpec:
    metadata = load_metadata(dataset_root)
    return DatasetSpec(
        class_names=tuple(metadata["class_names"]),
        num_points=int(metadata["num_points"]),
        param_dim=int(metadata["param_dim"]),
        param_scale=tuple(float(x) for x in metadata["param_scale"]),
    )


class PackedShardDataset(Dataset):
    def __init__(self, dataset_root: Path, split: str):
        metadata = load_metadata(dataset_root)
        if split not in metadata["splits"]:
            raise ValueError(f"Unknown split {split!r}")
        self.dataset_root = dataset_root
        self.split = split
        self.entries = list(metadata["splits"][split])
        if not self.entries:
            raise ValueError(f"Split {split!r} is empty")
        self.cumulative: list[int] = []
        total = 0
        for entry in self.entries:
            total += int(entry["num_samples"])
            self.cumulative.append(total)

    def __len__(self) -> int:
        return self.cumulative[-1]

    @lru_cache(maxsize=8)
    def _load_shard(self, shard_index: int) -> dict[str, np.ndarray]:
        path = shards_dir(self.dataset_root) / self.entries[shard_index]["path"]
        with np.load(path) as data:
            labels = data["labels"].astype(np.int64)
            return {
                "points": data["points"].astype(np.float32),
                "normals": data["normals"].astype(np.float32),
                "labels": labels,
                "instance_ids": data["instance_ids"].astype(np.int64)
                if "instance_ids" in data
                else np.full(labels.shape, -1, dtype=np.int64),
                "params": data["params"].astype(np.float32),
                "param_mask": data["param_mask"].astype(np.float32),
                "boundary": data["boundary"].astype(np.float32)
                if "boundary" in data
                else np.zeros(labels.shape, dtype=np.float32),
            }

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        if index < 0 or index >= len(self):
            raise IndexError(index)
        shard_index = int(np.searchsorted(self.cumulative, index, side="right"))
        prev_total = 0 if shard_index == 0 else self.cumulative[shard_index - 1]
        local_index = index - prev_total
        shard = self._load_shard(shard_index)
        return {
            "points": torch.from_numpy(shard["points"][local_index]),
            "normals": torch.from_numpy(shard["normals"][local_index]),
            "labels": torch.from_numpy(shard["labels"][local_index]),
            "instance_ids": torch.from_numpy(shard["instance_ids"][local_index]),
            "params": torch.from_numpy(shard["params"][local_index]),
            "param_mask": torch.from_numpy(shard["param_mask"][local_index]),
            "boundary": torch.from_numpy(shard["boundary"][local_index]),
        }


def make_dataloader(
    dataset: Dataset,
    batch_size: int,
    *,
    shuffle: bool,
    drop_last: bool = False,
) -> DataLoader:
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,
        drop_last=drop_last,
        pin_memory=torch.cuda.is_available(),
    )


def make_eval_splits(dataset_root: Path) -> tuple[Dataset, Dataset]:
    val_dataset = PackedShardDataset(dataset_root, "val")
    count = len(val_dataset)
    if count < 2:
        return val_dataset, val_dataset
    midpoint = max(1, count // 2)
    benchmark = Subset(val_dataset, range(0, midpoint))
    audit = Subset(val_dataset, range(midpoint, count))
    if len(audit) == 0:
        audit = benchmark
    return benchmark, audit


def make_transfer_eval_splits(dataset_root: Path) -> tuple[Dataset, Dataset, Dataset]:
    val_dataset = PackedShardDataset(dataset_root, "val")
    metadata = load_metadata(dataset_root)
    eval_slices = metadata.get("eval_slices", {}) if isinstance(metadata, dict) else {}
    slice_map = eval_slices.get("slices", {}) if isinstance(eval_slices, dict) else {}
    if isinstance(slice_map, dict) and slice_map:
        def _subset(name: str) -> Dataset | None:
            payload = slice_map.get(name, {})
            indices = [int(i) for i in payload.get("indices", []) if 0 <= int(i) < len(val_dataset)]
            if not indices:
                return None
            return Subset(val_dataset, indices)

        benchmark = _subset("benchmark")
        smoke = _subset("transfer_smoke")
        audit = _subset("audit")
        if benchmark is not None and smoke is not None and audit is not None:
            return benchmark, smoke, audit

    count = len(val_dataset)
    if count < 3:
        return val_dataset, val_dataset, val_dataset

    benchmark_midpoint = max(1, count // 2)
    benchmark = Subset(val_dataset, range(0, benchmark_midpoint))

    remaining_start = benchmark_midpoint
    remaining_count = count - remaining_start
    smoke_count = max(1, remaining_count // 2)
    smoke_end = min(count, remaining_start + smoke_count)
    smoke = Subset(val_dataset, range(remaining_start, smoke_end))
    audit = Subset(val_dataset, range(smoke_end, count))

    if len(smoke) == 0:
        smoke = benchmark
    if len(audit) == 0:
        audit = smoke
    return benchmark, smoke, audit


def move_batch_to_device(batch: dict[str, torch.Tensor], device: torch.device) -> dict[str, torch.Tensor]:
    moved: dict[str, torch.Tensor] = {}
    for key, value in batch.items():
        if value.dtype.is_floating_point:
            moved[key] = value.to(device=device, dtype=torch.float32, non_blocking=True)
        else:
            moved[key] = value.to(device=device, non_blocking=True)
    return moved


def confusion_matrix(pred: torch.Tensor, target: torch.Tensor, num_classes: int) -> torch.Tensor:
    flat = (target.reshape(-1) * num_classes + pred.reshape(-1)).detach().cpu().numpy().astype(np.int64, copy=False)
    bins = np.bincount(flat, minlength=num_classes * num_classes)
    return torch.from_numpy(bins.reshape(num_classes, num_classes))


@torch.no_grad()
def evaluate_model(
    model: torch.nn.Module,
    dataloader: DataLoader,
    device: torch.device,
    *,
    param_scale: torch.Tensor,
    num_classes: int,
) -> dict[str, float]:
    model.eval()
    accum_dtype = torch.float32
    total_confusion = torch.zeros((num_classes, num_classes), dtype=accum_dtype, device=device)
    total_sq_error = torch.zeros(1, dtype=accum_dtype, device=device)
    total_param_count = torch.zeros(1, dtype=accum_dtype, device=device)
    boundary_tp = torch.zeros(1, dtype=accum_dtype, device=device)
    boundary_fp = torch.zeros(1, dtype=accum_dtype, device=device)
    boundary_fn = torch.zeros(1, dtype=accum_dtype, device=device)

    for batch in dataloader:
        batch = move_batch_to_device(batch, device)
        logits, param_pred, boundary_logits, _ = model(batch["points"], batch["normals"])
        pred_labels = logits.argmax(dim=-1)
        total_confusion += confusion_matrix(pred_labels, batch["labels"], num_classes).to(device=device, dtype=accum_dtype)

        scale = param_scale.view(1, 1, -1)
        diff = (param_pred - batch["params"]) / scale
        masked_sq = diff.square() * batch["param_mask"]
        total_sq_error += masked_sq.sum(dtype=accum_dtype)
        total_param_count += batch["param_mask"].sum(dtype=accum_dtype)
        boundary_pred = torch.sigmoid(boundary_logits) >= 0.5
        boundary_target = batch["boundary"] >= 0.5
        boundary_tp += (boundary_pred & boundary_target).sum(dtype=accum_dtype)
        boundary_fp += (boundary_pred & ~boundary_target).sum(dtype=accum_dtype)
        boundary_fn += (~boundary_pred & boundary_target).sum(dtype=accum_dtype)

    intersection = total_confusion.diag()
    union = total_confusion.sum(dim=1) + total_confusion.sum(dim=0) - intersection
    valid = union > 0
    per_class_iou = torch.zeros_like(intersection)
    per_class_iou[valid] = intersection[valid] / union[valid]
    macro_iou = float(per_class_iou[valid].mean().item()) if valid.any() else 0.0

    denom = torch.clamp(total_param_count, min=1.0)
    param_rmse_norm = float(torch.sqrt(total_sq_error / denom).item())
    param_score = 1.0 / (1.0 + param_rmse_norm)
    boundary_precision = float((boundary_tp / torch.clamp(boundary_tp + boundary_fp, min=1.0)).item())
    boundary_recall = float((boundary_tp / torch.clamp(boundary_tp + boundary_fn, min=1.0)).item())
    boundary_f1 = (
        2.0 * boundary_precision * boundary_recall / max(boundary_precision + boundary_recall, 1e-8)
        if (boundary_precision + boundary_recall) > 0.0
        else 0.0
    )
    val_score = 0.7 * macro_iou + 0.3 * param_score
    return {
        "val_score": float(val_score),
        "macro_iou": float(macro_iou),
        "per_class_iou": [float(x) for x in per_class_iou.detach().cpu().tolist()],
        "param_rmse_norm": float(param_rmse_norm),
        "param_score": float(param_score),
        "boundary_precision": float(boundary_precision),
        "boundary_recall": float(boundary_recall),
        "boundary_f1": float(boundary_f1),
    }
