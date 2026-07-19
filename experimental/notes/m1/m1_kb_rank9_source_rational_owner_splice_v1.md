# M1 KoalaBear pair-global bounded-degree source--rational owner v1

Status: **PROVED LOCAL BOUNDED-DEGREE RATIONAL RIGIDITY / PROVED
PAIR-GLOBAL OWNER AND EXACT FIRST-MATCH REPLACEMENT / ZERO LEDGER MOVEMENT
RELATIVE TO THE SOURCE--MOBIUS OWNER / INDEPENDENT PROOF AND ARTIFACT REVIEWS
GREEN / KOALABEAR ROW OPEN**.

This packet replaces the pair-global source--Möbius owner by its adaptive
bounded-degree rational analogue.  The source--Möbius packet used three fixed
SP3 source anchors to synchronize degree-one maps.  Here all

\[
 s=|\Sigma|
\]

fixed source anchors are used.  Two rational maps of degree at most

\[
 E(s):=\left\lfloor\frac{s-1}{2}\right\rfloor
\]

that agree on those anchors have cross determinant of degree at most
\(2E(s)<s\), and hence are equal.  This synchronizes qualifying maps across
all selectors.  Their finite selected slopes lie in the image of
\(D\setminus\Sigma\), so the same intrinsic cap \(n-s_0\) applies without
using injectivity.

The old source--Möbius owner is absorbed, not charged a second time.  The
joint C5/source/base block, the paid ledger, and every downstream integer are
unchanged.  What improves is the residual: every surviving full-outside
rank-two record now satisfies

\[
 s\ge36{,}836,\qquad e\ge18{,}418,
 \qquad \deg\gcd(P,Q)\le1{,}030{,}157,
\]

where \(e\) is the degree of the gcd-reduced projective map.  Thus all
\(18{,}417\) possible gcd degrees from \(1{,}030{,}158\) through
\(k-2=1{,}048{,}574\) are removed from the full-outside rank-two residual.

## 1. Frozen pair-global data

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

Fix one received pair and the single SP3 translation used for that pair.
Write the translated sparse source pair and its support as

\[
 (\epsilon _0,\epsilon _1),\qquad
 \Sigma=\operatorname{supp}(\epsilon _0)
       \cup\operatorname{supp}(\epsilon _1)\subseteq D,
 \qquad s=|\Sigma|.
\tag{1.2}
\]

For every \(h\in\Sigma\), the source pair is nonzero.  Hence the intrinsic
projective source label

\[
 \lambda(h)=[-\epsilon _0(h):\epsilon _1(h)]
 \in\mathbf P^1(F)
\tag{1.3}
\]

is defined.  No union over alternative translations is permitted.

The inherited full-outside rank-two source floor is

\[
 s_0:=t-\left\lfloor\frac j{20}\right\rfloor+2
 =67{,}472-49{,}055+2=18{,}419.
\tag{1.4}
\]

Let \(\Gamma_{\rm in}\) be the exact finite residual slope set at the
source-owner slot, after all globally earlier first-match owners.  The
argument below is subset-stable: for any
\(\Gamma\subseteq\Gamma_{\rm in}\), it quantifies over every complete
selector that can be built on \(\Gamma\).  In the first pass take
\(\Gamma=\Gamma_{\rm in}\); after deletion take
\(\Gamma=\Gamma_{\rm out}\).

## 2. Qualifying records and their reduced maps

Fix any \(\Gamma\subseteq\Gamma_{\rm in}\).  Quantify over every complete
selector \(\sigma\) that can be built on \(\Gamma\), and over every
contributing rich graph line \(L\) in that selector satisfying the
predecessor contracts:

- carrier \(V_\sigma\subseteq D\) and the full-outside condition
  \(V_\sigma\cap\Sigma=\varnothing\);
- \(\beta_{\sigma,L}>0\), \(J_{\sigma,L}\ge21\), and
  \(x_{\sigma,L}\le\lfloor j/20\rfloor=49{,}055\);
- coefficient rank two for the polynomial lifts
  \(P_{\sigma,L},Q_{\sigma,L}\in F[X]_{\le k-1}\);
- the fixed source equations and source-rank-two floor
  \(s\ge t-x_{\sigma,L}+2\); and
- the moving-root transversality contract for every selected finite slope.

For one such record suppress \(\sigma,L\) and put

\[
 H=\gcd(P,Q)
\tag{2.1}
\]

with \(H\) monic.  This is the full polynomial gcd, not merely the locator of
forced domain roots.  Write

\[
 P=H\bar P,\qquad Q=H\bar Q,
 \qquad \gcd(\bar P,\bar Q)=1,
\tag{2.2}
\]

