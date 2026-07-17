# M1 KoalaBear branch-3 rank-nine mask-deficit route cut v1

- **Status:** PROVED current-scalar-interface route cut and exact conditional
  compiler; no unconditional ledger movement.
- **Scope:** the intrinsic selected-witness affine-rank-nine residual left by
  `m1_kb_branch3_actual_core_mds_rank_ladder_v1.md`.
- **Predecessors:**
  `experimental/notes/m1/m1_kb_branch3_tdd_excess_v1.md` and
  `experimental/notes/m1/m1_kb_branch3_actual_core_mds_rank_ladder_v1.md`.
- **Imported theorem:** the selected-witness set-pair inequality (P2) and
  actual-core MDS inequality (M2b) in
  `experimental/notes/thresholds/a6_actual_witness_core_rank_preflight.md`.
- **Companion verifiers:**
  `experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py` and
  `experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.sage`.

This packet answers one precise question: can the nonuniform inequality M2b,
using only the quantitative information already exported by the predecessors,
improve the coarse rank-nine cap?  The answer is no.  The all-zero deficit
histogram remains feasible in the scalar relaxation and reproduces the coarse
cap exactly.  This is a route cut for the current scalar interface, not a constructed
Reed--Solomon family.

The packet also proves the exact integer compiler for any future cumulative
deficit-tail lemma.  It records the sharp one-cut threshold, a generic
multi-cut extension, and the weakest right side at each fixed cutoff.  No such
incidence lemma is proved here, so the shared ledger does not move.

## 1. Frozen rank-nine state

The deployed row is

\[
n=2{,}097{,}152,
\quad k=1{,}048{,}576,
\quad A=1{,}116{,}048,
\]

with

\[
R=n-k=1{,}048{,}576,
\quad j=n-A=981{,}104,
\quad \Delta_0=R-j=67{,}472.
\tag{1.1}
\]

After the deep-owner deletion, every selected error has weight at least

\[
L=349{,}526.
\tag{1.2}
\]

The rank-ladder predecessor leaves the intrinsic rank-nine route

\[
s=9,
\qquad r=s-1=8,
\tag{1.3}
\]

for one fixed rank-minimizing complete selector.  Its basis carrier is the
complete support union

\[
V=\bigcup_{\eta\in\Gamma}E_\eta,
\qquad N_V=|V|=R+\nu,
\qquad 11\le\nu\le k,
\tag{1.4}
\]

and ten actual supports recover this union.  The restricted parity check has
kernel

\[
K_V=[R+\nu,\nu,R+1]_F
\tag{1.5}
\]

and source minimum-lift weight

\[
d_V=\min\{\operatorname{wt}(z):H_Vz=y_1\},
\qquad 1\le d_V\le R.
\tag{1.6}
\]

The already-paid baseline and remaining budget are

\[
U_{\rm paid}=2{,}602{,}502{,}999,
\qquad
B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\tag{1.7}
\]

Rank, carrier, source distance, and all masks below refer to this same
selector and restricted map.  Mixing them across selectors is invalid.

## 2. Exact deficit specialization of M2b

Define the error-weight deficit

\[
\delta_\eta=j-|E_\eta|.
\tag{2.1}
\]

Equations (1.2) and the witness weight cap give

\[
0\le\delta_\eta\le j-L=631{,}578=: \Delta_{\max}.
\tag{2.2}
\]

The actual zero mask inside the carrier is

\[
T_\eta=V\setminus E_\eta,
\qquad
a_\eta:=|T_\eta|
=N_V-j+\delta_\eta
=\nu+\Delta_0+\delta_\eta.
\tag{2.3}
\]

In the imported theorem, \(\kappa=\nu\) and \(r=8\).  Therefore

\[
a_\eta-\kappa+r
=\Delta_0+8+\delta_\eta
=67{,}480+\delta_\eta,
\tag{2.4}
\]

while the matched extension factor is

\[
\ell_\eta
=\max\{1,d_V+a_\eta-N_V\}
=\max\{1,d_V-j+\delta_\eta\}.
\tag{2.5}
\]

Thus the exact local multiplicity is

\[
\boxed{
\mu_{d_V}(\delta)
=
\left\lceil
\frac{\max\{1,d_V-j+\delta\}}9
\binom{67{,}480+\delta}{8}
\right\rceil .
}
\tag{2.6}
\]

Writing

\[
h_\delta
=\#\{\eta\in\Gamma:\delta_\eta=\delta\},
\tag{2.7}
\]

M2b becomes

\[
\boxed{
\sum_{\delta=0}^{\Delta_{\max}}
h_\delta\mu_{d_V}(\delta)
\le\binom{N_V}{9}.
}
\tag{2.8}
\]

