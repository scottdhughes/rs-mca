# M1 a327 cycleguard pre-chamber rank-defect screen

Status:

EXACT_EXTRACTION_NO_A327 / CYCLEG_PRECHAMBER_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `f220bb6` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The previous generation-time run computed proxy rank only after exact
pair-clear rank-slack chambers appeared. This screen moves the rank-defect
proxy one step earlier: basis profiles are ranked by cheap basis-quotient shape
before chamber directions are sampled.

## Search

The bounded pass collected basis profiles first, ranked the best cheap shapes,
and only computed the basis-quotient proxy matrix for those profiles.

```text
basis profiles collected = 96
proxy ranked profiles = 8
proxy positive profiles = 0
chamber_sampled = false
```

The best pre-chamber profile was:

```text
template = ninerow_P12_shear_c0_d16
basis = basisaware_0_1_2_3_4_5
matrix shape = 586 x 345
proxy rank/nullity = 345 / 0
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
```

## Interpretation

Moving the screen earlier did reduce the quotient system size: the best matrix
here is `586 x 345`, much smaller than the previously exact-audited `993 x 752`
chamber. But the proxy rank is still full.

This says the first cheap-shape basis profiles are still algebraically generic
from the basis-quotient perspective. It does not rule out rank-defective
profiles elsewhere in the generated front.

## Next Step

The next search should not only minimize matrix shape. It should engineer
dependencies before proxy rank:

- prefer repeated nonbasis support sets;
- prefer repeated or low-rank nonbasis coordinate rows;
- add a cheap row-dependency surrogate before full proxy rank;
- bias basis selection toward profiles whose nonbasis rows share support
  hashes and basis-coordinate patterns.

Only profiles with proxy nullity should go to Sage `GF(17^32)` exact audit.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift for any new chamber;
- any MCA/protocol consequence from this list-track proxy.
