# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T02:06:54+00:00`
- cycles_completed: `24`
- genesis seed: `cand_0001`
- last candidate: `cand_0322`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0322`
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
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0322`: outcome `keeper`; diagnosis `complete`; benchmark `0.3133963693141253`
- `cand_0321`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39580450134444234`
- `cand_0320`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3180179147188944`
- `cand_0319`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31157754362081386`
- `cand_0318`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4265914147216674`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.353078, audit averaged 0.299025, and the mean transfer gap was 0.054052.`
- recent benchmark avg: `0.35307754874398867`
- recent audit avg: `0.2990254430780208`
- recent transfer gap avg: `0.05405210566596787`
- `cand_0322`: benchmark `0.3133963693141253`, audit `0.3271146573056738`, gap `-0.013718287991548506`
- `cand_0321`: benchmark `0.39580450134444234`, audit `0.31604816980178535`, gap `0.07975633154265699`
- `cand_0320`: benchmark `0.3180179147188944`, audit `0.3138441184561639`, gap `0.004173796262730511`
- `cand_0319`: benchmark `0.31157754362081386`, audit `0.21143126658238642`, gap `0.10014627703842743`
- `cand_0318`: benchmark `0.4265914147216674`, audit `0.3266890032440945`, gap `0.0999024114775729`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_model, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (214 candidate(s), avg transfer gap 0.037817).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 830.4 MB on average, leaving most VRAM unused. 23 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `23`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0322`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0322`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `214`, audit_blocked `135`, avg_gap `0.037817039841816065`
- loss: `science_loss` (targeted); attempts `199`, audit_blocked `121`, avg_gap `0.03774526017201849`
- eval: `science_eval` (available); attempts `206`, audit_blocked `127`, avg_gap `0.03762110790112285`
- config: `science_config` (available); attempts `199`, audit_blocked `121`, avg_gap `0.03774526017201849`
- train: `science_train` (available); attempts `192`, audit_blocked `114`, avg_gap `0.03763345553632878`

### Recent Module Evidence
- `science_backend`: attempts `214`, audit_blocked `135`, avg_gap `0.037817039841816065`
- `science_model`: attempts `214`, audit_blocked `135`, avg_gap `0.037817039841816065`
- `science_eval`: attempts `206`, audit_blocked `127`, avg_gap `0.03762110790112285`
- `science_config`: attempts `199`, audit_blocked `121`, avg_gap `0.03774526017201849`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `heuristic`
- summary: `After 320 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
