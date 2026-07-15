# `c=0`, `g=X^a`: the complete `f=29` periodic projective stratum is paid

## Exact result

Work at

```text
p=2,130,706,433,
B=32,768,
t=981,105=29B+30,833,
a=67,472>B.
```

Canonically decompose a support with exactly 29 complete `mu_B` quotient
cosets as

```text
Omega=mu_64,
C_y={x in H:x^B=y} for y in Omega,
E=R disjoint_union union_(y in S) C_y,
|S|=29,       |R|=r=30,833<B,
```

Here `y` is a quotient value, not a multiplier in `H`; after choosing a lift
`x_y`, the fiber is `C_y=x_y mu_B`.  The shorthand `y mu_B` would collapse
because `mu_64 subset mu_B`.  The residual `R` contains no complete quotient
fiber.  Then the locator is

```text
L_E(X)=A_R(X) Q_S(X^B),
A_R=product_(x in R)(X-x),
Q_S(Y)=product_(y in S)(Y-y).                           (1)
```

For the monomial first-hard modulus

```text
g=X^a,
```

all degree-`t` locators in one projective residue ray have proportional
remainders modulo `X^a`.  This forces all locators in the `f=29` part of the
ray to have the **same residual support `R`**.  Consequently the accepted
fixed-residual three-invariant Hahn payment applies to the whole `f=29`
projective stratum, not merely one preselected residual support:

```text
N_(f=29)(one projective residue ray)
 <=64*25,307,496
 =1,619,679,744
 <T=274,854,110,496,187,592.                           (2)
```

The exact margin is

```text
274,854,108,876,507,848.                               (3)
```

This is a source-valid payment of one complete canonical stratum for the
literal deployed modulus `g=X^a`.  It is not a uniform theorem for arbitrary
`g` and does not pay supports with fewer than 29 complete quotient cosets.

The pinned inputs are

```text
work/DEPLOYED_C0_Q64_PERIODIC_FIXED_Q_REDUCTION.md
sha256=8b2d84ffb344bbb0a78c904358645322f5159c20c152760ea7cd97354228fc69

work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md
sha256=99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b

work/verify_c0_q64_three_invariant_hahn_payment.rb
sha256=baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5

work/verify_c0_q64_three_invariant_hahn_payment.expected.txt
sha256=28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1
```

## Proof of residual ownership

The constant coefficient of `Q_S` is

```text
q_0(S)=(-1)^29 product_(y in S)y in mu_64,             (4)
```

so it is nonzero.  Reducing (1) modulo `X^B` gives the exact polynomial
identity

```text
L_E == q_0(S) A_R modulo X^B.                          (5)
```

Now let `E,E'` lie in one projective residue ray modulo `X^a`.  There is a
nonzero scalar `c` such that

```text
L_E == c L_(E') modulo X^a.                            (6)
```

Because `a>B`, equation (6) remains true modulo `X^B`.  Equations (5)--(6)
give

```text
q_0(S) A_R == c q_0(S') A_(R') modulo X^B.             (7)
```

Both sides of (7) have actual degree exactly

```text
r=30,833<B.
```

Hence (7) is equality as polynomials, not only a congruence.  The residual
locators are monic of the same degree.  Comparing their leading
coefficients first gives

```text
q_0(S)=c q_0(S'),
```

and cancellation then gives

```text
A_R=A_(R').                                            (8)
```

Both locators are squarefree products of deployed linear factors, so (8)
is exactly `R=R'`.  This proves residual ownership without assuming that the
residual lies in one quotient coset.

Once `R` is fixed, the all-weight theorem specializes at `f=29` to the
fixed-absolute-scalar cap `25,307,496`.  Its constant quotient coefficient
lies in `mu_64`, so the projective ray meets at most 64 scalar cells.  This
proves (2)--(3).

## Scope and nonclaims

- The theorem is uniform over every distribution of the 30,833 residual
  roots among the 35 non-full quotient cosets.
- It pays all `f=29` locators in one projective ray simultaneously; there is
  no multiplication by the number of residual supports.
- It does not assert that projective congruence determines the residual when
  `f<=28`; then `t-fB>=B`, so the degree-`<B` ownership argument stops.
- It does not pay the sum of the `f=0..28` strata, arbitrary monic moduli
  `g`, the complete `c=0` theorem, or an official question.

## Replay

```bash
ruby --disable-gems -w work/verify_c0_q64_f29_projective_residual_owner_payment.rb
```
