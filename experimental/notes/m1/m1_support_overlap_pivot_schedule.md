# M1 support-overlap pivot schedule

Status: AUDIT / COMPUTATIONAL_CERTIFICATE / RREF_DERIVED_PATTERN / PARTIAL /
EXPERIMENTAL

This note isolates the largest pivot-pattern class from the M1 `a=327`
reduced-intersection matrix audit:

```text
support_overlap_rref_pivot
```

The ambient row remains

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains PR #133:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` pivot-schedule audit, not an MCA `N_bad` row, and it does
not claim protocol soundness, ordinary list decoding, exact `Lambda_mu`, exact
`delta*_C`, an `a=327` certificate, a deterministic pivot theorem, or a global
upper bound at `a=327`.

## Scope

The input is the pivot-pattern theorem audit:

```text
experimental/data/m1_rim_pivot_pattern_theorem.json
```

This branch filters to the 20 support-pattern matrices whose RREF pivot
certificates use only support-overlap rows.

The source packets are:

```text
constructive_rank_defect_support_design        8
support_pattern_multiplicity_mutation_search   6
support_pattern_surrogate_rank_feedback_search 6
```

## Result

For all 20 support-pattern matrices:

```text
schedule origin:             RREF_DERIVED_PATTERN
support-overlap pivots:      all compressed variables
compressed-variable range:   19..159
route-cut certified rows:    20
deterministic schedule:      not proved
```

The aggregate support-overlap pivot-pair profile is:

```text
1,2: 569
1,3: 386
1,4: 404
1,5: 353
1,6: 189
```

The Sage audit reconstructs the 20 support-pattern reduced matrices over
`GF(17^32)`, recomputes the RREF pivot rows, verifies the selected minors have
full rank, and checks that the resulting hashes agree with the JSON ledger.

## Interpretation

This packet proves a named tested-candidate route cut:

```text
ROUTE_CUT_CERTIFIED_CANDIDATES:
  the 20 support-overlap candidates have certified full-rank RREF pivot minors.
```

It does not prove the desired deterministic theorem:

```text
For every reduced matrix in the support_overlap_rref_pivot class, a
deterministic support-overlap pivot schedule selects a full column-rank minor.
```

The reason is specific: the schedules are extracted from Sage RREF pivot rows.
No rank-free combinatorial row-ordering rule or block-triangular pivot schedule
has been verified for the class.

## Status Ledger

COMPUTATIONAL_CERTIFICATE / AUDIT:

- 20 support-pattern reduced matrices isolated;
- all 20 have support-overlap RREF pivot schedules;
- all 20 selected minors are full rank over `GF(17^32)`;
- all 20 are certified route cuts for their tested candidates;
- no positive nullity appears;
- no `a=327` interleaved-list certificate appears.

PARTIAL / OPEN:

- deterministic combinatorial support-overlap schedule remains unproved;
- no block-triangular row ordering is established;
- generic-pairwise and quotient-residual pattern classes are outside this
  packet;
- global `Lambda_mu(C,327) <= 6` remains open.

NOT CLAIMED:

- deterministic combinatorial pivot schedule;
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

The next useful move is to search for a rank-free row-ordering rule behind the
20 RREF-derived schedules. If no such rule emerges, this class should remain an
audit-level route cut and the next pivot-pattern target should be the
`generic_pairwise_rref_pivot` family.
