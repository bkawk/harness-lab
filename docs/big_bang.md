# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-19T04:21:24+00:00`
- cycles_completed: `2104`
- genesis seed: `cand_0001`
- last candidate: `cand_2528`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `348`

## Latest Step
- candidate: `cand_2528`
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
- active_candidate: `cand_2528`
- backend_status: `finished`
- backend_pid: `3131354`
- backend_started_at: `2026-04-19T04:11:19+00:00`
- backend_last_poll_at: `2026-04-19T04:21:21+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_2528`: outcome `keeper`; diagnosis `complete`; benchmark `0.3190770051961683`
- `cand_2527`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3040392002048378`
- `cand_2526`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3991682001722413`
- `cand_2525`: outcome `dead_end`; diagnosis `complete`; benchmark `0.35793844867371316`
- `cand_2524`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3623200355769014`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_2357` -> gap `-0.00011202849963909411`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.348509, audit averaged 0.307597, and the mean transfer gap was 0.040912.`
- recent benchmark avg: `0.3485085779647724`
- recent audit avg: `0.3075970709812109`
- recent transfer gap avg: `0.04091150698356143`
- `cand_2528`: benchmark `0.3190770051961683`, audit `0.3280771846441545`, gap `-0.0090001794479862`
- `cand_2527`: benchmark `0.3040392002048378`, audit `0.310891921939904`, gap `-0.006852721735066181`
- `cand_2526`: benchmark `0.3991682001722413`, audit `0.291969100751007`, gap `0.10719909942123429`
- `cand_2525`: benchmark `0.35793844867371316`, audit `0.31669983405800783`, gap `0.04123861461570533`
- `cand_2524`: benchmark `0.3623200355769014`, audit `0.2903473135129815`, gap `0.07197272206391991`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (2419 candidate(s), avg transfer gap 0.031931).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 609.2 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_2528`
- loss: `instance_margin=0.38, param_loss_weight=0.25`

### Effective Backend Settings
- source_candidate: `cand_2528`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.25, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `2419`, audit_blocked `1027`, avg_gap `0.03193099494769028`
- loss: `science_loss` (targeted); attempts `2404`, audit_blocked `1013`, avg_gap `0.03189099239051575`
- eval: `science_eval` (available); attempts `2411`, audit_blocked `1019`, avg_gap `0.03189630921642201`
- config: `science_config` (available); attempts `2404`, audit_blocked `1013`, avg_gap `0.03189099239051575`
- train: `science_train` (available); attempts `2397`, audit_blocked `1006`, avg_gap `0.0318657439522959`

### Recent Module Evidence
- `science_backend`: attempts `2419`, audit_blocked `1027`, avg_gap `0.03193099494769028`
- `science_model`: attempts `2419`, audit_blocked `1027`, avg_gap `0.03193099494769028`
- `science_eval`: attempts `2411`, audit_blocked `1019`, avg_gap `0.03189630921642201`
- `science_config`: attempts `2404`, audit_blocked `1013`, avg_gap `0.03189099239051575`

### Code Context
- summary: `Backend code context maps the five modular science seams to their key functions, bounded lever surfaces, fixed implementation surfaces, and likely failure-mode touchpoints.`
- target_file: `src/harness_lab/science_loss.py`
- target_purpose: `Combines classification, parameter, boundary, and instance-separation losses into the training objective.`
- key_functions: `compute_instance_loss, compute_loss`
- levered_surfaces: `param_loss_weight, boundary_loss_weight, instance_loss_weight, instance_margin`
- fixed_surfaces: `Cross-entropy plus smooth-L1 plus BCE loss recipe; Instance similarity and same-class negative construction; Loss-term composition order`

### Failure-To-Code Hints
- `boundary_smoke:gap_too_wide` -> `science_eval, science_loss, science_model`: `Boundary smoke regressions often reflect a mix of strict smoke-gap thresholds, weak boundary pressure in the loss, or insufficient boundary-sensitive representation capacity.`
- `hard_transfer_regression` -> `science_loss, science_model, science_config`: `Hard-transfer failures usually point to brittle transfer-sensitive structure, insufficient representation robustness, or seed defaults that underweight difficult cases.`
- `transfer_smoke:gap_too_wide` -> `science_eval, science_model`: `A wide benchmark-to-smoke gap is often governed by smoke gate strictness and by whether the model capacity generalizes beyond the local benchmark slice.`

### Code Change Brief
- decision_state: `wait`
- decision_reason: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`
- target_file: `src/harness_lab/science_loss.py`
- target_functions: `compute_instance_loss, compute_loss`
- proposed_change: `Increase transfer-sensitive boundary or instance pressure modestly, for example by strengthening boundary_loss_weight or instance_margin, without changing eval thresholds.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `wait`
- target_file: `src/harness_lab/science_loss.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_loss.py, tests/test_science_loss.py`
- focused_tests: `tests/test_science_loss.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `wait`, so autonomous code mutation stays blocked. Recommended action is `wait`, not `targeted_mutation`.`
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
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
