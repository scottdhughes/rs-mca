# Grande Finale Lean Formalization

This Lean package contains partial formalization tracks for
`experimental/grande_finale.tex`.

The package root is `GrandeFinale`, with additional modules under
`GrandeFinale/`:

- `GrandeFinale.lean` formalizes the core staircase, first-match, moment, and
  finite certificate kernels.
- `GrandeFinale/ChallengeIntersection.lean` formalizes exact finite
  translate--challenge intersection averaging, received-line shear invariance,
  the challenge-restricted MCA numerator, and the outer ceiling compiler used
  in the proper-challenge lower bound.
- `GrandeFinale/CollisionAwarePole.lean` formalizes the exact full-field
  collision-aware simple-pole floor from a supplied finite Reed--Solomon
  codeword list, including polynomial representatives, the natural-number
  ceiling in equation (4.2), and its direct proper-challenge composition.
- `GrandeFinale/IdentityPrefixCollisionFloor.lean` composes the exact
  coefficient-prefix list floor with the collision-aware pole theorem,
  proving equation (4.3) and its proper-challenge ceiling transfer.
- `GrandeFinale/QFourierTao.lean` formalizes the log-moment-to-Q reduction.
- `GrandeFinale/QEntropyInverse.lean` formalizes the deterministic atoms around
  the entropic inverse route.
- `GrandeFinale/LargestFiberMoment.lean` proves the exact normalized
  largest-fiber `q`-moment bounds, their finite logarithmic consequence, and
  the Q-to-SP normalized second-moment transfer.
- `GrandeFinale/ExactProfileCompiler.lean` proves the exact finite incidence,
  residual-moment, natural-floor, and first-match budget implications behind
  (FC1)--(FC2).
- `GrandeFinale/FirstMatchAddBack.lean` proves ordered first-match
  disjointization, exact finite profile-union summation, and the weighted
  profile add-back formulas (AB1)--(AB3).
- `GrandeFinale/SubfieldConfinement.lean` proves that a nonbase slope
  explaining a base-valued Reed--Solomon line point forces pair explanation
  on the same support, and hence all MCA-bad slopes lie in the base field.
- `GrandeFinale/ExactPrefixList.lean` proves the exact correspondence between
  locator-prefix supports and degree-bounded listed polynomials, including
  recovery of the unique full agreement support and the no-extra-agreement
  clause.
- `GrandeFinale/PrefixPigeonhole.lean` defines the explicit locator coefficient
  prefix, identifies it with the cancellation predicate, and proves the
  literal ceiling-form prefix-fiber and polynomial-list lower bounds.
- `GrandeFinale/PrefixRigidityPacking.lean` constructs exact Johnson spheres
  and balls, proves the prefix-fiber distance bound, and derives the literal
  finite packing cap in equation (4.4).
- `GrandeFinale/ExactListLine.lean` proves the same-field, fixed-pole exact
  bijection between a complete finite polynomial list and the MCA-bad slopes
  of its simple-pole received line, including agreement-set preservation.
- `GrandeFinale/ExactPrefixRay.lean` specializes that bijection to the complete
  locator-prefix fiber, proving direct support-to-slope image equality, exact
  cardinality at a separating pole, and preservation of every full agreement
  support.
- `GrandeFinale/ExactPrefixRayUniqueness.lean` reconstructs the listed
  polynomial from any degree-bounded explanation of a selected prefix slope
  and proves uniqueness of its exact support/explaining-polynomial witness.
- `GrandeFinale/SeparatingPole.lean` proves the exact unordered-pair
  equation-(4.6) field-size bound for an off-domain separating pole and
  composes it with the complete same-field prefix fiber.
- `GrandeFinale/ScalarExtensionListLine.lean` proves interpolation descent for
  ambient explanations of a base-valued word, completeness of the mapped
  base list, and the full extension-field exact list--line theorem.
