#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.datasets import register_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Register a dataset for harness-lab.")
    parser.add_argument("dataset_id", help="Stable dataset id, e.g. abc_boundary512")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--kind", required=True, help="Dataset kind, e.g. attached, fetched, prepared.")
    parser.add_argument("--source", required=True, help="Dataset source label, e.g. mesh-para, abc, local.")
    parser.add_argument("--local-path", required=True, help="Local filesystem path to the dataset.")
    parser.add_argument("--status", default="ready", help="Dataset status.")
    parser.add_argument("--notes", default="", help="Short provenance notes.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    record = register_dataset(
        Path(args.memory_dir).resolve(),
        dataset_id=args.dataset_id,
        kind=args.kind,
        source=args.source,
        local_path=Path(args.local_path).resolve(),
        status=args.status,
        notes=args.notes,
    )
    print(f"dataset_id: {record.dataset_id}")
    print(f"source:     {record.source}")
    print(f"local_path: {record.local_path}")
    print(f"status:     {record.status}")


if __name__ == "__main__":
    main()
