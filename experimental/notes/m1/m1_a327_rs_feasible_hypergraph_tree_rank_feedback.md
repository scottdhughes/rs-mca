# M1 a327 RS-feasible hypergraph tree-rank feedback

Status: EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_EXACT_NULLITY_ZERO /
PARTIAL / EXPERIMENTAL.

This packet feeds the exact tree-divisibility obstruction from `aed0ef0` back
into selected-class hypergraph generation. It searches for RS-feasible
selected-class designs with exact support `327` and uses a finite-field proxy
rank to screen for positive tree-divisibility nullity before spending Sage time
over `GF(17^32)`.

It remains INTERLEAVED_LIST work only. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Source obstruction

The previous selected-class thin target was killed by exact tree-divisibility
rank:

```text
target = 9fcdb02_thin_selected_class
best_tree_shape = [2874,372]
best_tree_rank = 372
best_tree_nullity = 0
failure = TREE_DIVISIBILITY_NULLITY_ZERO
```

That moved the live obstruction from pair-cap feasibility to cycle-rank
constraints in the selected-class equality graph.

## Feedback model

The scanner generates selected received-class hypergraphs satisfying:

```text
support_i = 327 for all i
pair_ij <= 255 for all i<j
pair_i7 >= 142 for i=1,...,5
```

It then assigns the selected classes to the 512 coordinates, builds pair sets
`S_ij`, chooses several spanning trees, and computes a tree-divisibility proxy
rank over the prime field `GF(12289)`, which has a subgroup of order `512`.

The proxy rank is not a proof over `GF(17^32)`. It is a screen for positive
tree-divisibility nullity. Only proxy-positive cases should be sent to the
expensive exact Sage audit unless a diagnostic exact check is useful.

## First scan result

The first feedback batch tested 12 assigned RS-feasible hypergraphs. All passed
the support, pair-cap, and pair-7 guards. None had positive proxy nullity.

The best proxy case was:

```text
profile = tree_nullity_weighted_path
assignment_seed = 6
supports = [327,327,327,327,327,327,327]
pair7_counts = [172,171,171,171,172]
max_pair_count = 255
best_tree = pair7_heavy_tree
proxy_matrix_shape = [2924,424]
proxy_rank = 424
proxy_nullity = 0
failure = RANK_FEEDBACK_PROXY_FULL_RANK
```

The best proxy case was also audited over `GF(17^32)`:

```text
exact_matrix_shape = [2924,424]
exact_rank = 424
exact_nullity = 0
failure = RANK_FEEDBACK_EXACT_NULLITY_ZERO
```

So this first rank-feedback batch did not escape the tree-rank obstruction.
This is still not a global obstruction; it is a bounded negative for the tested
feedback profiles and the best exact-audited candidate.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

If no proxy-positive candidate appears after broadening the feedback search,
the next design layer should alter the selected-class incidence model itself:
reduce cycle pressure rather than merely reweight tree edges. If a proxy-positive
candidate appears, run the Sage exact tree-divisibility audit over `GF(17^32)`
and then test pair projections.
