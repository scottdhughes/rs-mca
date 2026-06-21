# L1 Prefix Anchored Trinary-Kernel Rigidity

- **Status:** PROVED (anchored trinary bijection, coefficient gap, divisor
  partition, S-unit system, quotient-periodic composition criterion) /
  EXPERIMENTAL (finite trinary-solution distributions) / CONJECTURAL
  (robustly aperiodic polynomial bound) / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-21.
- **Scope:** Paper B `conj:prefix-local` in the monomial-prefix lane. This
  note does not assert the arbitrary-word `conj:arbitrary-local`,
  Reed--Solomon list-decoding safety, MCA, line-decoding, or protocol safety.

## Purpose

The Fourier orbit and scalar-packet reductions show where cancellation must
occur, but they still leave an exponentially large frequency problem. This note
records a different structural route.

Fix one complement subset `A_0` in a prefix fiber. Every other complement subset
`A` in the same fiber gives a signed difference function

```text
z_A(h)=1_A(h)-1_{A_0}(h) in {-1,0,1}.
```

Interpolating `z_A` on `H=mu_n` compresses the whole anchored fiber into
low-degree three-valued polynomials with fixed anchor signs. The remaining
aperiodic prefix problem becomes a polynomial rigidity/counting problem rather
than a generic Fourier-norm problem.

## 0. Field Scope and Prefix Convention

Work in the split odd prime-field setting

```text
H=mu_n <= F_p^*,        n | p-1.
```

The complement subset has size

```text
m=n-(k+sigma).
```

The verifier uses the power-sum prefix coordinates

```text
p_j(A)=sum_{a in A} a^j,        1 <= j <= sigma.
```

For `p>sigma`, Newton identities identify these coordinates with the top
`sigma` coefficients of the complement locator used in
`l1_prefix_divisor_count.md`.

## 1. Anchored Trinary Bijection

Fix `A_0 subset H`, `|A_0|=m`, and let

```text
F(A_0)
=
{A subset H : |A|=m, p_j(A)=p_j(A_0) for 1<=j<=sigma}.
```

For `A in F(A_0)`, define

```text
z_A(h)=1_A(h)-1_{A_0}(h)
```

and let `g_A in F_p[X]`, `deg g_A<n`, be the unique interpolation polynomial
with

```text
g_A(h)=z_A(h)        (h in H).
```

Since `A` and `A_0` have equal size and equal first `sigma` power sums,

```text
sum_{h in H} z_A(h) h^j = 0,        0 <= j <= sigma.
```

For `H=mu_n` and `g(X)=sum_{i=0}^{n-1} c_i X^i`,

```text
sum_{h in H} g(h) h^j = n c_{n-j},        1 <= j < n,
```

and

```text
sum_{h in H} g(h)=n c_0.
```

Because `n` is invertible in `F_p`, the moment equations are equivalent to

```text
c_0=0,        c_{n-1}=...=c_{n-sigma}=0.
```

Equivalently,

```text
g_A in X F_p[X],        deg g_A <= n-sigma-1.
```

The anchor signs are:

```text
h in A_0       => g_A(h) in {0,-1},
h notin A_0   => g_A(h) in {0,1}.
```

Let

```text
L_B(X)=prod_{b in B}(X-b).
```

The sign conditions are equivalently

```text
L_{A_0} | g(g+1),
L_{H\A_0} | g(g-1).
```

**Theorem (anchored trinary bijection).**

```text
F(A_0)
<-->
{
g :
  g in X F_p[X],
  deg g <= n-sigma-1,
  L_{A_0} | g(g+1),
  L_{H\A_0} | g(g-1)
}.
```

The map from left to right is `A -> g_A`. The inverse sends `g` to

```text
A(g)
=
{h in A_0 : g(h)=0}
 union
{h in H\A_0 : g(h)=1}.
```

**Proof.** The forward direction was proved above. Conversely, suppose `g`
satisfies the displayed conditions. On `A_0`, `g` has values `0` or `-1`; off
`A_0`, it has values `0` or `1`. Thus `g=1_{A(g)}-1_{A_0}` on `H`. The
condition `g in X F_p[X]` gives

```text
sum_{h in H} g(h)=0,
```

so `|A(g)|=|A_0|`. The degree gap gives

```text
sum_{h in H} g(h)h^j=0        (1<=j<=sigma),
```

so `A(g)` has the same prefix power sums as `A_0`. Hence `A(g) in F(A_0)`.
The two constructions are inverse because they agree pointwise on `H`. `square`

