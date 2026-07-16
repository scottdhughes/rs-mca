# M1 KoalaBear branch-3 actual-core MDS rank ladder v1

- **Status:** PROVED imported-theorem splice / exact finite route cut under
  the literal predecessor hypotheses; no unconditional ledger movement.
- **Scope:** the complete rank-minimizing actual-witness selector in the
  KoalaBear branch-3 TDD residual at `A = 1,116,048`.
- **Predecessor:**
  `experimental/notes/m1/m1_kb_branch3_tdd_excess_v1.md`.
- **Imported theorem:** the actual-core basis-multiplicity theorem (M1)--(M5)
  in
  `experimental/notes/thresholds/a6_actual_witness_core_rank_preflight.md`.
- **Companion verifiers:**
  `experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py` and
  `experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.sage`.

This packet does not reprove the multiplicity theorem.  It checks its exact
consumer interface after restricting to the complete basis carrier supplied
by the predecessor.  The result pays intrinsic selected-witness affine ranks
four through eight uniformly and gives an exact carrier-size/extension-factor
payment boundary at rank nine.  Rank nine is the first rank not paid uniformly,
not an entirely unpaid stratum.  Branch 3 and the KoalaBear row remain open.

## 1. Frozen predecessor state

The deployed row is

\[
n=2{,}097{,}152,\qquad k=1{,}048{,}576,\qquad
A=1{,}116{,}048,
\]

with

\[
R=n-k=1{,}048{,}576,\qquad
j=n-A=981{,}104,\qquad
\Delta_0=R-j=A-k=67{,}472.
\tag{1.1}
\]

The already-paid baseline and remaining finite-slope budget are

\[
U_{\rm paid}=2{,}602{,}502{,}999,
\qquad
B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\tag{1.2}
\]

Let \(\Gamma\) be the complete retained slope family after the frozen
first-match owners.  The predecessor defines the finite nonempty set of
complete actual-witness selectors, chooses a selector \(\sigma_*\) attaining
the minimum affine rank

\[
s_*(\Gamma)=
\min_\sigma
\dim\operatorname{span}
\{e^\sigma_\eta-e^\sigma_{\eta_0}:\eta\in\Gamma\},
\tag{1.3}
\]

and applies the global carrier owner existentially before choosing this rank
minimizer.  We work on its complementary route

\[
|\Gamma|>15,
\qquad
\kappa_*(\Gamma)\ge11.
\tag{1.4}
\]

Thus every complete selector, including \(\sigma_*\), has complete support
union of size at least \(R+11\).  Suppress \(\sigma_*\) from the notation.
The selected errors satisfy

\[
He_\eta=y_0+\eta y_1,\qquad
\operatorname{wt}(e_\eta)\le j,
\qquad y_1\ne0,
\tag{1.5}
\]

and the declared transverse-witness condition

\[
\{y_0,y_1\}\not\subset H(F^{E_\eta})
\tag{1.6}
\]

for every retained slope.

## 2. Complete basis carrier and restricted MDS code

The predecessor proves, for two anchors \(\alpha\ne\beta\),

\[
\mathcal D
=\operatorname{span}\{e_\eta-e_\alpha:\eta\in\Gamma\}
=\langle b\rangle\oplus\mathcal R,
\qquad
s_*=1+\dim\mathcal R,
\tag{2.1}
\]

where \(Hb=y_1\ne0\) and \(\mathcal R\) is the span of the fixed-anchor
residual codewords.  If
\(r_{\gamma_2},\ldots,r_{\gamma_s}\) is a residual basis, then

\[
V=E_\alpha\cup E_\beta\cup
\bigcup_{h=2}^{s}E_{\gamma_h}
=\bigcup_{\eta\in\Gamma}E_\eta.
\tag{2.2}
\]

This is an equality with the complete union of the one fixed rank-minimizing
selector, not a cover by unrelated triples.  Put

\[
N_V=|V|=R+\nu.
\tag{2.3}
\]

Equation (1.4) gives \(11\le\nu\le k\).  Restricting the Reed--Solomon
parity check to \(V\) gives an \(R\times(R+\nu)\) weighted Vandermonde
matrix.  Every \(R\) columns are independent, so

\[
K_V=\ker H_V
\quad\hbox{is}\quad
[R+\nu,\nu,R+1]_{F}\ \text{MDS}.
\tag{2.4}
\]

All selected errors are supported in \(V\), so restriction changes neither
their weights nor the affine span.  Moreover

\[
K_0=\mathcal D\cap K_V=\mathcal R,
\qquad
r:=\dim K_0=s_*-1.
\tag{2.5}
\]

The transverse condition (1.6) is unchanged: its support image uses exactly
the same columns before and after restricting the ambient coordinate set to
\(V\).

## 3. Exact import of the actual-core MDS theorem

Apply the actual-core basis-multiplicity theorem with the following literal
dictionary:

