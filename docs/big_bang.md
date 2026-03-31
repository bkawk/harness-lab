# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T20:18:57+00:00`
- last_heartbeat: `2026-03-31T20:23:51+00:00`
- cycles_completed: `9`
- genesis seed: `cand_0001`
- last candidate: `cand_0140`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `9`

## Latest Step
- candidate: `cand_0140`
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
- `cand_0140`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.317`
- `cand_0139`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.292`
- `cand_0138`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.326`
- `cand_0137`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.409`
- `cand_0136`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.337`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.336200, audit averaged 0.302000, and the mean transfer gap was 0.034200.`
- recent benchmark avg: `0.3362`
- recent audit avg: `0.302`
- recent transfer gap avg: `0.03420000000000001`
- `cand_0140`: benchmark `0.317`, audit `0.2835`, gap `0.03350000000000003`
- `cand_0139`: benchmark `0.292`, audit `0.2555`, gap `0.03649999999999998`
- `cand_0138`: benchmark `0.326`, audit `0.297`, gap `0.029000000000000026`
- `cand_0137`: benchmark `0.409`, audit `0.3805`, gap `0.02849999999999997`
- `cand_0136`: benchmark `0.337`, audit `0.2935`, gap `0.04350000000000004`

## Hindsight
- summary: `The lab saw 62 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
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
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
