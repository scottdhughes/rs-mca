# M1 KoalaBear one-slack common-twist source-subline owner v1

Status: **PROVED LOCAL PAIR-GLOBAL SOURCE-SUBLINE CONFINEMENT / PROVED
EXACT FIRST-MATCH OWNER AND SELECTOR RESTART / COMMON-FACTOR ONE-SLACK
COMPONENT CLOSED / INDEPENDENT PROOF AND ARTIFACT REVIEWS GREEN /
KOALABEAR ROW OPEN**.

This packet closes exactly one of the two one-slack components left by the
moving-root slack/C5 boundary theorem:

```text
UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST.
```

The closure is a pair-global projective-subline owner.  Two rich members make
the gcd-reduced polynomial pencil base-defined.  Therefore the source labels
and every selected moving-root slope of one record lie on a \(B\)-subline of
\(\mathbf P^1(F)\).  Three distinct fixed source labels synchronize that
subline immediately.  The only apparent exception is a source with exactly
two labels.  In that case the nonbase common linear factor leaves a Frobenius
fingerprint on either source block:

\[
 \rho(h)^{p-1}
 =c\frac{h-\zeta^p}{h-\zeta}.
\]

Three fixed source points recover the pole \(\zeta\), and the two source
coordinates then recover the scalar coset defining the same \(B\)-subline.
Thus the exception also synchronizes across all selectors.

The owner charges the exact post-tangent incoming intersection with one
projective \(B\)-subline, at most

\[
 p-1=2{,}130{,}706{,}432
\]

finite slopes, deletes it, and restarts the complete-selector construction.
No common-factor one-slack record can occur after that restart.  The earlier
tangent owner is load-bearing in the two-point saving: it already removed
every finite source label.  A nonstandard \(B\)-subline can have all \(p+1\)
of its projective points in the ambient affine chart, but the fixed source has
at least two labels in every surviving record.

## 1. Frozen row, source, and first-match position

Fix

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
\tag{1.2}
\]

and define its fixed projective source labels

\[
 \lambda(h)=[-\epsilon _0(h):\epsilon _1(h)]
 \in\mathbf P^1(F),
 \qquad h\in\Sigma.
\tag{1.3}
\]

The pair in (1.2), its support, and the labels (1.3) precede every selector
choice.  Alternative translations are not unioned.

Let \(\Gamma_{\rm in}\) be the exact finite residual slope set at the new
owner slot, after the canonical C5 and bounded-degree source--rational owners.
The relevant local first-match segment is

```text
projective_base_pair_C5
source_rational_full_outside_bounded_degree
source_subline_common_linear_gcd_twist
residual_extension_valued_strata
residual_base_slope_universe.
```

Every statement below is subset-stable: for each
\(\Gamma\subseteq\Gamma_{\rm in}\), it quantifies over every complete
selector rebuilt on \(\Gamma\) and every qualifying record in that selector.

## 2. The one-slack common-factor record

Fix a qualifying full-outside, coefficient-rank-two rich record after the
source--rational deletion and selector restart.  The predecessor theorem gives

\[
 s:=|\Sigma|=t+2=67{,}474,
 \qquad (h,u,\ell)=(1,0,0),
\tag{2.1}
\]

\[
 e=x,
 \qquad 33{,}737\le x\le49{,}055,
 \qquad \delta_\eta=0
\tag{2.2}
\]

for every selected finite rich slope \(\eta\).  If \(C_L\) is the forced
outside-source common-root set, its monic locator lies in \(B[X]\), and the
full monic gcd has the exact form

\[
 H=L_{C_L}G,
 \qquad G=X-\zeta,
 \qquad \zeta\in F\setminus B.
\tag{2.3}
\]

The base case \(\zeta\in B\) was already removed by canonical C5 and is not
part of this cell.

Write

\[
 P=H\bar P,qquad Q=H\bar Q,qquad
 \gcd(\bar P,\bar Q)=1,qquad
 \max(\deg\bar P,\deg\bar Q)=x.
\tag{2.4}
\]

The moving-root cofactor lemma becomes

\[
 \boxed{
 \bar P+\eta\bar Q=\kappa_\eta L_{F_\eta},
 \qquad \kappa_\eta\in F^\times,
 \qquad L_{F_\eta}\in B[X],
 \qquad \deg L_{F_\eta}=x.}
\tag{2.5}
\]

There are at least two distinct selected slopes because \(J_L\ge21\).
The corresponding two members in (2.5) are linearly independent: the
coefficient vectors \((1,\eta_1)\), \((1,\eta_2)\) are independent and the
coefficient rank of \((\bar P,\bar Q)\) is two.  Hence

