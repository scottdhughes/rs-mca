# M31 maximal mass compiler: canonical global Popov shell and forced rank-46 tail

## Status

**PROVED canonical whole-list injection / PROVED exact variable-weight
packing cap / PROVED occupancy-sensitive rank-46 compiler / PROVED uniform
rank-three Forney--Pluecker dichotomy / SHARP ARITHMETIC ROUTE CUT / GLOBAL
M31 LIST ROW OPEN / LEDGER MOVEMENT ZERO.**

This packet is stacked on PR #1007 at
`97b7c94fd1822f897910589cf2aa786021f5ee01` and consumes the semantic warning
from PR #1005 at `568242657e69d9594c621814e12e53e7a9211332`.
It replaces the earlier selected rank-36 packet by the strongest compiler
currently forced from the complete forbidden-list mass and MDS incidence.

There are two exact global objects, and they must not be conflated.

1. Every listed codeword has one canonical padded degree-`R` locator in the
   Paper-D rank-two interpolation lattice.
2. Every high-multiplicity exact-weight layer has a primitive locator row made
   from its **actual errors** and hence a high-rank Forney frame.

At an interior weight the padded locator contains agreement roots, so the two
objects do not have the same syzygies.  The missing algebraic interface is
recorded as `UNPAID_PADDING_BRIDGE`, not silently assumed.

The exact deployed result is that every forbidden list forces at least
`259,881` marked rank-46 actual-error packets.  Each packet has three minimal
syzygy rows whose combined degree is at most

```text
62,295 < 67,447.
```

For the distinguished extra column, either an old-column rank-three basis
leaves a 43-support complementary subfamily with at most `62,295` new common
roots, or the extra column is a coloop and all 45 anchors collapse to rank at
most two.  Neither terminal is presently paid.

## 1. Deployed row

Throughout,

```text
p       = 2^31-1          = 2,147,483,647,
n       = 2^21            = 2,097,152,
K       = 2^20            = 1,048,576,
a       = 1,116,023,
w       = a-K             = 67,447,
R       = n-a             = 981,129,
B*      = floor(p^4/2^100)= 16,777,215,
L       = B*+1            = 16,777,216.
```

Let `D=(x_1,...,x_n)` be the ordered standard-position M31 domain and let
`C=RS_Fp(D,K)`.  For a received word `y`, write

```text
L_R(y)={c in F_p[X]_<K : wt(y-c)<=R}.
```

The theorem in this note is conditional on the existence of a forbidden
center only when it says “every forbidden list forces ...”.  It neither
constructs such a center nor proves that none exists.

## 2. Canonical whole-list injection into one rank-two lattice

For `c in L_R(y)`, let

```text
A_c={x in D:y(x)=c(x)}.
```

Choose `T_c` to be the first `a` points of `A_c` in the fixed domain order and
put

```text
W_c=Lambda_(D\T_c),              N_c=W_c c.              (2.1)
```

### Theorem 2.1 (canonical boundary Popov compiler)

The map

```text
c |-> (W_c,N_c)                                             (2.2)
```

is an injection from `L_R(y)` into the Paper-D interpolation lattice

```text
M_y={(W,N):W(x)y(x)=N(x) for every x in D}.                 (2.3)
```

Its image is exactly the degree-`R` split-locator census restricted by the
predicate “`D\Z(W)` is the first `a` points of the agreement set of `N/W`.”
Consequently it is a bijection between the whole list and that canonical
masked locus.

**Proof.**  The polynomial `W_c` is monic, has degree `R`, and divides
`Lambda_D`; `N_c` is divisible by `W_c` and has degree at most `R+K-1`.  At a
point of `T_c`, equation (2.3) follows from `y=c`; away from `T_c`, both sides
vanish.  Thus `(W_c,N_c)` lies in the lattice census.  If two codewords select
the same `T`, both agree with `y` on `a>=K` points, so their degree-`<K`
difference has at least `K` roots and is zero.  Conversely, a census pair
satisfying the displayed canonical predicate has `c=N/W` of degree `<K` and
recovers exactly the selected support.  This proves the bijection. `QED`

