# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-15T06:46:05+00:00`
- cycles_completed: `1604`
- genesis seed: `cand_0001`
- last candidate: `cand_2028`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `260`

## Latest Step
- candidate: `cand_2028`
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
- active_candidate: `cand_2028`
- backend_status: `finished`
- backend_pid: `3005301`
- backend_started_at: `2026-04-15T06:36:00+00:00`
- backend_last_poll_at: `2026-04-15T06:46:02+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_2028`: outcome `improved`; diagnosis `complete`; benchmark `0.2823259273101711`
- `cand_2027`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32058466868709934`
- `cand_2026`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3209717509132899`
- `cand_2025`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36911529295703505`
- `cand_2024`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3853700805450903`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_1625` -> gap `-0.00015162972740001557`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.335674, audit averaged 0.315473, and the mean transfer gap was 0.020201.`
- recent benchmark avg: `0.33567354408253713`
- recent audit avg: `0.3154729169960354`
- recent transfer gap avg: `0.02020062708650173`
- `cand_2028`: benchmark `0.2823259273101711`, audit `0.2926302506640718`, gap `-0.01030432335390069`
- `cand_2027`: benchmark `0.32058466868709934`, audit `0.2919018126017163`, gap `0.028682856085383013`
- `cand_2026`: benchmark `0.3209717509132899`, audit `0.2868745369391258`, gap `0.0340972139741641`
- `cand_2025`: benchmark `0.36911529295703505`, audit `0.36818408515433265`, gap `0.000931207802702394`
- `cand_2024`: benchmark `0.3853700805450903`, audit `0.33777389962093046`, gap `0.04759618092415985`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 2 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (1919 candidate(s), avg transfer gap 0.032311).`
- recommended_action: `wait`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 608.6 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_2028`
- eval: `transfer_smoke_min_boundary_f1=0.14, transfer_smoke_min_score=0.23`

### Effective Backend Settings
- source_candidate: `cand_2028`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.23, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.14`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1919`, audit_blocked `806`, avg_gap `0.03231137617388945`
- loss: `science_loss` (available); attempts `1904`, audit_blocked `792`, avg_gap `0.032263542271239745`
- eval: `science_eval` (targeted); attempts `1911`, audit_blocked `798`, avg_gap `0.032269084157608124`
- config: `science_config` (available); attempts `1904`, audit_blocked `792`, avg_gap `0.032263542271239745`
- train: `science_train` (available); attempts `1897`, audit_blocked `785`, avg_gap `0.03223292887857701`

### Recent Module Evidence
- `science_backend`: attempts `1919`, audit_blocked `806`, avg_gap `0.03231137617388945`
- `science_model`: attempts `1919`, audit_blocked `806`, avg_gap `0.03231137617388945`
- `science_eval`: attempts `1911`, audit_blocked `798`, avg_gap `0.032269084157608124`
- `science_config`: attempts `1904`, audit_blocked `792`, avg_gap `0.032263542271239745`

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
- summary: `The lab has stayed on `science_eval` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
