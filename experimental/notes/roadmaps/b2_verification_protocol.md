# b2 verification protocol (regime-first) — to avoid the 2026-07-06 mistakes

Adopted after the b2 "nail it" attempt validated the L¹-average mechanism in the WRONG b-regime
(`b~n/2`, which passes at small `n` but FAILS at prize) — while every Codex code-review passed, because
the code correctly computed the wrong-regime quantity. **Code-correct ≠ claim-valid.**

## Run every b2 sub-claim through this, in order

0. **Object & parameters FIRST (gates everything).** Pin from the primary source (CAP25 `b2_modp_giant_extras`
   node / the deployed row): the exact object counted, and the deployed `(n, b, t, q)` + relations. Then the
   **step-0 sanity arithmetic**: does the claim hold for the modeled quantity *at the deployed parameters*?
   (For b2: `C(n,b)/q^t ≤ n^3` at the deployed `b`? — `b2_regime_check.py`.) If unanswerable, do not model yet.
1. **Regime map.** List every governing threshold — `log2 C(n,b)` vs `t log2 q + 3 log2 n`; `√q` vs `n`;
   `t` vs `n`; `b` vs `n/2`. Compute each at BOTH toy and deployed scale. A toy validates a claim ONLY if it
   is on the same side of EVERY threshold. Flag distinctions the toy is too small to see.
2. **Toys must SEPARATE regimes** (`n ≫ t`, etc.), not collapse them. No feasible separating toy ⇒ say so;
   don't generalize from the collapsed toy.
3. **Adversarial regime-break.** Actively try to BREAK the bound at the extremes (largest `b`, largest `n`,
   worst ratio) before claiming it holds. If it breaks anywhere ⇒ state the regime restriction.
4. **Two-layer review.** Keep the Codex code-correctness loop AND add a distinct explicit question in the
   prompt: *"is this the right object, in the deployed regime?"* — not just "is the code correct."
5. **No premature labels.** Nothing is "citeable / off-the-shelf / tractable" until: reduction end-to-end,
   theorem named, hypotheses+regime checked vs deployed params, deployed arithmetic passes. Else: "candidate route."

## Current b2 state under this protocol
- The `extras_b ≤ n^3` claim is **regime-restricted** (holds `b ∈ [t, ~n/4]`; fails `b~n/2` at prize).
- The prize-relevant regime is `b ≈ t` (first moment ≪ 1) — a **rare-event / crude inverse theorem**
  ("pure counting can never close it", per the node), NOT the clean L¹-average calculation.
- **Step 0 is OPEN and next:** pin the deployed `b` (fiber size) at an actual prize row from CAP25, confirm
  it lies in `[t, ~n/4]`, and re-derive the operative bound in that regime (clean toy needs `n ≫ t`).
