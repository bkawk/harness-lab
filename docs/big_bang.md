# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T19:43:12+00:00`
- last_heartbeat: `2026-04-01T21:12:51+00:00`
- cycles_completed: `8`
- genesis seed: `cand_0001`
- last candidate: `cand_0295`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0295`
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
- `cand_0295`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29720201562223736`
- `cand_0294`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33998006136930964`
- `cand_0293`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34996466017366057`
- `cand_0292`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3572614070952871`
- `cand_0291`: outcome `dead_end`; diagnosis `complete`; benchmark `0.41228768477774347`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.351339, audit averaged 0.294922, and the mean transfer gap was 0.056417.`
- recent benchmark avg: `0.3513391658076476`
- recent audit avg: `0.2949224119129166`
- recent transfer gap avg: `0.05641675389473102`
- `cand_0295`: benchmark `0.29720201562223736`, audit `0.26414141766380617`, gap `0.03306059795843119`
- `cand_0294`: benchmark `0.33998006136930964`, audit `0.31066645313231545`, gap `0.029313608236994193`
- `cand_0293`: benchmark `0.34996466017366057`, audit `0.2733197924446983`, gap `0.07664486772896228`
- `cand_0292`: benchmark `0.3572614070952871`, audit `0.3056409058209038`, gap `0.05162050127438328`
- `cand_0291`: benchmark `0.41228768477774347`, audit `0.3208434905028593`, gap `0.09144419427488415`

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
- summary: `Recent backend evolution is concentrated in science_backend (187 candidate(s), avg transfer gap 0.036729).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 645.1 MB on average, leaving most VRAM unused. 9 scored candidate(s) have landed since structural commit `0ab69b5`.`
- scored_candidates_since_change: `9`
- last_structural_commit: `0ab69b5`
### Chosen Lever Values
- source_candidate: `cand_0295`
- train: `batch_size=3, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0295`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=2, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `187`, audit_blocked `129`, avg_gap `0.036729332741194574`
- loss: `science_loss` (targeted); attempts `172`, audit_blocked `115`, avg_gap `0.03654282709271622`
- eval: `science_eval` (available); attempts `179`, audit_blocked `121`, avg_gap `0.03644439507622397`
- config: `science_config` (available); attempts `172`, audit_blocked `115`, avg_gap `0.03654282709271622`
- train: `science_train` (available); attempts `165`, audit_blocked `108`, avg_gap `0.03635127631559659`

### Recent Module Evidence
- `science_backend`: attempts `187`, audit_blocked `129`, avg_gap `0.036729332741194574`
- `science_model`: attempts `187`, audit_blocked `129`, avg_gap `0.036729332741194574`
- `science_eval`: attempts `179`, audit_blocked `121`, avg_gap `0.03644439507622397`
- `science_config`: attempts `172`, audit_blocked `115`, avg_gap `0.03654282709271622`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
