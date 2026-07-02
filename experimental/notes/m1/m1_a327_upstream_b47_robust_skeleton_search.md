# M1 a=327 upstream B47-robust skeleton search

Status: `PARTIAL / EXPERIMENTAL`

This packet opens the next upstream constructive lane after the local
repaired-skeleton split/replacement basin was banked in `f2c7823`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is not an MCA row, not a protocol claim, not a public-board update, and
not a global obstruction theorem.

## Starting point

The local basin conservation note recorded:

```text
systems tested              = 45
exact vectors constructed   = 30
inconsistent systems        = 15
capacity-preserving vectors = 0
pair-guard-preserving       = 0
```

That route cut applies only to the tested repaired-skeleton compensated split
v2 grid.

## Why move upstream

The exhausted basin started from:

```text
capacity      = 333
B27/B37/B47/B57 = 657/656/1024/1024
collapse      = [[1,4,5,7],[6],[3],[2]]
```

The direct split and compensated split probes repeatedly reduced the residual
collapse only by destroying capacity and especially B47. The full v2 grid did
not find any tested replacement schedule that preserved:

```text
capacity >= 327
B27 >= 654
B37 >= 654
B47 >= 654
B57 >= 654
```

The next construction should therefore avoid building another skeleton whose
capacity and B47 support are concentrated in the same fragile `[1,4,5,7]`
residual class.

## Initial ledger

The scanner in this branch does not claim a new exact search. It builds a
deterministic upstream ledger from existing exact artifacts:

- the local basin conservation note;
- the reserve/pairclass co-design lineage;
- the post-split pair27/37 microrepair stage-2 lineage;
- the completed compensated split v2 probe grid.

It records source skeletons, split-probe outcomes, guard margins, and a
robustness score:

```text
min(capacity - 327,
    B27 - 654,
    B37 - 654,
    B47 - 654,
    B57 - 654)
```

The initial ledger finds no split-resilient source skeleton among the existing
exact probes. This is not a new mathematical negative; it is the handoff point
for a new upstream exact search.

## Target for the next exact pass

Search for repaired skeletons with:

```text
capacity >= 333
B27 >= 654
B37 >= 654
B47 >= 654 with slack
B57 >= 654
six-class dominance = 0 or low
residual collapse not concentrated in [1,4,5,7]
```

The core score should be split-aware, not just pre-split:

```text
min over probe splits of:
  capacity - 327
  B27 - 654
  B37 - 654
  B47 - 654
  B57 - 654
```

## Candidate directions

Prioritize skeletons whose residual collapse is already split or differently
distributed, such as:

```text
[[1,4],[5,7],[6],[3],[2]]
[[1,5],[4,7],[6],[3],[2]]
[[1,7],[4,5],[6],[3],[2]]
[[1,4,5],[7],[6],[3],[2]]
```

Candidate families for a future exact scanner:

- `quotient_fiber_buffer`
- `B47_robust_buffer`
- `split_resilient_pairclass`
- `balanced_residual_collapse`
- `triple_237_with_B47_guard`
- `alternate_collapse_selector`

Candidate split probes:

- `split_4_from_157`
- `split_14_vs_57`
- `split_1_from_457`
- `split_15_vs_47`
- `split_17_vs_45`

## Non-claims

- No `a=327` interleaved-list certificate.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No global obstruction outside the tested basin.

## Next step

Fill in an exact scanner that constructs upstream skeleton candidates and runs
cheap split probes before attempting full nondegenerate exact extraction. Do
not rerun the old compensated split v2 family without a materially new
upstream skeleton.
