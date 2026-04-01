# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T15:14:04+00:00`
- last_heartbeat: `2026-04-01T15:57:07+00:00`
- cycles_completed: `4`
- genesis seed: `cand_0001`
- last candidate: `cand_0261`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0261`
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
- `cand_0261`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3304419035054234`
- `cand_0260`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.398051963759918`
- `cand_0259`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3374651513876822`
- `cand_0258`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32573156546973003`
- `cand_0257`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.347923, audit averaged 0.333767, and the mean transfer gap was 0.014156.`
- recent benchmark avg: `0.3479226460306884`
- recent audit avg: `0.33376680576343687`
- recent transfer gap avg: `0.014155840267251571`
- `cand_0261`: benchmark `0.3304419035054234`, audit `0.33834432789583724`, gap `-0.007902424390413831`
- `cand_0260`: benchmark `0.398051963759918`, audit `0.354538818886763`, gap `0.04351314487315505`
- `cand_0259`: benchmark `0.3374651513876822`, audit `0.30963691763721723`, gap `0.027828233750464948`
- `cand_0258`: benchmark `0.32573156546973003`, audit `0.3325471586339299`, gap `-0.006815593164199885`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_model, budget_policy_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `11`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (153 candidate(s), avg transfer gap 0.035630).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.035630. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 645.6 MB on average, leaving most VRAM unused. 4 scored candidate(s) have landed since structural commit `23dc0ec`.`
- scored_candidates_since_change: `4`
- last_structural_commit: `23dc0ec`
### Chosen Lever Values
- source_candidate: `cand_0261`
- train: `batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0261`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `153`, audit_blocked `119`, avg_gap `0.03563009068137854`
- loss: `science_loss` (available); attempts `138`, audit_blocked `105`, avg_gap `0.035281875113147086`
- eval: `science_eval` (available); attempts `145`, audit_blocked `111`, avg_gap `0.03522271164638645`
- config: `science_config` (available); attempts `138`, audit_blocked `105`, avg_gap `0.035281875113147086`
- train: `science_train` (available); attempts `131`, audit_blocked `98`, avg_gap `0.034973953111369555`

### Recent Module Evidence
- `science_backend`: attempts `153`, audit_blocked `119`, avg_gap `0.03563009068137854`
- `science_model`: attempts `153`, audit_blocked `119`, avg_gap `0.03563009068137854`
- `science_eval`: attempts `145`, audit_blocked `111`, avg_gap `0.03522271164638645`
- `science_config`: attempts `138`, audit_blocked `105`, avg_gap `0.035281875113147086`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 259 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_model` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_model` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
