---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: In the base-field boundary census, every fixed-H chart is an exact split affine flat with explicit full-gcd resultant gates. For any family of at most B_star canonical triples, one common unit V exists if and only if each denominator is a unit on its declared H and the pairwise Wronskians vanish on H intersections and do not vanish on H symmetric differences. Thus there is no hidden triple-or-higher common-V compatibility at the deployed list size. Row closure is equivalent to a global split rational-function/divisor incidence bound, not another common-V rank or generic CRT lemma.
architecture: M31_BASE_FIELD_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1
parent_payload_sha256: fcc630ba68c803bb67378f836a84e6bdbcefe7fd9d5b468ef48fe919bd8307e3
atom_or_cell: Direct threshold-equivalent boundary-census diagnostic; no v4 atom value, owner transport, or signed-Xi payment.
quantifier: Every base-field M31 boundary partition D=S0 disjoint-union E0 and every family of at most 16777215 pairwise-distinct canonical reduced pairs decorated by split H locators. The fixed-H atlas retains all degrees m and excesses s. The pairwise reconstruction theorem uses B_star<p-1.
projection_and_unit: Distinct nonanchor codewords per received word in the parent boundary coordinate. The common unit is a nonzero table on E0, interpolated uniquely modulo L0.
claimed_bound: Exact equivalence and route cut only. The sufficient shallow-family upper 15775932 and the M31 row remain unproved. Ledger movement is zero.
status: PROVED PAIRWISE CRT EQUIVALENCE / PROVED SPLIT-FLAT ATLAS / GLOBAL INCIDENCE OPEN
impact: ROUTE_CUT / EXACT_RESIDUAL_REFORMULATION
falsifier: A family of at most B_star pairwise-distinct reduced pairs satisfying every individual denominator-unit and pairwise Wronskian gate for which no common unit realizes the declared full gcds; a realized common-unit family violating one of those gates; a fixed-H chart not represented by the displayed affine systems; or any use of this packet as a v4 payment.
replay: Independent standard-library and Sage finite-field controls, proof-critical mutations, source hashes, predecessor replay, and fresh proof review.
---

# M31 common-V split-flat and pairwise CRT equivalence

## Status

This packet proves two exact structural theorems for the base-field boundary
census left by the parent route-cut packet.

1. For fixed full gcd locator H, the admissible numerator locator G lies in
   an explicit affine split flat.  Boundary charts have constant codimension
   w and no rank-drop stratum.  A nonempty interior chart has at least one
   additional independent coefficient constraint.

2. For a family of at most B_star triples, the existence of one common unit
   V modulo L_0 is equivalent to the individual denominator-unit gates and
   explicit pairwise Wronskian vanishing and nonvanishing gates.  After the
   individual gates, pairwise compatibility is sufficient; there is no
   hidden triple or higher CRT obstruction at the deployed list size.

Neither theorem counts the resulting global split-locator family.  The M31
LIST row remains open, all four null v4 atoms remain null, and ledger,
endpoint, and score movement are zero.

## 1. Imported base-field boundary census

By scalar descent followed by fresh-symbol forcing over F_p, row closure is
equivalent at the direct threshold level to the base-field boundary census.
Write

$$
p=2^{31}-1,
n=2^{21},
K=2^{20},
a=1,116,023,
$$

$$
R=n-a=981,129,
w=a-K=67,447,
B_*=2^{24}-1=16,777,215.
$$

Let

$$
D=S_0\mathbin{\dot\cup}E_0,
|S_0|=a,
|E_0|=R,
$$

and put A_0=L_(S_0), L_0=L_(E_0).  A canonical nonanchor pair has

$$
G\mid A_0,
m=deg(G),
w+1\le m\le R,
$$

$$
b\ne0,
deg(b)<d:=m-w,
gcd(b,G)=1,
$$

$$
H=gcd(L_0,G-bV),
deg(H)=h=m+s\ge m.                                  (1.1)
$$

All locators are monic and split on their declared disjoint domains.  The
parent packet proves that any forbidden boundary list contains B_* canonical
nonanchor pairs, at least

$$
15,775,933                                             (1.2)
$$

