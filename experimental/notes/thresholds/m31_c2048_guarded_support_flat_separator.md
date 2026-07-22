---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The complete c=2048 varying-template exact-boundary sum is exactly one guarded incidence of target-field syndrome functionals with shortened dual flats. After imposing the proved fixed-template block caps, a uniform U bound is equivalent at every live budget scale to the separator VT(U): every U+1 support family either spans the full dual or absorbs one declared one-point escape. Failure of VT(U) constructs an actual target-field received word with all U+1 exact supports.
architecture: M31_C2048_GUARDED_SUPPORT_FLAT_SEPARATOR_V1
partition_digest: CERTIFICATE_BOUND; active partition unchanged
atom_or_cell: HIGH_BOUNDARY_EXACT_CODEWORD / U_new
quantifier: Every target-field boundary error support, every profile and exact partial template, and every support family through the full forbidden budget scale.
projection_and_unit: One target-field syndrome functional, shortened weighted-GRS flats W_E, all one-point extensions W_(E minus x), and fixed-template block loads.
claimed_bound: Exact forward-and-converse VT(U) compiler, exact target-field union gates, and exact shifted-locator rank interface. VT itself remains unproved.
status: PROVED EXACT GLOBAL INTERFACE AND CONVERSE / VT SEPARATOR OPEN
impact: VARYING-TEMPLATE COMPOSITION ROUTE CUT / ACTUAL-SOURCE CONVERSE
falsifier: A listed boundary codeword not represented by exactly one guarded support flat; a failed VT family that cannot be realized by a target-field syndrome despite q greater than the guard count; or a mismatch in the shifted-locator rank/escape test.
replay: Python exact constants, source closure, canonical certificate, and mutations; Sage exact MDS support-flat, annihilator, union-avoidance, and matrix fixtures.
---

# M31 `c=2048` guarded support-flat separator

## Status

```text
PROVED exact varying-template syndrome reindexing
PROVED VT(U) => uniform boundary support bound U
PROVED failure of VT(U) => actual target-field source when q>(U+1)R
PROVED exact shifted-locator rank and escape compiler
UNPROVEN VT(U) on the complete deployed support family
ledger movement = 0
global M1 terminal and active partition unchanged
M31 LIST row closed = false
```

This packet performs the global composition that the fixed-template quotient
and module-rank packets could not perform.  The datum common to different
partial templates is one target-field syndrome functional, not a separately
translated quotient received word and not one cofactor-prefix target.  The
old profile/template/cofactor sum is exactly one punctured incidence of that
functional with shortened dual flats.

The result freezes the maximal successor theorem `VT(U)` and proves its
converse at every live budget scale.  It does not prove `VT(U)`.  Consequently
it moves no atom.  The packet-local `c=2048` boundary subterminal remains
`UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`, while the active global M1 terminal
remains `UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER`.

### Provenance and novelty boundary

The exact support-flat/escape theorem and shifted-locator model are reused
from `m31_shortened_flat_hyperplane_wall.md`.  Two-support and selected
four-face annihilator/escape arguments, together with the 15/16 rank gate,
already appear in `m31_chebyshev_global_separator.md` and
`m31_sidon_three_fibre_escape_compiler.md`.  The new content here is the
arbitrary cap-respecting family theorem over `F_(p^4)`, its equivalence to a
uniform exact-boundary cap at the live target-field gates, the composition
across all partial templates, and the precise module-rank stratification
inherited from `m31_c2048_fixed_template_module_rank_route_cut.md`.  The
block caps and exact template partition come from
`m31_c2048_fixed_template_interleaved_quotient_route_cut.md`.  This is
boundary-only and does not
discharge the interior/whole-ball contract in
`m31_whole_ball_source_separator_compiler.md`.

## 1. Target-field support flats

Put

\[
 p=2^{31}-1,\qquad \mathbb F=\mathbb F_{p^4},\qquad
 q=|\mathbb F|=p^4,
\]
\[
 n=2^{21},\qquad K=2^{20},\qquad A=1116023,
\]
\[
 R=n-A=981129,\qquad w=K-R=67447.
\tag{1.1}
\]

Let `C=RS_F(D,K)` on the deployed base-field evaluation domain, now with
coefficients in `F`, and let `V=C^perp`.  Since `n=2K`,

\[
 \dim_{\mathbb F}V=K=1048576.
\]

For a boundary error support `E subset D`, `|E|=R`, define

\[
 W_E=\{v\in V:\operatorname{supp}(v)\subseteq D\setminus E\}.
\tag{1.2}
\]

The MDS shortening formula gives

