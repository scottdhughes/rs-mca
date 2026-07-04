# M1 a327 multiscale block-count quotient search

Status:

EXACT_EXTRACTION_NO_A327 / MULTISCALE_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The order-8 block-count quotient model isolated its obstruction at the ambient
pair bucket cap. This branch moves off order 8 and tests the same block-count
first model at order 16 and order 32.

The quotient parameters are:

```text
order 16: bucket size 32, quotient degree bound 7, quotient field GF(17)
order 32: bucket size 16, quotient degree bound 15, quotient field GF(17^2)
```

The ambient pair bucket cap is the quotient Reed-Solomon liftability cap: a
pair can be equal in at most `degree_bound` quotient buckets unless the quotient
difference is forced to vanish.

## Method

For each quotient order, CP-SAT solves four diagnostic models:

```text
support_only
pair7_guard
pair_cap
ambient_pair_cap
```

If the fully constrained model is feasible, the scanner builds the exact
quotient interpolation matrix over the stated quotient field, computes
rank/nullity, checks pair projections, and tries to construct a seven-distinct
quotient vector. A Sage `GF(17^32)` lift/audit is still not claimed here.

## Result

The bounded run is recorded in the JSON ledger.

```text
order 16:
  ambient pair cap feasible = true
  interpolation matrix = 58 x 48 over GF(17)
  rank/nullity = 48 / 0

order 32:
  ambient pair cap feasible = true
  interpolation matrix = 114 x 96 over GF(17^2)
  rank/nullity = 96 / 0

status = EXACT_EXTRACTION_NO_A327 / MULTISCALE_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL
```

The useful signal is that moving off order 8 removes the ambient pair-bucket
infeasibility, but the first block-count schedules found at order 16 and order
32 are algebraically full-rank at the quotient interpolation layer.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track multiscale quotient search;
- global obstruction outside the tested quotient block-count models.
