# M1 a=327 Z_lambda expansion-stability audit

Status:

EXACT_EXTRACTION_NO_A327 / ZEXP_EXPANSION_UNSTABLE / PARTIAL / EXPERIMENTAL

This note records a local audit following `b3d6a79`, the joint actual-template
right-kernel search. The previous checkpoint found actual template vectors with
a coefficient right kernel, but the proxy quotient matrix was still full rank.
This audit checks whether that coefficient kernel can survive multiplication by
the basis vanishing factors `Z_lambda`.

This is an interleaved-list experimental ledger only. It is not an MCA row, not
protocol evidence, and not a claim about global `Lambda_mu(C,327)`.

## Source checkpoint

The source search was:

- systems tested = 216
- actual-template right-kernel-positive candidates = 6
- proxy-positive candidates = 0
- best proxy quotient rank/nullity = 277 / 0
- best failure = JOINT_TEMPLATE_PROXY_FULL_RANK

The best actual-template candidate was:

- template = `single_outside_w7_v1`
- assignment = `signature_fiber_blocks`
- support vector = `[327,327,327,327,327,327,327]`
- pair7 counts = `[253,253,253,253,253]`
- max pair count = 253
- functional classes = 14
- functional span rank = 6

## Audit result

The expansion-stability audit found:

- profiles audited = 30
- stable lift targets = 0
- coefficient-kernel profiles over GF(17) = 30
- coefficient-kernel profiles over GF(12289) = 6
- failure counts = `{"ZEXP_BASIS_UNION_TOO_LARGE": 30}`

For the best profile:

- basis = `max_support_basis`
- basis class indices = `[0,1,2,3,4,5]`
- basis support sizes = `[253,216,216,216,179,179]`
- coefficient matrix shape = `8 x 6`
- coefficient rank/nullity over GF(17) = `5 / 1`
- coefficient rank/nullity over GF(12289) = `5 / 1`
- kernel basis = `[[1,1,1,1,1,1]]`
- basis-zero union size = 327
- stable common multiplier dimension = 0
- forced pair count = 15

The forced pairs are all pairs among witnesses `{2,3,4,5,6,7}`:

`P23, P24, P25, P26, P27, P34, P35, P36, P37, P45, P46, P47, P56, P57, P67`.

## Interpretation

The coefficient right kernel is real; it appears over GF(17), and for the best
profile also over GF(12289). The obstruction is not merely characteristic
mismatch. It is the next layer: after multiplying by the basis vanishing
factors, the right-kernel relation has no stable common multiplier because the
basis zero sets already cover 327 coordinates.

The same profile is also pair-degenerate. The kernel vector makes all pairs
among witnesses `{2,3,4,5,6,7}` project to zero, so even a stable multiplier
would not give seven distinct codewords without repairing pair projections.

## Non-claims

This audit does not claim:

- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- Sage GF(17^32) exact lift

## Next target

The next generator should optimize the actual `Z_lambda` layer directly:

- coefficient right kernel
- basis-zero union size at most 255, ideally with slack
- no forced pair projections
- support `[327,...,327]`
- pair caps `<=255`
- pair7 guards safe
- then proxy quotient nullity

This is narrower than another broad template scan. The missing object is a
right-kernel relation that remains valid after vanishing-factor expansion.
