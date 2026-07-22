---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Scalar descent followed by prime-field fresh-symbol boundary forcing reduces every live quartic violation to a boundary-anchor divisor/gcd census with all polynomial data in F_p. The resulting census admits sharp fixed-locator, pairwise-Wronskian, whole-list second-moment, base-field-scalarization, V=1 nonextremality, restricted support-packing, and Singleton route cuts. Every forbidden list retains at least 15775933 shallow pairs in the full common-V census. The locators are not proved distinct. Closure now requires a split-flat coefficient-incidence theorem uniform across the possible G and H locators while retaining their common arbitrary base-field unit V.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: Direct diagnostic of the boundary-anchor census left by M31_ALL_WEIGHT_ANCHOR_EXCHANGE_PADE_BIJECTION_V1; no v4 atom value and no signed-Xi payment.
quantifier: The combinatorial route cuts hold for every quartic boundary-anchor triple (A0,L0,V). For row closure it is sufficient, and by scalar descent plus prime-field boundary forcing equivalent, to prove the census bound for boundary triples with all data in F_p and V an arbitrary base-field unit modulo L0. The restricted support countermodel uses the literal deployed T2/T4 Chebyshev fibre tower but deliberately does not assert polynomial or common-V realizability.
projection_and_unit: Distinct nonanchor codewords per received word, represented canonically by pairs (G,b) relative to one boundary anchor. Abstract supports occur only in the stated interface countermodel and are never counted as codewords.
claimed_bound: Exact route cuts and residual localization only. The row-closing bound #X(V)<=16777214 remains unproved; ledger movement is zero.
status: PROVED EXACT ROUTE CUTS / SHALLOW COMMON-V FULL-LOCATOR RESIDUAL OPEN / ROW OPEN
impact: ROUTE_CUT / RESIDUAL_LOCALIZATION
falsifier: An error in any printed integer endpoint; a distinct fixed-G pair violating the Johnson cap; a zero Wronskian for distinct canonical pairs; a forbidden list with more than 1001282 companions of excess at least 366887; or a claimed closure derived only from the restricted support data refuted in Section 7.
replay: Two independent exact Python implementations, proof-critical mutations, source hashes, predecessor replay, and fresh independent proof review.
---

# M31 boundary common-V, full-locator route cut

## Status

The following statements are proved in this packet.

- The fixed-G Johnson bound and every displayed deployed endpoint.
- The nonzero cross-pair Wronskian and its root budget.
- The split-support global moment and its exact feasible-region gate.
- At most 1,001,282 nonanchor companions have excess at least 366,887.
- Every forbidden boundary list retains at least 15,775,933 shallow
  companions with excess from 0 through 366,886.
- Scalar descent and fresh-symbol boundary forcing compose over F_p, so a
  live counterexample would yield a boundary triple with all polynomial data
  in F_p and an arbitrary base-field unit V.
- The base-field evaluation condition has exact worst-case codimension
  3(m-w), not 3m.
- The V=1 slice is exactly a depth-w locator-prefix fiber, but an exhaustive
  F_7 control proves that arbitrary V can give a strictly larger census.
- Support size, one fixed exchange degree, pairwise MDS intersections, and
  the counts of complete T2 and T4 fibres do not imply the list bound.

The following statement is not proved.

- A coefficient-incidence bound for the full locator census coupled through
  one arbitrary base-field unit V.

The M31 row remains open. This packet moves no v4 ledger atom and changes no
official endpoint.

The packet tests the strongest consequences obtained here from one fixed
locator, two codewords, or the enumerated support data. It does not claim to
exclude every possible fixed-G theorem or every possible support owner. Its
purpose is to identify exactly which current interfaces fail and what
additional shared algebraic information must enter.

## 1. Exact boundary coordinate

Use the exact bijection in
experimental/notes/thresholds/m31_all_weight_anchor_exchange_pade_bijection_v1.md.
At a boundary anchor,

$$
|S_0| = a = 1,116,023,
|E_0| = R = 981,129,
w = a-K = 67,447.
$$

The remaining census consists of pairs satisfying

$$
G divides A_0,
m = deg(G),
w+1 <= m <= R,
$$

$$
b != 0,
deg(b) < m-w,
gcd(b,G) = 1,
$$

$$
H = gcd(L_0,G-bV),
h = deg(H) >= m.
$$

Every locator and gcd is monic. Put

$$
s = h-m >= 0.
$$

