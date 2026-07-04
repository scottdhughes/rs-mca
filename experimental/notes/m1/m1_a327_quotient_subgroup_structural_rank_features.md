# M1 a327 quotient-subgroup structural-rank features

Status:

EXACT_EXTRACTION_NO_A327 / STRUCTURAL_RANK_FULL_COLUMN_MATCHING / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The long CP-SAT front made `s=8`, `s=16`, and `s=32` count-feasible, but
their first proxy realization screens were full rank. This packet adds cheap
structural diagnostics before finite-field rank:

- equation count;
- active partition count;
- row-support diversity;
- quotient residue histograms;
- bipartite row-variable maximum matching size;
- full-column matching status.

## Interpretation

If a labelled quotient schedule has a full-column structural matching, then a
generic realization matrix can be full rank before any field arithmetic is
used. Such a schedule is not a good exact-lift target unless it has additional
algebraic symmetry not visible in the support pattern.

The useful target is:

```text
structural rank < variable count
```

That would not prove a witness, but it would give a rank-defect target worth
proxy-ranking and then, if pair projections clear, Sage-auditing.

## Result

The bounded structural-rank feature run is recorded in the JSON ledger.

```text
screens tested = 3
structural-positive screens = 0
best s = 32
best structural rank = 48
best variable count = 48
best structural nullity upper bound = 0
best equation count = 59
best label = grouped_baseline
failure = STRUCTURAL_RANK_FULL_COLUMN_MATCHING
```

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track quotient-subgroup proxy;
- global obstruction outside the tested structural-rank diagnostics.
