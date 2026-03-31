from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from harness_lab.memory import read_json


@dataclass(frozen=True)
class SimulatedOutcome:
    outcome_label: str
    benchmark_score: float
    benchmark_summary: str
    audit_score: float
    audit_summary: str
    observed_failure_modes: tuple[str, ...]
    evidence: tuple[str, ...]


def _seed_for_candidate(candidates_dir: Path, candidate_id: str) -> int:
    proposal = read_json(candidates_dir / candidate_id / "proposal.json")
    diagnosis = read_json(candidates_dir / candidate_id / "diagnosis" / "summary.json")
    payload = (
        f"{candidate_id}|"
        f"{proposal.get('rationale', '')}|"
        f"{proposal.get('target', {}).get('harness_component', '')}|"
        f"{proposal.get('target', {}).get('expected_failure_mode', '')}|"
        f"{diagnosis.get('mechanism', '')}|"
        f"{','.join(str(item) for item in proposal.get('changes', []))}"
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def simulate_candidate_outcome(candidates_dir: Path, candidate_id: str) -> SimulatedOutcome:
    proposal = read_json(candidates_dir / candidate_id / "proposal.json")
    diagnosis = read_json(candidates_dir / candidate_id / "diagnosis" / "summary.json")
    target = proposal.get("target", {})
    expected_failure_mode = str(target.get("expected_failure_mode", "")).strip()
    mechanism = str(target.get("harness_component", "")).strip() or str(diagnosis.get("mechanism", "")).strip()
    counterfactual_count = len(proposal.get("changes", []))
    seed = _seed_for_candidate(candidates_dir, candidate_id)

    benchmark_score = round(((seed % 260) / 1000) + 0.08 + (counterfactual_count * 0.01), 6)
    audit_penalty = 0.03 if expected_failure_mode else 0.015
    audit_score = round(max(0.0, benchmark_score - audit_penalty - ((seed // 17) % 40) / 2000), 6)

    if benchmark_score >= 0.32 and audit_score >= 0.27:
        outcome_label = "keeper"
        observed_failure_modes: tuple[str, ...] = ()
        benchmark_summary = f"Simulated benchmark improvement for {mechanism or 'the harness'}."
        audit_summary = "Simulated audit retained most of the benchmark gain."
    elif benchmark_score >= 0.24:
        outcome_label = "audit_blocked"
        observed_failure_modes = (expected_failure_mode,) if expected_failure_mode else ("transfer_regression",)
        benchmark_summary = f"Simulated local improvement around {mechanism or 'the harness'}."
        audit_summary = "Simulated audit regressed relative to the local gain."
    else:
        outcome_label = "dead_end"
        observed_failure_modes = (expected_failure_mode,) if expected_failure_mode else ("no_gain",)
        benchmark_summary = "Simulated benchmark showed no meaningful improvement."
        audit_summary = "Simulated audit confirmed the same failure pattern."

    evidence = (
        "simulated:benchmark",
        "simulated:audit",
        f"simulated:mechanism:{mechanism or 'generic'}",
    )
    return SimulatedOutcome(
        outcome_label=outcome_label,
        benchmark_score=benchmark_score,
        benchmark_summary=benchmark_summary,
        audit_score=audit_score,
        audit_summary=audit_summary,
        observed_failure_modes=tuple(item for item in observed_failure_modes if item),
        evidence=evidence,
    )
