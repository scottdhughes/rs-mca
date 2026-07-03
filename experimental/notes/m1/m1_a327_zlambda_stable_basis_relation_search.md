# M1 a=327 Z_lambda stable-basis relation search

Status:

EXACT_EXTRACTION_NO_A327 / ZREL_STABLE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL

This note records a relation-first refinement after `06d5270`. The previous
generator ranked basis choices by `Z_lambda` zero-set union but still allowed
bases with union larger than 255 into the coefficient-kernel stage. This search
restricts attention to stable bases first:

`basis_zero_union_size <= 255`.

Only after that does it test the coefficient right-kernel, pair projections, and
proxy quotient rank. This is still an interleaved-list experimental ledger only.
It is not an MCA row, not protocol evidence, and not a global
`Lambda_mu(C,327)` statement.

## Source checkpoint

The previous stability-aware generator found:

- systems tested = 216
- basis profiles tested = 13,440
- coefficient-kernel profiles = 30
- stable basis-union profiles = 0
- best failure = `ZSTABLE_BASIS_UNION_TOO_LARGE`

The new question was whether the stable region itself contains a coefficient
right kernel that the low-union front missed.

## Result

For the same 36-template actual-template family:

- systems tested = 216
- structural-pass candidates = 210
- stable basis combinations = 23,663,322
- stable basis profiles tested = 12,312
- stable coefficient-kernel profiles = 0
- pair-projection-clear profiles = 0
- proxy candidates tested = 0
- proxy-positive candidates = 0

Failure counts:

- `ZREL_STABLE_COEFFICIENT_FULL_RANK`: 210
- `ZREL_LOW_FUNCTIONAL_SPAN`: 6

The best stable-front structural system was:

- template = `single_outside_w7_v0`
- assignment = `signature_fiber_blocks`
- support vector = `[327,327,327,327,327,327,327]`
- pair7 counts = `[233,233,233,233,233]`
- max pair count = 233
- functional classes = 17
- functional span rank = 6
- stable basis combinations = 515
- stable basis profiles tested = 95
- stable coefficient-kernel profiles = 0

## Interpretation

This is a stronger local negative than the previous low-union front. In the
tested actual-template family, when the basis-zero union is actually small
enough for a common multiplier of degree less than 256, the nonbasis
coefficient matrix is full rank in every tested stable basis profile.

So the obstruction is now sharper:

stable `Z_lambda` bases exist, but the tested actual-template family does not
put the nonbasis coordinate rows into a right-kernel hyperplane on those bases.

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

The next generator should be even more constructive:

1. choose six stable basis functionals with union at most 255;
2. prescribe a nonzero right-kernel vector on that basis;
3. generate nonbasis functionals constrained to the corresponding hyperplane;
4. require all 21 pair projections to be nonzero;
5. only then solve selected-class support and pair guards.

That is the first generator that will truly build the stable relation before
the selected-class support schedule.
