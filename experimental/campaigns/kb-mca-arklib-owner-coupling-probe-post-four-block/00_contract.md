# Contract: ArkLib transfer and owner-coupling probe

## Exact stack boundary

This research packet is one child of

```text
e3bca2fb3fb3e7e5d34a92f2ecdd7cbf275309e6
```

the rank-twelve four-block payment through `K = 662,480`.

It audits the current canonical ArkLib/δ* repository at

```text
elizaOS/proximityprize
main 983069a332de36fd3d6ef6f33fccadafa01b0ff5
```

and tests one source-bound coupling at the adjacent `K = 662,479` wall.

## Positive output

The old relaxed extremal profile at `K = 662,479` cannot simultaneously
saturate its dominant fixed-pair owner and its two one-block correction rays.

Let `U` be the dirty coordinates on which the received pair already agrees
with the fixed pair, and put `u = |U|`.  Those coordinates lie on the
fixed-pair graph inside both ray parameter planes, so they cannot support
off-graph ray points.  Exact optimization over every legal
`0 <= u <= 58,812` gives

```text
old independent exceptional cap       1,099,983
shared-fiber coupled exceptional cap     828,956
saving                                  271,027
exceptional budget                    1,099,965
coupled slack                           271,009
```

This eliminates the specific independently maximized owner profile causing the
eighteen-slope wall.

## Nonclaims

This packet does **not** prove the adjacent cell paid.  A complete theorem
still must optimize the shared-fiber coupling over every feasible dirty
incidence profile, rather than only the old relaxed extremizer.

It does not prove affine error rank twelve, move an active-v4 ledger atom, or
close KoalaBear.
