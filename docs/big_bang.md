# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-03-31T22:39:06+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0156`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0156`
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
- `cand_0156`: outcome `improved`; diagnosis `complete`; benchmark `0.28253004436822543`
- `cand_0155`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3358701997513282`
- `cand_0154`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32343279344879683`
- `cand_0153`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0152`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.39496752181409667`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0155` -> audit `0.3332486601124782`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.334200, audit averaged 0.301233, and the mean transfer gap was 0.032967.`
- recent benchmark avg: `0.3342001398456118`
- recent audit avg: `0.30123265820845674`
- recent transfer gap avg: `0.03296748163715506`
- `cand_0156`: benchmark `0.28253004436822543`, audit `0.29403229796171`, gap `-0.011502253593484557`
- `cand_0155`: benchmark `0.3358701997513282`, audit `0.3332486601124782`, gap `0.002621539638849979`
- `cand_0154`: benchmark `0.32343279344879683`, audit `0.25183370946077877`, gap `0.07159908398801806`
- `cand_0152`: benchmark `0.39496752181409667`, audit `0.3258159652988599`, gap `0.06915155651523675`

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
- summary: `Recent backend evolution is concentrated in science_backend (49 candidate(s), avg transfer gap 0.037351).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.037351. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 592.9 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `49`, audit_blocked `43`, avg_gap `0.037350795098602806`
- loss: `science_loss` (available); attempts `34`, audit_blocked `29`, avg_gap `0.03673502514313311`
- eval: `science_eval` (available); attempts `41`, audit_blocked `35`, avg_gap `0.036291507552354774`
- config: `science_config` (available); attempts `34`, audit_blocked `29`, avg_gap `0.03673502514313311`
- train: `science_train` (available); attempts `27`, audit_blocked `22`, avg_gap `0.03565774080988027`

### Recent Module Evidence
- `science_backend`: attempts `49`, audit_blocked `43`, avg_gap `0.037350795098602806`
- `science_model`: attempts `49`, audit_blocked `43`, avg_gap `0.037350795098602806`
- `science_eval`: attempts `41`, audit_blocked `35`, avg_gap `0.036291507552354774`
- `science_config`: attempts `34`, audit_blocked `29`, avg_gap `0.03673502514313311`

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
