# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T02:42:44+00:00`
- cycles_completed: `26`
- genesis seed: `cand_0001`
- last candidate: `cand_0179`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `26`

## Latest Step
- candidate: `cand_0179`
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
- `cand_0179`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3116176670316466`
- `cand_0178`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.33489082804251497`
- `cand_0177`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3639046391840973`
- `cand_0176`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30229167785837185`
- `cand_0175`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32597718606334886`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0177` -> audit `0.3589113262474345`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.327736, audit averaged 0.266461, and the mean transfer gap was 0.061275.`
- recent benchmark avg: `0.32773639963599593`
- recent audit avg: `0.2664613961528994`
- recent transfer gap avg: `0.061275003483096536`
- `cand_0179`: benchmark `0.3116176670316466`, audit `0.2693187116940423`, gap `0.042298955337604305`
- `cand_0178`: benchmark `0.33489082804251497`, audit `0.24177800210330203`, gap `0.09311282593921294`
- `cand_0177`: benchmark `0.3639046391840973`, audit `0.3589113262474345`, gap `0.00499331293666283`
- `cand_0176`: benchmark `0.30229167785837185`, audit `0.2137506580672137`, gap `0.08854101979115817`
- `cand_0175`: benchmark `0.32597718606334886`, audit `0.2485482826525044`, gap `0.07742890341084446`

## Hindsight
- summary: `In the recent scored window, the lab saw 6 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
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
- summary: `Recent backend evolution is concentrated in science_backend (72 candidate(s), avg transfer gap 0.041216).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.041216. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 592.9 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `72`, audit_blocked `62`, avg_gap `0.041215754310564255`
- loss: `science_loss` (available); attempts `57`, audit_blocked `48`, avg_gap `0.04186428320589572`
- eval: `science_eval` (available); attempts `64`, audit_blocked `54`, avg_gap `0.04107785488530615`
- config: `science_config` (available); attempts `57`, audit_blocked `48`, avg_gap `0.04186428320589572`
- train: `science_train` (available); attempts `50`, audit_blocked `41`, avg_gap `0.042078112619539774`

### Recent Module Evidence
- `science_backend`: attempts `72`, audit_blocked `62`, avg_gap `0.041215754310564255`
- `science_model`: attempts `72`, audit_blocked `62`, avg_gap `0.041215754310564255`
- `science_eval`: attempts `64`, audit_blocked `54`, avg_gap `0.04107785488530615`
- `science_config`: attempts `57`, audit_blocked `48`, avg_gap `0.04186428320589572`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
