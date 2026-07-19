# Affine-prefix direct-partition phase route cut

## Status

This note records the independently audited finite layer of the R31 Role 14
return. It is a line-local theorem over the characteristic-five family below.
It is not a semantic first-match theorem and carries zero finite-ledger,
asymptotic-ledger, recurrence, Grand MCA, Grand List, or official-score charge.

The source contract is `origin/main` at
`3404d21b64c876c6d9b995ad3e29d7120ab27a54`. The exact predecessor is the
affine-prefix line compiler in PR #903. This note adds the support-wise
nontriviality line required by the current MCA definition, the exact phase
function, the inclusive finite `447/500` band, and direct-partition route cuts.

## Finite source family

For every integer `B >= 2`, let

```text
F_B = F_(5^(3B)),  n = 4B,  k = 2B-1,  m = 2B = k+1.
```

Choose an `F_5`-basis

```text
a_1,u_1,v_1,...,a_B,u_B,v_B
```

of `F_B` and set

```text
D_B = {a_i + eps*u_i + eta*v_i :
       1 <= i <= B and eps,eta in {0,1}}.
```

Let `C_B = RS_(F_B)(D_B,k)` and consider the received affine line

```text
R_gamma(X) = X^(2B) + gamma*X^(2B-1),  gamma in F_B.
```

For a `2B`-support `S` in `D_B`, write

```text
Q_S(X) = product_(x in S) (X-x)
       = X^(2B) + c_1(S) X^(2B-1) + ... .
```

If `gamma=c_1(S)`, then `h=R_gamma-Q_S` has degree less than `k`, and
the complete agreement set of `h` with `R_gamma` is exactly `S`.
Conversely, every exact-`2B` explanation has this form.

The support-wise nontriviality required by the source is explicit. The
direction word is `r_1=X^k|D_B`. If it were explained on a `2B=k+1` support
by some `g` of degree less than `k`, then the nonzero polynomial `X^k-g`
would have `k+1` distinct roots despite having degree `k`. This is impossible.
Thus every displayed witness satisfies `NT_C((r_0,r_1);S)` on the same
support `S`, not merely globally.

## Exact slope partition

One block has local signature polynomial

```text
Q(y) = 1 + 4y + 4y^2 + 4y^3 + y^4.
```

The only collision among the six size-two subsets is the pair of diagonals.
With

```text
P(y) = Q(y) + y^2 = 1 + 4y + 5y^2 + 4y^3 + y^4,
c_M = [y^(2M)] Q(y)^M,
L_(B,j) = binom(B,j) c_(B-j),
L_B = [y^(2B)] P(y)^B,
```

the exact witness incidence has a pairwise slope-disjoint partition

```text
C_B = disjoint_union_(j=0)^B C_(B,j),
|Z_(B,j)| = L_(B,j),
|C_(B,j)| = 2^j L_(B,j),
nu(gamma,h) = 1,
mu(gamma) = 2^j.
```

Consequently

```text
|Z_B| = L_B,
sum_j L_(B,j) = L_B,
sum_j 2^j L_(B,j) = binom(4B,2B),
B_C_B^MCA(2B) >= L_B.
```

The last line uses the support-wise argument above. No semantic C1--C9
primitive or survival assertion is involved.

## Representation moments and covering weights

For one ambiguous block, the ordered-difference multiplicities are `(1,2,1)`.
Tensoring `j` blocks gives

```text
|supp r_gamma| = 3^j,
max r_gamma = 2^j,
sum_w r_gamma(w)^tau = (2 + 2^tau)^j,
E_gamma = sum_w r_gamma(w)^2 = 6^j,
Delta_gamma = E_gamma/(2^j)^3 = (3/4)^j.
```

The ordinary image-normalized moment is one for every positive order. The
literal representation-weighted occupied-emission identity used here is
proved only at even orders `q=2h`: the weighted sum is `(sum_w r(w))^h`,
hence `(2^(2j))^h=(2^j)^q`.

For the nonnegative per-slope source-witness covering program, each slope in
the `j`-cell has `2^j` witnesses and the constraint is that its witness
weights sum to at least one. Summing the constraints proves total mass at
least `L_(B,j)`. Constant witness weight `2^(-j)` attains equality. This is
optimal only for this specified covering program; it says nothing about
signed cancellation, Fourier weights, additional incidence, or semantic
profile scales.

## Phase and finite band

For `0 <= theta <= 1`, with natural logarithms, define

