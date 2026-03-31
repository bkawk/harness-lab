from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import yaml

from harness_lab.datasets import get_dataset_record, register_dataset
from harness_lab.memory import read_json
from harness_lab.workspace import write_json

CLASS_NAMES = ["plane", "cylinder", "cone", "sphere", "other"]
PARAM_DIM = 8
TYPE_TO_LABEL = {
    "Plane": 0,
    "Cylinder": 1,
    "Cone": 2,
    "Sphere": 3,
}


def list_archive_members(archive: Path) -> list[str]:
    result = subprocess.run(
        ["bsdtar", "-tf", str(archive)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip() and not line.endswith("/")]


def shared_key(member: str) -> str:
    name = Path(member).name
    if "_trimesh_" in name:
        base = name.split("_trimesh_", 1)[0]
    elif "_step_" in name:
        base = name.split("_step_", 1)[0]
    elif "_features_" in name:
        base = name.split("_features_", 1)[0]
    else:
        raise ValueError(f"Unrecognized ABC member name: {member}")
    return f"{Path(member).parent.as_posix()}/{base}"


def build_index(members: list[str]) -> dict[str, str]:
    return {shared_key(member): member for member in members}


def extract_members_bulk(archive: Path, members: list[str], destination_root: Path) -> None:
    destination_root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["bsdtar", "-xf", str(archive), "-C", str(destination_root), *members], check=True)


