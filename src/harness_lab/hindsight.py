from __future__ import annotations

import json
import logging
import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("harness_lab.hindsight")

from harness_lab.llm import run_claude_json
from harness_lab.memory import build_backend_module_summary, build_candidate_index
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


def _recent_scored_candidates(index: dict, *, window: int = 8) -> list[dict]:
    scored = [
        item
        for item in index.get("candidates", [])
        if item.get("benchmark_score") is not None or item.get("audit_score") is not None
    ]
    return scored[-window:]


def _llm_hindsight_prompt(index: dict, heuristic_payload: dict) -> str:
    recent_candidates = _recent_scored_candidates(index, window=8)
    compact_recent = [
        {
            "candidate_id": item.get("candidate_id", ""),
            "outcome_label": item.get("outcome_label", ""),
            "diagnosis_mechanism": item.get("diagnosis_mechanism", ""),
            "backend_fingerprints": item.get("backend_fingerprints", []),
            "benchmark_score": item.get("benchmark_score"),
            "audit_score": item.get("audit_score"),
        }
        for item in recent_candidates
    ]
    payload = {
        "candidate_count": heuristic_payload.get("candidate_count", 0),
        "top_outcomes": heuristic_payload.get("top_outcomes", []),
        "top_failure_modes": heuristic_payload.get("top_failure_modes", []),
        "over_explored_mechanisms": heuristic_payload.get("over_explored_mechanisms", []),
        "under_explored_promising_mechanisms": heuristic_payload.get("under_explored_promising_mechanisms", []),
        "over_explored_backend_fingerprints": heuristic_payload.get("over_explored_backend_fingerprints", []),
        "under_explored_backend_fingerprints": heuristic_payload.get("under_explored_backend_fingerprints", []),
        "backend_module_notes": heuristic_payload.get("backend_module_notes", []),
        "backend_module_summary": heuristic_payload.get("backend_module_summary", {}),
        "throughput_summary": heuristic_payload.get("throughput_summary", {}),
        "process_classification_counts": heuristic_payload.get("process_classification_counts", {}),
        "recent_candidates": compact_recent,
        "heuristic_summary": heuristic_payload.get("summary", ""),
        "heuristic_findings": heuristic_payload.get("hindsight_findings", []),
        "heuristic_policy_adjustments": heuristic_payload.get("policy_adjustments", []),
    }
    return (
        "You are writing bounded hindsight for harness-lab.\n"
        "Return only JSON with keys: summary, hindsight_findings, policy_adjustments.\n"
        "hindsight_findings and policy_adjustments must be arrays of short strings.\n"
        "Keep the output grounded in the supplied evidence and preserve the lab's bounded, actionable style.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _normalize_llm_hindsight_payload(payload: dict, fallback: dict) -> dict | None:
    if not isinstance(payload, dict):
        return None
    summary = str(payload.get("summary", "")).strip()
    findings = [str(item).strip() for item in payload.get("hindsight_findings", []) if str(item).strip()]
    adjustments = [str(item).strip() for item in payload.get("policy_adjustments", []) if str(item).strip()]
    if not summary:
        return None
    normalized = dict(fallback)
    normalized["summary"] = summary
    normalized["hindsight_findings"] = findings[:8] if findings else list(fallback.get("hindsight_findings", []))
    normalized["policy_adjustments"] = adjustments[:8] if adjustments else list(fallback.get("policy_adjustments", []))
    normalized["hindsight_reviewer"] = "claude"
    return normalized


def build_hindsight(candidates_dir: Path) -> dict:
    index = build_candidate_index(candidates_dir)
    outcome_counts = Counter(index.get("outcome_label_counts", {}))
    failure_counts = Counter(index.get("observed_failure_mode_counts", {}))
    recent_scored = _recent_scored_candidates(index, window=8)
    recent_outcome_counts = Counter(str(item.get("outcome_label", "")).strip() for item in recent_scored if str(item.get("outcome_label", "")).strip())
    recent_failure_counts: Counter[str] = Counter()
    for candidate in recent_scored:
        for failure_mode in candidate.get("observed_failure_modes", []):
            label = str(failure_mode).strip()
            if label:
                recent_failure_counts[label] += 1
    mechanism_stats = _mechanism_stats(index)
    backend_fingerprint_stats = _backend_fingerprint_stats(index)
    backend_module_summary = build_backend_module_summary(candidates_dir)

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

    recent_hindsight_findings: list[str] = []
    historical_hindsight_findings: list[str] = []
    hindsight_findings: list[str] = []
    policy_adjustments: list[str] = []
    backend_module_notes: list[str] = []

    dead_end_count = int(outcome_counts.get("dead_end", 0))
    train_error_count = int(outcome_counts.get("train_error", 0))
    audit_blocked_count = int(outcome_counts.get("audit_blocked", 0))
    recent_dead_end_count = int(recent_outcome_counts.get("dead_end", 0))
    recent_train_error_count = int(recent_outcome_counts.get("train_error", 0))
    recent_audit_blocked_count = int(recent_outcome_counts.get("audit_blocked", 0))

    if recent_dead_end_count >= 2:
        recent_hindsight_findings.append(
            f"In the recent scored window, the lab repeated dead-end candidates {recent_dead_end_count} times; similar proposal shapes should cool down sooner."
        )
        policy_adjustments.append("Increase cooldown penalties for mechanisms with repeated dead_end outcomes.")
    elif dead_end_count >= 2:
        historical_hindsight_findings.append(
            f"Historically, the lab repeated dead-end candidates {dead_end_count} times; similar proposal shapes should cool down sooner."
        )
        policy_adjustments.append("Increase cooldown penalties for mechanisms with repeated dead_end outcomes.")
    if recent_train_error_count >= 1:
        recent_hindsight_findings.append(
            f"In the recent scored window, the lab encountered {recent_train_error_count} train-error outcomes; it should have used smaller or more instrumented follow-ups earlier."
        )
        policy_adjustments.append("Prefer safer follow-ups after any train_error and require stronger trace capture review.")
    elif train_error_count >= 1:
        historical_hindsight_findings.append(
            f"Historically, the lab encountered {train_error_count} train-error outcomes; it should have used smaller or more instrumented follow-ups earlier."
        )
        policy_adjustments.append("Prefer safer follow-ups after any train_error and require stronger trace capture review.")
    if recent_audit_blocked_count >= 1:
        recent_hindsight_findings.append(
            f"In the recent scored window, the lab saw {recent_audit_blocked_count} audit-blocked outcomes; it should emphasize transfer-stability checks."
        )
        policy_adjustments.append("Raise priority for proposals that directly target transfer stability after an audit_blocked result.")
    elif audit_blocked_count >= 1:
        historical_hindsight_findings.append(
            f"Historically, the lab saw {audit_blocked_count} audit-blocked outcomes; it should have emphasized transfer-stability checks earlier."
        )
        policy_adjustments.append("Raise priority for proposals that directly target transfer stability after an audit_blocked result.")
    hindsight_findings.extend(recent_hindsight_findings)
    hindsight_findings.extend(historical_hindsight_findings)
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
    backend_modules = list(backend_module_summary.get("modules", []))
    if backend_modules:
        top_module = backend_modules[0]
        note = f"Recent backend edits are concentrated in `{top_module['module']}`."
        if top_module.get("avg_transfer_gap") is not None:
            note = (
                f"Recent backend edits are concentrated in `{top_module['module']}`, "
                f"where the average transfer gap is {float(top_module['avg_transfer_gap']):.6f}."
            )
        backend_module_notes.append(note)
        if int(top_module.get("audit_blocked_count", 0) or 0) >= 2:
            backend_module_notes.append(
                f"`{top_module['module']}` changes are still encountering repeated audit-blocked outcomes."
            )
        if int(top_module.get("keeper_count", 0) or 0) >= 1:
            backend_module_notes.append(
                f"`{top_module['module']}` has already participated in at least one keeper and deserves explicit comparison against other modules."
            )

    # --- Import 2 & 5: aggregate process classification and throughput ---
    process_classification_counts: Counter[str] = Counter()
    throughput_wall_clocks: list[float] = []
    throughput_saved: list[float] = []
    early_completion_count = 0

    # Read from trace files
    for candidate_root in sorted(path for path in candidates_dir.iterdir() if path.is_dir()):
        # Process classification from run trace
        run_trace_path = candidate_root / "traces" / "run.json"
        if run_trace_path.exists():
            try:
                run_trace = json.loads(run_trace_path.read_text(encoding="utf-8"))
                pc = run_trace.get("process_classification", {})
                classification = str(pc.get("classification", "")).strip()
                if classification:
                    process_classification_counts[classification] += 1
            except (json.JSONDecodeError, ValueError, KeyError):
                pass
        # Throughput from dedicated file
        throughput_path = candidate_root / "traces" / "throughput.json"
        if throughput_path.exists():
            try:
                tp = json.loads(throughput_path.read_text(encoding="utf-8"))
                wall = float(tp.get("wall_clock_seconds", 0))
                saved = float(tp.get("time_saved_estimate_seconds", 0))
                throughput_wall_clocks.append(wall)
                throughput_saved.append(saved)
                if tp.get("early_completion_detected"):
                    early_completion_count += 1
            except (json.JSONDecodeError, ValueError, KeyError):
                pass

    throughput_summary = {
        "total_runs": len(throughput_wall_clocks),
        "avg_wall_clock": round(sum(throughput_wall_clocks) / len(throughput_wall_clocks), 3) if throughput_wall_clocks else 0,
        "avg_time_saved": round(sum(throughput_saved) / len(throughput_saved), 3) if throughput_saved else 0,
        "total_time_saved": round(sum(throughput_saved), 3),
        "early_completion_count": early_completion_count,
    }

    summary = (
        hindsight_findings[0]
        if hindsight_findings
        else "The lab has not yet accumulated enough varied evidence to produce a strong hindsight judgment."
    )

    payload = {
        "candidate_count": index.get("candidate_count", 0),
        "recent_scored_candidate_count": len(recent_scored),
        "summary": summary,
        "hindsight_findings": hindsight_findings,
        "policy_adjustments": policy_adjustments,
        "top_outcomes": _top_items(outcome_counts, limit=5, minimum=1),
        "top_failure_modes": _top_items(failure_counts, limit=5, minimum=1),
        "recent_top_outcomes": _top_items(recent_outcome_counts, limit=5, minimum=1),
        "recent_top_failure_modes": _top_items(recent_failure_counts, limit=5, minimum=1),
        "over_explored_mechanisms": over_explored[:5],
        "under_explored_promising_mechanisms": under_explored_promising[:5],
        "over_explored_backend_fingerprints": over_explored_backend_fingerprints[:5],
        "under_explored_backend_fingerprints": under_explored_backend_fingerprints[:5],
        "backend_module_summary": backend_module_summary,
        "backend_module_notes": backend_module_notes[:8],
        "mechanism_stats": [item.to_dict() for item in mechanism_stats],
        "backend_fingerprint_stats": backend_fingerprint_stats,
        "process_classification_counts": dict(sorted(process_classification_counts.items())),
        "throughput_summary": throughput_summary,
    }
    if str(os.environ.get("HARNESS_LAB_LLM_HINDSIGHT_ENABLED", "")).strip().lower() in {"1", "true", "yes"}:
        llm_payload = run_claude_json(_llm_hindsight_prompt(index, payload), cwd=candidates_dir.parent.parent)
        normalized = _normalize_llm_hindsight_payload(llm_payload or {}, payload)
        if normalized:
            log.info("hindsight authored by claude")
            return normalized
        log.warning("hindsight: claude fallback to heuristic (payload=%s)", "empty" if not llm_payload else "invalid")
    return payload


def write_hindsight(candidates_dir: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(output_path, build_hindsight(candidates_dir))
    return output_path


def read_hindsight(memory_dir: Path) -> dict:
    path = memory_dir / "hindsight.json"
    if not path.exists():
        return {
            "candidate_count": 0,
            "recent_scored_candidate_count": 0,
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
            "top_outcomes": [],
            "top_failure_modes": [],
            "recent_top_outcomes": [],
            "recent_top_failure_modes": [],
            "over_explored_mechanisms": [],
            "under_explored_promising_mechanisms": [],
            "over_explored_backend_fingerprints": [],
            "under_explored_backend_fingerprints": [],
            "backend_module_summary": {},
            "backend_module_notes": [],
            "mechanism_stats": [],
            "backend_fingerprint_stats": [],
            "process_classification_counts": {},
            "throughput_summary": {},
        }
    return json.loads(path.read_text(encoding="utf-8"))
