/-!
# Band-uniform signed death + narrow-band cube certificate (statement stub)

Maps to **hard input 2**: fourth packet of the arc (forcing -> typing ->
reduction -> scope).  T1: at the canonical q=2 rooting of EVERY failing
band, disjoint ell^2-compatible pieces obey sum c_i <= sqrt(K) f_max --
multiplicity-free (only disjointness is used), so any e^{o(N)} budget pays
e^{-Theta(N)} of the charge, band-uniformly; the rate is
e^{2(eta+kappa)N} via f_max^2 L < M^2.  T2: for a symmetric band avoiding
0, ONE list {(xi, hatf(xi))} determines h_A on EVERY sign-cube via the
theta-product transform -- e^{o(N)} certificate for narrow bands.  T3: the
named-pattern payment floor 2^s |hcube_v(D*)| <= cube ell^1 is sound
band-uniformly, exact (D* = empty) at the maximal band.

Note:     `experimental/notes/thresholds/band_uniform_cube_reduction.md`.
Verifier: `experimental/scripts/verify_band_uniform_reduction.py`
          (26/26, tamper 6/6).

Analytic results (PROVED in note + Python verifier; NOT in Lean): T1's cap
and count, T2's identity, T3's floor -- their trigonometric content lives
in the note and the Python scans.  This module is the DECIDABLE arithmetic
shadow of T1 ONLY (stdlib-only `native_decide`, no mathlib, no `sorry`):
its exact integer ingredients pinned at B in {6, 8} (base 3, c = 3^B), the
rate to B = 32, plus the antipodal integer core of the j* certificate
(the T2 input's one integer-exact fact).
-/

namespace BandUniformReduction

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Full slice `M = C(2B,B)`. -/
def slice (B : Nat) : Nat := binom (2 * B) B

/-- Level-`s` fiber size `w_s = C(B-s,(B-s)/2)`. -/
def fiberW (B s : Nat) : Nat := binom (B - s) ((B - s) / 2)

/-- Central fiber `f_max = C(B,B/2)`. -/
def maxFiber (B : Nat) : Nat := binom B (B / 2)

/-- Realized image `L = (3^B+1)/2` (B even). -/
def realizedImage (B : Nat) : Nat := (3 ^ B + 1) / 2

/-- Scaled maximal-band ledger `c * Omega~_+` (base 3), exact. -/
def cLedger (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    if s % 2 = B % 2 then
      acc + binom B s * 2 ^ s * fiberW B s
            * (3 ^ B * fiberW B s - slice B)
    else acc) 0

/-- Scaled square sum `c^2 * sum f^2 h_+^2` (base 3), exact. -/
def cSq (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    if s % 2 = B % 2 then
      acc + binom B s * 2 ^ s * (fiberW B s) ^ 2
            * (3 ^ B * fiberW B s - slice B) ^ 2
    else acc) 0

/-- Scaled plain square sum `c^2 * sum h_+^2` (base 3), exact. -/
def cH2 (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    if s % 2 = B % 2 then
      acc + binom B s * 2 ^ s
            * (3 ^ B * fiberW B s - slice B) ^ 2
    else acc) 0

/-! ## 1. T1's exact integer ingredients. -/

/-- The kappa-rate ingredient `f_max^2 L < M^2`. -/
theorem rate_ingredient :
    ∀ B ∈ [6, 8, 16, 32], (maxFiber B) ^ 2 * realizedImage B < (slice B) ^ 2 := by
  native_decide

/-- The `f_max^2` relaxation used by T1:
    `c^2 sum f^2 h_+^2 <= f_max^2 * c^2 sum h_+^2` (maximal band). -/
theorem fmax_relaxation :
    cSq 6 ≤ (maxFiber 6) ^ 2 * cH2 6 ∧
    cSq 8 ≤ (maxFiber 8) ^ 2 * cH2 8 := by native_decide

/-- The maximal-band `K = 2^{B/2}` cross-multiplied unsatisfiability
    (T1's chain instantiated exactly; the fold-charge wall, re-proved). -/
theorem budget_unsat :
    2 ^ 3 * cSq 6 < (cLedger 6) ^ 2 ∧
    2 ^ 4 * cSq 8 < (cLedger 8) ^ 2 := by native_decide

/-- Ledger cross-pins shared with the fold-charge packet. -/
theorem ledger_pins :
    cLedger 6 = 1771440 ∧ cLedger 8 = 475308288 := by native_decide

/-! ## 2. T2's exact angle inputs (the antipodal congruence at `j*`,
    re-pinned: the top shell frequency's certificate reads every scale). -/

/-- `4 (j* A_i mod c) in (c, 3c)` for every scale, `j* = (c-1)/2`,
    base 3, `B in {6, 8}` -- the integer form of `cos theta_i(j*) < 0`. -/
theorem antipodal_jstar :
    (∀ i ∈ [0, 1, 2, 3, 4, 5],
      3 ^ 6 < 4 * (((3 ^ 6 - 1) / 2 * 3 ^ i) % 3 ^ 6) ∧
      4 * (((3 ^ 6 - 1) / 2 * 3 ^ i) % 3 ^ 6) < 3 * 3 ^ 6) ∧
    (∀ i ∈ [0, 1, 2, 3, 4, 5, 6, 7],
      3 ^ 8 < 4 * (((3 ^ 8 - 1) / 2 * 3 ^ i) % 3 ^ 8) ∧
      4 * (((3 ^ 8 - 1) / 2 * 3 ^ i) % 3 ^ 8) < 3 * 3 ^ 8) := by
  native_decide

end BandUniformReduction
