# M1 RIM support-pattern pivot replay

Status: AUDIT / COMPUTATIONAL_CERTIFICATE / PIVOT_COVERAGE_COMPLETE / EXPERIMENTAL

This note records the support-pattern replay pass for exact full-rank `a=327`
reduced-intersection matrices in the M1 interleaved-list workstream for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` pivot-certificate audit, not an MCA `N_bad` row, and it does
not claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, an `a=327` certificate, or a global upper bound at `a=327`.

## Purpose

The previous coverage pass certified the two-level quotient-residual and
balanced-clique pairwise source packets:

```text
14 / 34 source matrices certified
20 / 34 support-pattern matrices pending
```

This pass replays the 20 pending support-pattern reduced-intersection matrices,
starting with the smallest compressed-variable cases, and extracts explicit
RREF pivot-minor certificates over `GF(17^32)`.

## Coverage

The scanner indexes and certifies all 34 exact full-rank source matrices:

```text
pairwise_divisibility_nullvector_system        6 / 6 certified
two_level_pairwise_divisibility                8 / 8 certified
constructive_rank_defect_support_design        8 / 8 certified
support_pattern_multiplicity_mutation_search   6 / 6 certified
support_pattern_surrogate_rank_feedback_search 6 / 6 certified
```

Thus total replayable pivot coverage improves from:

```text
14 / 34
```

to:

```text
34 / 34
```

The newly certified surface is exactly the 20 support-pattern matrices. For
each certified support-pattern matrix, the Sage audit reconstructs the reduced
matrix over `GF(17^32)`, extracts RREF pivot rows, forms the selected square
minor, and verifies that the minor has full rank.

## Aggregate Pivot Profile

Across all 34 certified matrices, the aggregate pivot row profile is:

```text
balanced_or_generic_pairwise_row: 1226
quotient_full_fiber_row:          383
residual_or_partial_fiber_row:     37
support_overlap_row:             1901
```

The support-pattern certificates use support-overlap rows for their pivots.
The pairwise-divisibility certificates use generic pairwise rows, while the
two-level quotient-residual certificates split between quotient-fiber and
residual rows.

## Status Ledger

COMPUTATIONAL_CERTIFICATE / AUDIT:

- 34 source full-rank reduced matrices indexed;
- 34 matrices now have explicit Sage-replayed pivot-minor certificates;
- all 20 support-pattern rows are newly certified in this pass;
- all certified minors are full rank over `GF(17^32)`;
- no certified row has positive nullity;
- no `a=327` interleaved-list certificate appears.

PARTIAL / OPEN:

- no common pivot-pattern theorem is claimed yet;
- no quotient-residual or support-pattern class theorem is claimed;
- global `Lambda_mu(C,327) <= 6` remains open.

NOT CLAIMED:

- `a=327` interleaved-list certificate;
- improvement over PR #133;
- global RIM full-rank theorem;
- global `Lambda_mu(C,327) <= 6`;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next Step

The next useful move is to mine the 34 pivot profiles for a common
pivot-pattern theorem. The immediate target should be a deterministic
row-ordering or block-pivot explanation for why the support-overlap rows pivot
all compressed variables in the 20 support-pattern matrices.
