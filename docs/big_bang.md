# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T13:43:27+00:00`
- last_heartbeat: `2026-03-31T13:56:52+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0026`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0026`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0005`
- published: `False`
- commit: `-`
- cycle mode: `normal_cycle`

## Active Backend
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0026`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0025`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0024`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0023`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0022`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0013` -> `0.3847249926656351`
- best audit: `cand_0013` -> `0.34928376207439393`
- tightest transfer: `cand_0015` -> gap `-0.004213186536637714`
- best stable: `cand_0009` -> audit `0.3292391423260943`

## Science Trend
- summary: `No scored candidates yet.`
- recent benchmark avg: `None`
- recent audit avg: `None`
- recent transfer gap avg: `None`
- no scored candidates yet

## Hindsight
- summary: `Of 25 candidates, 7 were keepers and 6 were audit-blocked, indicating transfer-stability is the dominant bottleneck. The top failure modes—transfer_collapse (3) and transfer_regression (2)—confirm that proposals pass local benchmarks but fail under audit-level transfer checks. Five under-explored backend fingerprints (budget_policy_changed, fusion_changed, instance_path_changed, local_encoder_changed, loss_recipe_changed) each show a positive outcome on limited attempts and deserve more coverage. Recent candidates (cand_0019–cand_0026) are mostly unevaluated, with only cand_0026 resolved as stalled via loss_recipe_changed, so the pipeline may have a scoring or completion bottleneck.`
- adjustment: `Require a lightweight transfer-stability smoke check before any candidate is submitted to full audit, to reduce audit_blocked rate.`
- adjustment: `Raise priority for proposals targeting budget_policy_changed, fusion_changed, instance_path_changed, local_encoder_changed, and loss_recipe_changed—test each independently to identify which fingerprint drives the positive signal.`
- adjustment: `Flag candidates stuck without outcome or scores for more than one cycle and auto-escalate for diagnosis to clear the evaluation backlog.`

## Policy
- summary: `Require a lightweight transfer-stability smoke check before any candidate is submitted to full audit, to reduce audit_blocked rate.`
- selection_mode: `balanced`
- cooldown_multiplier: `1.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `4`

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
- summary: `Recent branching still has room, but `loss_recipe_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
