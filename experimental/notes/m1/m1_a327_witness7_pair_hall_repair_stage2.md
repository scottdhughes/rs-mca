# M1 a=327 witness-7 pair Hall repair stage 2

Status: `TESTED_PAIR7_STAGE2_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `8669680`, where the first witness-7 pair Hall repair
improved the repaired tangent-skeleton bottleneck while keeping added six-class
dominance at zero.

## Baseline

Parent witness-7 pair Hall repair:

```text
proxy max-min:              315
capacity upper bound:       455
pair B values:              [631,631,631,631,631]
pair deficit to 654:        [23,23,23,23,23]
added six-class dominance:  0
old three-subset B:         [1536,1536,1536]
```

For target agreement `327`, each two-witness pair needs `2*327 = 654`
subset-credits. The live pair bottleneck remained:

```text
{1,7}, {2,7}, {3,7}, {4,7}, {5,7}
```

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is a proxy-field search over `GF(12289)`. It is not a `GF(17^32)` proof
record.

## Method

The scanner reconstructs the top three best `315` geometries from the parent
packet and applies a second-stage repair menu around those geometries.

Repair budgets:

```text
16, 24, 32, 48, 64, 96
```

Repair families:

```text
pair_i7
sliding_triple_i_i1_7
quad_i_i1_i2_7
mixed_pair_triple_7
quotient_fiber_balanced_pair7
residual_pair7
```

The scan records:

- proxy max-min;
- capacity upper bound;
- `B({1,7}),...,B({5,7})`;
- old three-subset guard values;
- total and added six-class dominance;
- failure mode.

## Result

First bounded stage-2 run:

```text
base repaired systems: 3
target systems:        108
proxy samples:         1728
proxy candidates:      0
```

All samples failed as:

```text
PAIR7_STAGE2_NOT_REPAIRED: 1728
```

Best retained sample:

```text
proxy max-min:                 314
capacity upper bound:          455
pair B values:                 [628,628,628,628,628]
pair Hall bound:               314
remaining pair deficit:        26
added six-class dominance:     0
failure mode:                  PAIR7_STAGE2_NOT_REPAIRED
```

The old three-subset guard remains safe:

```text
B({1,2,3}) = 1536
B({2,3,4}) = 1536
B({2,3,5}) = 1536
```

## Interpretation

This is a negative stage-2 checkpoint. It does not improve the first-stage
incumbent:

```text
proxy max-min:        315 -> 314
pair B:               631 -> 628
remaining deficit:     23 -> 26
capacity:             455 -> 455
added collapse:         0 -> 0
```

The useful conclusion is that the naive stage-2 repair menu does not compound
the first-stage witness-7 repair. The first-stage `315` geometry remains the
best local collapse-free pair-7 repair result.

The likely next attack is not another reconstruction-style stage-2 scan. It
should preserve the first-stage pair-repair rows as part of the protected
skeleton and then perform local additive or exchange mutations, so that the
rows responsible for `B({i,7})=631` are not displaced by the second-stage
refill step.

## Status labels

`CANDIDATE` means a proxy stage-2 witness-7 pair repair reaches `a>=327` with
low added collapse and needs exact `GF(17^32)` extraction.

`TESTED_PAIR7_STAGE2_NO_A327` means the bounded second-stage witness-7 pair
repair pass found no proxy `a>=327` candidate.

`PARTIAL` means protected-row local exchange repair, broader second-stage
menus, and exact-field lifting remain open.

## Failure labels

- `PAIR7_STAGE2_NOT_REPAIRED`: some `B({i,7})` remains below `654`.
- `PAIR7_STAGE2_COLLAPSE_RETURNS`: pair repair succeeds only by adding
  six-class dominance.
- `PAIR7_STAGE2_CAPACITY_LOSS`: pair repair increases `B({i,7})` but capacity
  drops below `327`.
- `PAIR7_STAGE2_LOW_RESCHEDULE`: pair Hall clears but proxy max-min remains
  below `327`.
- `PAIR7_STAGE2_PROXY_CANDIDATE`: proxy max-min reaches at least `327` with
  low/no added collapse.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No `GF(17^32)` proof record unless a later Sage audit verifies a candidate.
