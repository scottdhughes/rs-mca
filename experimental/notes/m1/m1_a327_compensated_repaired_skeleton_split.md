# M1 a=327 compensated repaired-skeleton split

Status: `PARTIAL / EXACT_SETUP_TIMEOUT / EXPERIMENTAL`

This packet follows `30d0cdb`, which cached the exact budget-32 repaired
skeleton and the direct `split_4_from_157` failure. The goal here was to test
whether that failed residual split can be paired with replacement rows that
restore the exact capacity and pair-Hall guards.

The branch currently records an exact setup timeout, not a mathematical
negative result: repeated exact attempts remained inside the `GF(17^32)`
budget-32 skeleton reconstruction before any compensated vector was
constructed.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is not an MCA row, not a protocol claim, and not a public-board update.

## Baseline

The source repaired skeleton is:

```text
source commit         = 30d0cdb
base skeleton commit  = 2dfd1d9
capacity              = 333
B({1,7})..B({5,7})    = [1024,657,656,1024,1024]
collapse pattern      = [[1,4,5,7],[6],[3],[2]]
```

The direct split failure from `7a02b97` is:

```text
split family          = split_4_from_157
capacity              = 315
B({1,7})..B({5,7})    = [1024,593,592,512,1024]
collapse pattern      = [[1,5,6,7],[4],[3],[2]]
```

The damage profile is:

```text
capacity loss = 18
B({2,7}) loss = 64
B({3,7}) loss = 64
B({4,7}) loss = 512
B({5,7}) loss = 0
```

So this branch treats `B({4,7})` as a first-class repair target, not merely
total capacity.

## Planned Search

The Sage audit reconstructs the exact budget-32 skeleton over `GF(17^32)`,
then tests split/replacement systems chosen from the persistent coordinate
ledger:

```text
split families: split_4_from_157, split_14_vs_57, split_1_from_457
replacement bundle sizes: 8, 16, 32
selectors: capacity_first, B27_B37_first, B47_first, balanced_repair,
           quotient_fiber_local
```

Replacement classes include:

```text
{2,7}, {3,7}, {4,7},
{2,3,7}, {2,4,7}, {3,4,7},
{4,5,7}, {1,4,7},
{1,4}, {1,4,5}, {1,4,5,7}
```

Rows that recreate the old six-class basin are not used as explicit
replacement classes.

The planned grid has `45` systems. The first attempted case was:

```text
split family              = split_4_from_157
replacement bundle size   = 8
selector                  = B47_first
```

That attempt did not return an exact vector within the practical interactive
budget because reconstruction was still in finite-field echelonization.

## Candidate Guards

A retained exact vector must preserve:

```text
capacity >= 327
B({2,7}) >= 654
B({3,7}) >= 654
B({4,7}) >= 654
B({5,7}) >= 654
D2 split
six-class dominance = 0
```

The audit only treats an exact vector with max-min agreement at least `327`
and seven distinct codewords as a candidate.

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

Do not bank a conservation theorem from this branch. The compensated split was
not actually tested to completion. The next useful infrastructure step is to
persist a stronger exact prepared state: reusable rows/pivots/free columns or a
Sage-native matrix/vector cache for the budget-32 skeleton. Then rerun this
same compensated split grid.
