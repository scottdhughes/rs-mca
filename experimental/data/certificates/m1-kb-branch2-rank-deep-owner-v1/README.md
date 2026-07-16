# M1 KoalaBear branch-2 rank/deep owner v1

This directory contains the deterministic certificate for the field-native
rank-drop half of KoalaBear branch 2 at `A=1,116,048`.

For an actual MCA-bad incidence, the packet proves

```text
rank_F M_A(gamma) = min(t, actual error weight).
```

Thus ambient row-rank drop implies error weight at most `t-1`.  Enlarging the
same witness to its full agreement set makes the slope MCA-bad at agreement
`n-t+1`, where Paper D's deep theorem gives the sharp global charge

```text
t = 67,472.
```

The proved set is a safe rank-drop envelope.  The literal first-match rank
cell first subtracts branch 1 and is therefore a subset of that envelope, so
the same charge pays it without changing first-match order.

Together with the predecessor's empty finite pivot-failure locus, this closes
deployed branch 2.  The legacy cyclotomic pivot bridge is marked
`RETIRED_NOT_REQUIRED_FOR_DEPLOYED_BRANCH2`; it is not claimed equivalent to
the field-native pivot.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.sage

python3 experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_kb_branch2_hankel_pivot_adapter_v1.sage

python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --tamper-selftest
python3 experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py --check
python3 experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py --tamper-selftest
```

The exact `F_7` control realizes three branch-2 slopes at toy depth `t=3`,
checks the padded-co-support factorization, lifts the same witnesses to the
deep agreement, and verifies that a contained pair can have raw rank drop at
every slope while contributing no MCA-bad slope.

The complete row remains open: branch 3 onward and `U_2`, `U_Q`, `U_A` are
not paid by this packet.
