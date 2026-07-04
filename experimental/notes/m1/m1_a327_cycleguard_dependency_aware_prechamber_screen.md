# M1 a327 cycleguard dependency-aware pre-chamber screen

Status:

EXACT_EXTRACTION_NO_A327 / CYCLEG_DEP_PRECHAMBER_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `31d5b30` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The previous pre-chamber screen ranked basis profiles by cheap matrix shape.
That shrank the proxy matrix but still found full rank. This screen adds
dependency-aware features before proxy rank: repeated support hashes, repeated
projective basis-coordinate rows, and repeated support/coordinate pairs among
the nonbasis constraints.

## Search

The bounded pass collected the same number of pre-chamber basis profiles and
ranked the best dependency-aware targets over `GF(12289)`.

```text
basis profiles collected = 96
proxy ranked profiles = 8
proxy positive profiles = 0
chamber_sampled = false
```

The best proxy-ranked profile was:

```text
template = ninerow_P12_shear_c0_d1
basis = basisaware_0_1_2_3_4_5
matrix shape = 697 x 456
dependency score = 39
support duplicate excess = 4
coordinate duplicate excess = 0
support-coordinate duplicate excess = 0
proxy rank/nullity = 456 / 0
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
```

## Interpretation

Dependency-aware selection found a different front from pure cheap-shape
selection, but the proxy quotient matrix was still full column rank. The best
dependency profile has repeated support structure, but it does not create
repeated basis-coordinate rows or repeated support-coordinate rows, and it does
not create proxy nullity.

This is a useful negative for passive screening. It says repeated support
features alone are not enough; the generator must force row dependencies more
directly rather than selecting for weak repeat signals after profile generation.

## Next Step

The next branch should construct dependency-forced basis profiles instead of
only screening them:

- force repeated nonbasis support-coordinate row classes;
- build deliberate low-rank coordinate patterns in the basis quotient rows;
- penalize profiles whose duplicate supports have distinct projective
  coordinates;
- proxy-rank only profiles with engineered row collisions or algebraic
  dependency templates.

Only proxy-positive profiles should go to Sage `GF(17^32)` exact audit.

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
- global obstruction outside the tested dependency-aware pre-chamber screen.
