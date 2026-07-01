# M1 a=327 post-split pair27/37 microrepair stage 2

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `44a03e2`, where the bounded `triple_237` budget-8
microrepair moved the active pairclass obstruction while preserving the
capacity/collapse guards:

```text
capacity              = 330
B({2,7}) / B({3,7})  = 645 / 644
B({5,7})              = 1024
collapse pattern      = [[1,4,5,7],[6],[3],[2]]
remaining deficit     = 9 / 10
```

The live question is whether continuing the same matched repair direction can
clear the final pairclass Hall gap without losing the fragile post-split
geometry.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit fixes the successful stage-1 geometry:

```text
base co-design family = quotient_fiber_buffer
base row extension    = 96
split                 = split_6_keep1457 at coordinate 1
stage-1 repair        = triple_237 budget 8
```

It then tests the same `triple_237` direction as a total-budget ladder:

```text
12, 16, 24, 32
```

Equivalently, these are additional matched `{2,7}` and `{3,7}` equality rows
on top of the budget-8 incumbent. The audit reuses a single exact
`GF(17^32)` context and evaluates every produced vector directly on `H`.

Hard guards:

```text
capacity >= 327
B({5,7}) >= 654
D2 split retained
collapse does not return to the six-class basin
old three-subset guards recorded
```

Primary objective:

```text
B({2,7}) >= 654 and B({3,7}) >= 654
```

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact
`GF(17^32)` witness with seven distinct degree-`<256` codewords and one
received word.

`EXACT_EXTRACTION_NO_A327` means this named stage-2 microrepair pass found no
exact `a>=327` witness.

`PARTIAL` means alternate post-split repair families, nullspace sampling, and
larger exact schedules remain open.

## Result

The total-budget ladder was productive:

```text
total triple_237 budget 12:
  capacity = 331
  B27/B37 = 647/646

total triple_237 budget 16:
  capacity = 331
  B27/B37 = 649/648

total triple_237 budget 24:
  capacity = 332
  B27/B37 = 653/652

total triple_237 budget 32:
  capacity = 333
  B27/B37 = 657/656
  B57 = 1024
  pair Hall bound = 328
  collapse pattern = [[1,4,5,7],[6],[3],[2]]
```

The budget-32 case clears the pairclass Hall targets:

```text
B({2,7}) >= 654
B({3,7}) >= 654
B({5,7}) >= 654
capacity >= 327
six-class dominance = 0
```

It is still not an exact witness, because the produced codeword tuple remains
degenerate:

```text
distinct_codewords = false
degenerate classes = [[1,4,5,7],[6],[3],[2]]
exact max-min      = null
```

So this branch clears the local pair Hall obstruction. The next obstruction is
nondegeneracy/rescheduling inside the repaired post-split skeleton, not
capacity or B27/B37 pairclass mass.

## Failure labels

- `MICROREPAIR_STAGE2_PAIRCLASS_NOT_REPAIRED`: B27/B37 remain below `654`.
- `MICROREPAIR_STAGE2_CAPACITY_LOSS`: B27/B37 improve, but capacity drops
  below `327`.
- `MICROREPAIR_STAGE2_PAIR57_LOSS`: `B({5,7})` drops below `654`.
- `MICROREPAIR_STAGE2_COLLAPSE_RETURNS`: repair succeeds only by returning
  collapse.
- `MICROREPAIR_STAGE2_LOW_RESCHEDULE`: capacity and pair guards clear, but
  exact max-min remains below `327`.
- `MICROREPAIR_STAGE2_EXACT_CANDIDATE`: exact max-min reaches at least `327`.
- `MICROREPAIR_STAGE2_TIMEOUT`: exact solve did not finish inside the case
  budget.

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
