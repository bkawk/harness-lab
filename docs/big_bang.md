# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T15:07:13+00:00`
- last_heartbeat: `2026-03-31T15:18:08+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0040`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0040`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0013`
- published: `False`
- commit: `-`
- cycle mode: `normal_cycle`

## Active Backend
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0040`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0039`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0038`: outcome `stalled`; diagnosis `empty`; benchmark `None`
- `cand_0037`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0036`: outcome `stalled`; diagnosis `complete`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0013` -> `0.3847249926656351`
- best audit: `cand_0013` -> `0.34928376207439393`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `No scored candidates yet.`
- recent benchmark avg: `None`
- recent audit avg: `None`
- recent transfer gap avg: `None`
- no scored candidates yet

## Hindsight
- summary: `Across 39 candidates the lab is dominated by stalled outcomes (10) and audit_blocked results (6), with only 1 improved and 7 keepers. The last 8 candidates (cand_0033–cand_0040) all stalled, every one carrying the same full set of backend fingerprints, indicating the search is stuck in a region where too many axes change simultaneously. Startup_timeout (8) is the leading failure mode, followed by transfer_collapse (3) and transfer_regression (2), confirming that transfer stability remains the central bottleneck.`
- adjustment: `Reduce simultaneous backend changes per candidate: isolate 1–2 fingerprint changes at a time instead of toggling all 6, so stall causes become identifiable.`
- adjustment: `Add a transfer-stability pre-check gate before full evaluation; reject candidates that regress on transfer metrics before they consume a full run budget.`
- adjustment: `Investigate and fix the startup_timeout path—8 of 10 early completions timing out means the harness infrastructure itself is a bottleneck, not candidate quality.`

## Policy
- summary: `Stabilize by isolating 1–2 fingerprint changes per candidate; fix startup_timeout infrastructure bottleneck before resuming broader search.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.5`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `low`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `7`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [4] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- `ops` addressed by `a3c7559`: `Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.`
- `evaluation` addressed by `930a088`: `Implemented a transfer-stability smoke gate before full audit.`

## Diversity
- summary: `Recent branching still has room, but `outcome_classifier_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
