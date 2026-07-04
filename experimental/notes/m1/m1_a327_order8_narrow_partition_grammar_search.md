# M1 a327 order-8 narrow partition grammar search

Status:

EXACT_EXTRACTION_NO_A327 / NARROW_GRAMMAR_NO_SUPPORT_SCHEDULE / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The full partition-first CP-SAT model is now modeled correctly, but the broad
support-feasibility search leaves too much symmetry unresolved. This branch
adds constructive seeds and a narrower partition grammar before running the
same degree-3 interpolation audit.

## Method

The grammar fixes pair-to-7 root buckets first. For each guarded witness
`1..5`, exactly three of the eight order-8 quotient buckets place that witness
in the selected zero block with witness `7`. This is the smallest ambient
bucket count capable of reaching the pair-to-7 guard:

```text
2 buckets * 64 = 128 < 142
3 buckets * 64 = 192 >= 142
```

Within each quotient bucket, CP-SAT chooses only a bounded residual grammar:

```text
zero block: [7] plus the seeded guarded witnesses for that bucket
residual blocks: bounded-cost set partitions of the non-zero witnesses
```

The model enforces:

```text
support_i = 327 for all seven witnesses
selected pair counts <= 255
pair-to-7 selected counts >= 142 for witnesses 1..5
ambient pair equality buckets <= 3
```

Any feasible schedule is sent to the existing order-8 `GF(17)` degree-3
interpolation audit. No Sage `GF(17^32)` exact lift is claimed in this branch.

## Result

The bounded run is recorded in the JSON ledger.

```text
root patterns tested = 512
residual grammar = bounded5
models tested = 512
CP-SAT statuses = 512 INFEASIBLE, 0 UNKNOWN
feasible support schedules = 0
interpolation audits = 0
status = EXACT_EXTRACTION_NO_A327 / NARROW_GRAMMAR_NO_SUPPORT_SCHEDULE / PARTIAL / EXPERIMENTAL
```

This branch should be read as a seeded support-feasibility route cut for the
tested zero-block narrow grammar, not as a public-row proof.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track narrow partition grammar;
- global obstruction outside the tested order-8 narrow partition grammar.
