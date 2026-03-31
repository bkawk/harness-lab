#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.diagnosis import update_diagnosis


def csv_or_empty(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    items = [item.strip() for item in raw.split(",")]
    return [item for item in items if item]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Update a candidate diagnosis summary.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0001")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--status", default=None, help="Diagnosis status: empty, in_progress, complete.")
    parser.add_argument("--summary", default=None, help="Short causal summary of what failed or succeeded.")
    parser.add_argument("--severity", default=None, help="Failure severity: unknown, low, medium, high, critical.")
    parser.add_argument("--mechanism", default=None, help="Mechanism or subsystem most implicated.")
    parser.add_argument("--failure-modes", default=None, help="Comma-separated failure mode tags.")
    parser.add_argument("--evidence", default=None, help="Comma-separated evidence snippets or trace labels.")
    parser.add_argument("--counterfactuals", default=None, help="Comma-separated counterfactual next-step notes.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    updated = update_diagnosis(
        Path(args.candidates_dir).resolve(),
        args.candidate_id,
        status=args.status,
        summary=args.summary,
        severity=args.severity,
        mechanism=args.mechanism,
        failure_modes=csv_or_empty(args.failure_modes),
        evidence=csv_or_empty(args.evidence),
        counterfactuals=csv_or_empty(args.counterfactuals),
    )
    print(f"candidate_id:  {updated.candidate_id}")
    print(f"status:        {updated.status}")
    print(f"severity:      {updated.severity}")
    print(f"mechanism:     {updated.mechanism}")
    print(f"failure_modes: {', '.join(updated.failure_modes) if updated.failure_modes else '-'}")


if __name__ == "__main__":
    main()
