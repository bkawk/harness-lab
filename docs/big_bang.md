# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T19:56:46+00:00`
- last_heartbeat: `2026-03-31T19:58:34+00:00`
- cycles_completed: `4`
- genesis seed: `cand_0001`
- last candidate: `cand_0095`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `4`

## Latest Step
- candidate: `cand_0095`
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
- `cand_0095`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.363`
- `cand_0094`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.363`
- `cand_0093`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.294`
- `cand_0092`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.442`
- `cand_0091`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0092` -> `0.442`
- best audit: `cand_0092` -> `0.4055`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.365500, audit averaged 0.331125, and the mean transfer gap was 0.034375.`
- recent benchmark avg: `0.3655`
- recent audit avg: `0.331125`
- recent transfer gap avg: `0.034374999999999975`
- `cand_0095`: benchmark `0.363`, audit `0.3245`, gap `0.03849999999999998`
- `cand_0094`: benchmark `0.363`, audit `0.3295`, gap `0.033499999999999974`
- `cand_0093`: benchmark `0.294`, audit `0.265`, gap `0.02899999999999997`
- `cand_0092`: benchmark `0.442`, audit `0.4055`, gap `0.03649999999999998`

## Hindsight
- summary: `The lab saw 18 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 94 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- summary: `After 94 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- summary: `The humans recently addressed 3 lab request(s).`
- `dataset` addressed by `3b11024`: `Added named stratified evaluation slices so prepared datasets can separate benchmark, smoke, and audit behavior more clearly.`
- `ops` addressed by `a3c7559`: `Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.`
- `evaluation` addressed by `930a088`: `Implemented a transfer-stability smoke gate before full audit.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
