# L1 Prefix Low-Excess Cyclotomic Norm Sieve

- **Status:** PROVED (low-excess exchange reduction, cyclotomic norm
  divisibility obstruction) / EXPERIMENTAL (finite norm-event audit) /
  CONJECTURAL (robust aperiodic counting after norm sieving) / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-21.
- **Scope:** Paper B `conj:prefix-local` in the monomial-prefix lane. This
  note does not assert the arbitrary-word `conj:arbitrary-local`,
  Reed--Solomon list-decoding safety, MCA, line-decoding, or protocol safety.

## Purpose

The anchored trinary model turns a prefix fiber into low-degree three-valued
polynomials. This note extracts a sharper arithmetic obstruction in the
low-excess exchange shells.

For a collision of complement subsets `A_0,A <= H`, write

```text
C=A cap A_0,
B=A\A_0,
B_0=A_0\A,
|B|=|B_0|=t.
```

Let

```text
P=L_B,        Q=L_{B_0}.
```

Then

```text
L_A-L_{A_0}=L_C(P-Q).
```

The same-prefix condition becomes a low-degree condition on the exchange gap
`P-Q`. Lifting the exchange locators to `Z[zeta_n]` then shows that a finite
field collision is either a characteristic-zero low-gap identity or a rational
prime dividing an explicit cyclotomic coefficient norm.

## 1. Low-Excess Exchange Reduction

Assume `A` and `A_0` have the same complement-prefix of length `sigma`. Since

```text
L_A=L_C P,
L_{A_0}=L_C Q,
```

and `L_C` is monic of degree `|C|=m-t`, the condition that `L_A-L_{A_0}` has
degree at most `m-sigma-1` is equivalent to

```text
deg(P-Q) <= t-sigma-1.
```

Define the exchange excess

```text
e=t-sigma-1.
```

Thus every collision gives disjoint equal-degree divisors `P,Q | X^n-1`
satisfying

```text
deg(P-Q) <= e.
```

Equivalently, with `R=P-Q`, one has

```text
X^n-1 = D_0 Q(Q+R),
deg R <= e.
```

This shell decomposition is exact. Negative `e` forbids a collision, while
small nonnegative `e` is a rigid low-gap exchange condition.

## 2. Cyclotomic Lift and Norm Obstruction

Let `K=Q(zeta_n)`. Lift exponent sets to roots of unity in `K`, and write

```text
tilde P(X)=prod_{b in B}(X-zeta_n^b),
tilde Q(X)=prod_{b in B_0}(X-zeta_n^b)
```

in `Z[zeta_n][X]`. Put

```text
Delta_j=[X^j](tilde P-tilde Q).
```

Let `omega in F_p` be the chosen order-`n` root defining the split embedding

```text
zeta_n |-> omega.
```

Reduction modulo the prime ideal

```text
mathfrak p=(p, zeta_n-omega)
```

sends `tilde P,tilde Q` to the finite-field exchange locators `P,Q`.

Therefore, if the finite collision has `deg(P-Q)<=e`, then

```text
Delta_j in mathfrak p        (j>e).
```

For every nonzero `Delta_j`, this implies

```text
p | |Norm_{K/Q}(Delta_j)|.
```

This gives the dichotomy:

1. all high-gap `Delta_j` vanish in characteristic zero, so the collision comes
   from a genuine characteristic-zero low-gap identity;
2. some high-gap `Delta_j` is nonzero, and the finite-field collision can occur
   only at rational primes dividing its cyclotomic norm.

This is a bad-prime sieve, not merely a finite-field coincidence test.

## 3. Relation to the Anchored Trinary Model

The exchange condition is the low-excess core of the anchored trinary system.
The trinary polynomial records the value partition of `H` into unchanged,
added, and removed points. The exchange locators `P` and `Q` record the added
and removed roots. In low-excess shells, the trinary constraints force the
locator gap `P-Q` to have very small degree.

Quotient-periodic or compositional patterns remain the first structured class
to remove. After those are excluded, a robust finite-field collision in a
low-excess shell must be explained either by:

- a characteristic-zero low-gap identity; or
- an explicit bad-prime norm event.

This is the arithmetic obstruction promised by the trinary route.

## 4. The `F_17,n=16,k=6,sigma=4` Certificate

The known prefix certificate has

```text
n=16,        k=6,        sigma=4,        m=6.
```

The finite verifier recovers:

```text
8008 complement subsets,
7968 prefix values,
40 two-point collision fibers.
```

For every collision pair:

```text
t=6,        e=t-sigma-1=1,
deg(P-Q)=1.
```

The 40 collision pairs split into three dilation orbits of sizes

```text
8, 16, 16.
```

For the three orbit representatives, the exact high-gap coefficient norms in
`Q(zeta_16)` are nonzero and divisible by `17`. The verifier reports:

```text
orbit 1: j=2,3,4,5 norms 13328, 53312, 5508, 2312
orbit 2: j=2,3,4,5 norms 73984, 4352, 13328, 4624
orbit 3: j=3,5     norms 591872, 147968
```

Each displayed norm is divisible by `17`. No orbit representative is an exact
characteristic-zero low-gap identity, and no representative is flagged as
compositional by the trinary monomial-support criterion.

Thus the entire `F_17` forty-collision certificate is explained as a finite
bad-prime norm event in the first nontrivial low-excess shell.

## 5. Sieve Target

For a fixed characteristic-zero exchange pattern, the bad rational primes are
contained in the finite set of prime divisors of the nonzero high-gap
coefficient norms. Therefore robust families of finite-field collisions must
come from:

```text
characteristic-zero low-gap identities
or
many distinct exchange patterns whose norms have the active prime as a divisor.
```

The conjectural next step is a robust aperiodic counting theorem for the latter
case: after quotient-periodic and low-defect patterns are removed, the number
of low-excess anchored exchange cores surviving modulo a fixed split prime
should be polynomially bounded.

This remains CONJECTURAL here.

## 6. Verifier

`experimental/scripts/verify_l1_prefix_low_excess_norm_sieve.py` checks:

- recovery of every prefix collision and its `(t,e,R)` exchange data;
- reproduction of the `F_17,n=16,k=6,sigma=4` forty-collision certificate;
- the fact that every collision lies in the `e=1` shell;
- three dilation orbits of collision pairs;
- reduction of the cyclotomic locator lift through `zeta_16 -> omega`;
- exact cyclotomic coefficient norms by resultants;
- divisibility of every nonzero high-gap norm by `17`;
- separation of characteristic-zero low-gap identities from bad-prime events;
- quotient/compositional flags using the anchored trinary monomial-support
  criterion.

The finite norm data are experimental diagnostics. The divisibility theorem is
proved, but the robust aperiodic norm-sieve count is not.
