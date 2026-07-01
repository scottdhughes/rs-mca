# M1 a=327 compensated split-and-replace

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `976d215`, where the coordinate-level slack selector showed
that the scalable pair-class extension-96 basin has no free split coordinates:

```text
capacity-critical coordinates: 512 / 512
pair57-critical coordinates:   512 / 512
capacity-preserving vectors:   0
best capacity upper bound:     315
```

The live question was whether a collapse-reducing split could be compensated by
one or two replacement rows that restore the capacity skeleton.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Baseline

The audit starts from the pre-split scalable pair-class system:

```text
pre-split pair B values = [1024,577,576,1024,1024]
pre-split capacity      = 384
pre-split collapse      = [[1,4,5,6,7],[3],[2]]
```

The best single split from the slack-selector basin had:

```text
post-split pair B values = [1024,593,592,1024,1024]
post-split capacity      = 315
post-split collapse      = [[1,4,5,7],[6],[3],[2]]
split gain B27/B37       = [16,16]
capacity loss            = 69
```

## Method

The compensated search tests the top five slack-ledger split candidates and
six replacement families:

```text
one_for_one_same_fiber
one_for_two_same_fiber
one_for_two_neighbor_fiber
one_for_two_balanced
one_for_two_pair57_restore
one_for_two_capacity_backfill
```

For a split such as:

```text
P_6(h) - P_1(h) = 1
```

the replacement rows try to restore capacity by forcing the split witness back
onto witness `7` at one or two other coordinates:

```text
P_6(h') = P_7(h')
```

Analogous replacement rows are used for split-`4` candidates.

## Result

All 30 exact systems completed without timeout:

```text
systems tested:              30
exact vectors constructed:   30
timeouts:                    0
pair57-preserving vectors:   30
pair27/37-improved vectors:  30
collapse-reduced vectors:    30
capacity-restored vectors:   0
```

Best retained row:

```text
pair B values          = [1024,593,592,1024,1024]
capacity upper bound   = 315
collapse pattern       = [[1,4,5,7],[6],[3],[2]]
failure mode           = COMP_SPLIT_CAPACITY_NOT_RESTORED
```

Failure count:

```text
COMP_SPLIT_CAPACITY_NOT_RESTORED: 30
```

Some two-row replacements increase the raw capacity total by one or two units,
but not enough to move the floor:

```text
capacity upper bound remains 315
target threshold is 327
```

## Interpretation

This is a stronger local obstruction than the single-split selector. The tested
compensated exchanges preserve the useful properties:

```text
B({2,7}), B({3,7}) stay at 593,592
B({5,7}) stays high
collapse remains reduced
```

But one or two replacement rows do not rebuild enough of the capacity skeleton:

```text
capacity-restored vectors: 0 / 30
```

So the current basin is not repaired by small local compensated exchanges.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means this named compensated split-and-replace pass
found no exact `a>=327` witness.

`PARTIAL` means larger compensated exchanges or upstream target redesign remain
open.

## Failure labels

- `COMP_SPLIT_CAPACITY_NOT_RESTORED`: split helps pair values but replacement
  does not restore capacity above `327`.
- `COMP_SPLIT_PAIR57_LOSS`: capacity may improve, but `B({5,7})` falls below
  `654`.
- `COMP_SPLIT_COLLAPSE_RETURNS`: replacement restores capacity by recreating
  the old collapse.
- `COMP_SPLIT_PAIR27_37_STALLS`: compensation loses the `B({2,7})` /
  `B({3,7})` gain.
- `COMP_SPLIT_LOW_RESCHEDULE`: capacity and pair guards survive, but exact
  max-min remains below `327`.
- `COMP_SPLIT_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

Small local surgery in this basin is now weak. The next local variant would
need larger compensated exchanges, but the cleaner move is upstream target
redesign:

```text
build pair-class creation systems with capacity slack above 400 before
attempting the collapse split
```

The theorem direction from this checkpoint is:

```text
in the scalable pair-class extension-96 basin, one- and two-row replacement
exchanges preserve the pair gains and low collapse but do not restore capacity
above 315.
```
