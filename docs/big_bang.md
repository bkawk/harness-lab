# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T14:20:42+00:00`
- cycles_completed: `16`
- genesis seed: `cand_0001`
- last candidate: `cand_0391`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0391`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `novelty_cycle`

## Active Backend
- active_candidate: `cand_0391`
- backend_status: `finished`
- backend_pid: `2373445`
- backend_started_at: `2026-04-02T14:10:39+00:00`
- backend_last_poll_at: `2026-04-02T14:20:42+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0391`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3132285381922586`
- `cand_0390`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3432851878462814`
- `cand_0389`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2960954506350956`
- `cand_0388`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39733018136861953`
- `cand_0387`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4118682268215486`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.352362, audit averaged 0.314174, and the mean transfer gap was 0.038188.`
- recent benchmark avg: `0.35236151697276075`
- recent audit avg: `0.3141736037487312`
- recent transfer gap avg: `0.03818791322402953`
- `cand_0391`: benchmark `0.3132285381922586`, audit `0.344813289292644`, gap `-0.03158475110038539`
- `cand_0390`: benchmark `0.3432851878462814`, audit `0.3131957289352084`, gap `0.030089458911073008`
- `cand_0389`: benchmark `0.2960954506350956`, audit `0.2137599838237347`, gap `0.08233546681136092`
- `cand_0388`: benchmark `0.39733018136861953`, audit `0.3574046793757272`, gap `0.039925501992892354`
- `cand_0387`: benchmark `0.4118682268215486`, audit `0.34169433731634186`, gap `0.07017388950520675`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `After 390 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (282 candidate(s), avg transfer gap 0.039000).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 766.4 MB on average, leaving most VRAM unused. 6 scored candidate(s) have landed since structural commit `4d32d84`.`
- scored_candidates_since_change: `6`
- last_structural_commit: `4d32d84`
### Chosen Lever Values
- source_candidate: `cand_0391`
- model: `global_dim=256, instance_dim=24`

### Effective Backend Settings
- source_candidate: `cand_0391`
- model: `hidden_dim=160, global_dim=256, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `282`, audit_blocked `159`, avg_gap `0.03899956321941251`
- loss: `science_loss` (targeted); attempts `267`, audit_blocked `145`, avg_gap `0.03901634424912585`
- eval: `science_eval` (available); attempts `274`, audit_blocked `151`, avg_gap `0.038892991521688326`
- config: `science_config` (available); attempts `267`, audit_blocked `145`, avg_gap `0.03901634424912585`
- train: `science_train` (available); attempts `260`, audit_blocked `138`, avg_gap `0.03897354948611235`

### Recent Module Evidence
- `science_backend`: attempts `282`, audit_blocked `159`, avg_gap `0.03899956321941251`
- `science_model`: attempts `282`, audit_blocked `159`, avg_gap `0.03899956321941251`
- `science_eval`: attempts `274`, audit_blocked `151`, avg_gap `0.038892991521688326`
- `science_config`: attempts `267`, audit_blocked `145`, avg_gap `0.03901634424912585`

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
- target_file: `src/harness_lab/science_train.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_train.py, tests/test_science_train.py`
- focused_tests: `tests/test_science_train.py`
- verification_status: `No verification run recorded yet.`

## External Review
- status: `reviewed`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 390 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
