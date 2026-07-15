# Primitive full-image and identity-window audit

Audit date: 2026-07-14.

## Formal claims

`AsymptoticSpine/FullImageIdentityWindow.lean` formalizes the finite arithmetic
interfaces extracted from:

- `experimental/notes/thresholds/fi_full_image_primitive.md`;
- `experimental/notes/thresholds/envelope_identity_window.md`.

For the full-image route it defines the scale tower
`realizedSize ≤ effectiveSize ≤ ambientSize` and proves:

- Gap 1 and Gap 2 compose multiplicatively into an ambient full-image
  certificate;
- an ambient certificate implies the weaker effective-scale certificate;
- a nonempty realized image is automatically full-image when the complete
  ambient size fits inside the printed finite loss;
- ambient max-fiber flatness certifies full image by pigeonhole;
- effective-scale max-fiber payment certifies Gap 1 by the same cancellation.

For the identity-envelope route it denominator-clears
`lambda = lambdaNum/lambdaDen` and proves:

- the lower and upper identity windows are exactly the complement of the
  strict failure band;
- every parameter point is in the window union or the failure band;
- when there is no field drop (`lambda=1`), the window union is global;
- for fold degree at least two, positive entropy, and strict field drop, the
  zero-target crossing `s=h` lies in the failure band and therefore is not
  identity-dominant;
- a target crossing satisfying the lower edge is in the dominance window.

## Axiom result

Direct Lean compilation reports only standard logical/kernel principles:
`propext`, `Classical.choice`, and `Quot.sound`, depending on the theorem.
Several structural implications use no axioms. There is no `sorryAx`, custom
axiom, or opaque proof placeholder.

## Correspondence boundary

**PROVED:** the finite two-gap composition, the shallow ambient-size compiler,
the two max-fiber pigeonhole compilers, the exact cleared window/failure-band
partition, no-field-drop coverage, and the strict field-drop crossing wall.

**CONDITIONAL:** interpreting a family of finite losses as `exp(o(n))`;
locating an analytic target crossing and verifying its lower-edge premise;
reducing the complete profile envelope to a single printed quotient
competitor. For multiple competitors the formal predicate must be intersected
over the rows (or a separately proved sound reduction must be supplied).

**NOT CLAIMED:** deep-prefix effective-span-collapse routing, exhaustion and
payment of an earlier structural profile, unconditional ambient full image on
deep leaves, or the analytic upper-envelope direction. The independent audit's
multi-folding soundness attack confirms that a naive cheapest-row reduction is
unsound; this module does not make that reduction.

## Verification

- direct module compilation with theorem axiom reports: passes;
- package `lake build`: passes (24 jobs);
- `verify_fi_certificate.py`: `RESULT: PASS (31 checks)`;
- `verify_envelope_window.py`: `RESULT: PASS (13295 checks)`;
- `verify_identity_window_audit.py`: `RESULT: PASS (7160 checks)`, including
  4608 exact-rational single-competitor points and the multi-folding soundness
  attack.
