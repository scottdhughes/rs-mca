# M1 a327 cycleguard dependency-forced profile generator

Status:

EXACT_EXTRACTION_NO_A327 / CYCLEG_DEP_FORCED_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `db1182b` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The dependency-aware pre-chamber screen selected profiles with repeated support
signals, but it did not force repeated basis-coordinate rows. This generator
moves one level earlier: it constructs basis profiles by avoiding duplicated
support/functionality groups so those groups remain in the nonbasis constraint
set, then proxy-ranks the strongest forced profiles.

## Search

The bounded run reconstructed the same cycle-guarded structural candidate
front and generated forced basis profiles from collision groups.

```text
selected candidates = 255
candidates with collision groups = 62
candidate collision group counts = {"support": 237}
forced profiles constructed = 96
support-coordinate collision profiles = 0
coordinate collision profiles = 0
proxy ranked profiles = 8
proxy positive profiles = 0
```

The best proxy-ranked forced profile was:

```text
template = ninerow_P12_shear_c1_d15
basis = depforced_support_0_0_1_2_3_4_5
forced group type = support
forced group nonbasis count = 5
matrix shape = 919 x 678
support duplicate excess = 9
coordinate duplicate excess = 0
support-coordinate duplicate excess = 0
proxy rank/nullity = 678 / 0
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
```

## Interpretation

This is a sharper negative than passive dependency-aware screening. The tested
front contains support collisions, and the generator can force them to remain
nonbasis. But it found no projective coordinate collisions and no
support-coordinate collisions. The resulting proxy systems are still full
column rank.

So the current cycle-guarded front is not merely missing a better basis choice.
It is missing duplicated projective functional structure. Support-only repeats
do not create the needed basis-quotient nullity.

## Next Step

The next branch should modify the template/functionality layer, not just the
basis-selection layer:

- synthesize projective functional collisions deliberately;
- preserve support and pair guards while creating duplicate or low-rank
  nonbasis coordinate rows;
- keep support-coordinate collision groups outside the chosen basis;
- proxy-rank only profiles with actual coordinate or support-coordinate
  collisions.

If such profiles still full-rank, the next obstruction is a stronger statement:
even engineered functional collisions do not create basis-quotient nullity in
the tested cycle-guarded family.

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
- global obstruction outside the tested dependency-forced pre-chamber generator.
