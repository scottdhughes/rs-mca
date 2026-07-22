# M31 order-32 Chebyshev maximum fiber and rotation route cut

**Date:** 2026-07-22
**Row:** Mersenne-31 LIST at target 2^-100
**Workboard item:** M0/M1
**Unit:** distinct codewords per received word
**Status:** exact deployed computation and symbolic route cut; row open

## 1. Result

Let

\[
p=2^{31}-1,\quad n=2^{21},\quad K=2^{20},\quad
A=1{,}116{,}023,\quad B_*=2^{24}-1,
\]

and put \(c=2^{16}\). On the pinned M31 Chebyshev domain,

\[
D=Z_{\mathbb F_p}(T_n),\qquad
Q=T_c(D),\qquad |Q|=32,
\]

with every fiber of \(T_c:D\to Q\) of size \(c\). Scaling the quotient
coordinate by a nonzero constant gives the 32 roots of \(T_{32}(2Y)\);
this bijective scaling does not change subset-sum fiber cardinalities.

For every \(b_0\in Q\), the exact deployed census proves

\[
\max_{z\in\mathbb F_p}
\#\left\{M\in\binom{Q\setminus\{b_0\}}{17}:
\sum_{b\in M}b=z\right\}
=\binom{15}{8}=6435.
\]

The maximizing key is unique and equals \(-b_0\). Its 6435 members are
exactly

\[
\{-b_0\}\ \cup\
\bigcup_{j\in J}\{u_j,-u_j\},
\qquad J\in\binom{[15]}8,
\]

where the other 30 quotient points form 15 antipodal pairs. Thus the
largest fiber is a visible \(T_2\)/antipodal quotient family rather than a
primitive residual.

This is a sharp route cut, not row safety:

\[
6435 < B_*+1=16{,}777{,}216.
\]

It eliminates the complete scale-\(2^{16}\), order-32, one-prefix
counterexample construction. It does not upper-bound arbitrary M31 lists,
move a Grande Finale v4 ledger atom, or close the row.

Both the literal cyclic rotation copied from the multiplicative quotient and
the intrinsic \(T_{31}\) Chebyshev rotation are even more rigid: their
deployed high-prefix maps are injective. Every rotated prefix fiber has size
one.

## 2. Exact lift from a quotient fiber to an M31 list

Fix \(b_0\in Q\), a set

\[
R_0\subset T_c^{-1}(b_0),\qquad |R_0|=1911,
\]

and its monic locator \(E(X)\). The exclusion \(b_0\notin M\) is
load-bearing. For

\[
M\in\binom{Q\setminus\{b_0\}}{17},\qquad
P_M(Y)=\prod_{b\in M}(Y-b)
=Y^{17}-e_1(M)Y^{16}+\cdots,
\]

define

\[
L_M(X)=E(X)P_M(T_c(X)).
\]

If \(e_1(M)=\xi\), use the common received polynomial

\[
U_\xi(X)=E(X)\bigl(T_c(X)^{17}-\xi T_c(X)^{16}\bigr)
\]

and the codeword polynomial \(f_M=U_\xi-L_M\). Since

\[
15c+1911=984{,}951<K<16c+1911=1{,}050{,}487,
\]

we have \(\deg f_M\le984{,}951<K\). On \(D\), \(f_M\) agrees with
\(U_\xi\) exactly on

\[
R_0\sqcup T_c^{-1}(M),
\]

whose size is

\[
1911+17c=1{,}116{,}023=A.
\]

Outside this support, \(f_M-U_\xi=-L_M\ne0\). Different \(M\)'s give
different monic locators and hence different codewords. Therefore a
quotient sum fiber of size \(L\) produces exactly \(L\) distinct base-field
RS codewords in one radius-\(n-A=981{,}129\) ball. The base-field list
embeds in the deployed extension-field code. There is no additional zero anchor,
so a row counterexample requires \(L\ge B_*+1\).

## 3. Exhaustive deployed census