```text
H(theta) = -theta log(theta) - (1-theta) log(1-theta),
lambda(theta) = H(theta) + (1-theta) log(14),
kappa(theta) = lambda(theta) - theta log(2).
```

If `j_B/B -> theta`, then

```text
(1/B) log L_(B,j_B) -> lambda(theta),
(1/n) log(L_(B,j_B)/(1+2^j_B)) -> kappa(theta)/4.
```

The derivative is

```text
kappa'(theta) = log((1-theta)/(28 theta)),
kappa''(theta) = -1/(theta(1-theta)).
```

Thus the unique maximum is at `theta=1/29`, where
`kappa=log(29/2)`. The unique later zero is

```text
theta_* = 0.8936588244321410561293819927796147008... .
```

At the inclusive rational endpoint, the exact integer inequality

```text
447^447 * 53^53 * 2^447 > 500^500 * 14^53
```

gives

```text
eta_447 = -kappa(447/500)
        = 0.0018637304802374014167631268... > 0.
```

Since `kappa` is decreasing on this interval, for every `B >= 2`,

```text
500j >= 447B  =>  L_(B,j) <= 2^j exp(-eta_447 B).
```

This is a line-local finite route cut, not a paid semantic-cell inequality.

## Direct-partition route cuts

An honest direct atlas here means a slope partition whose declared mean is
the full direct source-fibre mean

```text
Nbar_i = M_i/L_i,
```

without borrowed witnesses, semantic scales, or independently optimized line
data. The complete canonical `B+1`-cell atlas has envelope size

```text
sum_(j=0)^B (1+2^j) = B + 2^(B+1),
```

whose exponential rate is `log 2`, while `L_B` has rate `log 15`.

More generally, let an honest direct partition have `r` cells, slope counts
`L_i`, witness counts `M_i`, and a subexponential loss `K_B`.
Because `Nbar_i <= 2^B`, a total-envelope payment would force

```text
r >= L_B / (K_B (1+2^B)).
```

Its cell-count rate per code coordinate is at least

```text
c_direct = (1/4) log(15/2).
```

If every cell separately satisfies `L_i <= K_B(1+M_i/L_i)`, then
`L_i^2 <= K_B(L_i+M_i)`. Cauchy--Schwarz and
`sum_i M_i=binom(4B,2B)` give

```text
r >= L_B^2 / (K_B (L_B + binom(4B,2B))).
```

The resulting per-coordinate rate is at least

```text
c_typed = (1/4) log(225/16).
```

The largest cell phase itself has rate

```text
c_cell = (1/4) log(29/2).
```

These are route cuts against subexponential-cardinality partitions using only
the full direct source-fibre natural means. They are not impossibility results
for all MI+MA, Fourier, geometric-incidence, or semantic-owner arguments.

## Conditional semantic retention

If an actual slope-first-match raw cell, or a separately paid subcell, is
contained in one `j`-stratum and has actual residual mean at most `2^j`, then
payment forces retained fraction

```text
|R_(B,j)|/L_(B,j) <= exp(-kappa(theta)n/4 + o(n)).
```

Nothing here permits applying that estimate to a larger semantic cell spanning
several `j`-strata with a different actual residual mean.

## Replay

Run

```bash
python3 experimental/scripts/verify_affine_prefix_direct_partition_phase.py
python3 -O experimental/scripts/verify_affine_prefix_direct_partition_phase.py
```

Both outputs must match the checked-in expected transcript. The verifier pins
the current source and PR #903 compiler, reconstructs the local census and
first coefficient rows, checks all exact generating-function and moment
identities, certifies the reciprocal covering optimum, isolates the phase root,
checks the exact `447/500` endpoint and all eligible cells through `B=300`,
checks the direct-partition algebra, and rejects 10 semantic mutations.

## Nonclaims and remaining wall

This note does not prove:

- an actual primitive C1--C9 first-match cell;
- survival after earlier semantic owners;
- a complete semantic classifier or raw-witness atlas;
- a row-uniform theorem over arbitrary received lines;
- a theorem outside the stated characteristic-five family;
- a theorem against every direct, signed, Fourier, or semantic weighting;
- a C8 ray compiler or source-incidence theorem;
- Grand MCA hard input 2;
- a finite or asymptotic ledger payment;
- a recurrence-parent, Grand MCA, or Grand List theorem;
- any official-score movement.

The remaining wall is a source-valid image-scale theorem for every actual
primitive semantic first-match cell, followed by a disjoint same-line sum of
those budgets without interchanging `sup_line sum_lambda` with
`sum_lambda sup_line`.
