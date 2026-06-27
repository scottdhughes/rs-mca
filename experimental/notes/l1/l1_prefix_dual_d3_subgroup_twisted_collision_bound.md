# L1 Prefix Dual d=3 Subgroup Twisted Collision Bound

Date: 2026-06-26

Status: PROVED / IMPORTED STANDARD INPUT / EXPERIMENTAL.  The Fourier
identity, subgroup character expansion, frequency-stratum ledger, and collision
bound below are elementary once the stated one-variable Gauss and Katz
mixed-character inputs are admitted.  No full-affine point-count theorem is
used, and no general higher-`d` theorem is claimed.

## Purpose

The `d=2` cubic subgroup theorem closed the first proper-subgroup gap by
counting the actual `H^{2k}` object rather than substituting an untwisted
full-field point-count theorem.  The `d=3` input audit then isolated the
additional standard input: the quintic top stratum

```text
sum_{x in F_p^*} chi(x) psi(a1 x+a3 x^3+a5 x^5)
```

with `a5 != 0`, bounded by `5 sqrt(p)` through Katz's one-variable
mixed-character estimate.  This note promotes that audited input into the
corresponding `d=3` proper-subgroup collision theorem.

## Setup

Let `p>5`, let `H <= F_p^*` have order `n`, and put

```text
m = (p-1)/n.
```

Fix a nontrivial additive character `psi` of `F_p`.  For
`a1,a3,a5 in F_p`, define

```text
S_H(a1,a3,a5)
 = sum_{h in H} psi(a1 h+a3 h^3+a5 h^5).
```

For `k>=1`, define the proper-subgroup `d=3` odd-moment collision count

```text
V_{H,k}^{(3)}
 = #{(x,y) in H^{2k}:
      sum_i x_i   = sum_i y_i,
      sum_i x_i^3 = sum_i y_i^3,
      sum_i x_i^5 = sum_i y_i^5}.
```

## Exact Fourier Identity

Additive orthogonality in the three moment coordinates gives

```text
1_{u1=0} 1_{u3=0} 1_{u5=0}
 = p^{-3} sum_{a1,a3,a5 in F_p} psi(a1 u1+a3 u3+a5 u5).
```

Applying this to

```text
u_j = sum_i x_i^j - sum_i y_i^j,  j in {1,3,5},
```

and separating the `x` and `y` variables gives

```text
V_{H,k}^{(3)}
 = p^{-3} sum_{a1,a3,a5 in F_p} |S_H(a1,a3,a5)|^{2k}.
```

The principal frequency `(0,0,0)` contributes `n^{2k}/p^3`, so

```text
V_{H,k}^{(3)} - n^{2k}/p^3
 = p^{-3} sum_{(a1,a3,a5)!=(0,0,0)}
     |S_H(a1,a3,a5)|^{2k}
 >= 0.
```

Thus the random-scale principal term is

```text
n^{2k}/p^3.
```

## Subgroup Character Expansion

Let `H^perp` be the group of multiplicative characters of `F_p^*` that are
trivial on `H`.  It has size `m`, and for `x in F_p^*`,

```text
1_H(x) = (1/m) sum_{chi in H^perp} chi(x).
```

Therefore

```text
S_H(a1,a3,a5)
 = (1/m) sum_{chi in H^perp}
     sum_{x in F_p^*}
       chi(x) psi(a1 x+a3 x^3+a5 x^5).
```

This expansion is the exact boundary between the proper-subgroup problem and
the full-affine point-count benchmark: subgroup membership creates
multiplicative-character twists.

## Stratified Twisted Sum Bounds

The proof uses the following one-variable inputs.

1. Principal frequency:

```text
S_H(0,0,0)=n.
```

2. Linear stratum:

```text
a3=a5=0,  a1!=0.
```

For the trivial multiplicative character,

```text
sum_{x in F_p^*} psi(a1 x) = -1,
```

and for every nontrivial multiplicative character `chi`,

```text
|sum_{x in F_p^*} chi(x) psi(a1 x)| <= sqrt(p).
```

Averaging over `H^perp` gives

```text
|S_H(a1,0,0)| <= sqrt(p).
```

3. Cubic lower stratum:

```text
a5=0,  a3!=0.
```

The already-sealed cubic mixed input gives

```text
|sum_{x in F_p^*} chi(x) psi(a1 x+a3 x^3)| <= 3 sqrt(p),
```

for every multiplicative character `chi`, hence

```text
|S_H(a1,a3,0)| <= 3 sqrt(p).
```

4. Quintic top stratum:

