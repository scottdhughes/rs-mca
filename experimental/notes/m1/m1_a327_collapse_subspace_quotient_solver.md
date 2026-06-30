# M1 a=327 collapse-subspace quotient solver

Status: `TESTED_QUOTIENT_DIRECTIONS_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `f266cf1`, where soft target penalties preserved high
proxy capacity and reached proxy max-min `332`, but every proxy-positive sample
remained dominated by the `[1,3,4,5,6,7]` collapse.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Collapse subspace

With `P_1=0` and `D_i=P_i-P_1`, collapse of witnesses
`[1,3,4,5,6,7]` means:

```text
D_3 = D_4 = D_5 = D_6 = D_7 = 0
```

as polynomials, since equality on all 512 points of `H` forces equality for
degree-`<256` differences. The collapse subspace is therefore the part of the
target nullspace supported only on the `D_2` coefficient block.

This scanner computes, over the proxy field `GF(12289)`:

- the full target nullity;
- the dimension of the intersection with the collapse subspace;
- the quotient dimension;
- projection ranks onto each `D_i` block;
- samples of collapse-only, quotient-only, and collapse-plus-quotient
  directions.

The purpose is to test whether quotient directions can preserve the
high-capacity skeleton while reducing the collapse dominance.

## Result

The first pass analyzed the two distinct high-performing soft target cores
retained from `f266cf1`.

For both cores:

```text
proxy rank = 640
proxy nullity = 896
collapse-subspace dimension = 103
quotient dimension = 793
```

The quotient is therefore large: the target systems do contain many formal
directions outside the `[1,3,4,5,6,7]` collapse subspace.

The sampled tradeoff was negative:

```text
samples tested = 232
best capacity upper bound = 460
best proxy max-min = 332
best six-class dominance = 359
best failure mode = COLLAPSE_ONLY_HIGH_CAPACITY
```

Failure-mode counts:

```text
COLLAPSE_ONLY_HIGH_CAPACITY       10
QUOTIENT_DIRECTION_CAPACITY_LOSS  94
QUOTIENT_DIRECTION_LOW_RESCHEDULE 128
```

So the high-capacity/high-agreement proxy samples still come from the collapse
subspace. Tested quotient directions exist in abundance, but they either
destroy capacity or preserve enough capacity only to fall below the `a=327`
rescheduling target.

No collapse-reduced proxy `a>=327` candidate was found, and no exact
`GF(17^32)` audit was triggered.

## Status labels

`CANDIDATE` means a collapse-reduced proxy quotient sample reaches `a>=327`
and needs exact `GF(17^32)` extraction.

`TESTED_QUOTIENT_DIRECTIONS_NO_A327` means the bounded quotient samples found
no collapse-reduced proxy `a>=327` candidate.

`PARTIAL` means broader quotient sampling and exact-field nullspace extraction
remain open.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