\[
 \dim W_E=w,
 \qquad
 \dim W_{E\setminus\{x\}}=w+1
 \quad(x\in E),
\tag{1.3}
\]

and `W_E` is a codimension-one subspace of every one-point extension
`W_(E minus x)`.

For a received word `y`, write

\[
 \varphi_y(v)=\langle y,v\rangle\in V^*.
\tag{1.4}
\]

The exact shortened-flat theorem says that `E` is the exact error support of
one listed codeword if and only if

\[
 \varphi_y\in A_E^\circ,
\qquad
 A_E^\circ=\operatorname{Ann}(W_E)
 \setminus\bigcup_{x\in E}
       \operatorname{Ann}(W_{E\setminus\{x\}}).
\tag{1.5}
\]

The representation is duplicate-free because `R<d(C)=K+1`: an error
supported in `E` with a fixed syndrome is unique.  The escape punctures in
(1.5) are essential; containment alone would count errors whose actual
support is smaller.

The syndrome map

\[
 \mathbb F^D\longrightarrow V^*,\qquad y\longmapsto\varphi_y,
\tag{1.6}
\]

is surjective.  Its kernel is `V^perp=C`, hence its rank is
`n-K=dim V^*`.  This is pure linear algebra and remains true after base
extension from `F_p` to `F_(p^4)`.

## 2. Exact composition across partial templates

Let `Omega_(u,v)` be the boundary error supports whose agreement complements
have occupancy profile `(u,v)`.  For one exact partial agreement template
`P_0`, let `Omega_(u,v,P_0)` be its support block.  The predecessor's
fixed-template theorem gives

\[
 c_{u,v}=
 \begin{cases}
 1,&v\ge512,\\[1mm]
 \left\lfloor
 {\binom{1023-u-v}{512-v}\over\binom{544-v}{512-v}}
 \right\rfloor,&v\le511.
 \end{cases}
\tag{2.1}
\]

For every received word,

\[
 \#\{E\in\Omega_{u,v,P_0}:\varphi_y\in A_E^\circ\}
 \le c_{u,v}.
\tag{2.2}
\]

The complete exact profile count is therefore

\[
 M_{u,v}(y)=
 \sum_{E\in\Omega_{u,v}}
 1[\varphi_y\in A_E^\circ].
\tag{2.3}
\]

Equation (2.3) is the exact composition of the predecessor's disjoint sum
over profile, `P_0`, and attained normalized cofactor jet.  Indeed, the
profile and exact partial template are deterministic functions of `E`.  Once
`(y,E)` is fixed, the shortened-flat theorem gives the unique error and hence
the unique codeword.  Let `Y` be the degree-less-than-`n` interpolation
polynomial of `y`, let `C` be that codeword polynomial, and put
`S=D minus E`.  Then

\[
 Y-C=L_SH
\tag{2.4}
\]

fixes `H` and its normalized cofactor jet.  Conversely every old summand has
one exact support `E`.  Thus (2.3) reindexes every old summand and discards no
multiplicity.  Different templates still have different `L_(P_0)` factors,
but they now meet through the one shared syndrome functional `varphi_y`.

The same formulation applies to the union `Omega_boundary` of all boundary
profiles.  A frozen residual may be substituted only when it is a fixed
subset of the support universe, its first-match designation depends only on
the exact support/source key and survives replacement of the received word
by the converse construction, and every retained support block keeps its
proved cap.  A predicate depending on additional word or witness data is not
automatically a converse-stable support residual.

## 3. The maximal separator

For an integer `U`, define `VT(U)` as follows.

> For every set \(\mathcal T\subset\Omega_{\rm boundary}\) with
> \(|\mathcal T|=U+1\) and
> \[
> |\mathcal T\cap\Omega_{u,v,P_0}|\le c_{u,v}
> \tag{3.1}
> \]
> for every profile/template block, put
> \[
> X_{\mathcal T}=\sum_{E\in\mathcal T}W_E\subseteq V.
> \tag{3.2}
> \]
> Then either
> \[
> \boxed{X_{\mathcal T}=V}
> \tag{VT1}
> \]
> or
> \[
> \boxed{\exists E\in\mathcal T,\ x\in E:
> W_{E\setminus\{x\}}\subseteq X_{\mathcal T}.}
> \tag{VT2}
> \]

The profile-restricted version uses
\(\mathcal T\subset\Omega_{u,v}\) and the same block loads.

### Theorem 3.1 (forward implication)

If `VT(U)` holds, every target-field received word has at most `U` exact
boundary codewords in the declared support residual.

### Proof

