/-!
# Failing bands are wide + cylinder renormalization (statement stub)

Maps to **hard input 2**: fifth packet of the arc (forcing -> typing ->
reduction -> scope -> compression).  U1: failing bands are exponentially
wide (|A| >= (c/L) e^{2 eta N}; narrow bands never fail).  U2/U3 (base 3,
c = 3^B): the angle vector is the x3-orbit of theta_1, and on the cylinder
xi = 3^k m the top k factors degenerate to (1+z)^2 exactly, giving
  hatf_B(3^k m) = sum_j C(2k, B-j) [z^j] p_{B-k, m},
with a twisted form for r != 0 cylinders and a cube-certificate recursion
(base-5 COUNTEREXAMPLE pinned: the identity is base-3-specific).

Note:     `experimental/notes/thresholds/cylinder_renormalization.md`.
Verifier: `experimental/scripts/verify_cylinder_renormalization.py`
          (42/42, tamper 5/5).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
trigonometric content of U2/U3 and the cube corollary live in the note and
the scans.  This module is the DECIDABLE arithmetic shadow (stdlib-only
`native_decide`, no mathlib, no `sorry`): U1's exact modulus identity
c = 2L - 1 on base 3, the DEGENERATE m = 0 instance of U3's convolution
algebra (binomial rows; the trigonometric m != 0 content is Python-only),
and the shared class pins.
-/

namespace CylinderRenormalization

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Full slice `M = C(2B,B)`. -/
def slice (B : Nat) : Nat := binom (2 * B) B

/-- Realized image `L = (3^B+1)/2` (B even). -/
def realizedImage (B : Nat) : Nat := (3 ^ B + 1) / 2

/-- Collision count `M2`. -/
def collisionMass (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    if s % 2 = B % 2 then
      acc + binom B s * 2 ^ s * (binom (B - s) ((B - s) / 2)) ^ 2
    else acc) 0

/-! ## 1. U1's exact modulus identity (base 3): `c = 2L - 1`. -/

theorem modulus_identity :
    ∀ B ∈ [4, 6, 8, 16, 32, 64], 3 ^ B = 2 * realizedImage B - 1 := by
  native_decide

/-! ## 2. U3's combinatorial half: the `(1+z)^{2k}` convolution.

The graded convolution `[z^B] (1+z)^{2k} q(z) = sum_j C(2k, B-j) q_j` is
pure polynomial algebra; `native_decide` checks it on pinned integer
vectors (binomial rows `q_j = C(2(B-k), j)`, the `m = 0` instance of
`p_{B-k, m}`, whose scale-B value must be `C(2B, B) = M` -- the
degenerate-cylinder consistency `hatf_B(0) = M`). -/

/-- `[z^B] (1+z)^{2k} (1+z)^{2(B-k)} = C(2B, B)`: the `m = 0` instance,
    computed through the graded sum. -/
theorem degenerate_cylinder_consistency :
    ∀ B ∈ [6, 8], ∀ k ∈ [1, 2, 3],
      (List.range (2 * (B - k) + 1)).foldl
        (fun acc j => if j ≤ B then
          acc + binom (2 * k) (B - j) * binom (2 * (B - k)) j else acc) 0
      = slice B := by native_decide

/-- Vandermonde consistency of the graded sum at shifted extraction
    degrees (the convolution algebra at `[z^{B-1}]` and `[z^{B+1}]`,
    pinned): `sum_j C(2k, d-j) C(2(B-k), j) = C(2B, d)`. -/
theorem graded_vandermonde :
    ∀ B ∈ [6, 8], ∀ k ∈ [1, 2, 3], ∀ d ∈ [5, 6, 7, 8, 9],
      (List.range (2 * (B - k) + 1)).foldl
        (fun acc j => if j ≤ d then
          acc + binom (2 * k) (d - j) * binom (2 * (B - k)) j else acc) 0
      = binom (2 * B) d := by native_decide

/-! ## 3. Shared class pins. -/

theorem class_pins :
    collisionMass 6 = 3584 ∧ collisionMass 8 = 97444 ∧
    slice 6 = 924 ∧ slice 8 = 12870 := by native_decide

end CylinderRenormalization
