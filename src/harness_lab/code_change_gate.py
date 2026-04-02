from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path

from harness_lab.memory import read_json
from harness_lab.mutation_brief import code_change_brief_path
from harness_lab.workspace import write_json


def code_change_gate_path(memory_dir: Path) -> Path:
    return memory_dir / "code_change_gate.json"


def code_change_verification_path(memory_dir: Path) -> Path:
    return memory_dir / "code_change_verification.json"


def build_code_change_gate(memory_dir: Path) -> dict:
    brief = read_json(code_change_brief_path(memory_dir)) if code_change_brief_path(memory_dir).exists() else {}
    target_file = str(brief.get("target_file", "")).strip()
    focused_tests = [str(item).strip() for item in brief.get("focused_tests", []) if str(item).strip()]
    allowed_write_files = []
    for item in [target_file, *focused_tests]:
        if item and item not in allowed_write_files:
            allowed_write_files.append(item)
    compile_targets = [item for item in [target_file] if item.endswith(".py")]
    return {
        "summary": "Machine-enforced scope and verification gate for the current code-change brief.",
        "recommended_action": str(brief.get("recommended_action", "wait")).strip() or "wait",
        "target_module": str(brief.get("target_module", "")).strip(),
        "target_file": target_file,
        "allowed_write_files": allowed_write_files,
        "max_changed_files": len(allowed_write_files),
        "compile_targets": compile_targets,
        "focused_tests": focused_tests,
        "verification_required": list(brief.get("execution_contract", {}).get("verification_required", [])),
        "failure_behavior": list(brief.get("execution_contract", {}).get("failure_behavior", [])),
        "scope_limits": list(brief.get("execution_contract", {}).get("scope_limits", [])),
    }


def write_code_change_gate(memory_dir: Path) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = code_change_gate_path(memory_dir)
    write_json(path, build_code_change_gate(memory_dir))
    return path


def validate_code_change_scope(memory_dir: Path, changed_files: list[str]) -> dict:
    gate = read_json(code_change_gate_path(memory_dir)) if code_change_gate_path(memory_dir).exists() else build_code_change_gate(memory_dir)
    allowed = {str(item).strip() for item in gate.get("allowed_write_files", []) if str(item).strip()}
    normalized = [str(item).strip() for item in changed_files if str(item).strip()]
    violations: list[str] = []
    if len(normalized) > int(gate.get("max_changed_files", 0) or 0):
        violations.append("changed_file_count_exceeded")
    for item in normalized:
        if item not in allowed:
            violations.append(f"out_of_scope:{item}")
    return {
        "approved": len(violations) == 0,
        "changed_files": normalized,
        "allowed_write_files": sorted(allowed),
        "violations": violations,
    }


def _run_command(cmd: list[str], cwd: Path, *, stdout_limit: int, stderr_limit: int) -> dict:
    env = dict(os.environ)
    src_dir = cwd / "src"
    if src_dir.exists():
        existing = env.get("PYTHONPATH", "").strip()
        env["PYTHONPATH"] = str(src_dir) if not existing else f"{src_dir}{os.pathsep}{existing}"
    try:
        completed = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    except OSError as exc:
        return {
            "passed": False,
            "command": cmd,
            "stdout": "",
            "stderr": str(exc)[-stderr_limit:],
            "returncode": None,
        }
    return {
        "passed": completed.returncode == 0,
        "command": cmd,
        "stdout": completed.stdout[-stdout_limit:],
        "stderr": completed.stderr[-stderr_limit:],
        "returncode": completed.returncode,
    }


def run_code_change_verification(repo_dir: Path, memory_dir: Path, changed_files: list[str]) -> dict:
    gate = read_json(code_change_gate_path(memory_dir)) if code_change_gate_path(memory_dir).exists() else build_code_change_gate(memory_dir)
    scope = validate_code_change_scope(memory_dir, changed_files)
    compile_results: list[dict] = []
    tests_result = {"ran": False, "passed": False, "command": [], "stdout": "", "stderr": "", "returncode": None}

    if scope["approved"]:
        for relative_path in gate.get("compile_targets", []):
            cmd = [sys.executable, "-m", "py_compile", relative_path]
            compile_results.append(
                {
                    "path": relative_path,
                    **_run_command(cmd, repo_dir, stdout_limit=2000, stderr_limit=2000),
                }
            )
        compile_ok = all(item["passed"] for item in compile_results) if compile_results else True
        focused_tests = [str(item).strip() for item in gate.get("focused_tests", []) if str(item).strip()]
        if compile_ok and focused_tests:
            cmd = ["pytest", "-q", *focused_tests]
            tests_result = {"ran": True, **_run_command(cmd, repo_dir, stdout_limit=4000, stderr_limit=4000)}
        elif compile_ok:
            tests_result = {
                "ran": False,
                "passed": True,
                "command": [],
                "stdout": "",
                "stderr": "",
                "returncode": 0,
            }
    approved = scope["approved"] and all(item["passed"] for item in compile_results) and bool(tests_result["passed"])
    payload = {
        "summary": "Code-change verification passed." if approved else "Code-change verification failed or remains out of scope.",
        "approved": approved,
        "scope": scope,
        "recommended_action": str(gate.get("recommended_action", "wait")).strip() or "wait",
        "verification_required": list(gate.get("verification_required", [])),
        "compile_checks": compile_results,
        "focused_tests": tests_result,
        "failure_behavior": list(gate.get("failure_behavior", [])),
    }
    write_json(code_change_verification_path(memory_dir), payload)
    return payload