The weights in (2.6) are strictly increasing in \(\delta\).  Indeed,

\[
\binom{67{,}481+\delta}{8}
-\binom{67{,}480+\delta}{8}
=\binom{67{,}480+\delta}{7}>9,
\tag{2.9}
\]

and the extension factor is nondecreasing.  The ceiling in (2.6) therefore
does not destroy strictness.

The exact value of \(d_V\) matters after \(\delta=0\).  In particular,
\(d_V=1\) and \(d_V=j+1\) both have the same coarse factor
\(\max(1,d_V-j)=1\), but give very different positive-deficit weights.  A
consumer may use either a certified matched \(d_V\), or the universal lower
bound \(d_V\ge1\); it may not reconstruct (2.6) from the coarse factor alone.

## 3. All currently exported histogram constraints

Besides (2.8), the imported set-pair inequality gives

\[
\sum_{\delta=0}^{\Delta_{\max}}
\frac{h_\delta}{\binom{j+9-\delta}{9}}
\le1.
\tag{3.1}
\]

The distance of a nonzero difference of two selected errors gives, for
distinct slopes,

\[
\delta_\eta+\delta_\theta\le2j-d_V.
\tag{3.2}
\]

Indeed, \((\eta-\theta)^{-1}(e_\eta-e_\theta)\) is a \(y_1\)-lift, so its
weight is at least \(d_V\), while its support is contained in
\(E_\eta\cup E_\theta\).

Transversality makes the selected supports an inclusion antichain.  If, for
example, \(E_\eta\subseteq E_\theta\), then both selected errors lie in
\(F^{E_\theta}\).  Their syndrome difference puts \(y_1\) in
\(H_V(F^{E_\theta})\), and either syndrome then puts \(y_0\) there, contrary
to the transverse-witness hypothesis.  The complete-carrier identity is

\[
\bigcup_{\eta\in\Gamma}E_\eta=V,
\qquad
\bigcap_{\eta\in\Gamma}T_\eta=\varnothing.
\tag{3.3}
\]

These are genuine constraints.  None supplies a positive lower bound on any
\(\delta_\eta\), an average-deficit bound, or a cumulative deficit-tail bound.

## 4. Current-interface extremizer and route cut

Consider the histogram-only integer program obtained from (2.8):

\[
\max\sum_\delta h_\delta
\quad\text{subject to}\quad
\sum_\delta h_\delta\mu_{d_V}(\delta)
\le\binom{N_V}{9},
\qquad h_\delta\in\mathbf Z_{\ge0}.
\tag{4.1}
\]

Strict monotonicity (2.9) proves that its exact optimizer is

\[
h_0=\left\lfloor
\frac{\binom{N_V}{9}}{\mu_{d_V}(0)}
\right\rfloor,
\qquad
h_\delta=0\quad(\delta>0).
\tag{4.2}
\]

This is exactly the coarse uniform cap from the predecessor.

More strongly, put

\[
m=B_{\rm rem}+1
=274{,}980{,}725{,}508{,}892{,}089.
\tag{4.3}
\]

At every first-unpaid carrier point from the predecessor and hence at every
larger carrier in the corresponding coarse failure cell,

\[
m\mu_{d_V}(0)\le\binom{N_V}{9}.
\tag{4.4}
\]

The all-zero profile also passes every scalar constraint in Section 3:

- (3.1) reduces to
  \[
  m\le\binom{981{,}113}{9}
  =2{,}321{,}091{,}728{,}328{,}890{,}114{,}134{,}753{,}010{,}535{,}697{,}574{,}976{,}277{,}834{,}915;
  \]
- (3.2) reduces to \(0\le2j-d_V\), true since \(d_V\le R<2j\);
- equal-size distinct \(j\)-subsets form an antichain;
- every coarse-failure carrier satisfies
  \[
  j<N_V\le n<3j,
  \tag{4.5}
  \]
  so two \(j\)-sets cover \(V\) when \(N_V\le2j\), and three cover it when
  \(2j<N_V<3j\).  Additional distinct \(j\)-sets preserve the union.

For the last point, identify \(V\) with \([0,N_V)\).  If \(N_V\le2j\), use

\[
[0,j),\qquad[N_V-j,N_V).
\tag{4.6}
\]

If \(N_V>2j\), use

\[
[0,j),\qquad[j,2j),\qquad
[2j,N_V)\cup[0,3j-N_V).
\tag{4.7}
\]

All displayed sets have size \(j\) and their union is \(V\).  The number of
distinct \(j\)-subsets is more than sufficient: by binomial unimodality,

