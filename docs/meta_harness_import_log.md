# Meta-Harness Import Log

This log tracks the main ideas we wanted to absorb from the Meta-Harness artifact and whether they are already in `harness-lab`.

## Already Imported

- candidate bootstrap snapshot
  - each new candidate now starts with a compact scientific situation report
- polled command runner traces
  - command backends now write `traces/live_command.json`
- active backend dashboard surface
  - `docs/big_bang.md` can now show live backend state while a run is in flight

## Still Worth Importing

- stronger environment bootstrap for the runner command itself
  - include a compact preflight summary of toolchain, dataset readiness, and backend path directly in command traces
- earlier command-completion and stale-process handling
  - use polling data to classify:
    - completed quickly
    - stalled
    - crashed early
  - and feed that back into outcome labels and policy
- tighter completion discipline
  - add a final minimal-change or minimal-side-effects review before a candidate can be treated as a keeper
- higher-value use of bounded external review
  - optionally plug a real LLM reviewer into the new `external_review.json` contract
  - keep the split between:
    - `lab_advice`
    - `human_advice`
- command/runtime throughput accounting
  - preserve how much wall-clock was saved by polling or early completion detection
  - use that as another signal in policy and budget
- candidate preflight bundle
  - package the most relevant files for a candidate into one place before execution:
    - bootstrap snapshot
    - execution plan
    - proposal
    - diagnosis
    - backend/dataset readiness

## Current Recommendation

Let the lab run for a while before importing more.

The next import should be chosen from real evidence:

- if command runs stall, prioritize stale-process classification
- if keepers are noisy, prioritize stronger completion discipline
- if the lab gets repetitive, prioritize richer external review
