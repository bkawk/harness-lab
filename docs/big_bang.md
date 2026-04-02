# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T01:44:35+00:00`
- cycles_completed: `22`
- genesis seed: `cand_0001`
- last candidate: `cand_0320`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `4`

## Latest Step
- candidate: `cand_0320`
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
- `cand_0320`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3180179147188944`
- `cand_0319`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31157754362081386`
- `cand_0318`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4265914147216674`
- `cand_0317`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3232360976110454`
- `cand_0316`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3520256106046247`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.346290, audit averaged 0.284325, and the mean transfer gap was 0.061965.`
- recent benchmark avg: `0.34628971625540916`
- recent audit avg: `0.2843248944785196`
- recent transfer gap avg: `0.06196482177688952`
- `cand_0320`: benchmark `0.3180179147188944`, audit `0.3138441184561639`, gap `0.004173796262730511`
- `cand_0319`: benchmark `0.31157754362081386`, audit `0.21143126658238642`, gap `0.10014627703842743`
- `cand_0318`: benchmark `0.4265914147216674`, audit `0.3266890032440945`, gap `0.0999024114775729`
- `cand_0317`: benchmark `0.3232360976110454`, audit `0.27833325484539406`, gap `0.04490284276565132`
- `cand_0316`: benchmark `0.3520256106046247`, audit `0.2913268292645592`, gap `0.060698781340065455`

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
- summary: `Recent backend evolution is concentrated in science_backend (212 candidate(s), avg transfer gap 0.037868).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 793.0 MB on average, leaving most VRAM unused. 21 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `21`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0320`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0320`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `212`, audit_blocked `135`, avg_gap `0.037868355543059506`
- loss: `science_loss` (available); attempts `197`, audit_blocked `121`, avg_gap `0.03779989876619727`
- eval: `science_eval` (available); attempts `204`, audit_blocked `127`, avg_gap `0.037672527857833114`
- config: `science_config` (available); attempts `197`, audit_blocked `121`, avg_gap `0.03779989876619727`
- train: `science_train` (targeted); attempts `190`, audit_blocked `114`, avg_gap `0.037689051123808`

### Recent Module Evidence
- `science_backend`: attempts `212`, audit_blocked `135`, avg_gap `0.037868355543059506`
- `science_model`: attempts `212`, audit_blocked `135`, avg_gap `0.037868355543059506`
- `science_eval`: attempts `204`, audit_blocked `127`, avg_gap `0.037672527857833114`
- `science_config`: attempts `197`, audit_blocked `121`, avg_gap `0.03779989876619727`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 1 ranked requests for human help.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
