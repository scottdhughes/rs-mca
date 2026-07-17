# M1 KoalaBear branch-3 rank-nine mask-deficit route cut v1

This directory contains the deterministic certificate for the rank-nine
mask-deficit distribution gate following the actual-core MDS rank ladder.

The packet proves:

1. for one fixed rank-nine complete selector,

   ```text
   delta_eta = j - |E_eta|,
   0 <= delta_eta <= 631578,
   mu_d(delta) = ceil(
       max(1,d_V-j+delta) * C(67480+delta,8) / 9
   );
   ```

2. M2b is exactly

   ```text
   sum_delta h_delta * mu_d(delta) <= C(N_V,9);
   ```

3. M2b plus the currently exported set-pair, pairwise-deficit,
   antichain-size, and complete-union scalar constraints still permits the
   all-zero deficit profile and therefore cannot improve the predecessor's
   coarse rank-nine cap;
4. for any proved cumulative bound `H_D <= T`, the exact largest sufficient
   right side at a fixed cutoff is

   ```text
   T_star = floor(
       ((B_remaining+1)*mu_d(D+1) - C(N_V,9) - 1)
       / (mu_d(D+1)-mu_d(0))
   );
   ```

5. the universal worst corner is `N_V=n,d_V=1`, whose first useful cutoff is

   ```text
   H_18014 <= 17907572507584;
   ```

6. sorted multiple cumulative bounds admit an exact greedy compiler.

The scalar extremizer is not a constructed Reed--Solomon witness.  The packet
does not prove the missing incidence lemma, pay rank nine, move the ledger,
close branch 3, or close the KoalaBear row.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --write
python3 experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --tamper-selftest

python3 -O experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --check
python3 -O experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.sage

python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --tamper-selftest
python3 experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py \
  --tamper-selftest

python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py \
  --check
python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py \
  --tamper q
python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py \
  --tamper ell
python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py \
  --tamper mds
python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py \
  --tamper nonuniform
```

The Sage replay independently checks the deployed integer boundaries and a
tiny `GF(17)` weighted-Vandermonde row-basis model.  It is a control, not a
deployed census or an existence proof for a syndrome-line family.
