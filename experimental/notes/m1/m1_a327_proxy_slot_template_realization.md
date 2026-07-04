# M1 a=327 proxy-slot template realization

Status:

EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_ROWSPACE_FAIL / PARTIAL / EXPERIMENTAL

This packet follows `ce5589c` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The proxy-slot branch found a synthetic functional target with:

```text
support vector = [327,327,327,327,327,327,327]
pair7 counts = [233,233,233,233,233]
max pair count = 233
coefficient rank/right-kernel nullity = 5 / 1
GF(12289) proxy quotient rank/nullity = 1267 / 253
```

This branch asks whether that prescribed proxy-slot functional target can be
realized by actual seven template vectors over `GF(17)` while preserving the
same selected-class coordinate ledger.

## Linear Realization Audit

For each coordinate, the scanner takes the prescribed proxy-slot functional
rowspace and imposes that every selected witness difference lies in that
rowspace. This gives a homogeneous linear system in the `7 * 6 = 42`
template-vector coordinates:

```text
linear matrix = 4191 x 42
rank = 35
nullity = 7
diagonal translation rank = 6
diagonal in kernel = true
non-diagonal kernel dimension = 1
non-diagonal quotient exhausted = true
```

So, modulo diagonal translation, there is only one non-diagonal realization
direction to test.

## Result

The sampled kernel directions do not exactly realize the prescribed rowspaces:

```text
samples tested = 519
rowspace-valid samples = 0
seven-distinct rowspace-valid samples = 0
best realized total effective cost = 1774
best realized functional classes = 32
best realized functional span rank = 5
rowspace failures in representative = 3
```

The best sampled template vectors are seven distinct as vectors, but the
realized functional span drops to 5 and three coordinate rowspaces fail to
match the prescribed proxy-slot target.

## Interpretation

This is a local realization obstruction for the named synthetic proxy-slot
target. It does not invalidate the proxy-slot kernel mechanism: the synthetic
functional model really has proxy nullity 253. The failure is that this
particular prescribed functional rowspace system is not realized by actual
`GF(17)^6` template vectors in the tested coordinate ledger.

The next generator should put the template-vector realization constraint inside
the proxy-slot search, instead of engineering a functional target first and
trying to realize it afterward.

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
- MCA/protocol consequence from this list-track proxy

## Next Target

Build a realization-aware proxy-slot generator:

1. start from actual template vectors;
2. choose stable bases with small zero-set union;
3. prescribe slot kernels only when the resulting rowspace constraints remain
   realizable by actual template vectors;
4. then rerun the GF(12289) proxy audit.

Sage GF(17^32) should wait until a target clears both proxy nullity and
template realization.