The companion has agreement $a+s$, error weight $R-s$, and exact agreement
support

$$
T = (S_0 minus Z(G)) disjoint-union Z(H).
$$

For distinct companions i and j, their difference is a nonzero polynomial
of degree less than K. Therefore

$$
|T_i intersection T_j| <= K-1.
$$

Expanding the two support pieces gives

$$
|Z(G_i) intersection Z(G_j)|
+ |Z(H_i) intersection Z(H_j)|
<= m_i+m_j-w-1.                                      (1.1)
$$

Equation (1.1) is necessary. It does not retain the common polynomial V and
is not sufficient for polynomial or received-word realizability.

## 2. Fixed-locator Johnson theorem

### Theorem 2.1

Fix one monic divisor G of A_0 of degree m. Let $N_G(>=s)$ be the number of
admitted b values whose H has degree at least $m+s$. If

$$
Delta_G(m,s) = (m+s)^2 - R(m-w-1) > 0,               (2.1)
$$

then

$$
N_G(>=s)
<= floor( R(w+s+1) / Delta_G(m,s) ).                 (2.2)
$$

### Proof

For each admitted pair choose an arbitrary $(m+s)$-subset of Z(H). For
fixed G, (1.1) says that two such subsets intersect in at most

$$
lambda = m-w-1
$$

points. If N subsets of common size $r=m+s$ lie in an R-point universe, and
$d_x$ is the number containing x, then

$$
N^2 r^2 / R
<= sum_x d_x^2
= Nr + 2 sum_x C(d_x,2)
<= Nr + N(N-1)lambda.
$$

Thus

$$
N(r^2-R lambda) <= R(r-lambda).
$$

Substitution gives (2.2). This is an exact finite incidence second moment;
there is no probabilistic estimate.

### Corollary 2.2: deployed endpoints

At s=0, the denominator in (2.2) is positive exactly on

$$
67,448 <= m <= 72,858
$$

or

$$
908,271 <= m <= 981,129.                              (2.3)
$$

The cap is at most 3,730 exactly on the following endpoint subintervals of
those wings:

$$
67,448 <= m <= 72,837
$$

or

$$
908,292 <= m <= 981,129.                              (2.4)
$$

At the adjacent values m=72,838 and m=908,291 the cap is 3,872, so (2.4)
has no hidden rounding slack. The cap is at most 46 on

$$
67,448 <= m <= 71,176
$$

or

$$
909,953 <= m <= 981,129.                              (2.5)
$$

There is also a direct overlap bound. Two subsets of E_0 of size at least m
intersect in at least $2m-R$ points. Comparing this with
$m-w-1$ gives

$$
m >= R-w = 913,682  implies  N_G(>=0) <= 1.           (2.6)
$$

Uniformly over every legal m, the denominator is positive once
$s>=177,835$. The worst fixed-G cap there is 327,043. The cap is at most
3,730 for $s>=177,901$ and at most 46 for $s>=183,167$. The immediately
preceding excesses attain 3,731 and 47 respectively.

These exact Johnson caps do not sum over G. In the broad middle m range the
s=0 denominator is nonpositive, and even one pair per locator would leave
the combinatorial divisor choice C(a,m). No assertion is made that a
forbidden family must actually use distinct locators.

## 3. Pairwise Wronskian route cut

For distinct canonical pairs define

$$
W_ij = G_i b_j - G_j b_i.                             (3.1)
$$

### Lemma 3.1

One has

$$
W_ij != 0,
deg(W_ij) <= m_i+m_j-w-1,                             (3.2)
$$

and W_ij vanishes on both common-root sets

$$
Z(G_i) intersection Z(G_j)
$$

and

$$
Z(H_i) intersection Z(H_j).                          (3.3)
$$

### Proof

If W_ij=0, then $G_i b_j=G_j b_i$. The two coprimality gates imply that
$G_i$ divides $G_j$ and $G_j$ divides $G_i$. Monicity gives $G_i=G_j$, and
then $b_i=b_j$, contradicting distinctness. The strict b-degree gates give
the degree bound. Both G polynomials vanish on their common roots. On a
common H root, the gcd relations give $G_i=b_iV$ and $G_j=b_jV$, so (3.1)
also vanishes.

The guaranteed H-overlap is

$$
|Z(H_i) intersection Z(H_j)|
>= max(0,m_i+m_j+s_i+s_j-R).
$$

When the positive branch applies, it exceeds the degree in (3.2) only if

