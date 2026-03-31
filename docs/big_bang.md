# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T10:12:12+00:00`
- last_heartbeat: `2026-03-31T10:43:22+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0003`
- last dataset: `abc_boundary512_v64`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0003`
- dataset: `abc_boundary512_v64` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0003`
- published: `False`
- commit: `-`
- cycle mode: `normal_cycle`

## Recent Candidates
- `cand_0003`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36470791859428353`
- `cand_0002`: outcome `keeper`; diagnosis `complete`; benchmark `0.3137731112243285`
- `cand_0001`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28454701816760136`

## Science Leaders
- best benchmark: `cand_0003` -> `0.36470791859428353`
- best audit: `cand_0003` -> `0.33766418014737687`
- tightest transfer: `cand_0002` -> gap `-0.011832617593061645`
- best stable: `cand_0002` -> audit `0.32560572881739014`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.321009, audit averaged 0.326328, and the mean transfer gap was -0.005318.`
- recent benchmark avg: `0.3210093493287378`
- recent audit avg: `0.32632783208317423`
- recent transfer gap avg: `-0.005318482754436471`
- `cand_0003`: benchmark `0.36470791859428353`, audit `0.33766418014737687`, gap `0.027043738446906662`
- `cand_0002`: benchmark `0.3137731112243285`, audit `0.32560572881739014`, gap `-0.011832617593061645`
- `cand_0001`: benchmark `0.28454701816760136`, audit `0.3157135872847558`, gap `-0.03116656911715443`

## Hindsight
- summary: `The lab saw 2 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- selection_mode: `balanced`
- cooldown_multiplier: `1.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Use normal exploration budgeting.`
- exploration_mode: `balanced`
- tracked_mechanisms: `1`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
