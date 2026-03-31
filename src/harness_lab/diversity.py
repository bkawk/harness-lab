from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from harness_lab.memory import build_candidate_index
from harness_lab.workspace import write_json


def default_diversity() -> dict:
    return {
        "summary": "No diversity signal yet.",
        "recent_window": 0,
        "current_mechanism_streak": 0,
        "novelty_step_recommended": False,
        "recent_mechanism_counts": [],
        "recent_mechanism_sequence": [],
    }


def _recent_mechanisms(index: dict, window: int) -> list[str]:
    recent = list(index.get("candidates", []))[-window:]
    mechanisms: list[str] = []
    for item in recent:
        mechanism = str(item.get("diagnosis_mechanism") or item.get("harness_component") or "").strip()
        if mechanism:
            mechanisms.append(mechanism)
    return mechanisms


def build_diversity(candidates_dir: Path, *, window: int = 6) -> dict:
    index = build_candidate_index(candidates_dir)
    mechanisms = _recent_mechanisms(index, window)
    recent_counts = Counter(mechanisms)
    streak = 0
    latest = mechanisms[-1] if mechanisms else ""
    for mechanism in reversed(mechanisms):
        if mechanism == latest and mechanism:
            streak += 1
        else:
            break
    novelty_step_recommended = streak >= 3
    summary = "Recent branching is reasonably diverse."
    if novelty_step_recommended and latest:
        summary = f"The lab has stayed on `{latest}` for {streak} recent candidates; inject a novelty step."
    elif latest:
        summary = f"Recent branching still has room, but `{latest}` is the current active line."

    ranked_counts = [{"mechanism": key, "count": count} for key, count in sorted(recent_counts.items(), key=lambda item: (-item[1], item[0]))]
    return {
        "summary": summary,
        "recent_window": window,
        "current_mechanism_streak": streak,
        "novelty_step_recommended": novelty_step_recommended,
        "recent_mechanism_counts": ranked_counts,
        "recent_mechanism_sequence": mechanisms,
    }


def write_diversity(candidates_dir: Path, output_path: Path, *, window: int = 6) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(output_path, build_diversity(candidates_dir, window=window))
    return output_path


def read_diversity(memory_dir: Path) -> dict:
    path = memory_dir / "diversity.json"
    if not path.exists():
        return default_diversity()
    return json.loads(path.read_text(encoding="utf-8"))
