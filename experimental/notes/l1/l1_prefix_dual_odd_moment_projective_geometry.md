# L1 Prefix Dual Odd-Moment Projective Geometry

Date: 2026-06-26

## Purpose

This note upgrades the affine torus collision geometry to the projective
complete-intersection geometry needed for a singular-locus-sensitive
Hooley-Katz/Ghorpade-Lachaud point-count audit.

It does not count proper-subgroup points.  The projective theorem is an
untwisted full-field geometry statement.

## Setup

Let `K` be algebraically closed of characteristic zero or characteristic
`p>2d-1`.  Let `k>d>=1`.  In

```text
P^{2k-1} = Proj K[x_1,...,x_k,y_1,...,y_k],
```

define `Y_{d,k}` by the homogeneous equations

```text
F_r = sum_{i=1}^k x_i^{2r-1} - sum_{i=1}^k y_i^{2r-1} = 0,
1 <= r <= d.
```

## Theorem

For `k>d`, `Y_{d,k}` is a geometrically integral projective complete
intersection of dimension

```text
2k-d-1.
```

Its singular locus is the projective collision-map critical locus, and

```text
dim Sing(Y_{d,k}) <= d-2.
```

No irreducibility claim is made for `k=d`.

## Proof

The Jacobian matrix has entries

```text
dF_r/dx_i = (2r-1)x_i^{2r-2},
dF_r/dy_i = -(2r-1)y_i^{2r-2}.
```

The factors `2r-1` are invertible in the stated characteristic range.  Thus
each column is, up to sign, a Vandermonde column in the square coordinate.
For a projective point,

```text
rank J = min(d, #{x_1^2,...,x_k^2,y_1^2,...,y_k^2}),
```

where zero is allowed as one square value.

The rank drops exactly when the `2k` homogeneous coordinates use at most
`d-1` distinct square values.  A stratum with exactly `r` square values is
determined by:

- a partition of the coordinate positions into at most `r` classes;
- finitely many sign choices inside the nonzero classes;
- `r` square-value parameters, modulo the common projective scaling.

Hence such a stratum has projective dimension at most `r-1`.  Therefore

```text
dim Crit <= d-2,
```

with the convention that the critical locus is empty for `d=1`.

The ambient projective space has dimension `2k-1`, and `Y_{d,k}` is cut out
by `d` equations.  Krull's height theorem gives every irreducible component
dimension at least

```text
2k-d-1.
```

Since `k>d`,

```text
2k-d-1 > d-2.
```

No component can be contained in the critical locus.  Every component meets
the rank-`d` locus, where the Jacobian criterion gives a smooth point of
local dimension `2k-d-1`.  Thus all components have exactly this dimension.

The equations have height `d` in the regular local rings of projective space,
so they form a regular sequence locally.  Thus `Y_{d,k}` is a projective
local complete intersection and is Cohen-Macaulay.

For a pure-codimension-`d` complete intersection in a smooth ambient space,
the singular locus is defined by the equations and the `d x d` minors of the
Jacobian.  Consequently

```text
Sing(Y_{d,k}) = Y_{d,k} cap Crit,
dim Sing(Y_{d,k}) <= d-2.
```

The codimension of the singular locus inside `Y_{d,k}` is at least

```text
(2k-d-1)-(d-2) = 2(k-d)+1 >= 3.
```

The scheme is therefore regular in codimension one.  Since it is
Cohen-Macaulay, it satisfies `S_2`; by Serre's criterion it is normal.

A positive-dimensional projective complete intersection is connected.  A
Noetherian normal scheme is the disjoint union of its normal integral
components; connectedness therefore forces a single component.  Hence
`Y_{d,k}` is integral.  The same proof applies after base change to an
algebraic closure, so `Y_{d,k}` is geometrically integral.

## Boundary k=d

For `k=d`, the same critical-dimension bound gives only

```text
codim_Y Sing(Y_{d,d}) >= 1.
```

It does not prove normality.  This is exactly the boundary where matching and
permutation geometry can produce reducible fibers in the component atlas.
The theorem above is therefore restricted to `k>d`.

## Hooley-Katz Parameters

For `Y_{d,k}`:

```text
ambient projective dimension M = 2k-1,
variety dimension r = 2k-d-1,
singular-locus bound s = d-2,
multidegree e = (1,3,5,...,2d-1).
```

Ghorpade-Lachaud Theorem 6.1 gives

```text
||Y_{d,k}(F_p)| - pi_r|
 <= B_{d,k} p^{k-1} + C_{d,k} p^{k-3/2},
```

where

```text
B_{d,k} = b'_{2(k-d)}(2k-d, (1,3,...,2d-1))
```

and

```text
C_{d,k} <= 9*2^d*(d(2d-1)+3)^{2k}.
```

