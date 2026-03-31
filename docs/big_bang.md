# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T15:07:13+00:00`
- last_heartbeat: `2026-03-31T15:12:33+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0039`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0039`
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
- `cand_0039`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0038`: outcome `stalled`; diagnosis `empty`; benchmark `None`
- `cand_0037`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0036`: outcome `stalled`; diagnosis `complete`; benchmark `None`
- `cand_0035`: outcome `stalled`; diagnosis `complete`; benchmark `None`

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
- summary: `Across 38 candidates the lab is dominated by stalls (9) and audit blocks (6), with only 1 improved outcome. The last 8 candidates (cand_0032–0039) all stalled, every one carrying the same 6-fingerprint bundle, indicating the search is stuck in a single region of the design space. Startup timeouts (7) are the leading failure mode and account for most early-exit time savings, but they also mean many candidates never produce usable signal. Transfer-related failures (collapse + regression = 5) remain the second-largest cluster and feed directly into the audit-blocked outcomes.`
- adjustment: `Cap simultaneous fingerprint changes at 2–3 per candidate so stall/failure causes can be isolated.`
- adjustment: `After 3 consecutive stalls with the same fingerprint set, force the proposer to drop at least 2 of those axes before the next candidate.`
- adjustment: `Add a transfer-stability pre-check (lightweight probe on a held-out transfer split) before committing to a full run; gate audit submission on passing it.`

## Policy
- summary: `Cap simultaneous fingerprint changes at 2–3 per candidate to isolate stall causes; force fingerprint rotation after 3 consecutive stalls; add transfer-stability pre-check before full runs; penalise startup-timeout-prone configurations in proposal scoring.`
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
- summary: `Recent branching still has room, but `loss_recipe_changed` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
