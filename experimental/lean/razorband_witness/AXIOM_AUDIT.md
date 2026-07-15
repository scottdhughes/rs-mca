# Axiom and correspondence audit: C9 near-Sidon razor

Audit date: 2026-07-14.

## Axiom result

The main module prints axiom reports for the local classification, product
fiber, energy, normalized-excess, and repaired-razor theorems.

- The two finite exhaustive declarations use the expected executable decision
  axioms `Lean.ofReduceBool` and `Lean.trustCompiler`, together with standard
  foundations.
- The general moment-fiber, product-cardinality, exact-energy, limit,
  fixed-power, normalized-excess, small-image, and energy-implication theorems
  use only `propext`, `Classical.choice`, and `Quot.sound`.
- There is no `sorryAx`, custom axiom, or proof placeholder.

## Statement correspondence

**PROVED:** the local collision and signature census; the Boolean product
subfiber's two common moments; `f=2^k`, `E=6^k`, and
`Δ=(3/4)^k`; its absolute energy decay; the fixed-half-power countergate; the
three-block arithmetic; and the two repaired finite inequalities.

**CONDITIONAL COMPILER:** the normalized-excess theorem accepts the source's
finite image lower bound and ambient-mass upper bound explicitly. It does not
silently re-prove the separated-base/no-wrap identification of the entire
full-slice image.

**OPEN / NOT CLAIMED:** smooth/circle-domain admissibility, primitive
first-match survival, deep analytic payment, any span-side image conclusion,
ray compilation, and threshold/reserve comparison.

## Replay evidence

- default `lake build`: pass;
- direct module compile and axiom prints: pass;
- artifact verifier `--check`: pass;
- tamper self-test: 11/11 semantic mutations rejected.
