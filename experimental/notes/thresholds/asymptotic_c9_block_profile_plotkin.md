# Block-composition Plotkin packet for the endpoint C9 strip

## Status and scope

**PROVED (field-free coding theorem) / CONDITIONAL (endpoint application) /
AUDIT.**  This is a standalone extension of the endpoint locator and
one-block shortening packet integrated from PR #463.  It is not an amendment
to PR #463 or to the current profile-envelope audit in PR #483.  The coding
argument uses no field, Fourier transform, RS structure, or profile compiler.

The exact input is a binary constant-composition code on a predeclared
partition.  The endpoint corollary starts only after an external argument has
placed a same-syndrome family in one of those fixed profiles and supplied the
Johnson-distance lower bound.  That distinction is load-bearing.

## 1. Field-free block-profile theorem

Let

```text
[N] = B_1 disjoint-union ... disjoint-union B_J,   |B_j| = n_j,
```

and let `C` be a family of binary words such that every word has local weight
`m_j` on `B_j`.  Suppose every two distinct words have Johnson distance at
least the integer `D`, where `1 <= D <= N`.  Put

```text
q_j = min(m_j, n_j-m_j),
Q_P = sum_j m_j(n_j-m_j)/n_j
    = sum_j q_j(n_j-q_j)/n_j.
```

Complementing every coordinate in a block with `m_j > n_j/2` preserves
Hamming and Johnson distances and changes its common local weight to `q_j`.
All statements below may therefore be proved with `q_j <= n_j/2`.

### Theorem 1 (one-block shortening)

Fix a block `h` with `q_h>0` and an integer `0 <= u <= n_h-q_h`.  Define

```text
Q_{P,h}(u) = Q_P - q_h^2 u/[n_h(n_h-u)].
```

If `D > Q_{P,h}(u)`, then

```text
|C| <= [binom(n_h,q_h)/binom(n_h-u,q_h)]
       * D/[D-Q_{P,h}(u)].                              (BP)
```

The exact retention guarantee and threshold drop are

```text
|C_u| >= [binom(n_h-u,q_h)/binom(n_h,q_h)] |C|,
Q_P-Q_{P,h}(u) = q_h^2 u/[n_h(n_h-u)].                 (1)
```

Shortenings in several blocks may be iterated; retention factors multiply
and threshold drops add.

**Proof.**  At block length `n_h-r`, a family of size `A_r` has
`(n_h-r-q_h)A_r` zero incidences in that block.  Restricting to the most
frequent zero coordinate and deleting it retains at least the fraction
`(n_h-r-q_h)/(n_h-r)`.  Multiplication through `u` steps gives (1).

For the retained family of size `A`, let `a_i` count words containing
coordinate `i`.  Summing Johnson distances over unordered pairs and applying
Cauchy--Schwarz separately in each current block gives

```text
D binom(A,2)
 <= (1/2) sum_i a_i(A-a_i)
 <= (A^2/2) Q_{P,h}(u).
```

Thus `A <= D/[D-Q_{P,h}(u)]`; combine this with the retained fraction.  Direct
subtraction gives the threshold-drop identity in (1).  This proves (BP).

### Theorem 2 (equality line)

If `D=Q_P>0`, then

```text
|C| <= 2 r_P,   r_P = sum_{j:q_j>0}(n_j-1).             (EQ)
```

**Proof.**  Center every incidence vector blockwise by subtracting the vector
that is constantly `q_j/n_j` on block `j`.  The centered vectors have squared
norm `Q_P`, pairwise inner product `Q_P-d_J(x,x') <= 0`, and lie in a space of
dimension `r_P`.  After normalization, their Gram matrix `G` is positive
semidefinite, has diagonal `1`, and has off-diagonal entries in `[-1,0]`.
Since `1^T G 1 >= 0` and `t^2 <= -t` on `[-1,0]`,
`tr(G^2) <= 2|C|`.  Cauchy--Schwarz on the nonzero eigenvalues gives
`|C|^2 <= r_P tr(G^2) <= 2r_P|C|`, proving (EQ).

