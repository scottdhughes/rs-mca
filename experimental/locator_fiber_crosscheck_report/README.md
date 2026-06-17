# Locator-Fiber Cross-Check Report

Status: EXPERIMENTAL

This directory contains a small report tool for comparing locator-fiber sweep
CSV rows against optional Sage cross-check JSON. It is experimental evidence
tooling only. It does not assert Reed-Solomon, list-decoding, MCA, or protocol
safety, and it does not upgrade any theorem status.

The comparison key is:

```text
p,n,k,agreement_size,template
```

The tool compares:

- `supports_checked` versus Sage `scan.supports_tested`
- `fiber_size`
- `nontrivial_locator_constraint`

It reports matched cases, mismatches, Python-only rows, and Sage-only rows.

Example:

```bash
REPORT=experimental/locator_fiber_crosscheck_report/compare_locator_fiber_outputs.py
.venv/bin/python "$REPORT" \
  --python-csv /tmp/locator_fiber_sweep.csv \
  --sage-json /tmp/sage_locator_fiber_selected.json \
  --out-dir /tmp/locator_fiber_crosscheck_report
```
