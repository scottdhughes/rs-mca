# M1 KoalaBear branch-3 rank-nine syndrome rank reduction v1

- **Status:** PROVED deterministic rank-nine CA route cut; no unconditional
  ledger movement.
- **Scope:** the intrinsic affine-rank-nine complete-selector residual left by
  `m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md`.
- **Predecessors:**
  `m1_kb_branch3_actual_core_mds_rank_ladder_v1.md` and
  `m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md`.
- **External provenance:** the rank-reduction idea is independently
  reconstructed from Chen Yuan and Ruiqi Zhu,
  [*A Syndrome--Space Approach to Proximity Gaps and Correlated Agreement for
  Random Linear Codes and Random Reed--Solomon Codes*, arXiv:2605.07595v2](https://arxiv.org/abs/2605.07595),
  specifically Theorem 3.5 and Corollary 3.6 for witness-rank reduction, and
  Lemmas 4.2--4.3, Lemma 4.5, Corollary 4.6, and Theorem 4.7 for the
  correlated-agreement terminal.  Their deterministic mechanism is specialized
  to \(m=1\), \(h=2\), and \(E^+=E\), and re-proved below; no random-code
  theorem is imported here.
- **Companion verifiers:**
  `experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py`
  and
  `experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.sage`.

This packet replaces the broad missing mask-deficit incidence lemma by an exact
two-way route cut.  On the one fixed rank-minimizing complete selector:

1. if the received pair is column-far, deterministic witness-rank reduction
   bounds the retained slopes by
   \(3{,}337{,}935{,}545{,}766{,}696<B_{\rm rem}\);
2. if the pair is not column-far, the challenge-restricted exact
   sparsification theorem routes the same MCA-bad slopes to the already-named
   sparse mutual numerator.

The second branch remains unpaid.  Thus this is a rigorous route cut out of the
rank-nine M2b histogram lane, not branch-3 or KoalaBear-row closure.

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
\qquad d=R+1=1{,}048{,}577.
\tag{1.2}
\]

The predecessor fixes one rank-minimizing complete selector indexed by the
retained finite slope family \(\Gamma\), with

\[
|\Gamma|>15,
\qquad
e_\eta=f+\eta g-c_\eta,
\qquad c_\eta\in C,
\qquad
H_Ve_\eta=y_0+\eta y_1,
\qquad
\operatorname{wt}(e_\eta)\le j,
\tag{1.3}
\]

and actual supports \(E_\eta=\operatorname{supp}(e_\eta)\).  The same selector
has the transverse-witness condition

\[
\{y_0,y_1\}\not\subset H_V(F^{E_\eta})
\qquad(\eta\in\Gamma),
\tag{1.4}
\]

and intrinsic affine-difference space

\[
\mathcal D
=\operatorname{span}\{e_\eta-e_{\eta_0}:\eta\in\Gamma\},
\qquad
\dim\mathcal D=s=9.
\tag{1.5}
\]

Its complete basis carrier \(V\) satisfies

\[
K_V=\ker H_V=[R+\nu,\nu,R+1]_F,
\tag{1.6}
\]

so every nonzero word of \(K_V\) has weight at least \(d=R+1\).
All ranks, supports, syndromes, and witnesses below belong to this one selector
and this one restricted map \(H_V\).  Here \(H_V\) is the original RS
parity-check map restricted to the carrier columns.  Since every \(e_\eta\) is
supported on \(V\), zero extension identifies its restricted and original
syndromes, and

\[
y_0=Hf,
\qquad y_1=Hg.
\tag{1.7}
\]

The frozen arithmetic is

\[
U_{\rm paid}=2{,}602{,}502{,}999,
\qquad
B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\tag{1.8}
\]

## 2. The syndrome line is nondegenerate

First, \(y_1\ne0\): this is part of the predecessor rank decomposition.
Suppose for contradiction that \(y_0=\beta y_1\).  Since
\(|\Gamma|>15\), choose \(\eta\in\Gamma\) with \(\eta\ne-\beta\).  Then

