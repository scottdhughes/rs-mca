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
- `GrandeFinale/QFourierTao.lean` formalizes the log-moment-to-Q reduction.
- `GrandeFinale/QEntropyInverse.lean` formalizes the deterministic atoms around
  the entropic inverse route.
- `GrandeFinale/QPrimitiveCollision.lean` formalizes collision-tuple and
  low-support exclusion kernels.
- `GrandeFinale/QFiniteTables.lean` pins the four finite Q table rows and
  kernel-checks their exact integer inputs, budget-ratio truncations, printed
  margin rounding, and moment-floor convention split.
- `GrandeFinale/SyndromeLine.lean` formalizes the frontiers paper's exact
  syndrome-line normal form, deduplicated transverse secant compiler, and the
  resulting numerator equality for a surjective syndrome map.
- `GrandeFinale/ProfileEnvelopeWindow.lean` formalizes the exact rational
  identity-versus-folding exponent window for each actual complete-fiber pair,
  its finite-family intersection/failure-band union, and the no-field-drop
  crossing criterion.
- `GrandeFinale/BC.lean`, `GrandeFinale/SP.lean`, and
  `GrandeFinale/Frontier.lean` formalize theorem-level reductions around the
  BC, SP, and frontier ledgers.

The theorem-by-theorem scopes of the collision-aware-pole,
challenge-intersection, syndrome-line, and profile-window modules are recorded
in `COLLISION_AWARE_POLE_CORRESPONDENCE.md`,
`CHALLENGE_INTERSECTION_CORRESPONDENCE.md`, `SYNDROME_LINE_CORRESPONDENCE.md`,
and `PROFILE_ENVELOPE_WINDOW_CORRESPONDENCE.md`.

The collision-aware-pole and challenge-intersection modules formalize
complementary steps behind equation (13.3) of the frontiers paper. The first
proves the exact full-field simple-pole floor from a supplied finite codeword
list; the second transfers a supplied full-field floor to a proper challenge
set. `collisionAwarePole_challenge_of_codewordList` records their direct
composition. The Reed--Solomon prefix-list construction and list-size floor
remain separate upstream inputs.

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
cache. Contributor audit notes report a full pinned build on 2026-07-11 with
8038 jobs, including `GrandeFinale.CollisionAwarePole`; this integration did
not rerun Lake.
