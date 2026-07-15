# Largest-Fiber Moment Correspondence

Status: **PROVED** for the two exact finite inequalities listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`lem:largest-fiber-log-detail` and `lem:q-to-sp-detail`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Exact mean `bar N = M/L` | `GrandeFinale.LargestFiberMoment.fiberMean` |
| Normalized `q`-moment | `GrandeFinale.LargestFiberMoment.normalizedMoment` |
| `R^q/L <= moment <= R^(q-1)` | `GrandeFinale.LargestFiberMoment.largestFiber_normalizedMoment_bounds` |
| `q log R - log L <= log(moment)` | `GrandeFinale.LargestFiberMoment.q_mul_log_largestFiberRatio_sub_log_card_le_log_normalizedMoment` |
| `sum N^2 <= kappa * bar N * M` | `GrandeFinale.LargestFiberMoment.sum_sq_le_kappa_mul_mean_mul_sum` |
| `M⁻¹ sum N^2 <= kappa * bar N` | `GrandeFinale.LargestFiberMoment.secondMoment_div_total_le_kappa_mul_mean` |

The upper `q`-moment bound reuses the already-proved
`QEntropyInverse.collision_moment_le_of_max` after the exact normalization
identity `sum (N/bar N) = L`. The lower bound is the contribution of a
selected maximizing fiber. The Q-to-SP theorem applies the pointwise maximum
bound before summing and then divides by the positive total mass.

## Statement comparison

The manuscript assumes nonnegative integer fiber sizes. Lean proves the
stronger statements for arbitrary nonnegative real fibers on a finite target
set. A maximizing fiber is represented by `smax ∈ S` together with the
domination hypothesis `N s <= N smax`.

The finite logarithmic inequality obtained by taking logs is formalized
exactly. The subsequent sequence-level `o(n)` conclusion is not duplicated as
a second asymptotic interface.

## Verification

```text
lake env lean GrandeFinale/LargestFiberMoment.lean
```

The module prints the axioms of its principal results. No proof placeholder or
added axiom occurs.
