# Correlation exclusion of the `q=14`, `B=42`, `D=61` cell

## Theorem

Under the literal `M=212`, `q=14`, `B=42`, `U=E=0` boundary hypotheses,
the reduced arrangement cannot have exactly 61 double points.

Together with the frozen `D=39,44..60` payments, the next moment-feasible
double-count wall is `D=62`.

## 1. Exact profile census and nine immediate exclusions

For a point of multiplicity `k>=4`, put `w=k-3`.  The exact moment and line
equations are

```text
sum w c_w = D-3,
sum w^2 c_w = 471-D,
d_L = S_L-11,
t_L = 26-S_L-s_L.                                    (1)
```

Here `S_L` is the sum of the high-point weights on `L`, `s_L` is their
number, and `d_L,t_L` are the numbers of double and triple points on `L`.
Exact moment enumeration gives 1,458 profiles at `D=61`.  The frozen exact
disjoint-group gate leaves precisely ten:

```text
[4^9,5^5,12,13^3],
[4^12,5^2,6,12,13^3],
[5^7,6^2,12^3,14],
[4^11,5^4,12^2,13,14],
[4^14,5,6,12^2,13,14],
[4^3,5^11,14^3],
[4^15,5^2,12^3,15],
[4^5,5^10,13,14,15],
[4^24,14^2,15],
[4^9,5^8,12,15^2].                                  (2)
```

Call points of multiplicity at least 12 heavy.  A line contains at most two
heavy points.  If there are `H` heavy points, their total line incidence is
at most

```text
42 + binom(H,2),                                      (3)
```

because every incidence beyond the first on a line pays a distinct heavy
pair.  Rows 1,2,4,5,7 have heavy incidence 51, and row 3 has heavy incidence
50; all exceed the four-heavy ceiling 48.

Rows 6,8,10 have three heavy points and total heavy incidence exactly 42.
If `x,z` count lines containing two and zero heavy points, respectively,
then `x=z<=3`.  A multiplicity-5 point needs at least two no-heavy lines.
Among at most three fixed lines, at most three points can each lie on two of
them.  The three rows have respectively 11,10,8 multiplicity-5 points, so
they too are impossible.  Thus only

```text
[4^24,14^2,15]                                       (4)
```

remains.

## 2. Geometry of the last row

Let `A,B` have multiplicity 14, let `C` have multiplicity 15, and let
`P_1,...,P_24` have multiplicity 4.  The heavy incidence is 43.  With `x,z`
as above, `x-z=1` and `x<=3`.  Every `P_i` needs a no-heavy line, while one
no-heavy line cannot contain all 24 because (1) would give negative `t_L`.
Consequently `z=2,x=3`; call the no-heavy lines `L,M`.  All three heavy-pair
sides `AB,AC,BC` occur, and every small point lies on `L union M`.

The sides `AC,BC` cannot contain a small point, since their `S_L+s_L` would
be 27.  The side `AB` can contain at most one.  Moreover, a small point on
`AB` has only two distinct heavy connectors, so its other two lines must be
both `L` and `M`.  Thus a side-small point exists exactly in the second case
below, at `L intersect M`.

There are two exhaustive cases.

### Case I: `L intersect M` is ordinary

Every small point lies on exactly one of `L,M`.  The twelve low lines at
`A` must cover all 24 points, with at most one point from each of `L,M` on
each line.  Hence every such line contains a pair and the split is `12+12`.
The same holds at `B`.  The low pencils at `A,B,C` have sizes `12,12,13`.

Move the heavy triangle to the coordinate triangle and parameterize the
low pencils at `A,B` by sets `U,V subset F_p^*`, with `|U|=|V|=12`.  On a
low line through `C`, the number of `A-B` grid points is

```text
r(m)=|U intersect mV|.                                (5)
```

The thirteen low `C`-lines have distinct parameters.  If such a line
contains `r` small high points, (1) gives `t=13-2r`; summing over the `C`
pencil gives

```text
sum_C t = 13*13-2*24 = 121.                           (6)
```

All 24 small high points are `A-B` grid points.  Any triple on a `C`-low
line which is not an `A-B` grid triple must use one of the only external
lines `AB,L,M`.  Their triple capacities from (1) are `2,2,2`.  Therefore
the thirteen selected correlations satisfy

```text
sum_selected r(m) >= 24+(121-6)=139.                  (7)
```

The complete correlation identity is

```text
sum_(m in F_p^*) r(m)=|U||V|=144.                     (8)
```

Thus `|UV^{-1}|<=13+(144-139)=18`.  If `H` is its stabilizer and `h=|H|`,
Kneser's theorem yields

```text
|UV^{-1}| >= 2h ceil(12/h)-h.                         (9)
```

Since `p-1=2^24*127`, the only possible `h<=18` are `1,2,4,8,16`; the
lower bounds in (9) are `23,22,20,24,16`.  Only `h=16` survives.  The
quotient set is then one `H`-coset, both `U,V` lie in `H`-cosets, and every
one of the 16 correlations is at least `12+12-16=8`.  The thirteen selected
ones sum to at most `144-3*8=120`, contradicting (7).

### Case II: `P_0=L intersect M` is a small point

The two no-heavy lines contain 12 and 13 small points, since their sizes sum
to 25 and (1) caps each at 13.  The point `P_0` already lies on `L,M` and
must meet the three heavy points on only two further lines, so it lies on a
heavy-pair side.  It cannot lie on `AC` or `BC`, because there
`S_L+s_L=(1+11+12)+3=27>26`.  Hence `P_0` lies on `AB`, where equality 26
holds.

The same low-pencil parameterization has `|U|=|V|=12`.  Exactly 23 of the
small points are `A-B` grid points.  Formula (6) remains `121`, because all
24 small points lie on the `C` pencil.  Now the external triple capacities
are

```text
t_AB=0,  {t_L,t_M}={0,2}.
```

Therefore

```text
sum_selected r(m) >= 23+(121-2)=142.                 (10)
```

Equations (8) and (10) give `|UV^{-1}|<=13+(144-142)=15`.  But every
possible stabilizer order `h<=15` is one of `1,2,4,8`, whose Kneser lower
bounds are respectively `23,22,20,24`.  This final case is impossible.

The proof uses only the literal prime field.  The low-pencil parameters are
`F_p`-rational because the source arrangement lines are individually
`F_p`-rational under parameter-point dualization.

## Scope

The theorem pays only `D=61` in the two aggregate `q=14,B=42,U=E=0` rows.
It does not pay `D>=62` and makes no recurrence claim by itself.
