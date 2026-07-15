/-!
# Resonant-folding inverse on the Sidon-paired class (statement stub)

Maps to **hard input 2**: the transverse-charge packet forced the sixth
(packet-scale) alternative of avdeevvadim's #716 Sec 7.1 on the Sidon-paired
class and named its resonant spectrum as the first mandatory test instance.
This packet structures that instance: Theorem 1 (shell structure -- resonance
forces digit structure), Theorem 2 (parity domination -- every correlation is
certified by an explicit pair-parity product character), Theorem 3 (exact
three-level decomposition packet -> parity class -> sign fiber, with the
band excess created exactly by the class -> fiber refinement).

Note:     `experimental/notes/thresholds/resonant_folding_inverse.md`.
Verifier: `experimental/scripts/verify_resonant_folding_inverse.py`
          (84/84, tamper 5/5).

Class (#739, #749-corrected hypotheses): `P = {base^i : i < B}`
2-superincreasing, `c = 2 sum P + 1`, `T = P u (c-P)`, `a = B`,
`Phi = subset sum mod c`; `M = C(2B,B)`, `f_max = C(B,B/2)`,
`M2 = sum_s C(B,s) 2^s C(B-s,(B-s)/2)^2`.  Parity fold
`v(S)_i = |S cap pair_i| mod 2`, `s = |supp v|`; fold characters
`psi_H`, `h = |H|`.

Analytic results (PROVED in note + Python verifier; NOT in Lean -- this
module is their DECIDABLE arithmetic shadow, stdlib-only `native_decide`,
no mathlib, no `sorry`):
  Thm 1   |hat f(j)| >= rho M  =>  m(j,delta) <= ln(2 sqrt B / rho) /
          (2 ln sec(pi delta)); chain |hat f| <= 4^B cos(pi delta)^{2m} and
          4 B M^2 >= 16^B (the binomial input IS proved below).
  Thm 2   <chi_j o Phi, psi_H(j)> = [z^B] prod (1 + z^2 + 2z|cos theta_i|)
          >= |hat f(j)|, real nonnegative; equality on H(j) in {0, [B]};
          H(j*) = [B] exactly (the congruence IS proved below).
  Thm 3   (a) N_v = 2^s C(B-s,(B-s)/2), flat window; (b) fold spectrum =
          Krawtchouk values, +-M only at h in {0,B}; (c) parity-Parseval,
          participation ratio in [2,3]; (d) M2 = sum_v N_v^2 2^{-s}, maximizer
          s* ~ B/3.  All identities pinned below at B in {6, 8}.
-/

namespace ResonantFolding

/-! ## 0. Exact combinatorial scalars. -/

/-- `binom n k = C(n,k)` via the running product `prod_{i<k} (n-i)/(i+1)`. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Full slice `M = C(2B,B)`. -/
def slice (B : Nat) : Nat := binom (2 * B) B

/-- Collision count `M2 = sum_{s == B mod 2} C(B,s) 2^s C(B-s,(B-s)/2)^2`. -/
def collisionMass (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    if s % 2 = B % 2 then
      acc + binom B s * 2 ^ s * (binom (B - s) ((B - s) / 2)) ^ 2
    else acc) 0

/-- Ambient modulus `c = 2*sum_{i<B} base^i + 1`; for base 3 this is `3^B`. -/
def ambientMod (base B : Nat) : Nat := 2 * ((base ^ B - 1) / (base - 1)) + 1

/-! ## 1. Theorem 3a: the parity-class profile `N_v`. -/

/-- Class size `N_v = 2^s C(B-s,(B-s)/2)` for `s = |supp v| == B (mod 2)`,
    else 0 (Theorem 3a). -/
def classSize (B s : Nat) : Nat :=
  if s % 2 = B % 2 then 2 ^ s * binom (B - s) ((B - s) / 2) else 0

theorem profile_B6 :
    classSize 6 0 = 20 ∧ classSize 6 2 = 24 ∧ classSize 6 4 = 32 ∧
    classSize 6 6 = 64 ∧ classSize 6 1 = 0 ∧ classSize 6 3 = 0 ∧
    classSize 6 5 = 0 := by native_decide

theorem profile_B8 :
    classSize 8 0 = 70 ∧ classSize 8 2 = 80 ∧ classSize 8 4 = 96 ∧
    classSize 8 6 = 128 ∧ classSize 8 8 = 256 := by native_decide

/-- The classes tile the packet: `sum_v N_v = sum_s C(B,s) N(s) = M`. -/
theorem classes_tile_B6 :
    (List.range 7).foldl (fun acc s => acc + binom 6 s * classSize 6 s) 0
      = slice 6 := by native_decide

theorem classes_tile_B8 :
    (List.range 9).foldl (fun acc s => acc + binom 8 s * classSize 8 s) 0
      = slice 8 := by native_decide

/-- Flat marginal (Theorem 3a window): `2^B/sqrt(2B) <= N_v <= 2^B`,
    cross-multiplied. -/
theorem flat_window_B6 :
    ∀ s ∈ [0, 2, 4, 6],
      2 * 6 * (classSize 6 s) ^ 2 ≥ 4 ^ 6 ∧ classSize 6 s ≤ 2 ^ 6 := by
  native_decide

theorem flat_window_B8 :
    ∀ s ∈ [0, 2, 4, 6, 8],
      2 * 8 * (classSize 8 s) ^ 2 ≥ 4 ^ 8 ∧ classSize 8 s ≤ 2 ^ 8 := by
  native_decide

/-! ## 2. Theorem 3b: the fold spectrum (Krawtchouk values). -/

/-- `<psi_H> = sum_k (-1)^k C(2h,k) C(2B-2h,B-k)` (depends only on `h = |H|`;
    equals `[z^B](1-z)^{2h}(1+z)^{2(B-h)}`). -/
def foldFourier (B h : Nat) : Int :=
  (List.range (B + 1)).foldl (fun acc k =>
    acc + (if k % 2 = 0 then (1 : Int) else -1)
        * (binom (2 * h) k : Int) * (binom (2 * B - 2 * h) (B - k) : Int)) 0

theorem spectrum_B6 :
    (List.range 7).map (foldFourier 6)
      = [924, -84, 28, -20, 28, -84, 924] := by native_decide

theorem spectrum_B8 :
    (List.range 9).map (foldFourier 8)
      = [12870, -858, 198, -90, 70, -90, 198, -858, 12870] := by
  native_decide

/-- Only the two constant-on-packet characters reach `+-M` (endpoints exact,
    interior strictly smaller). -/
theorem spectrum_extremes_B6 :
    foldFourier 6 0 = (slice 6 : Int) ∧ foldFourier 6 6 = (slice 6 : Int) ∧
    (∀ h ∈ [1, 2, 3, 4, 5], (foldFourier 6 h).natAbs < slice 6) := by
  native_decide

theorem spectrum_extremes_B8 :
    foldFourier 8 0 = (slice 8 : Int) ∧ foldFourier 8 8 = (slice 8 : Int) ∧
    (∀ h ∈ [1, 2, 3, 4, 5, 6, 7], (foldFourier 8 h).natAbs < slice 8) := by
  native_decide

/-! ## 3. Theorem 3c: parity-Parseval and the participation ratio. -/

/-- `sum_H <psi_H>^2` over all `2^B` subsets, grouped by `h`. -/
def foldEnergy (B : Nat) : Int :=
  (List.range (B + 1)).foldl (fun acc h =>
    acc + (binom B h : Int) * (foldFourier B h) ^ 2) 0

/-- `2^B sum_v N_v^2`, grouped by `s`. -/
def classEnergy (B : Nat) : Int :=
  (2 ^ B : Int) * (List.range (B + 1)).foldl (fun acc s =>
    acc + (binom B s : Int) * (classSize B s : Int) ^ 2) 0

theorem parity_parseval_B6 :
    foldEnergy 6 = classEnergy 6 ∧ foldEnergy 6 = 1823744 := by native_decide

theorem parity_parseval_B8 :
    foldEnergy 8 = classEnergy 8 ∧ foldEnergy 8 = 346498048 := by
  native_decide

/-- Participation ratio window `2 M^2 <= sum_H <psi_H>^2 <= 3 M^2`:
    the fold spectrum is l^2-dominated by the two `+-M` characters. -/
theorem participation_window_B6 :
    2 * (slice 6 : Int) ^ 2 ≤ foldEnergy 6 ∧
    foldEnergy 6 ≤ 3 * (slice 6 : Int) ^ 2 := by native_decide

theorem participation_window_B8 :
    2 * (slice 8 : Int) ^ 2 ≤ foldEnergy 8 ∧
    foldEnergy 8 ≤ 3 * (slice 8 : Int) ^ 2 := by native_decide

/-! ## 4. Theorem 3d: exact `M2` reconstruction and the `s* ~ B/3` maximizer. -/

/-- `2^B M2 = sum_v N_v^2 2^{B-s}`: the collision mass is exactly the
    class -> sign-fiber refinement of the flat parity level. -/
def reconMass (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    acc + binom B s * (classSize B s) ^ 2 * 2 ^ (B - s)) 0

theorem reconstruction_B6 :
    reconMass 6 = 2 ^ 6 * collisionMass 6 ∧ collisionMass 6 = 3584 := by
  native_decide

theorem reconstruction_B8 :
    reconMass 8 = 2 ^ 8 * collisionMass 8 ∧ collisionMass 8 = 97444 := by
  native_decide

/-- Per-class collision term `T(s) = C(B,s) 2^s C(B-s,(B-s)/2)^2`. -/
def collisionTerm (B s : Nat) : Nat :=
  binom B s * 2 ^ s * (binom (B - s) ((B - s) / 2)) ^ 2

/-- The `M2` maximizer sits at `s* = B/3` exactly at `B = 6` (and within the
    note's `|s* - B/3| <= 2` window at `B = 8`, where `s* = 2`). -/
theorem maximizer_B6 :
    ∀ s ∈ [0, 4, 6], collisionTerm 6 2 > collisionTerm 6 s := by
  native_decide

theorem maximizer_B8 :
    ∀ s ∈ [0, 4, 6, 8], collisionTerm 8 2 > collisionTerm 8 s := by
  native_decide

/-! ## 5. The two exact inputs of Theorems 1-2. -/

/-- Theorem 1's binomial input `M >= 4^B/(2 sqrt B)`, cross-multiplied. -/
theorem shell_binomial_input :
    ∀ B ∈ [6, 8, 16], 4 * B * (slice B) ^ 2 ≥ 16 ^ B := by native_decide

/-- Theorem 2's half-frequency antipodal set is ALL of `[B]`:
    `cos(2 pi j* A_i / c) < 0` exactly, i.e. `4 (j* A_i mod c) in (c, 3c)`,
    at `j* = (c-1)/2`, for every scale -- base 3, `B in {6,8}`, and base 5,
    `B = 6`.  (So the `j*` resonance is certified by the constant character
    `psi_[B]`.) -/
theorem antipodal_all_base3_B6 :
    ∀ i ∈ [0, 1, 2, 3, 4, 5],
      ambientMod 3 6 < 4 * (((ambientMod 3 6 - 1) / 2 * 3 ^ i) % ambientMod 3 6) ∧
      4 * (((ambientMod 3 6 - 1) / 2 * 3 ^ i) % ambientMod 3 6) < 3 * ambientMod 3 6 := by
  native_decide

theorem antipodal_all_base3_B8 :
    ∀ i ∈ [0, 1, 2, 3, 4, 5, 6, 7],
      ambientMod 3 8 < 4 * (((ambientMod 3 8 - 1) / 2 * 3 ^ i) % ambientMod 3 8) ∧
      4 * (((ambientMod 3 8 - 1) / 2 * 3 ^ i) % ambientMod 3 8) < 3 * ambientMod 3 8 := by
  native_decide

theorem antipodal_all_base5_B6 :
    ∀ i ∈ [0, 1, 2, 3, 4, 5],
      ambientMod 5 6 < 4 * (((ambientMod 5 6 - 1) / 2 * 5 ^ i) % ambientMod 5 6) ∧
      4 * (((ambientMod 5 6 - 1) / 2 * 5 ^ i) % ambientMod 5 6) < 3 * ambientMod 5 6 := by
  native_decide

/-- Sanity: base-3 ambient modulus is `3^B`; `j*` values as scanned. -/
theorem ambient_pins :
    ambientMod 3 6 = 3 ^ 6 ∧ ambientMod 3 8 = 3 ^ 8 ∧
    ambientMod 5 6 = 7813 ∧
    (ambientMod 3 6 - 1) / 2 = 364 ∧ (ambientMod 3 8 - 1) / 2 = 3280 ∧
    (ambientMod 5 6 - 1) / 2 = 3906 := by native_decide

end ResonantFolding
