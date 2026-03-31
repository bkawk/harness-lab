# Hindsight

`harness-lab` now writes a hindsight artifact so the lab can critique its own recent evolution instead of only storing memory and rankings.

Output:

- `artifacts/memory/hindsight.json`

## What It Tries To Answer

- what did the lab repeat too long?
- which mechanisms look over-explored?
- which mechanisms look under-explored but promising?
- what policy adjustment should happen next?

This is the first explicit self-critique layer in the loop.

## Current Contents

The hindsight artifact summarizes:

- top repeated outcomes
- top repeated failure modes
- over-explored mechanisms
- under-explored promising mechanisms
- plain-language hindsight findings
- recommended policy adjustments

## CLI

Build hindsight manually with:

```bash
PYTHONPATH=src python3 scripts/build_hindsight.py
```

## Loop Integration

The normal loop now refreshes hindsight automatically whenever memory artifacts are rebuilt.

That means every candidate step now updates:

- `candidate_index.json`
- `parent_synthesis.json`
- `hindsight.json`

## Behavioral Effect

Hindsight is no longer only descriptive.

It now affects:

- parent ranking
  - under-explored promising mechanisms get a bonus
  - over-explored mechanisms get a penalty
- proposal drafting
  - hindsight policy adjustments are copied into the next proposal as explicit change items
  - the next proposal carries hindsight context in `memory_context.hindsight_context`

## Why It Matters

This is the difference between:

- “the lab remembers what happened”

and

- “the lab can say what it should have done differently”

That stronger retrospective judgment is important if the system is going to evolve its own proposal policy instead of only repeating local ranking heuristics.
