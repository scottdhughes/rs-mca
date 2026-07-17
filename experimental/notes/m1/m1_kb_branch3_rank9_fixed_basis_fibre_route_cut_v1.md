# M1 KoalaBear rank-nine fixed-basis fibre route cut v1

- **Status:** PROVED fixed-basis affine-line reduction / PROVED exact
  aggregate compiler / COUNTEREXAMPLE to the uniform cap 20 / no ledger
  movement.
- **Scope:** one matched complete affine-rank-nine selector from the
  KoalaBear branch-3 actual-core route, and the generic-local five-pencil
  family of `m1_rank9_regular_locator_span_shortcut_refuted_v1.md`.
- **Predecessors:**
  `m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md`,
  `m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md`, and
  `m1_rank9_regular_locator_span_shortcut_refuted_v1.md`.
- **Companion checks:**
  `verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.py` and
  `verify_m1_kb_branch3_rank9_fixed_basis_fibre_v1.sage`.

This packet audits one proposed route to the missing deficit-tail input

\[
 H_{18{,}014}
 =\#\{\eta:\delta_\eta\le18{,}014\}
 \le17{,}907{,}572{,}507{,}584.
\tag{0.1}
\]

The proposed route was to fix an eight-row basis of the actual kernel core
and prove that at most 20 low-deficit masks contain it.  The local reduction
to an affine word line is correct, and cap 20 would close (0.1) with a strict
margin.  The cap itself is false: the parametric five-pencil rank-nine family
already gives \(j+1\) full-weight masks through one fixed core basis.  An exact
\(j=20\) specialization has multiplicity 21.

The correct surviving target is aggregate, not pointwise.  This note prints
the exact total excess above 20 that the deployed double count can tolerate.

## 1. Frozen deployed interface

Use the KoalaBear row

\[
 n=2{,}097{,}152,\qquad k=1{,}048{,}576,\qquad
 A=1{,}116{,}048,
\]

\[
 R=n-k=1{,}048{,}576,\qquad
 j=n-A=981{,}104,\qquad
 \Delta_0=R-j=67{,}472.
\tag{1.1}
\]

Fix one complete selector on the source-bound branch-3 rank-nine successor,
with the rank, carrier, source distance, supports, and zero masks all belonging
to this same selector.  Write

\[
 K_0=\mathcal D\cap K_V,qquad \dim K_0=8,
\]

and let \(g_x\in F^8\) be the coordinate row of a fixed generator of \(K_0\)
at \(x\in V\).  For every selected slope put

\[
 E_\eta=\operatorname{supp}(e_\eta),qquad
 T_\eta=V\setminus E_\eta,qquad
 \delta_\eta=j-|E_\eta|.
\tag{1.2}
\]

The imported MDS row-flat argument proves that \(T_\eta\) contains at least

\[
 \binom{67{,}480+\delta_\eta}{8}
\tag{1.3}
\]

eight-subsets on which the rows \(g_x\) form a basis of \(F^8\).  Therefore,
for every \(\delta_\eta\le18{,}014\), it contains at least

\[
 C_0:=\binom{67{,}480}{8}
 =10{,}658{,}592{,}438{,}443{,}717{,}273{,}371{,}372{,}062{,}592{,}575
\tag{1.4}
\]

such bases.

For an eight-subset \(B\subseteq V\), define

\[
 m_B=
 \#\{\eta:\delta_\eta\le18{,}014,
                 B\subseteq T_\eta,
                 (g_x)_{x\in B}\text{ is a basis of }F^8\}.
\tag{1.5}
\]

Double counting gives

\[
 H_{18{,}014}C_0\le\sum_{B\in\binom V8}m_B.
\tag{1.6}
\]

This uses actual zero masks.  It does not use the padded size-\(j\) locator
support from the sparse Pad\'e chart.

## 2. Fixed-basis affine-line lemma

### Lemma 2.1

Fix an eight-subset \(B\) whose \(K_0\)-rows form a basis.  Then all selected
errors whose complete zero masks contain \(B\) lie on one affine word line

\[
 e_\eta=a_B+\eta b_B,qquad
 Ha_B=y_0,qquad Hb_B=y_1,qquad
 a_B|_B=b_B|_B=0.
\tag{2.1}
\]

