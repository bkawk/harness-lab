# Parent Synthesis

Before drafting the next proposal, `harness-lab` should explain which prior candidate is the best parent and why.

The synthesis artifact lives at:

```text
artifacts/memory/parent_synthesis.json
```

## What It Does

- ranks prior candidates as seeds for the next child
- makes parent selection inspectable instead of implicit
- carries forward score reasons into proposal memory context

## Initial Scoring Dimensions

- diagnosis completeness
- diagnosis severity
- number of failure modes captured
- presence of a causal summary
- presence of a mechanism
- lineage context

## Initial CLI

Write the synthesis artifact with:

```bash
PYTHONPATH=src python3 scripts/synthesize_parents.py --write-index
```

This refreshes:

- `artifacts/memory/candidate_index.json`
- `artifacts/memory/parent_synthesis.json`