\[
 U_L:=\operatorname{span}_F\{\bar P,\bar Q\}
 =\operatorname{span}_F\{L_{F_{\eta_1}},L_{F_{\eta_2}}\}
\tag{2.6}
\]

is the scalar extension of a two-dimensional polynomial plane over \(B\).

## 3. The record-level base subline

Define the gcd-reduced projective map

\[
 \psi_L([X:Z])
 =[-\bar P^{\rm hom}(X,Z):\bar Q^{\rm hom}(X,Z)].
\tag{3.1}
\]

Equation (2.6) says that the image of the base projective coefficient line is
one projective \(B\)-subline

\[
 S_L\subseteq\mathbf P^1(F),
 \qquad |S_L|=p+1.
\tag{3.2}
\]

This statement concerns a projective subline, not the intrinsic projective
syndrome field.  The pointwise nonbase factor \(X-\zeta\) can keep that
syndrome field equal to all of \(F\).

### Lemma 3.1 (source and moving slopes lie on the same subline)

For every qualifying record,

\[
 \boxed{\lambda(\Sigma)\subseteq S_L,}
\tag{3.3}
\]

and every selected finite rich slope satisfies

\[
 \boxed{[\eta:1]\in S_L.}
\tag{3.4}
\]

#### Proof

At a source point \(h\), source coupling gives
\((P(h),Q(h))=(\epsilon _0(h),\epsilon _1(h))\).  The source pair is
nonzero there, so \(H(h)\ne0\).  Cancelling \(H(h)\) gives

\[
 \psi_L([h:1])=\lambda(h).
\]

Both base-basis polynomials from (2.6) take values in \(B\) at \(h\in D\),
so the value lies on \(S_L\).  This proves (3.3).

For a selected slope, choose any \(z\in F_\eta\).  Equation (2.5) gives
\(\bar P(z)+\eta\bar Q(z)=0\), and the reduced pair cannot vanish
simultaneously.  Thus
\(\psi_L([z:1])=[\eta:1]\).  Again \(z\in D\subset B\), proving
(3.4). \(\square\)

## 4. Synchronization from the fixed source

Put

\[
 \Lambda=\lambda(\Sigma)\subseteq\mathbf P^1(F).
\tag{4.1}
\]

The cardinality of this fixed set gives an exhaustive trichotomy.

### 4.1 One label is impossible

If \(\Lambda=\{[a:b]\}\), then

\[
 b\bar P+a\bar Q
\tag{4.2}
\]

vanishes at every \(h\in\Sigma\).  It is nonzero by coefficient rank two,
has degree at most \(x\), and has \(s>x\) distinct roots, a contradiction.

### 4.2 Three labels determine the subline

Any three distinct points of \(\mathbf P^1(F)\) lie on a unique
\(B\)-subline.  Indeed, send them to \(0,1,\infty\); the image of
\(\mathbf P^1(B)\) is independent of the ordering because every permutation
of \(0,1,\infty\) is induced by an element of
\(\operatorname{PGL}_2(B)\).

Consequently, if \(|\Lambda|\ge3\), (3.3) forces every \(S_L\), across every
selector and record, to equal the one subline determined by any three fixed
source labels.

### 4.3 Exactly two labels: Frobenius recovers the twist

Suppose

\[
 \Lambda=\{\lambda_0,\lambda_\infty\}.
\tag{4.3}
\]

Fix once and for all, from the source data alone, one pair-coordinate
matrix in \(\operatorname{GL}_2(F)\) whose induced projective action on the
label coordinate \([-r_0:r_1]\) sends these labels to \(0=[0:1]\) and
\(\infty=[1:0]\).  Apply that same pair-coordinate matrix to the translated
received pair and to every explaining polynomial pair.  Denote the fixed
normalized source pair by
\((\rho _0,\rho _1)\), and put

\[
 \Sigma_0=\{h\in\Sigma:\rho _0(h)=0\},
 \qquad
 \Sigma_\infty=\{h\in\Sigma:\rho _1(h)=0\}.
\tag{4.4}
\]

These sets partition \(\Sigma\), and the other coordinate is nonzero on
each block.

For any record, its normalized \(B\)-subline contains \(0\) and
\(\infty\).  Every \(B\)-subline through those points is a scalar copy of
\(\mathbf P^1(B)\).  Equivalently, after a change of the base-polynomial
basis in (2.6), there are

\[
 \alpha,\beta\in F^\times,
 \qquad U,V\in B[X]
\tag{4.5}
\]

such that the normalized polynomial pair is

\[
 P'=\alpha L_{C_L}(X-\zeta)U,
 \qquad
 Q'=\beta L_{C_L}(X-\zeta)V.
\tag{4.6}
\]

The two normalized target fibers have at most \(x\) source points because
the corresponding nonzero polynomials \(U,V\) have degree at most \(x\).
Thus

