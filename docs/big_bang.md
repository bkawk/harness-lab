# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-03-31T22:49:41+00:00`
- cycles_completed: `4`
- genesis seed: `cand_0001`
- last candidate: `cand_0157`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `4`

## Latest Step
- candidate: `cand_0157`
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
- `cand_0157`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31726446786090573`
- `cand_0156`: outcome `improved`; diagnosis `complete`; benchmark `0.28253004436822543`
- `cand_0155`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3358701997513282`
- `cand_0154`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32343279344879683`
- `cand_0153`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0155` -> audit `0.3332486601124782`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.314774, audit averaged 0.281763, and the mean transfer gap was 0.033011.`
- recent benchmark avg: `0.31477437635731403`
- recent audit avg: `0.2817631904258503`
- recent transfer gap avg: `0.03301118593146374`
- `cand_0157`: benchmark `0.31726446786090573`, audit `0.24793809416843426`, gap `0.06932637369247147`
- `cand_0156`: benchmark `0.28253004436822543`, audit `0.29403229796171`, gap `-0.011502253593484557`
- `cand_0155`: benchmark `0.3358701997513282`, audit `0.3332486601124782`, gap `0.002621539638849979`
- `cand_0154`: benchmark `0.32343279344879683`, audit `0.25183370946077877`, gap `0.07159908398801806`

## Hindsight
- summary: `In the recent scored window, the lab saw 6 audit-blocked outcomes; it should emphasize transfer-stability checks.`
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
- summary: `Recent backend evolution is concentrated in science_backend (50 candidate(s), avg transfer gap 0.038046).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038046. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 590.4 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `50`, audit_blocked `44`, avg_gap `0.03804591637238257`
- loss: `science_loss` (available); attempts `35`, audit_blocked `30`, avg_gap `0.03775350478529993`
- eval: `science_eval` (available); attempts `42`, audit_blocked `36`, avg_gap `0.03716084613498942`
- config: `science_config` (available); attempts `35`, audit_blocked `30`, avg_gap `0.03775350478529993`
- train: `science_train` (available); attempts `28`, audit_blocked `23`, avg_gap `0.037004486125183915`

### Recent Module Evidence
- `science_backend`: attempts `50`, audit_blocked `44`, avg_gap `0.03804591637238257`
- `science_model`: attempts `50`, audit_blocked `44`, avg_gap `0.03804591637238257`
- `science_eval`: attempts `42`, audit_blocked `36`, avg_gap `0.03716084613498942`
- `science_config`: attempts `35`, audit_blocked `30`, avg_gap `0.03775350478529993`

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
