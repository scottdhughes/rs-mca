# M1 KoalaBear branch-3 rank-nine sparse chart-boundary route cut v1

- **Status:** PROVED local specialization / conditional first-match caps /
  regular split-locator route remains OPEN / no ledger movement.
- **Scope:** the non-column-far terminal
  `CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA` exported by
  `m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md` for one fixed
  rank-minimizing complete affine-rank-nine selector.
- **Generic source:**
  `experimental/notes/thresholds/cap25_v12_fixed_residual_excess_audit.md`,
  specialized here to the KoalaBear row and wired into the branch-3
  first-match contract.
- **Companion verifiers:**
  `experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py`
  and
  `experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.sage`.

This packet does not prove a new generic sparse-sigma theorem.  It extracts two
rigorous, disjoint subcells from the sparse route already reached by the
rank-nine packet:

\[
  \text{tangent slopes}\le j=981{,}104,
  \qquad
  \text{chosen-minor chart-boundary slopes}\le R-j=67{,}472.
\]

Their conditional union cap is

\[
  j+(R-j)=R=1{,}048{,}576.
\tag{0.1}
\]

The remaining object is a regular, full-row-rank, positive-residual
split-locator incidence.  It is a route to later owner masks, not a final
primitive classification.

## 1. Frozen predecessor state

The deployed row is

\[
 n=2{,}097{,}152,
 \qquad k=1{,}048{,}576,
 \qquad A=1{,}116{,}048.
\tag{1.1}
\]

Put

\[
 R=n-k=1{,}048{,}576,
 \qquad j=n-A=981{,}104,
 \qquad a:=R-j=67{,}472.
\tag{1.2}
\]

The predecessor proves a deterministic dichotomy on the one fixed complete
affine-rank-nine selector.  Its column-far terminal is paid by the
syndrome-rank cap.  Its complementary terminal is exactly

```text
CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA
```

and moves no ledger value.  Write \((f,g)\) for the predecessor's original
received pair and \(c_\eta\) for the selected explaining codeword at a retained
slope \(\eta\).  On the complementary branch, challenge-restricted exact
sparsification (SP3) chooses a common explaining codeword pair \((c_0,c_1)\),
translates the original pair, and preserves its exact MCA-bad slope set and
witness supports.  Hence we may fix the sparse pair

\[
 (\epsilon_1,\epsilon_2),
 \qquad
 E=\operatorname{supp}(\epsilon_1)\cup
   \operatorname{supp}(\epsilon_2),
 \qquad e=|E|\le j.
\tag{1.3}
\]

This packet partitions that sparse bad set locally, before intersection with
the global owner order.  Any globally earlier owner---including the existing
tangent branch---must be removed before aggregation.  Thus the local tangent
cell below is not a second global tangent owner, and this packet does not
silently absorb quotient, periodic, planted, extension, or base-field cells.

The rank-nine selector remains the same object after translation.  For every
retained slope \(\eta\), define

\[
 \widetilde c_\eta=c_\eta-c_0-\eta c_1\in C.
\]

Then the translated selected error is literally

\[
 \epsilon_1+\eta\epsilon_2-\widetilde c_\eta
 =f+\eta g-c_\eta=e_\eta.
\tag{1.4}
\]

Thus the retained slopes, actual error supports, affine-difference rank nine,
and witness-column rank ten are unchanged; they are not merely transferred by
an unproved rank-preservation assertion.

## 2. Exact closed-ball Pad\'e--Hankel form

For this Reed--Solomon row the redundancy is \(m=R\) and the closed-ball
radius is \(r=j\).  If \(s_i=\operatorname{Syn}(\epsilon_i)\), put

\[
 H_i=H_j(s_i),
 \qquad
 M(\gamma)=H_1+\gamma H_2.
\tag{2.1}
\]

The matrix dimensions and residual excess are

\[
 M(\gamma)\in
 F^{(R-j)\times(j+1)}=F^{67{,}472\times981{,}105},
\tag{2.2}
\]

