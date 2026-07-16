# M1 KoalaBear branch-2 Hankel pivot adapter v1

This directory contains the deterministic certificate for the field-native
finite-pivot half of KoalaBear branch 2 at `A=1,116,048`.

The packet imports the Paper-D support-locator syndrome recurrence, deploys
the canonical implicit Hankel adapter, proves that pivot failure has no actual
finite support-wise noncontained witnesses, and records an exact
`F_7 subset F_(7^2) subset F_(7^6)` two-support/two-root route cut.

It does **not** define the rank-drop policy, identify the Hankel pivot with the
legacy cyclotomic `red_p(B_0(S))`, assign a branch-2 charge, or change
`U_2`, `U_Q`, or `U_A`.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.sage

python3 experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py --check
python3 experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py --tamper-selftest
python3 experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py --check
python3 experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py --tamper-selftest
```

The Python verifier performs a deterministic certificate rebuild and an exact
`F_17` interpolation-versus-Hankel census.  The Sage replay independently
checks the extension-field route cut and both least-pivot charts.
