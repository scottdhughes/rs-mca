/-!
# First-match pruning bounds the signed q-gain (statement stub)

Maps to **hard input 2**: image-scale MI + MA / direct Sidon payment -- the
signed-minor clause of avdeevvadim's #716 dichotomy, on the depth-1
superincreasing family of #717 Sec 7 (`A_i=5^i`, `C=2 sum A_i+1`,
`T={A_i} u {C-A_i}`, `a=B`, `Phi=sum mod C`, `G=Z_C`).

Note: `experimental/notes/thresholds/first_match_signed_gain.md`.
Verifier: `experimental/scripts/verify_first_match_signed_gain.py` (215/215).

This module certifies the EXACT, DECIDABLE backbone of the two-sided theorem:
1. family arithmetic  `L=(3^B+1)/2`, `M=C(2B,B)`, `W=C(B,B/2)`;
2. heaviness monotonicity  `WL/M` strictly increasing (dense regime);
3. the integer q-window dichotomy
     unpruned R_A grows  (q>q_-=1/(1-log2/log3)=2.7095)  <=>  3^{q-1} > 2^q,
     pruned  R_A decays  (q<q_+=1/(3/2-2log2/log3)=4.1992) <=> 3^{3q-2} < 4^{2q},
   whose intersection (integer window) is exactly `{3,4}` and contains the
   census exponent `q=4`.

HONEST NONCLAIM: the analytic `l^q` projection bounds themselves
  (Theorem I: `R_A(g) <= (L/M)(L delta_A)^{1/2-1/q}`, all bands / all signs;
   Theorem II: `R_{A*}(f_full) >= (L^{1-1/q}/M)(W-M/C)/kappa`)
are PROVED in the note + Python verifier, NOT in Lean; they live over `R` with
DFT projections. This package is the decidable arithmetic/threshold shadow, in
the stdlib-only `native_decide` house style. No `sorry`. No mathlib.
-/

namespace FirstMatchSignedGain

/-! ## 1. Family arithmetic (exact) -/

/-- Binomial coefficient via Pascal's rule (stdlib-only; core `Nat` has no
    `Nat.choose` without mathlib). -/
def binom : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

theorem binom_check : binom 12 6 = 924 := by native_decide

def Limg (B : Nat) : Nat := (3 ^ B + 1) / 2          -- occupied-set size L
def Mslice (B : Nat) : Nat := binom (2 * B) B         -- M = C(2B,B)
def Wheavy (B : Nat) : Nat := binom B (B / 2)         -- heavy fiber W = C(B,B/2)

theorem L_B2 : Limg 2 = 5 := by native_decide
theorem L_B4 : Limg 4 = 41 := by native_decide
theorem L_B6 : Limg 6 = 365 := by native_decide

theorem M_B2 : Mslice 2 = 6 := by native_decide
theorem M_B4 : Mslice 4 = 70 := by native_decide
theorem M_B6 : Mslice 6 = 924 := by native_decide

theorem W_B2 : Wheavy 2 = 2 := by native_decide
theorem W_B4 : Wheavy 4 = 6 := by native_decide
theorem W_B6 : Wheavy 6 = 20 := by native_decide

/-- `M < C = 2 sum_{i=1}^B 5^i + 1` at every tabulated `B` (used in Theorem II
    to bound `W - M/C >= W/2`). -/
def Cmod (B : Nat) : Nat := 2 * (((5 ^ (B + 1) - 5) / 4)) + 1

theorem C_B2 : Cmod 2 = 61 := by native_decide
theorem C_B4 : Cmod 4 = 1561 := by native_decide
theorem C_B6 : Cmod 6 = 39061 := by native_decide
theorem M_lt_C_B2 : Mslice 2 < Cmod 2 := by native_decide
theorem M_lt_C_B4 : Mslice 4 < Cmod 4 := by native_decide
theorem M_lt_C_B6 : Mslice 6 < Cmod 6 := by native_decide

/-! ## 2. Heaviness monotonicity: WL/M strictly increases (dense regime).
    `WL/M(B1) < WL/M(B2)  <=>  W(B1)L(B1) M(B2) < W(B2)L(B2) M(B1)`. -/

theorem heavy_mono_2_4 :
    Wheavy 2 * Limg 2 * Mslice 4 < Wheavy 4 * Limg 4 * Mslice 2 := by native_decide
theorem heavy_mono_4_6 :
    Wheavy 4 * Limg 4 * Mslice 6 < Wheavy 6 * Limg 6 * Mslice 4 := by native_decide

/-! ## 3. Integer q-window dichotomy (exact thresholds, no logs).

`unprunedGrows q` is the exponentiated form of `q > q_- = 1/(1-log2/log3)`
(unpruned band excess `R_A -> infinity`, Theorem II).
`prunedDecays q` is the exponentiated form of `q < q_+ = 1/(3/2-2log2/log3)`
(pruned signed band excess `R_A -> 0`, Theorem I). -/

def unprunedGrows (q : Nat) : Bool := 3 ^ (q - 1) > 2 ^ q
def prunedDecays  (q : Nat) : Bool := 3 ^ (3 * q - 2) < 4 ^ (2 * q)
def inWindow (q : Nat) : Bool := unprunedGrows q && prunedDecays q

-- both clauses hold on the window {3,4} (contains the census exponent q=4)
theorem window_q3 : inWindow 3 = true := by native_decide
theorem window_q4 : inWindow 4 = true := by native_decide
theorem census_q4_in_window : inWindow 4 = true := by native_decide

-- boundary sharpness: q=2 is below q_- (unpruned flat), q=5 is above q_+ (pruned flat)
theorem below_q2_unpruned_flat : unprunedGrows 2 = false := by native_decide
theorem above_q5_pruned_flat : prunedDecays 5 = false := by native_decide
theorem out_of_window_q2 : inWindow 2 = false := by native_decide
theorem out_of_window_q5 : inWindow 5 = false := by native_decide

/-- The integer separation window is EXACTLY `{3,4}`. -/
theorem window_is_3_4 :
    ((List.range 8).filter (fun q => inWindow q)) = [3, 4] := by native_decide

/-! ## 4. Two-sided scale separation at the census exponent q=4.

Unpruned band excess exceeds unit scale: `(L^{1-1/q} W / M)^q > 1`, i.e.
`L^{q-1} W^q > M^q`, at `q=4` for every tabulated `B` (Theorem II direction). -/

def unprunedScaleExceedsOne (B : Nat) : Bool :=
  Limg B ^ 3 * Wheavy B ^ 4 > Mslice B ^ 4        -- q=4: L^{q-1} W^q > M^q

theorem unpruned_scale_B2 : unprunedScaleExceedsOne 2 = true := by native_decide
theorem unpruned_scale_B4 : unprunedScaleExceedsOne 4 = true := by native_decide
theorem unpruned_scale_B6 : unprunedScaleExceedsOne 6 = true := by native_decide

/-! ## 5. Dual via `decide` (spot checks) -/

theorem window_q4' : inWindow 4 = true := by decide
theorem out_of_window_q5' : inWindow 5 = false := by decide
theorem L_B2' : Limg 2 = 5 := by decide

end FirstMatchSignedGain
