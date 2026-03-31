from __future__ import annotations

import json
import os
from pathlib import Path

from harness_lab.workspace import write_json


DEFAULT_COMMAND_BACKEND = "python3 scripts/repo_command_backend.py"


def backend_profile_path(memory_dir: Path) -> Path:
    return memory_dir / "backend_profile.json"


def default_backend_profile() -> dict:
    return {
        "summary": "The repo-native science backend is available through the command runner with a realistic wall-clock training budget.",
        "preferred_backend": "command",
        "available_backends": ["command", "simulated"],
        "command_backend_configured": True,
        "command_backend_command": DEFAULT_COMMAND_BACKEND,
        "backend_source": "repo_default",
        "default_science_time_budget_seconds": 600,
        "evidence": ["backend:repo_native_default", "backend:science_default", "backend:science_budget:600"],
    }


def build_backend_profile() -> dict:
    command = os.environ.get("HARNESS_LAB_BACKEND_COMMAND", "").strip() or DEFAULT_COMMAND_BACKEND
    profile = default_backend_profile()
    if command and command != DEFAULT_COMMAND_BACKEND:
        profile.update(
            {
                "summary": "A custom external command backend is configured.",
                "preferred_backend": "command",
                "available_backends": ["command", "simulated"],
                "command_backend_configured": True,
                "command_backend_command": command,
                "backend_source": "env_override",
                "evidence": ["backend:command_configured"],
            }
        )
    return profile


def write_backend_profile(memory_dir: Path, output_path: Path | None = None) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = output_path or backend_profile_path(memory_dir)
    write_json(path, build_backend_profile())
    return path


def read_backend_profile(memory_dir: Path) -> dict:
    path = backend_profile_path(memory_dir)
    if not path.exists():
        return default_backend_profile()
    return json.loads(path.read_text(encoding="utf-8"))
