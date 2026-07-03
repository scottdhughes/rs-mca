# M1 a=327 prescribed Z_lambda-stable relation generator

Status:

CANDIDATE / PZREL_PROXY_PENDING / PARTIAL / EXPERIMENTAL

Realization status:

SYNTHETIC_FUNCTIONAL_PROXY_TARGET

This note records the first prescribed stable-relation generator after
`9cc5e91`. The previous stable-basis relation search showed that the actual
template family has stable bases, but their nonbasis coefficient matrices are
full rank. This branch therefore prescribes the right-kernel relation on stable
bases first, checks pair projections, and leaves proxy quotient rank and actual
template-vector realization as the next gates.

This is an interleaved-list experimental ledger only. It is not an MCA row, not
protocol evidence, and not a global `Lambda_mu(C,327)` statement.

## Source checkpoint

The previous stable-basis search found:

- systems tested = 216
- stable basis profiles tested = 12,312
- stable coefficient-kernel profiles = 0
- best failure = `ZREL_STABLE_COEFFICIENT_FULL_RANK`

## Result

The prescribed stable-relation generator found:

- systems tested = 216
- structural-pass candidates = 210
- engineered profiles tested = 14,310
- pair-projection-clear profiles = 1,770
- proxy candidates tested = 0
- proxy-positive candidates = 0

The status is proxy-pending because this run intentionally disabled proxy rank
after an initial smoke run showed the proxy quotient rank step can dominate
runtime for this target.

The best synthetic target is:

- template = `single_outside_w6_v0`
- assignment = `signature_fiber_blocks`
- support vector = `[327,327,327,327,327,327,327]`
- pair7 counts = `[206,206,206,206,206]`
- max pair count = 206
- source basis = `pzrel_union_85_14_15_16_17_18_19`
- prescribed kernel = `random_kernel_0`
- kernel vector = `[1,9,4,9,13,14]`
- basis support sizes = `[29,28,21,6,1,1]`
- basis-zero union size = 85
- stable common multiplier dimension = 171
- coefficient matrix shape = `14 x 6`
- coefficient rank = 5
- right-kernel nullity = 1
- right-kernel verified = true
- coordinate rows changed = 14
- forced pair count = 0

## Interpretation

This is the first checkpoint in the current line that satisfies the intended
stable-relation design gates at the synthetic functional level:

- stable basis-zero union `<=255`
- nonzero stable multiplier room
- coefficient right kernel
- no forced pair projections
- support and pair guards inherited from an actual selected-class ledger

It is not yet an exact-lift candidate. The nonbasis coefficient rows were
projected into the prescribed right-kernel hyperplane, so the next proof gates
are:

1. proxy quotient rank over GF(12289);
2. actual template-vector realization of the engineered functionals;
3. Sage GF(17^32) exact audit only if those pass.

## Non-claims

This audit does not claim:

- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- Sage GF(17^32) exact lift
- realized exact template vectors for the prescribed coefficients

## Next target

The immediate next branch should run the proxy quotient rank for the best
synthetic target as a single resumable case with a timeout, rather than doing it
inside the broad generator loop.
