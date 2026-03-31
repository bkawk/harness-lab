# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T10:12:12+00:00`
- last_heartbeat: `2026-03-31T10:22:13+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0001`
- last dataset: `abc_boundary512_v64`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0001`
- dataset: `abc_boundary512_v64` via `reused_prepared_dataset`
- seed action: `genesis_ready`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0001`
- published: `False`
- commit: `-`
- cycle mode: `normal_cycle`

## Recent Candidates
- `cand_0001`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28454701816760136`

## Science Leaders
- best benchmark: `cand_0001` -> `0.28454701816760136`
- best audit: `cand_0001` -> `0.3157135872847558`
- tightest transfer: `cand_0001` -> gap `-0.03116656911715443`
- best stable: `-` -> audit `-`

## Science Trend
- summary: `Across the last 1 scored candidates, benchmark averaged 0.284547, audit averaged 0.315714, and the mean transfer gap was -0.031167.`
- recent benchmark avg: `0.28454701816760136`
- recent audit avg: `0.3157135872847558`
- recent transfer gap avg: `-0.03116656911715443`
- `cand_0001`: benchmark `0.28454701816760136`, audit `0.3157135872847558`, gap `-0.03116656911715443`

## Hindsight
- summary: `The lab saw 1 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- selection_mode: `balanced`
- cooldown_multiplier: `1.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `normal`

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
- summary: `Recent branching still has room, but `initial_harness` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
