# Exclusion of the `q=14`, `B=42`, `D=46..58` boundary band

## Theorem

Assume the literal `M=212` rank-15 source reduction produces a reduced
arrangement of 42 projective lines with exact minimal syzygy degree 14 and
boundary data

```text
U=E=0,
R=14^2+14+1=211.
```

Then its number `D` of double arrangement points does not lie in

```text
46<=D<=58.
```

Together with the separately audited `D=39,44,45` theorems, the next exact
double-count wall in this `q=14,B=42` cell is `D=59`.

## 1. Weighted high-point identities

The boundary theorem gives exactly 15 distinct intersections on every line.
At a point of multiplicity `k>=4`, put

```text
w=k-3,              1<=w<=12.
```

All such points are marked and hence `k<=15`: the first aggregate residual
row has one unmarked point of multiplicity exactly two, and the second has no
unmarked point.

For a line `L`, let `S_L` be the sum of the weights of its high points, let
`s_L` be their number, and let `d_L,t_L` count double and triple points.  The
support and other-line incidence equations give

```text
d_L=S_L-11,
t_L=26-S_L-s_L.                                      (1)
```

Thus every line satisfies

```text
S_L>=11,
S_L+s_L<=26.                                         (2)
```

Globally, fixing `D` and deleting the double and triple baselines turns the
three arrangement moments into

```text
sum_w w c_w=D-3,
sum_w w^2 c_w=471-D,                                 (3)
```

where `c_w` is the number of high points of weight `w`.  Conversely the
number of triples is `211-D-sum c_w`, so the nonnegative solutions of (3),
with that count constraint, are the complete moment profiles.

## 2. Exact per-point disjoint-group gate

Fix a high point `P` of weight `w<=10`.  Each of its `k=w+3` incident lines
must receive other high-point weight at least `11-w`.  Distinct lines through
`P` use disjoint sets of other high points, because a second shared point
would make the two projective lines equal.

A point of weight at least 11 can support at most one of these lines.  For
the other points of weights 1 through 10, let `g_P` be the exact maximum
number of disjoint groups, each of total weight at least `11-w`.  Therefore
the necessary condition is

```text
w+3 <= B_big+g_P,                                     (4)
```

where `B_big` is the number of other weight-11-or-12 points.

The verifier computes `g_P` exactly.  Every group in an optimum may be
shrunk to an inclusion-minimal group.  Such a group has total weight at most
`(11-w)+9`.  All minimal count vectors are enumerated, and memoized dynamic
programming packs disjoint copies.  No floating point or external solver is
used.

The complete census is

```text
D    profiles satisfying (3)    survivors of (4)
46             6                         0
47            12                         0
48            21                         0
49            30                         0
50            55                         1
51            76                         0
52           107                         0
53           180                         0
54           237                         0
55           315                         1
56           444                         1
57           557                         3
58           720                         3.                         (5)
```

Thus only the eight profiles treated below remain.

## 3. The unique `D=50` profile and its rigid skeleton

The profile is

```text
[4^12,14,15^2].                                       (6)
```

Call the twelve multiplicity-4 points `P_i` and the three big points
`A,B,C`, with multiplicities 14,15,15.  At each `P_i`, (4) is equality:
its four lines consist of one line to each big point and one small-only line
containing at least ten other `P` points.  Fixing one such line shows that it
contains at least eleven of the twelve `P` points.  If it missed `P_j`, the
small-only line through `P_j` would share at least ten points with it, so the
two lines would be equal and would contain `P_j`, contradiction.  Hence all
twelve `P_i` lie on one line.

All 36 connectors `AP_i,BP_i,CP_i` are present.  The big points cannot be
collinear.  If they were, after the common `P` line, the 36 connectors, and
the big line, their remaining required incidences would need one singleton
line at `A` and two each at `B,C`, for 43 arrangement lines.  Thus they form
a triangle.  The 42 lines are exactly

```text
the common P-line;
36 connectors;
the three triangle sides;
one additional B-line and one additional C-line.       (7)
```

Equation (1) gives the double degrees

