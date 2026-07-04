# M1 a327 quotient-subgroup rank-aware v2 structural defect

Status:

EXACT_EXTRACTION_NO_A327 / RANKAWARE_V2_NO_STRUCTURAL_DEFECT / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The structural-rank feature pass found full-column matchings for the tested
`s=8`, `s=16`, and `s=32` quotient schedules. This rank-aware v2 screen puts
the simplest structural-defect condition directly into CP-SAT:

```text
equation_count < variable_count
```

If this is feasible, structural rank is automatically below full column rank,
making the schedule a much better proxy/exact-lift target.

## Method

For each of:

```text
s = 8, 16, 32
```

the scanner runs:

1. a structural-defect target model with `equation_count <= variable_count - 1`;
2. a fallback model minimizing equation count under the usual support, pair-cap,
   and pair-to-7 guards.

## Result

The 90-second-per-model bounded run is recorded in the JSON ledger.

```text
models tested = 6
structural-defect targets found = 0
fallbacks feasible = 1
best fallback = s=8
best fallback equation count = 224
best fallback variable count = 192
best fallback proxy rank/nullity = 192/0
failure = RANKAWARE_V2_NO_STRUCTURAL_DEFECT
```

The `equation_count < variable_count` target was infeasible for `s=8`, `s=16`,
and `s=32`. The fallback model found an `s=8` schedule, but its proxy
realization is still full rank.

No Sage exact lift is attempted without a proxy-positive candidate.

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
- global obstruction outside the bounded rank-aware v2 structural-defect
  screen.
