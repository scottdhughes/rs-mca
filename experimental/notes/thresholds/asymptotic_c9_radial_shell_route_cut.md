# Asymptotic C9 Radial-Shell Route Cut

Date: 2026-07-10

Status: `PROVED / ROUTE CUT` for the explicitly printed pairwise package below.
This is not a cut of radial information in general.

## Scope and provenance

This note repairs Role 06 of
`RS_MCA_C9_LINEAR_DEFICIT_9SOL_20260710_returns_raw`.  The repository authority
for the repair is `2acc7be`; PR `#483` is unrelated and is not a source for this
packet.  The Krawtchouk and MacWilliams conventions are consistent with the
existing
[`cap25_v13_entropy_inverse_fp_span_connectivity.md`](cap25_v13_entropy_inverse_fp_span_connectivity.md)
and
[`l1_prefix_dual_centered_krawtchouk_route_cut.md`](../l1/l1_prefix_dual_centered_krawtchouk_route_cut.md)
notes.

The conclusion concerns only the following displayed package:

1. the floors `(RM_j)` below;
2. ambient `p`-ary Delsarte positivity;
3. the allowed-weight support of the MDS code `C_D`; and
4. the shell caps `A_t(G) <= A_t(C_D)`.

No phrase such as "the radial constraints" in this note means anything beyond
these four items.

## Endpoint code and conventions

Let `p` be prime, let `N | p-1`, and choose `zeta in F_p^*` of order `N`.  At an
endpoint, the syndrome frequencies are `a,a+1,...,a+R-1`, while equal weight
adds frequency `0`.  After removing a repeated zero, the frequency set is a
cyclic interval `I_D` of size

```text
D=R     for a in {0,1-R},
D=R+1   for a in {1,-R}.
```

Define

```text
C_D = {z in F_p^N : sum_{i=0}^{N-1} z_i zeta^(ki)=0 for k in I_D}.
```

Multiplying columns by nonzero scalars moves `I_D` to `0,...,D-1`.  Every
`D x D` minor of the resulting parity-check matrix is a nonzero Vandermonde
determinant.  Hence

```text
C_D       is [N,N-D,D+1]_p,
C_D^perp  is [N,D,N-D+1]_p.
```

For a finite family `F subset F_p^N`, with `J=|F|`, define its normalized inner
distribution by

```text
A_t(F) = J^(-1) #{(x,x') in F^2 : d_H(x,x')=t}.
```

Thus `A_0(F)=1` and `sum_t A_t(F)=J`.  In contrast, throughout this note

```text
A_t(C_D) = #{c in C_D : wt(c)=t}
```

is the ordinary linear-code weight enumerator.  The same convention defines
`A_j(C_D^perp)`.

The `p`-ary Krawtchouk polynomial is

```text
K_j^(p)(t) = sum_{ell=0}^j (-1)^ell (p-1)^(j-ell)
              binom(t,ell) binom(N-t,j-ell),
```

with out-of-range binomial coefficients equal to zero.

## The exact coset floor

If `F subset b+C_D`, character orthogonality gives

```text
sum_t A_t(F) K_j^(p)(t)
  = J^(-1) sum_{u in F_p^N, wt(u)=j}
      |sum_{x in F} exp(2 pi i (u dot x)/p)|^2.
```

For `u in C_D^perp`, the character is constant on `b+C_D`, so its squared
coefficient is `J^2`.  Keeping those nonnegative terms proves the exact floor

```text
(RM_j)  sum_t A_t(F) K_j^(p)(t)
          >= |F| A_j(C_D^perp),              0 <= j <= N.
```

For `1 <= j <= N-D`, the dual enumerator vanishes and `(RM_j)` is just ambient
`p`-ary Delsarte positivity.  At `j=0`, it is the equality `sum_t A_t(F)=J`.
Also, for each fixed `x in F`, the differences `x'-x` are distinct words of
`C_D`.  Therefore an actual coset subset obeys `A_t(F)<=A_t(C_D)` and has no
pair distance outside the linear code's weight support.

## Repaired route-cut theorem

Fix `kappa>0`.  Uniformly over primes and integers satisfying

```text
N | p-1,                 kappa N <= D <= N/2,
```

there is `N_0(kappa)` such that, for `N >= N_0(kappa)`, every binary
constant-weight code `G subset {0,1}^N` with minimum Hamming distance at least
`2D` satisfies the following explicitly delimited package:

```text
A_t(G) >= 0,  A_0(G)=1,  sum_t A_t(G)=|G|;
sum_t A_t(G) K_j^(p)(t) >= 0                         for 0 <= j <= N;
sum_t A_t(G) K_j^(p)(t) >= |G| A_j(C_D^perp)         for 0 <= j <= N;  (RM_j)
A_t(G)=0 whenever A_t(C_D)=0;
A_t(G) <= A_t(C_D)                                   for 0 <= t <= N.
```

The distance assumption gives the stronger support statement
`A_t(G)=0` for `1 <= t < 2D`.  Since an MDS code `C_D` has no nonzero word below
weight `D+1` and has a word on every support of each size `t>=D+1`, this implies
the printed MDS allowed-shell condition.

Now fix `alpha_0,kappa,eta>0` and an admissible endpoint sequence with

