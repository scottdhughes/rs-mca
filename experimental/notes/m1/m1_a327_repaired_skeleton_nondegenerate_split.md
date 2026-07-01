# M1 a=327 repaired-skeleton nondegenerate split

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `2dfd1d9`, where the post-split `triple_237` stage-2
ladder cleared the local pair Hall obstruction:

```text
capacity             = 333
B({2,7}) / B({3,7}) = 657 / 656
B({5,7})             = 1024
pair Hall bound      = 328
six-class dominance  = 0
collapse pattern     = [[1,4,5,7],[6],[3],[2]]
```

The remaining obstruction is degeneracy of the repaired skeleton, specifically
the residual class `[1,4,5,7]`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence. It is not an MCA row, not a
protocol claim, and not a public proof record.

## Method

The audit reconstructs the budget-32 repaired skeleton from the prior exact
stage-2 audit, builds a coordinate ledger from the exact value-class geometry,
and only then places split constraints.

For each coordinate it records:

```text
value-class pattern
capacity contribution
B({2,7}), B({3,7}), B({5,7}) contribution
capacity / pair critical flags
split-safe score
```

The first exact pass tests guarded split families:

```text
split_14_vs_57
split_4_from_157
split_1_from_457
split_15_vs_47
```

with small pin budgets and three deterministic free schedules. The split rows
use nonzero evaluation offsets, so they attempt to split the residual class
rather than merely restating an equality.

Hard guards:

```text
capacity >= 327
B({2,7}) >= 654
B({3,7}) >= 654
B({5,7}) >= 654
D2 split retained
six-class collapse does not return
```

## Result

The first reduced exact pass tested the top retained
`split_4_from_157` row. It did reduce the residual class, but it did not
preserve the repaired skeleton:

```text
systems tested              = 1
exact vectors constructed   = 1
partial split vectors       = 1
nondegenerate vectors       = 0
capacity-preserving vectors = 0

best capacity               = 315
best pair values            = [1024,593,592,512,1024]
best collapse pattern       = [[1,5,6,7],[4],[3],[2]]
best failure mode           = REPAIRED_SPLIT_CAPACITY_LOSS
```

The coordinate ledger is also informative:

```text
coordinates             = 512
capacity-critical       = 512
B({2,7})-critical       = 145
B({3,7})-critical       = 144
B({5,7})-critical       = 512
syntactic split-safe rows = 730
```

So a direct split can reduce `[1,4,5,7]`, but the tested exact split row
falls back to the earlier capacity-loss geometry. This remains a local
negative checkpoint, not a proof record.

## Failure labels

- `REPAIRED_SPLIT_NOT_DISTINCT`: split does not reduce the residual
  degeneracy.
- `REPAIRED_SPLIT_PARTIAL_DISTINCT`: the residual class is reduced but the
  tuple is still not seven distinct codewords.
- `REPAIRED_SPLIT_CAPACITY_LOSS`: capacity drops below `327`.
- `REPAIRED_SPLIT_PAIR27_37_LOSS`: `B({2,7})` or `B({3,7})` falls below
  `654`.
- `REPAIRED_SPLIT_PAIR57_LOSS`: `B({5,7})` falls below `654`.
- `REPAIRED_SPLIT_COLLAPSE_RETURNS`: six-class collapse returns.
- `REPAIRED_SPLIT_LOW_RESCHEDULE`: pair/capacity guards clear and distinctness
  improves, but exact max-min remains below `327`.
- `REPAIRED_SPLIT_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

## Promotion rule

A public row requires all of:

```text
seven distinct degree<256 codewords
one received word on H
agreement >=327 for all seven
Sage audit over GF(17^32)
mca_counted = false
```

Until then, this remains local experimental material.
