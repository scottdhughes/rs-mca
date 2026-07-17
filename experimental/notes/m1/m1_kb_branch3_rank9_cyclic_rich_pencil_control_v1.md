# M1 rank-nine cyclic rich-pencil complete-selector control v1

- **Status:** PROVED exact cyclic toy closure / PROVED incomplete rank-nine
  countercontrol / deployed row OPEN / no ledger movement.
- **Scope:** the smallest row in the two-sparse, one-moving-root,
  high-carrier rank-nine ansatz.  It is not the KoalaBear domain or a deployed
  first-match census.
- **Predecessors:**
  `m1_kb_branch3_rank9_rich_pencil_atlas_v1.md`,
  `m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md`, and
  `m1_kb_branch3_low_excess_carrier_cut_v1.md`.
- **Companion checks:**
  `verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.sage` and
  `verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py`.

The rich-pencil atlas predecessor asks for an exact cyclic extension-field
control with one 21-slope rich pencil and the eight outlier directions needed
for intrinsic affine rank nine.  Such a selector exists.  It is not complete
on the bad-slope set.

The same cyclic model has a stronger resolution: all 66 noncontained bad
slopes admit one explicit complete selector with minimum affine rank two and
minimum carrier excess one.  The already proved existential complete-selector
owner therefore
routes the entire toy family to

~~~text
CERTIFIED_LOW_EXCESS_COMMON_CARRIER.
~~~

Thus the incomplete rank-nine selector is a valid local stress test of the
atlas identity, but it cannot be promoted to a first-match residual for this
toy received pair.

## 1. Exact cyclic Reed--Solomon row

Let

\[
 F=\mathbb F_{67^2}
  =\mathbb F_{67}[u]/(u^2+63u+2),
 \qquad |u|=4488,
\]

and put

\[
 \omega=u^{132}=55u+41,
 \qquad |\omega|=34,
 \qquad D=\{\omega^i:0\le i<34\}.
\]

Use

\[
 (n,k,R,j,A,t)=(34,13,21,20,14,1),
 \qquad C=\operatorname{RS}_F(D,13).
\tag{1.1}
\]

Write \(a=D_0=1\), \(b=D_1=\omega\), and

\[
 B=\{2,3,\ldots,33\}.
\]

The received pair is the two-coordinate pair

\[
 \epsilon_0=e_a,
 \qquad \epsilon_1=e_b.
\tag{1.2}
\]

Its syndrome plane has rank two.  It is not defined over the proper subfield:
if \(Y=[H\epsilon_0\ H\epsilon_1]\), exact Frobenius arithmetic gives

\[
 \operatorname{rank}_F Y=2,
 \qquad
 \operatorname{rank}_F[Y\mid Y^{(67)}]=3.
\tag{1.3}
\]

For every 12-set \(S\subset B\), define

\[
 P_S(X)=\prod_{i\in S}(X-D_i),
 \qquad
 q_S=P_S/P_S(a),
 \qquad
 \eta_S=q_S(b),
\tag{1.4}
\]

and

\[
 e_S=\epsilon_0+\eta_S\epsilon_1-\operatorname{ev}_D(q_S).
\tag{1.5}
\]

Then \(q_S\in C\) has degree 12 and

\[
 Z(e_S)=\{a,b\}\sqcup S,
 \qquad
 \operatorname{wt}(e_S)=20.
\tag{1.6}
\]

These are actual RS witnesses, not synthesized support masks.

## 2. The incomplete 29-slope rank-nine control

Take the 11-point core

~~~text
(4, 5, 13, 15, 16, 19, 21, 22, 27, 28, 30)
~~~

and all 21 root sets obtained by adding one point of its complement in \(B\).
Add the following eight root sets:

~~~text
(3,4,5,6,7,13,17,23,24,25,30,31)
(5,6,7,8,13,15,16,18,21,23,24,32)
(3,5,7,10,13,14,15,17,20,21,24,30)
(2,5,7,9,10,20,22,23,24,28,30,33)
(2,5,15,16,18,19,20,23,24,30,31,33)
(5,7,8,9,11,13,15,19,20,25,31,33)
(7,12,14,15,17,19,20,25,26,31,32,33)
(3,4,8,15,17,22,24,25,26,28,29,30)
~~~

The 29 slopes are distinct and lie in \(F\setminus\mathbb F_{67}\).  Exact
linear algebra gives

