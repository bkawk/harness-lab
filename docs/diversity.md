# Diversity

`harness-lab` now tracks recent branch diversity:

- `artifacts/memory/diversity.json`

This is the lab’s short-term memory of whether recent children are genuinely varied or just different versions of the same idea.

## What It Tracks

- recent mechanism sequence
- recent mechanism counts
- current mechanism streak
- whether a novelty step is recommended

## Why It Matters

Budget can stop an exhausted mechanism from dominating forever.

Diversity adds a shorter-horizon check:

- “even if this line still has some budget, have we been on it too many times in a row?”

That helps the lab avoid looking broad on paper while still feeling repetitive in practice.

## Current Integration

Diversity now affects:

- proposal drafting
  - recent mechanism streaks can trigger a novelty step
  - proposals can carry `diversity_novelty_step` or `diversity_warning`
  - proposals now include `memory_context.diversity_context`
- `big-bang`
  - the repo dashboard shows the current diversity summary and streak state
  - novelty-recommended cycles are now surfaced as explicit `novelty_cycle` control-plane states

## CLI

Build diversity manually with:

```bash
PYTHONPATH=src python3 scripts/build_diversity.py
```
