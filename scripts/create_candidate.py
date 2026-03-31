#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.workspace import create_candidate_workspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a new candidate workspace.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0001")
    parser.add_argument("--base-dir", default="artifacts/candidates", help="Workspace root for candidate bundles.")
    parser.add_argument("--parent-id", default=None, help="Optional parent candidate id.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    base_dir = Path(args.base_dir).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    workspace = create_candidate_workspace(base_dir, args.candidate_id, args.parent_id)
    print(f"candidate_id: {workspace.candidate_id}")
    print(f"root:         {workspace.root}")
    print(f"manifest:     {workspace.manifest_path}")
    print(f"proposal:     {workspace.proposal_path}")
    print(f"diagnosis:    {workspace.diagnosis_path}")


if __name__ == "__main__":
    main()
