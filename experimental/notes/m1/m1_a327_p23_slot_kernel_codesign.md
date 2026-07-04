# M1 a=327 P23 slot-kernel codesign

Status:

CANDIDATE / P23SLOT_PAIR_CLEAR_SLOT / PARTIAL / EXPERIMENTAL

This packet follows `ae37b1a` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous template-vector repair reduced the pair-projection obstruction to:

```text
forced pair = P23
slot nonzero rows = 12
```

This branch mutates around the best previous actual template mutation
`w1_c0_d16`, with direct pressure on witnesses 2 and 3 and on the slot-kernel
rows. It reruns:

```text
selected-class MILP
structural guard screening
basis-aware slot scoring
```

No Sage exact lift is attempted.

## Result

The bounded P23/slot-kernel pass used:

```text
mutations generated = 36
candidate systems constructed = 108
structural-pass candidates = 99
structural-pass candidates analyzed = 24
top classes = 14
random bases = 0
basis profiles tested = 13278
slot profiles tested = 79668
pair-clear slot profiles = 54
pair-clear slot-kernel profiles = 0
```

The best row is:

```text
mutation = w2_c1_d1
template = p23slot_w2_c1_d1
assignment = fiber_round_robin
basis = basisaware_1_6_7_8_10_12
coefficient matrix shape = [14,6]
coefficient rank/nullity = 6/0
stable-basis slot = 0
slot nonzero rows = 14
forced pair count = 0
forced pairs = none
```

Relative to `ae37b1a`:

```text
previous forced pair = P23
new forced pairs = none
pair projection obstruction = cleared
slot-kernel obstruction = remains
```

## Interpretation

This is the first actual-template branch in this local line with a pair-clear
stable-basis slot. That is a real change in the obstruction: pair projection is
no longer the active blocker.

The active blocker is now coefficient support:

```text
slot nonzero rows = 14
coefficient rank/nullity = 6/0
```

So this is not yet a proxy-positive kernel target and not an exact certificate.
The next branch should preserve pair-clear slots while reducing slot nonzero
rows or creating coefficient nullity.

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
- failure outside this bounded P23/slot-kernel front

## Next Target

Move to:

```text
m1-a327-pairclear-slot-kernel-row-reduction
```

Target:

```text
forced_pair_count = 0
slot_nonzero_rows -> 0
or coefficient_nullity > 0
```

Use Python first. If the remaining slot-row equations become a small linear
module/syzygy problem, Macaulay2 or Singular is the right next tool. Sage should
still wait until a pair-clear slot-kernel proxy target exists.
