# Rank-15 two-flat locator-saturation normal form

## Status

`PROVED` as a necessary structural theorem, with an exact arithmetic audit.
It is not a two-flat ceiling, a rank-15 closure, or a Grand List result.

For the deployed residual state, every putative survivor with
`212 <= M <= 218` is forced into one gcd-reduced polynomial pencil.  Almost
all residual evaluation points lie in 15-rich fibers of its rational map,
the selected fiber polynomials are pairwise coprime, and their product nearly
factors the evaluation-domain locator.  The theorem eliminates no value of
`M`.

## Source anchors and novelty boundary

The publication audit used the following frozen sources.

1. Current authority base:
   `origin/main@ea4eb0784417ca5ab503a3c31a7eef6464ad100a` and `agents.md`.
2. Packet copy of the pending affine-section source
   `experimental/notes/l2/affine_section_one_row_rank_reduction.md`, identical
   to commit `4b3b7f560ffae66cc6184feaabf0e10dcb907581` and SHA-256
   `3d2c7c3687d2fa4b6202e8de87f64f4e619d427183e23d91a2f1cde9b6451c31`.
   It supplies the one-row object, the actual-universal-set convention, and
   the stateful affine-section consumer.
3. R13 packet source `R12_ROLE_03_FINAL_RESPONSE.txt`, SHA-256
   `c65f6dba35d1bd21af7e198de341d45aef0d23d9d4731a95e9074c262efb6f5d`.
   Its direction-capacity result supplies the previously known residual state
   and the imported one-flat cap.  Its verdict label is not used as authority.
4. Preserved R13 Role 03 response, SHA-256
   `5fe3ecf2fa0b2ee68d7d370704dad8e6f58f86614f46f242ac7c7ac37ea850ec`.
   The proof and arithmetic below were reconstructed and independently
   replayed after hostile audit of its exact structural core.

The one-pencil moving-root proposition in
`experimental/asymptotic_rs_mca_frontiers.tex`
(`prop:split-pencil-payment`) is a conceptual neighbor, not a dependency.  The
object in `experimental/notes/thresholds/split_pencil_ray_collapse.md` is a
locator-module census and is also different: the present theorem concerns the
common polynomial direction pencil of one actual affine two-flat.

The numerical state is printed as a hypothesis below.  Thus the local theorem
does not depend on whether either pending affine-section commit merges.

## Object, field, partition, and normalization ledgers

```text
object:              base-field one-row Reed-Solomon agreement list
agreement predicate: |{x in H : P(x)=U(x)}| >= m (closed)
local affine object: exact affine two-flat in F[X]_<K
field theorem:       arbitrary field F, with H a set of distinct F-points
code/list field:     F; deployed specialization F_p
deployed field:      p=2^31-2^24+1=2,130,706,433
extension fields:    none used
MCA/CA/line object:  none used
challenge/list denominator: none used by the local theorem
q_gen/q_line/q_chal: not invoked or transferred
symbol q below:      coordinate-section list cap, not a field cardinality
domain structure:    no subgroup or smoothness hypothesis
```

There is no catalogue first-match operation in this theorem.  Instead there
are exact partitions:

```text
H = Z disjoint-union I disjoint-union active coordinates,
active coordinates -> one affine parameter line ell_x,
active coordinates -> one projective normal direction [A(x):B(x)],
H\Z = R disjoint-union C after the rich directions are selected.
```

Thus a coordinate, a saturated coordinate line, and a pair of listed points
are never charged to two different cells.  A later compiler may place the
entire two-flat state in its own first-match cell, but that is external to this
note.

All locators are monic.  The common gcd `G` is monic, the residual pair
`(A,B)` is coprime, every nonzero fiber polynomial is rescaled to monic form,
and `Q_T` and `E` are consequently monic.  Projective directions are not
counted with scalar multiplicity.  No identity such as `L_H=X^n-1` is used.

## Exact hypotheses

Let `F` be a field, let `H` be a set of `n` distinct elements of `F`, and let
`U:H -> F`.  Put

