# Diagnosis Schema

The diagnosis artifact is the first place where `harness-lab` tries to turn raw traces into scientific judgment.

Each candidate keeps a structured diagnosis file at:

```text
artifacts/candidates/<candidate_id>/diagnosis/summary.json
```

## Required Fields

- `candidate_id`
- `status`
  - `empty`
  - `in_progress`
  - `complete`
- `summary`
  - short causal read of the candidate
- `severity`
  - `unknown`
  - `low`
  - `medium`
  - `high`
  - `critical`
- `mechanism`
  - the subsystem or harness component implicated
- `failure_modes`
  - repeated tags that support clustering
- `evidence`
  - concrete trace labels, benchmark clues, or audit clues
- `counterfactuals`
  - what should be tried next if this diagnosis is right

## Why This Exists

`mesh-para` recorded outcomes well but often compressed the reason too quickly.

This schema is meant to hold onto the causal story long enough for:

- proposal generation
- cross-run synthesis
- promotion decisions
- reframing decisions

## Initial CLI

Update a diagnosis with:

```bash
PYTHONPATH=src python3 scripts/update_diagnosis.py cand_0001 \
  --status complete \
  --severity high \
  --mechanism proposal_context \
  --summary "Repeated the same context packing pattern and produced redundant retries." \
  --failure-modes redundant_retries,weak_diagnosis \
  --evidence trace:planner,benchmark:no_gain \
  --counterfactuals "shrink context window, inject prior-failure summary"
```
