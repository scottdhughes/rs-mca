# M31 Chebyshev global-separator certificate

This directory contains the canonical manifest for
`experimental/notes/thresholds/m31_chebyshev_global_separator.md`.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_chebyshev_global_separator.py --check
python3 -O experimental/scripts/verify_m31_chebyshev_global_separator.py --check
python3 experimental/scripts/verify_m31_chebyshev_global_separator.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_chebyshev_global_separator.py --tamper-selftest
sage experimental/scripts/verify_m31_chebyshev_global_separator.sage
```

To print a freshly generated manifest without writing files:

```text
python3 experimental/scripts/verify_m31_chebyshev_global_separator.py --print-certificate
```

The manifest pins three exact results: the `C2` projective/monomial
stabilizer of the standard-position M31 Chebyshev domain, the literal
pairwise-survivor/rank-16 boundary, and a nonzero `132 x 132` quotient
Macaulay determinant that rejects one declared complete-`T_1024`-fibre
embedding of four supports from the predecessor's local binary model.

The scope guard is load-bearing.  The certificate does not claim that every
arbitrary coordinate-pair embedding has the same determinant, does not close
the M31 list row, and leaves `U_Q`, `U_A`, and ledger movement unchanged.
The 28 semantic mutations are resealed before validation; two additional raw
corruptions exercise the certificate self-hash failure path.
