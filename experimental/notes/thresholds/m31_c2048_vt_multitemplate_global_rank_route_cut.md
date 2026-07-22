---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Every c=2048 boundary error locator has one row-uniform degree-filtered coordinate slice in the rank-2048 F[T] module, and its primitive rank-one locator line is exactly its positional partial-template block. A failed guarded separator packet either contains a fixed-template module-rank-drop subfamily or uses at least ceil(|T|/17) distinct template lines. At the three live packet sizes this forces respectively 542164, 986676, or 986896 lines. For x in E minus F, pairwise escape absorption is equivalent to support half-distance at most w; a common-root escape is never pairwise absorbed. Canonical depth-32 H=1 source cosets are injectively separated when v+v'<=32. Current hypotheses pay neither the heavy-line nor the dispersed-line branch.
architecture: M31_C2048_VT_MULTITEMPLATE_GLOBAL_RANK_ROUTE_CUT_V1
partition_digest: CERTIFICATE_BOUND; active partition unchanged
atom_or_cell: HIGH_BOUNDARY_EXACT_CODEWORD / U_new
quantifier: Every cap-respecting family of deployed exact-boundary supports for which VT1 and VT2 fail, at every target-field union gate bound by the parent packet.
projection_and_unit: Distinct exact boundary supports, primitive F(T) locator lines, fixed positional partial-template blocks, and one-point escape columns.
claimed_bound: Exact global locator-coordinate normal form; exact rank-one-line/template equivalence; exact two-support escape criterion; canonical depth-32 source-coset injectivity; and live lower bounds 542164, 986676, 986896 on active template lines in the no-heavy-line branch.
status: PROVED GLOBAL STRATIFICATION / BOTH TERMINAL BRANCHES UNPAID
impact: MAXIMAL CURRENT-HYPOTHESIS ROUTE CUT / MISSING MULTITEMPLATE INCIDENCE LEMMA ISOLATED
falsifier: A boundary locator outside the printed global degree slice; two different positional templates on one primitive locator line; an x in E minus F whose escape behavior disagrees with d<=w; a pairwise-absorbed common-root escape; a canonical depth-32 source-coset collision with v+v'<=32; or a cap-respecting failed VT packet that has neither a heavy module-deficient block nor the stated number of active lines.
replay: Python exact arithmetic, block-load optimizer, source-floor/coset arithmetic, canonical certificate, and mutations; Sage exact rank-one factorization, pairwise escape, and canonical-source signature controls.
---

# M31 `c=2048` VT multitemplate global-rank route cut

## Status

```text
PROVED row-uniform global locator coordinate slice in F[T]^2048
PROVED primitive locator line = positional partial-template block
PROVED exact pairwise escape inverse-residue criterion
PROVED heavy-line / many-template-line dichotomy at every live VT gate
PROVED canonical depth-32 H=1 source-coset injectivity for v+v'<=32
UNPROVEN payment of fixed-template module-rank drop
UNPROVEN guarded incidence theorem for the dispersed template-line arrangement
ledger movement = 0
M31 LIST row closed = false
```

This packet attacks the upper-theorem side of the guarded separator in the
whole varying-template family.  It identifies the correct global rank
object and pushes the fixed-template module theorem as far as its quantifiers
permit.

The outcome is a sharp route cut.  A forbidden packet cannot be closed by
another fixed-template rank computation.  It either enters the already
named but unpaid fixed-template module-rank-drop branch, or disperses over
nearly one million distinct primitive locator lines.  No current theorem
controls the guarded incidence of those lines.  Consequently no atom moves.

## 1. The row-uniform global locator module

Keep the parent notation

\[
 c=2048,\quad n=2097152,\quad K=1048576,
 \quad R=981129=479c+137,
 \quad w=K-R=67447.
\tag{1.1}
\]

Let `F` contain the deployed base field and let the monic degree-`c` fold be
`phi`.  The free-module identity

\[
 \mathbb F[X]=\bigoplus_{a=0}^{c-1}X^a\mathbb F[\phi]
\tag{1.2}
\]

associates to every boundary error locator `L_E`, `deg L_E=R`, a unique
column

\[
 \lambda_E(T)=(\lambda_{E,0},\ldots,\lambda_{E,c-1})^t
\]

such that

\[
 L_E(X)=\sum_{a=0}^{c-1}X^a\lambda_{E,a}(\phi(X)).
\tag{1.3}
\]

Degree filtration in the monic triangular basis gives the single deployed
degree-filtered `F`-vector-space slice of the ambient free module
`F[T]^2048`