This is the canonical-selector repair already suggested by
`l1_arbitrary_fiber_repair.md`, now wired to the Paper-D lattice.  It removes
the raw binomial multiplicity

```text
sum_c binomial(agr(y,c),a)                                  (2.4)
```

without losing any codeword.

Let `g_1,g_2` be a shifted weak-Popov basis of `M_y`, with row degrees
`d_1<=d_2`.  Paper D proves

```text
d_1+d_2=n-K+1.                                              (2.5)
```

Since `2w<=n-K`, its near-rational dichotomy gives:

- if `d_1<=w` and the census is nonempty, the radius-`R` list contains one
  codeword;
- if `d_1>=w+1`, every canonical pair has unique coordinates

  ```text
  A g_1+B g_2,
  deg A<=R-d_1,       deg B<=R-d_2.                         (2.6)
  ```

The coefficient dimension is exactly

```text
(R-d_1+1)+(R-d_2+1)=R-w+1=2R-K+1=913,683.                 (2.7)
```

Thus `ZERO_SYNDROME` and `NEAR_RATIONAL_SINGLETON` are terminal, while the
balanced global residual is the canonical masked split-pencil locus.

## 3. The suffix-pivot form and the padding factor

Let `h(c)` be the one-based index of the `a`-th agreement point.  Write

```text
h=a+r,             0<=r<=R.
```

Among `x_1,...,x_h` there are exactly `a` selected agreements and exactly `r`
errors.  Therefore

```text
W_c=Q_h P_c,
Q_h=product_(i>h)(X-x_i),
P_c=product_(i<h, y(x_i)!=c(x_i))(X-x_i),
deg P_c=r,          P_c(x_h)!=0.                           (3.1)
```

The nonvanishing/exact-error condition on the prefix roots is essential.  An
unmasked split divisor may discard an earlier agreement and is not the
canonical representative.

Division by the complete suffix is exact:

```text
Q_h(P,M) in M_y
  <=>
(P,M) lies in the interpolation lattice of y restricted to
the first h domain points.                                 (3.2)
```

Indeed the suffix coordinates vanish after multiplication by `Q_h`, and the
remaining equations are precisely the prefix interpolation equations.  Hence
the canonical whole-list locus is a disjoint stopping-time staircase of exact
prefix cells.

There is a second factorization.  If `E_c` is the actual error support and
`j=|E_c|`, then

```text
W_c=Lambda_(E_c) Q_c,       deg Q_c=R-j,                   (3.3)
```

where `Q_c` locates the agreement points discarded after the first `a` were
selected.  The roots of `Q_c` are **agreements**.  They do not support the
one-point escapes of an exact error locator.  Only at `j=R` is `Q_c=1`.

This is the load-bearing compatibility wall:

```text
canonical global rank-two Popov row
        -- UNPAID_PADDING_BRIDGE -->
actual-error high-rank layer row.                           (3.4)
```

No result below identifies those syzygy modules at an interior weight.

## 4. A variable-weight integer mean-overlap cap

Fix

```text
J_0=614,160,              s=n-J_0=1,482,992.                (4.1)
```

For every codeword of error weight at most `J_0`, choose the first `s`
agreement points, using the same domain order as in Section 2.  Because
`s>a`, the first-`a` selector is nested inside this one.

For distinct codewords `c_i,c_k`, their agreement sets intersect in at most
`K-1`: on the intersection the two degree-`<K` polynomials are equal.  The
same is true of their selected `s`-subsets.

Suppose there are `M` selected sets.  Let `r_x` be the number containing
`x`.  Then

```text
sum_x binomial(r_x,2) <= binomial(M,2)(K-1).                (4.2)
```

