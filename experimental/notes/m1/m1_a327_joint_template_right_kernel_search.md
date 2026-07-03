# M1 a327 joint template right-kernel search

Status: EXACT_EXTRACTION_NO_A327 / JOINT_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL.

This packet follows `f63a23f` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The prescribed-kernel proxy branch showed that coefficient right kernels can
create proxy quotient nullity, but the first prescribed target was not
realizable by actual template-vector rowspaces. This branch searches actual
`GF(17)^6` template vectors and right-kernel coefficient relations jointly.

The generator uses rank-5 hyperplane templates with controlled outside
directions, solves selected-class counts, assigns coordinates with the
dependency-aware orderings, and only then tests coefficient rank and proxy
quotient rank.

## Result

The bounded joint search tested:

```text
templates tested = 36
systems tested = 216
structural-pass candidates = 210
right-kernel-positive candidates = 6
proxy-ranked candidates = 6
proxy-ranked basis profiles = 42
proxy-positive candidates = 0
```

The best actual-template candidate is:

```text
template = single_outside_w7_v1
assignment = signature_fiber_blocks
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 14
functional span rank = 6
forced functional identities = 0
coefficient rank/right-kernel nullity = 5 / 1
proxy quotient rank/nullity = 277 / 0
```

Macaulay2 verifies the coefficient-level right kernel:

```text
coefficient matrix = 8 x 6
rank = 5
right-kernel generators = 1
left syzygy dimension = 3
```

## Interpretation

This branch reaches the fallback case from the right-kernel objective. The
right-kernel relation now exists for actual template vectors, not only for a
synthetic projection. However, after polynomial evaluation and the
`Z_lambda`-style quotient expansion, the proxy quotient matrix is full rank.

So the current obstruction is no longer coefficient right-kernel existence. It
is that the polynomial evaluation / vanishing-factor expansion destroys the
right-kernel relation in the tested actual-template family.

The next theorem or generator target should model this expansion explicitly:
find right-kernel relations that are stable after multiplication by the basis
vanishing factors, or prove that the tested one-outside rank-5 hyperplane
family always loses the coefficient kernel under quotient expansion.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- Sage `GF(17^32)` exact lift;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
