# M1 a327 connected-subtree selected-class construction

Status: CONSTRUCTION_FAIL / CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION /
PARTIAL / EXPERIMENTAL.

This packet tests the connected-subtree selected-class construction principle
for the M1 `a=327` interleaved-list lane. It remains INTERLEAVED_LIST work
only. It is not an MCA row, not protocol soundness, not exact `Lambda_mu`, and
not a global `Lambda_mu(C,327) <= 6` claim.

## Proposed construction

Choose a tree `T` on the seven witnesses. At each coordinate `h`, choose a
selected class `C_h` that is connected in `T`. For each tree edge `e`, define

```text
S_e = {h : both endpoints of e lie in C_h}.
```

If `|S_e| <= 255`, one can form an edge vanishing polynomial

```text
Z_e(X) = product_{h in S_e}(X-h)
```

of degree `<256`, choose edge differences `E_e = a_e Z_e`, and define witness
polynomials by path sums from a root. Connectedness makes all selected-class
equalities automatic.

## Counting obstruction

The construction cannot satisfy the `a=327` support and RS pair-cap constraints
on any seven-node tree.

For every connected selected class `C_h`, the number of tree edges inside
`C_h` is `|C_h|-1`. Therefore:

```text
sum_e |S_e| = sum_h (|C_h|-1)
           = selected_incidence_count - 512.
```

The support target requires:

```text
selected_incidence_count >= 7*327 = 2289,
sum_e |S_e| >= 2289 - 512 = 1777.
```

But the RS pair cap requires each tree edge count to be at most `255`. A
seven-node tree has six edges, hence:

```text
sum_e |S_e| <= 6*255 = 1530.
```

This gives the contradiction:

```text
1777 > 1530.
```

So connected-subtree selected classes cannot reach support `327` for all seven
witnesses while keeping all tree-edge pair counts at most `255`.

## Scanner result

The scanner also tested the proposed witness trees:

```text
path_1237456
path_1234765
balanced_T
two_pair_spine
```

All four count MILPs were infeasible. This is consistent with the general
tree-edge incidence obstruction above.

## Non-claims

This packet does not claim:

- no `a=327` witness exists;
- no RS-feasible selected-class hypergraph can lift;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

Do not pursue connected-subtree selected classes as a construction route. The
next viable abstraction must allow selected classes whose equality graph is not
a connected subtree of a six-edge witness tree, while still controlling
cycle-rank. One possible direction is a low-treewidth or bounded-cycle
incidence design that has enough edge capacity to support `7*327` selected
incidences without forcing pair counts above `255`.
