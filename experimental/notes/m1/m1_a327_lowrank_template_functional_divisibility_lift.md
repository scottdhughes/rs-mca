# M1 a327 low-rank template functional-divisibility lift

Status: CANDIDATE / FUNC_DIV_METADATA / PARTIAL / EXPERIMENTAL.

This packet follows `64e2fdf` and keeps the result strictly on the
INTERLEAVED_LIST track. The denominator is `17^32`, `mca_counted=false`, and
this is not an MCA row, not protocol soundness, not exact `Lambda_mu`, and not a
global `Lambda_mu(C,327) <= 6` claim.

## Source candidate

The source is the `mixed_rank6` low-rank template candidate:

```text
compressed coefficient matrix = 1533 x 1536
raw selected-class rows = 1777
proxy field = GF(12289)
proxy rank/nullity = 1280 / 256
```

The square free-column solve from `64e2fdf` reached exact `solve_right` over
`GF(17^32)` and timed out in submatrix echelonization. This branch exploits
the actual row structure instead of treating the system as a dense matrix.

## Functional-divisibility ledger

Each compressed low-rank row has the form:

```text
lambda . A(h) = 0
```

Rows are grouped by projective functional class `[lambda]`. For each class:

```text
S_lambda = { h in H : lambda . A(h) = 0 is required }
Z_lambda(X) = product_{h in S_lambda}(X - h)
```

The constraints become polynomial divisibility relations:

```text
lambda . A(X) = Z_lambda(X) Q_lambda(X)
```

The current `mixed_rank6` ledger has:

```text
functional classes = 15
forced functional identities = 2
quotient variables = 2327
functional-divisibility matrix = 3840 x 3863
formal full-space nullity lower bound = 23
```

The two forced identities are classes with support size `266 > 255`; those
functionals must vanish as degree-<256 polynomial identities.

## Proof gate

The matrix is wider than tall, so the full `(A,Q)` system has nonzero kernel
vectors by dimension count. That is not yet enough: a useful vector must have a
nonzero `A` component, satisfy all raw selected-class rows, produce seven
distinct codewords, and verify agreement directly on `H`.

Board-moving success requires Sage verification over `GF(17^32)`:

```text
H order = 512
seven distinct degree<256 codewords
one received word on H
agreement >=327 for all seven
denominator |F| = 17^32
mca_counted = false
```

## Next step

Extract a useful `A` from the functional-divisibility system, preferably by a
projection-aware solve that avoids spending time on pure `Q`-space kernel
directions. If a vector is found, certify it against all 1777 raw selected-class
rows before evaluating distinctness and agreement.