\[
 \dim\operatorname{span}\{e_\eta-e_{\eta_0}\}=9,
 \qquad
 \operatorname{rank}[e_\eta]=10,
 \qquad
 \dim K_0=8.
\tag{2.1}
\]

The first two rich supports and the eight outlier supports recover the full
32-point carrier, so

\[
 N_V=32,
 \qquad \nu=N_V-R=11.
\tag{2.2}
\]

The canonical graph-line atlas has exactly one nontrivial line.  It has

\[
 (J_L,M_L,x_L,(\delta_\eta),|Z_L|)
 =(21,21,1,(0^{21}),11).
\tag{2.3}
\]

Every eight-subset of \(Z_L\) is a \(K_0\)-basis, hence

\[
 \beta_L=\binom{11}{8}=165.
\tag{2.4}
\]

Direct mask enumeration and the atlas identity agree:

\[
 \mathcal E_{20}^{\rm direct}
 =\mathcal E_{20}^{\rm atlas}
 =165.
\tag{2.5}
\]

There are 14,355 candidate mask--basis incidences, 14,198 valid incidences,
10,898 distinct valid bases, and maximum multiplicity 21.  The codeword
pencil has GCD degree 11 and sparse plant size two.

This selector is complete only on its declared 29-slope set.  It is not a
complete selector of the received pair.

## 3. Hankel, noncontainment, and cyclic-owner checks

Let

\[
 \lambda_x=\left(\prod_{y\in D\setminus\{x\}}(x-y)\right)^{-1}.
\]

Because \(D\) is the root set of \(X^{34}-1\),

\[
 \lambda_x=x/34.
\tag{3.1}
\]

For each selected actual support \(E=B\setminus S\), with locator \(L_E\),
the exact \(t=1\) Hankel equations are

\[
 (H_1+\eta H_2)\ell_E=0,
 \qquad
 H_2\ell_E=\lambda_bL_E(b)\ne0.
\tag{3.2}
\]

The same moment-one minor is regular on all selected slopes:

\[
 \lambda_a a+\eta\lambda_b b\ne0.
\tag{3.3}
\]

Moreover,

\[
 \operatorname{rank}H_E=20,
 \qquad
 \operatorname{rank}H_{E\cup\{b\}}=21.
\tag{3.4}
\]

None of the 29 supports is periodic, and none satisfies the positive-core raw
Q0 predicate at \(c=2\) or \(c=17\).  These local checks do not turn the
incomplete selector into a first-match residual.

## 4. Exact 66-slope frontier

For \(i\in B\), put

\[
 r_i=\frac{b-D_i}{a-D_i}.
\tag{4.1}
\]

The slope attached to \(S\) is \(\prod_{i\in S}r_i\).  Exact subset-product
dynamic programming over all

\[
 \binom{32}{12}=225{,}792{,}840
\]

root sets finds exactly 66 noncontained slopes.  This is the complete
nonzero, noncontained radius-20 frontier: for a nonzero polynomial of degree
at most 12, fourteen agreements force exactly 12 roots in \(B\) and agreement
at both sparse coordinates.

The declared rank-nine selector covers 29 of these slopes and leaves 37.  A
selected slope has between 3,420,854 and 3,421,402 possible 12-root witnesses.
Thus one witness per declared slope is not a witness-exhaustive inventory.

There is also a later-owner projection that must not be confused with the
chosen selectors.  Exactly

\[
 \binom{15}{10}=3003
\]

actual supports are unions of ten available shift-17 pairs.  They are both
shift-17 periodic and raw Q0 at \(c=2\), and their slope projection covers all
66 frontier slopes, with 41 to 51 such witnesses per slope.  Raw Q0 at
\(c=17\) is impossible: its two 17-point fibres contain index 0 or index 1,
while every noncontained support is a subset of
\(B=\{2,\ldots,33\}\).  This existential periodic/Q0 inventory does not
affect the closure below because the branch-3 low-carrier owner is earlier.

## 5. Complete-selector closure

Let \(h=63\in F\), which has order 66.  Relative to \(r_2\), the exponents of
the 32 ratios \(r_i\), in the order \(i=2,\ldots,33\), are

~~~text
0,54,3,24,63,1,64,46,48,27,5,36,44,7,49,23,
17,57,33,62,4,35,13,58,60,42,39,43,16,37,52,40.
~~~

Fix the ten-root core

~~~text
C = (5, 7, 8, 9, 11, 15, 18, 20, 24, 33).
~~~

Its complement in \(B\) has 22 points.  The pairwise sums of their relative
exponents cover every residue modulo 66.  For each residue, choose the
lexicographically first pair and use

