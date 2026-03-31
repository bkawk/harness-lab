#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.publisher import publish_repo_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Commit and push tracked lab evolution to GitHub.")
    parser.add_argument("--repo-dir", default=".", help="Repository root to publish.")
    parser.add_argument("--message", required=True, help="Commit message for the lab snapshot.")
    parser.add_argument("--branch", default="main", help="Branch to push.")
    parser.add_argument("--remote", default="origin", help="Remote to push.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = publish_repo_snapshot(
        Path(args.repo_dir).resolve(),
        args.message,
        branch=args.branch,
        remote=args.remote,
    )
    print(f"created_commit: {result.created_commit}")
    print(f"pushed:         {result.pushed}")
    print(f"commit_sha:     {result.commit_sha or '-'}")
    print(f"message:        {result.message}")


if __name__ == "__main__":
    main()
