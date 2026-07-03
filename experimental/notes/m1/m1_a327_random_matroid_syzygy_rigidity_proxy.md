# M1 a327 random-matroid syzygy-rigidity proxy

Status: AUDIT / SYZYGY_RIGIDITY_PROXY / PARTIAL / EXPERIMENTAL.

This packet follows `c3bb743` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The dependency-engineered branch tested:

```text
systems tested = 108
proxy-ranked candidates = 8
proxy-ranked basis profiles = 24
proxy-positive candidates = 0
best quotient proxy rank/nullity = 1385 / 0
```

This audit takes the best dependency-engineered profile and asks a smaller
module question in Macaulay2: before the polynomial vanishing factors are
expanded, does the nonbasis coefficient presentation already have a right
kernel that could explain quotient nullity?

## Macaulay2 proxy

For `random_matroid_v3_seed_007_m6` with `signature_fiber_blocks` and basis
`deterministic_random_basis_10`, the extracted nonbasis coefficient matrix is:

```text
coefficient matrix = 41 x 6 over GF(12289)
```

Macaulay2 result:

```text
rank = 6
right kernel = 0
left syzygy dimension = 35
```

The full proxy quotient for the same basis is:

```text
quotient matrix = 1626 x 1385
quotient proxy rank/nullity = 1385 / 0
```

So the coefficient-level module has many row syzygies, as expected from a
`41 x 6` full-rank presentation, but it has no right kernel. The syzygies are
row-side relations, not the right-kernel nullity needed to create a selected
class lift.

## Interpretation

This explains why support-level dependency engineering did not move the
quotient rank. The dependency-engineered branch created duplicate and nested
functional supports, but the nonbasis coefficient presentation still spans the
six-dimensional basis with no right kernel. After the polynomial evaluation
factors are introduced, the full quotient matrix remains full column rank.

The next constructive move should engineer right-kernel relations directly in
the nonbasis coefficient matrix, not just duplicate support sets or rely on row
syzygies.

## Tool notes

Macaulay2 was the right tool for this small module/syzygy proxy. It is not used
as final certificate machinery here. Sage remains reserved for exact
`GF(17^32)` candidates after proxy nullity appears. Singular can be used for the
same small module presentation if we need a cross-check; `msolve` is still only
relevant if rank-defect conditions are encoded as polynomial equations.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- global rank rigidity outside the tested proxy front.
