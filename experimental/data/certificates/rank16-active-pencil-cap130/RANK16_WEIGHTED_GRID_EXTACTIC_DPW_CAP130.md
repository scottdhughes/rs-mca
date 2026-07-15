# Rank-16 all-profile Chern/Tjurina sharpening: occupancy at most 130

## Verdict

```text
EXACT SOURCE-VALID LOCAL THEOREM
EVERY SURVIVING FIXED-PAIR ACTIVE PENCIL HAS OCCUPANCY AT MOST 130
UNIFORM FOR EVERY CORE 0<=c<=832
THE SELECTED-131 ALL-PROFILE SCAN HAS ZERO FAILURES
THE ADJACENT SELECTED-130 SCAN FAILS, SO THIS METHOD STOPS SHARPLY AT 130
NO ACTIVE-HYPERPLANE OWNER THEOREM OR RANK-16 PAYMENT IS CLAIMED
```

This theorem consumes the source interface and characteristic-valid
DPW/extactic/Chern stripping theorem frozen in

```text
RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md
RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md.
```

Applying the accepted post-stripping Chern/Tjurina refinement to every legal
profile, including nonsquare profiles, closes the selected-131 scan and gives
the cap 130.

## 1. Frozen source interface

Fix an active pencil and suppose it contains at least `131` neighbors.  Choose
exactly `131`.  For core `0<=c<=832`, put

```text
d=5,116-c,
b=62,356+c,
U=913,633.
```

The accepted complete-tail theorem supplies actual tails `T_P` with

```text
sum_P |T_P| >=131b,
|union_P T_P| <=U.                                      (1)
```

The selected neighbors form a simple row-column grid.  Row and column degrees
are at most 14, and

```text
r,t<=R(c)=floor((72,588-c)/(5,116-c))-1,
R=13 on c=0..296,
R=14 on c=297..617,
R=15 on c=618..832.                                     (2)
```

A transverse tail line contains at most `s=min(r,t)` selected points.  The
accepted least-loaded primitive-direction coloring splits all actual
tail-coordinate copies into `d` reduced line arrangements whose loads differ
by at most one.  Every load is at most `214`.

For one color with `e` transverse lines, adjoin the `r` row lines, `t` column
lines, and the fixed endpoint line.  The arrangement degree is

```text
D=e+r+t+1<=245<p=2,130,706,433.                         (3)
```

If `k_P` is the number of transverse lines through selected point `P`, write

```text
I=sum_P k_P.
```

The exact arrangement ledger gives

```text
tau >= C(D,2)+C(r,2)+C(t,2)+sum_P C(k_P+1,2).           (4)
```

At fixed `I`, the last term is minimized by balancing the 131 integral
values.  This is the raw characteristic-valid DPW cap used below.

## 2. The all-profile post-stripping dichotomy

Let a minimal degree-`rho` projective logarithmic field have full zero divisor
of degree `h`.  The accepted stripping theorem says that this divisor is a
reduced union of exactly `h` arrangement lines.  After deletion, the remaining
arrangement has degree and exact mdr

```text
B=D-h,
q=rho-h.                                                (5)
```

The field has isolated zeros.  The following two branches exhaust every
`h=0..rho`.

### 2.1 Strict extactic branch

If `B>3q`, the accepted positive-characteristic extactic theorem makes the
remaining arrangement a pencil.  If the pencil is larger than
`max(r+1,t+1,2)`, its center is affine, so at most one row and one column
survive and

```text
h>=r+t-1.
```

The marked-incidence cap is then

```text
I <= e+130+(min(r,t)-1)(h-r-t+1).                       (6)
```

The right side and its transition to the trivial cap `I<=min(r,t)e` are
nondecreasing in `h`, so the verifier evaluates the worst endpoint exactly.

### 2.2 Isolated-field Chern/Tjurina branch

If `B<=3q`, every intersection of two remaining invariant lines is an
isolated zero.  A degree-`q` projective field is a section of
`T_(P^2)(q-1)`, whose top Chern length is

```text
q^2+q+1.                                                (7)
```

Therefore the number of distinct arrangement intersections is at most (7).

A deleted row or column contains at most 14 selected points, a deleted
transverse contains at most `min(r,t)`, and the endpoint line contains none.
Thus one deleted line removes at most

```text
ell=max(14,min(r,t))                                    (8)
```

selected incidences.  Across the 131 selected points, the remaining total
line multiplicity is at least

```text
S=I+2*131-h*ell.                                        (9)
```

For `f(m)=C(m-1,2)`, integral convexity gives the exact balanced known-point
excess

```text
E_min=F_131(max(0,S))
      +f(max(0,r+1-h))+f(max(0,t+1-h)).                (10)
```

For any arrangement point of multiplicity `m`, put

```text
E_x=C(m-1,2),
A_x=C(m,2)-1=E_x+(m-2)<=2E_x.                           (11)
```

Before deletion, the sum of `(m-2)` at selected points and endpoints is
`I+r+t-2`; deletion cannot increase it.  Combining (7), (10), and (11)
gives the exact safe lower bound

```text
tau >= C(B,2)+E_min
       +max(0,ceil((C(B,2)-(q^2+q+1)
                    -E_min-(I+r+t-2))/2)).              (12)
```

This must not exceed the accepted corrected DPW upper bound at exact `(B,q)`.
The predicate is not monotone in `I`, so the verifier descends through every
integer from the raw cap to zero.  It retains the frozen hostile regression

```text
D=32,rho=13,r=t=15,h=2:
tau_floor(I=0..15)=
650,650,649,649,648,648,647,647,
646,646,645,645,644,644,643,643.                        (13)
```

The isolated branch is exactly

```text
h=0..min(rho,floor((3rho-D)/2));                        (14)
```

every larger `h` going to the strict branch.  Equations (6)--(14) use `r`
and `t` separately and nowhere require `r=t`.  This is the load-bearing
all-profile extension.

## 3. Exact finite scan

For 131 selected points there are 28 legal grid profiles.  The verifier
checks

```text
c=0..832;
all 28 legal (r,t);
every balanced color load 0..214;
every rho=0..D-1;
every isolated deletion degree in (14);
the exact strict-pencil endpoint;
every integral marked incidence.
```

There are zero failures.  The unique minimum is

```text
c=0, d=5,116, b=62,356, R=13,
grid=13x13,
U=178d+2,985,
color caps Phi(178)=1,591, Phi(179)=1,600,
need=131*62,356=8,168,636,
capacity=(5,116-2,985)*1,591+2,985*1,600
        =8,166,421,
margin=2,215.                                           (15)
```

Hence no active pencil contains 131 neighbors:

```text
occupancy<=130.                                         (16)
```

The adjacent selected-130 scan fails already at the same core and profile:

```text
need=130*62,356=8,106,280,
capacity=8,135,725,
margin=-29,445.                                         (17)
```

Thus this exact relaxation stops sharply at (16); no cap 129 is claimed.

## Scope

This is a local active-pencil theorem.  It proves no active-hyperplane owner
bound, no rank-16 recurrence payment, and no official score change.

## Replay

```text
/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  work/verify_rank16_weighted_grid_extactic_dpw_cap130.py
```

The verifier hash-locks the two consumed source theorems, reconstructs every
all-profile cap, pins the full 833-row ledger hash, and replays the adjacent
selected-130 negative control.
