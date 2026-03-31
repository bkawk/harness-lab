#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.budget import write_budget


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the current exploration budget from hindsight and policy.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--output", default=None, help="Optional explicit output path. Defaults to artifacts/memory/budget.json.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    memory_dir = Path(args.memory_dir).resolve()
    output_path = Path(args.output).resolve() if args.output else None
    budget_path = write_budget(memory_dir, output_path)
    print(f"memory_dir: {memory_dir}")
    print(f"budget:     {budget_path}")


if __name__ == "__main__":
    main()