and define

\[
 e=\max\{\deg\bar P,\deg\bar Q\}.
\tag{2.3}
\]

Coefficient rank two implies \(e\ge1\).  The coprime pair defines the
nonconstant projective rational map

\[
 \psi_{\sigma,L}([X:Z])
 =[-\bar P^{\rm hom}(X,Z):\bar Q^{\rm hom}(X,Z)]
 :\mathbf P^1_F\longrightarrow\mathbf P^1_F
\tag{2.4}
\]

of degree \(e\), where both polynomials are homogenized to degree \(e\).
There is no base point: affine common roots are excluded by (2.2), and at
least one degree-\(e\) leading coefficient is nonzero at infinity.

Let \(d_H=\deg H\).  The degree contract gives

\[
 d_H+e\le k-1.
\tag{2.5}
\]

At every source point, full-outside coupling gives

\[
 P(h)=\epsilon _0(h),\qquad Q(h)=\epsilon _1(h).
\tag{2.6}
\]

The right side is nonzero, so \(H(h)\ne0\), and cancellation gives the
common anchor identity

\[
 \boxed{\psi_{\sigma,L}([h:1])=\lambda(h)
 \quad(h\in\Sigma).}
\tag{2.7}
\]

There is also a record-level upper bound for \(e\).  Since
\(\Sigma\cap V_\sigma=\varnothing\), the source plant is all of \(\Sigma\).
The outside-source common-root set has cardinality

\[
 c=A-x_{\sigma,L}-s.
\tag{2.8}
\]

Its locator divides \(H\), so \(d_H\ge c\).  Equations (2.5) and (2.8)
therefore give

\[
 \boxed{
 e\le k-1-c=s+x_{\sigma,L}-t-1\le s-18{,}418.}
\tag{2.9}
\]

This is the reduced projective degree bound; the unreduced degree
\(k-1\) is not used.

## 3. Adaptive rational rigidity

### Lemma 3.1 (\(s\)-anchor bounded-degree rigidity)

Let \(s\ge1\), and put

\[
 E(s)=\left\lfloor\frac{s-1}{2}\right\rfloor.
\tag{3.1}
\]

Suppose \(\psi_1,\psi_2:\mathbf P^1_F\to\mathbf P^1_F\) are nonconstant
rational maps of degrees \(e_1,e_2\le E(s)\).  If they agree at \(s\)
distinct finite inputs, then \(\psi_1=\psi_2\).

#### Proof

Choose coprime affine representatives

\[
 \psi_i=[-A_i:B_i],
 \qquad \max\{\deg A_i,\deg B_i\}=e_i.
\]

Projective equality at an input \(h\) is exactly the vanishing of the cross
determinant

\[
 \Delta(X)=A_1(X)B_2(X)-A_2(X)B_1(X).
\tag{3.2}
\]

It has degree at most

\[
 e_1+e_2\le2E(s)\le s-1.
\]

The \(s\) distinct common inputs are roots of \(\Delta\), so
\(\Delta=0\).  The two coprime pairs therefore represent the same element
of \(F(X)\), hence the same projective map. \(\square\)

The strict inequality \(s>e_1+e_2\) is load-bearing.  Agreement at only
\(e_1+e_2\) points does not force the cross determinant to vanish
identically without additional structure.

## 4. Intrinsic bounded-degree source--rational image

Call the fixed source data **bounded-degree rational-compatible** if
\(s\ge s_0\) and there exists a nonconstant rational map

\[
 \psi:\mathbf P^1_F\longrightarrow\mathbf P^1_F,
 \qquad 1\le\deg\psi\le E(s),
\tag{4.1}
\]

such that

\[
 \psi([h:1])=\lambda(h)qquad(h\in\Sigma).
\tag{4.2}
\]

Lemma 3.1 makes \(\psi\) unique within this degree range.  Define the finite
pair-global source--rational image

\[
 \mathcal R(\epsilon _0,\epsilon _1)=
 \begin{cases}
 \{\eta\in F:\ [\eta:1]=\psi([x:1])
       \text{ for some }x\in D\setminus\Sigma\},
       &\text{if (4.1)--(4.2) hold},\\[2mm]
 \varnothing,&\text{otherwise}.
 \end{cases}
\tag{4.3}
\]

This set depends only on the received pair and its fixed translation.  It
contains no selector, carrier, graph line, determinant basis, support, or
witness multiplicity.  Poles of \(\psi\) on \(D\setminus\Sigma\) contribute
projective infinity and are simply absent from the finite image (4.3).

Put

