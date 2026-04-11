# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-11T01:05:01+00:00`
- cycles_completed: `1059`
- genesis seed: `cand_0001`
- last candidate: `cand_1483`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `167`

## Latest Step
- candidate: `cand_1483`
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
- active_candidate: `cand_1483`
- backend_status: `finished`
- backend_pid: `2887175`
- backend_started_at: `2026-04-11T00:54:57+00:00`
- backend_last_poll_at: `2026-04-11T01:05:00+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1483`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2759748250949264`
- `cand_1482`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3917486956950484`
- `cand_1481`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4057469935161808`
- `cand_1480`: outcome `keeper`; diagnosis `complete`; benchmark `0.30477885732373966`
- `cand_1479`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32104954373776823`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.339860, audit averaged 0.301391, and the mean transfer gap was 0.038469.`
- recent benchmark avg: `0.3398597830735327`
- recent audit avg: `0.3013912421622873`
- recent transfer gap avg: `0.038468540911245394`
- `cand_1483`: benchmark `0.2759748250949264`, audit `0.28572930847370803`, gap `-0.009754483378781653`
- `cand_1482`: benchmark `0.3917486956950484`, audit `0.3291252694051878`, gap `0.06262342628986056`
- `cand_1481`: benchmark `0.4057469935161808`, audit `0.3029400323186173`, gap `0.1028069611975635`
- `cand_1480`: benchmark `0.30477885732373966`, audit `0.3100205466201838`, gap `-0.005241689296444141`
- `cand_1479`: benchmark `0.32104954373776823`, audit `0.2791410539937395`, gap `0.04190848974402872`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 1482 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (1374 candidate(s), avg transfer gap 0.032390).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 771.5 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1483`
- eval: `transfer_smoke_max_gap=0.04, transfer_smoke_min_boundary_f1=0.15`

### Effective Backend Settings
- source_candidate: `cand_1483`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.04, transfer_smoke_min_boundary_f1=0.15`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1374`, audit_blocked `584`, avg_gap `0.03238997380946173`
- loss: `science_loss` (targeted); attempts `1359`, audit_blocked `570`, avg_gap `0.03232335201362461`
- eval: `science_eval` (available); attempts `1366`, audit_blocked `576`, avg_gap `0.032330887510192585`
- config: `science_config` (available); attempts `1359`, audit_blocked `570`, avg_gap `0.03232335201362461`
- train: `science_train` (available); attempts `1352`, audit_blocked `563`, avg_gap `0.03228043481551218`

### Recent Module Evidence
- `science_backend`: attempts `1374`, audit_blocked `584`, avg_gap `0.03238997380946173`
- `science_model`: attempts `1374`, audit_blocked `584`, avg_gap `0.03238997380946173`
- `science_eval`: attempts `1366`, audit_blocked `576`, avg_gap `0.032330887510192585`
- `science_config`: attempts `1359`, audit_blocked `570`, avg_gap `0.03232335201362461`

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
- status: `reviewed`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 1482 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `transfer_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `transfer_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `science_eval` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