of which have

$$
0\le s\le366,886.                                    (1.3)
$$

The pairs need not have distinct G or H locators.

## 2. Exact fixed-H split-flat atlas

Fix a monic divisor H of L_0 with degree h=m+s and fix a unit V modulo
L_0, represented by a polynomial and hence also a unit modulo H.
For P_t=F_p[X]_(degree less than t), divide

$$
bV=H Q_(H,V)(b)+T_(H,V)(b),
deg(T_(H,V)(b))<h.                                   (2.1)
$$

Thus

$$
T_(H,V):P_d\longrightarrow P_h
$$

is the multiplication-by-V remainder map.

### Lemma 2.1: full column rank

The map T_(H,V) is injective.  Its h by d coefficient matrix has rank d.

### Proof

If T_(H,V)(b)=0, then H divides bV.  Since V is a unit modulo H, H divides
b.  But deg(b)<d=m-w<h=m+s, so b=0.

### Theorem 2.2: boundary charts

Suppose s=0, so deg(H)=deg(G)=m.  Then

$$
H\mid G-bV
\quad\Longleftrightarrow\quad
G=H+T_(H,V)(b).                                      (2.2)
$$

Writing L_0=HJ, the full-gcd condition is exactly

$$
gcd(J,1-Q_(H,V)(b))=1,                               (2.3)
$$

or equivalently the nonvanishing of the corresponding resultant.  Before
the split and coprimality gates, the candidate G values form the affine
d-flat

$$
H+T_(H,V)(P_d)
$$

inside the m-dimensional monic coefficient space.  Its codimension is

$$
m-d=w.                                               (2.4)
$$

In particular every boundary chart has the same rank.  There is no boundary
rank-drop component to classify.

### Proof

The remainder of the monic degree-m polynomial G modulo the monic degree-m
polynomial H is G-H.  Equation (2.2) follows from (2.1).  Substitution gives

$$
G-bV=H(1-Q_(H,V)(b)).
$$

Because L_0 is squarefree and H,J are coprime, its gcd with L_0 is exactly H
if and only if (2.3) holds.  Lemma 2.1 gives the dimension assertion.

### Theorem 2.3: interior charts

Suppose s>0.  Let C_(H,m,V) be the s by d block consisting of coefficient
rows m through h-1 of T_(H,V), in increasing degree order, and let

$$
e_0=(1,0,\ldots,0)^T\in F_p^s.
$$

Then H divides G-bV for a monic degree-m polynomial G if and only if

$$
C_(H,m,V)b=e_0,
\qquad
G=T_(H,V)(b).                                        (2.5)
$$

Writing L_0=HJ, the full-gcd gate is

$$
gcd(J,Q_(H,V)(b))=1.                                 (2.6)
$$

If (2.5) is consistent and rho=rank(C_(H,m,V)), then

$$
1\le rho\le\min(s,d),                                (2.7)
$$

and its G values form an affine (d-rho)-flat of monic degree-m locators.
Consequently every nonempty interior chart has ambient monic-locator
codimension at least w+1.  No stronger uniform rank claim is made.

### Proof

Here deg(G)=m<h, so the remainder of G modulo H is G.  Equation (2.5) is
exactly the condition that T_(H,V)(b) have coefficient 1 at X^m and zero
coefficients above it.  If C had rank zero, its image would not contain the
nonzero vector e_0, so consistency implies rho at least one.  Lemma 2.1
makes the map from the affine b-solution set to G injective.  Finally

$$
G-bV=-H Q_(H,V)(b),
$$

which gives (2.6).

For both boundary and interior charts one must still impose

$$
G\mid A_0,
\qquad
Res(G,b)\ne0,                                        (2.8)
$$

as well as the full-gcd resultant.  Since H is the full gcd in (1.1), the
sum over H is disjoint even though G may repeat.

Replacing the polynomial representative V by V+C L_0 leaves T unchanged
and changes Q by bCJ.  Hence the gcd gates (2.3) and (2.6) depend only on
the residue class of V modulo L_0, as required.

## 3. Eliminating the common unit

