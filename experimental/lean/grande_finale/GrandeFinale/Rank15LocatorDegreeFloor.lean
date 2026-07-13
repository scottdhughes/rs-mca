import Mathlib

/-!
# Rank-15 locator incidence-capacity degree floor: statement target

This module is an **UNPROVED STATEMENT TARGET** for
`experimental/notes/l2/rank15_locator_incidence_capacity_degree_floor.md`.
It records the deployed `M = 218` theorem at the imported locator-saturation
normal-form layer without claiming a Lean proof.

The finite set `R` is the literal residual evaluation set `H \ Z`.  Roots of
the monic common factor `G` are inactive, while every other coordinate carries
the actual affine section

`s * A(x) + t * B(x) = omega(x)`.

Thus the target retains the field, coprime polynomial pencil, proper-section
cap, degree budget, and pointwise agreement hypotheses used by the note.  It
does not replace the sections by a profile or include the desired degree floor
among its hypotheses.
-/

open scoped Classical

noncomputable section

namespace GrandeFinale
namespace Rank15LocatorDegreeFloor

set_option autoImplicit false

universe u

variable {F : Type u} [Field F] [DecidableEq F]

/-! ## Deployed constants -/

/-- `N = n - u`, the number of residual coordinates after the universal set. -/
def residualCoordinateCount : ℕ := 1_053_556

/-- `a = m - u`, the required agreement outside the universal set. -/
def residualAgreement : ℕ := 72_451

/-- The deployed number `M` of listed points in the affine two-flat. -/
def survivorCount : ℕ := 218

/-- The imported cap on every proper residual coordinate section. -/
def properSectionCap : ℕ := 15

/-- `lambda = K - 1 - u`, the degree budget after removing the universal set. -/
def residualDegreeBudget : ℕ := 4_979

/-- The degree floor proved in PR #733 under the imported normal form. -/
def deployedDegreeFloor : ℕ := 4_828

/-! ## Literal residual sections -/

/-- Residual coordinates at which the common polynomial factor does not
vanish.  The omitted coordinates are exactly the inactive set `I` of the
normal form. -/
def activeCoordinates (R : Finset F) (G : Polynomial F) : Finset F :=
  R.filter fun x => G.eval x ≠ 0

/-- The literal affine parameter-plane section attached to one active
coordinate. -/
def coordinateSection (S : Finset (F × F)) (A B : Polynomial F)
    (omega : F → F) (x : F) : Finset (F × F) :=
  S.filter fun p => p.1 * A.eval x + p.2 * B.eval x = omega x

/-- Active residual coordinates on which one listed parameter point agrees. -/
def agreementCoordinates (R : Finset F) (G A B : Polynomial F)
    (omega : F → F) (p : F × F) : Finset F :=
  (activeCoordinates R G).filter fun x =>
    p.1 * A.eval x + p.2 * B.eval x = omega x

/-- The normal-form degree `d = max(deg A, deg B)`.  The hypotheses below
ensure that both pencil directions are nonzero, so `natDegree` represents the
ordinary polynomial degrees here. -/
def pencilDegree (A B : Polynomial F) : ℕ :=
  max A.natDegree B.natDegree

/-! ## Imported normal-form hypotheses -/

/-- Bezout form of the imported condition `gcd(A,B) = 1`. -/
def CoprimePencil (A B : Polynomial F) : Prop :=
  ∃ U V : Polynomial F, U * A + V * B = 1

/-- The two polynomial directions remain linearly independent after the common
factor has been removed. -/
def IndependentPencil (A B : Polynomial F) : Prop :=
  ∀ alpha beta : F,
    Polynomial.C alpha * A + Polynomial.C beta * B = 0 →
      alpha = 0 ∧ beta = 0

/-- Exact hypotheses of the deployed `M = 218` survivor at the imported
rank-15 locator-saturation normal-form layer.

The two incidence conjuncts use the actual sections: every listed point has at
least `a = 72,451` active agreements, and every proper active section contains
at most `q = 15` listed points. -/
def DeployedSurvivorHypotheses (R : Finset F) (G A B : Polynomial F)
    (omega : F → F) (S : Finset (F × F)) : Prop :=
  R.card = residualCoordinateCount ∧
    S.card = survivorCount ∧
    G.Monic ∧
    CoprimePencil A B ∧
    IndependentPencil A B ∧
    pencilDegree A B + G.natDegree ≤ residualDegreeBudget ∧
    (∀ p ∈ S,
      residualAgreement ≤ (agreementCoordinates R G A B omega p).card) ∧
    ∀ x ∈ activeCoordinates R G,
      (coordinateSection S A B omega x).card ≤ properSectionCap

/-- Exact conclusion of the deployed degree-floor theorem. -/
def DegreeFloorConclusion (A B : Polynomial F) : Prop :=
  deployedDegreeFloor ≤ pencilDegree A B

/-- **UNPROVED STATEMENT TARGET.**  Every deployed `M = 218` survivor of the
imported rank-15 locator-saturation normal form has `d ≥ 4,828`.

This is a `Prop` definition, not a theorem declaration; no Lean proof is
claimed here. -/
def theoremTarget (R : Finset F) (G A B : Polynomial F)
    (omega : F → F) (S : Finset (F × F)) : Prop :=
  DeployedSurvivorHypotheses R G A B omega S →
    DegreeFloorConclusion A B

end Rank15LocatorDegreeFloor
end GrandeFinale