\[
 h=2j-R-1=913{,}631,
 \qquad
 \dim\ker M(\gamma)=j+1-(R-j)=913{,}633=h+2
\tag{2.3}
\]

whenever \(M(\gamma)\) has full row rank.

The exact closed-ball formulation says that a finite slope \(\gamma\) is
sparse MCA-bad if and only if some \(T\subseteq D\), \(|T|=j\), has split
squarefree locator

\[
 L_T(X)=\prod_{x\in T}(X-x),
 \qquad \ell_T=\operatorname{coeff}(L_T),
\]

with

\[
 M(\gamma)\ell_T=0,
 \qquad H_2\ell_T\ne0.
\tag{2.4}
\]

The second condition is the same-support noncontainment gate.  Dropping it
would count common extensions that do not witness MCA failure.

## 3. Tangent first-match cell

Call \(\gamma\) tangent if

\[
 \epsilon_1(x)+\gamma\epsilon_2(x)=0
 \quad\text{for some }x\in E.
\tag{3.1}
\]

Each coordinate with \(\epsilon_2(x)\ne0\) determines at most one finite
slope, while a coordinate with \(\epsilon_2(x)=0\) determines none.  Therefore

\[
 \#\{\text{tangent slopes}\}\le e\le j=981{,}104.
\tag{3.2}
\]

The packet assigns tangent bad slopes first to

```text
SPARSE_TANGENT_RANK9_CONDITIONAL_CAP
```

so every later sparse subcell explicitly excludes them.

## 4. Non-tangent full row rank

Fix a non-tangent slope and put

\[
 v_\gamma=\epsilon_1+\gamma\epsilon_2.
\]

Then \(v_\gamma\) is nonzero exactly on \(E\).  The Reed--Solomon moment
factorization gives

\[
 M(\gamma)
 =U_E\,\operatorname{diag}(\lambda_xv_\gamma(x))_{x\in E}\,V_E^t,
\tag{4.1}
\]

where \(U_E\) uses powers \(0,\ldots,R-j-1\), and \(V_E\) uses powers
\(0,\ldots,j\).  Since the domain points are distinct and \(e\le j\), the
right Vandermonde factor has row rank \(e\).  Hence

\[
 \operatorname{rank}M(\gamma)=\min(e,R-j).
\tag{4.2}
\]

If \(e\le R-j\), the proved sparse-threshold theorem leaves no non-tangent
MCA-bad slope.  Consequently every non-tangent bad slope satisfies

\[
 e\ge R-j+1=67{,}473
\]

and therefore

\[
 \operatorname{rank}M(\gamma)=R-j=67{,}472.
\tag{4.3}
\]

This is full row rank, not a rank-drop stratum.

## 5. One chosen-minor chart boundary

If there is no non-tangent bad slope, the tangent cell already exhausts the
sparse bad set.  Otherwise choose one non-tangent bad slope \(\gamma_0\).
By (4.3), some \((R-j)\times(R-j)\) column minor of
\(M(\gamma_0)\) is nonzero.  Freeze one such minor and write its determinant as

\[
 \Delta(\gamma).
\tag{5.1}
\]

Every entry of \(M(\gamma)\) is affine in \(\gamma\), so

\[
 \Delta\not\equiv0,
 \qquad
 \deg\Delta\le R-j=67{,}472.
\tag{5.2}
\]

Thus the non-tangent slopes on this chart boundary satisfy

\[
 \#\{\gamma:\Delta(\gamma)=0\}\le67{,}472.
\tag{5.3}
\]

They are assigned, after subtracting the tangent cell, to

```text
SPARSE_CHART_BOUNDARY_RANK9_CONDITIONAL_CAP
```

The wording is load-bearing: \(\Delta(\gamma)=0\) says that the selected
coordinate chart degenerates.  Another maximal minor can remain nonzero, and
indeed (4.3) says the full matrix still has rank \(R-j\) at every non-tangent
bad slope.  This cell must not be called a global rank-drop owner.

