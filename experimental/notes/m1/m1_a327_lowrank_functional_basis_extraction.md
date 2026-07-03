# M1 a327 low-rank functional-basis extraction

Status: EXACT_EXTRACTION_NO_A327 / FUNC_BASIS_PAIR_FORCED_BY_FORCED_IDENTITIES / PARTIAL / EXPERIMENTAL.

This packet follows `edf8a8c` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Result

The functional-divisibility checkpoint had:

```text
functional classes = 15
forced functional identities = 2
functional-divisibility matrix = 3840 x 3863
formal full-space nullity lower bound = 23
```

This branch applies forced-identity saturation. Functionals that differ by
already-forced identities are equivalent on the reduced template space, so their
support sets must be merged before testing for additional support sizes above
255.

The saturation result is:

```text
forced rank = 5
reduced template dimension = 1
remaining projected functional classes = 0
zero projected functionals = 15
pure_q_kernel_impossible = true
```

The surviving one-dimensional template space is annihilated by every witness
template vector in `mixed_rank6`. Therefore all 21 witness pairs are forced
equal by the forced identities alone.

## Interpretation

This is a local exact obstruction for the `mixed_rank6` low-rank template
candidate. It is not a failure of the low-rank template idea in general.

The important lesson is that proxy nullity can be carried by forced functional
identities that collapse the witness template space. Future low-rank searches
must penalize or forbid support-`>255` functional classes after saturation, or
must verify pair projections after forced-identity reduction before exact
lifting.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
