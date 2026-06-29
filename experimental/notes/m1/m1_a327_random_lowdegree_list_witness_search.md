# M1 a327 random low-degree list-witness search

Status: PARTIAL / TESTED_TUPLES_NO_A327 / EXPERIMENTAL

This note records the first direct constructive search for an `a=327`
interleaved-list witness over

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` search packet, not an MCA `N_bad` row, and it does not claim
protocol soundness, ordinary list decoding beyond the stated predicate, exact
`Lambda_mu`, exact `delta*_C`, an `a=327` certificate, or a global upper bound
at `a=327`.

## Search Layer

The scanner generates deterministic low-degree tuple descriptors. The Sage
audit reconstructs the actual field `GF(17^32)`, the subgroup `H` of order
`512`, and the seven codewords for each tuple. For a fixed tuple, every
coordinate gives value classes among the seven codewords. The received word can
choose one value class at each coordinate.

Before running a full assignment solver, the audit applies the exact capacity
upper bound

```text
max-min agreement <= floor(sum_h max_value_class_size(h) / 7).
```

If this upper bound is below `327`, the tuple cannot produce an `a=327`
certificate under any received-word rescheduling.

## Candidate Families

The first layer tests direct low-degree codeword tuples rather than quotient
packet repair or RIM support replay:

```text
random_sparse_subfield:
  sparse degree<256 polynomials with GF(17) coefficients.

common_root_core:
  seven codewords sharing a large root-core locator with distinct residuals.

monomial_orbit:
  affine monomial codewords a_i X^d + b_i.

clustered_root_core:
  a common root core plus two residual clusters.
```

These are deliberately simple families. They test whether a naive direct
low-degree search creates enough value-class collision capacity to clear
`a=327`.

## Result

The exact Sage capacity gate evaluates all deterministic candidates over
`GF(17^32)`.

The result is:

```text
TESTED_TUPLES_NO_A327
candidate tuples tested:      116
best capacity upper bound:    291
best candidate:               common_root_core_r255_00
best largest-class histogram: 257 coordinates with class size 1,
                              255 coordinates with class size 7
```

No candidate has value-class capacity upper bound at least `327`, so no
assignment solver or certificate hardening is triggered.

## Interpretation

This is a route cut only for the named first-layer direct low-degree tuple
families. It does not rule out:

```text
larger random low-degree searches
adaptive support/interpolation searches
multi-stage constructive received-word design
non-quotient families outside these descriptors
global Lambda_mu(C,327) <= 6
```

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_random_lowdegree_list_witness_search.py
python3 experimental/scripts/verify_m1_a327_random_lowdegree_list_witness_search.py
sage experimental/scripts/audit_m1_a327_random_lowdegree_list_witness_search.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_random_lowdegree_list_witness_search.sage --write-json
```

to regenerate the exact JSON record.

## Not Claimed

```text
MCA N_bad
protocol soundness
ordinary list decoding beyond the stated interleaved-list predicate
a=327 interleaved-list certificate
global Lambda_mu(C,327) <= 6
exact Lambda_mu
exact delta*_C
improvement over PR #133
```