\[
 |\Sigma_0|,|\Sigma_\infty|
 \ge s-x
 \ge67{,}474-49{,}055
 =18{,}419.
\tag{4.7}
\]

In particular each block contains three distinct fixed points.

For \(h\in\Sigma_0\), source coupling and (4.6) give

\[
 \rho _1(h)
 =\beta(h-\zeta)b_h,
 \qquad
 b_h=L_{C_L}(h)V(h)\in B^\times.
\tag{4.8}
\]

Since \(h\in B\), raising (4.8) to the \(p-1\) power removes \(b_h\):

\[
 \boxed{
 \rho _1(h)^{p-1}
 =\beta^{p-1}\frac{h-\zeta^p}{h-\zeta}.}
\tag{4.9}
\]

The right side is a nonconstant Möbius function of \(h\), because
\(\zeta\notin B\).  If two records yielded \((\zeta,c)\) and
\((\zeta',c')\), their two functions in (4.9) would agree on at least three
distinct points.  Their cross determinant has degree at most two, so the
functions coincide.  The unique pole then gives

\[
 \zeta=\zeta',
 \qquad c=c'.
\tag{4.10}
\]

Thus the nonbase twist is determined by the fixed source data.  Moreover,
the kernel of \(F^\times\to F^\times,\ z\mapsto z^{p-1}\) is exactly
\(B^\times\).  Hence (4.9)--(4.10) determine the coset

\[
 \beta B^\times.
\tag{4.11}
\]

The symmetric calculation on \(\Sigma_\infty\) determines

\[
 \alpha B^\times.
\tag{4.12}
\]

Therefore the ratio coset

\[
 (\alpha/\beta)B^\times
\tag{4.13}
\]

and the normalized scalar \(B\)-subline are fixed by the source pair alone.
Undoing the one fixed normalization gives one pair-global subline in the
original slope coordinates.  This proves synchronization also when the fixed
source has exactly two labels.

The proof remains valid if one swaps the names \(0,\infty\).  Scaling the
chosen \(\operatorname{GL}_2\) lift only scales \(\alpha,\beta\) in the
corresponding fixed coordinates and does not introduce selector dependence.

## 5. Pair-global owner theorem

Define \(S_{\rm src}\subseteq\mathbf P^1(F)\), using only the fixed source
pair, as follows.

- If \(|\Lambda|=1\), put \(S_{\rm src}=\varnothing\).
- If \(|\Lambda|\ge3\), use the unique \(B\)-subline containing three fixed
  labels, provided every source label lies on it; otherwise use the empty set.
- If \(|\Lambda|=2\), perform the fixed normalization in Section 4.3 and
  use the blocks in (4.4).  Require both blocks to contain at least three
  points.  Require a unique \(\zeta\in F\setminus B\) and nonzero constants
  \(c_0,c_\infty\in F^\times\) such that
  \[
   \rho _1(h)^{p-1}
    =c_0\frac{h-\zeta^p}{h-\zeta}
       \quad(h\in\Sigma_0),
   \qquad
   \rho _0(h)^{p-1}
    =c_\infty\frac{h-\zeta^p}{h-\zeta}
       \quad(h\in\Sigma_\infty).
  \tag{5.0}
  \]
  Also require \(c_0,c_\infty\) to lie in the image of
  \(z\mapsto z^{p-1}\) on \(F^\times\).  Their inverse images are unique
  cosets modulo \(B^\times\); choose any
  \(\beta,\alpha\in F^\times\) with
  \(\beta^{p-1}=c_0\) and \(\alpha^{p-1}=c_\infty\), define the normalized
  subline
  \[
   \{[-\alpha u:\beta v]:[u:v]\in\mathbf P^1(B)\},
  \]
  and undo the fixed label normalization.  If any existence, uniqueness,
  block-size, or power-image condition fails, use the empty set.

If no qualifying record exists, this definition may conservatively delete a
bounded intrinsic subline.  If a record does exist, Sections 3--4 prove that
the definition succeeds and that every record produces exactly this same
subline.

Put

\[
 Z_{\rm twist}
 =\{\eta\in\Gamma_{\rm in}:[\eta:1]\in S_{\rm src}\},
 \qquad
 \Gamma_{\rm out}=\Gamma_{\rm in}\setminus Z_{\rm twist}.
\tag{5.1}
\]

### Theorem 5.1 (pair-global common-twist source-subline owner)

For every \(\Gamma\subseteq\Gamma_{\rm in}\), every qualifying one-slack
common-factor record in every complete selector rebuilt on \(\Gamma\) has

\[
 \boxed{
 \Gamma_L^{\rm fin}
 \subseteq
 \{\eta\in F:[\eta:1]\in S_{\rm src}\}.}
\tag{5.2}
\]

