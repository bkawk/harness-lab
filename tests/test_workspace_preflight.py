"""Tests for workspace preflight directory and CandidateWorkspace.preflight_dir property."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness_lab.workspace import CandidateWorkspace, create_candidate_workspace


class TestWorkspacePreflight:
    def test_preflight_dir_created(self, tmp_path):
        ws = create_candidate_workspace(tmp_path, "cand_0001")
        assert ws.preflight_dir.exists()
        assert ws.preflight_dir.is_dir()

    def test_preflight_dir_path(self, tmp_path):
        ws = create_candidate_workspace(tmp_path, "cand_0001")
        assert ws.preflight_dir == ws.root / "preflight"

    def test_preflight_in_manifest(self, tmp_path):
        ws = create_candidate_workspace(tmp_path, "cand_0001")
        import json
        manifest = json.loads(ws.manifest_path.read_text())
        assert "preflight" in manifest["paths"]
        assert manifest["paths"]["preflight"] == "preflight"
