# M31 exact-syzygy coloop elimination and locator-only route cut

## Status

**CONSUMES PROVED PADDED RANK-THREE FRAME FROM PR #1021 / INDEPENDENT DIRECT
COMMON-SYNDROME CROSS-CHECK / RANK-TWO COLOOP TERMINAL ELIMINATED / PROVED
CANONICAL PLUECKER ROUTE / SHARP LOCATOR-ONLY ROUTE CUT / M31 LIST ROW OPEN /
LEDGER MOVEMENT ZERO.**

This packet is designed to stack on live PR #1021.  At head
`8a6316f4969eca577825d2504d0ec7d0239b3cb4` it independently derives the same
`62,295` numerical cap through the diagonal-saturation exact sequence,
minimal-index monotonicity, and an actual-error exceptional-index lemma.  The
integrated rank-46 source compiler from PR #1008 supplies the marked source
keys.  PR #1014 at `c7cbcf1cff1180b4aac0862ae3c3e665f6b29b21` supplies
counterpacket provenance; its finite data are restated here, not imported as
an ancestry dependency.

The `62,295` numerical conclusion is consumed overlap, not novelty here.  The
nonduplicate delta is:

1. a direct common-syndrome proof inside the canonical padded module, requiring
   no actual-error row transport or saturation monotonicity;
2. elimination of #1021's still-open rank-two-coloop branch; and
3. the exact M31-scale empty-core support counterfamily and the resulting
   locator--numerator escape floor.

PR #1021's padded frame, independently cross-checked in Sections 2--3, works
uniformly for all `259,881` marked source keys forced by a forbidden M31 list.
It preserves the ordered first-agreement selector, received word, every
actual error/padding mask, distinguished extra column, and signed occupancy
credit.  Thus the algebraic rank-three branch of

```text
UNPAID_MASKED_DIAGONAL_SATURATION
```

is already supplied by the dependency; this packet independently confirms it
without transport.  The new exact-syzygy theorem proves that the earlier
rank-two-coloop branch cannot occur.  It does **not** close the M31
row.  A sharp support-only counterfamily shows that even empty complementary
cores do not pay; the surviving terminal is a simultaneous canonical
locator--numerator escape theorem or typed semantic owner/refund.

## 1. Deployed source contract

The parameters are

```text
p       = 2^31-1          = 2,147,483,647,
n       = 2^21            = 2,097,152,
K       = 2^20            = 1,048,576,
a       = 1,116,023,
w       = a-K             = 67,447,
R       = n-a             = 981,129,
B*      = 16,777,215,
L       = B*+1            = 16,777,216.
```

For every listed codeword `c_i`, let `T_i` be its first `a` agreement points
in the fixed ordered domain and put

```text
W_i = Lambda_(D\T_i).
```

Every `W_i` is monic, split, squarefree, and has degree `R`.  A marked source
key is one exact-weight packet

```text
(j, ordered 45-anchor tuple, distinguished extra codeword),
```

so it has 46 such locators.  The exact signed occupancy identity in the source
compiler forces at least `259,881` distinct marked keys under the forbidden
list hypothesis.  Nothing below selects a subfamily of those keys or drops a
negative capacity credit.

## 2. Equal-degree primitive-row identity

The following standard Forney identity is the only polynomial-module input.
It is reproved because its application to the padded row is load-bearing.

### Lemma 2.1 (primitive equal-degree row)

Let `F` be a field and let

```text
P=(P_1,...,P_t) in F[X]^t
```

be primitive, with every `P_i` monic of the same degree `e`.  If

```text
lambda_1 <= ... <= lambda_(t-1)
```

are the vector degrees of a row-reduced basis of `Syz(P)`, then

```text
sum_(r=1)^(t-1) lambda_r = e.                            (2.1)
```

**Proof.**  For `D>=0`, consider

```text
Theta_D : direct_sum_i F[X]_<D -> F[X]_<e+D,
Theta_D((A_i))=sum_i P_i A_i.                            (2.2)
```

The predictable-degree property gives

```text
dim ker Theta_D=sum_r max(0,D-lambda_r).                 (2.3)
```

For all sufficiently large `D`, `Theta_D` is onto.  Indeed, divide a target
by monic `P_1`; the quotient has degree `<D`, and the remainder has degree
`<e`.  Since `gcd(P_1,...,P_t)=1`, fixed Bezout representations of
`1,X,...,X^(e-1)` handle every remainder once `D` exceeds the finitely many
coefficient degrees in those representations.  Hence, for large `D`,

