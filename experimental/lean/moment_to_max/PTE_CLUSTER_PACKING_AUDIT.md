# PTE cluster-packing Lean audit

Audit date: 2026-07-14.

## Formal claims

`MomentToMax/PTEClusterPacking.lean` formalizes the exact finite algebra from
`experimental/notes/thresholds/pte_cluster_packing_frontier.md`.

It proves:

- degree-two Boolean signatures over integer blocks transform explicitly under
  every affine map `x ↦ a*x+c`;
- when `a ≠ 0`, signature collision classes, semantic image cardinality, and
  semantic maximum-fibre cardinality are affine invariant;
- adding a common disjoint complement to both sides of a degree-two PTE trade
  preserves the collision;
- deleting one repairable representative from every collision pair preserves
  the image, hence the collision deficit is at least the number deleted; the
  source-shaped `2^(b-2r)` conclusion follows from the printed redundant-set
  cardinality;
- three distinct head values make the three Boolean head coordinates uniquely
  recoverable from weight, first moment, second moment, and the tail. The
  resulting unconditional Vandermonde injection bounds every split-block fibre
  by `2^n`, i.e. by `2^(b-3)` when the total block has `b=n+3` points;
- an executable sorted histogram over all `2^14` Boolean masks of the named
  block `{0,2,3,4,5,8,9,13,14,17,18,19,20,22}` returns exactly
  `(fstar,L1)=(12,12239)`;
- its cleared objective is exactly `146868/16384 > 1`, and the numerator
  factors multiplicatively under every finite tensor power.

## Axiom result

The general affine, trade, deletion, and Vandermonde theorems use only standard
Mathlib logical/kernel principles (`propext`, `Classical.choice`, and
`Quot.sound`, as applicable). There is no `sorryAx`, custom axiom, or proof
placeholder.

The exhaustive 14-point histogram theorem uses `native_decide`, so its axiom
report additionally contains `Lean.ofReduceBool` and `Lean.trustCompiler`.
The independent Python verifier recomputes the same histogram and all headline
arithmetic by a separate implementation.

## Correspondence boundary

**PROVED:** affine collision and semantic-statistic invariance over integer
blocks; the common-complement trade identity; the deletion/deficit compiler;
the unconditional three-coordinate Vandermonde cap; the exact named-block
histogram; and the finite cleared tensor arithmetic.

**CONDITIONAL:** instantiating the deletion compiler requires the explicit
complement-indexed repair set and its cardinality `2^(b-2r)`. The module proves
the common-complement collision that supplies its equality premise, but keeps
the finite packing of all pairs as a visible certificate.

**NOT CLAIMED:** optimizer symmetry, optimality of the named block outside the
reported census, the local-CLT central-coefficient estimate, convergence to the
printed decimal rate `0.156659`, monotonicity of the measured rate trend, a
sub-`log 2` asymptotic cap, or the values of `rho*` and `phi*`.

The optimized sorted-run evaluator is separately defined from the semantic
Finset statistics; its generic correctness is not promoted as a theorem here.
For the named block, its result is cross-checked independently by the source
verifier.

## Verification

- direct module compilation with principal theorem axiom reports: passes;
- package `lake build`: passes (8030 jobs);
- `python3 experimental/scripts/verify_pte_cluster_packing.py`:
  `RESULT: PASS (48/48)`.
