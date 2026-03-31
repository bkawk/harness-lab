#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.diagnosis import reconcile_diagnosis_from_outcome


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reconcile diagnosis from an executed candidate outcome.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0002")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    diagnosis = reconcile_diagnosis_from_outcome(Path(args.candidates_dir).resolve(), args.candidate_id)
    print(f"candidate_id:  {diagnosis.candidate_id}")
    print(f"status:        {diagnosis.status}")
    print(f"severity:      {diagnosis.severity}")
    print(f"mechanism:     {diagnosis.mechanism}")
    print(f"summary:       {diagnosis.summary}")


if __name__ == "__main__":
    main()
