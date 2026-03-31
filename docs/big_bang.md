# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T14:20:19+00:00`
- last_heartbeat: `2026-03-31T14:34:39+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0030`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0030`
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
- `cand_0030`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0029`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0028`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0027`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0026`: outcome `stalled`; diagnosis `complete`; benchmark `None`

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
- summary: `After 29 candidates the lab's dominant failure mode is transfer instability: 6 audit_blocked outcomes plus 3 transfer_collapse and 2 transfer_regression failures. Two recent runs (cand_0026, cand_0030) stalled on loss_recipe_changed, and 6 of the last 8 candidates lack scored outcomes, signalling a data-completeness gap. The single 'improved' outcome came from a candidate touching budget_policy_changed, fusion_changed, instance_path_changed, local_encoder_changed, and loss_recipe_changed — all under-explored fingerprints with a positive audit signal (~0.31).`
- adjustment: `Gate new candidate submissions on completing evaluation of the unscored backlog (cand_0023–cand_0029) before launching further runs.`
- adjustment: `Raise priority for proposals that pair loss_recipe_changed with a transfer-stability edit (e.g., fusion_changed or budget_policy_changed) rather than using it alone.`
- adjustment: `Raise priority for budget_policy_changed and instance_path_changed edits; both are under-explored with positive audit evidence.`

## Policy
- summary: `Gate new candidate submissions on completing evaluation of the unscored backlog (cand_0023–cand_0029) before launching further runs. Transfer instability is the binding constraint; prioritize paired edits that combine loss_recipe_changed with stabilisation mechanisms.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `6`

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

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`

## Diversity
- summary: `Recent branching still has room, but `loss_recipe_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
