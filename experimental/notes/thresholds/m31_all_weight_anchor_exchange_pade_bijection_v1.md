---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Relative to any actual listed anchor, the complete Reed--Solomon list across all exact weights is in bijection with one exact divisor/gcd incidence census (G,b). The correctly oriented interpolation module has basis (L0,0),(V,A0), and the exact error locator is G(L0/gcd(L0,G-bV)). A fresh-symbol forcing lemma reduces M31 row closure exactly to boundary anchors t=0, still with arbitrary unit V. The remaining row theorem is the uniform boundary pair-census bound 16777214.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: Exact all-weight diagnostic reduction of HIGH_BOUNDARY_EXACT_CODEWORD and HIGH_INTERIOR_EXACT_CODEWORD; no atom value and no signed-Xi payment.
quantifier: Every field, every distinct evaluation domain, every received word, and every actual listed anchor for the bijection; the M31 closing census need only be uniform over boundary-anchor triples because B_star+1 is strictly smaller than the field.
projection_and_unit: Exact bijection with distinct codewords per received word. The pair (G,b) is canonical relative to the chosen anchor; it is not a support count, ray count, or first-match owner.
claimed_bound: Exact complete-list identity, exact boundary-anchor forcing, and generic-unit-V route cut. At M31, the boundary closing pair-census target is at most 16777214. That census bound is unproved.
status: PROVED EXACT BIJECTION / PROVED BOUNDARY FORCING / PROVED GENERIC-V ROUTE CUT / ROW OPEN
impact: ALL_WEIGHT_REDUCTION / ROUTE_CUT
falsifier: Reversing the module congruence; allowing b=0; weakening deg b<g-w0; omitting gcd(b,G)=1; replacing the full monic gcd by an arbitrary divisor; changing the exact error locator or weight; violating B_star+1<|F| in the boundary reduction; or finding a direct listed codeword absent from the pair census.
replay: Exact Python prime-field exhaustion, independent Sage replay including characteristic two, proof-critical mutations, source hashes, and fresh independent proof review.
---

# Exact all-weight anchor-exchange Padé bijection

## Status

PROVED: exact complete-list bijection relative to every actual anchor.

PROVED: correctly oriented rank-two interpolation-module basis.

PROVED: exact error locator and exact weight formula.

PROVED: every unit V modulo L0 is realizable from one exact anchor.

PROVED: boundary-anchor, V=1 shift-pair specialization.

PROVED: fresh-symbol reduction of the deployed row to boundary anchors.

OPEN: the M31 census bound. Ledger movement is zero; U_Q, U_list-int,
U_ext, and U_new remain null.

This theorem is the first reduction in the current stack that parametrizes
the complete list without fixing an error weight, padding to the boundary, or
sampling a support chart. It converts the maximal cross-weight problem left
by the v4 global compiler into one exact divisor/gcd incidence census.

It is a reduction and route cut, not the missing upper bound. Rank two and
one exact anchor do not force V into a low-degree, rational, periodic, or
quotient subclass: every unit modulo L0 occurs.

Because the M31 counterexample threshold plus one is strictly smaller than
the code field, an elementary fresh-symbol argument reduces the direct row
problem further: it is enough to bound the complete census for boundary
anchors \(j_0=R\), while retaining arbitrary unit \(V\).  This is not the
invalid specialization \(V=1\).

## 1. General setup

Let F be a field, let D be a set of n distinct points of F, and let

\[
  1\le K\le a\le n,\qquad R=n-a.
\]

Identify RS_F(D,K) with the polynomials in F[X] of degree less than K. For a
received word y, let L_R(y) be its closed radius-R list. Fix an actual anchor
c0 in L_R(y), translate y and every codeword by c0, and let U in F[X] of
degree less than n interpolate the translated word. The zero codeword is now
the anchor.

Define the anchor agreement and error sets