Combining the two disjoint first-match subcells proves the conditional cap

\[
 981{,}104+67{,}472=1{,}048{,}576=R.
\tag{5.4}
\]

## 6. Exact residual

After the two subcells, every surviving slope lies on the regular chosen
chart and has a split-locator witness satisfying

\[
 \boxed{
 \Delta(\gamma)\ne0,
 \quad M(\gamma)\ell_T=0,
 \quad H_2\ell_T\ne0,
 \quad |T|=j,
 \quad L_T\text{ squarefree and }D\text{-split}.}
\tag{6.1}
\]

The selector also retains the predecessor's intrinsic affine-difference rank
nine and witness-column rank ten.  No proved implication currently converts
those witness ranks into a low-dimensional locator family.  The fail-closed
terminal is therefore

```text
REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE
```

and not `UNPAID_PRIMITIVE`: later quotient/periodic/Johnson/B11 or other
declared masks must still be tested wherever their executable hypotheses are
available.

## 7. Classifier and ledger semantics

On certified inputs use exactly:

```text
if original pair is column-far at agreement A:
    NON_CA_RANK9_SYNDROME_REDUCTION_PAID       # predecessor terminal
else:
    require SP3 translation and sparse support union <= j
    require an actual MCA-bad witness with H_2 ell_T != 0
    if gamma is tangent:
        SPARSE_TANGENT_RANK9_CONDITIONAL_CAP
    else:
        require full row rank and one chosen nonzero minor at gamma_0
        if Delta(gamma) == 0:
            SPARSE_CHART_BOUNDARY_RANK9_CONDITIONAL_CAP
        else:
            REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE
```

The cap (5.4) belongs to this local ordered partition of the predecessor's
sparse branch.  Global owner intersections must still be applied before any
ledger aggregation.  This packet does not prove the aggregation needed to add
\(R\) to the shared upper ledger.  Therefore

\[
 U_{\rm paid}^{\rm before}=U_{\rm paid}^{\rm after}
 =2{,}602{,}502{,}999,
\]

\[
 B_{\rm rem}^{\rm before}=B_{\rm rem}^{\rm after}
 =274{,}980{,}725{,}508{,}892{,}088.
\tag{7.1}
\]

## 8. Audit status and nonclaims

- **Dependency status:** SP3, the exact Pad\'e--Hankel formulation, the
  non-tangent rank factorization, and the generic chosen-minor bound are proved
  in the cited local sources.  The global first-match aggregation and the
  regular split-locator incidence bound remain unproved.
- **Parameter dependence:** (3.2)--(5.4) are exact finite-row integers.  The
  underlying local argument is field-uniform for distinct Reed--Solomon
  evaluation points.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** the Python certificate checks exact deployed
  arithmetic.  The Sage companion is a toy-scale control showing tangent,
  chart-boundary, and regular examples; it is not a deployed-field census.
- **Global verdict:** YELLOW.  Rank nine, branch 3, sparse sigma, and the
  KoalaBear row remain open.
- **Local verdict:** GREEN for the conditional two-subcell route cut.

In particular, this packet does not:

- prove a new generic sparse-sigma theorem;
- call a chosen-minor root a global rank drop;
- drop the noncontainment gate \(H_2\ell_T\ne0\);
- call the regular residual final primitive;
- pay all later owner masks;
- move \(U_{\rm paid}\) or \(B_{\rm rem}\);
- close rank nine, branch 3, or the KoalaBear row;
- attack intrinsic rank at least ten;
- authorize Lean or promotion into a stable paper.

## 9. Minimal next action

First falsify, in exact small Reed--Solomon models, any proposed implication
from affine witness rank nine / witness-column rank ten to bounded locator-span
dimension on (6.1).  If the implication survives, state the smallest exact
rank-to-locator bridge and test it before symbolic elimination.  If it fails,
bank the counterexample as a route cut proving that the present #874
hypotheses alone cannot pay the regular chart.
