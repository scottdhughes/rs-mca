# L1 d=2 Cubic Subgroup Twisted Bound Import Audit

Date: 2026-06-26

Status: IMPORTED / VERIFIED FINITELY.

## Purpose

The theorem note
`experimental/notes/l1/l1_prefix_dual_d2_cubic_subgroup_twisted_bound.md`
proves the proper-subgroup cubic collision estimate after importing two
standard one-variable character-sum bounds.  This audit records exactly what
is imported and how the verifier tests the imported bounds on finite rows.

The imported inputs are not full-affine point-count theorems.  They are
one-variable twisted character-sum estimates used after expanding the subgroup
indicator into multiplicative characters.

## Input A: Linear Gauss Sums

For `a != 0`,

```text
sum_{x in F_p^*} psi(a x) = -1
```

for the trivial multiplicative character, so the absolute value is exactly
`1`.  For every nontrivial multiplicative character `chi`,

```text
|sum_{x in F_p^*} chi(x) psi(a x)| <= sqrt(p).
```

Status: IMPORTED / STANDARD / VERIFIED FINITELY.

The verifier reports this under `standard_input_bound_cases` using:

```text
gauss_linear_bound_ok
max_observed_b0_ratio
```

and also records the trivial-character absolute value separately.

## Input B: Cubic Kummer--Artin--Schreier Sums

For `b != 0`, every multiplicative character `chi`, and `p>3`, import

```text
|sum_{x in F_p^*} chi(x) psi(a x + b x^3)| <= 3 sqrt(p).
```

Status: IMPORTED / STANDARD-WEIL-INPUT / VERIFIED FINITELY.

The nondegeneracy condition used here is visible in this cubic case: because
`p>3` and `b!=0`, the phase

```text
f(x)=a x + b x^3
```

has degree `3` prime to `p` and is not an Artin--Schreier coboundary plus a
constant on the affine line.  In the rational-function formulation, the
degree-three term prevents `f` from being of the form
`alpha(g(x)^p-g(x))+beta x+constant`.  The constant `3` is deliberately
conservative and is the only value consumed by the collision bound.

The verifier reports this under `standard_input_bound_cases` using:

```text
twisted_cubic_bound_ok
max_observed_b_nonzero_ratio
```

## Source Support

- Primary source for the conservative `3 sqrt(p)` constant: Nicholas M. Katz,
  *Estimates for Nonsingular Mixed Character Sums*,
  International Mathematics Research Notices 2007, Article ID rnm069
  (`https://web.math.princeton.edu/~nmk/nsingmixedfinal.pdf`).  Theorem 1.1
  gives a square-root bound with explicit constant `C(n,d,e)` for mixed sums
  `sum_x psi(f(x)) chi(g(x))` when `f` and `g` are Deligne polynomials satisfying
  the stated transversality hypotheses.  In the one-variable case used here,
  take

  ```text
  n=1,  f(X)=aX+bX^3,  g(X)=X,  d=3,  e=1.
  ```

  Since `b!=0` and `p>3`, `f` is Deligne of degree `3`, and `g=X` has degree
  `1`.  Katz's displayed formula gives

  ```text
  C(1,3,1) = (3-1)+(1-1)+1 = 3.
  ```

  Thus every nontrivial multiplicative-character twist satisfies the imported
  `3 sqrt(p)` bound.

- For the trivial multiplicative character and `b!=0`, use the ordinary
  additive Weil/Deligne bound for a degree-three polynomial: the full affine
  sum over `F_p` is bounded by `2 sqrt(p)`.  Passing to `F_p^*` changes the
  sum by the omitted `x=0` term, so the bound becomes `2 sqrt(p)+1`, which is
  at most `3 sqrt(p)` for `p>3`.

- Lei Fu, *Twisted Exponential Sums*
  (`https://arxiv.org/abs/math/0607164`), sets up finite-field mixed sums
  through Kummer sheaves and Artin--Schreier sheaves on tori and states that
  the resulting cohomological calculations estimate sums with multiplicative
  characters and additive phases under nondegeneracy hypotheses.
- Laszlo Merai, Igor E. Shparlinski, and Arne Winterhof, *Character sums over
  sparse elements of finite fields* (`https://arxiv.org/abs/2211.08452`),
  records a directly usable rational-function nondegeneracy framework for
  mixed multiplicative/additive character sums.  In particular, the paper
  states the natural Kummer and Artin--Schreier exclusions and notes that the
  additive-character condition applies when the additive rational function has
  degree at least `2` prime to the characteristic.

Before promotion outside `experimental/`, the exact theorem and constant should
be pinned to a primary source or textbook statement.  The present branch only
needs the conservative `3 sqrt(p)` inequality, and the finite verifier confirms
that the imported inequalities hold on the tested rows.

## Verifier Coverage

The verifier checks:

- exact subgroup character expansion for all tested `p,n`;
- direct sums against character-expanded sums;
- Katz's `C(1,3,1)=3` source-constant specialization;
- `2 sqrt(p)+1 <= 3 sqrt(p)` for the trivial-character cubic case when `p>3`;
- linear Gauss input ratios;
- cubic mixed input ratios;
- exact Fourier reconstruction of `V_{H,k}`;
- direct `H^{2k}` enumeration when under the explicit budget;
- exact histogram reconstruction when direct pair enumeration is too large;
- domain separation between full-affine, full-torus, and subgroup counts.

Tested rows use:

```text
p in {7,11,17,31},
k in {2,3,4},
even n | p-1.
```

## Status

IMPORTED / VERIFIED FINITELY:

- Input A, the linear Gauss bound;
- Input B, the cubic Kummer--Artin--Schreier bound with Katz constant
  `C(1,3,1)=3`;
- finite small-row regressions of both imported inequalities.

NOT CLAIMED:

- a new proof of the Weil/Kummer--Artin--Schreier theorem;
- a full-affine Hooley--Katz theorem;
- a full-torus theorem beyond comparison with the cubic benchmark;
- a higher-`d` subgroup theorem.
