from __future__ import annotations

from pathlib import Path

from harness_lab.backend import read_backend_profile
from harness_lab.budget import read_budget
from harness_lab.datasets import get_dataset_record
from harness_lab.diversity import read_diversity
from harness_lab.external_review import read_external_review
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight
from harness_lab.memory import build_candidate_index, read_json
from harness_lab.policy import read_policy
from harness_lab.workspace import write_json


def bootstrap_snapshot_path(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id / "memory" / "bootstrap_snapshot.json"


def decision_bundle_path(candidates_dir: Path, candidate_id: str) -> Path:
    return candidates_dir / candidate_id / "memory" / "decision_bundle.json"


def _compact_candidate(item: dict) -> dict:
    benchmark = item.get("benchmark_score")
    audit = item.get("audit_score")
    transfer_gap = None
    if benchmark is not None and audit is not None:
        transfer_gap = float(benchmark) - float(audit)
    return {
        "candidate_id": item.get("candidate_id", ""),
        "parent_id": item.get("parent_id"),
        "created_at": item.get("created_at", ""),
        "outcome_status": item.get("outcome_status", ""),
        "outcome_label": item.get("outcome_label", ""),
        "diagnosis_mechanism": item.get("diagnosis_mechanism", ""),
        "harness_component": item.get("harness_component", ""),
        "backend_fingerprints": item.get("backend_fingerprints", []),
        "failure_modes": item.get("failure_modes", []),
        "observed_failure_modes": item.get("observed_failure_modes", []),
        "benchmark_score": benchmark,
        "audit_score": audit,
        "transfer_gap": transfer_gap,
        "benchmark_summary": item.get("benchmark_summary", ""),
        "audit_summary": item.get("audit_summary", ""),
        "diagnosis_summary": item.get("diagnosis_summary", ""),
        "novelty_basis": item.get("novelty_basis", ""),
    }


def _read_science_progress(candidates_dir: Path, candidate_id: str) -> dict:
    path = candidates_dir / candidate_id / "traces" / "science_progress.json"
    if not path.exists():
        return {}
    payload = read_json(path)
    if not isinstance(payload, dict):
        return {}
    return payload


def build_decision_bundle(
    candidates_dir: Path,
    memory_dir: Path,
    candidate_id: str,
    *,
    parent_id: str | None,
    dataset_id: str,
    synthesis: dict | None = None,
) -> dict:
    index = build_candidate_index(candidates_dir)
    science_summary = read_json(memory_dir / "science_summary.json") if (memory_dir / "science_summary.json").exists() else {}
    science_debug_summary = read_json(memory_dir / "science_debug_summary.json") if (memory_dir / "science_debug_summary.json").exists() else {}
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    budget = read_budget(memory_dir)
    diversity = read_diversity(memory_dir)
    backend = read_backend_profile(memory_dir)
    hardware = read_hardware_profile(memory_dir)
    external_review = read_external_review(memory_dir)
    dataset_record = get_dataset_record(memory_dir, dataset_id) if dataset_id else None

    candidates = list(index.get("candidates", []))
    finished_scored = [
        _compact_candidate(item)
        for item in candidates
        if item.get("outcome_status") == "complete"
        and item.get("benchmark_score") is not None
        and item.get("audit_score") is not None
    ]
    pending_candidates = [
        _compact_candidate(item)
        for item in candidates
        if str(item.get("outcome_status", "")).strip() == "pending"
    ]
    stalled_candidates = [
        _compact_candidate(item)
        for item in candidates
        if "stale_process" in [str(mode).strip() for mode in item.get("observed_failure_modes", [])]
        or str(item.get("outcome_label", "")).strip() == "stalled"
    ]
    science_progress = _read_science_progress(candidates_dir, candidate_id)
    children_by_parent = index.get("children_by_parent", {})
    lineage_focus = []
    for item in (synthesis or {}).get("ranked_parents", [])[:5]:
        candidate = next((entry for entry in candidates if str(entry.get("candidate_id", "")) == str(item.get("candidate_id", ""))), None)
        if candidate is None:
            continue
        compact = _compact_candidate(candidate)
        compact["child_count"] = int(children_by_parent.get(compact["candidate_id"], 0) or 0)
        compact["ranking_reasons"] = item.get("reasons", [])
        compact["ranking_score"] = item.get("total_score", 0)
        lineage_focus.append(compact)

    return {
        "candidate_id": candidate_id,
        "parent_id": parent_id,
        "dataset_id": dataset_id,
        "candidate_count": int(index.get("candidate_count", 0) or 0),
        "dataset_context": dataset_record or {},
        "science_summary": science_summary,
        "science_debug_summary": science_debug_summary,
        "leaders": science_summary.get("leaders", {}),
        "recent_scored_candidates": finished_scored[-5:],
        "pending_candidates": pending_candidates[-8:],
        "stalled_candidates": stalled_candidates[-5:],
        "lineage_focus": lineage_focus,
        "top_parent_id": (synthesis or {}).get("top_parent_id"),
        "hindsight": {
            "summary": hindsight.get("summary", ""),
            "findings": hindsight.get("hindsight_findings", [])[:8],
            "policy_adjustments": hindsight.get("policy_adjustments", [])[:8],
            "over_explored_mechanisms": hindsight.get("over_explored_mechanisms", [])[:5],
            "under_explored_promising_mechanisms": hindsight.get("under_explored_promising_mechanisms", [])[:5],
            "over_explored_backend_fingerprints": hindsight.get("over_explored_backend_fingerprints", [])[:5],
            "under_explored_backend_fingerprints": hindsight.get("under_explored_backend_fingerprints", [])[:5],
            "throughput_summary": hindsight.get("throughput_summary", {}),
            "process_classification_counts": hindsight.get("process_classification_counts", {}),
        },
        "policy": policy,
        "budget": budget,
        "diversity": diversity,
        "backend": backend,
        "hardware": {
            "environment_hint": hardware.get("environment_hint", ""),
            "cpu_count": hardware.get("cpu_count"),
            "memory_gb_estimate": hardware.get("memory_gb_estimate"),
            "hostname": hardware.get("hostname", ""),
        },
        "external_review": {
            "status": external_review.get("status", ""),
            "trigger_reason": external_review.get("trigger_reason", ""),
            "reviewer": external_review.get("reviewer", ""),
            "lab_advice": external_review.get("lab_advice", [])[:5],
            "human_advice": external_review.get("human_advice", [])[:5],
            "situation_summary": external_review.get("situation_summary", ""),
        },
        "counts": {
            "mechanism_counts": index.get("diagnosis_mechanism_counts", {}),
            "backend_fingerprint_counts": index.get("backend_fingerprint_counts", {}),
            "failure_mode_counts": index.get("failure_mode_counts", {}),
            "outcome_label_counts": index.get("outcome_label_counts", {}),
            "children_by_parent": children_by_parent,
        },
        "science_progress": {
            "phase": science_progress.get("phase", ""),
            "updated_at": science_progress.get("updated_at", ""),
            "steps": science_progress.get("steps"),
            "elapsed_seconds": science_progress.get("elapsed_seconds"),
            "remaining_seconds": science_progress.get("remaining_seconds"),
            "peak_vram_mb": science_progress.get("peak_vram_mb"),
        },
    }


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
    science_debug_summary = read_json(memory_dir / "science_debug_summary.json") if (memory_dir / "science_debug_summary.json").exists() else {}
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    budget = read_budget(memory_dir)
    diversity = read_diversity(memory_dir)
    backend = read_backend_profile(memory_dir)
    hardware = read_hardware_profile(memory_dir)
    external_review = read_external_review(memory_dir)
    dataset_record = get_dataset_record(memory_dir, dataset_id) if dataset_id else None
    decision_bundle = build_decision_bundle(
        candidates_dir,
        memory_dir,
        candidate_id,
        parent_id=parent_id,
        dataset_id=dataset_id,
        synthesis=synthesis,
    )
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
        "science_debug_summary": {
            "summary": science_debug_summary.get("summary", ""),
            "likely_issue": science_debug_summary.get("likely_issue", ""),
            "recommended_fix": science_debug_summary.get("recommended_fix", ""),
            "findings": science_debug_summary.get("findings", [])[:5],
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
        "decision_bundle_summary": {
            "recent_scored_candidates": len(decision_bundle.get("recent_scored_candidates", [])),
            "pending_candidates": len(decision_bundle.get("pending_candidates", [])),
            "stalled_candidates": len(decision_bundle.get("stalled_candidates", [])),
            "lineage_focus": [item.get("candidate_id", "") for item in decision_bundle.get("lineage_focus", [])[:3]],
        },
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


def write_decision_bundle(
    candidates_dir: Path,
    memory_dir: Path,
    candidate_id: str,
    *,
    parent_id: str | None,
    dataset_id: str,
    synthesis: dict | None = None,
) -> Path:
    path = decision_bundle_path(candidates_dir, candidate_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(
        path,
        build_decision_bundle(
            candidates_dir,
            memory_dir,
            candidate_id,
            parent_id=parent_id,
            dataset_id=dataset_id,
            synthesis=synthesis,
        ),
    )
    return path
