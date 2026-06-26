# L1 Prefix Dual Large-Domain Weil Energy Floor

Date: 2026-06-26

Status: CONDITIONAL / AUDIT.  The large-domain energy floor is conditional on
the stated one-variable mixed Kummer--Artin--Schreier estimate with the
displayed constant.  Before promotion, the exact citation and any `D+O(1)`
constant loss should be checked against a primary source.

## Purpose

The primitive-energy exact and adversarial atlases show no rate-collapse
family, but they also do not justify a uniform primitive spectral gap in the
full reserve-scale regime.  This note proves a positive theorem in the
low-degree, large-domain window where ordinary one-variable Weil cancellation
is already strong enough.

The result applies to every nonzero odd frequency line.  No projective
primitivity hypothesis is required.

## Setup

Assume `p` is odd, `H <= F_p^*` has even order `n`, and `N=n/2`.
Let

```text
q(X)=sum_j r_j X^j
```

be a nonconstant odd polynomial in `F_p[X]` of degree `D < p`.
Equivalently for this note, `q` is nonzero, odd, and has positive degree
below `p`.  For `u in F_p^*`, define

```text
E_H(uq)=sum_{h in R} sin^2(2*pi*u*q(h)/p),
```

where `R` contains one representative from each antipodal pair in `H`.

Because `q(-h)=-q(h)`,

```text
sum_{h in H} psi(2u q(h))
```

is real and

```text
E_H(uq)
= N/2 - (1/4) sum_{h in H} psi(2u q(h)).
```

This is the same energy/exponential-sum identity used in the primitive
energy-rate certification checkpoint.

## Character Decomposition

Put

```text
m=(p-1)/n,
```

and let `H^perp` be the `m` multiplicative characters that are trivial on
`H`.  The subgroup indicator gives

```text
sum_{h in H} psi(2u q(h))
= (1/m) sum_{chi in H^perp} sum_{x in F_p^*} chi(x) psi(2u q(x)).
```

For the trivial character, the ordinary additive Weil bound gives

```text
|sum_{x != 0} psi(2u q(x))| <= (D-1)sqrt(p)+1.
```

For each nontrivial `chi`, the standard one-variable mixed
Kummer--Artin--Schreier bound gives

```text
|sum_{x != 0} chi(x) psi(2u q(x))| <= D sqrt(p).
```

The hypotheses are exactly the clean one-variable case: `D<p`, the additive
phase `2u q` is nonconstant, and the multiplicative factor is the squarefree
coordinate `x`.  Averaging over the `m` characters yields

```text
|sum_{h in H} psi(2u q(h))|
<= ((D-1)sqrt(p)+1+(m-1)D sqrt(p))/m
= D sqrt(p) - (sqrt(p)-1)/m
<= D sqrt(p).
```

Thus

```text
|sum_{h in H} psi(2u q(h))| <= D sqrt(p).
```

## Energy Floor

For every nonzero odd `q` of degree `D<p`,

```text
E_*([q])/N >= 1/2 - D sqrt(p)/(2n),
```

where

```text
E_*([q]) = min_{u in F_p^*} E_H(uq).
```

For the full group `H=F_p^*`, the sharper trivial-character estimate gives

```text
E_*([q])/N
>= 1/2 - ((D-1)sqrt(p)+1)/(2(p-1)).
```

Immediate thresholds:

```text
n >= 2D sqrt(p)  ==>  E_*/N >= 1/4,
n >= 4D sqrt(p)  ==>  E_*/N >= 3/8.
```

If the displayed lower bound is negative, it is `VACUOUS_NOT_FALSE`: the
theorem remains true but gives no positive spectral information.

No claim is made here for the zero polynomial, for phases of degree `D>=p`
before degree reduction, or for nonodd phases in the real-sum identity.

## Bessel Consequence

For a coefficient support `U` whose exponents are at most `D`, define

```text
A_U(lambda)
= (p-1)^(-|U|) sum_{r in (F_p^*)^U} exp(-lambda E_H(q_r)).
```

The torus average uses nonzero coefficients on the fixed support `U`; hence
every polynomial in the support stratum is genuinely nonzero.

If

```text
tau = 1/2 - D sqrt(p)/(2n) > 0,
```

then every torus coefficient vector satisfies `E_H(q_r) >= tau N`, and hence

```text
A_U(lambda) <= exp(-lambda tau N).
```

The same bound applies to the primitive submass when the primitive submass is
normalized by the full torus denominator.  Equivalently, for every
`tau' < tau`,

```text
F_u^prim(tau') = 0.
```

This is a genuine exponential closure theorem in the large-domain low-degree
window.

## Atlas Interpretation

For the `d=4` odd-frequency space, `D=2d-1=7`.

Full group `(p,n)=(257,256)`:

```text
E_*/N >= 1/2 - (6 sqrt(257)+1)/512 ~= 0.310181.
```

The adversarial atlas found approximately `0.354866`, consistent with the
theorem.

Proper subgroup `(p,n)=(257,128)`:

```text
E_*/N >= 1/2 - 7 sqrt(257)/256 ~= 0.061646.
```

The search found approximately `0.285275`; the theorem is nontrivial but not
sharp.

Proper subgroup `(p,n)=(193,64)`:

```text
1/2 - 7 sqrt(193)/128 < 0.
```

The theorem is vacuous here, while the exact atlas minimum is about
`0.170551`.  This is where a stronger primitive or averaged theorem is needed.

## Route Cut

For the full group `n=p-1`, the floor is

```text
E_*/N >= 1/2 - O(D/sqrt(p)).
```

It is powerful when `D=o(sqrt(p))`.  In the critical reserve regime

```text
d = Theta(n/log n),   D ~= n/log n,   p ~= n,
```

the factor `D sqrt(p)/n` is about `sqrt(n)/log n`, so the bound becomes
vacuous.  The remaining hard sector is therefore

```text
D sqrt(p) >= n,
dense primitive support,
d = Theta(n/log n).
```

That is the regime where the primitive counting-rate theorem, not ordinary
one-variable Weil cancellation, is still required.

## Status

CONDITIONAL, pending the mixed-Weil citation/constant check:

- multiplicative-character decomposition of subgroup sums;
- uniform mixed-Weil subgroup bound;
- large-domain energy floor;
- full-group refined floor;
- exponential Bessel torus-mass bound when `D sqrt(p) < n`;
- zero primitive low-energy rate below the floor.

EXPERIMENTAL:

- comparison against adversarial atlas minima;
- sharpness ratios by `p`, `n`, and `d`.

OPEN:

- dense high-degree regime `D sqrt(p) >= n`;
- exponential primitive low-energy count at reserve scale;
- uniform generated-field prefix local limit.
