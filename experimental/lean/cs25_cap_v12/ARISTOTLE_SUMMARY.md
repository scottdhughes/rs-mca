# Aristotle Summary: CAP25 Lean Track

This package is the Lean track for `tex/cs25_cap_v12.tex`.  The root module is
`cs25_cap_v12.lean`; all internal imports use the `cs25_cap_v12.*` namespace.

## What Is In The Proved Core

The current formalization contains a useful no-`sorry` core around the abstract
parts of Paper D:

- CA/MCA definitions, probability wrappers, and basic monotonicity.
- `ecaFloor` algebra and threshold certificate helpers.
- Bucket-counting / Cauchy-Schwarz lemmas.
- Simple-pole polynomial facts and deep-list bucket bounds.
- Subfield-confinement results for extension-valued challenges.
- Theorem A, the deep-point list-to-CA conversion.
- Safe-side CA-to-MCA transfer and deep-regime CA/MCA upper bounds.
- Johnson-style list-counting bound.
- Universal-cap reduction from a fiber-list hypothesis.
- RS submodule wrappers, RS sandwich statements, and deep-safe scanner
  soundness.
- Several quotient ledger and interleaving-transfer primitives.

## What Is Still Blueprint / Skeleton

The package deliberately keeps the construction-heavy parts as named theorem
skeletons with `sorry`.  These are the formal proof targets, not proved facts.

- `Fiber.lean`: multiplicative and map-smooth fiber lemmas, plus the `phi` cap.
- `AperiodicHankel.lean`: regular Hankel eliminant and packing certificates.
- `QuotientRemainder.lean`: quotient-remainder prefix/heaviest-prefix floors
  and first-grid cap consequences.
- `InterleavingTransfer.lean`: explicit head-floor and explicit-pairs
  witnesses.
- `QuotientLedgers.lean`: any remaining support-family ledger skeleton.
- `CircleCode.lean`: Chebyshev/circle-code analogues.
- `ECFFT.lean`: rational-map and ECFFT floor/cap statements.

## Local Check Status

Aristotle reports the no-`sorry` core as buildable in its original environment.
The Codex cleanup pass did not run `lake build`, because doing so would fetch
Mathlib.  Treat all build-clean and axiom-clean claims as pending local
verification in a Mathlib-enabled environment.
