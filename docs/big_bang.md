# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T05:21:46+00:00`
- cycles_completed: `41`
- genesis seed: `cand_0001`
- last candidate: `cand_0194`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `41`

## Latest Step
- candidate: `cand_0194`
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
- `cand_0194`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2834840213850871`
- `cand_0193`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3320291505510382`
- `cand_0192`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3386050697813844`
- `cand_0191`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3729256657302539`
- `cand_0190`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3106586247355788`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.327541, audit averaged 0.304654, and the mean transfer gap was 0.022886.`
- recent benchmark avg: `0.32754050643666843`
- recent audit avg: `0.3046543796382465`
- recent transfer gap avg: `0.02288612679842201`
- `cand_0194`: benchmark `0.2834840213850871`, audit `0.25345134589773444`, gap `0.030032675487352667`
- `cand_0193`: benchmark `0.3320291505510382`, audit `0.3681859104955394`, gap `-0.03615675994450118`
- `cand_0192`: benchmark `0.3386050697813844`, audit `0.2970281971976807`, gap `0.04157687258370368`
- `cand_0191`: benchmark `0.3729256657302539`, audit `0.3597440134315013`, gap `0.013181652298752566`
- `cand_0190`: benchmark `0.3106586247355788`, audit `0.2448624311687765`, gap `0.0657961935668023`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
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
- summary: `Recent backend evolution is concentrated in science_backend (87 candidate(s), avg transfer gap 0.039371).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.039371. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 593.5 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `87`, audit_blocked `74`, avg_gap `0.03937050600490901`
- loss: `science_loss` (available); attempts `72`, audit_blocked `60`, avg_gap `0.039503652150832576`
- eval: `science_eval` (available); attempts `79`, audit_blocked `66`, avg_gap `0.03906335997876597`
- config: `science_config` (available); attempts `72`, audit_blocked `60`, avg_gap `0.039503652150832576`
- train: `science_train` (available); attempts `65`, audit_blocked `53`, avg_gap `0.03939922578076529`

### Recent Module Evidence
- `science_backend`: attempts `87`, audit_blocked `74`, avg_gap `0.03937050600490901`
- `science_model`: attempts `87`, audit_blocked `74`, avg_gap `0.03937050600490901`
- `science_eval`: attempts `79`, audit_blocked `66`, avg_gap `0.03906335997876597`
- `science_config`: attempts `72`, audit_blocked `60`, avg_gap `0.039503652150832576`

## External Review
- status: `idle`
- trigger_reason: `-`
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