\[
 Z_{\rm SRat}=\Gamma_{\rm in}\cap
 \mathcal R(\epsilon _0,\epsilon _1),
 \qquad
 \Gamma_{\rm out}=\Gamma_{\rm in}\setminus Z_{\rm SRat}.
\tag{4.4}
\]

### Theorem 4.1 (pair-global bounded-degree source--rational owner)

For every \(\Gamma\subseteq\Gamma_{\rm in}\), across every selector built on
\(\Gamma\) and every qualifying record from Section 2 whose
reduced degree satisfies

\[
 e_{\sigma,L}\le E(s),
\tag{4.5}
\]

all reduced maps are one common map \(\psi\), and

\[
 \boxed{
 \bigcup_\sigma
 \bigcup_{\substack{L\ \mathrm{qualifying}\\ e_{\sigma,L}\le E(s)}}
 \Gamma_{\sigma,L}^{\rm fin}
 \subseteq\mathcal R(\epsilon _0,\epsilon _1).}
\tag{4.6}
\]

Consequently

\[
 \boxed{
 |Z_{\rm SRat}|
 \le|\mathcal R(\epsilon _0,\epsilon _1)|
 \le|D\setminus\Sigma|
 =n-s
 \le n-s_0
 =2{,}078{,}733.}
\tag{4.7}
\]

#### Proof

Equation (2.7) says that every qualifying map agrees with the same source
labels at the same \(s\) inputs.  Under (4.5), Lemma 3.1 makes all of these
maps equal.  It also shows that if the source data fail (4.1)--(4.2), then no
qualifying record satisfying (4.5) exists.

For a selected finite slope \(\eta\), moving-root transversality supplies
\(x\in W_{\sigma,L}\subseteq V_\sigma\) for which

\[
 P_{\sigma,L}(x)+\eta Q_{\sigma,L}(x)=0.
\tag{4.8}
\]

Because \(x\in W_{\sigma,L}\), the two values in (4.8) are not both zero;
in particular \(H_{\sigma,L}(x)\ne0\).  Full-outside gives
\(x\in D\setminus\Sigma\), and cancellation in (4.8) yields

\[
 [\eta:1]=\psi_{\sigma,L}([x:1]).
\tag{4.9}
\]

This proves (4.6).  Finally, the image of a finite set under an arbitrary
function has cardinality no larger than the domain.  No injectivity of a
degree-greater-than-one rational map is asserted or required.  Omitting
projective infinity can only decrease the finite image size, proving
(4.7). \(\square\)

### Corollary 4.2 (subset stability and post-restart exclusion)

The containment (4.6) holds for complete selectors built on every
\(\Gamma\subseteq\Gamma_{\rm in}\), with the same intrinsic image
\(\mathcal R(\epsilon_0,\epsilon_1)\).  In particular, after the exact
deletion in (4.4), it holds for selectors rebuilt on
\(\Gamma_{\rm out}\).  Since

\[
 \Gamma_{\rm out}\cap\mathcal R(\epsilon_0,\epsilon_1)=\varnothing,
\tag{4.10}
\]

no contributing qualifying record in a rebuilt selector can satisfy
\(e\le E(s)\): such a record has a selected finite slope, while (4.6) would
put every selected finite slope in the empty intersection (4.10).

#### Proof

The proof of Theorem 4.1 uses only the fixed source pair, the record-level
qualifying contracts, and membership of selected slopes in the set on which
the selector was built.  It never uses equality
\(\Gamma=\Gamma_{\rm in}\).  Thus it applies to every subset.  Equation
(4.10) is the definition of \(\Gamma_{\rm out}\) in (4.4), and the last
claim follows from (4.6). \(\square\)

### 4.3 Absorption of the source--Möbius owner

A compatible Möbius map has degree one and therefore satisfies (4.1), since
\(s\ge s_0\).  By Lemma 3.1 it is the unique bounded-degree compatible map.
Thus, on the old Möbius-compatible branch,

\[
 \mathcal R(\epsilon _0,\epsilon _1)
 =\mathcal M(\epsilon _0,\epsilon _1).
\tag{4.11}
\]

The new owner is a replacement for the old one.  It may additionally delete
the image of one compatible map of degree \(2\) through \(E(s)\), but it
never charges both images and never takes a union over degrees or selectors.

## 5. Exact first-match replacement and restart

Replace `source_mobius_full_outside_maximal_gcd` by

```text
source_rational_full_outside_bounded_degree
```

at the same first-match slot: immediately after `projective_base_pair_C5`
and before the residual extension-valued and residual-base cells.  Charge
only the exact incoming intersection \(Z_{\rm SRat}\) in (4.4), then delete
that set.

