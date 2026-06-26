# L1 Prefix Dual d=2 Cubic Subgroup Twisted Bound

Date: 2026-06-26

Status: PROVED / STANDARD-WEIL-INPUT / EXPERIMENTAL.  The Fourier identity,
subgroup character expansion, and moment bound below are elementary once the
stated one-variable Gauss and Kummer--Artin--Schreier bounds are admitted.  No
full-field point-count theorem is used, and no full-torus or higher-`d`
statement is claimed.

## Purpose

The cubic point-count benchmark separated three different counting problems:

```text
FULL_AFFINE_Fp_POINTS
FULL_TORUS_Fp_POINTS
PROPER_SUBGROUP_H_POINTS
```

The Hooley--Katz audit applies to the full affine `F_p` collision variety.  It
does not count tuples whose coordinates are restricted to a proper
multiplicative subgroup.  This note proves the corresponding `d=2` cubic
proper-subgroup moment bound by expanding subgroup membership into
multiplicative characters and bounding the resulting twisted one-variable
sums.

## Setup

Let `p>3`, let `H <= F_p^*` have order `n`, and put

```text
m = (p-1)/n.
```

Fix a nontrivial additive character `psi` of `F_p`.  For `a,b in F_p`, define

```text
S_H(a,b) = sum_{h in H} psi(a h + b h^3).
```

For `k>=1`, define the proper-subgroup cubic collision count

```text
V_{H,k}
 = #{(x,y) in H^{2k}:
      sum_i x_i = sum_i y_i,
      sum_i x_i^3 = sum_i y_i^3}.
```

## Exact Fourier Identity

Additive orthogonality in the two moment coordinates gives

```text
1_{u=0} 1_{v=0}
 = p^{-2} sum_{a,b in F_p} psi(a u + b v).
```

Applying this to

```text
u = sum_i x_i - sum_i y_i,
v = sum_i x_i^3 - sum_i y_i^3
```

and separating the `x` and `y` variables gives

```text
V_{H,k}
 = p^{-2} sum_{a,b in F_p} |S_H(a,b)|^{2k}.
```

The `(a,b)=(0,0)` term is `n^{2k}/p^2`, so

```text
V_{H,k} - n^{2k}/p^2
 = p^{-2} sum_{(a,b)!=(0,0)} |S_H(a,b)|^{2k} >= 0.
```

This identifies the random-scale principal term as

```text
n^{2k}/p^2.
```

## Subgroup Character Expansion

Let `H^perp` be the group of multiplicative characters of `F_p^*` that are
trivial on `H`.  It has size `m`, and for `x in F_p^*`,

```text
1_H(x) = (1/m) sum_{chi in H^perp} chi(x).
```

Therefore

```text
S_H(a,b)
 = (1/m) sum_{chi in H^perp}
     sum_{x in F_p^*} chi(x) psi(a x + b x^3).
```

This is the exact boundary between the full-field benchmark and the
proper-subgroup problem: the subgroup restriction creates multiplicative
character twists.

## Twisted Sum Bounds

The following one-variable inputs are used.

1. If `a!=0`, then for the trivial character,

```text
sum_{x in F_p^*} psi(a x) = -1,
```

and for every nontrivial multiplicative character `chi`,

```text
|sum_{x in F_p^*} chi(x) psi(a x)| <= sqrt(p).
```

2. If `b!=0`, then for every multiplicative character `chi`,

```text
|sum_{x in F_p^*} chi(x) psi(a x + b x^3)| <= 3 sqrt(p).
```

For the trivial character this follows from the ordinary cubic Weil bound on
the full affine sum, plus the omitted `x=0` term.  For nontrivial `chi`, this
is the one-variable Kummer--Artin--Schreier bound for the mixed cubic phase.
The hypotheses `p>3` and `b!=0` are essential here: the phase
`f(x)=a x+b x^3` has degree `3` prime to the characteristic and is not an
Artin--Schreier coboundary plus a linear/constant term.  The constant `3` is
deliberately conservative.  The import trail is recorded separately in
`experimental/notes/triage/l1-prefix-dual-d2-cubic-subgroup-twisted-bound-import-audit-2026-06-26.md`.

Averaging over `H^perp` gives the usable subgroup bounds:

```text
S_H(0,0) = n,
|S_H(a,0)| <= sqrt(p)       (a!=0),
|S_H(a,b)| <= 3 sqrt(p)     (b!=0).
```

## Proper-Subgroup Collision Bound

Insert the three frequency classes into the exact Fourier identity.

The principal frequency contributes

```text
n^{2k}/p^2.
```

The `b=0, a!=0` frequencies give at most

```text
(p-1) p^{-2} (sqrt(p))^{2k}
 = (p-1) p^{-2} p^k.
```

The `b!=0` frequencies give at most

```text
p(p-1) p^{-2} (3 sqrt(p))^{2k}
 = (p-1) p^{-1} (3 sqrt(p))^{2k}.
```

Thus

```text
0 <= V_{H,k} - n^{2k}/p^2
   <= (p-1)/p^2 * p^k
      + (p-1)/p * (3 sqrt(p))^{2k}.
```

Equivalently,

```text
0 <= V_{H,k}/n^{2k} - 1/p^2
   <= (p-1)/p^2 * (sqrt(p)/n)^{2k}
      + (p-1)/p * (3 sqrt(p)/n)^{2k}.
```

The second term controls the exponential behavior.  If

```text
n > (3+epsilon) sqrt(p),
```

then `(3 sqrt(p)/n)^{2k}` decays exponentially in `k`.  This is the
proper-subgroup analogue of the moment-specific cubic estimate; it is not a
consequence of an untwisted full-affine point-count theorem.

## Relation to Full-Group and Full-Affine Bounds

When `H=F_p^*`, this theorem still applies, but it is not the sharp full-torus
bound from the cubic benchmark.  In the full group,

```text
S^x(a,0) = -1       (a!=0),
|S^x(a,b)| <= 2 sqrt(p)+1      (b!=0),
```

so the earlier full-torus bound is smaller.  The point of the present theorem
is different: it is uniform for every subgroup `H` and explicitly accounts for
the multiplicative-character twists introduced by `1_H`.

The Hooley--Katz/Ghorpade--Lachaud audit remains a full-affine benchmark.  It
does not imply the estimate here unless it is supplemented by uniform twisted
control for all multiplicative characters arising from the subgroup
restriction.

## Status

PROVED, using the stated one-variable character-sum input:

- exact proper-subgroup cubic collision Fourier identity;
- multiplicative-character expansion for `H`;
- `b=0` and `b!=0` twisted-sum bounds;
- proper-subgroup random-scale collision estimate;
- exponential error decay when `n > (3+epsilon) sqrt(p)`.

STANDARD-WEIL-INPUT:

- Gauss bound for nontrivial multiplicative characters with linear additive
  phase;
- one-variable Kummer--Artin--Schreier bound with conservative constant
  `3 sqrt(p)` for the cubic mixed sums.

EXPERIMENTAL:

- finite-row sharpness and constant profiles;
- comparison with the full-group torus benchmark.

OPEN:

- sharper twisted constants;
- higher-`d` proper-subgroup twisted collision bounds;
- reserve-scale primitive low-energy count.
