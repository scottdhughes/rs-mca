# M1 a=327 nonbasis row dependency ansatz

Status:

EXACT_EXTRACTION_NO_A327 / NBDEP_NEAR_KERNEL_ONLY / PARTIAL / EXPERIMENTAL

This packet follows `3d5efb6` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous rank-defect template ansatz found no coefficient-kernel profiles
after forcing the obstruction functional into stable bases. This branch asks a
sharper local question: among the same realized template rowspaces, how close
are the forced stable-basis coefficient matrices to a right kernel?

For each forced stable-basis profile, the scanner searches exactly up to three
deleted nonbasis rows. A hit means the remaining nonbasis rows have coefficient
rank at most five and therefore admit a nonzero kernel vector. This is a
bounded diagnostic; it does not compute the unrestricted minimum row deletion
distance.

No Sage exact lift is attempted in this branch.

## Result

The bounded scan tested:

```text
systems tested = 384
target-present candidates = 84
forced basis profiles tested = 4260
row-removal limit = 3
actual kernel profiles = 0
near-kernel profiles = 252
remove-limit full-rank profiles = 4008
pair-projection-clear actual kernels = 0
```

Failure counts by candidate:

```text
NBDEP_NEAR_KERNEL_ONLY = 12
NBDEP_REMOVE_LIMIT_FULL_RANK = 72
NBDEP_TARGET_FUNCTIONAL_MISSING = 300
```

The best bounded near-kernel row is:

```text
template = rankdefect_hyperplane_r0_out7
assignment = signature_fiber_blocks
target mode = primary_e4
basis = nbdep_primary_e4_union_253_1_7_14_15_16_18
coefficient matrix shape = [13,6]
coefficient rank = 6
minimum rows removed within bound = 2
removed row indices = [1,5]
residual row classes = [2,6]
kernel vector = [0,0,1,1,1,0]
forced pair count = 10
forced pairs = P12,P13,P15,P16,P23,P25,P26,P35,P36,P56
```

So the branch finds near-kernel structure, but not an actual realized
coefficient kernel. Even the best two-row repair still forces ten pair
collapses in the induced projection test.

## Interpretation

This is a local negative for the current realized rank-defect template
rowspaces under bounded nonbasis-row deletion. The obstruction is now more
specific than full rank alone:

- no forced stable profile has an actual coefficient kernel;
- most profiles remain full rank after deleting up to three nonbasis rows;
- the best near-kernel requires deleting rows from classes `2` and `6`;
- the resulting kernel vector still collapses ten witness pairs.

The next constructive branch should not keep mutating these same rowspaces.
It should prescribe the nonbasis row dependency directly, including pair
projection clearance, then solve backward for selected classes or template
vectors that realize it.

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
- failure outside this bounded realized-template front
- unrestricted minimum nonbasis-row deletion distance

## Next Target

Move to a dependency-prescribed generator:

```text
m1-a327-prescribed-nonbasis-kernel-generator
```

Start from a desired kernel vector with pair projections nonzero, prescribe
nonbasis coefficient rows orthogonal to it, and then solve for selected masks
or template vectors that realize those rows while preserving support `327`,
pair caps, and pair-7 guards.
