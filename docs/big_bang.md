# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-08T22:56:18+00:00`
- cycles_completed: `790`
- genesis seed: `cand_0001`
- last candidate: `cand_1214`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `116`

## Latest Step
- candidate: `cand_1214`
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
- active_candidate: `cand_1214`
- backend_status: `finished`
- backend_pid: `2831306`
- backend_started_at: `2026-04-08T22:46:14+00:00`
- backend_last_poll_at: `2026-04-08T22:56:16+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1214`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28871395994566657`
- `cand_1213`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39002203554018566`
- `cand_1212`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3069835681011555`
- `cand_1211`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32964033383293934`
- `cand_1210`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3171569363923496`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.326503, audit averaged 0.299070, and the mean transfer gap was 0.027433.`
- recent benchmark avg: `0.32650336676245933`
- recent audit avg: `0.29907030240676236`
- recent transfer gap avg: `0.02743306435569696`
- `cand_1214`: benchmark `0.28871395994566657`, audit `0.23090934336878213`, gap `0.05780461657688443`
- `cand_1213`: benchmark `0.39002203554018566`, audit `0.32622676227320824`, gap `0.06379527326697743`
- `cand_1212`: benchmark `0.3069835681011555`, audit `0.3143389591757201`, gap `-0.007355391074564566`
- `cand_1211`: benchmark `0.32964033383293934`, audit `0.3430296178459068`, gap `-0.013389284012967462`
- `cand_1210`: benchmark `0.3171569363923496`, audit `0.2808468293701946`, gap `0.03631010702215498`

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
- summary: `Mechanisms science_loss, science_train, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (1105 candidate(s), avg transfer gap 0.033157).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 834.6 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1214`
- loss: `instance_loss_weight=0.06, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_1214`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1105`, audit_blocked `481`, avg_gap `0.033157172940071845`
- loss: `science_loss` (targeted); attempts `1090`, audit_blocked `467`, avg_gap `0.03308377711097846`
- eval: `science_eval` (available); attempts `1097`, audit_blocked `473`, avg_gap `0.03308893408783974`
- config: `science_config` (available); attempts `1090`, audit_blocked `467`, avg_gap `0.03308377711097846`
- train: `science_train` (available); attempts `1083`, audit_blocked `460`, avg_gap `0.03303495131779408`

### Recent Module Evidence
- `science_backend`: attempts `1105`, audit_blocked `481`, avg_gap `0.033157172940071845`
- `science_model`: attempts `1105`, audit_blocked `481`, avg_gap `0.033157172940071845`
- `science_eval`: attempts `1097`, audit_blocked `473`, avg_gap `0.03308893408783974`
- `science_config`: attempts `1090`, audit_blocked `467`, avg_gap `0.03308377711097846`

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
- reviewer: `heuristic`
- summary: `After 1212 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
