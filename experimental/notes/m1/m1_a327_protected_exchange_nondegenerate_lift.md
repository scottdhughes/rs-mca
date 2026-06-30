# M1 a=327 protected-exchange nondegenerate lift

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `a2d31ee`, where bounded exact `GF(17^32)` lifts of the
protected-exchange proxy candidates all landed in degenerate codeword tuples.

## Baseline

Prior exact audit:

```text
proxy candidates tested:      2
exact vectors constructed:    26
nondegenerate vectors:        0
best exact max-min:           287
best capacity upper bound:    447
best pair B values:           [575,575,575,575,575]
best failure mode:            DEGENERATE_CODEWORDS
```

The proxy candidate from `c9f2e4c` remains:

```text
proxy max-min:                335
proxy agreement vector:       [335,335,335,335,335,335,336]
proxy pair B values:          [671,671,671,671,671]
added six-class dominance:    0
```

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact `GF(17^32)` extraction experiment. It is not a proof record.

## Method

The Sage audit keeps the protected-exchange row schedule and adds affine
evaluation separation pins before solving:

```text
M_exact x = 0
P_i(h) - P_j(h) = gamma
```

The first bounded pass uses the protected-plus-exchange row schedule and six
pin families:

```text
one_pair_13
chain_6class
anchor_split_34567
pair7_preserving_chain
quotient_representative_split
two_pair_balanced_split
```

Pin coordinates are chosen outside the selected target rows when possible and
spread across quotient fibers.

## Result

First bounded nondegenerate-lift pass:

```text
pin sets tested:                         12
exact vectors constructed:               12
nondegenerate vectors:                   0
capacity-preserving nondegenerate:       0
best exact max-min:                      null
best capacity upper bound:               438
best pair B values:                      [1024,1024,512,1024,1024]
best failure mode:                       PIN_DOES_NOT_SPLIT
```

The pins do split parts of the degenerate class, but no tested pin set gives
seven distinct codewords. Representative degeneracy patterns:

```text
one_pair_13:
  [[1,2,4,5,6,7], [3]]

two_pair_balanced_split:
  [[1,2,5,6,7], [4], [3]]

chain_6class:
  [[1,2,7], [6], [5], [4], [3]]

anchor_split_34567:
  [[1,2], [7], [6], [5], [4], [3]]
```

The strongest splits break most of the collapse but leave witnesses `1` and
`2` identified and lose too much capacity.

## Interpretation

This is a sharper exact negative than `a2d31ee`.

Evaluation pins can force partial splitting inside the protected-exchange row
schedule, but the tested affine solves still do not produce seven distinct
exact codewords. The exact obstruction is now concentrated in the residual
collapse of witnesses `1` and `2` after stronger splitting.

The next exact attack should target that residual `[1,2]` collapse directly,
while preserving the capacity and pair-7 repair obtained before the final
anchor-style split destroys capacity.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means the bounded pinned exact lift found no
exact `a>=327` witness.

`PARTIAL` means other pin schedules, exact nullspace sampling, and residual
collapse-directed lifts remain open.

## Failure labels

- `PIN_INCONSISTENT`: no exact solution under the pins.
- `PIN_DOES_NOT_SPLIT`: the exact vector remains degenerate.
- `PIN_SPLITS_CAPACITY_LOSS`: the vector is nondegenerate but capacity drops
  below `327`.
- `PIN_SPLITS_PAIR7_LOSS`: pair-7 repair falls below the `B>=654` target.
- `PIN_SPLITS_LOW_RESCHEDULE`: pair/capacity survive, but exact max-min is
  below `327`.
- `EXACT_CANDIDATE_A327`: exact max-min reaches at least `327`.

## Non-claims

- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.
