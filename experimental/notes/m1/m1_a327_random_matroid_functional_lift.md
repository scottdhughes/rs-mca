# M1 a327 random-matroid functional lift

Status: CANDIDATE / RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT_PROXY_FULL_RANK /
PARTIAL / EXPERIMENTAL.

This packet follows `68a0780` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Objective

The forced-identity repair branch found that the `mixed_rank6` survivor was the
wrong exact-lift target and that `random_matroid_seeded_0_m6` survives
forced-identity saturation:

```text
template = random_matroid_seeded_0_m6
assignment = sorted_block
supports = [327,327,327,327,327,327,327]
pair7 counts = [204,204,204,204,204]
max pair count = 204
proxy rank/nullity = 1280 / 256
forced equal pairs after saturation = 0
```

This branch reconstructs that survivor and builds the functional-divisibility
quotient system for exact lifting.

## Result

The survivor has:

```text
functional classes = 35
forced functional identities = 0
functional span rank = 5
annihilator dimension = 1
basis profiles tested = 11
best basis = max_support_basis
best quotient matrix = 1211 x 714
```

The functional span rank is only `5`, even though the template dimension is `6`.
The one-dimensional annihilator is diagonal for all seven witness template
vectors, so it does not by itself separate codewords. The quotient system must
therefore be tested in the rank-5 functional span.

The best basis quotient matrix was proxy-audited over `GF(12289)`:

```text
proxy rank/nullity = 714 / 0
```

An exact Sage rank attempt over `GF(17^32)` on the same `1211 x 714` sparse
functional-divisibility matrix was started and interrupted after stalling in
exact echelonization. The recorded status is therefore an execution bottleneck,
not an exact mathematical obstruction.

## Tool reading

The Sage matrix documentation supports sparse matrix construction from
dictionary entries and `sparse=True`; that is already the right representation
for this quotient matrix. Sage's optimized matrix backend list is strongest for
prime/small modular and small binary-extension cases, while this branch uses
`GF(17^32)` through extension-field arithmetic. The observed timeout is
therefore consistent with the documented backend landscape.

The PARI/GP documentation gives generic `matker` and `matsolve` routines over
compatible scalar arithmetic. That makes PARI useful for sanity checks and for
the FFELT arithmetic underneath Sage, but it is not a reason to replace this
branch's structured reduction with a blind GP matrix solve.

Local algebraic-geometry tools are also available: `msolve` and Macaulay2
(`M2`). They are not the first-line certificate tools for this checkpoint,
because the current system is linear over `GF(17^32)`, not a small polynomial
system over a prime field. They become relevant if the next branch converts the
functional-divisibility constraints into module/syzygy form, or if rank-feedback
is reformulated as an ideal or determinantal condition over a proxy field.

## Interpretation

This branch does not produce an `a=327` certificate. It says:

- the random-matroid survivor is the correct post-repair target;
- its functional-divisibility quotient is much smaller than the earlier dense
  coefficient system;
- the best proxy quotient is full rank;
- exact `GF(17^32)` rank remains an infrastructure bottleneck at `1211 x 714`.

The next branch should not run a longer blind Sage rank. It should either reduce
the functional quotient further, test other basis profiles by proxy and exact
small minors, build an evaluation/Fourier-basis sparse exact route, or formulate
a module/syzygy proxy where Macaulay2 or `msolve` can actually add leverage.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
