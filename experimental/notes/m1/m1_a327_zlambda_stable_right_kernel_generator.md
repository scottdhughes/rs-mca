# M1 a=327 Z_lambda-stable right-kernel generator

Status:

EXACT_EXTRACTION_NO_A327 / ZSTABLE_BASIS_UNION_TOO_LARGE / PARTIAL / EXPERIMENTAL

This note records a first stability-aware actual-template generator following
`f47d995`. The generator prioritizes basis choices with small `Z_lambda`
zero-set union before doing proxy quotient rank. The scope is the 36-template
actual-template family from the joint template/right-kernel search, with the 64
lowest-union bases tested for each structural-pass system.

This is an interleaved-list experimental ledger only. It is not an MCA row, not
protocol evidence, and not a global `Lambda_mu(C,327)` statement.

## Source checkpoint

The previous `Z_lambda` expansion audit found:

- profiles audited = 30
- stable lift targets = 0
- coefficient-kernel profiles over GF(17) = 30
- best basis-zero union size = 327
- best forced pair count = 15
- best failure = `ZEXP_BASIS_UNION_TOO_LARGE`

That showed the actual-template coefficient kernel exists, but does not survive
the vanishing-factor expansion gates.

## Generator gate order

For each actual-template selected-class system, this scanner checks:

1. support vector `[327,327,327,327,327,327,327]`
2. pair caps `<=255` and pair7 guards
3. no forced functional identities
4. functional span rank `6`
5. low basis-zero union among basis choices
6. coefficient right kernel over GF(17)
7. stable common multiplier dimension, requiring basis-zero union `<=255`
8. pair-projection nondegeneracy
9. proxy quotient rank only if the stability and pair gates clear

## Result

The run found:

- systems tested = 216
- structural-pass candidates = 210
- basis profiles tested = 13,440
- coefficient-kernel profiles = 30
- stable basis-union profiles = 0
- pair-projection-clear profiles = 0
- proxy candidates tested = 0
- proxy-positive candidates = 0

Failure counts:

- `ZSTABLE_COEFFICIENT_FULL_RANK`: 204
- `ZSTABLE_BASIS_UNION_TOO_LARGE`: 6
- `ZSTABLE_LOW_FUNCTIONAL_SPAN`: 6

The best profile remains the known `single_outside_w7_v1` /
`signature_fiber_blocks` pattern:

- basis = `zstable_union_327_0_1_2_3_4_5`
- basis support sizes = `[253,216,216,216,179,179]`
- coefficient matrix shape = `8 x 6`
- coefficient rank/nullity over GF(17) = `5 / 1`
- coefficient rank/nullity over GF(12289) = `5 / 1`
- kernel basis = `[[1,1,1,1,1,1]]`
- best basis-zero union size = 327
- stable common multiplier dimension = 0
- forced pair count = 15

## Interpretation

The low-union front did not find a stable right-kernel profile. In this
template family, the bases small enough to be considered early by the
`Z_lambda` gate are coefficient-full-rank; the coefficient kernels reappear only
when the basis-zero union has already grown to 327, which leaves no common
multiplier of degree less than 256.

This is not a theorem over all bases or all templates. It is a bounded
generator checkpoint for the current actual-template family and its 64
lowest-union basis choices per structural-pass system.

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

The next generator should build the stability relation first rather than
choosing low-union bases after the template is fixed. Concretely:

- prescribe a basis-zero union of size at most 255;
- impose a coefficient right-kernel relation on that basis;
- require all 21 pair projections to be nonzero on the kernel;
- then assign selected-class supports and pair guards around the relation.

That is a stronger design constraint than the current actual-template family
was built to satisfy.
