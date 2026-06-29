# M1 a=327 pairwise-divisibility null-vector system

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records the first explicit pairwise-divisibility null-vector system
audit for an `a=327` interleaved-list certificate for

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

Earlier null-vector-first searches chose difference polynomials

```text
P_0 = 0,    D_i = P_i - P_0,    i=1,...,6
```

and then asked whether useful equality classes emerged. This checkpoint
reverses that direction for a finite set of structured designs. It first
chooses pairwise equality sets

```text
Z_ij subset H
```

and forces

```text
D_i(h) = D_j(h)       for h in Z_ij.
```

Equivalently, `D_i-D_j` is divisible by the locator polynomial of `Z_ij`.
The rank gate anchors `P_0=0`, compresses each `D_i` by the forced zero set
`Z_0i`, and computes the reduced linear system for the remaining pairwise
equalities.

The Python scanner uses `GF(12289)` only as a rank proxy and structural
screen. The exact retained candidates are independently audited in Sage over
`GF(17^32)`.

## Search Layer

The scanner generated 48 deterministic pairwise-divisibility specifications
across:

```text
balanced_clique_blocks
quotient_fiber_pairwise_blocks
pair_boundary_design
mixed_clique_design
```

Of these, 19 met the hard design constraints:

```text
min witness equality incidence >= 327
max pair equality size <= 255
anchor pair equality sizes < 256
```

The first rank-screen retained 12 structurally strongest designs, then kept
the top 6 after the `GF(12289)` reduced-rank proxy. All retained candidates
came from the `balanced_clique_blocks` family.

## Result

The six retained candidates were exact-audited over `GF(17^32)`.

```text
candidate                     compressed variables   exact rank   nullity
balanced_clique_m2_o1         179                    179          0
balanced_clique_m6_o1         205                    205          0
balanced_clique_m5_o1         205                    205          0
balanced_clique_m2_o0         206                    206          0
balanced_clique_m6_o0         214                    214          0
balanced_clique_m1_o0         217                    217          0
```

Thus each retained pairwise-divisibility system has full reduced rank over the
actual field and no non-diagonal null-vector. No `a=327` interleaved-list
certificate is produced.

## Status Ledger

ROUTE_CUT_TESTED_CANDIDATES:

- 48 pairwise-divisibility specifications generated;
- 19 satisfy the finite design constraints;
- 12 were structurally screened before rank feedback;
- 6 retained candidates were exact-audited over `GF(17^32)`;
- all 6 exact reduced rank gates are full rank;
- no retained candidate has positive nullity;
- no `a=327` certificate appears;
- no tested candidate improves PR #133.

PARTIAL / OPEN:

- larger pairwise-divisibility systems;
- stronger quotient-fiber pairwise designs;
- non-diagonal nullspace extraction if a positive-nullity system appears;
- value-class max-min verification after positive nullity;
- two-level quotient plus residual differences;
- global `Lambda_mu(C,327) <= 6`.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- global pairwise-divisibility obstruction;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- `PROOF_RECORD` lower bound without Sage extraction;
- exact `Lambda_mu`;
- exact `delta*_C`;
- global `Lambda_mu(C,327) <= 6`.

## Next Step

The first pairwise-divisibility layer shows that balanced clique-style
equality designs remain full-rank even when pairwise equality loci are chosen
jointly. The next useful move is not to treat this as a global obstruction.
Either enlarge the pairwise-divisibility generator toward quotient-fiber
boundary designs that survive the pair caps, or switch to a constructive
two-level quotient-plus-residual difference family where the pairwise equality
loci are built from polynomial divisibility rather than combinatorial clique
patterns alone.
