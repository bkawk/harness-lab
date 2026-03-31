import json

from harness_lab.science_train import write_science_progress


def test_write_science_progress_writes_phase_and_payload(tmp_path):
    write_science_progress(tmp_path, "training", candidate_id="cand_9999", steps=12)

    payload = json.loads((tmp_path / "science_progress.json").read_text())

    assert payload["phase"] == "training"
    assert payload["candidate_id"] == "cand_9999"
    assert payload["steps"] == 12
