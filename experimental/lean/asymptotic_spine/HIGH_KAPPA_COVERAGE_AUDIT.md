# High-kappa shallow-prefix coverage audit

Audit date: 2026-07-14.

## Formal claim

`AsymptoticSpine/HighKappaCoverage.lean` formalizes the exact finite routing
statement from `experimental/notes/thresholds/a4_covers_high_kappa.md`.
One ambient `ShallowPrefixClosureBounds` certificate supplies:

- the full-slice mass-to-average inequality;
- image size at most effective size;
- the shallow-prefix power bound `effectiveSize ≤ baseSize ^ prefixDepth`.

Together with the integrated prefix-fiber bridge, residual chart inclusion, and
`SE2Certificate`, the theorem
`balancedCoreShallowClosure_to_directRC` proves the direct `(RC)` bound. Its
all-kernel-dimensions corollary and `(A6)` compiler use the same certificate for
every residual kernel-dimension label.

## Axiom result

Direct Lean compilation prints:

- `kernelIndependentDirectRC_iff`: no axioms;
- the general shallow-closure and `(A6)` theorems: only `propext` and
  `Quot.sound`;
- the finite executable smoke test: `propext`, `Classical.choice`, and
  `Quot.sound`.

There is no `sorryAx`, custom axiom, or opaque proof placeholder.

## Correspondence boundary

**PROVED:** the finite closure route and residual transfer are independent of
the printed kernel-dimension label once the ambient shallow-prefix certificate
and the source's semantic fiber/`(SE2)` inputs are supplied.

**NOT CLAIMED:** the asymptotic inference
`prefixDepth * log(baseSize) = o(n)`, a deep-prefix `(MI)`/`(MA)` payment,
the measured energy trend, or an unconditional payment for every primitive
profile. Those remain exactly the source note's asymptotic/analytic boundary.

## Verification

- `lake build`: package default target passes;
- direct module compilation: passes with the axiom reports above;
- `python3 experimental/scripts/verify_a4_coverage.py`:
  `RESULT: PASS (63 checks)`.