It is harmless if \(\mathcal R\) contains an incoming bad slope with no
qualifying bounded-degree record.  A uniformly bounded set intrinsic to the
received pair may be deleted in full; this only shrinks every later family.
Earlier overlap is removed by intersection with \(\Gamma_{\rm in}\), and
later overlap is removed by the exact set difference.

After deletion:

1. apply the later pair-global extension and residual-base owners to the
   exact outgoing set;
2. rebuild the complete-selector universe on \(\Gamma_{\rm out}\);
3. rerun the global carrier and small-family gates;
4. choose a fresh affine-rank minimizer;
5. recompute the carrier, \(V\), \(H_V\), \(K_0\), \(d_V\), deficit
   histogram, and rich-pencil atlas; and
6. replay all established rank-at-most-three, rank-four-through-eight, and
   rank-nine terminals in their frozen order.

Restriction of an old complete selector proves that the rebuilt selector
universe is nonempty.  It gives a new minimum rank at most the old minimum,
but no old selector-derived field, carrier, basis, or atlas may be retained.
The source pair and labels (1.2)--(1.3) remain fixed because they precede the
selector choice.

The paid terminal is

```text
PAID_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL
```

under the owner ID printed above.

## 6. Exact accounting: replacement at zero cost

The C5/source-rational/base block has the same maximum-not-sum accounting as
the source--Möbius predecessor.

If the intrinsic projective syndrome field is \(B\), canonical C5 owns every
post-branch-5 finite slope and the joint charge is at most \(p+1\).  If it is
not \(B\), the C5 cell is empty; the source-rational owner has cap
\(n-s_0\), and exact later deletion leaves a disjoint residual-base cell of
cap \(p\).  Hence

\[
 \boxed{
 U_{C5/{\rm SRat}/B}
 =\max\{p+1,p+n-s_0\}
 =p+n-s_0
 =2{,}132{,}785{,}166.}
\tag{6.1}
\]

This equals the source--Möbius block exactly.  The ledger movement relative
to the integrated predecessor is therefore

\[
 \boxed{\Delta U_{\rm paid}=0,
 \qquad\Delta B_{\rm remaining}=0.}
\tag{6.2}
\]

The banked values remain

\[
 \boxed{U_{\rm paid}=2{,}605{,}562{,}836,}
\tag{6.3}
\]

\[
 \boxed{B_{\rm remaining}
 =274{,}980{,}725{,}505{,}832{,}251,}
\tag{6.4}
\]

\[
 T_{18{,}014}=17{,}907{,}568{,}905{,}216,
 \qquad K_{\rm remaining}=4{,}807{,}520,
 \qquad J_{\rm break}=166.
\tag{6.5}
\]

The predecessor payload bindings are

```text
source--Möbius owner:
  239ca25b91ef6a4f98af31aef9d5b5ddd970204043abe2153223eab5d39629e1
projective source load:
  68ada825d2e16544298ccc94dc390e3266ab175b375ab118de73f8e0e8040e0f
active-source reindex:
  4fa636866ddb4483ec577a44f3f832d1abaab5febab6c40271360214cfcecf3c
```

They bind the imported source equations, floor, first-match position, exact
joint block, and ledger.  The present replacement does not change
\(U_Q\), residual \(U_A\), or the complete target comparison.

## 7. Sharp consequences for every survivor

Consider a full-outside coefficient-rank-two contributing record after the
source-rational deletion and selector restart.  Corollary 4.2 applies
Theorem 4.1 to the rebuilt selector on \(\Gamma_{\rm out}\).  If its reduced
degree obeyed \(e\le E(s)\), every one of its selected finite slopes would
lie in the deleted owner image, contradicting (4.10).  Hence every surviving
such record must satisfy

\[
 \boxed{
 e\ge E(s)+1
 =\left\lceil\frac s2\right\rceil.}
\tag{7.1}
\]

Combine this with (2.9):

\[
 \left\lceil\frac s2\right\rceil
 \le e\le s-18{,}418.
\tag{7.2}
\]

For even \(s=2m\), (7.2) gives \(m\ge18{,}418\).  For odd
\(s=2m+1\), it gives \(m\ge18{,}418\).  Therefore

\[
 \boxed{s\ge36{,}836.}
\tag{7.3}
\]

Equations (7.1) and (7.3) then give

\[
 \boxed{e\ge18{,}418.}
\tag{7.4}
\]

Finally, (2.5) gives

\[
 \boxed{
 d_H\le k-1-e
 \le1{,}048{,}575-18{,}418
 =1{,}030{,}157.}
\tag{7.5}
\]

