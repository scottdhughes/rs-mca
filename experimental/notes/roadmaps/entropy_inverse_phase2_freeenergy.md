# Entropy-inverse crux, Phase 2: the free-energy branch is right, valid deployed — and is the max-fiber wall (2026-07-10)

Status: `MEASURED` (dense-regime free-energy decay confirmed) / `SCOPING` (the honest reduction). Verifier:
`experimental/scripts/entropy_inverse_phase2_freeenergy.py`. Follows Phase 1 (dichotomy → free-energy branch).

## What Phase 2 tested

Phase 1 put the load on the free-energy branch: for spread trades, the level's contribution to `Γ_ℓ` should
decay (`≤ exp(-Ω(Nℓ))`). Phase 2 tests whether it does, via the fiber-moment excess
`ratio_ℓ = Γ_ℓ / main_ℓ = E_s[(1+δ(s))^ℓ]` (`R(s) = mean·(1+δ(s))`, `main_ℓ = C^ℓ/Q^{w(ℓ-1)}`). Free-energy per
level `= (1/ℓ)log₂ ratio_ℓ`.

## Findings

**(1) The free-energy decay HOLDS in the dense (deployed) regime; DENSITY is the controlling parameter.**

| n | mean-fiber | `r₂` | `r₄` | free-energy/level |
|---|---|---|---|---|
| 16 | 44.5 | 1.0015 | 1.0095 | 0.0034 |
| 18 | 134.7 | 1.0008 | 1.0045 | 0.0016 |
| 20 | 109.9 | 1.0041 | 1.0250 | 0.0089 |
| 14 | 4.1 (sparse) | 1.22 | 2.68 | 0.36 |

Dense (mean-fiber `≫ 1`, `= exp(o(N))` per level `→ 0`) — decay holds. Sparse (mean-fiber `~1`, not deployed)
— excess blows up in `ℓ`. The deployed regime has mean-fiber `~2^192`, deep in the decay zone.

**(2) In the dense regime the excess factorizes through the second moment:** `ratio_ℓ ≈ ratio_2^{ℓ-1}`
(`r₄/r₂³ = 1.005–1.04`, `r₆/r₂⁵ ≈ 1.01`). Writing `ratio_ℓ = E[(1+δ)^ℓ]`, for small `δ` (dense) this is
variance-controlled: the whole ladder is set by `Var(δ) = ` the second moment `= B1`.

## The honest reduction (and the wall)

Factoring `ratio_ℓ = E_s[(1+δ)^ℓ]`: for BOUNDED `ℓ` and small `δ`, it is variance- (second-moment-) controlled,
which is the clean toy behaviour above. **But for the deployed `ℓ = (log N)^A`, `E[(1+δ)^ℓ]` is dominated by
`max(1+δ) = max-fiber / mean`** — so at the relevant levels the free-energy decay is EQUIVALENT to the
**max-fiber theorem** (C9 / `prob:row-sharp-q`). The toy factorization `ratio_ℓ = ratio_2^{ℓ-1}` is the
small-`ℓ`/small-`n` regime before the tail dominates; it does not survive to `ℓ = polylog N`.

**So the free-energy branch is the RIGHT branch (Phase 1) and NUMERICALLY VALID in the deployed regime
(Phase 2, density-controlled), but it is NOT an escape from the `√p`/max-fiber wall — at deployed `ℓ` its proof
IS the max-fiber theorem C9.** Every angle — direct moments (T5→NG route-cut, #448), the dichotomy (Phase 1),
free-energy (here) — bottoms out on the same single obstruction.

## Net of Phases 0–2 (the crux, fully mapped)

1. **Phase 0:** crux reduced to step 5 alone; the endpoint (b)-kill machine-checked (`VandermondeRank`, #501);
   slice-derivative lemma stated as a conditional.
2. **Phase 1:** the dichotomy's operative branch is free-energy (our lane), not small-doubling/PFR.
3. **Phase 2:** free-energy decay is numerically valid in the dense/deployed regime, controlled by density, with
   the excess factoring through the second moment for bounded `ℓ` — and equal to the max-fiber theorem (C9) at
   deployed `ℓ`.

**The single remaining obstruction is the max-fiber theorem C9 (the `√p`/BGK barrier), now confirmed as the
sole wall from three independent angles.** This is a genuine open problem in additive combinatorics /
character sums; it is not an engineering gap and no route in the project (or the surrounding literature) breaks
it. Our maximal contribution short of breaking it — reduce, machine-check everything around it, identify and
numerically validate the operative branch, localize the controlling parameter — is complete.
