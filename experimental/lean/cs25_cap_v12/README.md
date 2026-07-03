# Paper D / CAP25 Lean Skeleton

This package is the Lean formalization track for `tex/cs25_cap_v12.tex`
(Paper D / CAP25).  It is intentionally mixed-status: several core abstract
lemmas are fully proved, while the geometry and fiber-construction sections are
kept as explicit theorem skeletons with `sorry`.

The root module is `cs25_cap_v12.lean`; the implementation is split across:

- `cs25_cap_v12/Main.lean`
- `cs25_cap_v12/TheoremA.lean`
- `cs25_cap_v12/SafeSide.lean`
- `cs25_cap_v12/DeepMCA.lean`
- `cs25_cap_v12/Johnson.lean`
- `cs25_cap_v12/MainCap.lean`
- `cs25_cap_v12/RSSandwich.lean`
- `cs25_cap_v12/Scanner.lean`
- `cs25_cap_v12/BlueprintCommon.lean`
- `cs25_cap_v12/Fiber.lean`
- `cs25_cap_v12/QuotientRemainder.lean`
- `cs25_cap_v12/InterleavingTransfer.lean`
- `cs25_cap_v12/QuotientLedgers.lean`
- `cs25_cap_v12/AperiodicHankel.lean`
- `cs25_cap_v12/CircleCode.lean`
- `cs25_cap_v12/ECFFT.lean`

The package was edited by [Aristotle](https://aristotle.harmonic.fun).

## Proved Core

The no-`sorry` core includes:

- CA/MCA definitions, probability wrappers, `eca <= emca`, and support-wise MCA
  monotonicity.
- The `ecaFloor` algebra and threshold conversion helpers.
- Bucket-counting / Cauchy-Schwarz counting lemmas.
- Simple-pole polynomial facts and deep-list bucket bounds.
- Subfield-confinement statements for base-valued rows over extensions.
- Theorem A: deep-point list-to-CA conversion.
- Abstract safe-side results: CA-to-MCA transfer below half distance and
  deep-regime MCA/CA upper bounds.
- Johnson-style abstract list bound.
- Universal-cap reduction from an explicit fiber-list input.
- Reed-Solomon code/submodule wrappers and RS sandwich statements.
- Scanner soundness for deep-safe verdicts.
- Some quotient support/image ledger lemmas and interleaving-transfer lemmas.

## Skeletons / To Do

The following files intentionally contain theorem statements with `sorry`.  They
are the main completion queue.

- `Fiber.lean`: prove `lem_fiber_ii`, `lem_phi_fiber_ii`, and `thm_phi_cap`.
  This is the most important missing construction, because `MainCap.lean`
  consumes the fiber-list input as a hypothesis.
- `AperiodicHankel.lean`: prove the regular Hankel eliminant certificate and
  closed-ball regular packing theorem.
- `QuotientRemainder.lean`: prove the quotient-remainder prefix floor,
  heaviest-prefix locator floor, quantitative first-grid floor, and first-grid
  cap corollary.
- `InterleavingTransfer.lean`: prove the explicit head-floor even/odd
  witnesses and explicit-pairs theorem.  The abstract row-transfer lemmas are
  already present.
- `QuotientLedgers.lean`: complete the remaining support-family ledger skeleton
  if any `sorry` remains after import normalization.
- `CircleCode.lean`: prove Chebyshev semiconjugacy, fiber, circle-RS, grand cap,
  and stereographic statements.
- `ECFFT.lean`: prove rational-map floor, one-step ECFFT cap, graded rational
  floor, and macroscopic ECFFT cap.

At the time of this cleanup, the source scan reports `sorry`s in exactly the
blueprint/skeleton files above.  Treat these statements as formal targets, not
as proved lemmas.

## Local Check Status

I did not run `lake build` in this repository during the Codex cleanup pass, to
avoid fetching Mathlib.  Before relying on the no-`sorry` core, run the package
in an environment with Mathlib available and inspect the exact `#print axioms`
output for the headline declarations.
