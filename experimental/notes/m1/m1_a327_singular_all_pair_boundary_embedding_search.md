# M1 a327 singular all-pair-boundary embedding search

Status: ROUTE_CUT_TESTED_EMBEDDINGS / PARTIAL / EXPERIMENTAL

This note records a placement search for the all-pair-boundary value-class
incidence multiset over

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` audit packet, not an MCA `N_bad` row, and it does not claim
protocol soundness, ordinary list decoding beyond the stated predicate, exact
`Lambda_mu`, exact `delta*_C`, an `a=327` certificate, or a global upper bound
at `a=327`.

## Starting Point

The previous MILP incidence search found a value-class membership multiset with

```text
|S_i| = 327 for every i,
|S_i cap S_j| = 255 for every pair i<j.
```

That all-pair-boundary profile has membership histogram:

```text
size 1: 110
size 2: 45
size 3: 22
size 4: 21
size 5: 78
size 6: 103
size 7: 133
```

After anchoring `P_1=0`, each non-anchor difference polynomial has 255 forced
zeros, so the reduced interpolation system has only six compressed variables.
The live question is therefore very concrete:

```text
Can the same all-pair-boundary membership multiset be placed on H
so that this 6-variable reduced system becomes singular?
```

## Search Layer

The scanner tests 515 placements of the same multiset:

```text
deterministic embeddings:
  block
  bit_reversal
  fiber_round_robin

random embeddings:
  512 seeded full shuffles
```

Every tested embedding preserves:

```text
support sizes = 327 for all seven witnesses
pair intersections = 255 for all 21 pairs
compressed variables = 6
effective non-anchor equations = 659
```

The proxy field is `GF(12289)`, whose multiplicative group contains a subgroup
of order 512.

## Proxy Result

All 515 tested placements have full proxy rank:

```text
candidate embeddings: 515
proxy field: GF(12289)
proxy singular embeddings: 0
proxy full-rank embeddings: 515
best proxy rank/nullity: 6 / 0
```

Thus the search found no proxy-singular placement of the all-pair-boundary
multiset.

## Exact Audit

The Sage audit exact-checks nine representative placements over `GF(17^32)`:

```text
block
bit_reversal
fiber_round_robin
random_shuffle_0000
random_shuffle_0001
random_shuffle_0017
random_shuffle_0064
random_shuffle_0255
random_shuffle_0511
```

All nine have exact full rank:

```text
exact field: GF(17^32)
exact-audited embeddings: 9
exact full-rank embeddings: 9
exact positive nullity: 0
```

This route-cuts the tested placements. It also shows that the all-pair-boundary
incidence profile does not automatically produce a reduced rank defect, even
though it pushes every pair intersection to the RS cap.

This is not a global obstruction. Other placements of the same multiset,
different all-pair-boundary MILP optima, and non-value-class constructive
families remain open.

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_singular_all_pair_boundary_embedding_search.py --write
python3 experimental/scripts/verify_m1_a327_singular_all_pair_boundary_embedding_search.py
sage experimental/scripts/audit_m1_a327_singular_all_pair_boundary_embedding_search.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_singular_all_pair_boundary_embedding_search.sage --write-json
```

to regenerate the exact-audit JSON.

## Not Claimed

```text
MCA N_bad
protocol soundness
ordinary list decoding beyond the stated interleaved-list predicate
a=327 interleaved-list certificate
global Lambda_mu(C,327) <= 6
exact Lambda_mu
exact delta*_C
improvement over PR #133
```
