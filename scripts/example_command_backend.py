#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> None:
    candidate_id = os.environ["HARNESS_LAB_CANDIDATE_ID"]
    dataset_id = os.environ.get("HARNESS_LAB_DATASET_ID", "")
    dataset_path = os.environ.get("HARNESS_LAB_DATASET_PATH", "")
    result_path = Path(os.environ["HARNESS_LAB_RESULT_PATH"])
    result_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "outcome_label": "backend_demo",
        "benchmark_score": 0.123456,
        "benchmark_summary": f"Example command backend ran for {candidate_id} using dataset {dataset_id or '-'} at {dataset_path or '-'}",
        "audit_score": 0.111111,
        "audit_summary": "Example backend completed without a real audit path.",
        "observed_failure_modes": [],
        "evidence": [
            "backend:example_command",
            f"backend:candidate:{candidate_id}",
            f"backend:dataset:{dataset_id or 'none'}",
        ],
    }
    result_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote backend result for {candidate_id} to {result_path}")


if __name__ == "__main__":
    main()
