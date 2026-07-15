# Fixed-pair active-pencil grid and weighted-tail cut

## Verdict

```text
SOURCE-VALID LOCAL THEOREM
SECOND-MOMENT CAP <=155 FOR c=558..832
DIRECTION-PAIR CAP <=155 FOR c=554..832
LOW-CORE RANGE c=0..553 NOT PAID
NO RANK-16 STATE OR OFFICIAL SCORE PAYMENT
```

Fix the accepted saturated listed pair at

```text
u=1,043,459,   N=1,053,693,   a=72,588,   h=5,116.
```

In one active affine two-plane, let `c` be its common owned root core and
put

```text
d=5,116-c,             s=62,356+c,             U=913,633.
```

The common saturated neighbors in this plane form a simple bipartite graph
between their saturated lines through the two fixed endpoints.  Its row and
column degrees are at most `14`, and the number of available rows and columns
is at most

```text
R(c)=floor((72,588-c)/(5,116-c))-1.
```

The exact jumps are

```text
R=13 on c=0..296,
R=14 on c=297..617,
R=15 on c=618..832.
```

Every neighbor has at least `s` actual agreement coordinates outside the
actual agreement sets of both endpoints.  These tails live in a universe of
size at most `U`.  Tails of two neighbors sharing a row or a column are
disjoint; every other pair meets in at most `d` coordinates.

Integral column convexity gives the claimed second-moment cap.  A further
source-valid direction-pair relaxation uses that all coordinate lines in one
parallel direction consume one degree-`d` root fiber.  It improves the first
uniform `155` cutoff from `c=558` to `c=554`.

It does not prove a uniform `155` cap in `c=0..553`.  The strongest new
relaxation still admits `156` neighbors at `c=553` with only `778` incidences
of slack, and its maximum in the unpaid range is still `196`.

## 1. Actual agreements remove the support-selection ambiguity

Let the fixed endpoints be `P_0,P_1`, and let `P` be a common saturated
neighbor.  The three saturated differences have exactly `h` residual roots.
Their frozen selected-support intersections already have size `h`, so all
of those roots are actual received-word agreement coordinates.  Conversely,
two different candidates can agree with the received word together only at
a root of their difference.  Hence every saturated endpoint pair has exactly
`h` actual common agreements, independently of how the exact `m`-supports
were selected.

The common roots of the two-dimensional direction space are therefore
actual agreements of the whole plane; write their number as `c`.  The two
endpoint root blocks of `P`, outside this core, are disjoint and each has
size `d`.  If `A(P)` is the complete residual agreement set of `P`, define

```text
T_P=A(P) minus (A(P_0) union A(P_1)).
```

Then

```text
|T_P|=|A(P)|-2h+c >= a-2h+c=62,356+c=s.                 (1)
```

The ambient tail universe is the complement of the two complete endpoint
agreement sets.  Since each endpoint has at least `a` residual agreements
and their intersection has exactly `h`, its size is at most

```text
N-(2a-h)=1,053,693-(145,176-5,116)=913,633=U.           (2)
```

Thus using `U` in a lower convexity bound is conservative.  This proof uses
complete actual agreement sets; no first-match or reselection compatibility
is assumed.

## 2. The row--column graph is literal

The line `P_0P_1`, together with the distinct saturated neighbor directions
through `P_0`, has pairwise disjoint `d`-root blocks outside the plane core.
Every block lies in the same frozen selected support of `P_0`.  Therefore,
if there are `r` neighbor rows,

```text
c+(1+r)d<=a,
r<=R(c).                                                  (3)
```

The identical argument at `P_1` gives `t<=R(c)` columns.

One saturated affine line has exactly `u+h=K-1` actual universal agreement
coordinates.  After they are deleted, every listed point on it needs

```text
m-(K-1)=67,472
```

agreements among `n-(K-1)=1,048,577` coordinates.  At a nonconstant
coordinate section at most one scalar point of the line agrees.  Hence the
line contains at most

```text
floor(1,048,577/67,472)=15                               (4)
```

listed candidates.  The endpoint itself consumes one place, so every row
and column degree is at most `14`.

A row through `P_0` and a column through `P_1` meet in at most one affine
point.  Thus a neighbor is an edge of a simple bipartite graph `G` with

```text
r,t<=R(c),       Delta(G)<=14.                           (5)
```

In particular, for `e=|E(G)|`,

```text
e<=R(c) min(R(c),14).                                    (6)
```

For fixed `e`, convexity of the row and column degrees gives

```text
P(G)=sum_rows binom(deg,2)+sum_cols binom(deg,2)
    >=2 Cbal(e,R),                                       (7)

Cbal(e,R)=R binom(q,2)+rho q,       e=qR+rho, 0<=rho<R.
```

The right side is a relaxation when fewer than `R` rows or columns occur,
which is the safe direction for an upper bound.

## 3. Tail intersections and the exact second moment

For a tail coordinate `x`, the agreement equation restricted to the plane
is an affine line.  It contains neither endpoint.  Consequently it cannot
contain two neighbors in one row or in one column.  This proves directly
that tails on a common row or column are disjoint.

If two neighbors are in different rows and columns, a common tail coordinate
is a root of their nonzero plane direction.  After the common core is
divided out, that direction has degree at most `d`; hence

```text
|T_P intersection T_Q|<=d.                              (8)
```

Let `q_x` be the number of neighbor tails containing coordinate `x`.  From
(1)--(2), integral convexity yields

