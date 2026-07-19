# M1 KoalaBear moving-root cofactor/slack and C5 boundary v1

Status: **PROVED MOVING-ROOT COFACTOR DIVISIBILITY / PROVED EXACT SLACK
NORMAL FORM / PROVED C5 ABSORPTION AT ZERO SOURCE SLACK / ZERO LEDGER
MOVEMENT / FIRST ONE-SLACK COMPONENTS ISOLATED / INDEPENDENT PROOF REVIEW
GREEN / KOALABEAR ROW OPEN**.

This packet composes two facts that were previously banked but not composed:

1. the exact rich-pencil moving-zero identity
   \(|F_{\eta,L}|=x_L+\delta_\eta\); and
2. the full-outside, full-gcd-reduced degree inequality used by the adaptive
   source--rational owner.

For every qualifying selected finite slope, the reduced polynomial
\(\bar P_L+\eta\bar Q_L\) vanishes on the entire moving-zero set.  Hence

\[
 L_{F_{\eta,L}}\mid \bar P_L+\eta\bar Q_L,
 \qquad x_L+\delta_\eta\le e_L.
\]

This raises the source-size floor from \(36{,}836\) to \(67{,}473\).  At
the equality boundary, the full gcd and every moving polynomial are split
base-field locators.  Two distinct slopes then exhibit the fixed translated
received pair as an invertible \(F\)-coordinate transform of a \(B\)-valued
pair, so the already-paid projective-base C5 owner removes the boundary.
Thus every surviving record satisfies

\[
 \boxed{
 s\ge67{,}474,\qquad e\ge33{,}737,
 \qquad \deg\gcd(P,Q)\le1{,}014{,}838.}
\]

The argument is conditional only on the record-level contracts already
payload-bound by the predecessors.  It does not construct a deployed
complete selector and does not need one: it is a uniform implication for any
qualifying record that a rebuilt selector may produce.

## 1. Frozen row, fields, and first-match position

Fix the KoalaBear row

