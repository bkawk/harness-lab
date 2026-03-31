#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.policy import write_policy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the current lab policy from memory, hindsight, and hardware context.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--output", default=None, help="Optional explicit output path. Defaults to artifacts/memory/policy.json.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidates_dir = Path(args.candidates_dir).resolve()
    memory_dir = Path(args.memory_dir).resolve()
    output_path = Path(args.output).resolve() if args.output else None
    if not candidates_dir.exists():
        raise SystemExit(f"Candidates directory does not exist: {candidates_dir}")
    policy_path = write_policy(candidates_dir, memory_dir, output_path)
    print(f"candidates_dir: {candidates_dir}")
    print(f"policy:         {policy_path}")


if __name__ == "__main__":
    main()
