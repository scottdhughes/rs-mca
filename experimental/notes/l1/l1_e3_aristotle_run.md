# L1: Aristotle run on the KEY LEMMA — Lean formalization + a verified new lead

- **Status:** AUDIT (Aristotle output = DRAFT, re-verified here) + one VERIFIED new lead.
- **Agent/model:** Aristotle (Harmonic), project `70427d46-d108-4d03-8edd-bdf9594bb86f`
  (run `528d145d-…`, ~1h, terminal/IDLE). Lead re-verified by Claude Opus 4.8 in Sage.
- **Date:** 2026-07-06.

## What Aristotle produced (banked in `../../lean/l1_e3_aristotle/`)

- **Faithful Lean formalization** (`RequestProject/Main.lean`, builds vs Mathlib): the statement
  `E3_le : E3 p ℓ Γ ≤ ℓ - 2` under the exact hypotheses, with the **partition backbone PROVED,
  no sorry**: `card_cosetF_eq` (each nonempty coset has exactly `ℓ` elements), `card_powersF`
  (`(p-1)/ℓ` cosets), `levelMax_le_ell` (`μ(C) ≤ ℓ`). This is the Lean formalization the repo's
  AGENTS.md flagged as not-yet-done. The main inequality is a single **annotated `sorry`** (no
  axioms, no vacuous restatement — honest).
- **Independent reproduction** of our results: the upper half `dim(ΣV_k) ≤ ℓ-2` via the same
  functional `L(A)=[X^{ℓ-1}](A·Γ)`; the reduction to `dim Syz ≤ K`; and "realizability is
  essential" with a **clean explicit counterexample** to the coprime-only version: `N=4, K=3`,
  `h = X-1, X-2, X²-X-1` gives `dim Syz ≥ 6 > 3 = K`. (Matches our arbitrary-config finding.)

## The new lead — VERIFIED (`../scripts/verify_aristotle_syzygy_lead.sage`)

With `s_k := (Γ - c_k)/g_k` (polynomial since `g_k | Γ-c_k`), Aristotle derived and we CONFIRMED
on the saturators:

> **Every degree-bounded syzygy of the `h_k` is also a syzygy of the `s_k`:**
> `Σ_k h_k q_k = 0 (deg q_k ≤ μ_k-2)  ⟹  Σ_k s_k q_k = 0`, plus the companion identity
> `Σ_k w_k q_k s_k = Σ_k c_k q_k h_k`. (VERIFIED True, all 3 saturators, K=4/7/6.)

Derivation: multiply the syzygy by `Γ`, use `h_k(Γ-c_k) = (X^ℓ-w_k) s_k`, then separate degrees
(`X^ℓ·(Σ q_k s_k)` sits in degrees `≥ ℓ`; the rest is `≤ ℓ-2`), forcing the top part to vanish.

**Why it matters:** this uses the **single-`Γ` structure** (the exact ingredient the false
coprime-only version lacks) to narrow `Syz`. Equivalently, for every `t`, `Σ_k (h_k - t s_k) q_k = 0`
— the syzygy lives in the *pencil* `h_k - t s_k = ((X^ℓ - w_k) - t(Γ - c_k))/g_k` for ALL `t`
(connects to the frontier note's "pencil-locality / rotation-coupling" Route A). It cuts `Syz`
but does not yet close `dim Syz ≤ K` — that remains the open crux.

## Next step
Exploit `Syz(h) ⊆ Syz(s)` (the all-`t` pencil condition): a syzygy simultaneously kills
`{h_k}` and `{s_k}` with `deg s_k = deg h_k - 1`. Push this toward `dim Syz ≤ K` (or find the
next obstruction). Re-verify any step on a second engine before promotion.
