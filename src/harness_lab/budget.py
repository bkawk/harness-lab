from __future__ import annotations

import json
from pathlib import Path

from harness_lab.hindsight import read_hindsight
from harness_lab.policy import read_policy
from harness_lab.workspace import write_json


def default_budget() -> dict:
    return {
        "summary": "No budget yet.",
        "exploration_mode": "balanced",
        "mechanism_budgets": [],
    }


def build_budget(memory_dir: Path) -> dict:
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    over_explored = {
        str(item.get("mechanism", "")).strip()
        for item in hindsight.get("over_explored_mechanisms", [])
        if str(item.get("mechanism", "")).strip()
    }
    under_explored = {
        str(item.get("mechanism", "")).strip()
        for item in hindsight.get("under_explored_promising_mechanisms", [])
        if str(item.get("mechanism", "")).strip()
    }

    mechanism_budgets: list[dict] = []
    exhausted_mechanisms: list[str] = []
    for item in hindsight.get("mechanism_stats", []):
        mechanism = str(item.get("mechanism", "")).strip()
        if not mechanism:
            continue
        attempts = int(item.get("attempts", 0) or 0)
        positive_count = int(item.get("positive_count", 0) or 0)
        negative_count = int(item.get("negative_count", 0) or 0)
        allowed = 2
        if policy.get("selection_mode") == "stabilize":
            allowed = 1
        elif policy.get("selection_mode") == "exploit_underexplored":
            allowed = 3
        if mechanism in under_explored:
            allowed += 1
        if mechanism in over_explored:
            allowed = max(1, allowed - 1)
        if positive_count > 0:
            allowed += 1
        consumed = max(attempts - positive_count, negative_count)
        remaining = max(0, allowed - consumed)
        exhausted = remaining <= 0
        if exhausted:
            exhausted_mechanisms.append(mechanism)
        mechanism_budgets.append(
            {
                "mechanism": mechanism,
                "attempts": attempts,
                "allowed_followups": allowed,
                "consumed_followups": consumed,
                "remaining_followups": remaining,
                "exhausted": exhausted,
                "status": "under_explored" if mechanism in under_explored else ("over_explored" if mechanism in over_explored else "balanced"),
            }
        )

    # --- Import 5: throughput-adjusted budgets ---
    throughput_summary = hindsight.get("throughput_summary", {})
    early_completions = int(throughput_summary.get("early_completion_count", 0))
    total_runs = int(throughput_summary.get("total_runs", 0))
    if total_runs > 0 and early_completions / total_runs > 0.5:
        for item in mechanism_budgets:
            item["allowed_followups"] += 1
            item["remaining_followups"] = max(0, item["allowed_followups"] - item["consumed_followups"])
            item["exhausted"] = item["remaining_followups"] <= 0

    mechanism_budgets.sort(key=lambda item: (item["exhausted"], item["remaining_followups"], item["mechanism"]))
    exploration_mode = "balanced"
    summary = "Use normal exploration budgeting."
    if exhausted_mechanisms:
        exploration_mode = "force_broad_exploration"
        summary = f"Mechanisms {', '.join(exhausted_mechanisms[:3])} exhausted their follow-up budget; broaden the search."
    elif under_explored:
        exploration_mode = "focus_promising"
        summary = f"Give extra follow-up budget to promising mechanisms like {sorted(under_explored)[0]}."

    return {
        "summary": summary,
        "exploration_mode": exploration_mode,
        "selection_mode": policy.get("selection_mode", "balanced"),
        "mechanism_budgets": mechanism_budgets,
    }


def write_budget(memory_dir: Path, output_path: Path | None = None) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = output_path or (memory_dir / "budget.json")
    write_json(path, build_budget(memory_dir))
    return path


def read_budget(memory_dir: Path) -> dict:
    path = memory_dir / "budget.json"
    if not path.exists():
        return default_budget()
    return json.loads(path.read_text(encoding="utf-8"))
