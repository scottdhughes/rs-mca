# Near-norm-gate first-failure remainder packing

Status: `PROVED / POINTWISE / STRICT PRIME SUBREGIME`.

This supporting note counts the failed branch left by the integrated
split-prime descent from PR `#464`.  It is not a "small split primes" theorem:
the hypothesis is a lower norm gate and places no upper bound on `p`.  After a
fiber basepoint is fixed, every coefficient belongs to a one-sided mask.  A
common odd-root interval then turns distinct odd-channel remainders into a
Euclidean packing, and equality of the odd remainder compiles to a smaller
one-sided even-channel fiber.

The exact constant-factor movement relative to integrated `#464` is:

```text
#464 first failed scale:       P>4h makes failure impossible;
this note:                     P>(2+epsilon)h counts failures polynomially.
```

At full length, after relabeling the fixed positive epsilon, this fills the
near-gate band

```text
(1+epsilon)N <= p^(2R/N) < approximately 2N.
```

It does not change the polynomial order of the required prime.  In `(LD)` the
gate still requires `p>=N^(2+delta)` (for a fixed `delta>0` in the relevant
linear-deficit range), so the central `p=N^(1+o(1))` branch is untouched.

## 1. Finite half-channel theorem

Let `n=2h>=4` be a power of two.  Let `p` be prime with `p=1 mod n`, let
`zeta in F_p^x` have order `n`, and put `eta=zeta^2`.  Let `I` be a consecutive
cyclic interval in `Z/nZ`, and define the consecutive cyclic decimations

```text
O={u in Z/hZ: 2u+1 in I},   q=|O|,
E={v in Z/hZ: 2v   in I},   e=|E|.                       (1)
```

For each `0<=r<2h`, fix a one-sided coefficient mask

```text
A_r in {{0},{0,1},{0,-1}}.                               (2)
```

Let `F` be any family of integer polynomials

```text
f(X)=sum_(r=0)^(2h-1) b_r X^r,   b_r in A_r,             (3)
f(zeta^k)=0 in F_p for every k in I,
X^h+1 does not divide f in Z[X].
```

Any additional common restrictions may be imposed on `F`.  In particular,
the statement remains valid after a fixed-weight equation is added.  Put

```text
w_r=max A_r-min A_r in {0,1},
V_A=(1/4) sum_(i=0)^(h-1) (w_i+w_(i+h))^2 <= h,
P=p^(2q/h).                                               (4)
```

For `0<=J<=log_2(h)-1`, put `m_l=h/2^l` and assume, for every `0<=l<J`,

```text
p^floor(e/2^(l+1)) > (2m_l)^(m_l/4).                    (ED_l)
```

### Theorem 1 (odd-remainder packing with paid even lifts)

If `P>2V_A`, then

```text
|F| <= floor(2V_A/(P-2V_A)) 2^m_J.                      (5)
```

Uniformly, because `V_A<=h`, if `P>2h`, then

```text
|F| <= floor(2h/(P-2h)) 2^m_J.                          (6)
```

For a fixed odd remainder `d`, let `nu(d)` be the number of pair coordinates
at which the compatible lift list has size two.  Without any norm gate,

```text
|F(d)| <= 2^max(nu(d)-e,0).                              (7)
```

All quantifiers here are finite and literal: every dyadic `n=2h>=4`, every
split prime, every consecutive inherited interval, every one-sided mask, and
every subfamily satisfying any further collision constraints.  Pairwise
packing requires the *same* inherited odd-root interval for all members; a
collection of unrelated high-resultant-valuation words is not covered.

## 2. Proof of Theorem 1

Write

```text
f(X)=A(X)+X^hB(X),   deg A,deg B<h,
d=A-B,               s=A+B.                             (8)
```

At the odd and even `n`th roots respectively,

```text
f(zeta eta^u)=d(zeta eta^u),
f(eta^v)=s(eta^v).                                       (9)
```

Moreover, `X^h+1` divides `f` exactly when `d=0`, and
`Res(X^h+1,f)=Res(X^h+1,d)`.  Thus the first-failure condition in (3) is
exactly `d!=0`, while the inherited equations are

```text
d(zeta eta^u)=0 for u in O,
s(eta^v)=0 for v in E.                                  (10)
```

Let `g in Z[X]` be nonzero with `deg g<h` and suppose its reduction vanishes
at those same `q` odd roots.  Since `X^h+1=Phi_(2h)` is irreducible over `Q`,
its resultant with `g` is nonzero.  Split lifting and exact Parseval give

```text
p^q <= |Res(X^h+1,g)|,
sum_(xi^h=-1) |g(xi)|^2 = h sum_i g_i^2.                (11)
```

AM--GM on the `h` squared factors in the resultant therefore gives

```text
|Res(X^h+1,g)| <= (sum_i g_i^2)^(h/2),
sum_i g_i^2 >= P.                                       (12)
```

Apply (12) to each nonzero remainder `d` and to each nonzero difference
`d-d'`.  This use of differences is valid precisely because the root interval
`O` is common.  The set consisting of zero and all distinct nonzero
remainders is pairwise separated in squared Euclidean distance by at least
`P`.

