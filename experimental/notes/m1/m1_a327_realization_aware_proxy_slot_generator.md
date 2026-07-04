# M1 a=327 realization-aware proxy-slot generator

Status:

EXACT_EXTRACTION_NO_A327 / RAWARE_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL

This packet follows `8032816` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous proxy-slot target was genuinely proxy-positive:

```text
target template = sheared_outside_seed_001
GF(12289) proxy rank/nullity = 1267 / 253
```

but the template-realization audit found no actual low-rank template-vector
realization of that synthetic functional target:

```text
linear rank/nullity = 35 / 7
rowspace-valid samples = 0
best failure = TEMPLATE_REALIZATION_ROWSPACE_FAIL
```

This branch moves realization inside the generator. It searches only actual
template-vector rowspaces and asks whether any stable basis already has a
single basis slot whose coefficient is zero in every nonbasis row. Such a slot
would give a proxy-slot kernel without synthetic rowspace edits.

## Search Result

The bounded actual-template scan tested:

```text
systems tested = 216
structural-pass candidates = 210
stable basis combinations = 23,663,322
stable basis profiles tested = 12,312
slot profiles tested = 73,872
actual zero-slot profiles = 0
pair-projection-clear actual slots = 0
proxy-positive actual slots = 0
```

The closest profile was:

```text
template = single_outside_w7_v3
assignment = signature_fiber_blocks
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
basis = slot_union_142_5_7_9_11_13_17
basis support sizes = [74,74,74,74,37,31]
basis-zero union size = 142
stable common multiplier dimension = 114
coefficient matrix shape = 12 x 6
coefficient rank/nullity = 6 / 0
best slot nonzero rows = 2
forced pair count in that slot = 15
```

So the bounded actual-template front does not contain a realized proxy-slot
kernel. The nearest actual profile is close in slot support but still has a
full-rank coefficient matrix and many forced pair projections.

## Interpretation

The synthetic proxy-slot mechanism is not invalidated. This branch shows that,
in the tested actual-template/stable-basis front, the mechanism is not already
present without editing functional rowspaces.

The next useful target is more specific than another broad scan: take the
near-miss profile with two nonzero slot rows and search for template-vector or
coordinate assignment moves that kill those two slot coefficients while keeping:

- support `[327,...,327]`;
- pair caps `<=255`;
- pair7 guards;
- functional span rank 6;
- no forced identities;
- no forced pair projections.

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
- success or failure outside the bounded actual-template front

## Next Target

Build a near-miss repair branch for the actual profile:

```text
single_outside_w7_v3 / signature_fiber_blocks
basis slot_union_142_5_7_9_11_13_17
slot = 3
slot_nonzero_rows = 2
```

The repair should act before proxy rank: alter template vectors or coordinate
assignment just enough to make the two residual slot coefficients vanish, then
rerun pair-projection and GF(12289) proxy-rank checks.