\[
 S_0=\{x\in D:U(x)=0\},\qquad E_0=D\setminus S_0,
\]

and put

\[
 s_0=|S_0|,\quad j_0=|E_0|\le R,\quad w_0=s_0-K\ge a-K.
\tag{1.1}
\]

For T contained in D, write L_T for the monic locator of T, and set

\[
 A_0=L_{S_0},\qquad L_0=L_{E_0},\qquad \Lambda_D=A_0L_0.
\tag{1.2}
\]

If j0>0, exactness of the anchor gives

\[
 U=A_0H_0,\qquad \deg H_0<j_0,\qquad \gcd(H_0,L_0)=1.
\tag{1.3}
\]

Let V be the unique polynomial of degree less than j0 satisfying

\[
 VH_0\equiv1\pmod{L_0}.
\tag{1.4}
\]

Every gcd below is monic, and gcd(L0,0)=L0.

## 2. Correct module orientation

Define

\[
 \mathcal M_U=\{(W,N)\in F[X]^2:N\equiv WU\pmod{\Lambda_D}\}.
\tag{2.1}
\]

### Lemma 2.1

For j0>0, this module has the exact basis

\[
 (L_0,0),\qquad(V,A_0).
\tag{2.2}
\]

### Proof

Both vectors lie in the module because L0 U is divisible by A0 L0 and
A0-VU=A0(1-VH0) is divisible by A0 L0.

Conversely, let (W,N) lie in the module. Reduction modulo A0 gives A0|N, so
N=BA0. Dividing N-WU=A0(B-WH0) by A0 and reducing modulo L0 gives
B=WH0 modulo L0. Multiplication by V gives W=BV modulo L0, hence uniquely

\[
 W=AL_0+BV,\qquad N=BA_0.
\]

Thus (W,N)=A(L0,0)+B(V,A0). Uniqueness follows because F[X] is a domain,
or from the determinant A0 L0.

The orientation in (2.1) is load-bearing. If it is reversed to
W=NU modulo Lambda_D, then (L0,0) generally is not in the module.

## 3. Exact all-weight bijection

For a monic divisor G of A0 write g=deg G. Define X(V) to be the set of
pairs (G,b) satisfying

\[
\begin{aligned}
 &G\mid A_0,\quad G\ {\rm monic},\quad g\ge w_0+1,\\
 &0\ne b\in F[X],\quad \deg b<g-w_0,\quad \gcd(b,G)=1,\\
 &\deg\gcd(L_0,G-bV)\ge j_0+g-R.
\end{aligned}
\tag{3.1}
\]

### Theorem 3.1

If j0>0, the nonanchor codewords in L_R(y) are in bijection with X(V).
For a pair in X(V), define

\[
 H=\gcd(L_0,G-bV),\qquad J=L_0/H,\qquad C=A_0/G.
\tag{3.2}
\]

Then its codeword, exact error locator, and exact error weight are

\[
 c=Cb,\qquad L_E=GJ=G(L_0/H),\qquad
 j=j_0+g-\deg H.
\tag{3.3}
\]

Consequently the complete list has the exact cardinality

\[
 |\mathcal L_R(y)|=1+
 \sum_{\substack{G\mid A_0\ {\rm monic}\\\deg G\ge w_0+1}}
 \#\left\{b:
 \begin{array}{l}
  b\ne0,\ \deg b<\deg G-w_0,\ \gcd(b,G)=1,\\
  \deg\gcd(L_0,G-bV)\ge j_0+\deg G-R
 \end{array}\right\}.
\tag{3.4}
\]

### Proof

Let c be a nonzero listed codeword. Split D into four exact cells:

\[
\begin{array}{ll}
 C_{\rm set}=\{U=0,c=0\},&
 G_{\rm set}=\{U=0,c\ne0\},\\
 H_{\rm set}=\{U\ne0,c=U\},&
 J_{\rm set}=\{U\ne0,c\ne U\}.
\end{array}
\]

