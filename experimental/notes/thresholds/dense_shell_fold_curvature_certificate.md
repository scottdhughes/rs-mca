# Dense-shell FOLD: exact weighted-curvature certificate

## Status

```text
Status: PROVED PARTIAL.

For every monotone 18-value profile, the 18-over-17 spread fold is exactly
equivalent to one weighted second-difference inequality on its 17 drops.
If the drops are discretely concave, the sharper uniform factor 17/15 holds.

This does not prove that the realized dense-shell cascade has the required
monotonicity or curvature.  The full (FOLD) clause remains open.
```

This packet is theorem-shaped groundwork for Section 8.4 of
`dense_shell_prop_tail_reduction.md` at source floor
`upstream/main@3404d21`.  It does not repeat the packet's finite grid census.
In particular, the measured maximum `1.1322` remains COMPUTED evidence only.

The deterministic verifier is
`experimental/scripts/verify_dense_shell_fold_curvature_certificate.py`.
It checks exact integer coefficient identities, the third-difference sign,
the quadratic-profile literal, source markers, and fail-closed mutations.
The finite coefficient replay is a regression check; the proof is the exact
summation-by-parts argument below.  A stdlib-only Lean 4.14 package at
`experimental/lean/dense_shell_fold_curvature_certificate/` kernel-checks the
linear-arithmetic compiler.

Two in-session cross-checks preceded shipping.  One independently derived
the weighted identity and compiled a minimal Lean arithmetic skeleton.  The
other audited the Section 8.4 window, every constant and orientation, the
zero-spread boundary, the verifier mutations, and the final Lean declarations.
These are scoped in-session checks, not external verification.

## 1. Oriented drops and the exact identity

Let `L_0,...,L_17` be monotone.  Choose `sigma in {+1,-1}` so that

```text
p_i := sigma (L_i-L_{i+1}) >= 0,                 0 <= i <= 16.
```

Thus

```text
S := spread_{i<17}(L) = sum_{i=0}^{15} p_i,
spread_{i<18}(L)       = S+p_16.
```

Define the drop curvatures and positive weights

```text
kappa_j := p_{j+2}-2p_{j+1}+p_j,                0 <= j <= 14,
w_j     := (j+1)(15-j),
K       := sum_{j=0}^{14} w_j kappa_j.
```

The weights are

```text
15, 28, 39, 48, 55, 60, 63, 64, 63, 60, 55, 48, 39, 28, 15
```

and sum to `680`.

### Theorem 1 (weighted curvature identity)

For every real-valued drop vector `p_0,...,p_16`, without a sign
hypothesis,

```text
2S = 17p_0 + 15p_16 - K.                         (1)
```

#### Proof

Put `d_i=p_{i+1}-p_i`.  Since `kappa_j=d_{j+1}-d_j`, twice summing the
second differences gives

```text
p_i = p_0 + i d_0 + sum_{j=0}^{i-2} (i-1-j) kappa_j.   (2)
```

At `i=16`, (2) gives

```text
16d_0 = p_16-p_0-sum_{j=0}^{14}(15-j)kappa_j.          (3)
```

Summing (2) for `0 <= i <= 15`, substituting (3), and collecting the
coefficient of each `kappa_j` gives

```text
2S = 17p_0+15p_16-sum_{j=0}^{14}(j+1)(15-j)kappa_j.
```

This is (1).  QED.

### Theorem 2 (exact FOLD certificate)

Under the monotone-window setup, the denominator-cleared FOLD inequality

```text
50 spread_{i<18}(L) <= 57 spread_{i<17}(L)        (4)
```

is equivalent to

```text
7K <= 119p_0+5p_16.                               (5)
```

Indeed, (4) is `7S-50p_16 >= 0`, while (1) gives the exact identity

```text
2(7S-50p_16) = 119p_0+5p_16-7K.                  (6)
```

Thus (5) is neither an asymptotic surrogate nor a sufficient-only test: once
window monotonicity is known, it is exactly equivalent to FOLD.

## 2. A proved uniform subfamily

### Corollary 3 (discretely concave drops)

Assume the monotone-window setup and

```text
kappa_j <= 0                                      (0 <= j <= 14).   (7)
```

Then `K<=0`, and (1), together with `p_0>=0`, yields

```text
2S >= 15p_16.
```

Consequently

```text
15 spread_{i<18}(L) <= 17 spread_{i<17}(L),       (8)
50 spread_{i<18}(L) <= 57 spread_{i<17}(L),       (9)
```

because `17*50=850<855=57*15`.  If `S>0`, this is the ratio statement

```text
spread_{i<18}(L) / spread_{i<17}(L) <= 17/15 < 57/50.
```

If `S=0`, (1), nonnegativity, and (7) force `p_16=0`; the cleared
inequalities (8)-(9) still hold, while the ratio itself is intentionally left
undefined.

For a decreasing profile, `p_i=L_i-L_{i+1}` and

```text
kappa_j = - Delta^3 L_j.
```

Hence (7) is exactly the third-difference condition `Delta^3 L_j>=0`.  For
an increasing profile the sign is reversed, as dictated by the oriented-drop
definition.

### Corollary 4 (bounded positive curvature defect)

More generally, if `kappa_j<=delta` for all `j`, then

```text
K <= 680 delta.
```

Therefore the exact sufficient condition

```text
4760 delta <= 119p_0+5p_16                       (10)
```

implies FOLD.  Keeping the individual weighted sum `K` in (5) is sharper;
(10) is only the uniform-defect corollary.

## 3. The quadratic profile is exact

For the decreasing quadratic profile

```text
L_i=A-Ci^2,                                       C>0,
```

one has

```text
p_i=C(2i+1),
kappa_j=0,
spread_{i<17}(L)=C(1+3+...+31)=256C,
spread_{i<18}(L)=C(1+3+...+33)=289C.
```

Thus its exact ratio is `289/256`, and

```text
289/256 < 57/50
```

by the exact comparison `14450<14592`.  This proves the arithmetic CLT
profile literal.  It does not prove that a realized cascade profile is
quadratic or obeys (7).

## 4. Consumer ceiling and missing lemma

The proved result applies only to profiles for which all eighteen values lie
in one monotonicity orientation.  Corollary 3 further requires the stated
third-difference sign on the full index window `j=0,...,14`.  No claim is made
outside that domain.

Accordingly, this packet does not discharge Section 8.4's full (FOLD) clause
and does not upgrade PROP-TAIL.  The remaining analytic input can now be
stated precisely:

> **Missing realized-profile lemma.**  Prove, uniformly on the actual
> Section 8.4 parameter domain, either (i) the monotone-window hypotheses and
> the exact weighted inequality `7K<=119p_0+5p_16`, or (ii) a direct spread
> bound strong enough to replace it.  The stronger pointwise condition
> `kappa_j<=0` is sufficient but is not asserted to be necessary.

This is a statement of the open input, not a TODO disguised as a theorem.