\[
 \boxed{
 \lambda_E\in
 \mathbb F[T]_{\le479}^{138}
 \oplus
 \mathbb F[T]_{\le478}^{1910}.}
\tag{1.4}
\]

The leading `X^R` term is common to all monic locators.  Therefore every
difference belongs to

\[
 \boxed{
 \lambda_E-\lambda_F\in
 \mathbb F[T]_{\le479}^{137}
 \oplus
 \mathbb F[T]_{\le478}^{1911},}
\tag{1.5}
\]

whose `F`-dimension is exactly

\[
 137\cdot480+1911\cdot479=981129=R.
\tag{1.6}
\]

These are the global varying-template locator coordinate slices inside the
rank-2,048 free module.  They are not `F[T]`-submodules: multiplication by
`T` can leave the printed degree filtration.  The ambient free-module rank
is different from
the translated quotient-message module in the fixed-template parent.
Conflating the two ranks is invalid.

## 2. Primitive locator lines are exactly template blocks

Call a nonempty locator family `S` a **primitive locator line** when

\[
 \operatorname{rank}_{\mathbb F(T)}
 \{\lambda_E:E\in\mathcal S\}=1.
\tag{2.1}
\]

### Theorem 2.1 (rank-one classification)

A family of distinct deployed boundary supports is a primitive locator line
if and only if there is one fixed set `P subset D`, containing no complete
`phi`-fiber, and distinct equal-size sets `B_E` of quotient labels such that

\[
 E=P\sqcup\phi^{-1}(B_E)
\tag{2.2}
\]

for every member.  Equivalently, the family lies in one positional partial-
template block `(u,v,P_0)`.  Different positional partial templates give
different primitive locator lines.

### Proof

Let `M` be the intersection of the one-dimensional `F(T)` span in (2.1)
with `F[T]^c`.  It is a saturated rank-one submodule of a free module over
the PID `F[T]`, hence

\[
 M=\mathbb F[T]a
\]

for a primitive column `a`, unique up to `F^*`.  Primitivity means that its
coordinates have gcd one.  Since every `lambda_E` lies in `M`, there are
polynomials `h_E(T)` with

\[
 \lambda_E=h_Ea.
\]

Under (1.2), write `A(X)` for `a`.  After a constant normalization all
members factor as

\[
 L_E(X)=A(X)h_E(\phi(X)),
\tag{2.3}
\]

with `A` and all `h_E` monic.  Because every `L_E` is the squarefree locator
of a subset of `D`, `A` is squarefree and split on `D`; call its root set
`P`.  Primitivity excludes a factor `T-b` from all coordinates of `a`, so
`A` contains no complete fiber.  The quotient `h_E(phi)` is also squarefree
and split on `D`; hence `h_E` has distinct roots `B_E` in the quotient-label
set and its roots in `D` are exactly the complete fibers over `B_E`.  All
`h_E` have the same degree because all `L_E` are monic of degree `R`.
This proves (2.2).

Conversely, (2.2) gives

\[
 L_E=L_PV_{B_E}(\phi),
\]

so all columns are polynomial multiples of the one primitive column for
`L_P`.  The complement of `P` in every partial fiber is the same positional
agreement template `P_0`; the complete disagreement fibers are the only
moving part.  Thus primitive locator lines and positional template blocks
coincide.  \(\square\)

This classification is structural.  It does not declare every such line to
be paid by `C1_QUOTIENT_REMAINDER`.  The predecessor proves that owner only
on its explicitly declared fixed-remainder subclass; a general partial
template can meet several fibers and can have degree greater than `c`.

## 3. The exact two-support escape test

For two boundary supports `E,F`, put

\[
 d=|E\setminus F|=|F\setminus E|,
\]

and factor

\[
 L_E=GA,\qquad L_F=GB,
\tag{3.1}
\]

where `G=L_(E intersection F)` and the coprime monic polynomials `A,B` have
degree `d`.  If `x in E minus F`, write `A=(X-x)A_x`.  Let `q_(E,F,x)` be
the unique residue of degree less than `d` satisfying

\[
 Bq_{E,F,x}\equiv A_x\pmod A.
\tag{3.2}
\]

### Theorem 3.1 (pairwise escape criterion)

For `x in E minus F`,

\[
 \boxed{
 W_{E\setminus\{x\}}\subseteq W_E+W_F
 \quad\Longleftrightarrow\quad
 \deg q_{E,F,x}<w
 \quad\Longleftrightarrow\quad d\le w.}
\tag{3.3}
\]

In fact, `deg q_(E,F,x)=d-1`.  If `x in E intersection F`, the pair never
absorbs that escape.

The residue itself has the closed form

