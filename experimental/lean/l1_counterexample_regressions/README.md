# L1 counterexample regressions

This stdlib-only Lean package locks the spectrum arithmetic of the six
counterexamples in
`experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json`.

It checks the exact `E3`, residual `T`, active-fiber count, pair cap,
master identity, falsifier signature, peel invariance, and chart separation.
The independent Python verifier remains responsible for reconstructing each
spectrum from its raw finite-field `Gamma` vector.

Build and verify with:

```sh
lake build
python3 ../../scripts/verify_l1_e3_law_refuted.py
python3 ../../scripts/verify_l1_e3_law_refuted.py --tamper-selftest
```

A spectrum by itself is not asserted to be realizable. No general `E3`
ceiling, finite-field reconstruction theorem, or asymptotic claim is made.
