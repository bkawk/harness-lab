# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-10T15:36:22+00:00`
- cycles_completed: `1008`
- genesis seed: `cand_0001`
- last candidate: `cand_1432`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `161`

## Latest Step
- candidate: `cand_1432`
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
- active_candidate: `cand_1432`
- backend_status: `finished`
- backend_pid: `2876949`
- backend_started_at: `2026-04-10T15:26:17+00:00`
- backend_last_poll_at: `2026-04-10T15:36:20+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1432`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3609794265967499`
- `cand_1431`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39360385900657036`
- `cand_1430`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33631980006225626`
- `cand_1429`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3089240592559942`
- `cand_1428`: outcome `dead_end`; diagnosis `complete`; benchmark `0.30659778956110106`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.341285, audit averaged 0.313322, and the mean transfer gap was 0.027963.`
- recent benchmark avg: `0.34128498689653436`
- recent audit avg: `0.31332211302986956`
- recent transfer gap avg: `0.027962873866664795`
- `cand_1432`: benchmark `0.3609794265967499`, audit `0.32778952845378173`, gap `0.03318989814296819`
- `cand_1431`: benchmark `0.39360385900657036`, audit `0.3091905179393965`, gap `0.08441334106717385`
- `cand_1430`: benchmark `0.33631980006225626`, audit `0.2946770424960644`, gap `0.041642757566191846`
- `cand_1429`: benchmark `0.3089240592559942`, audit `0.29962123115767514`, gap `0.00930282809831906`
- `cand_1428`: benchmark `0.30659778956110106`, audit `0.33533224510243004`, gap `-0.028734455541328974`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (1323 candidate(s), avg transfer gap 0.032216).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 908.0 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1432`
- loss: `instance_loss_weight=0.06, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_1432`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1323`, audit_blocked `566`, avg_gap `0.03221590712755908`
- loss: `science_loss` (targeted); attempts `1308`, audit_blocked `552`, avg_gap `0.0321447198816951`
- eval: `science_eval` (available); attempts `1315`, audit_blocked `558`, avg_gap `0.032153389414958204`
- config: `science_config` (available); attempts `1308`, audit_blocked `552`, avg_gap `0.0321447198816951`
- train: `science_train` (available); attempts `1301`, audit_blocked `545`, avg_gap `0.032099096781122216`

### Recent Module Evidence
- `science_backend`: attempts `1323`, audit_blocked `566`, avg_gap `0.03221590712755908`
- `science_model`: attempts `1323`, audit_blocked `566`, avg_gap `0.03221590712755908`
- `science_eval`: attempts `1315`, audit_blocked `558`, avg_gap `0.032153389414958204`
- `science_config`: attempts `1308`, audit_blocked `552`, avg_gap `0.0321447198816951`

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
- status: `cooldown`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 1430 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
