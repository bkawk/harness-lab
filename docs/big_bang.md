# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-14T21:24:31+00:00`
- cycles_completed: `1554`
- genesis seed: `cand_0001`
- last candidate: `cand_1978`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `249`

## Latest Step
- candidate: `cand_1978`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `normal_cycle`

## Active Backend
- active_candidate: `cand_1978`
- backend_status: `finished`
- backend_pid: `2992615`
- backend_started_at: `2026-04-14T21:14:27+00:00`
- backend_last_poll_at: `2026-04-14T21:24:28+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1978`: outcome `dead_end`; diagnosis `complete`; benchmark `0.35539731804179336`
- `cand_1977`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3249487801142954`
- `cand_1976`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.37848114157520596`
- `cand_1975`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.37552345141175497`
- `cand_1974`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29521488657147676`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_1625` -> gap `-0.00015162972740001557`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.345913, audit averaged 0.311325, and the mean transfer gap was 0.034588.`
- recent benchmark avg: `0.34591311554290527`
- recent audit avg: `0.3113254208290018`
- recent transfer gap avg: `0.034587694713903536`
- `cand_1978`: benchmark `0.35539731804179336`, audit `0.3164740285966389`, gap `0.03892328944515444`
- `cand_1977`: benchmark `0.3249487801142954`, audit `0.3203222677774963`, gap `0.004626512336799116`
- `cand_1976`: benchmark `0.37848114157520596`, audit `0.32014770667701153`, gap `0.058333434898194425`
- `cand_1975`: benchmark `0.37552345141175497`, audit `0.3303328861092177`, gap `0.04519056530253729`
- `cand_1974`: benchmark `0.29521488657147676`, audit `0.26935021498464434`, gap `0.02586467158683242`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms science_loss, science_train, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (1869 candidate(s), avg transfer gap 0.032236).`
- recommended_action: `wait`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 602.0 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1978`
- eval: `transfer_smoke_max_gap=0.025, transfer_smoke_min_score=0.22`

### Effective Backend Settings
- source_candidate: `cand_1978`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.22, transfer_smoke_max_gap=0.025, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1869`, audit_blocked `783`, avg_gap `0.032235646953165616`
- loss: `science_loss` (available); attempts `1854`, audit_blocked `769`, avg_gap `0.03218592055916578`
- eval: `science_eval` (targeted); attempts `1861`, audit_blocked `775`, avg_gap `0.032191868360611144`
- config: `science_config` (available); attempts `1854`, audit_blocked `769`, avg_gap `0.03218592055916578`
- train: `science_train` (available); attempts `1847`, audit_blocked `762`, avg_gap `0.03215416571266835`

### Recent Module Evidence
- `science_backend`: attempts `1869`, audit_blocked `783`, avg_gap `0.032235646953165616`
- `science_model`: attempts `1869`, audit_blocked `783`, avg_gap `0.032235646953165616`
- `science_eval`: attempts `1861`, audit_blocked `775`, avg_gap `0.032191868360611144`
- `science_config`: attempts `1854`, audit_blocked `769`, avg_gap `0.03218592055916578`

### Code Context
- summary: `Backend code context maps the five modular science seams to their key functions, bounded lever surfaces, fixed implementation surfaces, and likely failure-mode touchpoints.`
- target_file: `src/harness_lab/science_eval.py`
- target_purpose: `Runs smoke-gate and audit outcome classification logic, including hard-fail rules and keeper thresholds.`
- key_functions: `should_run_full_audit, classify_smoke_block, classify_outcome`
- levered_surfaces: `transfer_smoke_min_score, transfer_smoke_max_gap, transfer_smoke_min_boundary_f1`
- fixed_surfaces: `Hard-fail rules for severe smoke regressions; Keeper/improved/audit_blocked/dead_end classification bands; Primary failure-mode attribution ordering`

### Failure-To-Code Hints
- `boundary_smoke:gap_too_wide` -> `science_eval, science_loss, science_model`: `Boundary smoke regressions often reflect a mix of strict smoke-gap thresholds, weak boundary pressure in the loss, or insufficient boundary-sensitive representation capacity.`
- `hard_transfer_regression` -> `science_loss, science_model, science_config`: `Hard-transfer failures usually point to brittle transfer-sensitive structure, insufficient representation robustness, or seed defaults that underweight difficult cases.`
- `transfer_smoke:gap_too_wide` -> `science_eval, science_model`: `A wide benchmark-to-smoke gap is often governed by smoke gate strictness and by whether the model capacity generalizes beyond the local benchmark slice.`

### Code Change Brief
- decision_state: `wait`
- decision_reason: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`
- target_file: `src/harness_lab/science_eval.py`
- target_functions: `should_run_full_audit, classify_smoke_block, classify_outcome`
- proposed_change: `Tighten or clarify smoke and audit classification so severe non-robustness fails earlier while borderline promising runs remain distinguishable.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `wait`
- target_file: `src/harness_lab/science_eval.py`
- max_changed_files: `3`
- allowed_write_files: `src/harness_lab/science_eval.py, tests/test_science_smoke_gate.py, tests/test_science_eval.py`
- focused_tests: `tests/test_science_smoke_gate.py, tests/test_science_eval.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `wait`, so autonomous code mutation stays blocked. Recommended action is `wait`, not `targeted_mutation`. Allowed write scope is 3 files; autonomous mutation requires a target file plus adjacent tests only.`
- execution_mode: `candidate_workspace_only`
- auto_publish: `False`
- silent_rollback: `False`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_eval` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
