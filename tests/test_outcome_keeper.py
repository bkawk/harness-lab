"""Tests for Import 3: tighter completion discipline (keeper validation)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_lab.outcome import validate_keeper_candidate, MAX_KEEPER_CHANGED_FILES
from harness_lab.workspace import create_candidate_workspace, write_json


def _setup_keeper(tmp_path, *, changed_files=3, severity="low", failure_modes=None, parent_failure_modes=None):
    """Create a candidate workspace configured as a keeper for testing."""
    candidates_dir = tmp_path / "candidates"
    ws = create_candidate_workspace(candidates_dir, "cand_0001")

    # Write outcome
    write_json(ws.outcome_path, {
        "candidate_id": "cand_0001",
        "status": "complete",
        "outcome_label": "keeper",
        "benchmark": {"score": 0.85, "summary": "good"},
        "audit": {"score": 0.80, "summary": "ok"},
        "observed_failure_modes": list(failure_modes or []),
        "evidence": [],
    })

    # Write diagnosis
    write_json(ws.diagnosis_path, {
        "candidate_id": "cand_0001",
        "status": "complete",
        "summary": "test",
        "severity": severity,
        "mechanism": "encoder",
        "failure_modes": list(failure_modes or []),
        "evidence": [],
        "counterfactuals": [],
    })

    # Write patch summary
    write_json(ws.patches_dir / "summary.json", {
        "changed_file_count": changed_files,
        "backend_fingerprints": ["encoder_tweak"],
    })

    # Optionally create a parent with failure modes
    if parent_failure_modes is not None:
        parent_ws = create_candidate_workspace(candidates_dir, "cand_0000")
        write_json(parent_ws.diagnosis_path, {
            "candidate_id": "cand_0000",
            "status": "complete",
            "summary": "parent",
            "severity": "medium",
            "mechanism": "encoder",
            "failure_modes": list(parent_failure_modes),
            "evidence": [],
            "counterfactuals": [],
        })
        # Update proposal to reference parent
        proposal = json.loads(ws.proposal_path.read_text())
        proposal["parent_id"] = "cand_0000"
        write_json(ws.proposal_path, proposal)

    return candidates_dir


class TestValidateKeeperCandidate:
    def test_approved_keeper(self, tmp_path):
        candidates_dir = _setup_keeper(tmp_path, changed_files=3, severity="low")
        result = validate_keeper_candidate(candidates_dir, "cand_0001")
        assert result["approved"] is True
        assert result["rejection_reason"] is None
        assert all(c["passed"] for c in result["checks"])
        # Verify review artifact was written
        review_path = candidates_dir / "cand_0001" / "outcome" / "keeper_review.json"
        assert review_path.exists()

    def test_rejected_no_changes(self, tmp_path):
        candidates_dir = _setup_keeper(tmp_path, changed_files=0)
        result = validate_keeper_candidate(candidates_dir, "cand_0001")
        assert result["approved"] is False
        failed = [c["check"] for c in result["checks"] if not c["passed"]]
        assert "has_changes" in failed

    def test_rejected_too_many_changes(self, tmp_path):
        candidates_dir = _setup_keeper(tmp_path, changed_files=MAX_KEEPER_CHANGED_FILES + 5)
        result = validate_keeper_candidate(candidates_dir, "cand_0001")
        assert result["approved"] is False
        failed = [c["check"] for c in result["checks"] if not c["passed"]]
        assert "bounded_changes" in failed

    def test_rejected_critical_severity(self, tmp_path):
        candidates_dir = _setup_keeper(tmp_path, severity="critical")
        result = validate_keeper_candidate(candidates_dir, "cand_0001")
        assert result["approved"] is False
        failed = [c["check"] for c in result["checks"] if not c["passed"]]
        assert "not_critical_severity" in failed

    def test_rejected_same_failure_modes_as_parent(self, tmp_path):
        failures = ["loss_divergence", "nan_gradient"]
        candidates_dir = _setup_keeper(
            tmp_path,
            failure_modes=failures,
            parent_failure_modes=failures,
        )
        result = validate_keeper_candidate(candidates_dir, "cand_0001")
        assert result["approved"] is False
        failed = [c["check"] for c in result["checks"] if not c["passed"]]
        assert "failure_modes_improved" in failed

    def test_approved_different_failure_modes_from_parent(self, tmp_path):
        candidates_dir = _setup_keeper(
            tmp_path,
            failure_modes=["new_issue"],
            parent_failure_modes=["old_issue"],
        )
        result = validate_keeper_candidate(candidates_dir, "cand_0001")
        assert result["approved"] is True

    def test_approved_bounded_lever_candidate_even_with_large_snapshot_diff(self, tmp_path):
        candidates_dir = _setup_keeper(tmp_path, changed_files=MAX_KEEPER_CHANGED_FILES + 9)
        proposal_path = candidates_dir / "cand_0001" / "proposal.json"
        proposal = json.loads(proposal_path.read_text())
        proposal["changes"] = [
            {
                "kind": "backend_lever",
                "mechanism": "science_train",
                "summary": "Increase batch size conservatively.",
            }
        ]
        proposal["backend_levers"] = {"science_train": {"batch_size": 3, "eval_batch_size": 3}}
        write_json(proposal_path, proposal)

        result = validate_keeper_candidate(candidates_dir, "cand_0001")

        assert result["approved"] is True
        bounded = next(check for check in result["checks"] if check["check"] == "bounded_changes")
        assert bounded["passed"] is True
        assert "lever_based_candidate" in bounded["detail"]
