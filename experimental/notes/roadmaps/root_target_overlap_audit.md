# Overlap-audit of the prize-DAG root TARGETs (2026-07-06)

- **Status:** AUDIT. Cross-references the 7 unproved DAG root TARGETs + the repo's computed
  `strategic_recommendations.md` (167 nodes, 67 open) against current PR/commit activity.
- **Purpose:** find a non-overlapping, analytic-NT-fit, prize-critical target for a fresh push.

## Result: the critical map is densely staffed -- no unworked prize-critical target

| Target / node | DAG class | Actively worked by | Effort-to-attack |
|---|---|---|---|
| **Conjecture F** (`conj_f`) | CRITICAL, unavoidable (both grand challenges) | LegaSage (#345 d=3 incidence census) | multi-week, hard, competitive |
| **petal_growth** (+ only alt `petal_mixed_amplification`) | CRITICAL, single point of failure (list side) | flagged R4; active | multi-week, hard |
| Q-side / max-fiber (parent of our `E_3`) | CRITICAL | holmbuar (#361), DannyExperiments (#351/#352) | multi-week, crowded |
| `xr_smallcore_spread_count` | ROUTE-INTERNAL (XR lane only) | LegaSage-adjacent | medium, contingent on choosing XR |
| `rate_half_band_closure`, `worst_word_challenger_pricing`, `u2c_giant_tnull_dichotomy`, `dli_prime_weighted_large_block_support`, `u1_x4_direct_column_budget` | leaf / route-internal / support-only | mixed | varies; mostly not standalone-critical |

## The one cheap, high-leverage, likely-unworked gap: R6 rules/ePrint lookups

`strategic_recommendations.md` R6: `field_cap_check`, `rules_freeze` are CRITICAL (S0), and
`f1_case_tower` is critical ONLY IF the official family admits non-generating rows -- decided by an
ePrint/rules **reading** (Q0.1/Q0.2). "A one-hour reading task can delete a critical node." No notes
found on these -> possibly unworked. **Highest EV/effort ratio in the audit** -- but it is careful
reading, not an analytic-NT proof.

## Recommendation

The "pivot to a non-overlapping root TARGET" premise does not hold: the effort is dense and every
prize-critical node has contributors. Realistic high-value moves, ranked:
1. **The cyclotomic-directions bridge writeup** (`../l1/l1_cyclotomic_directions_bridge.md`) -- the
   one genuinely-novel, durable output of this session; independent-novelty value.
2. **The R6 rules/ePrint lookups** (Q0.1/Q0.2) -- ~1 hour, non-overlapping, can delete a critical
   node; low glamour, high EV. Doable by careful reading.
3. **Compete on Conjecture F** -- most-leveraged, analytic-NT-shaped, but hard and already staffed
   (LegaSage). A real multi-week fight with uncertain differentiation.
4. **Bank the session** -- PR #360 is a solid, self-contained contribution; regroup deliberately.

Given density + the confirmed-hard cruxes, (1) is the durable play and (4) is the honest default;
(2) is the cheap opportunistic win; (3) only if the analytic-NT fight is specifically wanted.

## Correction (2026-07-06, after running the R6 lookups)

Two claims above were made on incomplete information and are now corrected (see
`../audits/rules_freeze_completion_R6.md`):
1. **"No notes found on these -> possibly unworked" is FALSE.** The R6 nodes are already substantially
   worked upstream: `../audits/rules_freeze.md`, `field_cap_check.md`, `prize_rules_pinning.md`,
   `m_handling.md`, `rules_m_reading.md` all exist and pin the field/rate/m box (PROVED/citation), and
   the `certifier_uniformity` DAG node already adopted "Reading B" (compiler semantics accepted) on
   2026-07-03. R6's net-new gap is narrower than stated: a **2026-07-06 drift recheck** + a
   **primary-source-grounded compiler-semantics freeze row**, not a from-scratch lookup.
2. **"can delete a critical node" is FALSE for the tower case.** Q0.1 resolves the *critical* way:
   `field_cap_check` confirms the family INCLUDES non-generating rows (extension fields `< 2^256`,
   `n` up to `2^41`), so `f1_case_tower` is **genuinely critical, no longer family-conditional** --
   confirmed, not deleted. The "one-hour reading deletes a critical node" hope does not hold here.
   (Root cause of the error: conflating `generating_escape` = "non-generating rows forced *tiny*" with
   "no non-generating rows"; they are not the same.)