Suppose `U+1` distinct exact supports form \(\mathcal T\).  The block-load conditions
(3.1) follow from (2.2).  By (1.5), `varphi_y` annihilates every `W_E`, so

\[
 X_{\mathcal T}\subseteq\ker\varphi_y.
\]

The syndrome is nonzero: zero syndrome means `y in C`, and
`R<d(C)` excludes a nonempty exact boundary error support.  Hence its kernel
is proper and (VT1) fails.  For every `E,x`, exactness gives
`W_(E minus x) not subset ker(varphi_y)`, so it cannot be contained in
\(X_{\mathcal T}\); (VT2) also fails.  This contradicts `VT(U)`.  \(\square\)

## 4. Failure of `VT` is an actual source

The converse is what makes (VT) a sharp theorem target rather than another
one-way rank diagnostic.

### Theorem 4.1 (target-field union-avoidance converse)

Let \(\mathcal T\) be any `U+1` distinct boundary supports for which neither
(VT1) nor (VT2) holds.  If

\[
 q>(U+1)R,
\tag{4.1}
\]

then one actual target-field received word has every member of \(\mathcal T\) as an
exact boundary error support.  In particular, failure of `VT(U)` is an
actual list source.

### Proof

Put

\[
 L=\operatorname{Ann}(X_{\mathcal T})\subseteq V^*.
\]

Failure of (VT1) gives `dim L>=1`.  For each `(E,x)`, define

\[
 B_{E,x}=
 L\cap\operatorname{Ann}(W_{E\setminus\{x\}})
 =\operatorname{Ann}(X_{\mathcal T}+W_{E\setminus\{x\}}).
\tag{4.2}
\]

Because \(W_E\subset X_{\mathcal T}\) and
\(W_{E\setminus\{x\}}/W_E\) is one-dimensional,
failure of (VT2) makes `B_(E,x)` a proper hyperplane of `L`.  There are at
most `(U+1)R` such hyperplanes.  If `d=dim L`, their union has at most

\[
 (U+1)R\,q^{d-1}<q^d=|L|
\]

points.  Choose `varphi` in `L` outside the union.  It annihilates every
`W_E` and no one-point extension.  It is nonzero because zero lies in every
`B_(E,x)`.  By (1.6), `varphi=varphi_y` for an actual target-field received
word `y`.  Equation (1.5) makes every \(E\in\mathcal T\) an exact support, and support
uniqueness gives distinct codewords.  \(\square\)

The converse does not require (3.1).  Indeed, if a family violates a proved
fixed-template cap, (4.1) already forces one VT alternative; otherwise the
constructed word would contradict (2.2).  Restricting the new theorem to
cap-respecting loads therefore loses no genuine hard case.

### Corollary 4.2 (exact equivalence at the target-field gate)

For \(\Omega_{\rm boundary}\), and for any fixed converse-stable residual
satisfying the conditions in Section 2, if `q>(U+1)R`, then `VT(U)` holds if
and only if every target-field received word has at most `U` exact boundary
codewords in that support universe.  The forward direction is Theorem 3.1.  If `VT(U)` fails, its
definition supplies a cap-respecting family of `U+1` supports for which both
alternatives fail, and Theorem 4.1 realizes them around one received word.

### Corollary 4.3 (module-rank stratification of a VT failure)

Assume (4.1), and let \(\mathcal T\) be a cap-respecting family for which both VT
alternatives fail.  Fix a block `(u,v,P_0)` with `v<=511`.  If

\[
 |\mathcal T\cap\Omega_{u,v,P_0}|
 \ge \Lambda^{SD}_{u,v}+1,
\tag{4.3}
\]

then this block contains a subfamily of size

\[
 2\le m\le\Lambda^{SD}_{u,v}+1
\]

whose translated quotient-message difference span is deficient over
`F(T)`, exactly as in the parent module-rank theorem.  Indeed, Theorem 4.1
first realizes all supports in \(\mathcal T\) around one target-field received word;
the parent Theorem 3.1 then applies to the fixed-template block.

This quotient-message module span is not the shortened-dual support span
\(X_{\mathcal T}\).  Corollary 4.3 stratifies a failed VT family but does not prove either
VT alternative and does not assign the deficient component to an owner.

### Deployed union gates

The target field has

\[
 q=21267647892944572736998860269687930881.
\]

All relevant guard counts are far smaller:

```text
U= 9,216,781: (U+1)R =  9,042,852,106,878
U=16,773,485: (U+1)R = 16,456,953,545,694
U=16,777,215: (U+1)R = 16,460,613,156,864
```