### Theorem 3 (adaptive profile payment)

No restriction on `J` is imposed for this fixed-profile estimate.  Fix
`kappa>0`, assume `D >= kappa N`, and define

```text
Delta = (Q_P-D)_+,
delta_k = min(kappa^2/4, 1/6),
nu = ceil((Delta+1)/delta_k).
```

If `D-Q_P >= 1`, then `|C| <= N`.  Otherwise, if

```text
nu <= floor(kappa N/2),
```

then

```text
|C| <= N 2^nu.                                          (AP)
```

Consequently, uniformly over any family of fixed profiles,

```text
D >= kappa N and (Q_P-D)_+ = o(N)  imply  |C|=exp(o(N)). (PROFILE-Q)
```

**Proof.**  The first claim is the unshortened Plotkin calculation.  In the
remaining case, `Q_P>D-1>=kappa N-1` and `Q_P <= sum_j q_j`.  Call a block
high-density when `q_j/n_j >= kappa/2`.  Low-density blocks contribute less
than `kappa N/2` to `sum_j q_j`; hence high-density blocks have total
`q`-mass greater than `kappa N/2-1`.  Each such block supplies `n_j-1 >= q_j`
balanced shortenings, so together they supply at least
`floor(kappa N/2)` operations.

For a current balanced block `(n,q)`, retain a zero coordinate, shorten, and
complement the remaining block if its new weight is above half.  With
`q'=min(q,n-1-q)`, the operation retains at least half the family and drops
the threshold by exactly

```text
q(n-q)/n - q'(n-1-q')/(n-1) = q^2/[n(n-1)].             (2)
```

Before the first dynamic complement, the density is at least `kappa/2`, so
the drop is at least `kappa^2/4`.  Thereafter the pre-operation states
alternate between `(2q+1,q)` and `(2q,q)`; their drops are respectively at
least `1/6` and `1/4`.  Thus every selected operation drops `Q_P` by at least
`delta_k` and costs at most a factor two.  After `nu` operations the retained
threshold is at most `D-1`, so the unshortened Plotkin count is at most
`D<=N`.  Restoring the retention loss proves (AP).  If `Delta=o(N)`, then
`nu=o(N)` and the operation-supply condition holds eventually, proving
PROFILE-Q.

### Corollary 4 (PROFILE-LD converse)

For fixed `c,kappa>0`, put

```text
epsilon(c,kappa)
  = [delta_k/8] min(kappa, c/log(2)) > 0.
```

For all sufficiently large `N`, if `D>=kappa N` and `|C|>=exp(cN)`, then

```text
Q_P-D >= epsilon(c,kappa) N.                            (PROFILE-LD)
```

Indeed, a smaller deficit makes `nu <= kappa N/2` and makes the logarithm of
the bound (AP) strictly smaller than `cN` for large `N`.  PROFILE-LD is only
an emitted residual condition.  This packet does not pay that condition.

## 2. Endpoint corollary

PR #463 supplies the following external input for the four prime-field
dyadic endpoint windows: two distinct supports in one endpoint syndrome fiber
have Johnson distance at least

```text
D=R       for a in {0,1-R},
D=R+1     for a in {1,-R}.
```

Therefore (BP), (EQ), and (AP) apply to the intersection of such a fiber with
any fixed local-weight profile, including after first-match pruning.  This is
the only RS-specific import.

Write `m=sum_j m_j`, `theta=m/N`, and `theta_j=m_j/n_j`.  Then the exact
variance identity is

```text
Q-Q_P = sum_j n_j(theta_j-theta)^2,
Q = m(N-m)/N.                                            (PV)
```

Hence a predeclared profile is paid pointwise whenever `D>=kappa N` and

```text
((Q-D) - sum_j n_j(theta_j-theta)^2)_+ = o(N)            (3)
```