If `Ms=qn+rho`, integer convexity gives the exact lower bound

```text
sum_x binomial(r_x,2)
 >= n binomial(q,2)+rho q.                                  (4.3)
```

For `M=3,731`,

```text
(q,rho)=(2,638,756,176),
lower  =7,296,315,170,144,
upper  =7,296,315,151,125,
gap    =               19,019.                              (4.4)
```

Thus the **total list mass over every variable weight `j<=J_0`** is at most

```text
3,730.                                                       (4.5)
```

The integer balancing is load-bearing.  Plain real Cauchy gives only `3,732`.
At `M=3,730`, the integer inequality remains feasible by `202,311`; this is an
upper-bound certificate, not an existence construction.

The verifier exhausts every relevant cutoff `K/2<=J<R` for which

```text
(n-J)^2>n(K-1).                                              (4.6)
```

There are `89,955` such rows, ending at `J=614,242`.  Lower cutoffs have cap
at most one and strictly more remaining layers, so cannot improve the
baseline-45 objective.  Among flat baselines,
`45` is the largest one that can force an excess, and `J_0=614,160` uniquely
maximizes its exact remaining mass.  Baseline `46` has negative margin, so
rank 47 is not forced by this incidence method.

## 5. Exact occupancy ledger and 259,881 rank-46 keys

For `j>J_0`, let `M_j` be the exact number of listed codewords of error weight
`j`, and put

```text
H_r=#{j in [J_0+1,R]:M_j>=r},
T_46=sum_(r>=46) H_r=sum_j max(M_j-45,0).                   (5.1)
```

There are

```text
H=R-J_0=366,969                                             (5.2)
```

high layers.  Write `N_low=sum_(j<=J_0)M_j` for the actual low-weight mass and
let

```text
C_low=3,730-N_low,
C_r=H-H_r       (1<=r<=45).                                (5.3)
```

These are genuine unused-capacity credits.  Layer cake gives the exact
identity

```text
|L_R(y)|
 =3,730+45H+[T_46-C_low-sum_(r=1)^45 C_r]
 =16,517,335+Xi_46.                                        (5.4)
```

Therefore

```text
|L_R(y)|<=B*  <=>  Xi_46<=259,880,                         (5.5)
|L_R(y)|>=L   <=>  Xi_46>=259,881.                         (5.6)
```

This signed occupancy functional is the mass-preserving object.  Bounding
`T_46` while forgetting the credits is sufficient but not equivalent.

In every high layer, order the exact error supports and retain the first 45
as anchors.  Each remaining support gives the source key

```text
(j, ordered 45-anchor tuple, distinguished extra support). (5.7)
```

The keys are distinct, and their number is exactly `T_46`.  Thus every
forbidden list forces at least

```text
259,881 marked rank-46 actual-error packets.                (5.8)
```

The arithmetic relaxation is sharp.  Put `3,730` objects at weight `J_0`, put
45 objects in every higher layer, and add one object on each weight

```text
721,249,...,981,129.                                        (5.9)
```

This has total `L`, maximum layer size 46, satisfies every global prefix cap
from Section 4, and satisfies the same-weight mean-overlap inequalities.  It
is **not** claimed to be realized by Reed--Solomon codewords.  It proves only
that rank 47 needs new source structure.

## 6. Uniform rank-three Forney frame

Fix one marked packet in a layer of weight `j`.  Let `C_0` be the intersection
of its 46 error supports, `c=|C_0|`, and divide that common locator from all
columns.  In the notation of PR #1007,

```text
D=K-j,
e=j-c,
S=e-D-1=2j-K-c-1.                                         (6.1)
```

Let

```text
mu_1<=...<=mu_45                                           (6.2)
```

be the Forney indices of the primitive 46-column locator row.  The inherited
non-surjectivity theorem gives

```text
sum_(i=1)^44 mu_i <= S <= 2R-K-1=913,681.                  (6.3)
```

