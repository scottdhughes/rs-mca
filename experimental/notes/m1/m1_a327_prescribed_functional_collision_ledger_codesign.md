# M1 a327 prescribed functional-collision ledger-codesign

Status:

EXACT_EXTRACTION_NO_A327 / LCODESIGN_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `e6fb874` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The fixed-ledger prescribed functional-collision realization branch proved that
actual `GF(17)` template vectors can realize a compressed functional-class
pattern. Its best realized template had only `11` functional classes and no
forced identities, but the quotient-variable budget collapsed to `129`, and the
proxy matrix was full rank.

This branch stops keeping the selected-class ledger fixed. It codesigns the
selected-class counts/assignments and actual template vectors together, with an
explicit quotient-variable floor before proxy rank.

## Search

The bounded run used actual template vectors only. For each template it solved
selected-class count constraints for:

- support `[327,327,327,327,327,327,327]`;
- safe pair caps;
- strong pair7 guards;
- no forced identities after realization;
- functional span rank `6`;
- enough quotient-variable budget to clear the branch floor when possible.

```text
template specs tested = 96
MILP-feasible templates = 96
systems tested = 192
structural-pass systems = 192
basis profiles constructed = 96
q-budget profiles = 12
proxy ranked profiles = 10
proxy positive profiles = 0
```

The best structural system was:

```text
template = lcodesign_0000_basis_simple
assignment = fiber_block
support = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
selected class sizes = {3:185, 4:6, 5:216, 6:105}
functional classes = 11
raw collision excess = 1766
forced functional identities = 0
functional span rank = 6
template equal pairs = []
```

The best proxy-ranked profile was:

```text
template = lcodesign_0001_basis_simple
basis = basisaware_1_4_7_8_9_10
q-variable floor = 350
best q-variable count = 771
matrix shape = 1012 x 771
proxy rank/nullity = 771 / 0
```

## Interpretation

This branch repaired the immediate problem from `e6fb874`: the quotient budget
no longer collapses to `129`. The best codesigned profile has `771` quotient
variables, comfortably above the `350` floor.

However, the proxy system is still full column rank:

```text
1012 rows
771 columns
rank = 771
nullity = 0
```

So the current obstruction is no longer synthetic realization and no longer
small quotient budget. It is lack of algebraic row dependency in the nonbasis
constraints. The selected-class ledger and actual template geometry can now be
codesigned to preserve guards and quotient slack, but the nonbasis rows remain
generic from the proxy-rank perspective.

## Next Step

The next constructive move should explicitly engineer row dependencies inside
the high-q-budget codesign front.

Recommended next branch:

```text
m1-a327-ledger-codesign-rowdependency-search
```

Objective:

- start from the `LCODESIGN` high-q-budget front;
- preserve support `[327,...,327]`, pair caps, pair7 guards, span rank `6`, and
  no forced identities;
- require `q_variable_count >= 350`;
- score repeated basis-coordinate rows, repeated support-coordinate rows,
  nested support sets, and large row-overlap blocks before proxy rank;
- proxy-rank only dependency-positive profiles.

Python remains the first-line generator. Macaulay2/Singular may help if the
row-dependency constraints are formalized as module/syzygy conditions. Sage
should remain reserved for exact `GF(17^32)` certification after a
proxy-positive realized candidate exists.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift for any new chamber;
- any MCA/protocol consequence from this list-track proxy;
- global obstruction outside the tested prescribed functional-collision
  ledger-codesign front.
