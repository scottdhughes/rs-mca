/-!
# Fold-level charge triviality and the flat-cube reduction (statement stub)

Maps to **hard input 2**: third packet of the arc (transverse-charge forcing
-> resonant-folding typing -> this reduction).  On the Sidon-paired class at
the maximal band, the forced sixth alternative reduces to ONE grammar
decision: admission of FLAT-CUBE EMISSION (ell^1 payment of certified-flat
sign-cubes).  Fold-measurable pieces are ell^2-charge-trivial at rate
e^{-(eta+kappa)N} for every failing band (Thm A, multiplicity only, no
clause, no (FR)); the exact charge ledger localizes the charge at levels
s ~ B/3 on both bases, with a BASE-3 light threshold at
s/B -> 1 - log2(4/3) (on base 5 every level is heavy) (Thm B); any
ell^2-capped scheme needs PN = 2^{B-o(B)} pieces (Thm C, exponent identity
2 g(1/3) - (2 log2 3 + 1) = 1... i.e. H(1/9) = 2 log2 3 - 8/3 exactly);
the sign-cube spectrum of the rooting weights is the explicit theta-product
transform of hat f and vanishes off D = empty at the maximal band (Thm D).

Note:     `experimental/notes/thresholds/fold_charge_localization.md`.
Verifier: `experimental/scripts/verify_fold_charge_localization.py`
          (49/49, tamper 5/5).

Analytic results (PROVED in note + Python verifier; NOT in Lean -- this
module is their DECIDABLE arithmetic shadow, stdlib-only `native_decide`,
no mathlib, no `sorry`): Thm A's cap, Thm B's exponent/concavity, Thm C's
PN exponent, Thm D's identity.  Below: the exact integer ledger, the light
threshold, the erratum witnesses, and the participation cross-multiplied
unsatisfiability, pinned at B in {6, 8} (base 3, c = 3^B).
-/

namespace FoldChargeLocalization

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Full slice `M = C(2B,B)`. -/
def slice (B : Nat) : Nat := binom (2 * B) B

/-- Level-`s` fiber size `w_s = C(B-s,(B-s)/2)`. -/
def fiberW (B s : Nat) : Nat := binom (B - s) ((B - s) / 2)

/-- Realized image `L = (3^B+1)/2` (B even). -/
def realizedImage (B : Nat) : Nat := (3 ^ B + 1) / 2

/-- Scaled level ledger `c * Omega~_+(s) = C(B,s) 2^s w_s (c w_s - M)_+`,
    base 3 (`c = 3^B`) -- exact integers. -/
def cLedgerTerm (B s : Nat) : Nat :=
  binom B s * 2 ^ s * fiberW B s * (3 ^ B * fiberW B s - slice B)

/-- Scaled square sum `c^2 * sum_{level s} f^2 h_+^2`
    `= C(B,s) 2^s w_s^2 (c w_s - M)_+^2`, base 3 -- exact integers.
    (Nat subtraction truncates at light levels, which is exactly `(.)_+`.) -/
def cSqTerm (B s : Nat) : Nat :=
  binom B s * 2 ^ s * (fiberW B s) ^ 2 * (3 ^ B * fiberW B s - slice B) ^ 2

/-! ## 1. Theorem B: the exact charge ledger (scaled by `c`). -/

theorem ledger_B6 :
    cLedgerTerm 6 0 = 273120 ∧ cLedgerTerm 6 2 = 1242000 ∧
    cLedgerTerm 6 4 = 256320 ∧ cLedgerTerm 6 6 = 0 ∧
    cLedgerTerm 6 0 + cLedgerTerm 6 2 + cLedgerTerm 6 4 = 1771440 := by
  native_decide

theorem ledger_B8 :
    cLedgerTerm 8 0 = 31248000 ∧ cLedgerTerm 8 2 = 265104000 ∧
    cLedgerTerm 8 4 = 178053120 ∧ cLedgerTerm 8 6 = 903168 ∧
    cLedgerTerm 8 8 = 0 ∧
    cLedgerTerm 8 0 + cLedgerTerm 8 2 + cLedgerTerm 8 4 + cLedgerTerm 8 6
      = 475308288 := by native_decide

