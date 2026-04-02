from __future__ import annotations

from harness_lab.autonomous_mutation_gate import build_autonomous_mutation_gate
from harness_lab.workspace import write_json


def test_autonomous_mutation_gate_blocks_when_decision_is_not_issue(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "recommended_action": "wait",
            "decision_state": "wait",
            "target_module": "science_loss",
            "target_file": "src/harness_lab/science_loss.py",
        },
    )
    write_json(
        memory_dir / "code_change_gate.json",
        {
            "max_changed_files": 2,
            "allowed_write_files": ["src/harness_lab/science_loss.py", "tests/test_science_loss.py"],
            "focused_tests": ["tests/test_science_loss.py"],
        },
    )

    payload = build_autonomous_mutation_gate(memory_dir)

    assert payload["eligible"] is False
    assert payload["state"] == "blocked"
    assert "Decision state is `wait`" in payload["reason"]


def test_autonomous_mutation_gate_blocks_when_scope_is_too_broad(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "decision_state": "issue",
            "target_module": "science_loss",
            "target_file": "src/harness_lab/science_loss.py",
        },
    )
    write_json(
        memory_dir / "code_change_gate.json",
        {
            "max_changed_files": 4,
            "allowed_write_files": [
                "src/harness_lab/science_loss.py",
                "tests/test_science_loss.py",
                "src/harness_lab/science_eval.py",
                "tests/test_science_eval.py",
            ],
            "focused_tests": ["tests/test_science_loss.py"],
        },
    )

    payload = build_autonomous_mutation_gate(memory_dir)

    assert payload["eligible"] is False
    assert "requires a target file plus adjacent tests only" in payload["reason"]


def test_autonomous_mutation_gate_enables_for_narrow_issue_state(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "decision_state": "issue",
            "target_module": "science_loss",
            "target_file": "src/harness_lab/science_loss.py",
        },
    )
    write_json(
        memory_dir / "code_change_gate.json",
        {
            "max_changed_files": 2,
            "allowed_write_files": ["src/harness_lab/science_loss.py", "tests/test_science_loss.py"],
            "focused_tests": ["tests/test_science_loss.py"],
        },
    )

    payload = build_autonomous_mutation_gate(memory_dir)

    assert payload["eligible"] is True
    assert payload["state"] == "enabled"
    assert payload["execution_mode"] == "candidate_workspace_only"
    assert payload["auto_publish"] is False
    assert payload["silent_rollback"] is False
