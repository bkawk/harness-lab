#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.runner import run_candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a candidate through a configured backend.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0002")
    parser.add_argument("--repo-dir", default=".", help="Repository root.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--backend", default="simulated", help="Runner backend. Options: simulated, command.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_candidate(
        Path(args.repo_dir).resolve(),
        Path(args.candidates_dir).resolve(),
        args.candidate_id,
        backend=args.backend,
    )
    print(f"candidate_id:    {result.candidate_id}")
    print(f"backend:         {result.backend}")
    print(f"outcome_label:   {result.outcome.outcome_label}")
    print(f"benchmark_score: {result.outcome.benchmark.get('score')}")
    print(f"audit_score:     {result.outcome.audit.get('score')}")


if __name__ == "__main__":
    main()
