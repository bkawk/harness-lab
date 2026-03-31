from __future__ import annotations

from pathlib import Path

import numpy as np

from harness_lab.abc_dataset import Sample, build_eval_slices, compute_metadata
from harness_lab.science_data import make_transfer_eval_splits
from harness_lab.workspace import write_json


def _sample(boundary_rate: float, rare_ratio: float, instance_ratio: float, num_points: int = 12) -> Sample:
    rare_count = int(num_points * rare_ratio)
    normal_count = num_points - rare_count
    labels = np.array(([4] * rare_count) + ([0] * normal_count), dtype=np.int64)
    boundary = np.zeros(num_points, dtype=np.float32)
    boundary[: int(num_points * boundary_rate)] = 1.0
    instance_ids = np.full(num_points, -1, dtype=np.int64)
    instance_ids[: int(num_points * instance_ratio)] = 0
    return Sample(
        points=np.zeros((num_points, 3), dtype=np.float32),
        normals=np.zeros((num_points, 3), dtype=np.float32),
        labels=labels,
        instance_ids=instance_ids,
        params=np.zeros((num_points, 8), dtype=np.float32),
        param_mask=np.zeros((num_points, 8), dtype=np.float32),
        boundary=boundary,
    )


def test_build_eval_slices_creates_named_stratified_subsets():
    samples = [
        _sample(0.05, 0.0, 0.1),
        _sample(0.10, 0.1, 0.2),
        _sample(0.20, 0.2, 0.3),
        _sample(0.30, 0.3, 0.4),
        _sample(0.40, 0.4, 0.5),
        _sample(0.50, 0.5, 0.6),
    ]
    payload = build_eval_slices(samples)
    slices = payload["slices"]
    assert payload["strategy"] == "difficulty_stratified_round_robin"
    assert set(slices) >= {"benchmark", "transfer_smoke", "audit", "audit_boundary", "audit_transfer"}
    assert slices["benchmark"]["summary"]["count"] >= 1
    assert slices["transfer_smoke"]["summary"]["count"] >= 1
    assert slices["audit"]["summary"]["count"] >= 1


def test_make_transfer_eval_splits_prefers_named_slices(tmp_path):
    dataset_root = tmp_path / "dataset"
    shards_dir = dataset_root / "shards"
    shards_dir.mkdir(parents=True)
    np.savez_compressed(
        shards_dir / "val_0000.npz",
        points=np.zeros((6, 4, 3), dtype=np.float32),
        normals=np.zeros((6, 4, 3), dtype=np.float32),
        labels=np.zeros((6, 4), dtype=np.int64),
        instance_ids=np.zeros((6, 4), dtype=np.int64),
        params=np.zeros((6, 4, 8), dtype=np.float32),
        param_mask=np.zeros((6, 4, 8), dtype=np.float32),
        boundary=np.zeros((6, 4), dtype=np.float32),
    )
    metadata = compute_metadata(
        shards_dir,
        4,
        "test shards",
        eval_slices={
            "strategy": "named",
            "slices": {
                "benchmark": {"indices": [0, 3], "summary": {"count": 2}},
                "transfer_smoke": {"indices": [1, 4], "summary": {"count": 2}},
                "audit": {"indices": [2, 5], "summary": {"count": 2}},
            },
        },
    )
    write_json(shards_dir / "metadata.json", metadata)
    benchmark, smoke, audit = make_transfer_eval_splits(dataset_root)
    assert len(benchmark) == 2
    assert len(smoke) == 2
    assert len(audit) == 2