$$
s_i+s_j >= R-w = 913,682.                             (3.4)
$$

Thus this two-codeword Wronskian argument cannot touch the boundary stratum
$s_i=s_j=0$, or any pair below (3.4). Adding the trivial forced G-overlap
inside S_0 still gives no boundary contradiction. Section 7 provides a
simultaneous abstract support family satisfying all these root budgets.

## 4. Global split-support moment

Let a family contain L nonanchor pairs and put

$$
M = sum_i m_i,
S = sum_i s_i.
$$

### Theorem 4.1

Every such family satisfies

$$
M^2/a + (M+S)^2/R - S
<= 2LM - L(L-1)(w+1).                                (4.1)
$$

Equivalently, for $mu=M/L$ and $sigma=S/L$,

$$
mu^2/a + (mu+sigma)^2/R - 2mu + w+1
<= (sigma+w+1)/L.                                    (4.2)
$$

### Proof

Sum (1.1) over unordered pairs. Cauchy-Schwarz on S_0 gives

$$
sum_(i<j) |Z(G_i) intersection Z(G_j)|
>= (M^2/a-M)/2.
$$

The corresponding total incidence on E_0 is M+S, so

$$
sum_(i<j) |Z(H_i) intersection Z(H_j)|
>= ((M+S)^2/R-(M+S))/2.
$$

The sum of the right side of (1.1) is

$$
(L-1)M - C(L,2)(w+1).
$$

Combining these inequalities proves (4.1); division by L squared gives
(4.2).

For a forbidden boundary list, retain exactly $B_*+1$ codewords, one of
which is the anchor. The selected nonanchor family has

$$
L = B_* = 16,777,215.                                 (4.3)
$$

Minimizing (4.2) over mu gives

$$
mu_* = a(R-sigma)/n
$$

and the exact necessary condition

$$
F(sigma)
= L(sigma^2+2a sigma-aR+n(w+1))
- n(sigma+w+1)
<= 0.                                                 (4.4)
$$

Exact integer evaluation gives

$$
F(366,886) = -35,406,814,945,353 < 0,                 (4.5)
$$

$$
F(366,887) = 14,351,365,971,580 > 0.                  (4.6)
$$

The positive root lies strictly between those integers, at approximately
366,886.7115778. The decimal is display-only. At sigma=366,886 the exact
quadratic in mu permits only

$$
326,151.4555... < mu < 327,601.1724... .              (4.7)
$$

The verifier decides (4.7) through integer discriminant comparisons, not
floating point. This feasible-region cut does not close the list because
(4.5) remains feasible.

The moment statements (4.3)-(4.7) apply to the selected full B_*-pair
family. A shallow subfamily obtained below obeys (4.2) with its own
cardinality; it is not assigned the full-family averages or polynomial
(4.4).

## 5. Exact cut of the deep excess tail

### Theorem 5.1

Let $N_deep(s)$ be the number of nonanchor companions with excess at least
s. Whenever the denominator is positive,

$$
N_deep(s)
<= floor( n(w+s+1) / ((a+s)^2-n(K-1)) ).              (5.1)
$$

### Proof

Truncate every relevant agreement support to an $(a+s)$-subset of the
n-point domain. Distinct RS codewords have agreement-support intersection
at most K-1. The incidence calculation in Theorem 2.1, now with universe n,
set size a+s, and intersection cap K-1, gives (5.1).

At the first positive denominator,

$$
s = 366,887,
(a+s)^2-n(K-1) = 909,700,
$$

and

$$
N_deep(366,887)
<= floor(910,866,513,920 / 909,700)
= 1,001,282.                                          (5.2)
$$

At s=366,886 the denominator is -2,056,119, so this second-moment route
supplies no finite cap there. Combining the B_* nonanchors in (4.3) with
(5.2), every forbidden boundary census contains at least

$$
16,777,215 - 1,001,282
= 15,775,933                                           (5.3)
$$

nonanchor pairs satisfying

$$
0 <= s <= 366,886.                                    (5.4)
$$

This is a direct-list diagnostic partition, not a first-match v4 payment.
No value is inserted into U_list-int or any other ledger atom.

There is also an exact chronology obstruction to treating (5.2) as a
replacement low-weight payment. Moving the rank-46 layer-cake cutoff to
s=366,887 would give the baseline

$$
1,001,282 + 45(366,887) = 17,511,197,
$$

which exceeds B_* by 733,982. The parent cutoff instead gives

$$
3,730 + 45(366,969) = 16,517,335.
$$

