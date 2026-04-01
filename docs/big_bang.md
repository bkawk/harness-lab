# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T17:50:34+00:00`
- last_heartbeat: `2026-04-01T18:56:04+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0281`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0281`
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
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0281`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4640540113671977`
- `cand_0280`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34979019362003316`
- `cand_0279`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4158628853709419`
- `cand_0278`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3070950882979646`
- `cand_0277`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36251520353125916`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.379863, audit averaged 0.330121, and the mean transfer gap was 0.049743.`
- recent benchmark avg: `0.3798634764374793`
- recent audit avg: `0.33012053703953254`
- recent transfer gap avg: `0.04974293939794676`
- `cand_0281`: benchmark `0.4640540113671977`, audit `0.37690772823427676`, gap `0.08714628313292094`
- `cand_0280`: benchmark `0.34979019362003316`, audit `0.3147329208892622`, gap `0.03505727273077097`
- `cand_0279`: benchmark `0.4158628853709419`, audit `0.3112992131463217`, gap `0.10456367222462021`
- `cand_0278`: benchmark `0.3070950882979646`, audit `0.3407755189288053`, gap `-0.033680430630840696`
- `cand_0277`: benchmark `0.36251520353125916`, audit `0.3068873039989968`, gap `0.05562789953226238`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 7 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_loss` until new evidence appears.`

## Policy
- summary: `After 280 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (173 candidate(s), avg transfer gap 0.036338).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 601.9 MB on average, leaving most VRAM unused. 6 scored candidate(s) have landed since structural commit `a225c8b`.`
- scored_candidates_since_change: `6`
- last_structural_commit: `a225c8b`
### Chosen Lever Values
- source_candidate: `cand_0281`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0281`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.04, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `173`, audit_blocked `125`, avg_gap `0.03633840449241149`
- loss: `science_loss` (targeted); attempts `158`, audit_blocked `111`, avg_gap `0.03609737306410542`
- eval: `science_eval` (available); attempts `165`, audit_blocked `117`, avg_gap `0.03600998251976769`
- config: `science_config` (available); attempts `158`, audit_blocked `111`, avg_gap `0.03609737306410542`
- train: `science_train` (available); attempts `151`, audit_blocked `104`, avg_gap `0.03586593498356143`

### Recent Module Evidence
- `science_backend`: attempts `173`, audit_blocked `125`, avg_gap `0.03633840449241149`
- `science_model`: attempts `173`, audit_blocked `125`, avg_gap `0.03633840449241149`
- `science_eval`: attempts `165`, audit_blocked `117`, avg_gap `0.03600998251976769`
- `science_config`: attempts `158`, audit_blocked `111`, avg_gap `0.03609737306410542`

## External Review
- status: `reviewed`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 280 candidates, the lab requested peer review because `dead_end_streak` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
