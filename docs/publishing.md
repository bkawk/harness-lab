# Publishing

`harness-lab` can publish its own tracked evolution to GitHub in a controlled way.

That means the repo itself can become the progress dashboard, instead of relying on a separate monitor app.

This is intentionally limited to tracked repository paths:

- `README.md`
- `docs/`
- `scripts/`
- `src/`
- `pyproject.toml`

It does **not** blindly add ignored runtime artifacts.

## Why This Matters

The lab should be able to preserve meaningful structural evolution:

- new schemas
- new planning logic
- new synthesis logic
- new tooling
- tracked status pages like `docs/big_bang.md`

without turning the repo into a dump of runtime output.

## Initial CLI

```bash
PYTHONPATH=src python3 scripts/publish_lab.py --message "Add candidate replay suppression"
```

This will:

1. stage only the tracked source/docs paths
2. create a commit if those paths changed
3. push the commit to `origin/main`

The long-running `big-bang` supervisor uses the same publishing mechanism after rewriting the tracked lab dashboard page.
