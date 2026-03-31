# Execution Plan

Each candidate should explain not only what it proposes, but how it expects to be evaluated.

The execution plan lives at:

```text
artifacts/candidates/<candidate_id>/execution/plan.json
```

## Why This Exists

The previous lab generation often mixed:

- proposal content
- execution assumptions
- success criteria
- audit expectations

This artifact separates them so the harness can reason about:

- what benchmark evidence to collect
- when audit is required
- what would count as a meaningful success
- what failure signals should trigger diagnosis updates

## Core Fields

- `candidate_id`
- `status`
- `benchmark`
  - `objective`
  - `steps`
  - `success_signals`
- `audit`
  - `required`
  - `steps`
  - `failure_signals`
- `trace_capture`
- `rationale`

## Initial CLI

Create or refresh a plan with:

```bash
PYTHONPATH=src python3 scripts/plan_execution.py cand_0002
```
