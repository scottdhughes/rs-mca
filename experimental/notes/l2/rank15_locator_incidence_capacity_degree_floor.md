# Rank-15 locator incidence-capacity degree floor

**Status:** PROVED under the imported rank-15 locator-saturation normal form.

## Result

This note consumes the actual affine two-flat state and notation of
`experimental/notes/thresholds/rank15_locator_saturation_normal_form.md`.
In particular, it assumes the imported proper-section cap `q = 15`, the
literal active coordinate sections

```text
ell_x = {(s,t) : s A(x) + t B(x) = omega_x},
h_x   = |S intersect ell_x|,
```

and the source normal-form inequalities. It does not replace these sections
by a formal profile, support shadow, or catalogue surrogate.

### Theorem (deployed `M = 218` degree floor)

For the deployed residual state

```text
N = 1,053,556,
a = 72,451,
M = 218,
q = 15,
W_218 = 1,044,534,
```

every `M = 218` survivor of the imported rank-15 locator-saturation normal
form has

```text
d >= 4,828.
```

Thus all 36 layers `4,792 <= d <= 4,827` are impossible. In particular, the
source's first residual branch

```text
M = 218, d = 4,792, t = b = 218, 0 <= r <= 8
```

is impossible.

At the first unexcluded degree `d = 4,828`, every survivor must satisfy

```text
t = b = 218,
r <= 151,
8 r + 7 delta + eta <= 1,658,
deg(E) <= 7,970 - 14 r,
Q_T^105 divides Psi_S,
```

where

```text
delta = 218 * 4,828 - E_15,
eta   = sum_{x : h_x < 15} (8 - h_x).
```

The theorem is field-uniform once the imported normal form holds: it uses
only incidence geometry, degree bounds, and integer determinants. It does not
use the cyclic identity `L_H = X^n - 1`.

## Incidence-capacity lemma

Call a parameter-plane line *rich* when it contains 15 listed points. Let
`G` be the graph on the `M` listed points in which two points are adjacent
exactly when their pair lies on no rich line. Suppose `G` has maximum degree
`Delta`.

Every non-rich coordinate section has occupancy at most `Delta + 1`. Indeed,
two points on a non-rich coordinate line cannot also lie on a rich line,
because two affine points determine a unique line. Therefore all pairs in a
non-rich section are edges of `G`. Since a non-rich section also has
occupancy below 15, put

```text
s = min(Delta + 1, 14).
```

Let `E_15` be the number of active coordinates with occupancy 15. If there
are `t` rich projective directions and every corresponding pencil member has
degree at most `d`, then

```text
E_15 <= t d.
```

The literal agreement incidence therefore obeys

```text
M a <= s(N - r) + (15 - s)t d.                           (1)
```

The coefficient `15 - s` is nonnegative, so substituting `E_15 <= td` has
the displayed direction for every `Delta`. This is an aggregate bound on the
actual coordinate sections. In the deployed branch `Delta = 7`, hence `s=8`.

## Proof of the assigned branch

When `b = t = 218`, the rich-line incidence count is `218 * 15`. A point lies
on at most 15 rich lines: the 14 other points on distinct rich lines through
it are disjoint. Equality in the total incidence count forces every point to
lie on exactly 15 rich lines. Those lines cover `15 * 14 = 210` other points,
so every point has exactly `217 - 210 = 7` uncovered neighbors.

Thus `G` is 7-regular and every non-rich coordinate section has occupancy at
most 8. Equation (1) gives

```text
M a <= 8(N - r) + 7 t d.
```

At `d = 4,792` the right side is

```text
8(1,053,556 - r) + 7(218)(4,792)
  = 15,741,040 - 8r,
```

whereas

```text
M a = 218(72,451) = 15,794,318.
```

The deficit is `53,278 + 8r`, a contradiction for every `r >= 0`.

## One-deficient rich-line family

Suppose `b = t = 217`. If `k_p` denotes the number of rich lines through a
listed point `p`, then `k_p <= 15` and

```text
sum_p (15 - k_p) = 15.
```

The deficiency set `D = {p : k_p < 15}` has at most 15 points. Every point
outside `D` still has uncovered degree 7. Hence any non-rich line of occupancy
at least 9 is contained in `D`. There can be at most one such line, since two
distinct 9-point lines would place at least `9 + 9 - 1 = 17` points in `D`.
Its coordinate multiplicity is at most `d`. All remaining non-rich sections
have occupancy at most 8. Consequently,

```text
sum_x h_x <= 8(N - r) + 7(217)d + 6d
             = 8(N - r) + 1,525d.                       (2)
```

## Elimination through `d = 4,826`

The imported rich-fiber coverage inequality is

```text
t d >= W_218 + 14r,       W_218 = 1,044,534.             (3)
```

For `d <= 4,826`, `216d < W_218`, so `t >= 217`. Since
`t <= b <= 218`, only the `b = 218` and `b = t = 217` cases remain.

For `b = 218`, the 7-regular bound, even with `t = 218`, gives

```text
sum_x h_x <= 8N + 7(218)(4,826)
           = 15,792,924 < 15,794,318.
```

For `b = t = 217`, (2) gives

```text
sum_x h_x <= 8N + 1,525(4,826)
           = 15,788,098 < 15,794,318.
```

Hence `d >= 4,827`.

## The borderline layer `d = 4,827`

Equation (3) again forces `t >= 217`. The branches with `t = 217` fail:

```text
b = 218:      8N + 7(217)(4,827) = 15,760,661,
b = t = 217:  8N + 1,525(4,827)  = 15,789,623.
```

