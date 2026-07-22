---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: For every c=2048 occupancy profile and fixed partial agreement template, any exact-boundary family above the printed conditional relaxed-Singleton threshold Lambda_SD(u,v) contains a minimal bad subfamily whose difference span loses rank over F(T) in the free F[phi]-module. The conditional thresholds are at most 17 and sum to 1988814 over all 261192 profiles, but known fixed-prefix sources already occupy rank one and exceed them in 193 profiles. Rank-drop classification and varying-template aggregation remain open.
architecture: M31_C2048_FIXED_TEMPLATE_MODULE_RANK_ROUTE_CUT_V1
partition_digest: CERTIFICATE_BOUND; no ledger atom assigned
atom_or_cell: HIGH_BOUNDARY_EXACT_CODEWORD / U_new
quantifier: Every target-field received word, every feasible occupancy profile, and every fixed exact partial agreement template at the deployed exact boundary.
projection_and_unit: Fixed-template quotient received word in the rank-2048 free F[phi]-module; minimal bad difference span; F(T)-column rank.
claimed_bound: Oversized fixed-template family implies module-rank drop. Conditional post-classification profile thresholds have maximum 17 and exact sum 1988814.
status: PROVED LOCAL DICHOTOMY / RANK-DROP AND VARYING-TEMPLATE OWNERS OPEN
impact: FULL-MODULE-RANK ROUTE CUT / CONDITIONAL BUDGET FIT
falsifier: A fixed-template family above Lambda_SD(u,v) for which every Chen-Zhang minimal bad difference span has full F(T)-column rank; a failed determinant-valuation inequality; or a mismatch in the exact profile/source census.
replay: Python exact all-profile census, canonical certificate, and semantic mutations; Sage determinant-valuation, rank-drop, and census replay.
---

# M31 `c=2048` fixed-template module-rank route cut

## Status

```text
PROVED full-module-rank determinant-valuation inequality
PROVED oversized fixed-template list => deficient minimal difference span
PROVED exact 261192-profile relaxed-Singleton threshold census
UNPROVEN classification/payment of deficient module components
UNPROVEN varying-template attained-incidence aggregation
ledger movement = 0
M31 LIST row closed = false
```

This packet takes the maximal successor to the fixed-template interleaved
quotient theorem.  It applies the minimal-sublist argument of Chen--Zhang's
strong-subspace-design proof only after replacing their folded-Wronskian
input by a direct determinant-valuation bound in the deployed free
`F[phi]` module.  Thus no folded-Reed--Solomon orbit or generator hypothesis
is imported.

The result is a dichotomy, not a payment.  A fixed-template list above an
explicit conditional threshold at most 17 must contain a difference span of
deficient `F(T)`-rank.  This exceptional stratum is not hypothetical: the
known fixed-prefix source lies in module rank one and exceeds the conditional
threshold in 193 profiles.  Classifying those deficient components and
aggregating across different partial templates are still required before any
atom can move.

## 1. Fixed-template quotient code

Keep the deployed constants

\[
 p=2^{31}-1,\quad n=2^{21},\quad K=2^{20},\quad
 A=1116023,\quad c=2048,
\]

and let `F` be any coefficient field containing `F_p`; in the application
`F=F_{p^4}`.  For a feasible occupancy profile `(u,v)`, put

\[
 h=u+v+1,\qquad r=1911+2048v,
\]
\[
 f=544-v,\qquad M=1023-u-v.
\tag{1.1}
\]

Fix the partial labels and one exact partial agreement template `P_0` of
size `r`.  The predecessor packet proves that, when `v<=511`, translation
and division by the fixed locator `L_0` identify its codewords with the
linear message space

\[
 \mathcal V_v=
 F[T]_{\le D}^{137}\oplus F[T]_{\le D-1}^{1911},
 \qquad D=511-v,
\tag{1.2}
\]

of dimension

