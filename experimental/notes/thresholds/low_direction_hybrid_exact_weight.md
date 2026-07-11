# Low-direction hybrid exact-weight compiler

- **Status:** PROVED for the stated per-chart branch.
- **Track:** asymptotic hard input C / condition A6.
- **Base audited:** `origin/main` at `8264eae`.
- **Verifier:**
  `experimental/scripts/verify_low_direction_hybrid_exact_weight.py`
  (zero arguments, Python standard library only).

## Exact theorem

Let `H_U : F^U -> F^R` have the genuine weighted Reed-Solomon parity
columns

```text
h_x = lambda_x (1,x,...,x^(R-1))^T,  lambda_x != 0,
```

at distinct `x in U`, where

```text
N=|U|=R+kappa,  kappa>=1.
```

Fix `0<=t<R`, `y_0,y_1 in im(H_U)` with `y_1!=0`, and an actual
post-first-match set `Z_lambda^o` of distinct transverse slopes.  For every
`gamma in Z_lambda^o`, choose one actual witness `c_gamma` such that

```text
H_U c_gamma = y_0 + gamma y_1,
wt(c_gamma) <= t,
{y_0,y_1} not subset span{h_x:x in supp(c_gamma)}.          (1)
```

Define the direction distance and choose a minimum lift:

```text
d = min{wt(v):H_U v=y_1},
J = supp(v),
M = N-d,
Delta = R+1-d = M-kappa+1.                                (2)
```

Assume `t<M`.  For every integer `0<=e<=t`, put

```text
D_e = min(M,max(Delta,d+2e-2t)),                           (3)
J_e = M D_e - 2Me + e^2,                                  (4)
h_e = max(1,d+e-t).                                        (5)
```

If `J_e>0` for every `0<=e<=t`, then

```text
|Z_lambda^o|
  <= sum_(e=0)^t floor(d/h_e) floor(M(D_e-e)/J_e)          (6)
  <= N^4.                                                  (7)
```

Consequently, along any sequence with `N<=n`, this chart directly satisfies

```text
|Z_lambda^o| <= exp(o(n))(1+barN_lambda).                  (8)
```

The result is not a bound for the whole low-weight list of every affine GRS
coset.  It is a bound for the actual line-compatible punctured words and the
actual slope multiplicity above each such word, after first-match deletion.

## Proof

### 1. The actual punctured affine GRS coset

The kernel of `H_U` is an `[N,kappa,R+1]` GRS code.  Also `d<=R`, because
any `R` parity columns form a basis and hence give an `R`-coordinate lift of
`y_1`.

Let `P_J` delete the coordinates in `J`.  If a kernel word is killed by
`P_J`, it is supported on at most `d<=R` coordinates.  The kernel minimum
distance `R+1` forces that word to vanish.  Thus puncturing is injective on
the kernel.  Its image `C_J` has length `M`, dimension `kappa`, and distance
at least `R+1-d`.  Singleton gives the reverse inequality, so

```text
C_J is an [M,kappa,Delta] GRS code,
Delta=R+1-d=M-kappa+1.                                    (9)
```

The same injectivity argument applies to every affine solution set.  Hence

```text
A = P_J({u:H_U u=y_0})                                    (10)
```

is one actual affine coset of `C_J`, and each `w in A` has a unique affine
lift `u` with `H_U u=y_0`.

For a selected slope, set

```text
u_gamma = c_gamma-gamma v,
w_gamma = P_J(u_gamma)=P_J(c_gamma) in A.                  (11)
```

The last equality uses that `v` vanishes outside `J`.  Therefore
`e_gamma=wt(w_gamma)` lies in `[0,t]`.

### 2. Exact slope multiplicity above one punctured word

Fix `w in A` of weight `e`, and let `u` be its unique affine lift.  Every
selected slope mapping to `w` has

```text
c_gamma = u+gamma v.                                      (12)
```

Outside `J`, this word has exactly `e` nonzero coordinates.  Its weight
bound therefore forces at least `d+e-t` zero coordinates on `J` when that
number is positive.

Transversality forces at least one zero on `J` even when `d+e-t<=0`.  If
`c_gamma` were nonzero everywhere on `J`, then `supp(v)=J` would be contained
in `supp(c_gamma)`.  Outside `J`, `u=c_gamma`, while all coordinates inside
`J` already belong to `supp(c_gamma)`; hence both `supp(u)` and `supp(v)`
would be contained in `supp(c_gamma)`.  This would put both `y_0=H_U u` and
`y_1=H_U v` in the parity-column span of that support, contradicting (1).