def build_matched_subset(
    *,
    stl_archive: Path,
    step_archive: Path,
    feat_archive: Path,
    output_dir: Path,
    limit: int,
    offset: int,
) -> dict:
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    stl_index = build_index(list_archive_members(stl_archive))
    step_index = build_index(list_archive_members(step_archive))
    feat_index = build_index(list_archive_members(feat_archive))
    shared = sorted(set(stl_index) & set(step_index) & set(feat_index))
    if not shared:
        raise ValueError("No matched STL/STEP/features entries found across the provided archives.")

    selected = shared[offset : offset + limit]
    if not selected:
        raise ValueError("Requested slice produced an empty selection.")

    stl_members = [stl_index[key] for key in selected]
    step_members = [step_index[key] for key in selected]
    feat_members = [feat_index[key] for key in selected]

    samples = []
    with tempfile.TemporaryDirectory(prefix="harness_lab_abc_extract_") as temp_dir:
        temp_root = Path(temp_dir)
        temp_stl = temp_root / "stl"
        temp_step = temp_root / "step"
        temp_feat = temp_root / "feat"
        extract_members_bulk(stl_archive, stl_members, temp_stl)
        extract_members_bulk(step_archive, step_members, temp_step)
        extract_members_bulk(feat_archive, feat_members, temp_feat)

        for i, key in enumerate(selected):
            sample_id = f"{i + offset:06d}"
            sample_dir = raw_dir / sample_id
            sample_dir.mkdir(parents=True, exist_ok=True)
            stl_member = stl_index[key]
            step_member = step_index[key]
            feat_member = feat_index[key]
            (sample_dir / "mesh.stl").write_bytes((temp_stl / stl_member).read_bytes())
            (sample_dir / "model.step").write_bytes((temp_step / step_member).read_bytes())
            (sample_dir / "features.yml").write_bytes((temp_feat / feat_member).read_bytes())
            samples.append(
                {
                    "sample_id": sample_id,
                    "shared_key": key,
                    "source_files": {
                        "mesh": Path(stl_member).name,
                        "step": Path(step_member).name,
                        "features": Path(feat_member).name,
                    },
                }
            )

    manifest = {
        "count": len(samples),
        "offset": offset,
        "archives": {
            "stl": str(stl_archive),
            "step": str(step_archive),
            "features": str(feat_archive),
        },
        "samples": samples,
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def load_binary_stl(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with path.open("rb") as handle:
        header = handle.read(80)
        if len(header) != 80:
            raise ValueError(f"Invalid STL header in {path}")
        tri_count = int(np.frombuffer(handle.read(4), dtype="<u4")[0])
        data = np.frombuffer(handle.read(), dtype=np.uint8)
    expected = tri_count * 50
    if data.size != expected:
        raise ValueError(f"Unexpected STL payload size in {path}: {data.size} != {expected}")
    tri = data.reshape(tri_count, 50)
    normals = tri[:, :12].view("<f4").reshape(tri_count, 3).astype(np.float32)
    vertices = tri[:, 12:48].view("<f4").reshape(tri_count, 3, 3).astype(np.float32)
    return vertices, normals


def normalize(x: np.ndarray) -> np.ndarray:
    denom = np.linalg.norm(x, axis=-1, keepdims=True)
    denom = np.clip(denom, 1e-8, None)
    return (x / denom).astype(np.float32)


def triangle_areas(vertices: np.ndarray) -> np.ndarray:
    cross = np.cross(vertices[:, 1] - vertices[:, 0], vertices[:, 2] - vertices[:, 0])
    return (0.5 * np.linalg.norm(cross, axis=1)).astype(np.float32)


def parse_surface(surface: dict) -> tuple[int, np.ndarray, np.ndarray]:
    label = TYPE_TO_LABEL.get(surface.get("type"), 4)
    params = np.zeros(PARAM_DIM, dtype=np.float32)
    mask = np.zeros(PARAM_DIM, dtype=np.float32)
    location = np.array(surface.get("location", [0.0, 0.0, 0.0]), dtype=np.float32)

    if label == 0:
        z_axis = np.array(surface.get("z_axis", [0.0, 0.0, 1.0]), dtype=np.float32)
        params[:3] = location
        params[3:6] = normalize(z_axis[None, :])[0]
        mask[:6] = 1.0
    elif label == 1:
        z_axis = np.array(surface.get("z_axis", [0.0, 0.0, 1.0]), dtype=np.float32)
        params[:3] = location
        params[3:6] = normalize(z_axis[None, :])[0]
        params[6] = float(surface.get("radius", 0.0))
        mask[:7] = 1.0
    elif label == 2:
        z_axis = np.array(surface.get("z_axis", [0.0, 0.0, 1.0]), dtype=np.float32)
        radius = float(surface.get("radius", 0.0))
        apex_angle = float(surface.get("angle", 0.0))
        if apex_angle == 0.0 and radius > 0.0:
            apex_angle = math.atan(radius / max(1e-6, np.linalg.norm(location)))
        params[:3] = location
        params[3:6] = normalize(z_axis[None, :])[0]
        params[6] = apex_angle
        params[7] = radius
        mask[:] = 1.0
    elif label == 3:
        params[:3] = location
        params[6] = float(surface.get("radius", 0.0))
        mask[0:3] = 1.0
        mask[6] = 1.0
    return label, params, mask


def sample_points(
    triangles: np.ndarray,
    face_normals: np.ndarray,
    face_labels: np.ndarray,
    face_instance: np.ndarray,
    face_params: np.ndarray,
    face_masks: np.ndarray,
    face_boundary: np.ndarray,
    num_points: int,
    rng: np.random.Generator,
) -> dict[str, np.ndarray]:
    areas = triangle_areas(triangles)
    probs = areas / np.clip(areas.sum(), 1e-8, None)
    face_ids = rng.choice(len(triangles), size=num_points, replace=True, p=probs)
    chosen = triangles[face_ids]
    r1 = np.sqrt(rng.random(num_points, dtype=np.float32))
    r2 = rng.random(num_points, dtype=np.float32)
    points = (
        (1.0 - r1)[:, None] * chosen[:, 0]
        + (r1 * (1.0 - r2))[:, None] * chosen[:, 1]
        + (r1 * r2)[:, None] * chosen[:, 2]
    ).astype(np.float32)
    return {
        "points": points,
        "normals": face_normals[face_ids].astype(np.float32),
        "labels": face_labels[face_ids].astype(np.int64),
        "instance_ids": face_instance[face_ids].astype(np.int64),
        "params": face_params[face_ids].astype(np.float32),
        "param_mask": face_masks[face_ids].astype(np.float32),
        "boundary": face_boundary[face_ids].astype(np.float32),
    }


def vertex_key(vertex: np.ndarray) -> tuple[float, float, float]:
    return tuple(float(x) for x in np.round(vertex.astype(np.float64), decimals=6))


def compute_face_boundary(triangles: np.ndarray, face_labels: np.ndarray) -> np.ndarray:
    edge_to_faces: dict[tuple[tuple[float, float, float], tuple[float, float, float]], list[int]] = {}
    for face_idx, tri in enumerate(triangles):
        verts = [vertex_key(tri[i]) for i in range(3)]
        edges = [
            tuple(sorted((verts[0], verts[1]))),
            tuple(sorted((verts[1], verts[2]))),
            tuple(sorted((verts[2], verts[0]))),
        ]
        for edge in edges:
            edge_to_faces.setdefault(edge, []).append(face_idx)
    face_boundary = np.zeros(len(triangles), dtype=np.float32)
    for adjacent_faces in edge_to_faces.values():
        if len(adjacent_faces) < 2:
            continue
        labels = {int(face_labels[idx]) for idx in adjacent_faces}
        if len(labels) > 1:
            for idx in adjacent_faces:
                face_boundary[idx] = 1.0
    return face_boundary


def convert_sample(sample_dir: Path, output_path: Path, num_points: int, rng: np.random.Generator) -> None:
    triangles, stl_normals = load_binary_stl(sample_dir / "mesh.stl")
    tri_normals = normalize(np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]))
    valid = np.linalg.norm(stl_normals, axis=1) > 1e-6
    face_normals = np.where(valid[:, None], normalize(stl_normals), tri_normals).astype(np.float32)

    with (sample_dir / "features.yml").open("r", encoding="utf-8") as handle:
        features = yaml.safe_load(handle)
    surfaces = features.get("surfaces", [])

    face_labels = np.full(len(triangles), 4, dtype=np.int64)
    face_instance = np.full(len(triangles), -1, dtype=np.int64)
    face_params = np.zeros((len(triangles), PARAM_DIM), dtype=np.float32)
    face_masks = np.zeros((len(triangles), PARAM_DIM), dtype=np.float32)
    for surface_idx, surface in enumerate(surfaces):
        label, params, mask = parse_surface(surface)
        for face_idx in surface.get("face_indices", []):
            if 0 <= face_idx < len(triangles):
                face_labels[face_idx] = label
                face_instance[face_idx] = surface_idx
                face_params[face_idx] = params
                face_masks[face_idx] = mask

    face_boundary = compute_face_boundary(triangles, face_labels)
    sample = sample_points(
        triangles,
        face_normals,
        face_labels,
        face_instance,
        face_params,
        face_masks,
        face_boundary,
        num_points,
        rng,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output_path, **sample)


