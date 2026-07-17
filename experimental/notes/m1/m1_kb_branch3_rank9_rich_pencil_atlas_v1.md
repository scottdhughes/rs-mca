# M1 KoalaBear rank-nine rich-pencil aggregate route cut v1

- **Status:** PROVED canonical rich-pencil identity / PROVED exact scalar
  route cut / exact generic-local control / deployed incidence OPEN / no
  ledger movement.
- **Scope:** the low-deficit part of one fixed complete affine-rank-nine
  selector on the source-bound sparse successor at
  \(A=1{,}116{,}048\).
- **Predecessors:**
  m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md,
  m1_kb_branch3_5_mask_contract_v1.md,
  m1_kb_branch3_rank9_sparse_chart_boundary_v1.md, and
  m1_rank9_regular_locator_span_shortcut_refuted_v1.md.
- **Companion checks:**
  verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.py and
  verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1.sage.

The fixed-basis predecessor reduced the missing tail to

\[
 \mathcal E_{20}
 =\sum_{B\in\binom V8}(m_B-20)_+
 \le E_{\max},
\tag{0.1}
\]

where

\[
 E_{\max}
 =5{,}284{,}485{,}264{,}881{,}189{,}380{,}664{,}190{,}436{,}821{,}715{,}347{,}228{,}277{,}374.
\tag{0.2}
\]

It also proved that the pointwise cap \(m_B\le20\) is false.  The next
legitimate object is therefore not another basis-by-basis owner.  This packet
groups every excess basis canonically by the affine graph line, equivalently
the sparse codeword pencil, that it determines.

The result is an exact identity and a sharper missing theorem.  It does not
bound the deployed rich pencils.  An exact scalar relaxation at
\(x=M-j=1\) shows that the already proved per-line, MDS, degree, and plant-size
constraints still permit one component to exceed (0.2).  Deployed polynomial,
domain, selector-exhaustion, or source-bound first-match coupling must be
load-bearing.

## 1. Frozen selector and deficit tail

Use

\[
 n=2{,}097{,}152,\qquad k=1{,}048{,}576,\qquad
 A=1{,}116{,}048,
\]

\[
 R=n-k=1{,}048{,}576,\qquad
 j=n-A=981{,}104,\qquad
 t=R-j=67{,}472.
\tag{1.1}
\]

Fix one complete selected-witness family \(\Gamma\) with intrinsic affine
rank nine.  On its complete basis carrier \(V\), the actual errors have the
proved representation

\[
 e_\eta=u+\eta v+w_\eta,\qquad
 w_\eta\in K_0,\qquad \dim K_0=8,
\tag{1.2}
\]

with

\[
 Hu=y_0,\qquad Hv=y_1\ne0.
\tag{1.3}
\]

Let

\[
 E_\eta=\operatorname{supp}(e_\eta),\qquad
 T_\eta=V\setminus E_\eta,\qquad
 \delta_\eta=j-|E_\eta|.
\tag{1.4}
\]

For the cutoff \(D_0=18{,}014\), put

\[
 \Gamma_D=\{\eta\in\Gamma:0\le\delta_\eta\le D_0\}.
\tag{1.5}
\]

Choose a basis \(r_1,\ldots,r_8\) of \(K_0\) and write

\[
 w_\eta=\sum_{i=1}^8z_{\eta,i}r_i,\qquad z_\eta\in F^8.
\tag{1.6}
\]

The graph points \((\eta,z_\eta)\) are distinct because their first
coordinates are distinct.

## 2. Canonical affine graph lines

For \(\alpha,\beta\in F^8\), define the graph line

\[
 L_{\alpha,\beta}
 =\{(\eta,\alpha+\eta\beta):\eta\in F\}.
\tag{2.1}
\]

Its selected slopes, size, and word pencil are

\[
 \Gamma_L
 =\{\eta\in\Gamma_D:z_\eta=\alpha+\eta\beta\},
 \qquad J_L=|\Gamma_L|,
\tag{2.2}
\]

\[
 a_L=u+\sum_i\alpha_i r_i,\qquad
 b_L=v+\sum_i\beta_i r_i.
\tag{2.3}
\]

Thus

\[
 e_\eta=a_L+\eta b_L\qquad(\eta\in\Gamma_L).
\tag{2.4}
\]

Let

\[
 Z_L=\{x\in V:a_L(x)=b_L(x)=0\},\qquad
 W_L=V\setminus Z_L,
\tag{2.5}
\]

\[
 M_L=|W_L|,\qquad x_L=M_L-j.
\tag{2.6}
\]

Extend \(a_L,b_L\) by zero on \(D\setminus V\).  Thus the full-domain
common-zero set is \(D\setminus W_L\), while the basis mass below uses only
the \(K_0\)-rows indexed by \(V\).

