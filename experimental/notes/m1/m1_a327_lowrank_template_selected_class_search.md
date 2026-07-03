# M1 a327 low-rank template selected-class search

Status: CANDIDATE / LOWRANK_TEMPLATE_PROXY_POSITIVE / PARTIAL /
EXPERIMENTAL.

This packet tests a low-rank coefficient template route for the M1 `a=327`
interleaved-list lane. It remains INTERLEAVED_LIST work only. It is not an MCA
row, not protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Motivation

The previous selected-class rank-defect search generated `14` RS-feasible
selected-class hypergraphs, but every proxy quotient matrix had full column
rank:

```text
best_proxy_rank = 1536
best_proxy_nullity = 0
```

So generic selected-class hypergraphs are still too algebraically independent.
This branch changes the codeword parameterization rather than only changing the
selected-class hypergraph.

## Low-rank coefficient template

Fix coefficient vectors `v_1,...,v_7 in F^m` and write

```text
P_i(X) = v_i dot A(X)
```

where `A(X)` is an `m`-tuple of unknown degree-`<256` polynomials. At coordinate
`h`, a selected class `C_h` imposes the equations

```text
(v_i - v_a) dot A(h) = 0
```

for a basis of the affine differences inside `C_h`. Therefore the equation
cost at `h` is the affine rank of `{v_i : i in C_h}`, not `|C_h|-1`.

This directly attacks the quotient-rank obstruction by reducing the effective
number of independent equality equations per selected class.

## First templates

The scanner tests:

```text
pencil_line_arrangement_m2
planar_rich_rank5
pair7_guarded_rank5
mixed_rank6
random_matroid_seeded_0_m6
```

Each candidate still has to satisfy:

```text
support_i = 327
pair_ij <= 255
pair_i7 >= 142
```

The Sage audit ranks the low-rank template matrix over the proxy field
`GF(12289)` first and banks proxy-positive candidates before attempting dense
`GF(17^32)` rank. Exact `GF(17^32)` auditing is an explicit follow-on step.

## First-pass result

The scanner generated `10` low-rank template selected-class systems. The proxy
audit over `GF(12289)` found positive nullity:

```text
proxy_positive_candidates = 8
best_template = mixed_rank6
best_effective_cost = 1533
best_variable_count = 1536
best_proxy_rank = 1280
best_proxy_nullity = 256
```

This is not an exact proof record. It is a strong proxy candidate showing that
the low-rank template model can manufacture the rank defect that the generic
selected-class quotient search could not find. Exact `GF(17^32)` rank and pair
projection audits remain pending.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- not an MCA row;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.

## Next step

If a proxy-positive template appears, run the exact `GF(17^32)` audit with an
explicit timeout/batching plan, test all 21 pair projections on the exact
kernel, and construct an explicit received word only if no pair is forced equal.
