# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T15:30:02+00:00`
- last_heartbeat: `2026-03-31T15:35:14+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0041`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0041`
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
- `cand_0041`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0040`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0039`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0038`: outcome `stalled`; diagnosis `empty`; benchmark `None`
- `cand_0037`: outcome `stalled`; diagnosis `complete`; benchmark `None`

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
- summary: `Across 40 candidates the lab is dominated by stalls (11) and audit blocks (6), with only 1 improved and 7 keepers. The last 8 candidates (cand_0034–0041) all stalled with identical 6-fingerprint changesets, indicating the search is stuck in a region where too many backends change simultaneously. Startup timeouts (9) are the leading failure mode, followed by transfer collapse (3) and transfer regression (2). Early-exit heuristics saved ~5k seconds across 11 runs, but the exploration loop is not converting that time savings into progress.`
- adjustment: `Cap simultaneous backend changes at 2 per candidate; the 6-fingerprint changeset pattern produces only stalls.`
- adjustment: `Investigate and fix startup_timeout root cause (9 occurrences) before launching more candidates—this is infrastructure waste, not search signal.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Cap simultaneous backend changes at 2 per candidate; fix startup_timeout infrastructure before spending more search budget; prioritize transfer-stability proposals after audit blocks.`
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
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [4] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- `ops` addressed by `a3c7559`: `Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.`
- `evaluation` addressed by `930a088`: `Implemented a transfer-stability smoke gate before full audit.`

## Diversity
- summary: `Recent branching still has room, but `fusion_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
