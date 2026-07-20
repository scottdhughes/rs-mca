# M1 KoalaBear one-slack moving-cofactor Frobenius owner v1

Status: **PROVED LOCAL PAIR-GLOBAL SOURCE-FROBENIUS OWNER / PROVED EXACT
FIRST-MATCH DELETION AND SELECTOR RESTART / MOVING-COFACTOR ONE-SLACK
COMPONENT CLOSED / INDEPENDENT PROOF, GEOMETRY, AND ARTIFACT REVIEWS GREEN /
KOALABEAR ROW OPEN**.

This packet closes the second primitive one-slack component left by the
moving-root slack theorem:

```text
UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR.
```

For the fixed translated source pair, put

\[
 S_a(Z)=\epsilon _0(a)+Z\epsilon _1(a)
 \qquad(a\in\Sigma).
\]

Every selected member in the moving-cofactor cell makes every four-anchor
determinant

\[
 E_T(Z)=\det_{a\in T}
 \begin{bmatrix}
 aS_a(Z)^p&S_a(Z)^p&aS_a(Z)&S_a(Z)
 \end{bmatrix}
\tag{0.1}
\]

vanish at its slope.  The determinant has degree at most \(2p+2\).  The
load-bearing point is that, whenever a qualifying record exists, at least one
of the polynomials (0.1) is nonzero.  If all were zero, the fixed source
would either descend to a degree-at-most-one rational map, contradicting the
proved reduced-degree floor, or would produce \(|F|\) distinct lines in one
ruling of a smooth quadric while only \(|\Sigma|\) singular opposite-ruling
lines are available.

Choose the first nonzero determinant using the fixed domain order, charge its
finite incoming roots once, delete them, and rebuild every selector-derived
object.  This gives the pair-global cap

\[
 2p+2=4{,}261{,}412{,}868.
\tag{0.2}
\]

It closes the moving-cofactor one-slack component, but it does not close rank
nine or KoalaBear.

## 1. Frozen row, source, and first-match position

Fix

\[
 p=2{,}130{,}706{,}433,
 \qquad B=\mathbf F_p\subset F=\mathbf F_{p^6},
 \qquad D\subset B^\times,
\]

\[
 n=2^{21}=2{,}097{,}152,
 \quad k=2^{20}=1{,}048{,}576,
 \quad A=1{,}116{,}048,
\]

\[
 j=n-A=981{,}104,
 \qquad t=A-k=67{,}472.
\tag{1.1}
\]

Fix one received pair and the one SP3 translation used for that pair.  Write

\[
 (\epsilon _0,\epsilon _1),\qquad
 \Sigma=\operatorname{supp}(\epsilon _0)
       \cup\operatorname{supp}(\epsilon _1)\subseteq D,
 \qquad s=|\Sigma|.
\tag{1.2}
\]

At every \(a\in\Sigma\), the source pair is nonzero.  The pair, its support,
its domain order, and all values \(S_a(Z)\) precede every selector choice.
No union over alternative translations is allowed.

Let \(\Gamma_{\rm in}\) be the exact finite residual slope set after the
canonical C5, bounded-degree source--rational, and common-twist source-subline
owners.  The relevant first-match segment is

```text
projective_base_pair_C5
source_rational_full_outside_bounded_degree
source_subline_common_linear_gcd_twist
source_frobenius_moving_linear_cofactor
residual_extension_valued_strata
residual_base_slope_universe.
```

All statements below are subset-stable: for every
\(\Gamma\subseteq\Gamma_{\rm in}\), they quantify over every complete
selector rebuilt on \(\Gamma\) and every qualifying record in that selector.

## 2. Exact moving-cofactor normal form

Fix a qualifying full-outside coefficient-rank-two rich record after the
earlier deletions and restarts.  The moving-root slack theorem gives

\[
 s=t+2=67{,}474,
 \qquad(h,u,\ell)=(0,1,0),
\tag{2.1}
\]

