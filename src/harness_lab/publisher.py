from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


TRACKED_PATHS = (
    "README.md",
    "docs",
    "scripts",
    "src",
    "pyproject.toml",
)


@dataclass(frozen=True)
class PublishResult:
    created_commit: bool
    pushed: bool
    commit_sha: str | None
    message: str


def _run_git(repo_dir: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


def _summarize_git_error(error: subprocess.CalledProcessError) -> str:
    stderr = (error.stderr or "").strip()
    stdout = (error.stdout or "").strip()
    detail = stderr or stdout or str(error)
    return detail.splitlines()[-1]


def publish_repo_snapshot(repo_dir: Path, message: str, *, branch: str = "main", remote: str = "origin") -> PublishResult:
    existing_paths = [path for path in TRACKED_PATHS if (repo_dir / path).exists()]
    if not existing_paths:
        return PublishResult(created_commit=False, pushed=False, commit_sha=None, message="No publishable tracked paths found.")

    _run_git(repo_dir, "add", *existing_paths)
    staged = _run_git(repo_dir, "diff", "--cached", "--name-only")
    if not staged:
        return PublishResult(created_commit=False, pushed=False, commit_sha=None, message="No publishable tracked changes to commit.")

    _run_git(repo_dir, "commit", "-m", message)
    commit_sha = _run_git(repo_dir, "rev-parse", "HEAD")
    try:
        _run_git(repo_dir, "pull", "--rebase", "--autostash", remote, branch)
        commit_sha = _run_git(repo_dir, "rev-parse", "HEAD")
        _run_git(repo_dir, "push", remote, branch)
    except subprocess.CalledProcessError as error:
        return PublishResult(
            created_commit=True,
            pushed=False,
            commit_sha=commit_sha,
            message=f"Created {commit_sha} locally, but publish failed: {_summarize_git_error(error)}",
        )
    return PublishResult(
        created_commit=True,
        pushed=True,
        commit_sha=commit_sha,
        message=f"Published {commit_sha} to {remote}/{branch}.",
    )
