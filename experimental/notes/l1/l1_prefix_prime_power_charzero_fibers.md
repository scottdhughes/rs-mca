# L1 Prefix Prime-Power Characteristic-Zero Fibers

- **Status:** PROVED (iterated prime-power moment rigidity, exact
  `K_{d_sigma}` exchange classification, anchored characteristic-zero fiber
  formula, maximum characteristic-zero fiber bound) / EXPERIMENTAL (small
  exhaustive audits and finite `F_17` certificate comparison) / OPEN
  (aggregate finite-field bad-prime norm-event control) / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-21.
- **Scope:** Paper B `conj:prefix-local` in the monomial-prefix lane. This
  note does not assert the arbitrary-word `conj:arbitrary-local`,
  Reed--Solomon list-decoding safety, MCA, line-decoding, or protocol safety.

## Purpose

The dyadic first-moment note proves that characteristic-zero first-moment
exchange equality forces `K_2` exchange structure. This note iterates that
argument over prime-power domains.

For `n=ell^a`, the first `sigma` characteristic-zero power-sum equations force
exchange sets to be unions of cosets of

```text
K_{d_sigma},        d_sigma=ell^{ceil(log_ell(sigma+1))},
```

the smallest `ell`-power strictly larger than `sigma`. This gives an exact
formula for every anchored characteristic-zero prefix fiber and a polynomial
bound at reserve scale.

The result classifies only the exchange core between two anchored complements.
It does not say the full anchor is globally quotient-periodic: mixed cosets in
the common part of the anchor can remain arbitrary.

## 1. Prime-Power Moment Rigidity

Let

```text
n=ell^a,        zeta=zeta_n,
```

with `ell` prime. Let `B,B_0 subset mu_n` be disjoint equal-size exchange sets.
Write their exponent sets as subsets of `Z/nZ` and set

```text
F(Y)
=
sum_{zeta^i in B} Y^i
-
sum_{zeta^j in B_0} Y^j
in Z[Y],
deg F<n.
```

The characteristic-zero power-sum identities

```text
sum_{b in B} b^j = sum_{b_0 in B_0} b_0^j
        (1 <= j <= sigma)
```

are exactly

```text
F(zeta^j)=0        (1 <= j <= sigma).
```

Let `1 <= sigma < n` and

```text
d_sigma=ell^{ceil(log_ell(sigma+1))}.
```

Thus `d_sigma` is the smallest `ell`-power with `d_sigma>sigma`.

### Theorem

For disjoint equal-size exchange sets `B,B_0 subset mu_n`,

```text
sum_{b in B} b^j = sum_{b_0 in B_0} b_0^j
        (1 <= j <= sigma)
```

if and only if both `B` and `B_0` are unions of `K_{d_sigma}`-cosets.

### Proof

The case `j=1` gives

```text
F(zeta)=0.
```

Since

```text
Phi_{ell^a}(Y)
=
1+Y^{n/ell}+Y^{2n/ell}+...+Y^{(ell-1)n/ell},
```

and `deg F<n`, divisibility by `Phi_{ell^a}` forces the coefficients of `F`
to be constant on the exponent classes

```text
i, i+n/ell, ..., i+(ell-1)n/ell.
```

The coefficients lie in `{-1,0,1}` because `B` and `B_0` are disjoint.
Therefore the positive and negative supports are each unions of `K_ell`-cosets.

After quotienting by `K_ell`, write

```text
bar B, bar B_0 subset mu_{n/ell}.
```

Because each `K_ell`-coset has size `ell`,

```text
sum_{y in bar B} y
=
(1/ell) sum_{b in B} b^ell,
```

and similarly for `B_0`. Hence the original `ell`-th moment identity is the
first-moment identity for the quotient exchange sets. Applying the
first-moment rigidity again forces `K_{ell^2}`-coset structure upstairs.

Iterating with the moments

```text
j=1, ell, ell^2, ...
```

while `ell^r <= sigma` gives `K_{ell^{r+1}}`-structure. This reaches exactly
`K_{d_sigma}`.

