# M1 KoalaBear branch-3 rank-nine syndrome rank reduction v1

This directory contains the fail-closed certificate for the deterministic
rank-nine syndrome-rank route cut.

For the one fixed rank-minimizing complete selector, the packet verifies:

1. predecessor transversality and `|Gamma| > 15` make the selected syndrome
   line nondegenerate;
2. affine-difference rank `s=9` therefore gives witness-column rank `t=10`;
3. on an original received pair that is column-far at agreement `A`, exact
   deterministic rank reduction gives

   ```text
   |Gamma| <= floor((j+1)*(R+1)^8/(R+1-j)^8)
           = 3337935545766696
           < B_remaining;
   ```

4. an original pair that is not column-far routes, through challenge-restricted
   exact sparsification, to the open sparse mutual numerator.

The only mathematical terminals are:

```text
NON_CA_RANK9_SYNDROME_REDUCTION_PAID
CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA
```

The second terminal is not a paid owner.  This packet moves no ledger value
and does not close rank nine, branch 3, or the KoalaBear row.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
  --write
python3 experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
  --tamper-selftest

python3 -O experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
  --check
python3 -O experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.sage

python3 experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --tamper-selftest
python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --tamper-selftest
```

The Sage companion independently checks the exact deployed arithmetic, an
exhaustive `GF(7)` rank-reduction control, and the guardrail that a full
low-weight syndrome line need not have one common support.  It is not a
deployed-field census or a substitute for the symbolic proof in the note.