#### Proof

The actual-core representation may be written

\[
 e_\eta=u+\eta v+w_\eta,qquad w_\eta\in K_0,
\tag{2.2}
\]

with \(Hu=y_0\) and \(Hv=y_1\).  Since the rows on \(B\) form a basis, the
restriction map

\[
 \rho_B:K_0\longrightarrow F^B
\]

is an isomorphism.  If \(B\subseteq T_\eta\), the zero equations give

\[
 \rho_B(w_\eta)=-u|_B-\eta v|_B.
\]

Thus

\[
 w_\eta=k_{B,0}+\eta k_{B,1},qquad
 k_{B,0}=-\rho_B^{-1}(u|_B),qquad
 k_{B,1}=-\rho_B^{-1}(v|_B).
\]

Set \(a_B=u+k_{B,0}\) and \(b_B=v+k_{B,1}\).  This proves (2.1).  In
particular \(b_B\ne0\), because \(Hb_B=y_1\ne0\).  ∎

Put

\[
 W_B=\operatorname{supp}(a_B)\cup\operatorname{supp}(b_B),qquad
 M_B=|W_B|.
\tag{2.3}
\]

At every coordinate of \(W_B\), the function

\[
 \eta\longmapsto a_B(x)+\eta b_B(x)
\]

is a nonzero affine function and hence vanishes at at most one slope.  Define

\[
 \Gamma_B=\{\eta:B\subseteq T_\eta\},\qquad J_B=|\Gamma_B|.
\]

For the retained slopes in \(\Gamma_B\), the zero set of the word at \(\eta\)
inside \(W_B\) has exact size

\[
 M_B-|E_\eta|=M_B-j+\delta_\eta.
\]

These zero sets are disjoint.  Therefore the exact weighted inequality is

\[
 \boxed{
 J_B(M_B-j)+\sum_{\eta\in\Gamma_B}\delta_\eta\le M_B.}
\tag{2.4}
\]

In particular, when \(M_B>j\),

\[
 J_B(M_B-j)\le M_B.
\tag{2.5}
\]

No MDS, Johnson, or asymptotic estimate is hidden in (2.4).  It is the exact
coordinate-zero incidence bound for an affine word line.

## 3. Exact trichotomy and the corrected integer threshold

There are three cases.

### 3.1 Common-support side

If \(M_B\le j\), then \(a_B\) and \(b_B\) are lifts of \(y_0,y_1\) on one
common support of size at most \(j\).  Thus the original received pair is not
column-far at agreement \(A\).  This routes to

```text
CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA
```

and is not a zero-cost owner.

### 3.2 Large-union side

To force \(J_B\le20\) from (2.5), it is enough and integer-sharp to rule out
\(J_B\ge21\).  The condition is

\[
 21(M_B-j)>M_B,
\]

equivalently

\[
 \boxed{
 M_B\ge
 \left\lfloor\frac{21j}{20}\right\rfloor+1
 =1{,}030{,}160=:M_{20}.}
\tag{3.1}
\]

At \(M_B=M_{20}\),

\[
 21(M_B-j)=1{,}030{,}176>M_B,
\]

whereas at \(M_B=M_{20}-1\),

\[
 21(M_B-j)=1{,}030{,}155<M_B.
\]

The earlier diagnostic \(\lceil20j/19\rceil=1{,}032{,}742\) is a stronger
condition forcing the real ratio \(M_B/(M_B-j)\le20\); at the deployed
integer it already forces \(J_B\le19\).  It is not the sharp integer threshold
for excluding 21 slopes.

### 3.3 Low-union fixed-basis side

The unresolved interval is

\[
 \boxed{981{,}105\le M_B\le1{,}030{,}159.}
\tag{3.2}
\]

It lies strictly below \(R=1{,}048{,}576\).  Name it

```text
LOW_UNION_FIXED_BASIS_AFFINE_LINE_ROUTE
```

and do not force it into an existing owner.  For one fixed \(B\), this fibre
has a low carrier and affine rank at most one.  But the proved carrier and
rank-\(\le3\) payments are global one-family terminals.  The project notes
explicitly forbid summing them over an unproved cover by many \(B\)'s.  The
carriers for different bases may vary, and a slope may contain many bases.

