# Hardware Awareness

`harness-lab` should notice the machine it is running on and carry that context into planning and execution.

Why:

- available hardware changes over time
- the same candidate may deserve different evaluation policies on different machines
- a living lab should know when it is on a constrained laptop versus a roomier Linux box

The current profile artifact lives at:

```text
artifacts/memory/hardware_profile.json
```

## What It Captures

- hostname
- platform and release
- machine architecture
- CPU count
- load average
- estimated physical memory
- environment hint

## What It Influences Now

Hardware is no longer just recorded.

It now influences:

- parent candidate ranking
- proposal guardrails
- execution-plan wording
- outcome evidence

Examples:

- a constrained local environment can down-rank heavy dead-end parent lines
- a local macOS environment can inject compact-experiment guardrails into drafted proposals

## Initial CLI

Refresh the profile with:

```bash
PYTHONPATH=src python3 scripts/refresh_hardware.py
```
