# M1 a=327 prescribed nonbasis kernel generator

Status:

EXACT_EXTRACTION_NO_A327 / PNK_NEAR_KERNEL_FORCED_PAIR / PARTIAL / EXPERIMENTAL

This packet follows `46b73ec` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous nonbasis-row dependency ansatz found near-kernel profiles but no
actual coefficient kernels. This branch adds the missing pair-projection gate:
for each retained best profile from the previous ledger, it searches bounded
row-deletion nullspaces for a kernel vector whose 21 witness-pair projections
are all nonzero.

The default profile source is `previous_summaries`, meaning the scan revisits
the retained best-profile front from `46b73ec`. It does not claim coverage of
all 4,260 forced stable-basis profiles.

No Sage exact lift is attempted in this branch.

## Result

The bounded prescribed-kernel scan tested:

```text
systems tested = 384
profile source = previous_summaries
previous front profiles = 70
target-present candidates = 84
forced basis profiles tested = 84
row-removal limit = 3
actual pair-clear kernel profiles = 0
near pair-clear kernel profiles = 0
actual kernel profiles = 0
near kernel profiles = 12
remove-limit full-rank profiles = 72
```

Failure counts by candidate:

```text
PNK_NEAR_KERNEL_FORCED_PAIR = 12
PNK_REMOVE_LIMIT_FULL_RANK = 72
PNK_TARGET_FUNCTIONAL_MISSING = 300
```

The best row remains:

```text
template = rankdefect_hyperplane_r0_out7
assignment = signature_fiber_blocks
target mode = primary_e4
basis = nbdep_primary_e4_union_253_1_7_14_15_16_18
coefficient matrix shape = [13,6]
coefficient rank = 6
minimum rows removed within bound = 2
removed row indices = [1,5]
residual row classes = [2,6]
kernel vector = [0,0,1,1,1,0]
forced pair count = 10
forced pairs = P12,P13,P15,P16,P23,P25,P26,P35,P36,P56
```

So the retained realized-template near-kernel front does not contain a
pair-clear kernel within the three-row deletion bound.

## Interpretation

This is a bounded local negative for the prescribed-kernel version of the
current rank-defect template rowspaces. The result sharpens the obstruction:
even when a two-row near-kernel appears, the best kernel vector is still trapped
in a ten-pair collapse pattern.

The next constructive route should stop searching these realized rowspaces
post hoc. It should generate template vectors and selected masks while
simultaneously enforcing:

```text
nonbasis rows orthogonal to a prescribed kernel vector
all pair projections nonzero
support = [327,...,327]
pair caps and pair-7 guards
```

That is a backward synthesis problem, not another profile scan.

## Non-claims

This packet does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- failure outside this bounded retained-profile front
- coverage of all forced stable-basis profiles from `46b73ec`

## Next Target

Move to a backward synthesis branch:

```text
m1-a327-pairclear-kernel-backward-synthesis
```

Use Python first to generate selected classes and template vectors from a
pair-clear kernel vector. If the constraint system becomes a module/syzygy or
determinantal problem, use Macaulay2 or Singular. Use `msolve` only if the
template-realization equations become genuinely nonlinear. Sage should wait
until a proxy-positive, realized, pair-clear target exists.
