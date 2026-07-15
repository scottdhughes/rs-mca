# Coefficient-Prefix Pigeonhole Correspondence

Status: **PROVED** for the explicit coefficient-prefix map and the literal
finite list-size ceiling in `prop:exact-prefix-list`.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`prop:exact-prefix-list` and equation (4.1).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Locator coefficient prefix | `GrandeFinale.PrefixPigeonhole.coefficientPrefix` |
| Monic received polynomial with prescribed prefix | `GrandeFinale.PrefixPigeonhole.prefixPolynomial` |
| Prefix fiber of `m`-subsets | `GrandeFinale.PrefixPigeonhole.coefficientFiber` |
| Explicit polynomial is monic of degree `m` and has prefix `z` | `GrandeFinale.PrefixPigeonhole.prefixPolynomial_isMonicOfDegree`, `GrandeFinale.PrefixPigeonhole.coefficientPrefix_prefixPolynomial` |
| Coefficient-prefix equality is equivalent to leading cancellation | `GrandeFinale.PrefixPigeonhole.coefficientPrefix_eq_iff_degree_sub_lt` |
| Coefficient fiber equals the cancellation-defined support family | `GrandeFinale.PrefixPigeonhole.mem_coefficientFiber_iff_mem_prefixSupportFinset` |
| Finite list equals the exact polynomial list set | `GrandeFinale.PrefixPigeonhole.mem_listedPolynomials_iff`, `GrandeFinale.PrefixPigeonhole.coe_listedPolynomials_eq` |
| Literal ceiling-form heavy-fiber bound | `GrandeFinale.PrefixPigeonhole.exists_large_coefficientFiber` |
| Literal ceiling-form list-size bound | `GrandeFinale.PrefixPigeonhole.prefixPolynomial_list_floor`, `GrandeFinale.PrefixPigeonhole.exists_prefix_list_floor` |

## Statement comparison

The source writes the locator prefix from the leading term downward as
`(c_1, ..., c_w)`, where `w = m - K`. Lean stores the same coefficients from
degree `K` upward as a function `Fin (m - K) -> B`. This reverses their display
order but preserves the prefix fibers exactly.

The explicit polynomial is

`X^m + sum_i C (z i) * X^(K + i)`.

Its locator-prefix fiber is proved equal to the cancellation-defined family
used by `ExactPrefixList`. The generic finite max-fiber theorem then yields

`choose |D| m ⌈/⌉ |B|^(m-K) <= |fiber z|`,

where `⌈/⌉` is natural ceiling division. Injectivity of the locator map shows
that the same bound holds for the complete finite list. This is the literal
ceiling in the source, rather than a floor-division relaxation.

## Scope boundaries

The final theorem counts the unique degree-less-than-`K` polynomial
representatives in the exact list over the finite base field. The evaluation
domain is a `Finset B`, so `D subset B` is built into the type. The module does
not itself export the later rigidity cap or separating-pole list--line
bijection. `PrefixRigidityPacking.lean` supplies the exact Johnson packing cap;
the complete fiber is composed with the fixed-pole, scalar-extension, and
proper-challenge interfaces in the downstream prefix modules.

## Verification

```text
lake env lean GrandeFinale/PrefixPigeonhole.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
