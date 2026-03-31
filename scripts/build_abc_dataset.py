#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from harness_lab.abc_dataset import build_prepared_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a prepared local ABC dataset artifact from a bootstrapped ABC source bundle."
    )
    parser.add_argument("source_dataset_id", help="Registered abc_source dataset id, e.g. abc_raw_v1")
    parser.add_argument("prepared_dataset_id", help="Prepared dataset id to write, e.g. abc_boundary512")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--datasets-dir", default="artifacts/datasets", help="Directory for dataset artifacts.")
    parser.add_argument("--limit", type=int, default=16, help="How many matched ABC samples to extract.")
    parser.add_argument("--offset", type=int, default=0, help="Offset into the matched ABC keyspace.")
    parser.add_argument("--num-points", type=int, default=2048, help="Points to sample per object.")
    parser.add_argument("--val-count", type=int, default=1, help="How many samples to reserve for validation.")
    parser.add_argument("--shard-size", type=int, default=128, help="Samples per packed shard.")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for reproducible sampling.")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) // 2), help="Preprocess worker count.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = build_prepared_dataset(
        memory_dir=Path(args.memory_dir).resolve(),
        datasets_dir=Path(args.datasets_dir).resolve(),
        source_dataset_id=args.source_dataset_id,
        prepared_dataset_id=args.prepared_dataset_id,
        limit=args.limit,
        offset=args.offset,
        num_points=args.num_points,
        val_count=args.val_count,
        shard_size=args.shard_size,
        seed=args.seed,
        workers=args.workers,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
