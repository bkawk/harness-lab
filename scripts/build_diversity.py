#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.diversity import write_diversity


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the current branch diversity artifact from recent candidate history.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--output", default="artifacts/memory/diversity.json", help="Output JSON path for diversity state.")
    parser.add_argument("--window", type=int, default=6, help="How many recent candidates to consider.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidates_dir = Path(args.candidates_dir).resolve()
    output_path = Path(args.output).resolve()
    if not candidates_dir.exists():
        raise SystemExit(f"Candidates directory does not exist: {candidates_dir}")
    path = write_diversity(candidates_dir, output_path, window=args.window)
    print(f"candidates_dir: {candidates_dir}")
    print(f"diversity:      {path}")


if __name__ == "__main__":
    main()
