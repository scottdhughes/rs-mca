# M1 a327 quotient-subgroup long CP-SAT front

Status:

CANDIDATE / LONG_CPSAT_QUOTIENT_CP_FEASIBLE / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The first quotient-subgroup search found a feasible `s=4` count schedule, but
the realization and rank-aware generation layers stayed proxy full-rank. This
branch revisits the unresolved larger quotient fibers:

```text
s = 8, 16, 32
```

The goal is to determine whether those screens were merely time-limited in the
earlier bounded pass.

## Method

The long front reuses the OR-Tools count model from the quotient-subgroup
primal-kernel screen and keeps the same guards:

```text
support_i = 327 for all seven witnesses
pair equality on H <= 255
pair-to-7 selected counts >= 142
```

No Sage exact lift is attempted here. A feasible count schedule would still
need quotient-coordinate labelling, proxy-rank screening, pair-projection tests,
and only then a Sage `GF(17^32)` audit.

## Result

The bounded long-front run found count-feasible screens for all three larger
fiber sizes:

```text
screens tested = 3
CP-feasible screens = 3
best s = 8
best pair7 counts = [248,248,248,248,248]
best max pair equality on H = 248
best active partition count = 30
failure = LONG_CPSAT_QUOTIENT_CP_FEASIBLE
```

This is a count-layer candidate only. It does not yet construct quotient
polynomials or an exact `GF(17^32)` witness.

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
- global obstruction outside the bounded long CP-SAT front.
