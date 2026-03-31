# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T14:20:19+00:00`
- last_heartbeat: `2026-03-31T14:20:34+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0026`
- last dataset: `abc_boundary512`
- last commit: `f36022df8375abd455c26bd2f60e1a97523a2ed7`
- last publish message: `Published f36022df8375abd455c26bd2f60e1a97523a2ed7 to origin/main.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- no completed big-bang step yet

## Active Backend
- active_candidate: `cand_0030`
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
- summary: `After 28 candidates the lab's dominant failure mode is transfer instability: 6 audit_blocked outcomes plus 3 transfer_collapse and 2 transfer_regression failures. Only 1 candidate reached 'improved'. Recent runs (cand_0022–0029) are mostly unevaluated, with cand_0026 stalled on a loss_recipe_changed edit. Five under-explored backend fingerprints each show a single positive outcome, suggesting the lab should broaden its backend-edit repertoire rather than repeat well-trodden paths.`
- adjustment: `Gate new candidates on a transfer-stability pre-check before full audit to catch collapse/regression early and reduce audit_blocked waste.`
- adjustment: `Prioritize proposals that combine under-explored fingerprints (budget_policy_changed, fusion_changed, instance_path_changed, local_encoder_changed) with explicit transfer-stability safeguards.`
- adjustment: `Investigate and clear the evaluation bottleneck blocking cand_0022–0025 and cand_0027–0029 before launching further candidates.`

## Policy
- summary: `Gate new candidates on a transfer-stability pre-check before full audit to catch collapse/regression early and reduce audit_blocked waste.`
- selection_mode: `balanced`
- cooldown_multiplier: `1.0`
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
- summary: `Recent branching still has room, but `instance_path_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
