# M1 a327 cycleguard rank-defect feedback search

Status:

EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKDEFECT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `cf761a0` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The previous exact audit cut the best cycle-guarded chamber:

```text
matrix shape = 993 x 752
rank/nullity = 752 / 0
failure mode = CYCLEG_EXACT_NULLITY_ZERO
```

The next useful selection criterion is therefore basis-quotient rank defect
before spending Sage time.

## Search

This scan reuses the banked `0fc5a00` cycle-guarded front. It reconstructs the
40 banked exact pair-clear rank-slack summaries and ranks their
basis-quotient functional-divisibility matrices over `GF(12289)`, where
`12289 - 1` is divisible by `512`.

```text
front basis profiles tested = 876
front exact pair-clear rank-slack profiles = 80
ranked summaries = 40
proxy positive profiles = 0
failure mode = CYCLEG_RANKDEFECT_PROXY_FULL_RANK
```

The best proxy-ranked profile is:

```text
template = ninerow_P24_shear_c0_d1
basis = basisaware_0_1_2_3_4_7
matrix shape = 777 x 536
proxy rank/nullity = 536 / 0
forced pairs = []
inactive rank = 4
```

## Interpretation

The result says the currently banked top summaries remain full-rank under the
cheap basis-quotient proxy. It does not say that no cycle-guarded chamber can
have rank defect, and it does not say that `a=327` is impossible.

The constructive implication is narrower:

```text
do not select chambers only by pair-clear/rank-slack metadata;
add basis-quotient proxy nullity to the chamber-generation objective.
```

## Next Step

The next branch should generate new chambers with rank-defect feedback inside
the search loop, rather than ranking only the already banked summaries. A
profile should be preferred only if it keeps:

```text
exact pair-clear chamber
inactive rank slack
low basis-quotient proxy rank
positive proxy nullity if possible
```

Only proxy-positive chambers should go to Sage `GF(17^32)` exact audit.

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
