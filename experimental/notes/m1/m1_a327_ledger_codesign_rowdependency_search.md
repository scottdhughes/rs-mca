# M1 a327 ledger-codesign row-dependency search

Status:

EXACT_EXTRACTION_NO_A327 / ROWDEP_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `af2492f` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The prescribed functional-collision ledger-codesign branch fixed the quotient
budget collapse from the fixed-ledger front. Its best proxy-ranked profile had
`771` quotient variables, but the proxy matrix was still full column rank. This
branch keeps the high-q-budget ledger-codesign front and asks whether the
nonbasis rows contain visible dependency structure before proxy rank.

## Search

The bounded run rebuilt the ledger-codesign front with actual template vectors
and selected-class assignments, then scored basis profiles by repeated
basis-coordinate rows, repeated support rows, repeated support-coordinate rows,
nested supports, and support overlap.

```text
structural-pass systems = 240
basis profiles constructed = 160
dependency-positive profiles = 160
dependency q-budget profiles = 18
proxy ranked profiles = 12
proxy positive profiles = 0
```

The best dependency-scored profile was:

```text
template = lcodesign_0002_basis_simple
basis = basisaware_1_4_7_8_9_10
support = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 12
functional span rank = 6
forced functional identities = 0
q-variable count = 802
matrix shape = 1043 x 802
best dependency score = 1954
nested support pairs = 4
support overlap total = 1025
exact repeated coordinate/support/support-coordinate pairs = 0 / 0 / 0
```

The best proxy-ranked profile was:

```text
template = lcodesign_0001_basis_simple
basis = basisaware_1_4_7_8_9_10
support = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 11
functional span rank = 6
forced functional identities = 0
q-variable count = 771
matrix shape = 1012 x 771
proxy rank/nullity = 771 / 0
failure = ROWDEP_PROXY_FULL_RANK
```

## Interpretation

The branch confirms that the high-q ledger-codesign front has broad support
overlap and nested-support structure, but that signal is not enough to produce
proxy nullity. The top 12 dependency-positive, q-budget profiles all remain
full column rank over the proxy field.

The diagnostic detail matters: the best profiles have no exact repeated
basis-coordinate rows, no repeated support rows, and no repeated
support-coordinate rows. The positive dependency score is coming from overlap
and nesting, not exact row collision. That makes the next target sharper.

## Next Step

The next constructive branch should force exact row collisions, not just broad
overlap:

```text
m1-a327-ledger-codesign-exact-rowcollision-search
```

Objective:

- preserve support `[327,...,327]`, pair caps, pair7 guards, span rank `6`, and
  no forced identities;
- keep `q_variable_count >= 350`;
- require repeated basis-coordinate or repeated support-coordinate classes
  before proxy rank;
- proxy-rank only profiles with exact collision evidence.

Python/NumPy remains the right first-line generator. Macaulay2 or Singular may
be useful only after the row-collision predicates are formalized as a
module/syzygy condition. Sage should wait for a proxy-positive realized
candidate or for a small exact certificate check.

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
- global obstruction outside the tested ledger-codesign rowdependency front.
