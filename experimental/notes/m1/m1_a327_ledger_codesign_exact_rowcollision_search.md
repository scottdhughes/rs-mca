# M1 a327 ledger-codesign exact row-collision search

Status:

EXACT_EXTRACTION_NO_A327 / EXACT_ROWCOLLISION_Q_BUDGET_FAIL / PARTIAL / EXPERIMENTAL

This packet follows `b74ba9e` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The row-dependency branch found broad overlap and nested-support structure in
the high-q ledger-codesign front, but the proxy-ranked profiles remained full
column rank. Its best profiles also had no exact repeated coordinate, support,
or support-coordinate row collisions.

This branch asks for the sharper condition directly: can exact row-collision
profiles be forced while preserving the quotient-variable budget needed for a
meaningful proxy rank test?

## Search

The bounded run expanded the ledger-codesign front and tested both natural
basis profiles and forced-collision profiles. A forced profile tries to keep a
candidate-level collision group out of the basis so at least two members land in
the nonbasis row set.

```text
structural-pass systems = 360
candidates scanned = 60
candidates with collision groups = 60
candidate collision groups = {support: 60}
basis profiles constructed = 540
natural profiles constructed = 480
forced profiles constructed = 60
q-budget profiles = 36
exact-collision profiles = 438
exact-collision q-budget profiles = 0
proxy ranked profiles = 0
proxy positive profiles = 0
```

The best exact-collision profile was:

```text
template = lcodesign_0003_basis_simple
basis = basisaware_0_1_2_3_4_6
profile kind = natural
support = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 12
functional span rank = 6
forced functional identities = 0
matrix shape = 512 x 271
best exact-collision q-variable count = 271
repeated coordinate pairs = 0
repeated support pairs = 1
repeated support-coordinate pairs = 0
```

## Interpretation

Exact row collisions are available in the high-q ledger-codesign lineage, but
they are not compatible with the current q-budget floor. All `438`
exact-collision profiles fell below `q_variable_count >= 350`; the best
collision profile had only `271` q variables. Conversely, the `36` q-budget
profiles had no exact row collisions.

This is a sharper obstruction than the prior broad row-dependency result:

```text
overlap/nested support: present but proxy-full-rank
exact support collision: present but q-budget too low
exact coordinate/support-coordinate collision: absent in the tested profiles
```

No proxy rank was run in this branch because no profile simultaneously cleared
the exact-collision and q-budget gates.

## Next Step

The next constructive branch should stop treating exact collisions as a basis
selection effect and instead codesign the selected-class ledger to preserve q
variables while forcing support collisions.

Recommended branch:

```text
m1-a327-ledger-codesign-collision-budget-codesign
```

Objective:

- add support-collision terms directly to the selected-count/MILP objective;
- preserve support `[327,...,327]`, pair caps, pair7 guards, span rank `6`, and
  no forced identities;
- keep `q_variable_count >= 350`;
- require at least one exact support collision in the chosen basis profile;
- only then proxy-rank the candidate.

Python remains the right first-line tool for the count/assignment generator.
Macaulay2 or Singular can help later if the support-collision plus q-budget
constraints are recast as a module/syzygy problem. Sage should wait for a
proxy-positive or small exact certificate candidate.

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
- global obstruction outside the tested ledger-codesign exact-rowcollision
  front.
