# Coherent-phase frequency blocks in endpoint C9

Status: `PROVED PARTIAL FOURIER-BLOCK PAYMENT / LARGE-CHARACTERISTIC ROUTE CUT`.

This note isolates an analytic major-arc block that is stable under every
fixed-weight first-match mask.  Every coefficient in the block can be a
constant fraction of the mask size, but the block is so sparse that its total
Fourier contribution is superexponentially below the image-normalized mean.

The same block meets every projective frequency line over sufficiently large
split primes.  Consequently, a scalar-invariant small-value-set condition
cannot by itself classify all large Fourier coefficients.

This is one directly paid partial Fourier block and one route cut.  It is not
the manuscript's full paid Fourier/Sidon cell, a proof of the full
primitive-C9 statement, or a proof of C1--C8 exhaustion.

## 1. Endpoint notation

Let `N | p-1`, where `p` is prime, and let

```text
T = alpha H = {t_0,...,t_(N-1)} subset F_p^x
```

with `H` cyclic of order `N`.  Fix `1 <= R < N` and use the endpoint `a=1`.
In the live primitive-leaf notation the columns are

```text
v_i = rho_i (1,t_i,...,t_i^(R-1)).
```

For the exact RS dual weight on `T`,

```text
P_T(X) = X^N-alpha^N,
rho_i = 1/P_T'(t_i) = t_i/(N alpha^N).
```

Thus, for a dual coordinate `d=(d_0,...,d_(R-1))`,

```text
d dot v_i
  = sum_(j=0)^(R-1) d_j t_i^(j+1)/(N alpha^N)
  = f_c(t_i),
c_k = d_(k-1)/(N alpha^N),       1 <= k <= R.
```

The map `d -> c` is invertible.  Hence the exact endpoint residual Fourier
coefficient is represented by the phase

```text
f_c(X) = sum_(k=1)^R c_k X^k,       c in F_p^R.
```

The theorem below is for this exact-dual endpoint specialization.  It does not
cover an arbitrary primitive leaf with unrelated nonzero weights `rho_i`.

Let `1 <= m <= N` and let `Omega` be any nonempty subset of the weight-`m`
Boolean slice.  Write

```text
Phi(x) = (sum_i x_i t_i^k)_(1 <= k <= R),
M = |Omega|,
E_Omega(c) = sum_(x in Omega) e_p(c dot Phi(x))
           = sum_(x in Omega) e_p(sum_i x_i f_c(t_i)),
e_p(z) = exp(2 pi i z/p).
```

No invariance or raw/full-slice assumption is imposed on `Omega`.

For `z in F_p`, let `||z||_p` denote the absolute value of its centered
integer representative.  For an integer `q >= 2`, define

```text
CP_q(t_0) = {
  c in F_p^R : ||f_c(t_i)-f_c(t_0)||_p <= floor(p/q) for every i
},
h_q = 2 floor(p/q)+1.
```

## 2. Exact coherent-phase theorem

### Theorem 1 (count, coefficient size, and partial contribution)

With the notation above:

```text
|CP_q(t_0)| <= h_q^R.                                      (2.1)
```

For `q=12m`, every `c in CP_q(t_0)` satisfies

```text
|E_Omega(c)| >= cos(pi/6) M.                               (2.2)
```

Nevertheless, for every `y in F_p^R`,

```text
|p^(-R) sum_(c in CP_(12m)(t_0) \ {0})
          E_Omega(c) e_p(-c dot y)|
    <= M (h_(12m)/p)^R.                                    (2.3)
```

#### Proof

Choose `R` points `t_1,...,t_R` distinct from `t_0`.  The linear map

```text
c -> (f_c(t_j)-f_c(t_0))_(1 <= j <= R)
```

is bijective.  Indeed, an element of its kernel makes the degree-at-most-`R`
polynomial `f_c(X)-f_c(t_0)` vanish at `R+1` distinct points.  It is therefore
zero, and `f_c(0)=0` then gives `c=0`.  Each selected difference has at most
`h_q` allowed values, proving (2.1).

Now take `q=12m`.  For `c in CP_q(t_0)`, choose centered integers `delta_i`
representing `f_c(t_i)-f_c(t_0)`.  If `x` has weight `m`, then

```text
|sum_i x_i delta_i| <= m p/(12m) = p/12.
```

After the common rotation by `e_p(-m f_c(t_0))`, every summand defining
`E_Omega(c)` has argument in `[-pi/6,pi/6]`.  Its real part is at least
`cos(pi/6)`, and summing proves (2.2) for every mask `Omega`.

Finally, use `|E_Omega(c)| <= M`, the triangle inequality, and (2.1):

```text
|p^(-R) sum_(c in CP_(12m) \ {0}) E_Omega(c)e_p(-c dot y)|
  <= M |CP_(12m)|/p^R
  <= M (h_(12m)/p)^R.
```

This proves (2.3).

### Corollary 2 (image-normalized partial-block payment)

