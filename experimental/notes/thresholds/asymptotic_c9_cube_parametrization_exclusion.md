# Endpoint full-cube parametrization exclusion

Status: `PROVED / REUSABLE_CONSTRUCTION-CLASS_EXCLUSION`.

This packet excludes positive-rate endpoint common-fiber families presented by
full binary cubes with sublinear generator-coordinate incidence, or by coded
local rules with sublinear total local Walsh-span rank.  It applies after an
arbitrary mask, provided the parametrized image still has fixed weight and one
fixed endpoint syndrome.  It does not bound an arbitrary fiber or extract such
a cube from a large residual fiber.

## 1. Endpoint rows and notation

Let `N=2^s>=2`, let `p` be an odd prime with `N | (p-1)`, and let `zeta` have
order `N` in `F_p^x`.  Fix `alpha,c in F_p^x`, `1<=R<=N/2`, and

```text
a in {0,1,1-R,-R} modulo N.
```

For `0<=i<N`, put `t_i=alpha zeta^i` and define

```text
Phi_a(x) = sum_i x_i c zeta^(a i) (1,t_i,...,t_i^(R-1)).
```

The factors `c alpha^k` are nonzero row scalings, so the normalized syndrome
rows have exponents `a,a+1,...,a+R-1` modulo `N`.  Put

```text
D=R   if a in {0,1-R},
D=R+1 if a in {1,-R}.
```

Let `d>=0`, let `X:F_2^d -> {0,1}^N`, and assume that there are fixed `m` and
`y` such that, for every `u in F_2^d`,

```text
|X(u)|=m,                 Phi_a(X(u))=y.                 (H)
```

Let `U` be uniform on `F_2^d`; all entropies below are base two.  For
`0<=i<N` and `1<=j<=d`, define

```text
Inf_j(X_i) = Pr[X_i(U) != X_i(U+e_j)],
J_i        = {j : Inf_j(X_i)>0}.
```

## 2. Exact finite theorem

### Theorem 1 (nonlinear cube-incidence bound)

For every choice of the finite parameters and every map satisfying `(H)`,

```text
2D H_2(X(U)) <= sum_i sum_j Inf_j(X_i) <= sum_i |J_i|.   (I)
```

In particular, if `X` is injective, then

```text
2Dd <= sum_i |J_i|.                                      (I')
```

Thus, if every output coordinate is affected by at most `Delta` input
directions, then

```text
d <= N Delta/(2D).                                       (I'')
```

No linearity, coordinate disjointness, injectivity, or balanced-image
assumption is used in `(I)`.

### Theorem 2 (local Walsh-span bound)

Embed each Boolean coordinate in `F_p` and write its Walsh transform as

```text
hat X_i(lambda)
  = 2^(-d) sum_{u in F_2^d} X_i(u)(-1)^(lambda dot u)
  in F_p.
```

For each coordinate let

```text
V_i = span_F2{lambda != 0 : hat X_i(lambda) != 0},
r_i = dim_F2 V_i.
```

Then, for every map satisfying `(H)`, whether or not it is injective,

```text
(D+1) log_2 |im X| <= sum_i r_i.                         (W)
```

If `X_i` factors through `b_i` binary linear forms on `F_2^d`, followed by an
arbitrary Boolean function, then `r_i<=b_i` and hence

```text
log_2 |im X| <= (sum_i b_i)/(D+1).                       (W')
```

Consequently, if a `d`-dimensional binary linear code of physical switches is
parametrized by information bits, each output coordinate depends on at most
`Delta` physical switches, and the resulting common-fiber map is injective,
then

```text
d <= N Delta/(D+1).                                      (C)
```

## 3. Endpoint inputs

### Lemma 3 (fixed-weight endpoint distance)

Two distinct weight-`m` words in one `Phi_a` fiber have Hamming distance at
least `2D`.

### Proof

Cancel their common support and call the disjoint remainders `A` and `B`.
Equal weight gives `|A|=|B|=e>0`.  At `a=0`, syndrome equality gives equality
of the locator power sums through order `R-1=D-1`.  At `a=1`, the syndrome
gives orders `1,...,R` and equal weight supplies order zero, so the range is
again through `D-1=R`.  For `a=1-R` and `a=-R`, replace every locator by its
inverse and reverse the consecutive window; these become the preceding two
cases.

Because `N | (p-1)`, one has `p>N`.  If `e<=D-1`, Newton's triangular
identities are invertible through order `e`, so the equal power sums determine
the same elementary symmetric functions for `A` and `B`.  Their monic locator
polynomials are equal, contradicting the fact that `A` and `B` are disjoint
and nonempty.  Hence `e>=D`, and the Hamming distance is `2e>=2D`.

### Lemma 4 (augmented endpoint full spark)

Adjoin the weight row to the endpoint syndrome rows and delete a duplicate
row when exponent zero already occurs.  The resulting `D x N` matrix `W_a`
has exponent set

```text
{0,...,R-1}       for a=0,
{0,...,R}         for a=1,
{1-R,...,0}       for a=1-R,
{-R,...,0}        for a=-R.
```

Every nonzero vector in `ker W_a` has support at least `D+1`.

### Proof

Each exponent set is consecutive.  Multiplying each column by an appropriate
nonzero power of `zeta^i` shifts a negative window to `{0,...,D-1}`.  Every
`D`-column minor is therefore, up to a nonzero factor, the Vandermonde product

```text
product_{r<s} (zeta^(i_s)-zeta^(i_r)),
```

which is nonzero because the `zeta^i` are distinct.  Any at most `D` columns
are independent, proving the kernel-support claim.

## 4. Proof of the cube-incidence bound

