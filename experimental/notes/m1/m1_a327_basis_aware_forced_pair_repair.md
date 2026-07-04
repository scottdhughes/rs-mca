# M1 a=327 basis-aware forced-pair repair

Status:

EXACT_EXTRACTION_NO_A327 / BAFPAIR_PARTIAL_FORCED_PAIR_REPAIR / PARTIAL / EXPERIMENTAL

This packet follows `37d9718` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous basis-aware search reduced the best pair-projection obstruction to
four forced pairs:

```text
P12, P17, P27, P46
```

This branch widens the basis-aware front and treats those pairs as the repair
target. It uses the same actual pair-clear template specs and selected-class
MILP layer, but scans more basis candidates:

```text
top classes = 32
random bases = 1024
```

No Sage exact lift is attempted.

## Result

The repair scan tested:

```text
systems tested = 12
basis profiles tested = 16437
slot profiles tested = 98622
pair-clear slot profiles = 0
pair-clear slot-kernel profiles = 0
```

The best row is:

```text
template = pairclear_slot5_pair7_guarded
assignment = pair7_block
basis = basisaware_6_7_8_14_15_16
coefficient matrix shape = [11,6]
coefficient rank/nullity = 6/0
stable-basis slot = 5
slot nonzero rows = 11
forced pair count = 3
forced pairs = P12,P46,P57
```

Relative to `37d9718`:

```text
previous forced pairs = P12,P17,P27,P46
target pairs repaired = P17,P27
target pairs remaining = P12,P46
new forced pair introduced = P57
forced pair count delta = -1
```

So this is real local progress, but not a candidate: no pair-clear coefficient
slot exists in the tested front, and the coefficient matrix remains full rank.

## Interpretation

Basis-aware repair is the right lever. It repaired two of the four named target
pairs and reduced the total forced-pair count from four to three. The remaining
obstruction is now concentrated in:

```text
P12, P46, P57
```

The next branch should not merely widen random bases again. It should target
those three projection zeros directly, either by template variation or by
constructing basis functionals whose slot coordinate separates those pair
differences.

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
- failure outside this bounded forced-pair repair front

## Next Target

Move to:

```text
m1-a327-basis-aware-three-pair-projection-repair
```

Target the remaining projection zeros:

```text
P12, P46, P57
```

Use Python first to bias basis construction and template variants against
those pairs. If the basis-coordinate constraints become algebraic, use
Macaulay2/Singular or `msolve` on the small system. Sage should still wait
until a realized proxy-positive, pair-clear target exists.
