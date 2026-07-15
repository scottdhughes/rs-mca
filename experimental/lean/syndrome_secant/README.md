# Balanced-core transverse-secant formalization

This Lean/Mathlib package formalizes the finite, field-independent counting
argument from
[`experimental/notes/thresholds/ray_compiler_balanced_core.md`](../../notes/thresholds/ray_compiler_balanced_core.md).

## Status

**PROVED (fixed chart, explicit hypotheses).** For a chart `U` of cardinality
`R + κ`, the main theorem proves

```text
#slopes ≤ Nat.choose (R + κ) (κ + 1)
```

over an arbitrary field. The assumptions are printed rather than hidden:

- `mdsKernelOn U row`: every `κ`-subset of the chart uniquely determines a
  kernel coefficient vector;
- each slope has an error support `E ⊆ U` with `#E ≤ t < R`;
- the corresponding kernel-corrected moving lift vanishes on `U \ E`;
- the two fixed lifts are transverse on that zero set.

The last theorem,
`balancedCore_transverseSecant_card_le_of_supported_witness`, is the
source-shaped entry point.

## Formal proof structure

[`SyndromeSecant/BalancedCoreTransverseSecant.lean`](SyndromeSecant/BalancedCoreTransverseSecant.lean)
contains:

1. affine-root uniqueness and the injection into `(κ+1)`-subsets;
2. a kernel-row formulation of line consistency and transversality;
3. `exists_transverse_subset_of_mds`, the MDS localization bridge: a
   transverse set of at least `κ+1` coordinates contains a transverse
   `(κ+1)`-subset;
4. the fixed-chart cardinality theorem under source-shaped supported-witness
   hypotheses;
5. the earlier finite `F_5²` executable secant example, retained in
   `SyndromeSecant.lean` as a regression fixture.

The localization proof fixes a `κ`-point base. If every one-point extension
were degenerate, MDS coefficient uniqueness would force the same two kernel
representations across the entire source set, contradicting transversality.
Each resulting transverse subset admits at most one slope, so charging slopes
to subsets is injective.

## Scope boundary

The formal result covers the note's finite per-chart theorem and removes any
field-size factor from that count. It does **not** claim:

- that every RS atlas branch is confined to one fixed chart;
- a subexponential bound on the number of charts;
- an asymptotic `(RC)` discharge for unbounded `κ`;
- handling of off-chart witnesses;
- a separate Lean construction proving that a concrete Vandermonde matrix
  satisfies `mdsKernelOn` (the exact MDS kernel consequence is an explicit
  theorem hypothesis).

Consequently, the asymptotic `(RC)` conclusion remains conditional on chart
confinement/exhaustion and on a regime such as `κ = o(n / log n)`.

## Verification

From this directory:

```bash
lake build
lake env lean SyndromeSecant/BalancedCoreTransverseSecant.lean
```

From the repository root, the independent source verifier is:

```bash
python3 experimental/scripts/verify_ray_compiler_core.py
```

Recorded on 2026-07-14:

- full Mathlib package build: pass;
- source verifier: `RESULT: PASS (173 checks)`;
- all printed main theorems depend only on `propext`, `Classical.choice`, and
  `Quot.sound`.
