# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, or certificate
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-06-17 - Locator-fiber sweep generator

- **Agent/model:** Codex / GPT-5.
- **Files added or changed:**
  - `experimental/locator_fiber_sweep/README.md`
  - `experimental/locator_fiber_sweep/run_locator_fiber_sweep.py`
  - `experimental/locator_fiber_sweep/test_run_locator_fiber_sweep.py`
- **Status:** EXPERIMENTAL.
- **What is being added:** A tiny standard-library locator-fiber sweep
  generator for prime-field toy cases. It exhaustively enumerates agreement
  supports, writes per-run JSON reports, and emits a `locator_fiber_sweep.csv`
  table suitable for downstream experimental analysis.
- **How it is useful:** Supports the locator-fiber toy-case program by creating
  reproducible CSV/JSON evidence without editing the main papers or asserting
  Reed-Solomon, list-decoding, MCA, or protocol safety.
- **What to do next:** Compare the generated CSV with the locator-fiber sweep
  analyzer, add optional Sage cross-checks for selected nontrivial rows, and
  decide after review whether any part should be promoted to `scripts/`.
