---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The complete deployed quartic-field list admits a source-bound low/boundary/interior exact-support partition; low weight contributes at most 3730 codewords, and any forbidden list forces at least 259881 target-field marked rank-46 diagnostic keys, each with a three-row coupled locator-numerator kernel frame of combined degree at most 62295. The boundary/interior codeword residual is exhaustive and remains unpaid.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: U_paid=LOW_EXACT_WEIGHT_PACKING; U_new=HIGH_BOUNDARY_EXACT_CODEWORD or HIGH_INTERIOR_EXACT_CODEWORD; U_Q, U_list-int, and U_ext remain null; UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL is a forced diagnostic terminal
quantifier: Every received word over F_(p^4); the marked-key consequence is conditional only on list size at least B_star+1.
projection_and_unit: Distinct agreeing codewords per received word; marked keys retain one distinguished codeword each and are not counted as slopes or raw supports.
claimed_bound: U_paid(low exact weights through 614160)<=3730 directly on the quartic target; every forbidden list forces at least 259881 target-field marked rank-46 keys; each key has coupled partial-degree bounds 20765, 41530, and 62295<67447; all other atom values remain null.
status: PROVED
impact: ROUTE_CUT
falsifier: A prime-field-only step in the direct field-generic lift, a failure of exact support uniqueness, the integer packing/occupancy identity, the coupled joint-index theorem on a marked key, or the five-atom/codeword-unit contract.
replay: Python normal and optimized checks, independent Python replay, semantic mutations, predecessor arithmetic replays, and Sage finite-field controls.
---

# M31 v4 LIST source adapter and global coupled residual

## Status

**PROVED SOURCE TRANSPORT / PROVED GLOBAL EXACT-SUPPORT EXHAUSTION / PROVED
COUPLED RANK-THREE FRAME ON EVERY MARKED RESIDUAL KEY / ONE SOURCE-BOUND
LOW-WEIGHT PAYMENT / EXPLICIT UNPAID GLOBAL RESIDUAL / ROW OPEN.**

This packet performs the architecture step that the local 16-column packet
could not perform.  It starts with an arbitrary hypothetical violation of the
deployed Mersenne-31 list inequality, lifts the exact-support and coupled
source theorems directly to the deployed quartic field, retains the complete
target-list histogram, and applies the mass-preserving rank-46 source compiler
before doing any local algebra.  Scalar descent is retained only as an
independent threshold cross-check.

The legal non-oracular partition of the complete target-field list
is global and codeword-exhaustive: low exact weights enter one fixed
algebraic predicate, while every remaining codeword enters a fixed boundary
or interior residual predicate.  Separately, every forbidden
list produces at least `259881` distinct marked source keys.  The
distinguished codeword in each key is retained, so the diagnostic unit remains
codewords per received word.  The coupled Padé--Forney theorem then gives a
rank-three locator--numerator kernel frame on **every** marked key, not on one
sampled packet.

The marked keys are not cells and are not charged: selecting the first 45
members of a computed list is forbidden by the v4 non-oracular payment rule.
They are consequences of an over-budget value of the legal residual.  The
result does not close the row.  No current theorem coalesces the marked
keys into at most four common root unions, routes all of them to disjoint v4
owners with refunds, or eliminates their primitive component.  The exact
terminal is

```text
UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL.
```

That terminal is a v4 adapter residual, not a claim that an actual forbidden
list exists.

## 1. Exact deployed contract

Put

```text
p       = 2^31-1           = 2,147,483,647,
n       = 2^21             = 2,097,152,
K       = 2^20             = 1,048,576,
a       = 1,116,023,
R       = n-a              = 981,129,
w       = a-K              = 67,447,
B*      = floor(p^4/2^100) = 16,777,215,
L       = B*+1             = 16,777,216.
```

The deployed list code is

\[
 C_4=\operatorname{RS}_{\mathbb F_{p^4}}(D,K),
 \qquad D\subseteq\mathbb F_p,
\]

and the numerator is the maximum number of distinct codewords agreeing with
one received word on at least `a` coordinates.  It is not an MCA slope count.

Grande Finale v4 requires the ordered LIST sum

\[
 U_{\rm paid}+U_Q+U_{\rm list-int}+U_{\rm ext}+U_{\rm new}.
\tag{1.1}
\]

