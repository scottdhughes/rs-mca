# M1 a327 quotient-subgroup realization search

Status:

EXACT_EXTRACTION_NO_A327 / QUOTIENT_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `7e21f1d` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Input

The previous quotient-subgroup count screen found an OR-Tools feasible schedule:

```text
s = 4
fiber size = 4
quotient length = 128
quotient degree bound = 63
support vector = [327,327,327,327,327,327,327]
pair7 counts = [252,252,252,252,252]
max pair equality on H = 252
active partition count = 22
```

The count screen did not construct quotient polynomials. This branch expands
that aggregate count schedule into labelled quotient coordinates and tests the
first quotient-polynomial realization layer.

## Model

The quotient-subgroup form is:

```text
f_i(X) = P_i(X^4)
degree <= 63
deg(f_i) < 256
```

For each quotient coordinate, the scheduled partition imposes equality rows:

```text
P_i(y) = P_j(y)
```

for witnesses in the same partition block. The proxy realization uses quotient
differences relative to witness 7, so the proxy matrix has:

```text
variables = 6 * 64 = 384
```

The first proxy field is `GF(257)`, which contains a multiplicative subgroup of
order `128`.

## Result

The deterministic labelled expansion preserves the count-screen guards:

```text
support vector = [327,327,327,327,327,327,327]
pair7 counts = [252,252,252,252,252]
max pair equality on H = 252
```

The first labelled realization proxy is full rank:

```text
proxy field = GF(257)
proxy matrix = [495,384]
proxy rank/nullity = 384/0
failure = QUOTIENT_REALIZATION_PROXY_FULL_RANK
```

This is a route cut for this deterministic labelled expansion only. It does not
prove that the aggregate `s=4` count schedule is unrealizable under every
labelling, nor does it rule out the unresolved `s=8`, `s=16`, or `s=32`
quotient-subgroup schedules.

## Interpretation

The support and pair-cap layer remains useful: it showed that a quotient-native
schedule can clear the list-track count constraints. The current obstruction is
now exact quotient-polynomial realization, not selected-support accounting.

The next constructive move is to mutate the quotient-coordinate labelling or
choose the labelled partitions with rank feedback, aiming for:

```text
proxy nullity > 0
no forced pair equality
```

Only after that should a Sage `GF(17^32)` exact audit attempt a lift.

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
- global obstruction outside the labelled quotient schedule tested here.
