# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T08:36:40+00:00`
- cycles_completed: `66`
- genesis seed: `cand_0001`
- last candidate: `cand_0490`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `7`

## Latest Step
- candidate: `cand_0490`
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
- active_candidate: `cand_0490`
- backend_status: `finished`
- backend_pid: `2599900`
- backend_started_at: `2026-04-03T08:26:37+00:00`
- backend_last_poll_at: `2026-04-03T08:36:39+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0490`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32251320421996765`
- `cand_0489`: outcome `improved`; diagnosis `complete`; benchmark `0.27551286650964446`
- `cand_0488`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2945081219577682`
- `cand_0487`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33176724944463015`
- `cand_0486`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3962179916217762`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0482` -> audit `0.3819516821922625`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.324104, audit averaged 0.295021, and the mean transfer gap was 0.029083.`
- recent benchmark avg: `0.32410388675075735`
- recent audit avg: `0.2950210119109411`
- recent transfer gap avg: `0.029082874839816225`
- `cand_0490`: benchmark `0.32251320421996765`, audit `0.33445722097780617`, gap `-0.011944016757838516`
- `cand_0489`: benchmark `0.27551286650964446`, audit `0.3090840525921247`, gap `-0.03357118608248022`
- `cand_0488`: benchmark `0.2945081219577682`, audit `0.22013978859963576`, gap `0.07436833335813245`
- `cand_0487`: benchmark `0.33176724944463015`, audit `0.29509117653573996`, gap `0.03667607290889019`
- `cand_0486`: benchmark `0.3962179916217762`, audit `0.31633282084939895`, gap `0.07988517077237722`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 2 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_loss, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (381 candidate(s), avg transfer gap 0.035287).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 652.1 MB on average, leaving most VRAM unused. 31 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `31`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0490`
- eval: `transfer_smoke_max_gap=0.035, transfer_smoke_min_score=0.22`

### Effective Backend Settings
- source_candidate: `cand_0490`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.22, transfer_smoke_max_gap=0.035, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `381`, audit_blocked `198`, avg_gap `0.035287342392312515`
- loss: `science_loss` (targeted); attempts `366`, audit_blocked `184`, avg_gap `0.0351445530872303`
- eval: `science_eval` (available); attempts `373`, audit_blocked `190`, avg_gap `0.035124473208506965`
- config: `science_config` (available); attempts `366`, audit_blocked `184`, avg_gap `0.0351445530872303`
- train: `science_train` (available); attempts `359`, audit_blocked `177`, avg_gap `0.03503212716507411`

### Recent Module Evidence
- `science_backend`: attempts `381`, audit_blocked `198`, avg_gap `0.035287342392312515`
- `science_model`: attempts `381`, audit_blocked `198`, avg_gap `0.035287342392312515`
- `science_eval`: attempts `373`, audit_blocked `190`, avg_gap `0.035124473208506965`
- `science_config`: attempts `366`, audit_blocked `184`, avg_gap `0.0351445530872303`

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
- decision_state: `iterate`
- decision_reason: ``science_loss` is already the active recent seam with outcomes ['dead_end', 'dead_end'], so keep iterating on that line rather than issuing a brand-new brief.`
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
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `iterate`, so autonomous code mutation stays blocked.`
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
