# Loop

`harness-lab` is meant to feel alive: each candidate should be able to move through a repeatable local research loop instead of existing as a disconnected JSON bundle.

Before the loop matters, the harness needs its data to be ready in a repeatable way. The repo-native data entrypoint is:

```bash
PYTHONPATH=src python3 scripts/ensure_abc_ready.py \
  abc_raw_v1 abc_boundary512
```

That keeps the future loop grounded in one stable assumption: the prepared local ABC dataset either already exists or can be rebuilt reproducibly from the registered source bundle.

The highest-level orchestration entrypoint is:

```bash
PYTHONPATH=src python3 scripts/run_lab.py \
  --source-dataset-id abc_raw_v1 \
  --prepared-dataset-id abc_boundary512
```

That single command now does:

```text
ensure_abc_ready
-> create a seed baseline candidate if none exists yet
-> choose the next candidate id
-> draft proposal
-> capture harness source snapshot and parent diff
-> plan execution
-> optionally simulate and finalize outcome
-> reconcile diagnosis
-> refresh memory and parent synthesis
-> refresh hindsight
-> optionally publish tracked evolution
```

The long-running supervisor is:

```bash
PYTHONPATH=src python3 scripts/big_bang.py \
  --source-dataset-id abc_raw_v1 \
  --prepared-dataset-id abc_boundary512 \
  --cycles 0
```

`big-bang` is meant to be the moment the lab becomes continuously alive:

- ensure data readiness
- create the genesis seed if needed
- advance the next candidate
- rewrite a tracked status page under `docs/`
- publish the new lab state to GitHub

While a backend run is still in flight, `docs/big_bang.md` now also shows an `Active Backend` section sourced from the candidate's live runner trace. That makes the repo dashboard reflect in-progress science work instead of only completed cycles.

The first time `big-bang` enters `running`, the lab records `vital_spark_at` in `artifacts/memory/big_bang_state.json` and surfaces it in `docs/big_bang.md`.

For a real Ubuntu-style long-running process, use the control wrapper:

```bash
scripts/big_bang_ctl.sh start
scripts/big_bang_ctl.sh status
scripts/big_bang_ctl.sh stop
```

That wrapper keeps a PID file, a log file, and a small control record under `artifacts/memory/`, and it reports health from both process liveness and `big_bang_state.json` heartbeat freshness.

The first loop command advances one candidate through:

```text
proposal drafting
-> hardware refresh
-> source snapshot and patch capture
-> execution planning
-> backend trace capture
-> optional outcome writeback
-> diagnosis reconciliation
-> memory refresh
-> parent synthesis refresh
-> hindsight refresh
```

## Initial CLI

Draft and plan a candidate:

```bash
PYTHONPATH=src python3 scripts/advance_loop.py cand_0002
```

Run the full local loop with a simulated outcome:

```bash
PYTHONPATH=src python3 scripts/advance_loop.py cand_0002 \
  --repo-dir . \
  --finalize-outcome \
  --simulate-outcome \
  --runner-backend simulated
```
