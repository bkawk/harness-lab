# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T15:30:02+00:00`
- last_heartbeat: `2026-03-31T15:41:13+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0042`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0042`
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
- `cand_0042`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0041`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0040`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0039`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0038`: outcome `stalled`; diagnosis `empty`; benchmark `None`

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
- summary: `Across 41 candidates the lab is dominated by stalls (12) and audit blocks (6), with only 1 improved and 7 keepers. The last 8 candidates (cand_0035–0042) all stalled with identical 6-fingerprint changesets, indicating the search is stuck in a region where too many backend axes change simultaneously. Startup timeouts account for 10 of 18 failure-mode hits, confirming that candidates never reach evaluation. Transfer-stability failures (collapse + regression = 5) remain the second-largest cluster and feed directly into the audit-blocked outcomes.`
- adjustment: `Cap simultaneous backend fingerprint changes at 2 per candidate to reduce startup-timeout risk and improve fault isolation.`
- adjustment: `Add a fast pre-flight check (< 30s) that verifies process startup before committing full evaluation budget.`
- adjustment: `After 3 consecutive stalls with the same fingerprint set, force a fallback to single-axis mutation to isolate the blocking change.`

## Policy
- summary: `Cap simultaneous backend fingerprint changes at 2 per candidate and tighten startup-timeout ceiling to break the 8-candidate stall streak; fall back to single-axis mutation after 3 consecutive stalls with the same fingerprint set.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.5`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `low`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `8`

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
- summary: `The lab has 2 ranked requests for human help.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [4] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- `ops` addressed by `a3c7559`: `Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.`
- `evaluation` addressed by `930a088`: `Implemented a transfer-stability smoke gate before full audit.`

## Diversity
- summary: `Recent branching still has room, but `startup_timeout` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
