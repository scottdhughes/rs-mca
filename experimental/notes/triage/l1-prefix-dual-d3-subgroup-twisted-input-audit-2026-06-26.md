# L1 d=3 Subgroup Twisted Input Audit

Date: 2026-06-26

Status: AUDIT / STANDARD-WEIL-INPUT / EXPERIMENTAL.

## Purpose

The `d=2` cubic subgroup theorem proves an actual `H^{2k}` collision estimate
by expanding the subgroup indicator into multiplicative characters and then
using one-variable mixed Kummer--Artin--Schreier bounds.  This note audits the
next standard input needed for the `d=3` template.  It does not prove a full
`d=3` collision theorem.

The object that would arise after subgroup expansion is

```text
sum_{h in H} psi(a1 h + a3 h^3 + a5 h^5),
```

and the twisted inner sums are

```text
sum_{x in F_p^*} chi(x) psi(a1 x + a3 x^3 + a5 x^5).
```

The question is whether the cubic proof template extends with a standard
degree-five one-variable mixed-character bound, which exact constant is
justified, what degeneracies must be excluded, and whether the resulting
bound has any nonvacuous parameter window.

## Standard Input Needed

Assume `p>5`.  Let `chi` be a multiplicative character of `F_p^*`.

### Linear stratum

If `a1 != 0` and `a3=a5=0`, then

```text
|sum_{x in F_p^*} chi(x) psi(a1 x)| <= sqrt(p)
```

for nontrivial `chi`, while the trivial-character sum has absolute value
`1`.  This is the same Gauss input used in the cubic branch.

### Cubic lower stratum

If `a5=0` and `a3 != 0`, the previously imported cubic bound gives

```text
|sum_{x in F_p^*} chi(x) psi(a1 x + a3 x^3)| <= 3 sqrt(p).
```

This is a lower-degree stratum, not a failure of the degree-five input.

### Quintic top stratum

If `a5 != 0`, import the conservative bound

```text
|sum_{x in F_p^*} chi(x) psi(a1 x + a3 x^3 + a5 x^5)| <= 5 sqrt(p).
```

For nontrivial `chi`, use Katz, *Estimates for Nonsingular Mixed Character
Sums*, Theorem 1.1
(`https://web.math.princeton.edu/~nmk/nsingmixedfinal.pdf`), with

```text
n=1,  f(X)=a1 X+a3 X^3+a5 X^5,  g(X)=X,  d=5,  e=1.
```

Because `a5 != 0` and `p>5`, `f` has degree `5` prime to the characteristic
and is Deligne in the one-variable sense used by Katz.  The Kummer factor is
`g=X`, of degree `1`.  Katz's displayed one-variable constant gives

```text
C(1,5,1) = (5-1)+(1-1)+1 = 5.
```

For the trivial multiplicative character, the ordinary additive Weil/Deligne
bound for a degree-five polynomial gives at most `4 sqrt(p)` for the full
affine sum over `F_p`.  Passing to `F_p^*` removes the `x=0` term, so the
bound becomes `4 sqrt(p)+1`, which is at most `5 sqrt(p)` for `p>5`.

## Degeneracies To Exclude

The degree-five standard input is only being claimed in the top stratum:

```text
p > 5,  a5 != 0.
```

The following cases must remain separate:

- `p <= 5`: the degree-five Deligne/Katz input is not invoked.
- `a5=0, a3!=0`: use the cubic `3 sqrt(p)` input.
- `a5=a3=0, a1!=0`: use the linear Gauss input.
- `a1=a3=a5=0`: this is the principal frequency and contributes the random
  main term.

For `p>5` and `a5!=0`, the phase cannot be an Artin--Schreier coboundary plus
a constant in this degree-five polynomial setting, since its top degree is
prime to `p` and below `p`.

## Candidate d=3 Moment Bound

If the exact `d=3` Fourier identity is later written out, it will have the
form

```text
V_{H,k}^{(3)}
 = p^{-3} sum_{a1,a3,a5 in F_p} |S_H(a1,a3,a5)|^{2k},
```

with principal term

```text
n^{2k}/p^3.
```

Using the stratified inputs above would give the candidate error bound

```text
0 <= V_{H,k}^{(3)} - n^{2k}/p^3
   <= (p-1)/p^3 * p^k
      + (p-1)/p^2 * (3 sqrt(p))^{2k}
      + (p-1)/p * (5 sqrt(p))^{2k}.
```

Equivalently,

```text
0 <= V_{H,k}^{(3)}/n^{2k} - 1/p^3
   <= (p-1)/p^3 * (sqrt(p)/n)^{2k}
      + (p-1)/p^2 * (3 sqrt(p)/n)^{2k}
      + (p-1)/p * (5 sqrt(p)/n)^{2k}.
```

The top stratum dominates the exponential window.  Without Markov loss, the
candidate estimate has an exponentially decaying error when

```text
n > (5+epsilon) sqrt(p).
```

With low-energy Markov loss `alpha^{-2k}`, `alpha=1-2 tau`, the top-stratum
base becomes

```text
5 sqrt(p) / (alpha n),
```

so the window requires

```text
n > (5+epsilon) sqrt(p) / alpha.
```

## Audit Conclusion

The cubic `H^{2k}` proof template appears to extend to `d=3` at the level of
standard one-variable input, with top-stratum constant `5 sqrt(p)` under the
explicit hypotheses `p>5` and `a5!=0`.

This is only an input audit.  It does not claim:

- a full `d=3` proper-subgroup collision theorem;
- a sharp twisted constant;
- a higher-`d` theorem;
- a reserve-scale generated-field local limit.

## Verifier Coverage

The verifier
`experimental/scripts/verify_l1_prefix_dual_d3_subgroup_twisted_input_audit.py`
checks:

- subgroup character expansion for the quintic phase on tested rows;
- direct subgroup sums against character-expanded sums;
- Katz constants `C(1,3,1)=3` and `C(1,5,1)=5`;
- the trivial-character `4 sqrt(p)+1 <= 5 sqrt(p)` reduction for `p>5`;
- finite linear, cubic, and quintic mixed-sum ratios;
- the stratified candidate absolute and normalized bounds;
- nonvacuous parameter windows with and without Markov loss;
- explicit rejection of `p<=5`.

Tested finite rows use `p in {7,11,17,31}` and even subgroup orders dividing
`p-1`.

## Status

IMPORTED / VERIFIED FINITELY:

- linear Gauss input;
- cubic lower-stratum Katz input with `C(1,3,1)=3`;
- quintic top-stratum Katz input with `C(1,5,1)=5`;
- finite regressions of the imported inequalities.

OPEN:

- writing the full `d=3` collision theorem;
- optimizing the degree-five constant;
- extending the twisted input uniformly to higher odd moments;
- reserve-scale primitive low-energy count.
