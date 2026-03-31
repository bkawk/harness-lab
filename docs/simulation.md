# Simulation

`harness-lab` still needs a lightweight way to make the loop feel alive before a real benchmark runner exists.

The simulation layer provides a deterministic stand-in:

- it reads proposal and diagnosis context
- it emits plausible benchmark and audit scores
- it assigns an outcome label
- it can optionally write that outcome back into the candidate workspace

This is not a substitute for a real runner.
It is a bridge that lets the local loop behave like a system instead of a collection of disconnected CLIs.

## Initial CLI

Preview a simulated outcome:

```bash
PYTHONPATH=src python3 scripts/simulate_outcome.py cand_0002
```

Write the simulated outcome:

```bash
PYTHONPATH=src python3 scripts/simulate_outcome.py cand_0002 --write
```
