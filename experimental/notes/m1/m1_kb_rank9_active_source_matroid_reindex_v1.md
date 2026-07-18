# M1 KoalaBear rank-nine active-source matroid reindex v1

## Status

**PROVED** exact universal/active source split, active-source nonloop lemma,
and sharp rank-eight matroid reindex. **PROVED** local implication route cut:
the existing regular-chart and source-plant hypotheses do not remove the
universal outside-carrier cell. **OPEN** deployed selector coverage, the
universal-cell payment, the active source-hit basis tail, and the KoalaBear
row.

The live terminals are

~~~text
UNPAID_UNIVERSAL_SOURCE_CELL
UNBOUND_ACTIVE_SOURCE_HIT_BASIS_TAIL
UNPAID_ACTIVE_RANK1_SELECTOR_COMPLETENESS
UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR
~~~

and the encompassing predecessor terminal remains

~~~text
UNBOUND_POST_TANGENT_SOURCE_LOAD.
~~~

This packet is stacked on
`m1_kb_rank9_projective_source_load_v1.md`. It does not move the ledger.

## 1. Frozen post-tangent interface

Use the exact KoalaBear row

\[
 n=2^{21},\quad k=2^{20},\quad A=1{,}116{,}048,
 \quad j=981{,}104,\quad t=A-k=67{,}472,
\tag{1.1}
\]

and the rebuilt post-tangent excess gate

\[
 E'_{\max}=
 5{,}284{,}472{,}953{,}556{,}748{,}839{,}425{,}672{,}939{,}211{,}329{,}356{,}986{,}005{,}299.
\tag{1.2}
\]

Fix one complete selector rebuilt after tangent deletion. Its carrier is

\[
 V=\bigcup_{\eta\in\Gamma}E_\eta.
\tag{1.3}
\]

For a contributing graph line \(L\), retain the predecessor notation

\[
 Z_L=\{x\in V:a_L(x)=b_L(x)=0\},\qquad
 W_L=V\setminus Z_L,
\tag{1.4}
\]

\[
 w_L=\beta_L(J_L-20),\qquad \beta_L>0,\quad J_L\ge21,
\tag{1.5}
\]

and

\[
 S_L=(D\setminus W_L)\cap\Sigma,qquad
 s_L=|S_L|\ge t-x_L+1\ge18{,}418.
\tag{1.6}
\]

All source, carrier, kernel, graph-line, polynomial-lift, regular-chart, and
determinant-mass data in this note must belong to this one selector. The
deployed existence of such a source-bound complete selector remains an
unproved predecessor input.

## 2. Exact universal/active source split

Put

\[
 U=\Sigma\setminus V,\qquad q=|U|,
\tag{2.1}
\]

and, for each line,

\[
 I_L=\Sigma\cap Z_L,\qquad r_L=|I_L|,
 \qquad z_L=|Z_L|.
\tag{2.2}
\]

### Lemma 2.1 (source-carrier split)

For every contributing line,

\[
 \boxed{S_L=U\sqcup I_L,\qquad s_L=q+r_L.}
\tag{2.3}
\]

Consequently

\[
 \boxed{r_L\ge\max\{0,t-x_L+1-q\}.}
\tag{2.4}
\]

#### Proof

Because \(W_L=V\setminus Z_L\),

\[
 D\setminus W_L=(D\setminus V)\sqcup Z_L.
\]

Intersecting this disjoint union with \(\Sigma\) gives

\[
 S_L=(\Sigma\setminus V)\sqcup(\Sigma\cap Z_L)=U\sqcup I_L.
\]

Taking cardinalities and using (1.6) proves (2.3)--(2.4). \(\square\)

The split exposes the first hard gate. If

\[
 q\le18{,}417,
\tag{2.5}
\]

then every contributing line has \(r_L>0\). Without (2.5), the printed plant
floor permits \(r_L=0\): all of a line's source plant may lie outside the
carrier, where the same-selector affine equations have rank zero.

## 3. Active source rows are matroid nonloops

Choose the fixed basis \(r_1,\ldots,r_8\) of \(K_0\), and let

\[
 g_h=(r_1(h),\ldots,r_8(h)).
\tag{3.1}
\]

The graph line has coordinates
\(z_\eta=\alpha_L+\eta\boldsymbol\beta_L\), and at every plant point

\[
 g_h\alpha_L=-u(h),\qquad
 g_h\boldsymbol\beta_L=-v(h).
\tag{3.2}
\]

### Lemma 3.1 (active nonloop)

If \(h\in I_L\), then

\[
 \boxed{g_h\ne0.}
\tag{3.3}
\]

#### Proof

