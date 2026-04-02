# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T01:56:02+00:00`
- cycles_completed: `23`
- genesis seed: `cand_0001`
- last candidate: `cand_0321`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `4`

## Latest Step
- candidate: `cand_0321`
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
- `cand_0321`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39580450134444234`
- `cand_0320`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3180179147188944`
- `cand_0319`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31157754362081386`
- `cand_0318`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4265914147216674`
- `cand_0317`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3232360976110454`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.355045, audit averaged 0.289269, and the mean transfer gap was 0.065776.`
- recent benchmark avg: `0.3550454944033727`
- recent audit avg: `0.28926916258596486`
- recent transfer gap avg: `0.06577633181740783`
- `cand_0321`: benchmark `0.39580450134444234`, audit `0.31604816980178535`, gap `0.07975633154265699`
- `cand_0320`: benchmark `0.3180179147188944`, audit `0.3138441184561639`, gap `0.004173796262730511`
- `cand_0319`: benchmark `0.31157754362081386`, audit `0.21143126658238642`, gap `0.10014627703842743`
- `cand_0318`: benchmark `0.4265914147216674`, audit `0.3266890032440945`, gap `0.0999024114775729`
- `cand_0317`: benchmark `0.3232360976110454`, audit `0.27833325484539406`, gap `0.04490284276565132`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_loss` until new evidence appears.`

## Policy
- summary: `After 320 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (213 candidate(s), avg transfer gap 0.038091).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 830.8 MB on average, leaving most VRAM unused. 22 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `22`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0321`
- train: `batch_size=4, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0321`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=2, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `213`, audit_blocked `135`, avg_gap `0.03809116392603609`
- loss: `science_loss` (targeted); attempts `198`, audit_blocked `121`, avg_gap `0.038041027690199916`
- eval: `science_eval` (available); attempts `205`, audit_blocked `127`, avg_gap `0.03790632676719325`
- config: `science_config` (available); attempts `198`, audit_blocked `121`, avg_gap `0.038041027690199916`
- train: `science_train` (available); attempts `191`, audit_blocked `114`, avg_gap `0.0379409510065556`

### Recent Module Evidence
- `science_backend`: attempts `213`, audit_blocked `135`, avg_gap `0.03809116392603609`
- `science_model`: attempts `213`, audit_blocked `135`, avg_gap `0.03809116392603609`
- `science_eval`: attempts `205`, audit_blocked `127`, avg_gap `0.03790632676719325`
- `science_config`: attempts `198`, audit_blocked `121`, avg_gap `0.038041027690199916`

## External Review
- status: `reviewed`
- trigger_reason: `exhaustion_signal`
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
- summary: `The lab has stayed on `science_train` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
