from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class CandidateSummary:
    candidate_id: str
    parent_id: str | None
    created_at: str
    proposal_status: str
    harness_component: str
    expected_failure_mode: str
    novelty_basis: str
    diagnosis_status: str
    diagnosis_summary: str
    diagnosis_severity: str
    diagnosis_mechanism: str
    outcome_status: str
    outcome_label: str
    hardware_environment: str
    source_commit: str
    source_branch: str
    snapshot_file_count: int
    changed_file_count: int
    trace_count: int
    backend_fingerprints: tuple[str, ...]
    benchmark_score: float | None
    audit_score: float | None
    benchmark_summary: str
    audit_summary: str
    failure_modes: tuple[str, ...]
    observed_failure_modes: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "proposal_status": self.proposal_status,
            "harness_component": self.harness_component,
            "expected_failure_mode": self.expected_failure_mode,
            "novelty_basis": self.novelty_basis,
            "diagnosis_status": self.diagnosis_status,
            "diagnosis_summary": self.diagnosis_summary,
            "diagnosis_severity": self.diagnosis_severity,
            "diagnosis_mechanism": self.diagnosis_mechanism,
            "outcome_status": self.outcome_status,
            "outcome_label": self.outcome_label,
            "hardware_environment": self.hardware_environment,
            "source_commit": self.source_commit,
            "source_branch": self.source_branch,
            "snapshot_file_count": self.snapshot_file_count,
            "changed_file_count": self.changed_file_count,
            "trace_count": self.trace_count,
            "backend_fingerprints": list(self.backend_fingerprints),
            "benchmark_score": self.benchmark_score,
            "audit_score": self.audit_score,
            "benchmark_summary": self.benchmark_summary,
            "audit_summary": self.audit_summary,
            "failure_modes": list(self.failure_modes),
            "observed_failure_modes": list(self.observed_failure_modes),
        }


def summarize_candidate(candidate_root: Path) -> CandidateSummary:
    workspace = read_json(candidate_root / "workspace.json")
    proposal = read_json(candidate_root / "proposal.json")
    diagnosis = read_json(candidate_root / "diagnosis" / "summary.json")
    outcome = read_json(candidate_root / "outcome" / "result.json")
    source_manifest_path = candidate_root / "source" / "manifest.json"
    patch_summary_path = candidate_root / "patches" / "summary.json"
    target = proposal.get("target", {})
    failure_modes = tuple(str(item) for item in diagnosis.get("failure_modes", []))
    observed_failure_modes = tuple(str(item) for item in outcome.get("observed_failure_modes", []))
    evidence = [str(item) for item in outcome.get("evidence", [])]
    source_manifest = read_json(source_manifest_path) if source_manifest_path.exists() else {}
    patch_summary = read_json(patch_summary_path) if patch_summary_path.exists() else {}
    hardware_environment = ""
    for item in evidence:
        if item.startswith("hardware:env:"):
            hardware_environment = item.split("hardware:env:", 1)[1]
            break
    benchmark = outcome.get("benchmark", {})
    audit = outcome.get("audit", {})
    return CandidateSummary(
        candidate_id=str(workspace["candidate_id"]),
        parent_id=workspace.get("parent_id"),
        created_at=str(workspace["created_at"]),
        proposal_status=str(proposal.get("status", "")),
        harness_component=str(target.get("harness_component", "")),
        expected_failure_mode=str(target.get("expected_failure_mode", "")),
        novelty_basis=str(target.get("novelty_basis", "")),
        diagnosis_status=str(diagnosis.get("status", "")),
        diagnosis_summary=str(diagnosis.get("summary", "")),
        diagnosis_severity=str(diagnosis.get("severity", "unknown")),
        diagnosis_mechanism=str(diagnosis.get("mechanism", "")),
        outcome_status=str(outcome.get("status", "")),
        outcome_label=str(outcome.get("outcome_label", "")),
        hardware_environment=hardware_environment,
        source_commit=str(source_manifest.get("commit", "")),
        source_branch=str(source_manifest.get("branch", "")),
        snapshot_file_count=int(source_manifest.get("tracked_file_count", 0) or 0),
        changed_file_count=int(patch_summary.get("changed_file_count", 0) or 0),
        trace_count=len(list((candidate_root / "traces").glob("*"))),
        backend_fingerprints=tuple(str(item) for item in patch_summary.get("backend_fingerprints", [])),
        benchmark_score=benchmark.get("score"),
        audit_score=audit.get("score"),
        benchmark_summary=str(benchmark.get("summary", "")),
        audit_summary=str(audit.get("summary", "")),
        failure_modes=failure_modes,
        observed_failure_modes=observed_failure_modes,
    )