The checked-in four-row v1 machine compiler predates this contract: it names
the v3 architecture, omits \(U_{\rm ext}\), and uses slope/received-line units
globally.  It cannot receive this packet by a data-only change.  The new
manifest therefore freezes a separate v4 M31 LIST contract with codeword
units and all five atoms.  The old v1 artifact remains a historical v3
structural preflight.

## 2. Direct target-field source lift

The earlier source and coupled packets stated their deployed structural
theorems over \(\mathbb F_p\).  The part consumed here has no prime-field
step.  The following lemma supplies the missing target-field bridge.

### Lemma 2.1 (field-generic exact-layer and coupled-kernel lift)

Let \(\mathbb K\) be any field containing the distinct evaluation set
\(D\), and put

\[
 C_{\mathbb K}=\operatorname{RS}_{\mathbb K}(D,K).
\]

For any received word \(y\in\mathbb K^D\), every exact-support, full-layer,
common-core, divided-difference Padé, polynomial-syzygy, and pair-collision
statement consumed in Sections 3--5 below remains valid over \(\mathbb K\).
In particular, for every complete exact layer of size at least 46 and every
46-member subpacket obtained after dividing the common core
\(C_j=\bigcap_{|E(c)|=j}E(c)\) of the complete layer, the coupled
locator--numerator kernel is free of rank 44 and has

\[
 \sum_{i=1}^{44}\nu_i
 \le 2j-K-|C_j|-1.
\tag{2.1}
\]

### Proof

The proof uses only the following field-generic facts.

1.  The dual of a generalized Reed--Solomon code on distinct points is a
    generalized Reed--Solomon code over the same field, with every dual
    weight nonzero.  Thus the weighted evaluation isomorphism
    \(\operatorname{Ev}_u:\mathbb K[X]_{<K}\to C_{\mathbb K}^\perp\)
    is available.  Finite-dimensional orthogonality over \(\mathbb K\)
    gives
    \[
      (C_{\mathbb K}^\perp\cap U_{D\setminus E})^\perp
      =C_{\mathbb K}+U_E.
    \]
    Hence dual containment is equivalent to a codeword explanation supported
    on \(E\).  Uniqueness and pairwise support separation use only the MDS
    distance \(K+1\), which is unchanged after extending the coefficient
    field.

2.  Divisibility by the split squarefree locator \(L_E\), the one-point
    quotient, the divided-difference identity, and the resultant product are
    polynomial identities over an arbitrary field.  They give every
    containment recurrence and every one-point escape over \(\mathbb K\).

3.  Intersecting root sets computes the full common gcd over
    \(\mathbb K[X]\).  After division, the reduced locator row is primitive.
    The reduced functional is nonzero by any retained escape.  The polynomial
    part of \(P_iS_\lambda\) and its order at infinity follow coefficient by
    coefficient, so the common Padé source is unchanged.

4.  The ring \(\mathbb K[X]\) is a PID.  Bézout splitting, free syzygy
    modules, row-reduced predictable degree, cofactor duality, determinantal
    divisors, and the exact index sums therefore hold verbatim.  None uses
    the cardinality or prime subfield of \(\mathbb K\).

5.  For two distinct codeword explanations, their difference is supported
    on the union of the two exact error supports.  The pair-minor formula is
    obtained by evaluation on more distinct points of \(D\) than its degree;
    the polynomial root bound is valid over every field.  Thus
    \(\Omega_{ij}=\gamma Q_{ij}h_{ij}\) with
    \(\gamma\in\mathbb K^\times\), and every pair minor is nonzero.
    Applying the PID kernel theorem to an arbitrary 46-member restriction
    gives (2.1), including the restricted-row determinantal divisor.

The maximizing-layer choice in the predecessor was used only to force one
large layer.  Once a complete layer with at least 46 members is present, the
five arguments above apply to that layer independently.  This proves the
lemma.  \(\square\)

Specialize Lemma 2.1 to
\(\mathbb K=\mathbb F_{p^4}\).  The evaluation domain remains the same
subset of \(\mathbb F_p\), hence of \(\mathbb K\), and the MDS distance
remains \(K+1\).  Consequently the complete exact-support histogram and
every marked key below belong to the original deployed quartic-field list.
No projection is used, and every distinguished key codeword is a target
codeword.