```text
alpha_0 N <= m <= (1-alpha_0)N,
kappa N <= D <= Q-eta N,
Q=m(N-m)/N.
```

If such a sequence exists, deterministic lexicographic greedy Johnson
packings of weight `m` and minimum Johnson distance at least `D` have size
`exp(cN)` for a constant `c=c(alpha_0,kappa,eta)>0`.  Their genuine Johnson
intersection data satisfy arbitrary valid Johnson constraints, and their pair
distributions satisfy precisely the displayed cyclic package.  Therefore a
hierarchy whose Johnson side is arbitrary but whose cyclic input consists only
of this package and nonnegative combinations of its inequalities cannot prove
an `exp(o(N))` upper bound in this regime.

## Proof of asymptotic redundancy

Only the high dual shells require work.  Write

```text
j=N-D+r,                 1 <= r <= D.
```

For `t>=2D`, a nonzero term in `K_j^(p)(t)` has
`ell >= t-D+r >= D+r`.  Vandermonde convolution therefore gives

```text
|K_j^(p)(t)| <= binom(N,j)(p-1)^(j-D-r),
K_j^(p)(0)    = binom(N,j)(p-1)^j.
```

Using `|G|<=2^N`, the distance support, and `sum_{t>0}A_t(G)=|G|-1`,

```text
sum_t A_t(G)K_j^(p)(t)
 >= binom(N,j)(p-1)^j
      [1-(|G|-1)/(p-1)^(D+r)].                         (1)
```

For a fixed support of size `j`, shortening the `D`-dimensional MDS dual on
the complementary `N-j` coordinates leaves dimension `r`.  Hence

```text
A_j(C_D^perp) <= binom(N,j)p^r.                        (2)
```

The error ratio in `(1)` is at most `2^N/N^(kappa N+1)=o(1)`.  The ratio of
`|G|` times `(2)` to the diagonal term is at most

```text
2^N (p/(p-1))^r / (p-1)^(N-D)
 <= 2^N exp(1/2) / N^(N/2) = o(1).
```

Thus `(RM_j)` holds for every high shell once `N` is sufficiently large.  A
finite sufficient pair, recorded for replay but not asserted to be necessary,
is

```text
2^(N+1) <= (p-1)^(D+1),
2^(N+1) (p/(p-1))^D <= (p-1)^(N-D).                    (3)
```

For the caps, fix a support `S` of size `t>=2D`.  The subcode of `C_D`
supported on `S` has dimension `t-D`.  The union of its `t` coordinate
hyperplanes contains at most `t p^(t-D-1)` words.  Since `p>N>=t`, at least

```text
(p-t)p^(t-D-1) >= p^(D-1)
```

codewords have support exactly `S`.  Consequently

```text
A_t(C_D) >= binom(N,t)(p-t)p^(t-D-1) >= p^(D-1).
```

This exceeds `A_t(G)<=|G|-1<=2^N` for sufficiently large `N`; the finite
condition `p^(D-1)>2^N` is a convenient sufficient check.

Finally, with `theta=m/N` and binary entropy `h`, put

```text
f_theta(delta)
 = theta h(delta/theta)
   +(1-theta)h(delta/(1-theta)).
```

The Johnson ball of radius `D-1` has size

```text
sum_{s=0}^{D-1} binom(m,s)binom(N-m,s).
```

On the compact admissible density set,
`f_theta(theta(1-theta)-eta)<h(theta)` uniformly.  The usual binomial entropy
bounds and lexicographic greedy deletion therefore give

```text
|G_N| >= exp(c_* N)/(N+1)^2 >= exp((c_*/2)N)
```

for sufficiently large `N`, where the compactness gap `c_*>0` depends only on
`alpha_0,kappa,eta`.

## What is not cut

The positive-rate `G_N` is not claimed to lie in a syndrome coset.  It is a
feasible object only for arbitrary valid Johnson constraints augmented by the
printed package.  This note does not cut or identify with that package:

- the full Fourier projection or dual-translation identities;
- distance-graph spectra or other nonradial information;
- complete-weight-enumerator constraints;
- triple or common-syndrome constraints;
- Terwilliger constraints, semidefinite programs, or higher-moment constraints.

There is no actual syndrome-coset counterexample here, no C1--C8 survival or
coverage statement, no proof of C9-LD, and no deployed finite-row conclusion.

## Verifier and finite fixtures

Run:

```bash
python3 experimental/scripts/verify_asymptotic_c9_radial_shell_route_cut.py
python3 -O experimental/scripts/verify_asymptotic_c9_radial_shell_route_cut.py
```

The stdlib-only verifier uses explicit exceptions for every gate, so the check
set is unchanged under `-O`.  It exactly enumerates small endpoint MDS codes,
checks the Krawtchouk character normalization, checks coset floors, and checks
three deterministic greedy constant-weight fixtures against the printed
package.  Those small fixtures are normalization tests, not evidence for the
asymptotic quantifier.  A separate `(N,p,D)=(8,257,2)` fixture checks the finite
sufficient inequalities `(3)` and the shell-cap bound; it is an inequality
fixture, not a finite C9 result or an admissible positive-rate sequence.
