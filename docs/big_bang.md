# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T09:16:42+00:00`
- last_heartbeat: `2026-04-01T09:47:57+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0224`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0224`
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
- `cand_0224`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3378123307088491`
- `cand_0223`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3306176623249132`
- `cand_0222`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3234491172910994`
- `cand_0221`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0220`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32856356006880877`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.330111, audit averaged 0.305955, and the mean transfer gap was 0.024155.`
- recent benchmark avg: `0.3301106675984176`
- recent audit avg: `0.3059552165569813`
- recent transfer gap avg: `0.024155451041436266`
- `cand_0224`: benchmark `0.3378123307088491`, audit `0.33634708448675976`, gap `0.0014652462220893225`
- `cand_0223`: benchmark `0.3306176623249132`, audit `0.287004544693982`, gap `0.043613117630931175`
- `cand_0222`: benchmark `0.3234491172910994`, audit `0.28560840631751905`, gap `0.03784071097358033`
- `cand_0220`: benchmark `0.32856356006880877`, audit `0.31486083072966453`, gap `0.013702729339144237`

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
- summary: `Mechanisms initial_harness, science_model, budget_policy_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `9`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (116 candidate(s), avg transfer gap 0.038163).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038163. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 2 scored candidate(s) have landed since structural commit `2be55f0`.`
- secondary_context: `Recent real-backend runs are only using about 590.5 MB on average, leaving most VRAM unused. 2 scored candidate(s) have landed since structural commit `2be55f0`.`
- scored_candidates_since_change: `2`
- last_structural_commit: `2be55f0`
### Chosen Lever Values
- source_candidate: `cand_0224`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0224`
- model: `hidden_dim=96, global_dim=192, instance_dim=12, k_neighbors=8, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `116`, audit_blocked `94`, avg_gap `0.03816290215519894`
- loss: `science_loss` (available); attempts `101`, audit_blocked `80`, avg_gap `0.03807807391533945`
- eval: `science_eval` (available); attempts `108`, audit_blocked `86`, avg_gap `0.03782582192057618`
- config: `science_config` (available); attempts `101`, audit_blocked `80`, avg_gap `0.03807807391533945`
- train: `science_train` (available); attempts `94`, audit_blocked `73`, avg_gap `0.03788219912257011`

### Recent Module Evidence
- `science_backend`: attempts `116`, audit_blocked `94`, avg_gap `0.03816290215519894`
- `science_model`: attempts `116`, audit_blocked `94`, avg_gap `0.03816290215519894`
- `science_eval`: attempts `108`, audit_blocked `86`, avg_gap `0.03782582192057618`
- `science_config`: attempts `101`, audit_blocked `80`, avg_gap `0.03807807391533945`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 222 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `hard_transfer_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_model` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_model` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `hard_transfer_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `science_model` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