\[
 H=L_C\in B[X],
 \qquad e=x+1,
 \qquad33{,}736\le x\le49{,}055,
\tag{2.2}
\]

where \(H=\gcd(P,Q)\) is monic and

\[
 P=H\bar P,\qquad Q=H\bar Q,\qquad
 \gcd(\bar P,\bar Q)=1,
 \qquad\max(\deg\bar P,\deg\bar Q)=e.
\tag{2.3}
\]

For every selected finite slope \(\eta\),

\[
 \bar P+\eta\bar Q=L_{F_\eta}A_\eta,
 \qquad\deg A_\eta\le1-\delta_\eta,
 \qquad\delta_\eta\in\{0,1\}.
\tag{2.4}
\]

Here \(F_\eta\subseteq W\subseteq D\setminus\Sigma\), the sets
\(F_\eta\) are pairwise disjoint, and

\[
 |F_\eta|=x+\delta_\eta.
\tag{2.5}
\]

A member is **projectively base-defined** if
\(\bar P+\eta\bar Q\) is a nonzero scalar multiple of a polynomial in
\(B[X]\).  This includes every \(\delta_\eta=1\) member, every constant
cofactor, and every linear cofactor whose root belongs to \(B\).  Two such
members give a base-polynomial basis for the reduced pencil and are already
owned by C5.  Thus a primitive surviving record has at most one
projectively base-defined member and at least \(J_L-1\ge20\) genuine
nonbase members.

For every genuine nonbase member, (2.4) has the exact form

\[
 \boxed{
 \bar P+\eta\bar Q
 =\kappa_\eta L_{F_\eta}(X)(X-\zeta_\eta),
 \qquad
 \kappa_\eta\in F^\times,
 \quad\zeta_\eta\in F\setminus B.}
\tag{2.6}
\]

Moreover,

\[
 |C|+|F_\eta|=c+x=A-s=k-2,
\tag{2.7}
\]

so the unreduced polynomial member has the sharper form

\[
 P+\eta Q
 =\kappa_\eta L_{C\sqcup F_\eta}(X)(X-\zeta_\eta),
 \qquad\deg L_{C\sqcup F_\eta}=k-2.
\tag{2.8}
\]

No regular-chart equation or rank-nine outlier direction is discarded here.
The theorem below is a necessary source-only condition for every record
satisfying all inherited contracts.

## 3. Source Frobenius fingerprint

For \(a\in\Sigma\), define

\[
 S_a(Z)=\epsilon _0(a)+Z\epsilon _1(a)\in F[Z].
\tag{3.1}
\]

Source coupling and \(H=L_C\in B[X]\) give, at a selected slope,

\[
 S_a(\eta)=P(a)+\eta Q(a)
 =H(a)(\bar P(a)+\eta\bar Q(a)).
\tag{3.2}
\]

For a genuine nonbase member, (2.6) and (3.2) imply

\[
 S_a(\eta)
 =\kappa_\eta b_{a,\eta}(a-\zeta_\eta),
 \qquad b_{a,\eta}=H(a)L_{F_\eta}(a)\in B^\times.
\tag{3.3}
\]

The base scalar disappears after taking the \((p-1)\)-st power:

\[
 \boxed{
 S_a(\eta)^{p-1}
 =\kappa_\eta^{p-1}
  \frac{a-\zeta_\eta^p}{a-\zeta_\eta}.}
\tag{3.4}
\]

Equivalently, with \(c_\eta=\kappa_\eta^{p-1}\),

\[
 aS_a(\eta)^p-\zeta_\eta S_a(\eta)^p
 -c_\eta aS_a(\eta)+c_\eta\zeta_\eta^pS_a(\eta)=0.
\tag{3.5}
\]

For a four-subset \(T\subseteq\Sigma\), define the source-only polynomial

\[
 \boxed{
 E_T(Z)=\det_{a\in T}
 \begin{bmatrix}
 aS_a(Z)^p&S_a(Z)^p&aS_a(Z)&S_a(Z)
 \end{bmatrix}.}
\tag{3.6}
\]