The first value is the conditional combined face/carrier target.  The second
is `B_star-U_paid` and would directly pay the complete boundary after the
proved low cell.  The third covers a full forbidden packet of size
`B_star+1`.  These union arguments use `p^4`; the analogous statement does
not follow over `F_p`, where the number of guards is larger than the field.

Scaling a nonzero syndrome does not change containment or escape, so the
incidence is projective.  Zero syndrome is handled separately as above.

## 5. Exact shifted-locator matrix gate

Use the standard weighted-GRS realization

\[
 V=\{(u_zg(z))_{z\in D}:\deg g<K\}.
\]

For

\[
 L_E(X)=\prod_{x\in E}(X-x),
\]

one has

\[
 W_E=L_E\mathbb F[X]_{<w}
 =\operatorname{span}_{\mathbb F}
 \{X^rL_E:0\le r<w\}
\tag{5.1}
\]

in coefficient coordinates of length `K`.  Let \(M_{\mathcal T}\) be the
matrix obtained by stacking these shifted-locator rows for all
\(E\in\mathcal T\).  Then

\[
 \operatorname{row}(M_{\mathcal T})=X_{\mathcal T},
 \qquad
 \dim\operatorname{Ann}(X_{\mathcal T})
 =K-\operatorname{rank}M_{\mathcal T}.
\tag{5.2}
\]

Call the packet containment-compatible when this annihilator is nonzero.

For an escape, append the `w+1` shifted rows of

\[
 L_{E\setminus\{x\}}={L_E\over X-x}.
\]

Since `W_E` is already present, the rank rises by either zero or one.  It
rises by zero exactly when the escape is absorbed as in (VT2).

For fifteen supports,

\[
 15w=1011705<K,
 \qquad K-15w=36871,
\tag{5.3}
\]

so a nonzero common-syndrome space is automatic.  If no one-point escape is
absorbed by the support span, every escape cuts a proper hyperplane in that
common annihilator; at the deployed field `q>15R`, so Theorem 4.1 then avoids
their union.  Thus (VT2), not containment rank, is the sole obstruction for
fifteen supports and still has to be checked.
Sixteen is the first containment-rank gate:

\[
 16w=1079152,
 \qquad 16w-K=30576.
\tag{5.4}
\]

A compatible 16-packet has rank at most `K-1`, hence its stacked matrix has
left-kernel, or row-syzygy, dimension at least

\[
 16w-(K-1)=30577.
\tag{5.5}
\]

Thus a standalone 16-column computation matters only if it classifies a
component of the complete `VT` system and preserves all support mass and
one-point escapes.

## 6. Chronology and exact remaining theorem

The packet-local `c=2048` boundary subterminal remains

```text
UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER.
```

The active global M1 terminal remains

```text
UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER.
```

This packet supplies its exact whole-family diagnostic:

```text
UNPROVEN_GUARDED_SUPPORT_FLAT_SEPARATOR_VT.
```

Neither string is a new first-match owner.  No value of `U_paid`, `U_Q`,
`U_list-int`, `U_ext`, or `U_new` moves.

A proof of whole-boundary `VT(16,773,485)` would give a direct numerical
`HIGH_BOUNDARY_EXACT_CODEWORD`/`U_new` payment after the proved
`U_paid<=3730`.  It would still leave high interior, `U_list-int`, and
`U_ext` open.  The smaller `9,216,781` target is usable only after its
conditional light-bi-deep/face/carrier split becomes a fixed,
first-match-disjoint source selection.

The syndrome bridge does not pay `U_Q`.  One syndrome can contain multiple
locator-prefix targets, as the integrated exact `F_7` regression proves.
Booking (2.3) to `U_Q` requires a further arbitrary-syndrome-to-prefix or
effective-image theorem.

The next mathematical attack is the theorem `VT(U)` itself, stratified by
the `F(T)`-affine rank exposed in the parent module-rank packet.  Rank-one
components include the known fixed-prefix sources; full-module-rank minimal
bad subfamilies have already been excluded above their conditional
thresholds.  Every surviving rank-deficient component must be routed to a
named paid owner, force (VT2), or remain an explicit primitive component.

## 7. Scope and nonclaims

The forward implication, converse, base-extension, and matrix compiler are
exact theorems.  `VT(U)` over the complete deployed support family is open.
The small-field Sage fixtures test the algebraic interfaces; they are not an
exhaustive deployed proof.  No source floors from different profiles are
claimed simultaneously.

There is no layer-cake, moment, Markov, probabilistic Chebyshev, or dyadic
argument.  `Chebyshev` refers only to the deployed fold.  No stable paper,
official endpoint, score, or prize claim changes.