Since `X` is deterministic and the input bits are independent, the chain rule
and conditioning on all other input bits give

```text
H_2(X(U))
 = sum_j I(X(U);U_j | U_{<j})
 <= sum_j I(X(U);U_j | U_{-j})
 = sum_j H_2(X(U) | U_{-j}).                             (1)
```

For fixed `U_{-j}`, the two equiprobable values of `U_j` give conditional
entropy one exactly when their outputs differ, and zero otherwise.  Hence the
last expression in `(1)` is

```text
sum_j Pr[X(U) != X(U+e_j)].                              (2)
```

Every changed edge joins two distinct words satisfying `(H)`, so Lemma 3
makes its output Hamming distance at least `2D`.  Averaging the Hamming
distance over directed cube edges gives

```text
sum_i sum_j Inf_j(X_i)
 >= 2D sum_j Pr[X(U) != X(U+e_j)]
 >= 2D H_2(X(U)).
```

Each influence is at most one and vanishes off `J_i`, proving the upper bound
in `(I)`.  Injectivity gives `H_2(X(U))=d`; summing `|J_i|<=Delta` proves the
two corollaries.

## 5. Proof of the Walsh-span bound

The vector `W_a X(u)` is constant in `u` by `(H)`.  Fourier transforming and
discarding the constant mode gives, for every `lambda!=0`,

```text
W_a hat X(lambda)=0.                                     (3)
```

Let `V=sum_i V_i` and `r=dim V`.  Every translation by an element of
`V^perp` fixes every active character of every coordinate, hence fixes `X`.
Thus `X` factors through `F_2^d/V^perp`, and

```text
|im X| <= 2^r.                                           (4)
```

Choose a basis `lambda_1,...,lambda_r` of `V` from the union of the active
mode sets.  Each coefficient vector `hat X(lambda_k)` is nonzero; `(3)` and
Lemma 4 give it support at least `D+1`.  For fixed `i`, the selected basis
modes active at coordinate `i` are independent elements of `V_i`, so there
are at most `r_i` of them.  Double counting the active coordinate-mode pairs
therefore gives

```text
(D+1)r
 <= sum_k |supp hat X(lambda_k)|
 <= sum_i r_i.                                           (5)
```

Combine `(4)` and `(5)` to obtain `(W)`.  If `X_i` factors through `b_i`
linear forms, all its active modes lie in their span, giving `(W')`; applying
this after a linear information-bit parametrization gives `(C)`.

## 6. Asymptotic route cut

Suppose along endpoint rows that `D>=kappa N` for fixed `kappa>0`.  Then

```text
max_i |J_i|=o(N)  and X injective  imply d=o(N),
max_i b_i=o(N)                         imply |im X|=exp(o(N)).
```

More quantitatively, let a nonempty exact residual have size `M`, image size
`L`, and image-mean fiber size `barN=M/L>=1`.  If a parametrized common-fiber
family `A_N` satisfies `|A_N|>=e^(cN) barN` for fixed `c>0`, then every
injective full-cube parametrization and every Walsh parametrization obey

```text
sum_i |J_i| >= (2 kappa c/ln 2) N^2,
sum_i r_i   >= (kappa c/ln 2) N^2.                       (6)
```

Taking a power-of-two subfamily changes the logarithm by less than one, hence
subtracts only `O(N)` from the right sides of `(6)`.  Thus a positive-rate
family cannot be generated by bounded-overlap trades,
sublinear-overlap nonlinear cube generators, a positive-rate affine binary
subspace, or linearly coded bounded-local-switch rules.  A surviving
positive-rate construction of these types must carry quadratic total
generator incidence or local Walsh rank.

## 7. Prior credit, nonclaims, and exact wall

The endpoint distance input is the previously preserved endpoint
locator-distance packet.  The affine/Walsh-support obstruction and the
independent disjoint-product specialization are also prior weaker routes and
are not claimed as the novelty here.  The contribution of this packet is the
arbitrary nonlinear full-cube entropy/influence incidence inequality and the
local Walsh-span image-rank formulation for arbitrary nonlinear coordinate
rules.

This packet does **not**:

- bound arbitrary endpoint fibers or extract a structured cube from one;
- prove literal or residual `C9-LD`;
- prove ordered `C1--C8` coverage, emission, or add-back;
- prove `RC`, pay a source cell, or move a deployed finite row;
- show that every exponential fiber contains a low-incidence or low-rank cube.

The exact remaining wall is an extraction theorem: from an exponentially
heavy exact post-`C1--C8` endpoint residual fiber, extract a positive-rate
parametrized subfamily with subquadratic total incidence or local Walsh rank,
or prove that the residual instead lies in a paid source class.  The present
theorem only rules out the extracted low-complexity alternative.

The repository authority for this packet is `origin/main` at
`2acc7bef9584fa34fc564d3b6ba827332a41bb90`.  Its source is the hostile-audit
survivor from Role 07, "Actual-row positive-rate counterpacket builder"; the
proof above has been rewritten to be self-contained rather than treating the
worker verdict as an authority.

## 8. Verification

Run

```sh
python3 experimental/scripts/verify_asymptotic_c9_cube_parametrization_exclusion.py --check
```

The standard-library verifier exhausts small endpoint rows for locator
distance and augmented full spark.  In one reported six-word endpoint fiber,
it enumerates all maps from `F_2^2` into a printed four-word subalphabet and
all maps from `F_2^3` into a printed three-word subalphabet.  It checks `(I)`,
every nonzero Walsh coefficient's kernel/support condition, the quotient image
bound, and the rank double count using integer comparisons.  It does not
enumerate all maps into the full six-word fiber.  These computations audit the
printed finite identities; they are not used as proof of the general theorem.
