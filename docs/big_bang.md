# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-02T23:46:16+00:00`
- cycles_completed: `18`
- genesis seed: `cand_0001`
- last candidate: `cand_0442`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0442`
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
- active_candidate: `cand_0442`
- backend_status: `finished`
- backend_pid: `2389770`
- backend_started_at: `2026-04-02T23:36:13+00:00`
- backend_last_poll_at: `2026-04-02T23:46:15+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0442`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3193791598329632`
- `cand_0441`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3623301971291769`
- `cand_0440`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37598419646345344`
- `cand_0439`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3035209864968145`
- `cand_0438`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33093710151806555`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.338430, audit averaged 0.304146, and the mean transfer gap was 0.034284.`
- recent benchmark avg: `0.3384303282880947`
- recent audit avg: `0.3041463316525541`
- recent transfer gap avg: `0.0342839966355406`
- `cand_0442`: benchmark `0.3193791598329632`, audit `0.31680168757115734`, gap `0.00257747226180588`
- `cand_0441`: benchmark `0.3623301971291769`, audit `0.3354737366344834`, gap `0.026856460494693535`
- `cand_0440`: benchmark `0.37598419646345344`, audit `0.3324703881918281`, gap `0.04351380827162532`
- `cand_0439`: benchmark `0.3035209864968145`, audit `0.26445348385634193`, gap `0.039067502640472596`
- `cand_0438`: benchmark `0.33093710151806555`, audit `0.27153236200895986`, gap `0.059404739509105686`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (333 candidate(s), avg transfer gap 0.036805).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 742.5 MB on average, leaving most VRAM unused. 17 scored candidate(s) have landed since structural commit `7fea1af`.`
- scored_candidates_since_change: `17`
- last_structural_commit: `7fea1af`
### Chosen Lever Values
- source_candidate: `cand_0442`
- loss: `instance_loss_weight=0.06, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0442`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `333`, audit_blocked `181`, avg_gap `0.03680465918585511`
- loss: `science_loss` (targeted); attempts `318`, audit_blocked `167`, avg_gap `0.03671183011850085`
- eval: `science_eval` (available); attempts `325`, audit_blocked `173`, avg_gap `0.0366564866466947`
- config: `science_config` (available); attempts `318`, audit_blocked `167`, avg_gap `0.03671183011850085`
- train: `science_train` (available); attempts `311`, audit_blocked `160`, avg_gap `0.03661924225668414`

### Recent Module Evidence
- `science_backend`: attempts `333`, audit_blocked `181`, avg_gap `0.03680465918585511`
- `science_model`: attempts `333`, audit_blocked `181`, avg_gap `0.03680465918585511`
- `science_eval`: attempts `325`, audit_blocked `173`, avg_gap `0.0366564866466947`
- `science_config`: attempts `318`, audit_blocked `167`, avg_gap `0.03671183011850085`

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
- status: `cooldown`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 440 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_eval` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_eval` as a more explicit evolvable backend module if it keeps dominating search.`
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