```text
a5!=0.
```

The `d=3` input audit imports Katz, *Estimates for Nonsingular Mixed Character
Sums*, Theorem 1.1
(`https://web.math.princeton.edu/~nmk/nsingmixedfinal.pdf`), with

```text
n=1,  f(X)=a1 X+a3 X^3+a5 X^5,  g(X)=X,  d=5,  e=1.
```

Because `a5!=0` and `p>5`, `f` has degree `5` prime to the characteristic,
and `g=X` has degree `1`.  Katz's displayed one-variable constant gives

```text
C(1,5,1) = (5-1)+(1-1)+1 = 5.
```

Thus for every nontrivial multiplicative character,

```text
|sum_{x in F_p^*} chi(x) psi(a1 x+a3 x^3+a5 x^5)| <= 5 sqrt(p).
```

For the trivial multiplicative character, the ordinary additive Weil/Deligne
bound gives `4 sqrt(p)` for the full affine degree-five sum, and deleting the
`x=0` term gives `4 sqrt(p)+1 <= 5 sqrt(p)` for `p>5`.  Hence

```text
|S_H(a1,a3,a5)| <= 5 sqrt(p)       (a5!=0).
```

This Katz input is imported standard input and is finitely audited in
`experimental/notes/triage/l1-prefix-dual-d3-subgroup-twisted-input-audit-2026-06-26.md`.
It is not reproved here.

## Frequency Counts

The nonprincipal frequencies split as:

```text
linear:       a3=a5=0, a1!=0       count = p-1,
cubic lower:  a5=0, a3!=0          count = p(p-1),
quintic top:  a5!=0                count = p^2(p-1).
```

Together with the principal frequency, these add to

```text
1 + (p-1) + p(p-1) + p^2(p-1) = p^3.
```

## Proper-Subgroup Collision Bound

Insert the frequency strata into the exact Fourier identity.  The principal
frequency gives `n^{2k}/p^3`.  The three error strata give:

```text
(p-1) p^{-3} (sqrt(p))^{2k}
 = (p-1)/p^3 * p^k,

p(p-1) p^{-3} (3 sqrt(p))^{2k},

p^2(p-1) p^{-3} (5 sqrt(p))^{2k}.
```

Therefore

```text
0 <= V_{H,k}^{(3)} - n^{2k}/p^3
   <= (p-1)/p^3 * p^k
      + p(p-1)/p^3 * (3 sqrt(p))^{2k}
      + p^2(p-1)/p^3 * (5 sqrt(p))^{2k}.
```

Equivalently,

```text
0 <= V_{H,k}^{(3)}/n^{2k} - 1/p^3
   <= (p-1)/p^3 * (sqrt(p)/n)^{2k}
      + p(p-1)/p^3 * (3 sqrt(p)/n)^{2k}
      + p^2(p-1)/p^3 * (5 sqrt(p)/n)^{2k}.
```

The final term controls the exponential behavior.  If

```text
n > (5+epsilon) sqrt(p),
```

then the normalized error decays exponentially in `k`.  With a low-energy
Markov loss `alpha^{-2k}`, `alpha=1-2 tau`, the corresponding sufficient
condition becomes

```text
n > (5+epsilon) sqrt(p) / alpha.
```

## Domain Separation

This theorem counts `PROPER_SUBGROUP_H_POINTS`, and it specializes to the full
torus only when `H=F_p^*`.  It does not count `FULL_AFFINE_Fp_POINTS`, and it
does not follow from the untwisted Hooley--Katz/Ghorpade--Lachaud audit unless
one also supplies uniform twisted estimates for the multiplicative characters
introduced by `1_H`.

## Status

PROVED:

- exact `H^{2k}` `d=3` odd-moment collision Fourier identity;
- multiplicative-character expansion of `1_H`;
- linear/cubic/quintic frequency-stratum ledger;
- proper-subgroup random-scale collision estimate;
- normalized error bound;
- exponential error decay when `n > (5+epsilon) sqrt(p)`.

IMPORTED / VERIFIED:

- Gauss linear bound;
- Katz one-variable mixed Kummer--Artin--Schreier bound with `C(1,5,1)=5`;
- finite small-row regressions of the imported inequalities.

NOT CLAIMED:

- general `d` proper-subgroup theorem;
- reserve-scale generated-field local limit;
- full-affine Hooley--Katz theorem;
- full-torus theorem beyond explicit comparison rows.

OPEN:

- sharper twisted constants;
- higher-`d` proper-subgroup twisted collision bounds;
- dense high-degree primitive low-energy count.
