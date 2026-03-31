#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

from harness_lab.big_bang import run_big_bang


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the long-lived harness-lab supervisor loop. This is the first self-evolving control plane."
    )
    parser.add_argument("--repo-dir", default=".", help="Repository root.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--datasets-dir", default="artifacts/datasets", help="Directory for dataset artifacts.")
    parser.add_argument("--source-dataset-id", default="abc_raw_v1", help="Registered abc_source dataset id.")
    parser.add_argument("--prepared-dataset-id", default="abc_boundary512", help="Prepared dataset id for execution.")
    parser.add_argument("--limit", type=int, default=512, help="How many matched ABC samples to extract if rebuilding.")
    parser.add_argument("--offset", type=int, default=0, help="Offset into the matched ABC keyspace.")
    parser.add_argument("--num-points", type=int, default=2048, help="Points to sample per object.")
    parser.add_argument("--val-count", type=int, default=64, help="How many samples to reserve for validation.")
    parser.add_argument("--shard-size", type=int, default=128, help="Samples per packed shard.")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for reproducible sampling.")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) // 2), help="Preprocess worker count.")
    parser.add_argument("--interval-seconds", type=int, default=30, help="Delay between big-bang cycles.")
    parser.add_argument("--cycles", type=int, default=1, help="How many cycles to run. Use 0 for endless mode.")
    parser.add_argument("--no-publish", action="store_true", help="Do not self-publish tracked evolution after each cycle.")
    parser.add_argument("--runner-backend", default="auto", help="Runner backend to use. `auto` follows the current policy.")
    return parser


def main() -> None:
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    args = build_parser().parse_args()
    result = run_big_bang(
        repo_dir=Path(args.repo_dir).resolve(),
        candidates_dir=Path(args.candidates_dir).resolve(),
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
        interval_seconds=args.interval_seconds,
        cycles=args.cycles,
        publish=not args.no_publish,
        runner_backend=args.runner_backend,
    )
    print(f"cycles_completed: {result.cycles_completed}")
    print(f"last_candidate:   {result.last_candidate_id or '-'}")
    print(f"last_commit:      {result.last_commit_sha or '-'}")
    print(f"state_path:       {result.status_path}")
    print(f"dashboard_path:   {result.dashboard_path}")


if __name__ == "__main__":
    main()
