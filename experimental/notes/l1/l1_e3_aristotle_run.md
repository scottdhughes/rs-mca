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

## Pushing the pencil lead — outcome: DEPENDENT (no cut), but a clean geometric reframing

`../scripts/pencil_cut_test.sage`. The pencil identity is exact:
`X^ell - t*Gamma - b_k(t) = g_k*(h_k - t*s_k)`, `b_k(t)=w_k - t*c_k` (verified). So the `K` excess
fibers are **common level sets of the pencil `F_t = X^ell - t*Gamma`** — equivalently the fibers of
the map `phi = (X^ell, Gamma) : x -> (x^ell, Gamma(x))`, and `mu_k = |coset_k ∩ Gamma^{-1}(c_k)|`.

**But the `s_k` condition does NOT cut `Syz` — it is a dependent consequence.** Adding
`Sum s_k q_k = 0`, then the companion `Sum u_k q_k = 0` (`u_k = w_k s_k - c_k h_k`), then a
`Gamma`-variant, leaves `dim Syz` UNCHANGED (`4, 7, 6, 5` for the saturators + non-saturator;
verified). Reason (exact): `Gamma*(Sum h_k q_k) = X^ell*(Sum s_k q_k) + (deg <= ell-2)`, so
`Sum s_k q_k` is *determined by* `Sum h_k q_k` (map `M`: top-`X^ell` part of `Gamma*A`) and vanishes
automatically on `Syz`. Every pencil-derived relation is such a consequence. So the lead reframes but
does not reduce the dimension. (Corrects Aristotle's "cuts down Syz".)

**Reframed crux (geometric):** `E_3 <= ell-2` <=> the degree-`ell` map `phi=(X^ell,Gamma)` has total
fiber-excess `Sum_{|fiber|>=3}(|fiber|-2) <= ell-2` — a rigidity of a single pencil.

## Open routes (neither elementary-in-hand)
1. **Pencil / AG genus count:** bound the common level sets of the pencil `{X^ell - t*Gamma}` (or the
   fibers of `phi`) via a Riemann–Hurwitz / value-set argument. Deep, not faked here.
2. **Direct rank of `Syz`:** the `dim Syz <= K` linear-algebra bound, without the (dependent) pencil
   conditions — still the K>=3 open chart. Re-verify any step on a second engine before promotion.