- `GrandeFinale/PrefixChallengeFloor.lean` composes the extension-field exact
  prefix realization with proper-challenge translate averaging, proving the
  prescribed-fiber floor and the literal nested-ceiling largest-fiber bound.
- `GrandeFinale/QPrimitiveCollision.lean` formalizes collision-tuple and
  low-support exclusion kernels.
- `GrandeFinale/QFiniteTables.lean` pins the four finite Q table rows and
  kernel-checks their exact integer inputs, budget-ratio truncations, printed
  margin rounding, and moment-floor convention split.
- `GrandeFinale/SyndromeLine.lean` formalizes the frontiers paper's exact
  syndrome-line normal form, deduplicated transverse secant compiler, and the
  resulting numerator equality for a surjective syndrome map.
- `GrandeFinale/RSParityKernel.lean` constructs the barycentric weighted
  Vandermonde parity map, proves its at-most-`R` column independence and
  surjectivity, and identifies its kernel exactly with the injective
  Reed--Solomon evaluation code.
- `GrandeFinale/RSSupportHyperplanes.lean` identifies supported-error syndrome
  images with weighted-column spans and proves that exact `(R-1)` supports
  give an injective family of nonzero functional kernels.
- `GrandeFinale/RSExactSupportUpper.lean` proves the exact-agreement reduction
  for injective Reed--Solomon codes and the full-field support-atlas bound
  `B_MCA <= choose |D| a` for `a >= k+1`.
- `GrandeFinale/RSFirstAdjacentRow.lean` composes the parity kernel,
  exact-support hyperplanes, separating-line compiler, and support upper bound
  to prove the full-field AD1 numerator equality.
- `GrandeFinale/RSFirstAdjacentThreshold.lean` defines the exact first-safe
  proposition and derives both literal AD2 target-budget implications.
- `GrandeFinale/ExactAdjacentRow.lean` proves the literal
  `max M (choose M 2) < |F|` hyperplane-avoidance construction and compiles its
  `M` distinct transverse intersections into the exact support-wise MCA
  numerator lower bound.
- `GrandeFinale/ProfileEnvelopeWindow.lean` formalizes the exact rational
  identity-versus-folding exponent window for each actual complete-fiber pair,
  its finite-family intersection/failure-band union, and the no-field-drop
  crossing criterion.
- `GrandeFinale/BC.lean`, `GrandeFinale/SP.lean`, and
  `GrandeFinale/Frontier.lean` formalize theorem-level reductions around the
  BC, SP, and frontier ledgers.

The theorem-by-theorem scopes of the collision-aware-pole,
identity-prefix-collision-floor, challenge-intersection, syndrome-line,
RS parity-kernel, support-hyperplane, exact-support-upper, first-adjacent-row,
first-adjacent-threshold, largest-fiber-moment, exact-profile, first-match
add-back, subfield-confinement, exact-prefix-list, prefix-pigeonhole,
prefix-rigidity-packing, exact-list-line, exact-prefix-ray,
prefix-ray-uniqueness, separating-pole, scalar-extension-list-line,
proper-challenge-prefix-floor, and profile-window modules are recorded
in `COLLISION_AWARE_POLE_CORRESPONDENCE.md`,
`IDENTITY_PREFIX_COLLISION_FLOOR_CORRESPONDENCE.md`,
`CHALLENGE_INTERSECTION_CORRESPONDENCE.md`, `SYNDROME_LINE_CORRESPONDENCE.md`,
`RS_PARITY_KERNEL_CORRESPONDENCE.md`,
`RS_SUPPORT_HYPERPLANES_CORRESPONDENCE.md`,
`RS_EXACT_SUPPORT_UPPER_CORRESPONDENCE.md`,
`RS_FIRST_ADJACENT_ROW_CORRESPONDENCE.md`,
`RS_FIRST_ADJACENT_THRESHOLD_CORRESPONDENCE.md`,
`EXACT_ADJACENT_ROW_CORRESPONDENCE.md`,
`LARGEST_FIBER_MOMENT_CORRESPONDENCE.md`,
`EXACT_PROFILE_COMPILER_CORRESPONDENCE.md`,
`FIRST_MATCH_ADDBACK_CORRESPONDENCE.md`,
`SUBFIELD_CONFINEMENT_CORRESPONDENCE.md`,
`EXACT_PREFIX_LIST_CORRESPONDENCE.md`,
`PREFIX_PIGEONHOLE_CORRESPONDENCE.md`,
`PREFIX_RIGIDITY_PACKING_CORRESPONDENCE.md`,
`EXACT_LIST_LINE_CORRESPONDENCE.md`,
`EXACT_PREFIX_RAY_CORRESPONDENCE.md`,
`EXACT_PREFIX_RAY_UNIQUENESS_CORRESPONDENCE.md`,
`SEPARATING_POLE_CORRESPONDENCE.md`,
`SCALAR_EXTENSION_LIST_LINE_CORRESPONDENCE.md`,
`PREFIX_CHALLENGE_FLOOR_CORRESPONDENCE.md`, and
`PROFILE_ENVELOPE_WINDOW_CORRESPONDENCE.md`.

