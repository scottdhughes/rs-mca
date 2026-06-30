# M1 a=327 Hall-guided target mutation

Status: `TESTED_HALL_MUTATIONS_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `ed4cf43`, where the rescheduler dual/Hall audit gave a
certificate-level explanation for the current `260` wall. The best tangent
tuple has capacity `404` and six-class dominance `4`, but its rescheduler
optimum is capped by a Hall subset bound:

```text
rescheduler max-min: [260,261,260,260,260,260,260]
Hall bound:          260
```

Representative tight subsets are:

```text
U = {1,2,3}: B(U)=781
U = {2,3,4}: B(U)=781
U = {2,3,5}: B(U)=781
```

For a target agreement `327`, each three-witness subset needs

```text
B(U) >= 3 * 327 = 981.
```

The tested geometry is therefore short by `200` subset-credits on each tight
three-witness obstruction.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

The scanner uses the tight Hall subsets as first-class target-selection
objects. For each candidate target coordinate, it computes the predicted
contribution to the three tight subset credits and solves a MILP over target
coordinates with:

- total row budget at most `640`;
- Hall-repair row mass at least `32`, `64`, `96`, or `128`;
- secondary witness-credit and quotient-fiber balance terms;
- objective variants emphasizing minimum tight-subset contribution, average
  contribution, the common core `{2,3}`, or a capacity hybrid.

For every selected target system, it solves the coefficient system over
`GF(12289)`, samples nullspace tuples, evaluates value classes, recomputes the
Hall bound, and runs the exact proxy rescheduler when capacity is at least
`327`.

This remains a proxy search. Public movement requires an exact `GF(17^32)`
certificate and Sage verification.

## Result

First bounded run:

```text
systems tested:              16
codeword tuple samples:      256
acceptable proxy candidates: 0
proxy field:                 GF(12289)
```

Failure modes:

```text
HALL_NOT_REPAIRED:             192
HALL_REPAIR_COLLAPSE_RETURNS:   64
```

The Hall-guided objective did repair the diagnosed tight subsets in the best
raw sample:

```text
best capacity upper bound: 460
best Hall bound:           332
best proxy max-min:        332
best agreement vector:     [332,333,332,332,332,332,332]
best tight-subset B:       [1177,1177,1177]
six-class dominance:       359
failure mode:              HALL_REPAIR_COLLAPSE_RETURNS
```

Thus the tight-subset obstruction from `ed4cf43` is a useful control knob:
the selected target systems can raise the three-witness Hall bound from `260`
to `332`. However, this improvement occurs by returning to the high-collapse
geometry rather than by producing a low-collapse, usable proxy witness.

No exact `GF(17^32)` audit was triggered.

## Interpretation

This branch does not show that Hall repair is impossible. It shows that the
first direct Hall-repair MILP repairs the starved subsets by restoring the same
collapse basin that earlier exact-lift branches identified:

```text
high Hall bound / high capacity / high six-class dominance
```

The next useful target is therefore not generic Hall repair, but
collapse-constrained Hall repair: increase `B(U)` for the tight subsets while
explicitly capping the six-class dominance or requiring the repair rows to stay
inside the low-collapse tangent skeleton.

## Status labels

`CANDIDATE` means a proxy Hall-guided candidate reaches `a>=327` while passing
the collapse-control filters and needs exact `GF(17^32)` extraction.

`TESTED_HALL_MUTATIONS_NO_A327` means the bounded Hall-guided mutation pass
found no proxy `a>=327` candidate.

`PARTIAL` means broader Hall-guided target systems, tangent directions, and
exact-field lifting remain open.

## Failure labels

- `HALL_NOT_REPAIRED`: the sample Hall bound remains at or below the baseline
  `260`.
- `HALL_REPAIR_DESTROYS_CAPACITY`: Hall bound improves but capacity falls
  below `327`.
- `HALL_REPAIR_LOW_RESCHEDULE`: Hall bound and capacity improve, but exact
  proxy max-min remains below `327`.
- `HALL_REPAIR_COLLAPSE_RETURNS`: collapse dominance returns.
- `HALL_PROXY_CANDIDATE`: proxy max-min reaches at least `327`.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