Use C,G,H,J for their monic locators. Then

\[
 A_0=CG,\qquad L_0=HJ,\qquad L_E=GJ.
\tag{3.5}
\]

The exact locator pair (GJ,GJc) belongs to M_U. Write it in the basis:

\[
 (GJ,GJc)=\alpha(L_0,0)+\beta(V,A_0).
\tag{3.6}
\]

The second coordinate gives GJc=beta A0=beta CG, hence Jc=beta C.
Since gcd(C,J)=1, there is a unique nonzero b with beta=Jb and c=Cb.
The first coordinate then gives

\[
 GJ=\alpha HJ+JbV,\qquad
 G=\alpha H+bV.
\tag{3.7}
\]

Thus the module coefficients are

\[
 \alpha=(G-bV)/H,\qquad \beta=bL_0/H.
\tag{3.8}
\]

They are not the exchange pair (G,b); keeping these roles distinct is
load-bearing.

Because deg C=s0-g and deg c<K,

\[
 \deg b<K-(s_0-g)=g-w_0.
\tag{3.9}
\]

Nonzero b forces g>=w0+1. At the roots of G, U=0 and C is nonzero, so exact
nonagreement is equivalent to b being nonzero at every root of G, namely
gcd(b,G)=1.

For x in E0, both A0(x) and V(x) are nonzero and V(x)H0(x)=1. Therefore

\[
 U(x)=c(x)\quad\Longleftrightarrow\quad G(x)=b(x)V(x).
\tag{3.10}
\]

Hence H is the full monic gcd gcd(L0,G-bV), not an arbitrary divisor. The
error weight is

\[
 j=\deg G+\deg J=j_0+g-\deg H,
\]

and j<=R is exactly the last gate in (3.1).

Conversely choose a pair satisfying (3.1), define C,H,J,c by (3.2)-(3.3),
and repeat the pointwise calculation. The degree gate gives deg c<K.
Agreement occurs exactly on the roots of C and H; error occurs exactly on
the roots of G and J. Thus the error locator is GJ and the weight is at most
R.

The inverse is canonical: the exact error support recovers G as the locator
of E intersect S0, then C=A0/G and b=c/C. This proves both directions and
uniqueness.

### Corollary 3.2 (slack-normal form)

Put

\[
 w=a-K,\qquad t=R-j_0,\qquad m=g-t,\qquad h=\deg H.
\tag{3.11}
\]

Then \(s_0=a+t\) and \(w_0=w+t\).  Consequently the complete set of
nonanchor pairs in Theorem 3.1 is equivalently described by

\[
\begin{aligned}
 &0\le t\le R,\qquad w+1\le m\le R-t,\qquad
   G\mid A_0,\quad \deg G=m+t,\quad G\text{ monic},\\
 &0\ne b,\qquad \deg b<m-w,\qquad \gcd(b,G)=1,\\
 &H=\gcd(L_0,G-bV),\qquad h\ge m.
\end{aligned}
\tag{3.12}
\]

The exact companion weight is

\[
 j=R+m-h.
\tag{3.13}
\]

In particular, the companion is on the radius boundary exactly when
\(h=m\), and is interior exactly when \(h>m\).  If \(t>R-w-1\), the
nonanchor census is empty and the list is the singleton anchor.

### Proof

The identities

\[
 s_0=n-j_0=a+t,\qquad w_0=s_0-K=w+t
\]

give

\[
 g\ge w_0+1\iff m\ge w+1,qquad
 \deg b<g-w_0\iff\deg b<m-w.
\]

The radius gate becomes

\[
 h\ge j_0+g-R=(R-t)+(m+t)-R=m,
\]

while \(h\le\deg L_0=j_0=R-t\) gives \(m\le R-t\).  Finally,
\(j=j_0+g-h=R+m-h\).  This proves every assertion.

### Corollary 3.3 (fresh-symbol boundary forcing)