\[
H_Ve_\eta=(\beta+\eta)y_1\ne0.
\]

Because \(e_\eta\) is supported on \(E_\eta\), this puts \(y_1\) in
\(H_V(F^{E_\eta})\), and hence also puts \(y_0=\beta y_1\) there.  This
contradicts (1.4).  Therefore

\[
\dim\operatorname{span}\{y_0,y_1\}=2.
\tag{2.1}
\]

This bridge is load-bearing.  Merely knowing \(y_1\ne0\) would not justify the
rank exponent below.

## 3. Affine rank nine means witness-column rank ten

Every difference has syndrome in \(\langle y_1\rangle\), and the difference
of two distinct slopes has nonzero syndrome.  Thus

\[
H_V(\mathcal D)=\langle y_1\rangle.
\tag{3.1}
\]

On the other hand,

\[
H_Ve_{\eta_0}=y_0+\eta_0y_1\notin\langle y_1\rangle
\]

by (2.1), so \(e_{\eta_0}\notin\mathcal D\).  Since every selected error is
the anchor plus an element of \(\mathcal D\), the witness matrix

\[
X=[e_\eta]_{\eta\in\Gamma}
\]

has exact column rank

\[
t=\dim\operatorname{span}\{e_\eta:\eta\in\Gamma\}
=1+\dim\mathcal D=10.
\tag{3.2}
\]

Using \(t=9\) here would confuse affine-difference rank with raw
witness-column rank.

## 4. Specialized deterministic rank reduction

We prove the exact local lemma needed by this packet.

### Lemma 4.1 (one rank-reduction step)

Let \(C=\ker H\subseteq F^N\) have minimum distance at least \(d\), and let
\(0<E<d\).  Suppose distinct scalars \(\eta_1,\ldots,\eta_K\) and columns
\(x_i\in F^N\) satisfy

\[
Hx_i=s_0+\eta_i s_1,
\qquad \operatorname{wt}(x_i)\le E,
\qquad \dim\langle s_0,s_1\rangle=2.
\tag{4.1}
\]

If \(X=[x_1|\cdots|x_K]\) has rank \(t\ge3\), then a submatrix covering at
least

\[
K\gamma,
\qquad \gamma=\frac{d-E}{d},
\tag{4.2}
\]

of the same distinct slopes has rank at most \(t-1\).

#### Proof

Let \(u=(1,\ldots,1)\) and \(v=(\eta_1,\ldots,\eta_K)\).  The syndrome
matrix has row space \(\langle u,v\rangle\), which lies in the row space of
\(X\).  Extend \(u,v\) to a row-space basis
\(u,v,w_3,\ldots,w_t\) and write

\[
X=a u^T+b v^T+\sum_{h=3}^t c_h w_h^T.
\tag{4.3}
\]

Applying \(H\) and comparing the independent row-space basis gives

\[
Ha=s_0,
\qquad Hb=s_1,
\qquad Hc_h=0\quad(3\le h\le t).
\tag{4.4}
\]

The coefficient map in (4.3) must have rank \(t\), because the row-space
coordinate matrix has row rank \(t\) and \(X\) has rank \(t\).  In particular
\(c_t\ne0\).  Hence \(c_t\in C\setminus\{0\}\), so
\(|\operatorname{supp}(c_t)|\ge d\).  Every column \(x_i\) has at least
\(|\operatorname{supp}(c_t)|-E\) zero coordinates on this support.  Double
counting selects a coordinate where at least

\[
K\frac{|\operatorname{supp}(c_t)|-E}
       {|\operatorname{supp}(c_t)|}
\ge K\frac{d-E}{d}=K\gamma
\]

