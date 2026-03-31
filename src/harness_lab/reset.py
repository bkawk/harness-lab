from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


IDLE_BIG_BANG_MARKDOWN = """# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `idle`
- vital_spark_at: `-`
- started_at: `-`
- last_heartbeat: `-`
- cycles_completed: `0`
- genesis seed: `cand_0001`
- last candidate: `-`
- last dataset: `-`
- last commit: `-`
- last publish message: `-`
- last cycle mode: `-`
- novelty cycles triggered: `0`

## Latest Step
- no completed big-bang step yet

## Recent Candidates
- no candidate history yet

## Hindsight
- summary: `No hindsight yet.`
- adjustment: `No policy adjustments yet.`

## Policy
- summary: `No policy yet.`
- selection_mode: `-`
- cooldown_multiplier: `-`
- preferred_runner_backend: `-`
- publish_every_cycles: `-`
- novelty_cycle_priority: `-`

## Budget
- summary: `No budget yet.`
- exploration_mode: `-`
- tracked_mechanisms: `0`

## Backend
- summary: `No backend profile yet.`
- preferred_backend: `-`
- available_backends: `-`
- command_backend_configured: `False`

## Diversity
- summary: `No diversity yet.`
- current_mechanism_streak: `-`
- novelty_step_recommended: `False`
"""


@dataclass(frozen=True)
class ResetResult:
    candidates_cleared: bool
    logs_cleared: bool
    memory_files_removed: tuple[str, ...]
    dashboard_path: Path


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
        return
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)


def reset_lab_runtime(repo_dir: Path) -> ResetResult:
    artifacts_dir = repo_dir / "artifacts"
    candidates_dir = artifacts_dir / "candidates"
    logs_dir = artifacts_dir / "logs"
    memory_dir = artifacts_dir / "memory"
    docs_dir = repo_dir / "docs"
    dashboard_path = docs_dir / "big_bang.md"

    _remove_path(candidates_dir)
    candidates_dir.mkdir(parents=True, exist_ok=True)

    _remove_path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)

    removed: list[str] = []
    if memory_dir.exists():
        for path in sorted(memory_dir.iterdir()):
            if path.name == "datasets.json":
                continue
            removed.append(path.name)
            _remove_path(path)
    memory_dir.mkdir(parents=True, exist_ok=True)

    docs_dir.mkdir(parents=True, exist_ok=True)
    dashboard_path.write_text(IDLE_BIG_BANG_MARKDOWN, encoding="utf-8")

    return ResetResult(
        candidates_cleared=True,
        logs_cleared=True,
        memory_files_removed=tuple(removed),
        dashboard_path=dashboard_path,
    )
