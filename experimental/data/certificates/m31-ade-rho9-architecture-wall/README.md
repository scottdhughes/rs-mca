# M31 rho-nine ADE architecture wall certificate

This directory contains the generated exact certificate for
`experimental/notes/thresholds/m31_ade_rho9_architecture_wall.md`.

Regenerate and replay from the repository root:

```text
python3 experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --write
python3 experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --check
python3 -O experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --check
python3 experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --tamper-selftest
sage experimental/scripts/verify_m31_ade_rho9_architecture_wall.sage
```

The certificate is intentionally fail-closed.  It records zero ledger
movement, does not construct a constant-weight prefix fiber, and does not
exclude the first residual two-shell row.  The Python replay uses a
best-effort 256 MiB address-space cap; platforms such as macOS that refuse to
lower `RLIMIT_AS` remain safe because the checker is formula-only and never
materializes the large root graph or Gram matrix.
