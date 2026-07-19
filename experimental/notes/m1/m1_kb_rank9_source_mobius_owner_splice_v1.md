# M1 KoalaBear pair-global source--Möbius owner v1

Status: **PROVED PAIR-GLOBAL SOURCE--MÖBIUS OWNER / PROVED EXACT
FIRST-MATCH SPLICE / FULL-OUTSIDE MAXIMAL-GCD CELL PAID / KOALABEAR ROW
OPEN**.

This packet strengthens the conditional synchronization theorem in the
full-outside maximal-gcd predecessor.  The predecessor synchronized reduced
Möbius maps only after fixing one selector and therefore left a deployed
complete-selector provenance gate.  That gate is unnecessary: the SP3
translation and its sparse source pair are fixed once for the received pair,
so the same three source anchors synchronize qualifying maps even when they
come from different selectors.

The resulting owner is defined before choosing a selector.  It charges a set
of finite slopes once per received pair, deletes that set exactly, and then
restarts every selector-derived construction.  It closes only the
full-outside, coefficient-rank-two, full-gcd-degree `k-2` cell.  Lower-gcd,
non-full-outside, \(U_Q\), and residual \(U_A\) remain open.

## 1. Row and pair-global source data

Fix the KoalaBear row

\[
 p=2{,}130{,}706{,}433,
 \qquad B=\mathbf F_p\subset F=\mathbf F_{p^6},
 \qquad D\subset B,\qquad |D|=n,
\]

\[
 n=2^{21},\quad k=2^{20},\quad A=1{,}116{,}048,
 \quad j=n-A=981{,}104,
 \quad t=A-k=67{,}472.
\tag{1.1}
\]

Fix one received pair and the single SP3 translation used for that pair.
Write its translated sparse source pair as

\[
 (\epsilon _0,\epsilon _1),\qquad
 \Sigma=\operatorname{supp}(\epsilon _0)
       \cup\operatorname{supp}(\epsilon _1)\subseteq D.
\tag{1.2}
\]

No union over alternative SP3 translations is taken.  For every
\(h\in\Sigma\), the pair
\((\epsilon _0(h),\epsilon _1(h))\) is nonzero, so the projective source
label

\[
 \lambda(h)=[-\epsilon _0(h):\epsilon _1(h)]\in\mathbf P^1(F)
\tag{1.3}
\]

is defined.

The full-outside rank-two source floor is

\[
 s_0:=t-\left\lfloor\frac j{20}\right\rfloor+2
 =67{,}472-49{,}055+2=18{,}419.
\tag{1.4}
\]

## 2. Intrinsic source--Möbius image

Call the source data **Möbius-compatible** if \(|\Sigma|\ge s_0\) and there
exists \(\phi\in\operatorname{PGL}_2(F)\) such that

\[
 \phi([h:1])=\lambda(h)
 \qquad(h\in\Sigma).
\tag{2.1}
\]

Such a map is unique: it is determined by its values at any three distinct
inputs in \(\Sigma\).  Define the finite source--Möbius image by

\[
 \mathcal M(\epsilon _0,\epsilon _1)=
 \begin{cases}
 \{\eta\in F:\ [\eta:1]=\phi([x:1])
       \text{ for some }x\in D\setminus\Sigma\},
       &\text{if the source data are Möbius-compatible},\\[2mm]
 \varnothing,&\text{otherwise}.
 \end{cases}
\tag{2.2}
\]

This definition is intrinsic to the received pair and its fixed translation.
It contains no selector, carrier, graph line, support, determinant basis, or
witness multiplicity.

Let \(\Gamma_{\rm in}\) be the exact finite bad-slope set remaining after
the globally earlier first-match owners.  Put

\[
 Z_{\rm SMob}=\Gamma_{\rm in}\cap
   \mathcal M(\epsilon _0,\epsilon _1),
 \qquad
 \Gamma_{\rm out}=\Gamma_{\rm in}\setminus Z_{\rm SMob}.
\tag{2.3}
\]

### Theorem 2.1 (pair-global source--Möbius owner)

Fix the received pair and translation above.  Quantify over every complete
selector \(\sigma\) that can be built on \(\Gamma_{\rm in}\).  For each
selector, quantify over every contributing rich graph line \(L\) satisfying
the predecessor's printed hypotheses:

- carrier \(V_\sigma\subseteq D\) and full-outside condition
  \(V_\sigma\cap\Sigma=\varnothing\);
- contributing low-deficit rich-line conditions
  \(\beta_{\sigma,L}>0\), \(J_{\sigma,L}\ge21\), and
  \(x_{\sigma,L}\le\lfloor j/20\rfloor\);
- coefficient rank two;
- full monic gcd
  \(H_{\sigma,L}=\gcd(P_{\sigma,L},Q_{\sigma,L})\) of degree \(k-2\);
- the fixed source equations, the inherited source-rank-two floor
  \(|\Sigma|\ge t-x_{\sigma,L}+2\), and the moving-root transversality
  contract.

