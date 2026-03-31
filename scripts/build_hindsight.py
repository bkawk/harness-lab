#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.hindsight import write_hindsight


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a hindsight artifact from candidate history.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--output", default="artifacts/memory/hindsight.json", help="Output JSON path for hindsight.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidates_dir = Path(args.candidates_dir).resolve()
    output_path = Path(args.output).resolve()
    if not candidates_dir.exists():
        raise SystemExit(f"Candidates directory does not exist: {candidates_dir}")
    hindsight_path = write_hindsight(candidates_dir, output_path)
    print(f"candidates_dir: {candidates_dir}")
    print(f"hindsight:      {hindsight_path}")


if __name__ == "__main__":
    main()
