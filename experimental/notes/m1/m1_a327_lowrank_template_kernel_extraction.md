# M1 a327 low-rank template kernel extraction

Status: CANDIDATE / LOWRANK_KERNEL_SQUARE_SOLVE_TIMEOUT / PARTIAL / EXPERIMENTAL.

This packet follows `c5f1caa` and keeps the same track discipline:
INTERLEAVED_LIST only, denominator `17^32`, `mca_counted=false`. It is not an
MCA row; in particular, it is not an MCA row, not protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Source candidate

The source is the `mixed_rank6` low-rank selected-class template:

```text
raw selected-class rows = 1777
compressed low-rank basis rows = 1533
variables = 1536
proxy field = GF(12289)
proxy rank/nullity = 1280 / 256
```

The previous exact audit reached the compressed `GF(17^32)` matrix stage but
timed out in dense rank. Since the compressed homogeneous system has fewer rows
than columns, this branch tries to construct exact kernel vectors directly
instead of asking Sage for a full rank first.

A metadata pass confirmed the compressed coefficient matrix shape:

```text
1533 x 1536
```

The first square free-column solve reached `solve_right` over `GF(17^32)` and
was interrupted in the submatrix rank/echelonization step. This is still an
exact linear-algebra infrastructure timeout, not a mathematical obstruction.

## Strategies

The Sage audit includes:

1. square free-column solves in coefficient basis;
2. an evaluation-basis sparse formulation using values `A_j(h)` on `H`;
3. raw selected-class row certification after any vector is constructed.

The raw-row certification is mandatory. A vector is useful only if it satisfies
the full selected-class equations, produces seven distinct codewords, and
verifies the agreement vector directly on `H`.

## Proof gate

Board-moving success requires Sage verification over `GF(17^32)`:

```text
H order = 512
seven distinct degree<256 codewords
one received word on H
agreement >=327 for all seven
denominator |F| = 17^32
mca_counted = false
```

Anything short of that remains local experimental evidence.

## Non-claims

This packet does not claim:

- an `a=327` certificate unless the Sage proof record is present;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
