# M1 a327 order-8 block-count partition grammar search

Status:

EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_AMBIENT_INFEASIBLE / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The previous narrow grammar forced pair-to-7 roots as the primary seed. This
branch moves support incidence into the primary model. CP-SAT now chooses
positive selected blocks and their counts directly inside each order-8 quotient
bucket, then infers the smallest equality partition containing those selected
blocks. If the full guard model becomes feasible, the same degree-3 interpolation
audit is run afterward.

## Method

For each of the eight order-8 quotient buckets, the model chooses disjoint
positive selected blocks from all nonempty witness subsets of sizes `1..7`.
Each positive selected block has an integer count in `1..64`, and bucket counts
sum to `64`.

The diagnostic models are layered:

```text
support_only:       support_i = 327
pair7_guard:        support_i = 327 and selected pair-to-7 >= 142
pair_cap:           pair7_guard plus selected pair counts <= 255
ambient_pair_cap:   pair_cap plus ambient pair bucket counts <= 3
```

The final ambient-pair cap is the order-8 Reed-Solomon pair cap in quotient
language: a pair cannot be equal in four quotient buckets without forcing the
degree-3 quotient difference to vanish identically.

## Result

The bounded run is recorded in the JSON ledger.

```text
block sizes = 1..7
support_only = feasible
pair7_guard = feasible
pair_cap = feasible
ambient_pair_cap = infeasible
interpolation audit = not run
status = EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_AMBIENT_INFEASIBLE / PARTIAL / EXPERIMENTAL
```

The important signal is that support incidence and pair-to-7 mass are not the
problem by themselves. The obstruction appears when the order-8 ambient pair
bucket cap is imposed on disjoint selected blocks.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track block-count quotient
  grammar;
- global obstruction outside the tested order-8 block-count quotient model.