/-- The `s ~ B/3` level dominates the ledger at both pinned sizes. -/
theorem ledger_argmax :
    (∀ s ∈ [0, 4, 6], cLedgerTerm 6 2 > cLedgerTerm 6 s) ∧
    (∀ s ∈ [0, 4, 6, 8], cLedgerTerm 8 2 > cLedgerTerm 8 s) := by
  native_decide

/-- Light threshold: zero-charge levels are exactly `{s : c w_s <= M}` --
    `{6}` at `B = 6`, `{8}` at `B = 8`. -/
theorem light_levels :
    3 ^ 6 * fiberW 6 6 ≤ slice 6 ∧ 3 ^ 6 * fiberW 6 4 > slice 6 ∧
    3 ^ 8 * fiberW 8 8 ≤ slice 8 ∧ 3 ^ 8 * fiberW 8 6 > slice 8 := by
  native_decide

/-! ## 2. The window erratum witnesses (transverse-charge Sec 5, prose). -/

/-- Lower end fails exactly on `{4,6}` (B=6) / `{4,6,8}` (B=8):
    `w_s L < 2M` there, `w_s L >= 2M` on the heavy levels. -/
theorem erratum_witnesses_B6 :
    fiberW 6 4 * realizedImage 6 < 2 * slice 6 ∧
    fiberW 6 6 * realizedImage 6 < 2 * slice 6 ∧
    fiberW 6 2 * realizedImage 6 ≥ 2 * slice 6 ∧
    fiberW 6 0 * realizedImage 6 ≥ 2 * slice 6 := by native_decide

theorem erratum_witnesses_B8 :
    fiberW 8 4 * realizedImage 8 < 2 * slice 8 ∧
    fiberW 8 6 * realizedImage 8 < 2 * slice 8 ∧
    fiberW 8 8 * realizedImage 8 < 2 * slice 8 ∧
    fiberW 8 2 * realizedImage 8 ≥ 2 * slice 8 := by native_decide

/-- The upper end IS universal at the pinned sizes: `w_s^2 L < M^2`,
    every level. -/
theorem window_upper_universal :
    (∀ s ∈ [0, 2, 4, 6], (fiberW 6 s) ^ 2 * realizedImage 6 < (slice 6) ^ 2) ∧
    (∀ s ∈ [0, 2, 4, 6, 8], (fiberW 8 s) ^ 2 * realizedImage 8 < (slice 8) ^ 2) := by
  native_decide

/-! ## 3. Theorem C: participation unsatisfiability (cross-multiplied). -/

/-- `K = 2^{B/2}` ell^2-capped pieces cannot pay:
    `K * c^2 sum f^2 h_+^2 < (c Omega~_+)^2` at `B in {6, 8}`. -/
theorem participation_unsat_B6 :
    2 ^ 3 * (cSqTerm 6 0 + cSqTerm 6 2 + cSqTerm 6 4 + cSqTerm 6 6)
      < (cLedgerTerm 6 0 + cLedgerTerm 6 2 + cLedgerTerm 6 4) ^ 2 := by
  native_decide

theorem participation_unsat_B8 :
    2 ^ 4 * (cSqTerm 8 0 + cSqTerm 8 2 + cSqTerm 8 4 + cSqTerm 8 6 + cSqTerm 8 8)
      < (cLedgerTerm 8 0 + cLedgerTerm 8 2 + cLedgerTerm 8 4 + cLedgerTerm 8 6) ^ 2 := by
  native_decide

/-- Thm A's rate ingredient (shared with the prior packets):
    `f_max^2 L < M^2` at the pinned sizes and beyond. -/
theorem rate_ingredient :
    ∀ B ∈ [6, 8, 16, 32], (binom B (B / 2)) ^ 2 * realizedImage B < (slice B) ^ 2 := by
  native_decide

/-- Existence side (re-verified, consumed by the erratum discussion):
    `f_max L >= 2M`. -/
theorem heavy_exists :
    ∀ B ∈ [6, 8, 16, 32], binom B (B / 2) * realizedImage B ≥ 2 * slice B := by
  native_decide

end FoldChargeLocalization
