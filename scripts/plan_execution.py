#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.execution import plan_execution_for_candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create an execution plan for a drafted candidate.")
    parser.add_argument("candidate_id", help="Stable candidate id, e.g. cand_0002")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    plan = plan_execution_for_candidate(Path(args.candidates_dir).resolve(), args.candidate_id)
    print(f"candidate_id:    {plan.candidate_id}")
    print(f"status:          {plan.status}")
    print(f"audit_required:  {plan.audit.get('required')}")
    print(f"benchmark_steps: {len(plan.benchmark.get('steps', []))}")
    print(f"trace_capture:   {', '.join(plan.trace_capture)}")


if __name__ == "__main__":
    main()
