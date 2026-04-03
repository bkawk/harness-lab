# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T09:09:31+00:00`
- cycles_completed: `69`
- genesis seed: `cand_0001`
- last candidate: `cand_0493`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `7`

## Latest Step
- candidate: `cand_0493`
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
- active_candidate: `cand_0493`
- backend_status: `finished`
- backend_pid: `2641144`
- backend_started_at: `2026-04-03T08:59:28+00:00`
- backend_last_poll_at: `2026-04-03T09:09:30+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0493`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3299386730592102`
- `cand_0492`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4045840192762462`
- `cand_0491`: outcome `keeper`; diagnosis `complete`; benchmark `0.3632484978354048`
- `cand_0490`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32251320421996765`
- `cand_0489`: outcome `improved`; diagnosis `complete`; benchmark `0.27551286650964446`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.339159, audit averaged 0.326049, and the mean transfer gap was 0.013110.`
- recent benchmark avg: `0.3391594521800947`
- recent audit avg: `0.3260491527072618`
- recent transfer gap avg: `0.013110299472832876`
- `cand_0493`: benchmark `0.3299386730592102`, audit `0.2757866536978898`, gap `0.054152019361320414`
- `cand_0492`: benchmark `0.4045840192762462`, audit `0.3288937482652668`, gap `0.07569027101097942`
- `cand_0491`: benchmark `0.3632484978354048`, audit `0.3820240880032215`, gap `-0.018775590167816714`
- `cand_0490`: benchmark `0.32251320421996765`, audit `0.33445722097780617`, gap `-0.011944016757838516`
- `cand_0489`: benchmark `0.27551286650964446`, audit `0.3090840525921247`, gap `-0.03357118608248022`

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
- summary: `Mechanisms initial_harness, science_loss, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (384 candidate(s), avg transfer gap 0.035302).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 613.2 MB on average, leaving most VRAM unused. 34 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `34`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0493`
- loss: `instance_loss_weight=0.06, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0493`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `384`, audit_blocked `199`, avg_gap `0.03530208650853786`
- loss: `science_loss` (targeted); attempts `369`, audit_blocked `185`, avg_gap `0.035161169727179545`
- eval: `science_eval` (available); attempts `376`, audit_blocked `191`, avg_gap `0.03514097547105468`
- config: `science_config` (available); attempts `369`, audit_blocked `185`, avg_gap `0.035161169727179545`
- train: `science_train` (available); attempts `362`, audit_blocked `178`, avg_gap `0.03505011005275261`

### Recent Module Evidence
- `science_backend`: attempts `384`, audit_blocked `199`, avg_gap `0.03530208650853786`
- `science_model`: attempts `384`, audit_blocked `199`, avg_gap `0.03530208650853786`
- `science_eval`: attempts `376`, audit_blocked `191`, avg_gap `0.03514097547105468`
- `science_config`: attempts `369`, audit_blocked `185`, avg_gap `0.035161169727179545`

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
- decision_reason: ``science_loss` is already the active recent seam with outcomes ['keeper', 'dead_end', 'audit_blocked'], so keep iterating on that line rather than issuing a brand-new brief.`
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
- summary: `The lab has stayed on `science_loss` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
