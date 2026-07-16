# M1 KoalaBear branch-3 TDD excess route cut v1

This directory contains the deterministic certificate for the exact
triple-distance-defect (TDD) route cut following the KoalaBear branch-3
deep-owner packet.

The packet proves:

1. for a TDD triple union of size `R+1+e`,
   `Delta=M_U*Q` with `deg(Q)<=e`, shortened dimension `e+1`, and silent
   shell size at most `e`;
2. minimizing affine rank over all complete actual-witness selectors is a
   safe intrinsic contract, and on a minimizing selector the affine rank is
   exactly one plus the span rank of the fixed-anchor TDD residual codewords;
3. after applying the global carrier existentially over selectors, the
   predecessor theorem regenerates a TDD on the rank-minimizing selector;
4. a basis of those residuals plus two anchor supports recovers that
   selector's complete union;
5. intrinsic complete-selector affine rank at most three has cap
   `C(j+3,3)=157397034144292985`, which fits the remaining budget;
6. low local TDD excess alone does not force the displayed TDD supports
   themselves to have pairwise common-GCD or cyclic-shift symmetry; and
7. raw support-union or `(U,[Q])` enumeration is not a valid payment.

No charge is banked.  Without an intrinsic selector certificate, the
executable terminal is
`UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED`.  The mathematical
primitive complement is
`UNPAID_PRIMITIVE_INTRINSIC_RANK3_TDD_SPREAD`; its first unresolved
intrinsic-rank stratum is represented by five actual slopes, three independent
residual codewords, and minimum complete-selector affine rank four.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py --write
python3 experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.sage

python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py \
  --tamper-selftest
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py \
  --check
python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py \
  --check
python3 experimental/scripts/verify_all_lineray_affine_core.py --check
```

The Sage replay is an independent `GF(17)` control.  It is not a deployed
field census and is not used to promote numerical evidence into proof.
