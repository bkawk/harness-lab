from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from harness_lab.memory import build_candidate_index
from harness_lab.workspace import write_json

POSITIVE_OUTCOMES = {"keeper", "improved"}
NEGATIVE_OUTCOMES = {"dead_end", "train_error", "audit_blocked"}


@dataclass(frozen=True)
class MechanismStats:
    mechanism: str
    attempts: int
    positive_count: int
    negative_count: int
    avg_benchmark_score: float | None
    outcome_counts: dict[str, int]

    def to_dict(self) -> dict:
        return {
            "mechanism": self.mechanism,
            "attempts": self.attempts,
            "positive_count": self.positive_count,
            "negative_count": self.negative_count,
            "avg_benchmark_score": self.avg_benchmark_score,
            "outcome_counts": self.outcome_counts,
        }


def _top_items(counter: Counter[str], *, limit: int = 5, minimum: int = 1) -> list[dict]:
    ranked = [(key, count) for key, count in counter.items() if count >= minimum]
    ranked.sort(key=lambda item: (-item[1], item[0]))
    return [{"label": key, "count": count} for key, count in ranked[:limit]]


def _mechanism_stats(index: dict) -> list[MechanismStats]:
    buckets: dict[str, dict] = defaultdict(
        lambda: {
            "attempts": 0,
            "positive_count": 0,
            "negative_count": 0,
            "scores": [],
            "outcomes": Counter(),
        }
    )
    for candidate in index.get("candidates", []):
        mechanism = str(candidate.get("diagnosis_mechanism") or candidate.get("harness_component") or "").strip()
        if not mechanism:
            continue
        bucket = buckets[mechanism]
        bucket["attempts"] += 1
        outcome_label = str(candidate.get("outcome_label", "")).strip()
        if outcome_label:
            bucket["outcomes"][outcome_label] += 1
        if outcome_label in POSITIVE_OUTCOMES:
            bucket["positive_count"] += 1
        if outcome_label in NEGATIVE_OUTCOMES:
            bucket["negative_count"] += 1
        score = candidate.get("benchmark_score")
        if isinstance(score, (int, float)):
            bucket["scores"].append(float(score))

    results: list[MechanismStats] = []
    for mechanism, bucket in buckets.items():
        scores = list(bucket["scores"])
        results.append(
            MechanismStats(
                mechanism=mechanism,
                attempts=int(bucket["attempts"]),
                positive_count=int(bucket["positive_count"]),
                negative_count=int(bucket["negative_count"]),
                avg_benchmark_score=(sum(scores) / len(scores)) if scores else None,
                outcome_counts=dict(sorted(bucket["outcomes"].items())),
            )
        )
    results.sort(key=lambda item: (-item.attempts, item.mechanism))
    return results


def _backend_fingerprint_stats(index: dict) -> list[dict]:
    buckets: dict[str, dict] = defaultdict(
        lambda: {
            "attempts": 0,
            "positive_count": 0,
            "negative_count": 0,
            "audit_scores": [],
            "outcomes": Counter(),
        }
    )
    for candidate in index.get("candidates", []):
        fingerprints = [str(item).strip() for item in candidate.get("backend_fingerprints", []) if str(item).strip()]
        if not fingerprints:
            continue
        outcome_label = str(candidate.get("outcome_label", "")).strip()
        audit_score = candidate.get("audit_score")
        for fingerprint in fingerprints:
            bucket = buckets[fingerprint]
            bucket["attempts"] += 1
            if outcome_label:
                bucket["outcomes"][outcome_label] += 1
            if outcome_label in POSITIVE_OUTCOMES:
                bucket["positive_count"] += 1
            if outcome_label in NEGATIVE_OUTCOMES:
                bucket["negative_count"] += 1
            if isinstance(audit_score, (int, float)):
                bucket["audit_scores"].append(float(audit_score))

    results: list[dict] = []
    for fingerprint, bucket in buckets.items():
        audit_scores = list(bucket["audit_scores"])
        results.append(
            {
                "fingerprint": fingerprint,
                "attempts": int(bucket["attempts"]),
                "positive_count": int(bucket["positive_count"]),
                "negative_count": int(bucket["negative_count"]),
                "avg_audit_score": (sum(audit_scores) / len(audit_scores)) if audit_scores else None,
                "outcome_counts": dict(sorted(bucket["outcomes"].items())),
            }
        )
    results.sort(key=lambda item: (-item["attempts"], item["fingerprint"]))
    return results