```text
dim ker Theta_D=tD-(e+D)=(t-1)D-e.                       (2.4)
```

Comparing (2.3) and (2.4) proves (2.1). `QED`

This is the same identity proved in
`experimental/notes/l2/rank16_left_kernel_forney_route_cut.md`, equations
(17)--(20).  No diagonal-saturation assertion is used.

### Lemma 2.2 (common received-word defect)

Suppose now that `T_1,...,T_t` are pairwise distinct size-`a=K+w` selected
agreement supports of pairwise distinct degree-`<K` polynomials `c_i` against
one received word `y`.  Put

```text
U=union_i T_i,
E_i=Lambda_(U\T_i),
e=|U|-a.
```

For the ordered Forney indices of `(E_i)`, one has

```text
sum_i max(0,lambda_i-w) >= 1.                             (2.5)
```

**Proof.**  Let `V_U=RS(U,K)^perp` and let `Z_i` be its shortening to `T_i`.
The functional

```text
phi_y(z)=sum_(x in U)y(x)z_x
```

annihilates every `Z_i`, because `y=c_i` on `T_i`.  It is nonzero on `V_U`.
Otherwise `y|U` would be the evaluation of one polynomial `Q` of degree
`<K`; then `Q=c_i` on the `a>=K` points of `T_i` for every `i`, contradicting
the distinctness of the `c_i`.  Hence the quotient defect

```text
h=dim V_U-dim(sum_i Z_i)
```

is at least one.

At truncation degree `D=w`, the usual Lagrange-dual identification sends the
sum of the `Z_i` to the image of the Macaulay map `Theta_w` in (2.2).  Thus

```text
h=(e+w)-rank Theta_w.
```

Using (2.1), (2.3), and `rank Theta_w=tw-dim ker Theta_w` gives the exact
identity

```text
h=sum_i max(0,lambda_i-w).                                (2.6)
```

Therefore (2.5) follows. `QED`

This is the selected-union common-syndrome theorem in
`rank16_left_kernel_forney_route_cut.md`, equations (8) and (19), specialized
to the canonical selected supports.  Its common-received-word premise is
load-bearing.

There is an equivalent direct interpolation-lattice proof of the only
consequence needed below.  Write `G=Lambda_(D\U)` and `M_i=E_i c_i`.  For a syzygy row `A` of
degree at most `w`, the canonical lattice combination has first coordinate
zero:

```text
sum_i A_i (G E_i,G M_i)=(0,G sum_i A_i M_i).
```

The second coordinate must vanish on all of `D`, so `Lambda_D/G` divides
`sum_i A_iM_i`.  But

```text
deg sum_i A_iM_i <= e+K-1+w < deg(Lambda_D/G)=e+a,
```

and hence that sum is zero.  If every Forney basis row had degree at most
`w`, all of them would annihilate `(M_i)`.  Over `F_p(X)`, the annihilator of
`Syz(E_i)` is the line spanned by `(E_i)`, forcing `M_i=fE_i` and therefore
all `c_i=f`, a contradiction.  Thus some index is at least `w+1`, agreeing
with (2.5).  This second proof keeps the full canonical lattice pair visible.

## 3. Direct canonical-padded frame

Fix one marked 46-column packet and set

```text
G=gcd(W_1,...,W_46),
P_i=W_i/G,
e=R-deg G.                                                (3.1)
```

Every `P_i` is monic of degree `e`, the row `(P_i)` is primitive, and

```text
Syz(W_1,...,W_46)=Syz(P_1,...,P_46).                      (3.2)
```

Equation (3.2) follows by cancelling the nonzero common factor `G` in the
integral domain `F_p[X]`.  It is an equality of the actual canonical padded
syzygy modules; it is not a map from the actual-error module.

There is also an order-sensitive refinement.  If column `i` has stopping
pivot `h_i=a+r_i`, then `r_i<=j` and `W_i` contains the complete suffix after
`h_i`.  Thus the complete suffix after `max_i h_i` divides `G`, giving

```text
deg G >= n-max_i h_i >= R-j,
e <= j <= R.                                              (3.3)
```

The proof retains the canonical order rather than averaging it away.

Let

