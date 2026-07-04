# M1 a327 low-rank common-kernel degeneracy probe

Status: EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_COMMON_KERNEL_DEGENERACY / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Probe

The previous low-rank template ledgers had a strong-looking proxy signal:

```text
proxy rank / nullity = 1280 / 256
```

The probe checks whether this is genuine rank defect or a common-kernel
artifact. For a low-rank template with dimension 6, raw selected-class rows are
literal witness-difference functionals. Let `Lambda` be the span of all such
functionals. If:

```text
rank(Lambda) = 5
proxy rank = 5 * 256 = 1280
proxy nullity = 1 * 256 = 256
```

then the proxy kernel is exactly the common annihilator `Lambda^perp` tensored
with degree `<256` polynomials. If the co-occurrence graph on the seven
witnesses is connected, this common-kernel direction forces every pair of
witness codewords equal.

## Result

The two tested proxy-positive low-rank templates both satisfy the common-kernel
degeneracy signature:

```text
mixed_rank6:
  functional span rank is 5
  common-kernel dimension is 1
  proxy rank/nullity = 1280 / 256
  co-occurrence graph connected
  all 21 witness pairs forced equal on the common kernel

random_matroid_seeded_0_m6:
  functional span rank is 5
  common-kernel dimension is 1
  proxy rank/nullity = 1280 / 256
  co-occurrence graph connected
  all 21 witness pairs forced equal on the common kernel
```

So the apparent 256-dimensional proxy nullity is not a path to seven distinct
codewords for these two templates. It is the one-dimensional common annihilator
times `F[X]_<256`.

## Interpretation

This is a local route cut for the tested low-rank templates:

- `mixed_rank6`;
- `random_matroid_seeded_0_m6`.

It explains why the earlier forced-identity saturation pass was not enough:
there need not be a single functional with support at least 256. The aggregate
span can still have codimension 1, and the surviving common-kernel direction
can collapse every witness pair once the co-occurrence graph is connected.

The next constructive attack should avoid templates with
`rank(Lambda)<template_dimension` unless the free complement separates at least
one disconnected witness component. For the current connected ledgers, a useful
low-rank template needs full functional span or additional compressed nullity
beyond `256*(template_dimension-rank(Lambda))`.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- a global obstruction outside the tested low-rank templates.
