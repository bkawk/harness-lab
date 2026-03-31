from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def _extract_json_object(text: str) -> dict | None:
    text = text.strip()
    if not text:
        return None
    candidates = [text]
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.insert(0, text[start : end + 1])
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def run_claude_json(prompt: str, *, cwd: Path) -> dict | None:
    claude_bin = os.environ.get("HARNESS_LAB_CLAUDE_BIN", "claude").strip() or "claude"
    args = [claude_bin, "-p", prompt]
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=int(os.environ.get("HARNESS_LAB_LLM_TIMEOUT_SECONDS", "120") or 120),
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return _extract_json_object(completed.stdout)