\[
\begin{array}{c|c}
\text{imported symbol}&\text{KoalaBear basis-carrier object}\\ \hline
N&N_V=R+\nu\\
\kappa&\nu\\
t&j\\
Z&\Gamma\\
D_Z&\mathcal D\\
K_0&\mathcal R\\
s&s_*\\
r&s_*-1.
\end{array}
\tag{3.1}
\]

For the complete zero mask
\(T_\eta=V\setminus E_\eta\),

\[
|T_\eta|
=N_V-|E_\eta|
\ge N_V-j
=\nu+\Delta_0.
\tag{3.2}
\]

To avoid collision with the predecessor's interpolating codeword \(q\), call
the imported theorem's uniform mask floor \(q_{\rm mask}\).  It may be chosen
as

\[
q_{\rm mask}=\nu+\Delta_0.
\tag{3.3}
\]

It satisfies \(q_{\rm mask}\ge\nu+1\).  If \(d_V\) is the minimum weight of
an \(H_Vz=y_1\) lift, write the theorem's extension factor as

\[
\ell_{\rm mask}
=\max\{1,d_V+q_{\rm mask}-N_V\}
=\max\{1,d_V-j\}
\ge1.
\tag{3.4}
\]

No unproved lower bound on \(d_V-j\) is used.  Taking only
\(\ell_{\rm mask}\ge1\), the per-slope multiplicity at rank \(s\) is at least

\[
\mu_s
=\left\lceil
\frac1s
\binom{q_{\rm mask}-\nu+(s-1)}{s-1}
\right\rceil
=\left\lceil
\frac1s
\binom{\Delta_0+s-1}{s-1}
\right\rceil.
\tag{3.5}
\]

The imported theorem therefore gives the exact uniform cap

\[
|\Gamma|
\le
\left\lfloor
\frac{\binom{N_V}{s}}{\mu_s}
\right\rfloor
\le
B_s:=
\left\lfloor
\frac{\binom n s}{\mu_s}
\right\rfloor.
\tag{3.6}
\]

The last inequality uses only \(N_V\le n\).  The cancellation in (3.5) is
why no enumeration over the possible carrier excess \(\nu\) is needed.

For the residual dichotomy we apply this to the rank minimizer.  Payment is
slightly more flexible: the same identities and basis-carrier proof apply
afresh to any one complete actual-witness selector.  Thus exhibiting any
complete selector satisfying a paid rank/cap condition pays the whole retained
family; rank-minimizing status is needed only before declaring the complementary
intrinsic residual.

## 4. Exact rank ladder

Python big-integer evaluation of (3.5)--(3.6) gives:

| \(s\) | residual rank \(r=s-1\) | basis supports | \(B_s\) | comparison with \(B_{\rm rem}\) |
|---:|---:|---:|---:|:---|
| 4 | 3 | 5 | 62,966,423,050 | fits |
| 5 | 4 | 6 | 1,956,990,754,759 | fits |
| 6 | 5 | 7 | 60,822,165,928,712 | fits |
| 7 | 6 | 8 | 1,890,289,605,334,110 | fits |
| 8 | 7 | 9 | 58,747,334,643,050,472 | fits |
| 9 | 8 | 10 | 1,825,750,153,566,470,657 | fails only at the uniform worst case |

At the first new rank,

\[
\mu_4
=\left\lceil\frac14\binom{67{,}475}{3}\right\rceil
=12{,}799{,}651{,}012{,}707,
\tag{4.1}
\]

and

\[
B_4
=\left\lfloor
\frac{\binom{2{,}097{,}152}{4}}{\mu_4}
\right\rfloor
=62{,}966{,}423{,}050.
\tag{4.2}
\]

The caps are increasing on the finite scanned range \(4\le s\le9\), so
the single worst conditional terminal for ranks four through eight is

\[
B_{4:8}=B_8=58{,}747{,}334{,}643{,}050{,}472
<B_{\rm rem}.
\tag{4.3}
\]

Equivalently,

\[
U_{\rm paid}+B_{4:8}
=58{,}747{,}337{,}245{,}553{,}471
<274{,}980{,}728{,}111{,}395{,}087=B_*.
\tag{4.4}
\]

The exact margin in (4.4) is

\[
216{,}233{,}390{,}865{,}841{,}616.
\tag{4.5}
\]

This is one global terminal for the complete retained slope family.  The
five rank caps are alternatives indexed by the one intrinsic rank \(s_*\);
they are not summed, and no cap is charged once per triple, basis, or
subfamily.

### Coarse-uniform rank-nine boundary

At rank nine, retain the actual carrier size \(N_V\) and extension factor
\(\ell_{\rm mask}\) instead of replacing them by \(n\) and one.

The rank, carrier size, source minimum-lift weight, and extension factor must
all be certified for the same complete selector and the same restricted map
\(H_V\).  Mixing any of these data across selectors is invalid.

Put

\[
D_9=\binom{67{,}480}{8},
\qquad
\mu_9(\ell)=\left\lceil\frac{\ell D_9}{9}\right\rceil.
\tag{4.6}
\]

Then the actual selector is paid whenever

