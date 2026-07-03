# M1 a=327 prescribed Z_lambda-stable proxy audit

Status:

EXACT_EXTRACTION_NO_A327 / PZREL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

Realization status:

SYNTHETIC_FUNCTIONAL_PROXY_TARGET

This note records a single-case proxy quotient audit for the best prescribed
`Z_lambda`-stable relation target from `70b744e`. The target satisfied the
synthetic stable-relation gates, so the next required check was proxy quotient
rank over GF(12289).

This is an interleaved-list experimental ledger only. It is not an MCA row, not
protocol evidence, and not a global `Lambda_mu(C,327)` statement.

## Target

The audited target was:

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
- coefficient rank/right-kernel nullity = `5 / 1`
- right-kernel verified = true
- forced pair count = 0

## Proxy result

The proxy quotient matrix over GF(12289) was built and ranked:

- proxy matrix shape = `1691 x 1450`
- proxy rank/nullity = `1450 / 0`
- timeout = false

So the best synthetic stable-relation target is full rank at the proxy
quotient layer.

## Interpretation

This is a useful negative for the specific prescribed target. It shows that
the earlier gates are not enough:

- stable basis-zero union can be small;
- a coefficient right kernel can be prescribed;
- pair projections can all be nonzero;
- yet the `Z_lambda` polynomial expansion can still produce a full-rank proxy
  quotient matrix.

The next generator should therefore prescribe or optimize the proxy quotient
dependencies directly, not only the coefficient right-kernel relation.

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

Move one layer deeper:

1. keep stable basis union `<=255`;
2. keep no forced pair projections;
3. prescribe a right-kernel relation that survives the proxy quotient matrix,
   not just the coefficient matrix;
4. then revisit actual template-vector realization.