Equivalently, the owner removes every qualifying full-outside rank-two
record with

\[
 1{,}030{,}158\le d_H\le k-2=1{,}048{,}574.
\tag{7.6}
\]

The interval (7.6) contains exactly \(18{,}417\) integer gcd degrees.  The
surviving full-outside route cut is therefore

```text
UNPAID_FULL_OUTSIDE_REDUCED_DEGREE_AT_LEAST_18418
```

rather than the unquantified lower-gcd terminal.  A qualifying low-degree
record itself supplies the compatible map in (4.1)--(4.2), so absence of a
separately precomputed compatible map is not an additional residual in the
paid degree range.

## 8. Relation to the canonical reduced rational-host compiler

The integrated note
`experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md`
(the packet proposed in PR #721) is complementary, not a dependency and not
a duplicate owner.  That compiler starts from one already-given reduced
rational-host presentation of a received line and gives a witness-exhaustive
support/`LineRay` bijection.  The present theorem instead starts from the
full-outside SP3 source equations of rank-nine graph-line records and
synchronizes their gcd-reduced maps across selectors.

The rational-host compiler does not prove the pair-global source-anchor
rigidity or the cap (4.7).  Conversely, the source-rational owner does not
extract a rational-host presentation, compile exact supports, bound its
aggregate `LineRay` scale, or settle its complete profile envelope.  Any
future composition must retain both first-match ledgers and must not identify
their rational maps without an explicit bridge.

## 9. Dependencies, residuals, and nonclaims

### Proved in this packet

- Lemma 3.1, including the exact adaptive degree threshold;
- Theorem 4.1 under the imported qualifying-record contracts;
- Corollary 4.2, including subset stability and the post-restart exclusion;
- the intrinsic image cap without injectivity;
- absorption of the old source--Möbius image;
- the exact first-match replacement and downstream restart rule;
- zero ledger movement; and
- the survivor bounds (7.3)--(7.5).

### Imported and payload-bound

- the single pair-global SP3 translation and fixed sparse source pair;
- full-outside source coupling and the rank-two source floor;
- the rich-line bound \(x_{\sigma,L}\le49{,}055\);
- the moving-root transversality bridge;
- the first-match order and selector-restriction restart; and
- the integrated C5/source--Möbius/base ledger.

### Still open

```text
UNPAID_FULL_OUTSIDE_REDUCED_DEGREE_AT_LEAST_18418
UNBOUND_POST_TANGENT_SOURCE_LOAD
```

The second terminal includes non-full-outside, active rank-one, universal
source-cell, and active source-hit basis-tail components.  The complete
rank-nine payment, \(U_Q\), residual \(U_A\), complete profile-envelope
comparison, and lower-reserve comparison also remain open.

This packet does **not**:

- assume a degree-greater-than-one rational map is injective;
- union maps over selectors, degrees, or alternative translations;
- replace the full gcd by the forced domain-root locator;
- count graph lines, determinant bases, witnesses, or support patterns;
- retain selector-derived data after first-match deletion;
- pay a map with degree at least \(18{,}418\);
- pay non-full-outside source-load cells;
- move the ledger, determine \(U_Q\) or \(U_A\), or close KoalaBear;
- start rank at least ten, Lean formalization, or stable-paper promotion; or
- use exact finite-field controls as proof of a deployed selector theorem.

### Audit

- **Parameter dependence:** Lemma 3.1 and Theorem 4.1 are finite and
  field-uniform under the printed contracts.  The values \(s_0=18{,}419\),
  \(18{,}418\), \(36{,}836\), and \(1{,}030{,}157\) use the exact KoalaBear
  row.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not used.
- **Numerical evidence:** none is used in the proof.  Exact finite-field
  controls and mutation tests belong to the companion certificate packet and
  cannot promote an unstated deployed hypothesis.
- **Local verdict:** GREEN for the symbolic bounded-degree rigidity, owner,
  first-match replacement, accounting identity, and survivor inequalities
  under the payload-bound predecessor contracts.
- **Global verdict:** YELLOW.  The residual terminals and global KoalaBear
  ledger remain open.  Fresh independent proof and artifact reviews of this
  local packet are GREEN; they do not promote the global row.

## 10. Minimal next action

Bank this zero-movement replacement and attack only the first actual record
satisfying
`UNPAID_FULL_OUTSIDE_REDUCED_DEGREE_AT_LEAST_18418`.  Freeze that record's
exact high-degree support/source equations before choosing any new symbolic
tool; do not mix in non-full-outside source load, \(U_Q\), or residual
\(U_A\).
