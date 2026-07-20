# M31 shortened-flat/projective-hyperplane wall certificate

This directory contains the canonical exact manifest for
`experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md`.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --check
python3 -O experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --check
python3 experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --tamper-selftest
sage experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.sage
```

To print a freshly generated manifest without writing files:

```text
python3 experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py --print-certificate
```

The manifest is fail-closed.  It records an exact arbitrary-center
shortened-flat formulation and two architecture route cuts, while retaining
zero ledger movement and explicitly leaving the prime-field and quartic-field
M31 list rows open.  Every mutation in the self-test is resealed before
validation, so the suite tests semantic guards rather than only the manifest
self-hash.

The manifest also pins the upstream heads and source hashes reused from PRs
#720, #748, #993, and #1000.  The locator bridge is deliberately limited to
the syndrome/Hankel recurrence: the GF(7) regression proves that it is not the
deployed weight--power-sum prefix fiber, so this packet makes no `U_Q`
payment.
