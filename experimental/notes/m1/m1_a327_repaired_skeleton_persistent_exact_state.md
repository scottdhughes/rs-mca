# M1 a=327 repaired-skeleton persistent exact state

Status: `AUDIT / EXACT_STATE_REPLAY / PARTIAL / EXPERIMENTAL`

This packet follows `7a02b97`, which showed that a direct
`split_4_from_157` row can reduce the residual `[1,4,5,7]` class but cuts
through the repaired capacity/pair skeleton.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact-state replay/cache packet. It is not a proof record, not an
MCA row, and not a protocol claim.

## Replayed State

The source repaired skeleton is the budget-32 post-split `triple_237` geometry:

```text
source commit         = 2dfd1d9
capacity              = 333
B({1,7})..B({5,7})    = [1024,657,656,1024,1024]
collapse pattern      = [[1,4,5,7],[6],[3],[2]]
six-class dominance   = 0
```

The failed direct split from `7a02b97` is replayed as:

```text
split family          = split_4_from_157
capacity              = 315
B({1,7})..B({5,7})    = [1024,593,592,512,1024]
collapse pattern      = [[1,5,6,7],[4],[3],[2]]
failure mode          = REPAIRED_SPLIT_CAPACITY_LOSS
```

## Persisted Metadata

The Sage audit reconstructs over `GF(17^32)` and records deterministic hashes:

```text
base vector hash
base codeword-evaluation hash
base value-class hash
failed-split vector hash
failed-split codeword-evaluation hash
failed-split value-class hash
fixed row-spec hash
failed split-spec hash
coordinate-ledger hash
result hash
```

The JSON also records row counts, effective ranks, nullities, split specs, and
a compact coordinate-level before/after ledger.

Raw `GF(17^32)` elements are not serialized into dependency-free JSON. The
record persists reconstruction recipes and hashes; the Sage audit is the exact
replay layer.

## Coordinate Ledger

For every coordinate in `H`, the ledger records:

```text
coordinate index
quotient fiber
value-class pattern before/after failed split
capacity contribution before/after
B({2,7}), B({3,7}), B({4,7}), B({5,7}) before/after
split damage score
replacement priority score
```

This is intended to support the next compensated split search. The failed split
damages not only total capacity but also `B({2,7})`, `B({3,7})`, and
`B({4,7})`; later replacement rows must compensate those deficits together.

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

## Next Step

Use this replay/cache packet as the base for a compensated repaired-skeleton
split. Split rows should be treated as destructive unless paired with
replacement rows that preserve:

```text
capacity >= 327
B({2,7}) >= 654
B({3,7}) >= 654
B({4,7}) >= 654
B({5,7}) >= 654
six-class dominance = 0
```