Equation (3.5) supplies a nonzero right-kernel vector for the four rows, so

\[
 E_T(\eta)=0
\tag{3.7}
\]

for every genuine nonbase member and every \(T\).  If the member is
projectively base-defined, then
\(S(\eta)^p=cS(\eta)\) coordinatewise for one \(c\in F^\times\), so the
first two determinant columns are scalar multiples of the last two.  Thus
(3.7) also holds for the exceptional projectively base-defined member.

Two columns of (3.6) have degree \(p\), and two have degree one.  Therefore

\[
 \boxed{\deg E_T\le2p+2.}
\tag{3.8}
\]

The determinant uses only the fixed source pair.  It contains no selector,
carrier, graph line, support, cofactor, or recovered pole.

## 4. A nonzero four-anchor eliminant must exist

### Lemma 4.1 (source Frobenius nondegeneracy)

If a qualifying record from Section 2 exists, then

\[
 \boxed{E_T\ne0\text{ in }F[Z]
 \quad\text{for some }T\in\binom\Sigma4.}
\tag{4.1}
\]

#### Proof

Write

\[
 u=(\epsilon _0(a))_{a\in\Sigma},\qquad
 v=(\epsilon _1(a))_{a\in\Sigma},\qquad
 M=\operatorname{diag}(a)_{a\in\Sigma}.
\tag{4.2}
\]

The source points are distinct elements of \(B^\times\), so \(M\) is
invertible and has distinct diagonal entries.  Let \(w^{(p)}\) denote
coordinatewise \(p\)-th power.

For every \(y\in F\), source coupling gives

\[
 u+yv=\bigl(H(a)(\bar P(a)+y\bar Q(a))\bigr)_{a\in\Sigma}.
\tag{4.3}
\]

Coefficient rank two makes \(\bar P+y\bar Q\) nonzero, and it has degree at
most \(e\).  Consequently

\[
 |\operatorname{supp}(u+yv)|\ge s-e
 \ge67{,}474-49{,}056=18{,}418>1.
\tag{4.4}
\]

The same bound holds for \(u^{(p)}+zv^{(p)}\), because Frobenius is a
bijection on \(F\).  Hence every plane

\[
 U_y=\operatorname{span}_F\{u+yv,M(u+yv)\},
\qquad
 V_z=\operatorname{span}_F\{u^{(p)}+zv^{(p)},
 M(u^{(p)}+zv^{(p)})\}
\tag{4.5}
\]

has dimension two.

Assume for contradiction that every \(E_T\) is the zero polynomial.  The
four-vector wedge whose coordinates are those minors is then identically
zero:

\[
 \begin{aligned}
 &M(u^{(p)}+Z^pv^{(p)})\wedge(u^{(p)}+Z^pv^{(p)})\\
 &\qquad\wedge M(u+Zv)\wedge(u+Zv)=0.
 \end{aligned}
\tag{4.6}
\]

The first wedge pair is quadratic in \(Z^p\), and the second is quadratic
in \(Z\).  The nine exponents

\[
 ip+j,\qquad0\le i,j\le2,
\tag{4.7}
\]

are distinct because \(p>2\).  Every coefficient in (4.6) therefore
vanishes separately.  Replacing \(Z\) and \(Z^p\) by independent variables
gives

\[
 U_y\cap V_z\ne\{0\}
 \qquad(y,z\in F).
\tag{4.8}
\]

Put

\[
 W_0=\operatorname{span}_F\{u,v,Mu,Mv\}.
\tag{4.9}
\]

Suppose first that \(\dim W_0\le3\).  There are
\(\alpha,\beta,\gamma,\delta\in F\), not all zero, such that

\[
 (\alpha+\gamma a)\epsilon _0(a)
 +(\beta+\delta a)\epsilon _1(a)=0
 \qquad(a\in\Sigma).
\tag{4.10}
\]

Since \(H(a)\ne0\) on \(\Sigma\), source coupling turns (4.10) into