The union-of-hyperplanes nonforcing argument also becomes no weaker over
\(\mathbb F_{p^4}\): the number of forbidden hyperplanes for 67 supports is
less than \(p<p^4\).  Thus the conclusion that bounded local rank alone
does not force a collision remains valid on the target field.  The literal
prime-field `67/68` cutoff does not transfer: over the quartic field the
union bound continues beyond 68.  Only the valid 67-support nonforcing
conclusion is consumed here.

### Independent scalar-descent cross-check

The proved scalar-descent theorem applies with extension degree four and

\[
 t=R=981129,
 \qquad g=a-K+1=67448.
\]

Its exact strict incidence gate is

\[
 L t H_4 < g N_4,
\]

with margin

```text
592061458020761914489814638395392.
```

Consequently, if a received word over \(\mathbb F_{p^4}\) has at least
\(L\) distinct agreeing codewords, choose any \(L\) of them.  One nonzero
\(\mathbb F_p\)-linear functional
\(\lambda:\mathbb F_{p^4}\to\mathbb F_p\) preserves those \(L\)
codewords distinctly and preserves every agreement coordinate.  We obtain a
received word \(y\in\mathbb F_p^D\) and \(L\) distinct members of

\[
 C=\operatorname{RS}_{\mathbb F_p}(D,K)
\]

within error weight \(R\).

This is a threshold reduction, not an additive extension-cell payment.
It does **not** justify writing \(U_{\rm ext}=0\) in (1.1).  Instead it says
that a direct contradiction may be proved on the prime-field source.  The
v4 `U_ext` atom remains null until a compatible additive interpretation is
proved.

The functional \(\lambda\) is chosen after the hypothetical \(L\)-sublist
is supplied.  The scalar theorem therefore does not provide one public,
objectwise first-match map.  We make no such use of it: Sections 3--7 work
directly with the original quartic received word and its complete target
list, by Lemma 2.1.

## 3. Exact-support universe and the bankable target low cap

Return to the original target-field received word
\(y\in\mathbb F_{p^4}^D\).  For every listed target codeword \(c\), put

\[
 E(c)=\{x\in D:y(x)\ne c(x)\}.
\]

Since \(R<K+1=d(C_4)\), distinct listed codewords have distinct exact error
supports.  Conversely every support satisfying the shortened-dual
containment and every one-point escape determines one unique codeword.
Thus the complete list is partitioned without multiplicity by

\[
 M_j=\#\{c:|E(c)|=j\},\qquad 0\le j\le R,
\tag{3.1}
\]

and

\[
 |\mathcal L_R(y)|=\sum_{j=0}^{R}M_j.
\tag{3.2}
\]

Set

```text
J0 = 614160,
s  = n-J0 = 1482992.
```

For each codeword with \(|E(c)|\le J_0\), choose the first \(s\) agreement
coordinates in the fixed public ordering of \(D\).  Two such selected sets
intersect in at most \(K-1\), because two distinct degree-\(<K\) codewords
cannot agree at \(K\) evaluation points.  Integer convexity in the resulting
pair-incidence count proves

\[
 \boxed{\sum_{j\le J_0}M_j\le3730.}
\tag{3.3}
\]

At `3731` selected sets the exact lower pair incidence exceeds the exact
upper incidence by `19019`; at `3730` the relaxation remains feasible by
`202311`.  The proof uses only that two distinct degree-\(<K\) polynomials
over \(\mathbb F_{p^4}\) have at most \(K-1\) common evaluation roots.
Equation (3.3) is therefore uniform in the original target received word and
uses a fixed algebraic weight predicate.  In the frozen first-match order it
supplies

```text
LOW_EXACT_WEIGHT_PACKING -> U_paid <= 3730.
```

This is a direct quartic-field codeword payment, not an inherited scalar
projection payment.  No other atom is assigned an integer in this packet.

As a small independent sharpening of the earlier layer extraction, the
entire ball \(|E|\le K/2\) contains at most one codeword, not one per weight:
two such errors would have union size at most \(K<d(C_4)\).  Hence a forbidden
list already forces a same-weight layer of size at least

\[
 \left\lceil\frac{L-1}{R-K/2}\right\rceil=37.
\tag{3.4}
\]

