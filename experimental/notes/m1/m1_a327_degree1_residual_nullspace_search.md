# M1 a=327 Degree-1 Residual Nullspace Search

Status: `ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL`

This note records a bounded null-vector-first search for an `a=327`
interleaved-list witness over

```text
RS[F_17^32, H, 256]
```

It is local audit/search evidence only. It does not update PR #133 and does
not claim a global upper bound at `a=327`.

## Model

Anchor

```text
P_1 = 0
D_i = P_i - P_1,  i = 2,...,7.
```

The tested family is

```text
D_i(X) = c_i L_i(X) R_i(X),
deg L_i = 254,
deg R_i <= 1,
deg D_i <= 255.
```

Here each `L_i` is a locator with 254 prescribed roots in `H`, each `R_i`
is a constant, `X`, or a one-root residual, and the constants `c_i` are
chosen from top value-collision labels. The search then evaluates the seven
codewords

```text
0, D_2, ..., D_7
```

and uses the largest value class at each coordinate as a capacity upper bound
for any received-word schedule.

If the capacity upper bound is below 327, no received-word assignment can
give all seven codewords agreement at least 327.

## Proxy Scan

Script:

```text
experimental/scripts/scan_m1_a327_degree1_residual_nullspace_search.py
```

Data:

```text
experimental/data/m1_a327_degree1_residual_nullspace_search.json
```

The proxy scan used `GF(12289)` and tested:

```text
source root tuples:        28
254-root tuples:           112
residual patterns/tuple:   13
constant candidates:       48,048
proxy a=327 candidates:    0
```

The best proxy capacity upper bound was

```text
293 < 327
```

from

```text
root tuple: all_pair_boundary_random_shuffle_0255_drop_first
residual:   common_root_000
```

So the proxy stage found no `a=327` candidate.

## Exact Sage Audit

Script:

```text
experimental/scripts/audit_m1_a327_degree1_residual_nullspace_search.sage
```

Data:

```text
experimental/data/m1_a327_degree1_residual_nullspace_search_exact_audit.json
```

The Sage audit recomputed seven selected candidates over `GF(17^32)`.
All selected candidates stayed below the target:

```text
exact selections:       7
exact candidates:       0
best exact capacity:    292 < 327
```

The exact-audited candidates are therefore route-cut as tested candidates.
This is not a route cut for all degree-1 residual families, all locator
choices, or all interleaved-list witnesses.

## Verification

Verifier:

```text
experimental/scripts/verify_m1_a327_degree1_residual_nullspace_search.py
```

The verifier checks the JSON ledgers, candidate counts, capacity bounds,
exact-audit status, and non-claims.

## Non-Claims

Not claimed:

- `a=327` interleaved-list certificate;
- global `Lambda_mu(C,327) <= 6`;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`;
- improvement over PR #133.

The denominator remains `|F| = 17^32`, and `mca_counted = false`.

## Next Step

This affine residual layer still has low value-class capacity. A natural next
bounded search is a multi-prime PARI/GP or Sage proxy sieve for the
all-pair-boundary embeddings, followed by exact `GF(17^32)` audit only for
proxy-positive candidates.
