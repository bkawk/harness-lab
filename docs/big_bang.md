# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T14:31:50+00:00`
- cycles_completed: `98`
- genesis seed: `cand_0001`
- last candidate: `cand_0522`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `14`

## Latest Step
- candidate: `cand_0522`
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
- active_candidate: `cand_0522`
- backend_status: `finished`
- backend_pid: `2656217`
- backend_started_at: `2026-04-03T14:21:47+00:00`
- backend_last_poll_at: `2026-04-03T14:31:49+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0522`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3642763347126906`
- `cand_0521`: outcome `improved`; diagnosis `complete`; benchmark `0.285442091126753`
- `cand_0520`: outcome `dead_end`; diagnosis `complete`; benchmark `0.31431643175552154`
- `cand_0519`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29726954227335733`
- `cand_0518`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34899316296241`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.322060, audit averaged 0.316957, and the mean transfer gap was 0.005103.`
- recent benchmark avg: `0.3220595125661465`
- recent audit avg: `0.3169568395541744`
- recent transfer gap avg: `0.005102673011972103`
- `cand_0522`: benchmark `0.3642763347126906`, audit `0.3310420666013949`, gap `0.033234268111295706`
- `cand_0521`: benchmark `0.285442091126753`, audit `0.29545013478787574`, gap `-0.010008043661122734`
- `cand_0520`: benchmark `0.31431643175552154`, audit `0.36295721559462535`, gap `-0.04864078383910381`
- `cand_0519`: benchmark `0.29726954227335733`, audit `0.29904967129187815`, gap `-0.0017801290185208152`
- `cand_0518`: benchmark `0.34899316296241`, audit `0.29628510949509784`, gap `0.052708053467312166`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_train, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (413 candidate(s), avg transfer gap 0.034411).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 808.9 MB on average, leaving most VRAM unused. 63 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `63`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0522`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0522`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `413`, audit_blocked `206`, avg_gap `0.03441130171046722`
- loss: `science_loss` (targeted); attempts `398`, audit_blocked `192`, avg_gap `0.034247601232061074`
- eval: `science_eval` (available); attempts `405`, audit_blocked `198`, avg_gap `0.03424362901978203`
- config: `science_config` (available); attempts `398`, audit_blocked `192`, avg_gap `0.034247601232061074`
- train: `science_train` (available); attempts `391`, audit_blocked `185`, avg_gap `0.03412774862437251`

### Recent Module Evidence
- `science_backend`: attempts `413`, audit_blocked `206`, avg_gap `0.03441130171046722`
- `science_model`: attempts `413`, audit_blocked `206`, avg_gap `0.03441130171046722`
- `science_eval`: attempts `405`, audit_blocked `198`, avg_gap `0.03424362901978203`
- `science_config`: attempts `398`, audit_blocked `192`, avg_gap `0.034247601232061074`

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
- decision_state: `issue`
- decision_reason: ``science_loss` is the top bounded seam and is not yet saturated by recent same-seam activity, so issue a fresh code-change brief.`
- target_file: `src/harness_lab/science_loss.py`
- target_functions: `compute_instance_loss, compute_loss`
- proposed_change: `Increase transfer-sensitive boundary or instance pressure modestly, for example by strengthening boundary_loss_weight or instance_margin, without changing eval thresholds.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `targeted_mutation`
- target_file: `src/harness_lab/science_loss.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_loss.py, tests/test_science_loss.py`
- focused_tests: `tests/test_science_loss.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation is eligible for this seam.`
- eligible: `True`
- state: `enabled`
- reason: `Autonomous code mutation is eligible: issue state, bounded scope, focused tests, and failure behavior are all in place.`
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
- summary: `The lab has stayed on `science_train` for 4 recent candidates; inject a novelty step.`
- current_mechanism_streak: `4`
- novelty_step_recommended: `True`
