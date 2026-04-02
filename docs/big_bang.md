# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-02T22:16:47+00:00`
- cycles_completed: `10`
- genesis seed: `cand_0001`
- last candidate: `cand_0434`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0434`
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
- active_candidate: `cand_0434`
- backend_status: `finished`
- backend_pid: `2388079`
- backend_started_at: `2026-04-02T22:06:45+00:00`
- backend_last_poll_at: `2026-04-02T22:16:47+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0434`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32024070356814005`
- `cand_0433`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2869017496564448`
- `cand_0432`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3074464428019116`
- `cand_0431`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3362243106985924`
- `cand_0430`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32523788222479433`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.315210, audit averaged 0.270259, and the mean transfer gap was 0.044952.`
- recent benchmark avg: `0.3152102177899766`
- recent audit avg: `0.2702587110671698`
- recent transfer gap avg: `0.04495150672280679`
- `cand_0434`: benchmark `0.32024070356814005`, audit `0.28153899633313884`, gap `0.038701707235001215`
- `cand_0433`: benchmark `0.2869017496564448`, audit `0.2220313856955909`, gap `0.06487036396085394`
- `cand_0432`: benchmark `0.3074464428019116`, audit `0.24722688946291943`, gap `0.06021955333899215`
- `cand_0431`: benchmark `0.3362243106985924`, audit `0.3291051030651251`, gap `0.007119207633467295`
- `cand_0430`: benchmark `0.32523788222479433`, audit `0.271391180779075`, gap `0.05384670144571935`

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
- summary: `Recent backend evolution is concentrated in science_backend (325 candidate(s), avg transfer gap 0.036712).`
- recommended_action: `targeted_mutation`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 819.9 MB on average, leaving most VRAM unused. 9 scored candidate(s) have landed since structural commit `7fea1af`.`
- scored_candidates_since_change: `9`
- last_structural_commit: `7fea1af`
### Chosen Lever Values
- source_candidate: `cand_0434`
- train: `batch_size=4, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0434`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=2, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `325`, audit_blocked `178`, avg_gap `0.0367120947542045`
- loss: `science_loss` (available); attempts `310`, audit_blocked `164`, avg_gap `0.03661198520620044`
- eval: `science_eval` (targeted); attempts `317`, audit_blocked `170`, avg_gap `0.03655718831376266`
- config: `science_config` (available); attempts `310`, audit_blocked `164`, avg_gap `0.03661198520620044`
- train: `science_train` (available); attempts `303`, audit_blocked `157`, avg_gap `0.03651412402101143`

### Recent Module Evidence
- `science_backend`: attempts `325`, audit_blocked `178`, avg_gap `0.0367120947542045`
- `science_model`: attempts `325`, audit_blocked `178`, avg_gap `0.0367120947542045`
- `science_eval`: attempts `317`, audit_blocked `170`, avg_gap `0.03655718831376266`
- `science_config`: attempts `310`, audit_blocked `164`, avg_gap `0.03661198520620044`

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
- trigger_reason: `repeated_audit_blocked`
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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
