# b2 Step 0 — object + regime PINNED from CAP25 (2026-07-06): a major reframe

- **Status:** Step-0 result (regime-first protocol). Tex-verified; corrects the earlier b2 model.
- **Method:** CAP25 extraction agent + my own verification of every load-bearing tex citation
  (`cap25_cap_v13_raw.tex`) + deployed-row arithmetic. This is the two-layer check the protocol requires.

## The object (verified, tex-quoted)

`Φ_{m,w}: (D choose m) → 𝔅^w, M ↦ ((-1)^h e_h(M))_{h≤w}`  (`:7251`, `prob:capfpr-Q`), `|D|=n`, `K=ρn`,
`m=K+w`, denominator `|𝔅|^w`. The zero-fiber = my "t-null blocks" (Newton: `e_1..e_w=0 ⟺ p_1..p_w=0`).
The `≤ n^3` (repo `16 n^3` budget) bounds only the **residual** — the moment-trade + primitive-non-coset
columns — after the exactly-counted coset-union main term (b1) and boundary column (QA.25) are peeled off.
Structured alternative (`:7543`): a **quotient stabilizer / common block structure / low-dim exceptional
incidence** — an **open `n^C` inverse-theorem target, NOT proved**; and `:7217` requires explicit `C` +
constants inside the finite margin (poly-loss ≠ certificate).

## The REGIME — corrected: ultra-DENSE, not rare-event (the key fix)

The extraction's `w = t ≈ 2^33` was WRONG. The **actual deployed prefix depth is `w ≈ 4096`** (QM31 row,
`:5149`: `w=m-⌈(k+1)/16⌉=69632-65537=4095`; `:5154`: `w=4096`), with a **"band depth" `w ≈ 67466`**
(`:8471`). Consequently the deployed regime is **near-full-entropy / ultra-dense**:
- `:8471`: `C(n,m) ≈ p^w · 2^192` ⟹ **mean fiber ≈ 2^192** (= "ultra-dense bulk at mean ≈ q/k", `:7119`).
- My earlier "first moment ≪ 1, rare-event" characterization was an artifact of the wrong `w=2^33`;
  the deployed rows are DENSE. (The repo b2-DAG node's `t·log2 q ≈ 2.15e12`, `t~2^33` is a *different*
  parameterization that does not match CAP25's deployed `w~4096–67466`.)

## What the problem REALLY is (verified, `:8471`)

`(Q)` = **balanced subset-sum equidistribution on a moment curve** `v_ξ = (ξ, ξ²/2, …, ξ^w/w)` at
near-full entropy = the **function-field analogue of equidistribution of the divisors of a fixed integer
in residue classes**. Fourier: Parseval pins typical character sums at `C(N,m) p^{-w/2}`, so fiber control
needs **square-root cancellation TWICE** over the `p^w` frequencies (two independent layers).
Difficulty is **depth-dependent**:
- **head depths `w ≤ w_0`**: **PROVED** (classical regime of polylogarithmic moduli);
- **band depth `w ≈ 67466`**: **OPEN EVEN OVER ℤ** (moduli of size `(#divisors)^{1-o(1)}`).

## Strategic upshot (honest)

- **b2 is NOT the crude/tractable lane.** It is divisor equidistribution at the `(#div)^{1-o(1)}` scale —
  a recognized deep problem, open over ℤ at band depth. The "crude inverse theorem in the rare-event
  regime" I was about to attack was the WRONG problem (wrong `w`, wrong regime, wrong difficulty).
- **The protocol worked:** Step-0 (pin object+params from primary source, check the arithmetic) caught a
  wrong-`w` model before any effort went into it. Code-green earlier had masked it (correct code, wrong `w`).
- **Immediate open question (decides b2's fate):** is the DEPLOYED `w` in the **head** range (`w ≤ w_0`,
  PROVED — then b2 is essentially done for those rows) or the **band** range (`w ≈ 67466`, OPEN)? Need
  `w_0` (the proved head-depth bound) and the exact deployed `w` per campaign row. That is the next step,
  NOT grinding an inverse theorem.
- **Novelty framing (upside):** connecting the deployed rows to divisor-equidistribution / short-interval
  results in `𝔽_q[X]` (Hayes / Keating–Rudnick / Sawin) is the correct literature — and the function-field
  moment-curve structure may be more tractable than the ℤ analogue. That is the real D1-style lit target,
  now correctly aimed.

## Deployed arithmetic (my verification, `b2_regime_check.py` extended)
With the WRONG `w=2^33`: `b/n≈ρ≤0.254<0.5`, first-moment exp `~-4e11` (rare) — but this used the wrong
`w`. With the CORRECT deployed `w~4096`, the mean fiber is `~2^192` (dense), per `:8471`. Re-do the
regime arithmetic at the true `w` once `w_0` and the per-row `w` are pinned.