\[
 ((\alpha+\gamma X)\bar P
  +(\beta+\delta X)\bar Q)(a)=0
 \qquad(a\in\Sigma).
\tag{4.11}
\]

The polynomial in (4.11) has degree at most \(e+1\), whereas

\[
 s=67{,}474>49{,}057\ge e+1.
\tag{4.12}
\]

It is therefore identically zero.  Coprimality implies that \(\bar P\)
divides the linear polynomial \(\beta+\delta X\) and \(\bar Q\) divides
\(\alpha+\gamma X\).  Neither linear polynomial is zero: the identity and
the nonzero pair \((\bar P,\bar Q)\) would otherwise force both to vanish.
The reduced map would have degree at most one,
contradicting

\[
 e=x+1\ge33{,}737.
\tag{4.13}
\]

Hence \(\dim W_0=4\).  If
\(E_0=\operatorname{span}\{u,v\}\), then

\[
 W_0=E_0\oplus ME_0.
\tag{4.14}
\]

The projective lines \(\mathbf P(U_y)\) are pairwise skew and lie in one
ruling; together with the omitted line
\(U_\infty=\operatorname{span}\{v,Mv\}\), they form that ruling of the
smooth Segre quadric

\[
 \mathcal Q
 =\{[rw+sMw]:[w]\in\mathbf P(E_0),\ [r:s]\in\mathbf P^1(F)\}
 \subseteq\mathbf P(W_0).
\tag{4.15}
\]

The Frobenius-conjugate space
\(W_0^{(p)}=E_0^{(p)}\oplus ME_0^{(p)}\) also has dimension four.  It
follows that the lines \(\mathbf P(V_z)\), \(z\in F\), are distinct: if
two coincided, that one line would contain both \(E_0^{(p)}\) and
\(ME_0^{(p)}\), contradicting the four-dimensional direct sum.

By (4.8), every \(\mathbf P(V_z)\) meets every line of the first ruling.
Meeting any two puts it inside \(\mathbf P(W_0)\); meeting a third makes it
an opposite-ruling line of (4.15).  Equivalently, for a unique
\([r_z:s_z]\in\mathbf P^1(F)\),

\[
 V_z=(r_zI+s_zM)E_0.
\tag{4.16}
\]

This elementary ruling statement follows directly by writing the three
intersection points as \(r_y(u+yv)+s_yM(u+yv)\) and comparing their
\(E_0\) and \(ME_0\) coordinates; the ratio \([r_y:s_y]\) must be the
same on all three lines.

Let \(R_z=r_zI+s_zM\).  If \(R_z\) were invertible, choose nonzero
\(q\in E_0^{(p)}\) with
\(V_z=\operatorname{span}\{q,Mq\}\).  Write \(q=R_zw\) and
\(Mq=R_zw'\) with \(w,w'\in E_0\).  Since \(R_z\) commutes with \(M\),

\[
 R_zMw=Mq=R_zw',
\]

