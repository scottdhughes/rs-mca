# M1 a327 value-class MILP incidence seeds

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a solver-assisted value-class incidence search for the
`a=327` interleaved-list target over

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

## Why This Search

The previous high-overlap value-class beam reached nine pair intersections at
the RS cap `255`, but it was still a heuristic mutation search. This packet
uses `scipy.optimize.milp` to solve the smaller incidence-count problem first:

```text
512 coordinates,
7 witness supports,
|S_i| = 327 for every i,
|S_i cap S_j| <= 255 for every pair.
```

The variables are counts of membership masks

```text
E_h subset {1,...,7}.
```

After the MILP solves the count profile, the scanner embeds each profile onto
the 512 evaluation positions using three deterministic layouts:

```text
block,
bit_reversal,
fiber_round_robin.
```

## MILP Profiles

The scanner solves six profile objectives:

```text
all_sizes_max_pairs_at255
all_sizes_max_pairs_at250
all_sizes_min_anchor_variables
sizes_3_6_max_pairs_at255
sizes_3_7_max_pairs_at255
sizes_4_5_max_pairs_at255
```

The strongest combinatorial profile is:

```text
profile: all_sizes_max_pairs_at255
membership histogram:
  size 1: 110
  size 2: 45
  size 3: 22
  size 4: 21
  size 5: 78
  size 6: 103
  size 7: 133
pair intersections at 255: 21 / 21
anchor compressed variables: 6
```

Thus the incidence-count constraints alone do not block an all-pair-boundary
`a=327` value-class design. The algebraic rank gate is still decisive.

## Rank Audit

The Sage audit screens all 18 profile/embedding candidates over `GF(12289)`,
then exact-audits eight selected candidates over `GF(17^32)` using
proxy-selected square minors.

```text
candidate profiles: 6
embeddings per profile: 3
candidate incidence designs: 18
proxy field: GF(12289)
proxy-positive candidates: 0
exact selected candidates: 8
exact full-rank minors: 8
singular exact minors: 0
```

The exact selected set includes all three embeddings of the all-pair-boundary
profile:

```text
all_sizes_max_pairs_at255_block:             exact rank 6, nullity 0
all_sizes_max_pairs_at255_bit_reversal:      exact rank 6, nullity 0
all_sizes_max_pairs_at255_fiber_round_robin: exact rank 6, nullity 0
```

It also exact-audits lower- and medium-dimensional variants:

```text
all_sizes_min_anchor_variables_block:        exact rank 6,   nullity 0
sizes_3_7_max_pairs_at255_block:             exact rank 130, nullity 0
sizes_3_7_max_pairs_at255_fiber_round_robin: exact rank 130, nullity 0
sizes_3_6_max_pairs_at255_block:             exact rank 201, nullity 0
sizes_4_5_max_pairs_at255_block:             exact rank 440, nullity 0
```

Thus these named MILP incidence seeds cannot yield an `a=327`
interleaved-list witness through their reduced value-class incidence matrices.
In particular, putting every pair intersection exactly at the RS cap is not by
itself enough to create a rank defect.

This is not a global `a=327` obstruction. The broader value-class design space,
different embeddings of the non-selected profiles, and non-value-class
constructive families remain open.

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_valueclass_milp_incidence_seeds.py --write
python3 experimental/scripts/verify_m1_a327_valueclass_milp_incidence_seeds.py
sage experimental/scripts/audit_m1_a327_valueclass_milp_incidence_seeds.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_valueclass_milp_incidence_seeds.sage --write-json
```

to regenerate the rank-audit JSON.

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
