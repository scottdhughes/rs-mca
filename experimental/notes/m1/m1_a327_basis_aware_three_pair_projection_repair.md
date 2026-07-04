# M1 a=327 basis-aware three-pair projection repair

Status:

EXACT_EXTRACTION_NO_A327 / BATHREE_TARGET_CLEAR_NEW_FORCED / PARTIAL / EXPERIMENTAL

This packet follows `0aa9daa` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous forced-pair repair checkpoint left the obstruction concentrated in
three pair projections:

```text
P12, P46, P57
```

This branch reuses the actual template specs and selected-class MILP layer from
the basis-aware search, but ranks stable-basis slots by those three target
projections first. It is not an exact Sage lift.

The run used:

```text
top classes = 32
random ordered bases = 1024
```

For the structural-pass candidates, this covers the same basis-profile front as
`0aa9daa` and adds the same ordered-basis augmentation, but scores the profiles
against the new target set.

## Result

The repair scan tested:

```text
systems tested = 12
basis profiles tested = 16437
slot profiles tested = 98622
target-clear slot profiles = 7440
target-clear slot-kernel profiles = 0
pair-clear slot profiles = 0
pair-clear slot-kernel profiles = 0
```

The best target-clear row is:

```text
template = pairclear_slot5_pair7_guarded
assignment = pair7_block
basis = threepair_0_4_7_10_14_16
coefficient matrix shape = [11,6]
coefficient rank/nullity = 6/0
stable-basis slot = 5
slot nonzero rows = 11
target forced pair count = 0
total forced pair count = 5
forced pairs = P15,P23,P26,P36,P47
```

Relative to `0aa9daa`:

```text
previous forced pairs = P12,P46,P57
target pairs repaired = P12,P46,P57
target pairs remaining = none
new forced pairs introduced = P15,P23,P26,P36,P47
total forced pair count delta = +2
```

## Interpretation

The three named projection zeros are individually repairable by changing the
stable basis. However, within the tested actual-template and selected-class
front, repairing them by basis choice simply moves the forced-pair obstruction
to a different five-pair set. No pair-clear slot exists, and no target-clear
slot is a coefficient kernel.

This is useful local information: the obstruction is no longer a fixed pair
identity like `P12` or `P46`; it is a tradeoff in the stable-basis projection
geometry for the current template family.

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
- failure outside this bounded basis-aware projection-repair front

## Next Target

Do not keep reordering the same basis front. The next useful move is template
variation or small algebraic repair of the actual template vectors so that the
stable-basis projection slot can clear all 21 pairs without trading into a new
forced-pair set.

Candidate branch:

```text
m1-a327-template-vector-pairprojection-repair
```

Target:

```text
keep support/pair guards and structural pass
keep functional span rank 6
avoid forced functional identities
find a stable-basis slot with forced_pair_count = 0
then only after that, run proxy/Sage exact audit
```