\[
 \boxed{q_{E,F,x}=B(x)^{-1}A_x.}
\tag{3.4}
\]

### Proof

Modulo `W_E=GA F[X]_(<w)`, the one-point extension
`W_(E minus x)=GA_x F[X]_(<w+1)` is generated by the one class of `GA_x`:
for every `h`,

\[
 A_xh=h(x)A_x+A\,{h-h(x)\over X-x}.
\]

Thus absorption is equivalent to polynomials `p,q` of degree less than `w`
satisfying

\[
 Ap+Bq=A_x.
\tag{3.5}
\]

Reduction modulo `A` makes `q` congruent to (3.2).  If a representative of
degree less than `w` exists, taking the least-degree residue does so, and
the quotient `p` in (3.5) also has degree less than `w`.  This proves (3.3).
Indeed, the right side of (3.4) has degree `d-1`; at each root of `A_x` both
sides of (3.2) vanish, and at `x` equation (3.2) is exact.  Since `A` is
squarefree, interpolation on its `d` roots proves (3.4).  In particular the
residue has exactly the `d-1` distinct roots of `A_x` and degree `d-1`.
Finally, if
`x` is a common root, every member of `W_E+W_F` is divisible by `X-x`, while
the extra class in `W_(E minus x)/W_E` is not.  \(\square\)

The same factorization gives an exact pairwise-flat formula:

\[
 \boxed{
 \dim_{\mathbb F}(W_E\cap W_F)=\max(w-d,0).}
\tag{3.6}
\]

A common element is exactly a polynomial of degree less than `K=R+w`
divisible by `lcm(L_E,L_F)=GAB`, whose degree is `R+d`.  This proves (3.6).

Consequently every failed VT family has

\[
 |E\setminus F|\ge w+1=67448
\tag{3.7}
\]

for every distinct pair.  This necessary condition is sharp at the level of
the existing inputs: for actual codewords it is already the ordinary RS
distance consequence, because their common agreement set is a root set of
a nonzero polynomial of degree less than `K`.  Thus no two-support span in an
actual boundary list absorbs a one-point escape.  The close-pair lemma pays no
new mass; moreover (3.6) says all distinct support flats in an actual
boundary list intersect trivially.  Thus every useful flat dependency and
every VT2 mechanism is genuinely higher-order: it must use at least three
support flats.

## 4. The global heavy-line / dispersed-line dichotomy

Let `T` be a cap-respecting family of `m` boundary supports for which both
VT alternatives fail, and assume the target-field converse gate

\[
 q>mR.
\tag{4.1}
\]

The parent guarded-separator theorem realizes all members around one actual
target-field received word.  Partition `T` into its primitive locator lines,
equivalently its positional template blocks by Theorem 2.1.  For a block of
profile `(u,v)`, use the parent's exact threshold `Lambda^SD_(u,v)<=17`.

### Theorem 4.1 (maximal current-hypothesis dichotomy)

Exactly one of the following conclusions is available from the current
fixed-template theorem.

1. **Heavy line.**  Some block has at least
   `Lambda^SD_(u,v)+1` members.  That block contains a translated quotient-
   message difference span whose `F(T)` rank is smaller than its `F`-affine
   dimension.  Its current diagnostic is

   ```text
   UNPAID_FIXED_TEMPLATE_MODULE_RANK_DROP.
   ```

2. **Dispersed lines.**  Every block has at most its conditional threshold,
   and the number `tau(T)` of distinct primitive locator lines satisfies

   \[
   \boxed{\tau(\mathcal T)\ge\left\lceil{m\over17}\right\rceil.}
   \tag{4.2}
   \]

### Proof

The target-field converse supplies the common received word needed by the
fixed-template parent.  Apply that theorem to every block.  If one block is
heavy, conclusion 1 follows.  Otherwise every line carries at most 17
members, so summing line loads gives (4.2).  \(\square\)

At the three live packet sizes, (4.2) is

```text
packet size  9,216,782  => at least 542,164 template lines
packet size 16,773,486  => at least 986,676 template lines
packet size 16,777,216  => at least 986,896 template lines
```

The last two packet sizes are respectively `(B_star-U_paid)+1` and
`B_star+1`.

## 5. Canonical depth-32 source-coset separation

The preceding dichotomy does not permit floors constructed around different
received words to be added.  On the canonical `H=1` source stratum, this
non-summability can be made exact.

For a source profile `(u,v)`, put

\[
 h=u+v+1,\qquad r=1911+2048v,\qquad f=544-v.
\tag{5.1}
\]

