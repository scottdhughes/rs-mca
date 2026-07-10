# Frobenius cyclotomic-defect bound for primitive C9

Status: `PROVED / STRICT_SUBREGIME`.

This note proves a pointwise fiber bound for cyclic multiplicative leaves whose
weights are compatible with the prime-field Frobenius action.  The result is
uniform over every Boolean mask, so arbitrary first-match pruning does not
create a separate mask-stability problem in this subregime.

It does not prove the unrestricted primitive-C9 statement.

## 1. General defect theorem

Let `p` be a prime, let `K` be a finite field of characteristic `p`, and let
`zeta in K^x` have order `N`.  In particular, `p` does not divide `N`.  Fix
`alpha,c in K^x`, an index `a in Z/NZ`, and scalars

```text
u_0,...,u_{N-1} in F_p^x.
```

Put

```text
t_i   = alpha zeta^i,
rho_i = c u_i zeta^(a i),
v_i   = rho_i (1,t_i,...,t_i^(R-1)) in K^R
```

for `0 <= i < N` and `1 <= R <= N`.  For an arbitrary family
`Omega subseteq {0,1}^N`, define

```text
Phi(x) = sum_i x_i v_i.
```

Let

```text
I = {a,a+1,...,a+R-1} subseteq Z/NZ,
Z_p(N,I) = union_{ell >= 0} p^ell I,
d_p(N,I) = N - |Z_p(N,I)|.
```

### Theorem 1 (cyclotomic-defect fiber bound)

For every `y in K^R`,

```text
|Omega intersect Phi^(-1)(y)| <= p^d_p(N,I).
```

The theorem does not require fixed weight, density, invariance, or a lower
bound on `|Omega|`.

### Proof

If the fiber is empty there is nothing to prove.  Otherwise fix
`x^(0)` in the fiber.  For a second point `x` in that fiber set

```text
e_i = u_i (x_i-x_i^(0)) in F_p
```

and form

```text
f_x(X) = sum_{i=0}^{N-1} e_i X^i in F_p[X].
```

Equality of the `j`-th syndrome coordinates, for `0 <= j < R`, gives

```text
0 = c alpha^j sum_i e_i zeta^(i(a+j)).
```

Hence `f_x(zeta^k)=0` for every `k in I`.  Since the coefficients of
`f_x` lie in `F_p`,

```text
f_x(zeta^(p k)) = f_x(zeta^k)^p.
```

Thus `f_x` vanishes at every root indexed by `Z_p(N,I)`.  The polynomial

```text
G_Z(X) = product_{k in Z_p(N,I)} (X-zeta^k)
```

belongs to `F_p[X]`: its root set is Frobenius invariant.  The roots are
distinct, and its coefficients are fixed by the `p`-power Frobenius, whose
fixed field in `K` is `F_p`.  Thus `G_Z` divides `f_x` in `F_p[X]`.  Since
`deg f_x < N`, every such polynomial has the form `G_Z h` with
`deg h < N-|Z_p(N,I)|`.  There are exactly `p^d_p(N,I)` possible polynomials
of this form.

Finally, `x -> f_x` is injective on the fiber because every `u_i` is nonzero
and `x^(0)` is fixed.  This proves the bound.

## 2. Characteristic 5 on dyadic cosets

Fix `kappa in (0,1]` and define

```text
J_kappa = ceil(log_2(4/kappa)),
D_kappa = 2^(J_kappa-1),
B_kappa = 5^D_kappa.
```

### Theorem 2 (dyadic defect bound)

If `N=2^s`, `p=5`, and `R >= kappa N`, then every cyclic interval `I` of
length `R` satisfies

```text
d_5(N,I) <= D_kappa.
```

Consequently, every fiber in Theorem 1 has size at most `B_kappa`, a constant
depending only on `kappa`.

### Proof

For `r >= 2`, multiplication by `5` generates the subgroup

```text
<5> = {u in (Z/2^r Z)^x : u = 1 mod 4}.
```

Indeed, `v_2(5^(2^j)-1)=j+2`, so the order of `5` modulo `2^r` is
`2^(r-2)`.

Write a nonzero frequency as `k=2^v u`, with `u` odd.  For `v <= s-2`, its
orbit under multiplication by `5` is exactly one of the two classes

```text
k = 2^v mod 2^(v+2),
k = 3*2^v mod 2^(v+2).
```

Every cyclic interval of length at least `2^(v+2)` meets every residue class
modulo `2^(v+2)`.  If `v <= s-J_kappa`, then

```text
2^(v+2) <= 2^(s-J_kappa+2) <= kappa 2^s <= R,
```

so the full `5`-orbit of every frequency of valuation at most
`s-J_kappa` lies in `Z_5(N,I)`.  A frequency outside `Z_5(N,I)` is therefore
zero or has valuation greater than `s-J_kappa`.  There are at most

