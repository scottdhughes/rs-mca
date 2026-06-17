# Locator-Fiber Sweep

Status: EXPERIMENTAL

This directory contains a tiny prime-field locator-fiber sweep generator. It is
experimental evidence tooling only. It does not assert Reed-Solomon,
list-decoding, MCA, or protocol safety, and it does not upgrade any theorem
status.

The generator exhaustively checks tiny agreement-support fibers over prime
fields. It writes:

- per-run JSON reports
- `locator_fiber_sweep.csv`
- `locator_fiber_sweep.md`

The CSV output is shaped for downstream analysis by locator-fiber sweep
analyzers. Rows with `agreement_size <= k` are interpolation-floor sanity rows;
nontrivial locator-fiber constraints begin at `agreement_size > k`.

This contribution is intentionally small and standard-library only.
Use a fresh output directory for each run; the script does not delete stale files
from previous experiments.

Example:

```bash
SWEEP=experimental/locator_fiber_sweep/run_locator_fiber_sweep.py
.venv/bin/python "$SWEEP" \
  --out-dir /private/tmp/rs-mca-locator-fiber-sweep \
  --p 5 \
  --k 2 \
  --agreement-size 2 \
  --agreement-size 3 \
  --template zero \
  --template monomial \
  --template random \
  --seed 0 \
  --max-witnesses 2
```
