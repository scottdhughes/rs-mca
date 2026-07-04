# M1 a=327 template-vector pair-projection repair

Status:

EXACT_EXTRACTION_NO_A327 / TVPAIR_SLOT_PAIR_CLEAR_BROKEN / PARTIAL / EXPERIMENTAL

This packet follows `90745f2` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous basis-aware projection repair showed that basis reordering can
clear the named three-pair front, but only by introducing five new forced
pairs:

```text
P15, P23, P26, P36, P47
```

This branch moves one level upstream. It mutates the actual template vectors
around `pairclear_slot5_pair7_guarded`, preserves the pair-clear raw slot, then
reruns:

```text
selected-class MILP
structural guard screening
basis-aware slot scoring
```

No Sage exact lift is attempted.

## Result

The first bounded vector-repair pass used:

```text
mutations generated = 24
candidate systems constructed = 72
structural-pass candidates = 72
structural-pass candidates analyzed = 24
top classes = 14
random bases = 0
basis profiles tested = 22242
slot profiles tested = 133452
pair-clear slot profiles = 0
pair-clear slot-kernel profiles = 0
```

The best row is:

```text
mutation = w1_c0_d16
template = tvpair_w1_c0_d16
assignment = fiber_round_robin
basis = basisaware_0_7_8_9_11_12
coefficient matrix shape = [12,6]
coefficient rank/nullity = 6/0
stable-basis slot = 4
slot nonzero rows = 12
forced pair count = 1
forced pair = P23
```

Relative to `90745f2`, this is a strong local improvement:

```text
previous best forced pairs = P15,P23,P26,P36,P47
new best forced pair = P23
forced pair count delta = -4
```

## Interpretation

Template-vector repair is the right lever. A single actual-vector mutation
reduces the stable-basis pair-projection obstruction from five forced pairs to
one. However, the remaining slot is not a coefficient kernel:

```text
slot nonzero rows = 12
coefficient rank/nullity = 6/0
```

So this is not a proxy-positive candidate and not an exact certificate. The
next repair should target `P23` and the slot-kernel equations together, not
only pair projections.

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
- failure outside this bounded template-vector repair front

## Next Target

Move to:

```text
m1-a327-p23-slot-kernel-codesign
```

Target both remaining obstructions:

```text
forced pair = P23
slot nonzero rows = 12
```

The next search should mutate template vectors and stable-basis choice together
with a score like:

```text
primary: forced_pair_count
secondary: slot_nonzero_rows
tertiary: coefficient_nullity
```

Only after a pair-clear slot or slot-kernel proxy target appears should Sage
`GF(17^32)` exact audit run.