Let \(\mathcal C\subseteq F^D\) be any code, let \(0\le R<n\), and let
\(B\ge0\) be an integer satisfying

\[
 B+1<|F|.
\tag{3.14}
\]

If some closed radius-\(R\) ball contains at least \(B+1\) codewords, then
there is a received word whose radius-\(R\) ball contains the same selected
\(B+1\) codewords and for which at least one selected codeword has distance
exactly \(R\).  Consequently, the uniform list bound

\[
 \max_y |\mathcal L_R(y)|\le B
\tag{3.15}
\]

holds if and only if it holds for received words having a boundary codeword.

### Proof

Choose \(B+1\) distinct codewords in a counterexample ball and write
\(a=n-R\).  Among the selected words choose \(c_0\) with the fewest
agreements with the center, say \(a+t\).  Every selected word has at least
\(a+t\) agreements.  Select any \(t\) coordinates on which \(c_0\) agrees
with the center.  At each selected coordinate replace the received symbol by
an element of \(F\) outside the at most \(B+1\) symbols used there by the
selected codewords; (3.14) supplies such an element.

No selected codeword gains an agreement, and each loses at most \(t\).
Thus every selected word retains at least \(a\) agreements, while \(c_0\)
loses exactly \(t\) and has exactly \(a\).  The same \(B+1\) words remain in
the ball and \(c_0\) is on its boundary.  The reverse implication in (3.15)
is immediate.

## 4. Edge cases

If j0=0, then U=0. Every nonzero codeword of degree less than K has at least
n-K+1>R nonzero evaluations, so the list is the singleton anchor.

Before imposing b!=0, the anchor has the canonical tuple (G,H,b)=(1,1,0).
Separating it prevents duplicate zero representations.

The divisor G=A0 is legal. The case H=L0 is legal and restores every old
anchor error. The case G-bV=0 is handled by gcd(L0,0)=L0.

The case H=1 is a useful rejected control: j=j0+g is at least
j0+w0+1=n-K+1>R.

The strict degree inequality, b!=0, gcd(b,G)=1, full gcd, and exact unpadded
anchor support are all load-bearing.

## 5. Boundary anchors and V=1

For a boundary anchor j0=R, the ball gate is

\[
 \deg H\ge g.
\tag{5.1}
\]

A second codeword has exact boundary weight R precisely when deg H=g; it is
interior when deg H>g.

If moreover U=A0, then H0=V=1. Since deg b<g, the monic polynomial G-b has
degree g. Hence deg H<=g. Combined with (5.1), every admitted pair has

\[
 H=G-b,\qquad \deg H=g,\qquad b=G-H.
\tag{5.2}
\]

Thus the depth-w0 shift-pair/quotient family is an exact stratum of the
all-weight bijection. For general V, deg H may exceed g; no such conclusion
is available.

## 6. Arbitrary-unit-V route cut

Fix a partition D=S0 disjoint-union E0 with j0>0. Let v:E0->F^* be
arbitrary. Interpolate V=v and H0=v^(-1), both with degree less than j0, and
set U=A0 H0. Then U vanishes exactly on S0, is nonzero on E0, and

\[
 VH_0\equiv1\pmod{L_0}.
\]

Therefore V ranges over the entire unit group (F[X]/(L0))^*. Rank two plus
one exact anchor alone cannot force V into any proper low-degree, rational,
periodic, or quotient subclass. Such structure must come from an additional
consequence of a large complete-list incidence.

This is a route cut, not a counterexample to the missing census bound.

## 7. M31 specialization and exact remaining theorem

For M31,

\[
\begin{aligned}
 p&=2^{31}-1,\quad F=\mathbb F_{p^4},\\
 n&=2^{21}=2\,097\,152,\quad K=2^{20}=1\,048\,576,\\
 a&=1\,116\,023,\quad R=981\,129,\quad
 w=a-K=67\,447,\\
 B_*&=16\,777\,215.
\end{aligned}
\]

