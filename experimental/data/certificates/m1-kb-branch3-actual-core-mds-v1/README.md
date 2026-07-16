# M1 KoalaBear branch-3 actual-core MDS rank ladder v1

This directory contains the deterministic certificate for the actual-core MDS
multiplicity splice following the KoalaBear branch-3 TDD intrinsic-rank packet.

The packet proves, under the predecessor's literal complete-selector contract:

1. the basis carrier is the complete support union of one rank-minimizing
   selector;
2. restriction to that carrier gives an `[R+nu,nu,R+1]` MDS kernel;
3. the selected affine core has dimension `s` and kernel part `r=s-1`;
4. every complete zero mask has size at least `nu+67472`;
5. the imported actual-core basis-multiplicity theorem gives

   ```text
   mu_s = ceil(C(67472+s-1,s-1)/s),
   |Gamma| <= floor(C(2097152,s)/mu_s);
   ```

6. the exact caps fit the remaining KoalaBear budget for intrinsic ranks four
   through eight; and
7. rank nine is paid outside an exact coarse-uniform
   carrier-size/extension-factor failure region; larger actual masks and the
   theorem's nonuniform sum may pay points inside that region.

The rank caps are mutually exclusive global terminals for the one complete
retained family.  They are not summed and are not charged per triple or
subfamily.  No unconditional ledger movement, complete rank-nine payment,
branch-3 closure, row closure, or deployed selector census is claimed.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py --write
python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --tamper-selftest

python3 -O experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --check
python3 -O experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.sage

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

The Sage replay is an independent `GF(17)` MDS row-basis control.  It does not
enumerate the deployed field and does not replace the imported proof.
