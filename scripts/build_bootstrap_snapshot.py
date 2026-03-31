#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.bootstrap import write_bootstrap_snapshot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a candidate bootstrap snapshot from current lab state.")
    parser.add_argument("candidate_id")
    parser.add_argument("--candidates-dir", type=Path, default=Path("artifacts/candidates"))
    parser.add_argument("--memory-dir", type=Path, default=Path("artifacts/memory"))
    parser.add_argument("--parent-id", default=None)
    parser.add_argument("--dataset-id", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = write_bootstrap_snapshot(
        args.candidates_dir,
        args.memory_dir,
        args.candidate_id,
        parent_id=args.parent_id,
        dataset_id=args.dataset_id,
        synthesis=None,
    )
    print(path)


if __name__ == "__main__":
    main()
