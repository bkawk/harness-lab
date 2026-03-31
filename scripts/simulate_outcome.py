#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.outcome import update_outcome_for_candidate
from harness_lab.simulator import simulate_candidate_outcome


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulate a candidate outcome from proposal and diagnosis context.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0002")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--write", action="store_true", help="Also write the simulated outcome into outcome/result.json.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidates_dir = Path(args.candidates_dir).resolve()
    simulated = simulate_candidate_outcome(candidates_dir, args.candidate_id)
    if args.write:
        update_outcome_for_candidate(
            candidates_dir,
            args.candidate_id,
            status="complete",
            outcome_label=simulated.outcome_label,
            benchmark_score=simulated.benchmark_score,
            benchmark_summary=simulated.benchmark_summary,
            audit_score=simulated.audit_score,
            audit_summary=simulated.audit_summary,
            observed_failure_modes=list(simulated.observed_failure_modes),
            evidence=list(simulated.evidence),
        )
    print(f"candidate_id:       {args.candidate_id}")
    print(f"outcome_label:      {simulated.outcome_label}")
    print(f"benchmark_score:    {simulated.benchmark_score}")
    print(f"audit_score:        {simulated.audit_score}")
    print(f"failure_modes:      {', '.join(simulated.observed_failure_modes) if simulated.observed_failure_modes else '-'}")


if __name__ == "__main__":
    main()
