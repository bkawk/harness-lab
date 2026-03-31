from __future__ import annotations

import difflib
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from harness_lab.workspace import write_json

SNAPSHOT_GLOBS = (
    "README.md",
    "pyproject.toml",
    "src/harness_lab/**/*.py",
    "scripts/**/*.py",
    "docs/**/*.md",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _git(repo_dir: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def snapshot_file_set(repo_dir: Path) -> list[Path]:
    files: dict[str, Path] = {}
    for pattern in SNAPSHOT_GLOBS:
        for path in repo_dir.glob(pattern):
            if path.is_file():
                files[str(path.relative_to(repo_dir))] = path
    return [files[key] for key in sorted(files)]


def build_repo_state(repo_dir: Path) -> dict:
    branch = ""
    commit = ""
    dirty = False
    status_lines: list[str] = []
    try:
        branch = _git(repo_dir, "rev-parse", "--abbrev-ref", "HEAD")
        commit = _git(repo_dir, "rev-parse", "HEAD")
        status = _git(repo_dir, "status", "--short")
        status_lines = [line for line in status.splitlines() if line.strip()]
        dirty = bool(status_lines)
    except Exception:
        status_lines = ["git_state_unavailable"]
    return {
        "captured_at": utc_now(),
        "repo_dir": str(repo_dir),
        "branch": branch,
        "commit": commit,
        "dirty": dirty,
        "git_status": status_lines,
    }


def _snapshot_root(candidate_root: Path) -> Path:
    return candidate_root / "source" / "repo_snapshot"


def _manifest_path(candidate_root: Path) -> Path:
    return candidate_root / "source" / "manifest.json"


def capture_repo_snapshot(repo_dir: Path, candidate_root: Path) -> dict:
    snapshot_root = _snapshot_root(candidate_root)
    if snapshot_root.exists():
        shutil.rmtree(snapshot_root)
    snapshot_root.mkdir(parents=True, exist_ok=True)

    copied_files: list[str] = []
    for source_path in snapshot_file_set(repo_dir):
        rel_path = source_path.relative_to(repo_dir)
        target_path = snapshot_root / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        copied_files.append(str(rel_path))

    payload = {
        **build_repo_state(repo_dir),
        "snapshot_root": "source/repo_snapshot",
        "tracked_files": copied_files,
        "tracked_file_count": len(copied_files),
    }
    write_json(_manifest_path(candidate_root), payload)
    return payload


def _load_snapshot_file(candidate_root: Path, relative_path: str) -> list[str]:
    path = _snapshot_root(candidate_root) / relative_path
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


@dataclass(frozen=True)
class EvidenceCapture:
    snapshot_manifest: Path
    diff_summary: Path
    combined_patch: Path
    changed_files: tuple[str, ...]


def capture_candidate_evidence(
    repo_dir: Path,
    candidates_dir: Path,
    candidate_id: str,
    parent_id: str | None,
) -> EvidenceCapture:
    candidate_root = candidates_dir / candidate_id
    (candidate_root / "patches").mkdir(parents=True, exist_ok=True)
    (candidate_root / "source").mkdir(parents=True, exist_ok=True)
    capture_repo_snapshot(repo_dir, candidate_root)

    summary_path = candidate_root / "patches" / "summary.json"
    combined_patch_path = candidate_root / "patches" / "against_parent.patch"
    changed_files: list[str] = []
    patch_chunks: list[str] = []

    if parent_id:
        parent_root = candidates_dir / parent_id
        parent_manifest = json.loads(_manifest_path(parent_root).read_text(encoding="utf-8")) if _manifest_path(parent_root).exists() else {}
        child_manifest = json.loads(_manifest_path(candidate_root).read_text(encoding="utf-8"))
        parent_files = set(parent_manifest.get("tracked_files", []))
        child_files = set(child_manifest.get("tracked_files", []))
        for relative_path in sorted(parent_files | child_files):
            parent_lines = _load_snapshot_file(parent_root, relative_path)
            child_lines = _load_snapshot_file(candidate_root, relative_path)
            if parent_lines == child_lines:
                continue
            changed_files.append(relative_path)
            diff = difflib.unified_diff(
                parent_lines,
                child_lines,
                fromfile=f"{parent_id}/{relative_path}",
                tofile=f"{candidate_id}/{relative_path}",
            )
            patch_chunks.append("".join(diff))

    combined_patch_path.write_text("".join(patch_chunks), encoding="utf-8")
    write_json(
        summary_path,
        {
            "candidate_id": candidate_id,
            "parent_id": parent_id,
            "captured_at": utc_now(),
            "changed_files": changed_files,
            "changed_file_count": len(changed_files),
            "combined_patch": str(combined_patch_path.relative_to(candidate_root)),
        },
    )
    return EvidenceCapture(
        snapshot_manifest=_manifest_path(candidate_root),
        diff_summary=summary_path,
        combined_patch=combined_patch_path,
        changed_files=tuple(changed_files),
    )
