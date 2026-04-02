from __future__ import annotations

from harness_lab.code_change_gate import (
    build_code_change_gate,
    run_code_change_verification,
    validate_code_change_scope,
)
from harness_lab.workspace import write_json


def test_build_code_change_gate_uses_brief_scope(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "target_module": "science_loss",
            "target_file": "src/harness_lab/science_loss.py",
            "focused_tests": ["tests/test_science_loss.py"],
            "execution_contract": {
                "verification_required": ["Run py_compile.", "Run focused tests."],
                "failure_behavior": ["Abort on failure."],
                "scope_limits": ["Keep the patch narrow."],
            },
        },
    )

    payload = build_code_change_gate(memory_dir)

    assert payload["recommended_action"] == "targeted_mutation"
    assert payload["target_file"] == "src/harness_lab/science_loss.py"
    assert payload["allowed_write_files"] == [
        "src/harness_lab/science_loss.py",
        "tests/test_science_loss.py",
    ]
    assert payload["max_changed_files"] == 2
    assert payload["compile_targets"] == ["src/harness_lab/science_loss.py"]
    assert payload["verification_required"] == ["Run py_compile.", "Run focused tests."]


def test_validate_code_change_scope_rejects_out_of_scope_files(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "target_file": "src/harness_lab/science_loss.py",
            "focused_tests": ["tests/test_science_loss.py"],
            "execution_contract": {},
        },
    )

    payload = validate_code_change_scope(
        memory_dir,
        ["src/harness_lab/science_loss.py", "tests/test_science_loss.py", "src/harness_lab/science_eval.py"],
    )

    assert payload["approved"] is False
    assert "changed_file_count_exceeded" in payload["violations"]
    assert "out_of_scope:src/harness_lab/science_eval.py" in payload["violations"]


def test_run_code_change_verification_records_scope_failure_without_running_checks(tmp_path):
    repo_dir = tmp_path / "repo"
    memory_dir = tmp_path / "artifacts" / "memory"
    repo_dir.mkdir(parents=True)
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "target_file": "src/harness_lab/science_loss.py",
            "focused_tests": ["tests/test_science_loss.py"],
            "execution_contract": {
                "verification_required": ["Run py_compile.", "Run focused tests."],
                "failure_behavior": ["Abort on failure."],
                "scope_limits": ["Keep the patch narrow."],
            },
        },
    )

    payload = run_code_change_verification(repo_dir, memory_dir, ["src/harness_lab/science_eval.py"])

    assert payload["approved"] is False
    assert payload["scope"]["approved"] is False
    assert payload["compile_checks"] == []
    assert payload["focused_tests"]["ran"] is False


def test_run_code_change_verification_runs_compile_and_tests(tmp_path):
    repo_dir = tmp_path / "repo"
    memory_dir = tmp_path / "artifacts" / "memory"
    source_dir = repo_dir / "src" / "harness_lab"
    tests_dir = repo_dir / "tests"
    source_dir.mkdir(parents=True)
    tests_dir.mkdir(parents=True)
    memory_dir.mkdir(parents=True)

    (source_dir / "science_loss.py").write_text("def compute_loss():\n    return 1\n", encoding="utf-8")
    (tests_dir / "test_science_loss.py").write_text(
        "from harness_lab.science_loss import compute_loss\n\n\ndef test_compute_loss():\n    assert compute_loss() == 1\n",
        encoding="utf-8",
    )
    (source_dir / "__init__.py").write_text("", encoding="utf-8")

    write_json(
        memory_dir / "code_change_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "target_file": "src/harness_lab/science_loss.py",
            "focused_tests": ["tests/test_science_loss.py"],
            "execution_contract": {
                "verification_required": ["Run py_compile.", "Run focused tests."],
                "failure_behavior": ["Abort on failure."],
                "scope_limits": ["Keep the patch narrow."],
            },
        },
    )

    payload = run_code_change_verification(
        repo_dir,
        memory_dir,
        ["src/harness_lab/science_loss.py", "tests/test_science_loss.py"],
    )

    assert payload["approved"] is True
    assert payload["scope"]["approved"] is True
    assert payload["compile_checks"][0]["passed"] is True
    assert payload["focused_tests"]["ran"] is True
    assert payload["focused_tests"]["passed"] is True
