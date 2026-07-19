# Route-D rooted-emission cardinality: Lean map

This standalone Lean 4.14 package corresponds to
`experimental/notes/thresholds/route_d_rooted_emission_no_go.md` at
integration commit `3404d21b64c876c6d9b995ad3e29d7120ab27a54`
(source packet PR #913, payload
`7a5036e718bb8d1f87343e9ff9a1861918d4ae7b`).  The source packet remains a
`COUNTEREXAMPLE` to unrooted or selector-free support emission.

## Statement map

| Source statement | Lean declaration | Status | Exact boundary |
|---|---|---|---|
| “Minimal viable rooted-emission lemma,” final inequality only | `KbRowsharpRouteDRootedEmissionNoGo.rootedEmission_fixedLine_cardinality_of_injective` | PROVED | From an exact residual's duplicate-freeness and an already supplied injection into `Fin t × Fin p`, proves `residual.length ≤ t*p`. |
| Historical statement-target name | `KbRowsharpRouteDRootedEmissionNoGo.rootedEmission_fixedLine_target_unproved` | PROVED COMPATIBILITY ALIAS | Preserves the original declaration interface and forwards to the proved cardinality wrapper; new consumers should use the preceding name. |
| Primitive `F_17` fiber and punctured-padding certificates | declarations through `punctured_padding_obstruction_fixture` | PROVED | Existing executable finite regressions; they do not instantiate the rooted-emission interface. |

The cardinality proof encodes `Fin t × Fin p` into `Nat`, proves the encoded
residual has no duplicates, and bounds it by `List.range (t*p)`.  Its
load-bearing hypotheses are `hExact.1` and `hInjective`.  The exact residual
characterization and `hMarkPreserving` remain in the declaration for direct
integrated-stub interface continuity and boundary visibility, but are not
needed for this finite-set inequality.

The theorem does not construct `emit`; construct a received line or actual MCA
incidence; or prove noncontainment or a Hankel rank drop.  It does not identify
`Fin t` with `Z_rankdrop` or prove `|Z_rankdrop| ≤ t`.  It does not execute or
validate the eight first-match deletions.  The `commonCore` decoder is not a
decoder for the complete deployed marked key.  It proves no global Route-D
payment, deployed row, or threshold.

## Reproduce

```sh
cd experimental/lean/kb_rowsharp_route_d_rooted_emission_no_go
lake clean
lake build
cd ../../..
python3 experimental/scripts/verify_route_d_rooted_emission_no_go.py --check --self-test
python3 experimental/scripts/verify_route_d_rooted_emission_cardinality_formalization.py --check
python3 experimental/scripts/verify_route_d_rooted_emission_cardinality_formalization.py --tamper-selftest --check
```

The package is Std-only and pinned to `leanprover/lean4:v4.14.0`.