Thus every slope above `w` consumes at least

```text
h_e=max(1,d+e-t)                                          (13)
```

zero coordinates on `J`.  For each `x in J`, the coordinate
`u(x)+gamma v(x)` is a nonconstant affine function of `gamma`, so it vanishes
for at most one slope.  There are only `d` coordinates in `J`.  The number
of slopes above one fixed punctured word is therefore at most

```text
floor(d/h_e).                                             (14)
```

This is the actual slope-cluster factor; no raw-witness count is substituted.

### 3. The two-block common-zero separation

Fix `e`, and let `W_e` be the distinct words among the `w_gamma` having
weight exactly `e`.  For each `w in W_e`, retain one corresponding slope and
witness, and define zero sets in the two coordinate blocks by

```text
X_w = {x in U\J:w(x)=0},
Y_w = {x in J:c_w(x)=0}.                                  (15)
```

Then `|X_w|=M-e` and

```text
|Y_w| >= b_e := max(0,d+e-t).                             (16)
```

For distinct `w,w'`, the difference `w-w'` is a nonzero word of `C_J`, so

```text
|X_w intersect X_w'| <= M-Delta.                          (17)
```

Their retained slopes are distinct.  After division by the nonzero slope
difference, `c_w-c_w'` is a lift of `y_1`; it has weight at least `d` and
therefore at most `N-d=M` zero coordinates.  Common zeros in the two blocks
give

```text
|X_w intersect X_w'|+|Y_w intersect Y_w'| <= M.           (18)
```

Since both `Y` sets lie in a `d`-set,

```text
|Y_w intersect Y_w'|
  >= max(0,2b_e-d)
   = max(0,d+2e-2t).                                      (19)
```

Combining (17)--(19), and capping an impossible separation at the block
length, gives

```text
|X_w intersect X_w'| <= M-D_e,
D_e=min(M,max(Delta,d+2e-2t)).                            (20)
```

The new term `d+2e-2t` is the forced overlap contribution from the
minimum-lift block.  It is absent from the integrated high-direction and
punctured-Johnson tests, which use only one of the two zero caps.

### 4. Exact constant-weight incidence bound

Put

```text
L_e=|W_e|,  A_e=M-e,  C_e=M-D_e.
```

For each outside coordinate `x`, let `r_x` count the sets `X_w` containing
it.  Then

```text
sum_x r_x = L_e A_e,
sum_x r_x^2 >= L_e^2 A_e^2/M                              (21)
```

by Cauchy-Schwarz.  The pairwise intersection bound gives

```text
sum_x binom(r_x,2) <= binom(L_e,2) C_e.                   (22)
```

Using `sum r_x^2=sum r_x+2 sum binom(r_x,2)` in (21)--(22) yields

```text
L_e(A_e^2-MC_e) <= M(A_e-C_e).                            (23)
```

The two quantities in (23) are exactly

```text
A_e^2-MC_e = (M-e)^2-M(M-D_e) = J_e,
A_e-C_e = D_e-e.                                         (24)
```

If `J_e>0`, then

```text
L_e <= floor(M(D_e-e)/J_e).                               (25)
```

If the uncapped separation in (20) exceeds `M`, no distinct pair exists.
The capped formula still gives at least one because

```text
M(D_e-e)-J_e=e(M-e)>=0.                                   (26)
```

Thus (25) also covers that case.

### 5. Sum, polynomial bound, and post-first-match compiler

Multiplying (14) and (25), then summing the exact weights, proves (6).  Under
`t<M`, there are at most `M` strata.  Each positive integer `J_e` is at
least one, while

```text
d<=N,  M(D_e-e)<=M^2<=N^2.
```

This proves (7).  For a nonempty full profile slice,
`barN_lambda=|Omega_lambda^0|/L_lambda>=1`; with `N<=n`, one has
`N^4=exp(O(log n))=exp(o(n))`, proving (8).  No ambient-image substitution,
full-image hypothesis, or A4 estimate is used in this final A6 conversion.

The proof was written for the actual `Z_lambda^o`.  Any earlier algebraic or
first-match deletion only removes slopes, so the estimate is monotone under
the complete preceding deletion order.

