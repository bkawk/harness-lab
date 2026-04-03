# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T08:14:34+00:00`
- cycles_completed: `64`
- genesis seed: `cand_0001`
- last candidate: `cand_0488`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `7`

## Latest Step
- candidate: `cand_0488`
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
- active_candidate: `cand_0488`
- backend_status: `finished`
- backend_pid: `2572365`
- backend_started_at: `2026-04-03T08:04:31+00:00`
- backend_last_poll_at: `2026-04-03T08:14:33+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0488`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2945081219577682`
- `cand_0487`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33176724944463015`
- `cand_0486`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3962179916217762`
- `cand_0485`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2989685321361417`
- `cand_0484`: outcome `keeper`; diagnosis `complete`; benchmark `0.30975248878043204`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0482` -> audit `0.3819516821922625`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.326243, audit averaged 0.293004, and the mean transfer gap was 0.033239.`
- recent benchmark avg: `0.32624287678814967`
- recent audit avg: `0.2930039889251259`
- recent transfer gap avg: `0.033238887863023744`
- `cand_0488`: benchmark `0.2945081219577682`, audit `0.22013978859963576`, gap `0.07436833335813245`
- `cand_0487`: benchmark `0.33176724944463015`, audit `0.29509117653573996`, gap `0.03667607290889019`
- `cand_0486`: benchmark `0.3962179916217762`, audit `0.31633282084939895`, gap `0.07988517077237722`
- `cand_0485`: benchmark `0.2989685321361417`, audit `0.2988030610322522`, gap `0.00016547110388953623`
- `cand_0484`: benchmark `0.30975248878043204`, audit `0.33465309760860273`, gap `-0.02490060882817069`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, science_loss, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (379 candidate(s), avg transfer gap 0.035621).`
- recommended_action: `targeted_mutation`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 649.5 MB on average, leaving most VRAM unused. 29 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `29`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0488`
- model: `instance_dim=24, instance_modulation_scale=0.15`

### Effective Backend Settings
- source_candidate: `cand_0488`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `379`, audit_blocked `197`, avg_gap `0.03562093402341868`
- loss: `science_loss` (available); attempts `364`, audit_blocked `183`, avg_gap `0.0354912725752985`
- eval: `science_eval` (targeted); attempts `371`, audit_blocked `189`, avg_gap `0.03546495600044029`
- config: `science_config` (available); attempts `364`, audit_blocked `183`, avg_gap `0.0354912725752985`
- train: `science_train` (available); attempts `357`, audit_blocked `176`, avg_gap `0.03538558116253731`

### Recent Module Evidence
- `science_backend`: attempts `379`, audit_blocked `197`, avg_gap `0.03562093402341868`
- `science_model`: attempts `379`, audit_blocked `197`, avg_gap `0.03562093402341868`
- `science_eval`: attempts `371`, audit_blocked `189`, avg_gap `0.03546495600044029`
- `science_config`: attempts `364`, audit_blocked `183`, avg_gap `0.0354912725752985`

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
- decision_state: `issue`
- decision_reason: ``science_eval` is the top bounded seam and is not yet saturated by recent same-seam activity, so issue a fresh code-change brief.`
- target_file: `src/harness_lab/science_eval.py`
- target_functions: `should_run_full_audit, classify_smoke_block, classify_outcome`
- proposed_change: `Tighten or clarify smoke and audit classification so severe non-robustness fails earlier while borderline promising runs remain distinguishable.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `targeted_mutation`
- target_file: `src/harness_lab/science_eval.py`
- max_changed_files: `3`
- allowed_write_files: `src/harness_lab/science_eval.py, tests/test_science_smoke_gate.py, tests/test_science_eval.py`
- focused_tests: `tests/test_science_smoke_gate.py, tests/test_science_eval.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Allowed write scope is 3 files; autonomous mutation requires a target file plus adjacent tests only.`
- execution_mode: `candidate_workspace_only`
- auto_publish: `False`
- silent_rollback: `False`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
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
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
