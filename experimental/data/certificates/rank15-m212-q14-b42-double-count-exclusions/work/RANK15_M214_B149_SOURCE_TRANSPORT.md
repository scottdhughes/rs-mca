# Source transport from an exact M214 two-flat to the active-deletion arrangement

## Theorem

Work over the deployed field

```text
p=2,130,706,433,
n=2,097,152,
K=1,048,576,
m=1,116,047.
```

Let `A` be an exact affine two-flat in `F_p[X]_<K`, let `Z` be its actual
universal agreement set with `|Z|=u`, and suppose the full intersection of
`A` with the one-row agreement list has exactly

```text
M=214
```

points.  Assume every proper coordinate section outside `Z` contains at most
15 of these points.  Put

```text
N=n-u,  a=m-u,  lambda=K-1-u.
```

If

```text
214a-14N-148lambda > 0,                                  (1)
```

then this two-flat is impossible.

## Proof

Apply the source-pinned locator-saturation normal form to the exact full
intersection `S=L_m(U) intersect A`.  Its rich-line equations give

```text
t d >= W_214+14r,
W_214=214a-14N,
d<=lambda-r,
t<=b<=214,                                                (2)
```

where `t` is the number of selected rich directions and `b` is the number of
distinct rich affine coordinate-section lines, each containing exactly 15
points of `S`.  If `t<=148`, then

```text
t d <=148(lambda-r)
     < W_214+14r,
```

because the difference is

```text
W_214-148lambda+162r>0
```

by (1).  Therefore

```text
149<=t<=b<=214.                                           (3)
```

Projectively complete the affine parameter plane and dualize it.  The 214
distinct listed points become 214 distinct projective lines.  Every distinct
rich affine line becomes a distinct marked point through exactly the 15 dual
lines corresponding to its 15 listed points.  Delete every dual line that
contains no marked point.  If `d_active` is the number retained, then

an active line contains at most 15 marked points: the fourteen other active
lines used at distinct marked points on it are disjoint, so
`14 k_L<=d_active-1<=213`.  Counting marked incidences therefore gives
`15b=sum_L k_L<=15d_active`.  Hence

```text
149<=b<=d_active<=214,
```

every marked point lies on exactly 15 retained lines, and every retained line
contains at least one marked point.  This is exactly the object excluded by
the live full active-deletion theorem in characteristic greater than 214.
Since `p>214`, contradiction.

## Exact current base-row cells

The frozen post-M215 compiler has the exact M214 plateau

```text
u=1,042,095..1,043,955,
q=15.
```

On this plateau the left side of (1) decreases by 52 per state.  It is
positive precisely on

```text
u=1,042,095..1,043,939                    (1,845 cells),
```

with endpoint values `95,890` and `2`; at `u=1,043,940` it is `-50`.
Thus the theorem source-validly caps these exact cells by 213.  It does not
cover the final 16 M214 cells `1,043,940..1,043,955`.

## Source pins and nonclaims

```text
locator-saturation normal form
48d72c94743f5a9c900b35197279a69bf00a8a133c7b27bf3ff39004b1257085

post-M214 cumulative compiler
f0a260c321a31f55cbdc253b5dfb8665acfc659461cc096770502567e6885c8a

live M214/b149 active-deletion theorem
5c1cb60b16960dde16d36185182dfdeb64bc7b7817cd02cf4b634398916a0810
```

This theorem does not apply to a provisional upper bound larger than 214 by
silently selecting a 214-subset: the pinned normal form defines `S` as the
full two-flat/list intersection.  It also does not reproduce or consume the
separate unpublished shifted-row `c=57` recurrence, and it makes no official
score claim.
