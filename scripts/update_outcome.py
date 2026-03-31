#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.outcome import update_outcome_for_candidate


def csv_or_empty(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    items = [item.strip() for item in raw.split(",")]
    return [item for item in items if item]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Update a candidate execution outcome.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0002")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--status", default=None, help="Outcome status: pending or complete.")
    parser.add_argument("--outcome-label", default=None, help="Short result label such as keeper, dead_end, or audit_blocked.")
    parser.add_argument("--benchmark-score", type=float, default=None, help="Optional benchmark score.")
    parser.add_argument("--benchmark-summary", default=None, help="Short benchmark summary.")
    parser.add_argument("--audit-score", type=float, default=None, help="Optional audit score.")
    parser.add_argument("--audit-summary", default=None, help="Short audit summary.")
    parser.add_argument("--observed-failure-modes", default=None, help="Comma-separated observed failure mode tags.")
    parser.add_argument("--evidence", default=None, help="Comma-separated evidence snippets or trace labels.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    outcome = update_outcome_for_candidate(
        Path(args.candidates_dir).resolve(),
        args.candidate_id,
        status=args.status,
        outcome_label=args.outcome_label,
        benchmark_score=args.benchmark_score,
        benchmark_summary=args.benchmark_summary,
        audit_score=args.audit_score,
        audit_summary=args.audit_summary,
        observed_failure_modes=csv_or_empty(args.observed_failure_modes),
        evidence=csv_or_empty(args.evidence),
    )
    print(f"candidate_id:    {outcome.candidate_id}")
    print(f"status:          {outcome.status}")
    print(f"outcome_label:   {outcome.outcome_label or '-'}")
    print(f"benchmark_score: {outcome.benchmark.get('score')}")
    print(f"audit_score:     {outcome.audit.get('score')}")


if __name__ == "__main__":
    main()