Here, to avoid a collision with Theorem 2.1, write `P_ag` for the **partial
agreement template**: it has size `r` and meets every one of its `h` partial
fibers in between 1 and 2,047 points.  Expand

\[
 L_{P_{\rm ag}}(X)=
 \sum_{a=0}^{2047}X^a\Lambda_{P_{\rm ag},a}(\phi(X)).
\tag{5.2}
\]

The column `Lambda_(P_ag)(T)` has degree `v`; its component `a=1911` is
monic of degree `v`.  Define the reciprocal column

\[
 A_{P_{\rm ag}}(z)=z^v\Lambda_{P_{\rm ag}}(z^{-1}),
\tag{5.3}
\]

and, for `eta=(eta_1,...,eta_32) in F^32`, put

\[
 B_\eta(T)=T^f+\eta_1T^{f-1}+\cdots+\eta_{32}T^{f-32},
\]
\[
 J_\eta(z)=1+\eta_1z+\cdots+\eta_{32}z^{32},
\qquad
 U_{P_{\rm ag},\eta}=L_{P_{\rm ag}}B_\eta(\phi).
\tag{5.4}
\]

### Theorem 5.1 (canonical source-coset injectivity)

Assume `v,v'<=511`, equivalently `f,f'>=33`, so the displayed depth-32
source formula belongs to the cancellation regime rather than the separate
full-coefficient edge.  For nonzero `lambda,lambda' in F`, the projectively scaled canonical source
centers define the same received-word coset modulo `F[X]_(<K)` if and only if

\[
 \lambda A_{P_{\rm ag}}(z)J_\eta(z)
 \equiv
 \lambda' A_{P'_{\rm ag}}(z)J_{\eta'}(z)
 \pmod {z^{33}}
\tag{5.5}
\]

componentwise.  If

\[
 v+v'\le32,
\tag{5.6}
\]

then (5.5) holds only when

\[
 P_{\rm ag}=P'_{\rm ag},\qquad
 \eta=\eta',\qquad
 \lambda=\lambda'.
\tag{5.7}
\]

### Proof

The criterion (5.5) has the following direct off-by-one derivation.  Since
`K=512c` and `v+f=544`, two scaled centers differ by a polynomial of degree
less than `K` if and only if every free-module component has `T`-degree at
most 511.  Equivalently,

\[
 z^{544}\left(
 \lambda\Lambda_{P_{\rm ag}}(z^{-1})B_\eta(z^{-1})
 -\lambda'\Lambda_{P'_{\rm ag}}(z^{-1})B_{\eta'}(z^{-1})
 \right)
\]

is componentwise divisible by `z^(544-511)=z^33`.  Using (5.3)--(5.4) gives
exactly (5.5), with no coefficient beyond depth 32 silently discarded.
Wedge that
congruence with `A_(P'_ag)`.  Since `J_eta(0)=1` and `lambda` is nonzero,
`J_eta` and `lambda` are units modulo `z^33`; hence

