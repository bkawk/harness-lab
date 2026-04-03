# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T11:32:52+00:00`
- cycles_completed: `82`
- genesis seed: `cand_0001`
- last candidate: `cand_0506`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `10`

## Latest Step
- candidate: `cand_0506`
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
- active_candidate: `cand_0506`
- backend_status: `finished`
- backend_pid: `2652114`
- backend_started_at: `2026-04-03T11:22:49+00:00`
- backend_last_poll_at: `2026-04-03T11:32:51+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0506`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4158922620068207`
- `cand_0505`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4179873445287302`
- `cand_0504`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3350810187507207`
- `cand_0503`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36042272557593874`
- `cand_0502`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34618271608005985`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.375113, audit averaged 0.325089, and the mean transfer gap was 0.050024.`
- recent benchmark avg: `0.37511321338845405`
- recent audit avg: `0.32508900668289314`
- recent transfer gap avg: `0.0500242067055609`
- `cand_0506`: benchmark `0.4158922620068207`, audit `0.31092843358861516`, gap `0.10496382841820556`
- `cand_0505`: benchmark `0.4179873445287302`, audit `0.3078415074109127`, gap `0.1101458371178175`
- `cand_0504`: benchmark `0.3350810187507207`, audit `0.3499892079638075`, gap `-0.014908189213086787`
- `cand_0503`: benchmark `0.36042272557593874`, audit `0.33125658905878186`, gap `0.029166136517156882`
- `cand_0502`: benchmark `0.34618271608005985`, audit `0.3254292953923485`, gap `0.020753420687711355`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 505 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (397 candidate(s), avg transfer gap 0.034868).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 858.1 MB on average, leaving most VRAM unused. 47 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `47`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0506`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0506`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `397`, audit_blocked `201`, avg_gap `0.03486812596948184`
- loss: `science_loss` (targeted); attempts `382`, audit_blocked `187`, avg_gap `0.034715153706904416`
- eval: `science_eval` (available); attempts `389`, audit_blocked `193`, avg_gap `0.03470316789058758`
- config: `science_config` (available); attempts `382`, audit_blocked `187`, avg_gap `0.034715153706904416`
- train: `science_train` (available); attempts `375`, audit_blocked `180`, avg_gap `0.03459922928936334`

### Recent Module Evidence
- `science_backend`: attempts `397`, audit_blocked `201`, avg_gap `0.03486812596948184`
- `science_model`: attempts `397`, audit_blocked `201`, avg_gap `0.03486812596948184`
- `science_eval`: attempts `389`, audit_blocked `193`, avg_gap `0.03470316789058758`
- `science_config`: attempts `382`, audit_blocked `187`, avg_gap `0.034715153706904416`

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
- status: `reviewed`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 505 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
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
- summary: `The lab has stayed on `science_train` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
