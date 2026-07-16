# M1 quadratic-parameter residual route cut v1

This directory contains the deterministic certificate for the exhaustive
degree-two parameter stratum of branch 6 at the KoalaBear MCA row
`A=1,116,048`.

The packet proves exact scalarization to a diagonal three-interleaved line,
canonical least-noncontained-coordinate witness coverage, and fixed-support
single-root incidence relative to the declared post-5 residual predicate.  It
does not claim to machine-replay the branch-1--5 masks.  Every current leaf terminates
`UNPAID_TOWER_DEGREE_2`; `U_2`, `U_Q`, and `U_A` remain null.

Replay:

```bash
python3 experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py --check
python3 experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_fp2_residual_route_cut_v1.sage
```

The `F_49` census is a fixed-line Frobenius-closure falsifier only.  It is not
a deployed first-match survivor or a numeric payment.