def build_candidate_index(candidates_dir: Path) -> dict:
    if not candidates_dir.exists():
        return {
            "candidate_count": 0,
            "proposal_status_counts": {},
            "harness_component_counts": {},
            "diagnosis_severity_counts": {},
            "diagnosis_mechanism_counts": {},
            "outcome_status_counts": {},
            "outcome_label_counts": {},
            "hardware_environment_counts": {},
            "backend_fingerprint_counts": {},
            "failure_mode_counts": {},
            "observed_failure_mode_counts": {},
            "children_by_parent": {},
            "candidates": [],
        }

    summaries: list[CandidateSummary] = []
    proposal_status_counts: Counter[str] = Counter()
    harness_component_counts: Counter[str] = Counter()
    diagnosis_severity_counts: Counter[str] = Counter()
    diagnosis_mechanism_counts: Counter[str] = Counter()
    outcome_status_counts: Counter[str] = Counter()
    outcome_label_counts: Counter[str] = Counter()
    hardware_environment_counts: Counter[str] = Counter()
    backend_fingerprint_counts: Counter[str] = Counter()
    failure_mode_counts: Counter[str] = Counter()
    observed_failure_mode_counts: Counter[str] = Counter()
    children_by_parent: Counter[str] = Counter()

    for candidate_root in sorted(path for path in candidates_dir.iterdir() if path.is_dir()):
        if not (candidate_root / "workspace.json").exists():
            continue
        summary = summarize_candidate(candidate_root)
        summaries.append(summary)
        if summary.proposal_status:
            proposal_status_counts[summary.proposal_status] += 1
        if summary.harness_component:
            harness_component_counts[summary.harness_component] += 1
        if summary.diagnosis_severity:
            diagnosis_severity_counts[summary.diagnosis_severity] += 1
        if summary.diagnosis_mechanism:
            diagnosis_mechanism_counts[summary.diagnosis_mechanism] += 1
        if summary.outcome_status:
            outcome_status_counts[summary.outcome_status] += 1
        if summary.outcome_label:
            outcome_label_counts[summary.outcome_label] += 1
        if summary.hardware_environment:
            hardware_environment_counts[summary.hardware_environment] += 1
        for fingerprint in summary.backend_fingerprints:
            backend_fingerprint_counts[fingerprint] += 1
        for failure_mode in summary.failure_modes:
            failure_mode_counts[failure_mode] += 1
        for failure_mode in summary.observed_failure_modes:
            observed_failure_mode_counts[failure_mode] += 1
        if summary.parent_id:
            children_by_parent[summary.parent_id] += 1

    summaries.sort(key=lambda item: (item.created_at, item.candidate_id))
    return {
        "candidate_count": len(summaries),
        "proposal_status_counts": dict(sorted(proposal_status_counts.items())),
        "harness_component_counts": dict(sorted(harness_component_counts.items())),
        "diagnosis_severity_counts": dict(sorted(diagnosis_severity_counts.items())),
        "diagnosis_mechanism_counts": dict(sorted(diagnosis_mechanism_counts.items())),
        "outcome_status_counts": dict(sorted(outcome_status_counts.items())),
        "outcome_label_counts": dict(sorted(outcome_label_counts.items())),
        "hardware_environment_counts": dict(sorted(hardware_environment_counts.items())),
        "backend_fingerprint_counts": dict(sorted(backend_fingerprint_counts.items())),
        "failure_mode_counts": dict(sorted(failure_mode_counts.items())),
        "observed_failure_mode_counts": dict(sorted(observed_failure_mode_counts.items())),
        "children_by_parent": dict(sorted(children_by_parent.items())),
        "candidates": [summary.to_dict() for summary in summaries],
    }


