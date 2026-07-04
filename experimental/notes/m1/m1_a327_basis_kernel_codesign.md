# M1 a=327 basis/kernel co-design

Status:

EXACT_EXTRACTION_NO_A327 / CODESIGN_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `cfc4f6d` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous forced-basis audit showed that, for the local same-mask front,
forcing the obstruction functional into the stable basis kills the coefficient
right kernel.

This branch broadens the source front. It rebuilds the 36-template actual
candidate generator and imposes basis inclusion during basis selection:

```text
primary_e4:      [0,0,0,1,0,0]
both_residuals:  [0,0,0,1,0,0] and [0,0,0,1,4,8]
```

The search is still actual-template only:

- no synthetic rowspace edits,
- support and pair guards enforced,
- obstruction-functional basis inclusion checked before any proxy/Sage lift,
- coefficient rank defect required before pair-projection or proxy testing.

## Result

The bounded co-design scan tested:

```text
systems tested = 216
structural-pass candidates = 210
target-present candidates = 144
forced basis combinations = 257298
forced basis profiles tested = 4530
coefficient-kernel profiles = 0
pair-projection-clear profiles = 0
proxy-positive profiles = 0
```

Failure counts:

```text
CODESIGN_COEFFICIENT_FULL_RANK = 132
CODESIGN_TARGET_FUNCTIONAL_MISSING = 66
CODESIGN_NO_STABLE_TARGET_BASIS = 12
CODESIGN_LOW_FUNCTIONAL_SPAN = 6
```

The best bookkeeping row is:

```text
template = single_outside_w2_v3
assignment = signature_fiber_blocks
target-present modes = [primary_e4]
forced basis profiles tested = 72
forced basis combinations = 973
best failure = CODESIGN_COEFFICIENT_FULL_RANK
```

No forced-basis profile in this broader actual-template front has coefficient
rank defect.

## Interpretation

This is a broader local negative than `cfc4f6d`: it is no longer only the
`nearmiss_w7_c1_v9` ledger. Across the existing 36-template generator, the
obstruction functional can often be present and forced into stable bases, but
the nonbasis coefficient matrix remains full rank in every tested profile.

The current obstacle is now:

```text
obstruction-functional basis inclusion and coefficient rank defect are not
co-designed by the existing actual-template generator.
```

The next useful branch should therefore generate templates with an explicit
rank-defect ansatz, not just filter the existing generator after the fact.

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
- failure outside this bounded 36-template co-design front

## Next Target

Move to a determinantal/syzygy construction branch:

```text
m1-a327-rankdefect-template-ansatz
```

Instead of choosing templates first and checking rank defect later, prescribe a
rank-5 coefficient relation among nonbasis rows and solve for template vectors
or selected masks that realize it. Use Python/NumPy for finite-field linear
screening; use Macaulay2 or Singular if the rank-defect constraints are best
handled as minors, syzygies, or module conditions.