\[
\left\lfloor
\frac{\binom{N_V}{9}}{\mu_9(\ell_{\rm mask})}
\right\rfloor
\le B_{\rm rem}.
\tag{4.7}
\]

For the coarse uniform choice \(q_{\rm mask}=N_V-j\), the exact largest paid
carrier sizes for the only potentially failing extension factors are:

| \(\ell_{\rm mask}\) | largest paid \(N_V\) |
|---:|---:|
| 1 | 1,699,344 |
| 2 | 1,835,392 |
| 3 | 1,919,971 |
| 4 | 1,982,333 |
| 5 | 2,032,097 |
| 6 | 2,073,683 |

For \(\ell_{\rm mask}\ge7\), every \(N_V\le n\) is paid.  Consequently the exact
failure region of this coarse uniform corollary is

\[
1\le\ell_{\rm mask}\le6,
\qquad
N_V>N_{\max}(\ell_{\rm mask}),
\tag{4.8}
\]

not on all rank-nine selectors.  This is not the full residual of the imported
theorem: larger actual zero masks may permit a stronger uniform \(q\), and
the nonuniform sum (M2b) may pay points inside (4.8).  No lower bound
\(\ell_{\rm mask}\ge7\) and no upper bound \(N_V\le1{,}699{,}344\) is asserted for
the deployed residual.

## 5. Updated fail-closed owner order

For the complete retained family, apply:

1. a named already-paid quotient, periodic, Johnson, or common-support owner;
2. one certified global carrier with intrinsic excess at most ten;
3. the predecessor complete-selector affine-core terminal \(s_*\le3\);
4. the uniform actual-core MDS multiplicity terminal \(4\le s_*\le8\);
5. the exact rank-nine actual-core MDS terminal (4.7);
6. a future deduplicated TDD-root-union terminal only after a canonical
   injection or bounded multiplicity theorem is proved;
7. otherwise emit either
   `UNPAID_BY_COARSE_UNIFORM_RANK9_MDS_JOINT_BOUND` or
   `UNPAID_PRIMITIVE_INTRINSIC_RANK_AT_LEAST_10_TDD_SPREAD`.

The first rank not paid uniformly is now

```text
INTRINSIC_GLOBAL_CARRIER_EXCESS kappa_* AT_LEAST_11
AND INTRINSIC_ACTUAL_AFFINE_RANK s_* EXACTLY_9
AND ITS_TDD_DEFECT_SPAN_RANK EXACTLY_8
AND TEN_ACTUAL_SUPPORTS_RECOVER_THAT_SELECTOR'S_COMPLETE_UNION.
```

Within that rank, (4.7) pays every point outside the coarse joint failure
region (4.8).  Before inventing new structure inside (4.8), one must retain
the actual mask sizes and try the imported nonuniform sum (M2b).  Any remaining
payment needs additional information, for example a stronger source-distance
bound, a named structured owner, or another proved multiplicity gain.  This
packet does not assert such information.

## 6. Ledger semantics and nonclaims

This packet changes the conditional owner partition but does not add an
unconditional charge to the shared ledger.  The baseline values in (1.2)
therefore remain unchanged while the coarse rank-nine failure region and ranks
at least ten are open.  For any received pair whose complete rank-minimizing selector
has \(s_*\le8\), the applicable conditional cap plus the paid baseline fits
\(B_*\).  Rank-nine selectors are also paid outside (4.8); the remaining
pairs are unresolved by this coarse corollary or lie at intrinsic rank at
least ten.

In particular, the packet does **not**:

- prove branch 3 or the KoalaBear row safe;
- determine the deployed intrinsic rank without a complete-selector
  certificate;
- add the rank caps together or charge them per subfamily;
- infer \(d_V-j\ge1\), or any extension factor larger than one;
- pay the entire intrinsic rank-nine stratum;
- prove a canonical TDD-union injection;
- determine \(U_2\), \(U_Q\), or \(U_A\);
- begin a degree-three parameter class, higher-\(m\) analysis, Lean
  formalization, or Paper-D promotion.

## 7. Audit verdict

- **Dependencies:** the basis-carrier equality, rank identity, complete
  selector, transversality, and weight budget are proved by the predecessor;
  the MDS multiplicity inequality is imported from the named local theorem.
- **Parameter dependence:** the splice is field-general until the exact
  KoalaBear values \(n,R,j,\Delta_0,B_{\rm rem}\) are substituted.  No
  asymptotic estimate is used.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** exact Python big integers and a tiny Sage MDS control
  only.  The Sage control is not a deployed-field census and is not used as a
  proof of the theorem.
- **Verdict:** GREEN for the imported-theorem splice, the exact ranks
  four-through-eight terminal, and the rank-nine joint cut; YELLOW for branch
  3 and the KoalaBear row.

The minimal next action after independent review is to bank this updated
owner partition and first run the nonuniform (M2b) payment inside (4.8),
retaining every actual mask size together with \(N_V\) and
\(\ell_{\rm mask}\).
TheoremSearch, Singular, Macaulay2, and Lean are not useful before a residual
rank-nine compatibility statement is frozen after that exact payment.