The collision-aware-pole and challenge-intersection modules formalize
complementary steps behind equation (13.3) of the frontiers paper. The first
proves the exact full-field simple-pole floor from a supplied finite codeword
list; the second transfers a supplied full-field floor to a proper challenge
set. `collisionAwarePole_challenge_of_codewordList` records their direct
composition. `IdentityPrefixCollisionFloor` supplies the source-exact
identity-prefix specialization with list size exactly `L_m`. The
Reed--Solomon prefix-list construction and list-size floor
are split between `ExactPrefixList` and `PrefixPigeonhole`: the first proves
the exact support/list correspondence, and the second proves the explicit
coefficient-prefix pigeonhole ceiling. `ExactListLine` now supplies the exact
same-field conversion from any complete finite polynomial list to the bad
slopes of a fixed separating pole, and `ExactPrefixRay` exports its direct
prefix-fiber specialization and exact support preservation.
`PrefixRigidityPacking` separately supplies the exact Johnson-distance and
packing limitation for every coefficient fiber.
`ExactPrefixRayUniqueness` additionally proves occupancy one for every
selected prefix support at a separating pole, and `SeparatingPole` supplies
that pole under the exact same-field equation-(4.6) budget.
`ScalarExtensionListLine` supplies coefficient descent, ambient-list
completeness, and the full finite extension-field list--line interface.
`PrefixChallengeFloor` composes that exact extension-field realization with
the proper-challenge compiler and preserves the literal inner and outer
natural ceilings.

The profile-window module proves exponent-level dominance only after `h`, `s`,
and every actual `(c,lambda)` pair are supplied. QR6/QR8 normalization,
folding-family exhaustiveness, (A2)/(A4)/(A7), and the bridge to the full
profile envelope remain explicit outside inputs.

The central open mathematical target remains Q: the primitive entropic inverse
theorem / row-sharp prefix-fiber bound needed by `grande_finale.tex`.  The
finite-table module certifies the transcription and elementary integer
arithmetic of the printed target; its decimal margins and moment-order floors
are pinned audited data, not Lean derivations of `Real.log` or the huge
binomial coefficients.  These Lean files do not prove the full adjacent safe
rows or the full asymptotic closure by themselves.

Do not run `lake build` casually in this repository. Build this package only
with the pinned Lean/Mathlib versions and the matching precompiled Mathlib
cache. A full pinned default build on 2026-07-14 completed successfully with
8050 jobs, including `GrandeFinale.CollisionAwarePole` and the newly integrated
statement-target modules. The compatibility repairs needed for that build
change syntax and required typeclass/scope declarations only; they do not prove
the targets that remain explicitly marked unproved.
