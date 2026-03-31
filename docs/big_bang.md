# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T11:03:54+00:00`
- last_heartbeat: `2026-03-31T11:35:05+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0009`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0009`
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
- `cand_0009`: outcome `keeper`; diagnosis `complete`; benchmark `0.3027662528883464`
- `cand_0008`: outcome `keeper`; diagnosis `complete`; benchmark `0.32574714077255956`
- `cand_0007`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.382538488978586`
- `cand_0006`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0005`: outcome `improved`; diagnosis `complete`; benchmark `0.2932505653803283`

## Science Leaders
- best benchmark: `cand_0007` -> `0.382538488978586`
- best audit: `cand_0003` -> `0.33766418014737687`
- tightest transfer: `cand_0008` -> gap `0.00592187393956084`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.326076, audit averaged 0.318730, and the mean transfer gap was 0.007346.`
- recent benchmark avg: `0.32607561200495505`
- recent audit avg: `0.3187299378731327`
- recent transfer gap avg: `0.007345674131822355`
- `cand_0009`: benchmark `0.3027662528883464`, audit `0.3292391423260943`, gap `-0.026472889437747893`
- `cand_0008`: benchmark `0.32574714077255956`, audit `0.3198252668329987`, gap `0.00592187393956084`
- `cand_0007`: benchmark `0.382538488978586`, audit `0.31839459354361344`, gap `0.06414389543497256`
- `cand_0005`: benchmark `0.2932505653803283`, audit `0.3074607487898244`, gap `-0.014210183409496091`

## Hindsight
- summary: `The lab saw 3 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
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
