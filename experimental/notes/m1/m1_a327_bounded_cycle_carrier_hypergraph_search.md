# M1 a327 bounded-cycle carrier hypergraph search

Status: CONSTRUCTION_FAIL / BOUNDED_CYCLE_COUNT_INFEASIBLE / PARTIAL /
EXPERIMENTAL for the first-pass graph set.

This packet moves past the connected-subtree construction after the tree count
obstruction. It remains INTERLEAVED_LIST work only. It is not an MCA row, not
protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Source obstruction

The connected-subtree construction on a seven-witness tree cannot meet the
`a=327` support target and the RS pair cap simultaneously. The support target
requires

```text
7 * 327 = 2289
```

selected witness incidences. Any connected selected class on a tree uses
`|C_h|-1` tree edges, so the tree-edge incidence load is at least

```text
2289 - 512 = 1777.
```

A seven-vertex tree has only six edge carriers, and each carrier edge is capped
at `255` by the Reed-Solomon pairwise root bound. Thus a tree supplies at most

```text
6 * 255 = 1530
```

edge incidences. The deficit is `247`. Therefore any carrier construction of
this type needs at least

```text
ceil(1777 / 255) = 7
```

edge carriers.

## Bounded-cycle carrier model

The new model uses a carrier graph `G` on the seven witnesses with `7`, `8`, or
`9` edges. At each coordinate `h`, it chooses:

- a selected class `C_h`;
- a spanning carrier edge set `T_h` inside `G[C_h]`.

For each carrier edge `e`, define the edge-load set

```text
S_e = {h : e is used in T_h}.
```

The scanner enforces:

```text
support_i >= 327
pair_ij <= 255
edge_load_e <= 255
pair_i7 >= 142 for i=1,...,5
```

The selected classes are still received-word classes, not full value-class
partitions. Witnesses outside `C_h` are not constrained at coordinate `h`.

## First-pass result

The scanner tested nine carrier graphs with `7`, `8`, and `9` edges:

```text
m7_cycle_12347_tail_56
m7_cycle_1475_spine_1236
m7_cycle_237_path_1456
m8_two_triangles_sharing_7
m8_square_1457_triangle_237
m8_b47_robust
m9_low_cycle_robust
m9_dense_7_hub
m9_b47_b57_robust
```

All nine count MILPs were infeasible under the simultaneous support, pair-cap,
pair-7 guard, and edge-load constraints. Therefore this packet did not run a
nontrivial exact edge-divisibility lift. This is a first-pass obstruction for
the named graph families, not a global theorem for all carrier graphs with
`7`-`9` edges.

## Exact edge-divisibility lift

For a carrier edge `e=(u,v)`, the exact lift uses

```text
Z_e(X) = product_{h in S_e} (X-h)
P_v(X)-P_u(X) = Z_e(X) Q_e(X)
deg Q_e < 256 - |S_e|.
```

Because the carrier graph may have cycles, the Sage audit imposes cycle
constraints:

```text
sum_cycle +/- Z_e Q_e = 0
```

as polynomial identities. These cycle constraints make path sums well-defined,
so witness codewords can be reconstructed from edge differences.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

The next constructive step is either a wider carrier-graph generator or a
relaxed bounded-cycle model that allows more carrier edges while still keeping
the exact edge-divisibility lift small. A board-moving result would still
require Sage to verify seven distinct degree-`<256` codewords over `GF(17^32)`,
one received word on the `512`-point subgroup `H`, and agreement at least `327`
for all seven witnesses with `mca_counted=false`.
