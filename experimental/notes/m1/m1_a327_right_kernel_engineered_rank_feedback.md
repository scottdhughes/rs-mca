# M1 a327 right-kernel-engineered rank feedback

Status: EXACT_EXTRACTION_NO_A327 / RIGHT_KERNEL_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL.

This packet follows `e237ab6` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous syzygy proxy showed that the best dependency-engineered profile
had many row-side syzygies but no right kernel:

```text
coefficient matrix = 41 x 6
coefficient rank = 6
right kernel nullity = 0
left syzygy dimension = 35
quotient proxy rank/nullity = 1385 / 0
```

This branch asks whether the generator can directly find basis profiles whose
nonbasis coefficient presentation has a right kernel before the polynomial
evaluation factors are expanded.

## Result

The bounded right-kernel-engineered scan tested:

```text
templates tested = 18
systems tested = 108
structural-pass candidates = 96
coefficient profiles tested = 3276
right-kernel-positive candidates = 0
proxy-ranked candidates = 0
proxy-positive candidates = 0
```

The best recorded candidate is:

```text
template = random_matroid_v3_seed_010_m6
assignment = signature_fiber_blocks
functional classes = 45
basis profiles tested = 35
support vector = [327,327,327,327,327,327,327]
pair7 counts = [233,233,233,233,233]
max pair count = 233
selected class size counts = {3:87, 4:97, 5:328}
```

Every structurally valid candidate still had full-rank nonbasis coefficient
profiles. No profile reached the quotient proxy stage.

## Interpretation

This is a sharper failure than the previous dependency-engineered scan. The
tested assignments satisfy the selected-class support and pair guards, have no
forced functional identities, and keep functional span rank 6, but the selected
basis profiles do not create a nontrivial right-kernel relation in coefficient
space.

So the next useful generator should not only choose a basis and hope the
nonbasis rows drop rank. It should construct the coefficient matrix with a
prescribed right kernel first, then assign selected classes and supports around
that relation.

## Tool notes

Python/NumPy-style finite-field elimination is the right first tool for this
screen. Macaulay2 is only useful once a right-kernel-positive coefficient
matrix exists. Sage should still wait until proxy quotient nullity appears.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