```text
lambda_1<=...<=lambda_45
```

be the Forney indices of the common module in (3.2).  Lemma 2.1 gives

```text
sum_(r=1)^45 lambda_r=e<=R=981,129.                       (3.4)
```

Lemma 2.2 gives `lambda_45>=w+1=67,448`.  Consequently

```text
sum_(r=1)^44 lambda_r
  <= R-(w+1)
  =913,681.                                               (3.5)
```

For a nondecreasing nonnegative sequence of length `m` and total at most
`S`, write `S=mq+r`, `0<=r<m`.  Its largest possible first-`k` sum is

```text
P_k(S,m)=kq+max(0,r-(m-k)).                               (3.6)
```

Indeed, if the `k`-th entry is at most `q`, the first `k` sum is at most
`kq`; otherwise all final `m-k` entries are at least `q+1`, leaving at most
`kq+r-(m-k)` for the first `k`.  Balanced sequences attain the two cases.

At `(S,m)=(913,681,44)` one has

```text
913,681=44*20,765+21
```

and therefore

```text
lambda_1                         <=20,765,
lambda_1+lambda_2                <=41,530,
lambda_1+lambda_2+lambda_3       <=62,295 <67,447,
lambda_1+...+lambda_4            <=83,060 >67,447.        (3.7)
```

So every marked key has three canonical padded syzygy rows whose combined
degree is at most `62,295`, with exact margin

```text
67,447-62,295=5,152.                                     (3.8)
```

At most `floor(913,681/67,447)=13` of the first 44 indices can reach the
cutoff, so at least 31 of all 45 are strictly below it.  The four-row
inequality in (3.7) is a route cut for this aggregate bound, not a
counterexample to a stronger rank-four theorem.

The packet width is also sharp for this total-sum-plus-syndrome argument.  For
`t` columns there are `t-2` indices left after reserving one index at least
`w+1`.  With 43 columns,

```text
P_3(913,681,41)=66,852<67,447,
```

whereas 42 columns give

```text
P_3(913,681,40)=68,526>67,447.                            (3.9)
```

Thus 43 is the smallest column count for which the present two inputs certify
rank three.  The deployed packet has 46 columns, including the distinguished
extra source object.

### Why this bypasses PR #1014

The padding audit proves that

```text
Syz(P_i Q_i)
  ~= {A in Syz(P_i):Q_i divides A_i for every i},
```

so low actual-error rows need not transport.  The rows in (3.7) are instead
constructed as a minimal basis of `Syz(W_1,...,W_46)` itself.  No actual-error
row is named, no coordinate is divided by a padding factor, and no equality
between the actual-error and padded Forney profiles is asserted.  The audit's
`F_11` counterpacket is respected: its two canonical orders have direct padded
pair indices 2 and 3, exactly as the gcd-reduced equal-degree identity says.

This proves the direct-construction alternative in item 4 of the successor
contract in PR #1014 for every marked rank-46 key.

## 4. Canonical Pluecker route and elimination of the coloop branch

Let the first three padded minimal rows form a `3 x 46` polynomial matrix
`B`.  It has row rank three over `F_p(X)`.  For a three-subset `I` of columns,
write `Delta_I=det B_I`.

### Lemma 4.1 (complementary reduced-core divisibility)

For every `I`,

```text
gcd(P_k:k notin I) divides Delta_I.                       (4.1)
```

**Proof.**  Let `alpha` be a root common to all complementary `P_k`.  Since
the full row `(P_i)` is primitive, some `P_i(alpha)` with `i in I` is nonzero.
Evaluating the three syzygy equations at `alpha` gives a nonzero vector
supported on `I` in the kernel of `B_I(alpha)`.  Hence
`Delta_I(alpha)=0`.  Every `P_i` is split and squarefree, so their gcd is
squarefree and all of it divides `Delta_I`. `QED`

### Lemma 4.2 (single-column deletion preserves syzygy rank)

Let `L` be any subspace of the syzygy space of a polynomial row
`P=(P_1,...,P_t)` with every `P_i` nonzero.  Over `F_p(X)`, deleting any one
coordinate is injective on `L`.

**Proof.**  A vector in the kernel of deletion is supported on the deleted
coordinate `i`.  Its syzygy equation is `P_i A_i=0`.  Since `F_p(X)` is a
field and `P_i` is nonzero, `A_i=0`. `QED`

