# M1 a327 quotient-subgroup long-front realization

Status:

EXACT_EXTRACTION_NO_A327 / LONG_FRONT_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The long CP-SAT front found count-feasible schedules for:

```text
s = 8, 16, 32
```

This packet feeds those schedules through quotient-coordinate labelling and
proxy realization over `GF(193)`, which contains subgroups of orders `64`,
`32`, and `16`.

## Result

The bounded proxy-realization run did not find positive quotient nullity:

```text
screens realized = 3
proxy-positive screens = 0
best s = 32
best matrix = [59,48]
best rank/nullity = 48/0
failure = LONG_FRONT_REALIZATION_PROXY_FULL_RANK
```

No Sage `GF(17^32)` lift is attempted without proxy nullity and pair-projection
clearance.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track quotient-subgroup proxy;
- global obstruction outside the tested long-front realization schedules.
