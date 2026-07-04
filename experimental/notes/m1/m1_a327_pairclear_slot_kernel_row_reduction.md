# M1 a=327 pair-clear slot-kernel row reduction

Status:

CANDIDATE / PCSLOT_PAIR_CLEAR_SLOT_REDUCE_ROWS / PARTIAL / EXPERIMENTAL

This packet follows `984fc16` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous P23 slot-kernel codesign checkpoint found an actual-template
pair-clear slot:

```text
mutation = w2_c1_d1
pair-clear slot profiles = 54
forced pair count = 0
forced pairs = none
slot nonzero rows = 14
coefficient rank/nullity = 6/0
```

This branch keeps the pair-clear target and mutates around `w2_c1_d1`, with
the objective of reducing the coefficient support in the proxy slot or creating
coefficient nullity. It reruns:

```text
selected-class MILP
structural guard screening
basis-aware slot scoring
```

No Sage `GF(17^32)` exact lift is attempted.

## Result

The bounded row-reduction pass used:

```text
mutations generated = 48
candidate systems constructed = 144
structural-pass candidates = 132
structural-pass candidates analyzed = 48
structural-pass candidates skipped = 84
top classes = 14
random bases = 0
basis profiles tested = 44463
slot profiles tested = 266778
pair-clear slot profiles = 684
pair-clear slot-kernel profiles = 0
```

The best row is:

```text
mutation = w1_c3_d1
template = pcslot_w1_c3_d1
assignment = fiber_round_robin
basis = basisaware_1_4_7_8_9_12
coefficient matrix shape = [14,6]
coefficient rank/nullity = 6/0
stable-basis slot = 5
slot nonzero rows = 11
forced pair count = 0
forced pairs = none
```

Relative to `984fc16`:

```text
slot rows improved 14 -> 11
forced pair count remains 0
pair-clear slot profiles increased 54 -> 684
pair-clear slot-kernel profiles remain 0
```

## Interpretation

This is useful local progress. The pair projection obstruction remains cleared,
and the coefficient-support obstruction moved from 14 slot rows to 11 slot
rows. But the coefficient matrix is still full rank:

```text
coefficient rank/nullity = 6/0
```

So this is still not a proxy-positive kernel target and not an exact
certificate. The active blocker is now the eleven nonzero coefficient rows in
the pair-clear slot.

## Non-claims

This packet does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- failure outside this bounded pair-clear row-reduction front

## Next Target

Move to either:

```text
m1-a327-pairclear-slot-kernel-row-reduction-stage2
```

or the more algebraic:

```text
m1-a327-pairclear-slot-row-syzygy
```

Target:

```text
forced_pair_count = 0
slot_nonzero_rows <= 10
or coefficient_nullity > 0
```

Use Python first for deterministic mutation and basis scoring. If the remaining
eleven slot-row equations can be isolated as a small module or syzygy problem,
Macaulay2 or Singular is the right next tool. Sage should still wait until a
pair-clear slot-kernel proxy target exists.
