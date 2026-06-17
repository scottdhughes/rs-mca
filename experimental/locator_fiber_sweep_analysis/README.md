# Locator-Fiber Sweep Analysis

Status: EXPERIMENTAL

This directory contains a local analyzer for locator-fiber sweep CSV outputs.
It is experimental evidence tooling only. It does not assert Reed-Solomon,
list-decoding, MCA, or protocol safety, and it does not upgrade any theorem
status.

The analyzer reads `locator_fiber_sweep.csv` files with the schema exercised in
`test_analyze_locator_fiber_sweep.py` and writes:

- `locator_fiber_sweep_analysis.csv`
- `locator_fiber_sweep_analysis.md`
- `locator_fiber_sweep_analysis.json`

It separates interpolation-floor sanity rows from nontrivial locator-fiber rows,
checks expected sanity baselines, and highlights sparse random nonzero fibers,
monomial nonzero fibers, and quotient-periodic support summaries.

This contribution includes the analyzer, a tiny input fixture, schema-by-test,
and report output. It does not include a canonical sweep generator.

Example:

```bash
ANALYZER=experimental/locator_fiber_sweep_analysis/analyze_locator_fiber_sweep.py
CSV=experimental/locator_fiber_sweep_analysis/examples/tiny_locator_fiber_sweep.csv
.venv/bin/python "$ANALYZER" \
  --csv "$CSV" \
  --out-dir /private/tmp/rs-mca-locator-fiber-analysis \
  --top-fibers 20
```
