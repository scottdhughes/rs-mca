# M1 a=327 compensated repaired-skeleton split v2 batched runner

Status: `EXACT_INFRASTRUCTURE / PARTIAL / EXPERIMENTAL`

This packet adds batching infrastructure for the cached compensated
repaired-skeleton split v2 grid from `4eb9b1a`. The mathematical search target
is unchanged: run the 45 exact split/replacement cases through the
Sage-native budget-32 repaired-skeleton cache and test whether any case
preserves the capacity and pair-Hall guards while reducing the residual
`[1,4,5,7]` collapse.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is not an MCA row, not a protocol claim, and not a public-board update.

## Why batching is needed

Commit `4eb9b1a` proved that cached exact append solving works and writes
resumable JSON, but the full 45-case grid is too brittle as one long Sage
process. The current bottleneck is per-case residual solving over
`GF(17^32)`, especially projection and solve work around:

```text
pivot_inverse * free_matrix
```

This branch therefore runs one case per Sage subprocess with an external
wall-clock timeout.

## Added workflow

The runner is:

```text
experimental/scripts/run_m1_a327_compensated_repaired_skeleton_split_v2_batch.py
```

The merger is:

```text
experimental/scripts/merge_m1_a327_compensated_repaired_skeleton_split_v2_results.py
```

The Sage audit now supports:

```text
--case-index N
--case-range START:END
--list-cases
```

Per-case files are written atomically under:

```text
experimental/data/m1_a327_compensated_repaired_skeleton_split_v2_cases/
```

and merged back into:

```text
experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json
```

## Case order

The case order is priority-first, with the known B47 damage targeted early:

```text
split_4_from_157 + B47_first + bundle 32
split_4_from_157 + balanced_repair + bundle 32
split_4_from_157 + quotient_fiber_local + bundle 32
split_4_from_157 + B47_first + bundle 16
split_4_from_157 + balanced_repair + bundle 16
split_14_vs_57 + B47_first + bundle 32
split_14_vs_57 + balanced_repair + bundle 32
split_1_from_457 + B47_first + bundle 32
```

The remaining cases then sweep the full 45-system grid.

## Priority Batch Result

The first priority batch `--cases 0:8 --timeout-seconds 1800` completed with
no timeouts:

```text
systems tested              = 8 / 45
timeouts                    = 0
exact vectors constructed   = 6
capacity-preserving vectors = 0
pair-guard-preserving       = 0
partial-split vectors       = 6
nondegenerate vectors       = 1
best failure                = COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED
best capacity               = 182
best pair values            = [581,657,656,521,581]
best collapse pattern       = [[1,5],[7],[6],[4],[3],[2]]
```

Case failures:

```text
COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED = 6
COMP_REPAIRED_SPLIT_INCONSISTENT          = 2
```

This is a useful local negative for the B47-priority front of the queue, but
not a mathematical route cut. The remaining 37 cases must run before any local
conservation note is justified.

## Non-claims

- No `a=327` interleaved-list certificate.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.

## Next step

Run the prioritized cases in batches with realistic timeouts, then merge and
verify the aggregate JSON. Only after all 45 cases have run should this basin
be considered for a local conservation note.
