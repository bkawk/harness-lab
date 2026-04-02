from __future__ import annotations

from pathlib import Path

from harness_lab.code_change_gate import code_change_gate_path
from harness_lab.memory import read_json
from harness_lab.mutation_brief import code_change_brief_path
from harness_lab.workspace import write_json


def autonomous_mutation_gate_path(memory_dir: Path) -> Path:
    return memory_dir / "autonomous_mutation_gate.json"


def build_autonomous_mutation_gate(memory_dir: Path) -> dict:
    brief = read_json(code_change_brief_path(memory_dir)) if code_change_brief_path(memory_dir).exists() else {}
    gate = read_json(code_change_gate_path(memory_dir)) if code_change_gate_path(memory_dir).exists() else {}

    decision_state = str(brief.get("decision_state", "wait")).strip() or "wait"
    recommended_action = str(brief.get("recommended_action", "wait")).strip() or "wait"
    target_module = str(brief.get("target_module", "")).strip()
    target_file = str(brief.get("target_file", "")).strip()
    focused_tests = [str(item).strip() for item in gate.get("focused_tests", []) if str(item).strip()]
    allowed_write_files = [str(item).strip() for item in gate.get("allowed_write_files", []) if str(item).strip()]
    max_changed_files = int(gate.get("max_changed_files", 0) or 0)

    reasons: list[str] = []
    eligible = True

    if decision_state != "issue":
        eligible = False
        reasons.append(f"Decision state is `{decision_state}`, so autonomous code mutation stays blocked.")
    if recommended_action != "targeted_mutation":
        eligible = False
        reasons.append(f"Recommended action is `{recommended_action}`, not `targeted_mutation`.")
    if not target_module or not target_file:
        eligible = False
        reasons.append("Target module/file is not specific enough yet.")
    if not focused_tests:
        eligible = False
        reasons.append("No focused tests are defined for the target seam.")
    if max_changed_files <= 0 or max_changed_files > 2:
        eligible = False
        reasons.append(f"Allowed write scope is {max_changed_files} files; autonomous mutation requires a target file plus adjacent tests only.")
    if not allowed_write_files:
        eligible = False
        reasons.append("The code-change gate does not have an enforceable allowlist yet.")

    reason = (
        "Autonomous code mutation is eligible: issue state, bounded scope, focused tests, and failure behavior are all in place."
        if eligible
        else " ".join(reasons)
    )

    return {
        "summary": "Autonomous code mutation is eligible for this seam." if eligible else "Autonomous code mutation remains blocked for this seam.",
        "eligible": eligible,
        "state": "enabled" if eligible else "blocked",
        "reason": reason,
        "target_module": target_module,
        "target_file": target_file,
        "decision_state": decision_state,
        "recommended_action": recommended_action,
        "max_changed_files": max_changed_files,
        "allowed_write_files": allowed_write_files,
        "focused_tests": focused_tests,
        "execution_mode": "candidate_workspace_only",
        "auto_publish": False,
        "silent_rollback": False,
        "requirements": [
            "Decision state must be `issue`.",
            "Recommended action must be `targeted_mutation`.",
            "Scope must stay within the target file plus adjacent focused tests.",
            "Focused tests and py_compile must pass before any promotion decision.",
            "Failed attempts stay visible and do not auto-publish.",
        ],
    }


def write_autonomous_mutation_gate(memory_dir: Path) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = autonomous_mutation_gate_path(memory_dir)
    write_json(path, build_autonomous_mutation_gate(memory_dir))
    return path
