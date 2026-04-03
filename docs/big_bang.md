# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T19:21:50+00:00`
- cycles_completed: `124`
- genesis seed: `cand_0001`
- last candidate: `cand_0548`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `15`

## Latest Step
- candidate: `cand_0548`
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
- active_candidate: `cand_0548`
- backend_status: `finished`
- backend_pid: `2662184`
- backend_started_at: `2026-04-03T19:11:47+00:00`
- backend_last_poll_at: `2026-04-03T19:21:50+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0548`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3443248281949328`
- `cand_0547`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.299283287858241`
- `cand_0546`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2928022709881227`
- `cand_0545`: outcome `keeper`; diagnosis `complete`; benchmark `0.32218652033588974`
- `cand_0544`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4059290645352841`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.332905, audit averaged 0.298740, and the mean transfer gap was 0.034165.`
- recent benchmark avg: `0.33290519438249405`
- recent audit avg: `0.298740441189876`
- recent transfer gap avg: `0.03416475319261806`
- `cand_0548`: benchmark `0.3443248281949328`, audit `0.269164975902105`, gap `0.07515985229282784`
- `cand_0547`: benchmark `0.299283287858241`, audit `0.3043097373179068`, gap `-0.005026449459665794`
- `cand_0546`: benchmark `0.2928022709881227`, audit `0.2695143614176269`, gap `0.023287909570495813`
- `cand_0545`: benchmark `0.32218652033588974`, audit `0.3184508852868754`, gap `0.003735635049014363`
- `cand_0544`: benchmark `0.4059290645352841`, audit `0.33226224602486604`, gap `0.07366681851041806`

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
- summary: `Mechanisms initial_harness, science_train, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (439 candidate(s), avg transfer gap 0.034727).`
- recommended_action: `targeted_mutation`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 767.8 MB on average, leaving most VRAM unused. 89 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `89`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0548`
- eval: `transfer_smoke_max_gap=0.04, transfer_smoke_min_score=0.22`

### Effective Backend Settings
- source_candidate: `cand_0548`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.22, transfer_smoke_max_gap=0.04, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `439`, audit_blocked `219`, avg_gap `0.03472657491213007`
- loss: `science_loss` (available); attempts `424`, audit_blocked `205`, avg_gap `0.034584879604439255`
- eval: `science_eval` (targeted); attempts `431`, audit_blocked `211`, avg_gap `0.03457610641037267`
- config: `science_config` (available); attempts `424`, audit_blocked `205`, avg_gap `0.034584879604439255`
- train: `science_train` (available); attempts `417`, audit_blocked `198`, avg_gap `0.03447917975232317`

### Recent Module Evidence
- `science_backend`: attempts `439`, audit_blocked `219`, avg_gap `0.03472657491213007`
- `science_model`: attempts `439`, audit_blocked `219`, avg_gap `0.03472657491213007`
- `science_eval`: attempts `431`, audit_blocked `211`, avg_gap `0.03457610641037267`
- `science_config`: attempts `424`, audit_blocked `205`, avg_gap `0.034584879604439255`

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
- summary: `Recent branching still has room, but `science_eval` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