Thus a putative survivor has `t = b = 218`. Write `e_l` for the coordinate
multiplicity of a rich line and set

```text
delta = sum_{l rich} (4,827 - e_l),
eta   = sum_{x non-rich} (8 - h_x).
```

The exact incidence identity becomes

```text
sum_x h_x = M a + 132 - (8r + 7 delta + eta),
```

so a survivor requires

```text
8r + 7 delta + eta <= 132.                               (4)
```

Every listed point receives at most `15 * 4,827 = 72,405` agreements from
rich lines, but it needs `a = 72,451`. It therefore needs at least 46
non-rich incidences. More precisely, with

```text
epsilon_p = sum_{l contains p} (4,827 - e_l),
```

point `p` needs at least `46 + epsilon_p` non-rich incidences and
`sum_p epsilon_p = 15 delta`.

### Forcing 25 or 26 disjoint `K_8` components

An 8-point non-rich line is a `K_8` in the 7-regular uncovered graph. It is
therefore an entire connected component, and distinct such lines are
disjoint. If there are `c` such components and `v = 218 - 8c` residual
vertices, every residual vertex requires at least 46 non-rich incidences.
Every coordinate section meeting a residual vertex has occupancy at most 7
and contributes at least one unit to `eta`. Therefore

```text
46v <= 7 eta <= 7(132),
```

so `v <= 20`. A 7-regular residual graph cannot have two vertices. Hence
`c` is 25 or 26.

### Excluding 26 components by an integer-square determinant

For `c = 26`, the residual uncovered graph `R` has ten vertices and is
7-regular. Let `B_inc` be the square point-rich-line incidence matrix. Its
row and column sums are 15, and

```text
B_inc B_inc^T = 14 I + J - A_G.                           (5)
```

The determinant of (5) must be the integer square `det(B_inc)^2`. Since
`G = 26 K_8 disjoint-union R`, the matrix determinant lemma yields

```text
det(14 I + J - A_G)
  = 225 * 7^25 * 15^182 * det(14 I_10 - A_R).             (6)
```

The complement of `R` is 2-regular. Its possible cycle partitions are

```text
10, 7+3, 6+4, 5+5, 4+3+3.
```

Exact Bareiss determinants give respectively

```text
7 * 11^2 * 13 * 19^2 * 239^2,
2^2 * 7^3 * 17 * 3121^2,
2^10 * 3^2 * 5^2 * 7^3 * 13^2 * 17,
7 * 11^4 * 17 * 19^4,
2^4 * 3^2 * 5^2 * 7^5 * 13 * 17^2.
```

After multiplication by the prefactor in (6), an odd valuation remains at
13 or 17 in every case. The determinant is not a square, contradicting (5).

### Excluding 25 components by residual clique capacity

For `c = 25`, the residual set `R` has 18 vertices and induces a 7-regular
graph. A non-rich section meeting `R` lies wholly inside `R` and has occupancy
at most 7. Let `q_R` be the number of such sections. The required 828 residual
incidences give `q_R >= 119`. Equation (4) then gives

```text
8r + 7 delta <= 13,
```

so `(r, delta)` is one of `(0,0)`, `(1,0)`, `(0,1)`. Counting the 9,200
non-rich incidences required by the 200 points in the `K_8` components gives
`q_R <= 121` in all three cases.

A 7-point non-rich line is a `K_7`. Two distinct such lines cannot share a
vertex, because the shared vertex would then have at least 12 uncovered
neighbors. Thus there are at most two. If their number is `k = 0,1,2`, the
remaining `18 - 7k` vertices can only be covered by sections of occupancy at
most 6. Even using 121 sections, the maximal residual incidences are

```text
k = 0: 709,
k = 1: 762,
k = 2: 816.
```

All are below 828. This excludes `c = 25`, completes the contradiction at
`d = 4,827`, and proves `d >= 4,828`.

## First residual state

At `d = 4,828`, (3) forces `t >= 217`. Both `t = 217` branches still fail:

```text
b = 218:      8N + 7(217)(4,828) = 15,762,180,
b = t = 217:  8N + 1,525(4,828)  = 15,791,148.
```

Therefore `t = b = 218`. The imported degree/gcd ledger gives
`r <= 4,979 - 4,828 = 151`. The remaining aggregate incidence room is

```text
8N + 7(218)(4,828) - M a = 1,658,
```

and `218(4,828) - W_218 = 7,970`, giving the displayed constraints.

## Verification

`experimental/scripts/verify_rank15_locator_incidence_capacity_degree_floor.py`
replays all load-bearing arithmetic, constructs the five ten-vertex residual
matrices, computes their determinants by fraction-free Bareiss elimination,
checks prime valuations, and verifies the residual clique-cover table. It uses
explicit failures rather than `assert`, so normal and optimized Python runs
have identical semantics.

## Nonclaims and exact remaining wall

This theorem does not prove `M <= 217`, let alone the required uniform ceiling
`M <= 211`. It does not eliminate `M = 218` for `d >= 4,828`, assert that the
first residual state is realizable, eliminate `M = 217,...,212`, close the
other rank-15 sectors, control affine rank at least 16, change the current
statewise recurrence endpoint, prove the deployed one-row target, or solve
Grand List or Grand MCA.

The next exact target is

```text
M = 218, d = 4,828, t = b = 218, r <= 151,
G 7-regular on 218 vertices with 763 edges,
8r + 7 delta + eta <= 1,658,
deg(E) <= 7,970 - 14r,
Q_T^105 divides Psi_S.
```

It is a weighted 7-regular clique-cover/pencil system, not the eliminated
degree-4,792 correction branch.