```text
L_m(U) = {P in F[X]_<K : |{x in H : P(x)=U(x)}| >= m}.
```

Let

```text
calA = P_0 + span_F{V_1,V_2}
```

be an exact affine two-flat in `F[X]_<K`, so `V_1,V_2` are linearly
independent.  Let its *actual* universal agreement set be

```text
Z = {x in H : P(x)=U(x) for every P in calA},   |Z|=u,
S = L_m(U) intersect calA,                      |S|=M.
```

Assume every proper coordinate section outside the universal set contains at
most `q` listed points:

```text
|S intersect {P in calA : P(x)=U(x)}| <= q       for every x in H\Z.
```

The deployed specialization is

```text
n = 2,097,152,  K = 1,048,576,  m = 1,116,047,
u = 1,043,596,  q = 15,
N = n-u = 1,053,556,
a = m-u = 72,451,
lambda = K-1-u = 4,979,
212 <= M <= 218.
```

The cap `q=15` is an explicit imported local hypothesis.  This note neither
reproves it nor promotes its pending affine-section compiler.

## Theorem: locator-saturation normal form

Let

```text
L_Z(X) = product_{z in Z} (X-z).
```

After choosing the displayed basis of the direction space, there are
polynomials `G,A,B` with `G` monic such that

```text
V_1 = L_Z G A,          V_2 = L_Z G B,
gcd(A,B)=1.
```

Put

```text
g = deg G,       d = max(deg A,deg B),
I = {x in H\Z : G(x)=0},       r=|I|.
```

Then

```text
r <= g,          d+g <= lambda,          d <= lambda-r.       (1)
```

Every point of `I` is inactive: no polynomial in `calA` agrees with `U`
there.  For `x in H\(Z union I)`, the agreement equation is the affine line

```text
ell_x = {(s,t) in F^2 : s A(x)+t B(x)=omega_x}.                (2)
```

Write `h_x=|S intersect ell_x|`, so `0 <= h_x <= q`.

### Saturation and rich-line multiplicity

For the deployed `q=15`, define

```text
Delta_M = 15N-Ma,             W_M = N-Delta_M = Ma-14N.
```

Then

```text
15r + sum_active (15-h_x) <= Delta_M,                          (3)
#{x active : h_x=15} >= W_M+14r.                              (4)
```

If an affine parameter line `ell` contains exactly 15 points of `S`, and

```text
e_ell = #{x active : ell_x=ell},
```

then

```text
e_ell >= ceil((15a-N)/14) = ceil(33,209/14) = 2,373.          (5)
```

The integer threshold is sharp for this argument:

```text
N+14*2,372 = 15a-1 = 1,086,764.                              (6)
```

### One coprime pencil and a finite-image rational map

For a projective direction `nu=[alpha:beta] in P^1(F)`, put

```text
F_nu(X) = monic normalization of beta A(X)-alpha B(X).
```

Distinct `F_nu` are pairwise coprime.  Let `T` be the set of directions
supporting a 15-point coordinate line and put `t=|T|`.  For every direction
define

```text
c_nu = #{x active : [A(x):B(x)]=nu}.
```

For `nu in T`,

```text
2,373 <= c_nu <= deg F_nu <= d,
sum_{nu in T} c_nu >= W_M+14r,
td >= W_M+14r.                                                (7)
```

Let `b_nu` be the number of 15-point affine lines in direction `nu`, and let
`b=sum b_nu`.  Rich-line packing gives

```text
t <= b <= floor(M floor((M-1)/14)/15) = M,                   (8)
b_nu <= floor(d/2,373) <= 2.                                  (9)
```

The coprime pair defines a rational map on the entire residual evaluation
set,

```text
phi:H\Z -> P^1(F),       phi(x)=[A(x):B(x)].
```

For `nu in T`, let

```text
R_nu = {x in H\Z : F_nu(x)=0},
R = disjoint-union_{nu in T} R_nu,       rho=|R|,
C = (H\Z)\R.
```

Then

```text
rho >= W_M+14r,          |C| <= Delta_M-14r.                 (10)
```