Apply Lemma 4.2 to the rank-three row space of `B` and delete the distinguished
extra column.  Rank three always survives.  Hence a basis triple `I` can be
chosen among the 45 anchors; there is no rank-two-coloop branch.  The
complementary 43-column family contains the extra column, and its common root
set after the global gcd `G` is

```text
C_I=U\union_(k notin I)T_k.                               (4.2)
```

By Lemma 4.1,

```text
|C_I|<=deg Delta_I<=62,295.                               (4.3)
```

The sole fail-closed terminal is

```text
UNPAID_CANONICAL_COMMON_CORE_OWNER_REFUND.                (4.4)
```

In particular, the abstract coloop matrix used as a control in the earlier
rank-46 Sage packet is not realizable as a syzygy matrix with a nonzero
distinguished locator: its last coordinate would force that locator to be
zero.  The old fixture checked an abstract matroid alternative, not the exact
syzygy equations.

The quotient by `G` in the proof of (3.4) does not delete any source object or
change its signed occupancy credit; the same rows are syzygies of the full
`W_i`.  But (4.1) controls only the complementary core beyond the packet-wide
`G`.  A global counting argument must therefore retain `G`, the canonical
root-status masks, and the received-line explanation data.  Treating `G` as a
free semantic deletion would recreate the add-back gap under a new name.

## 5. Sharp failures of locator-only payment

### 5.1 Independent root unions

The exact signed allowance is

```text
259,880.
```

Even grant the optimistic statement that a whole marked key injects into the
roots of one nonzero rank-three minor of degree `62,295`.  Independent minors
pay at most

```text
4*62,295=249,180,      residual 10,700,
5*62,295=311,475>259,880 by 51,595.                       (5.1)
```

Thus a separately chosen polynomial in each of `259,881` source keys is not a
global charge.  The sharp arithmetic extremizer from the source compiler has
only 46 objects in each occupied layer, so it also survives every such local
degree cap.

After the direct frame theorem, a closing result must do at least one of the
following on the **same signed source-key ledger**:

1. deduplicate all keys into a global root resource of total size at most
   `259,880` (equivalently, at most four independent worst-case
   degree-`62,295` resources plus a residual payment);
2. construct a fixed first-match semantic owner carrying the complete
   received-line -> witness -> codeword -> ray -> distinct-slope chain and an
   exact charge/refund;
3. eliminate the compatible primitive canonical common-core component; or
4. prove a stronger source theorem that rules out the signed occupancy
   extremizer.

This already rules out independent local minors.  The next subsection
sharpens it further by showing that even a uniformly empty relative core does
not supply a locator-only payment.

### 5.2 Exact M31-scale empty-core support counterfamily

There is a stronger route cut.  It shows that even an empty complementary
core in every possible basis chart is not a support-only payment.

Partition the M31 domain abstractly as

```text
D=F disjoint_union V disjoint_union B_0 disjoint_union ... disjoint_union B_31,
|F|=9,       |V|=4,087,       |B_i|=65,408.               (5.2)
```

The sizes sum to `2,097,152`.  Let `Z` be the family of 15-subsets
`S subset Z/32Z` with `sum S=0`.  Translation by `t` changes the subset sum by
`15t`; since 15 is a unit modulo 32, every translation orbit contains one
subset of each color.  The action is free for the same reason.  Hence

```text
|Z|=binomial(32,15)/32=17,678,835.                        (5.3)
```

Choose distinct `S_r in Z`.  With fixed labels `F={f_0,...,f_8}` and
`V={v_0,...,v_4086}`, define the degree-`R` root set

```text
W_r=(F\{f_(r mod 9)})
      union {v_(r mod 4087)}
      union union_(i in S_r) B_i,                         (5.4)
T_r=D\W_r.
```

Then

```text
|W_r|=8+1+15*65,408=981,129=R,
|T_r|=1,116,023=a.                                       (5.5)
```

Two different members of `Z` meet in at most 13 block labels.  Indeed, an
intersection of size 14 would make them differ by one swap, while equality of
their sums modulo 32 would force the removed and inserted labels to be equal.
Therefore

```text
|W_r intersect W_s| <=13*65,408+8+1=850,313,
|T_r intersect T_s| <=n-2R+850,313=985,207<K-1            (5.6)
```

with margin `63,368`.  Thus the family violates no pairwise MDS agreement
condition.