Conversely, if `B` and `B_0` are unions of `K_{d_sigma}`-cosets, then for
every `1 <= j < d_sigma`,

```text
sum_{kappa in K_{d_sigma}} kappa^j=0.
```

Since `sigma<d_sigma`, every moment `1 <= j <= sigma` vanishes separately on
each `K_{d_sigma}`-coset. The two exchange sets therefore have equal first
`sigma` power sums.

## 2. Anchored Characteristic-Zero Fibers

Fix an anchor `A_0 subset mu_n`. Let `d=d_sigma`. Count the `K_d`-cosets by
their relation to `A_0`:

```text
u = #{K_d-cosets contained in A_0},
v = #{K_d-cosets disjoint from A_0}.
```

Mixed cosets, which meet both `A_0` and its complement, cannot participate in a
characteristic-zero same-prefix exchange: the exchange core must be a union of
full `K_d`-cosets on both sides.

Thus every same-prefix set is obtained by removing `r` full cosets from `A_0`
and adding `r` empty cosets, for some `r`. Hence

```text
|Phi_sigma^{-1}(Phi_sigma(A_0))|
=
sum_r binom(u,r) binom(v,r)
=
binom(u+v,u).
```

This is the exact anchored characteristic-zero prefix-fiber size.

## 3. Maximum Characteristic-Zero Fiber

For fixed `|A_0|=m`, the maximum occurs by filling as many whole `K_d`-cosets
inside `A_0` and outside `A_0` as possible. Therefore

```text
max_{|A_0|=m}
|Phi_sigma^{-1}(Phi_sigma(A_0))|
=
binom(
  floor(m/d)+floor((n-m)/d),
  floor(m/d)
).
```

In particular,

```text
max |Phi_sigma^{-1}(c)|
<= 2^{n/d_sigma}
<  2^{n/sigma}.
```

If

```text
sigma >= C n / log_2 n,
```

then

```text
2^{n/d_sigma} < 2^{n/sigma} <= n^{1/C}.
```

So the characteristic-zero prime-power prefix fibers satisfy a polynomial
local-limit bound at reserve scale.

## 4. Relation to Locator Coefficients

Let

```text
L_A(X)=prod_{a in A}(X-a).
```

For equal-size sets, equality of the first `sigma` power sums is equivalent,
by Newton identities, to equality of the top `sigma` locator coefficients.
Thus the characteristic-zero exchange classification is the characteristic-zero
version of the monomial-prefix fiber condition.

The verifier cross-checks this equivalence over `F_17` for `n=16` by comparing
finite power-sum fibers with fibers cut out by the top locator coefficients.
That is a finite audit of the dictionary, not a characteristic-zero theorem.

## 5. The `F_17,n=16,k=6,sigma=4` Certificate

For the known finite-field certificate,

```text
n=16,        sigma=4.
```

Here

```text
d_sigma=8.
```

The observed exchange size is

```text
t=6.
```

Since `8` does not divide `6`, no characteristic-zero `K_8` exchange core can
produce those collisions. The forty `F_17` collisions are therefore genuinely
modular bad-prime events in the sense of the low-excess norm sieve.

## 6. Boundary and Open Step

This note proves the characteristic-zero prime-power prefix-fiber story. It
does not bound finite-field bad-prime events in aggregate.

The remaining finite-field task is:

```text
control the total contribution of modular norm events after
characteristic-zero K_{d_sigma}-coset fibers are removed.
```

That is the next arithmetic counting problem for the monomial-prefix lane.

## 7. Verification

The companion verifier is

```text
experimental/scripts/verify_l1_prefix_prime_power_charzero_fibers.py
```

It checks:

- exhaustive signed classification for `n=8,16` and `n=9`;
- exact anchored fiber formulas for `n=8` and `n=9`;
- the maximum formula for `n=16`;
- positive structured examples where `d_sigma | t`;
- the `n=16,sigma=4,t=6` characteristic-zero impossibility;
- finite Newton/top-coefficient equivalence over `F_17`;
- the distinction between exchange-core structure and global quotient
  periodicity of the anchor.