def process_task(task: tuple[str, str, int, int]) -> None:
    sample_dir_str, output_path_str, num_points, seed = task
    convert_sample(Path(sample_dir_str), Path(output_path_str), num_points, np.random.default_rng(seed))


def preprocess_subset(
    *,
    input_dir: Path,
    output_dir: Path,
    num_points: int,
    val_count: int,
    seed: int,
    workers: int,
) -> dict:
    raw_dir = input_dir / "raw"
    sample_dirs = sorted(path for path in raw_dir.iterdir() if path.is_dir())
    if not sample_dirs:
        raise ValueError(f"No raw sample directories found under {raw_dir}")

    train_dirs = sample_dirs[:-val_count] if val_count < len(sample_dirs) else sample_dirs[:-1]
    val_dirs = sample_dirs[len(train_dirs) :]
    tasks = []
    for split, dirs in [("train", train_dirs), ("val", val_dirs)]:
        for i, sample_dir in enumerate(dirs):
            tasks.append((str(sample_dir), str(output_dir / split / f"{sample_dir.name}.npz"), num_points, seed + len(tasks) + i))

    if workers <= 1:
        for task in tasks:
            process_task(task)
    else:
        with Pool(processes=workers) as pool:
            pool.map(process_task, tasks)

    manifest = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "num_points": num_points,
        "class_names": CLASS_NAMES,
        "train_count": len(train_dirs),
        "val_count": len(val_dirs),
    }
    write_json(output_dir / "preprocess_manifest.json", manifest)
    return manifest


