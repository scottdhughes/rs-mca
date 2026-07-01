# M1 a=327 pair {2,7}/{3,7} class creation

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `618321c`, where the exact exchange audit showed that the
current low-collapse, capacity-preserving `D_2`-split basin cannot be repaired
by rescheduling alone:

```text
B({2,7}) = 514
B({3,7}) = 513
{2,7} shared coordinates: [0,18]
{3,7} shared coordinates: [18]
exchange graph feasible: false
```

The live obstruction is therefore not selection among existing value classes.
The required `{2,7}` and `{3,7}` value classes are mostly absent.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact-field construction experiment over `GF(17^32)`. It is not a
public proof record and does not update any board row.

## Method

The audit builds `{2,7}` and `{3,7}` equalities into the algebraic target
system as first-class exact rows:

```text
P_2(h) = P_7(h)  for h in T_27
P_3(h) = P_7(h)  for h in T_37
```

The first bounded pass tests:

```text
|T_27| = |T_37| = 32
designs:
  disjoint_low_high
  overlap_all
  even_odd
free pattern:
  d2_first_free
```

The coordinate sets are quotient-fiber structured and avoid the already-known
shared coordinates `[0,18]`.

Larger class-creation sizes are deliberately left open:

```text
64, 96, 128, 160
```

The first attempt at the larger grid was interrupted because exact
`GF(17^32)` echelonization dominated runtime. This note records the completed
size-32 exact probe only.

## Result

The size-32 class-creation rows do create new pair-credit material:

```text
B({2,7}): 514 -> 545
B({3,7}): 513 -> 544
capacity upper bound: 375
D2 split vectors: 6/6
```

But the repair is far short of the target:

```text
target B({i,7}) = 654
best B({2,7}) = 545
best B({3,7}) = 544
pair27 repaired vectors: 0
pair37 repaired vectors: 0
full pair repaired vectors: 0
```

The best low-collapse design is `overlap_all`:

```text
pair B values = [1024,545,544,1024,1024]
capacity upper bound = 375
six-class dominance = 0
failure mode = PAIR_CLASS_PARTIAL_REPAIR
```

All six constructed exact vectors remain degenerate:

```text
degenerate classes = [[1,4,5,6,7],[3],[2]]
```

The disjoint/even-odd designs have the same pair values but return
six-class-dominance count `32`, so they are classified as
`PAIR_CLASS_COLLAPSE_RETURNS`.

## Interpretation

This is a useful positive/negative exact probe.

Positive:

```text
structured exact class creation can raise B({2,7}) and B({3,7})
while retaining D2 split and capacity >=327.
```

Negative:

```text
the size-32 layer is too small to repair the pair deficits,
and the exact vectors still identify witnesses [1,4,5,6,7].
```

So this checkpoint does not produce an `a=327` certificate, but it does show
that class creation is the correct algebraic knob: unlike exchange repair, it
actually creates new `{2,7}` and `{3,7}` pair material.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact
`GF(17^32)` witness with seven distinct degree-`<256` codewords and one
received word.

`EXACT_EXTRACTION_NO_A327` means this named exact class-creation probe found
no exact `a>=327` witness.

`PARTIAL` means larger class-creation systems, additional free schedules, and
nondegeneracy-preserving variants remain open.

## Failure labels

- `PAIR_CLASS_SYSTEM_INCONSISTENT`: imposed `P_2=P_7` / `P_3=P_7` rows make
  the exact system unsolvable or rank-defective under the current solver.
- `PAIR_CLASS_UNDOES_D2_SPLIT`: exact solution collapses `[1,2]` again.
- `PAIR_CLASS_COLLAPSE_RETURNS`: six-class collapse returns.
- `PAIR_CLASS_CAPACITY_LOSS`: pair classes are created but capacity drops below
  `327`.
- `PAIR_CLASS_PARTIAL_REPAIR`: `B({2,7})` / `B({3,7})` improve but remain
  below `654`.
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

The next exact attack should continue class creation, but with better exact
linear-algebra strategy:

```text
sizes 64,96,128,160
more free schedules
nondegeneracy-preserving constraints
or row-subset / block elimination to avoid dense full exact echelonization
```

The key question is whether larger structured `T_27` / `T_37` sets can push
`B({2,7})` and `B({3,7})` toward `654` without preserving the
`[1,4,5,6,7]` degenerate class.