## Strict positive-rate family beyond both Johnson tests

For every integer `m>=1`, take

```text
(N,R,kappa,t,d)=(90m,86m,4m,31m,50m),
M=40m,
Delta=36m+1.                                              (27)
```

Both rates are positive: `kappa/N=2/45` and `kappa/M=1/10`.  Both integrated
Johnson sufficient conditions fail strictly:

```text
(N-t)^2=(59m)^2=3481m^2 < 3600m^2=N(N-d),                (28)
Delta M-2tM+t^2=m(40-79m)<0.                             (29)
```

The integrated deep branch also fails:

```text
3t=93m>86m=R.                                             (30)
```

Moreover `kappa=Theta(N)`, so the bounded-kernel transverse-secant branch is
not subexponential here.

For (27), `d+2e-2t=2e-12m`, and exact integrality gives

```text
D_e = 36m+1       for 0<=e<=24m,
      2e-12m      for 24m+1<=e<=26m-1,
      40m         for 26m<=e<=31m.                        (31)
```

Consequently,

```text
J_e = e^2-80me+1440m^2+40m   for 0<=e<=24m,
      e^2-480m^2              for 24m+1<=e<=26m-1,
      (40m-e)^2               for 26m<=e<=31m.            (32)
```

The first quadratic decreases through `e=24m`, the middle quadratic
increases, and the last expression decreases through `e=31m`.  Their
relevant endpoint identities are

```text
J_(24m)   = 96m^2+40m,
J_(24m+1) = 96m^2+48m+1,
J_(31m)   = 81m^2.                                       (33)
```

Thus `J_e>=81m^2>0` at every exact weight.

For the explicit slope bound, write the two factors in (6) as

```text
a_e=floor(50m/(19m+e)),
b_e=floor(40m(D_e-e)/J_e).                                (34)
```

Globally `a_e<=2`, and `a_e<=1` once `e>=6m+1`.  On `0<=e<=6m`,

```text
2J_e-40m(D_e-e)
  =2e^2-120me+1440m^2+40m
  >=792m^2+40m>0,                                        (35)
```

so `b_e<=1` there.  Globally `b_e<=4`.  On the first interval this follows
from

```text
5J_e-40m(D_e-e)
  =5e^2-360me+5760m^2+160m
  >=160m>0.                                               (36)
```

On the middle interval the exact factorization is

```text
5J_e-40m(D_e-e)=5(e-24m)(e+16m)>0.                       (37)
```

On the capped interval,

```text
40m(D_e-e)/J_e=40m/(40m-e)<=40/9<5.                      (38)
```

There are `6m+1` low strata and `25m` remaining strata.  Therefore

```text
|Z_lambda^o| <= 2(6m+1)+4(25m)=112m+2.                   (39)
```

This is uniform in the field, received line, affine punctured coset, and
all preceding first-match deletions.

## Actual weighted-RS realization and nontrivial coset

Let `F` contain at least `90m` elements, choose `U subset F` of size `90m`,
and allow arbitrary nonzero parity weights `lambda_x`.  Put

```text
G_U(X)=prod_(x in U)(X-x),
omega_x=(lambda_x G_U'(x))^(-1).
```

The actual weighted kernel is

```text
ker H_U={(omega_x p(x))_(x in U):deg p<kappa}.             (40)
```

Indeed, for `deg p<kappa` and `0<=j<R`, the polynomial `X^j p(X)` has
degree at most `N-2`; the Lagrange leading-coefficient identity gives
`sum_x x^j p(x)/G_U'(x)=0`.  This proves containment in the kernel, and
both spaces have dimension `kappa`.

Choose a `40m`-set `T_0 subset U`, define

```text
f(X)=prod_(x in T_0)(X-x),
v_x=omega_x f(x),
y_1=H_U v.                                                (41)
```

The vector `v` vanishes exactly on `T_0`, so `wt(v)=50m`.  Every other lift
of `y_1` is `omega_x(f(x)+p(x))` with `deg p<4m`.  The polynomial `f+p` has
degree exactly `40m`, hence at most `40m` roots in `U`.  Every lift has
weight at least `50m`, and therefore

```text
d=50m.                                                    (42)
```