def write_candidate_index(candidates_dir: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_candidate_index(candidates_dir)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def build_science_summary(candidates_dir: Path, recent_window: int = 5) -> dict:
    index = build_candidate_index(candidates_dir)
    candidates = list(index.get("candidates", []))
    scored = [
        item
        for item in candidates
        if item.get("benchmark_score") is not None or item.get("audit_score") is not None
    ]

    def score_key(item: dict, field: str) -> tuple[float, str]:
        value = item.get(field)
        if value is None:
            return (-1.0, str(item.get("candidate_id", "")))
        return (float(value), str(item.get("candidate_id", "")))

    best_benchmark = max(scored, key=lambda item: score_key(item, "benchmark_score"), default=None)
    best_audit = max(scored, key=lambda item: score_key(item, "audit_score"), default=None)
    best_transfer = min(
        (
            item
            for item in scored
            if item.get("benchmark_score") is not None and item.get("audit_score") is not None
        ),
        key=lambda item: (
            abs(float(item["benchmark_score"]) - float(item["audit_score"])),
            -float(item["audit_score"]),
            str(item.get("candidate_id", "")),
        ),
        default=None,
    )
    stable_candidates = [
        item
        for item in scored
        if item.get("outcome_label") == "keeper"
        or (
            item.get("benchmark_score") is not None
            and item.get("audit_score") is not None
            and abs(float(item["benchmark_score"]) - float(item["audit_score"])) <= 0.025
        )
    ]
    best_stable = max(stable_candidates, key=lambda item: score_key(item, "audit_score"), default=None)

    recent_scored = [
        item
        for item in candidates[-recent_window:]
        if item.get("benchmark_score") is not None and item.get("audit_score") is not None
    ]
    benchmark_avg = (
        sum(float(item["benchmark_score"]) for item in recent_scored) / len(recent_scored)
        if recent_scored
        else None
    )
    audit_avg = (
        sum(float(item["audit_score"]) for item in recent_scored) / len(recent_scored)
        if recent_scored
        else None
    )
    avg_gap = (
        sum(float(item["benchmark_score"]) - float(item["audit_score"]) for item in recent_scored) / len(recent_scored)
        if recent_scored
        else None
    )

    if recent_scored:
        trend_summary = (
            f"Across the last {len(recent_scored)} scored candidates, "
            f"benchmark averaged {benchmark_avg:.6f}, audit averaged {audit_avg:.6f}, "
            f"and the mean transfer gap was {avg_gap:.6f}."
        )
    else:
        trend_summary = "No scored candidates yet."

    def compact(item: dict | None) -> dict:
        if not item:
            return {}
        benchmark = item.get("benchmark_score")
        audit = item.get("audit_score")
        gap = None
        if benchmark is not None and audit is not None:
            gap = float(benchmark) - float(audit)
        return {
            "candidate_id": item.get("candidate_id", ""),
            "outcome_label": item.get("outcome_label", ""),
            "benchmark_score": benchmark,
            "audit_score": audit,
            "transfer_gap": gap,
            "diagnosis_mechanism": item.get("diagnosis_mechanism", ""),
        }

    return {
        "candidate_count": int(index.get("candidate_count", 0)),
        "scored_candidate_count": len(scored),
        "recent_window": recent_window,
        "trend_summary": trend_summary,
        "leaders": {
            "best_benchmark": compact(best_benchmark),
            "best_audit": compact(best_audit),
            "best_transfer": compact(best_transfer),
            "best_stable": compact(best_stable),
        },
        "recent_trend": {
            "benchmark_avg": benchmark_avg,
            "audit_avg": audit_avg,
            "avg_transfer_gap": avg_gap,
            "candidates": [
                {
                    "candidate_id": item.get("candidate_id", ""),
                    "outcome_label": item.get("outcome_label", ""),
                    "benchmark_score": item.get("benchmark_score"),
                    "audit_score": item.get("audit_score"),
                    "transfer_gap": float(item["benchmark_score"]) - float(item["audit_score"]),
                }
                for item in recent_scored
            ],
        },
    }


def write_science_summary(candidates_dir: Path, output_path: Path, recent_window: int = 5) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_science_summary(candidates_dir, recent_window=recent_window)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path