Thus the stronger direct deep-tail cap is numerically worse in the frozen
rank-46 chronology. This proves the advertised zero ledger movement rather
than merely declining to claim a payment.

## 6. Scalar descent and the base-field gate

### 6.1 Live counterexamples reduce to base-field boundary triples

Put

$$
L=B_*+1=2^{24}.
$$

The scalar-descent theorem in
`experimental/notes/thresholds/m31_scalar_descent_equivalence.md` applies
to the deployed extension F_(p^4)/F_p.  Its projective-functional counts
are

$$
N_4=9,903,520,305,059,670,166,633,185,280,
$$

$$
H_4=4,611,686,016,279,904,257.
$$

The exact strict gate is

$$
L R H_4 < (w+1)N_4,
$$

with respective sides

$$
75,911,179,514,902,718,909,260,442,370,048
$$

and

$$
667,972,637,535,664,633,399,075,080,765,440.
$$

The exact positive margin is

$$
592,061,458,020,761,914,489,814,638,395,392.         (6.1)
$$

Consequently, any quartic-valued center with a forbidden list projects,
under one F_p-linear functional, to an F_p-valued center with the same L
distinct F_p Reed--Solomon codewords and with all their agreement counts
preserved from below.  Since

$$
L=2^{24}<p,
$$

the fresh-symbol boundary-forcing lemma can then be applied inside F_p.
After translating by the resulting base-field boundary codeword, the
interpolating polynomial U and the anchor polynomials A_0,L_0,H_0,V all lie
in F_p[X].  The canonical companion data G,H,b obtained from base-field
codewords also lie in F_p[X].

It follows that the deployed quartic row closes if and only if the boundary
census bound

$$
#X(V) <= 16,777,214
$$

holds for every resulting base-field boundary triple, with V an arbitrary
unit in F_p[X]/(L_0).  Every such base-field unit remains realizable by an
anchor, so this reduction does not authorize V=1 or any low-degree,
periodic, rational, or quotient specialization.  It is a preprocessing
equivalence, not a v4 ledger payment.

### 6.2 The unreduced quartic scalar gate stops at m-w

The deployed evaluation points lie in F_p, while polynomial coefficients
live in F_(p^4). Fix H inside E_0 with at least m points, put d=m-w, and fix
a unit table V on H. Consider

$$
B(H,V) = {
 b in F_(p^4)[X] :
 deg(b)<d and b(x)V(x) in F_p for every x in H
}.                                                     (6.2)
$$

### Lemma 6.2

The F_p-dimension of B(H,V) is at most d. This is sharp: for V=1,

$$
B(H,1) = F_p[X]_(degree less than d)
$$

and has dimension d.

### Proof

Evaluate on any d distinct points of H. Evaluation is injective on
polynomials of degree less than d. At each point the allowed value b(x)
lies in the one-dimensional F_p-space $V(x)^(-1)F_p$. The product target
has dimension d, proving the upper bound.

For V=1, d base-field evaluations of a degree-less-than-d polynomial lie in
F_p exactly when its interpolated coefficients lie in F_p. This proves
equality.

On the roots of $H=gcd(L_0,G-bV)$, one has $bV=G$ in F_p, so (6.2) is
necessary for every census pair. The ambient b-coefficient space has
F_p-dimension 4d. Therefore this condition always imposes codimension at
least 3d. The V=1 equality shows that no larger codimension can be
guaranteed uniformly: the exact worst case is 3d=3(m-w).

Consequently a uniform p^(-3m) gain, or an extra independent gain from all
h points merely repeating the same base-field condition, is unavailable
from scalarization alone. This lemma does not count admissible (G,H,b)
incidences. The split-locator and common-V conditions must do additional
work.

For the live counterexample reduction in Section 6.1, V and b are already
base-field objects, so this scalar condition is automatic.  It supplies no
additional rank dichotomy or incidence count in the reduced census.

### 6.3 The V=1 slice is a prefix fiber but is not extremal

Take the base-field boundary anchor U=A_0=L_(S_0), so V=1.  Every admitted
pair has

$$
H=gcd(L_0,G-b),
$$

with deg(H)>=m=deg(G).  Since G-b is monic of degree m and H divides G-b,
one necessarily has

$$
H=G-b,
deg(H)=m,
b=G-H.                                                (6.3)
$$

For the companion support T write

$$
G=L_(S_0 minus T),
H=L_(T minus S_0).
$$

The common locator C gives

