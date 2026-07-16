# KoalaBear MCA 1116048 base-slope universe v2

This certificate banks the global-once bound `p` for the residual finite
slopes in the base field `F_p`.  The MCA numerator counts distinct slopes, so
no SPI chart adapter is needed for this branch.

The packet replaces the predecessor `t*p` generated-collision charge.  It
does not add the two charges, bound slopes in `F_(p^6) \ F_p`, or prove the
KoalaBear row safe.

Replay with:

```bash
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --tamper-selftest
```

The certificate content-binds the distinct-slope definition, fixed-support
slope injection, first-match disjointization, predecessor packet, proof note,
and verifier.
