# Policy

`harness-lab` now writes an explicit policy state derived from hindsight and hardware context.

Output:

- `artifacts/memory/policy.json`

## What Policy Controls

The current policy layer is lightweight but real. It can influence:

- selection mode
- cooldown strength
- under-explored mechanism bonus
- preferred runner backend
- publish cadence for `big-bang`
- novelty cycle priority

## Why It Exists

Hindsight tells the lab what it should have done differently.

Policy is the next layer:

- hindsight -> judgment
- policy -> changed behavior

Without policy, the lab can critique itself but still act the same way.

## Current Integration

Policy now affects:

- parent synthesis
  - over-explored penalties scale with `cooldown_multiplier`
  - under-explored bonuses come from policy
- proposal drafting
  - proposals now carry `memory_context.policy_context`
  - proposals add policy-aware change items
- `big-bang`
  - the dashboard shows current policy
  - publish cadence follows `publish_every_cycles`
  - `--runner-backend auto` follows `preferred_runner_backend`

## CLI Surface

Build policy manually with:

```bash
PYTHONPATH=src python3 scripts/build_policy.py
```

Policy is also refreshed automatically whenever memory artifacts are refreshed through the normal loop.
