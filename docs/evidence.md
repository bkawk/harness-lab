# Evidence Capture

`harness-lab` now treats source provenance and raw runner traces as first-class candidate artifacts.

Each evolved candidate should leave behind:

- a harness source snapshot under `source/repo_snapshot/`
- a source manifest under `source/manifest.json`
- a parent diff under `patches/against_parent.patch`
- a patch summary under `patches/summary.json`
- backend command and output traces under `traces/`

## Why This Matters

This is the bridge back to the Meta-Harness idea:

- proposals should be grounded in full prior evidence
- source state should be inspectable, not inferred
- execution should leave raw traces, not just scalar outcomes

Even while the runner is still simulated, the candidate workspace now preserves:

- which harness files were present
- which repo commit and branch they came from
- whether the repo was dirty at capture time
- what command the backend ran
- what stdout and stderr it produced

## Key Files

- `source/manifest.json`
  - commit, branch, dirty state, tracked files, capture time
- `patches/summary.json`
  - changed file list and patch count relative to parent
- `patches/against_parent.patch`
  - combined unified diff against the parent snapshot
- `traces/run.json`
  - backend, command, cwd, timings, return code, and outcome summary
- `traces/runner_stdout.log`
  - raw backend stdout
- `traces/runner_stderr.log`
  - raw backend stderr

## Current Boundary

Today the backend is still `simulated`, but the evidence path is no longer fake:

- the runner invokes a real subprocess
- trace files are written to disk
- the outcome is linked back to those traces

The next step is to swap the simulated backend for a real mesh-to-parametric evaluation path without changing the candidate workspace contract.
