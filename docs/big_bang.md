# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-20T03:06:10+00:00`
- cycles_completed: `2226`
- genesis seed: `cand_0001`
- last candidate: `cand_2650`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `370`

## Latest Step
- candidate: `cand_2650`
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
- active_candidate: `cand_2650`
- backend_status: `finished`
- backend_pid: `3155251`
- backend_started_at: `2026-04-20T02:56:06+00:00`
- backend_last_poll_at: `2026-04-20T03:06:07+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_2650`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3624953330936685`
- `cand_2649`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28386888359888646`
- `cand_2648`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32473516095854893`
- `cand_2647`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3692976597947535`
- `cand_2646`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3990786759391976`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_2357` -> gap `-0.00011202849963909411`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.347895, audit averaged 0.296087, and the mean transfer gap was 0.051808.`
- recent benchmark avg: `0.347895142677011`
- recent audit avg: `0.2960871411097461`
- recent transfer gap avg: `0.05180800156726488`
- `cand_2650`: benchmark `0.3624953330936685`, audit `0.3180364083724194`, gap `0.04445892472124907`
- `cand_2649`: benchmark `0.28386888359888646`, audit `0.29064207033135425`, gap `-0.006773186732467795`
- `cand_2648`: benchmark `0.32473516095854893`, audit `0.2884431605781348`, gap `0.036292000380414136`
- `cand_2647`: benchmark `0.3692976597947535`, audit `0.27096509894802007`, gap `0.09833256084673342`
- `cand_2646`: benchmark `0.3990786759391976`, audit `0.312348967318802`, gap `0.08672970862039558`

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
- summary: `Recent backend evolution is concentrated in science_backend (2541 candidate(s), avg transfer gap 0.031695).`
- recommended_action: `wait`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 725.2 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_2650`
- eval: `transfer_smoke_max_gap=0.035, transfer_smoke_min_boundary_f1=0.1`

### Effective Backend Settings
- source_candidate: `cand_2650`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.035, transfer_smoke_min_boundary_f1=0.1`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `2541`, audit_blocked `1083`, avg_gap `0.03169459511172492`
- loss: `science_loss` (available); attempts `2526`, audit_blocked `1069`, avg_gap `0.03165522184712722`
- eval: `science_eval` (targeted); attempts `2533`, audit_blocked `1075`, avg_gap `0.03166084481631876`
- config: `science_config` (available); attempts `2526`, audit_blocked `1069`, avg_gap `0.03165522184712722`
- train: `science_train` (available); attempts `2519`, audit_blocked `1062`, avg_gap `0.031630547902944776`

### Recent Module Evidence
- `science_backend`: attempts `2541`, audit_blocked `1083`, avg_gap `0.03169459511172492`
- `science_model`: attempts `2541`, audit_blocked `1083`, avg_gap `0.03169459511172492`
- `science_eval`: attempts `2533`, audit_blocked `1075`, avg_gap `0.03166084481631876`
- `science_config`: attempts `2526`, audit_blocked `1069`, avg_gap `0.03165522184712722`

### Code Context
- summary: `Backend code context maps the five modular science seams to their key functions, bounded lever surfaces, fixed implementation surfaces, and likely failure-mode touchpoints.`
- target_file: `src/harness_lab/science_eval.py`
- target_purpose: `Runs smoke-gate and audit outcome classification logic, including hard-fail rules and keeper thresholds.`
- key_functions: `should_run_full_audit, classify_smoke_block, classify_outcome`
- levered_surfaces: `transfer_smoke_min_score, transfer_smoke_max_gap, transfer_smoke_min_boundary_f1`
- fixed_surfaces: `Hard-fail rules for severe smoke regressions; Keeper/improved/audit_blocked/dead_end classification bands; Primary failure-mode attribution ordering`

### Failure-To-Code Hints
- `boundary_smoke:gap_too_wide` -> `science_eval, science_loss, science_model`: `Boundary smoke regressions often reflect a mix of strict smoke-gap thresholds, weak boundary pressure in the loss, or insufficient boundary-sensitive representation capacity.`
- `hard_transfer_regression` -> `science_loss, science_model, science_config`: `Hard-transfer failures usually point to brittle transfer-sensitive structure, insufficient representation robustness, or seed defaults that underweight difficult cases.`
- `transfer_smoke:gap_too_wide` -> `science_eval, science_model`: `A wide benchmark-to-smoke gap is often governed by smoke gate strictness and by whether the model capacity generalizes beyond the local benchmark slice.`

### Code Change Brief
- decision_state: `wait`
- decision_reason: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`
- target_file: `src/harness_lab/science_eval.py`
- target_functions: `should_run_full_audit, classify_smoke_block, classify_outcome`
- proposed_change: `Tighten or clarify smoke and audit classification so severe non-robustness fails earlier while borderline promising runs remain distinguishable.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `wait`
- target_file: `src/harness_lab/science_eval.py`
- max_changed_files: `3`
- allowed_write_files: `src/harness_lab/science_eval.py, tests/test_science_smoke_gate.py, tests/test_science_eval.py`
- focused_tests: `tests/test_science_smoke_gate.py, tests/test_science_eval.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `wait`, so autonomous code mutation stays blocked. Recommended action is `wait`, not `targeted_mutation`. Allowed write scope is 3 files; autonomous mutation requires a target file plus adjacent tests only.`
- execution_mode: `candidate_workspace_only`
- auto_publish: `False`
- silent_rollback: `False`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 2648 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_transfer_regression` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_transfer_regression` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_eval` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
