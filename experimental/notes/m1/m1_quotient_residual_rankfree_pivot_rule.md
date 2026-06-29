# M1 quotient-residual rank-free pivot rule

Status: AUDIT / COMPUTATIONAL_CERTIFICATE / RREF_MIMIC_PARTIAL_SUCCESS /
PARTIAL / EXPERIMENTAL

This note tests whether the eight `quotient_residual_rref_pivot` matrices from
the M1 `a=327` reduced-intersection matrix audit admit a rank-free pivot rule.

The ambient row remains:

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` pivot-rule audit, not an MCA `N_bad` row, and it does not
claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, an `a=327` certificate, a deterministic pivot theorem, or a global
upper bound at `a=327`.

## Scope

The input is:

```text
experimental/data/m1_rim_pivot_pattern_theorem.json
```

This branch filters to:

```text
quotient_residual_rref_pivot
```

which consists of eight two-level quotient-plus-residual matrices:

```text
six 6-column quotient-residual matrices
two 192-column anchor-relaxed quotient-residual matrices
```

Their RREF-derived pivot-minor certificates are already part of the 34/34 pivot
coverage packet. This branch asks whether quotient/residual metadata can select
full-rank minors before any finite-field row reduction.

## Rank-Free Rules Tested

For each of the eight quotient-residual matrices, the Sage audit reconstructs
the matrix over `GF(17^32)`, replays the RREF-derived full-rank certificate,
and tests eleven metadata row-selection rules:

```text
compressed_variable_block_order
fiber_coordinate_order
incidence_greedy_matching_v1
pair_boundary_pressure_asc
pair_boundary_pressure_desc
pair_label_coordinate_order
quotient_full_fiber_first
quotient_residual_balanced_order
residual_partial_fiber_first
row_type_pair_order
rref_profile_type_pair_quota_mimic
```

The first ten rules use quotient/residual row type, fiber, pair label,
coordinate, incidence, or compressed-variable metadata. The last rule is a
weaker theorem candidate: it mimics the RREF row-type and pair-count profile but
still does not use finite-field row reduction or determinant arithmetic to pick
rows.

## Result

```text
quotient-residual matrices:          8
rank-free rule attempts:             88
rank-free successes:                 2
deterministic-rule successes:        0
RREF-mimic-rule successes:           2
large-matrix rank-free successes:    0
```

The two successes occur only for `rref_profile_type_pair_quota_mimic` on
6-column matrices:

```text
punctured_eight_fiber_11
seven_fibers_plus_residual_11
```

No deterministic metadata rule succeeds, and neither 192-column
anchor-relaxed matrix has a rank-free success.

## Interpretation

This packet proves a named tested-candidate audit fact:

```text
ROUTE_CUT_CERTIFIED_CANDIDATES:
  the eight quotient-residual candidates have certified full-rank RREF pivot
  minors over GF(17^32).

RREF_MIMIC_PARTIAL_SUCCESS:
  a row-type/pair-quota mimic selects full-rank minors for two small matrices,
  but no deterministic metadata schedule works and no large matrix is covered.
```

It does not prove the desired deterministic theorem:

```text
For the quotient_residual_rref_pivot class, a metadata-only row schedule
selects a full column-rank minor over GF(17^32).
```

The only successful schedules still depend on RREF-derived profile data, not a
rank-free structural rule.

## Status Ledger

COMPUTATIONAL_CERTIFICATE / AUDIT:

- eight quotient-residual reduced matrices isolated;
- all eight RREF-derived pivot-minor certificates replay over `GF(17^32)`;
- eleven metadata rules tested on each matrix;
- two RREF-profile mimic attempts select full-rank minors;
- no deterministic metadata rule succeeds;
- no `a=327` interleaved-list certificate appears.

PARTIAL / OPEN:

- no deterministic quotient-residual pivot schedule is proved;
- the two 192-column anchor-relaxed cases remain RREF-derived only;
- global `Lambda_mu(C,327) <= 6` remains open.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- global `Lambda_mu(C,327) <= 6`;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next Step

The three pivot-pattern classes now have rank-free rule audits. A useful next
summary packet would compare them:

```text
support_overlap:    0 / 160 rank-free successes
generic_pairwise:   0 / 48 rank-free successes
quotient_residual:  2 / 88 rank-free successes, RREF-mimic only
```

That comparison should decide whether to attempt a theorem around the two small
quotient-residual mimic successes or stop the rank-free pivot-rule lane as
mostly RREF-derived.