At coordinate `i`, every remainder lies in

```text
D_i=A_i-A_(i+h),   diam D_i=w_i+w_(i+h).                (13)
```

Let the distinct remainders be `d^(1),...,d^(r)`, adjoin `d^(0)=0`, and put
`M=r+1`.  Coordinatewise Popoviciu variance, followed by summation, gives

```text
sum_(0<=u<v<=r) ||d^(u)-d^(v)||_2^2 <= M^2 V_A.         (14)
```

The separation lower bound and (14) imply

```text
binom(M,2)P <= M^2V_A,
r(P-2V_A) <= 2V_A.                                      (15)
```

This proves the exact distinct-remainder factor in (5).

It remains to pay multiplicity above one remainder.  Fix `d` and one word
`f*` above it.  For another word `f` above `d`, the two half-increments agree:

```text
r_i=b_i-b_i*=b_(i+h)-b_(i+h)*,
f-f*=(1+X^h)r(X).                                       (16)
```

Each `r_i` lies in one of `{0}`, `{0,1}`, `{0,-1}`: it is the intersection of
the two one-sided common-increment lists.  Subtracting the even equations in
(10), and using that `p` is odd, yields

```text
r(eta^v)=0 for every v in E.                            (17)
```

Hence a same-remainder family injects into a length-`h` one-sided Boolean
fiber with a consecutive zero interval of length `e`.  Under `(ED_l)`, the
integrated #464 Parseval/resultant step successively extracts
`X^(m_l/2)+1`.  After `J` levels the increment is periodic modulo `m_J`, so
there are at most `2^m_J` choices.  Multiplication by (15) proves (5) and (6).

For (7), at the `nu(d)` coordinates with two compatible lifts, the `e`
consecutive even evaluations form an MDS submatrix: every `e` columns are a
Vandermonde matrix up to nonzero row and column factors.  The other
`nu(d)-e` choices determine the pivot coordinates.  This gives (7), with the
usual value one when `nu(d)<e`.  In particular, counting remainders without
paying their even lifts would be invalid.

## 3. Polynomial first-failure count

Fix `kappa,epsilon>0`.  For all sufficiently large `h`, suppose

```text
q,e >= kappa h-1,   |q-e|<=1,
p^(2q/h) >= (2+epsilon)h.                               (18)
```

Then

```text
|F| <= h^C(kappa,epsilon).                              (19)
```

Indeed, (15) gives at most `2/epsilon` odd remainders.  Let

```text
r'=(2+epsilon)/(2+epsilon/2),
H*=ceil(4 log((2+epsilon)h)/(kappa log r'))+2.           (20)
```

At an inner even-channel scale with half-length `H>=H*`, consecutive
decimation leaves at least `(q/h)H-2` odd roots.  For sufficiently large `h`,
monotonicity and (18) imply

```text
p^(2q_H/H) >= (2+epsilon/2)h > 4H,                      (21)
```

which is the powered form of the #464 descent gate at that scale.  Descent
therefore reaches length below `2H*`; each remainder has at most
`2^(2H*)=h^O(kappa,epsilon)` lifts.  This proves (19).  Equivalently, the exact
prime gate in (18) is

```text
p >= ((2+epsilon)h)^(h/(2q)).                           (22)
```

If `q/h` tends to a fixed `theta>=kappa`, the polynomial order of (22) is
`h^(1/(2theta)+o(1))`.  The improvement from `4h` to `(2+epsilon)h` changes a
constant, not this exponent.

## 4. Integration over first-failed scales

Let

```text
N=2^s,   N | p-1,   kappa N<=R<=N/2,
t_i=alpha zeta^i,
rho_i=c zeta^(a i),
v_i=rho_i(1,t_i,...,t_i^(R-1)),                         (23)
```

where `p` is prime, `zeta` has order `N`, `alpha,c` are nonzero, and
`a in Z/NZ`.  This is a pure cyclic monomial window.  For an arbitrary Boolean
mask `Omega subseteq {0,1}^N`, define

```text
Phi(x)=sum_i x_i v_i.                                   (24)
```

### Theorem 2 (near-norm-gate pure-window fiber bound)

For fixed `kappa,epsilon>0`, if

```text
p^(2R/N) >= (1+epsilon)N,                               (25)
```

then, for all sufficiently large `N`,

```text
max_y |Omega intersect Phi^(-1)(y)| <= N^C(kappa,epsilon). (26)
```

An explicit finite bound follows by setting

```text
A=(1+epsilon)N,
r_epsilon=(1+epsilon)/(1+epsilon/2),
H_0=ceil(2 log A/(kappa log r_epsilon))+2,
C_epsilon=max(1,2/epsilon):

max_y |Omega intersect Phi^(-1)(y)|
 <= 2+C_epsilon ceil(log_2 N) 2^(2H_0).                 (27)
```

### Proof

Fix a fiber basepoint `x^(0)` and put

```text
f_0(X)=sum_i (x_i-x_i^(0))X^i.                          (28)
```

Fiber equality is exactly the vanishing of `f_0` on the common consecutive
interval `{a,...,a+R-1}`.  After `j` successful dyadic divisions,

