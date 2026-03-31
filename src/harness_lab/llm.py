from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path

log = logging.getLogger("harness_lab.llm")


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
    timeout = int(os.environ.get("HARNESS_LAB_LLM_TIMEOUT_SECONDS", "120") or 120)
    args = [claude_bin, "-p", prompt]
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        log.warning("claude call timed out after %ds", timeout)
        return None
    except OSError as exc:
        log.warning("claude binary not found or not executable: %s", exc)
        return None
    except subprocess.SubprocessError as exc:
        log.warning("claude subprocess error: %s", exc)
        return None
    if completed.returncode != 0:
        stderr_snippet = (completed.stderr or "").strip()[:200]
        log.warning("claude exited %d: %s", completed.returncode, stderr_snippet)
        return None
    result = _extract_json_object(completed.stdout)
    if result is None:
        stdout_snippet = (completed.stdout or "").strip()[:200]
        log.warning("claude returned non-JSON output: %s", stdout_snippet)
    return result
