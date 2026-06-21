# L1 Prefix Dyadic Characteristic-Zero First-Moment Rigidity

- **Status:** PROVED (dyadic signed first-moment rigidity, `K_2`
  exchange-core classification, one-coefficient norm-event consequence,
  prime-power `K_l` generalization) / EXPERIMENTAL (finite orbit and norm
  certificates) / CONJECTURAL (bad-prime density/counting bounds) / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-21.
- **Scope:** Paper B `conj:prefix-local` in the monomial-prefix lane. This
  note does not assert the arbitrary-word `conj:arbitrary-local`,
  Reed--Solomon list-decoding safety, MCA, line-decoding, or protocol safety.

## Purpose

The low-excess norm sieve shows that finite-field exchange collisions are
either characteristic-zero low-gap identities or bad-prime norm events. This
note proves that, over dyadic domains, the first possible characteristic-zero
condition is already rigid.

For `n=2^a`, equality of first moments for two disjoint signed exchange sets
forces both exchange sets to be antipodal unions. Therefore every dyadic
characteristic-zero low-excess exchange core is `K_2`-exchange-structured.

This does not classify the full anchored complements. The common portion
`C=A cap A_0` may be arbitrary. The theorem classifies only the exchange core
`B=A\A_0`, `B_0=A_0\A`.

## 1. Dyadic First-Moment Rigidity

Let

```text
n=2^a,        zeta=zeta_n.
```

Let `B,B_0 subset mu_n` be disjoint exchange sets and write their exponent
sets as subsets of `Z/nZ`. Define the signed indicator polynomial

```text
F(Y)
=
sum_{zeta^i in B} Y^i
-
sum_{zeta^j in B_0} Y^j
in Z[Y],
deg F<n.
```

The first-moment equality

```text
sum_{b in B} b = sum_{b_0 in B_0} b_0
```

is exactly

```text
F(zeta)=0.
```

Since

```text
Phi_{2^a}(Y)=Y^{n/2}+1,
```

and `deg F<n`, this implies

```text
F(Y)=(Y^{n/2}+1)G(Y),
deg G<n/2.
```

Equivalently, the coefficients of `F` at exponents `i` and `i+n/2` are equal.
The coefficients of `F` lie in `{-1,0,1}` because `B` and `B_0` are disjoint.
Therefore every positive coefficient occurs with its antipode, and every
negative coefficient occurs with its antipode.

Thus:

```text
-B=B,        -B_0=B_0.
```

Equivalently, both exchange sets are unions of `K_2={+-1}`-cosets.

## 2. Locator Composition Consequence

For an exchange set `B`, let

```text
L_B(X)=prod_{b in B}(X-b).
```

Then

```text
B=-B
```

if and only if

```text
L_B(X)=tilde L_B(X^2)
```

for a polynomial `tilde L_B`. Indeed, each antipodal pair contributes

```text
(X-b)(X+b)=X^2-b^2.
```

Conversely, if `L_B` is a polynomial in `X^2`, its root set is invariant under
`X -> -X`, hence `B=-B`.

Therefore the dyadic first-moment theorem says:

```text
characteristic-zero first-moment equality
  => K_2-exchange-structured locator cores.
```

Again, this is an exchange-core statement, not a global quotient-periodicity
statement for the anchored complements `C union B` and `C union B_0`.

## 3. Consequence for Low-Excess Norm Sieve

Let

```text
P=L_B,        Q=L_{B_0},        deg P=deg Q=t.
```

The low-excess condition from `l1_prefix_low_excess_norm_sieve.md` is

```text
deg(P-Q) <= t-sigma-1.
```

If `sigma>=1`, then the `X^{t-1}` coefficients of `P` and `Q` agree. Since

```text
[X^{t-1}]L_B = -sum_{b in B} b,
```

this gives the first-moment equality

```text
sum_{b in B} b = sum_{b_0 in B_0} b_0.
```

By the dyadic theorem, every characteristic-zero low-excess exchange core over
a dyadic domain is `K_2`-exchange-structured.

For any exchange pair that is not antipodally invariant, the first high
coefficient

```text
Delta_{t-1}
=
-sum_{b in B} b + sum_{b_0 in B_0} b_0
```

is a nonzero cyclotomic integer. If this pair becomes a finite-field prefix
collision modulo a prime ideal over `p`, then

```text
Delta_{t-1} in mathfrak p,
```

and hence

```text
p | |Norm_{Q(zeta_n)/Q}(Delta_{t-1})|.
```

Thus, for dyadic non-`K_2` exchange pairs, one coefficient already gives the
bad-prime certificate. The remaining high-coefficient norms strengthen the
certificate but are not needed to distinguish characteristic-zero structure
from genuinely modular behavior.

## 4. Prime-Power Generalization

Let

```text
n=ell^a
```

with `ell` prime. Then

```text
Phi_{ell^a}(Y)=
1+Y^{n/ell}+Y^{2n/ell}+...+Y^{(ell-1)n/ell}.
```

If a signed coefficient polynomial `F`, `deg F<n`, satisfies `F(zeta_n)=0`,
then `Phi_n | F`, so the coefficients are constant on cosets

```text
i, i+n/ell, ..., i+(ell-1)n/ell.
```

Since the coefficients are in `{-1,0,1}`, both positive and negative supports
are unions of the `K_ell`-cosets. Therefore equality of first moments forces
both exchange sets to be unions of `K_ell`-cosets.

The dyadic result is the case `ell=2`.

## 5. The `F_17,n=16,k=6,sigma=4` Certificate

The verifier checks the known forty collision pairs from the prefix certificate.
They split into three dilation orbits. For each orbit representative:

```text
t=6,        t-1=5.
```

The first high coefficient `Delta_5` is algebraically nonzero and has norm
divisible by `17`:

```text
orbit 1: |Norm(Delta_5)| = 2312
orbit 2: |Norm(Delta_5)| = 4624
orbit 3: |Norm(Delta_5)| = 147968
```

Each displayed norm is divisible by `17`. Thus one coefficient already explains
the finite-field low-gap collision as a bad-prime event in every orbit.

The size-8 orbit has an additional subtlety: negation swaps the two anchored
complements as unordered collision partners. This must not be mistaken for

```text
B=-B,        B_0=-B_0.
```

The verifier checks this explicitly. The size-8 orbit is not classified as
`K_2`-exchange-structured.

## 6. Sieve Target

After quotient-periodic, low-defect, and `K_2` exchange-structured cores are
removed in the dyadic setting, every remaining low-excess finite-field
collision carries a one-coefficient bad-prime certificate.

The next analytic step is not another finite scan. It is a counting or
density-over-primes theorem for bad-prime exchange events:

```text
p | Norm(Delta_{t-1})
```

as the robustly aperiodic exchange core varies.

That density/counting bound is CONJECTURAL here.

## 7. Verifier

`experimental/scripts/verify_l1_prefix_dyadic_charzero_rigidity.py` checks:

- exact divisibility by `Phi_n(Y)=Y^{n/2}+1` via coefficient relations, with no
  floating-point roots;
- signed-coefficient antipodal classification for `n=8` and `n=16`;
- the locator equivalence `B=-B iff L_B(X) in Q(zeta_n)[X^2]`;
- all three `F_17` collision orbits have algebraically nonzero
  `Delta_{t-1}`;
- `17` divides the norm of that first coefficient for every orbit;
- the size-8 orbit where negation swaps the complements is not misclassified as
  `B=-B`;
- the prime-power `K_ell` generalization on `n=9`, `ell=3`.

The finite norm certificates are experimental diagnostics. The signed
first-moment rigidity theorem and its prime-power generalization are proved.
