# M1 generic-pairwise rank-free pivot rule

Status: AUDIT / COMPUTATIONAL_CERTIFICATE /
RREF_DERIVED_PATTERN_ONLY / PARTIAL / EXPERIMENTAL

This note tests whether the six `generic_pairwise_rref_pivot` matrices from
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
generic_pairwise_rref_pivot
```

which consists of six balanced-clique pairwise-divisibility matrices. Their
RREF-derived pivot-minor certificates are already part of the 34/34 pivot
coverage packet. This branch asks whether simpler metadata-only row schedules
can reproduce those full-rank certificates.

## Rank-Free Rules Tested

For each of the six generic-pairwise matrices, the Sage audit reconstructs the
matrix over `GF(17^32)`, replays the RREF-derived full-rank certificate, and
tests eight rank-free row-selection rules:

```text
anchored_pair_proxy_first
compressed_variable_block_order
incidence_greedy_matching_v1
nonanchored_difference_first
pair_boundary_pressure_asc
pair_boundary_pressure_desc
pair_label_lexicographic_order
rref_profile_pair_quota_mimic
```

The first seven rules use only pair labels, coordinate order, row incidence, or
compressed-variable block metadata. The last rule is deliberately weaker as a
theorem candidate: it uses the RREF pivot pair-count profile but not finite-field
row reduction or determinant arithmetic.

## Result

```text
generic-pairwise matrices:       6
rank-free rule attempts:         48
rank-free successes:             0
rref-derived certificates:       6 replayed
best failed minor rank ratio:    149 / 205
```

All 48 rank-free rule attempts selected singular minors. In particular, even
the `rref_profile_pair_quota_mimic` rule did not recover a full-rank minor in
this tested class.

## Interpretation

This packet proves a named tested-candidate audit fact:

```text
ROUTE_CUT_CERTIFIED_CANDIDATES:
  the six generic-pairwise candidates have certified full-rank RREF pivot
  minors over GF(17^32).

RREF_DERIVED_PATTERN_ONLY:
  the tested rank-free metadata rules do not select full-rank minors.
```

It does not prove the desired deterministic theorem:

```text
For the generic_pairwise_rref_pivot class, a metadata-only row schedule selects
a full column-rank minor over GF(17^32).
```

The reason is concrete: the only certified full-rank schedules remain extracted
from Sage RREF pivot rows.

## Status Ledger

COMPUTATIONAL_CERTIFICATE / AUDIT:

- six generic-pairwise reduced matrices isolated;
- all six RREF-derived pivot-minor certificates replay over `GF(17^32)`;
- eight rank-free metadata rules tested on each matrix;
- all 48 rank-free rule attempts selected singular minors;
- no positive nullity appears;
- no `a=327` interleaved-list certificate appears.

PARTIAL / OPEN:

- no deterministic generic-pairwise pivot schedule is proved;
- quotient-residual pattern class remains outside this packet;
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

Move to the `quotient_residual_rref_pivot` class. At that point all three
pattern classes will have either a rank-free explanation or a clear
`RREF_DERIVED_PATTERN_ONLY` audit result.
