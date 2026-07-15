# Axiom audit: balanced-core transverse-secant formalization

Audit date: 2026-07-14.

## Audited claims

The principal audited declarations are:

- `affineSecant_root_unique`;
- `slope_card_le_choose_of_affine_charge`;
- `lineConsistentOn_unique_of_transverse`;
- `exists_transverse_subset_of_mds`;
- `transverseSecant_card_le_of_mds_source`;
- `balancedCore_transverseSecant_card_le`;
- `balancedCore_transverseSecant_card_le_of_supported_witness`.

Each is followed by `#print axioms` in
`SyndromeSecant/BalancedCoreTransverseSecant.lean`.

## Result

A direct Lean check reports only:

```text
[propext, Classical.choice, Quot.sound]
```

These are standard Mathlib foundations. There is no `sorryAx`, no custom
axiom, and no `native_decide` dependency in the general theorem chain. The
legacy finite executable example still uses `native_decide` and `decide` only
for its explicitly enumerated `F_5²` regression facts.

## Claim boundary

The audit certifies the finite fixed-chart theorem under the explicit
`mdsKernelOn`, supported-witness, and transversality hypotheses. It does not
certify chart exhaustion, off-chart reduction, the asymptotic small-`κ`
condition, or a Vandermonde-to-`mdsKernelOn` instantiation.
