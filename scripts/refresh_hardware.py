#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from harness_lab.hardware import refresh_hardware_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Refresh the hardware profile used by the lab.")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    profile = refresh_hardware_profile(Path(args.memory_dir).resolve())
    print(f"hostname:         {profile.hostname}")
    print(f"platform:         {profile.platform_name} {profile.platform_release}")
    print(f"machine:          {profile.machine}")
    print(f"cpu_count:        {profile.cpu_count}")
    print(f"memory_gb:        {profile.memory_gb_estimate}")
    print(f"environment_hint: {profile.environment_hint}")


if __name__ == "__main__":
    main()
