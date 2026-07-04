# M1 a327 collision-budget syzygy search

Status:

EXACT_EXTRACTION_NO_A327 / SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY / PARTIAL / EXPERIMENTAL

This packet follows `856d30a` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The collision-budget codesign branch cleared the immediate gate:

```text
exact support collision = yes
q_variable_count >= 350 = yes
best q-variable count = 851
proxy rank/nullity = 851 / 0
```

So the remaining obstruction is not ledger feasibility. It is algebraic row
rank. This branch searches for small row-block dependencies inside the
collision-budget proxy matrices before proxy rank.

## Search

The scanner reconstructed all `240` collision-budget profiles from `856d30a`.
For each profile, it built the proxy matrix rows over `GF(12289)` with row
metadata and scored:

- zero rows;
- projective/scalar duplicate rows;
- low-rank blocks among rows sharing the same coordinate position;
- low-rank blocks among rows sharing both support hash and coordinate position;
- low-rank blocks among rows sharing the same support hash.

Results:

```text
collision-budget profiles reconstructed = 240
syzygy profiles scored = 240
syzygy-positive profiles = 0
proxy ranked profiles = 0
proxy positive profiles = 0
best syzygy score = 0
projective duplicate pairs = 0
```

The best scored profile was the same high-q collision-budget profile:

```text
template = lcodesign_0002_basis_simple
basis = collbudget_low_support_basis_support_0_11_6_7_10_5_2
q-variable count = 851
matrix shape = 1092 x 851
repeated support pairs = 1
row block rows/cols = 1092 / 851
zero rows = 0
projective duplicate pairs = 0
position low-rank blocks = 0 / 216 tested
support-position low-rank blocks = 0 / 74 tested
support low-rank blocks = 0 / 5 tested
```

## Interpretation

The tested collision-budget front has no small row-block syzygy of the types
checked here. The exact support collision is real and the q-budget is high, but
the induced proxy rows remain locally generic:

```text
exact support collision: achieved
q-budget: achieved
small row-block syzygy: not found
proxy rank: not run, because no syzygy-positive profile was found
```

This does not rule out larger or more structured dependencies. It says the
natural local row-block mechanisms do not explain a rank defect in this tested
front.

## Next Step

The next constructive branch should move from local row-block syzygies to a
global right-kernel design condition:

```text
m1-a327-collision-budget-rightkernel-codesign
```

Objective:

- preserve collision-budget profiles with `q_variable_count >= 350`;
- prescribe a candidate right-kernel vector or low-dimensional kernel subspace;
- codesign basis profiles so every nonbasis row annihilates that kernel;
- then proxy-rank only candidates with a verified right-kernel certificate.

This is now more promising than looking for accidental small blocks. Python and
NumPy remain first-line. Macaulay2 or Singular may help if the right-kernel
condition is recast as a module constraint. Sage should wait for a proxy-positive
or small exact certificate.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track proxy;
- global obstruction outside the tested collision-budget syzygy front.
