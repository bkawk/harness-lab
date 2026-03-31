#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.external_review import maybe_request_external_review


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or refresh the bounded external review artifact.")
    parser.add_argument("--candidates-dir", type=Path, default=Path("artifacts/candidates"))
    parser.add_argument("--memory-dir", type=Path, default=Path("artifacts/memory"))
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = maybe_request_external_review(args.candidates_dir, args.memory_dir, force=args.force)
    print(f"status: {payload.get('status', 'idle')}")
    print(f"trigger_reason: {payload.get('trigger_reason', '') or '-'}")
    print(f"reviewer: {payload.get('reviewer', 'none')}")


if __name__ == "__main__":
    main()