\[
 d=137(D+1)+1911D=2048D+137=1046665-2048v.
\tag{1.3}
\]

Evaluation at the `M` available quotient labels gives a linear code

\[
 \mathcal C_{u,v,P_0}:\mathcal V_v\longrightarrow(F^{2048})^M.
\tag{1.4}
\]

The map is injective because `M-D=512-u>=33`.  Every member of the exact
boundary family agrees with the one fixed quotient received word on exactly
`f` quotient labels.  When `v>=512`, the common partial template already has
at least `K` points, so the predecessor's uniqueness theorem applies; below
we only discuss `v<=511`.

For an available label `b`, define

\[
 H_b=\{q\in\mathcal V_v:q_0(b)=\cdots=q_{2047}(b)=0\}.
\tag{1.5}
\]

## 2. The direct module-rank design lemma

Let `W` be an `ell`-dimensional `F`-linear subspace of `V_v`, and choose an
`F`-basis as the columns of a `2048 x ell` polynomial matrix `A_W(T)`.
Call `W` **module-regular** when

\[
 \operatorname{rank}_{F(T)}A_W=\ell.
\tag{2.1}
\]

### Lemma 2.1 (determinant-valuation bound)

If `W` is module-regular, then

\[
 \boxed{\sum_{b}\dim_F(W\cap H_b)\le\ell D,}
\tag{2.2}
\]

where the sum may range over any distinct field labels, in particular the
`M` deployed available labels.

### Proof

Let `delta_ell(A_W)` be the monic gcd of all maximal minors.  Module
regularity makes it nonzero.  If a maximal minor uses `a` of the 137
degree-`D` rows and `ell-a` degree-`D-1` rows, its degree is at most

\[
 aD+(\ell-a)(D-1).
\tag{2.3}
\]

Consequently

\[
 \deg\delta_\ell(A_W)
 \le B_\ell:=\ell(D-1)+\min(\ell,137)
 \le\ell D.
\tag{2.4}
\]

When `D=0`, module regularity itself forces `ell<=137`; then (2.4) reads
`deg delta_ell<=0`.  Thus the displayed bound never uses a negative degree.

At a label `b`, set `s_b=dim_F(W intersection H_b)`.  This is the nullity of
the full evaluation matrix `A_W(b)`.  Smith normal form over the DVR
`F[T]_(T-b)` gives

\[
 s_b\le \operatorname{ord}_{T-b}\delta_\ell(A_W).
\tag{2.5}
\]

Summing (2.5) over distinct labels and using (2.4) proves (2.2).  Basis
changes here are in `GL_ell(F)` and change the determinantal divisor only by
a unit.  A rational `GL_ell(F(T))` change is not legal: it can create or
cancel the local factors whose valuations are being counted.
\(\square\)

For `1<=ell<=2048`, (1.3) also gives

\[
 \ell D\le {\ell(d-1)\over2049-\ell},
\tag{2.6}
\]

because `d-1=2048D+136` and

\[
 (d-1)-D(2049-\ell)=136+D(\ell-1)\ge0.
\tag{2.7}
\]

Thus one module-regular span satisfies exactly the strong-subspace-design
inequality required at that span, without asserting that the entire quotient
code is a strong subspace design.  The latter global assertion is false when
module-deficient spans exist.

## 3. Localized relaxed-Singleton dichotomy

For `v<=511`, let `Lambda^SD_{u,v}` be the least integer `1<=L<=2048`
satisfying

\[
 (L+1)f(2049-L)
 \ge M(2049-L)+Ld.
\tag{3.1}
\]

For `v>=512`, set `Lambda^SD_{u,v}=1`, in agreement with fixed-template
uniqueness.  The superscript distinguishes this conditional threshold from
the repository's already-used `L_(u,v)` notation for a proved source floor.

### Theorem 3.1 (oversized family forces module-rank drop)