def build_hindsight(candidates_dir: Path) -> dict:
    index = build_candidate_index(candidates_dir)
    outcome_counts = Counter(index.get("outcome_label_counts", {}))
    failure_counts = Counter(index.get("observed_failure_mode_counts", {}))
    mechanism_stats = _mechanism_stats(index)
    backend_fingerprint_stats = _backend_fingerprint_stats(index)

    over_explored: list[dict] = []
    under_explored_promising: list[dict] = []
    over_explored_backend_fingerprints: list[dict] = []
    under_explored_backend_fingerprints: list[dict] = []
    for stat in mechanism_stats:
        if stat.attempts >= 3 and stat.positive_count == 0 and stat.negative_count >= 2:
            over_explored.append(
                {
                    **stat.to_dict(),
                    "why": "Repeated attempts produced only negative outcomes.",
                }
            )
        if stat.attempts <= 2 and (
            stat.positive_count > 0 or (stat.avg_benchmark_score is not None and stat.avg_benchmark_score >= 0.6)
        ):
            under_explored_promising.append(
                {
                    **stat.to_dict(),
                    "why": "This mechanism has limited exploration with comparatively better evidence.",
                }
            )

    over_explored.sort(key=lambda item: (-item["attempts"], item["mechanism"]))
    under_explored_promising.sort(
        key=lambda item: (
            -item["positive_count"],
            -(item["avg_benchmark_score"] if item["avg_benchmark_score"] is not None else -1.0),
            item["mechanism"],
        )
    )

    for stat in backend_fingerprint_stats:
        if stat["attempts"] >= 3 and stat["positive_count"] == 0 and stat["negative_count"] >= 2:
            over_explored_backend_fingerprints.append(
                {
                    **stat,
                    "why": "This backend change type has been tried repeatedly without a positive outcome.",
                }
            )
        if stat["attempts"] <= 2 and (
            stat["positive_count"] > 0 or (stat["avg_audit_score"] is not None and stat["avg_audit_score"] >= 0.28)
        ):
            under_explored_backend_fingerprints.append(
                {
                    **stat,
                    "why": "This backend change type has limited attempts and comparatively better audit evidence.",
                }
            )
    over_explored_backend_fingerprints.sort(key=lambda item: (-item["attempts"], item["fingerprint"]))
    under_explored_backend_fingerprints.sort(
        key=lambda item: (
            -item["positive_count"],
            -(item["avg_audit_score"] if item["avg_audit_score"] is not None else -1.0),
            item["fingerprint"],
        )
    )

    hindsight_findings: list[str] = []
    policy_adjustments: list[str] = []

    dead_end_count = int(outcome_counts.get("dead_end", 0))
    train_error_count = int(outcome_counts.get("train_error", 0))
    audit_blocked_count = int(outcome_counts.get("audit_blocked", 0))

    if dead_end_count >= 2:
        hindsight_findings.append(
            f"The lab repeated dead-end candidates {dead_end_count} times; similar proposal shapes should cool down sooner."
        )
        policy_adjustments.append("Increase cooldown penalties for mechanisms with repeated dead_end outcomes.")
    if train_error_count >= 1:
        hindsight_findings.append(
            f"The lab encountered {train_error_count} train-error outcomes; it should have used smaller or more instrumented follow-ups earlier."
        )
        policy_adjustments.append("Prefer safer follow-ups after any train_error and require stronger trace capture review.")
    if audit_blocked_count >= 1:
        hindsight_findings.append(
            f"The lab saw {audit_blocked_count} audit-blocked outcomes; it should have emphasized transfer-stability checks earlier."
        )
        policy_adjustments.append("Raise priority for proposals that directly target transfer stability after an audit_blocked result.")
    if over_explored:
        hindsight_findings.append(
            f"The mechanism `{over_explored[0]['mechanism']}` appears over-explored relative to its evidence."
        )
        policy_adjustments.append(f"Reduce parent/proposal priority for `{over_explored[0]['mechanism']}` until new evidence appears.")
    if under_explored_promising:
        hindsight_findings.append(
            f"The mechanism `{under_explored_promising[0]['mechanism']}` looks under-explored and should have been revisited sooner."
        )
        policy_adjustments.append(f"Bias the next parent/proposal choice toward `{under_explored_promising[0]['mechanism']}`.")
    if over_explored_backend_fingerprints:
        hindsight_findings.append(
            f"The backend change type `{over_explored_backend_fingerprints[0]['fingerprint']}` appears over-used relative to its outcomes."
        )
        policy_adjustments.append(
            f"Cool down backend edits tagged `{over_explored_backend_fingerprints[0]['fingerprint']}` until a different scientific line shows evidence."
        )
    if under_explored_backend_fingerprints:
        hindsight_findings.append(
            f"The backend change type `{under_explored_backend_fingerprints[0]['fingerprint']}` looks promising and under-explored."
        )
        policy_adjustments.append(
            f"Raise priority for backend edits tagged `{under_explored_backend_fingerprints[0]['fingerprint']}`."
        )

    summary = (
        hindsight_findings[0]
        if hindsight_findings
        else "The lab has not yet accumulated enough varied evidence to produce a strong hindsight judgment."
    )

    return {
        "candidate_count": index.get("candidate_count", 0),
        "summary": summary,
        "hindsight_findings": hindsight_findings,
        "policy_adjustments": policy_adjustments,
        "top_outcomes": _top_items(outcome_counts, limit=5, minimum=1),
        "top_failure_modes": _top_items(failure_counts, limit=5, minimum=1),
        "over_explored_mechanisms": over_explored[:5],
        "under_explored_promising_mechanisms": under_explored_promising[:5],
        "over_explored_backend_fingerprints": over_explored_backend_fingerprints[:5],
        "under_explored_backend_fingerprints": under_explored_backend_fingerprints[:5],
        "mechanism_stats": [item.to_dict() for item in mechanism_stats],
        "backend_fingerprint_stats": backend_fingerprint_stats,
    }


def write_hindsight(candidates_dir: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(output_path, build_hindsight(candidates_dir))
    return output_path


def read_hindsight(memory_dir: Path) -> dict:
    path = memory_dir / "hindsight.json"
    if not path.exists():
        return {
            "candidate_count": 0,
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
            "top_outcomes": [],
            "top_failure_modes": [],
            "over_explored_mechanisms": [],
            "under_explored_promising_mechanisms": [],
            "over_explored_backend_fingerprints": [],
            "under_explored_backend_fingerprints": [],
            "mechanism_stats": [],
            "backend_fingerprint_stats": [],
        }
    import json

    return json.loads(path.read_text(encoding="utf-8"))
