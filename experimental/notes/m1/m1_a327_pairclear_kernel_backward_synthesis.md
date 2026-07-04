# M1 a=327 pair-clear kernel backward synthesis

Status:

EXACT_EXTRACTION_NO_A327 / PKBS_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL

This packet follows `81fceb2` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous prescribed-nonbasis-kernel branch showed that retained
realized-template near-kernels do not escape pair collapse. This branch starts
one step earlier: it generates actual template vectors whose original slot
separates all seven witnesses, then searches stable-basis coefficient slots for
a pair-clear kernel target.

This is still a Python/GF(17) synthesis layer. No Sage `GF(17^32)` lift is
attempted.

## Result

The first-pass backward synthesis tested:

```text
template specs tested = 4
MILP profiles constructed = 4
systems tested = 12
structural-pass candidates = 3
stable-basis profiles tested = 123
slot profiles tested = 738
actual zero-slot profiles = 0
pair-projection-clear actual slots = 0
proxy-positive actual slots = 0
```

Screen/failure counts:

```text
PKBS_FORCED_IDENTITY = 6
PKBS_LOW_FUNCTIONAL_SPAN = 3
PKBS_SLOT_NOT_KERNEL = 3
```

The best row is:

```text
template = pairclear_slot5_pair7_guarded
assignment = pair7_block
basis = slot_union_179_3_6_12_13_14_16
coefficient matrix shape = [11,6]
coefficient rank/nullity = 6/0
best stable-basis slot = 2
slot nonzero rows = 3
forced pair count = 11
forced pairs = P13,P24,P25,P26,P27,P45,P46,P47,P56,P57,P67
```

So the pair-clear original template coordinate does not automatically become a
pair-clear stable-basis coefficient direction. In the tested front, every
candidate either fails structural screening or has no actual zero-slot kernel.

## Interpretation

This branch is a useful first backward-synthesis diagnostic, not a route cut.
It shows that enforcing pair separation in a raw template coordinate is too
weak. The next synthesis layer must choose or constrain the stable basis itself
so that the coefficient-kernel direction is pair-clear, instead of hoping a
pair-clear raw coordinate survives the change of basis.

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
- failure outside this four-template backward-synthesis front

## Next Target

Move to a basis-aware backward synthesis:

```text
m1-a327-basis-aware-pairclear-kernel-synthesis
```

The next generator should synthesize:

```text
template vectors
selected classes
stable basis functionals
coefficient kernel vector
```

simultaneously, with the pair-projection map enforced in stable-basis
coordinates. Use Python first. Use Macaulay2 or Singular only if this becomes a
module/syzygy or determinantal-minor problem. Use `msolve` only if nonlinear
template equations become small enough to solve directly.
