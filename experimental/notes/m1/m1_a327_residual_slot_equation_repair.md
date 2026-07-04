# M1 a=327 residual-slot equation repair

Status:

EXACT_EXTRACTION_NO_A327 / RESIDUAL_SLOT_INVARIANT_NONZERO / PARTIAL / EXPERIMENTAL

This packet follows `fae2021` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous near-miss repair isolated the best actual-template profile:

```text
template = nearmiss_w7_c1_v9
base template = single_outside_w7_v3
assignment = signature_fiber_blocks
basis = slot_union_142_6_8_10_12_15_16
slot = 3
slot nonzero rows = 2
forced pair count = 10
```

This branch treats the two residual slot coefficients as equations rather than
running another broad mutation front.

## Direct Residual Equations

The two residual rows are:

```text
class 1: functional [0,0,0,1,0,0], coordinates [7,0,0,1,10,12]
class 5: functional [0,0,0,1,4,8], coordinates [1,0,0,1,16,0]
```

Both have slot-3 coefficient `1`, hence both obstruct the actual slot kernel.

For the fixed best basis family, the first three basis rows have the form:

```text
e3 + u, e2 + u, e1 + u
```

with `u=(0,0,0,0,U,V)`, and the remaining rows are:

```text
e4 - e5, e3 - e5, e6
```

The GF(17) parameter audit checked all valid `(U,V)` pairs. For both residual
functionals:

```text
slot coefficient values = [1]
```

So the residual equations reduce locally to `1=0`; they cannot be solved by
tuning the witness-7 induced `u` parameter while preserving this basis pattern.

## Exhaustive Stable-Basis Check

For the same actual template and selected-count ledger, the audit constructed
all stable profiles returned by the existing stable-combo front:

```text
stable basis combinations = 326
stable profiles constructed = 122
slot profiles tested = 732
actual zero-slot profiles = 0
pair-projection-clear actual slots = 0
best slot nonzero rows = 2
best forced pair count = 10
```

This confirms the `slot_union_142_6_8_10_12_15_16` profile is not just a
front-limit artifact: no stable basis for the current actual template gives an
actual zero-slot profile.

## Interpretation

This is a scoped local negative for the residual-equation repair of the
`nearmiss_w7_c1_v9` actual template. The best fixed-basis residual equations
are invariantly nonzero, and the exhaustive stable-basis check finds no
alternative actual zero slot.

The next constructive move should change the selected-count ledger or template
family more materially. Continuing small witness-7 perturbations around this
profile is unlikely to help unless they also change the functional-class/basis
incidence that makes the residual coefficient invariant.

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
- success or failure outside this residual slot profile

## Next Target

Move one step up from local residual repair:

```text
m1-a327-realization-aware-ledger-perturbation
```

The branch should alter the selected-count ledger or template family so the
obstruction class `[0,0,0,1,0,0]` is either included in the stable basis or no
longer has invariant nonzero projection onto the candidate slot. Use
Python/NumPy first; use Macaulay2 or Singular only if the incidence equations
become a module/elimination problem.
