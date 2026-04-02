# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T03:58:05+00:00`
- cycles_completed: `34`
- genesis seed: `cand_0001`
- last candidate: `cand_0332`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0332`
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
- `cand_0332`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.41029974976391587`
- `cand_0331`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30686888118056277`
- `cand_0330`: outcome `dead_end`; diagnosis `complete`; benchmark `0.348135404293185`
- `cand_0329`: outcome `keeper`; diagnosis `complete`; benchmark `0.30550183895481997`
- `cand_0328`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3896409037905773`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.352089, audit averaged 0.332147, and the mean transfer gap was 0.019942.`
- recent benchmark avg: `0.3520893555966122`
- recent audit avg: `0.33214733181355727`
- recent transfer gap avg: `0.01994202378305492`
- `cand_0332`: benchmark `0.41029974976391587`, audit `0.35923581843548724`, gap `0.051063931328428624`
- `cand_0331`: benchmark `0.30686888118056277`, audit `0.3548833239705644`, gap `-0.04801444279000161`
- `cand_0330`: benchmark `0.348135404293185`, audit `0.3175619767458397`, gap `0.030573427547345322`
- `cand_0329`: benchmark `0.30550183895481997`, audit `0.3040924480694087`, gap `0.0014093908854112547`
- `cand_0328`: benchmark `0.3896409037905773`, audit `0.3249630918464863`, gap `0.064677811944091`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

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
- summary: `Recent backend evolution is concentrated in science_backend (224 candidate(s), avg transfer gap 0.037736).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 683.6 MB on average, leaving most VRAM unused. 33 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `33`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0332`
- model: `global_dim=256, hidden_dim=160`

### Effective Backend Settings
- source_candidate: `cand_0332`
- model: `hidden_dim=160, global_dim=256, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `224`, audit_blocked `140`, avg_gap `0.03773620424103179`
- loss: `science_loss` (targeted); attempts `209`, audit_blocked `126`, avg_gap `0.03766218726467743`
- eval: `science_eval` (available); attempts `216`, audit_blocked `132`, avg_gap `0.037547144732802754`
- config: `science_config` (available); attempts `209`, audit_blocked `126`, avg_gap `0.03766218726467743`
- train: `science_train` (available); attempts `202`, audit_blocked `119`, avg_gap `0.0375533968762097`

### Recent Module Evidence
- `science_backend`: attempts `224`, audit_blocked `140`, avg_gap `0.03773620424103179`
- `science_model`: attempts `224`, audit_blocked `140`, avg_gap `0.03773620424103179`
- `science_eval`: attempts `216`, audit_blocked `132`, avg_gap `0.037547144732802754`
- `science_config`: attempts `209`, audit_blocked `126`, avg_gap `0.03766218726467743`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 330 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
