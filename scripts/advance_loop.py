#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.loop import advance_candidate_loop


def csv_or_empty(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    items = [item.strip() for item in raw.split(",")]
    return [item for item in items if item]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Advance one candidate through the local harness-lab loop.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0002")
    parser.add_argument("--repo-dir", default=".", help="Repository root.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--parent-id", default=None, help="Optional explicit parent candidate id.")
    parser.add_argument("--finalize-outcome", action="store_true", help="Also write an outcome and reconcile diagnosis in this loop step.")
    parser.add_argument("--simulate-outcome", action="store_true", help="Generate a deterministic simulated outcome before reconciling.")
    parser.add_argument("--runner-backend", default="simulated", help="Runner backend to use when simulating or running outcomes.")
    parser.add_argument("--outcome-label", default="simulated_pending", help="Outcome label to write when finalizing.")
    parser.add_argument("--benchmark-score", type=float, default=None, help="Optional benchmark score when finalizing.")
    parser.add_argument("--benchmark-summary", default=None, help="Optional benchmark summary when finalizing.")
    parser.add_argument("--audit-score", type=float, default=None, help="Optional audit score when finalizing.")
    parser.add_argument("--audit-summary", default=None, help="Optional audit summary when finalizing.")
    parser.add_argument("--observed-failure-modes", default=None, help="Comma-separated observed failure mode tags when finalizing.")
    parser.add_argument("--evidence", default=None, help="Comma-separated evidence labels when finalizing.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = advance_candidate_loop(
        Path(args.repo_dir).resolve(),
        Path(args.candidates_dir).resolve(),
        Path(args.memory_dir).resolve(),
        args.candidate_id,
        parent_id=args.parent_id,
        outcome_label=args.outcome_label,
        benchmark_score=args.benchmark_score,
        benchmark_summary=args.benchmark_summary,
        audit_score=args.audit_score,
        audit_summary=args.audit_summary,
        observed_failure_modes=csv_or_empty(args.observed_failure_modes),
        evidence=csv_or_empty(args.evidence),
        finalize_outcome=args.finalize_outcome,
        simulate_outcome=args.simulate_outcome,
        runner_backend=args.runner_backend,
    )
    print(f"candidate_id:      {result.candidate_id}")
    print(f"parent_id:         {result.parent_id or '-'}")
    print(f"proposal_status:   {result.proposal_status}")
    print(f"execution_status:  {result.execution_status}")
    print(f"outcome_status:    {result.outcome_status}")
    print(f"diagnosis_status:  {result.diagnosis_status}")
    print(f"next_top_parent:   {result.top_parent_id or '-'}")


if __name__ == "__main__":
    main()