For `n_0=44`, write `S=n_0 q+r`.  The exact maximum of the first `k` entries
of a nondecreasing nonnegative sequence with total at most `S` is

```text
P_k(S,n_0)=kq+max(0,r-(n_0-k)).                            (6.4)
```

At the deployed worst case this gives

```text
mu_1                         <=20,765,
mu_1+mu_2                    <=41,530,
mu_1+mu_2+mu_3               <=62,295 <67,447,
mu_1+mu_2+mu_3+mu_4          <=83,060 >67,447.             (6.5)
```

Thus rank three is the largest rank certified uniformly below the cutoff by
the inherited aggregate-index bound.  The inequality for four rows only says
that this bound cannot certify rank four; it is not a counterexample to a
stronger rank-four theorem.
At most `floor(913681/67447)=13` of the first 44 indices can reach the cutoff;
including the exceptional last index, at least 31 of the 45 lie below it.

### Lemma 6.1 (Pluecker/common-core divisibility)

Let the first `r` minimal syzygy rows form an `r x 46` polynomial matrix.  For
an `r`-subset `I` of columns, let `Delta_I` be its minor.  Then

```text
gcd(P_k:k notin I) divides Delta_I.                         (6.6)
```

**Proof.**  Let `alpha` be a root common to the complementary locators.  The
reduced locator row is primitive, so at least one locator in `I` is nonzero at
`alpha`.  Reducing every syzygy equation modulo `X-alpha` leaves a nonzero
vector supported on `I` in the kernel of the `I`-minor matrix.  Hence that
minor vanishes at `alpha`.  The locators are split and squarefree, so every
root of the complementary gcd occurs with multiplicity one and the entire gcd
divides the minor. `QED`

### Corollary 6.2 (rank-three/coloop dichotomy)

Distinguish the extra support in (5.7) and inspect the column matroid of the
first three syzygy rows.

- If deletion of the extra column preserves rank three, choose a basis triple
  among the old 45 columns.  Its complementary 43-support subfamily contains
  the distinguished extra support.  By (6.6), its common core beyond `C_0`
  has degree at most `62,295`.
- If deletion lowers the rank, the extra column is a coloop and the old 45
  columns have rank at most two.

These are exactly

```text
UNPAID_COMMON_CORE_ADD_BACK
UNPAID_RANK2_COLOOP.                                        (6.7)
```

No existing owner is assigned without its semantic hypotheses and exact
charge/refund.

## 7. Why independent root unions still cannot close

Grant a much stronger local conclusion than has been proved: suppose an
entire layer injected into roots of one nonzero low Pluecker minor.  The
rank-two and rank-three degree caps would be `41,530` and `62,295`, while the
sharp arithmetic extremizer of Section 5 has every layer of size at most 46.
It survives either local bound with enormous room.

Against the exact signed allowance `259,880`, at most

```text
6 rank-two keys:   6*41,530=249,180, residual 10,700,
4 rank-three keys: 4*62,295=249,180, residual 10,700         (7.1)
```

can be charged independently; the seventh or fifth respectively exceeds the
allowance.  A polynomial chosen separately in each of hundreds of thousands
of source keys is therefore numerically irrelevant.  Closure needs one of:

1. cross-layer/source-key deduplication to at most the counts in (7.1);
2. a named semantic first-match owner with exact disjoint charge and refund;
3. elimination of the primitive component; or
4. a stronger source theorem that defeats the arithmetic extremizer.

## 8. Compatibility with upstream #1005

PR #1005 proves that the rooted-shell inequality

```text
p^w max(d_e(A)-3,0) <= 7 H_e                              (8.1)
```

would place its M31 Q family below budget, but leaves only `80,429` reserve.
It also gives the exact `F_241` support-only counterexample

```text
58,081(10-3)=406,567 > 308,700=7*44,100.                   (8.2)
```

