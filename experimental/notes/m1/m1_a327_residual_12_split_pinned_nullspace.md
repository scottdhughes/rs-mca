# M1 a=327 residual [1,2] split and pinned-nullspace audit

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `024481e`, where exact evaluation pins inside the
protected-exchange schedule could split most of the degenerate class but still
failed to produce seven distinct codewords.

## Baseline

Prior exact pinned-lift audit:

```text
pin sets tested:                         12
exact vectors constructed:               12
nondegenerate vectors:                   0
capacity-preserving nondegenerate:       0
best capacity upper bound:               438
best pair B values:                      [1024,1024,512,1024,1024]
best failure mode:                       PIN_DOES_NOT_SPLIT
```

The strongest prior split was the `anchor_split_34567` family:

```text
remaining collapse:                      [[1,2],[7],[6],[5],[4],[3]]
capacity upper bound:                    155
```

So this audit targets the residual `[1,2]` collapse directly.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact `GF(17^32)` extraction experiment. It is not a proof record
and does not update any public row.

## Method

The Sage audit reconstructs the two protected-exchange proxy candidates and
keeps the protected/exchange target row schedule. It then starts from the
strongest split family:

```text
anchor_split_34567
```

and tests two residual layers.

First, it samples the pinned affine solution space by assigning deterministic
values to free columns in the `D_2` block:

```text
affine_pivot_solution
d2_first_free
d2_first4_free
d2_even_sparse
```

Second, it adds targeted residual pins:

```text
P_2(h) = gamma
```

at safe quotient-spread coordinates, for deterministic `gamma` values.

For every exact vector, the audit evaluates all seven codewords on `H`,
computes value classes, Hall pair values, old three-subset guards, capacity,
degenerate classes, and the exact rescheduler when the capacity and pair-Hall
screens allow it.

## Result

Corrected full-attempt summary:

```text
residual pin sets tested:                32
pinned-nullspace samples tested:         8
exact vectors constructed:               40
nondegenerate vectors:                   38
capacity-preserving nondegenerate:       0
best exact max-min:                      null
best capacity upper bound:               83
best pair B values:                      [575,513,512,512,512]
best degenerate classes:                 [[7],[6],[5],[4],[3],[2],[1]]
best failure mode:                       RESIDUAL12_SPLIT_CAPACITY_LOSS
```

Per protected-exchange proxy candidate:

```text
7d2bb937c72e__PX48__one_for_two:
  attempts:                              20
  failures:                              1 PIN_DOES_NOT_SPLIT, 19 CAPACITY_LOSS
  best capacity upper bound:             83

7d2bb937c72e__PX32__one_for_two:
  attempts:                              20
  failures:                              1 PIN_DOES_NOT_SPLIT, 19 CAPACITY_LOSS
  best capacity upper bound:             81
```

## Interpretation

This is a sharper exact negative than `024481e`.

The residual `[1,2]` split is algebraically reachable in this bounded exact
setup: 38 of 40 constructed vectors are nondegenerate. But every
nondegenerate vector loses the high-capacity protected-exchange geometry.

The failure has moved from:

```text
residual [1,2] degeneracy
```

to:

```text
residual [1,2] split destroys capacity and pair-7 repair
```

The bounded schedules therefore do not give an exact `a>=327` witness.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means the named exact residual split schedules found
no exact `a>=327` witness.

`PARTIAL` means other residual split schedules, gentler split layers, and
larger exact nullspace searches remain open.

## Failure labels

- `RESIDUAL12_PIN_INCONSISTENT`: no solution after a residual pin.
- `RESIDUAL12_PIN_DOES_NOT_SPLIT`: `[1,2]` still collapses.
- `RESIDUAL12_SPLIT_CAPACITY_LOSS`: seven distinct codewords exist, but
  capacity drops below `327`.
- `RESIDUAL12_SPLIT_PAIR7_LOSS`: capacity survives but pair-7 Hall values fall
  below the `B>=654` target.
- `RESIDUAL12_SPLIT_LOW_RESCHEDULE`: pair/capacity survive, but exact max-min
  is below `327`.
- `RESIDUAL12_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

Do not keep adding hard residual pins after `anchor_split_34567`: that regime
can split `[1,2]`, but it destroys capacity. A better next attack should make
the residual split gentler, for example by sampling around earlier partial
split families before the final anchor split collapses capacity, or by
constructing capacity-preserving `D_2` perturbations inside the
protected-exchange schedule rather than pinning after the destructive split.
