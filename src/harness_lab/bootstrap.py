from __future__ import annotations

from pathlib import Path

from harness_lab.backend import read_backend_profile
from harness_lab.budget import read_budget
from harness_lab.datasets import get_dataset_record
from harness_lab.diversity import read_diversity
from harness_lab.external_review import read_external_review
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight
from harness_lab.memory import read_json
from harness_lab.policy import read_policy
from harness_lab.workspace import write_json


def bootstrap_snapshot_path(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id / "memory" / "bootstrap_snapshot.json"


def build_bootstrap_snapshot(
    candidates_dir: Path,
    memory_dir: Path,
    candidate_id: str,
    *,
    parent_id: str | None,
    dataset_id: str,
    synthesis: dict | None = None,
) -> dict:
    index = read_json(memory_dir / "candidate_index.json") if (memory_dir / "candidate_index.json").exists() else {"candidate_count": 0, "candidates": []}
    science_summary = read_json(memory_dir / "science_summary.json") if (memory_dir / "science_summary.json").exists() else {}
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    budget = read_budget(memory_dir)
    diversity = read_diversity(memory_dir)
    backend = read_backend_profile(memory_dir)
    hardware = read_hardware_profile(memory_dir)
    external_review = read_external_review(memory_dir)
    dataset_record = get_dataset_record(memory_dir, dataset_id) if dataset_id else None
    candidates = list(index.get("candidates", []))
    recent_candidates = []
    for item in candidates[-5:]:
        recent_candidates.append(
            {
                "candidate_id": item.get("candidate_id", ""),
                "outcome_label": item.get("outcome_label", ""),
                "diagnosis_mechanism": item.get("diagnosis_mechanism", ""),
                "backend_fingerprints": item.get("backend_fingerprints", []),
                "benchmark_score": item.get("benchmark_score"),
                "audit_score": item.get("audit_score"),
            }
        )
    return {
        "candidate_id": candidate_id,
        "parent_id": parent_id,
        "dataset_id": dataset_id,
        "candidate_count": int(index.get("candidate_count", 0) or 0),
        "top_parent_id": (synthesis or {}).get("top_parent_id"),
        "dataset_context": dataset_record or {},
        "science_summary": {
            "trend_summary": science_summary.get("trend_summary", ""),
            "leaders": science_summary.get("leaders", {}),
            "recent_trend": science_summary.get("recent_trend", {}),
        },
        "hindsight_summary": hindsight.get("summary", ""),
        "policy_summary": policy.get("summary", ""),
        "budget_summary": budget.get("summary", ""),
        "diversity_summary": diversity.get("summary", ""),
        "backend_summary": backend.get("summary", ""),
        "hardware_summary": {
            "environment_hint": hardware.get("environment_hint", ""),
            "cpu_count": hardware.get("cpu_count"),
            "memory_gb_estimate": hardware.get("memory_gb_estimate"),
        },
        "external_review_summary": {
            "status": external_review.get("status", ""),
            "trigger_reason": external_review.get("trigger_reason", ""),
            "reviewer": external_review.get("reviewer", ""),
            "lab_advice": external_review.get("lab_advice", [])[:3],
            "human_advice": external_review.get("human_advice", [])[:2],
        },
        "recent_candidates": recent_candidates,
        "mechanism_counts": index.get("diagnosis_mechanism_counts", {}),
        "backend_fingerprint_counts": index.get("backend_fingerprint_counts", {}),
        "failure_mode_counts": index.get("failure_mode_counts", {}),
    }


def write_bootstrap_snapshot(
    candidates_dir: Path,
    memory_dir: Path,
    candidate_id: str,
    *,
    parent_id: str | None,
    dataset_id: str,
    synthesis: dict | None = None,
) -> Path:
    path = bootstrap_snapshot_path(candidates_dir, candidate_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(
        path,
        build_bootstrap_snapshot(
            candidates_dir,
            memory_dir,
            candidate_id,
            parent_id=parent_id,
            dataset_id=dataset_id,
            synthesis=synthesis,
        ),
    )
    return path
