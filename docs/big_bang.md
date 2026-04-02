# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T11:43:09+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0377`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0377`
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
- active_candidate: `cand_0377`
- backend_status: `finished`
- backend_pid: `2368598`
- backend_started_at: `2026-04-02T11:33:07+00:00`
- backend_last_poll_at: `2026-04-02T11:43:09+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0377`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.326609357428949`
- `cand_0376`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4217569746031925`
- `cand_0375`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32024029786255914`
- `cand_0374`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0373`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2649241643960756`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.333383, audit averaged 0.275602, and the mean transfer gap was 0.057781.`
- recent benchmark avg: `0.33338269857269404`
- recent audit avg: `0.2756021122054262`
- recent transfer gap avg: `0.057780586367267864`
- `cand_0377`: benchmark `0.326609357428949`, audit `0.31392605848350374`, gap `0.012683298945445232`
- `cand_0376`: benchmark `0.4217569746031925`, audit `0.3168344490563814`, gap `0.10492252554681109`
- `cand_0375`: benchmark `0.32024029786255914`, audit `0.23736898486272834`, gap `0.0828713129998308`
- `cand_0373`: benchmark `0.2649241643960756`, audit `0.23427895641909124`, gap `0.030645207976984334`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (268 candidate(s), avg transfer gap 0.038819).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 725.8 MB on average, leaving most VRAM unused. 12 scored candidate(s) have landed since structural commit `4c8bac2`.`
- scored_candidates_since_change: `12`
- last_structural_commit: `4c8bac2`
### Chosen Lever Values
- source_candidate: `cand_0377`
- model: `hidden_dim=160, instance_modulation_scale=0.15`

### Effective Backend Settings
- source_candidate: `cand_0377`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `268`, audit_blocked `155`, avg_gap `0.038818732370306794`
- loss: `science_loss` (targeted); attempts `253`, audit_blocked `141`, avg_gap `0.03882526028630811`
- eval: `science_eval` (available); attempts `260`, audit_blocked `147`, avg_gap `0.03869938393101312`
- config: `science_config` (available); attempts `253`, audit_blocked `141`, avg_gap `0.03882526028630811`
- train: `science_train` (available); attempts `246`, audit_blocked `134`, avg_gap `0.038773540572041555`

### Recent Module Evidence
- `science_backend`: attempts `268`, audit_blocked `155`, avg_gap `0.038818732370306794`
- `science_model`: attempts `268`, audit_blocked `155`, avg_gap `0.038818732370306794`
- `science_eval`: attempts `260`, audit_blocked `147`, avg_gap `0.03869938393101312`
- `science_config`: attempts `253`, audit_blocked `141`, avg_gap `0.03882526028630811`

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
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `targeted_mutation`
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
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
