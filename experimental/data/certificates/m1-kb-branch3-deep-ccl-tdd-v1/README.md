# M1 KoalaBear branch-3 deep / CCL / TDD v1

This directory contains the deterministic certificate for two exact
KoalaBear branch-3 results at `A=1,116,048`.

1. The already-paid branch-2 rank-drop owner extends to every branch-3 slope
   admitting an actual noncontained witness of weight at most
   `floor((n-k)/3)=349525`.  The combined cap is `349526`, so the new ledger
   delta is `349526-67472=282054`.
2. For any selected surviving heavier family, the integrated global-carrier
   owner is applied first.  If its union has excess above `10`, the family
   either has size at most `15` or has a nonzero triple-distance defect whose
   three actual supports have union at least `1048577`.

The certificate banks only the deep-owner extension.  The terminal
`UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT` remains open.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --write
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --tamper-selftest

python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --tamper-selftest
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --tamper-selftest
```

No Sage or elimination replay is load-bearing.  The deployed result is a
symbolic theorem-interface audit plus exact big-integer arithmetic.  The
verifier includes exact finite-field CCL and TDD controls.
