# Outcome Schema

Each candidate needs a structured record of what actually happened after execution.

The outcome artifact lives at:

```text
artifacts/candidates/<candidate_id>/outcome/result.json
```

## Why This Exists

Without an outcome artifact, the loop stops at intention:

- proposal says what should change
- execution plan says how to test it
- but nothing structured says what happened

This file closes that loop.

## Core Fields

- `candidate_id`
- `status`
  - `pending`
  - `complete`
- `outcome_label`
  - examples:
    - `keeper`
    - `dead_end`
    - `audit_blocked`
    - `train_error`
- `benchmark`
  - `score`
  - `summary`
- `audit`
  - `score`
  - `summary`
- `observed_failure_modes`
- `evidence`

## Initial CLI

Record an outcome with:

```bash
PYTHONPATH=src python3 scripts/update_outcome.py cand_0002 \
  --status complete \
  --outcome-label dead_end \
  --benchmark-score 0.18 \
  --benchmark-summary "No improvement over parent trace." \
  --observed-failure-modes redundant_retries \
  --evidence trace:benchmark,metric:no_gain
```