This is the direct presentation retaining the degree-one equation.  Since
`F_1` is linear, one can eliminate it and view the same projective variety in
`P^{2k-2}` as a complete intersection of multidegree

```text
(3,5,...,2d-1)
```

and codimension `d-1`.  The primitive Betti coefficient is unchanged:

```text
b'_{2(k-d)}(2k-d, (1,3,...,2d-1))
 =
b'_{2(k-d)}(2k-d-1, (3,5,...,2d-1)).
```

The universal lower-weight bound improves to

```text
C_{d,k}^{red}
 <= 9*2^{d-1}*((d-1)(2d-1)+3)^{2k-1}.
```

The verifier records both presentations and uses the linear-eliminated
presentation as the operative GL lower-weight bound.

The exponent gain is

```text
(r+s+1)/2 = k-1.
```

## Affine Cone Conversion

The affine homogeneous collision variety is the cone over `Y_{d,k}`.  Thus

```text
|X_{d,k}(F_p)| = 1 + (p-1)|Y_{d,k}(F_p)|.
```

Since

```text
1 + (p-1) pi_r = p^{r+1} = p^{2k-d},
```

the projective estimate gives

```text
||X_{d,k}(F_p)| - p^{2k-d}|
 <= B_{d,k} p^k + C_{d,k} p^{k-1/2}.
```

This is a full-affine `F_p` estimate.  It is not a full-torus estimate and
does not count `H^{2k}` for a proper multiplicative subgroup `H`.

## Low-Energy Fraction

Let

```text
alpha = 1-2 tau.
```

If `L_{d,k}(tau)` is the number of projective coefficient lines with

```text
max_{u!=0} |S(ua)| >= alpha p,
```

then the high-moment identity and the imported point-count bound imply

```text
sum_{a in F_p^d} |S(a)|^{2k}
 = p^d |X_{d,k}(F_p)|.
```

The zero coefficient contributes `p^{2k}`, so

```text
sum_{a != 0} |S(a)|^{2k}
 = p^d (|X_{d,k}(F_p)| - p^{2k-d}).
```

This subtraction is nonnegative because the left side is a sum of
nonnegative moments.  If `L_{d,k}(tau)` projective coefficient lines are bad,
each line has at least one scalar representative with moment at least
`(alpha p)^{2k}`, and hence

```text
L_{d,k}(tau)/|P^{d-1}(F_p)|
 <= ((p-1)p^d)/(p^d-1)
    alpha^{-2k}
    (B_{d,k}p^{-k} + C_{d,k}p^{-k-1/2}).
```

The verifier audits this expression without simplifying away the constants.

## Reserve-Scale Audit Outcome

The verifier evaluates the requested grid

```text
A in {1,1.5,2,3,4,6,8},
C in {0.25,0.5,1,2},
theta in {0.25,0.5,0.75,1},
tau in {0.05,0.10,0.15,0.20},
N in {256,1024,4096,16384}.
```

Rows with `k<=d` are marked as rejected geometry rows.  On the remaining
`1736` rows, the current audit gives the following operative
linear-eliminated presentation totals:

```text
PASS_BETTI_TERM = 1359,
FAIL_BETTI_TERM = 377,
PASS_LOWER_WEIGHT_TERM = 866,
FAIL_LOWER_WEIGHT_TERM = 870,
MPP_CONDITION_MET = 0,
MPP_CONDITION_FAIL = 1736.
```

For comparison, the original presentation retaining the linear equation gave:

```text
PASS_BETTI_TERM_ORIGINAL_PRESENTATION = 1356,
FAIL_BETTI_TERM_ORIGINAL_PRESENTATION = 380,
PASS_LOWER_WEIGHT_TERM_ORIGINAL_PRESENTATION = 866,
FAIL_LOWER_WEIGHT_TERM_ORIGINAL_PRESENTATION = 870.
```

Thus the favorable Hooley-Katz exponent is real, and the leading Betti term
can pass in many polynomial-field windows.  The unrestricted
Ghorpade-Lachaud lower-weight constant is much more expensive; eliminating
the degree-one equation improves the bound but does not change the
lower-weight pass/fail split on this grid.  The Matera-Perez-Privitelli
field-size prerequisite fails throughout this reserve-scale grid.

## Status

PROVED:

- projective collision complete-intersection geometry for `k>d`;
- geometric integrality;
- singular-locus dimension at most `d-2`;
- exact affine-cone conversion;
- exact high-moment use of any imported projective point-count bound.

IMPORTED / AUDITED:

- Ghorpade-Lachaud Theorem 6.1;
- primitive Betti formula;
- explicit lower-weight bound;
- Matera-Perez-Privitelli Theorem 4.5 and field-size condition.

AUDIT:

- reserve-scale constant viability.

OPEN:

- viable polynomial-field point-count constants;
- multiplicative-character-twisted subgroup point counts;
- reserve-scale primitive low-energy count.
