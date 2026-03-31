# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T20:05:55+00:00`
- last_heartbeat: `2026-03-31T20:09:29+00:00`
- cycles_completed: `7`
- genesis seed: `cand_0001`
- last candidate: `cand_0114`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `7`

## Latest Step
- candidate: `cand_0114`
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
- `cand_0114`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.283`
- `cand_0113`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.295`
- `cand_0112`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.446`
- `cand_0111`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.302`
- `cand_0110`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.321200, audit averaged 0.281800, and the mean transfer gap was 0.039400.`
- recent benchmark avg: `0.3212`
- recent audit avg: `0.2818`
- recent transfer gap avg: `0.039399999999999984`
- `cand_0114`: benchmark `0.283`, audit `0.2565`, gap `0.026499999999999968`
- `cand_0113`: benchmark `0.295`, audit `0.2605`, gap `0.034499999999999975`
- `cand_0112`: benchmark `0.446`, audit `0.402`, gap `0.043999999999999984`
- `cand_0111`: benchmark `0.302`, audit `0.2585`, gap `0.04349999999999998`
- `cand_0110`: benchmark `0.28`, audit `0.2315`, gap `0.048500000000000015`

## Hindsight
- summary: `The lab saw 37 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
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
- summary: `The humans recently addressed 1 lab request(s).`
- `dataset` addressed by `3b11024`: `Added named stratified evaluation slices so prepared datasets can separate benchmark, smoke, and audit behavior more clearly.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
