# Kneser and grid exclusion of the `q=14`, `B=42`, `D=60` cell

## Theorem

Under the literal `M=212`, `q=14`, `B=42`, `U=E=0` boundary hypotheses,
the reduced arrangement cannot have exactly 60 double points.

Together with the audited `D=39,44..59` payments, the next moment-feasible
double-count wall is `D=61`.

## 1. Exact profile census

With high-point weight `w=k-3`, the moment and line equations are

```text
sum w c_w=D-3,
sum w^2 c_w=471-D,
d_L=S_L-11,
t_L=26-S_L-s_L.                                      (1)
```

Exact moment enumeration gives 1,183 profiles at `D=60`.  The independently
audited per-point disjoint-group gate leaves exactly eight:

```text
[4^6,5^6,12,13^3],
[4^8,5^5,12^2,13,14],
[5^12,14^3],
[4^12,5^3,12^3,15],
[4^2,5^11,13,14,15],
[4^21,5,14^2,15],
[4^6,5^9,12,15^2],
[4^23,13,15^2].                                     (2)
```

For heavy weights at least nine, a line contains at most two heavy points.
Thus `I_9<=42+binom(B_9,2)`.  Rows 1,2,4 have four heavy points with total
incidence 51, exceeding 48.  Rows 3,5,7 have three heavy points with total
incidence 42, hence at most three no-heavy lines; their 12,11,9
multiplicity-5 points each need two no-heavy lines, while at most three
points can lie on two of three fixed lines.  These six rows are impossible.

## 2. The `[4^23,13,15^2]` row

Let `A` have multiplicity 13, let `B,C` have multiplicity 15, and let the
23 small points be `P_i`.  Heavy incidence is 43.  If `x,z` count lines with
two and zero heavy points, then `x-z=1` and `x<=3`.  Every `P_i` needs a
no-heavy line.  One no-heavy line cannot contain 23 small points by (1), so
`z=2,x=3`.

Call the no-heavy lines `L,M`.  If their intersection were not a `P_i`, the
23 points would each lie on exactly one of them.  After its two heavy sides,
`A` has only 11 lines, each meeting `L,M` in at most two small points, so it
could cover at most 22.  Therefore `P_0=L intersect M` is one of the small
points.

The point `P_0` has two remaining lines with which to meet three heavy
partners.  It must lie on a heavy-pair side.  It cannot lie on `BC`, since

```text
S+s=(12+12+1)+3=28>26.
```

Relabel so `P_0` lies on `AB`.  The 11 non-side lines through `A` must cover
the remaining 22 small points, forcing eleven perfect pairs between
`L\{P_0}` and `M\{P_0}`.  Hence both no-heavy lines contain twelve small
points.

The side `BC` has `d=13,t=0`.  Its thirteen remaining lines are precisely
the eleven `A`-low lines and `L,M`, so all their intersections with `BC` are
distinct doubles.  Every `A`-low line has `d=1`; its two small high points
and eleven triples therefore form a complete transversal of the same
`13 x 13` grid formed by the low pencils at `B,C`.

All lines are individually `F_p`-rational by parameter-point dualization.
Eleven distinct complete grid transversals give eleven ratios in the
stabilizer of a 13-set in `F_p^*`.  The stabilizer order divides 13, hence is
13, forcing `13 | (p-1)`.  But `(p-1) mod 13=10`.  This row is impossible.

## 3. The `[4^21,5,14^2,15]` skeleton

Let `A,B` have multiplicity 14, `C` multiplicity 15, `Q` multiplicity 5,
and let `P_1,...,P_21` have multiplicity 4.  Heavy incidence is again 43,
and `Q` forces exactly two no-heavy lines and all three heavy-pair sides.
Every `P_i` lies on exactly one no-heavy line and connects separately to all
three heavy points.  Equation (1) forces the split

```text
10+11.                                                  (3)
```

The low pencils at `A,B` each have 12 lines: the `Q` connector, ten paired
small-point connectors, and one singleton connector.  The low pencil at
`C` has 13 lines.  Together with the three sides and two no-heavy lines this
is exactly 42 lines.

## 4. A `12 x 12` correlation overload

Let `U,V subset F_p^*`, `|U|=|V|=12`, parameterize the low pencils at `A,B`
after moving the heavy triangle to the coordinate triangle.  For a low line
through `C`, the number of `A-B` grid points on it is the multiplicative
correlation

```text
r(m)=|U intersect mV|.                                  (4)
```

The 13 low `C`-lines give 13 distinct parameters.

If one such line contains `r` small `P` points and contains `Q` with
indicator `q`, (1) gives

```text
t=13-2r-3q.
```

Summing over the `C` pencil, using 21 total `P` points and one `Q`, gives

```text
sum_C t=13*13-2*21-3=124.                              (5)
```

Every one of the 22 low high points (`P_i` and `Q`) is already an `A-B` grid
point on its `C` line.  A triple on a `C`-low line which is not an `A-B` grid
triple must use one of the only ordinary external lines `AB,L,M`: two
distinct `A`-low lines meet at `A`, two distinct `B`-low lines meet at `B`,
and `AC,BC` meet all `C` lines at the heavy point `C`.  From (1),

```text
t_AB=2, t_L=3, t_M=1.
```

Thus at most six of the 124 triples are non-grid.  The thirteen correlations
in (4) satisfy

```text
sum_selected r(m)>=22+(124-6)=140.                     (6)
```

On the other hand the complete correlation identity is

```text
sum_(m in F_p^*) r(m)=|U||V|=144.                      (7)
```

Therefore the quotient set `UV^{-1}` has size at most 17.

Let `H` be the stabilizer of `UV^{-1}` and `h=|H|`.  Kneser's theorem gives

```text
|UV^{-1}| >= |UH|+|VH|-h
            >= 2h ceil(12/h)-h.                        (8)
```

Since

```text
p-1=2^24*127,
```

the possible divisor values `h<=17` are `1,2,4,8,16`.  The lower bounds in
(8) are respectively

```text
23,22,20,24,16.
```

Only `h=16` can survive `|UV^{-1}|<=17`.  Because the quotient set is a union
of `H`-cosets, it then has size 16, and (8) forces both `U,V` to lie in single
`H`-cosets.  Every one of the 16 correlations is consequently at least

```text
12+12-16=8.
```

The thirteen selected correlations can sum to at most

```text
144-3*8=120,
```

contradicting (6).  This excludes the last row and proves the theorem.

## Scope

The theorem pays only `D=60` in the two aggregate `q=14,B=42,U=E=0` rows.
It does not pay `D>=61` and makes no recurrence claim by itself.

