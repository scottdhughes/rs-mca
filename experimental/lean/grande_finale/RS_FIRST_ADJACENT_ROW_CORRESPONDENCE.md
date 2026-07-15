# Exact First Adjacent Reed--Solomon Row Correspondence

Status: **PROVED** for the full-field numerator equality (AD1).

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:exact-first-adjacent-row`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Exact `a`-support index has cardinality `choose |D| a` | `GrandeFinale.RSFirstAdjacentRow.card_exactSupportIndex` |
| Exact `(R-1)` supports form a binomial-sized family of distinct syndrome hyperplanes | `GrandeFinale.RSFirstAdjacentRow.exists_exactSupportHyperplanes` |
| At agreement `k+1`, the numerator equals `choose |D| (R-1)` | `GrandeFinale.RSFirstAdjacentRow.B_MCA_rsEval_eq_choose_redundancy_pred` |
| At agreement `k+1`, the numerator equals `choose |D| (k+1)` | `GrandeFinale.RSFirstAdjacentRow.B_MCA_rsEval_eq_choose_succ` |

The proof uses the barycentric weighted Vandermonde parity map and its exact
Reed--Solomon kernel. Exact `(R-1)` supports provide the finite hyperplane
family; the literal `max(M, choose M 2) < |F|` gate feeds the separating-line
compiler and gives the lower bound `M`. The exact support-atlas theorem gives
the matching upper bound, and binomial symmetry identifies the redundancy and
agreement forms of `M`.

## Scope boundaries

This module proves equation (AD1) with the manuscript's literal field-size
gate. It does not define the target-dependent first-safe scan or derive the two
AD2 threshold implications.

## Verification

```text
lake env lean GrandeFinale/RSFirstAdjacentRow.lean
```

The module prints the axioms of its principal results. No proof placeholder or
added axiom occurs.
