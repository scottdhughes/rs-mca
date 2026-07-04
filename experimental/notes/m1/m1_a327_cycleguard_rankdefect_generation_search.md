# M1 a327 cycleguard rank-defect generation search

Status:

EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKGEN_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `639c399` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The previous rank-defect feedback packet post-ranked the 40 banked summaries
from `0fc5a00` and found no proxy-positive basis-quotient systems. This packet
moves the proxy rank test into chamber generation.

## Search

The bounded generation pass used the same cycle-pair guard, then tested
basis-quotient proxy rank as soon as an exact pair-clear rank-slack chamber was
found.

```text
basis profiles scored = 636
exact pair-clear rank-slack chambers seen = 8
proxy ranked profiles = 8
proxy positive profiles = 0
stopped reason = RANK_PROFILE_LIMIT_REACHED
```

The best live-ranked profile was:

```text
template = ninerow_P12_shear_c2_d1
basis = basisaware_0_1_2_6_7_8
matrix shape = 919 x 678
proxy rank/nullity = 678 / 0
forced pairs = []
inactive rank = 4
zero rows = 5
```

## Interpretation

The new feedback location is correct: proxy rank is now evaluated during
generation, not only after the fact. The first bounded pass still found only
full-rank basis-quotient systems.

This does not prove that no rank-defective cycle-guarded chamber exists. It
says the first eight generated exact pair-clear rank-slack chambers remain
proxy full-rank.

## Next Step

Do not send these full-rank chambers to Sage. The next constructive move is to
make low proxy rank part of the generator objective earlier, before basis
profiles are accepted. Possible directions:

- score candidate basis profiles by projected quotient-variable count and
  repeated support structure before sampling directions;
- bias toward lower-row, lower-column basis-quotient systems;
- add a cheap partial-rank screen on nonbasis constraints before pair-clear
  direction enumeration;
- widen generation only after this earlier rank-defect scoring is in place.

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