\[
 S=C\sqcup\{i,j\}.
\tag{5.1}
\]

This gives exactly one selected witness at every one of the 66 frontier
slopes.  Exact replay proves

\[
 \text{affine rank}=2,
 \qquad
 \text{raw rank}=3,
 \qquad
 \deg\gcd(q_S:S)=10.
\tag{5.2}
\]

The affine-linear difference map from normalized code polynomials to errors is

\[
 T(h)=h(b)e_b-\operatorname{ev}_D(h).
\]

It is injective on polynomials of degree at most 12: if \(T(h)=0\), then
\(h\) vanishes at the 33 points \(D\setminus\{b\}\), so \(h=0\).  Hence the
polynomial and error families have the same affine rank.

The affine rank two is exact, not merely an upper bound.  If a complete
selector of 66 normalized degree-at-most-12 polynomials lay on an affine line,
let \(c\) be the number of common roots in \(B\).  A noncommon coordinate can
be a root of at most one line point, so

\[
 66\cdot12\le66c+(32-c)=65c+32.
\]

Hence \(c\ge12\).  The line direction also vanishes at \(a\), because every
selected polynomial is normalized to \(q(a)=1\).  A nonzero direction of
degree at most 12 would therefore have at least 13 roots, a contradiction.
Thus every complete selector has affine rank at least two, and the displayed
selector attains it.

The union of all selected error supports is exactly \(B\setminus C\), so

\[
 N_V=22,
 \qquad
 \kappa=N_V-R=1\le10.
\tag{5.3}
\]

This carrier excess is also minimal.  If a complete selector had carrier
\(U\) with \(|U|\le21\), every 12-root set would contain the common core
\(B\setminus U\) of size at least 11.  A core of size 11 permits at most
\(|U|\le21\) distinct one-point extensions, a core of size 12 permits one,
and a larger core is impossible.  None can cover 66 distinct slopes.  Thus
\(\kappa_*\ge1\), while the lexicographic selector proves \(\kappa_*\le1\).

The integrated global-carrier owner is existential over complete selectors.
Consequently this one complete selector pays the safe branch-3 successor
envelope before the incomplete rank-nine selector can define a residual:

\[
 B_1=
 \frac{\binom{22}{2}}{\binom{1}{1}}
 =231\ge66.
\]

~~~text
CERTIFIED_LOW_EXCESS_COMMON_CARRIER.
~~~

Because literal branch-1 survival is intentionally unresolved, the precise
first-match statement is that every toy slope terminates at or before this
branch-3 low-excess gate; the packet does not assign an exact earlier owner.

The chosen complete selector has zero periodic supports and zero positive-core
Q0 supports at \(c=2,17\).  This selected-support statement is compatible
with the separate 3003-witness existential Q0 projection recorded above.

## 6. Minimality and scope

Within the two-sparse, one-moving-root, high-carrier rank-nine ansatz:

- \(J\ge21\) forces \(R\ge21\);
- carrier excess at least 11 forces \(k-2\ge11\), hence \(k\ge13\);
- therefore \(n\ge34\);
- a rich affine line contributes rank one, so eight outliers are necessary
  for affine rank nine.

If an order-34 cyclic group lies in \(\mathbb F_{p^e}^{\times}\) for
\(e\in\{2,6\}\), then the order of \(p\) modulo 17 divides both 16 and \(e\),
so \(p\equiv\pm1\pmod {17}\).  The smallest possible prime is \(p=67\).
Thus this row is minimal inside the stated ansatz.

This packet does not:

- instantiate the KoalaBear field or its order-\(2^{21}\) domain;
- prove a deployed complete-selector inventory;
- prove global branch-1 survival for the two-sparse pair;
- pay the deployed rich-pencil aggregate;
- move \(U_{\rm paid}\) or \(B_{\rm rem}\);
- close deployed rank nine, \(U_Q\), or \(U_A\);
- authorize Lean or stable-paper promotion.

The exact conclusion is a toy closure and a route-design warning: incomplete
rank-nine selectors can display the hostile local atlas geometry even when a
different complete selector routes the whole family to an earlier paid owner.

## 7. Replay

~~~bash
HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.py \
  --tamper-selftest
~~~

- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** all arithmetic is exact toy-scale Sage arithmetic;
  it is not asymptotic or deployed evidence.
- **Verdict:** GREEN for this cyclic toy closure; YELLOW for any deployed
  implication.
