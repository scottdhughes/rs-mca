# M1 a=327 post-split pair27/37 microrepair

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `6c54e44`, the reserve/pairclass co-design checkpoint.
That branch crossed the post-split capacity wall but left a narrow pairclass
deficit:

```text
post-split capacity       = 329
post-split pair B values  = [1024,641,640,1024,1024]
B({2,7}) deficit to 654   = 13
B({3,7}) deficit to 654   = 14
collapse pattern          = [[1,4,5,7],[6],[3],[2]]
```

The live question is whether a small post-split repair layer can add those
last pair credits without sacrificing the newly achieved capacity margin.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is exact `GF(17^32)` experimental evidence only. It is not a public proof
record and does not update any board row.

## Method

The audit replays the known best co-design case:

```text
base row family        = quotient_fiber_buffer
base row extension     = 96
split                  = split_6_keep1457 at coordinate 1
```

It then builds an exact post-split coordinate ledger from that vector. The
bounded committed audit runs the most direct matched repair:

```text
triple_237, budget 8
```

This imposes matched `{2,7}` and `{3,7}` equalities on four post-split
coordinates. The wider planned grid remains:

```text
pair27_micro
pair37_micro
balanced_pair27_37_micro
triple_237
postsplit_survivor_pair_micro
quotient_fiber_pair27_37_micro
```

The tested repair budgets are:

```text
8
```

The planned larger budgets are:

```text
16, 24, 32
```

The primary objective is:

```text
maximize min(B({2,7}), B({3,7}))
```

with hard guards:

```text
capacity >= 327
B({5,7}) >= 654
D2 split retained
collapse remains reduced
no six-class collapse return
```

The repair layer is intentionally narrow. It does not reopen the broad
capacity-buffer search, and it does not optimize MCA/protocol quantities.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact
`GF(17^32)` witness with seven distinct degree-`<256` codewords and one
received word.

`EXACT_EXTRACTION_NO_A327` means this named microrepair pass found no exact
`a>=327` witness.

`PARTIAL` means larger repair families, additional exact free schedules, and
alternate post-split row selectors remain open.

## Bounded result

The checked `triple_237` budget-8 microrepair preserved the useful geometry and
moved the weak pairs in the right direction:

```text
baseline capacity      = 329
baseline B27/B37       = 641 / 640
microrepair capacity   = 330
microrepair B27/B37    = 645 / 644
B27/B37 deficit        = 9 / 10
B57                    = 1024
collapse pattern       = [[1,4,5,7],[6],[3],[2]]
failure mode           = MICROREPAIR_PAIRCLASS_NOT_REPAIRED
```

So this branch does not produce an exact a=327 certificate, but it confirms
that a matched `{2,3,7}` post-split microrepair can add exact pairclass mass
without losing the fragile capacity/collapse skeleton.

## Failure labels

- `MICROREPAIR_PAIRCLASS_NOT_REPAIRED`: B27/B37 remain below `654`.
- `MICROREPAIR_CAPACITY_LOSS`: B27/B37 improve, but capacity drops below
  `327`.
- `MICROREPAIR_PAIR57_LOSS`: `B({5,7})` drops below `654`.
- `MICROREPAIR_COLLAPSE_RETURNS`: repair succeeds only by returning collapse.
- `MICROREPAIR_LOW_RESCHEDULE`: capacity and pair guards clear, but exact
  max-min remains below `327`.
- `MICROREPAIR_EXACT_CANDIDATE`: exact max-min reaches at least `327`.
- `MICROREPAIR_TIMEOUT`: exact solve did not finish inside the case budget.

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
