# M1 a=327 rescheduler-aware quotient-plane search

Status: `TESTED_QUOTIENT_PLANES_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `ad3d73a`, where affine quotient lines could almost remove
the `[1,3,4,5,6,7]` collapse while preserving capacity above `327`, but the
received-word rescheduler fell to max-min `259`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

Target: seven degree-`<256` codewords and one received word on `H` with
minimum agreement at least `327`.

## Method

The scanner starts from the retained quotient lines:

```text
c + lambda q1
```

and tests quotient planes:

```text
c + lambda q1 + mu q2
```

where `q2` is selected to touch weak witness blocks from the line's exact
proxy rescheduler output. The first pass keeps `lambda` fixed at the best line
value, screens 32 `mu` values per second direction by capacity and collapse
dominance, and runs the exact proxy rescheduler only on the best promising
`mu` for each second direction.

This is a proxy search only. A public proof record still requires exact
`GF(17^32)` reconstruction and Sage verification.

## Result

The first bounded plane pass tested:

- retained quotient lines: `10`;
- second quotient directions: `320`;
- lambda/mu pairs: `10,240`;
- proxy plane candidates: `0`.

Every tested plane sample failed the capacity screen:

```text
PLANE_CAPACITY_LOSS: 10240
best capacity upper bound: 165
best six-class dominance: 0
best proxy max-min: null
```

Thus the tested `q2` directions do reduce the collapse signature, but they
destroy the collision capacity before the received-word rescheduler is
meaningful. This is stronger than the line-search failure in one direction:
the best lines kept capacity but rescheduled poorly, while this first
rescheduler-aware plane layer loses capacity immediately.

No exact `GF(17^32)` audit was triggered.

## Status labels

`CANDIDATE` means a proxy plane candidate reaches `a>=327` and needs exact
`GF(17^32)` extraction.

`TESTED_QUOTIENT_PLANES_NO_A327` means the bounded quotient-plane sweep found
no proxy `a>=327` candidate.

`PARTIAL` means broader direction scoring, two-dimensional lambda/mu sweeps,
and exact-field extraction remain open.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