@dataclass(frozen=True)
class Sample:
    points: np.ndarray
    normals: np.ndarray
    labels: np.ndarray
    instance_ids: np.ndarray
    params: np.ndarray
    param_mask: np.ndarray
    boundary: np.ndarray


def resample_points(sample: Sample, num_points: int, rng: np.random.Generator) -> Sample:
    current = sample.points.shape[0]
    if current == num_points:
        return sample
    if current > num_points:
        indices = rng.choice(current, size=num_points, replace=False)
    else:
        extra = rng.choice(current, size=num_points - current, replace=True)
        indices = np.concatenate([np.arange(current), extra], axis=0)
    return Sample(
        points=sample.points[indices].astype(np.float32),
        normals=sample.normals[indices].astype(np.float32),
        labels=sample.labels[indices].astype(np.int64),
        instance_ids=sample.instance_ids[indices].astype(np.int64),
        params=sample.params[indices].astype(np.float32),
        param_mask=sample.param_mask[indices].astype(np.float32),
        boundary=sample.boundary[indices].astype(np.float32),
    )


def validate_sample(sample: Sample, num_points: int) -> None:
    if sample.points.shape != (num_points, 3):
        raise ValueError(f"points must have shape {(num_points, 3)}, got {sample.points.shape}")
    if sample.normals.shape != (num_points, 3):
        raise ValueError(f"normals must have shape {(num_points, 3)}, got {sample.normals.shape}")
    if sample.labels.shape != (num_points,):
        raise ValueError(f"labels must have shape {(num_points,)}, got {sample.labels.shape}")
    if sample.instance_ids.shape != (num_points,):
        raise ValueError(f"instance_ids must have shape {(num_points,)}, got {sample.instance_ids.shape}")
    if sample.params.shape != (num_points, PARAM_DIM):
        raise ValueError(f"params must have shape {(num_points, PARAM_DIM)}, got {sample.params.shape}")
    if sample.param_mask.shape != (num_points, PARAM_DIM):
        raise ValueError(f"param_mask must have shape {(num_points, PARAM_DIM)}, got {sample.param_mask.shape}")
    if sample.boundary.shape != (num_points,):
        raise ValueError(f"boundary must have shape {(num_points,)}, got {sample.boundary.shape}")


def stack_samples(samples: list[Sample]) -> dict[str, np.ndarray]:
    return {
        "points": np.stack([s.points for s in samples], axis=0).astype(np.float32),
        "normals": np.stack([s.normals for s in samples], axis=0).astype(np.float32),
        "labels": np.stack([s.labels for s in samples], axis=0).astype(np.int64),
        "instance_ids": np.stack([s.instance_ids for s in samples], axis=0).astype(np.int64),
        "params": np.stack([s.params for s in samples], axis=0).astype(np.float32),
        "param_mask": np.stack([s.param_mask for s in samples], axis=0).astype(np.float32),
        "boundary": np.stack([s.boundary for s in samples], axis=0).astype(np.float32),
    }


