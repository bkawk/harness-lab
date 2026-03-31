#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.proposal import draft_proposal_for_candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Draft a new proposal from indexed diagnosis memory.")
    parser.add_argument("candidate_id", help="Stable child candidate id, e.g. cand_0002")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--parent-id", default=None, help="Optional explicit parent candidate id.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    draft = draft_proposal_for_candidate(
        Path(args.candidates_dir).resolve(),
        args.candidate_id,
        parent_id=args.parent_id,
    )
    print(f"candidate_id:          {draft.candidate_id}")
    print(f"parent_id:             {draft.parent_id}")
    print(f"harness_component:     {draft.target.get('harness_component', '')}")
    print(f"expected_failure_mode: {draft.target.get('expected_failure_mode', '')}")
    print(f"novelty_basis:         {draft.target.get('novelty_basis', '')}")
    print(f"changes:               {len(draft.changes)}")


if __name__ == "__main__":
    main()