\[
 A_{P_{\rm ag}}\wedge A_{P'_{\rm ag}}
 \equiv0\pmod {z^{33}}.
\tag{5.8}
\]

Every component of this wedge has degree at most `v+v'`.  Under (5.6), a
polynomial of degree at most 32 divisible by `z^33` is zero.  Thus the two
columns are proportional over `F(z)`, equivalently

\[
 {L_{P_{\rm ag}}\over L_{P'_{\rm ag}}}\in\mathbb F(\phi).
\tag{5.9}
\]

The divisor of a rational function of `phi` is constant on each complete
simple domain fiber.  The divisor of the left side of (5.9) is `+1` on
`P_ag minus P'_ag`, `-1` on the reverse difference, and zero elsewhere.
Both templates are strictly partial on every partial fiber, so fiberwise
constancy forces both differences to be empty.  Hence the templates agree.
The `a=1911` component of each `A_(P_ag)` has constant coefficient one, so
it is itself a unit modulo `z^33`.  Together with the monic normalization of
(5.2), the constant terms `J_eta(0)=J_eta'(0)=1`, and (5.5), this forces
equality of the scalings and all 32 coefficients.
\(\square\)

For the originally certified base-field source blocks, `eta` lies in the
subspace `F_p^32`; the target-field statement above allows `F^32`.

The five largest separately realized source floors are

```text
(u,v)=(0,0): 6,796,405
(u,v)=(0,1): 3,614,120
(u,v)=(1,0): 3,182,286
(u,v)=(0,2): 1,920,222
(u,v)=(1,1): 1,693,898
```

Every pair has `v+v'<=4`, so Theorem 5.1 makes their canonical source cosets
distinct.  Their formal sum is

\[
 17,206,931=B_*+429,716,
\tag{5.10}
\]

but it is **not** a list around one received word and cannot be booked.  The
top three already have distinct cosets and sum to

\[
 13,592,811=B_*-3,184,404.
\tag{5.11}
\]

There is one exact fixed-cofactor extension.  Multiplying every source
identity by one fixed polynomial `H` with no roots on `D` preserves exact
supports.  The depth-32 source codeword degree is at most `K-137`, so
`deg H<=136` preserves both the code degree and the separation theorem.  At
`deg H=137`, the current uniform degree proof at depth 32 reaches degree `K`
and must refine to depth 33; an individual member could have accidental extra
cancellation.  Separation for one fixed nonzero `H` is immediate: if
`H(lambda U-lambda' U')` has degree less than `K`, then the integral-domain
degree law forces `lambda U-lambda' U'` itself to have degree less than `K`,
so Theorem 5.1 applies.  Root-freeness of `H` is used only to preserve the
exact support.  For each of the top five profiles,

\[
 \left\lceil{\binom{1023-u-v}{544-v}\over p^{33}}\right\rceil=1.
\tag{5.12}
\]

Thus the existing depth-33 pigeonhole certificate supplies only one member
for each top-five profile; it is a lower floor, not an upper bound on the
attained depth-33 bucket.  Larger attained depth-33 buckets are not excluded.
Cofactors with roots on the evaluation domain, support-dependent cofactors
`H_E`, and the arbitrary-word attained-cofactor family remain explicitly
open.

## 6. Why the present hypotheses stop here

The block caps together with the fixed-template threshold/module implications
alone do not exclude either abstract load shape in Theorem 4.1.

* At profile `(0,0)`, the proved fixed-template cap is the 255-digit integer
  printed by the predecessor, vastly larger than every live packet size,
  while `Lambda^SD_(0,0)=17`.  Thus one heavy line is not excluded; the
  module theorem only routes it to its unpaid rank-drop terminal.  The
  separately realized 6,796,405-member fixed-remainder source confirms that
  large rank-one locator-line VT failures actually occur, although that
  floor remains below `B_star`.
* The number of positional `(0,0)` templates alone is at least

  \[
  1024\binom{2048}{137},
  \tag{6.1}
  \]

  a 220-digit integer.  Hence the abstract load vector with one member on
  each of `m` lines satisfies every current block cap and every conditional
  threshold at all three live sizes.  This is a countermodel only for those
  blockwise inequalities.  It does not establish the pairwise-distance
  condition, the VT incidence conditions, or occurrence around one received
  word.

Locator rank does not repair the gap by itself.  One primitive locator line
is exactly the heavy fixed-template branch.  Multiple lines may lie in a
low-dimensional `F(T)` span, and neither the parent determinant-valuation
bound nor the fixed-template minimal-sublist theorem controls their guarded
one-point escapes.  Conversely, the exact two-template construction in the
fixed-template predecessor gives an actual two-line list, so merely leaving
rank one does not force VT1 or VT2.

The surviving exact primitive is therefore

```text
UNPAID_VT_MULTITEMPLATE_GUARDED_LINE_INCIDENCE.
```

It is a diagnostic, not a new first-match owner.  A closing successor must
prove a **single row-uniform guarded line-arrangement theorem**: for every
failed-VT packet in the dispersed branch, the simultaneous degree-bounded
relations among at least the number of lines in (4.2) must either satisfy an
explicit genuinely higher-order absorption
`W_(E minus x) subset sum_(F in T) W_F`, enter a chronology-valid paid owner,
or fit an exact target-field root-union budget.  The pairwise criterion in
Section 3 cannot supply that absorption.  Another theorem confined to one
template line cannot close this branch.

## 7. Scope and nonclaims

No value of `U_paid`, `U_Q`, `U_list-int`, `U_ext`, or `U_new` changes.
Neither branch of Theorem 4.1 is paid.  The active boundary subterminal
remains `UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER`, the parent VT diagnostic
remains open, and the active global M1 terminal remains
`UNPAID_CROSS_WEIGHT_EXCESS_DEFICIT_Q_OWNER`.

The abstract load shapes in Section 6 prove insufficiency only of the present
block-cap and fixed-template threshold implications; they are not deployed
received-word counterexamples.  The small-field Sage controls replay only
the exact algebra in Theorems 2.1, 3.1, and 5.1.  They do not establish
asymptotic or deployed VT incidence.

There is no layer-cake, moment, Markov, probabilistic Chebyshev, or dyadic
argument.  `Chebyshev` refers only to the deployed fold.
