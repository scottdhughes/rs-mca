# M1 a=327 obstruction-functional basis forcing

Status:

EXACT_EXTRACTION_NO_A327 / BASISFORCE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `abb1956` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The residual-slot and ledger-perturbation audits isolated the obstruction
functional:

```text
[0,0,0,1,0,0]
```

and the secondary residual functional:

```text
[0,0,0,1,4,8]
```

This branch forces those functionals into stable bases instead of waiting for
them to appear naturally. It keeps:

- actual template rowspaces only,
- no synthetic rowspace edits,
- support `[327,327,327,327,327,327,327]`,
- pair caps and pair-7 guards,
- the same bounded 96 selected-count ledger perturbation front from `abb1956`.

Two target modes are tested:

```text
primary_e4:       basis contains [0,0,0,1,0,0]
both_residuals:   basis contains [0,0,0,1,0,0] and [0,0,0,1,4,8]
```

## Result

The bounded actual-template scan tested:

```text
systems tested = 576
forced basis combinations = 4608
forced basis profiles tested = 576
coefficient-kernel profiles = 0
pair-projection-clear profiles = 0
proxy-positive profiles = 0
```

Every valid forced stable basis had a full-rank coefficient matrix:

```text
best failure = BASISFORCE_COEFFICIENT_FULL_RANK
```

The best bookkeeping row remains the base ledger:

```text
perturbation = base
assignment = signature_fiber_blocks
```

but it has no coefficient-kernel profile once the obstruction functional is
forced into the basis.

## Interpretation

This is a bounded local negative for the obvious repair after `abb1956`.
Forcing `[0,0,0,1,0,0]` into the stable basis removes the residual-slot issue,
but it also kills the actual right kernel in every tested forced stable basis.

The obstruction has moved from:

```text
residual slot coefficient nonzero
```

to:

```text
obstruction-functional basis inclusion + coefficient rank defect cannot be
co-designed in this bounded same-template/same-mask front.
```

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
- failure outside this bounded forced-basis front

## Next Target

The next constructive branch should co-design basis inclusion and right-kernel
rank defect from the start:

```text
m1-a327-basis-kernel-codesign
```

Do not keep perturbing the same ledger locally. Generate selected masks and
template vectors with a hard constraint that the obstruction functional belongs
to the basis and the nonbasis coefficient matrix has rank at most 5. Use
Python/NumPy first. Use Macaulay2 or Singular if the rank-defect constraints are
best expressed as minors, syzygies, or module conditions.
