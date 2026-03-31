from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from shutil import copy2, copytree, rmtree

from harness_lab.memory import read_json
from harness_lab.workspace import write_json


@dataclass(frozen=True)
class DatasetRecord:
    dataset_id: str
    kind: str
    source: str
    local_path: str
    status: str
    notes: str

    def to_dict(self) -> dict:
        return {
            "dataset_id": self.dataset_id,
            "kind": self.kind,
            "source": self.source,
            "local_path": self.local_path,
            "status": self.status,
            "notes": self.notes,
        }


def dataset_registry_path(memory_dir: Path) -> Path:
    return memory_dir / "datasets.json"


def read_dataset_registry(memory_dir: Path) -> dict:
    path = dataset_registry_path(memory_dir)
    if not path.exists():
        return {"datasets": []}
    return read_json(path)


def get_dataset_record(memory_dir: Path, dataset_id: str) -> dict | None:
    registry = read_dataset_registry(memory_dir)
    for item in registry.get("datasets", []):
        if item.get("dataset_id") == dataset_id:
            return item
    return None


def _safe_read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def prepared_dataset_quality(record: dict) -> dict:
    local_path = Path(str(record.get("local_path", "")))
    build_manifest = _safe_read_json(local_path / "build_manifest.json")
    metadata = _safe_read_json(local_path / "shards" / "metadata.json")
    preprocess_manifest = {}
    preprocess_path = build_manifest.get("preprocess_manifest")
    if preprocess_path:
        preprocess_manifest = _safe_read_json(local_path / str(preprocess_path))

    splits = metadata.get("splits", {}) if isinstance(metadata, dict) else {}
    train_samples = int(
        build_manifest.get("train_count")
        or preprocess_manifest.get("train_count")
        or sum(int(entry.get("num_samples", 0) or 0) for entry in splits.get("train", []))
    )
    val_samples = int(
        build_manifest.get("val_count_actual")
        or preprocess_manifest.get("val_count")
        or sum(int(entry.get("num_samples", 0) or 0) for entry in splits.get("val", []))
    )
    num_points = int(metadata.get("num_points", 0) or 0)
    eval_slices = metadata.get("eval_slices", {}) if isinstance(metadata, dict) else {}
    slice_map = eval_slices.get("slices", {}) if isinstance(eval_slices, dict) else {}
    named_eval_slices = len(slice_map) if isinstance(slice_map, dict) else 0
    score = 0
    if train_samples > 0:
        score += min(train_samples, 4096)
    if val_samples > 0:
        score += min(val_samples * 64, 4096)
    if num_points > 0:
        score += min(num_points // 4, 1024)
    if build_manifest:
        score += 256
    if named_eval_slices >= 3:
        score += 384
    if val_samples >= 16:
        score += 512
    if val_samples >= 64:
        score += 1024
    return {
        "dataset_id": str(record.get("dataset_id", "")),
        "train_samples": train_samples,
        "val_samples": val_samples,
        "num_points": num_points,
        "named_eval_slices": named_eval_slices,
        "has_build_manifest": bool(build_manifest),
        "score": score,
    }


def choose_best_prepared_dataset(memory_dir: Path) -> dict | None:
    registry = read_dataset_registry(memory_dir)
    candidates = [
        item
        for item in registry.get("datasets", [])
        if item.get("source") == "abc" and item.get("status") == "ready" and item.get("kind") == "prepared"
    ]
    if not candidates:
        return None
    ranked = sorted(
        candidates,
        key=lambda item: (
            prepared_dataset_quality(item)["score"],
            prepared_dataset_quality(item)["val_samples"],
            prepared_dataset_quality(item)["train_samples"],
            str(item.get("dataset_id", "")),
        ),
        reverse=True,
    )
    return ranked[0]


def write_dataset_registry(memory_dir: Path, payload: dict) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = dataset_registry_path(memory_dir)
    write_json(path, payload)
    return path


def register_dataset(
    memory_dir: Path,
    *,
    dataset_id: str,
    kind: str,
    source: str,
    local_path: Path,
    status: str = "ready",
    notes: str = "",
) -> DatasetRecord:
    registry = read_dataset_registry(memory_dir)
    datasets = [item for item in registry.get("datasets", []) if item.get("dataset_id") != dataset_id]
    record = DatasetRecord(
        dataset_id=dataset_id,
        kind=kind,
        source=source,
        local_path=str(local_path),
        status=status,
        notes=notes,
    )
    datasets.append(record.to_dict())
    datasets.sort(key=lambda item: item["dataset_id"])
    write_dataset_registry(memory_dir, {"datasets": datasets})
    return record


def stage_local_dataset_path(
    datasets_dir: Path,
    *,
    dataset_id: str,
    source_path: Path,
    link_name: str | None = None,
) -> Path:
    datasets_dir.mkdir(parents=True, exist_ok=True)
    if not source_path.exists():
        raise FileNotFoundError(f"Source dataset path does not exist: {source_path}")

    target_name = link_name or dataset_id
    target_path = datasets_dir / target_name
    if source_path.is_dir():
        if target_path.exists() or target_path.is_symlink():
            target_path.unlink()
        target_path.symlink_to(source_path)
        return target_path

    target_path.parent.mkdir(parents=True, exist_ok=True)
    copy2(source_path, target_path)
    return target_path


def import_dataset_copy(
    memory_dir: Path,
    datasets_dir: Path,
    *,
    dataset_id: str,
    source_path: Path,
    source_label: str,
    kind: str = "prepared",
    notes: str = "",
) -> DatasetRecord:
    datasets_dir.mkdir(parents=True, exist_ok=True)
    if not source_path.exists():
        raise FileNotFoundError(f"Source dataset path does not exist: {source_path}")

    target_path = datasets_dir / dataset_id
    if target_path.exists():
        if target_path.is_symlink() or target_path.is_file():
            target_path.unlink()
        else:
            rmtree(target_path)
    if source_path.is_dir():
        copytree(source_path, target_path, dirs_exist_ok=True)
    else:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_path, target_path)

    return register_dataset(
        memory_dir,
        dataset_id=dataset_id,
        kind=kind,
        source=source_label,
        local_path=target_path,
        status="ready",
        notes=notes or f"Imported by copy from {source_path}",
    )
