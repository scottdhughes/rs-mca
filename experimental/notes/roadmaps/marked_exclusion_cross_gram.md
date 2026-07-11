# Marked-exclusion cross-Gram reconstruction

**Status:** `PROVED` as a universal finite operator identity and exact
positive-density RS replay; `PRE-ATLAS` only. The post-first-match signed-Gram
participation bound and actual-slope compiler remain open.

**Verifier:**

```text
python3 experimental/scripts/verify_marked_exclusion_cross_gram.py
```

The verifier uses only the Python standard library. It replays the single and
signed-pair identities on the prime-order subgroup source
`(n,p,g,r)=(7,14197,1054,3)`, checks the coefficient-pattern injection, and
transports the single-support boundary through Newton's map for `w=2,3`.

## 1. Universal single-support identity

Let `D` have size `n`, let `Phi:D->A` map into a finite abelian group, and
fix `2<=r<=n-1`. Put

```text
sigma(B)=sum_{x in B} Phi(x),
X_r={(B,x): |B|=r-1, x in D}.
```

On `l2(X_r)`, define the unrestricted marked-addition synthesis operator and
exclusion projection by

```text
U_r e_(B,x) = e_(sigma(B)+Phi(x)),
P_r e_(B,x) = 1_{x in B} e_(B,x).
```

Set

```text
a=(r-1)/n,
T_r=U_r(P_r-aI),
G_r=U_r(I-P_r).
```

Thus `T_r` is the mass-matched marked-exclusion correction and `G_r` is the
genuine-addition operator. Since every column of `U_r` is a standard output
basis vector, all three output Gram operators are diagonal. If `C_r(s)` is
the unrestricted output multiplicity and `nu_r(s)` is the multiplicity of
an `r`-subset boundary value, then

```text
U_r U_r^* = M_(C_r),
G_r G_r^* = r M_(nu_r).                                  (1)
```

The exact cross-Gram reconstruction is

```text
H_r:=G_rG_r^*
   =(1-a)U_rU_r^*-U_rT_r^*.                              (2)
```

Indeed, an excluded marked column has coefficient `1-a` in `T_r`, while a
genuine column has coefficient `-a`. At output `s`, if `kappa_r(s)` is the
excluded multiplicity, then

```text
(U_rT_r^*)(s,s)=kappa_r(s)-a C_r(s).
```

Subtracting this from `(1-a)C_r(s)` leaves
`C_r(s)-kappa_r(s)=r nu_r(s)`, proving (2). In particular

```text
rank(H_r)=|im(nu_r)|.                                    (3)
```

The same column calculation gives the covariance identity

```text
(1-a)^2 U_rU_r^*-T_rT_r^*=(1-2a)H_r.                    (4)
```

When `a!=1/2`, (4) also reconstructs `H_r`. At `a=1/2`, however,

```text
T_rT_r^*=(1/4)U_rU_r^*,                                 (5)
```

so covariance alone loses all genuine-versus-excluded orientation. The
cross-Gram formula (2) remains exact and nonsingular.

## 2. Multiplicity-sensitive image bounds

Because `H_r=rM_(nu_r)` is positive semidefinite,

```text
|im(nu_r)| >= (tr H_r)^2/tr(H_r^2),
|im(nu_r)| >= tr(H_r)/||H_r||_op.                        (6)
```

These are weighted by the actual output multiplicities. They do not replace
the weighted Fourier/frame quantity by unweighted energy on a difference
set.

The mass-matched correction cannot be treated as uniformly small at positive
density. Universally,

```text
||T_r||_HS^2/||G_r||_HS^2=a=(r-1)/n.                    (7)
```

This follows by counting excluded and genuine marked columns: their fractions
are `a` and `1-a`, and their squared correction coefficients are `(1-a)^2`
and `a^2`.

## 3. Signed-pair analogue

For `2r<=n`, let

```text
X_r^pm={(C,B,x): |C|=r-1, |B|=r, C cap B=empty, x in D},
U_r^pm e_(C,B,x)=e_(sigma(C)-sigma(B)+Phi(x)).
```

Let `P_r^pm` project onto `x in C union B`, set

```text
b=(2r-1)/n,
T_r^pm=U_r^pm(P_r^pm-bI),
G_r^pm=U_r^pm(I-P_r^pm).
```

If `omega_(r,r)` is the multiplicity of an ordered disjoint signed support
pair, the identical marked-column calculation gives

```text
G_r^pm(G_r^pm)^*=rM_(omega_(r,r))
 =(1-b)U_r^pm(U_r^pm)^*-U_r^pm(T_r^pm)^*.                (8)
```

Its covariance decoder is singular at `b=1/2`, asymptotically
`r/n=1/4`, while (8) remains exact.

## 4. Sharp positive-density obstruction

On the injected multiplicative-subgroup source used by the dense-exclusion
route cut, coefficient-pattern injectivity separates all genuine and repeat
outputs. For the single-support operator the nonzero singular values are

| operator | singular value | multiplicity |
|---|---:|---:|
| `G_r` | `sqrt(r)` | `binom(n,r)` |
| `T_r`, genuine sector | `a sqrt(r)` | `binom(n,r)` |
| `T_r`, repeat sector | `1-a` | `(r-1)binom(n,r-1)` |

Consequently no Schatten norm makes `T_r` a perturbatively small replacement
for `G_r` at fixed density. In particular, (7) stays bounded away from zero,
the operator-norm ratio tends to the density, and the nuclear-norm ratio
diverges. The surviving object is the signed defect (2), not separate norm
smallness of its two terms.

The exact replay at `(n,p,g,r)=(7,14197,1054,3)` gives

```text
G_3: sqrt(3), multiplicity 35,
T_3: (2/7)sqrt(3), multiplicity 35,
T_3: 5/7, multiplicity 42,
||T_3||_HS^2/||G_3||_HS^2=2/7.
```

For the signed-pair operator, the cross-Gram defect has eigenvalue `3` on
exactly `140` genuine outputs and zero on the excluded sectors.

## 5. RS boundary compiler

For `w=2,3` in characteristics where `2` and `3` are invertible, Newton's
identities give a triangular bijection between the first `w` power sums and
the first `w` elementary symmetric coefficients, including formal locators
with repeated roots. Relabeling the output basis by this bijection is unitary.
Therefore the single-support ranks, spectra, Schatten norms, and realized
image statements above transfer without normalization loss to the actual
locator-prefix boundary.

For signed pairs, only the zero-fiber equivalence is asserted: two equal-size
supports have equal first `w` power sums exactly when they have equal first
`w` locator coefficients. There is no claim of a global unitary conjugacy
between their difference codomains.

## 6. Exact remaining wall and nonclaims

For an actual post-atlas primitive weighted-Vandermonde profile `lambda`, the
next required theorem is a signed-Gram participation estimate for the
first-match-masked defect, for example

```text
(tr H_lambda)^2 <= exp(o(n)) |Z_lambda| tr(H_lambda^2),   (9)
```

or a corresponding operator-norm estimate. It must retain signed phases and
representation multiplicities. After (9), one still needs first-match
profile add-back and an actual-slope compiler.

This note does not prove (9), primitive Q, A4, A2, A6, A7, a post-atlas
survivor bound, a deployed M31 row, a complete finite upper ledger, or
`U(a0+1)<=B*`. The `n=7` replay is source validation, not a deployed-row
certificate.