This improves the earlier `36`-column extraction but is not the main global
compiler below.

## 4. Exact occupancy and all marked rank-46 keys

There are

```text
H=R-J0=366969
```

high weights.  Define

\[
 N_{\rm low}=\sum_{j\le J_0}M_j,
 \qquad
 T_{46}=\sum_{j>J_0}\max(M_j-45,0),
\]

\[
 H_r=\#\{j\in[J_0+1,R]:M_j\ge r\},
 \quad
 C_{\rm low}=3730-N_{\rm low},
 \quad
 C_r=H-H_r\ (1\le r\le45).
\]

Layer cake gives the exact identity

\[
 |\mathcal L_R(y)|
 =3730+45H+
 \left(T_{46}-C_{\rm low}-\sum_{r=1}^{45}C_r\right).
\tag{4.1}
\]

The fixed base is

\[
 3730+45H=16,517,335,
\]

so, writing the signed parenthesis in (4.1) as \(\Xi_{46}\),

\[
 |\mathcal L_R(y)|\ge L
 \Longrightarrow
 \Xi_{46}\ge259881.
\tag{4.2}
\]

Every credit is nonnegative, hence

\[
 \boxed{T_{46}\ge259881.}
\tag{4.3}
\]

Order every complete high-weight layer canonically by the incidence vector
of its exact support.  Use the first 45 members as anchors, and for each
remaining member form the key

\[
 (j;E_1,\ldots,E_{45};E_*).
\tag{4.4}
\]

There are exactly \(T_{46}\) keys, and different keys have different
distinguished codewords.  This retains the codeword projection while loading
the complete same-weight layer as algebraic context.  The anchors are not
charged as 45 new owners, and the signed credits in (4.1) are not discarded.

The lexicographic key selection is a source theorem used to expose the
residual.  It is not the source partition and is not promoted to an
admissible v4 algebraic payment: the v4 definition forbids invoking,
recovering, or enumerating the agreeing-codeword projection in a payment.
In particular, the `45H` term in (4.1) is an exact occupancy baseline, not an
unrecorded `U_paid` charge.

## 5. Coupled rank-three theorem on every global key

Fix the complete exact layer containing one key (4.4), with common weight
\(j\).  Put

\[
 C_j=\bigcap_{c:\,|E(c)|=j}E(c)
\]

and divide the common error core \(C_j\) of the **entire layer**.  Write its
primitive reduced locators as

\[
 P_1,\ldots,P_{46},
 \qquad
 e=\deg P_i,
 \qquad
 D_0=K-j.
\]

The 46 columns of the key are then restricted from this full-layer row.  They
may acquire an additional common factor; the joint-kernel theorem explicitly
allows a nonprimitive restricted locator row and absorbs that factor in its
determinantal divisor.  The actual received-word functional gives the
divided-difference numerator
row

\[
 B_i(Y)=\lambda_X\!\left(\frac{P_i(X)-P_i(Y)}{X-Y}\right).
\]

Containment, all one-point escapes, squarefreeness, and pairwise MDS
separation are inherited from the exact-support source.  In particular the
two-row polynomial matrix

\[
 \begin{pmatrix}
 P_1&\cdots&P_{46}\\
 B_1&\cdots&B_{46}
 \end{pmatrix}
\tag{5.1}
\]

has rank two.  Its polynomial right kernel is free of rank 44.  If

\[
 0\le\nu_1\le\cdots\le\nu_{44}
\]

are its row-reduced indices, the coupled joint-index theorem gives

\[
 \sum_{i=1}^{44}\nu_i
 \le e-D_0-1
 =2j-K-|C_j|-1
 \le2R-K-1
 =913681.
\tag{5.2}
\]

For a nondecreasing nonnegative sequence of length 44 and total at most
`913681`, write

```text
913681 = 44*20765 + 21.
```

Exact balancing gives

\[
 \boxed{
 \nu_1\le20765,\qquad
 \nu_1+\nu_2\le41530,\qquad
 \nu_1+\nu_2+\nu_3\le62295.
 }
\tag{5.3}
\]

The next partial sum can be `83060`, so rank four is not certified below the
cutoff by this aggregate information.  Since

\[
 D_0=K-j\ge K-R=67447,
\]

the first three rows in (5.3) are independent coupled locator--numerator
relations strictly below the source cutoff:

\[
 62295<67447\le D_0.
\tag{5.4}
\]

This conclusion holds for every marked key from (4.3).  It is stronger than
the preceding locator-only rank-three frame: every row annihilates both the
locator row and the actual divided-difference numerator row.

For each pair, the determinant

\[
 \Omega_{ij}=P_iB_j-P_jB_i
\]

is a fixed nonzero scalar times the overlap gcd and the actual codeword
collision polynomial.  Thus any future common factor or root-union owner is
typed by actual codeword collisions rather than locator support alone.

## 6. Frozen v4 chronology and exhaustive residual

The adapter freezes the following source order on the **codewords** of the
full deployed quartic-field list:

```text
SOURCE: DIRECT_TARGET_FIELD_EXACT_LAYER_LIFT
CROSS_CHECK_ONLY: SCALAR_DESCENT_AT_FORBIDDEN_THRESHOLD

U_paid:
  LOW_EXACT_WEIGHT_PACKING

U_Q:
  no assigned target cell; a certified boundary-prefix target map is missing

U_list_int:
  no assigned target cell; a certified arbitrary-word chart map is missing

U_ext:
  no assigned target cell; direct field lift is not U_ext=0

U_new:
  HIGH_BOUNDARY_EXACT_CODEWORD: |E(c)|=R
  HIGH_INTERIOR_EXACT_CODEWORD: J0<|E(c)|<R
```

A codeword with \(j=R\) is boundary, but it is **not** automatically in
\(U_Q\): no theorem maps its arbitrary syndrome layer to one frozen locator-
prefix target with the required attained-image normalization.  A codeword
with \(J_0<j<R\) is interior, but it is not automatically paid by
\(U_{\rm list-int}\): no theorem supplies the global arbitrary-word chart
inventory and add-back.  Both therefore first-match to the corresponding
explicit codeword-valued `U_new` residual in this open adapter.

Together with the low predicate, this classification covers every codeword
exactly once and keeps boundary and interior disjoint.  The two high residual
counts include the entire `45H` occupancy baseline; no codeword is hidden in
the signed identity.  The marked keys form a separate, injective diagnostic
subfamily: (4.3) proves that any forbidden list forces at least `259881` of
them inside these residual cells before any compatible owner has been
supplied.

The local full-budget v4 fixed-union, affine-span, rank-flat, common-zero,
codimension-one, and support-flag propositions cannot be applied merely to a
46-member key.  Their hypotheses concern a complete first-match chart, and
their full-budget ceilings are not mutually summable.  Loading paid columns
as algebraic context is permitted; charging them again is not.

## 7. Exact route cut

The available signed occupancy allowance after the exact low cap and the
formal high-layer baseline is

\[
 B^*-(3730+45H)=259880.
\tag{7.1}
\]

Even granting the optimistic conclusion that one key injects into roots of
one nonzero polynomial of degree `62295`, independent key-by-key root unions
cannot close the row:

\[
 4\cdot62295=249180,
 \qquad
 259880-249180=10700,
\]

while

\[
 5\cdot62295=311475>259880.
\tag{7.2}
\]

Moreover, the coupled packet's exact finite-field fixture has several
degree-zero coupled rows and no collision, and its 67-support hyperplane
avoidance theorem shows that bounded local rank alone does not force a
collision owner.  Therefore another standalone 16-, 30-, or 46-column
calculation cannot close the row unless it supplies a theorem acting across
the global marked-key family.

The next closure theorem must do at least one of the following, uniformly in
the received word and with the source key retained:

1. coalesce all surviving key polynomials into at most four global root
   unions, including the exact `10700` remainder;
2. route every key to a named, disjoint v4 owner with an exact charge and
   refund preserving (4.1);
3. prove the primitive coupled component empty; or
4. bound the complete boundary/interior distinguished-codeword projection by
   `259880` directly.

Absent one of these statements, the correct diagnostic terminal inside the
two exhaustive `U_new` codeword cells is

```text
UNPAID_GLOBAL_COUPLED_RANK46_RESIDUAL
```

and

```text
U_Q        = null
U_list_int = null
U_ext      = null
U_new      = null
row closed = false
ledger movement beyond LOW_EXACT_WEIGHT_PACKING = 0.
```

