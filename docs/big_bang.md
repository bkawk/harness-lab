# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T14:53:41+00:00`
- last_heartbeat: `2026-03-31T15:01:25+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0037`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0037`
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
- `cand_0037`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0036`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0035`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0034`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0033`: outcome `stalled`; diagnosis `complete`; benchmark `None`

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
- summary: `Across 36 candidates the lab produced 7 keepers and 1 improved, but 7 stalled and 6 were audit-blocked. The recent window (cand_0030–0037) is entirely stalled with no audit or benchmark scores, indicating a systemic backend-startup or process-lifecycle problem rather than a modelling issue. Startup timeouts (5) and transfer collapse (3) dominate failure modes. Early-exit heuristics are saving meaningful wall-clock time (avg 396s saved per early exit) but the candidates they're applied to are not reaching audit, so the savings are moot until candidates can boot reliably.`
- adjustment: `Add a startup-health gate before any model-level evaluation: if the backend does not reach a ready state within a tight timeout, recycle the candidate immediately and log the infrastructure fault separately from model diagnosis.`
- adjustment: `When multiple backend fingerprints change simultaneously (≥4), require an incremental decomposition step—test subsets of changes in isolation before bundling them into a single candidate.`
- adjustment: `Raise priority for transfer-stability pre-checks so audit_blocked outcomes are caught before a full training run, not after.`

## Policy
- summary: `Stabilize backend startup before resuming model-level exploration. All 8 recent candidates stalled due to infrastructure faults (startup_timeout ×5, transfer_collapse ×3), not modelling errors. Add a startup-health gate to recycle broken candidates immediately and separate infra faults from model diagnosis. After 3 consecutive stalls, trigger configuration-bisect instead of emitting new candidates from the same change set.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.5`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `low`

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
- summary: `Recent branching still has room, but `instance_path_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
