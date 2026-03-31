# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T14:46:46+00:00`
- last_heartbeat: `2026-03-31T14:51:15+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0033`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0033`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0013`
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
- `cand_0033`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0032`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0031`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0030`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0029`: outcome `-`; diagnosis `empty`; benchmark `None`

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
- summary: `Across 32 candidates the lab produced 7 keepers and 1 improved, but 6 audit-blocked outcomes and 3 stalls reveal two systemic gaps: transfer-stability checks arrive too late, and broad multi-fingerprint changes (cand_0031–0033) stall before producing signal. The dominant failure mode is transfer_collapse (3), followed by stale_process (2) and transfer_regression (2). Recent candidates (cand_0027–0029) lack outcome labels entirely, suggesting incomplete evaluation or silent failures in the pipeline.`
- adjustment: `Run a transfer-stability smoke check before full audit; reject candidates showing transfer_collapse or transfer_regression signals at the smoke-gate stage.`
- adjustment: `Cap simultaneous backend fingerprint changes at 3 per candidate; cand_0031–0033 show that 6-fingerprint changes stall without yielding evaluable outcomes.`
- adjustment: `After a loss_recipe_changed stall, require the next candidate using that mechanism to include an explicit stability patch before re-entry (prevents the cand_0026 → cand_0030 repeat).`

## Policy
- summary: `Run a transfer-stability smoke check before full audit; reject candidates showing transfer_collapse or transfer_regression signals at the smoke-gate stage.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `7`

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
- summary: `Recent branching still has room, but `outcome_classifier_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
