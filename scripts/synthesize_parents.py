#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.synthesis import refresh_memory_artifacts, synthesize_parent_candidates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank diagnosed candidates and write a parent synthesis artifact.")
    parser.add_argument("--candidates-dir", default="artifacts/candidates", help="Directory containing candidate workspaces.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--write-index", action="store_true", help="Also refresh candidate_index.json before synthesis.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidates_dir = Path(args.candidates_dir).resolve()
    memory_dir = Path(args.memory_dir).resolve()
    if args.write_index:
        payload = refresh_memory_artifacts(candidates_dir, memory_dir)
    else:
        payload = synthesize_parent_candidates(candidates_dir, memory_dir / "parent_synthesis.json")
    print(f"top_parent_id: {payload.get('top_parent_id')}")
    for item in payload.get("ranked_parents", [])[:5]:
        reasons = ", ".join(item.get("reasons", []))
        print(f"{item['candidate_id']}: score={item['total_score']} reasons={reasons}")


if __name__ == "__main__":
    main()
