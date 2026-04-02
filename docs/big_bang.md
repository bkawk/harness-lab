# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T12:28:46+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0381`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0381`
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
- active_candidate: `cand_0381`
- backend_status: `finished`
- backend_pid: `2369609`
- backend_started_at: `2026-04-02T12:18:43+00:00`
- backend_last_poll_at: `2026-04-02T12:28:46+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0381`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3167835652760768`
- `cand_0380`: outcome `keeper`; diagnosis `complete`; benchmark `0.3156770526144398`
- `cand_0379`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3569308938495921`
- `cand_0378`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3999281160334707`
- `cand_0377`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.326609357428949`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.343186, audit averaged 0.302977, and the mean transfer gap was 0.040209.`
- recent benchmark avg: `0.34318579704050567`
- recent audit avg: `0.3029768342115203`
- recent transfer gap avg: `0.04020896282898544`
- `cand_0381`: benchmark `0.3167835652760768`, audit `0.23925325578151743`, gap `0.07753030949455939`
- `cand_0380`: benchmark `0.3156770526144398`, audit `0.33047592762384076`, gap `-0.014798875009400969`
- `cand_0379`: benchmark `0.3569308938495921`, audit `0.3458892985814711`, gap `0.011041595268120985`
- `cand_0378`: benchmark `0.3999281160334707`, audit `0.2853396305872682`, gap `0.11458848544620254`
- `cand_0377`: benchmark `0.326609357428949`, audit `0.31392605848350374`, gap `0.012683298945445232`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 2 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `After 380 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (272 candidate(s), avg transfer gap 0.038955).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 765.8 MB on average, leaving most VRAM unused. 16 scored candidate(s) have landed since structural commit `4c8bac2`.`
- scored_candidates_since_change: `16`
- last_structural_commit: `4c8bac2`
### Chosen Lever Values
- source_candidate: `cand_0381`
- model: `global_dim=256, instance_dim=24`

### Effective Backend Settings
- source_candidate: `cand_0381`
- model: `hidden_dim=160, global_dim=256, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `272`, audit_blocked `157`, avg_gap `0.03895545379889462`
- loss: `science_loss` (targeted); attempts `257`, audit_blocked `143`, avg_gap `0.03897026236549341`
- eval: `science_eval` (available); attempts `264`, audit_blocked `149`, avg_gap `0.038842819740737174`
- config: `science_config` (available); attempts `257`, audit_blocked `143`, avg_gap `0.03897026236549341`
- train: `science_train` (available); attempts `250`, audit_blocked `136`, avg_gap `0.03892407158069004`

### Recent Module Evidence
- `science_backend`: attempts `272`, audit_blocked `157`, avg_gap `0.03895545379889462`
- `science_model`: attempts `272`, audit_blocked `157`, avg_gap `0.03895545379889462`
- `science_eval`: attempts `264`, audit_blocked `149`, avg_gap `0.038842819740737174`
- `science_config`: attempts `257`, audit_blocked `143`, avg_gap `0.03897026236549341`

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
- status: `reviewed`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 380 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