$$
L_(S_0)-L_T=C(G-H).
$$

Therefore

$$
deg(G-H)<m-w
$$

is equivalent to

$$
deg(L_(S_0)-L_T)<K,
$$

which is equality of the first w nonleading locator coefficients.  Hence

$$
#X_(S_0)(1)
= |Fib_w(prefix_w(L_(S_0)))|-1.                       (6.4)
$$

Because p>w, Newton identities also identify this prefix with equality of
the first w power sums.  The deployed fixed-remainder source proves the
existential lower floor

$$
max_(|S_0|=a) #X_(S_0)(1) >= 6,796,404.               (6.5)
$$

This is a raw source floor, not a v4 payment or a uniform lower bound for
every anchor.

The dimension sharpness at V=1 in Lemma 6.2 does not make V=1 extremal for
the census.  An exhaustive finite control already refutes that inference.
Over F_7 take

$$
D=(0,1,2,3,4,5),
K=2,
a=3,
y=(0,0,0,1,5,4).
$$

Every depth-one prefix fiber of a three-subset has size at most 3, so the
largest V=1 companion census has size 2.  The zero codeword is a boundary
anchor for y on S_0={0,1,2}, but its ball also contains the three companions

$$
3+4X,
5X,
2+6X.
$$

For this anchor

$$
H_0=6+5X+3X^2,
V=1+3X+5X^2,
$$

and V is a unit modulo L_0 with evaluation table (6,2,1) on E_0.  Thus

$$
max_(S,V)#X_S(V) >= 3 > 2 = max_S #X_S(1).            (6.6)
$$

The control is exhaustive, not asymptotic evidence.  It proves that a
general reduction from arbitrary V to V=1 is false.  A special comparison
on the deployed Chebyshev domain would be a genuinely new theorem and is
not supplied by scalar descent or the rank-two anchor module.

## 7. Restricted Chebyshev support countermodel

This section is an impossibility result for one enumerated proof interface.
It is not a received word, a family of RS codewords, or a counterexample to
the M31 row.

The standard-position M31 domain has K=n/2 complete T2 fibres, each with two
points. The exact Chebyshev tower pairs two T2 fibres into each complete T4
fibre.

Choose w T2 fibres, at most one from each T4 fibre, and place both of their
points in every support. In each of the remaining

$$
K-w = 981,129 = R
$$

T2 fibres choose exactly one point. Encode those choices by a binary word
z of length R, and call the resulting support T_z. Then

$$
|T_z| = 2w+R = K+w = a.                               (7.1)
$$

Every T_z has exactly w complete T2 fibres and no complete T4 fibre.
Moreover,

$$
|T_z intersection T_z'| = a - HammingDistance(z,z'). (7.2)
$$

Take a maximal binary code C of length R and minimum distance w+1. The
greedy covering argument gives

$$
|C| >= 2^R / Volume(R,w),
$$

where

$$
Volume(R,w) = sum_(i=0)^w C(R,i).
$$

Set x=1/16. Since $x^w <= x^i$ for i<=w,

$$
x^w Volume(R,w) <= (1+x)^R.
$$

Hence

$$
Volume(R,w)
<= 17^R / 16^(R-w)
< 44^w
< 2^(6w).                                             (7.3)
$$

The middle comparison is checked as one exact integer inequality. It
follows that

$$
|C| > 2^(R-6w) = 2^576447.                            (7.4)
$$

Translate C by one of its words so that it contains zero; distances are
unchanged. Pigeonhole the nonzero words by Hamming weight. Since R<2^20,
one fixed nonzero weight m contains more than

$$
2^576427 > B_*
$$

words. Relative to T_0, every support in that shell has

$$
|T_0 minus T_z| = |T_z minus T_0| = m,
s=0.                                                  (7.5)
$$

Equation (7.2) and the minimum distance give pairwise intersection at most
$a-(w+1)=K-1$. Thus the associated abstract G/H exchange sets satisfy
(1.1), at one fixed m, with the declared complete-fibre counts.

This proves only the following route cut: support cardinality, one fixed
exchange degree, pairwise MDS or Wronskian root budgets, and the numbers of
complete T2 and T4 fibres do not imply the M31 census bound. The construction
does not satisfy or refute stronger owner-specific support hypotheses, and
it does not realize G, b, V, or a common received word.

## 8. Elementary Singleton packing is too shallow

If N agreement supports have size at least r>=K and pairwise intersection
at most K-1, then their K-subsets are disjoint. Therefore

