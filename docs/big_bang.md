# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T20:10:40+00:00`
- last_heartbeat: `2026-03-31T20:13:41+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0122`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `6`

## Latest Step
- candidate: `cand_0122`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `novelty_cycle`

## Active Backend
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0122`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.374`
- `cand_0121`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.38`
- `cand_0120`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.327`
- `cand_0119`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.446`
- `cand_0118`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.441`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.393600, audit averaged 0.359500, and the mean transfer gap was 0.034100.`
- recent benchmark avg: `0.3936`
- recent audit avg: `0.3595`
- recent transfer gap avg: `0.03410000000000002`
- `cand_0122`: benchmark `0.374`, audit `0.348`, gap `0.026000000000000023`
- `cand_0121`: benchmark `0.38`, audit `0.354`, gap `0.026000000000000023`
- `cand_0120`: benchmark `0.327`, audit `0.2925`, gap `0.03450000000000003`
- `cand_0119`: benchmark `0.446`, audit `0.4085`, gap `0.03750000000000003`
- `cand_0118`: benchmark `0.441`, audit `0.3945`, gap `0.046499999999999986`

## Hindsight
- summary: `The lab saw 44 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `8`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`

## What We Did
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
