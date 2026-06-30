# M1 a=327 capacity-preserving residual [1,2] split

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `5105961`, where hard residual `[1,2]` splitting after the
`anchor_split_34567` layer produced many nondegenerate exact vectors, but every
nondegenerate vector lost the protected-exchange capacity geometry.

## Baseline

Prior hard residual split:

```text
exact vectors constructed:               40
nondegenerate vectors:                   38
capacity-preserving nondegenerate:       0
best capacity upper bound:               83
best pair B values:                      [575,513,512,512,512]
best failure mode:                       RESIDUAL12_SPLIT_CAPACITY_LOSS
```

That showed:

```text
splitting [1,2] exactly is possible;
splitting [1,2] after the final hard split destroys capacity.
```

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact `GF(17^32)` extraction experiment. It is not a public
certificate and does not update any board row.

## Method

This audit starts earlier than `anchor_split_34567`.

It reconstructs the two protected-exchange proxy candidates and preserves the
protected row schedule carrying the witness-7 pair repair. It then tests
residual `[1,2]` splitting in two gentler modes:

```text
D2 nullspace sampling under protected rows
soft residual P_2(h)=gamma pins under protected rows
```

The bounded pass uses three pre-anchor partial split layers:

```text
none
one_pair_13
two_pair_balanced_split
```

and deterministic `D_2` free-column patterns:

```text
affine_pivot_solution
d2_first_free
d2_first4_free
d2_even_sparse
```

For each exact vector, the audit records:

```text
D2 split status
degenerate classes
capacity upper bound
B({1,7}),...,B({5,7})
old three-subset guards
six-class dominance
exact rescheduler result when screens allow
```

## Result

First bounded capacity-preserving residual split pass:

```text
protected rows:                          64
residual pin sets tested:                54
pinned-nullspace samples tested:         24
exact vectors constructed:               76
D2 split vectors:                        72
capacity-preserving D2 split vectors:    48
low-collapse capacity-preserving splits: 24
best capacity upper bound:               439
best pair B values:                      [1024,514,1024,1024,1024]
best exact max-min:                      null
best failure mode:                       RESIDUAL12_SPLIT_COLLAPSE_RETURNS
```

Per candidate, the failure mode profile is symmetric:

```text
RESIDUAL12_NOT_SPLIT:                    2
RESIDUAL12_PIN_DOES_NOT_SPLIT:           1
RESIDUAL12_SPLIT_CAPACITY_LOSS:          12
RESIDUAL12_SPLIT_COLLAPSE_RETURNS:       12
RESIDUAL12_SPLIT_PAIR7_LOSS:             12
```

The best high-capacity `D2` split has:

```text
capacity upper bound:                    439
pair B values:                           [1024,514,1024,1024,1024]
six-class dominance:                     510
degenerate classes:                      [[1,3,4,5,6,7],[2]]
```

The best low-collapse capacity-preserving splits have lower capacity but still
lose the pair-7 repair:

```text
capacity upper bound:                    366
pair B values:                           [1024,514,512,1024,1024]
six-class dominance:                     0
degenerate classes:                      [[1,4,5,6,7],[3],[2]]
```

## Interpretation

This is a strong refinement of `5105961`.

The hard split result said residual `[1,2]` splitting destroys capacity. This
packet shows that gentler, earlier splitting can preserve capacity:

```text
48 capacity-preserving D2 splits
24 low-collapse capacity-preserving D2 splits
```

But none of those vectors preserve the witness-7 pair repair. The best
capacity-preserving split returns to the six-witness collapse basin, while the
best low-collapse splits leave `B({2,7})` and `B({3,7})` near `512`.

So the obstruction has moved again:

```text
D2 split + capacity is possible;
D2 split + capacity + pair-7 repair is not found in the tested schedules.
```

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means the named exact residual split schedules found
no exact `a>=327` witness.

`PARTIAL` means other protected schedules, gentler `D_2` perturbations, and
larger exact nullspace searches remain open.

## Failure labels

- `RESIDUAL12_NOT_SPLIT`: `P_1` and `P_2` remain identified.
- `RESIDUAL12_PIN_DOES_NOT_SPLIT`: the exact solve returns a vector with no
  useful residual split.
- `RESIDUAL12_SPLIT_CAPACITY_LOSS`: `D_2` splits, but capacity drops below
  `327`.
- `RESIDUAL12_SPLIT_COLLAPSE_RETURNS`: capacity survives, but the six-witness
  collapse returns.
- `RESIDUAL12_SPLIT_PAIR7_LOSS`: capacity and low collapse survive, but the
  witness-7 pair repair falls below the stage-1 baseline.
- `RESIDUAL12_SPLIT_LOW_RESCHEDULE`: pair/capacity survive, but exact max-min
  is below `327`.
- `RESIDUAL12_CAPACITY_PRESERVING_SPLIT`: `D_2` splits and capacity survives,
  but no exact `a>=327` certificate is produced.
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

The next exact attack should preserve pair-7 repair explicitly while searching
within the low-collapse capacity-preserving `D_2` split regime. The current
best low-collapse split already keeps capacity above `327`; the missing piece
is raising the weak pair values, especially `B({2,7})` and `B({3,7})`, without
returning to the six-class collapse.