$$
N <= floor( C(n,K) / C(r,K) ).                        (8.1)
$$

Writing r=n-t, the deployed floors are

$$
t=23:  8,389,620 <= B_*,
$$

$$
t=24:  16,779,424 > B_*.                             (8.2)
$$

Thus this packing route first fits the budget only at agreement n-23. A
nonanchor companion has m>=w+1 and hence agreement at most

$$
n-(w+1) = n-67,448.
$$

The Singleton packing transition is unreachable in the live census.

## 9. Exact residual localization

Combining the proved cuts, any counterexample to the M31 row can be
boundary-forced and then contains at least 15,775,933 canonical pairs
satisfying

$$
G_i divides A_0,
67,448 <= m_i <= 981,129,
$$

$$
b_i != 0,
deg(b_i) < m_i-67,447,
gcd(b_i,G_i)=1,
$$

$$
H_i = gcd(L_0,G_i-b_iV),
m_i <= deg(H_i) <= m_i+366,886,                      (9.1)
$$

for one common arbitrary base-field unit V modulo L_0. For a live violation,
Section 6.1 permits A_0,L_0,V,G_i,H_i,b_i all to be chosen in F_p[X]. This
is a full-locator census: the G_i are allowed to range and must not be frozen
by the proof. It is not proved that the shallow family actually contains
multiple distinct G_i.

The selected full B_*-pair family also obeys the moment gate (4.2)-(4.6).
The shallow subfamily obeys (4.2) with its own size and averages.

The maximal successor is the exact base-field split-flat incidence theorem.
For a fixed monic divisor H of L_0 with deg(H)=m+s and d=m-w, define

$$
T_(H,V): F_p[X]_(degree less than d)
          --> F_p[X]_(degree less than m+s),
b maps to bV modulo H.                               (9.2)
$$

Because V is a unit modulo H and d<m+s, this map is injective and has rank
exactly d.  At the boundary s=0 the candidate locator is

$$
G=H+T_(H,V)(b),                                      (9.3)
$$

so the missing object is the intersection of the divisor set Div_m(A_0)
with an affine d-flat.  There is no boundary rank-drop stratification: the
constraint has constant codimension w.  For s>0, monicity of G gives an
affine system on the top s coefficient rows of T_(H,V), after which one must
still impose G divides A_0, gcd(b,G)=1, and the resultant gate making H the
full gcd rather than a chosen divisor.

The successor must count these split-flat intersections uniformly over H
while retaining the same arbitrary base-field V across the full census.
Any low-rank interior component must route to a named quotient/Chebyshev
owner or remain an explicit primitive component.

The exact cuts in this packet show that repeating the enumerated
fixed-locator Johnson, pairwise-root, restricted support-packing, or
base-field-scalarization arguments cannot by itself prove the missing
uniform census theorem.

## 10. Ledger and proof audit

The parent source adapter retains

$$
U_paid = 3,730,
U_Q = U_list-int = U_ext = U_new = null.
$$

This packet has

$$
ledger movement = 0,
official endpoint movement = 0.
$$

Statement audited:

The implication chain from the exact boundary-anchor census to the shallow
common-V, full-locator residual (9.1), together with the failure of the
enumerated weaker interfaces to close it.

Dependencies:

- PROVED: the scalar-descent equivalence and its strict deployed margin.
- PROVED: the parent all-weight bijection and fresh-symbol boundary forcing,
  applied over F_p after scalar descent.
- PROVED: every finite incidence inequality and deployed endpoint here.
- PROVED: the exact T2/T4 fibre tower in the deployed standard-position
  Chebyshev domain, imported from the foundation theorem.
- UNPROVEN: a common-V, full-locator coefficient-incidence theorem and the
  row bound.

Parameter dependence:

Every numerical threshold uses exactly

$$
(n,K,a,R,w,B_*)
= (2097152,1048576,1116023,981129,67447,16777215).
$$

Layer-cake and dyadic summability:

Not applicable.

Moment, Markov, and Chebyshev:

Sections 2, 4, and 5 use exact finite incidence second moments. There is no
Markov inequality or analytic Chebyshev inequality. In Section 7,
Chebyshev names the deployed polynomial folding tower.

Numerical evidence:

Python evaluates exact integers and rational discriminants only. No toy or
floating-point evidence is promoted to proof.

Verdict:

YELLOW. The route cuts and residual localization are GREEN; the M31 list
row remains open.
