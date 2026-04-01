# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T15:14:04+00:00`
- last_heartbeat: `2026-04-01T15:46:06+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0260`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0260`
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
- `cand_0260`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.398051963759918`
- `cand_0259`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3374651513876822`
- `cand_0258`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32573156546973003`
- `cand_0257`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0256`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2829415365286318`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.336048, audit averaged 0.316152, and the mean transfer gap was 0.019895.`
- recent benchmark avg: `0.3360475542864905`
- recent audit avg: `0.3161521546679491`
- recent transfer gap avg: `0.01989539961854138`
- `cand_0260`: benchmark `0.398051963759918`, audit `0.354538818886763`, gap `0.04351314487315505`
- `cand_0259`: benchmark `0.3374651513876822`, audit `0.30963691763721723`, gap `0.027828233750464948`
- `cand_0258`: benchmark `0.32573156546973003`, audit `0.3325471586339299`, gap `-0.006815593164199885`
- `cand_0256`: benchmark `0.2829415365286318`, audit `0.2678857235138864`, gap `0.0150558130147454`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 259 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (152 candidate(s), avg transfer gap 0.035948).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.035948. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 681.6 MB on average, leaving most VRAM unused. 3 scored candidate(s) have landed since structural commit `23dc0ec`.`
- scored_candidates_since_change: `3`
- last_structural_commit: `23dc0ec`
### Chosen Lever Values
- source_candidate: `cand_0260`
- model: `hidden_dim=160`

### Effective Backend Settings
- source_candidate: `cand_0260`
- model: `hidden_dim=160, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `152`, audit_blocked `118`, avg_gap `0.03594784626584418`
- loss: `science_loss` (available); attempts `137`, audit_blocked `104`, avg_gap `0.03563296697902969`
- eval: `science_eval` (available); attempts `144`, audit_blocked `110`, avg_gap `0.03555701502651668`
- config: `science_config` (available); attempts `137`, audit_blocked `104`, avg_gap `0.03563296697902969`
- train: `science_train` (available); attempts `130`, audit_blocked `97`, avg_gap `0.03534357705535045`

### Recent Module Evidence
- `science_backend`: attempts `152`, audit_blocked `118`, avg_gap `0.03594784626584418`
- `science_model`: attempts `152`, audit_blocked `118`, avg_gap `0.03594784626584418`
- `science_eval`: attempts `144`, audit_blocked `110`, avg_gap `0.03555701502651668`
- `science_config`: attempts `137`, audit_blocked `104`, avg_gap `0.03563296697902969`

## External Review
- status: `reviewed`
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
- summary: `The lab has stayed on `science_model` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
