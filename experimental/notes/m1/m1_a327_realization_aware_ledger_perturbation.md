# M1 a=327 realization-aware ledger perturbation

Status:

EXACT_EXTRACTION_NO_A327 / LEDGERPERT_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL

This packet follows `8a15096` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The residual-slot equation audit showed that the best fixed-basis residual
equations reduce to an invariant nonzero slot coefficient. This branch moves
one level up and perturbs the selected-count ledger while keeping:

- the actual `nearmiss_w7_c1_v9` template vectors,
- exact support `[327,327,327,327,327,327,327]`,
- pair caps and pair-7 guards,
- actual template rowspaces only,
- no synthetic rowspace edits.

The count-ledger kernel under the coordinate-count and seven support equations
has basis:

```text
[0,1,-1,0,0,-1,1,0,0,0,0]
[0,1,0,-1,0,-1,0,1,0,0,0]
[1,-1,1,-1,0,0,0,0,-2,1,1]
```

The bounded scan walked this kernel with coefficient bound `6` and kept the
first 96 feasible ledgers after support/pair screening.

## Result

The bounded actual-template scan tested:

```text
ledger profiles tested = 96
systems tested = 576
structural-pass candidates = 576
slot profiles tested = 127800
actual zero-slot profiles = 0
pair-projection-clear actual slots = 0
proxy-positive actual slots = 0
```

The best result remains the unperturbed base ledger:

```text
perturbation = base
kernel coefficients = [0,0,0]
assignment = signature_fiber_blocks
basis = slot_union_142_6_8_10_12_15_16
slot = 3
best slot nonzero rows = 2
forced pair count = 10
```

## Interpretation

This is a bounded local negative for same-mask selected-count perturbations of
the current actual template. The count-kernel directions preserve the support
ledger, but they do not create an actual zero-slot profile in the tested front.

The current obstruction is no longer just the two residual coefficients in one
fixed basis. Same-mask ledger motion also returns to the same best profile.
The next constructive move should allow a larger change:

- introduce new selected masks,
- change the low-rank template family,
- or explicitly require the obstruction functional `[0,0,0,1,0,0]` to appear
  in the stable basis while preserving pair projections.

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
- failure outside this bounded same-mask ledger perturbation front

## Next Target

The next branch should be:

```text
m1-a327-obstruction-functional-basis-forcing
```

Instead of hoping the obstruction functional enters a stable basis naturally,
force basis inclusion of `[0,0,0,1,0,0]` or an equivalent row during ledger and
template generation. Use Python/NumPy first; use Macaulay2 or Singular only if
the forced-basis incidence conditions become a module/elimination problem.
