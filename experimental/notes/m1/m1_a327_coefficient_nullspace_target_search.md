# M1 a327 coefficient-nullspace target search

Status: ROUTE_CUT_TESTED_ROOT_SETS / PARTIAL / EXPERIMENTAL

This note records a coefficient-level search for the `a=327`
interleaved-list target over

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

## Model

The previous all-pair-boundary incidence search reduced the scalar problem to
six variables. This packet attacks that reduced determinant condition directly.

Anchor:

```text
P_1 = 0.
```

For witnesses `i=2,...,7`, choose 255-point root sets `Z_i` and write

```text
D_i(X) = c_i L_i(X),
```

where `L_i` is the locator polynomial vanishing on `Z_i`. Since

```text
deg L_i = 255,    deg D_i < 256,
```

only the scalar coefficient `c_i` remains.

For a non-anchor pair equality at coordinate `h`, the scalar equation is

```text
c_i L_i(h) = c_j L_j(h).
```

So a successful construction needs locator-ratio labels that are
multiplicatively consistent enough to produce large value classes.

## Proxy Search

The scanner tests four root-set families:

```text
quotient_fiber_plus_residual:      6 tuples
cyclic_interval:                   6 tuples
seeded_random_255:                24 tuples
all_pair_boundary_embedding_roots: 8 tuples
```

For each root tuple, it computes locator values over proxy field `GF(12289)`.
It then generates scalar tuples from the most frequent base locator-ratio
labels:

```text
c_1 = 1,
c_i in top 3 labels for L_1(h)/L_i(h).
```

The scan tested:

```text
root tuples: 44
scalar/root candidates: 10,736
proxy field: GF(12289)
proxy candidates reaching a=327 capacity: 0
```

The best proxy candidate is:

```text
root tuple: all_pair_boundary_random_shuffle_0064
family: all_pair_boundary_embedding_roots
capacity total: 2053
capacity upper bound: floor(2053/7) = 293
largest-class histogram:
  1: 176
  2: 29
  3: 12
  4: 21
  5: 78
  6: 63
  7: 133
```

Since `293 < 327`, no proxy assignment solve reaches the target.

## Exact Audit

The Sage audit exact-checks six selected root tuples over `GF(17^32)` using the
same scalar locator-ratio generation:

```text
all_pair_boundary_block
all_pair_boundary_random_shuffle_0064
all_pair_boundary_random_shuffle_0255
interval_shift_000_step_17
quotient_residual_shift_00
random_255_tuple_000
```

Each exact tuple tests 244 distinct scalar candidates. No exact selected tuple
reaches the `a=327` capacity threshold:

```text
all_pair_boundary_block:                best exact capacity upper bound 292
all_pair_boundary_random_shuffle_0064:  best exact capacity upper bound 292
all_pair_boundary_random_shuffle_0255:  best exact capacity upper bound 292
interval_shift_000_step_17:             best exact capacity upper bound 292
quotient_residual_shift_00:             best exact capacity upper bound 291
random_255_tuple_000:                   best exact capacity upper bound 291
```

Thus the tested scalar locator-ratio root-set families do not produce an
`a=327` interleaved-list witness.

This is not a global obstruction. Other root sets, different scalar search
rules, higher-dimensional residual factors, and non-scalar coefficient models
remain open.

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_coefficient_nullspace_target_search.py --write
python3 experimental/scripts/verify_m1_a327_coefficient_nullspace_target_search.py
sage experimental/scripts/audit_m1_a327_coefficient_nullspace_target_search.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_coefficient_nullspace_target_search.sage --write-json
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
