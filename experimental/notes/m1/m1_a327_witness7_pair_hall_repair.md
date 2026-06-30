# M1 a=327 witness-7 pair Hall repair

Status: `TESTED_PAIR7_REPAIR_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `d1fd9d0`, where tangent-skeleton Hall repair moved the
proxy bottleneck from the original three-witness subsets to a much sharper
witness-7 pair family.

## Baseline

Parent tangent-skeleton repair:

```text
proxy max-min:                308
capacity upper bound:         453
six-class dominance total:    0
added six-class dominance:    0
agreement vector:             [308,308,308,308,308,308,308]
old three-subset B:           [1536,1536,1536]
```

New tight pairs:

```text
{1,7}: B=616, deficit to 654 = 38
{2,7}: B=616, deficit to 654 = 38
{3,7}: B=616, deficit to 654 = 38
{4,7}: B=616, deficit to 654 = 38
{5,7}: B=616, deficit to 654 = 38
```

For target agreement `327`, each two-witness pair needs `2*327 = 654`
subset-credits.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This remains a proxy-field search over `GF(12289)`. It is not a
`GF(17^32)` proof record.

## Method

The scanner reconstructs the best repaired tangent-skeleton value geometries
from `d1fd9d0`, then adds localized witness-7 pair repair rows while retaining
the repaired tangent skeleton.

Repair budgets:

```text
8, 16, 24, 32, 48
```

Repair families:

```text
pair_i7
triple_i_j_7
mixed_pair_triple_7
quotient_fiber_balanced_i7
residual_pair_i7
```

The scan records:

- proxy max-min;
- capacity upper bound;
- pair values `B({1,7}),...,B({5,7})`;
- old three-subset guard values;
- total and added six-class dominance.

## Result

First bounded run:

```text
base repaired systems: 5
target systems:        125
proxy samples:         2000
proxy candidates:      0
```

All samples failed as:

```text
PAIR7_NOT_REPAIRED: 2000
```

Best retained sample:

```text
proxy max-min:                 315
agreement vector:              [315,315,315,315,315,315,316]
capacity upper bound:          455
pair B values:                 [631,631,631,631,631]
pair Hall bound:               315
remaining pair deficit:        23
six-class dominance total:     0
added six-class dominance:     0
failure mode:                  PAIR7_NOT_REPAIRED
```

The old three-subset guard remains safe:

```text
B({1,2,3}) = 1536
B({2,3,4}) = 1536
B({2,3,5}) = 1536
```

## Interpretation

This is another positive diagnostic but not a candidate.

Compared with `d1fd9d0`:

```text
proxy max-min:        308 -> 315
pair B:               616 -> 631
remaining deficit:     38 -> 23
capacity:             453 -> 455
added collapse:         0 -> 0
```

The witness-7 pair repair is moving the correct bottleneck without reintroducing
collapse, but the first bounded repair layer does not clear the pair target
`B>=654`.

The next useful attack is a second-stage or higher-budget pair repair around
the best `315` geometry, rather than returning to broad target generation.

## Status labels

`CANDIDATE` means a proxy witness-7 pair repair reaches `a>=327` with
low added collapse and needs exact `GF(17^32)` extraction.

`TESTED_PAIR7_REPAIR_NO_A327` means the bounded witness-7 pair repair pass
found no proxy `a>=327` candidate.

`PARTIAL` means broader pair repair, second-stage repair, and exact-field
lifting remain open.

## Failure labels

- `PAIR7_NOT_REPAIRED`: some `B({i,7})` remains below `654`.
- `PAIR7_REPAIR_COLLAPSE_RETURNS`: pair repair succeeds only by adding
  six-class dominance.
- `PAIR7_REPAIR_CAPACITY_LOSS`: pair repair increases `B({i,7})` but capacity
  drops below `327`.
- `PAIR7_REPAIR_LOW_RESCHEDULE`: pair Hall clears but proxy max-min remains
  below `327`.
- `PAIR7_PROXY_CANDIDATE`: proxy max-min reaches at least `327` with low/no
  added collapse.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
