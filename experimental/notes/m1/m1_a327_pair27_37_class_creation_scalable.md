# M1 a=327 pair {2,7}/{3,7} class creation scalable solve

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `07e987c`, where exact pair-class creation first moved the
weak pair Hall values:

```text
B({2,7}): 514 -> 545
B({3,7}): 513 -> 544
capacity upper bound: 375
```

The current packet tests whether that exact mechanism scales to larger
structured `T_27/T_37` class-creation sets without dense unbounded
`GF(17^32)` echelonization.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not an
`a=327` proof record and does not update any public board row.

## Method

The audit starts from the best size-32 class-creation geometry from `07e987c`
and adds structured extension rows:

```text
P_2(h) = P_7(h) for h in extension T_27
P_3(h) = P_7(h) for h in extension T_37
```

The exact solve is run case-by-case as timeout-bounded Sage child processes,
so slow extension-field linear algebra is recorded rather than hanging the
whole audit.

First scalable pass:

```text
T sizes:                 64, 96
extension row blocks:    32, 64
designs:
  overlap_all
  same_fiber_shifted
  disjoint_low_high
case timeout:            35 seconds
free pattern:            d2_first_free
```

Each case records:

```text
row count
exact rank after row insertion
nullity after row insertion
D2 split
capacity
B({2,7}), B({3,7})
six-class dominance
degenerate classes
```

## Result

All 12 timeout-bounded exact child cases completed:

```text
systems tested:              12
timeouts:                    0
exact vectors constructed:   12
D2 split vectors:            12
low-collapse vectors:        10
```

The pair-class creation effect scales linearly in this first row-block range:

```text
block 32:
  row count:         161
  rank after:        161
  nullity after:     1375
  pair B values:     [1024,561,560,1024,1024]
  capacity:          379

block 64:
  row count:         193
  rank after:        193
  nullity after:     1343
  pair B values:     [1024,577,576,1024,1024]
  capacity:          384
```

Best result:

```text
B({2,7}) = 577
B({3,7}) = 576
capacity upper bound = 384
failure mode = PAIR_CLASS_PARTIAL_REPAIR
```

No pair target is reached:

```text
target B({2,7}), B({3,7}) >= 654
pair27 repaired vectors: 0
pair37 repaired vectors: 0
full pair repaired vectors: 0
```

All exact vectors remain degenerate:

```text
degenerate classes = [[1,4,5,6,7],[3],[2]]
```

The disjoint `block=64` cases return six-class dominance count `32`; the
overlap and same-fiber-shifted cases keep six-class dominance `0`.

## Interpretation

This is a meaningful exact improvement, but not a certificate.

The good news:

```text
structured pair-class creation scales:
  545/544 -> 577/576
while retaining:
  D2 split
  capacity >=327
  low collapse in 10/12 cases
```

The bad news:

```text
the remaining pair deficit is still 77/78 credits,
and the exact vectors still identify [1,4,5,6,7].
```

So the pair-class creation direction is still the right algebraic knob, but
the next obstruction is now sharper:

```text
large enough pair creation must be combined with nondegeneracy repair for
the [1,4,5,6,7] class.
```

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact
`GF(17^32)` witness with seven distinct degree-`<256` codewords and one
received word.

`EXACT_EXTRACTION_NO_A327` means this named scalable class-creation pass found
no exact `a>=327` witness.

`PARTIAL` means larger row blocks, additional free schedules, and
nondegeneracy-coupled pair creation remain open.

## Failure labels

- `SCALABLE_SYSTEM_TIMEOUT`: exact block solve exceeded the timeout.
- `SCALABLE_SYSTEM_FULL_RANK`: exact system had no useful sampled solution or
  failed the prepared linear solve.
- `PAIR_CLASS_PARTIAL_REPAIR`: `B({2,7})` / `B({3,7})` improve but remain
  below `654`.
- `PAIR_CLASS_CAPACITY_LOSS`: pair values improve but capacity drops below
  `327`.
- `PAIR_CLASS_UNDOES_D2_SPLIT`: exact vector collapses `[1,2]` again.
- `PAIR_CLASS_COLLAPSE_RETURNS`: six-class collapse returns.
- `PAIR_CLASS_LOW_RESCHEDULE`: pair values and capacity clear, but exact
  max-min remains below `327`.
- `PAIR_CLASS_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

The next exact attack should not return to rescheduler exchange. The classes
are still being created algebraically, and the mechanism scales.

The next target should combine:

```text
larger pair-class row blocks
additional free schedules
nondegeneracy constraints for [1,4,5,6,7]
```

The immediate question is whether the `577/576` pair values can be pushed
toward `654` while breaking the `[1,4,5,6,7]` identification rather than
waiting to split it after the pair geometry is built.