\[
 p=2{,}130{,}706{,}433,
 \qquad B=\mathbf F_p\subset F=\mathbf F_{p^6},
 \qquad D\subset B,
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

The first-match order contains

```text
projective_base_pair_C5
source_rational_full_outside_bounded_degree
residual_extension_valued_strata
residual_base_slope_universe
```

in that order.  The present packet adds no owner and no charge.  It proves
that one boundary of the residual left after the source--rational deletion is
already empty because it would have been deleted by the earlier C5 owner.

## 2. Qualifying post-restart records

Work after the exact source--rational deletion and the mandatory complete
selector restart.  Fix any contributing rich graph line \(L\) in any rebuilt
selector satisfying the inherited contracts:

- full outside source: \(V\cap\Sigma=\varnothing\);
- \(\beta_L>0\), \(J_L\ge21\), and
  \(x_L\le49{,}055\);
- coefficient rank two for
  \(P_L,Q_L\in F[X]_{\le k-1}\);
- source coupling
  \[
   a_L=\epsilon _0-\operatorname{ev}(P_L),\qquad
   b_L=\epsilon _1-\operatorname{ev}(Q_L);
  \tag{2.1}
  \]
- the full monic gcd, not only a forced locator,
  \[
   H_L=\gcd(P_L,Q_L),\qquad
   P_L=H_L\bar P_L,\quad Q_L=H_L\bar Q_L,
   \quad\gcd(\bar P_L,\bar Q_L)=1;
  \tag{2.2}
  \]
- the reduced degree
  \[
   e_L=\max\{\deg\bar P_L,\deg\bar Q_L\};
  \tag{2.3}
  \]
- and the exact moving-zero and support equations for every selected finite
  slope \(\eta\in\Gamma_L\).

Suppress \(L\) below.  Put

\[
 Z=\{z\in V:a(z)=b(z)=0\},\qquad
 W=V\setminus Z,
\tag{2.4}
\]

\[
 F_\eta=\{x\in W:a(x)+\eta b(x)=0\}.
\tag{2.5}
\]

If \(E_\eta=\operatorname{supp}(a+\eta b)\) and
\(\delta_\eta=j-|E_\eta|\), the rich-pencil atlas proves

\[
 E_\eta=W\setminus F_\eta,
 \qquad |F_\eta|=x+\delta_\eta,
 \qquad x+\delta_\eta\ge1.
\tag{2.6}
\]

Here \(x=x_L=|W|-j\).  Since the selected errors lie in the low-deficit
family, \(\delta_\eta\ge0\).

The full-outside common-root set is

\[
 C_L=(D\setminus W)\setminus\Sigma,
 \qquad c=|C_L|=A-x-s.
\tag{2.7}
\]

Its squarefree monic locator \(L_{C_L}\in B[X]\) divides \(H\).  Therefore,
with \(d_H=\deg H\),

\[
 d_H\ge c,
 \qquad d_H+e\le k-1,
\tag{2.8}
\]

and hence

\[
 e\le k-1-c=s+x-t-1.
\tag{2.9}
\]

Finally, because this is the residual after the adaptive source--rational
owner and selector restart, its subset-stable exclusion gives

\[
 e\ge\left\lceil\frac s2\right\rceil.
\tag{2.10}
\]

## 3. Moving-root cofactor divisibility

### Lemma 3.1 (full moving-root cofactor)

For every selected finite slope \(\eta\in\Gamma_L\), there is a nonzero
polynomial \(A_\eta\in F[X]\) such that

\[
 \boxed{
 \bar P+\eta\bar Q=L_{F_\eta}A_\eta,}
\tag{3.1}
\]

and

\[
 \boxed{
 \deg A_\eta
 \le e-(x+\delta_\eta).}
\tag{3.2}
\]

In particular,

\[
 \boxed{x+\delta_\eta\le e.}
\tag{3.3}
\]

#### Proof

Full outside gives \(W\subseteq V\subseteq D\setminus\Sigma\).  Hence
\(\epsilon _0=\epsilon _1=0\) on \(W\).  Equations (2.1) and (2.5) give

\[
 P(x)+\eta Q(x)=0\qquad(x\in F_\eta).
\tag{3.4}
\]

No point of \(F_\eta\subset W\) is a common root of \(P,Q\).  Indeed, a
common root in \(V\) would have \(a=b=0\) and therefore belong to \(Z\),
contrary to \(W=V\setminus Z\).  Thus \(H(x)\ne0\) on \(F_\eta\), and
cancelling \(H\) in (3.4) yields

\[
 \bar P(x)+\eta\bar Q(x)=0
 \qquad(x\in F_\eta).
\tag{3.5}
\]

Coefficient rank two makes \(\bar P+\eta\bar Q\) nonzero for every finite
\(\eta\).  The points in \(F_\eta\subset D\) are distinct, so their locator
divides this polynomial.  Since its degree is at most \(e\), (3.1)--(3.3)
follow. \(\square\)

The whole set \(F_\eta\), rather than one chosen moving root, is load-bearing.
The earlier one-root bridge alone does not imply (3.3).

## 4. Exact slack normal form

Define four nonnegative integer slacks

\[
 r=s-t-1,
 \qquad h=d_H-c,
 \qquad u=e-x,
 \qquad \ell=k-1-d_H-e.
\tag{4.1}
\]

The symbol \(u\) is local to this note and is not the atlas word called
\(u\) in some predecessors.

### Lemma 4.1 (slack simplex)

Every qualifying record satisfies

\[
 \boxed{h+u+\ell=r,}
\tag{4.2}
\]

and, for every selected \(\eta\),

\[
 \boxed{0\le\delta_\eta\le u.}
\tag{4.3}
\]

#### Proof

The quantities \(h\) and \(\ell\) are nonnegative by (2.8).  Lemma 3.1
gives \(u=e-x\ge\delta_\eta\ge0\).  Using
\(c=A-x-s\) and \(t=A-k\),

\[
\begin{aligned}
 h+u+\ell
 &=(d_H-c)+(e-x)+(k-1-d_H-e)\\
 &=k-1-c-x\\
 &=k-1-(A-x-s)-x\\
 &=s-t-1=r.
\end{aligned}
\]

This proves both claims. \(\square\)

In particular,

\[
 r=h+u+\ell\ge u\ge\delta_\eta.
\]

An immediate consequence is

\[
 \boxed{s\ge t+\delta_\eta+1\ge t+1=67{,}473.}
\tag{4.4}
\]

Thus every parametric source size from the predecessor floor \(36{,}836\)
through \(67{,}472\) is empty.  No selector census is needed for this
exclusion.

## 5. C5 absorption at the equality boundary

### Theorem 5.1 (zero-slack boundary is already C5-owned)

No post-C5, post-source-rational qualifying record has

\[
 s=t+1=67{,}473.
\tag{5.1}
\]

#### Proof

At (5.1), (4.2) forces

\[
 h=u=\ell=0.
\tag{5.2}
\]

Equation (4.3) then gives \(\delta_\eta=0\) for every selected slope.  The
equalities \(h=0\) and \(u=0\) give

\[
 H=L_{C_L}\in B[X],
 \qquad e=x.
\tag{5.3}
\]

Indeed, \(L_{C_L}\mid H\), both polynomials are monic, and they have the
same degree.  Lemma 3.1 now has a constant nonzero cofactor:

\[
 \bar P+\eta\bar Q
 =\kappa_\eta L_{F_\eta},
 \qquad \kappa_\eta\in F^\times.
\tag{5.4}
\]

Choose two distinct selected slopes \(\eta_1,\eta_2\), which exist because
\(J_L\ge21\).  The matrix

\[
 \begin{pmatrix}1&1\\ \eta_1&\eta_2\end{pmatrix}
\tag{5.5}
\]

is invertible, and (5.4) gives the explicit coordinate identity

\[
 [\bar P\ \bar Q]
 = [L_{F_{\eta_1}}\ L_{F_{\eta_2}}]
   \operatorname{diag}(\kappa_{\eta_1},\kappa_{\eta_2})
   \begin{pmatrix}1&1\\ \eta_1&\eta_2\end{pmatrix}^{-1}.
\tag{5.6}
\]

Hence the \(F\)-span of
\((\bar P,\bar Q)\) has the base-polynomial basis
\((L_{F_{\eta_1}},L_{F_{\eta_2}})\).  Multiplying by the base polynomial
\(H=L_{C_L}\), and then restricting to the fixed source, define

\[
 R_i=\mathbf 1_\Sigma
      L_{C_L}L_{F_{\eta_i}}\in B^D
 \qquad(i=1,2).
\tag{5.7}
\]

On \(\Sigma\), source coupling gives \((\epsilon _0,\epsilon _1)=(P,Q)\).
Off \(\Sigma\), both sides of the translated source pair vanish.  Therefore
(5.4)--(5.7) exhibit

\[
 (\epsilon _0,\epsilon _1)=(R_1,R_2)M
\tag{5.8}
\]

for one \(M\in\operatorname{GL}_2(F)\).  The original received pair differs
from the translated source pair only by two explaining codewords, which are a
syndrome gauge.  Thus the fixed received pair has positive-rank intrinsic
projective syndrome field \(B\), unless its syndrome rank is zero.  In the
rank-zero case the support-wise noncontained exact-witness residual is empty.
In the positive-rank case the earlier canonical C5 owner is
witness-exhaustive and deletes every post-branch-5 slope.

Either alternative contradicts the existence of this later qualifying
record. \(\square\)

The extension-valued numbers \(\eta_i\) and \(\kappa_{\eta_i}\) in (5.4)
are harmless: they occur only in the allowed invertible reparametrization
\(M\).  The base-field objects needed for descent are the two words (5.7).

## 6. Revised residual and exact accounting

Theorem 5.1 and integrality strengthen (4.4) to

\[
 \boxed{s\ge67{,}474.}
\tag{6.1}
\]

The adaptive source--rational survivor inequality (2.10) gives

\[
 \boxed{e\ge\left\lceil\frac{67{,}474}{2}\right\rceil
 =33{,}737.}
\tag{6.2}
\]

Consequently

\[
 \boxed{d_H\le k-1-e
 \le1{,}048{,}575-33{,}737
 =1{,}014{,}838.}
\tag{6.3}
\]

Thus every full-gcd degree in

\[
 1{,}014{,}839\le d_H\le k-2=1{,}048{,}574
\tag{6.4}
\]

is excluded from the surviving full-outside rank-two residual.  This is
\(33{,}736\) degrees in total, compared with \(18{,}417\) in the immediate
predecessor: exactly \(15{,}319\) additional degrees are removed.

The new terminal is

```text
UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67474
```

with the simultaneous degree and gcd bounds (6.2)--(6.3).

No new slope set is charged.  Source sizes below (5.1) are impossible, and
the equality source size belongs to the already-banked C5 cell.  Hence

\[
 \boxed{\Delta U_{\rm paid}=0,
 \qquad\Delta B_{\rm remaining}=0.}
\tag{6.5}
\]

The predecessor values remain

\[
 U_{\rm paid}=2{,}605{,}562{,}836,
 \qquad
 B_{\rm remaining}=274{,}980{,}725{,}505{,}832{,}251.
\tag{6.6}
\]

The packet does not alter \(U_Q\), the balanced-core/sparse residuals, the
complete profile-envelope comparison, or the lower reserve.

## 7. The first one-slack frontier

At the first unresolved source size \(s=t+2=67{,}474\), one has \(r=1\).
The nonnegative integral solutions of (4.2) are exactly

\[
 (h,u,\ell)=(1,0,0),\quad(0,1,0),\quad(0,0,1).
\tag{7.1}
\]

### 7.1 The degree-slack cell \((0,0,1)\)

Here \(H=L_{C_L}\in B[X]\), \(e=x\), and every \(\delta_\eta=0\).
The proof of Theorem 5.1 applies verbatim.  This cell is

```text
PAID_PROJECTIVE_BASE_PAIR_C5_AT_ONE_SOURCE_SLACK.
```

### 7.2 The common-factor cell \((1,0,0)\)

Here every reduced moving member is still a scalar base locator, but

\[
 H=L_{C_L}G,
 \qquad G\text{ monic},\quad\deg G=1.
\tag{7.2}
\]

If \(G\in B[X]\), the same two-slope argument makes the translated pair
projectively base-defined and C5 owns it.  Therefore the narrow primitive
residual requires a genuinely nonbase linear factor:

```text
UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST.
```

This includes no assertion that every nonbase twist is compatible with the
regular locator equations or a deployed selector.

### 7.3 The moving-cofactor cell \((0,1,0)\)

Here \(H=L_{C_L}\in B[X]\), \(e=x+1\), and

\[
 \bar P+\eta\bar Q=L_{F_\eta}A_\eta,
 \qquad \deg A_\eta\le1-\delta_\eta.
\tag{7.3}
\]

Thus \(\delta_\eta\in\{0,1\}\).  A slope with \(\delta_\eta=1\) has a
constant cofactor and hence gives a scalar base locator.  If two selected
slopes have \(\delta=1\), the two-slope C5 argument applies.  More generally,
any two selected members that are projectively in \(B[X]\) force C5
absorption.  A surviving primitive component therefore has at most one such
member; in particular at most one slope has \(\delta=1\).  Since
\(J_L\ge21\), at least twenty selected slopes then have \(\delta=0\) and a
potentially nonbase linear cofactor.  The fail-closed terminal is

```text
UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR.
```

The next algebraic attack must bind (7.2) or (7.3) to the eight outlier
directions and the regular locator equations.  Generic high-degree
elimination is neither needed nor authorized.

## 8. Dependencies, residuals, and nonclaims

### Proved in this packet

- the whole-moving-set divisibility (3.1);
- the cofactor degree bound (3.2);
- the exact slack simplex (4.2)--(4.3);
- emptiness for \(s\le67{,}472\);
- C5 absorption at \(s=67{,}473\);
- the revised source, reduced-degree, and full-gcd bounds;
- zero ledger movement; and
- the exact one-slack trichotomy and its forced C5 subcells.

### Imported and payload-bound

- the fixed received pair and SP3 translation;
- the post-deletion subset-stable source--rational survivor condition;
- full-outside source coupling and the full-gcd degree inequality;
- the exact rich-pencil identity \(|F_\eta|=x+\delta_\eta\);
- coefficient rank two, \(\beta_L>0\), and \(J_L\ge21\);
- projective syndrome descent and witness-exhaustive C5 ownership; and
- the existing first-match order and zero-movement ledger.

### Still open

```text
UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST
UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR
UNBOUND_POST_TANGENT_SOURCE_LOAD
```

The complete rank-nine payment, image-scale \(Q\)/MI input, balanced-core and
sparse residuals, complete profile-envelope comparison, and lower reserve
remain open.

This packet does **not**:

- construct or enumerate a deployed complete selector;
- infer the whole-moving-set identity from a single chosen root;
- apply to non-full-outside or coefficient-rank-one records;
- count determinant bases, graph lines, supports, or witnesses;
- claim that either one-slack primitive terminal is nonempty;
- force a nonbase linear component into C5 or another owner;
- add a C5 charge or move any ledger value;
- determine \(U_Q\), close rank nine, or close KoalaBear;
- begin rank at least ten, Lean formalization, or stable-paper promotion; or
- promote exact toy controls to a deployed theorem.

### Audit

- **Parameter dependence:** Lemmas 3.1 and 4.1 are field-uniform under their
  printed record contracts.  The numerical floors and ceilings use the exact
  KoalaBear row.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not used.
- **Numerical evidence:** none is used in the proof.  The companion Sage
  controls are exact toy-scale interface checks only.
- **Local verdict:** GREEN after a fresh independent proof audit.
- **Global verdict:** YELLOW.  The one-slack terminals and global KoalaBear
  ledger remain open.

## 9. Minimal next action

Bank this zero-movement route cut.  Then classify only the two one-slack
components in Sections 7.2--7.3 against the exact regular-locator equations
and the eight rank-nine outlier directions.  Stop at the first compatible
primitive component.  Do not start a generic degree-\(33{,}737\) elimination,
non-full-outside aggregation, rank at least ten, or Lean.
