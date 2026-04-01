# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-01T22:23:01+00:00`
- cycles_completed: `4`
- genesis seed: `cand_0001`
- last candidate: `cand_0302`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0302`
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
- `cand_0302`: outcome `dead_end`; diagnosis `complete`; benchmark `0.41320331208073857`
- `cand_0301`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34707212997570036`
- `cand_0300`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29574560126772687`
- `cand_0299`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3128551711335869`
- `cand_0298`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.342219, audit averaged 0.292418, and the mean transfer gap was 0.049801.`
- recent benchmark avg: `0.34221905361443816`
- recent audit avg: `0.2924175624944527`
- recent transfer gap avg: `0.04980149111998544`
- `cand_0302`: benchmark `0.41320331208073857`, audit `0.31541424042073174`, gap `0.09778907166000683`
- `cand_0301`: benchmark `0.34707212997570036`, audit `0.28642407490251676`, gap `0.060648055073183604`
- `cand_0300`: benchmark `0.29574560126772687`, audit `0.23282680776107983`, gap `0.06291879350664703`
- `cand_0299`: benchmark `0.3128551711335869`, audit `0.3350051268934826`, gap `-0.0221499557598957`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_loss` until new evidence appears.`

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
- summary: `Recent backend evolution is concentrated in science_backend (194 candidate(s), avg transfer gap 0.036821).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 710.9 MB on average, leaving most VRAM unused. 3 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `3`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0300`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0302`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `194`, audit_blocked `130`, avg_gap `0.03682117588866312`
- loss: `science_loss` (targeted); attempts `179`, audit_blocked `116`, avg_gap `0.03665018532376818`
- eval: `science_eval` (available); attempts `186`, audit_blocked `122`, avg_gap `0.036551420653317186`
- config: `science_config` (available); attempts `179`, audit_blocked `116`, avg_gap `0.03665018532376818`
- train: `science_train` (available); attempts `172`, audit_blocked `109`, avg_gap `0.03647147787286532`

### Recent Module Evidence
- `science_backend`: attempts `194`, audit_blocked `130`, avg_gap `0.03682117588866312`
- `science_model`: attempts `194`, audit_blocked `130`, avg_gap `0.03682117588866312`
- `science_eval`: attempts `186`, audit_blocked `122`, avg_gap `0.036551420653317186`
- `science_config`: attempts `179`, audit_blocked `116`, avg_gap `0.03665018532376818`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 300 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
