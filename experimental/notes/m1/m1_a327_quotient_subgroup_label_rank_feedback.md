# M1 a327 quotient-subgroup label rank feedback

Status:

EXACT_EXTRACTION_NO_A327 / QUOTIENT_LABEL_RANK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows the first `s=4` quotient-subgroup realization screen and
remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The aggregate `s=4` CP-SAT schedule is support-feasible, but the first
deterministic labelling of its 22 active partition types onto 128 quotient
coordinates had proxy rank/nullity:

```text
GF(257) matrix [495,384]
rank/nullity = 384/0
failure = QUOTIENT_REALIZATION_PROXY_FULL_RANK
```

This branch keeps the aggregate schedule fixed and mutates only the labelled
quotient-coordinate assignment. The selected-block counts, support vector,
pair-to-7 counts, and pair caps are preserved by construction.

## Search

The rank-feedback scanner tests:

- grouped baseline labelling;
- round-robin labelling;
- residue-spread labellings;
- deterministic random shuffles.

For every labelling, it rebuilds the quotient equality matrix over `GF(257)`.
A useful next candidate requires:

```text
proxy nullity > 0
no forced pair equality
```

## Result

The bounded scan did not find a positive-nullity labelling:

```text
labellings tested = 72
proxy-positive labellings = 0
best label = grouped_baseline
best matrix = [495,384]
best rank/nullity = 384/0
failure = QUOTIENT_LABEL_RANK_PROXY_FULL_RANK
```

The result is local to the tested labelled assignments. It does not rule out:

- a different labelling of the same aggregate schedule;
- a rank-aware CP-SAT schedule rather than post-hoc label mutation;
- the unresolved `s=8`, `s=16`, or `s=32` quotient screens;
- a different quotient-subgroup construction.

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
- global obstruction outside the tested quotient-coordinate labellings.