The certificate uses the 32 attained normalized quotient labels

    1515618352 2142581798 519472958 942646298
    419097603 7265015 1945140650 1179963362
    970712266 1077313983 114254582 186614876
    869502427 1006664095 2113254329 1972112504
    175371143 34229318 1140819552 1277981220
    1960868771 2033229065 1070169664 1176771381
    967520285 202342997 2140218632 1728386044
    1204837349 1628010689 4901849 631865295

over \(\mathbb F_p\). The replay verifies that they are distinct roots of
\(T_{32}(2Y)\), have total sum zero, and satisfy
\(q_i=-q_{31-i}\).

For a fixed omission, the C++ verifier splits the remaining 31 labels into
halves of sizes 15 and 16, enumerates all subset sums by cardinality, joins
the cardinalities totaling 17, materializes exactly

\[
\binom{31}{17}=265{,}182{,}525
\]

residues, sorts them, and scans every run. There is no sampling, hash
collision assumption, floating-point arithmetic, or randomization. The
Python verifier checks 16 omissions exhaustively and transports the other
16 by the exact negation involution. The C++ implementation also provides
an all-punctures mode.

The numbers of distinct sums for omission indices \(0,\ldots,31\) are

    14269003 14244093 14262839 14249825 14244487 14249841 14262617 14247825
    14253497 14262119 14304595 14248081 14263481 14290175 14257265 14306833
    14306833 14257265 14290175 14263481 14248081 14304595 14262119 14253497
    14247825 14262617 14249841 14244487 14249825 14262839 14244093 14269003

Every omission has maximum multiplicity 6435, exactly one maximizing key,
and maximizing key equal to the negative of the omitted label. The explicit
antipodal family supplies the matching lower bound
\(\binom{15}{8}=6435\); the exhaustive run supplies the upper bound and
uniqueness.

This is an exact finite computational theorem. It is not promoted into an
unproved symbolic inequality about larger quotient sizes.

## 4. Why neither quotient rotation produces a large fiber

### 4.1 Literal multiplicative-style rotation

Let

\[
\Lambda_Q(Y)=2^{-31}T_{32}(Y)
\]

be the monic unscaled quotient locator, and imitate the multiplicative
rotation by

\[
R_M(Y)=Y^{31}P_M(Y)\bmod\Lambda_Q(Y).
\]

The root identity survives: \(0\notin Q\), so
\(R_M(q)=q^{31}P_M(q)\) at every \(q\in Q\). The desired prefix
compression does not survive. Put

\[
\rho_j=Y^{31+j}\bmod\Lambda_Q,\qquad 0\le j\le16.
\]

Exact Sage linear algebra gives

\[
\operatorname{rank}
\left([Y^k]\rho_j\right)_{
16\le k\le31,\ 0\le j\le16}=16.
\]

Its one-dimensional kernel is generated, with constant coefficient one,
by

\[
\begin{aligned}
K_0(Y)={}&1+922883926Y^2+1787128909Y^4+237254192Y^6\\
&+577962578Y^8+30724201Y^{10}+53081916Y^{12}\\
&+1776865326Y^{14}+821554693Y^{16}.
\end{aligned}
\]

The same replay verifies

\[
\deg(Y^{31}K_0\bmod\Lambda_Q)\le15,
\qquad \gcd(K_0,\Lambda_Q)=1.
\]

If two distinct 17-subsets \(M,N\subset Q\setminus\{b_0\}\) had the
same rotated high part, then

\[
P_M-P_N=tK_0
\]

for some \(t\ne0\). A common element of \(M\cap N\) would be a common
root of \(K_0\) and \(\Lambda_Q\), impossible. Thus
\(M\cap N=\varnothing\). But two 17-subsets of a 31-point set cannot be
disjoint. The rotated map is therefore injective.

### 4.2 Intrinsic Chebyshev rotation

The quotient-intrinsic analogue replaces the monomial multiplier by

\[
R_M^{\rm Ch}(Y)=T_{31}(Y)P_M(Y)\bmod T_{32}(Y).
\]