Suppose \(g_h=0\). Equations (3.2) give \(u(h)=v(h)=0\). Every selected
error has the same-selector representation

\[
 e_\eta=u+\eta v+\sum_{i=1}^8z_{\eta,i}r_i,
\]

so \(e_\eta(h)=0\) for every \(\eta\in\Gamma\). This contradicts
\(h\in Z_L\subseteq V\) and the carrier identity
\(V=\bigcup_{\eta\in\Gamma}E_\eta\). Thus \(g_h\ne0\). \(\square\)

Hence each active source point is a nonloop of the representable rank-eight
row matroid on \(Z_L\). This is stronger than the ambient rank-two incidence
observation in the predecessor, but it is not yet a determinant-mass bound.

## 4. Sharp matroid exchange reindex

Let

\[
 \beta_{L,0}=
 \#\{B\subseteq Z_L:|B|=8,\ B\text{ is a }K_0\text{-basis},\ B\cap I_L=\varnothing\},
\tag{4.1}
\]

\[
 \beta_{L,1}=
 \#\{B\subseteq Z_L:|B|=8,\ B\text{ is a }K_0\text{-basis},\ |B\cap I_L|=1\},
\tag{4.2}
\]

and let \(\beta_{L,\mathrm{hit}}\) count all such bases meeting \(I_L\).
Thus

\[
 \beta_L=\beta_{L,0}+\beta_{L,\mathrm{hit}},
 \qquad \beta_{L,1}\le\beta_{L,\mathrm{hit}}.
\tag{4.3}
\]

### Theorem 4.1 (active-source basis exchange)

If \(r_L>0\), then

\[
 \boxed{
 r_L\beta_{L,0}
 \le (z_L-r_L-7)_+\,\beta_{L,1}.}
\tag{4.4}
\]

Consequently

\[
 \boxed{
 \beta_L\le C_L\beta_{L,\mathrm{hit}},\qquad
 C_L=\max\left\{1,\frac{z_L-7}{r_L}\right\}.}
\tag{4.5}
\]

#### Proof

Count directed exchanges \((B,h,b)\), where \(B\) is a basis avoiding
\(I_L\), \(h\in I_L\), \(b\in B\), and

\[
 B'=B\setminus\{b\}\cup\{h\}
\]

is a basis. Since \(h\) is a nonloop and \(B\) is a basis, the fundamental
circuit of \(h\) with respect to \(B\) contains an exchangeable element
\(b\). Thus every pair \((B,h)\) supplies at least one exchange, giving at
least \(r_L\beta_{L,0}\) directed exchanges.

