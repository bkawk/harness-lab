#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.datasets import import_dataset_copy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Copy a prepared dataset from mesh-para into harness-lab so the lab stays self-contained."
    )
    parser.add_argument("dataset_id", help="Stable dataset id, e.g. abc_boundary512")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--datasets-dir", default="artifacts/datasets", help="Directory for imported datasets.")
    parser.add_argument("--source-path", required=True, help="Existing dataset path from mesh-para.")
    parser.add_argument(
        "--source-label",
        default="abc",
        help="Registry source label to use after import. Defaults to abc so imported data behaves like local ABC data.",
    )
    parser.add_argument(
        "--kind",
        default="prepared",
        help="Dataset kind, e.g. prepared or cache.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    record = import_dataset_copy(
        Path(args.memory_dir).resolve(),
        Path(args.datasets_dir).resolve(),
        dataset_id=args.dataset_id,
        source_path=Path(args.source_path).resolve(),
        source_label=args.source_label,
        kind=args.kind,
        notes=f"Copied from mesh-para path {Path(args.source_path).resolve()}",
    )
    print(f"dataset_id: {record.dataset_id}")
    print(f"imported:   {record.local_path}")
    print(f"source:     {record.source}")
    print(f"notes:      {record.notes}")


if __name__ == "__main__":
    main()
