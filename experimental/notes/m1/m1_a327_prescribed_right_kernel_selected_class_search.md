# M1 a327 prescribed right-kernel selected-class search

Status: CANDIDATE / PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL.

This packet follows `6d58c96` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous right-kernel-engineered branch tested:

```text
systems tested = 108
structural-pass candidates = 96
coefficient profiles tested = 3276
right-kernel-positive candidates = 0
```

That said the tested generator was still choosing full-rank nonbasis
coefficient presentations. This branch changes the order of operations: it
prescribes a coefficient right-kernel relation first, while preserving the
selected-class support ledger from structurally valid candidates.

## Result

The prescribed-kernel proxy scan tested:

```text
systems tested = 108
structural-pass candidates = 96
engineered profiles tested = 6912
right-kernel-positive candidates = 96
proxy-ranked candidates = 12
proxy-ranked basis profiles = 12
proxy-positive candidates = 12
```

The best proxy-positive target is:

```text
template = random_matroid_v3_seed_010_m6
assignment = signature_fiber_blocks
basis = max_support_basis__slot_6_kernel
support vector = [327,327,327,327,327,327,327]
pair7 counts = [233,233,233,233,233]
max pair count = 233
functional classes = 45
coefficient rank/right-kernel nullity = 5 / 1
proxy quotient rank/nullity = 687 / 166
```

Macaulay2 verifies the engineered coefficient presentation:

```text
coefficient matrix = 39 x 6
rank = 5
right-kernel generators = 1
left syzygy dimension = 34
```

## Interpretation

This is the first branch in this line where the right-kernel mechanism survives
the proxy quotient expansion: the quotient matrix over `GF(12289)` has nullity
166.

The caveat is important. The selected-class support ledger is inherited from
actual template candidates, but the nonbasis coefficient rows are prescribed in
basis coordinates. A later branch must realize these engineered functional rows
by actual template vectors before this can become a Sage exact-lift target.

So the next problem is no longer "can right-kernel relations produce proxy
nullity?" In this synthetic functional target, yes. The next problem is:

```text
Can the prescribed basis-coordinate rows be realized by seven template vectors
and selected classes while preserving support and pair guards?
```

## Tool notes

Python finite-field elimination is the right screen for the prescribed
coefficient relation and proxy quotient. Macaulay2 is useful for cross-checking
the small coefficient module. Sage remains reserved for an exact `GF(17^32)`
audit after the engineered coefficient rows are realized by actual template
vectors.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- realized exact template vectors for the prescribed coefficients;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
