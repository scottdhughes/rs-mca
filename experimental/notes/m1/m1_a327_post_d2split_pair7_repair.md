# M1 a=327 post-D2-split pair-7 repair

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `f272e60`, where exact `D_2` splitting and capacity
preservation were both achieved over `GF(17^32)`, but witness-7 pair repair
was not preserved.

## Baseline

Capacity-preserving residual split checkpoint:

```text
exact vectors constructed:               76
D2 split vectors:                        72
capacity-preserving D2 split vectors:    48
low-collapse capacity-preserving splits: 24
best capacity upper bound:               439
best pair B values:                      [1024,514,1024,1024,1024]
best failure mode:                       RESIDUAL12_SPLIT_COLLAPSE_RETURNS
```

The best low-collapse capacity-preserving split had:

```text
capacity upper bound:                    366
pair B values:                           [1024,514,512,1024,1024]
six-class dominance:                     0
degenerate classes:                      [[1,4,5,6,7],[3],[2]]
```

So the post-split obstruction is concentrated in the weak witness-7 pairs,
especially `B({2,7})`.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact `GF(17^32)` extraction experiment. It is not a public
certificate and does not update any board row.

## Method

The audit reconstructs the protected-exchange proxy candidates and starts from
the low-collapse capacity-preserving `D_2` split regime:

```text
partial split family:                    one_pair_13
free patterns:                           d2_first_free, d2_first4_free, d2_even_sparse
```

It then adds homogeneous pair-repair constraints at safe coordinates:

```text
P_2(h) = P_7(h)
P_3(h) = P_7(h)
P_2(h) = P_3(h) = P_7(h)
```

The goal is to raise the weak pair values without undoing:

```text
D2 split
capacity >= 327
low six-class dominance
```

Each exact vector is evaluated directly on `H`; the verifier records capacity,
pair Hall values, collapse, degeneracy, and exact rescheduling when the screens
allow it.

## Result

First bounded post-D2 pair-repair pass:

```text
base vectors tested:                     6
repair pin sets tested:                  72
exact vectors constructed:               78
D2 split retained:                       78
capacity-preserving vectors:             78
low-collapse capacity-preserving:        78
pair27 repaired vectors:                 0
full pair7 repaired vectors:             0
best pair B values:                      [1024,514,513,1024,1024]
best capacity upper bound:               366
best exact max-min:                      null
best failure mode:                       POST_D2_PAIR7_NOT_REPAIRED
```

The failure profile is symmetric across the two proxy candidates:

```text
POST_D2_PAIR7_NOT_REPAIRED:              39 / candidate
```

The best tested repair pins slightly improve the third pair value but leave
the main weak pair unchanged:

```text
B({2,7}) = 514
B({3,7}) = 513
target    = 654
```

## Interpretation

This is a clean negative for the first post-D2 pair-repair layer.

Unlike the previous branch, this audit does not lose the residual split,
capacity, or low-collapse geometry. Every constructed exact vector retains:

```text
D2 split
capacity >= 327
six-class dominance <= 20
```

But the tested `P_2=P_7`, `P_3=P_7`, and `P_2=P_3=P_7` repair rows do not
increase the weak pair Hall values enough. The pair-7 obstruction is therefore
not caused by immediate capacity loss or collapse return in this layer.

The live obstruction is now:

```text
low-collapse capacity-preserving D2 split geometry is stable,
but local homogeneous pair-repair pins do not restore B({2,7}).
```

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means the named exact post-D2 pair-repair schedules
found no exact `a>=327` witness.

`PARTIAL` means other pair-repair schedules, inhomogeneous repair pins,
larger nullspace searches, and pair-Hall-guided exact sampling remain open.

## Failure labels

- `POST_D2_PAIR7_NOT_REPAIRED`: capacity and low collapse survive, but
  pair-7 Hall values remain below `654`.
- `POST_D2_PAIR7_REPAIR_UNDOES_D2_SPLIT`: repair causes `[1,2]` collapse.
- `POST_D2_PAIR7_REPAIR_COLLAPSE_RETURNS`: repair returns to six-class
  collapse.
- `POST_D2_PAIR7_REPAIR_CAPACITY_LOSS`: repair drops capacity below `327`.
- `POST_D2_PAIR7_REPAIR_LOW_RESCHEDULE`: pair/capacity survive, but exact
  max-min is below `327`.
- `POST_D2_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

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

The next exact repair should not repeat local homogeneous `P_i=P_7` pins. A
better target is pair-Hall-guided nullspace sampling inside the stable
low-collapse capacity-preserving `D_2` split regime, with the objective of
raising `B({2,7})` rather than adding isolated pair equality rows.