If \(g_x\in F^8\) is the coordinate row of the chosen \(K_0\) generator,
define the exact independent-basis mass

\[
 \beta_L
 =
 \#\left\{
 B\in\binom{Z_L}{8}:
 \det(g_x)_{x\in B}\ne0
 \right\}.
\tag{2.7}
\]

Only graph lines with \(J_L\ge21\) can contribute to (0.1).

## 3. Exact rich-pencil atlas identity

### Theorem 3.1

For the fixed selector and cutoff (1.5),

\[
 \boxed{
 \mathcal E_{20}
 =\sum_{L:J_L\ge21}\beta_L(J_L-20).}
\tag{3.1}
\]

The sum is over distinct graph lines, not over pairs of slopes or choices of
bases.

### Proof

Let \(B\subseteq V\) be an eight-subset whose \(K_0\)-rows form a basis and
whose multiplicity

\[
 m_B=\#\{\eta\in\Gamma_D:B\subseteq T_\eta\}
\]

is at least 21.  Restriction

\[
 \rho_B:K_0\longrightarrow F^B
\]

is an isomorphism.  The equations \(e_\eta|_B=0\) uniquely force

\[
 w_\eta|_B=-u|_B-\eta v|_B.
\]

Hence all graph points belonging to \(\Gamma_B\) lie on one unique graph
line \(L_B\).  Conversely, if \(B\) is an independent eight-subset of
\(Z_L\), then (2.4) vanishes on \(B\) for every \(\eta\in\Gamma_L\).
Any further selected slope vanishing on \(B\) is forced by the same
restriction equations to lie on \(L\).  Therefore

\[
 \Gamma_B=\Gamma_L,\qquad m_B=J_L.
\tag{3.2}
\]

Thus rich bases are partitioned, without overlap, by the unique graph line
they determine.  Line \(L\) contains exactly the \(\beta_L\) independent
bases in \(Z_L\), and each contributes \(J_L-20\).  Summing proves (3.1).
\(\square\)

The coordinates \(z_\eta\) depend on the chosen basis of \(K_0\), but the
underlying word pencil \((a_L,b_L)\), its common-zero set, and the total in
(3.1) do not.

## 4. Exact moving-zero and support equations

For \(\eta\in\Gamma_L\), define

\[
 F_{\eta,L}
 =\{x\in W_L:a_L(x)+\eta b_L(x)=0\}.
\tag{4.1}
\]

Then

\[
 E_\eta=W_L\setminus F_{\eta,L},
\qquad
 |F_{\eta,L}|=M_L-|E_\eta|=x_L+\delta_\eta.
\tag{4.2}
\]

At a fixed coordinate of \(W_L\), a nonzero affine function of \(\eta\)
vanishes at at most one slope.  Hence the \(F_{\eta,L}\) are pairwise
disjoint and

\[
 \boxed{
 J_Lx_L+\sum_{\eta\in\Gamma_L}\delta_\eta
 \le j+x_L.}
\tag{4.3}
\]

If \(\beta_L>0\), choose an independent \(B\subseteq Z_L\).  Transversality
implies \(F_{\eta,L}\ne\varnothing\) for every selected slope: otherwise
\(b_L\) and \(a_L=e_\eta-\eta b_L\) would both be supported on \(E_\eta\),
giving \(y_1\)- and \(y_0\)-lifts on the same actual support.  Therefore

\[
 x_L+\delta_\eta\ge1.
\tag{4.4}
\]

For a rich low-deficit line, (4.3)--(4.4) give the exact necessary outer
interval

\[
 \boxed{-18{,}013\le x_L\le
 \left\lfloor\frac j{20}\right\rfloor
 =49{,}055.}
\tag{4.5}
\]

For any padded radius-\(j\) locator support \(O_\eta\), write

\[
 O_\eta=E_\eta\sqcup P_\eta,\qquad |P_\eta|=\delta_\eta.
\tag{4.6}
\]

The support locators obey

\[
 L_{E_\eta}L_{F_{\eta,L}}=L_{W_L},
\qquad
 L_{O_\eta}=L_{E_\eta}L_{P_\eta}.
\tag{4.7}
\]

On the regular sparse chart the same slope must also satisfy

\[
 \Delta(\eta)\ne0,\qquad
 (H_1+\eta H_2)\ell_{O_\eta}=0,\qquad
 H_2\ell_{O_\eta}\ne0.
\tag{4.8}
\]

Equations (4.7)--(4.8), not only (4.3), are the fixed support-incidence
system for a future symbolic attack.

## 5. Sparse codeword-pencil and forced plant

On the source-bound sparse route, let

