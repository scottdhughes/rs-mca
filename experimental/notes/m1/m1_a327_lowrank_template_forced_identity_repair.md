# M1 a327 low-rank template forced-identity repair

Status: CANDIDATE / LOWRANK_REPAIR_SATURATION_PASS / PARTIAL / EXPERIMENTAL.

This packet follows `ff3c0da` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Objective

The `mixed_rank6` proxy-positive candidate was killed by forced-identity saturation:
forced rank `5`, reduced dimension `1`, and all `21` witness pairs
forced equal. This branch adds that obstruction as a filter for the low-rank
template search.

For every candidate, the scanner computes:

- projective functional classes;
- support sizes;
- forced identities with support `>255`;
- saturation after projection by forced identities;
- reduced template dimension;
- pair-projection ranks on the reduced template space.

## Result

The filter was applied to the ten existing low-rank template systems:

```text
candidates tested = 10
proxy-positive candidates = 8
saturation-pass candidates = 2
```

Failure counts:

```text
LOWRANK_REPAIR_PROXY_NOT_POSITIVE = 2
LOWRANK_REPAIR_REDUCED_DIM_TOO_SMALL = 6
LOWRANK_REPAIR_SATURATION_PASS = 2
```

The two surviving candidates are the `random_matroid_seeded_0_m6` assignments.
The best survivor has:

```text
template = random_matroid_seeded_0_m6
reduced template dimension = 6
forced equal pairs = 0
proxy rank/nullity = 1280 / 256
supports = [327,327,327,327,327,327,327]
pair7 counts = [204,204,204,204,204]
max pair count = 204
```

This means the next exact-lift target should not be `mixed_rank6`; it should be
the `random_matroid_seeded_0_m6` survivor after this saturation filter.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
