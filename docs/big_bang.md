# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-09T23:46:51+00:00`
- cycles_completed: `923`
- genesis seed: `cand_0001`
- last candidate: `cand_1347`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `142`

## Latest Step
- candidate: `cand_1347`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `novelty_cycle`

## Active Backend
- active_candidate: `cand_1347`
- backend_status: `finished`
- backend_pid: `2858128`
- backend_started_at: `2026-04-09T23:36:48+00:00`
- backend_last_poll_at: `2026-04-09T23:46:49+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1347`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3441675394015741`
- `cand_1346`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32445176247506435`
- `cand_1345`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3712851837186957`
- `cand_1344`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36324099677994315`
- `cand_1343`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30967211987041937`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.342564, audit averaged 0.299971, and the mean transfer gap was 0.042592.`
- recent benchmark avg: `0.34256352044913935`
- recent audit avg: `0.2999714474895842`
- recent transfer gap avg: `0.042592072959555125`
- `cand_1347`: benchmark `0.3441675394015741`, audit `0.3070878946972718`, gap `0.03707964470430225`
- `cand_1346`: benchmark `0.32445176247506435`, audit `0.32701910616072216`, gap `-0.002567343685657808`
- `cand_1345`: benchmark `0.3712851837186957`, audit `0.31807529043363814`, gap `0.05320989328505754`
- `cand_1344`: benchmark `0.36324099677994315`, audit `0.3000342044117318`, gap `0.06320679236821136`
- `cand_1343`: benchmark `0.30967211987041937`, audit `0.2476407417445571`, gap `0.06203137812586226`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (1238 candidate(s), avg transfer gap 0.032716).`
- recommended_action: `wait`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 599.1 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1347`
- eval: `transfer_smoke_min_boundary_f1=0.1, transfer_smoke_min_score=0.26`

### Effective Backend Settings
- source_candidate: `cand_1347`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.26, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.1`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1238`, audit_blocked `535`, avg_gap `0.032716255154501675`
- loss: `science_loss` (available); attempts `1223`, audit_blocked `521`, avg_gap `0.032645867536867997`
- eval: `science_eval` (targeted); attempts `1230`, audit_blocked `527`, avg_gap `0.03265264384610802`
- config: `science_config` (available); attempts `1223`, audit_blocked `521`, avg_gap `0.032645867536867997`
- train: `science_train` (available); attempts `1216`, audit_blocked `514`, avg_gap `0.032599932522330115`

### Recent Module Evidence
- `science_backend`: attempts `1238`, audit_blocked `535`, avg_gap `0.032716255154501675`
- `science_model`: attempts `1238`, audit_blocked `535`, avg_gap `0.032716255154501675`
- `science_eval`: attempts `1230`, audit_blocked `527`, avg_gap `0.03265264384610802`
- `science_config`: attempts `1223`, audit_blocked `521`, avg_gap `0.032645867536867997`

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
- summary: `The lab has stayed on `science_eval` for 4 recent candidates; inject a novelty step.`
- current_mechanism_streak: `4`
- novelty_step_recommended: `True`
