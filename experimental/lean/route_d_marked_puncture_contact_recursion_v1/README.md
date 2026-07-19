# Route-D marked-puncture contact recursion: Lean map

This standalone Lean 4.14 package corresponds to
`experimental/notes/thresholds/route_d_marked_puncture_contact_recursion_v1.md`
at integration commit `3404d21b64c876c6d9b995ad3e29d7120ab27a54`
(source packet PR #918, payload `5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`).

## Statement map

| Source statement | Lean declaration | Status | Exact boundary |
|---|---|---|---|
| Theorem 1, carried-`Q` erase/insert bijection | `RouteDMarkedPunctureContactRecursionV1.carriedQ_leastContact_erase_insert_equiv` | PROVED | Proves the generic subtype equivalence from explicit forward/backward structural and inverse-law hypotheses. |
| Theorem 1, least-contact disjointization used by the tagged union | `RouteDMarkedPunctureContactRecursionV1.least_contact_partition` | PROVED | Proves contact iff unique least contact from explicit existence and uniqueness hypotheses. |
| Corollary 2, hereditary boundary sum | `RouteDMarkedPunctureContactRecursionV1.hereditary_cardinality_bound` | PROVED | Proves the abstract sum inequality from exact carried cardinalities, deletion heredity, and an explicit inclusion-to-cardinality bound. |
| Finite F_7/F_11 recursion and obstruction fixtures | declarations ending in `_pin` | PROVED | Existing executable regressions; they do not instantiate the generic interfaces over finite support types. |

The first three declarations were previously honest statement targets with
`sorry`.  Their proofs are generic logical/cardinality wrappers.  They do not
formalize the source note end to end: signed locator deconvolution, the concrete
finite families and tagged-union cardinality identity, executable first-match
existence/uniqueness, deployed deletion heredity, local recursive bounds,
rank-drop routing, and the root-blind owner/payment remain outside this package.

## Reproduce

```sh
cd experimental/lean/route_d_marked_puncture_contact_recursion_v1
lake clean
lake build
cd ../../..
python3 experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --check
python3 experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py --tamper-selftest
python3 experimental/scripts/verify_route_d_marked_puncture_recursion_formalization.py --check
python3 experimental/scripts/verify_route_d_marked_puncture_recursion_formalization.py --tamper-selftest --check
```

The package is Std-only and pinned to `leanprover/lean4:v4.14.0`.
