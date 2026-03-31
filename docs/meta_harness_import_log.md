# Meta-Harness Import Log

This log tracks the main ideas we wanted to absorb from the Meta-Harness artifact and whether they are already in `harness-lab`.

## Already Imported

- candidate bootstrap snapshot
  - each new candidate now starts with a compact scientific situation report
- polled command runner traces
  - command backends now write `traces/live_command.json`
- active backend dashboard surface
  - `docs/big_bang.md` can now show live backend state while a run is in flight
- stronger environment bootstrap for the runner command
  - `build_environment_preflight()` gathers toolchain, dataset readiness, and backend path
  - written to `traces/environment_preflight.json` and embedded in the run trace
- earlier command-completion and stale-process handling
  - `classify_process_behavior()` labels each run as completed_quickly, normal_completion, slow_completion, crashed_early, or stalled
  - stale-process timeout (`HARNESS_LAB_RUNNER_STALE_SECONDS`, default 600s) terminates stuck processes and records a `stalled` outcome
  - classifications are aggregated in hindsight and feed into policy adjustments
- tighter completion discipline
  - `validate_keeper_candidate()` gates keeper candidates through a minimal-change review
  - checks: has_changes, bounded_changes, not_critical_severity, failure_modes_improved
  - rejected keepers are downgraded to dead_end with evidence
  - review artifact written to `outcome/keeper_review.json`
- higher-value use of bounded external review
  - `_run_llm_review()` optionally calls an LLM via the Anthropic SDK
  - configured via `HARNESS_LAB_LLM_REVIEW_MODEL` and `HARNESS_LAB_LLM_REVIEW_API_KEY`
  - falls back to heuristic review if not configured or if the call fails
  - preserves the lab_advice / human_advice split
- command/runtime throughput accounting
  - `compute_throughput_accounting()` tracks wall-clock, polling overhead, and time saved
  - written to `traces/throughput.json` and embedded in the run trace
  - aggregated in hindsight as `throughput_summary`
  - policy reads throughput signals (`efficient_polling`, `low_polling_savings`)
  - budget grants extra follow-ups when >50% of runs complete early
- candidate preflight bundle
  - `build_preflight_bundle()` packages bootstrap snapshot, execution plan, proposal, diagnosis, backend/dataset readiness
  - written to `preflight/bundle.json` before command execution
  - path passed to backend via `HARNESS_LAB_PREFLIGHT_BUNDLE_PATH` env var

## Current Recommendation

All planned imports are now integrated. Focus on:

- running the lab to generate real evidence for the new signals
- watching for stale-process events or keeper rejections in practice
- enabling LLM review when the lab gets repetitive (set `HARNESS_LAB_LLM_REVIEW_MODEL`)