\[
\binom{N_V}{j}\ge\binom{N_V}{9}>B_{\rm rem}.
\tag{4.8}
\]

Equations (4.6)--(4.8) are only a cardinality/antichain/union fixture.  They do
not construct error values satisfying the common syndrome line, rank nine,
transversality, and all predecessor equations simultaneously.

We may therefore bank the following sharply scoped route cut:

> **Current-scalar-interface M2b route cut.**  M2b together with the currently
> exported scalar, set-pair, pairwise-deficit, antichain-size, and
> complete-union constraints does not improve the predecessor's coarse
> rank-nine cap.  A new positive-deficit incidence input is necessary for this
> M2b route.

This statement does not assert that an actual deployed Reed--Solomon family
realizes (4.2).  A future syndrome-line incidence theorem could exclude it;
that would be genuinely new information.

## 5. Sharp one-cut cumulative compiler

Fix the same \(N_V,d_V\), and a cutoff

\[
0\le D<\Delta_{\max}.
\]

Define

\[
H_D=\sum_{0\le\delta\le D}h_\delta,
\qquad
\mu_0=\mu_{d_V}(0),
\qquad
\mu_+=\mu_{d_V}(D+1),
\qquad
C_V=\binom{N_V}{9}.
\tag{5.1}
\]

For a proposed forbidden family of size \(m=B_{\rm rem}+1\), put

\[
G_D=C_V+1-m\mu_0,
\qquad
L_D=\left\lceil\frac{G_D}{\mu_+-\mu_0}\right\rceil,
\qquad
T_D^*=m-L_D.
\tag{5.2}
\]

When \(T_D^*\ge0\), the exact one-cut implication is

\[
\boxed{
H_D\le T_D^*
\quad\Longrightarrow\quad
|\Gamma|\le B_{\rm rem}.
}
\tag{5.3}
\]

Equivalently,

\[
T_D^*
=
\left\lfloor
\frac{m\mu_+-C_V-1}{\mu_+-\mu_0}
\right\rfloor.
\tag{5.4}
\]

The \(+1\), ceiling, and \(D+1\) are load-bearing.

To prove (5.3), among \(m\) items with at most \(T\) deficits at most \(D\),
the minimum possible M2b weight is

\[
T\mu_0+(m-T)\mu_+.
\tag{5.5}
\]

This is strictly larger than \(C_V\) precisely for \(T\le T_D^*\).  At
\(T=T_D^*+1\), the two-bin histogram

\[
h_0=T_D^*+1,
\qquad
h_{D+1}=m-T_D^*-1
\tag{5.6}
\]

has weight at most \(C_V\).  Hence (5.4) is the largest, and therefore weakest,
sufficient integer right side at this fixed cutoff, sharp within the one-cut
M2b histogram relaxation.

Different cutoffs are incomparable: increasing \(D\) counts more slopes but
also permits a larger right side.  There is no single globally weakest \(D\).

## 6. Exact deployed tail thresholds

For any fixed cutoff, the hardest carrier and source-distance corner is

\[
N_V=n,
\qquad d_V=1.
\tag{6.1}
\]

Indeed, \(\binom{N_V}{9}\) increases with \(N_V\), whereas
\(\mu_{d_V}(\delta)\) is nondecreasing with \(d_V\).  Thus a bound proved at
(6.1) is uniform over every remaining coarse failure cell.

At this universal corner, the first cutoff for which any nonnegative one-cut
bound can close is

\[
D_{\rm crit}=18{,}014.
\tag{6.2}
\]

The exact multiplicities are

\[
\mu_0
=1{,}184{,}288{,}048{,}715{,}968{,}585{,}930{,}152{,}451{,}399{,}175,
\tag{6.3}
\]

\[
\mu_{18{,}015}
=7{,}863{,}582{,}775{,}712{,}820{,}188{,}422{,}356{,}536{,}857{,}430.
\tag{6.4}
\]

Formula (5.2) gives

\[
L_{18{,}014}
=274{,}962{,}817{,}936{,}384{,}505,
\tag{6.5}
\]

and the sharp uniform condition

\[
\boxed{
H_{18{,}014}
\le17{,}907{,}572{,}507{,}584.
}
\tag{6.6}
\]

At the right side in (6.6), the exact histogram cap is \(B_{\rm rem}\); adding
one makes the cap \(B_{\rm rem}+1\).  At \(D=18{,}013\), the formal right side
is negative,

\[
T_{18{,}013}^*=-12{,}386{,}728{,}892{,}028,
\tag{6.7}
\]

so even requiring \(H_{18{,}013}=0\) cannot close.

