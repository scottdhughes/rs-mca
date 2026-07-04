# M1 a=327 realized-slot near-miss repair

Status:

EXACT_EXTRACTION_NO_A327 / NREPAIR_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL

This packet follows `e8ce88b` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The realization-aware proxy-slot generator found no actual zero-slot profiles
in the bounded actual-template front. Its closest profile was:

```text
template = single_outside_w7_v3
assignment = signature_fiber_blocks
basis = slot_union_142_5_7_9_11_13_17
slot nonzero rows = 2
forced pair count = 15
```

This branch performs a focused repair around that near miss. It preserves the
selected-count ledger and tests actual template-vector perturbations, so support
and pair guards remain exact by construction. The mutation front contains the
base outside-witness vector, all one-coordinate witness-7 mutations, and a
second-order refinement around the best one-coordinate mutation `w7_c1_v9`.

## Search Result

The bounded repair scan tested:

```text
mutation profiles tested = 177
systems tested = 1062
structural-pass candidates = 1050
stable basis combinations = 853704
stable basis profiles tested = 30738
slot profiles tested = 184428
actual zero-slot profiles = 0
pair-projection-clear actual slots = 0
proxy-positive actual slots = 0
```

The best repaired near miss is:

```text
template = nearmiss_w7_c1_v9
base template = single_outside_w7_v3
assignment = signature_fiber_blocks
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 17
functional span rank = 6
forced functional identities = 0
basis = slot_union_142_6_8_10_12_15_16
basis support sizes = [74,74,74,37,37,31]
basis-zero union size = 142
stable common multiplier dimension = 114
coefficient matrix shape = 11 x 6
coefficient rank/nullity = 6 / 0
slot nonzero rows = 2
forced pair count = 10
```

So the repair improved the pair-projection side of the near miss from 15 forced
pairs to 10, but it did not kill the two residual slot coefficients.

## Interpretation

This is a useful local negative for small actual-template perturbations around
the `single_outside_w7_v3` near miss. The selected-count ledger remains viable
and the best mutation improves pair projections, but the actual zero-slot
condition does not appear in this mutation front.

The next move should not be a broader random mutation alone. The two residual
slot coefficients should be treated as explicit equations. A better follow-up
is a symbolic or linearized repair branch that solves for template-vector
perturbations making those two coefficients vanish while keeping pair
projections nonzero.

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
- success or failure outside this local mutation front

## Next Target

Build a residual-equation repair branch for the best repaired profile:

```text
nearmiss_w7_c1_v9 / signature_fiber_blocks
basis = slot_union_142_6_8_10_12_15_16
slot = 3
slot_nonzero_rows = 2
```

The branch should derive the two residual slot coefficients as equations in
template-vector perturbation variables. Use Python first; switch to Macaulay2
or Singular if the coefficient equations become a small module/elimination
problem.
