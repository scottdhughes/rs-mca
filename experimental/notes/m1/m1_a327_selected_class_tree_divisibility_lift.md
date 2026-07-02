# M1 a327 selected-class tree-divisibility lift

Status: EXACT_EXTRACTION_NO_A327 / TREE_DIVISIBILITY_NULLITY_ZERO / PARTIAL / EXPERIMENTAL.

This packet starts from the selected-class quotient target in `016f04d` and
uses Reed-Solomon root-polynomial divisibility to replace the raw
`1777 x 1536` quotient matrix by smaller tree-divisibility systems.

It remains INTERLEAVED_LIST work only. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Input target

The input selected-class hypergraph has:

```text
supports = [327,327,327,327,327,327,327]
selected_incidences = 2289
max_pair_count = 194
pair7_counts = [194,194,194,193,194]
```

The pair cap `|S_ij| <= 255` holds for every pair, so every pair difference has
a nonnegative quotient degree.

## Divisibility model

For each pair `i,j`, define

```text
S_ij = {h in H : i and j are in the selected class C_h}
Z_ij(X) = product_{h in S_ij} (X - h).
```

The selected-class quotient equations require `P_i - P_j` to vanish on `S_ij`.
Because all codewords have degree `<256`, this is equivalent to

```text
P_i - P_j = Z_ij Q_ij,
deg Q_ij < 256 - |S_ij|.
```

Choose a maximum-weight spanning tree `T` on the seven witnesses and root it at
`1`. For each tree edge `e=(u,v)`, introduce a tree variable

```text
E_e = P_v - P_u = Z_e Q_e.
```

Every non-tree pair difference is then the signed sum of the tree edge
polynomials along the tree path. The non-tree constraints impose that this path
sum vanishes on the corresponding `S_ij`.

## Exact equivalence

The tree-divisibility system is equivalent to the original selected-class
quotient system:

- any quotient solution gives tree-edge differences divisible by the tree-edge
  `Z_ij`;
- any tree-divisibility solution reconstructs `P_1=0` and all other `P_i` by
  summing tree-edge differences along root paths;
- the non-tree equations enforce all remaining selected-class pair equalities.

The pair-projection test is unchanged: after computing the tree solution space,
test whether any pair difference is forced to be zero on the entire space. If no
pair is forced equal, a deterministic combination of basis vectors should yield
seven distinct codewords.

## Exact audit result

The best recorded tree is `balanced_tree`:

```text
edges = [[1,2],[2,3],[3,4],[4,5],[4,6],[6,7]]
matrix_shape = [2874,372]
rank = 372
nullity = 0
failure = TREE_DIVISIBILITY_NULLITY_ZERO
```

Two alternate tree choices were also checked without changing the conclusion:

```text
max_weight_tree: matrix_shape = [2874,372], rank = 372, nullity = 0
pair7_heavy_tree: matrix_shape = [2875,373], rank = 373, nullity = 0
```

This is a local exact negative for the `9fcdb02` thin selected-class target.
It does not rule out other RS-feasible selected-class hypergraphs.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

Run the Sage tree-divisibility audit over `GF(17^32)`. A board-moving result
requires an explicit Sage-verified candidate with seven distinct degree-`<256`
codewords, one received word on `H`, and agreement at least `327` for all seven
witnesses.
