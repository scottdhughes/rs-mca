# L1 Prefix: Centered Krawtchouk Route Cut

Date: 2026-06-25

Status: AUDIT / ROUTE CUT.  The centered identities below are correct under
the stated rank hypotheses.  Averaged statements over all tested subsets must
either restrict to full-rank subsets or replace the uniform baseline `p^{-s}`
by `p^{-rank(T)}` subset by subset.

## Purpose

This note repairs a tempting but false dense-support argument in the dual
Bessel lane.  A single tested moment zero has an unavoidable uniform
`1/p` baseline, so it cannot be exponentially rare.  The support-average
Krawtchouk transform cancels those baselines exactly, but the cancellation
leaves a high-order centered correlation problem rather than a
single-moment anticoncentration problem.

## Setup

Let `S` be the tested moment coordinates, `|S|=t`.  For `U subset S`,
`|U|=u`, define the coefficient-torus average

```text
A_U =
(p-1)^(-u) sum_{r in (F_p^*)^U} exp(-lambda E_U(r)).
```

Let `Y=(Y_1,...,Y_N)` have independent Bessel-law coordinates, and let

```text
M_j(Y)=sum_i a_{j,i}Y_i.
```

Fourier expansion gives

```text
A_U =
E_Y prod_{j in U}
[
  (p-1)^(-1) sum_{r_j != 0} psi(r_j M_j(Y))
].
```

By additive-character orthogonality,

```text
(p-1)^(-1) sum_{r != 0} psi(rm)
= 1                 if m=0,
= -1/(p-1)          if m!=0.
```

With `I_j=1_{M_j=0}`, the bracket is

```text
kappa(M_j) = (p I_j - 1)/(p-1)
           = (p/(p-1))(I_j - 1/p).
```

Therefore

```text
A_U =
(p/(p-1))^u
E prod_{j in U} (I_j - 1/p).
```

Averaging over all `u`-element coefficient supports gives

```text
bar A_u =
(p/(p-1))^u
E [
  e_u(I_1-1/p,...,I_t-1/p) / binom(t,u)
].
```

This is the exact centered Krawtchouk identity.

## Zero-Count Form

Let

```text
Z=#{j in S:M_j=0},       W=t-Z.
```

Then

```text
bar A_u = E Phi_u(W),
```

where

```text
Phi_u(W)=
binom(t,u)^(-1)
sum_{k=0}^u
binom(W,k) binom(t-W,u-k) (-1/(p-1))^k.
```

Under the uniform law on `F_p^t`, the zero indicators are independent
Bernoulli `(1/p)`, and every centered coefficient of positive degree has
expectation zero.  The uniform `1/p` baselines cancel exactly.

## Joint-Deviation Transform

For `T subset S`, `|T|=s`, define

```text
P_T = Pr[M_j=0 for every j in T].
```

When the `s` moment forms have rank `s`, the uniform baseline is `p^{-s}`.
Set

```text
Delta_T = P_T - p^{-s},
bar Delta_s = binom(t,s)^(-1) sum_{|T|=s} Delta_T.
```

Expanding the centered product and cancelling the uniform terms gives

```text
bar A_u =
(p/(p-1))^u
sum_{s=1}^u
binom(u,s) (-1/p)^(u-s) bar Delta_s.
```

Equivalently,

```text
bar A_u =
(p/(p-1))^u
sum_{j=0}^{u-1}
binom(u,j) (-1/p)^j bar Delta_{u-j}.
```

The inverse transform is

```text
bar Delta_s =
p^{-s} sum_{v=1}^s binom(s,v)(p-1)^v bar A_v,
```

or, in zero-count language,

```text
bar Delta_s =
E binom(Z,s)/binom(t,s) - p^{-s}.
```

## Correct Odlyzko Bound

The product-measure subspace lemma decays with codimension.  If the moment
forms indexed by `T` have rank `s`, their common zero set has codimension
`s`, so

```text
P_T <= nu_0^s,
```

where `nu_0=max_x nu_lambda(x)=nu_lambda(0)`.

The exponent is `s`, not `N-s` and not `N-1` for one equation.  Substituting
this into the centered transform yields the unconditional estimate

```text
bar A_u
<=
((p nu_0 + 1)/(p-1))^u - (p-1)^(-u)
<= beta_{p,lambda}^u,
```

where

```text
beta_{p,lambda}=(p nu_0+1)/(p-1).
```

When `beta_{p,lambda}<1`, this is exponential in `u`.  At the reserve scale
`u=Theta(N/log N)`, it is only `exp(-Theta(N/log N))`, not `exp(-Theta(N))`.

## Counterexample to the False Single-Zero Closure

For

```text
p=257, N=128, lambda=1/3,
```

one has

```text
Pr[M_1=0] ~= 1/p
```

but

```text
nu_0^(N-1) ~= 1.55e-9.
```

Thus

```text
Pr[M_1=0] <= nu_0^(N-1)
```

is false by more than six orders of magnitude.  The centered deviation
`Pr[M_1=0]-1/p` is small; the uncentered event is not.

## Near-Full-Deviation Criterion

The centered identity gives a correct sufficient criterion.  For `L<=u`,

```text
bar A_u
<=
(p/(p-1))^u
[
  sum_{j=0}^{L-1} binom(u,j)p^{-j} bar Delta_{u-j}
  +
  sum_{j=L}^{u-1} binom(u,j)p^{-j}
].
```

If

```text
u=Theta(N/log N),      p>=2N+1,      L=epsilon u,
```

then the second sum is `exp(-Omega_epsilon(N))`.  Therefore, if for some
`c,epsilon>0`,

```text
sup_{(1-epsilon)u <= s <= u} bar Delta_s <= exp(-cN),
```

then

```text
bar A_u <= exp(-c'N).
```

The primitive version must use the unnormalized primitive submass with the
same denominator as the full average.  Conditional averages normalized only
over primitive frequencies need a separate denominator analysis.

## Status

PROVED under the full-rank moment-subset hypothesis:

- exact centered torus/Krawtchouk identity;
- exact cancellation of uniform `1/p` baselines;
- joint-zero-deviation transform and inverse;
- correct codimension-`s` Odlyzko bound;
- unconditional `exp(-Theta(u))` estimate when `beta_{p,lambda}<1`;
- near-full-deviation criterion for `exp(-Theta(N))`.

COUNTEREXAMPLE:

- `Pr[M_j=0] <= nu_0^(N-1)`;
- crude uncentered single-zero closure.

OPEN:

- exponential control of near-full averaged joint deviations;
- primitive dense-support Bessel-energy bound;
- uniform generated-field prefix local limit.
