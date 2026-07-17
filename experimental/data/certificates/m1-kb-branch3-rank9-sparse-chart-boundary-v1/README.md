# M1 KoalaBear rank-nine sparse chart-boundary route cut v1

This directory contains the fail-closed certificate for the conditional
sparse tangent and chosen-minor chart-boundary specialization stacked on the
rank-nine syndrome-rank packet.

The predecessor stack was manually integrated into upstream `main` by commit
`48115af63b7178a543db35a631e252eba7e35ba3`.  This migrated replay is stacked
on the schema/one-cut repair packet at
`beb213b6ad7c42d02be7eb09a22c0e1b51d9e18e` (PR #915), which repairs the
integrated predecessor without moving its ledger.

For the one fixed complete affine-rank-nine selector, the packet verifies:

1. the column-far branch keeps the predecessor terminal;
2. challenge-restricted SP3 translates the complementary branch to a sparse
   pair with support union at most `j=981104`;
3. tangent slopes contribute at most `j`;
4. every non-tangent bad slope has a full-row-rank
   `67472 x 981105` Hankel matrix;
5. one maximal minor selected at a non-tangent bad slope has degree at most
   `67472`, so its chart boundary contributes at most `67472` slopes;
6. tangent-first disjointization gives the conditional cap
   `981104 + 67472 = 1048576 = R`;
7. the regular split-locator route remains open, later owner masks remain
   pending, and the shared ledger does not move.

The mathematical terminals are:

```text
NON_CA_RANK9_SYNDROME_REDUCTION_PAID
SPARSE_TANGENT_RANK9_CONDITIONAL_CAP
SPARSE_CHART_BOUNDARY_RANK9_CONDITIONAL_CAP
REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE
```

The second and third names are conditional subcell caps, not unconditional
additions to `U_paid`.  A zero of the chosen minor is a chart boundary, not a
global rank drop.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py \
  --tamper-selftest

# Regeneration is permitted only after the shipped certificate passes.
python3 experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py \
  --write
python3 experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py \
  --check

python3 -O experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py \
  --check
python3 -O experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py \
  --tamper-selftest

HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.sage

python3 experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
  --check
python3 experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py \
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

The Sage companion reconstructs an exact `GF(11)` Reed--Solomon toy in which:

- three tangent bad slopes saturate the toy tangent cap;
- a selected maximal minor vanishes at a non-tangent bad slope while the full
  matrix retains maximal row rank; and
- other non-tangent bad slopes lie on the regular chosen chart.

It is a finite control and guardrail, not a deployed-field census or a proof of
the symbolic lemma.