The fixed-H atlas still writes a unit V explicitly.  The following theorem
shows that, at the deployed family size, V contributes no compatibility
beyond pairs.

The CRT elimination itself needs no M31 degree inequality.  Let I index
pairwise distinct reduced pairs (G_i,b_i), each decorated by a monic divisor
H_i of L_0.  Here G_i is a monic divisor of the squarefree locator A_0,
H_i is a monic divisor of the squarefree locator L_0, and

$$
gcd(G_i,b_i)=1.                                      (3.1)
$$

For i distinct from j define

$$
W_(ij)=G_i b_j-G_j b_i,
\qquad
J_(ij)=gcd(H_i,H_j),                                 (3.2)
$$

and the symmetric-difference locator

$$
Delta_(ij)=H_iH_j/J_(ij)^2.                          (3.3)
$$

### Theorem 3.1: pairwise CRT equivalence

Assume

$$
|I|<p-1.                                             (3.4)
$$

There exists a unit V in F_p[X]/(L_0) satisfying

$$
H_i=gcd(L_0,G_i-b_iV)
\quad\hbox{for every }i\in I                         (3.5)
$$

if and only if the individual gates

$$
gcd(b_i,H_i)=1\qquad(i\in I)                         (3.5a)
$$

hold and, for every distinct i,j,

$$
J_(ij)\mid W_(ij),                                   (3.6)
$$

and

$$
gcd(Delta_(ij),W_(ij))=1.                            (3.7)
$$

For distinct reduced pairs W_(ij) is nonzero.  Conditions (3.6) and
(3.7) say exactly that W_(ij) vanishes on Z(H_i) intersection Z(H_j) and is
nonzero on their symmetric difference.

### Proof: necessity

Let x be a root of H_i.  Since G_i has roots only in S_0 and x lies in E_0,
G_i(x) is nonzero.  Equation (3.5) and the unit condition give

$$
b_i(x)\ne0,
\qquad
V(x)=G_i(x)/b_i(x).                                  (3.8)
$$

On a common H_i,H_j root the two ratios in (3.8) agree, giving (3.6).  On a
root belonging to exactly one of H_i,H_j, exactness of the other full gcd
says the ratios do not agree, giving (3.7).  Condition (3.5a) also follows
from (3.5), so it is a necessary declared gate.

### Proof: sufficiency

For every covered point

$$
x\in\bigcup_i Z(H_i),
$$

choose any i with x in Z(H_i) and set

$$
v_x=G_i(x)/b_i(x).                                   (3.9)
$$

This is defined and nonzero by (3.5a) and the disjoint root domains.
Condition (3.6) makes it independent of the chosen i.  Condition (3.7)
ensures that if x is not a root of H_j, then

$$
G_j(x)-b_j(x)v_x\ne0.                                (3.10)
$$

At an uncovered point x, avoid zero and every value

$$
G_i(x)/b_i(x)
$$

for which b_i(x) is nonzero.  There are at most |I|+1 forbidden field
elements.  By (3.4), at least one value remains.  If b_i(x)=0, then
G_i(x) is nonzero and index i excludes no value.

The resulting table x maps to v_x is nonzero on E_0.  Interpolate it modulo
the squarefree polynomial L_0 to obtain a unit V.  Equations (3.9)-(3.10)
make the root set of G_i-b_iV inside E_0 exactly Z(H_i), proving (3.5).

The field-size hypothesis is load-bearing.  Without it, the nonzero ratios
at one uncovered point can exhaust the multiplicative group even when every
pairwise H gate is vacuous.

This failure is sharp.  Over F_5 take E_0={0}, S_0=F_5^*, and, for every
a in F_5^*, take

$$
G_a=X-a,
\qquad b_a=1,
\qquad H_a=1.
$$

Every pairwise H gate is vacuous, but at the sole uncovered point the four
forbidden ratios G_a(0)/b_a(0) exhaust F_5^*.  Hence no unit V exists when
|I|=p-1.  The strict inequality in (3.4) cannot be weakened to
|I|<=p-1.

### Corollary 3.2: exact boundary-list realization

