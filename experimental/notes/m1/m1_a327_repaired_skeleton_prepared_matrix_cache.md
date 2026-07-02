# M1 a=327 repaired-skeleton prepared matrix cache

Status: `PARTIAL / EXACT_INFRASTRUCTURE_LIMIT / EXPERIMENTAL`

This packet follows `1a75dfe`, which planned the compensated repaired-skeleton
split grid but timed out before constructing any compensated vector. The goal
here is to determine whether the existing exact-state replay is strong enough
to serve as a prepared matrix cache.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an infrastructure/cache audit. It is not a proof record, not an MCA
row, and not a protocol claim.

## Cached Replay Facts

The parent exact-state replay still verifies the budget-32 repaired skeleton:

```text
base source commit    = 2dfd1d9
capacity              = 333
B({1,7})..B({5,7})    = [1024,657,656,1024,1024]
collapse pattern      = [[1,4,5,7],[6],[3],[2]]
field                 = GF(17^32)
H order               = 512
```

The failed direct split remains:

```text
failed split commit   = 7a02b97
capacity              = 315
B({1,7})..B({5,7})    = [1024,593,592,512,1024]
```

## Prepared-State Manifest

The manifest records the available linear-algebra metadata:

```text
matrix shape          = [354,1536]
rank                  = 354
nullity               = 1182
fixed specs           = 129
free pattern          = d2_first_free
cache type            = RECONSTRUCTION_ONLY
```

The available parent replay gives deterministic hashes for the fixed specs,
base vector, base codeword evaluations, base value classes, and coordinate
ledger. It does not persist:

```text
pivot columns
free columns
independent row indices
row-reduced state
Sage-native matrix/echelon object
```

So this branch does not yet provide the prepared matrix cache needed by the
compensated split grid.

## Append Test

The small append test result is inherited from `1a75dfe`:

```text
planned compensated systems = 45
systems attempted           = 1
exact vectors constructed   = 0
failure                     = COMP_REPAIRED_SPLIT_TIMEOUT
timeout stage               = repaired_context GF(17^32) skeleton reconstruction
```

This should be interpreted as an infrastructure limitation, not a mathematical
failure of compensated split/replacement.

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

To make the compensated split grid feasible, the next infrastructure step must
persist actual reusable exact linear-algebra state, such as pivot/free columns,
independent row indices, or a Sage-native prepared matrix/echelon artifact.
Only after that should the `1a75dfe` compensated split grid be rerun.
