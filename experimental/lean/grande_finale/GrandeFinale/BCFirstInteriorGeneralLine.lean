import Mathlib

/-!
# First-interior general-line BC modular fibers

This module proves the determinant-algebra kernel of
`bc_first_interior_general_line_modular_fibers.md`.  It also records numerical
rank and row-sharp compiler shapes as **UNPROVED STATEMENT TARGETS**.  Those
placeholders do not formalize the polynomial quotient map or its fiber.
-/

open Polynomial

noncomputable section

namespace GrandeFinale
namespace BCFirstInteriorGeneralLine

set_option autoImplicit false

universe u

variable {F : Type u} [Field F]

/--
The first determinant-derived small-multiplier identity.  If
`(W,N)=A(W1,N1)+B(W2,N2)`, `N=Wc`, `Lambda=W V`, and the basis determinant is
`gamma Lambda`, then `W1 c-N1=gamma B V`.
-/
theorem small_multiplier_identity
    (W1 N1 W2 N2 A B W N V Lambda c : F[X]) (gamma : F)
    (hW : W ≠ 0)
    (hdet : W1 * N2 - W2 * N1 = C gamma * Lambda)
    (hWrep : W = A * W1 + B * W2)
    (hNrep : N = A * N1 + B * N2)
    (hNc : N = W * c)
    (hLambda : Lambda = W * V) :
    W1 * c - N1 = C gamma * B * V := by
  apply mul_left_cancel₀ hW
  calc
    W * (W1 * c - N1) = W1 * N - N1 * W := by rw [hNc]; ring
    _ = W1 * (A * N1 + B * N2) - N1 * (A * W1 + B * W2) := by
      rw [hNrep, hWrep]
    _ = B * (W1 * N2 - W2 * N1) := by ring
    _ = B * (C gamma * Lambda) := by rw [hdet]
    _ = W * (C gamma * B * V) := by rw [hLambda]; ring

/--
The symmetric determinant-derived coordinate identity
`N2-W2 c=gamma A V`.
-/
theorem large_multiplier_identity
    (W1 N1 W2 N2 A B W N V Lambda c : F[X]) (gamma : F)
    (hW : W ≠ 0)
    (hdet : W1 * N2 - W2 * N1 = C gamma * Lambda)
    (hWrep : W = A * W1 + B * W2)
    (hNrep : N = A * N1 + B * N2)
    (hNc : N = W * c)
    (hLambda : Lambda = W * V) :
    N2 - W2 * c = C gamma * A * V := by
  apply mul_left_cancel₀ hW
  calc
    W * (N2 - W2 * c) = N2 * W - W2 * N := by rw [hNc]; ring
    _ = N2 * (A * W1 + B * W2) - W2 * (A * N1 + B * N2) := by
      rw [hWrep, hNrep]
    _ = A * (W1 * N2 - W2 * N1) := by ring
    _ = A * (C gamma * Lambda) := by rw [hdet]
    _ = W * (C gamma * A * V) := by rw [hLambda]; ring

/--
Algebraic converse: the two quotient identities recombine to the locator and
numerator coordinates.  Degree, monicity, and split-divisor hypotheses are the
separate coding-theoretic wrapper.
-/
theorem two_divisibilities_recombine
    (W1 N1 W2 N2 A B V Lambda c : F[X]) (gamma : F)
    (hgamma : gamma ≠ 0)
    (hdet : W1 * N2 - W2 * N1 = C gamma * Lambda)
    (hA : N2 - W2 * c = C gamma * A * V)
    (hB : W1 * c - N1 = C gamma * B * V) :
    (A * W1 + B * W2) * V = Lambda ∧
      (A * N1 + B * N2) * V = c * Lambda := by
  have hC : C gamma ≠ (0 : F[X]) := by simpa using hgamma
  constructor
  · apply mul_left_cancel₀ hC
    calc
      C gamma * ((A * W1 + B * W2) * V) =
          W1 * (C gamma * A * V) + W2 * (C gamma * B * V) := by ring
      _ = W1 * (N2 - W2 * c) + W2 * (W1 * c - N1) := by
        rw [hA, hB]
      _ = W1 * N2 - W2 * N1 := by ring
      _ = C gamma * Lambda := hdet
  · apply mul_left_cancel₀ hC
    calc
      C gamma * ((A * N1 + B * N2) * V) =
          N1 * (C gamma * A * V) + N2 * (C gamma * B * V) := by ring
      _ = N1 * (N2 - W2 * c) + N2 * (W1 * c - N1) := by
        rw [hA, hB]
      _ = c * (W1 * N2 - W2 * N1) := by ring
      _ = C gamma * (c * Lambda) := by rw [hdet]; ring

/--
**UNPROVED STATEMENT TARGET (fixed-multiplier quotient ranks).**

`rankFull` is the rank on polynomials of degree at most `m`; `rankMonic` is
the direction rank on the monic degree-`m` affine slice.  The intended
polynomial theorem assumes `m=K+w`, `d=deg W1`, `b=deg B`, and
`e=deg gcd(B,W1)`.
-/
def fixedMultiplierRankNumericalShapeTarget
    (K w d b e rankFull rankMonic : Nat) : Prop :=
  3 <= K ->
    d <= w + 2 ->
    b <= 1 ->
    e <= d ->
    e <= b ->
    rankFull = max d (w + 1 + b) - e ∧
      rankMonic = max d (w + b) - e

/--
**UNPROVED STATEMENT TARGET (row-sharp modular-locator fiber).**

The division-free inequality is
`cellCount * fieldSize^rank <= overhead * choose(n,m)`.  A uniform theorem of
this shape, summed over the at-most one- or two-dimensional multiplier family,
would pay the first-interior residual at effective depth `w`.
-/
def modularLocatorFiberNumericalBoundTarget
    (cellCount fieldSize rank overhead n m : Nat) : Prop :=
  cellCount * fieldSize ^ rank <= overhead * Nat.choose n m

end BCFirstInteriorGeneralLine
end GrandeFinale
