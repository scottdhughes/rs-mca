Continues PR #480.

# CAP25 v13 raw: an exact degree-two spherical-LP cut rules out 187 M31 integral-ratio shell pairs

Status: `PROVED` (the degree-two spherical-LP lemma and its application to an
exact 187-point subset of the PR #480 grid); the other 3,254,698 grid points
remain `OPEN`.  This is Exit 2 of the integral-ratio ruleout task.

**Verifier:**
`experimental/scripts/verify_m31_integral_ratio_lp_ruleout.py` (zero-argument,
stdlib-only; `RESULT: PASS (22/22 checks)`; eight corruption self-tests).
**Data:**
`experimental/data/cap25_v13_m31_integral_ratio_lp_ruleout.json`.

## 0. Result

At the binding Mersenne-31 list row, PR #480 reduces every first violating
two-shell family to one of exactly 3,254,885 integral-ratio pairs `(k,t)`.  For
each pair put

```text
e1=(k-1)t,   e2=kt.
```

This note proves the following exact additional cut.

> **Degree-two LP cut (`PROVED`).** Among the 3,254,885 pairs, exactly 187
> satisfy the sign conditions below and have spherical-LP upper bound strictly
> below `L0=2^24=16,777,216`.  No two-shell family of size at least `L0` in the
> M31 prefix fiber can realize any of those 187 pairs.  Exactly 3,254,698 pairs
> survive this cut.

The integer caps on the 187 eliminated pairs range from 2,137,934 to
16,722,247.  Thus even the weakest eliminated cap is

```text
B* - 16,722,247 = 16,777,215 - 16,722,247 = 54,968
```

below the deployed budget.  This is a genuine exact improvement over #480's
dead-margin wall, but it does not pay the whole two-shell cell.

This packet continues [PR #480](https://github.com/przchojecki/rs-mca/pull/480).
The faithful twin-coset toy source is
[PR #476](https://github.com/przchojecki/rs-mca/pull/476); no toy assertion is
used in the proof here.

## 1. Exact input grid from PR #480  `AUDIT`

The deployed constants are

```text
p=2^31-1=2,147,483,647,   n=2^21=2,097,152,
m=981,129,                w=67,447,
B*=2^24-1=16,777,215,     L0=B*+1=16,777,216.
```

For a family of constant-`m` supports in one depth-`w` power-sum fiber, #480
proves moment rigidity `e1>=w+1`, the integral-ratio form above, `2<=k<=774`,
and the centered-radius cut.  With

```text
R=m(n-m)=1,094,962,529,967,
```

the resulting exact grid is

```text
2 <= k <= 774,
ceil(67,448/(k-1)) <= t
  <= min(floor(981,129/k), floor(R/(2,097,152(k-1)))).       (1.1)
```

There are 773 nonempty `k` rows and 3,254,885 pairs.  The endpoint rows are

```text
k=2:   67,448 <= t <= 490,564  (423,117 values),
k=774:     88 <= t <= 675          (588 values).
```

The verifier regenerates (1.1); it does not import #480's JSON.

## 2. A degree-two spherical bound  `PROVED`

Let `F` be any constant-`m` family on an `n`-point ground set whose two exchange
distances are `e1<e2`.  For each support `A`, center its incidence vector:

```text
y_A = 1_A - (m/n) 1,       r = ||y_A||^2 = m(n-m)/n,
u_A = y_A/sqrt(r).
```

The vectors `u_A` are unit vectors in the `D=n-1` dimensional space orthogonal
to `1`.  Since `|A intersect B|=m-e(A,B)`, their two off-diagonal inner products
are

```text
a = 1-e1/r,       b = 1-e2/r.                               (2.1)
```

Write `Q1=(<u_A,u_B>)` and `Q0=J`.  Both are positive semidefinite.  Also

```text
Q2 = (D (Q1 o Q1) - J)/(D-1)                               (2.2)
```

is positive semidefinite: it is the Gram matrix of the scaled traceless
tensors `u_A tensor u_A-I/D`.  Here `o` is the entrywise product.

For `f(x)=(x-a)(x-b)`, use

```text
x^2 = 1/D + ((D-1)/D) ((D x^2-1)/(D-1))
```

entrywise to obtain the exact kernel identity

```text
F := (f(<u_A,u_B>))
   = f0 Q0 - (a+b) Q1 + ((D-1)/D) Q2,
f0 := ab + 1/D.                                             (2.3)
```

Assume

```text
a+b <= 0,       f0 > 0.                                    (2.4)
```

All three coefficients in (2.3) are then nonnegative.  If `L=|F|`, positivity
of `Q1,Q2` gives

```text
1^T F 1 >= f0 L^2.                                         (2.5)
```

Every off-diagonal entry of `F` is zero because its argument is `a` or `b`,
while every diagonal entry is `f(1)`.  Hence the left side of (2.5) is
`L f(1)`.  Since `f0>0`,

```text
L <= f(1)/f0
  = e1 e2 / ((r-e1)(r-e2) + r^2/D).                        (2.6)
```

This proves (2.6) without an imported classification theorem or a numerical
positivity test.

## 3. Integer-only elimination gate  `PROVED`

For the M31 row set `D=n-1=2,097,151` and retain `R=m(n-m)`.  Clearing positive
denominators in (2.4) gives

```text
(e1+e2)n >= 2R,                                             (3.1)
den := D(R-e1 n)(R-e2 n)+R^2 > 0.                           (3.2)
```

When (3.1)--(3.2) hold, the right side of (2.6) is exactly

```text
N/den,       N := e1 e2 n^2 D.                              (3.3)
```

Thus the pair is eliminated precisely by this certificate when

```text
N < L0 den.                                                 (3.4)
```

Indeed, (3.4) and (2.6) give the strict real inequality `L<L0`, so integrality
gives `L<=B*`.  The reported integer cap is `U=floor(N/den)`.  Equations
(3.1)--(3.4) use only integer arithmetic.

## 4. Exact scan certificate  `PROVED`

Scanning every pair in (1.1) yields

| gate | exact count |
|---|---:|
| original PR #480 grid | 3,254,885 |
| satisfies both LP sign conditions (3.1)--(3.2) | 224 |
| also satisfies the strict budget gate (3.4) | **187** |
| survives this packet | **3,254,698** |

The 187 eliminated points use 187 distinct `k` values, with minimum `k=10` and
maximum `k=773`.  The first five in lexicographic `(k,t)` order are

| `k` | `t` | `e1` | `e2` | `U=floor(N/den)` |
|---:|---:|---:|---:|---:|
| 10 | 58,013 | 522,117 | 580,130 | 12,442,360 |
| 15 | 37,294 | 522,116 | 559,410 | 11,783,702 |
| 29 | 18,647 | 522,116 | 540,763 | 3,648,189 |
| 30 | 18,004 | 522,116 | 540,120 | 3,560,399 |
| 33 | 16,316 | 522,112 | 538,428 | 14,998,880 |

Over all 187 rows, the exact checksums are

```text
sum k  = 85,533,       sum t  = 451,179,
sum e1 = 97,623,861,   sum e2 = 98,075,040.
```

Canonicalizing each row as `k,t,e1,e2,U` and joining rows with semicolons gives
5,730 ASCII bytes and SHA-256

```text
add3990426c7cd56da1585ca942c4b7ba79d377cb5721157fd3e3eb1efa4d604.
```

The 37 sign-admissible rows not eliminated by (3.4) have integer caps ranging
from 16,852,822 to 748,346,571.  Even the smallest is 75,607 above `B*`, so this
specific degree-two polynomial gives no budget conclusion on those 37 rows.

## 5. What the M31 moments do, and do not, supply

The M31 moment structure is what makes the finite search possible: Newton
rigidity supplies `e1>=w+1`, and #480's moment/Gram reduction supplies the
integral ratio and the exact grid (1.1).  The new step after that reduction is
real spherical positivity; it is valid for every constant-weight two-distance
family and therefore certifies the selected M31 grid points without any
unproved transfer from finite-field rank to real rank.

The new LP step does **not** use the enormous modular `-k` nullity from #480.
Combining that modular condition with a stronger polynomial, a Smith-form
obstruction, or a graph classification remains the natural route on the
3,254,698 surviving pairs.

## 6. Nonclaims

- This packet does not rule out all 3,254,885 pairs or pay the two-shell cell.
- It does not construct a family above `B*`, at deployment or in a toy model.
- Conditions (3.1)--(3.2) are sufficient conditions for this LP proof, not
  necessary conditions for a realizable shell pair.
- A value `U>B*` is only failure of this certificate; it is not evidence that a
  family of that size exists.
- No result from the faithful toys of #476 is promoted to a deployed theorem.

## 7. Reproduce

From the repository root:

```text
ulimit -v 2097152; python3 experimental/scripts/verify_m31_integral_ratio_lp_ruleout.py
```

The verifier regenerates all 3,254,885 grid points, every number in this note,
the exact rational kernel identity, the cut certificate, and eight independent
data-corruption rejections.
