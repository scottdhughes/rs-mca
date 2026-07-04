# M1 a=327 proxy-slot kernel generator

Status:

CANDIDATE / PSLOT_PROXY_KERNEL_TARGET / PARTIAL / EXPERIMENTAL

Realization status:

SYNTHETIC_FUNCTIONAL_PROXY_TARGET

This note records a proxy-kernel-prescribed generator for the M1 a=327
selected-class low-rank lane. It is an interleaved-list experimental ledger
only. It is not an MCA row, not protocol evidence, and not a global
`Lambda_mu(C,327)` statement.

## Purpose

The prior prescribed `Z_lambda` stable proxy audit found a stable coefficient
right kernel with no forced pair projections, but the expanded GF(12289) proxy
quotient matrix was full rank:

- previous proxy matrix shape = `1691 x 1450`
- previous proxy rank/nullity = `1450 / 0`

This branch targets the expanded proxy matrix directly. For each stable basis,
it tries single-slot prescriptions that set one basis coordinate to zero in all
nonbasis coefficient rows. If no nonbasis row becomes zero and all pair
projections remain nonzero in that slot, the corresponding `Q` block is a
guaranteed kernel block of the expanded proxy quotient system.

## Search Result

The bounded scan tested:

- systems tested = 216
- stable basis combinations = 23,663,322
- stable basis profiles tested = 12,312
- slot profiles tested = 73,872
- zero-row-free slot profiles = 73,872
- pair-projection-clear slot profiles = 42
- proxy-slot kernel targets = 42

The best target is:

- template = `sheared_outside_seed_001`
- assignment = `signature_fiber_blocks`
- support vector = `[327,327,327,327,327,327,327]`
- pair7 counts = `[233,233,233,233,233]`
- max pair count = 233
- functional classes = 27
- functional span rank = 6
- source basis = `slot_union_10_17_18_23_24_25_26`
- engineered basis = `slot_union_10_17_18_23_24_25_26__slot_0`
- basis class indices = `[17,18,23,24,25,26]`
- basis support sizes = `[3,3,3,3,3,1]`
- basis-zero union size = 10
- stable common multiplier dimension = 246
- q variable count = 1520
- coefficient matrix shape = `21 x 6`
- coefficient rank/right-kernel nullity = `5 / 1`
- proxy kernel slot = 0
- proxy kernel block degree = 253
- guaranteed proxy nullity lower bound = 253
- forced pair count = 0

## Proxy Audit

The best target was also ranked directly over GF(12289):

- proxy matrix shape = `1761 x 1520`
- proxy rank/nullity = `1267 / 253`
- proxy status = `PROXY_RANK_PASS`

This is the first proxy-positive checkpoint in this lane after the expanded
`Z_lambda` quotient obstruction appeared.

## Interpretation

This does not construct seven RS codewords. It shows that the synthetic
functional proxy layer can be engineered to have a large quotient kernel while
preserving:

- support 327 for all seven witnesses;
- pair caps below 255;
- pair7 guards with large slack;
- full functional span rank 6;
- no forced pair projections.

The remaining gap is realization. The prescribed functional coefficients must
still be lifted to actual template vectors or to an exact GF(17^32) system that
verifies seven distinct degree-<256 codewords and one received word on `H`.

## Non-claims

This ledger does not claim:

- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- Sage GF(17^32) exact lift
- realized exact template vectors for the prescribed coefficients

## Next Target

Move from synthetic proxy coefficients to realization:

1. Realize the `sheared_outside_seed_001` proxy-slot coefficients as actual
   low-rank template vectors or prove the realization obstruction.
2. If realization succeeds, run the exact GF(17^32) audit for the proxy-positive
   target.
3. If realization fails, write the obstruction as a coefficient-realization
   theorem target rather than returning to broad random mutation.
