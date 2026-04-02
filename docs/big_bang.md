# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T08:12:47+00:00`
- last_heartbeat: `2026-04-02T08:23:36+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0357`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0357`
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
- active_candidate: `cand_0357`
- backend_status: `finished`
- backend_pid: `2362426`
- backend_started_at: `2026-04-02T08:13:33+00:00`
- backend_last_poll_at: `2026-04-02T08:23:36+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0357`: outcome `dead_end`; diagnosis `complete`; benchmark `0.43267521948314225`
- `cand_0356`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0355`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3739433674508438`
- `cand_0354`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31534977637624456`
- `cand_0353`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.373989, audit averaged 0.275329, and the mean transfer gap was 0.098661.`
- recent benchmark avg: `0.37398945443674353`
- recent audit avg: `0.27532859503055696`
- recent transfer gap avg: `0.09866085940618656`
- `cand_0357`: benchmark `0.43267521948314225`, audit `0.2748558974743814`, gap `0.15781932200876087`
- `cand_0355`: benchmark `0.3739433674508438`, audit `0.31264258790788735`, gap `0.06130077954295643`
- `cand_0354`: benchmark `0.31534977637624456`, audit `0.23848729970940216`, gap `0.0768624766668424`

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
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (249 candidate(s), avg transfer gap 0.038754).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 0 scored candidate(s) have landed since structural commit `8eb05e7`.`
- secondary_context: `Recent real-backend runs are only using about 603.1 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `8eb05e7`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `8eb05e7`
### Chosen Lever Values
- source_candidate: `cand_0357`
- loss: `boundary_loss_weight=0.1, instance_loss_weight=0.08`

### Effective Backend Settings
- source_candidate: `cand_0357`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `249`, audit_blocked `149`, avg_gap `0.03875437445553408`
- loss: `science_loss` (targeted); attempts `234`, audit_blocked `135`, avg_gap `0.0387570857713673`
- eval: `science_eval` (available); attempts `241`, audit_blocked `141`, avg_gap `0.03862308335527244`
- config: `science_config` (available); attempts `234`, audit_blocked `135`, avg_gap `0.0387570857713673`
- train: `science_train` (available); attempts `227`, audit_blocked `128`, avg_gap `0.03869858377336515`

### Recent Module Evidence
- `science_backend`: attempts `249`, audit_blocked `149`, avg_gap `0.03875437445553408`
- `science_model`: attempts `249`, audit_blocked `149`, avg_gap `0.03875437445553408`
- `science_eval`: attempts `241`, audit_blocked `141`, avg_gap `0.03862308335527244`
- `science_config`: attempts `234`, audit_blocked `135`, avg_gap `0.0387570857713673`

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
- proposed_change: `Adjust transfer-sensitive loss pressure in a bounded way so boundary and instance structure hold up better on transfer slices.`
- wait_option: `Only 0 scored candidate(s) have landed since the last structural change; wait on broad mutation until at least 3 post-change scored candidates exist, but conservative lever nudges are still allowed.`

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
- summary: `The lab has stayed on `science_loss` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