## 2. Global Trinary Divisor Partition

Every candidate satisfies

```text
X^n-1 | g(g^2-1),
```

because `g(h) in {-1,0,1}` for every `h in H`.

Assume odd characteristic. Define

```text
D_0 = gcd(g, X^n-1),
D_+ = gcd(g-1, X^n-1),
D_- = gcd(g+1, X^n-1).
```

Since `0`, `1`, and `-1` are distinct, these split divisors are pairwise
coprime and

```text
D_0 D_+ D_- = X^n-1.
```

If the exchange size between `A` and `A_0` is `t`, then

```text
deg D_+ = deg D_- = t,
deg D_0 = n-2t.
```

Indeed, `D_+` records points added to `A_0`, `D_-` records points removed from
`A_0`, and the zero divisor records unchanged membership.

## 3. Polynomial S-Unit System

Write

```text
g       = D_0 U_0,
g - 1   = D_+ U_+,
g + 1   = D_- U_-.
```

Then

```text
D_0 U_0 - D_+ U_+ = 1,
D_- U_- - D_0 U_0 = 1,
D_- U_- - D_+ U_+ = 2.
```

These identities are tautological after substituting the three displayed
factorizations, but they give a concrete polynomial S-unit system attached to
each anchored prefix-fiber collision.

Thus the anchored fiber is represented by a finite family of split divisor
partitions of `X^n-1` satisfying low-degree and anchor constraints.

## 4. Quotient-Periodic Composition Criterion

For `d | n`, let `K_d=mu_d <= H`.

**Lemma.** For `deg g<n`,

```text
g(kappa x)=g(x) for every kappa in K_d, x in H
```

if and only if

```text
g(X)=tilde g(X^d) mod (X^n-1).
```

Since `deg g<n`, this is equivalent to saying that every nonzero monomial
coefficient of `g` occurs in a degree divisible by `d`.

**Proof.** Write `g(X)=sum_{i=0}^{n-1} c_i X^i`. If `g` is invariant under
`K_d`, then for every `kappa in K_d`,

```text
sum_i c_i (kappa^i-1) x^i = 0        (x in H).
```

The functions `x^i`, `0<=i<n`, are linearly independent on `H`. Hence
`c_i(kappa^i-1)=0` for every `i` and every `kappa in K_d`. If `c_i != 0`, then
`kappa^i=1` for all `kappa in K_d`, so `d | i`. Conversely, if only multiples
of `d` occur, then `g(kappa x)=g(x)` for every `kappa in K_d`. `square`

This places the quotient-periodic lane directly inside the anchored trinary
model. Quotient-periodic solutions are precisely the compositional trinary
solutions, and low-defect quotient closures correspond to solutions near these
composition strata.

## 5. Correct Robustly Aperiodic Target

After removing compositional quotient-periodic solutions and the low-defect
closures already isolated in the quotient-defect lane, the structural target is
the following conjectural rigidity statement:

```text
#{ anchored, robustly aperiodic g :
     g in X F_p[X],
     deg g <= n-sigma-1,
     X^n-1 | g(g^2-1),
     anchor signs relative to A_0 hold }
<= n^B.
```

This note does not prove that bound. It supplies the exact algebraic object on
which such a bound should be attacked.

The point is that the remaining prefix-local difficulty is no longer merely an
exponentially large Fourier sum. It can also be phrased as a rigidity/counting
problem for low-degree three-valued polynomials on a multiplicative subgroup,
with quotient-periodic composition components explicitly visible.

## 6. Verifier

`experimental/scripts/verify_l1_prefix_trinary_kernel_rigidity.py` checks:

- prefix fibers and independent anchored trinary enumeration;
- the bijection in both directions;
- `g(0)=0` as the zero constant coefficient and the degree gap
  `deg g <= n-sigma-1`;
- both anchor divisibilities;
- `X^n-1 | g(g^2-1)`;
- the divisor partition `D_0D_+D_-=X^n-1`;
- the three S-unit equations;
- recovery of `A` from the value partition of `g`;
- stabilizers of the value partition against the composition criterion
  `g=tilde g(X^d)`;
- rejection of global three-valued low-degree solutions that violate the
  anchor signs;
- the known `F_17,n=16,k=6,sigma=4` forty-collision certificate in trinary
  language;
- a proper-subgroup regression with `p=17,n=8`.

The finite distributions are experimental diagnostics. The robustly aperiodic
polynomial bound remains CONJECTURAL.