Then all such records, across all selectors, have one common reduced map
\(\phi\), and

\[
 \boxed{
 \bigcup_{\sigma}
 \bigcup_{L\ \mathrm{qualifying}}
 \Gamma_{\sigma,L}^{\rm fin}
 \subseteq
 \mathcal M(\epsilon _0,\epsilon _1).}
\tag{2.4}
\]

Consequently

\[
 \boxed{
 |Z_{\rm SMob}|
 \le |\mathcal M(\epsilon _0,\epsilon _1)|
 \le |D\setminus\Sigma|
 \le n-s_0
 =2{,}078{,}733.}
\tag{2.5}
\]

### Proof

Take one qualifying record \((\sigma,L)\).  Full gcd degree \(k-2\) and
coefficient rank two give

\[
 P_{\sigma,L}=H_{\sigma,L}(U_1X+U_0),\qquad
 Q_{\sigma,L}=H_{\sigma,L}(V_1X+V_0),
\tag{2.6}
\]

with \(U_1V_0-U_0V_1\ne0\).  Its reduced projective map is

\[
 \phi_{\sigma,L}([X:Z])
 =[-(U_1X+U_0Z):V_1X+V_0Z].
\tag{2.7}
\]

For every \(h\in\Sigma\), full-outside source coupling gives

\[
 P_{\sigma,L}(h)=\epsilon _0(h),\qquad
 Q_{\sigma,L}(h)=\epsilon _1(h).
\tag{2.8}
\]

The pair on the right is nonzero, so
\(H_{\sigma,L}(h)\ne0\).  Cancelling the common factor projectively yields

\[
 \phi_{\sigma,L}([h:1])
 =[-\epsilon _0(h):\epsilon _1(h)]
 =\lambda(h)
 \qquad(h\in\Sigma).
\tag{2.9}
\]

The source floor (1.4) applies to every qualifying record.  Thus any two
maps obtained from any two selectors agree on at least three common inputs
and are equal by three-point rigidity in \(\operatorname{PGL}_2(F)\).  The
word "common" refers only to the reduced map and the union of slope labels;
no determinant weight, atlas excess, \(\beta_L\), or \(J_L\) is mixed across
selectors.

For a selected finite slope \(\eta\in\Gamma_{\sigma,L}^{\rm fin}\), the
moving-root bridge supplies \(x\in W_{\sigma,L}\subseteq V_\sigma\) such
that

\[
 [\eta:1]=\phi_{\sigma,L}([x:1]).
\tag{2.10}
\]

Since \(V_\sigma\subseteq D\) and
\(V_\sigma\cap\Sigma=\varnothing\), one has
\(x\in D\setminus\Sigma\).  Equations (2.2), (2.9), and (2.10) prove
(2.4).  If \(|\Sigma|<s_0\), the inherited source floor excludes every
qualifying record; if (2.1) fails, (2.9) shows that no qualifying record can
exist.  Thus the empty branch of (2.2) is also correct.

Finally, a Möbius map is injective on \(\mathbf P^1(F)\).  Distinct inputs
in \(D\setminus\Sigma\) therefore have distinct projective images.  Removing
the possible image at projective infinity cannot increase the number of
finite slopes.  This proves (2.5). \(\square\)

## 3. Exact first-match splice and selector restart

Insert `source_mobius_full_outside_maximal_gcd` immediately after
`projective_base_pair_C5` and before the residual extension-valued and base
cells.  The owner is charged once per received pair, after intersection with
the exact incoming residual as in (2.3).

This is an ordinary global first-match deletion.  It is valid even when
\(\mathcal M\) contains a residual bad slope that has no qualifying
maximal-gcd witness: deleting additional slopes from a uniformly bounded
pair-global set only reduces every later family.  Earlier overlap is removed
by the intersection in (2.3), and later overlap is removed by the exact set
difference.

After deletion:

1. apply the later pair-global extension and residual-base owner cells to
   the exact outgoing set;
2. rebuild the complete-selector universe on the surviving set;
3. rerun the global carrier gate and small-family gate;
4. choose a fresh affine-rank minimizer;
5. recompute the carrier, \(V\), \(H_V\), \(K_0\), \(d_V\), deficit
   histogram, and rich-pencil atlas;
6. replay the rank-at-most-three, rank-four-through-eight, and rank-nine
   terminals in their established order.

Restriction of any old complete selector certifies that the rebuilt selector
universe is nonempty.  Restriction of an old rank-nine selector gives new
minimum rank at most nine, but it does not preserve any old derived field.
The pair-global source data (1.2) remain fixed; selector-derived data do not.

## 4. Joint C5/source--Möbius/base block

The projective-base C5 owner and the source--Möbius owner are not independent
additive cases.

If the syndrome matrix \(Y_R\) has rank zero, the predecessor's noncontained
exact-witness residual is empty.  Hence assume \(\operatorname{rank}Y_R>0\),
so the intrinsic projective syndrome field is defined.