Every selected value has at least 2,373 active preimages, and all but at most
`Delta_M-14r` residual evaluation points map into the `t` selected values.

### Exact evaluation-domain locator identity

For a finite set `Y`, let `L_Y` be its monic locator.  Define

```text
Q_T = product_{nu in T} F_nu,       E = Q_T/L_R.
```

The quotient is a polynomial and the following identity is exact in `F[X]`:

```text
L_Z L_C Q_T = E L_H.                                             (11)
```

Factorwise, `F_nu=L_{R_nu}E_nu` and `E=product E_nu`.  Moreover,

```text
deg E <= td-W_M-14r
      <= 4,979t-W_M-(t+14)r,                                  (12)
r <= floor((4,979t-W_M)/(t+14)).                              (13)
```

### Pair-difference coupling

Write the parameter points of `S` as `p_i=(s_i,t_i)` and put

```text
Psi_S(X) = product_{i<j}
           ((s_i-s_j)A(X)+(t_i-t_j)B(X)).
```

Each 15-point line contains 105 pairs, so the exact divisor is

```text
product_{nu in T} F_nu(X)^(105 b_nu)  divides  Psi_S(X).       (14)
```

This couples the finite incidence configuration to the same polynomial
pencil used in the locator identity.

## Proof

Every direction polynomial vanishes on the actual universal set `Z`, hence
`V_i=L_Z R_i` with `deg R_i<=K-1-u=lambda`.  Taking the monic gcd
`G=gcd(R_1,R_2)` and writing `R_1=GA`, `R_2=GB` proves `d+g<=lambda` and
`gcd(A,B)=1`.  The set `I` has at most `g` distinct roots.  At a point of
`I`, both direction polynomials vanish.  If `P_0(x)=U(x)`, that point would
belong to `Z`; therefore it is inactive.  Outside `Z union I`, `(A(x),B(x))`
is nonzero because `A,B` are coprime, and division of the agreement equation
by `L_Z(x)G(x)` gives (2).  This proves (1).

Every `P in S` has at least `a=m-u` agreements outside `Z`, all at active
coordinates.  Double counting gives

```text
Ma <= sum_active h_x
   = 15(N-r)-sum_active(15-h_x),
```

which is (3).  Every nonsaturated active coordinate contributes at least one
to the deficiency sum, giving (4).

Fix 15 listed parameter points on a line `ell`.  Their total outside-`Z`
agreement count is at least `15a`.  A coordinate with `ell_x=ell` contributes
15.  Every other active coordinate line meets `ell` in at most one point, and
an inactive coordinate contributes zero.  Hence

```text
15a <= 15e_ell+(N-e_ell)=N+14e_ell,
```

which proves (5) and (6).

If a nonconstant polynomial divided `F_nu` and `F_mu` for two distinct
projective directions, invertible linear combinations would make it divide
both `A` and `B`.  This contradicts coprimality.  Every active coordinate of
direction `nu` is a distinct root of `F_nu`, proving the upper side of (7);
(5) gives its lower side.  Every saturated coordinate belongs to a rich
direction, so summing proves the remaining parts of (7).

At a listed point, distinct 15-point lines through it consume disjoint sets of
14 other listed points.  Thus at most `floor((M-1)/14)=15` rich lines pass
through one listed point.  Counting point-line incidences proves (8).  In one
direction, distinct rich lines are parallel and consume disjoint coordinate
sets of size at least 2,373, while their total multiplicity is at most `d`.
This proves (9).

Pairwise coprimality makes the sets `R_nu` disjoint.  Their union contains all
active points counted by the `c_nu`, proving (10).  The squarefree locator
`L_{R_nu}` divides `F_nu`, hence `L_R` divides `Q_T`.  Since

```text
L_H=L_Z L_R L_C,
```

substitution of `Q_T=E L_R` proves (11).  Degree counting, (7), and
`d<=4,979-r` prove (12); nonnegativity of `deg E` gives (13).

Finally, if `p_i,p_j` lie on a rich line of normal direction
`nu=[alpha:beta]`, their difference vector is a nonzero scalar multiple of
`(beta,-alpha)`.  The corresponding factor of `Psi_S` is therefore a nonzero
scalar multiple of `F_nu`.  The 105 pairs on each rich line prove (14).