Therefore “periodic-looking,” “trivial stabilizer,” “empty support core,” or
other support-only labels cannot pay a rank-46 packet.  A valid combined
compiler must retain the received word/line, explanation, first-match
projector, natural source key, owner charge, and refund.  The `F_241` orbit is
a mandatory negative regression and terminates at
`REQUIRES_SEMANTIC_FIRST_MATCH` unless those data are actually supplied.

The exact proposed order is:

```text
ZERO_SYNDROME
NEAR_RATIONAL_SINGLETON
NAMED_EXISTING_OWNER_WITH_EXACT_CHARGE_AND_REFUND
CANONICAL_MASKED_SPLIT_PENCIL
UNPAID_PADDING_BRIDGE
UNPAID_COMMON_CORE_ADD_BACK
UNPAID_RANK2_COLOOP.                                       (8.3)
```

## 9. Literature and tool audit

TheoremSearch located the standard predictable-degree theorem for shifted
reduced polynomial matrices, but no theorem matching the semantic padding or
owner/refund problem.  An independent outside search found the relevant
algorithmic normal-form literature:

- [Jeannerod--Neiger--Villard, *Fast computation of approximant bases in
  canonical form*](https://arxiv.org/abs/1801.04553);
- [Jeannerod--Neiger--Schost--Villard, *Fast Computation of Minimal
  Interpolation Bases in Popov Form for Arbitrary
  Shifts*](https://arxiv.org/abs/1602.00651);
- [Beckermann--Labahn--Villard, *Normal forms for general polynomial
  matrices*](https://doi.org/10.1016/j.jsc.2006.02.001).

These sources support the polynomial-matrix normal form and predictable-degree
machinery.  They do not supply the project-specific canonical exactness mask,
interior padding-factor bridge, first-match owner classification, or finite
M31 charge ledger.  No novelty is claimed for standard Popov reduction or the
classical integer mean-overlap argument.

Tool allocation after this packet is now precise:

- Python big integers: occupancy/credit ledger, source-key deduplication, and
  exact owner/refund arithmetic;
- Sage 10.9: canonical padded/error factor pairs, shifted-Popov bases, and
  rank-three/coloop finite-field controls;
- Singular/Macaulay2/Oscar: only after one fixed primitive padding or coloop
  incidence component is written down;
- TheoremSearch plus outside primary-source search: only for that frozen
  component;
- Lean: not during discovery.  The current obstacle is theorem discovery and
  semantic typing, not arithmetic formalization.

## 10. Replay

```bash
python3 experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --check
python3 -O experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --check
python3 experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_canonical_popov_rank46_compiler.sage
git diff --check
```

The Python verifier scans every relevant finite mean-overlap cutoff from
`K/2` through the exact first-failure boundary (the smaller cutoffs have the
separately proved cap at most one), regenerates the
occupancy and arithmetic-extremizer certificates, checks the rank-46 degree
bounds, and rejects hostile mutations.  The Sage replay independently checks
the lattice selector/padding factorization and rank-three Pluecker divisibility
on exact finite fields.  Toy checks are controls, not deployed enumerations.

## 11. Nonclaims

- The M31 list row is not closed.
- The arithmetic extremizer is not claimed source-realized.
- A rank-47 layer is not proved impossible; it is merely not forced by the
  current incidence hypotheses.
- The rank-46 local frame is not identified with the global rank-two Popov
  basis at an interior weight.
- Padding points are not errors and do not carry one-point escapes.
- Neither the noncoloop common-core branch nor the coloop branch is paid.
- The support-only `F_241` counterexample is not assigned an owner.
- No `U_Q`, `U_A`, list-interior, boundary, whole-ball, or completion atom is
  banked.
- No stable-paper TeX, Lean theorem, official rate, or prize claim is changed.

The exact next proof object is no longer “find a low minor.”  It is a semantic
padding/owner theorem on the 259,881 marked rank-46 source keys, carrying the
occupancy credits of (5.4) from source through terminal.
