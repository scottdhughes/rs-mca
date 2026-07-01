# M1 a=327 scalable pairclass with [1,4,5,6,7] split

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `e99acf6`, where scalable exact pair-class creation moved
the weak pair values to:

```text
B({2,7}) = 577
B({3,7}) = 576
capacity upper bound = 384
degenerate classes = [[1,4,5,6,7],[3],[2]]
```

The live question was whether controlled split constraints for the persistent
`[1,4,5,6,7]` block could be added while continuing to grow the pair-class
geometry.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit starts from the same protected-exchange / class-creation schedule as
`e99acf6` and tests:

```text
target class size:     128
pair row extensions:   32, 64, 96
free patterns:
  d2_first_free
  d2_first4_free
  d2_even_sparse
```

For each row extension it adds one controlled split family:

```text
split_7_from_1456
split_14_567
split_145_67
chain_split_14567
```

The split rows are evaluation constraints at coordinates outside the pair-class
rows. Each case is run in a timeout-bounded Sage child process.

## Result

All 12 exact systems completed without timeout:

```text
systems tested:              12
exact vectors constructed:   36
timeouts:                    0
collapse-reduced vectors:    36
capacity-preserving vectors: 0
```

The split constraints do reduce the persistent collapse in every sampled
vector. Examples:

```text
split_7_from_1456:
  [[1,4,5,6],[7],[3],[2]]

split_14_567:
  [[1,4,6,7],[5],[3],[2]]

split_145_67:
  [[1,4,5,7],[6],[3],[2]]

chain_split_14567:
  [[1,7],[6],[5],[4],[3],[2]]
```

The pair-class rows continue to grow the weak pair values:

```text
extension 32:  B({2,7}),B({3,7}) = 561,560
extension 64:  B({2,7}),B({3,7}) = 577,576
extension 96:  B({2,7}),B({3,7}) = 593,592
```

Best retained row:

```text
pair B values          = [1024,593,592,1024,514]
capacity upper bound   = 315
collapse pattern       = [[1,4,6,7],[5],[3],[2]]
failure mode           = PAIRCLASS_SPLIT_CAPACITY_LOSS
```

The decisive negative is:

```text
capacity-preserving vectors: 0 / 36
```

So this first split-coupled layer breaks the `[1,4,5,6,7]` class, but every
tested split destroys capacity below the `327` threshold.

## Interpretation

The branch proves two exact facts at once:

```text
pair-class creation still scales: 577/576 -> 593/592
controlled split constraints really reduce the collapse class
```

But the combination fails in this row schedule because capacity falls:

```text
best capacity after split = 315 < 327
```

This is a sharper obstruction than the previous checkpoint. The issue is not
that the `[1,4,5,6,7]` class cannot be split. It can. The issue is that the
tested split families remove too much capacity-carrying value-class structure.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means this named split-coupled class-creation pass
found no exact `a>=327` witness.

`PARTIAL` means softer split placement, capacity-aware split coordinates,
larger row blocks, and additional nullspace sampling remain open.

## Failure labels

- `PAIRCLASS_GROWTH_STALLS`: `B({2,7})` and `B({3,7})` do not improve.
- `PAIRCLASS_SPLIT_INCONSISTENT`: split constraints make the exact system
  unsolvable or unproductive.
- `PAIRCLASS_SPLIT_CAPACITY_LOSS`: split works but capacity is below `327`.
- `PAIRCLASS_SPLIT_PAIR_LOSS`: split works but the weak pair values regress.
- `PAIRCLASS_SPLIT_LOW_RESCHEDULE`: pair values and capacity survive, but
  exact max-min remains below `327`.
- `PAIRCLASS_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

The next attack should keep pair-class creation, but choose split constraints
by capacity slack rather than using generic split families.

The useful target is now:

```text
pair-class extension 96 gives B({2,7}),B({3,7}) = 593,592
need split placement that keeps capacity >=327
```

So the next branch should identify capacity-critical coordinates/classes in
the scalable pairclass geometry and place split rows only off that protected
skeleton.