Here `null` means that no exact nonnegative integer upper payment has been
proved.  It does not mean that the corresponding codeword cell is empty.  The
signed occupancy identity is used only to force the diagnostic family from a
hypothetical violation; it does not replace the additive v4 ledger.

## 8. Compiler migration, upstream overlap, and provenance gate

The open-PR audit was refreshed against `origin/main@a3017697a` on
2026-07-21.  The numerical ingredients are deliberately not claimed as new:

- #1021 and #1025 already record the `20765`, `41530`, and `62295`
  rank-three consequences in locator or padded-locator form;
- #1022 already records the same four-versus-five `62295` root-union
  arithmetic and the `10700` remainder for its locator-only route cut;
- #1023 is the exact-support/full-layer source dependency; and
- #1028 is the coupled locator--numerator dependency.

The nonduplicate delta here is the direct symbolic lift of that chain to the
deployed quartic coefficient field, the exhaustive target-codeword v4
partition, the bankable `U_paid<=3730` cell, and the application of the
coupled theorem to every globally forced target-field marked key.  None of
#1021, #1022, or #1025 supplies that target-field five-atom adapter or a
bankable completion atom.

The adapter manifest corrects three load-bearing mismatches in the old live
machine contract:

1. `GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1`, not v3;
2. five LIST atoms, including `U_ext`;
3. `DISTINCT_CODEWORDS_PER_RECEIVED_WORD`, not slopes per received line.

It also hash-binds the promoted v4 manuscript, scalar descent, whole-list
rank-46 compiler, full-packet source, coupled theorem, and all verifier
sources.  The older rank-46 certificate currently fails its all-source gate
because it pins the pre-v4 `grande_finale.tex` hash.  Its arithmetic and
theorem sources are unchanged; this adapter independently recomputes every
consumed integer and binds the current source bytes.  The stale predecessor
pin is reported, not silently treated as a passing replay.

Passing the new schema and mutation suite proves internal identity, exact
arithmetic, and the stated source composition.  It does not turn the null
atoms into upper bounds or certify row closure.

## 9. Edge cases and falsification

The verifier rejects at least the following mutations:

- quartic/base-field or codeword/slope unit swaps;
- `L=B*` in place of `B*+1`;
- a non-strict scalar-descent gate or a projection collision;
- omission of any exact-support weight;
- raw support witnesses in place of canonical codewords;
- treating the lexicographic first-45/excess split as a v4 owner;
- omitting the `45H` codeword baseline from the exhaustive residual cells;
- dropping one-point escapes or the full same-weight layer context;
- changing the low cap `3730`, cutoff `614160`, or packing margins;
- discarding the signed occupancy credits;
- changing `259881` to `259880`;
- using 45 rather than 44 joint indices;
- changing `62295` or the strict cutoff `62295<67447`;
- folding `U_ext` into another atom;
- assigning a boundary key to Q without a target-map theorem;
- assigning an interior key to `U_list_int` without global coverage;
- forcing the unpaid residual to zero;
- stale source hashes or a changed partition order.

No analytic or dyadic layer-cake, moment, Markov, or Chebyshev argument occurs.
The only layer-cake is the finite exact identity (4.1); it has no additive
error term and therefore presents no summability issue.
All arithmetic is exact and finite at the displayed M31 row.

## 10. Nonclaims

- The M31 list row is not closed.
- No forbidden received word is constructed.
- Scalar descent is not an additive `U_ext=0` theorem.
- The lexicographic 45-anchor source keys are not promoted to v4 paid owners.
- A boundary exact support is not silently identified with one Q target.
- A source common support is not silently identified with a common-zero
  direction-code owner.
- No fixed-union or affine-span full-budget ceiling is summed over many keys.
- No root of a low-degree key polynomial is counted without a cross-key
  coalescing theorem.
- No stable paper, endpoint, radius, official score, or Lean theorem changes.

## 11. Replay

From the repository root:

```text
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 -O experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --check
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_list_v4_source_adapter_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py --check
python3 -O experimental/scripts/verify_m31_list_v4_source_adapter_v1_independent.py --check
```

The scalar-descent, full-packet, coupled, rank-46 arithmetic, and Sage finite-
field controls are replayed separately during release validation.  Their
computations verify source arithmetic and toy identities; they do not replace
the symbolic proofs above.