Conversely, \(B'\) meets \(I_L\) exactly at \(h\). Recovering a basis
avoiding \(I_L\) replaces \(h\) by an element of

\[
 Z_L\setminus\bigl(I_L\cup(B'\setminus\{h\})\bigr),
\]

which has at most \(z_L-r_L-7\) elements. This proves (4.4). If that number
is negative, no avoiding basis exists. Otherwise

\[
 \beta_{L,0}
 \le\frac{z_L-r_L-7}{r_L}\beta_{L,1}
 \le\frac{z_L-r_L-7}{r_L}\beta_{L,\mathrm{hit}}.
\]

Adding \(\beta_{L,\mathrm{hit}}\) proves (4.5). \(\square\)

The coefficient is sharp under precisely these matroid hypotheses. Take a
rank-eight representable matroid consisting of seven coloops and one parallel
class of size \(z_L-7\), with exactly \(r_L\) members of the parallel class
in \(I_L\). Then

\[
 \beta_{L,0}=z_L-r_L-7,qquad
 \beta_{L,1}=\beta_{L,\mathrm{hit}}=r_L,
\]

and equality holds in (4.4)--(4.5). Thus an improvement must use the RS
support equations, the regular locator equations, completeness, or another
owner; it cannot follow from nonloop matroid data alone.

## 5. Exact load split and the new residual

Define the universal-cell excess

\[
 \mathcal E_{\mathrm{out}}
 =\sum_{L:r_L=0}\beta_L(J_L-20).
\tag{5.1}
\]

For \(r_L>0\), reallocate the whole line weight uniformly over \(I_L\):

\[
 \Lambda_h^{\mathrm{act}}
 =\sum_{\substack{L:r_L>0\\h\in I_L}}
   \frac{\beta_L(J_L-20)}{r_L}.
\tag{5.2}
\]

This is a new active reallocation, not the predecessor's allocation over all
of \(S_L=U\sqcup I_L\). It gives the exact identity

\[
 \boxed{
 \mathcal E_{20}^{\mathrm{nz}}
 =\mathcal E_{\mathrm{out}}
 +\sum_{h\in\Sigma\cap V}\Lambda_h^{\mathrm{act}}.}
\tag{5.3}
\]

Theorem 4.1 yields only

\[
 \boxed{
 \mathcal E_{20}^{\mathrm{nz}}
 \le \mathcal E_{\mathrm{out}}
 +\sum_{L:r_L>0}
 C_L\beta_{L,\mathrm{hit}}(J_L-20).}
\tag{5.4}
\]

This is the sharp endpoint of the source split plus abstract basis exchange.
Neither term on the right is bounded by the current contracts. In particular:

1. condition (2.5) would remove \(\mathcal E_{\mathrm{out}}\), but it is not
   currently proved by a producer or theorem;
2. even under (2.5), no existing regular-chart theorem bounds the weighted
   source-hit basis tail in (5.4).

Therefore (5.4) does not imply
\(\mathcal E_{20}^{\mathrm{nz}}\le E'_{\max}\), and the ledger does not move.

## 6. Full outside-source subcell

The extreme subcell

\[
 \Sigma\cap V=\varnothing
\tag{6.1}
\]

is stronger than merely having \(r_L=0\). It admits one additional exact
reduction, but that reduction still does not pay the determinant mass.

### Lemma 6.1 (rank one is impossible under full outside source)

Assume (6.1) and that the source syndrome line has rank two. Then every
contributing polynomial pair \((P_L,Q_L)\) has coefficient rank two.

#### Proof

Suppose instead that

\[
 (P_L,Q_L)=(rH,sH).
\]

At every point of \(\Sigma\subseteq D\setminus V\), zero extension and source
coupling give

\[
 (\epsilon_0,\epsilon_1)=(rH,sH).
\]

Off \(\Sigma\), both source vectors vanish. Thus the full-domain source pair
is proportional (including the cases \(r=0\) or \(s=0\)), so its syndrome
span has dimension at most one. This contradicts the transverse source-line
hypothesis. \(\square\)

For rank two, the common-root polynomial satisfies
\(c_L\le k-2\), rather than merely \(c_L\le k-1\). Since now
\(s_L=|\Sigma|\),

\[
 \boxed{|\Sigma|\ge t-x_L+2.}
\tag{6.2}
\]

If \(\nu=|V|-R\), then the outside-source root identity gives

\[
 c_L=(n-|V|-|\Sigma|)+z_L
     =k-\nu-|\Sigma|+z_L,
\]

and comparison with
\(c_L=A-x_L-|\Sigma|=k+t-x_L-|\Sigma|\) yields

\[
 z_L=t+\nu-x_L.
\tag{6.3}
\]

Moreover \(|\Sigma|\le|D\setminus V|=k-\nu\). Combining this with
(6.2) gives \(\nu\le j+x_L-2\), and therefore

\[
 \boxed{z_L=t+\nu-x_L\le t+j-2=k-2.}
\tag{6.4}
\]

Consequently the ambient determinant cap improves to

\[
 \beta_L\le\binom{k-2}{8}.
\tag{6.5}
\]

This improvement is numerically non-closing. Exact KoalaBear arithmetic gives

\[
 \binom{k-2}{8}
 =36{,}246{,}039{,}468{,}738{,}550{,}380{,}845{,}141{,}167{,}443{,}501{,}061{,}373{,}961.
\tag{6.6}
\]

The first single-line slope count for which the cap exceeds the remaining
budget is

\[
 J_L=20+\left\lfloor
 \frac{E'_{\max}}{\binom{k-2}{8}}
 \right\rfloor+1=166,
\tag{6.7}
\]

and

\[
 \binom{k-2}{8}(166-20)-E'_{\max}
 =7{,}448{,}808{,}879{,}079{,}516{,}177{,}717{,}671{,}235{,}421{,}797{,}974{,}593{,}007>0.
\tag{6.8}
\]

The source/support equations themselves permit this scale. Recall that the
deployed KoalaBear domain is a multiplicative subgroup
\(D\subset\mathbf F_p^\times\), so every point of \(D\) is nonzero. For
\(x_L=1\), choose disjoint sets

\[
 |\Sigma|=t+1,\qquad |C|=k-2,\qquad
 W=D\setminus(\Sigma\sqcup C),\quad |W|=j+1.
\tag{6.9}
\]

Let \(G=L_C\) and define

\[
 P=GX,qquad Q=-G.
\tag{6.10}
\]

Put \((\epsilon_0,\epsilon_1)=(P,Q)\) on \(\Sigma\), and zero elsewhere.
For every \(\rho\in W\), the explaining polynomial

\[
 P+\rho Q=G(X)(X-\rho)
\tag{6.11}
\]

gives an actual error supported on \(W\setminus\{\rho\}\), of size \(j\).
The exact agreement set is

\[
 \Sigma\sqcup C\sqcup\{\rho\},
\]

of size \(A\), and it is support-wise noncontained: agreement with either
source separately on \(\Sigma\sqcup C\) already forces the polynomial
\(P\) or \(Q\), while \(P(\rho)\ne0\) and \(Q(\rho)\ne0\) because
\(\rho\in W\subset D\subset\mathbf F_p^\times\) and \(G\) has no root in
\(W\). The source
syndrome pair is
independent as follows. A vanishing syndrome combination would give a
degree-less-than-\(k\) word equal to
\(G(\alpha X-\beta)\) on \(\Sigma\sqcup C\). Since

\[
 |\Sigma\sqcup C|=(t+1)+(k-2)=A-1>k-1,
\]

the two degree-less-than-\(k\) polynomials must agree identically. The full
source vector is zero on \(W\), so \(G(\alpha X-\beta)\) must also vanish on
every point of \(W\). Because \(G\) has no root in \(W\) and \(W\) contains
more than one point, this forces \(\alpha=\beta=0\).

Thus 166 distinct moving-root slopes are compatible with the exact
same-row source, support, rank-two, plant, and noncontainment equations. This
is a one-line construction, not a complete affine-rank-nine selector. Here
\(C\) is the outside-carrier gcd root set, not the atlas set \(Z_L\):
the carrier is \(V=W\), the one-line family has \(Z_L=\varnothing\), and
\(\beta_L=0\). It therefore demonstrates the compatible \(J_L=166\) scale
only; it does not construct the eight sparse outlier directions, their
regular charts, or positive determinant mass in (6.5). The remaining
promotion gate is therefore precise:

~~~text
UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR
~~~

Any closure of the full outside-source subcell must use the eight actual
outlier directions/regular first-match equations or a different complete
selector. Rank-one elimination and the degree cap alone are insufficient.

## 7. Exact active rank-one regular countercontrol

The active source-hit term in (5.4) also cannot be removed by combining rank
one, tangent deletion, affine rank nine, determinant mass, and regular-chart
equations locally. There is an exact record-level control over
\(F=\mathbf F_{1009}\) with

\[
 (n,k,R,j,A,t)=(50,10,40,36,14,4).
\tag{7.1}
\]

Let

\[
 H=\prod_{r=0}^{8}(X-r),\qquad (P_L,Q_L)=(0,H).
\tag{7.2}
\]

The source is supported on \(\Sigma=\{9,\ldots,43\}\), of size
\(35\le j\). Its values are frozen in the companion Python and Sage
replays. The selected family consists of 31 non-tangent slopes on the scalar
\(H\)-pencil and eight exact outlier directions. Every selected error has
weight 36 and exactly 14 agreements.

Exact linear algebra gives

\[
 \operatorname{rank}[e_\eta]=10,qquad
 \dim\operatorname{span}\{e_\eta-e_{\eta_0}\}=9,
\tag{7.3}
\]

\[
 \dim K_0=8,qquad
 K_0=\mathcal D_{\rm aff}\cap\operatorname{RS}(D,10),
 \qquad V=D.
\tag{7.4}
\]

The rich line has

\[
 Z_L=\{0,\ldots,12\},\qquad x_L=1,qquad
 S_L=\{9,10,11,12\},
\tag{7.5}
\]

so \(s_L=4=t-x_L+1\). All four plant points lie in the finite source fiber
\(\theta=0\). Among the \(\binom{13}{8}\) candidate row sets, exactly

\[
 \beta_L=1{,}197
\tag{7.6}
\]

are \(K_0\)-bases. Hence the surviving rank-one line has positive weight

\[
 \boxed{w_L=1{,}197(31-20)=13{,}167,}
\tag{7.7}
\]

with normalized load \(13{,}167/4\) at each plant point.

The zero-codeword slope \(0\) is in the tangent image, while all 39 selected
slopes are outside that image. After deleting zero, the 31 displayed slopes
exhaust the scalar-\(H\) component. On every selected agreement support,
neither individual source restriction is a degree-less-than-ten codeword.

For every one of the 39 records, the degree-36 split locator \(\ell_E\)
satisfies

\[
 (M_0+\eta M_1)\ell_E=0,qquad M_1\ell_E\ne0,
\tag{7.8}
\]

and the same four-column minor is nonzero. Thus tangent deletion, exact
source coupling, strong support-wise noncontainment, affine rank nine, the
actual kernel intersection, determinant mass, the plant floor, and regularity
do not imply zero rank-one load.

This construction is complete only for the displayed scalar-\(H\) component.
It is not proved to be a complete or rank-minimizing selector for every
MCA-bad codeword of the received pair, and earlier deployed owner masks have
not been executed. Its exact conclusion is therefore

~~~text
UNPAID_ACTIVE_RANK1_SELECTOR_COMPLETENESS
~~~

It refutes a local rank-one payment shortcut; it does not refute the deployed
existential Routes S/U/C.

## 8. Exact RS countercontrol for the universal cell

The existing cyclic control over \(\mathbf F_{67^2}\) supplies a rigorous
local countermodel to deleting the first term of (5.3). It uses

\[
 (n,k,R,j,A,t)=(34,13,21,20,14,1),
\]

\[
 \Sigma=\{D_0,D_1\},\qquad
 V=\{D_2,\ldots,D_{33}\}.
\tag{8.1}
\]

Hence \(q=2\). Its unique rich line has

\[
 J_L=21,qquad z_L=11,qquad
 \beta_L=\binom{11}{8}=165,qquad s_L=2.
\tag{8.2}
\]

Because \(I_L=\Sigma\cap Z_L=\varnothing\), it has \(r_L=0\) and

\[
 \boxed{\mathcal E_{\mathrm{out}}=165.}
\tag{8.3}
\]

The exact Sage replay verifies affine rank nine, raw rank ten, kernel rank
eight, all 29 same-support noncontainment checks, all 29 regular Hankel
equations, and all 29 nonzero regular minors. Thus source coupling,
noncontainment, rank nine, the plant, and the regular chart do not force
\(r_L>0\) or zero universal-cell load.

This selector is deliberately incomplete for the full 66-slope toy received
pair. A different complete selector routes that toy family to the earlier
low-carrier owner. Therefore (8.3) refutes the local same-selector implication,
not Route S/Route U for the deployed KoalaBear row.

## 9. Audit status and nonclaims

- **PROVED:** Lemma 2.1, Lemma 3.1, Theorem 4.1, its sharpness under
  representable-matroid hypotheses, the exact active load split, rank-one
  exclusion in the full outside-source subcell, and the rank-two degree cap.
- **IMPORTED/REPLAYED:** the post-tangent atlas identity, positive plant,
  same-selector equations, the exact cyclic rank-nine control, and the exact
  \(\mathbf F_{1009}\) active rank-one control.
- **UNPROVEN:** deployed compatible-selector production or uniform coverage;
  \(q\le18{,}417\); payment of \(\mathcal E_{\mathrm{out}}\); payment of the
  active source-hit basis tail; complete rank-nine payment; \(U_Q\); \(U_A\).
- **Parameter dependence:** Sections 2--6 are finite and field-uniform under
  their printed hypotheses. The number \(18{,}417\), (6.6)--(6.8), and the
  budget in (1.2) are KoalaBear-specific. Sections 7--8 are exact finite-field
  record-level countercontrols over \(\mathbf F_{1009}\) and
  \(\mathbf F_{67^2}\), respectively.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not used.
- **Global verdict:** YELLOW. The reindex and local route cut are GREEN; the
  deployed payment is open.

This packet does not:

- assume \(\Sigma\subseteq V\);
- discard universal rank-zero source points;
- turn one incomplete selector into a deployed counterexample;
- infer a determinant-mass bound from plant size or matroid exchange alone;
- double-charge the tangent owner;
- move \(U_{\rm paid}\), determine \(U_Q,U_A\), or close KoalaBear;
- begin rank at least ten, Lean, or stable-paper promotion.

## 10. Minimal next action

Attack exactly the two terms in (5.4), in first-match order.

1. Prove a complete-selector source/carrier dichotomy: either some paying
   rebuilt selector satisfies \(q\le18{,}417\), or the universal cell receives
   a named owner or an exact budget-fitting count.
2. On the \(q\le18{,}417\) branch, freeze the weighted source-hit basis sum
   in (5.4), including the eight outlier directions and equations (4.7)--(4.8)
   of the rich-pencil predecessor.
3. On the active rank-one branch, the local algebra is exhausted: require a
   complete-selector/minimality proof or execute the earlier owner masks on
   the exact \(\mathbf F_{1009}\) support template. Do not recycle the tangent
   charge.
4. On the full outside-source branch, test the exact 166-slope moving-root
   template (6.9)--(6.11) against the eight-outlier and regular first-match
   equations. Either those equations are inconsistent, or they produce the
   named multiselector route cut above.
5. Stop at the first compatible primitive component. A pointwise source-load
   estimate, abstract matroid bound, or additional toy sweep is not a
   substitute for those two obligations.
