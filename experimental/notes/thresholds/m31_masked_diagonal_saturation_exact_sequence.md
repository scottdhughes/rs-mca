# M31 masked diagonal saturation: exact sequence and rank-three bound

## Status

**PROVED LOCAL / CONDITIONAL M31 COROLLARY / INDEPENDENT HOSTILE AUDIT
ACCEPT / LEDGER MOVEMENT ZERO / OFFICIAL SCORE `0/2`.**

This note closes one algebraic part of `UNPAID_MASKED_DIAGONAL_SATURATION`.
It does not close the Mersenne-31 list row.

The diagonal-saturation isomorphism and its equal-degree row shift overlap
with live PR #1014. The nonduplicate contribution here is:

1. a canonical exact sequence and exact colength for the saturation quotient;
2. successive-minimal-index monotonicity for a full-rank submodule;
3. the primitive-row degree-sum identities;
4. an RS-specific lower bound for the largest actual-error index; and
5. the resulting conditional padded rank-three bound
   `lambda_1 + lambda_2 + lambda_3 <= 62,295 < 67,447`.

The numerical statement is per marked rank-46 packet, conditional on a
hypothetical forbidden M31 list. The source compiler forces at least 259,881
such packets if that list exists; it does not assert that exactly 259,881
packets exist.

## 1. Algebraic setup

Let `F` be a field and `A=F[X]`. Fix `t>=2`. Let

```text
P_1,...,P_t, Q_1,...,Q_t in A
```

be monic nonzero polynomials with

```text
deg P_i=e,  deg Q_i=d,  gcd(P_1,...,P_t)=1.
```

Put `W_i=P_i Q_i`, let `G=gcd(W_1,...,W_t)` be monic, and set
`g=deg G`. Define

```text
M = Syz(P_1,...,P_t),
N = {a in M : Q_i divides a_i for every i}.
```

Write the sorted minimal indices of `M`, `N`, and `Syz(W_1,...,W_t)` as

```text
mu_1 <= ... <= mu_(t-1),
nu_1 <= ... <= nu_(t-1),
lambda_1 <= ... <= lambda_(t-1).
```

Row degree is the maximum coordinate degree. Minimal indices are the sorted
row degrees of a row-reduced basis.

## 2. Exact diagonal-saturation theorem

### Theorem 2.1

Under the setup above:

1. Coordinatewise multiplication is an isomorphism

   ```text
   Delta_Q : Syz(W_1,...,W_t) -> N,
   (b_i) |-> (Q_i b_i).
   ```

2. Equal padding degrees give the exact shift

   ```text
   nu_i = lambda_i + d.
   ```

3. There is a canonical exact sequence of finite-length `A`-modules

   ```text
   0 -> M/N -> direct_sum_i A/(Q_i) -> A/(G) -> 0,       (2.1)
   ```

   where the last map sends `(a_i mod Q_i)` to
   `sum_i P_i a_i mod G`. Consequently,

   ```text
   dim_F(M/N)=td-g.                                      (2.2)
   ```

4. Inclusion cannot decrease a successive minimal index:

   ```text
   nu_k >= mu_k  for 1<=k<=t-1.                         (2.3)
   ```

5. The degree sums are

   ```text
   sum_i mu_i=e,
   sum_i lambda_i=e+d-g.                                (2.4)
   ```

### Proof

For (1), `sum_i W_i b_i=0` is equivalent to
`sum_i P_i(Q_i b_i)=0`. The image has each coordinate divisible by `Q_i`,
and coordinatewise division gives the inverse.

For (2), every monic `Q_i` has the same degree `d`, so multiplication by the
diagonal `Q` raises every nonzero row degree by exactly `d` and preserves the
row-leading coefficient vector. It therefore maps a row-reduced basis to a
row-reduced basis with all row degrees shifted by `d`.

For (3), define

```text
psi : direct_sum_i A/(Q_i) -> A/(G),
psi((a_i)) = sum_i P_i a_i mod G.
```

This is well-defined because changing `a_i` by `Q_i b_i` changes the sum by
`W_i b_i`, which is divisible by `G`. It is onto because the primitive row
`P` has Bezout coefficients. The image of `M` in the source quotient has
kernel `N`, hence is `M/N`. It equals `ker psi`: if
`sum_i P_i a_i=Gh`, use `(W_1,...,W_t)=(G)` to choose `b_i` with
`sum_i W_i b_i=Gh`; then `(a_i-Q_i b_i)` is a syzygy representing the same
residue class. Taking `F`-dimensions gives (2.2).

For (4), let a rank-`r` polynomial module have a row-reduced basis with
sorted row degrees `alpha_i`. Predictable degree gives

```text
rdeg(sum_i f_i b_i)=max_i(deg f_i+alpha_i).
```

Therefore the largest possible `A`-rank of a family of elements of row degree
at most `s` is exactly the number of `alpha_i<=s`. Since `N` is contained in
`M`, the degree-bounded rank in `N` is at most that in `M`. This is equivalent
to `nu_k>=mu_k` for every `k`.

For (5), let `B` be a row-reduced `(t-1) x t` basis matrix for `M`. Its signed
maximal-minor vector spans the same one-dimensional right kernel over `F(X)`
as `P`. Since `P` is primitive and `A^t/M` is torsion-free, Smith normal form
shows that this minor vector is a unit multiple of `P`. Row reduction makes
one maximal minor have degree exactly `sum_i mu_i`, while each nonzero minor
has degree `e`; hence `sum_i mu_i=e`. Applying the same argument to the
primitive row `U_i=W_i/G`, whose entries have degree `e+d-g`, gives the second
identity in (2.4).