If that intrinsic projective syndrome field is \(B\),
canonical C5 owns every post-branch-5 finite slope.  Every later cell is empty
and the joint charge is at most

\[
 p+1.
\tag{4.1}
\]

If the intrinsic projective syndrome field is not \(B\), the canonical base
C5 cell is empty.  The source--Möbius cell has cap \(n-s_0\), and the exact
later residual-base owner has cap \(p\).  Exact deletion makes those two sets
disjoint, so this case has cap

\[
 p+n-s_0.
\tag{4.2}
\]

The uniform pair-global block is therefore the maximum

\[
 \boxed{
 U_{C5/{\rm SMob}/B}
 =\max\{p+1,\ p+n-s_0\}
 =p+n-s_0
 =2{,}132{,}785{,}166.}
\tag{4.3}
\]

It is not the sum \((p+1)+(n-s_0)+p\).  The old C5/base block was \(p+1\),
so the exact ledger movement is

\[
 (p+n-s_0)-(p+1)=n-s_0-1=2{,}078{,}732.
\tag{4.4}
\]

## 5. Exact ledger movement

The predecessor ledger is

\[
 U_{\rm paid}^{\rm old}=2{,}603{,}484{,}104,
 \qquad
 B_{\rm remaining}^{\rm old}
 =274{,}980{,}725{,}507{,}910{,}983.
\tag{5.1}
\]

Replacing its joint block by (4.3) gives

\[
 \boxed{U_{\rm paid}=2{,}605{,}562{,}836,}
\tag{5.2}
\]

\[
 \boxed{B_{\rm remaining}
 =274{,}980{,}725{,}505{,}832{,}251.}
\tag{5.3}
\]

The exact one-cut replay gives

\[
 T_{18{,}014}=17{,}907{,}568{,}905{,}216,
\tag{5.4}
\]

\[
 E_{\max}
 =5{,}284{,}446{,}868{,}708{,}864{,}089{,}047{,}283{,}796,
 538{,}880{,}969{,}739{,}059{,}774,
\tag{5.5}
\]

\[
 K_{\rm remaining}=4{,}807{,}520,
 \qquad J_{\rm break}=166.
\tag{5.6}
\]

The tail target drops by \(2{,}447{,}306\) relative to the C5 predecessor.
The values of \(U_Q\) and residual \(U_A\) remain unknown, so (5.2)--(5.6)
do not close the KoalaBear row.

## 6. Exact controls and falsifiers

The companion Sage replay works over
\(\mathbf F_5\subset\mathbf F_{5^6}\).  It treats two distinct carriers and
polynomial pairs as selector-carrier proxies for the same source pair and
checks that their selected moving roots map into one common image of
\(D\setminus\Sigma\).  It does not construct complete selector witness
assignments or the \(\beta_L,J_L\) rich-line predicates.  It also checks:

- distinct nonbase full gcd factors do not affect the common reduced map;
- a different-source-label reduced-map proxy can produce a different map,
  illustrating why alternative translations may not be unioned;
- two source anchors do not synchronize two Möbius maps;
- noninjective source labels admit no compatible Möbius map;
- a moving root in \(\Sigma\) is outside the permitted source--Möbius image;
- a projective-infinity image is not counted as a finite slope.

These are exact toy-scale controls for the projective bookkeeping.  They do
not instantiate a deployed selector and are not used as proof of Theorem 2.1.

The Python checker binds the theorem to the exact predecessor payloads,
recomputes every integer above, writes a canonical JSON certificate, and
rejects mutations of the translation, anchors, compatibility, full-outside
condition, moving-root bridge, owner order, deletion/restart, maximum rule,
ledger links, source hashes, and scope guards.

## 7. Closed cell, residual route cuts, and verdict

This packet removes

```text
UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE
```

as a blocker for the printed full-outside maximal-gcd cell.  No Route S/U/C
selector inventory is needed for that payment.  The paid terminal is

```text
PAID_PAIR_GLOBAL_SOURCE_MOBIUS_MAXIMAL_GCD.
```

The following remain open:

```text
UNPAID_NO_COMPATIBLE_SOURCE_MOBIUS_RECORD
UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP
UNBOUND_POST_TANGENT_SOURCE_LOAD
```

The first is a primitive route cut for broader residuals: a slope surviving
the owner has no compatible full-outside maximal-gcd source--Möbius record.
It must not be forced into this owner.  The second covers lower full-gcd
degree.  The third includes non-full-outside and other source-load cells.

**Local verdict:** GREEN.  The pair-global source--Möbius theorem, exact
first-match deletion, and maximum-not-sum ledger movement are proved under
the printed predecessor contracts.

**Global verdict:** YELLOW.  The KoalaBear row, \(U_Q\), residual \(U_A\),
lower-gcd maps, and other rank-nine components remain unresolved.  No
rank-at-least-ten work, Lean formalization, or stable-paper promotion is
authorized by this packet.