\[
 (\epsilon_0,\epsilon_1),\qquad
 \Sigma=\operatorname{supp}(\epsilon_0)\cup
        \operatorname{supp}(\epsilon_1),\qquad |\Sigma|\le j
\tag{5.1}
\]

be the exact translated received pair.  Each graph line corresponds to two
Reed--Solomon code polynomials \(P_L,Q_L\), of degree at most \(k-1\), with

\[
 a_L=\epsilon_0-\operatorname{ev}(P_L),\qquad
 b_L=\epsilon_1-\operatorname{ev}(Q_L).
\tag{5.2}
\]

Suppose first that at least one of \(P_L,Q_L\) is nonzero.  Every point of
\((D\setminus W_L)\setminus\Sigma\) is then a common domain root of
\(P_L\) and \(Q_L\).  Therefore

\[
 G_L:=
 L_{(D\setminus W_L)\setminus\Sigma}
 \mid\gcd(P_L,Q_L).
\tag{5.3}
\]

\[
 A-x_L-|\Sigma|
 \le\deg G_L\le k-1.
\tag{5.4}
\]

Moreover,

\[
 |(D\setminus W_L)\cap\Sigma|
 =A-x_L-\deg G_L
 \ge t-x_L+1.
\tag{5.5}
\]

Thus every nonzero rich line has at least \(t-x_L+1\) source-bound common
agreement points inside the sparse support.  Throughout (4.5), this lower
bound is positive; at the upper endpoint it is 18,418.

If \(P_L=Q_L=0\), then \(a_L=\epsilon_0\),
\(b_L=\epsilon_1\), and \(W_L=\Sigma\), so \(M_L\le j\) and
\(x_L\le0\).  This harmless zero-codeword pencil remains inside the atlas,
but no GCD degree is asserted for it.

Equation (5.5) is a precise plant, but it is not a paid owner.  The
branch-3--5 contract proves that branch 5 has no declared source-bound
algebraic plant family or distinct-slope payment.  An arbitrary set of
common agreement points cannot be relabelled as a paid planted prefix.

## 6. Exact hostile scalar relaxation

The already proved scalar constraints do not imply (0.1).  Take the permitted
full carrier \(V=D\) and

\[
 x=1,\qquad M=j+1,\qquad J=109,\qquad
 \delta_\eta=0\quad(1\le\eta\le109).
\tag{6.1}
\]

The moving-zero inequality is feasible because

\[
 Jx=109\le j+1=981{,}105.
\tag{6.2}
\]

The full-domain common-zero set has size

\[
 n-M=A-1=1{,}116{,}047.
\tag{6.3}
\]

The ambient allowance in which every eight-subset is independent is

\[
\begin{aligned}
 \beta_{\rm all}
 &=\binom{A-1}{8}\\
 &=59{,}693{,}694{,}123{,}933{,}928{,}155{,}753{,}913{,}658{,}726{,}468{,}844{,}598{,}995.
\end{aligned}
\tag{6.4}
\]

Only

\[
\begin{aligned}
 \beta_{\rm break}
 &=\left\lfloor\frac{E_{\max}}{109-20}\right\rfloor+1\\
 &=59{,}376{,}238{,}931{,}249{,}318{,}883{,}867{,}308{,}278{,}895{,}678{,}058{,}744{,}690
\end{aligned}
\tag{6.5}
\]

bases are needed to violate (0.1).  Thus

\[
 \beta_{\rm all}(109-20)-E_{\max}
 =
 28{,}253{,}512{,}148{,}930{,}225{,}197{,}907{,}878{,}804{,}940{,}379{,}941{,}033{,}181
 >0.
\tag{6.6}
\]

The polynomial degree floors are also scalar-feasible.  With
\(|\Sigma|=j\), (5.4) only requires

\[
 \deg G_L\ge A-1-j=134{,}943<k,
\tag{6.7}
\]

and (5.5) requires 67,472 planted agreement points inside \(\Sigma\).

This is an exact relaxation witness, not a Reed--Solomon selector.  It does
not prove that \(\beta_{\rm all}\) is attained together with the rank-nine
outlier directions, exact witness exhaustion, KoalaBear domain, or regular
first-match gates.  It proves only the sharp route cut:

> per-line zero incidence, ambient basis capacity, the present MDS row-flat
> constraints, and the polynomial degree/plant-size inequalities do not by
> themselves imply the aggregate gate.

The missing theorem must couple the determinant mass \(\beta_L\), the rich
slope count \(J_L\), the eight outlier directions which create rank nine,
and the source-bound sparse equations.

## 7. Exact generic-local atlas control

The Sage companion reuses the exact \(j=20\), \(\mathbb F_{2^{37}}\)
five-pencil family from the fixed-basis predecessor.  It enumerates only the
105 complete size-12 zero masks:

