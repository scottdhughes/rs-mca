# Hostile audit 4: rank-16 all-profile weighted-grid/extactic cap 130

## Verdict

```text
PASS AS AN EXACT SOURCE-VALID LOCAL THEOREM
EVERY SURVIVING FIXED-PAIR ACTIVE PENCIL HAS OCCUPANCY AT MOST 130
UNIFORM FOR EVERY CORE 0<=c<=832
ALL 28 SELECTED-131 GRID PROFILES, INCLUDING EVERY NONSQUARE PROFILE, PASS
THE SELECTED-130 13x13 NEGATIVE CONTROL FAILS WITH MARGIN -29,445
NO ACTIVE-HYPERPLANE OWNER THEOREM
NO RANK-16 PARENT PAYMENT OR OFFICIAL SCORE CHANGE
```

I read the cap-130 theorem and claimant verifier in full, together with both
theorem objects it consumes and the hostile audits of the
DPW/extactic and stripped-field Chern/Tjurina inputs.  The claimant replay
byte-matches its expected output under both normal and optimized Python.
The attached Ruby audit does not import claimant code.  It reconstructs the
all-profile scan, pins the source and claimant objects, and byte-matches its
own frozen expected output with warnings enabled.

## 1. Exact source quantifiers

The fixed-pair theorem supplies the following facts for every literal core
`0<=c<=832`, not only for the earlier square-profile rows:

```text
d=5,116-c,
b=62,356+c,
U=913,633,
sum_P |T_P| >= 131b,
|union_P T_P| <= U.
```

The `T_P` are complete actual received-word agreement tails.  Selecting an
arbitrary 131 neighbors therefore introduces neither a support-reselection
quantifier nor an unowned coordinate.  The chosen neighbors form a simple
row-column graph, every row and column degree is at most 14, and

```text
r,t <= floor((72,588-c)/(5,116-c))-1.
```

The exact ceilings are 13 on `c=0..296`, 14 on `c=297..617`, and 15 on
`c=618..832`.  A transverse tail line contains at most `min(r,t)` selected
points, and one primitive direction owns at most `d` coordinate copies.
These are precisely the hypotheses used by the cap-130 argument.

## 2. Weighted-to-reduced coloring and all-profile dispatch

Coloring each primitive-direction class injectively among `d` colors and
always choosing least-loaded colors makes the color loads differ by at most
one.  A geometric line has one primitive direction, so every color is a
genuinely reduced line arrangement.  The fixed endpoint line, the `r` row
lines, and the `t` column lines are distinct from all transverse tail lines.

For 131 selected points the exact degree-14/simple-grid necessary conditions
give 28 ordered pairs `(r,t)`.  They include nonsquare pairs.  The claimant
and independent audit apply the stripped-field refinement to all 28 pairs;
there is no weaker nonsquare-profile dispatch.

For an actual union size `M<=U`, the balanced color loads are `e` and `e+1`.
At fixed `e` the sum of the two one-color caps is affine in the number of
high colors.  Thus its maximum over every possible remainder occurs at one
of the two endpoints checked by both replays.  This remains valid even if a
one-color relaxation is nonmonotone in `e`; no assumption of monotonicity is
used.

## 3. Characteristic and branch audit

One color has arrangement degree

```text
D=e+r+t+1 <= 214+15+15+1 = 245 < p=2,130,706,433.
```

Every original and stripped degree and every local line multiplicity is
therefore nonzero in the literal characteristic.  The ordinary multiple-point
Tjurina formula, Euler subtraction, the vector-bundle DPW bound, and the
degree-`q<p` extactic lemma all meet their printed hypotheses.  No
Hirzebruch/BMY or characteristic-zero transfer occurs.

If a minimal degree-`rho` logarithmic field has divisorial zero, the accepted
two-sided mdr comparison forces that divisor to be a reduced union of exactly
`h` arrangement lines.  The remaining arrangement has

```text
B=D-h, q=rho-h
```

and the remaining field has isolated zeros.  The dichotomy is exhaustive:

```text
B<=3q  iff  0<=h<=floor((3rho-D)/2),
B>3q   for every larger h<=rho.
```

The audit independently scans every isolated value of `h`.  On the strict
branch the incidence cap is nondecreasing in `h`, so the worst endpoint is
`h=rho`; the audit separately verifies in every original `D>3rho` cell that
`D-rho>max(r+1,t+1,2)`, including zero transverse load.  When a later strict
pencil is small enough to fit at a point of the fixed line, the replay uses
the trivial geometric cap.  Hence no pencil-center case is omitted.

## 4. Deleted-line and Chern/Tjurina payment

A deleted row or column contains at most 14 selected points, a deleted
transverse at most `min(r,t)`, and the endpoint line none.  Therefore one
deleted divisor line removes at most

```text
ell=max(14,min(r,t))
```

selected line incidences.  This is particularly important for the `15x15`
profile, where `ell=15`, not 14.  Across the 131 selected points, the remaining
total line multiplicity is at least

```text
I+262-h*ell.
```

Balancing this quantity gives the correct convex lower floor for
`sum binom(m-1,2)`.  Independently allowing all `h` deleted lines to lower
each endpoint multiplicity gives a weaker, hence safe, endpoint floor.

Every intersection of two remaining invariant lines is a zero of the
isolated projective field.  The top Chern length is `q^2+q+1`, so the number
of distinct remaining arrangement intersections is at most that number.
For a multiplicity-`m` intersection,

```text
E=binom(m-1,2),
A=binom(m,2)-1=E+(m-2)<=2E.
```

Before deletion, the known selected points and endpoints have total
`sum(m-2)=I+r+t-2`; deletion cannot increase it.  These statements reproduce
the claimant's residual Tjurina floor with the correct signs.

The floor is not monotone in `I`.  Both replays retain the hostile regression

```text
D=32, rho=13, r=t=15, h=2:
650,650,649,649,648,648,647,647,
646,646,645,645,644,644,643,643.
```

Consequently both descend through every integral incidence from the raw cap
to zero.  No binary inversion is used.

## 5. Independent exact replay

The Ruby reconstruction checks all 28 profiles, every load `0..214`, every
integer mdr, every isolated deletion degree, the strict-pencil endpoint, and
all 833 core rows.  It obtains zero failures.  The unique minimum is

```text
c=0, grid=13x13,
loads 178/179 with 2,985 high colors,
one-color caps 1,591/1,600,
need 8,168,636,
capacity 8,166,421,
margin 2,215.
```

Therefore 131 neighbors are impossible and the local occupancy is at most
130.  The independent `selected=130`, `c=0`, `13x13` negative control gives

```text
need 8,106,280,
capacity 8,135,725,
margin -29,445.
```

This only shows that this exact relaxation stops at 130; it does not realize
a source counterexample with 130 neighbors.

## Frozen hashes and replay

```text
cap-130 theorem
166e3947422fab3024ca99e4022d6d61e7b0c64a416a16abc533f4bfa96e23e2

cap-130 claimant verifier
3e5f4f3ee3a313db07ee314393bba5db9478d0ba3e360744b27e00a514400e9f

cap-130 claimant expected output
94929ecbd4b7b5d93677a3d2c6a9a4116de4c0cebb11e0877d5259b29a1000d3

independent audit verifier
1bc99e3a567bd0e0761b545b8e9279a9d10fe24042d596293c40b31bf535f490

independent audit expected output
aef940238ed78bee247250d41069b0e91058c0db7579942a58cf0a32aa6703e6
```

```text
/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  work/verify_rank16_weighted_grid_extactic_dpw_cap130.py

/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -O -B \
  work/verify_rank16_weighted_grid_extactic_dpw_cap130.py

/usr/bin/ruby --disable-gems -w \
  work/audit4_dch_rank16_weighted_grid_extactic_dpw_cap130.rb
```

## Scope

This audit accepts only the uniform local fixed-pair active-pencil occupancy
cap 130.  It proves no active-hyperplane owner bound, does not eliminate the
rank-16 parent state, supplies no recurrence payment, and changes neither
official score.