Let `L=|Phi(Omega)|`, so the mean nonempty fiber size is `barN=M/L`.
Fix `alpha_0,kappa>0`.  If

```text
m >= alpha_0 N,       R >= kappa N,
```

then, for all sufficiently large `N`, the contribution in (2.3), relative to
`barN`, is at most

```text
L (h_(12m)/p)^R
  <= 2^N ((1+1/(6 alpha_0))/N)^(kappa N)
  = exp(-kappa N log N + O_(alpha_0,kappa)(N)).             (2.4)
```

#### Proof

Because `N | p-1`, one has `p >= N+1`.  Also

```text
h_(12m)/p <= 2/(12m)+1/p
             <= (1+1/(6 alpha_0))/N.
```

Use `L <= M <= 2^N`, `R >= kappa N`, and take `N` large enough that the
displayed base is below one.

Thus `CP_(12m)(t_0)` is a mask-stable, directly paid partial Fourier block even
though each of its individual coefficients is a constant-fraction major arc.
This does not pay the full Fourier/Sidon cell of the profile-envelope paper.

## 3. Projective ubiquity

### Theorem 3 (simultaneous scalar dilation)

If `p > q^(N-1)`, every nonzero projective line in `F_p^R` contains a
representative in `CP_q(t_0)`.

#### Proof

Fix `u != 0` and put

```text
d_i = f_u(t_i)-f_u(t_0),       1 <= i < N.
```

Place the `q^(N-1)+1` points

```text
({j d_1/p},...,{j d_(N-1)/p}),       0 <= j <= q^(N-1),
```

in the `q^(N-1)` boxes of side length `1/q` in `[0,1)^(N-1)`.  Two points
lie in the same box.  Their positive index difference `lambda` satisfies

```text
1 <= lambda <= q^(N-1) < p,
||lambda d_i||_p < p/q
```

for every `i`.  Hence `lambda u` is a nonzero member of `CP_q(t_0)`.

This theorem does not classify a frequency.  It says that scalar dilation
alone can make every projective frequency direction coherent-phase when the
split prime is unrestricted.

## 4. Scalar-invariant value-set route cut

Take the projective line generated by `f_u(X)=X`.  Every nonzero scalar
multiple is injective on `H`, so its value set has the maximum possible size
`N`.  If

```text
p > (12m)^(N-1),
```

Theorem 3 puts a nonzero representative `c` of this line in
`CP_(12m)(t_0)`, and Theorem 1 gives

```text
|E_Omega(c)| >= cos(pi/6) M.
```

Thus a theorem asserting that a large coefficient alone forces a small value
set is false over the unrestricted large-split-prime class.  More generally,
projective ubiquity defeats any proposed frequency-side inverse conclusion
that is invariant under nonzero scalar multiplication and fails on at least
one projective line.  This is not an exact witness-side C1--C8 exclusion.

## 5. Relation to the current frontier

- The image normalization `barN=M/L` is imported from the existing C9 audit.
- The signed masked coefficient `E_Omega(c)` is the residual coefficient, not
  the full-slice elementary symmetric polynomial unless `Omega` is the whole
  slice.
- The coherent-phase count and partial-block payment show that the current
  major-arc verification sentence in `experimental/asymptotic_rs_mca.tex` is
  too strong: directly paid sparse major-arc blocks may be removed before the
  remaining large coefficients are routed to algebraic cells.
- Projective ubiquity cuts only a value-set-only or other scalar-invariant
  frequency inverse.  It does not contradict the measured correlation packet
  on small value sets.
- The next target is a phase-separated inverse theorem: after deleting
  `CP_(12m)(t_0)`, route every remaining theorem-scale masked coefficient to a
  literal paid C1--C8 predicate or to additional blocks whose total dual
  density is at most `exp(o(N))/L`.

## 6. Verification

Run

```sh
python3 experimental/scripts/verify_asymptotic_c9_coherent_phase_block.py --check
```

The verifier exhausts every weight and every nonempty mask on a small split
row, checks the evaluation-difference bijection and coherent-phase
inequalities, and checks projective ubiquity on every projective line of a
second row where the coherent-phase set is a proper nontrivial subset.  The
sector and counting checks are integer-exact; the displayed finite DFT checks
are numerical smoke tests with absolute tolerance `1e-10`.

## 7. Nonclaims

- No unrestricted primitive-C9 or C9-LD theorem is proved.
- No full Fourier/Sidon cell is paid.
- No exact C1--C8 coverage, exhaustion, or residual-emission theorem is
  proved.
- No witness-side C1--C8 counterexample is constructed.
- No claim is made that every remaining large coefficient has quotient,
  dihedral, ramification, or any other algebraic structure.
- No raw-to-mask transfer is claimed outside the coherent-phase block.
- No arbitrary-weight primitive leaf is covered; the exact-dual endpoint
  relation for `rho_i` is used.
- No small-split-prime theorem is proved.
- No KoalaBear, Mersenne-31, QM31, or other deployed finite row is moved.
- No adjacent certificate `U(a0+1) <= B* < L(a0)` is supplied.