Before using the first-match order, (5.2) gives the projective cap

\[
 |S_{\rm src}|\le p+1,
\tag{5.3}
\]

with equality whenever a subline is recovered.

Every finite source label belongs to the global tangent image
\(\mathcal T(\epsilon _0,\epsilon _1)\), which was deleted before the present
slot.  If ambient projective infinity is not in \(S_{\rm src}\), all \(p+1\)
subline points are finite and at least two finite source labels are absent.
If infinity is in the subline, there are only (p) finite points; if infinity
is one of the two source labels, at least one further finite source label is
absent, and otherwise at least two are absent.  The three-or-more-label case
only improves these bounds.  Consequently

\[
 \boxed{|Z_{\rm twist}|\le p-1=2{,}130{,}706{,}432.}
\tag{5.4}
\]

After the exact deletion (5.1), no qualifying one-slack common-factor record
can occur in a complete selector rebuilt on \(\Gamma_{\rm out}\).

#### Proof

Lemma 3.1 puts every source label and selected slope of a record on \(S_L\).
The three cases of Section 4 either rule out the record or prove
\(S_L=S_{\rm src}\), uniformly across selectors.  This proves (5.2).
Equation (5.4) follows from the cardinality of a projective \(B\)-subline and
the earlier exact tangent deletion just described.
The argument used only the fixed source and record-level hypotheses, so it
applies unchanged to every subset \(\Gamma\).  On
\(\Gamma_{\rm out}\), (5.1) makes the right side of (5.2) disjoint from the
available finite slopes, proving the post-restart exclusion. \(\square\)

The paid terminal is

```text
PAID_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST.
```

The former terminal

```text
UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST
```

is removed.  This is a closure of that component, not a closure of rank nine
or of the KoalaBear row.

## 6. First-match deletion and complete-selector restart

Charge only the exact incoming intersection (Z_{\rm twist}), then delete
it.  Apply later extension and base-slope owners only to
\(\Gamma_{\rm out}\).  Rebuild, rather than restrict and retain, all
selector-derived data:

1. the complete-selector universe;
2. the global carrier and small-family gates;
3. the affine-rank minimizer;
4. the carrier, \(V\), Padé matrices, \(K_0\), and \(d_V\);
5. the deficit histogram and rich-pencil atlas; and
6. all rank-at-most-three, rank-four-through-eight, and rank-nine terminals
   in their frozen order.

Restriction of a former complete selector witnesses nonemptiness of the new
selector universe and gives a new minimum rank no larger than the old one.
No old carrier, line, basis, chart, support, witness, determinant weight, or
rank-nine outlier direction is retained.  The fixed source pair and
translation remain unchanged.

## 7. Exact ledger movement

The source-subline owner is a new disjoint first-match block, so the
conservative movement is

\[
 \boxed{\Delta U_{\rm paid}=p-1=2{,}130{,}706{,}432.}
\tag{7.1}
\]

Starting from the banked predecessor values,

\[
 U_{\rm paid}^{\rm old}=2{,}605{,}562{,}836,
 \qquad
 B_{\rm remaining}^{\rm old}
 =274{,}980{,}725{,}505{,}832{,}251,
\tag{7.2}
\]

the new exact values are

\[
 \boxed{U_{\rm paid}^{\rm new}=4{,}736{,}269{,}268,}
\tag{7.3}
\]

\[
 \boxed{
 B_{\rm remaining}^{\rm new}
 =274{,}980{,}723{,}375{,}125{,}819.}
\tag{7.4}
\]

The exact rank-nine one-cut replay changes the sufficient low-deficit target
to

\[
 T_{18{,}014}=17{,}905{,}060{,}408{,}872,
\tag{7.5}
\]

while \(K_{\rm remaining}=4{,}807{,}520\) and the uniform break remains
\(J=166\).  These are downstream arithmetic consequences, not additional
mathematical payment.

The packet assigns no value to \(U_Q\) or the remaining \(U_A\), does not
compare the complete upper ledger with the target, and does not change the
unsafe-side reserve.

## 8. Remaining residual and stop conditions

The other one-slack component remains open:

```text
UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR.
```

Also open are non-full-outside source load, other residual
extension-valued strata, \(U_Q\), the complete profile envelope, and the
lower reserve.  No rank-at-least-ten work, generic elimination, Lean
formalization, stable-paper promotion, or KoalaBear closure is authorized by
this local theorem.

The companion Sage file is an exact toy control.  It tests projective
three-label synchronization, the two-label Frobenius pole/coset recovery, and
a nonbase-twist witness pencil.  It is not a deployed selector, a selector
census, or a proof of the symbolic theorem.
