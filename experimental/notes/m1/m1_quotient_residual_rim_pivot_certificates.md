# M1 quotient-residual RIM pivot certificates

Status: AUDIT / COMPUTATIONAL_CERTIFICATE / PARTIAL / EXPERIMENTAL

This note records a first pivot-certificate audit for exact full-rank
`a=327` reduced-intersection matrices in the M1 interleaved-list workstream for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` rank-certificate audit, not an MCA `N_bad` row, and it does
not claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, an `a=327` certificate, or a global upper bound at `a=327`.

## Purpose

Several recent support/equality-family searches retained candidates whose
reduced rank gates were exact full rank over `GF(17^32)`. This audit starts to
replace black-box "Sage says full rank" evidence with replayable pivot-minor
certificates.

The scanner indexes exact full-rank matrices from these local packets:

```text
pairwise_divisibility_nullvector_system        6
two_level_pairwise_divisibility                8
constructive_rank_defect_support_design        8
support_pattern_multiplicity_mutation_search   6
support_pattern_surrogate_rank_feedback_search 6
```

This gives 34 exact full-rank source matrices.

## First-Pass Scope

The Sage audit reconstructs the two-level quotient-plus-residual source
matrices from the previous checkpoint. For this first pass it extracts explicit
pivot minors only for the six small boundary candidates with compressed
dimension `6`.

The two anchor-relaxed two-level rows have compressed dimension `192` and are
left as:

```text
PIVOT_EXTRACTION_DEFERRED
```

The balanced-clique and support-pattern source packets are indexed from their
JSON rank ledgers but not replayed in this first pivot audit, and are recorded
as:

```text
SOURCE_REPLAY_PENDING
```

## Certified Small Quotient-Residual Rows

The six certified rows are:

```text
common_six_fiber_residual_11
common_six_fiber_residual_10
punctured_eight_fiber_11
punctured_eight_fiber_10
seven_fibers_plus_residual_11
seven_fibers_plus_residual_10
```

For each row the reconstructed reduced matrix has shape:

```text
3825 x 6
```

and the Sage audit extracts a `6 x 6` pivot minor of full rank over
`GF(17^32)`. Each selected minor has `minor_rank = 6`, `minor_rank_full = true`,
and `minor_det_nonzero = true`.

The pivot-row type profiles are:

```text
seven_fibers_plus_residual_*:
  quotient_full_fiber_row: 6

punctured_eight_fiber_*:
  quotient_full_fiber_row: 5
  residual_or_partial_fiber_row: 1

common_six_fiber_residual_*:
  quotient_full_fiber_row: 1
  residual_or_partial_fiber_row: 5
```

Aggregated across the six certified rows:

```text
quotient_full_fiber_row:        24
residual_or_partial_fiber_row:  12
```

The common pivot pair profile is:

```text
1,2: 2
1,3: 1
1,4: 1
1,5: 1
1,6: 1
```

This is useful evidence that the small two-level boundary systems are not just
empirically full rank: their full rank can be replayed by explicit finite-field
pivot minors.

## Status Ledger

COMPUTATIONAL_CERTIFICATE / AUDIT:

- 34 source full-rank reduced matrices indexed from recent local packets;
- 6 small two-level quotient-residual matrices reconstructed in Sage;
- 6 explicit full-rank pivot minors extracted over `GF(17^32)`;
- pivot row and column hashes recorded in JSON;
- no positive nullity found in the certified rows;
- no `a=327` interleaved-list certificate appears.

PARTIAL / OPEN:

- 2 anchor-relaxed two-level rows still need large-matrix pivot extraction;
- 6 balanced-clique pairwise-divisibility rows are source-replay pending;
- 20 support-pattern reduced-intersection rows are source-replay pending;
- symbolic pivot-pattern theorem for the quotient-residual class;
- quotient-residual designs outside the indexed sources;
- global `Lambda_mu(C,327) <= 6`.

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

The immediate next step is to extend replayable pivot extraction to the two
large anchor-relaxed quotient-residual matrices and then to the balanced-clique
pairwise rows. If those pivot certificates share the same row-pattern geometry,
the result may become a genuine quotient-residual RIM pivot obstruction rather
than a collection of tested-candidate audits.