```text
f_0(X)=(1+X^n_j+...+X^(N-n_j))f_j(X),   n_j=N/2^j.      (29)
```

The coefficient on each residue class belongs to `{0,1}` if every basepoint
bit in that class is zero, to `{0,-1}` if every one is one, and to `{0}` if
the class is mixed.  Thus Theorem 1 applies at the unique first failed scale.
With `h_j=n_j/2`, its inherited root counts satisfy

```text
q_j,e_j >= floor((R/N)h_j),   |q_j-e_j|<=1.             (30)
```

The pair `(j,f_j)` reconstructs `f_0` through (29), and `f_0` reconstructs
`x`; summing first-failure counts is therefore an injection, not a
difference-word heuristic.

When `h_j>=H_0`, (25), (30), and the definition of `H_0` give

```text
p^(2q_j/h_j) >= (1+epsilon/2)N.                         (31)
```

Since `2h_j<=N`, Theorem 1 leaves at most `2/epsilon` remainders.  The same
calculation on every inner even-channel scale with half-length at least `H_0`
gives a norm above `4H`, so #464 descent leaves at most `2^(2H_0)` lifts.
Below the cutoff that trivial lift bound already holds.  There are at most
`ceil(log_2 N)` first-failure scales.  The fully divisible terminal branch
contains at most the basepoint and one all-coordinate flip.  This proves
(27), hence (26).

For any independently specified nonempty exact residual of (24), (26) is
polynomial and therefore `exp(o(N))`; since the image-normalized factor
`barN=M/L` is at least one, this supplies the corresponding pointwise C9
bound inside (25).  It does not emit that residual from C1--C8 and does not
prove `RC` or add-back.

## 5. Half-window finite corollary

At `R=N/2`, every split prime satisfies `p>=N+1`.  At the top scale,
`q=e=N/4`, so `P=p` and Theorem 1 gives at most

```text
N/(p-N) <= N                                             (32)
```

odd remainders.  For a fixed remainder, every inner length `m>=4` satisfies
the even-channel #464 gate `p>2m`, and descent stops with at most four lifts.
The top first-failure branch therefore has size at most `4N`.  If the top
scale succeeds, the same gate pays every later scale and the terminal
length-two word has at most four possibilities.  Hence, for every Boolean
mask and every pure cyclic monomial window,

```text
max_y |Omega intersect Phi^(-1)(y)| <= 4N+4.            (33)
```

This finite half-window statement is outside `(LD)`.  Its fixed-weight C9
consequence overlaps integrated PR `#463`; only the arbitrary-mask finite
bound and the explicit remainder-count/same-incidence machinery are new here.

## 6. Relation to integrated #464

- Integrated `#464` supplies the split-root resultant lower bound, exact
  odd-root Parseval identity, recursive quotient extraction, and periodic
  fiber ceiling used in `(ED_l)`.
- This note does not amend `#464`.  It is a new supporting packet for the
  previously uncounted first-failure branch.
- The new theorem-facing step is the width-sensitive Popoviciu packing (15),
  together with the same-remainder compiler (16)--(17) and the unique-scale
  injection (29)--(30).
- `#483` is unrelated to this argument.
- No external-literature novelty claim is made.

## 7. Verification

Run both interpreter modes:

```sh
python3 experimental/scripts/verify_asymptotic_c9_near_norm_gate_remainder_packing.py --check
python3 -O experimental/scripts/verify_asymptotic_c9_near_norm_gate_remainder_packing.py --check
```

The standard-library verifier uses explicit exceptions rather than bare
`assert`, so normal and optimized runs execute the same checks.  It checks
the half-channel identities, exact integer resultants and resultant-energy
separation, coordinatewise Popoviciu arithmetic, the same-remainder compiler,
MDS ceilings, descent-gate arithmetic, half-window finite bounds, and
first-failure decomposition/reconstruction smoke checks.  The output reports
how many nonempty sampled remainder families actually trigger a positive
descent level; a zero count is not presented as empirical descent coverage.

Coverage is **exhaustive** over all `3^4` one-sided masks and all consecutive
cyclic intervals at `n=4`.  Coverage at `n=8,16` is a deterministic,
representative **sample** of masks, intervals, and pure-window fibers.  These
finite scans are audit evidence; the proof above, not sampling, establishes
the quantified theorem.

## 8. Nonclaims and exact remaining wall

- No `RC` or residual-to-full compiler is proved.
- No C1--C8 emission or exhaustion theorem is proved.
- No count for arbitrary ternary words is proved; the one-sided basepoint mask
  and common inherited interval are essential.
- No deployed finite row, Paper A--D theorem, or paper frontier is changed.
- No bound in the central `p=N^(1+o(1))` fixed-linear-deficit branch is proved.
- No full-fiber claim outside pure cyclic monomial windows is made.

The exact remaining wall is a subexponential weighted remainder count below
`P=2h`: count nonzero `d_i in A_i-A_(i+h)` on a common odd interval, weighted
by their compatible even-channel lifts (or by the unconditional factor in
(7)).  A raw count of distinct `d` that discards same-remainder incidence is
not sufficient.
