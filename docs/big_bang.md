# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T09:43:01+00:00`
- cycles_completed: `72`
- genesis seed: `cand_0001`
- last candidate: `cand_0496`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `8`

## Latest Step
- candidate: `cand_0496`
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
- active_candidate: `cand_0496`
- backend_status: `finished`
- backend_pid: `2649564`
- backend_started_at: `2026-04-03T09:32:58+00:00`
- backend_last_poll_at: `2026-04-03T09:43:00+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0496`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3714239440254619`
- `cand_0495`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37458841823997546`
- `cand_0494`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3239300296990433`
- `cand_0493`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3299386730592102`
- `cand_0492`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4045840192762462`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.360893, audit averaged 0.313126, and the mean transfer gap was 0.047767.`
- recent benchmark avg: `0.3608930168599874`
- recent audit avg: `0.3131261393544908`
- recent transfer gap avg: `0.04776687750549661`
- `cand_0496`: benchmark `0.3714239440254619`, audit `0.31152099424044616`, gap `0.05990294978501576`
- `cand_0495`: benchmark `0.37458841823997546`, audit `0.3412452020178973`, gap `0.03334321622207814`
- `cand_0494`: benchmark `0.3239300296990433`, audit `0.30818409855095397`, gap `0.01574593114808931`
- `cand_0493`: benchmark `0.3299386730592102`, audit `0.2757866536978898`, gap `0.054152019361320414`
- `cand_0492`: benchmark `0.4045840192762462`, audit `0.3288937482652668`, gap `0.07569027101097942`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 495 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, science_loss, science_train exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (387 candidate(s), avg transfer gap 0.035311).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 707.0 MB on average, leaving most VRAM unused. 37 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `37`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0496`
- train: `batch_size=4, eval_batch_size=4`

### Effective Backend Settings
- source_candidate: `cand_0496`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=4, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `387`, audit_blocked `199`, avg_gap `0.03531075459176699`
- loss: `science_loss` (targeted); attempts `372`, audit_blocked `185`, avg_gap `0.03517142875634224`
- eval: `science_eval` (available); attempts `379`, audit_blocked `191`, avg_gap `0.035151231708819106`
- config: `science_config` (available); attempts `372`, audit_blocked `185`, avg_gap `0.03517142875634224`
- train: `science_train` (available); attempts `365`, audit_blocked `178`, avg_gap `0.03506157801393746`

### Recent Module Evidence
- `science_backend`: attempts `387`, audit_blocked `199`, avg_gap `0.03531075459176699`
- `science_model`: attempts `387`, audit_blocked `199`, avg_gap `0.03531075459176699`
- `science_eval`: attempts `379`, audit_blocked `191`, avg_gap `0.035151231708819106`
- `science_config`: attempts `372`, audit_blocked `185`, avg_gap `0.03517142875634224`

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
- status: `reviewed`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 495 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