uniformly.  A union conclusion requires the **total predeclared family of
partition/profile labels** to have size `exp(o(N))`, with all error terms in
(3) and PROFILE-Q uniform over that family.  For one partition with `J`
blocks, `(N+1)^J` bounds the number of local-count profiles, so
`J log N=o(N)` is a sufficient but not necessary profile-count condition.
It does not construct the partition family or prove that a source cell lands
in it.

For a nonempty fixed cell, let `M` be its size and let `L` be the size of its
**actual** syndrome image.  Then `M/L>=1`; the pointwise bound
`max_y |F_y|=exp(o(N))` therefore implies

```text
max_y |F_y| <= exp(o(N)) M/L.
```

This actual-image observation is not a comparison with the paper's declared
natural-profile budget.  In particular it does not prove the closed-ledger
residual-to-full comparison `M_lambda/L_lambda <= exp(o(N)) barN_lambda`.

## 3. Forced-coordinate specialization

Suppose all words share `b_1` forced ones and a disjoint set of `b_0` forced
zeros, with `N-b_0-b_1>0`.  Deleting them leaves the one-block profile
threshold

```text
Q_{b_0,b_1}
  = (m-b_1)(N-m-b_0)/(N-b_0-b_1),

Q-Q_{b_0,b_1}
  = [b_0 m(m-b_1) + b_1(N-m)(N-m-b_0)]
    /[N(N-b_0-b_1)].                                    (FB)
```

Thus `(Q_{b_0,b_1}-D)_+=o(N)` is a direct specialization of PROFILE-Q.
Forced-one and forced-zero cases are not a second theorem or a novelty claim;
they are the block-profile theorem after deleting constant coordinates.
If `b_0+b_1=N`, the family contains at most the single forced word and needs no
threshold formula.

## 4. Current-paper audit and nonclaims

The source response's diagnosis of `experimental/asymptotic_rs_mca.tex:116`
belongs to a superseded draft and is discarded.  At authority `2acc7be`, the
current paper states explicitly that the C3 upper payment remains part of the
closed-ledger hypothesis.  This packet neither repairs nor challenges that
conditional statement.

This packet makes none of the following claims:

- no source-to-profile extraction or proof that C3 witnesses have (3);
- no predeclared-atlas coverage or exhaustion theorem;
- no natural-profile budget or residual-to-full comparison;
- no direct ray compiler (`RC`);
- no Sidon payment or major-arc routing theorem;
- no primitive add-back theorem;
- no payment of fixed-linear PROFILE-LD cells;
- no full C9-LD theorem;
- no finite KoalaBear, Mersenne, QM31, or adjacent-row conclusion;
- no external novelty for the classical shortening, Plotkin, or Gram method.

## 5. Replay

Run from the repository root:

```sh
python3 experimental/scripts/verify_asymptotic_c9_block_profile_plotkin.py --check
python3 -O experimental/scripts/verify_asymptotic_c9_block_profile_plotkin.py --check
python3 -m py_compile experimental/scripts/verify_asymptotic_c9_block_profile_plotkin.py
```

The verifier is stdlib-only and uses explicit exceptions rather than
optimization-sensitive `assert` statements.  It checks exact one-block drops
and retention, finite equality-line Gram fixtures, adaptive trajectories with
dynamic complementation, the variance and forced-coordinate identities, and
small split-prime endpoint profile fixtures.  A nonvacuous two-word
constant-composition fixture at `N=512`, `m=q=256`, and `D=128` reaches the
exact adaptive gate `nu=floor(kappa N/2)=64` and checks
the accumulated drop, retention, final Plotkin gap, and code bound.  The
output separately reports each endpoint bound branch; in particular, the
small endpoint scan honestly reports zero adaptive-bound hits.  These finite
checks are sanity certificates for the displayed algebra, not substitutes
for the proof or for any of the compiler obligations listed above.
