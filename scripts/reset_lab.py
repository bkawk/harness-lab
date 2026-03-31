#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.reset import reset_lab_runtime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reset harness-lab back to a genesis-ready state while preserving datasets."
    )
    parser.add_argument("--repo-dir", default=".", help="Repository root.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = reset_lab_runtime(Path(args.repo_dir).resolve())
    print(f"candidates_cleared: {result.candidates_cleared}")
    print(f"logs_cleared:       {result.logs_cleared}")
    print(f"memory_removed:     {', '.join(result.memory_files_removed) if result.memory_files_removed else '-'}")
    print(f"dashboard_reset:    {result.dashboard_path}")


if __name__ == "__main__":
    main()
