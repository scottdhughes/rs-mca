# M1 a=327 capacity-skeleton protected split placement

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `6aa1f9e`, where scalable pair-class creation plus
controlled `[1,4,5,6,7]` splitting reached:

```text
B({2,7}),B({3,7}) = 593,592
B({5,7})           = 514
capacity upper bound = 315
collapse pattern     = [[1,4,6,7],[5],[3],[2]]
failure mode         = PAIRCLASS_SPLIT_CAPACITY_LOSS
```

The live question was whether split placement could preserve the capacity
skeleton, especially the `{5,7}` pair, while still reducing the persistent
collapse block.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit starts from the scalable pair-class schedule and tests split families
that keep witness `7` attached to capacity-carrying classes where possible:

```text
target class size:     128
pair row extensions:   32, 64, 96
free patterns:
  d2_first_free
  d2_first4_free
  d2_even_sparse
split families:
  keep_57_split_146_vs_57
  keep_567_split_14_vs_567
  keep_1457_split_6
  keep_157_split_46
  capacity_slack_only
```

Each exact system is run as a timeout-bounded Sage child process. Every
constructed vector is evaluated directly on `H` for capacity, pair Hall values,
degenerate classes, and exact rescheduler data.

## Result

All 15 exact systems completed without timeout:

```text
systems tested:                 15
exact vectors constructed:      45
timeouts:                       0
collapse-reduced vectors:       45
pair57-preserving vectors:      27
pair27/37-improved vectors:     15
capacity-preserving vectors:    0
```

Best retained row:

```text
pair B values          = [1024,593,592,1024,1024]
capacity upper bound   = 315
collapse pattern       = [[1,4,5,7],[6],[3],[2]]
failure mode           = SPLIT_CAPACITY_LOSS
```

The failure split is:

```text
SPLIT_CAPACITY_LOSS:     27
SPLIT_DESTROYS_PAIR57:   18
```

## Interpretation

The protected placement did what it was supposed to do locally:

```text
B({5,7}) can be preserved at 1024
the collapse block can be reduced
B({2,7}),B({3,7}) can stay at 593,592
```

But none of the protected split placements preserved the global capacity
threshold:

```text
capacity-preserving vectors: 0 / 45
best capacity after protected split = 315 < 327
```

So the obstruction is sharper than the previous checkpoint. The issue is no
longer only that splitting sacrifices `{5,7}`. Even split placements that
preserve `{5,7}` and reduce collapse still lose enough global capacity to fall
below the `327` threshold.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means this named protected split-placement pass
found no exact `a>=327` witness.

`PARTIAL` means other split placements, nullspace schedules, and target
systems in this family remain open.

## Failure labels

- `SPLIT_DESTROYS_PAIR57`: `B({5,7})` drops below `654`.
- `SPLIT_CAPACITY_LOSS`: pair guards may survive, but capacity is below `327`.
- `SPLIT_DOES_NOT_REDUCE_COLLAPSE`: collapse pattern is unchanged.
- `SPLIT_PAIR27_37_STALLS`: `B({2,7})` / `B({3,7})` do not improve.
- `SPLIT_LOW_RESCHEDULE`: capacity and pair guards survive, but exact max-min
  remains below `327`.
- `SPLIT_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

## Next target

The next attack should stop using fixed split families and instead derive
split placements from a coordinate-level capacity ledger. The useful question
is whether there are split coordinates where:

```text
B({2,7}),B({3,7}) stay near 593,592
B({5,7}) stays >=654
capacity stays >=327
collapse is still reduced
```

If no such coordinates exist, the theorem target becomes a local obstruction:
inside this scalable pair-class basin, reducing the collapse while preserving
the pair guards still forces global capacity below `327`.