## Two exact capacity relaxations

These are necessary conditions only.  For `2<=j<=15`, define

```text
B_j(M) = floor(M floor((M-1)/(j-1))/j),
D_M(d,N_0) = N_0 + sum_{j=2}^{15} min(N_0,d B_j(M)).          (15)
```

For each direction, let `h_nu` be the maximum occupancy of one of its
coordinate lines.  Directions with `h_nu=0` are omitted.  Integer layer cake,
with the omitted baseline bounded by `N_0`, gives

```text
sum_x h_x <= sum_nu c_nu h_nu <= D_M(d,N_0).                 (16)
```

The inequality in (16), rather than an equality over zero-occupancy
directions, is essential statement hygiene.  With `N_0=N-r`, every survivor
satisfies

```text
Ma <= D_M(d,N-r).                                            (17)
```

There is also an exact pair-budget relaxation.  Select one maximum-occupancy
line in each occupied direction.  Distinct selected directions use disjoint
pairs, so

```text
sum_nu binom(h_nu,2) <= binom(M,2).                           (18)
```

Let `U_q(f,B)` be the maximum number of occupancy upgrades available to `f`
full-weight directions with pair budget `B`.  If `L` is the largest integer
`0<=L<=q-1` satisfying

```text
f L(L+1)/2 <= B,
```

then

```text
U_q(f,B) = f(q-1)                                      if L=q-1,
           fL+min(f,floor((B-fL(L+1)/2)/(L+1)))        otherwise. (19)
```

Write `N_0=fd+s`, `0<=s<d`, and `B=binom(M,2)`.  The exact optimum of the
relaxation is

```text
P_M(d,N_0) = N_0+d U_15(f,B)                              if s=0,

P_M(d,N_0) = N_0 + max_{1<=h<=15}
  [s(h-1)+d U_15(f,B-binom(h,2))]                         if s>0. (20)
```

Terms with negative remaining budget are omitted.  To prove (20), transfer
coordinate weight from a lower-occupancy direction to a higher-occupancy
direction until the latter has weight `d` or the former is empty.  Pair cost
does not increase and the objective does not decrease.  Thus all upgraded
directions have weight `d` except possibly one of weight `s`.  For each full
direction, its successive upgrades cost `1,2,...,14` pairs and all have value
`d`, so filling the cheapest complete layers proves (19) and (20).  Therefore

```text
Ma <= P_M(d,N-r).                                            (21)
```

## Complete deployed degree ledger

Let

```text
t_0    = ceil(W_M/4,979),
d_dir  = min{d : Ma<=D_M(d,N)},
d_pair = min{d : Ma<=P_M(d,N)},
d_min  = max(d_dir,d_pair).
```

Let `r_max` be the largest `r` for which both capacity inequalities can still
hold after imposing the maximal possible degree `d=4,979-r` and replacing
`N` by `N-r`.  Exact integer evaluation gives:

| M | Delta_M | W_M | t_0 | d_dir | d_pair | necessary d >= | r_max |
|---:|--------:|----:|----:|------:|-------:|---------------:|------:|
| 212 | 443,728 | 609,828 | 123 | 3,717 | 4,674 | 4,674 | 304 |
| 213 | 371,277 | 682,279 | 138 | 3,807 | 4,675 | 4,675 | 303 |
| 214 | 298,826 | 754,730 | 152 | 3,949 | 4,676 | 4,676 | 303 |
| 215 | 226,375 | 827,181 | 167 | 4,089 | 4,676 | 4,676 | 302 |
| 216 | 153,924 | 899,632 | 181 | 4,228 | 4,676 | 4,676 | 302 |
| 217 | 81,473 | 972,083 | 196 | 4,480 | 4,677 | 4,677 | 302 |
| 218 | 9,022 | 1,044,534 | 210 | 4,792 | 4,677 | 4,792 | 176 |

