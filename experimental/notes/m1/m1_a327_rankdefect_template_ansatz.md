# M1 a=327 rank-defect template ansatz

Status:

EXACT_EXTRACTION_NO_A327 / RANKDEFECT_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `d7b67e4` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous co-design scan showed that the existing 36-template generator does
not combine obstruction-functional basis inclusion with coefficient rank
defect. This branch changes the template generator itself.

The new templates are rank-defect-oriented ansatzes:

- choose a rank-5 hyperplane in `GF(17)^6`,
- put most witness template vectors in that hyperplane,
- add one outside witness direction to restore full functional span,
- solve the selected-count MILP,
- enforce support and pair guards,
- force obstruction-functional basis inclusion,
- require coefficient rank defect before pair/proxy checks.

No Sage exact lift is attempted in this branch.

## Result

The bounded ansatz scan tested:

```text
templates generated = 64
systems tested = 384
structural-pass candidates = 384
target-present candidates = 84
forced basis combinations = 7498470
forced basis profiles tested = 4260
coefficient-kernel profiles = 0
pair-projection-clear profiles = 0
proxy-positive profiles = 0
```

Failure counts:

```text
RANKDEFECT_COEFFICIENT_FULL_RANK = 84
RANKDEFECT_TARGET_FUNCTIONAL_MISSING = 300
```

The best bookkeeping row is:

```text
template = rankdefect_hyperplane_r0_out6
assignment = signature_fiber_blocks
support = [327,327,327,327,327,327,327]
pair7 = [215,215,215,215,215]
max pair count = 215
target-present modes = [primary_e4]
forced basis combinations = 19026
forced basis profiles tested = 72
best failure = RANKDEFECT_COEFFICIENT_FULL_RANK
```

So these rank-5-hyperplane-plus-outside ansatzes improve pair slack but still
do not produce a coefficient-kernel profile when the obstruction functional is
forced into the basis.

## Interpretation

This is a bounded local negative for the first explicit rank-defect template
ansatz. The failure is no longer due to pair guards or support feasibility.
The ansatz creates valid support/pair ledgers, but the forced stable-basis
coefficient matrices remain full rank.

The next search should target the coefficient matrix more directly. The
template ansatz should prescribe repeated or dependent nonbasis coordinate rows,
not only place witnesses in a rank-5 hyperplane.

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
- failure outside this bounded rank-defect ansatz front

## Next Target

Move to a nonbasis-row dependency ansatz:

```text
m1-a327-nonbasis-row-dependency-ansatz
```

Instead of hoping rank defect follows from a rank-5 witness hyperplane,
prescribe repeated nonbasis coordinate rows or an explicit right-kernel vector
for the coefficient matrix, then solve backward for template vectors and
selected masks. Use Python/NumPy first; use Macaulay2 or Singular if this
becomes a determinantal/minor or syzygy problem.