Fix a received word, a feasible profile `(u,v)` with `v<=511`, and one exact
partial template `P_0`.  If its exact-boundary family contains at least
`Lambda^SD_{u,v}+1` distinct codewords, then the Chen--Zhang minimal-bad-sublist
extraction produces a subfamily of size `m`, with

\[
 2\le m\le \Lambda^{SD}_{u,v}+1,
\]

whose translated difference span `W` has

\[
 1\le\dim_F W\le m-1
\quad\hbox{and}\quad
 \operatorname{rank}_{F(T)}A_W<\dim_F W.
\tag{3.2}
\]

Equivalently, a fixed-template family in which every extracted minimal bad
difference span is module-regular has size at most `Lambda^SD_{u,v}`.
For `v>=512`, the predecessor's common-template uniqueness theorem gives cap
one directly, so no rank-dichotomy assertion is needed.

### Proof

For a subfamily `V`, let `e_b` be the codewords agreeing with the quotient
received word at label `b`, and put

\[
 \operatorname{wt}(V)=\sum_b(|e_b|-1)_+.
\]

The `L+1` codewords agree on `f` blocks each, so

\[
 \operatorname{wt}(V)\ge(L+1)f-M.
\]

Equation (3.1) is precisely the weak, equality-inclusive threshold

\[
 (L+1)f-M\ge {Ld\over2049-L}.
\tag{3.3}
\]

The minimal-sublist selection in Chen--Zhang, Lemma B.4, chooses an
inclusion-minimal `V_0` of size `m>=2` satisfying

\[
 \operatorname{wt}(V_0)\ge{(m-1)d\over2050-m},
\]

while every proper subfamily of size at least two fails its corresponding
inequality.  Translate one vertex to zero, let `ell=affdim_F(V_0)`, and let
`W` be the resulting difference span.  For every `b`, write
`a_b=affdim_F(e_b)`.  The affine-matroid partition and hyperedge-loss bound
in their Theorem 2.15, used exactly as in Lemma B.4, gives

\[
 \sum_b\dim_F(W\cap H_b)
 \ge\sum_b a_b
 \ge {\ell d\over2050-m}
 \ge {\ell d\over2049-\ell}
 > {\ell(d-1)\over2049-\ell}.
\tag{3.4}
\]

The first inequality holds because the `a_b` independent incident
differences lie in `W intersection H_b`.  The final strict one-unit gap is
why equality in (3.1) is already forbidden.  If `W` were module-regular,
Lemma 2.1 and (2.6) would give

\[
 \sum_b\dim_F(W\cap H_b)
 \le\ell D
 \le {\ell(d-1)\over2049-\ell},
\]

contradicting (3.4).  Hence the selected `W` is module-deficient.
\(\square\)

The imported combinatorial facts are Theorem B.3, Lemma B.4, and the
hyperedge-loss lemma cited there from [Chen--Zhang, arXiv:2408.15925 v3,
Appendix B](https://arxiv.org/abs/2408.15925).  Their folded-Wronskian
criterion, multiplicative generator, and folded evaluation orbits are not
used.  The audited 31-page v3 PDF has SHA-256
`1d4a4859229351d1c345653e5d7eb63682f855c0b080b947d40fe1ecaf88c56a`.
The new algebraic input replacing those ingredients is Lemma 2.1.

## 4. Exact deployed threshold census

Exhausting the proved 261,192 profile atlas gives

\[
 \max_{u,v}\Lambda^{SD}_{u,v}=17,
 \qquad
 \sum_{u,v}\Lambda^{SD}_{u,v}=1,988,814.
\tag{4.1}
\]

The complete histogram is

```text
L=1: 32703     L=7: 16092     L=13: 15314
L=2: 16896     L=8: 15957     L=14: 15184
L=3: 16657     L=9: 15833     L=15: 13886
L=4: 16486     L=10:15705     L=16:  6170
L=5: 16349     L=11:15574     L=17:   712
L=6: 16227     L=12:15447
```

Exactly four profiles attain equality in (3.1):

```text
(u,v,L) = (31,365,14), (91,400,12), (223,239,8), (285,266,6).
```

They are included at the displayed threshold.  Replacing `>=` by `>` would
incorrectly increase the total by four.

### The rank-drop stratum is already large

The conditional threshold is not an unconditional cap.  At profile `(0,0)`,

\[
 W=\operatorname{Span}_F\{e_0,Te_0\}
\]

has `F`-dimension two and `F(T)`-rank one.  For every one of the 1,023
available quotient labels,

\[
 W\cap H_b=F\,(T-b)e_0.
\]

Hence

\[
 \sum_b\dim_F(W\cap H_b)=1023>2D=1022,
\]

so the unconditional strong-subspace-design assertion fails by one.

More decisively, in the proved fixed-prefix source, let
`C_0=U mod L_P` and `Q_0=(U-C_0)/L_P`.  After the fixed locator `L_P` is
cancelled, each quotient message is `q_E=Q_0-V_E(phi)`, so differences have
the form

\[
 q_E-q_{E'}=-(V_E-V_{E'})e_0.
\tag{4.2}
\]

