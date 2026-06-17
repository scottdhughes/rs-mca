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

### 2026-06-17 - Locator-fiber sweep analyzer

- **Agent/model:** Codex / GPT-5.
- **Files added or changed:**
  - `experimental/locator_fiber_sweep_analysis/README.md`
  - `experimental/locator_fiber_sweep_analysis/analyze_locator_fiber_sweep.py`
  - `experimental/locator_fiber_sweep_analysis/examples/tiny_locator_fiber_sweep.csv`
  - `experimental/locator_fiber_sweep_analysis/test_analyze_locator_fiber_sweep.py`
- **Status:** EXPERIMENTAL.
- **What is being added:** A local analyzer for locator-fiber sweep CSV outputs.
  It includes a tiny input fixture, separates interpolation-floor sanity rows
  from nontrivial locator-fiber rows, and reports sparse random nonzero fibers,
  monomial nonzero fibers, and quotient-periodic support summaries.
- **How it is useful:** Supports the locator-fiber toy-case program by turning
  exhaustive scan rows into reviewable experimental frontiers and sanity checks.
- **What to do next:** Run on canonical local sweep packets, add independent
  Sage cross-checks for selected nontrivial rows, and decide after review
  whether the analyzer should be promoted to `scripts/`.
