# Axis g-Damping Spectral-Gap Lattice Bound

- **Status:** PROVED (single axis sub-case) / AUDIT.
- **Date:** 2026-07-14.
- **Scope:** the worst *monomial-resonance* direction of the exact second-moment
  (split-pair census) problem at the deployed KoalaBear list row.  This note proves one
  sub-lemma at the **deployed band depth** `w = 67471`; it does **not** assert MCA/list
  proximity safety, does not close the finite one-step problem, and does not edit Papers A–D.

## Summary

The exact second moment at the deployed band depth (`towards-prize.md` §0.3(4):
"the exact second moment is governed by the constant-shift split-pair census") splits, after
the prefix-fiber reformulation, into a sum over directions `t`.  The heaviest directions are
the **monomial axes** `t = s·e_j`, where the evaluation collapses onto a subgroup
`mu_h`, `h = n/gcd(j,n)`, with multiplicity `g = gcd(j,n)`.  At the deployed parameters the
worst axis is `j = 65536`, giving `h = 32`, `g = 2^16` (no smaller `h` is reachable, since
`j <= w` forces `gcd(j, 2^21) <= 2^16`).

This note proves that this worst axis contributes **negligibly**:
\[
  \kappa^2(h=32,\ g=2^{16}) \le 2^{-76842.78},
\]
against a requirement of `2^{-82.8}` (the level at which the axis contribution to the
normalized second moment is `O(1)`) — a margin of `76760` bits.

## Object

For a collapsed axis, the per-axis normalized second moment is
\[
  \kappa^2 = \frac{\sum_v N_j(v)^2}{\binom nm^2} - \frac1p,
  \qquad N_j(v) = \#\{\,S \subseteq \mu_n : |S| = m,\ \textstyle\sum_{a\in S} a^j = v\,\},
\]
the exact (integer) collision count of the single power-sum statistic `p_j` under
reduction mod `p`.  `kappa^2 = 1` is maximal concentration; `kappa^2 = 0` is perfect
equidistribution.

## Proof (Cauchy-saddle + exact lattice spectral gap)

Let `psi(z) = exp(2 pi i z / p)`, `r = m/(n-m)`, `lambda = 4 m (n-m)/n^2`,
`B = (1+r)^n / (r^m \binom nm)`.  With `G(s) = sum_{b in mu_32} psi(s b)`:

1. **Saddle bound.** Cauchy's coefficient formula and `|1 + r e^{iu}|/(1+r) <= exp(-lambda sin^2(u/2)/2)`
   give, for the axis word `E(s) = [x^m] prod_{b in mu_32}(1 + x psi(sb))^g`,
   \[
     |E(s)| / \binom nm \le B \exp\!\big(-\tfrac{\lambda g}{4}\,(32 - |G(s)|)\big).
   \]

2. **Spectral gap = exact lattice minimum.** `G(s) = sum_{k=0}^{15} 2 cos(2 pi s zeta^k / p)`
   with `zeta` of order 32 (`zeta^16 = -1`).  Using `1 - cos(2 pi u) >= 8 ||u||^2`, the gap
   `32 - |G(s)|` is lower-bounded by the shortest vector of the lattice
   `L = Z(1, zeta, ..., zeta^15) + p Z^16` (positive alignment) and its affine coset
   `2L - p·1` (negative alignment).  Exact Fincke–Pohst enumeration at the deployment prime:
   \[
     M_+ = 523523694273046106, \qquad M_- = 1853062447130638824,
   \]
   whence `32 - |G(s)| >= delta := min(16 M_+/p^2,\ 4 M_-/p^2) = 1.6326865391` for all `s != 0`.
   (The binding value is the anti-aligned `M_-` term.)

3. **Assemble.** `kappa^2 <= B^2 exp(-lambda g delta / 2)`.  With `lambda = 0.995860`,
   `log2 B = 10.82276`, `g = 65536`, `delta = 1.632687`:
   `log2 kappa^2 <= -76842.78`.

The bound is finite (not an extrapolation): the lattice minima are exact integers at the
deployment prime.

## Verifier

`experimental/scripts/verify_axis_gdamping_lattice.sage` (Sage/fplll) reproduces:
`zeta` order 32; `det L = p^15`; `M_+`, `M_-` byte-exact; `delta`, `lambda`, `B`,
`log2 kappa^2 <= -76842.78`; and a head-depth CRT-DP sanity of the exact `kappa^2(h=32, g)`
ladder (`g = 1,2,4` at `p = 61441` give `-22.50, -35.33, -60.36`, confirming the object).

**Cross-check (two engines).** `M_+` is independently reproduced by PARI `qfminim`
(exact enumeration), and `M_-` by PARI/Sage CVP; the two engines agree exactly.  The
head-depth `kappa^2` is independently reproduced by a PARI character-route
(`[x^m] prod(1 + x psi(sb))^g`) matching the CRT integer DP to 4 decimals.

**Lean.** The one elementary analytic step — `1 - cos(2 pi u) >= 8 u^2` for `|u| <= 1/2`,
used to reduce the character gap to the lattice minimum — is formalized 0-sorry in
`experimental/lean/grande_finale/GrandeFinale/AxisGdampingCosGap.lean` (Mathlib `v4.28.0`).
The exact lattice minima `M_+`, `M_-` are supplied by the Sage/fplll + PARI certificate above
(Mathlib has no shortest-vector infrastructure); the Cauchy-saddle coefficient estimate is
outside current Mathlib.  A full 0-sorry Lean proof is therefore not attempted here.

## Consumers

The axis piece of the deployed-band-depth second moment (`towards-prize.md` §0.3(4), (5);
the "hard finite problem" that "remains" at band depth `~6.7e4`).  This lemma discharges the
monomial-resonance term of that second moment.  The off-axis (arc-cluster) term reduces to a
theta-quotient equidistribution estimate that is **not** proved here (see risk-limits).

## Risk-limits

- Proves ONE axis sub-case at the deployed depth; does **not** close the finite one-step
  problem, and does **not** move any official safe/unsafe agreement.
- The off-axis theta-quotient (the arc-cluster directions) remains a `CONJECTURE` / `GAP-WALL`:
  its deployment estimate is a calibrated extrapolation, not a proof.
- No MCA/list/CA proximity-safety assertion; no `q_line`-for-`q_gen` entropy substitution;
  no Paper A–D or stable-TeX edit; no official-score movement.
