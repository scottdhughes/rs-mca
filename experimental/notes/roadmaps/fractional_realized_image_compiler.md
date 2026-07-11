# Fractional realized-image compiler

**Status:** `PROVED` as an exact incidence compiler; `OPEN` as A4 payment.

For each actual slope `gamma` in one exact-agreement first-match cell, let
`Omega_gamma` be its retained-support family and let `n_gamma(z)` count those
supports with boundary value `z`. Put

```text
m_gamma=sum_z n_gamma(z),
E_gamma=sum_z n_gamma(z)^2,
P_gamma=m_gamma^2/E_gamma,
Theta_gamma=L/P_gamma=L E_gamma/m_gamma^2.                (1)
```

Assume the actual support families are pairwise disjoint. If `M` is a support
capacity for their union and `N(z)` is a pointwise boundary capacity, then

```text
sum_gamma P_gamma<=M,
sum_gamma n_gamma(z)<=N(z).                               (2)
```

The first inequality uses `P_gamma<=m_gamma` and disjointness; the second is
the pointwise form of the same incidence capacity.

## Fractional cover theorem

Suppose `K>=0` and nonnegative weights `omega(z)` satisfy, for every actual
slope,

```text
(K/L)P_gamma+sum_z omega(z)n_gamma(z)>=1.                 (3)
```

Summing (3) and applying (2) gives the exact payment

```text
|Z^circ|<=K M/L+sum_z omega(z)N(z).                       (4)
```

This is the correct normalization: the support-capacity charge is `M/L`, not
`L/M`. The theorem is an exact finite inequality and does not use a formal
codomain in place of the realized boundary image.

Useful specializations include:

- **Threshold charge:** slopes with `Theta_gamma<=K` are paid by the first
  term of (3).
- **Harmonic form:** `sum_gamma Theta_gamma^(-1)<=M/L`.
- **Diffuse charge:** the remaining slopes may be paid by boundary weights
  whose pointwise cost is controlled by `N(z)`.
- **First-match add-back:** applying (4) separately on disjoint ordered cells
  and summing preserves the exact profile ledger.

The character-frame identity for the probability measure
`mu_gamma(z)=n_gamma(z)/m_gamma` reads

```text
Theta_gamma=(L/Q_gamma)
  sum_chi |hat(mu_gamma)(chi)|^2,                         (5)
```

with the source's Fourier normalization and realized boundary group of size
`Q_gamma`. Any frame input must retain representation multiplicities; no
unweighted difference-set energy is substituted.

## Verification and remaining wall

```text
python3 experimental/scripts/verify_fractional_realized_image_compiler.py
```

The standard-library verifier exhausts `6,144` small exact incidence/payment
systems, checks (1)--(4) with `Fraction` arithmetic, and includes tamper tests
for reversing `M/L`, `m^2/E`, `L/P`, or `n/m`.

The first unproved line is source-specific: prove (3), with subexponential
total right-hand side, for one named post-atlas primitive weighted-
Vandermonde class. This note does not establish that certificate, primitive
Q, A4, A2, A6, A7, a deployed finite row, a complete upper ledger, or
`U(a0+1)<=B*`.
