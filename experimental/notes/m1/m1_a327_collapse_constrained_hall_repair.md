# M1 a=327 collapse-constrained Hall repair

Status: `TESTED_CONSTRAINED_HALL_REPAIR_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `4d5ce7f`, where direct Hall-guided target mutation
successfully repaired the tight Hall subsets but did so by returning to the
large six-class collapse basin.

Parent baseline:

```text
best Hall bound:       332
best proxy max-min:    332
best agreement vector: [332,333,332,332,332,332,332]
best tight-subset B:   [1177,1177,1177]
six-class dominance:   359
failure mode:          HALL_REPAIR_COLLAPSE_RETURNS
```

The purpose of this branch is to measure the tradeoff between Hall repair and
six-class dominance.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

This remains a proxy-field search over `GF(12289)`. It is not a
`GF(17^32)` proof record.

## Method

The scanner uses the tight Hall subsets from `ed4cf43`:

```text
U1 = {1,2,3}
U2 = {2,3,4}
U3 = {2,3,5}
```

For each target system it tries to maximize the minimum of the three
tight-subset credits while enforcing a hard cap on six-like target-row
pressure. It then samples proxy nullspace vectors and classifies the resulting
value-class geometry by the actual sampled six-class dominance.

Dominance caps tested:

```text
350, 300, 250, 200, 150, 100, 50, 25
```

Repair row budgets:

```text
32, 64, 96, 128
```

Selection objectives:

```text
hall_min_repair
hall_avg_repair
hall_core23_repair
hall_capacity_hybrid
```

## Result

First bounded run:

```text
systems tested:         128
codeword tuple samples: 2048
proxy candidates:       0
```

Failure modes:

```text
HALL_REPAIR_CAPACITY_LOSS:      1536
HALL_REPAIR_COLLAPSE_RETURNS:    512
```

The best cap-satisfying frontier point is the same across the dominance caps
in the first run:

```text
best cap-satisfying capacity upper bound: 165
best cap-satisfying Hall bound:           165
best cap-satisfying six-class dominance:  0
best cap-satisfying failure mode:         HALL_REPAIR_CAPACITY_LOSS
```

The strongest rejected collapse-return sample shows the other side of the
tradeoff:

```text
proxy max-min:          334
agreement vector:       [334,334,334,334,334,334,334]
capacity upper bound:   461
Hall bound:             334
tight-subset B:         [1180,1180,1180]
six-class dominance:    356
dominance cap:          150
failure mode:           HALL_REPAIR_COLLAPSE_RETURNS
```

Thus, the hard cap succeeds at removing the collapse, but every cap-satisfying
sample loses the capacity geometry. The Hall-repair objective can still push
the proxy max-min above `327`, but only by violating the dominance cap and
returning to the collapse basin.

## Pareto summary

For every dominance cap tested, the best cap-satisfying sample had:

```text
capacity upper bound: 165
Hall bound:           165
six-class dominance:  0
failure mode:         HALL_REPAIR_CAPACITY_LOSS
```

The tight-subset `B(U)` values vary only slightly around:

```text
[738..747, 727..734, 739..746]
```

These are well below the `981` needed for a three-witness subset at agreement
`327`.

## Interpretation

This branch gives a clean obstruction curve for the tested target-selection
family:

```text
Hall repair above 327  -> high six-class dominance
low six-class dominance -> capacity/Hall collapse
```

It does not prove that all Hall-guided repairs are impossible. It does show
that the first hard-constrained Hall repair formulation cannot escape the
tradeoff already visible in `4d5ce7f`.

The next useful attack should not be unconstrained Hall repair. It should
search for Hall repair inside the already low-collapse tangent skeleton, so
the repair rows are not free to rebuild the collapse basin and are not forced
to destroy the collision skeleton wholesale.

## Status labels

`CANDIDATE` means a proxy candidate reaches `a>=327` while satisfying a
material dominance cap and needs exact `GF(17^32)` extraction.

`TESTED_CONSTRAINED_HALL_REPAIR_NO_A327` means the bounded hard-cap Hall
repair sweep found no acceptable proxy `a>=327` candidate.

`PARTIAL` means broader dominance-aware Hall repair and exact-field lifting
remain open.

## Failure labels

- `HALL_REPAIR_COLLAPSE_RETURNS`: Hall repair improves, but sampled
  six-class dominance violates the cap or remains too high.
- `HALL_REPAIR_BLOCKED_BY_CAP`: the cap prevents the tight Hall bound from
  reaching the target.
- `HALL_REPAIR_CAPACITY_LOSS`: the cap-satisfying value-class geometry has
  capacity below `327`.
- `HALL_REPAIR_LOW_RESCHEDULE`: Hall and capacity are adequate, but proxy
  max-min remains below `327`.
- `HALL_CONSTRAINED_PROXY_CANDIDATE`: proxy max-min reaches at least `327`
  under a material dominance cap.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
