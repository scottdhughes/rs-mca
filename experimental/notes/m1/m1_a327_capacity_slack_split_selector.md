# M1 a=327 capacity-slack split selector

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `395e7e0`, where fixed protected split families preserved
`{5,7}` in some exact vectors but still lost global capacity:

```text
best pair B values      = [1024,593,592,1024,1024]
best capacity upper     = 315
best collapse pattern   = [[1,4,5,7],[6],[3],[2]]
failure counts:
  SPLIT_CAPACITY_LOSS:    27
  SPLIT_DESTROYS_PAIR57:  18
```

The live question was whether an exact coordinate-level ledger could find
actual slack coordinates for split placement, instead of using fixed split
families.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit builds an exact coordinate ledger from the scalable pair-class
extension-96 schedule:

```text
base system: scalable_pairclass_overlap_all_extension96
B({2,7}),B({3,7}) before split: 593,592
```

For every coordinate it records:

```text
value-class pattern
capacity contribution
B({2,7}), B({3,7}), B({5,7}) contribution
quotient fiber
capacity-critical flag
pair57-critical flag
candidate split rows and local split-safe score
```

Then it tests slack-ranked split rows with:

```text
split location budgets: 8, 16, 32
selectors:
  greedy
  pair27_weighted
  pair37_weighted
  capacity_safe
free patterns:
  d2_first_free
  d2_first4_free
  d2_even_sparse
```

Each selected split system is solved and evaluated over `GF(17^32)`.

## Ledger result

The coordinate ledger is the main diagnostic:

```text
coordinates:              512
capacity-critical count:  512
pair57-critical count:    512
split-safe candidates:    860
retained candidate rows:  96
retained score range:     0 only
```

So there are many split rows that look locally safe in the weak sense that
they preserve `{5,7}` and reduce collapse, but none have positive slack. Every
retained candidate pays one unit of local capacity damage and gives no local
`B({2,7})` / `B({3,7})` gain.

## Exact selector result

All 12 selected exact systems completed without timeout:

```text
systems tested:                 12
split rows tested:              12
exact vectors constructed:      36
timeouts:                       0
pair57-preserving vectors:      36
pair27/37-improved vectors:     36
collapse-reduced vectors:       36
capacity-preserving vectors:    0
```

All selector objectives chose the same least-damaging row:

```text
P_6(h) - P_1(h) = 1 at coordinate h = 1
```

Best retained row:

```text
pair B values          = [1024,593,592,1024,1024]
capacity upper bound   = 315
collapse pattern       = [[1,4,5,7],[6],[3],[2]]
failure mode           = SPLIT_SELECTOR_CAPACITY_LOSS
```

Failure count:

```text
SPLIT_SELECTOR_CAPACITY_LOSS: 36
```

## Interpretation

This is a clean exact obstruction for the current scalable pair-class basin.
The issue is not merely that a hand-designed split family cut through `{5,7}`.
The ledger says the whole coordinate set is capacity-critical and pair57
critical in this base geometry:

```text
capacity-critical coordinates: 512 / 512
pair57-critical coordinates:   512 / 512
```

Even the best locally safe split rows have no positive slack, and exact solving
returns the same capacity wall:

```text
capacity upper bound = 315 < 327
```

So the current target-system basin appears to have no coordinate-level slack
for this style of collapse-reducing split placement.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means this named slack-selector pass found no exact
`a>=327` witness.

`PARTIAL` means other target-system basins, multi-row split selectors, and
different pair-class schedules remain open.

## Failure labels

- `NO_SPLIT_SAFE_COORDINATES`: ledger finds no candidate split rows.
- `SPLIT_SELECTOR_CAPACITY_LOSS`: selected split rows reduce capacity below
  `327`.
- `SPLIT_SELECTOR_PAIR57_LOSS`: `B({5,7})` falls below `654`.
- `SPLIT_SELECTOR_PAIR27_37_STALLS`: `B({2,7})` / `B({3,7})` do not improve.
- `SPLIT_SELECTOR_COLLAPSE_NOT_REDUCED`: collapse pattern is unchanged.
- `SPLIT_SELECTOR_LOW_RESCHEDULE`: capacity and pair guards survive, but exact
  max-min remains below `327`.
- `SPLIT_SELECTOR_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

The next attack should stop trying single-coordinate split placement in this
same basin. The useful options are:

```text
multi-row compensated split selectors that add replacement capacity rows, or
return to target-system design so pair-class creation does not make every
coordinate capacity-critical before the collapse split is attempted.
```

If a theorem direction is wanted, this checkpoint supports:

```text
inside the scalable pair-class extension-96 basin, every locally safe
collapse-reducing split row is still capacity-critical, and the sampled exact
slack selectors all fall to capacity 315.
```