Every such difference family therefore has module rank at most one even when
its `F`-affine dimension is much larger.  The separately realized
fixed-multipartial-template sources give at least
6,796,405 members at `(0,0)` and 1,693,898 at `(1,1)`, while
`Lambda^SD=17` at both.  Exact comparison of the proved source-floor formula
with the conditional thresholds gives

```text
profiles with source floor > Lambda^SD: 193
  Lambda^SD=17:                         176
  Lambda^SD=16:                          17
```

These profile floors are not claimed simultaneously around one received
word.  Thus the theorem genuinely routes a large known family to rank drop;
it does not nearly close the boundary by itself.  Only the #1039 certified
fixed-remainder structured subfamily is known to route by or at C1 under the
declared first-match order.  The other separately realized multiprefix
rank-one source profiles are not thereby C1-classified.  Arbitrary rank-one
and higher-defect components remain unclassified.

The conditional post-classification arithmetic is favorable:

\[
 1,988,814<9,216,781
\]

by `7,227,967`, and

\[
 U_{paid}+1,988,814=3,730+1,988,814=1,992,544<B_*
\]

by `14,784,671`.  These are only target comparisons.  They become a real
charge only after a disjoint owner pays every module-deficient component and
the varying-template aggregation is proved.

## 5. Nested diagnostic subterminal

Theorem 3.1 refines the oversized fixed-template branch to the nested
diagnostic

```text
UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP
```

inside the unchanged global terminal

```text
UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER.
```

A rank drop means there is a nontrivial `F(T)`-linear relation among the
free-module component columns.  Clearing denominators gives a polynomial
syzygy, but rank drop alone is not a quotient, periodicity, or codeword
payment.  The next classification must assign each deficient component to a
declared chronology-valid owner or retain it as an explicit primitive
component.

This is not a partition update: `UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`
remains active globally and no first-match owner or codeword charge changes.

Different exact partial templates remain a separate obstruction.  Their
translations use different `L_0` and different remainders `C_0=Y mod L_0`,
so Theorem 3.1 cannot sum their threshold caps.  The predecessor's exact
two-template source shows this distinction is realized.

## 6. Scope and nonclaims

This packet moves no value in `U_paid`, `U_Q`, `U_list-int`, `U_ext`, or
`U_new`.  It proves neither the conditional sum (4.1) as a global list bound
nor the 9,216,781 boundary payment.  It does not classify module-rank drop,
aggregate varying templates, pay high interior weights, or close the M31
row.  It does not transfer the Chen--Zhang FRS theorem directly to Chebyshev
fibers.

There is no probabilistic moment, Markov, Chebyshev, layer-cake, or dyadic
argument.  All profile counts are exact integer enumerations.  `Chebyshev`
refers only to the deployed polynomial fold.
