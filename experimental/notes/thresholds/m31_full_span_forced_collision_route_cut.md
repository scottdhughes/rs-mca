---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Characterize identically forced collision forms on the complete exact-layer containment-functional space and decide whether that condition alone forces packing number at most four or a four-point transversal for the natural anchor-extra collision-root unions.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: U_new diagnostic refinement; U_paid remains 3730 and U_Q, U_list-int, U_ext, and high U_new remain null
quantifier: Every field, every exact-support family, and every pairwise common error point for the abstract theorem; the finite falsifier is one complete GF(17) same-received-word layer and is not a deployed survivor.
projection_and_unit: Distinct codewords per received word; collision incidences and locator-span membership are diagnostics, not additive charges.
claimed_bound: A collision form is identically forced exactly when its representing polynomial lies in the span of the selected containment rows. If that span is the whole syndrome hyperplane, forced means only actual collision. An exhaustive GF(17) complete layer realizes this full-span branch on every marked key while retaining packing number five and transversal number six for the natural anchor-extra forced-collision-root unions. Separately, the proved deployed identity-prefix boundary source forces T46 at least 1,993,633, refuting the proposed raw T46 cap and making signed chronology/refunds mandatory.
status: PROVED
impact: ROUTE_CUT
falsifier: Either a claimed implication from identically forced collision on every marked key to packing number at most four or a four-point transversal for the natural anchor-extra collision-root unions, or a claimed row-uniform raw bound T46<=259880.
replay: Standard-library Python normal/optimized checks and mutations, independent Sage replay, strict JSON schema/hash gates, and predecessor replays.
---

# Full-span forced collisions do not coalesce the natural root unions

## 1. Result

This packet closes the algebraic classification requested by the target-field
deformation dichotomy, but the classification is a route cut rather than a
payment.

Let

\[
 V=\mathbb F[X]_{<K}
\]

and let \(\mathcal S\) be any family of candidate exact error supports.  The
selected containment rows span

\[
 \mathcal A(\mathcal S)
 =\operatorname{span}_{\mathbb F}
 \left\{X^tL_E:
 E\in\mathcal S,\ 0\le t<K-|E|\right\}\subseteq V.
\tag{1.1}
\]

Their common containment-functional space is exactly

\[
 \mathscr L(\mathcal S)=\mathcal A(\mathcal S)^\perp\subseteq V^*.
\tag{1.2}
\]

For \(x\in E_i\cap E_k\), the collision form from the predecessor packet is
represented by one polynomial \(g_{ik,x}\in V\).  Finite-dimensional
annihilator duality gives the exact criterion

\[
 \boxed{
 \chi_{ik,x}|_{\mathscr L(\mathcal S)}\equiv0
 \quad\Longleftrightarrow\quad
 g_{ik,x}\in\mathcal A(\mathcal S).}
\tag{1.3}
\]

This is a complete symbolic classification of the words “identically
forced.”  It is not yet an owner: the right side is membership in a global
linear span, with no quotient, periodic, Johnson, extension, or first-match
semantics attached.

The obstruction is sharp.  In the complete \(GF(17)\) layer already used by
the predecessor, the 137 exact degree-six locators span the entire
six-dimensional syndrome hyperplane.  Hence the common functional space is
only the original one-dimensional line, and every actual collision is
automatically identically forced.  Nevertheless every one of the 92 marked
keys has a forced collision, while their natural forced-root unions still
have exact disjoint-packing optimum five and exact transversal number six.

Thus merely recognizing an identically forced component does not imply
packing number at most four or a four-point transversal for these natural
anchor--extra forced-root unions.  A closing theorem must use a genuinely
M31-specific bound or owner/refund for split exact locators in one syndrome
hyperplane, a cross-weight/complete-list invariant, or the direct
signed occupancy bound \(\Xi_{46}\le259880\).  A raw distinguished-codeword
cap at that value is ruled out in Section 6.

## 2. Exact annihilator criterion

Fix a field \(\mathbb F\), a finite evaluation domain \(D\subset\mathbb F\),
and \(K\ge1\).  For \(E\subseteq D\) with \(|E|<K\), put

\[
 L_E(X)=\prod_{a\in E}(X-a).
\tag{2.1}
\]

The containment condition for a functional \(\ell\in V^*\) is

\[
 \ell(X^tL_E)=0,
 \qquad 0\le t<K-|E|.
\tag{2.2}
\]

