# M1 a327 cycleguard stable-window exact audit

Status:

EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_NULLITY_ZERO / PARTIAL / EXPERIMENTAL

This packet follows `c142977` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global `Lambda_mu(C,327)` statement.

## Source chamber

The corrected chamber-realization checkpoint is:

```text
template = ninerow_P57_shear_c1_d1
basis = basisaware_0_1_2_3_4_5
direction = [1,4,0,0,10,0]
forced pairs = []
inactive rank/nullity = 4 / 2
zero class union size = 253
zero-row window dimension = 3
scalar required vanishing union size = 512
scalar stable-window dimension = 0
```

The key correction is that the `253`-point support is only a zero-row window.
It is not a scalar common-multiplier window for the whole selected-class
system. A scalar common multiplier would need to vanish on the active row
classes and on all nonzero basis classes, which covers all `512` coordinates.

So the scalar shortcut is closed. The next gate is the chamber-induced
basis-quotient functional-divisibility audit.

## Exact target

The reconstructed basis profile has:

```text
basis class indices = [0,1,2,3,4,5]
basis support sizes = [216,142,142,105,105,74]
quotient variables = 752
nonbasis constraints = 19
matrix shape = 993 x 752
```

The Sage audit builds this matrix over `GF(17^32)`. It records exact rank and
nullity. If nullity is positive, it then tests all 21 pair projections and
tries deterministic kernel samples.

## Exact Result

The exact Sage audit over `GF(17^32)` returned:

```text
matrix shape = 993 x 752
rank = 752
nullity = 0
failure mode = CYCLEG_EXACT_NULLITY_ZERO
```

Therefore this corrected cycle-guarded chamber has no nonzero
basis-quotient functional-divisibility kernel. It does not produce an `a=327`
candidate.

## Success gate

This becomes a proof record only if Sage verifies:

```text
GF(17^32)
H order = 512
seven distinct degree<256 codewords
one received word on H
agreement >=327 for all seven codewords
denominator |F| = 17^32
mca_counted = false
```

This packet is a local exact-audit obstruction for the named chamber only.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- any MCA/protocol consequence from this list-track proxy.