so invertibility gives \(Mw=w'\in E_0\).  This places the nonzero vector
\(Mw\) in \(E_0\cap ME_0\), contradicting (4.14).  Thus every \(R_z\)
is singular.

Because \(M\) is diagonal, \(rI+sM\) is singular precisely when

\[
 r+sa=0
\tag{4.17}
\]

for some \(a\in\Sigma\).  There are exactly \(s\) such projective
parameters \([r:s]\).  We have obtained at most \(s\) possible distinct
lines \(V_z\), whereas \(z\in F\) supplies

\[
 |F|=p^6>s
\tag{4.18}
\]

distinct lines.  This contradiction proves (4.1). \(\square\)

The proof uses the deployed multiplicative-domain condition
\(D\subset B^\times\).  If zero were admitted as a source coordinate, the
invertibility and singular-line count would have to be restated; that case is
outside this row.

## 5. Pair-global determinantal owner

Order the four-subsets of \(\Sigma\) lexicographically using the fixed domain
order.  From the source data alone, choose the first \(T_*\) for which
\(E_{T_*}\ne0\).  If no such four-set exists, define the owner set to be
empty.  Otherwise put

\[
 \mathcal R_{\rm mov}(\epsilon _0,\epsilon _1)
 =\{\eta\in F:E_{T_*}(\eta)=0\}.
\tag{5.1}
\]

This definition is fail-closed and intrinsic to the fixed source pair.  It
does not choose a determinant from a selector or take a union over
determinants, records, supports, or recovered cofactors.

Let

\[
 Z_{\rm mov}=\Gamma_{\rm in}\cap
 \mathcal R_{\rm mov}(\epsilon _0,\epsilon _1),
 \qquad
 \Gamma_{\rm out}=\Gamma_{\rm in}\setminus Z_{\rm mov}.
\tag{5.2}
\]

### Theorem 5.1 (pair-global moving-cofactor Frobenius owner)

For every \(\Gamma\subseteq\Gamma_{\rm in}\), every qualifying
moving-cofactor one-slack record in every complete selector rebuilt on
\(\Gamma\) satisfies

\[
 \boxed{\Gamma_L^{\rm fin}\subseteq
 \mathcal R_{\rm mov}(\epsilon _0,\epsilon _1).}
\tag{5.3}
\]

Moreover,

\[
 \boxed{
 |Z_{\rm mov}|
 \le|\mathcal R_{\rm mov}|
 \le2p+2=4{,}261{,}412{,}868.}
\tag{5.4}
\]

After the exact deletion (5.2), no such record can occur in a complete
selector rebuilt on \(\Gamma_{\rm out}\).

#### Proof

If a qualifying record exists, Lemma 4.1 makes \(T_*\) exist.  Section 3
then puts every selected slope of every qualifying record among the roots of
the same source-only polynomial \(E_{T_*}\), proving (5.3).  The ordinary
root bound and (3.8) prove (5.4).

The proof uses only the fixed source and record-level hypotheses, so it
applies to every subset \(\Gamma\).  On \(\Gamma_{\rm out}\), (5.2) makes
the right side of (5.3) disjoint from the available finite slopes, proving
the post-restart exclusion. \(\square\)

The paid terminal is

```text
PAID_PAIR_GLOBAL_SOURCE_FROBENIUS_MOVING_LINEAR_COFACTOR.
```

The former terminal

```text
UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR
```

is removed.

## 6. First-match deletion and complete-selector restart

Charge only the exact incoming intersection \(Z_{\rm mov}\), then delete it.
Apply later extension-valued and residual-base owners only to
\(\Gamma_{\rm out}\).  Rebuild, rather than retain, all selector-derived
objects:

1. the complete-selector universe;
2. global carrier and small-family gates;
3. the affine-rank minimizer;
4. the carrier, \(V\), Padé matrices, \(K_0\), and \(d_V\);
5. the deficit histogram and rich-pencil atlas; and
6. every rank-at-most-three, rank-four-through-eight, and rank-nine terminal
   in its frozen order.

Restriction of a former complete selector witnesses nonemptiness of the new
selector universe and gives a new minimum rank no larger than the old one.
No old carrier, graph line, support, basis, chart, determinant mass, witness,
or rank-nine outlier direction is retained.  The fixed source pair and SP3
translation remain unchanged.

## 7. Exact accounting and revised residual floor

The source-Frobenius owner is a new disjoint first-match block, so the
conservative movement is

\[
 \boxed{\Delta U_{\rm paid}=2p+2=4{,}261{,}412{,}868.}
\tag{7.1}
\]

Starting from the banked common-twist packet,

\[
 U_{\rm paid}^{\rm old}=4{,}736{,}269{,}268,
\qquad
 B_{\rm remaining}^{\rm old}
 =274{,}980{,}723{,}375{,}125{,}819,
\tag{7.2}
\]

the new exact values are

\[
 \boxed{U_{\rm paid}^{\rm new}=8{,}997{,}682{,}136,}
\tag{7.3}
\]

\[
 \boxed{
 B_{\rm remaining}^{\rm new}
 =274{,}980{,}719{,}113{,}712{,}951.}
\tag{7.4}
\]

The exact rank-nine one-cut replay gives

\[
 T_{18{,}014}=17{,}900{,}043{,}416{,}181,
\tag{7.5}
\]

\[
 E_{\max}
 =5{,}204{,}235{,}748{,}184{,}821{,}982{,}241{,}887{,}438{,}598{,}935{,}212{,}904{,}144{,}649,
\tag{7.6}
\]

while \(K_{\rm remaining}=4{,}807{,}520\) and the uniform break improves
from \(J=166\) to \(J=164\).  These are downstream exact-arithmetic
consequences, not additional mathematical payment.

The zero-source-slack boundary and all three one-source-slack cells are now
owned.  Therefore every surviving full-outside coefficient-rank-two rich
record satisfies

\[
 \boxed{s\ge t+3=67{,}475.}
\tag{7.7}
\]

The earlier source--rational exclusion then gives

\[
 \boxed{e\ge\left\lceil\frac s2\right\rceil\ge33{,}738,}
\qquad
 \boxed{\deg H\le k-1-e\le1{,}014{,}837.}
\tag{7.8}
\]

The revised full-outside terminal is

```text
UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67475.
```

The packet assigns no value to \(U_Q\) or the remaining \(U_A\), does not
compare the complete upper ledger with the target, and does not alter the
lower reserve.

## 8. Dependencies, residuals, and nonclaims

### Proved in this packet

- the source fingerprint (3.4);
- the four-anchor determinant condition (3.6)--(3.8);
- Lemma 4.1, including both the rational-degenerate and Segre-ruling cases;
- the intrinsic root owner and its \(2p+2\) cap;
- subset-stable deletion and selector restart;
- closure of the moving-cofactor one-slack component; and
- the revised full-outside source, reduced-degree, and gcd floors.

### Imported and payload-bound

- the fixed source pair and SP3 translation;
- the moving-root cofactor divisibility and one-slack simplex;
- full-outside source coupling and \(H=L_C\in B[X]\);
- coefficient rank two, \(\beta_L>0\), and \(J_L\ge21\);
- the earlier C5, source--rational, and common-twist owners;
- exact deletion/restart semantics; and
- the banked paid ledger and one-cut arithmetic.

### Still open

```text
UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67475
UNBOUND_POST_TANGENT_SOURCE_LOAD
UNPAID_U_Q_AND_RESIDUAL_U_A
```

The complete profile envelope and lower reserve also remain open.

This packet does **not**:

- construct or enumerate a deployed complete selector;
- use a toy finite-field record as proof;
- choose an eliminant from a selector or charge one root set per record;
- claim that the determinant condition is sufficient for a record;
- retain selector-derived data after deletion;
- pay non-full-outside source load;
- determine \(U_Q\) or residual \(U_A\);
- close rank nine or KoalaBear;
- authorize rank at least ten, Lean, or stable-paper promotion; or
- edit Papers A--D.

### Audit

- **Parameter dependence:** Sections 3--5 are field-uniform for
  \(B=\mathbf F_p\subset F\), distinct source points in \(B^\times\),
  \(p>2\), \(|F|>s\), \(s-1>e+1\), and \(s-e>1\).  The displayed charge,
  floors, and ledgers use the exact KoalaBear row.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not used.
- **Numerical evidence:** none is used in the proof.  The companion Sage
  control is exact toy-scale interface evidence only.
- **Local verdict:** GREEN after independent proof, adversarial geometry,
  and artifact/accounting reviews.
- **Global verdict:** YELLOW.  Rank nine, the remaining ledgers, and
  KoalaBear remain open.

## 9. Minimal next action

Package and bank the independently reviewed determinant owner, exact charge,
and revised source floor.  Then attack the new \(r\ge2\) full-outside
residual through its complete slack-profile partition; do not return to the
closed one-slack cells and do not begin rank at least ten.
