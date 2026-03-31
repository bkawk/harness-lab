# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T18:35:17+00:00`
- last_heartbeat: `2026-03-31T18:55:55+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0085`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0085`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0079`
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
- `cand_0085`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32620864478060324`
- `cand_0084`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3185653946291464`
- `cand_0083`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0082`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2967862979088503`
- `cand_0081`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0079` -> `0.3904422083225122`
- best audit: `cand_0013` -> `0.34928376207439393`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.313853, audit averaged 0.261755, and the mean transfer gap was 0.052099.`
- recent benchmark avg: `0.3138534457728666`
- recent audit avg: `0.26175465470825493`
- recent transfer gap avg: `0.05209879106461174`
- `cand_0085`: benchmark `0.32620864478060324`, audit `0.24851853042575162`, gap `0.07769011435485162`
- `cand_0084`: benchmark `0.3185653946291464`, audit `0.26521645234857905`, gap `0.05334894228056736`
- `cand_0082`: benchmark `0.2967862979088503`, audit `0.2715289813504341`, gap `0.025257316558416232`

## Hindsight
- summary: `The lab saw 10 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 84 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- summary: `After 84 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