For certified exact source distances at the full carrier, the first useful
cutoffs are:

| source-distance information | coarse \(\ell_0\) | first \(D\) | sharp \(T_D^*\) |
|:--|--:|--:|--:|
| universal \(d_V\ge1\) | 1 | 18,014 | 17,907,572,507,584 |
| \(d_V-j=1\) | 1 | 5 | 16,733,545,009,172,851 |
| \(d_V-j=2\) | 2 | 4 | 20,034,624,384,082,026 |
| \(d_V-j=3\) | 3 | 3 | 24,986,249,357,852,538 |
| \(d_V-j=4\) | 4 | 2 | 33,238,965,528,645,962 |
| \(d_V-j=5\) | 5 | 1 | 49,744,409,690,947,096 |
| \(d_V-j=6\) | 6 | 0 | 99,260,765,817,180,096 |

The first two rows have the same coarse factor and demonstrate why exact
\(d_V\) provenance cannot be discarded.

A bound only on \(h_0=H_0\) is not uniform.  At the worst corner, even
\(h_0=0\) permits \(h_1=B_{\rm rem}+1\), because

\[
\left\lfloor
\frac{\binom n9}{\mu_1(1)}
\right\rfloor
=1{,}825{,}533{,}707{,}437{,}507{,}960
>B_{\rm rem}.
\tag{6.8}
\]

## 7. Generic multi-cut compiler

Suppose a future incidence theorem proves sorted cumulative bounds

\[
0\le D_1<\cdots<D_q<\Delta_{\max},
\qquad
0\le T_1\le\cdots\le T_q\le m,
\qquad
H_{D_i}\le T_i.
\tag{7.1}
\]

Because the weights (2.6) are strictly increasing, the exact minimum M2b
weight among \(m\)-item histograms obeying (7.1) is

\[
T_1\mu(0)
+\sum_{i=2}^{q}(T_i-T_{i-1})\mu(D_{i-1}+1)
+(m-T_q)\mu(D_q+1).
\tag{7.2}
\]

The greedy construction filling each cheapest available bin attains (7.2),
so there is no hidden dynamic-programming relaxation.  If (7.2) exceeds
\(\binom{N_V}{9}\), M2b pays the family.  Unsorted cutoffs, decreasing caps,
or bounds not proved for the same selector are rejected.

## 8. Toy exact control

The companion Sage replay uses a weighted Vandermonde parity check over
\(\mathbf F_{17}\) with

\[
N=8,
\quad R=6,
\quad\kappa=2,
\quad j=5,
\quad s=2,
\quad r=1,
\quad d=1.
\tag{8.1}
\]

For deficits zero and one, the theorem gives multiplicities \(1,2\), and an
exhaustive injective-mask row-basis check gives the same minimum counts.  With
ambient budget \(\binom82=28\) and test size \(m=15\), the all-zero histogram
has weight 15.  The sharp one-cut boundary at \(D=0\) is

\[
H_0\le1:\quad1+14\cdot2=29>28,
\tag{8.2}
\]

whereas

\[
h_0=2,
\quad h_1=13:\quad2+13\cdot2=28.
\tag{8.3}
\]

This checks the integer boundary, ceiling, and greedy compiler.  It is a toy
MDS/arithmetic control, not an actual syndrome-line family and not deployed
evidence.

## 9. Ledger semantics and next lemma

This packet proves a route cut and a conditional compiler.  It does not prove
any deployed cumulative bound \(H_D\le T_D^*\).  Therefore

\[
U_{\rm paid}^{\rm after}=U_{\rm paid}^{\rm before},
\qquad
B_{\rm rem}^{\rm after}=B_{\rm rem}^{\rm before}.
\tag{9.1}
\]

The next mathematical obligation is now exact:

> Prove, for every surviving rank-nine complete selector, at least one
> cumulative bound \(H_D\le T_D^*(N_V,d_V)\), or freeze the exact syndrome-line
> support template that violates every currently available bound.

Any numerically sufficient tail is not an owner until its incidence proof is
present.  Intrinsic rank at least ten remains out of scope until this rank-nine
obligation is exhausted.

## Audit status

- **Dependencies:** #864 selector/carrier bridge and #867 rank ladder PROVEN;
  P2 and M2b IMPORTED/PROVEN; positive-deficit incidence lemma UNPROVEN.
- **Parameter dependence:** exact finite KoalaBear row only.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** exact integer certificate and a toy \(\mathbf F_{17}\)
  control; no deployed census.
- **Packet verdict:** GREEN route cut and compiler.
- **Global verdict:** YELLOW; rank nine, branch 3, and the row remain open.
