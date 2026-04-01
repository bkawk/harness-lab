# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T17:17:04+00:00`
- last_heartbeat: `2026-04-01T17:27:38+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0271`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0271`
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
- `cand_0271`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3254030537839083`
- `cand_0270`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0269`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31242958357735207`
- `cand_0268`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3465403762922386`
- `cand_0267`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32249526042852283`

## Science Leaders
- best benchmark: `cand_0265` -> `0.450557453846711`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.326717, audit averaged 0.306514, and the mean transfer gap was 0.020203.`
- recent benchmark avg: `0.32671706852050547`
- recent audit avg: `0.30651431431833454`
- recent transfer gap avg: `0.020202754202170936`
- `cand_0271`: benchmark `0.3254030537839083`, audit `0.31108845222457515`, gap `0.014314601559333173`
- `cand_0269`: benchmark `0.31242958357735207`, audit `0.27392692143674885`, gap `0.03850266214060322`
- `cand_0268`: benchmark `0.3465403762922386`, audit `0.2989189963718152`, gap `0.04762137992042342`
- `cand_0267`: benchmark `0.32249526042852283`, audit `0.3421228872401989`, gap `-0.01962762681167607`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_loss` until new evidence appears.`

## Policy
- summary: `After 270 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (163 candidate(s), avg transfer gap 0.035606).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 1 scored candidate(s) have landed since structural commit `2fbef1e`.`
- secondary_context: `Recent real-backend runs are only using about 611.1 MB on average, leaving most VRAM unused. 1 scored candidate(s) have landed since structural commit `2fbef1e`.`
- scored_candidates_since_change: `1`
- last_structural_commit: `2fbef1e`
### Chosen Lever Values
- source_candidate: `cand_0271`
- loss: `boundary_loss_weight=0.08, instance_loss_weight=0.07`

### Effective Backend Settings
- source_candidate: `cand_0271`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.08, instance_loss_weight=0.07, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `163`, audit_blocked `125`, avg_gap `0.035605729593001005`
- loss: `science_loss` (targeted); attempts `148`, audit_blocked `111`, avg_gap `0.035273517488436226`
- eval: `science_eval` (available); attempts `155`, audit_blocked `117`, avg_gap `0.03521774299989157`
- config: `science_config` (available); attempts `148`, audit_blocked `111`, avg_gap `0.035273517488436226`
- train: `science_train` (available); attempts `141`, audit_blocked `104`, avg_gap `0.03498250637891246`

### Recent Module Evidence
- `science_backend`: attempts `163`, audit_blocked `125`, avg_gap `0.035605729593001005`
- `science_model`: attempts `163`, audit_blocked `125`, avg_gap `0.035605729593001005`
- `science_eval`: attempts `155`, audit_blocked `117`, avg_gap `0.03521774299989157`
- `science_config`: attempts `148`, audit_blocked `111`, avg_gap `0.035273517488436226`

## External Review
- status: `reviewed`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 270 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `The lab has stayed on `science_loss` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
