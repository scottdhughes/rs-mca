# M1 a327 prescribed-kernel template realization

Status: EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_ROWSPACE_FAIL / PARTIAL / EXPERIMENTAL.

This packet follows `42e00f2` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The prescribed right-kernel proxy found a synthetic functional target with:

```text
coefficient rank/right-kernel nullity = 5 / 1
proxy quotient rank/nullity = 687 / 166
```

This branch asks whether that prescribed functional target can be realized by
actual seven template vectors over `GF(17)`, while preserving the same
selected-class support ledger.

## Linear realization audit

For each coordinate, the scanner takes the prescribed functional rowspace and
imposes that every selected witness difference lies in that rowspace. This gives
a homogeneous linear system in the `7 * 6 = 42` template-vector coordinates:

```text
linear matrix = 4193 x 42
rank = 35
nullity = 7
diagonal translation rank = 6
diagonal in kernel = true
non-diagonal kernel dimension = 1
non-diagonal quotient exhausted = true
```

So there is only one non-diagonal direction modulo diagonal translation.

## Result

The non-diagonal direction does not realize the prescribed rowspaces:

```text
samples tested = 263
rowspace-valid samples = 0
seven-distinct rowspace-valid samples = 0
best realized total effective cost = 1687
best realized functional classes = 33
best realized functional span rank = 5
rowspace failures in representative = 90
```

The best sampled template vectors are seven distinct as vectors, but their
realized functional span drops to 5 and the rowspaces do not match the
prescribed proxy target.

## Interpretation

The prescribed right-kernel relation survives quotient expansion as a synthetic
functional proxy, but this particular target is not directly realizable by
actual template-vector affine difference spaces. The obstruction is now a
template-realization constraint, not coefficient right-kernel existence and not
proxy quotient rank.

The next generator should put the realization constraint inside the search:
construct template vectors and right-kernel coefficient relations together,
rather than projecting an already-built functional profile into a right-kernel
hyperplane afterward.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- Sage `GF(17^32)` exact lift;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