columns vanish.  On those columns, solve the selected coordinate of (4.3) for
the coefficient of \(c_t\), substitute it back, and eliminate the direction
\(w_t\).  The surviving columns keep their original weights, slopes, and
syndromes, while their rank is at most \(t-1\).  ∎

### Lemma 4.2 (rank-two terminal or common support)

Under Lemma 4.1, suppose the original witness matrix has rank \(t\ge2\).  If
\(K\gamma^{t-2}>1\), then at least \(K\gamma^{t-2}\) witnesses lie on one
affine word line

\[
a+\eta b,
\qquad Ha=s_0,
\qquad Hb=s_1.
\tag{4.5}
\]
after at most \(t-2\) rank reductions.  If no pair of lifts \(a',b'\) with
\(Ha'=s_0\), \(Hb'=s_1\) has

\[
|\operatorname{supp}(a')\cup\operatorname{supp}(b')|\le E,
\tag{4.6}
\]

then

\[
K\gamma^{t-2}\le E+1.
\tag{4.7}
\]

#### Proof

If \(K\gamma^{t-2}\le1\), then (4.7) is immediate.  Otherwise every
intermediate retained set needed before the rank-two terminal contains at
least two distinct slopes.  Apply Lemma 4.1 until the rank reaches two (or
drops there early); since \(0<\gamma<1\), the retained size is still at least
\(K\gamma^{t-2}\).  The two independent syndrome rows then force the word
columns to have the affine form (4.5).  Put

\[
W=\operatorname{supp}(a)\cup\operatorname{supp}(b),
\qquad M=|W|.
\]

The no-common-support hypothesis (4.6) gives \(M\ge E+1\).  At each coordinate
of \(W\), the nonzero affine function \(a(x)+\eta b(x)\) vanishes for at most
one slope.  If \(J\) surviving distinct slopes all have weight at most \(E\),
then each contributes at least \(M-E\) zeros on \(W\).  Hence

\[
|J|(M-E)\le M,
\qquad
|J|\le\frac{M}{M-E}\le E+1.
\tag{4.8}
\]

Together with \(|J|\ge K\gamma^{t-2}\), this proves (4.7).  ∎

The proof is deterministic and applies to every linear code with the displayed
minimum distance.  Random-code and asymptotic results from the source paper are
not used.

## 5. Exact KoalaBear payment

Apply Lemma 4.2 to \(C=K_V\), \(E=j\), \(d=R+1\), and \(t=10\).  Then

\[
\gamma
=\frac{d-j}{d}
=\frac{67{,}473}{1{,}048{,}577},
\qquad t-2=8.
\tag{5.1}
\]

On the column-far branch, (4.7) gives

\[
|\Gamma|
\le
\left\lfloor
(j+1)\left(\frac{d}{d-j}\right)^8
\right\rfloor
=3{,}337{,}935{,}545{,}766{,}696.
\tag{5.2}
\]

The exact remaining-budget margin is

\[
B_{\rm rem}
-3{,}337{,}935{,}545{,}766{,}696
=271{,}642{,}789{,}963{,}125{,}392>0.
\tag{5.3}
\]

This bound is independent of the carrier size \(N_V\), the source minimum-lift
weight \(d_V\), and the deficit histogram.  It therefore pays every column-far
rank-nine selector throughout the coarse M2b failure region.  Non-column-far
points in that region take the separate sparse-sigma route below.

## 6. Exact sparsification route for the complementary branch

Classify the original received pair \((f,g)\) before applying the
restricted-selector lemma.  If it is not column-far at agreement \(A\), there
are original-code words \(c_0,c_1\) and a support \(S\subseteq D\),
\(|S|\ge A\), on which \(c_0=f\) and \(c_1=g\).  Put

\[
x_0=f-c_0,
\qquad x_1=g-c_1.
\]

Then

\[
|\operatorname{supp}(x_0)\cup\operatorname{supp}(x_1)|
\le n-|S|\le n-A=j.
\tag{6.1}
\]

