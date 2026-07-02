# M1 a327 selected-class quotient nullspace lift

Status: CANDIDATE / EXACT_SOLVE_PENDING / PARTIAL / EXPERIMENTAL.

This packet starts from the selected-class thin exact-lift target in `9fcdb02`
and replaces the explicit received-word formulation by a quotient system in
codeword differences. It remains INTERLEAVED_LIST work only. It is not an MCA row,
not protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Thin selected-class target

The input hypergraph has:

```text
supports = [327,327,327,327,327,327,327]
selected_incidences = 2289
max_pair_count = 194
pair7_counts = [194,194,194,193,194]
```

This target satisfies the Reed-Solomon pair cap `pair_ij <= 255` and keeps all
selected supports exactly at the `a=327` threshold.

## Quotient system

At each coordinate `h`, the selected-class formulation imposes:

```text
P_i(h) = r_h for i in C_h
```

The received value `r_h` can be eliminated locally by choosing an anchor
`a_h in C_h` and imposing:

```text
P_i(h) - P_{a_h}(h) = 0 for i in C_h \ {a_h}.
```

Then quotient out the global diagonal solution by setting:

```text
D_i = P_i - P_1, i = 2,...,7.
```

The quotient system has:

```text
variables = 6*256 = 1536
equations = 2289 - 512 = 1777
matrix_shape = [1777,1536]
```

The equations are exactly the selected-class equalities, and no equality is
imposed between witnesses outside the selected received class.

## Pair-projection criterion

Let `Q` be the solution space of the quotient system over `GF(17^32)`. For
each pair `i<j`, define the pair-projection map

```text
pi_ij: Q -> coeffs(P_i - P_j).
```

In quotient coordinates this projection is one of `D_i`, `D_j`, or
`D_i - D_j`.

If `Q` is nonzero and no `pi_ij` is identically zero, then there exists a
quotient vector giving seven distinct codewords. The bad condition
`P_i = P_j` is a proper linear subspace of `Q` for each pair, and 21 proper
subspaces cannot cover a vector space over `GF(17^32)`.

An explicit candidate still needs to be constructed and checked by Sage.

## Current audit result

The first Sage audit records prefix-rank evidence for row prefixes
`128`, `256`, and `512`. Each prefix is full row rank over `GF(17^32)`.

The full `1777 x 1536` rank/nullspace solve was attempted, but the monolithic
Sage echelonization path exceeded the interactive budget and was interrupted.
The current ledger is therefore a prefix-rank audit, not a full quotient
nullspace lift.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

Run the Sage quotient audit over `GF(17^32)`. If the quotient nullity is
positive, run the pair-projection test. If every pair projection is nonzero,
construct a deterministic quotient vector avoiding all pair-equality
subspaces, define the received word from the selected anchors, and verify
agreement at least `327` for all seven witnesses.
