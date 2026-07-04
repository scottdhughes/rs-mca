# M1 a327 quotient-subgroup primal-kernel codesign

Status:

PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The prior quotient-subgroup front found feasible support schedules, but the
realization and rank-aware screens stayed full rank. This branch stops
post-hoc schedule mutation and moves the dependency into the primal
codeword-difference model first.

The tested family is an order-8 quotient construction in characteristic 17:

```text
g_i(X) = c_i * prod_{r in R_i}(X^64 - r)
```

where each `R_i` is a three-root subset of the order-8 quotient. This makes
each nonbaseline witness agree with witness 7 on three 64-point buckets before
CP-SAT allocates selected received-word blocks.

## Method

The scanner runs two gates:

1. a conservative root-bucket CP-SAT model using only zero blocks and
   singleton blocks;
2. concrete locator-cubic instantiations over `GF(17)` followed by selected
   block allocation on the actual equality partitions.

This is dependency-engineered because the equality rows come from explicit
degree-192 polynomials in `X^64`, not from a support schedule later hoped to
have rank defect.

## Result

The bounded run is recorded in the JSON ledger.

```text
root geometry feasible = false
locator attempts = 500
locator feasible allocations = 0
best failure = PRIMAL_KERNEL_SELECTED_ALLOCATION_INFEASIBLE
status = EXACT_EXTRACTION_NO_A327 / PRIMAL_KERNEL_CODESIGN_NO_ALLOCATION / PARTIAL / EXPERIMENTAL
```

The conservative zero/singleton root-bucket model was infeasible. The scanner
then tested 500 concrete three-root locator-cubic instantiations over `GF(17)`;
none admitted a selected-block allocation meeting support 327, pair caps, and
pair-to-7 guards.

## Interpretation

This is a local obstruction for the tested order-8 three-root locator family.
It does not close the broader primal-kernel route. The next generator should
allow richer degree-3 quotient codewords or design the eight quotient-bucket
partitions directly and then solve the degree-3 interpolation constraints.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track quotient-subgroup
  construction;
- global obstruction outside the tested order-8 primal-kernel codesign family.