## 4. Exact deployed compiler

If every basis satisfied \(m_B\le20\), (1.6) would give

\[
 H_{18{,}014}
 \le
 \left\lfloor
 \frac{20\binom n8}{\binom{67{,}480}{8}}
 \right\rfloor
 =17{,}411{,}776{,}716{,}968.
\tag{4.1}
\]

The margin below the target in (0.1) is

\[
 495{,}795{,}790{,}616.
\tag{4.2}
\]

Replacing 20 by 21 gives

\[
 \left\lfloor
 \frac{21\binom n8}{\binom{67{,}480}{8}}
 \right\rfloor
 =18{,}282{,}365{,}552{,}816,
\tag{4.3}
\]

which exceeds the target by \(374{,}793{,}045{,}232\).  Hence 20 is the
largest useful uniform integer for this particular basis double count.

The pointwise cap is stronger than necessary.  Define the aggregate excess

\[
 \mathcal E_{20}:=
 \sum_{B\in\binom V8}(m_B-20)_+.
\tag{4.4}
\]

Since the large-union fibres contribute no excess, only (3.2) and the
common-support side can contribute.  The exact largest sufficient allowance is

\[
\begin{aligned}
 E_{\max}
 &=(17{,}907{,}572{,}507{,}584+1)
   \binom{67{,}480}{8}
   -20\binom n8-1\\
 &=5{,}284{,}485{,}264{,}881{,}189{,}380{,}664{,}190{,}436{,}821{,}715{,}347{,}228{,}277{,}374.
\end{aligned}
\tag{4.5}

Indeed,

\[
 \sum_Bm_B
 \le20\binom{|V|}{8}+\mathcal E_{20}
 \le20\binom n8+E_{\max}
 <(17{,}907{,}572{,}507{,}584+1)C_0.
\]

Together with (1.6), this proves (0.1).  At \(E_{\max}+1\), the resulting
integer quotient is exactly \(17{,}907{,}572{,}507{,}585\).  Thus (4.5) is
sharp inside this aggregate basis-incidence compiler.

The missing theorem can therefore be stated without the false pointwise cap:

\[
 \boxed{\mathcal E_{20}\le E_{\max}.}
\tag{4.6}

Any proof of (4.6) must use deployed support incidence, full-family
exhaustion, or an executable first-match owner.  The MDS row-flat profile
alone only supplies the lower incidence (1.6).

## 5. Exact counterexample to the pointwise cap

The five-pencil construction in the locator-span predecessor works for every
\(j\ge10\).  It has

\[
 n=j+14,qquad k=13,qquad R=j+1,qquad
 (s_*,t,\kappa_*)=(9,10,11),
\tag{5.1}
\]

and a unique complete transverse regular selector on its explicitly declared
retained family.  Every selected error has weight exactly \(j\), hence
\(\delta=0\).

Each of the five pencils has a fixed eleven-point core \(C\).  Its zero masks
are

\[
 T_z=C\cup\{z\},qquad z\in B\setminus C,qquad |B\setminus C|=j+1.
\tag{5.2}
\]

In the exact \(j=10\) control, the restriction of \(K_0\) to each frozen core
has rank eight.  The parametric family retains that old \(K_0\), while its
affine rank remains nine; hence the kernel core remains the same
eight-dimensional space.  Choose any eight-row basis \(B_0\subset C\).  Then

\[
 B_0\subset T_z\quad\text{for all }z\in B\setminus C,
\qquad m_{B_0}=j+1.
\tag{5.3}

The Sage companion gives a fully explicit first violating specialization:

\[
 F=\mathbb F_{2^{37}},qquad
 (n,k,R,j,A)=(34,13,21,20,14),
\]

with 105 distinct declared slopes, rank tuple \((9,10,11)\), five core
restriction ranks all equal to eight, and

\[
 m_{B_0}=21>20.
\tag{5.4}

This is a generic-local counterexample.  It does not instantiate the
KoalaBear cyclic domain, exhaust the full bad-slope family, execute its
periodic/quotient/Johnson/B11 masks, or violate the deployed aggregate bound
(4.6).

## 6. Existing-owner and literature audit

The existing-owner audit is fail-closed:

- \(M_B\le j\) is exactly the non-column-far sparse route, still unpaid;
- \(M_B\ge M_{20}\) gives the proved cap 20;
- (3.2) is not paid by repeatedly invoking a global carrier or low-rank
  terminal;
- the rank-nine column-far family is already paid by the predecessor's
  syndrome-rank reduction, so the hard use of (4.6) is on the sparse side;
- the sparse regular split-locator aggregation remains open.

TheoremSearch was queried for MDS/RS affine-line support, generalized-weight,
and list-recovery theorems.  Its returned projective-incidence results did not
match this fixed-basis selector interface.  A separate primary-source search
found:

- Srivastava's affine-subspace/Hamming-ball intersection theorem
  ([arXiv:2410.09031](https://arxiv.org/abs/2410.09031)); at the deployed
  rank-nine dimension its useful minimum-distance regime is already inside
  the stronger source-distance region paid by the existing M2b terminal;
- Brakensiek--Gopi--Makam's higher-order MDS/list-decoding equivalence for
  generic RS codes
  ([arXiv:2206.05256](https://arxiv.org/abs/2206.05256)); no corresponding
  fixed-domain higher-order-MDS certificate is known here;
- Tamo's point--polynomial incidence theorem
  ([arXiv:2312.12962](https://arxiv.org/abs/2312.12962)); its stated RS
  average-radius regime does not reach this row.

None is imported into the proof of Sections 1--5.  The search therefore does
not supply the missing aggregate theorem (4.6).

## 7. Classifier and ledger semantics

For one certified fixed basis use:

```text
derive the exact affine word line and M_B
if M_B <= j:
    CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA
elif M_B >= 1030160:
    FIXED_BASIS_AFFINE_LINE_CAP_20
else:
    LOW_UNION_FIXED_BASIS_AFFINE_LINE_ROUTE
```

For the whole tail use:

```text
if a deployed proof gives aggregate excess E_20 <= E_max:
    PAID_BY_RANK9_FIXED_BASIS_AGGREGATE_EXCESS
else:
    UNPAID_RANK9_FIXED_BASIS_AGGREGATION
```

The current status is the second terminal.  Therefore

\[
 U_{\rm paid}=2{,}602{,}502{,}999,
 \qquad
 B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088
\]

remain unchanged.

## 8. Audit status and nonclaims

- **PROVED:** fixed-basis affine-line reduction, zero-incidence inequality,
  sharp union threshold, exact deployed aggregate compiler, and the explicit
  \(j=20\) counterexample to cap 20.
- **UNPROVEN:** the deployed aggregate excess inequality (4.6), full sparse
  first-match aggregation, rank at least ten, \(U_Q\), and \(U_A\).
- **Parameter dependence:** Sections 1 and 4 use exact KoalaBear integers;
  Sections 2--3 are field-uniform; Section 5 is an exact finite-field
  counterexample family.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** Python uses exact big integers; Sage gives an exact
  \(\mathbb F_{2^{37}}\) construction.  Neither is a KoalaBear deployed-field
  census.
- **Global verdict:** YELLOW.  This is a rigorous route cut, not rank-nine or
  branch-3 closure.

In particular, this packet does not:

- claim a deployed counterexample to (0.1);
- replace the declared-family quantifier by full bad-slope exhaustion;
- sum low-carrier or low-rank owners over fixed bases;
- call non-column-far correlated agreement a paid owner;
- move the ledger;
- close branch 3 or the KoalaBear row;
- attack intrinsic rank at least ten;
- determine \(U_Q\) or \(U_A\);
- authorize Lean or stable-paper promotion.

## 9. Minimal next action

Do not pursue a uniform fixed-basis cap.  On the source-bound sparse regular
route, freeze the low-union bases from (3.2) and prove either:

1. the aggregate excess bound (4.6), with a canonical/exhaustive
   first-match projector; or
2. an exact deployed countertemplate whose aggregate excess exceeds
   \(E_{\max}\).

The current five-pencil family says that pointwise elimination is impossible;
the next theorem must couple different bases or use the deployed domain.