Assume in addition all canonical degree and split-locator gates from
Section 1.  Given the unit V constructed in Theorem 3.1, take its inverse
H_0 modulo L_0 and set

$$
U=A_0H_0,
\qquad
c_i=(A_0/G_i)b_i.                                    (3.11)
$$

Then U restricted to D is a base-field received word with the zero
codeword as a boundary anchor, and every c_i is a distinct degree-less-than-K
codeword in its radius-R ball.  Its agreement support is exactly

$$
(S_0\setminus Z(G_i))\mathbin{\dot\cup}Z(H_i).        (3.12)
$$

Conversely every selected base-field boundary list gives such a family.
Hence, for |I|=B_*, the individual-unit plus pairwise criterion is an exact
boundary-counterexample criterion, not only a necessary condition.

### Proof

The degree gate gives

$$
deg(c_i)
<a-m_i+(m_i-w)=a-w=K.
$$

On S_0 the roots of A_0/G_i give the first part of (3.12), while
gcd(b_i,G_i)=1 prevents accidental agreements on Z(G_i).  On E_0,
V=H_0^(-1) and the exact gcd identity in (3.5) give precisely Z(H_i).
If c_i=c_j, cancellation of A_0 gives G_i b_j=G_j b_i.  Monicity and the
two reduced coprimality gates force (G_i,b_i)=(G_j,b_j), contrary to the
declared distinctness.  The converse is the parent boundary bijection.

## 4. Exact deployed consequence

For a selected forbidden family one has |I|=B_*, and

$$
p-1-B_*
=2,130,706,431>0.                                   (4.1)
$$

At the forced shallow-family width the margin is even larger:

$$
p-1-15,775,933
=2,131,707,713.                                      (4.1a)
$$

Thus Theorem 3.1 applies with enormous exact slack.  It proves the route cut

$$
\text{common-V full-gcd realizability}
\quad\Longleftrightarrow\quad
\text{individual-unit and pairwise exact-Wronskian compatibility}. (4.2)
$$

There is no missing triple, higher syzygy, or generic CRT compatibility
lemma to discover for this census.  The common V is reconstructible once the
pairwise gates hold.

Let N_(m,s,H)(V) count the fixed-H chart after (2.3) or (2.6), (2.8), and
the split-locator gates.  The full census is the disjoint sum

$$
#X(V)
=\sum_(m=w+1)^R\ \sum_(s=0)^(R-m)
  \ \sum_{\substack{H\mid L_0\\deg(H)=m+s}}
  N_(m,s,H)(V).                                      (4.3)
$$

Combining Theorem 3.1 with the parent deep-tail cut, the exact sufficient
successor theorem is:

> Every split rational-function family satisfying the individual-unit gate,
> every pairwise compatibility gate, all canonical gates, and
> 0<=s<=366,886 has size at most 15,775,932.

A forbidden list would instead supply 15,775,933 such shallow members.
This one-unit gap is exact.

## 5. Sharp local route cuts

At the first legal boundary degree,

$$
m=w+1=67,448,
\qquad
d=1.                                                 (5.1)
$$

Before the split and full-gcd gates a fixed-H boundary chart has p-1
nonzero scalar parameters, and

$$
p-1
=128(16,777,214)+254.                                (5.2)
$$

Thus dimension counting alone exceeds the complete companion target in one
chart.

The split-root condition gives the exact elementary cap

$$
N_H\le\left\lfloor a/m\right\rfloor=16.              (5.3)
$$

Indeed each alpha in S_0 determines at most one scalar parameter, while
each admitted G consumes m distinct roots.  For fixed G, the corresponding
level sets on E_0 are disjoint, giving

$$
N_G\le\left\lfloor R/m\right\rfloor=14.              (5.4)
$$

Neither cap sums globally.  Already

$$
{R\choose2}=481,306,566,756>B_*,                     (5.5)
$$

and the number of legal degree-m H locators is much larger.  A forbidden
family need not repeat either locator.  Theorem 3.1 shows that appealing
again to unspecified common-V compatibility cannot repair this global
locator sum.

There is a second exact route cut.  Fix G dividing A_0, let deg(G)=m and
d=m-w, and define the received table

