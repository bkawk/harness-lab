# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T15:07:13+00:00`
- last_heartbeat: `2026-03-31T15:07:26+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0037`
- last dataset: `abc_boundary512`
- last commit: `d2e7a85d341dce611b6b5efe67b5e34e2a73bf0c`
- last publish message: `Published d2e7a85d341dce611b6b5efe67b5e34e2a73bf0c to origin/main.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- no completed big-bang step yet

## Active Backend
- active_candidate: `cand_0039`
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
- summary: `The lab saw 6 audit-blocked outcomes; it should have emphasized transfer-stability checks earlier.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
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
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [4] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- `ops` addressed by `a3c7559`: `Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.`
- `evaluation` addressed by `930a088`: `Implemented a transfer-stability smoke gate before full audit.`

## Diversity
- summary: `Recent branching still has room, but `budget_policy_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
