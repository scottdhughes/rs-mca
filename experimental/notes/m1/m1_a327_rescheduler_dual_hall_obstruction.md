# M1 a=327 rescheduler dual/Hall obstruction audit

Status: `RESCHEDULER_OBSTRUCTION_CERTIFICATE / PARTIAL / EXPERIMENTAL`

This packet follows `758af1b`, where collision-tangent quotient directions
preserved capacity and mostly fixed collapse:

```text
best capacity upper bound: 404
best six-class dominance: 4
best proxy max-min: 260
```

The live bottleneck is therefore the received-word rescheduler. This audit
turns that bottleneck into an explicit subset-credit calculation.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Hall-style upper bound

For a fixed seven-codeword tuple, every coordinate `h` gives value classes
`C`. The rescheduler chooses one class per coordinate. For any nonempty witness
subset `U`, define

```text
B(U) = sum_h max_C |C intersect U|.
```

If every witness in `U` receives at least `a` credits, then necessarily

```text
|U| a <= B(U).
```

Thus every tuple has a cheap exact upper bound

```text
hall_bound = min_U floor(B(U) / |U|).
```

There are only `2^7 - 1 = 127` witness subsets, so this is a small exact
audit over the proxy value-class partitions.

## Method

The scanner reconstructs proxy value-class partitions for representative
samples from:

- `m1_a327_collapse_quotient_line_search.json`;
- `m1_a327_rescheduler_aware_quotient_plane_search.json`;
- `m1_a327_collision_tangent_quotient_plane_search.json`.

For each sample it records:

- capacity upper bound;
- exact proxy rescheduler max-min when capacity is at least `327`;
- Hall subset bound;
- tight witness subsets;
- deficit to target `327`;
- critical-coordinate histograms for a tight subset.

## Result

The first audit replayed `86` retained samples and deduplicated them to `30`
unique value-class geometries:

```text
collapse_quotient_line:                 2
collision_tangent_quotient_plane:       9
rescheduler_aware_quotient_plane:      19
```

The failure split was:

```text
HALL_TIGHT:          11
LOW_CAPACITY_SCREEN: 19
```

The best current tangent tuple is Hall-tight:

```text
source:                  collision_tangent_quotient_plane
capacity upper bound:    404
six-class dominance:     4
rescheduler max-min:     260
agreement vector:        [260,261,260,260,260,260,260]
Hall bound:              260
failure mode:            HALL_TIGHT
```

Representative tight witness subsets are three-witness sets:

```text
U = {1,2,3}: B(U)=781, floor(B(U)/3)=260, deficit to a=327 is 200
U = {2,3,4}: B(U)=781, floor(B(U)/3)=260, deficit to a=327 is 200
U = {2,3,5}: B(U)=781, floor(B(U)/3)=260, deficit to a=327 is 200
```

For the first tight subset, `401` coordinates are critical in the sense that
no value class credits all witnesses in the subset. The dominant critical
pattern is concentrated in the recorded value-class mask histogram, with a
broad quotient-fiber spread rather than a single-fiber obstruction.

This means the current best tangent geometry is not failing because the MILP
rescheduler missed an assignment. It is failing because a subset-credit Hall
bound already caps the optimum at `260`.

## Status labels

`RESCHEDULER_OBSTRUCTION_CERTIFICATE` means at least one analyzed tuple has
Hall bound equal to the exact proxy rescheduler optimum, giving a replayable
subset-credit obstruction for that tuple.

`AUDIT` means Hall bounds were computed, but no tight Hall certificate was
found in the analyzed set.

`PARTIAL` means broader tuple families and exact `GF(17^32)` lifting remain
outside this audit.

## Failure labels

- `LOW_CAPACITY_SCREEN`: the tuple is already below `327` capacity.
- `HALL_TIGHT`: Hall bound equals the exact proxy rescheduler optimum.
- `HALL_GAP`: Hall bound is below `327` but above the exact rescheduler
  optimum.
- `BALANCE_GAP`: Hall bound permits `327`, but the exact rescheduler still
  falls short.
- `UNKNOWN`: assignment was not run for the sample.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record.
