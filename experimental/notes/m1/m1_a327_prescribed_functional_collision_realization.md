# M1 a327 prescribed functional-collision realization

Status:

EXACT_EXTRACTION_NO_A327 / PFCOLL_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `af58bd0` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The previous functional-collision template synthesis branch showed that local
single-entry template-vector mutations can preserve the structural guards, but
still leave the basis-quotient proxy matrix full rank. The next gate was to
avoid synthetic functional targets and ask whether actual low-rank template
vectors can realize a prescribed compressed functional-class pattern.

This branch keeps the selected-class coordinate ledger from the current
cycle-guarded endpoint fixed and synthesizes actual `GF(17)` template vectors
with prescribed collision-heavy geometries. It then checks the realized
functional ledger and proxy-ranks only structural-pass templates.

## Search

The bounded run tested actual template-vector families with prescribed
functional-collision structure.

```text
templates tested = 180
structural-pass templates = 72
prescribed collision realized templates = 72
basis profiles constructed = 48
proxy ranked profiles = 8
proxy positive profiles = 0
```

The best realized actual template was:

```text
template = pfcoll_0000_basis_simple
support = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 11
raw collision excess = 1766
forced functional identities = 0
functional span rank = 6
template equal pairs = []
```

The best proxy-ranked profile was:

```text
basis = basisaware_0_1_2_3_4_5
matrix shape = 370 x 129
proxy rank/nullity = 129 / 0
q variables = 129
row surplus = 241
```

## Interpretation

This is a useful narrowing. Actual template vectors can realize a much more
compressed functional-class pattern than the previous local-mutation endpoint:
the realized ledger has only `11` functional classes and no forced identities.
However, the best basis quotient is still full column rank over `GF(12289)`.

The failure is therefore no longer "the prescribed pattern is synthetic." This
branch realizes the pattern with actual template vectors. The remaining
obstruction is that the realized quotient-variable budget is too small and the
nonbasis constraints remain independent:

```text
best proxy matrix = 370 x 129
rank = 129
nullity = 0
```

Literal pair-difference collision geometries were also tested in the bounded
family, but they tended to trigger forced functional identities on this fixed
selected-class ledger. The structural-pass realization came from compressed
functional classes induced by the selected-class masks, not from safe literal
pair-difference repetitions.

## Next Step

The next constructive branch should not widen this fixed-ledger realization
blindly. It should search for a selected-class ledger and template geometry
together, with an explicit lower bound on quotient variables.

Recommended next branch:

```text
m1-a327-prescribed-functional-collision-ledger-codesign
```

Objective:

- keep actual template vectors, not synthetic functional rows;
- require support `[327,...,327]` and safe pair caps;
- realize compressed functional classes with no forced identities;
- avoid quotient-variable collapse like `q_variable_count = 129`;
- proxy-rank only candidates with enough quotient slack to plausibly produce
  nullity.

Python remains the first-line generator. Macaulay2 or Singular are useful only
if the realization/codesign constraints become a module, syzygy, or elimination
problem. Sage should remain reserved for exact `GF(17^32)` certification after
a realized proxy-positive template exists.

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
  realization front.
