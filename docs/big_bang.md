# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-04T22:02:04+00:00`
- cycles_completed: `268`
- genesis seed: `cand_0001`
- last candidate: `cand_0692`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `36`

## Latest Step
- candidate: `cand_0692`
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
- active_candidate: `cand_0692`
- backend_status: `finished`
- backend_pid: `2724029`
- backend_started_at: `2026-04-04T21:52:01+00:00`
- backend_last_poll_at: `2026-04-04T22:02:03+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0692`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32116840822380355`
- `cand_0691`: outcome `dead_end`; diagnosis `complete`; benchmark `0.42175734683874483`
- `cand_0690`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3901111638611123`
- `cand_0689`: outcome `improved`; diagnosis `complete`; benchmark `0.28105452520447083`
- `cand_0688`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3338132309506979`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.349581, audit averaged 0.321645, and the mean transfer gap was 0.027935.`
- recent benchmark avg: `0.34958093501576587`
- recent audit avg: `0.32164548916294017`
- recent transfer gap avg: `0.027935445852825713`
- `cand_0692`: benchmark `0.32116840822380355`, audit `0.3418605297323377`, gap `-0.020692121508534167`
- `cand_0691`: benchmark `0.42175734683874483`, audit `0.31684555247372137`, gap `0.10491179436502346`
- `cand_0690`: benchmark `0.3901111638611123`, audit `0.30572104113981247`, gap `0.08439012272129981`
- `cand_0689`: benchmark `0.28105452520447083`, audit `0.311425277592225`, gap `-0.030370752387754163`
- `cand_0688`: benchmark `0.3338132309506979`, audit `0.3323750448766043`, gap `0.001438186074093628`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 691 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (583 candidate(s), avg transfer gap 0.035074).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 825.8 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_0692`
- train: `batch_size=3, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0692`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.08, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=2, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `583`, audit_blocked `270`, avg_gap `0.0350743261425073`
- loss: `science_loss` (targeted); attempts `568`, audit_blocked `256`, avg_gap `0.03497960600495173`
- eval: `science_eval` (available); attempts `575`, audit_blocked `262`, avg_gap `0.03496880152695594`
- config: `science_config` (available); attempts `568`, audit_blocked `256`, avg_gap `0.03497960600495173`
- train: `science_train` (available); attempts `561`, audit_blocked `249`, avg_gap `0.03490777406904713`

### Recent Module Evidence
- `science_backend`: attempts `583`, audit_blocked `270`, avg_gap `0.0350743261425073`
- `science_model`: attempts `583`, audit_blocked `270`, avg_gap `0.0350743261425073`
- `science_eval`: attempts `575`, audit_blocked `262`, avg_gap `0.03496880152695594`
- `science_config`: attempts `568`, audit_blocked `256`, avg_gap `0.03497960600495173`

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
- status: `reviewed`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 691 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
