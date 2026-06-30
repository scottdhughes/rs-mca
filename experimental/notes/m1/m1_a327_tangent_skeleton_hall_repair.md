# M1 a=327 tangent-skeleton Hall repair

Status: `TESTED_TANGENT_HALL_REPAIR_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `f0d758d`. The hard dominance-cap Hall repair branch made
the tradeoff explicit:

```text
unconstrained Hall repair -> proxy 334, high collapse
hard cap on collapse      -> collapse removed, capacity 165
```

This branch tries the intermediate move: repair the Hall-tight subsets inside
the already low-collapse tangent skeleton from `758af1b` / `ed4cf43`, rather
than adding generic Hall rows that can rebuild the collapse basin.

## Baseline

The starting tangent geometry has:

```text
capacity upper bound: 404
six-class dominance:  4
proxy max-min:        260
Hall bound:           260
agreement vector:     [260,261,260,260,260,260,260]
```

The original tight Hall subsets are:

```text
U = {1,2,3}: B(U)=781
U = {2,3,4}: B(U)=781
U = {2,3,5}: B(U)=781
```

Each needs `981` credits to support agreement `327`.

## Method

The scanner reconstructs retained low-collapse tangent value-class geometries,
then builds target systems from:

- tangent-skeleton rows from dominant value classes;
- localized Hall-repair rows at coordinates where the original tight subsets
  have subset-credit deficit.

Repair families:

```text
pair_23
triples_123_234_235
mixed_pair_triple
fiber_balanced_pair23
```

Repair row budgets:

```text
16, 32, 64, 96
```

The scan records both total six-class dominance and dominance added relative
to the source tangent skeleton.

## Result

First bounded run:

```text
base tangent systems: 5
target systems:       80
proxy samples:        1280
proxy candidates:     0
```

Failure modes:

```text
TANGENT_HALL_NOT_REPAIRED:              880
TANGENT_HALL_REPAIR_COLLAPSE_RETURNS:   320
TANGENT_HALL_REPAIR_LOW_RESCHEDULE:      80
```

Best retained sample:

```text
proxy max-min:                     308
agreement vector:                  [308,308,308,308,308,308,308]
capacity upper bound:              453
Hall bound:                        308
six-class dominance total:         0
six-class dominance added:         0
failure mode:                      TANGENT_HALL_REPAIR_LOW_RESCHEDULE
```

The original three-witness Hall subsets are over-repaired in the best sample:

```text
B({1,2,3}) = 1536
B({2,3,4}) = 1536
B({2,3,5}) = 1536
```

The new Hall bottleneck becomes a two-witness family involving witness `7`:

```text
U = {1,7}: B(U)=616, floor(B/2)=308
U = {2,7}: B(U)=616, floor(B/2)=308
U = {3,7}: B(U)=616, floor(B/2)=308
U = {4,7}: B(U)=616, floor(B/2)=308
U = {5,7}: B(U)=616, floor(B/2)=308
```

For agreement `327`, each two-witness subset needs `654`, so the remaining
deficit is `38` subset-credits.

## Interpretation

This is a meaningful positive diagnostic, even though it is not a candidate.
Compared with the tangent baseline:

```text
Hall bound / proxy max-min: 260 -> 308
capacity:                   404 -> 453
six-class dominance added:  0
```

So Hall repair inside the tangent skeleton can improve balance without
returning to the collapse basin. The obstruction moved from the original
three-witness Hall subsets to a sharper pair bottleneck involving witness `7`.

The next useful attack should be witness-7 pair Hall repair inside this
already repaired tangent skeleton, targeting the `38` remaining credits for
the tight pairs `{i,7}` rather than repeating the original `{1,2,3}`,
`{2,3,4}`, `{2,3,5}` repair.

## Status labels

`CANDIDATE` means a proxy tangent-skeleton Hall repair reaches `a>=327` with
low added collapse and needs exact `GF(17^32)` extraction.

`TESTED_TANGENT_HALL_REPAIR_NO_A327` means the bounded tangent-skeleton Hall
repair pass found no proxy `a>=327` candidate.

`PARTIAL` means broader tangent-skeleton repair and exact-field lifting remain
open.

## Failure labels

- `TANGENT_HALL_NOT_REPAIRED`: the original Hall bound does not improve.
- `TANGENT_HALL_REPAIR_COLLAPSE_RETURNS`: Hall improves by adding collapse.
- `TANGENT_HALL_REPAIR_CAPACITY_LOSS`: Hall repair destroys capacity below
  `327`.
- `TANGENT_HALL_REPAIR_LOW_RESCHEDULE`: Hall/capacity improve but proxy
  max-min remains below `327`.
- `TANGENT_HALL_PROXY_CANDIDATE`: proxy max-min reaches at least `327` with
  low added collapse.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