In particular, every survivor has `d>=4,674`; any mechanism whose residual
fibers all have degree at most 4,096 is excluded from this state.

For `M=218`, (13) gives the complete locator-only inactive-root ledger:

| t | 4,979t-W_218 | necessary r <= |
|--:|--------------:|---------------:|
| 210 | 1,056 | 4 |
| 211 | 6,035 | 26 |
| 212 | 11,014 | 48 |
| 213 | 15,993 | 70 |
| 214 | 20,972 | 91 |
| 215 | 25,951 | 113 |
| 216 | 30,930 | 134 |
| 217 | 35,909 | 155 |
| 218 | 40,888 | 176 |

## Sharp `M=218, d=4,792` branch

Here (7) gives

```text
4,792t >= 1,044,534+14r.
```

Since `t<=218` and

```text
218*4,792-1,044,534=122,
```

one must have

```text
t=218,       r<=8.                                           (22)
```

Equations (8) and (22) force `b=t=218`: there is exactly one rich line in
each direction.  There are `218*15` point-line incidences, and each listed
point lies on at most 15 rich lines.  Equality forces every point to lie on
exactly 15.  Hence the graph joining pairs not covered by a rich line is
7-regular and has

```text
binom(218,2)-218 binom(15,2) = 763 = 218*7/2                (23)
```

edges.

Let `e_nu` be the coordinate multiplicity of the unique rich line in
direction `nu`.  Equations (4) and (12) give

```text
sum_{nu in T} (4,792-e_nu) <= 122-14r,
deg E <= 122-14r.                                           (24)
```

Thus `deg E<=122` at `r=0` and `deg E<=10` at `r=8`.  The pair divisor
specializes to

```text
Q_T^105 divides Psi_S.                                      (25)
```

Up to a nonzero scalar, the quotient is the product of the 763 uncovered
pair-difference pencil factors.

## Reproducibility

Run

```text
python3 experimental/scripts/verify_rank15_locator_saturation_normal_form.py
```

The verifier is standard-library only and contains no `assert`-dependent
logic.  It recomputes every integer in (5), (6), the two tables, and
(22)-(24); finds both degree floors and every `r_max` by exhaustive integer
search; compares (19)-(20) against a literal direction-weight dynamic program
on 1,200 deterministic small instances; and rejects boundary tamper claims.
It is intentionally optimization-safe and produces identical output under
`python3` and `python3 -O`.

## Ledger impact

This is a strict normal-form reduction, not a threshold improvement.  No
value of `M` in `212,...,218` is removed, so the published local ceiling
remains 218.  The first possible downstream consumer is the dimension-two
state inside the pending dimension-15 affine-section recurrence.  The local
result is insensitive to the Grand MCA catalogue, image-denominator, ray,
profile, reserve, and endpoint ledgers.

## Explicit nonclaims

This note does not prove any of the following:

- `M<=211`, or the nonexistence of a survivor for any `M` in `212,...,218`;
- a source-valid construction with `M>=212`;
- realizability of any row of either necessary-condition table;
- representability of the forced 218-line incidence structure over `F_p`;
- closure of affine rank 15, control of affine rank at least 16, or the
  one-row Grand List target;
- an interleaved Grand List endpoint, an adjacent safe/unsafe certificate,
  any Grand MCA statement, or any official prize movement;
- a multiplicative-subgroup identity for `L_H`;
- sufficiency of either capacity relaxation.

## Exact remaining wall

The first branch to eliminate is the simultaneous algebraic system

```text
M=218, d=4,792, t=b=218, r<=8,
deg E<=122-14r,
L_Z L_C Q_T = E L_H,
Q_T^105 divides Psi_S,
```

with a 7-regular uncovered-pair graph and only 763 uncovered pair factors.
After that, all remaining normal forms must be eliminated for `M=217` down to
`M=212`; removing only the top part of the interval does not prove ceiling
211.  The statewise dimension-two recurrence must then be replayed rather
than assuming this displayed state remains the unique maximizer.  Even a
local ceiling 211 would close only the rank-15 recurrence route: a separate
theorem is still required for one-row lists of affine dimension at least 16.