Consequently (1.2) is a definition-free equality: intersecting the kernels
of all functionals \(\ell\mapsto\ell(X^tL_E)\) is the annihilator of their
span.

For distinct supports \(E_i,E_k\) and \(x\in E_i\cap E_k\), define

\[
 g_{ik,x}
 =L_{E_k}'(x)\frac{L_{E_i}}{X-x}
  -L_{E_i}'(x)\frac{L_{E_k}}{X-x}.
\tag{2.3}
\]

Its degree is less than \(K\), so it lies in \(V\), and the collision form is

\[
 \chi_{ik,x}(\ell)=\ell(g_{ik,x}).
\tag{2.4}
\]

Equivalently, with

\[
 v_{i,x}=\frac{L_{E_i}}{(X-x)L_{E_i}'(x)},
\]

one has

\[
 g_{ik,x}=L_{E_i}'(x)L_{E_k}'(x)(v_{i,x}-v_{k,x}).
\tag{2.5}
\]

Because the derivative factors are nonzero, (1.3) is also equality of the
two normalized escape columns in the quotient

\[
 V/\mathcal A(\mathcal S).
\tag{2.6}
\]

It is not equality of the raw locators or of the unnormalized columns.

### Theorem 2.1 (forced-collision annihilator criterion)

For the data above, the following are equivalent:

1. \(\chi_{ik,x}\) vanishes on every \(\ell\in\mathscr L(\mathcal S)\);
2. \(g_{ik,x}\in\mathcal A(\mathcal S)\);
3. \([v_{i,x}]=[v_{k,x}]\) in \(V/\mathcal A(\mathcal S)\);
4. there are polynomials \(A_E\), with
   \(\deg A_E<K-|E|\), such that
   \[
      g_{ik,x}=\sum_{E\in\mathcal S}A_EL_E;
   \tag{2.7}
   \]
5. appending the coefficient row of \(g_{ik,x}\) to any coefficient matrix
   spanning (1.1) does not increase its rank.

#### Proof

By (1.2), assertion 1 says exactly that every element of
\(\mathcal A(\mathcal S)^\perp\) annihilates \(g_{ik,x}\).  Since \(V\) is
finite dimensional,

\[
 \left(\mathcal A(\mathcal S)^\perp\right)^\perp
 =\mathcal A(\mathcal S),
\]

which proves \(1\Longleftrightarrow2\).  Equation (2.5) and nonvanishing of
the two derivative values prove \(2\Longleftrightarrow3\).  Expanding the
definition (1.1) and collecting the allowed powers of \(X\) proves
\(2\Longleftrightarrow4\).  The elementary row-span criterion proves
\(2\Longleftrightarrow5\).  \(\square\)

No algebraic closure, saturation, genericity, or asymptotic argument is used.

### 2.2 Same-layer Popov--Forney specialization

For one complete weight-\(j\) layer, let

\[
 G=\gcd(L_E:E\in\mathcal S),
 \qquad L_{E_i}=GP_i,
 \qquad e=j-\deg G,
 \qquad D_0=K-j,
\tag{2.8}
\]

and define

\[
 \Theta_{D_0}:\bigoplus_i\mathbb F[X]_{<D_0}
 \longrightarrow\mathbb F[X]_{<e+D_0},
 \qquad (A_i)_i\longmapsto\sum_iA_iP_i.
\tag{2.9}
\]

Then \(\mathcal A(\mathcal S)=G\operatorname{im}\Theta_{D_0}\).  The
criterion (1.3) can be written without the extracted common core.  If
\(x\notin Z(G)\), put

\[
 d_{ik,x}
 =\frac{P_i}{(X-x)P_i'(x)}
  -\frac{P_k}{(X-x)P_k'(x)}.
\tag{2.10}
\]

If \(x\in Z(G)\), put

\[
 d_{ik,x}
 =\frac{P_i/P_i(x)-P_k/P_k(x)}{X-x}.
\tag{2.11}
\]

The numerator in (2.11) vanishes at \(x\), so the quotient is a polynomial.
Direct substitution into (2.5) gives in both cases

\[
 \boxed{
 \chi_{ik,x}|_{\mathscr L}\equiv0
 \quad\Longleftrightarrow\quad
 d_{ik,x}\in\operatorname{im}\Theta_{D_0}.}
\tag{2.12}
\]

Thus the predecessor formula

\[
 \dim\operatorname{coker}\Theta_{D_0}
 =\sum_r\max(0,\mu_r-D_0)
\tag{2.13}
\]

measures the exact residual space of normalized collision columns.

There is an equivalent bounded-syzygy test.  Define

\[
 \alpha_{i,x}=
 \begin{cases}
 P_i'(x)^{-1},&x\notin Z(G),\\
 P_i(x)^{-1},&x\in Z(G).
 \end{cases}
\tag{2.14}
\]

Then (2.12) holds if and only if there is a locator syzygy

\[
 B=(B_s)_s,
 \qquad \sum_sB_sP_s=0,
 \qquad \max_s\deg B_s\le D_0,
\tag{2.15}
\]

whose evaluation is

\[
 B(x)=-\alpha_{i,x}e_i+\alpha_{k,x}e_k.
\tag{2.16}
\]

Indeed, from \(d_{ik,x}=\sum_sA_sP_s\), take

\[
 B_s=(X-x)A_s-\alpha_{i,x}\mathbf1_{s=i}
                    +\alpha_{k,x}\mathbf1_{s=k}.
\tag{2.17}
\]

Conversely (2.16) makes each numerator
\(B_s+\alpha_{i,x}\mathbf1_{s=i}-\alpha_{k,x}\mathbf1_{s=k}\)
divisible by \(X-x\), recovering multipliers of degree less than \(D_0\).

Let \(S(X)\) be a row-reduced Popov basis of the locator syzygy module, and
let \(S_{\le D_0}\) be its rows of degree at most \(D_0\).  Predictable
degree gives

\[
 \mathcal R_x
 =\operatorname{rowspan}_{\mathbb F}S_{\le D_0}(x)
 \subseteq\mathbb F^{|\mathcal S|}
\tag{2.18}
\]

as exactly the evaluations at \(x\) of all syzygies satisfying (2.15).
Therefore

\[
 \boxed{
 \chi_{ik,x}|_{\mathscr L}\equiv0
 \quad\Longleftrightarrow\quad
 -\alpha_{i,x}e_i+\alpha_{k,x}e_k\in\mathcal R_x.}
\tag{2.19}
\]

If \(H_x\) generates \(\mathcal R_x^\perp\), this is equality of scaled
columns,

\[
 \alpha_{i,x}H_x[:,i]=\alpha_{k,x}H_x[:,k].
\tag{2.20}
\]

This is the exact column relation available to a global incidence theorem.
It is not equality of locator columns, canonical Popov--Padé columns, or
codewords.

## 3. Pairwise common-locator factor

The representing polynomial retains the actual pairwise common support.
Let

\[
 C=\gcd(L_{E_i},L_{E_k})=(X-x)C_x,
 \qquad L_{E_i}=CP_i,
 \qquad L_{E_k}=CP_k.
\tag{3.1}
\]

Then

\[
 L_{E_i}'(x)=C_x(x)P_i(x),
 \qquad
 L_{E_k}'(x)=C_x(x)P_k(x),
\]

and direct substitution gives

\[
 g_{ik,x}
 =C_x(x)C_x
  \bigl(P_k(x)P_i-P_i(x)P_k\bigr).
\tag{3.2}
\]

The parenthesized polynomial vanishes at \(X=x\); therefore

\[
 C\mid g_{ik,x}.
\tag{3.3}
\]

For distinct supports, \(g_{ik,x}\ne0\): otherwise the coprime monic
polynomials \(P_i,P_k\) would be scalar multiples and hence equal, forcing
\(E_i=E_k\).

Equation (3.3) types the collision polynomial correctly, but it does not pay
the component.  Pairwise common support can vary with \((i,k)\), and
membership in the global span (1.1) supplies neither a fixed common core nor
a disjoint first-match charge.

The actual collision locator of the coupled predecessor is

\[
 J_{ik}=\gcd(C,h_{ik}),
\]

where

\[
 c_k-c_i=L_{D\setminus(E_i\cup E_k)}h_{ik}.
\]

A forced collision at \(x\) gives \((X-x)\mid J_{ik}\), and the MDS
distance sharpens the pair-local overlap bound to

\[
 |E_i\cup E_k|\ge |D|-K+1+\deg J_{ik},
 \qquad
 |E_i\cap E_k|
 \le |E_i|+|E_k|-|D|+K-1-\deg J_{ik}.
\tag{3.4}
\]

In the deployed and toy regimes \(|D|=2K\), and one forced root gives the
specialization

\[
 |E_i\cup E_k|\ge K+2,
 \qquad
 |E_i\cap E_k|\le |E_i|+|E_k|-K-2.
\tag{3.4a}
\]

This one-unit gain is rigorous but pair-local.  It becomes a payment only if
a global collision graph supplies enough disjoint or commonly owned edges.

### 3.1 Exact graph-to-common-zero adapter

At a fixed coordinate \(x\), equality in (2.6), or equivalently scaled-column
equality (2.20), is an equivalence relation among the exact supports
containing \(x\).  Let \(\mathcal F\) be one equivalence class and suppose
\(x\in E_i\) for every \(i\in\mathcal F\).  Reconstruction gives, for every
\(\ell\in\mathscr L\),

\[
 c_i^\ell(x)=c_k^\ell(x)
 \qquad(i,k\in\mathcal F).
\tag{3.5}
\]

For the original exact functional the common error is nonzero.  Hence, after
fixing \(i_0\in\mathcal F\), evaluation at \(x\) vanishes on the direction
space

\[
 C'_{\mathcal F}
 =\operatorname{span}\{c_i-c_{i_0}:i\in\mathcal F\},
\tag{3.6}
\]

and \(x\) is a fixed mismatch for every member of the class.  If the same
family \(\mathcal F\) contains every \(x\in Z\) in every one of its supports
and lies in one quotient-column equality class at each such \(x\), then

\[
 Z\subseteq Z(C'_{\mathcal F})
\tag{3.7}
\]

and \(Z\) is a common fixed-mismatch block.  This is the strongest legal
bridge into the existing common-zero, rank-flat, and puncturing compilers.
Those compilers still require a complete first-match chart and their literal
row inequalities; one pair edge or one 46-key is not such a chart.

## 4. The maximum-rank branch

Suppose the selected family is exact for a nonzero original functional
\(\ell_0\).  Then

\[
 \mathcal A(\mathcal S)\subseteq\ker\ell_0,
 \qquad
 \dim\mathcal A(\mathcal S)\le K-1.
\tag{4.1}
\]

At maximum rank,

\[
 \dim\mathcal A(\mathcal S)=K-1,
\tag{4.2}
\]

so

\[
 \mathcal A(\mathcal S)=\ker\ell_0,
 \qquad
 \mathscr L(\mathcal S)=\mathbb F\ell_0.
\tag{4.3}
\]

Combining (1.3) and (4.3) yields

\[
 \chi_{ik,x}|_{\mathscr L}\equiv0
 \quad\Longleftrightarrow\quad
 \chi_{ik,x}(\ell_0)=0.
\tag{4.4}
\]

The predecessor reconstruction theorem identifies the right side with
equality of the two explaining codewords at the common error point \(x\).
Thus, in the maximum-rank branch, “identically forced” is exactly “an actual
collision already occurs.”  It adds no deformation rigidity and no named
owner.

For lower rank, Theorem 2.1 remains the complete criterion.  Proper forms
can be avoided by the predecessor hyperplane argument; forced forms are
precisely quotient-column equalities (2.6).  Any further semantic conclusion
must therefore be a new theorem about the split-locator span, the complete
list, or the active owner chronology.

## 5. Exhaustive \(GF(17)\) full-span regression

Use exactly the predecessor fixture

\[
 D=(0,1,\ldots,13),\quad K=7,\quad j=R=6,
\]

with moment functional

\[
 \ell\!\left(\sum_{r=0}^{6}q_rX^r\right)
 =4q_0+q_2+3q_3+4q_4+10q_5+8q_6
 \pmod {17}.
\tag{5.1}
\]

The standard-library verifier and independent Sage script exhaust all
\(\binom{14}{6}=3003\) supports and reproduce the complete exact layer of
137 distinct same-received-word codewords.  Since \(K-j=1\), the containment
generators are the 137 locator polynomials themselves.  Exact row reduction
gives

\[
 \operatorname{rank}\{L_E:E\in\mathcal E\}=6=K-1.
\tag{5.2}
\]

Hence their span is \(\ker\ell\), and the common functional space has
dimension one.  More strongly, the first 45 locators already have rank six;
therefore every 46-column marked family consisting of those anchors and one
extra support also spans \(\ker\ell\).  Identically forced has the same
maximum-rank meaning on each marked family, not only after all 137 supports
are pooled.

Across all \(\binom{137}{2}\) pairs, the exact census is

\[
\begin{array}{c|r}
\text{quantity}&\text{exact value}\\ \hline
\text{common-point incidences}&23813\\
\text{actual / identically forced collision incidences}&1326\\
\text{proper noncollision incidences}&22487\\
\text{distinct forced collision polynomials}&1219\\
\text{rank of their polynomial span}&4.
\end{array}
\tag{5.3}
\]

Every one of the 23813 instances satisfies (3.2)--(3.3).  Every actual
collision polynomial lies in the six-dimensional locator span; every
noncollision form is nonzero on the one-dimensional common functional space.

Freeze the same first 45 supports as anchors and the remaining 92 as marked
extras.  There are 597 anchor--extra forced collision incidences, which give
357 roots after deduplicating within each key.  Every key has a nonempty
forced-root union.  Nevertheless the exact packing and transversal values
remain

\[
 \nu=5,
 \qquad
 \tau=6.
\tag{5.4}
\]

Thus the predecessor's five pairwise-disjoint natural anchor--extra witness
unions and four minimum six-point transversals now lie entirely inside the
identically forced branch.

These computations are toy-scale exact controls.  They prove the stated
parameter-uniform implication false; they do not extrapolate to the deployed
field.

## 6. Consequence for the live M31 chronology

The active source-bound values remain

```text
U_paid     = 3730
U_Q        = null
U_list-int = null
U_ext      = null
U_new      = null
```

The previous diagnostic terminal was

```text
UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND
```

Theorem 2.1 replaces the unspecified word “forced” by an exact certificate,
but does not supply an owner.  Its local full-span subterminal is

```text
UNPAID_SPLIT_LOCATOR_HYPERPLANE_OWNER_REFUND
```

The missing local object is now explicit: a row-uniform bound or chronology-valid
owner/refund theorem for the complete family of split exact locators inside
one syndrome hyperplane.  In the maximum-rank branch this is not a smaller
problem hidden behind linear algebra; it is the global exact-layer counting
problem itself.

The exact occupancy interface makes the closing numerical target equally
explicit.  With

\[
 H=366969,
 \qquad
 3730+45H=16517335,
\]

the signed identity is

\[
 |\mathcal L|=16517335+\Xi_{46}.
\tag{6.1}
\]

Thus a joint chronology/refund theorem proving

\[
 \Xi_{46}\le259880
\tag{6.2}
\]

closes the exact budget.  Without a new cross-atom refund interface, the
apparently cleaner raw-tail theorem would be

\[
 T_{46}\le259880,
\tag{6.3}
\]

but it is already false on a proved deployed source.  The identity-prefix
construction in the actual-hyperplane activation packet gives one received
word whose complete boundary layer satisfies

\[
 M_R\ge1993678.
\tag{6.4}
\]

Consequently

\[
 T_{46}\ge M_R-45\ge1993633
 =259880+1733753.
\tag{6.5}
\]

The construction certifies only a subfamily of the complete list and does
not prove that the received word is over budget.  Its complete-list budget
status remains `UNKNOWN`.  However, its received polynomial is monic of
degree \(a\).  Subtracting any codeword of degree less than \(K<a\) leaves a
monic degree-\(a\) polynomial, so a codeword in the radius-\(R=n-a\) ball has
exactly \(a\) agreement roots.  The complete ball is therefore boundary-only:

\[
 N_{\rm low}=0,
 \qquad M_j=0\quad(j<R).
\tag{6.6}
\]

Since \(M_R\ge1993678>45\), its occupancy deficit is exactly

\[
 \Delta_{46}
 =3730+45(H-1)
 =16517290,
 \qquad
 \Xi_{46}=M_R-16517335.
\tag{6.7}
\]

Consequently (6.2) specializes on this center to

\[
 M_R\le16517335+259880=16777215=B^*.
\tag{6.8}
\]

Thus the signed target already contains the binding row-sharp \(Q\)
maximum-fiber problem; it is not a cheaper occupancy lemma.  The v4 grammar
has no negative-refund atom, so the deficits in (6.7) cannot simply be posted
as negative charges.  The source nevertheless rigorously refutes (6.3), any
row-uniform cap of (259880) on the raw excess, and any owner theorem that
silently discards the occupancy deficits.  The 45-anchor occupancy baseline
is not itself an owner.  The global terminal is therefore

```text
UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER
```

with `UNPAID_SPLIT_LOCATOR_HYPERPLANE_OWNER_REFUND` retained as the local
scaled-column subterminal.  The missing theorem must retain the signed
credits in \(\Xi_{46}\), pay the boundary \(Q\) maximum, and prove (6.2)
through the literal v4 chronology.

The open upstream common-core add-back packet #1033 is compatible with this
conclusion: it can make restoration multiplicity one after a shortened
component is paid, but it does not create the shortened payment or the
semantic owner.  The open rank-two-coloop packet #1034 is parallel to a
branch already eliminated in the predecessor stack.  Neither changes the
terminal above.

## 7. Route cut and next maximal theorem

The following parameter-uniform implication is false:

> complete exact same-weight layer for one received word, plus the canonical
> masked Padé bridge, exact escapes, MDS separation, rank-two coupled rows,
> nonzero pair minors, and at least one identically forced collision on every
> marked key, implies packing number at most four or a four-point transversal
> for the natural anchor--extra forced-collision-root unions.

The exhaustive fixture satisfies every premise and violates both
conclusions by (5.4).

This does not refute arbitrary grouping into four polynomials, a non-root
owner, an M31-specific domain theorem, or a chronology-valid refund.
Therefore another symbolic membership test, fixed-width rank computation,
or representative pair-minor factorization cannot close the row by itself.
A maximal successor theorem must do one of the following:

1. construct the missing target-field boundary-prefix map and route the
   identity-prefix family, with its exact attained-image normalization, into
   a certified \(U_Q\) cell;
2. partition the remaining complete split-locator hyperplane sections into
   named v4 owners with disjoint exact charges and the occupancy deficits
   refunded exactly once;
3. use cross-weight completeness to prove the signed bound
   \(\Xi_{46}\le259880\), while allowing a single raw boundary layer to have
   excess at least \(1993633\); or
4. directly prove the full list bound \(|\mathcal L_R(y)|\le B^*\) without
   replacing the signed identity by a raw-tail cap.

More concretely, the Popov form (2.20) suggests a complete-layer
forced-column incidence theorem: partition excess distinguished codewords by
their first repeated scaled-column class, then prove every complete class is
periodic/quotient-owned, fixed-union with nullity at most \(4980\), affine of
dimension at most six, common-zero/rank-flat/puncture-owned through
(3.7), or belongs to a primitive residual whose net \(\Xi_{46}\), after all
canonical missing-layer and missing-anchor credits, is at most \(259880\).
Until that global connectivity/concentration theorem is proved, the global
terminal remains `UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER` and the
primitive scaled-column subterminal is

```text
UNPAID_PRIMITIVE_FORCED_ESCAPE_COLUMN_COLLISION
```

The signed formulation is mandatory, not merely sharper: the actual
identity-prefix source rules out its raw-tail substitute.  It is M31-specific
and global and cannot be replaced by another local key calculation.

## 8. Replay and provenance

From the repository root:

```bash
python3 experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m31_full_span_forced_collision_route_cut_v1.sage
```

The manifest binds this note, both verifiers, the strict schema, the complete
canonical predecessor, the v4 target-source adapter, the proved deployed
actual-boundary source and its verifier/certificate, and the active Grande
Finale v4 ledger.  All finite decisions use exact arithmetic.

A targeted TheoremSearch query and a separate primary-source web search were
run only to test whether a known theorem already bounds this deterministic
split-locator hyperplane section.  The returned results concerned random or
generic RS evaluation sets, folded/linearized variants, ordinary Johnson
radius decoding, or unrelated hyperplane designs.  No result is imported as
a dependency, and no absence-of-literature claim is part of the proof.

There is no layer-cake, dyadic summability, Markov, Chebyshev, or moment
optimization argument in this packet.

## 9. Nonclaims

- The deployed M31 list row is not closed.
- Maximum locator-span rank is not proved for a deployed forbidden family.
- The \(GF(17)\) fixture is not a deployed counterexample.
- Annihilator membership is not a quotient, periodic, Johnson, extension, or
  other v4 owner.
- Pairwise common-locator divisibility is not a fixed global common core.
- No value is assigned to \(U_Q\), \(U_{\rm list-int}\), \(U_{\rm ext}\), or
  high \(U_{\rm new}\).
- The factor-one add-back claimed by open #1033 is not imported or banked.
- No stable-paper theorem, adjacent endpoint, official score, or Lean claim
  changes.
