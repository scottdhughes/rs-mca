# M1 a=327 two-level pairwise divisibility

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a two-level quotient-plus-residual pairwise-divisibility
search for an `a=327` interleaved-list certificate for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` construction audit, not an MCA `N_bad` row, and it does not
claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, or a global upper bound at `a=327`.

## Method

The previous pairwise-divisibility checkpoint tested balanced clique-style
equality patterns. This checkpoint keeps the same reduced rank gate but builds
each pairwise equality set

```text
Z_ij subset H
```

from the quotient map `x -> x^32`. Each `Z_ij` is a two-level set:

```text
Z_ij = quotient_fiber_part_ij union residual_part_ij.
```

The scanner anchors `P_0=0`, writes `D_i=P_i-P_0`, and imposes

```text
D_i - D_j = 0 on Z_ij.
```

After compressing by the anchor zero sets `Z_0i`, it computes the reduced
pairwise-divisibility matrix. The Python scanner uses `GF(12289)` only as a
rank proxy. The retained candidates are independently audited over
`GF(17^32)` with Sage.

## Candidate Families

The scanner generated 48 deterministic two-level specifications across four
families:

```text
seven_fibers_plus_residual
punctured_eight_fiber
common_six_fiber_residual
anchor_relaxed_boundary
```

All 48 satisfy the finite pairwise constraints. The retained exact-audited
set is family-balanced, with two candidates per family.

The first three families put every pair at the boundary:

```text
|Z_ij| = 255 for all 21 pairs.
```

The `anchor_relaxed_boundary` family keeps non-anchor pairs at the boundary
but leaves the six anchor pairs at seven full quotient fibers:

```text
|Z_0i| = 224,     |Z_ij| = 255 for i,j >= 1.
```

This avoids collapsing the compressed dimension to one variable per witness
for the anchor-relaxed rows.

## Result

The eight retained candidates were exact-audited over `GF(17^32)`.

```text
candidate                         compressed variables   exact rank   nullity
anchor_relaxed_boundary_11        192                    192          0
anchor_relaxed_boundary_10        192                    192          0
common_six_fiber_residual_11      6                      6            0
common_six_fiber_residual_10      6                      6            0
punctured_eight_fiber_11          6                      6            0
punctured_eight_fiber_10          6                      6            0
seven_fibers_plus_residual_11     6                      6            0
seven_fibers_plus_residual_10     6                      6            0
```

Thus every retained two-level pairwise-divisibility system has full reduced
rank over the actual field and no non-diagonal null-vector. No `a=327`
interleaved-list certificate is produced.

## Status Ledger

ROUTE_CUT_TESTED_CANDIDATES:

- 48 two-level quotient-plus-residual pairwise designs generated;
- all 48 satisfy the pairwise design constraints;
- 16 entered structural/rank screening;
- 8 retained candidates were exact-audited over `GF(17^32)`;
- all 8 exact reduced rank gates are full rank;
- no retained candidate has positive nullity;
- no `a=327` certificate appears;
- no tested candidate improves PR #133.

PARTIAL / OPEN:

- larger two-level pairwise-divisibility systems;
- designs with anchor pairs below 224 or non-anchor pairs below 255;
- non-diagonal nullspace extraction if a positive-nullity system appears;
- value-class max-min verification after positive nullity;
- symbolic reduced-rank obstruction for quotient-residual classes;
- global `Lambda_mu(C,327) <= 6`.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- global two-level pairwise-divisibility obstruction;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- `PROOF_RECORD` lower bound without Sage extraction;
- exact `Lambda_mu`;
- exact `delta*_C`;
- global `Lambda_mu(C,327) <= 6`.

## Next Step

This checkpoint shows that the first quotient-fiber boundary designs are still
full-rank, even when pairwise equality loci are quotient-structured and
residual-defected. If the next step stays constructive, it should loosen the
anchor and non-anchor equality sizes instead of pushing every pair to the
boundary. If that also stays full-rank, the better move is a symbolic
obstruction theorem for this quotient-residual reduced rank class rather than
more hand-generated candidates.
