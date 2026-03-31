# Budget

`harness-lab` now writes an explicit exploration budget:

- `artifacts/memory/budget.json`

This sits one level above policy.

## What Budget Controls

Budget answers:

- how many follow-ups should a mechanism still get?
- which mechanisms are exhausted?
- when should the lab force broader exploration?

## Current Integration

Budget now affects:

- parent synthesis
  - exhausted mechanisms get a strong penalty
  - mechanisms with headroom get a small boost
- proposal drafting
  - proposals now carry `memory_context.budget_context`
  - proposals add budget-aware guardrails and exploration notes
  - when the budget says `force_broad_exploration`, the next proposal tries to jump to a different mechanism on purpose
- `big-bang`
  - the dashboard shows the current budget summary and exploration mode

## Why It Matters

Without a budget layer, the lab can still get stuck exploiting the same promising-looking mechanism too long.

Budget gives the control plane a simple answer to:

- “have we already given this idea enough chances?”

That is the start of explicit exploration budgeting rather than implicit repetition.