```text
1 + sum_{v=s-J_kappa+1}^{s-1} 2^(s-v-1)
  = 2^(J_kappa-1)
```

such frequencies.  If `s<J_kappa`, the same conclusion follows from the
trivial bound `d_5(N,I) <= N <= 2^(J_kappa-1)`.

## 3. Image-normalized C9 corollary

Let `Omega^circ` be any nonempty subset of a fixed-weight Boolean slice to
which Theorem 2 applies.  Set

```text
S = Phi(Omega^circ),  L = |S|,  M = |Omega^circ|,
barN = M/L,           F_y = Omega^circ intersect Phi^(-1)(y).
```

All fibers indexed by `S` are nonempty, hence

```text
1 <= barN <= max_y |F_y| <= B_kappa.
```

For every fixed `sigma>0` and every sequence `q_N>=1`, the C9 sub-sum obeys

```text
(1/L) sum_{Delta(F_y) <= exp(-sigma N)} (|F_y|/barN)^q_N
    <= B_kappa^q_N
    = exp(O_kappa(q_N))
    = exp(o(N q_N)).
```

Thus image-normalized C9 holds pointwise on this strict subregime.  The proof
uses only `Omega^circ subseteq {0,1}^N`; any C1--C8 first-match deletion is
therefore harmless once the residual leaf has the displayed domain, map, and
weight form.

## 4. Actual multiplicative weights covered

The result includes the unweighted map (`a=0`, `u_i=1`) and every shifted
monomial window.  It also includes the dual-weighted syndrome normalization
used in `cap25_cap_v13_raw.tex`.  For `T=alpha H`, `|H|=N`,

```text
P_T(X) = X^N-alpha^N,
P_T'(t) = N t^(N-1) = N alpha^N/t,
1/P_T'(t) = t/(N alpha^N).
```

Because `5` does not divide `N`, this is a nonzero scalar times `zeta^i`, the
required form with `a=1`.

For every `s>=3`, `ord_(2^s)(5)=2^(s-2)`, so
`F_(5^(2^(s-2)))` contains a cyclic subgroup of order `2^s`.  The subregime is
therefore nonempty at arbitrarily large dyadic lengths.

## 5. Relation to existing packets

- `experimental/cap25_v13_missing_inputs_strategy.md` already identifies the
  null-prefix problem as a binary word problem in a cyclic code with consecutive
  zeros.  Theorem 1 supplies a pointwise upper bound when Frobenius expands that
  zero interval to all but `d_p(N,I)` frequencies.
- `experimental/notes/roadmaps/midlarge_h_routes.md` uses the same Frobenius
  closure mechanism at `p=-1 mod N` to rigidify minimal trades.  It does not
  give the all-fiber defect bound above.
- PR #422 and PR #447 concern prime-field image containment, Frobenius syndrome
  relations, and differential-locator rank/index laws.  They do not give this
  pointwise fiber upper bound.
- PR #444 gives general MDS pair-count bounds that become constant near
  `R/N>1/2`.  Theorem 2 reaches every fixed `R/N>=kappa>0`, but only on the
  stated characteristic-5 dyadic/Frobenius-compatible subregime.
- PR #439 isolates the image-normalized C9 interface.  Section 3 pays that
  interface for this subregime without asserting a general mask-transfer or
  Fourier-flatness theorem.

The cyclic-code dimension argument itself is standard.  The contribution here
is the exact RS-MCA specialization, defect parameter, dyadic orbit estimate,
and image-normalized C9 corollary.

## 6. Verification

Run

```sh
python3 experimental/scripts/verify_asymptotic_c9_frobenius_cyclotomic_defect.py --check
```

The verifier checks the order and orbit descriptions, exhausts every cyclic
interval for `N=2^s` through the printed cap, and independently enumerates
weighted fixed-density fibers over `F_25` at `N=8`.

## 7. Nonclaims and next wall

- No unrestricted C9 or primitive-Q theorem is proved.
- No exact C1--C8 coverage or exhaustion theorem is proved.
- No multi-leaf add-back theorem is proved.
- No target-normalized frontier compiler theorem is proved.
- No prime-field dyadic row is covered: if `N | p-1`, Frobenius acts trivially
  on the frequencies and this argument gives `d_p(N,I)=N-R`.
- No circle or twin-coset row is covered.
- No KoalaBear, Mersenne-31, QM31, or other deployed finite row is certified.

The next uncovered class is the prime-field dyadic multiplicative row with
fixed density and `0<R/N<=1/2`.  Its exact target is a subexponential
zero-error two-list bound on the post-C1--C8 residual, or an actual surviving
positive-rate fiber.
