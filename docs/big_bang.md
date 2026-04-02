# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-02T23:01:28+00:00`
- cycles_completed: `14`
- genesis seed: `cand_0001`
- last candidate: `cand_0438`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0438`
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
- active_candidate: `cand_0438`
- backend_status: `finished`
- backend_pid: `2388887`
- backend_started_at: `2026-04-02T22:51:26+00:00`
- backend_last_poll_at: `2026-04-02T23:01:28+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0438`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33093710151806555`
- `cand_0437`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3379068128942522`
- `cand_0436`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34030803153874006`
- `cand_0435`: outcome `dead_end`; diagnosis `complete`; benchmark `0.35698016528984455`
- `cand_0434`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32024070356814005`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.337275, audit averaged 0.287607, and the mean transfer gap was 0.049668.`
- recent benchmark avg: `0.33727456296180847`
- recent audit avg: `0.28760702697010343`
- recent transfer gap avg: `0.04966753599170506`
- `cand_0438`: benchmark `0.33093710151806555`, audit `0.27153236200895986`, gap `0.059404739509105686`
- `cand_0437`: benchmark `0.3379068128942522`, audit `0.2874684931898782`, gap `0.05043831970437396`
- `cand_0436`: benchmark `0.34030803153874006`, audit `0.29734581983144237`, gap `0.04296221170729769`
- `cand_0435`: benchmark `0.35698016528984455`, audit `0.3001494634870978`, gap `0.05683070180274674`
- `cand_0434`: benchmark `0.32024070356814005`, audit `0.28153899633313884`, gap `0.038701707235001215`

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
- summary: `Mechanisms initial_harness, science_model, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (329 candidate(s), avg transfer gap 0.036923).`
- recommended_action: `targeted_mutation`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 782.9 MB on average, leaving most VRAM unused. 13 scored candidate(s) have landed since structural commit `7fea1af`.`
- scored_candidates_since_change: `13`
- last_structural_commit: `7fea1af`
### Chosen Lever Values
- source_candidate: `cand_0438`
- eval: `transfer_smoke_min_boundary_f1=0.14, transfer_smoke_min_score=0.26`

### Effective Backend Settings
- source_candidate: `cand_0438`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.26, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.14`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `329`, audit_blocked `180`, avg_gap `0.03692279137738136`
- loss: `science_loss` (available); attempts `314`, audit_blocked `166`, avg_gap `0.03683447827626636`
- eval: `science_eval` (targeted); attempts `321`, audit_blocked `172`, avg_gap `0.03677583389813671`
- config: `science_config` (available); attempts `314`, audit_blocked `166`, avg_gap `0.03683447827626636`
- train: `science_train` (available); attempts `307`, audit_blocked `159`, avg_gap `0.03674365281754385`

### Recent Module Evidence
- `science_backend`: attempts `329`, audit_blocked `180`, avg_gap `0.03692279137738136`
- `science_model`: attempts `329`, audit_blocked `180`, avg_gap `0.03692279137738136`
- `science_eval`: attempts `321`, audit_blocked `172`, avg_gap `0.03677583389813671`
- `science_config`: attempts `314`, audit_blocked `166`, avg_gap `0.03683447827626636`

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
- decision_state: `switch`
- decision_reason: ``science_eval` is already active in the recent scored window but is repeating dead-end outcomes without a keeper signal, so switch seams instead of issuing another brief here.`
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
- reason: `Decision state is `switch`, so autonomous code mutation stays blocked. Allowed write scope is 3 files; autonomous mutation requires a target file plus adjacent tests only.`
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
- summary: `Recent branching still has room, but `science_eval` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
