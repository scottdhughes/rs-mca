# M1 A4 fail-closed SPI atlas manifest v1

**Status:** AUDIT / PARTIAL INFRASTRUCTURE.  This note does not prove the
KoalaBear MCA row at agreement `A=1,116,048`, does not improve the public
frontier, and does not identify a capacity index with an SPI chart.

## Purpose

The M1 A4 lane needs a canonical first-match atlas in which every admitted
SPI chart ends at exactly one of:

1. `CERTIFIED_SLOPE_ELIMINANT`;
2. `NAMED_PAID_OWNER`; or
3. `UNPAID_PRIMITIVE`.

The machine-readable contract is

```text
experimental/data/schemas/m1_a4_spi_atlas_manifest_v1.schema.json
```

and the verifier is

```text
experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py
```

Version 1 is deliberately fail closed.  Compressed families are capacity-only
and their adapter status is fixed to `UNPROVEN`; proved charts must be printed
explicitly.  A paid owner must be the first eligible owner in the frozen order,
must cite one unique source claim for its global charge, and may not multiply
that charge by the number of charts.  Version 1 also permits at most one global
charge per owner, blocking alternate JSON pointers to the same theorem.  An
eliminant must be nonzero, have its
printed degree, and include explicit source-bound ideal generators and
multipliers whose polynomial identity is replayed modulo the base field.  The
same source record must bind the variable and the SHA-256 digest of the exact
canonical chart key, preventing an unrelated ideal from being reused.  It
is charged either by exhaustive base-field root enumeration on small controls
or by its degree on large fields.  Eliminant charges are summed over disjoint,
chart-specific root spaces; cross-chart root deduplication requires a separate
theorem and is unavailable in v1.  An unpaid terminal may carry no owner,
charge, numeric amount, or eliminant.

## Deployed row arithmetic

For the KoalaBear MCA row,

```text
p = 2,130,706,433
e = 6
q = p^6
  = 93,571,093,019,388,561,295,270,373,781,649,880,353,786,165,192,103,559,169
n = 2,097,152
k = 1,048,576
A = 1,116,048
j = n-A = 981,104
t = A-k = 67,472
w = t-1 = 67,471
```

The syndrome-kernel lower bound is

\[
j+1-t=913{,}633.
\]

In particular, this row is not deficiency one.  A deficiency-one SPI lemma
cannot be imported merely because it has an attractive local eliminant.

The exact challenge budget is

\[
B_*=\left\lfloor\frac{q}{2^{128}}\right\rfloor
   =\left\lfloor\frac{q-1}{2^{128}}\right\rfloor
   =274{,}980{,}728{,}111{,}395{,}087.
\]

The two floors coincide here because `q` is odd and no multiple of `2^128`
lies between `q-1` and `q`.

## Imported paid baseline

The prior exact first-match packet proves the following base-generated-field
image-cell charge after its earlier gates:

\[
U_{\rm gen}=tp
=143{,}763{,}024{,}447{,}376.
\]

It also records the terminal quotient charge

\[
U_{\rm quot,terminal}=471{,}447{,}040.
\]

Thus the imported global-once baseline is

\[
U_{\rm paid}=143{,}763{,}495{,}894{,}416,
\]

leaving

\[
B_*-U_{\rm paid}
=274{,}836{,}964{,}615{,}500{,}671.
\]

These are exact integer identities.  They do not decide the target inequality

\[
U_{\rm paid}+U_Q+U_A\le B_*,
\]

because `U_Q` and `U_A` are still unknown.

The imported source packet is pinned to integration commit
`0955594bf354b6a396574b65fbb242715edd3267`.  The manifest also pins the live
SHA-256 hashes of its note, JSON packet, and verifier and replays the printed
first-match order and generated-collision branch fields.

## The adapter obstruction

The prior generated-collision theorem starts with a normalized affine row
packet

\[
L_i(S,Z)=A_i(S)+ZB_i(S)
\]

and sends a finite base-valued survivor to its first nonzero cross-defect row
and a slope in `F_p`.  If `R` affine rows survive, it proves

\[
R\le t,
\qquad
\#\text{image cells}\le Rp\le tp.
\]

What it does **not** emit is a list of `67,472` deployed SPI charts.  Its row
index is `i`; a new SPI atlas index called `h` has not been proved equal to
`i`.  Nor does the source bound raw support multiplicity.  The theorem applies
only to finite slopes in `F_p`, after the prior containment, rank, pivot, and
denominator gates.  Slopes in `F_(p^6) - F_p` remain open.

Consequently the range

```text
h = 0, ..., 67,471
```

is stored only as a **capacity namespace**.  It has the right cardinality for
the source upper bound, but its `chart_adapter_status` is `UNPROVEN`, it
represents zero SPI charts, and its terminal is `UNPAID_PRIMITIVE`.  The valid
`p` per-index cap and `tp` family cap are metadata about the conditional source
owner; they are not recharged and do not create a new ledger deduction.

This is the load-bearing correction in this packet.  Marking all capacity
labels paid would replace a missing mathematical adapter with a cardinality
coincidence.

## Canonical key and first-match discipline

An explicit chart key contains

```text
(A, quantifier_scope, locator_chart_id, patch, rank_s,
 pivot_rows, pivot_cols, pivot_kind, h).
```

The manifest rejects duplicate keys independently of human-readable chart
IDs.  Each explicit chart prints every owner gate in frozen order.  A named
owner must equal the first eligible gate.  A bounded compressed family may use
a candidate owner only after its adapter and every scope gate are proved.
The policy also names its final unpaid fallback explicitly.  For this M1 row
that gate is `primitive_qfin_residual`; `UNPAID_PRIMITIVE` is the terminal
kind, not an M1 owner ID.  The fallback can never be selected as a paid owner,
and every paid terminal must reference a registered charge belonging to the
same owner.