$$
r_(G,V)(x)=G(x)/V(x),\qquad x\in E_0.                (5.6)
$$

Because G and V are units on E_0, every b in P_d satisfies

$$
deg(gcd(L_0,G-bV))
=agr_(E_0)(b,r_(G,V)).                               (5.7)
$$

Conversely, as V ranges over the units modulo L_0, the table r_(G,V)
ranges bijectively over all nonzero-valued received words E_0 to F_p^*: for
a prescribed nonzero table r set V(x)=G(x)/r(x) and interpolate modulo L_0.
Thus a fixed-G slice is exactly an ordinary Reed--Solomon list census around
an arbitrary nonzero-valued received word, of dimension d and agreement
threshold m, with only the additional filter gcd(b,G)=1.

In particular, a putative forbidden family may concentrate on one repeated
G.  No proof may assume cross-G variation or treat a common V as a source of
pseudorandomness.  The fixed-G Johnson denominator is

$$
m^2-R(d-1),                                         (5.8)
$$

and it is nonpositive throughout the exact integer interval

$$
72,859\le m\le908,270.                              (5.9)
$$

Consequently another fixed-G Johnson or moment substitution cannot settle
the broad middle range from the current hypotheses.  A closing theorem must
either prove a beyond-Johnson capacity-gap bound for these arbitrary
nonzero received words, uniformly over E_0, or use the split-numerator and
coprimality structure together with global aggregation.  The normalized
agreement-minus-dimension gap is

$$
(m-d)/R=w/R=67,447/981,129.                          (5.10)
$$

## 6. Architecture and proof audit

The parent direct threshold equivalence remains valid, but it does not
transport exact error supports or first-match owners into the v4 target-field
chronology.  This packet therefore has

$$
ledger\ movement=0,
\qquad
official\ endpoint\ movement=0.
$$

The parent values remain

$$
U_{paid}=3,730,
\qquad
U_Q=U_{list-int}=U_{ext}=U_{new}=null.
$$

Statement audited:

The exact fixed-H affine atlas and the implication chain from a family of
split-locator triples to one common base-field unit, and back.

Dependencies:

- PROVED: scalar descent to the base-field direct threshold and base-field
  fresh-symbol boundary forcing.
- PROVED: the all-weight anchor-exchange bijection and the parent shallow
  residual 15,775,933.
- PROVED HERE: the split-flat equations, full-gcd resultants, and pairwise
  CRT equivalence under |I|<p-1.
- UNPROVEN: the global split rational-function/divisor incidence upper
  15,775,932 and every v4 owner payment.

Parameter dependence:

Every deployed number uses exactly

$$
(p,n,K,a,R,w,B_*)
=(2147483647,2097152,1048576,1116023,981129,67447,16777215).
$$

Layer-cake and dyadic summability:

Not applicable.

Moment, Markov, and Chebyshev:

No new moment or probabilistic inequality is used.  Chebyshev refers only to
the deployed evaluation domain in the parent packets.

Numerical evidence:

Finite-field controls test the exact algebra and edge cases.  They are not
promoted into a deployed incidence upper.

Verdict:

YELLOW.  The pairwise equivalence and split-flat atlas are GREEN; the global
incidence theorem and M31 LIST row remain open.

## 7. Maximal successor

Attack the individual-unit and pairwise-compatible split rational-function
family directly.
The exact objects are

$$
r_i=G_i/b_i,
$$

with split numerator G_i, low-degree denominator b_i, exact H_i agreement
locator, and pairwise cross-difference W_(ij).  Any proof must exploit the
global distribution of split G and H locators, or route an exhaustive
component to a source-bound quotient/Chebyshev owner.  Repeating fixed-H
rank calculations, generic CRT saturation, or a V=1 specialization cannot
close the row.

Use Sage for exact finite-field atlas and clique controls, Python big
integers for the deployed thresholds and mutation certificate, and
Singular/Oscar only after one fixed split-incidence component is identified.
TheoremSearch and outside literature search should target list bounds for
split rational-function interpolation and divisor-flat incidence, not
generic simultaneous Pade solvability.
