# Reed--Solomon Parity-Kernel Correspondence

Status: **PROVED** for the weighted Vandermonde parity-check construction
listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially the
Reed--Solomon syndrome construction in the proof of
`thm:exact-first-adjacent-row` (AD1).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Barycentric evaluation weights are nonzero | `GrandeFinale.RSParityKernel.barycentricWeight_ne_zero` |
| Every at-most-`R` weighted Vandermonde column family is independent | `GrandeFinale.RSParityKernel.weightedColumns_linearIndependent` |
| The height-`R` parity map is surjective when `R <= |D|` | `GrandeFinale.RSParityKernel.parityCheck_surjective` |
| Every degree-`< k` evaluation word is killed when `k + R = |D|` | `GrandeFinale.RSParityKernel.rsEval_le_ker_parityCheck` |
| The parity kernel equals the existing Reed--Solomon evaluation code | `GrandeFinale.RSParityKernel.ker_parityCheck_eq_rsEval` |

The annihilation proof applies `Lagrange.coeff_eq_sum` to
`P * X^j` for each `j < R`. The coefficient at degree `|D|-1` vanishes, and
the resulting barycentric identity is exactly the corresponding parity row.
Kernel equality then follows from evaluation injectivity and rank--nullity.

## Scope boundaries

This module constructs the exact syndrome map and proves the MDS column
independence needed for AD1. It does not yet identify the spans of individual
`(R-1)`-element error supports with distinct hyperplanes, prove the exact
support upper bound, or derive the final AD1 equality and AD2 implications.

## Verification

```text
lake env lean GrandeFinale/RSParityKernel.lean
```

The module prints the axioms of its principal results. No `sorry`, `admit`,
`native_decide`, or added axiom occurs.
