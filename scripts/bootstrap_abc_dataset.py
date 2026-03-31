#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

from harness_lab.datasets import register_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap an ABC-backed dataset source into harness-lab."
    )
    parser.add_argument("dataset_id", help="Stable dataset id, e.g. abc_raw_v1")
    parser.add_argument("--memory-dir", default="artifacts/memory", help="Directory for memory artifacts.")
    parser.add_argument("--datasets-dir", default="artifacts/datasets", help="Directory for dataset payloads.")
    parser.add_argument("--stl-archive", default=None, help="Existing local STL archive path.")
    parser.add_argument("--step-archive", default=None, help="Existing local STEP archive path.")
    parser.add_argument("--feat-archive", default=None, help="Existing local features archive path.")
    parser.add_argument("--stl-url", default=None, help="Download URL for STL archive.")
    parser.add_argument("--step-url", default=None, help="Download URL for STEP archive.")
    parser.add_argument("--feat-url", default=None, help="Download URL for features archive.")
    parser.add_argument("--reuse-existing", action="store_true", help="Reuse archives already present under artifacts/datasets/<dataset_id>/archives/.")
    parser.add_argument("--notes", default="", help="Short provenance notes.")
    return parser


def resolve_source(name: str, local_path: str | None, url: str | None, existing_path: Path, reuse_existing: bool) -> tuple[str, str]:
    if reuse_existing and existing_path.exists() and not local_path and not url:
        return "existing", str(existing_path)
    if bool(local_path) and bool(url):
        raise ValueError(f"Provide only one of --{name}-archive or --{name}-url.")
    if local_path:
        return "local", local_path
    if url:
        return "url", str(url)
    if existing_path.exists():
        return "existing", str(existing_path)
    raise ValueError(
        f"No source available for {name}. Put the archive at {existing_path}, provide --{name}-archive, or provide --{name}-url."
    )


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    return destination


def materialize_input(
    datasets_dir: Path,
    dataset_id: str,
    *,
    label: str,
    source_kind: str,
    source_value: str,
) -> tuple[Path, dict]:
    target_dir = datasets_dir / dataset_id / "archives"
    target_name = f"{label}{Path(source_value).suffix or '.bin'}"
    target_path = target_dir / target_name
    if source_kind == "existing":
        return target_path, {
            "label": label,
            "mode": "present_local",
            "local_path": str(target_path),
            "sha256": sha256_for_file(target_path),
        }
    if source_kind == "local":
        source_path = Path(source_value).expanduser().resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        return target_path, {
            "label": label,
            "mode": "copied_local",
            "source_path": str(source_path),
            "local_path": str(target_path),
            "sha256": sha256_for_file(target_path),
        }

    downloaded_path = download_file(source_value, target_path)
    return downloaded_path, {
        "label": label,
        "mode": "downloaded",
        "source_url": source_value,
        "local_path": str(downloaded_path),
        "sha256": sha256_for_file(downloaded_path),
    }


def main() -> None:
    args = build_parser().parse_args()
    memory_dir = Path(args.memory_dir).resolve()
    datasets_dir = Path(args.datasets_dir).resolve()
    archives_dir = datasets_dir / args.dataset_id / "archives"

    inputs = {
        "stl": resolve_source("stl", args.stl_archive, args.stl_url, archives_dir / "stl.tar", args.reuse_existing),
        "step": resolve_source("step", args.step_archive, args.step_url, archives_dir / "step.tar", args.reuse_existing),
        "features": resolve_source("feat", args.feat_archive, args.feat_url, archives_dir / "features.tar", args.reuse_existing),
    }

    manifest = {
        "dataset_id": args.dataset_id,
        "source": "abc",
        "kind": "abc_source",
        "inputs": {},
    }

    dataset_root = datasets_dir / args.dataset_id
    dataset_root.mkdir(parents=True, exist_ok=True)

    for label, (source_kind, source_value) in inputs.items():
        _, payload = materialize_input(
            datasets_dir,
            args.dataset_id,
            label=label,
            source_kind=source_kind,
            source_value=source_value,
        )
        manifest["inputs"][label] = payload

    manifest_path = dataset_root / "source_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    record = register_dataset(
        memory_dir,
        dataset_id=args.dataset_id,
        kind="abc_source",
        source="abc",
        local_path=dataset_root,
        status="ready",
        notes=args.notes or "Bootstrapped directly from ABC archives.",
    )

    print(f"dataset_id:     {record.dataset_id}")
    print(f"source:         {record.source}")
    print(f"local_path:     {record.local_path}")
    print(f"manifest_path:  {manifest_path}")
    print(f"status:         {record.status}")


if __name__ == "__main__":
    main()
