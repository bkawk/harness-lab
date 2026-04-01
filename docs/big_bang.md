# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T17:50:34+00:00`
- last_heartbeat: `2026-04-01T18:34:01+00:00`
- cycles_completed: `4`
- genesis seed: `cand_0001`
- last candidate: `cand_0279`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0279`
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
- `cand_0279`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4158628853709419`
- `cand_0278`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3070950882979646`
- `cand_0277`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36251520353125916`
- `cand_0276`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32872138855302646`
- `cand_0275`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0265` -> `0.450557453846711`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.353549, audit averaged 0.318783, and the mean transfer gap was 0.034765.`
- recent benchmark avg: `0.353548641438298`
- recent audit avg: `0.3187834151422893`
- recent transfer gap avg: `0.03476522629600873`
- `cand_0279`: benchmark `0.4158628853709419`, audit `0.3112992131463217`, gap `0.10456367222462021`
- `cand_0278`: benchmark `0.3070950882979646`, audit `0.3407755189288053`, gap `-0.033680430630840696`
- `cand_0277`: benchmark `0.36251520353125916`, audit `0.3068873039989968`, gap `0.05562789953226238`
- `cand_0276`: benchmark `0.32872138855302646`, audit `0.31617162449503344`, gap `0.012549764057993018`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (171 candidate(s), avg transfer gap 0.036008).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 591.1 MB on average, leaving most VRAM unused. 4 scored candidate(s) have landed since structural commit `a225c8b`.`
- scored_candidates_since_change: `4`
- last_structural_commit: `a225c8b`
### Chosen Lever Values
- source_candidate: `cand_0279`
- config: `lr=0.0004, weight_decay=5e-05`

### Effective Backend Settings
- source_candidate: `cand_0279`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=5e-05, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `171`, audit_blocked `125`, avg_gap `0.0360082261798857`
- loss: `science_loss` (targeted); attempts `156`, audit_blocked `111`, avg_gap `0.03572966122781512`
- eval: `science_eval` (available); attempts `163`, audit_blocked `117`, avg_gap `0.03565657695058349`
- config: `science_config` (available); attempts `156`, audit_blocked `111`, avg_gap `0.03572966122781512`
- train: `science_train` (available); attempts `149`, audit_blocked `104`, avg_gap `0.035474681604518256`

### Recent Module Evidence
- `science_backend`: attempts `171`, audit_blocked `125`, avg_gap `0.0360082261798857`
- `science_model`: attempts `171`, audit_blocked `125`, avg_gap `0.0360082261798857`
- `science_eval`: attempts `163`, audit_blocked `117`, avg_gap `0.03565657695058349`
- `science_config`: attempts `156`, audit_blocked `111`, avg_gap `0.03572966122781512`

## External Review
- status: `cooldown`
- trigger_reason: `dead_end_streak`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_config` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