Every actual anchor has w0>=67447. Every nonanchor therefore has

\[
 0\le t\le913\,681,\qquad
 67\,448\le m\le981\,129-t,\qquad
 g=m+t,\qquad \deg b<m-67\,447.
\tag{7.1}
\]

Here

\[
 B_*+1=16\,777\,216<|F|=p^4.
\tag{7.2}
\]

By Corollary 3.3, the direct M31 row closes if and only if it closes for
received words with a boundary anchor.  For such an anchor \(j_0=R\),
\(t=0\), \(w_0=w\), and \(m=g\).  Thus the exact remaining theorem is

\[
 \sum_{\substack{G\mid A_0\ {\rm monic}\\67\,448\le g\le981\,129}}
 \#\left\{b:
 \begin{array}{l}
  b\ne0,\ \deg b<g-67\,447,\ \gcd(b,G)=1,\\
  \deg\gcd(L_0,G-bV)\ge g
 \end{array}\right\}
 \le16\,777\,214
\tag{7.3}
\]

uniformly for every boundary-anchor M31 triple \((A_0,L_0,V)\).  The unit
\(V\) remains arbitrary.  Equation (7.3) counts companions at every exact
weight and already deduplicates the complete list relative to the anchor.
The current stack does not prove (7.3).

In v4 ledger terms, the theorem supplies a canonical diagnostic coordinate
for every residual codeword. It does not assign those codewords to a paid
atom and does not prove the signed Xi46 gate. Ledger movement is zero.

## 8. Upstream and literature compatibility

PR #1051 proves a quotient-rotation LIST lower construction on a different
multiplicative-coset row. It supplies no M31 payment, but it is a mandatory
falsifier for a domain-uniform or support-only attempt at (7.3): a successor
must route that quotient-prefix family or use a genuinely fixed-Chebyshev
primitive hypothesis.

Generic-domain and folded block-metric capacity theorems likewise do not
bound (7.3) for the fixed scalar Chebyshev domain. A plausible successor is
a weighted Chebyshev-folded incidence theorem expressed directly through
gcd(L0,G-bV), with exact partial-fiber and cross-weight credits.

## 9. Proof audit

Statement audited:

The exact bijection (3.4), its M31 specialization (7.3), the fresh-symbol
boundary reduction, and the implication
from one exact anchor to structural restrictions on V.

Dependencies:

- PROVEN: interpolation, the module basis, four-cell exactness, the
  bijection, exact locator/weight, fresh-symbol boundary forcing, M31
  arithmetic, and arbitrary unit-V realization.
- PROVEN TOY CONTROL: exhaustive prime-field and characteristic-two checks.
- UNPROVEN: (7.3), every new owner payment, and the signed Xi46 inequality.

Parameter dependence:

Theorem 3.1 is field- and domain-generic for distinct evaluation points. The
degree floor and census target in Section 7 use the exact M31 row.

Layer-cake / dyadic summability:

Not applicable. Equation (3.4) is an exact finite identity with no error.

Moment / Markov / Chebyshev:

Not applicable. Chebyshev names the deployed evaluation-domain fold.

Edge cases:

The module orientation is (2.1), b is nonzero, every gcd is the full monic
gcd, and j0=0 is separate. The pair census is canonical relative to a chosen
actual anchor, not globally across different anchors.

Verdict:

YELLOW. The exact all-weight reduction and generic-V route cut are proved,
but the M31 pair-census upper bound remains open.

Maximal next action:

Attack (7.3) directly for \(t=0\) and arbitrary unit \(V\). Derive a weighted
Chebyshev-folded affine-containment/Wronskian dichotomy for the exact
gcd-incidence matrix.
Every component must either fit the complete census budget, route to a named
v4 owner with disjoint add-back, or survive as an explicit primitive route
cut. Do not return to a fixed-width boundary chart.