The challenge-restricted exact sparsification theorem
`experimental/rs_mca_thresholds.tex`, equation (SP3), says that translation by
\((c_0,c_1)\) preserves the exact MCA-bad slope set and its witness supports.
Consequently this branch routes to

```text
CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA
```

and not to a zero-cost owner.

If instead the original pair is column-far, then in particular there cannot be
lifts of \(y_0,y_1\) supported on a common subset of \(V\) of size at most
\(j\): zero extension would produce original-code words explaining the pair on
at least \(A\) coordinates.  Thus the no-common-support hypothesis of Lemma
4.2 holds on the restricted selector, and Section 5 pays that branch.

This distinction is essential: the existence of one common explaining support
does not erase slope-dependent noncontained supports.  The sparse mutual
numerator at this row remains open.

## 7. False shortcut guardrail

The weaker assertion that every syndrome on the affine line has some
weight-\(j\) lift does **not** imply (6.1).  A finite exact guardrail already
occurs for the \([5,2,4]_{\mathbb F_7}\) MDS code with parity-check columns

\[
h_x=(1,x,x^2)^T,
\qquad x\in\{0,1,2,3,4\}.
\]

For \(E=2\), every point \((0,1,\alpha)^T\), \(\alpha\in\mathbb F_7\), is a
linear combination of the two columns \(h_i,h_j\) for some distinct
\(i,j\in\{0,1,2,3,4\}\) with \(i+j=\alpha\).  Hence the whole syndrome line
lies in the radius-two syndrome ball.  But the first-coordinate-zero part of
each two-column span is one-dimensional, generated by
\((0,1,i+j)^T\), so no support of size at most two contains lifts of both
\((0,1,0)^T\) and \((0,0,1)^T\).

The Sage companion exhausts this example.  It prevents the proximity-line
alternative from being silently substituted for the correlated-agreement
dichotomy used in Section 6.

## 8. Fail-closed classifier and ledger semantics

For the one fixed complete rank-nine selector, after all predecessor owners,
use exactly:

```text
if the original pair is not column-far at agreement A:
    CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA
else:
    NON_CA_RANK9_SYNDROME_REDUCTION_PAID
```

The second terminal has the cap (5.2).  The first terminal changes lanes but
remains unpaid.  Therefore

\[
U_{\rm paid}=2{,}602{,}502{,}999,
\qquad
B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088
\]

remain unchanged.  No raw cap from the two alternatives is added to another
conditional cap.

## 9. Audit status and nonclaims

- **Proof status:** GREEN for nondegeneracy, witness-rank typing, the
  specialized deterministic rank-reduction lemma, exact arithmetic, and the
  route to challenge-restricted sparse sigma.
- **Global status:** YELLOW.  Sparse sigma, intrinsic ranks at least ten,
  \(U_Q\), \(U_A\), branch 3, and the KoalaBear row remain open.
- **Parameter dependence:** the local lemma is field-uniform and deterministic;
  the printed exponent, cap, and budget comparison are KoalaBear-specific.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** the deployed comparison is exact integer arithmetic;
  the Sage examples are controls, not asymptotic evidence.

In particular, this packet does **not**:

- claim that a full low-weight syndrome line has one common support;
- call correlated agreement a paid or zero-cost MCA owner;
- pay the sparse mutual numerator;
- add a new unconditional ledger charge;
- assert that every rank-nine selector is unrealizable;
- attack intrinsic rank at least ten;
- prove branch 3 or the KoalaBear row safe;
- determine \(U_Q\) or \(U_A\);
- edit or promote any stable paper theorem;
- authorize Lean formalization before the local packet is independently
  reviewed.

## 10. Minimal next action

After independent review and predecessor replay, bank this as a route cut and
move the research lane to the first-match sparse mutual numerator.  Do not
resume generic M2b histogram optimization: the only rank-nine alternative not
paid by (5.2) has already been translated to the sparse-support problem.
