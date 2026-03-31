# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T11:37:20+00:00`
- last_heartbeat: `2026-03-31T12:29:45+00:00`
- cycles_completed: `5`
- genesis seed: `cand_0001`
- last candidate: `cand_0015`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0015`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0005`
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
- `cand_0015`: outcome `keeper`; diagnosis `complete`; benchmark `0.3135445321688846`
- `cand_0014`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.352639679895705`
- `cand_0013`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3847249926656351`
- `cand_0012`: outcome `keeper`; diagnosis `complete`; benchmark `0.3108136488217508`
- `cand_0011`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.46583702651600367`

## Science Leaders
- best benchmark: `cand_0011` -> `0.46583702651600367`
- best audit: `cand_0011` -> `0.36377532164684445`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.365512, audit averaged 0.329403, and the mean transfer gap was 0.036109.`
- recent benchmark avg: `0.3655119760135958`
- recent audit avg: `0.32940282759528694`
- recent transfer gap avg: `0.03610914841830891`
- `cand_0015`: benchmark `0.3135445321688846`, audit `0.31775771870552233`, gap `-0.004213186536637714`
- `cand_0014`: benchmark `0.352639679895705`, audit `0.3119135206432276`, gap `0.04072615925247741`
- `cand_0013`: benchmark `0.3847249926656351`, audit `0.34928376207439393`, gap `0.03544123059124116`
- `cand_0012`: benchmark `0.3108136488217508`, audit `0.3042838149064463`, gap `0.006529833915304484`
- `cand_0011`: benchmark `0.46583702651600367`, audit `0.36377532164684445`, gap `0.10206170486915922`

## Hindsight
- summary: `The lab saw 6 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Raise priority for backend edits tagged `budget_policy_changed`.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- selection_mode: `balanced`
- cooldown_multiplier: `1.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `1`

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

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