def sample_profile(sample: Sample) -> dict[str, float]:
    labels = sample.labels.astype(np.int64, copy=False)
    unique_labels = np.unique(labels)
    boundary_rate = float(sample.boundary.mean())
    rare_ratio = float(np.mean(labels == 4))
    instance_ratio = float(np.mean(sample.instance_ids >= 0))
    complexity = (
        (boundary_rate * 0.45)
        + (rare_ratio * 0.3)
        + (min(len(unique_labels), len(CLASS_NAMES)) / len(CLASS_NAMES) * 0.15)
        + (instance_ratio * 0.1)
    )
    return {
        "boundary_rate": boundary_rate,
        "rare_ratio": rare_ratio,
        "instance_ratio": instance_ratio,
        "unique_class_count": float(len(unique_labels)),
        "difficulty_score": float(complexity),
    }


def build_eval_slices(val_samples: list[Sample]) -> dict[str, object]:
    count = len(val_samples)
    if count == 0:
        return {
            "strategy": "empty",
            "slices": {},
            "profiles": [],
        }

    profiles = []
    for idx, sample in enumerate(val_samples):
        profile = sample_profile(sample)
        profile["index"] = idx
        profiles.append(profile)

    ranked = sorted(profiles, key=lambda item: (float(item["difficulty_score"]), float(item["boundary_rate"]), int(item["index"])))
    benchmark_idx = [int(item["index"]) for pos, item in enumerate(ranked) if pos % 3 == 0]
    smoke_idx = [int(item["index"]) for pos, item in enumerate(ranked) if pos % 3 == 1]
    audit_idx = [int(item["index"]) for pos, item in enumerate(ranked) if pos % 3 == 2]

    if not smoke_idx:
        smoke_idx = list(benchmark_idx)
    if not audit_idx:
        audit_idx = list(smoke_idx)

    top_boundary = sorted(profiles, key=lambda item: (-float(item["boundary_rate"]), int(item["index"])))
    top_transfer = sorted(profiles, key=lambda item: (-float(item["difficulty_score"]), int(item["index"])))
    focus_count = max(1, min(count, max(2, count // 4)))

    def summarize(indices: list[int]) -> dict[str, object]:
        selected = [profiles[idx] for idx in indices]
        if not selected:
            return {"count": 0}
        return {
            "count": len(indices),
            "avg_boundary_rate": float(sum(float(item["boundary_rate"]) for item in selected) / len(selected)),
            "avg_difficulty_score": float(sum(float(item["difficulty_score"]) for item in selected) / len(selected)),
            "avg_rare_ratio": float(sum(float(item["rare_ratio"]) for item in selected) / len(selected)),
        }

    slices = {
        "benchmark": {"indices": benchmark_idx, "summary": summarize(benchmark_idx)},
        "transfer_smoke": {"indices": smoke_idx, "summary": summarize(smoke_idx)},
        "audit": {"indices": audit_idx, "summary": summarize(audit_idx)},
        "audit_boundary": {
            "indices": [int(item["index"]) for item in top_boundary[:focus_count]],
            "summary": summarize([int(item["index"]) for item in top_boundary[:focus_count]]),
        },
        "audit_transfer": {
            "indices": [int(item["index"]) for item in top_transfer[:focus_count]],
            "summary": summarize([int(item["index"]) for item in top_transfer[:focus_count]]),
        },
    }
    return {
        "strategy": "difficulty_stratified_round_robin",
        "slices": slices,
        "profiles": profiles,
    }


def save_shards(split: str, samples: list[Sample], data_dir: Path, shard_size: int) -> list[dict[str, object]]:
    shard_entries = []
    buffer: list[Sample] = []
    shard_index = 0
    for sample in samples:
        buffer.append(sample)
        if len(buffer) >= shard_size:
            filename = f"{split}_{shard_index:04d}.npz"
            np.savez_compressed(data_dir / filename, **stack_samples(buffer))
            shard_entries.append({"path": filename, "num_samples": len(buffer)})
            buffer.clear()
            shard_index += 1
    if buffer:
        filename = f"{split}_{shard_index:04d}.npz"
        np.savez_compressed(data_dir / filename, **stack_samples(buffer))
        shard_entries.append({"path": filename, "num_samples": len(buffer)})
    return shard_entries


def compute_metadata(
    data_dir: Path,
    num_points: int,
    description: str,
    *,
    eval_slices: dict | None = None,
) -> dict[str, object]:
    split_entries = {}
    class_counts = np.zeros(len(CLASS_NAMES), dtype=np.int64)
    param_sum_sq = np.zeros(PARAM_DIM, dtype=np.float64)
    param_count = np.zeros(PARAM_DIM, dtype=np.float64)
    for split in ("train", "val"):
        entries = []
        for filename in sorted(path.name for path in data_dir.glob(f"{split}_*.npz")):
            with np.load(data_dir / filename) as shard:
                labels = shard["labels"]
                params = shard["params"]
                param_mask = shard["param_mask"]
                class_counts += np.bincount(labels.reshape(-1), minlength=len(CLASS_NAMES)).astype(np.int64)
                if split == "train":
                    param_sum_sq += np.square(params * param_mask).sum(axis=(0, 1))
                    param_count += param_mask.sum(axis=(0, 1))
                entries.append({"path": filename, "num_samples": int(labels.shape[0])})
        split_entries[split] = entries
    param_scale = np.sqrt(param_sum_sq / np.clip(param_count, 1.0, None))
    param_scale = np.clip(param_scale, 1e-2, None)
    return {
        "version": 1,
        "description": description,
        "num_points": int(num_points),
        "param_dim": PARAM_DIM,
        "has_instance_ids": True,
        "class_names": CLASS_NAMES,
        "splits": split_entries,
        "class_counts": class_counts.tolist(),
        "param_scale": param_scale.astype(np.float32).tolist(),
        "eval_slices": eval_slices or {},
    }


def load_external_sample(path: Path, num_points: int, rng: np.random.Generator) -> Sample:
    with np.load(path) as data:
        sample = Sample(
            points=data["points"].astype(np.float32),
            normals=data["normals"].astype(np.float32),
            labels=data["labels"].astype(np.int64),
            instance_ids=data["instance_ids"].astype(np.int64),
            params=data["params"].astype(np.float32),
            param_mask=data["param_mask"].astype(np.float32),
            boundary=data["boundary"].astype(np.float32),
        )
    sample = resample_points(sample, num_points, rng)
    validate_sample(sample, num_points)
    return sample


def build_packed_dataset(*, input_dir: Path, output_dir: Path, num_points: int, shard_size: int, seed: int) -> dict:
    train_files = sorted((input_dir / "train").glob("*.npz"))
    val_files = sorted((input_dir / "val").glob("*.npz"))
    if not train_files or not val_files:
        raise ValueError("pack mode requires at least one .npz file in both train and val")
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("*.npz"):
        stale.unlink()
    if (output_dir / "metadata.json").exists():
        (output_dir / "metadata.json").unlink()
    rng = np.random.default_rng(seed)
    train_samples = [load_external_sample(path, num_points, rng) for path in train_files]
    val_samples = [load_external_sample(path, num_points, rng) for path in val_files]
    eval_slices = build_eval_slices(val_samples)
    save_shards("train", train_samples, output_dir, shard_size)
    save_shards("val", val_samples, output_dir, shard_size)
    metadata = compute_metadata(
        output_dir,
        num_points,
        "Prepared ABC mesh-to-parametric training shards",
        eval_slices=eval_slices,
    )
    write_json(output_dir / "metadata.json", metadata)
    return metadata


def build_prepared_dataset(
    *,
    memory_dir: Path,
    datasets_dir: Path,
    source_dataset_id: str,
    prepared_dataset_id: str,
    limit: int,
    offset: int,
    num_points: int,
    val_count: int,
    shard_size: int,
    seed: int,
    workers: int,
) -> dict:
    source_record = get_dataset_record(memory_dir, source_dataset_id)
    if not source_record:
        raise ValueError(f"Source dataset {source_dataset_id} is not registered.")
    if source_record.get("source") != "abc" or source_record.get("kind") != "abc_source":
        raise ValueError(f"Source dataset {source_dataset_id} is not an abc_source bundle.")

    source_root = Path(str(source_record["local_path"]))
    source_manifest = read_json(source_root / "source_manifest.json")
    prepared_root = datasets_dir / prepared_dataset_id
    subset_dir = prepared_root / "raw_subset"
    preprocess_dir = prepared_root / "preprocessed"
    shards_dir = prepared_root / "shards"
    prepared_root.mkdir(parents=True, exist_ok=True)

    subset_manifest = build_matched_subset(
        stl_archive=Path(source_manifest["inputs"]["stl"]["local_path"]),
        step_archive=Path(source_manifest["inputs"]["step"]["local_path"]),
        feat_archive=Path(source_manifest["inputs"]["features"]["local_path"]),
        output_dir=subset_dir,
        limit=limit,
        offset=offset,
    )
    preprocess_manifest = preprocess_subset(
        input_dir=subset_dir,
        output_dir=preprocess_dir,
        num_points=num_points,
        val_count=val_count,
        seed=seed,
        workers=workers,
    )
    metadata = build_packed_dataset(
        input_dir=preprocess_dir,
        output_dir=shards_dir,
        num_points=num_points,
        shard_size=shard_size,
        seed=seed,
    )

    build_manifest = {
        "source_dataset_id": source_dataset_id,
        "prepared_dataset_id": prepared_dataset_id,
        "limit": limit,
        "offset": offset,
        "num_points": num_points,
        "val_count": val_count,
        "shard_size": shard_size,
        "seed": seed,
        "workers": workers,
        "subset_manifest": str((subset_dir / "manifest.json").relative_to(prepared_root)),
        "preprocess_manifest": str((preprocess_dir / "preprocess_manifest.json").relative_to(prepared_root)),
        "shards_metadata": str((shards_dir / "metadata.json").relative_to(prepared_root)),
        "subset_count": subset_manifest["count"],
        "train_count": preprocess_manifest["train_count"],
        "val_count_actual": preprocess_manifest["val_count"],
    }
    write_json(prepared_root / "build_manifest.json", build_manifest)
    record = register_dataset(
        memory_dir,
        dataset_id=prepared_dataset_id,
        kind="prepared",
        source="abc",
        local_path=prepared_root,
        status="ready",
        notes=f"Prepared from {source_dataset_id} with limit={limit} offset={offset}",
    )
    return {
        "record": record.to_dict(),
        "build_manifest": build_manifest,
        "metadata": metadata,
    }


def ensure_prepared_dataset(
    *,
    memory_dir: Path,
    datasets_dir: Path,
    source_dataset_id: str,
    prepared_dataset_id: str,
    limit: int,
    offset: int,
    num_points: int,
    val_count: int,
    shard_size: int,
    seed: int,
    workers: int,
) -> dict:
    prepared = get_dataset_record(memory_dir, prepared_dataset_id)
    if prepared and prepared.get("status") == "ready" and prepared.get("kind") == "prepared":
        prepared_root = Path(str(prepared["local_path"]))
        metadata_path = prepared_root / "shards" / "metadata.json"
        build_manifest_path = prepared_root / "build_manifest.json"
        return {
            "record": prepared,
            "build_manifest": read_json(build_manifest_path) if build_manifest_path.exists() else {},
            "metadata": read_json(metadata_path) if metadata_path.exists() else {},
            "action": "reused_prepared_dataset",
        }

    payload = build_prepared_dataset(
        memory_dir=memory_dir,
        datasets_dir=datasets_dir,
        source_dataset_id=source_dataset_id,
        prepared_dataset_id=prepared_dataset_id,
        limit=limit,
        offset=offset,
        num_points=num_points,
        val_count=val_count,
        shard_size=shard_size,
        seed=seed,
        workers=workers,
    )
    payload["action"] = "built_prepared_dataset"
    return payload
