# Locator-Fiber Cross-Check Report

Status: EXPERIMENTAL

This directory contains a small report tool for comparing locator-fiber sweep
CSV rows against optional Sage cross-check JSON. It is experimental evidence
tooling only. It does not assert Reed-Solomon, list-decoding, MCA, or protocol
safety, and it does not upgrade any theorem status.

The comparison key is:

```text
p,n,k,agreement_size,template,seed
```

The `seed` component is active for `template=random`; non-random templates
normalize it to `null` so optional producer defaults do not create false
case splits.

The tool compares:

- `supports_checked` versus Sage `scan.supports_tested`
- `fiber_size`
- `nontrivial_locator_constraint`

It reports matched cases, mismatches, Python-only rows, and Sage-only rows.

Example:

```bash
REPORT=experimental/locator_fiber_crosscheck_report/compare_locator_fiber_outputs.py
EXAMPLES=experimental/locator_fiber_crosscheck_report/examples
.venv/bin/python "$REPORT" \
  --python-csv "$EXAMPLES/locator_fiber_sweep_p5.csv" \
  --sage-json "$EXAMPLES/sage_locator_fiber_p5_monomial.json" \
  --sage-json "$EXAMPLES/sage_locator_fiber_p5_zero.json" \
  --out-dir /tmp/locator_fiber_crosscheck_report \
  --fail-on-mismatch \
  --fail-on-unmatched
```

Pass `--sage-json` more than once to combine separate per-case or per-batch
Sage outputs. Duplicate Sage cases across inputs are rejected.

Use `--fail-on-mismatch` when the report should act as a check and exit
nonzero if any matched Python/Sage case disagrees.

Use `--fail-on-unmatched` when every Python row is expected to have a Sage
counterpart and every Sage row is expected to have a Python counterpart.