## 3. RS exceptional-index lemma

Let `Omega` be `n=2K` distinct field points, let `y:Omega->F`, and let
`c_1,...,c_t` be distinct polynomials of degree less than `K`. Suppose every
`c_i` has exact error weight `j<K` against `y`. Let

```text
E_i = {x : c_i(x) != y(x)},
C_0 = intersection_i E_i,
c = |C_0|,
P_i = product_(x in E_i\C_0) (X-x).
```

### Theorem 3.1

For the minimal indices of `Syz(P_1,...,P_t)`,

```text
mu_(t-1) >= K-j+1.                                      (3.1)
```

### Proof

Set `D_0=K-j`. For a syzygy `A=(A_i)` of row degree at most `D_0`, define

```text
F_A = sum_i A_i P_i c_i.
```

At every `x` outside `C_0`, a term either vanishes because `x` is an error of
`c_i`, or has `c_i(x)=y(x)`. Thus the syzygy equation makes `F_A(x)=0` at all
`n-c` such points. But

```text
deg F_A <= (K-j)+(j-c)+(K-1)=n-c-1,
```

so `F_A=0`. Every degree-at-most-`D_0` element of `Syz(P)` therefore lies in
the simultaneous kernel of the rows `(P_i)` and `(P_i c_i)`. Those rows have
rank two over `F(X)`: proportionality would force all distinct `c_i` to equal
one rational function. Their simultaneous kernel has rank `t-2`. If
`mu_(t-1)<=D_0`, all `t-1` rows of a row-reduced basis would lie in that
rank-`t-2` kernel, a contradiction. This proves (3.1).

## 4. Conditional M31 rank-three corollary

Use the pinned values

```text
p = 2^31-1,       n = 2^21,       K = 2^20,
a = 1,116,023,    R = n-a = 981,129,
w = a-K = 67,447,
B* = floor(p^4/2^100) = 16,777,215.
```

Assume a hypothetical forbidden M31 list exists and fix one marked rank-46
packet forced by the source compiler in exact error-weight layer `j`. Remove
its actual common error core `C_0`. Let `P_i` be the reduced actual-error
locators and let `Q_i` locate the discarded agreement points under the fixed
first-`a` selector. Then

```text
deg Q_i=(n-j)-a=R-j=d.
```

With `W_i=P_iQ_i` and `g=deg gcd(W_i)`, Theorems 2.1 and 3.1 give

```text
lambda_45 = nu_45-d
          >= mu_45-d
          >= (K-j+1)-(R-j)
          = w+1
          = 67,448.                                      (4.1)
```

The degree sum is

```text
sum_(i=1)^45 lambda_i=R-|C_0|-g.
```

Hence

```text
sum_(i=1)^44 lambda_i <= 913,681.                         (4.2)
```

For nonnegative integers `x_1<=...<=x_m` of total at most `mq+r`, the exact
balancing bound is

```text
sum_(i=1)^k x_i <= kq + max(0,r-(m-k)).                  (4.3)
```

Indeed, either `x_k<=q`, or each of the final `m-k` entries is at least
`q+1`. Here `913,681=44*20,765+21`. Applying (4.3) to the first 44 indices
gives

```text
lambda_1                         <= 20,765,
lambda_1+lambda_2                <= 41,530,
lambda_1+lambda_2+lambda_3       <= 62,295 < 67,447,
lambda_1+lambda_2+lambda_3+lambda_4 <= 83,060.            (4.4)
```

Thus only the rank-three bound crosses the deployed width. No rank-four
conclusion follows.

## 5. Noncoloop gcd consequence

Let `U_i=W_i/G`, and let the first three rows of a row-reduced minimal basis
form a `3 x 46` matrix `H`. Distinguish the source packet's extra column. If
deleting it preserves rank three, choose a nonzero `3 x 3` minor `Delta_I`
among old columns and let `J` be the 43-column complement. Then

```text
gcd(U_j : j in J) divides Delta_I,
deg gcd(U_j : j in J) <= 62,295.                          (5.1)
```

For an irreducible `h`, let `m=min_(j in J) v_h(U_j)`. The equations
`H_I U_I=-H_J U_J`, followed by the adjugate of `H_I`, show that `h^m`
divides every `Delta_I U_i`, `i in I`. Primitivity of `U` supplies an
`i in I` with `v_h(U_i)=0`, so `h^m` divides `Delta_I`. This proves (5.1)
with multiplicity. If deleting the extra column lowers rank, the old columns
have rank at most two; that coloop branch remains unpaid.

The minor controls only actual-common roots outside both the removed actual
core and the padded gcd. Typed roots from those two sets require a separate
add-back theorem.

## 6. Audit, overlap, and nonclaims

- Source base: `18cfc199d4612f5dfc01bf6c0155a65a1eaa3832`.
- Source-current Python verifier passed normal and `-O` checks and all 34
  semantic mutations in both modes.
- The repaired theorem's independent hostile-proof audit returned `ACCEPT`.
- Live PR #1014 head `c7cbcf1cff1180b4aac0862ae3c3e665f6b29b21`
  already contains the basic isomorphism/shift and the masked-root
  counterpacket. Those pieces are restated only to make this theorem
  self-contained.
- The exact audit and replay hashes are recorded in
  `experimental/data/certificates/m31-masked-diagonal-saturation/`.

This note does **not** prove existence or nonexistence of a forbidden list,
an exact packet count, a semantic first-match owner, a common-core add-back,
a rank-two coloop payment, cross-key deduplication, a full list upper bound,
an adjacent-row endpoint, recurrence, or an official theorem. Exact ledger
effect: `0`. Official score: `0/2`.
