# L1 `E_3 <= ell-2`: roadmap, tools, and the confirmed-open status

- **Status:** ROADMAP / AUDIT. 2026-07-06. Consolidates the CAP25 v13 (§16/17/23) reading, the
  prize-DAG structure, and the outcomes of two Aristotle runs.

## Where the crux sits (confirmed genuinely open)

`E_3 <= ell-2` (= `dim Syz <= K` for `K>=3`, our proved reduction) is the **finite max-fiber /
identity-scale collision problem** of CAP25 v13 §16 (Remark 16.10, Prop 16.17). It is open there,
open in the prize-DAG (identity-scale-collision / ImgFib sub-DAG feeding Conjecture-F -> Grand List),
and both Aristotle runs (`70427d46...`, `935d6f84...`) failed to prove it (honest `sorry`, no
fabrication). The paper's own verdict: **character maxima face a `sqrt(p)` barrier**; the second
moment cannot close it (independently reproduced here as the pair-cap giving only `(ell-1)(ell-2)/6`).

## What the paper says the proof needs (lines 7543, 8144)

1. **An inverse theorem:** "if the primitive dense-bulk max fiber is `> n^C (n choose m)|B|^{-w}`,
   the responsible support family has a quotient stabilizer, a common block structure, or a
   low-dimensional exceptional incidence." (Structure-vs-randomness / additive combinatorics.)
2. **The high-moment hierarchy `Gamma_r`** up to `r* ~ w*beta/log n ~ 10^5` at deployed depth --
   "a second-moment bound alone cannot close the finite problem; the hierarchy is where joint
   cancellation beyond the sharp per-frequency Weil cost must appear."
3. **Kernel-section / pencil rigidity** -- CAP25 §23 (Thm 23.3: a kernel section that passes the
   split test at superlinearly many slopes collapses to a constant divisor / tangent pair). This is
   the M1 (slope) side; our `Syz` is a kernel section and `X^ell - t*Gamma` is the pencil.

## Monodromy probe -- inconclusive, with a caveat (`../scripts/pencil_monodromy.sage`)

`psi: X -> X^ell/Gamma(X)` has fibers `psi^{-1}(t_0)` = roots of `X^ell - t_0 Gamma`. First-pass
Frobenius cycle-type sampling at `t_0 in F_p^*` is FLAWED for the Galois group (rational `t_0` all
lie in `psi`'s image, hence reducible -- cannot read `Gal(./F_p(t))`). **Deeper caveat:** `E_3` is
an ARITHMETIC (Frobenius-collision) invariant, while pencil monodromy is largely GEOMETRIC
(ramification); the geometric monodromy may not see the mod-`p` collisions. The correct version is
arithmetic: Chebotarev sampling at `F_{p^d}` places (`d>1`, generic), or `Oscar` function-field
`galois_group`, and correlating the ARITHMETIC monodromy (not branch points) with `E_3`.

## Next steps (ranked) and tools

1. **Arithmetic monodromy done right** (Oscar `galois_group` over `F_p(t)`, or `F_{p^d}`-Chebotarev)
   -- does extremal `Gamma` give a small/structured arithmetic Galois group vs `S_ell` for random?
   Tools: **Oscar/Hecke**, Sage/PARI (factor over `F_{p^d}`).
2. **Inverse theorem** for the max-fiber (the paper's named route): large fiber => structured
   support. Tools: additive combinatorics; computational structure-detection (Sage/FLINT).
3. **High-moment `Gamma_r`** via exact group-algebra DP in `Z[x]/(x^p-1)` + character sums. Tools:
   **python-flint/gmpy2** (exact), **PARI** (`lfun`), research CPU box / RunPod for scale.
4. **Transport CAP25 §23 kernel-section rigidity to the L1 syzygy** (M1->L1 adaptation). Tools:
   **Macaulay2/Singular/Oscar** (syzygies, resolvents), read §23 fully.
5. Keep the PR (#360) as the banked advance; poll for triage.

**Tooling verdict:** no new tools needed -- we have the full analytic-NT (PARI/Sage), AG (Oscar/
M2/Singular/HomotopyContinuation), exact-bignum (FLINT/gmpy2), scale (CPU box/RunPod), and formal
(Lean/Aristotle) stack. The gap is a TECHNIQUE shift to arithmetic-monodromy / inverse-theorem /
high-moment methods -- not analytic-only (character sums provably cap out, per us and the paper).

## Strategic note (prize-DAG)

`E_3` is a sub-problem feeding Conjecture-F, not one of the 7 unproved root TARGETs
(`petal_growth`, `rate_half_band_closure`, `worst_word_challenger_pricing`, `u2c_giant_tnull_dichotomy`,
`xr_smallcore_spread_count`, `dli_prime_weighted_large_block_support`, `u1_x4_direct_column_budget`).
If the goal is prize-critical leverage rather than this specific crux, those root TARGETs are where
the determination actually turns -- worth weighing against continuing the E_3 rank attack.
