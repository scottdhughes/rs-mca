# M1 a=327 collision-tangent quotient-plane search

Status: `TESTED_TANGENT_PLANES_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `84d5194`. The previous rescheduler-aware quotient-plane
search tested generic weak-block second directions and found only immediate
capacity loss:

```text
best capacity upper bound: 165
proxy plane candidates: 0
failure mode: PLANE_CAPACITY_LOSS
```

That result says the tested `q2` directions were transverse to the
high-capacity collision skeleton. This packet instead constructs `q2` inside a
tangent space that preserves selected dominant value-class equalities from the
best quotient-line candidates.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

For a retained quotient line

```text
v = c + lambda q1
```

the scanner computes dominant value classes at each coordinate. It then
selects protected classes until each witness has a protection budget of
`260`, `280`, `300`, or `320` protected credits.

For every protected class `C` at coordinate `h`, the tangent direction `q2`
must satisfy:

```text
q2_i(h) = q2_j(h) for i,j in C.
```

Those are linear constraints on the existing proxy nullspace basis. The scan
then samples basis directions from the resulting tangent space and evaluates:

```text
v + mu q2.
```

This is a proxy search over `GF(12289)`. A public proof record still requires
exact `GF(17^32)` reconstruction and Sage verification.

## Result

The first bounded tangent-plane pass tested:

- retained quotient lines: `5`;
- protection budgets: `260`, `280`, `300`, `320`;
- tangent spaces built: `20`;
- tangent directions tested: `320`;
- `mu` values tested: `10,240`;
- proxy tangent candidates: `0`.

Unlike the previous generic plane search, the tangent construction preserves
capacity:

```text
best capacity upper bound: 404
best six-class dominance: 4
best proxy max-min: 260
best agreement vector: [260,261,260,260,260,260,260]
```

The failure modes were:

```text
TANGENT_REDUCED_CAPACITY_UNSCHEDULED: 10240
TANGENT_LOW_RESCHEDULE: 76
TANGENT_BALANCE_IMPROVES: 4
```

The internal `TANGENT_REDUCED_CAPACITY_UNSCHEDULED` screen label means the
capacity/collapse screen passed before the bounded assignment-solve budget was
applied. The exact proxy rescheduler was run on `80` retained tangent samples.

This reverses the previous plane failure: generic weak-block directions killed
capacity immediately, while collision-tangent directions preserve capacity and
low collapse. The improvement in rescheduled max-min is small, from `259` to
`260`, so the live bottleneck is now balance inside the tangent-preserving
subspace.

No exact `GF(17^32)` audit was triggered.

## Status labels

`CANDIDATE` means a proxy tangent-plane candidate reaches `a>=327` and needs
exact `GF(17^32)` extraction.

`TESTED_TANGENT_PLANES_NO_A327` means the bounded tangent-plane sweep found no
proxy `a>=327` candidate.

`PARTIAL` means broader protection schedules, tangent combinations, and exact
field extraction remain open.

## Failure labels

- `TANGENT_SPACE_ZERO`: protection constraints killed all tangent directions.
- `TANGENT_CAPACITY_LOSS`: the tangent sample lost capacity below `327`.
- `TANGENT_COLLAPSE_RETURNS`: capacity survived but six-class dominance
  returned.
- `TANGENT_LOW_RESCHEDULE`: capacity and low collapse survived but max-min
  remained below `327`.
- `TANGENT_BALANCE_IMPROVES`: max-min improved over the parent line but stayed
  below `327`.
- `TANGENT_PROXY_CANDIDATE`: proxy max-min reached at least `327`.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
