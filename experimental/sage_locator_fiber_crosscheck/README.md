# Sage Locator-Fiber Cross-Checks

Status: EXPERIMENTAL

This directory contains optional SageMath cross-checks for tiny locator-fiber
experiments. Sage is not part of the core Python requirements. These checks are
independent verification aids for finite toy cases only.

The script reconstructs the prime-field multiplicative domain in Sage, repeats
support interpolation over `GF(p)`, and reports the same locator-fiber summary
quantities used by the experimental Python sweep generator.

It makes no Reed-Solomon, list-decoding, MCA, or protocol safety assertion, and
it does not upgrade any theorem status.

Run one small case:

```bash
SAGE_CHECK=experimental/sage_locator_fiber_crosscheck/sage_locator_fiber_crosscheck.sage
sage -python "$SAGE_CHECK" \
  --p 5 --n 4 --k 2 --agreement-size 3 --template monomial \
  --json-out /tmp/sage_locator_fiber_p5_monomial.json
```

Run the selected local cross-check set:

```bash
SAGE_CHECK=experimental/sage_locator_fiber_crosscheck/sage_locator_fiber_crosscheck.sage
sage -python "$SAGE_CHECK" \
  --preset selected \
  --json-out /tmp/sage_locator_fiber_selected.json
```
