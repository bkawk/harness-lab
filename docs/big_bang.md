# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T20:05:55+00:00`
- last_heartbeat: `2026-03-31T20:10:04+00:00`
- cycles_completed: `8`
- genesis seed: `cand_0001`
- last candidate: `cand_0115`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `8`

## Latest Step
- candidate: `cand_0115`
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
- `cand_0115`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.328`
- `cand_0114`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.283`
- `cand_0113`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.295`
- `cand_0112`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.446`
- `cand_0111`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.302`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.330800, audit averaged 0.291500, and the mean transfer gap was 0.039300.`
- recent benchmark avg: `0.3308`
- recent audit avg: `0.2915`
- recent transfer gap avg: `0.03929999999999998`
- `cand_0115`: benchmark `0.328`, audit `0.28`, gap `0.04799999999999999`
- `cand_0114`: benchmark `0.283`, audit `0.2565`, gap `0.026499999999999968`
- `cand_0113`: benchmark `0.295`, audit `0.2605`, gap `0.034499999999999975`
- `cand_0112`: benchmark `0.446`, audit `0.402`, gap `0.043999999999999984`
- `cand_0111`: benchmark `0.302`, audit `0.2585`, gap `0.04349999999999998`

## Hindsight
- summary: `The lab saw 38 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 114 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- status: `reviewed`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 114 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `startup_timeout` if that failure mode keeps dominating.`
- human advice: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `startup_timeout` if that failure mode keeps dominating.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `dataset` addressed by `3b11024`: `Added named stratified evaluation slices so prepared datasets can separate benchmark, smoke, and audit behavior more clearly.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
