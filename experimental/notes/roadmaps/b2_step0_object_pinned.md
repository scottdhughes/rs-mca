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
- **RESOLVED (2026-07-06): DEPLOYED = BAND = OPEN at every row.** Proved head-depth bound is tiny:
  `w_0 = 21–22` (KoalaBear) / `10–11` (Mersenne-31) — `:7111` ("pays one Weil cost √p per power sum, and
  this is exactly what stops it at `w_0=21–22`"), `:8158`, `cor:capff1-collision-head`. Deployed rows sit
  at `w = 4096` (MCA, `:5149`) to `w = 67470/67446` (list frontier, `:6944` `prop:capff1-identity-frontier`)
  — orders of magnitude ABOVE `w_0`. So the max-fiber bound is proved only for the first ~21 rungs and is
  **OPEN at every deployed depth**. `:7115`: even a poly-loss bound "does NOT decide the printed adjacent
  pairs" (margins 22.2/22.0/3.3/3.1 bits) — needs the constant-factor `(1+o(1))`-of-mean form.
- **VERDICT: b2 is OPEN at every deployed row — NOT a shippable milestone.** The "b2 is the tractable
  entry point" thesis is REFUTED. b2 = the √p-barrier max-fiber inequality at band depth = divisor
  equidistribution open over ℤ. b2 and L1 are in the SAME difficulty class (both √p-barrier; b2 stops at
  `w_0=21` for the same reason L1 route A did). Neither has a crude escape.
- **Novelty framing (upside):** connecting the deployed rows to divisor-equidistribution / short-interval
  results in `𝔽_q[X]` (Hayes / Keating–Rudnick / Sawin) is the correct literature — and the function-field
  moment-curve structure may be more tractable than the ℤ analogue. That is the real D1-style lit target,
  now correctly aimed.

## Deployed arithmetic (my verification, `b2_regime_check.py` extended)
With the WRONG `w=2^33`: `b/n≈ρ≤0.254<0.5`, first-moment exp `~-4e11` (rare) — but this used the wrong
`w`. With the CORRECT deployed `w~4096`, the mean fiber is `~2^192` (dense), per `:8471`. Re-do the
regime arithmetic at the true `w` once `w_0` and the per-row `w` are pinned.