The deployed first-match order is imported verbatim from the source packet:

1. `contained_or_noncontained_failure`;
2. `rank_drop_or_pivot_failure`;
3. `tangent_common_line_residue`;
4. `quotient_periodic_or_divisor_stabilized`;
5. `planted_prefix_structured`;
6. `extension_valued_slope`;
7. `base_generated_field_collision`;
8. `sparse_sigma_or_sparse_support`;
9. `m1_half_turn_or_coefficient_shadow`;
10. `primitive_qfin_residual`.

## GF(19) machinery control

The second artifact is a non-banking finite control.  It uses the frozen
sequential layout

```text
q=19, n=18, k=5, sigma=3
core       = [0,1,2,3]
petals     = [4..7], [8..11], [12..15]
background = [16,17]
```

and the exact profile

\[
(\ell,d,r,t,(a_i))=(4,4,2,2,(3,3)),
\qquad (G_2,G_R)=(2,3).
\]

Choosing two labelled petals and three of four points in each gives

\[
\binom32\binom43^2=48
\]

canonical patterns.  The verifier regenerates all 48.  There are 16 patterns
in each occupancy class `(3,3,0)`, `(3,0,3)`, and `(0,3,3)`; every mask is
distinct and has stabilizer one under the repository's cyclic exponent-shift
action.  Complete-fibre scales, the auxiliary/global Johnson coordinates, and
the B11 classification are derived from the pinned full-list scanner helpers,
not compared against a second hardcoded copy.  The canonical assignment-list
and mask-list digests are respectively

```text
03d00b8d225d5af19ed74f105895d31aa738abb50dc3111e65f4bb90be387644
49bf3c30e5139c61638b8917e298ddc7d0f36418ccce13d202968adace871fd2
```

The frozen L1 owner order is periodic support, invariant quotient descent,
auxiliary Johnson, global Johnson, B11 `G2`, B11 `GR`, then
`UNPAID_PRIMITIVE`.  For this control, the exact auxiliary-Johnson margin is
`-12`, the global Johnson gate has `lambda=0<lambda_J=1`, and the B11
coordinates escape the paid box.  All 48 terminals are therefore
`UNPAID_PRIMITIVE`.

The per-pattern cofactor charge is

\[
19^{4-3+1}=19^2=361,
\]

and the exact control total is `48*361=17,328`.  The artifact sets
`ledger_consequence=false`: it is not linked to the post-stack L1 ledger and
does not bank this number.  It tests the atlas/certificate machinery only.

## Verification and mutations

Run

```sh
python3 experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py --check
python3 experimental/scripts/verify_m1_a4_spi_atlas_manifest_v1.py --tamper-selftest
```

The checker uses only the Python standard library.  It parses JSON with
duplicate-key and nonstandard-constant rejection, walks the closed Draft
2020-12 schema, recomputes every source and payload hash, replays both row
arithmetics, regenerates the 48-pattern control, checks first-match ownership,
and uses a safe disjoint-chart sum for eliminants.  Exact enumeration is
permitted only for base fields of size at most `10,000`; on larger fields the
certificate charge is the verified nonzero eliminant degree unless a future
factor/gcd certificate extends the schema.

The KoalaBear imported ledger is checked against an exact row-specific charge
registry, including owner, binding, JSON pointer, scope, identifier, and
amount.  This blocks a second owner from charging an alias pointer to the same
source theorem.

Semantic mutations cover field and budget drift, wrong `j,t,w`, a false
deficiency-one flag, missing pivot/localization gates, duplicate chart keys,
owner-order drift, a later owner selected before an eligible earlier owner,
zero and mis-degreed eliminants, source-generator and polynomial-combination
drift, omitted large-field roots, cross-chart root-space collapse, undercounted
disjoint chart sums, global charges multiplied per chart, same-claim charges
under distinct IDs, numeric charges on unpaid terminals, false row
completeness, negative or null ledger terms, a false proved inequality, wrong
cyclic stabilizer data, hardcoded owner-gate drift, and source/payload hash
drift.  They also cover cross-owner theorem aliases, paid fallback terminals,
and paid-owner/charge-owner mismatches.  Positive controls exercise exact
enumeration, safe degree charging, a complete-manifest inequality failure,
and both paid and unpaid explicit M1 terminal semantics.

The predecessor packet's fast committed-artifact check passes.  On the local
Python 3.14 runtime, its optional `--full --check` rebuild differs from the
committed JSON in 17 floating-point diagnostic `log2` values at the last few
ulps.  A recursive comparison found no exact integer, first-match, charge, or
status difference.  This v1 manifest therefore pins and consumes only the
committed packet's exact load-bearing fields; it does not treat byte-for-byte
reproduction of those non-load-bearing floats as a theorem gate.

## Verdict and next lemma

**YELLOW.**  The manifest contract and finite control are exact.  The deployed
row remains open because the SPI-to-affine-row adapter is unproved and the
extension-valued and primitive residuals are unbounded.

The next mathematical lemma is narrow:

> After the frozen earlier M1 gates, map every admitted base-valued finite SPI
> chart to one unique normalized affine row in the existing generated-field
> packet, preserving the pivot, denominator, noncontainment, and first-match
> hypotheses; otherwise emit the chart explicitly as `UNPAID_PRIMITIVE`.

After that adapter is proved, the capacity namespace must be expanded into
explicit charts (or a separately reviewed v2 compressed-chart schema) before
it can become a represented paid atlas component.  The exact inequality must
then be rerun with explicit nonnegative `U_Q` and `U_A`; no null term may be
promoted to zero.
