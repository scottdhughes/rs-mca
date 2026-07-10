# Entropy-inverse crux, Phase 1: the dichotomy falls on the free-energy branch (2026-07-10)

Status: `MEASURED` (reconnaissance; small-toy, indicative not conclusive). Verifier:
`experimental/scripts/entropy_inverse_phase1_dichotomy.py`. Follows Phase 0
(`entropy_inverse_phase0_reduction.md`): with the crux reduced to step 5 (the exp-scale structuralization), the
one strategic question is which branch of the L869 dichotomy the deployed load falls on.

## The question

`grande_finale.tex` L869 states `prob:entropy-inverse-q` as a per-level dichotomy on the heavy-fiber trades
`Y = 1_S - 1_{S'}` (colliding `m`-subsets, same first-`w` power-sum prefix):

- **small-doubling** trades (`H(Y-Y') ≤ H(Y)+o(N)`) → Green–Ruzsa/PFR structuralization (step 5, **not our lane**);
- **or free-energy decay** of `Y-Y'` bounds that level's contribution to `Γ_ℓ` by `exp(-Ω(Nℓ))`
  (the Sidon/free-energy branch — character-sum/analytic, **our lane**).

Which branch is operative decides whether our tools reach the deployed rows.

## Measurement

For toy dense rows, form all heavy-fiber trades, **remove the quotient/`μ_d`-coset-structured (major-arc)
trades** (the #465 families) to isolate the PRIMITIVE residual, and measure the additive doubling constant
`K = |Y+Y|/|Y|` and `F_p`-rank. Small-doubling (PFR) requires `K = O(1)`.

| row | primitive `|Y|` | `K` | random `K` | rank / (n-w) | verdict |
|---|---|---|---|---|---|
| p=97, n=16, m=8, w=2 | 256 | 103.5 | 128.5 | 13/14 | spread |
| p=113, n=16, m=8, w=2 | 176 | 75.9 | 88.5 | 13/14 | spread |
| p=241, n=16, m=8, w=2 | 32 | 15.0 | 16.5 | 10/14 | spread |

**The primitive trades are SPREAD:** `K = Θ(|Y|)` (always `~0.8×` the random baseline, always `≫ O(1)`), with
near-full rank. Small-doubling would need `K = O(1)`; we are two orders off. So the **small-doubling/PFR escape
is not triggered** — the load falls on the **free-energy branch (our lane).**

This confirms the reframe: the "randomness" of the primitive residual — which defeated our moment/T5→NG route
and which defeats PFR (PFR needs structure) — is exactly what the free-energy branch consumes (spread ⟹ decay).
The branch we cannot do is vacuous; the branch we can is the operative one.

## Caveats (honest)

- Small toys (`n=16`, `|Y| = 32–256`); indicative of the branch, not deployed-scale.
- The coset filter removes only full `μ_d`-coset unions; a mild residual additive energy (`~1.2–1.7×` random)
  survives — real residual structure, but far below the small-doubling regime (`E/|Y|² ≈ 3` vs `|Y| = 256`).
- Only `w=2` yields a populated primitive residual at this size; `w ≥ 3` empties it (collisions rare and mostly
  structured) — suggestive that the primitive residual thins with the constraint, but toy-limited.
- Phase 1 tells us WHICH disjunct to establish (free-energy decay); it does not prove the free-energy bound.

## Phase 2 (next)

Attack the **free-energy decay bound**: for spread primitive trades, bound the level's contribution to `Γ_ℓ` by
`exp(-Ω(Nℓ))` via a free-energy / Sidon estimate. This is analytic/character-sum — the same signed-`e_m` /
`Γ_ℓ` ladder we mapped in B1 (#448), but now on the decay side rather than the (failed) direct moment side.
Our `Γ_ℓ` machinery, the prefix-flatness bound (#498), and the moment law T5 are the inputs. In parallel: the
slice-derivative lemma (step 6, algebraic) stays a valid conditional target.
