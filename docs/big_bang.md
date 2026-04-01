# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T02:53:19+00:00`
- cycles_completed: `27`
- genesis seed: `cand_0001`
- last candidate: `cand_0180`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `27`

## Latest Step
- candidate: `cand_0180`
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
- `cand_0180`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.38787447979792317`
- `cand_0179`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3116176670316466`
- `cand_0178`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.33489082804251497`
- `cand_0177`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3639046391840973`
- `cand_0176`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30229167785837185`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0177` -> audit `0.3589113262474345`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.340116, audit averaged 0.282223, and the mean transfer gap was 0.057893.`
- recent benchmark avg: `0.3401158583829108`
- recent audit avg: `0.2822229697474314`
- recent transfer gap avg: `0.05789288863547939`
- `cand_0180`: benchmark `0.38787447979792317`, audit `0.3273561506251645`, gap `0.06051832917275868`
- `cand_0179`: benchmark `0.3116176670316466`, audit `0.2693187116940423`, gap `0.042298955337604305`
- `cand_0178`: benchmark `0.33489082804251497`, audit `0.24177800210330203`, gap `0.09311282593921294`
- `cand_0177`: benchmark `0.3639046391840973`, audit `0.3589113262474345`, gap `0.00499331293666283`
- `cand_0176`: benchmark `0.30229167785837185`, audit `0.2137506580672137`, gap `0.08854101979115817`

## Hindsight
- summary: `In the recent scored window, the lab saw 6 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 179 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `8`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (73 candidate(s), avg transfer gap 0.041496).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.041496. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 592.9 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `73`, audit_blocked `63`, avg_gap `0.041495501772335186`
- loss: `science_loss` (available); attempts `58`, audit_blocked `49`, avg_gap `0.042203447678020506`
- eval: `science_eval` (available); attempts `65`, audit_blocked `55`, avg_gap `0.04139655118510046`
- config: `science_config` (available); attempts `58`, audit_blocked `49`, avg_gap `0.042203447678020506`
- train: `science_train` (available); attempts `51`, audit_blocked `42`, avg_gap `0.042462283797731835`

### Recent Module Evidence
- `science_backend`: attempts `73`, audit_blocked `63`, avg_gap `0.041495501772335186`
- `science_model`: attempts `73`, audit_blocked `63`, avg_gap `0.041495501772335186`
- `science_eval`: attempts `65`, audit_blocked `55`, avg_gap `0.04139655118510046`
- `science_config`: attempts `58`, audit_blocked `49`, avg_gap `0.042203447678020506`

## External Review
- status: `reviewed`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 179 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.`
- human advice: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 5 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
