# M1 a327 order-8 partition-first interpolation search

Status:

PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The previous order-8 degree-3 branch sampled quotient polynomials first and
then failed selected-block allocation. This branch reverses the direction:
CP-SAT chooses the eight quotient-bucket equality partitions and selected-block
counts first, then the scanner checks degree-3 interpolation over `GF(17)`.

## Method

The CP-SAT model chooses one set partition of seven witnesses for each of the
eight order-8 quotient buckets. It also chooses selected-block counts inside
each 64-point bucket.

It enforces:

```text
support_i = 327 for all seven witnesses
selected pair counts <= 255
pair-to-7 selected counts >= 142 for witnesses 1..5
ambient pair equality buckets <= 3
```

The first model asks for:

```text
equation_count <= 23
```

because degree-3 quotient interpolation has 24 variables. The fallback model
minimizes equation count under the same support and pair guards.

After CP-SAT returns a schedule, the scanner builds the exact `GF(17)`
degree-3 interpolation matrix, computes rank/nullity, checks pair projections,
and tries to construct a seven-distinct quotient vector.

## Result

The bounded run is recorded in the JSON ledger.

```text
max local partition cost = 4
partition patterns per bucket = 813
structural-defect target = INFEASIBLE
support feasibility = UNKNOWN
min-equation fallback = UNKNOWN
interpolation audit = not run
status = EXACT_EXTRACTION_NO_A327 / PARTITION_FIRST_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL
```

The rank-defect-shaped target `equation_count <= 23` is infeasible in this
bounded local partition grammar. The broader support-feasibility and
min-equation fallback models did not resolve within the 60-second-per-model
run, so this is an execution checkpoint, not a mathematical obstruction for
partition-first designs.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track partition-first quotient
  construction;
- global obstruction outside the tested order-8 partition-first interpolation
  search.