```text
sum_x binom(q_x,2)>=Cint(es,U),                          (9)

Cint(I,U)=U binom(floor(I/U),2)
          +(I mod U) floor(I/U).
```

Equations (7)--(8) give the opposite bound

```text
sum_x binom(q_x,2)
 <=d[binom(e,2)-P(G)]
 <=d[binom(e,2)-2 Cbal(e,R)].                           (10)
```

The verifier exhausts every `c=0,...,832` and every integer allowed by (6).
The resulting maxima include

```text
c=0:   169,
c=297: 196,
c=557: 156,
c=558: 155,
c=832: 101.
```

Thus (9)--(10) prove `e<=155` uniformly for `558<=c<=832`, but not below.

## 4. Exact direction-pair strengthening

Coordinates whose agreement lines are parallel have the same kernel
direction.  Their evaluation parameters are roots of one primitive
direction polynomial of degree at most `d`.  Thus their total coordinate
weight is at most `d`.

For every occupied direction `nu`, let `h_nu` be the largest number of
neighbors on one of its coordinate lines.  A tail line meets every row and
column in at most one point, so

```text
1<=h_nu<=R.                                               (11)
```

Choose one line attaining `h_nu` in each direction.  Lines in different
directions use disjoint neighbor pairs, while row- and column-sharing pairs
cannot occur on a tail line.  Therefore

```text
sum_nu binom(h_nu,2)
 <=B(e,R):=binom(e,2)-2 Cbal(e,R).                       (12)
```

Let `P_R(d,U,B)` be the largest possible tail incidence in this relaxation.
Move coordinate weight from a direction with smaller `h_nu` to one with
larger `h_nu`.  The objective does not decrease and (12) does not increase.
At the optimum, `floor(U/d)` direction weights are `d` and at most one is
the remainder `U mod d`.

For `f` full directions, the exact upgrade count is obtained in layers.  If
`L` is the largest integer `0<=L<=R-1` with

```text
f L(L+1)/2<=B,
```

then the `f` baseline lines receive `fL` upgrades, followed by at most

```text
min(f, floor((B-fL(L+1)/2)/(L+1)))
```

one-step upgrades.  The verifier also compares this closed form with a
literal dynamic program on every small regression instance.  It checks the
partial direction by all `h=1,...,R`.

The exact strengthened maxima include

```text
c=0:   169,
c=297: 196,
c=553: 156,
c=554: 155,
c=557: 153,
c=558: 152,
c=618: 148,
c=832: 101.                                              (13)
```

Thus

```text
e<=155       for every 554<=c<=832.                      (14)
```

The boundary is exact for this relaxation:

```text
c=553,e=156: incidence need=9,813,804,
             capacity      =9,814,582, margin=+778;

c=554,e=156: incidence need=9,813,960,
             capacity      =9,813,232, margin=-728.       (15)
```

The balanced graph degree sequence in the surviving `R=14,e=156` row is
source-combinatorially feasible: an `11`-regular circulant bipartite graph
on `14+14` vertices, plus two absent edges in distinct rows and columns, has
two degrees `12` and twelve degrees `11` on each side.  This does not realize
the polynomial plane; it shows that the `+778` in (15) cannot be rejected by
silently strengthening the degree convexity.

## 5. Why Hirzebruch and the current marked-arrangement theorem do not close
the remaining range

Projectively moving the endpoint line to infinity makes the neighbors a
grid subset, and over characteristic zero Hirzebruch's inequality would give
a much stronger rich-transversal constraint.  The literal field is
`F_p`.  The packet's frozen

```text
work/RANK15_HIRZEBRUCH_LIFTABILITY_WALL.md
```

records the load-bearing fact that `p` being larger than the number of points
does not transfer Hirzebruch/BMY to a positive-characteristic arrangement.
No incidence-preserving characteristic-zero lift is available here.

The positive-characteristic DPW/Jacobian machinery applies to a reduced line
arrangement.  Tail coordinates instead give integer line multiplicities
`w_ell`, with only

```text
sum_(ell parallel nu) w_ell<=d.                          (16)
```

If the actual tail universe has size `U'<=U`, one may color the copies in
(16) into `d` reduced arrangements, balancing their degrees at
`floor(U'/d)` or `ceil(U'/d)`.  This is a valid max-flow decomposition, and
convexity gives useful summed Tjurina lower bounds.  Replacing `U'` by `U`
is legitimate in the preceding capacity relaxation, but adding fictitious
generic lines is not a source arrangement and therefore cannot be used to
claim a DPW contradiction.
However every color has its own unknown minimal Jacobian syzygy degree and
divisorial deletion profile.  The existing marked-arrangement theorem is a
small-degree, high-multiplicity statement and supplies no theorem that sums
those independent DPW/Chern ledgers across the `d` colors.  Random thinning
likewise loses the required point degrees.  Importing the characteristic-zero
inequality or treating the multiarrangement as one reduced arrangement would
be invalid.

Therefore the exact remaining local obligation is a characteristic-`p`
weighted-arrangement theorem strong enough to exclude `e=156` for
`0<=c<=553`, or a different source inequality.  This document proves no such
theorem.

## Scope

The result is a local per-active-pencil cap.  It does not by itself sum the
fixed-core classes, prove the active-hyperplane occupancy `Q<=1,046`,
eliminate `u=1,043,459`, propagate any rank-16 recurrence, address the other
affine ranks, or move either official score.

## Replay

```text
ruby --disable-gems -w \
  work/verify_rank16_fixed_pair_active_pencil_grid_tail_cut.rb
```

Expected first line:

```text
RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT: PASS
```