```text
15 lines of degree 1,
24 lines of degree 2,
two lines of degree 12,
one line of degree 13.                                  (8)
```

In particular the side `BC` has only the two high points `B,C`, double
degree 13, and exactly 13 remaining arrangement lines: the twelve `AP_i`
and the common `P` line.  Since it has 15 distinct support points, all 13
remaining intersections are distinct doubles.  Hence every `a_i=AP_i` uses
its sole double at `BC`.  Its other 12 ordinary support points are triples.

Let

```text
X={BP_i:1<=i<=12} union {the extra B-line},
Y={CP_i:1<=i<=12} union {the extra C-line}.              (9)
```

These are two 13-line pencils.  Each `a_i` contains `P_i=BP_i intersect CP_i`
and its twelve triple points.  Its 24 remaining ordinary line incidences are
exactly the other 12 members of `X` and the other 12 members of `Y`.  Two
members of one pencil cannot meet on `a_i`, since their center is not on
`a_i`; therefore each triple pairs one `X` line with one `Y` line.  Thus
`a_i` contains 13 `X-Y` grid points.

The entire skeleton is individually `F_p`-rational by the literal source
transport.  Move the rational triangle `A,B,C` to the coordinate triangle.
Parameterize `X,Y` by 13-element sets `U,V subset F_p^*`.  A line through
`A` of slope `m` contains all 13 grid points exactly when

```text
U=mV.                                                     (10)
```

The twelve distinct `a_i` therefore give twelve distinct elements
`m_i/m_1` in the stabilizer `H={h:hV=V}`.  The free action of `H` on `V`
shows `|H|` divides 13, while `|H|>=12`; hence `|H|=13` and
`13 | (p-1)`.  But for `p=2,130,706,433`,

```text
(p-1) mod 13=10.                                         (11)
```

This excludes `D=50`.

## 4. Heavy-incidence and no-heavy-line gates

Call weights at least nine *heavy*.  Equation (2) allows at most two heavy
points on one line.  If there are `B_9` heavy points with total arrangement
incidence `I_9`, and `x,y,z` lines contain respectively two, one, zero heavy
points, then

```text
2x+y=I_9,
x+y+z=42,
x<=binom(B_9,2).
```

Therefore

```text
I_9<=42+binom(B_9,2).                                    (12)
```

The `D=55` and `D=56` survivors are

```text
[4^8,5^2,13^4],
[4^11,5,13^4].                                          (13)
```

In both, the four multiplicity-13 points have `I_9=52`, while (12) gives
at most `42+binom(4,2)=48`.  Both are impossible.

At `D=57`, the first survivor `[4^14,13^4]` dies by the same inequality.
The other two are

```text
[4^12,5^4,14^2,15],
[4^14,5^3,13,15^2].                                    (14)
```

Their three heavy points have total incidence 43.  Thus `x=z+1` and
`x<=3`, so at most `z=2` lines contain no heavy point.  A multiplicity-5
point has only three heavy partners, hence at least two of its five lines
contain no heavy point.  Two projective lines have at most one common point,
so at most one multiplicity-5 point can lie on both no-heavy lines.  The
profiles in (14) have four and three such points.  Contradiction.

The three `D=58` survivors are

```text
[4^15,5^3,14^2,15],
[5^11,12,15^2],
[4^17,5^2,13,15^2].                                    (15)
```

In the first and third profiles the three heavy points have total incidence
43, so there are at most two no-heavy lines; three or two multiplicity-5
points cannot all lie on both.  In the middle profile the heavy incidence is
42, so `x=z<=3`.  A point lying on at least two of three fixed lines can be
charged to one pair of those lines; each line pair has only one intersection.
Thus at most `binom(3,2)=3` points can each lie on two no-heavy lines, not
the eleven in (15).  This excludes `D=58` and proves the theorem.

## Scope

This is an exact payment of `D=46..58` inside the two aggregate
`q=14,B=42,U=E=0` rows only.  It does not pay `D=59`; the local packing scan
leaves three `D=59` profiles, and the first unresolved one after elementary
heavy-line cuts is `[4^20,5,13,15^2]`.

