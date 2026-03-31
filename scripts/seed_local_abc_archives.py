#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Seed harness-lab's canonical ABC archive location from already-downloaded local files."
    )
    parser.add_argument("dataset_id", help="Stable source dataset id, e.g. abc_raw_v1")
    parser.add_argument("--datasets-dir", default="artifacts/datasets", help="Directory for dataset artifacts.")
    parser.add_argument("--stl-archive", required=True, help="Existing local STL archive path.")
    parser.add_argument("--step-archive", required=True, help="Existing local STEP archive path.")
    parser.add_argument("--feat-archive", required=True, help="Existing local features archive path.")
    return parser


def copy_one(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source archive does not exist: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> None:
    args = build_parser().parse_args()
    datasets_dir = Path(args.datasets_dir).resolve()
    archives_dir = datasets_dir / args.dataset_id / "archives"

    targets = {
        "stl": archives_dir / "stl.tar",
        "step": archives_dir / "step.tar",
        "features": archives_dir / "features.tar",
    }
    sources = {
        "stl": Path(args.stl_archive).expanduser().resolve(),
        "step": Path(args.step_archive).expanduser().resolve(),
        "features": Path(args.feat_archive).expanduser().resolve(),
    }

    for label in ("stl", "step", "features"):
        copy_one(sources[label], targets[label])
        print(f"{label}: {targets[label]}")


if __name__ == "__main__":
    main()
