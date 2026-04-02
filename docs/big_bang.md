# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T13:14:27+00:00`
- cycles_completed: `10`
- genesis seed: `cand_0001`
- last candidate: `cand_0385`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0385`
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
- active_candidate: `cand_0385`
- backend_status: `finished`
- backend_pid: `2370883`
- backend_started_at: `2026-04-02T13:04:24+00:00`
- backend_last_poll_at: `2026-04-02T13:14:27+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0385`: outcome `dead_end`; diagnosis `complete`; benchmark `0.312050059020566`
- `cand_0384`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3511298156258632`
- `cand_0383`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36144773206113506`
- `cand_0382`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3872610046089459`
- `cand_0381`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3167835652760768`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.345734, audit averaged 0.292205, and the mean transfer gap was 0.053530.`
- recent benchmark avg: `0.3457344353185174`
- recent audit avg: `0.2922047641030081`
- recent transfer gap avg: `0.053529671215509264`
- `cand_0385`: benchmark `0.312050059020566`, audit `0.2792825702129062`, gap `0.032767488807659784`
- `cand_0384`: benchmark `0.3511298156258632`, audit `0.3023741938585425`, gap `0.048755621767320734`
- `cand_0383`: benchmark `0.36144773206113506`, audit `0.32495448186650894`, gap `0.036493250194626126`
- `cand_0382`: benchmark `0.3872610046089459`, audit `0.3151593187955656`, gap `0.07210168581338033`
- `cand_0381`: benchmark `0.3167835652760768`, audit `0.23925325578151743`, gap `0.07753030949455939`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, science_model, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (276 candidate(s), avg transfer gap 0.039095).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 0 scored candidate(s) have landed since structural commit `4d32d84`.`
- secondary_context: `Recent real-backend runs are only using about 644.5 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `4d32d84`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `4d32d84`
### Chosen Lever Values
- source_candidate: `cand_0385`
- loss: `boundary_loss_weight=0.15, instance_loss_weight=0.05`

### Effective Backend Settings
- source_candidate: `cand_0385`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.05, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `276`, audit_blocked `158`, avg_gap `0.039094869373640186`
- loss: `science_loss` (targeted); attempts `261`, audit_blocked `144`, avg_gap `0.03911783562894606`
- eval: `science_eval` (available); attempts `268`, audit_blocked `150`, avg_gap `0.03898881456267011`
- config: `science_config` (available); attempts `261`, audit_blocked `144`, avg_gap `0.03911783562894606`
- train: `science_train` (available); attempts `254`, audit_blocked `137`, avg_gap `0.0390770571818466`

### Recent Module Evidence
- `science_backend`: attempts `276`, audit_blocked `158`, avg_gap `0.039094869373640186`
- `science_model`: attempts `276`, audit_blocked `158`, avg_gap `0.039094869373640186`
- `science_eval`: attempts `268`, audit_blocked `150`, avg_gap `0.03898881456267011`
- `science_config`: attempts `261`, audit_blocked `144`, avg_gap `0.03911783562894606`

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
- target_file: `src/harness_lab/science_loss.py`
- target_functions: `compute_instance_loss, compute_loss`
- proposed_change: `Increase transfer-sensitive boundary or instance pressure modestly, for example by strengthening boundary_loss_weight or instance_margin, without changing eval thresholds.`
- wait_option: `Only 0 scored candidate(s) have landed since the last structural change; wait on broad mutation until at least 3 post-change scored candidates exist, but conservative lever nudges are still allowed.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `wait`
- target_file: `src/harness_lab/science_loss.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_loss.py, tests/test_science_loss.py`
- focused_tests: `tests/test_science_loss.py`
- verification_status: `No verification run recorded yet.`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
