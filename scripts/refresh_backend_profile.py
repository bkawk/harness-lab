#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.backend import read_backend_profile, write_backend_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Refresh the backend readiness profile the lab uses for runner selection.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory where backend_profile.json should live.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    memory_dir = Path(args.memory_dir).resolve()
    path = write_backend_profile(memory_dir)
    profile = read_backend_profile(memory_dir)
    print(f"path:                {path}")
    print(f"preferred_backend:   {profile.get('preferred_backend')}")
    print(f"available_backends:  {', '.join(profile.get('available_backends', [])) or '-'}")
    print(f"command_configured:  {profile.get('command_backend_configured')}")


if __name__ == "__main__":
    main()