Now `J=U\T_0`.  Choose a `6m`-set `S subset T_0`, a vector `w` supported
exactly on `S`, a partition `J=B_1 disjoint_union B_2` with
`|B_1|=|B_2|=25m`, and distinct slopes `gamma_1,gamma_2`.  Define `u` by

```text
u|_(T_0)=w,
u|_(B_i)=-gamma_i v|_(B_i),
y_0=H_U u,
c_i=u+gamma_i v.                                         (43)
```

Then

```text
supp(c_1)=S disjoint_union B_2,
supp(c_2)=S disjoint_union B_1,
wt(c_1)=wt(c_2)=6m+25m=31m=t.                            (44)
```

Because `t<d`, `y_1` is not in the parity-column span of either support;
both slopes are transverse.  Puncturing `J` gives the same word `w` from
both witnesses, and

```text
A=w+C_J.                                                  (45)
```

This coset is nontrivial: `w!=0` and `wt(w)=6m<Delta=36m+1`, so `w` is not
in `C_J`.  At exact weight `e=6m`, one has

```text
h_e=25m,
floor(d/h_e)=2,
floor(M(D_e-e)/J_e)=1.                                   (46)
```

Thus the two-slope construction attains the exact slope-cluster factor.

## Exact complementary wall

The proof applies one exact-weight stratum at a time.  Therefore an unpaid
chart with `t<M` must have an occupied exact punctured weight `e` for which
`J_e<=0`.  The capped regime `D_e=M` cannot cause failure, because

```text
J_e=(M-e)^2>0  for e<=t<M.                                (47)
```

Only the following two walls remain:

```text
Punctured-distance wall:
  d+2e-2t<=Delta,
  e^2-2Me+MDelta<=0.                                      (48)

Mixed minimum-lift wall:
  Delta<d+2e-2t<M,
  e^2<=M(2t-d).                                           (49)
```

The separate full-support locus `t>=M` is outside this theorem.  A next
attack should fix one occupied weight satisfying (48) or (49), then use
higher-order GRS incidence/generalized-weight information or compile
low-affine-rank concentration to an already named pencil, saturation, or
rank-collapse profile.

## Ledger effect and nonclaims

- **A6:** paid only for actual realized minimum-lift charts with `t<M` and
  positive `J_e` on every occupied exact-weight stratum.  The stronger
  all-weights hypothesis in the theorem is a convenient uniform certificate.
- **A2:** not proved.  There is no witness-exhaustive atlas theorem, no proof
  of only `exp(o(n))` realized charts/supports/minimum lifts, and no global
  add-back statement.
- **A4:** not proved.  There is no image-scale MI+MA, direct Sidon payment,
  full-image certificate, or primitive max-fiber theorem.
- **A7:** not proved.  There is no complete profile-envelope comparison with
  the target and no quotient-field dominance conclusion.
- **A5:** the theorem assumes the actual weighted-Vandermonde geometry; it
  does not replace it with a synthetic moment map.
- **Finite ledger:** no CAP25 v13 row, M31 cell, row-sharp-Q atom, finite
  survivor census, adjacent safe/unsafe inequality, or deployed budget is
  changed.
- The theorem does not bound the complete low-weight list of a general affine
  GRS coset, does not cover an occupied `J_e<=0` stratum, and does not cover
  `t>=M`.
- The explicit two-slope chart is a source-valid raw chart, but no claim is
  made that it survives every earlier quotient, planted, pencil, curve, or
  saturation deletion in a complete atlas.
- No lower reserve, full RS-MCA theorem, or prize solve is claimed.

## Verification coverage

Run

```text
/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  experimental/scripts/verify_low_direction_hybrid_exact_weight.py
```

The verifier uses exact integer and prime-field arithmetic only.  It:

1. exhausts all raw transverse syndrome lines in four small `F_5` charts and
   checks (3)--(7), before any first-match deletion;
2. checks every family weight `0<=e<=31m` for `1<=m<=200`, including (28)--(39)
   and the exact theorem sum;
3. checks the breakpoint, endpoint, monotonicity, factorization, and interval
   certificates through `m=10,000`; and
4. exhausts bounded integer chart parameters and verifies that every
   nonpositive `J_e` with `t<M` lies in exactly one of (48)--(49); and
5. constructs the actual `m=1` weighted realization over `F_97`, verifies the
   weighted kernel, both transverse witnesses, their common punctured word,
   the nontrivial affine coset, and (42)--(46).
