# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T10:44:47+00:00`
- last_heartbeat: `2026-03-31T10:54:49+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0005`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0005`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0005`
- published: `False`
- commit: `-`
- cycle mode: `novelty_cycle`

## Recent Candidates
- `cand_0005`: outcome `improved`; diagnosis `complete`; benchmark `0.2932505653803283`
- `cand_0004`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0003`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36470791859428353`
- `cand_0002`: outcome `keeper`; diagnosis `complete`; benchmark `0.3137731112243285`
- `cand_0001`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28454701816760136`

## Science Leaders
- best benchmark: `cand_0003` -> `0.36470791859428353`
- best audit: `cand_0003` -> `0.33766418014737687`
- tightest transfer: `cand_0002` -> gap `-0.011832617593061645`
- best stable: `cand_0002` -> audit `0.32560572881739014`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.314070, audit averaged 0.321611, and the mean transfer gap was -0.007541.`
- recent benchmark avg: `0.3140696533416354`
- recent audit avg: `0.3216110612598368`
- recent transfer gap avg: `-0.007541407918201376`
- `cand_0005`: benchmark `0.2932505653803283`, audit `0.3074607487898244`, gap `-0.014210183409496091`
- `cand_0003`: benchmark `0.36470791859428353`, audit `0.33766418014737687`, gap `0.027043738446906662`
- `cand_0002`: benchmark `0.3137731112243285`, audit `0.32560572881739014`, gap `-0.011832617593061645`
- `cand_0001`: benchmark `0.28454701816760136`, audit `0.3157135872847558`, gap `-0.03116656911715443`

## Hindsight
- summary: `The lab saw 2 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
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

## Diversity
- summary: `The lab has stayed on `initial_harness` for 5 recent candidates; inject a novelty step.`
- current_mechanism_streak: `5`
- novelty_step_recommended: `True`
