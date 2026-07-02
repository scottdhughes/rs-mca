# M1 a=327 local basin conservation note

Status: `AUDIT / ROUTE_CUT_LOCAL_BASIN / EXPERIMENTAL`

This note banks a local negative exact-search checkpoint for the M1 `a=327`
interleaved-list lane. It summarizes the repaired-skeleton split/replacement
basin after the full compensated split v2 grid completed.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is a local route cut for the tested exact repaired-skeleton basin. It is
not an MCA row, not a protocol claim, not a public-board update, and it is not
a global obstruction theorem.

## Baseline repaired skeleton

The tested basin starts from the repaired budget-32 skeleton:

```text
capacity        = 333
pair B values   = [1024,657,656,1024,1024]
pair Hall bound = 328
six-class dom.  = 0
collapse        = [[1,4,5,7],[6],[3],[2]]
```

This skeleton had cleared the earlier local capacity and pair-Hall thresholds,
but still had the residual degenerate class `[1,4,5,7]`.

## Failed direct split damage

The direct split attempt `split_4_from_157` reduced the residual class but cut
through the repaired skeleton:

```text
capacity 333 -> 315   loss 18
B27      657 -> 593   loss 64
B37      656 -> 592   loss 64
B47     1024 -> 512   loss 512
B57     1024 -> 1024  loss 0
```

The large B47 loss made B47 repair a first-class constraint in the compensated
v2 grid.

## Infrastructure used

The v2 grid used the Sage-native repaired-skeleton cache from `c181b13` and the
batched runner from `c491cdb`. The runner executed one Sage case per subprocess
with external timeouts and atomic per-case JSON output.

The full-grid data was committed in `62c15cc`.

## Full v2 grid result

The full compensated split v2 grid completed:

```text
systems tested              = 45 / 45
timeouts                    = 0
exact vectors constructed   = 30
inconsistent systems        = 15
capacity-preserving vectors = 0
pair-guard-preserving       = 0
partial-split vectors       = 30
nondegenerate vectors       = 3
```

Failure counts:

```text
COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED = 30
COMP_REPAIRED_SPLIT_INCONSISTENT          = 15
```

Best aggregate vector:

```text
capacity        = 174
pair B values   = [583,657,656,524,524]
collapse        = [[4,5],[7],[6],[3],[2],[1]]
failure mode    = COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED
```

## Local conservation diagnosis

In the tested exact repaired-skeleton basin, the recorded split/replacement
schedules did not simultaneously preserve:

```text
capacity >= 327
B27 >= 654
B37 >= 654
B47 >= 654
B57 >= 654
reduced residual collapse from [1,4,5,7]
```

The observed local tradeoff is that every constructed exact vector from the
full v2 grid reduced the residual collapse only at the cost of falling below
the capacity guard, while the remaining systems were inconsistent.

## What remains open

This note does not rule out:

- different repaired skeletons;
- larger replacement bundles;
- different split families;
- upstream target systems with more slack;
- nonlocal quotient-fiber redesigns;
- a different `a=327` construction;
- any global statement about `Lambda_mu(C,327)`.

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

## Next direction

Do not keep rerunning this compensated split v2 family. A plausible next
constructive branch should move upstream and search for a B47-robust repaired
skeleton where either B47 is not fragile under split, or `[1,4,5,7]` is never
the residual collapse class.
