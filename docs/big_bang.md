# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T00:25:01+00:00`
- cycles_completed: `13`
- genesis seed: `cand_0001`
- last candidate: `cand_0166`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `13`

## Latest Step
- candidate: `cand_0166`
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
- `cand_0166`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32597718606334886`
- `cand_0165`: outcome `improved`; diagnosis `complete`; benchmark `0.2764831794445113`
- `cand_0164`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.33632390209959534`
- `cand_0163`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3624054124267029`
- `cand_0162`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3671837718672786`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0155` -> audit `0.3332486601124782`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.333675, audit averaged 0.286712, and the mean transfer gap was 0.046963.`
- recent benchmark avg: `0.3336746903802874`
- recent audit avg: `0.2867115976305347`
- recent transfer gap avg: `0.046963092749752654`
- `cand_0166`: benchmark `0.32597718606334886`, audit `0.2485482826525044`, gap `0.07742890341084446`
- `cand_0165`: benchmark `0.2764831794445113`, audit `0.3048762100453634`, gap `-0.02839303060085213`
- `cand_0164`: benchmark `0.33632390209959534`, audit `0.33246646951913505`, gap `0.003857432580460285`
- `cand_0163`: benchmark `0.3624054124267029`, audit `0.2750895604906516`, gap `0.08731585193605129`
- `cand_0162`: benchmark `0.3671837718672786`, audit `0.2725774654450192`, gap `0.09460630642225937`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
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
- summary: `Recent backend evolution is concentrated in science_backend (59 candidate(s), avg transfer gap 0.039296).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.039296. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 593.4 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `59`, audit_blocked `52`, avg_gap `0.03929557713593353`
- loss: `science_loss` (available); attempts `44`, audit_blocked `38`, avg_gap `0.03949406688966694`
- eval: `science_eval` (available); attempts `51`, audit_blocked `44`, avg_gap `0.038792696648432864`
- config: `science_config` (available); attempts `44`, audit_blocked `38`, avg_gap `0.03949406688966694`
- train: `science_train` (available); attempts `37`, audit_blocked `31`, avg_gap `0.03930166889636307`

### Recent Module Evidence
- `science_backend`: attempts `59`, audit_blocked `52`, avg_gap `0.03929557713593353`
- `science_model`: attempts `59`, audit_blocked `52`, avg_gap `0.03929557713593353`
- `science_eval`: attempts `51`, audit_blocked `44`, avg_gap `0.038792696648432864`
- `science_config`: attempts `44`, audit_blocked `38`, avg_gap `0.03949406688966694`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