Let \(U_j\) be the second-kind Chebyshev polynomials, normalized by
\(U_0=1\) and \(U_1=2Y\). The Sage replay derives over the integers, for
\(0\le j\le16\),

\[
T_{31}U_j\equiv T_{31-j}\pmod{T_{32}}.
\]

For \(j\ge1\), it verifies the stronger exact identity

\[
T_{31}U_j=T_{31-j}+T_{32}U_{j-1}.
\]

Consequently the intrinsic degree-16-through-31 high map again has shape
\(16\times17\), rank 16, and one-dimensional kernel, now generated exactly
by \(U_{16}\). The integral resultant is

\[
\operatorname{Res}_{\mathbb Z}(U_{16},T_{32})=2^{496},
\]

so \(U_{16}\) and \(T_{32}\) are coprime modulo the odd deployed prime.
The same common-root argument proves injectivity on every punctured
17-subset family. Thus the intrinsic Chebyshev rotation also has maximum
prefix fiber one.

The obstruction is structural: monomial rotation on the norm-one torus
does not descend through the inversion quotient to the Chebyshev
coordinate. Reduction modulo \(T_{32}\) spreads the high coefficients
through both parity blocks instead of compressing them to one coordinate;
the intrinsic \(T_{31}\) multiplier refines all the way to an injective
prefix instead.

## 5. Higher-MDS diagnostic

For a fixed puncture \(Q'=Q\setminus\{b_0\}\), a common-sum fiber is a
list in the quotient code
\(\operatorname{RS}[\mathbb F_p,Q',16]\), with agreement 17 and distance
14. By Brakensiek--Gopi--Makam, arXiv:2206.05256v4, Theorem 1.13, the
dual \(\mathrm{MDS}(15)\) condition would imply
\(\mathrm{LD\text{-}MDS}(\le14)\). Fifteen such codewords would then be
forbidden because

\[
15\cdot14=14(31-16).
\]

The exact 6435-member fiber shows that this structured specialization is
not \(\mathrm{LD\text{-}MDS}(\le14)\), and therefore the required dual
higher-MDS gate fails for every puncture. Generic RS higher-MDS theorems
cannot be specialized to this deterministic Chebyshev domain without
classifying precisely this antipodal degeneracy.

Ordinary MDS, distinct evaluation points, or a higher-MDS statement for the
wrong primal code would not prove the needed implication.

## 6. Scope, nonclaims, and next terminal

This packet proves all of the following:

1. the quotient-fiber-to-M31-list lift is exact;
2. every deployed order-32 one-sum fiber has maximum 6435;
3. the unique maximum is the antipodal \(T_2\) family;
4. both the literal multiplicative-style and intrinsic Chebyshev rotation
   adapters have fiber size one; and
5. the tempting generic higher-MDS shortcut fails on the deployed quotient.

It does **not** prove M31 row safety, a global U_Q, the arbitrary-unit
boundary census, or the uniform deterministic punctured-RS cap. Ledger movement is zero.

The next maximal exact quotient attack is the scale-\(2^{15}\), order-64,
two-prefix map on 34 moving quotient labels (with the same 1911-point
partial fiber), together with an exhaustive owner decomposition of every
large two-prefix fiber. A successful result must either exceed
\(B_*+1\), prove a source-bound global payment, or cut that entire rung.
The broader fixed-\(G\) ordinary-RS and varying-\(G\) incidence terminals
remain open in parallel. The exact next terminal is
UNPAID_C32768_ORDER64_TWO_PREFIX_OR_GLOBAL_Q_AGGREGATION.

## 7. Review status

A fresh proof audit independently checked the quotient lift, the exact
degree and agreement arithmetic, codeword distinctness, extension-field
embedding, and the \(B_*+1\) endpoint. The exhaustive C++ census and Sage
rotation computation are separately replayable. No Lean claim is made;
Axle was used only as a capability smoke test on an unrelated deliberately
false toy theorem and is not evidence for this packet.