The certificate pins 45 explicit zero-sum anchor rows.  Their block
occurrences lie between 20 and 22.  It exhausts all
`binomial(45,3)=14,190` deleted anchor triples.  After any deletion:

* no block can remain in all 42 anchors, because every block is absent from at
  least 23 of the original anchors;
* no `f_i` can remain in all 42, because exactly five of the first 45 tags omit
  it and deleting three leaves at least two omissions; and
* no `v_i` can remain in all 42, because the first 45 `V`-tags are distinct.

Consequently the remaining 42 anchor locators have empty intersection.  After
adding any distinguished extra, the complementary 43-locator gcd is still
one for **every** possible anchor basis triple, not merely for the triple
eventually selected by a Forney basis.  The 45-anchor gcd is itself one.  Each
46-packet therefore has the coarse direct padded bound

```text
P_3(R,45)=65,406<w                                       (5.7)
```

from Lemma 2.1, no coloop, and an empty relative common core in every chart.

Order these anchors first, then any other members of `Z`, and retain exactly
`L=16,777,216` supports in the boundary layer.  Consecutive tags cover all of
`V`; the anchors both use and omit every block and fixed point.  Hence the
global locator gcd and global selected-agreement core are both empty.  The
signed occupancy values are nevertheless

```text
T_46=L-45                         =16,777,171,
C_low                              =3,730,
sum_(r=1)^45 C_r=45*366,968       =16,513,560,
Xi_46=T_46-C_low-sum_r C_r        =259,881.               (5.8)
```

This is an exact support design, not a common-received-word Reed--Solomon
list.  It does not refute Lemma 2.2 and is not a counterexample to the M31
theorem.  It rigorously refutes the locator-only implication

```text
canonical-size boundary masks + pairwise MDS overlap + low padded Forney/Pluecker
  + no coloop + empty complementary gcd
  ==> paid add-back.                                     (5.9)
```

The active terminal is therefore sharpened from the support-only phrase in
(4.4) to

```text
UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND.  (5.10)
```

A closing theorem must use the simultaneous canonical pairs
`(W_i,N_i=W_i c_i)`, their common received-word equations, and all one-point
escapes, or construct a typed semantic owner with an exact global refund.  In
the signed ledger its output must satisfy

```text
sum_owner U_owner + |R_residual|
  <=259,880+C_low+sum_(r=1)^45 C_r.                       (5.11)
```

More `W`-only gcd, Pluecker, quotient-symmetry, or support-stabilizer algebra
cannot establish (5.11) from the current hypotheses.

## 6. Replay and proof boundary

```bash
python3 experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --check
python3 -O experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --check
python3 experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.sage
git diff --check
```

The Python certificate exhausts every allowed small-index total, pins the
exact prefix optimizer, the common-syndrome exceptional index, the smallest
packet width certified by both inputs, all deployed margins, the signed
source-key preservation contract, and the independent-root-union route cut.
It also independently counts the 32 zero-sum colors, checks the explicit
45-anchor table, exhausts all 14,190 triple deletions, and replays the
empty-core signed occupancy counterfamily.  It is stdlib-only, hash-bound,
and mutation tested.

The Sage replay recovers a complete Forney profile from exact truncated
Macaulay kernels for a split equal-degree locator row, constructs three low
syzygies, and checks all complementary-gcd/Pluecker divisibilities.  It also
replays both orders of the `F_11` padding counterpacket.  These finite-field
calculations are exact controls, not a deployed M31 enumeration.  Lemmas 2.1
through 4.2 and the explicit construction in Section 5 are the proof.

## 7. Nonclaims

* The M31 list/MCA row is not closed and no completion atom moves.
* No actual-error Forney row is transported through padding.
* No packet-wide common root is silently deleted from semantic data.
* No support-only quotient, periodicity, empty-core, or rank-two label is
  declared a paid owner.
* No cross-key injectivity or slope deduplication is inferred from a local
  minor.
* The empty-core support family is not claimed to be a same-received-word RS
  list, to survive a deployed C1--C8 semantic owner, or to lack every
  algebraic quotient symmetry.
* The arithmetic extremizer is not claimed to be source-realized.
* `U_Q`, `U_A`, list-interior, boundary, and whole-ball atoms remain open.
* No stable-paper TeX, Lean theorem, official rate, or prize claim changes.
