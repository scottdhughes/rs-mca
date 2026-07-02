# M1 a=327 repaired-skeleton Sage-native cache

Status: `EXACT_STATE_CACHE / EXPERIMENTAL`

This branch attempts to upgrade the repaired-skeleton cache from
`RECONSTRUCTION_ONLY` to a Sage-native prepared linear-algebra artifact.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an infrastructure/cache packet. It is not an MCA row, not a protocol
claim, and not a public-board update.

## Target State

The repaired skeleton remains:

```text
capacity              = 333
B({1,7})..B({5,7})    = [1024,657,656,1024,1024]
collapse pattern      = [[1,4,5,7],[6],[3],[2]]
matrix shape          = [354,1536]
rank                  = 354
nullity               = 1182
fixed specs           = 129
free pattern          = d2_first_free
```

The failed split damage to eventually compensate is:

```text
capacity loss = 18
B({2,7}) loss = 64
B({3,7}) loss = 64
B({4,7}) loss = 512
B({5,7}) loss = 0
```

## Cache Plan

The Sage audit tries to persist a native artifact under
`experimental/data/cache/` containing:

```text
independent matrix A
right-hand side
pivot columns
free columns
pivot matrix
base vector
fixed specs
field and metadata hashes
```

The successful cache artifact is:

```text
cache type      = SAGE_NATIVE
artifact        = experimental/data/cache/m1_a327_repaired_skeleton_budget32_prepared_state.sobj
artifact hash   = f77410189226820cf8e8a2830f3a48523a92e485347702754c854fa8955addb4
artifact size   ~= 92 MB
matrix shape    = [354,1536]
rank/nullity    = 354 / 1182
```

The Python verifier checks only JSON metadata and hashes. Loading Sage-native
objects is reserved for the Sage audit.

## Append Test

The minimal append test is deliberately small. It loads the cached base state
and enforces one `split_4_from_157` row by solving a one-row residual constraint
through the cached pivot/free structure. The goal is not to run the full
compensated grid yet; it is to prove the cache can avoid the timeout seen in
`1a75dfe`.

The append test passes:

```text
status          = CACHE_SMALL_APPEND_PASS
capacity        = 260
pair values     = [1024,657,656,512,1024]
collapse        = [[1,5,7],[4,6],[3],[2]]
```

This append vector is not a candidate. It only proves that cached
pivot/free-state append solving now constructs exact vectors without repeating
the full repaired-skeleton setup.

## Non-claims

- No `a=327` interleaved-list certificate.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.

## Next Step

Rerun the compensated repaired-skeleton split grid from the cached state. The
first production search should target the same 45 systems from `1a75dfe`, but
use the cached pivot/free machinery instead of `repaired_context()`.