\[
 105\binom{12}{8}=51{,}975
\]

candidate mask-basis incidences.  It obtains

\[
 (\beta_L)_L=(161,165,165,161,165),
\tag{7.1}
\]

\[
 \mathcal E_{20}^{\rm direct}
 =\mathcal E_{20}^{\rm atlas}
 =817.
\tag{7.2}
\]

There are 51,765 valid mask-basis incidences, 35,238 distinct valid bases,
and maximum multiplicity 21.  Each of the five rich graph lines has
\(J_L=21\), \(M_L=21\), \(x_L=1\), zero deficits, common GCD degree 11,
and two planted sparse-support agreements.

This proves the atlas identity on one exact generic-local family.  It neither
instantiates the KoalaBear field/domain nor exceeds the deployed aggregate
allowance.

## 8. Source-bound first-match semantics

The branch-3--5 contract forbids a residual described as “after branches
3--5.”  Branch 4 supplies executable Q0 membership but only partial payment,
and branch 5 remains source-unbound.  A legitimate rich-pencil theorem must
therefore cover the whole declared sparse rank-nine successor envelope, with
only actually executable global projections removed.

The sparse tangent and chosen-minor cells have the local disjoint cap

\[
 j+(R-j)=R.
\tag{8.1}
\]

If a future theorem proves their global source-bound aggregation before the
rich atlas, the corresponding diagnostic excess allowance is

\[
\begin{aligned}
 E_{\max}^{\rm reg}
 &=(17{,}907{,}572{,}507{,}584-R+1)
   \binom{67{,}480}{8}
   -20\binom n8-1\\
 &=5{,}284{,}474{,}088{,}536{,}964{,}647{,}104{,}906{,}794{,}161{,}883{,}442{,}156{,}354{,}174.
\end{aligned}
\tag{8.2}
\]

That global aggregation is not currently proved, so (8.2) is diagnostic
only.  The conservative live gate remains (0.1)--(0.2).

The fail-closed terminal is

~~~text
UNPAID_SOURCE_BOUND_RICH_PENCIL_AGGREGATE
~~~

and the ledger remains

\[
 U_{\rm paid}=2{,}602{,}502{,}999,\qquad
 B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\tag{8.3}
\]

## 9. Audit status and nonclaims

- **PROVED:** canonical graph-line decomposition, exact aggregate identity,
  moving-zero equations, rich-line necessary \(x\)-interval,
  nonzero-codeword sparse GCD/plant implication, and hostile scalar
  relaxation.
- **EXACT CONTROL:** the \(\mathbb F_{2^{37}}\) five-pencil atlas replay.
- **UNPROVEN:** deployed weighted rich-pencil incidence, full sparse
  first-match aggregation, source-bound plant payment, lower Q0 rungs,
  rank at least ten, \(U_Q\), and \(U_A\).
- **Parameter dependence:** Sections 1, 6, and 8 use exact KoalaBear
  integers; Sections 2--5 are field-uniform under the printed selector and
  sparse-translation hypotheses.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** all printed arithmetic is exact.  The Sage family
  is toy-scale and generic-local, not deployed-field evidence.
- **Global verdict:** YELLOW.  This is a rigorous compiler and route cut,
  not rank-nine payment or KoalaBear closure.

This packet does not:

- realize the hostile scalar profile as a Reed--Solomon selector;
- claim \(\beta_L=\binom{|Z_L|}{8}\) in the deployed residual;
- define or use a fictitious post-branches-3--5 complement;
- turn arbitrary planted points into a branch-5 owner;
- sum local tangent/boundary caps into the global ledger;
- move \(U_{\rm paid}\) or \(B_{\rm rem}\);
- close rank nine, branch 3, or the KoalaBear row;
- attack intrinsic rank at least ten;
- determine \(U_Q\) or \(U_A\);
- authorize Lean or stable-paper promotion.

## 10. Minimal next action

Machine-encode the source-bound rich-pencil atlas on exact cyclic
\(\mathbb F_{p^6}/\mathbb F_p\) controls.  For each line print

\[
 (J_L,M_L,x_L,(\delta_\eta),|Z_L|,\beta_L,
   \deg G_L,|(D\setminus W_L)\cap\Sigma)
\]

and the exact contribution \(\beta_L(J_L-20)\).  Add the eight outlier
directions needed for intrinsic rank nine and enforce the full witness,
noncontainment, regular-chart, carrier, and executable-owner conditions.

Stop at the first exact source-bound countertemplate.  If none survives,
freeze its determinant/GCD support equations before using elimination.
Do not start rank at least ten, \(U_Q\), \(U_A\), or Lean.
