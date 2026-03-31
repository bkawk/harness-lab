#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

from harness_lab.orchestrator import run_lab_step


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one self-evolving harness-lab step: ensure data, create the next candidate, advance the loop, optionally publish."
    )
    parser.add_argument("--repo-dir", default=".", help="Repository root.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--datasets-dir", default="artifacts/datasets", help="Directory for dataset artifacts.")
    parser.add_argument("--source-dataset-id", default="abc_raw_v1", help="Registered abc_source dataset id.")
    parser.add_argument("--prepared-dataset-id", default="abc_boundary512", help="Prepared dataset id for execution.")
    parser.add_argument("--candidate-id", default=None, help="Optional explicit candidate id.")
    parser.add_argument("--parent-id", default=None, help="Optional explicit parent candidate id.")
    parser.add_argument("--limit", type=int, default=512, help="How many matched ABC samples to extract if rebuilding.")
    parser.add_argument("--offset", type=int, default=0, help="Offset into the matched ABC keyspace.")
    parser.add_argument("--num-points", type=int, default=2048, help="Points to sample per object.")
    parser.add_argument("--val-count", type=int, default=64, help="How many samples to reserve for validation.")
    parser.add_argument("--shard-size", type=int, default=128, help="Samples per packed shard.")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed for reproducible sampling.")
    parser.add_argument("--workers", type=int, default=None, help="Preprocess worker count.")
    parser.add_argument("--no-finalize-outcome", action="store_true", help="Only draft and plan; do not finalize outcome.")
    parser.add_argument("--no-simulate-outcome", action="store_true", help="Skip simulated outcome generation.")
    parser.add_argument("--runner-backend", default="simulated", help="Runner backend to use.")
    parser.add_argument("--publish", action="store_true", help="Commit and push tracked structural evolution after the step.")
    parser.add_argument("--publish-message", default=None, help="Commit message when publishing.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_lab_step(
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
        workers=args.workers or max(1, (os.cpu_count() or 4) // 2),
        candidate_id=args.candidate_id,
        parent_id=args.parent_id,
        finalize_outcome=not args.no_finalize_outcome,
        simulate_outcome=not args.no_simulate_outcome,
        runner_backend=args.runner_backend,
        publish=args.publish,
        publish_message=args.publish_message,
    )
    print(f"candidate_id:      {result.candidate_id}")
    print(f"dataset_action:    {result.dataset_action}")
    print(f"dataset_id:        {result.dataset_id}")
    print(f"seed_action:       {result.seed_action}")
    print(f"proposal_status:   {result.loop.proposal_status}")
    print(f"execution_status:  {result.loop.execution_status}")
    print(f"outcome_status:    {result.loop.outcome_status}")
    print(f"diagnosis_status:  {result.loop.diagnosis_status}")
    print(f"next_top_parent:   {result.loop.top_parent_id or '-'}")
    print(f"published:         {result.published}")
    print(f"publish_commit:    {result.commit_sha or '-'}")
    print(f"publish_message:   {result.publish_message}")


if __name__ == "__main__":
    main()
