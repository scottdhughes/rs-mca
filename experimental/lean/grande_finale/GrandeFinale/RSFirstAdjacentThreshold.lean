import GrandeFinale.RSFirstAdjacentRow

/-!
# Exact first adjacent Reed--Solomon threshold

This module derives the two target-dependent threshold implications (AD2) from
the exact AD1 numerator and the exact support-atlas upper bound. It uses the
manuscript's proposition-level characterization of the first safe agreement:
the chosen grid point is safe, and every earlier grid point is unsafe.
-/

open scoped Classical

noncomputable section

namespace GrandeFinale.RSFirstAdjacentThreshold

open GrandeFinale.CollisionAwarePole
open GrandeFinale.RSExactSupportUpper
open GrandeFinale.RSFirstAdjacentRow

variable {D F : Type*} [Field F] [Fintype D] [DecidableEq D]
  [Fintype F] [DecidableEq F]

/-- Agreement `a` is the target-dependent first safe point on the exact
Reed--Solomon grid `{k+1, ..., n}`. -/
def IsFirstSafeMCA (C : Set (D → F))
    (k n budget a : Nat) : Prop :=
  k + 1 ≤ a ∧ a ≤ n ∧
    GrandeFinale.B_MCA C a ≤ budget ∧
    ∀ a', k + 1 ≤ a' → a' < a →
      budget < GrandeFinale.B_MCA C a'

omit [DecidableEq F] in
/-- The first-safe agreement is unique whenever it exists. -/
theorem isFirstSafeMCA_unique
    (C : Set (D → F)) (k n budget : Nat) {a a' : Nat}
    (ha : IsFirstSafeMCA C k n budget a)
    (ha' : IsFirstSafeMCA C k n budget a') :
    a = a' := by
  apply Nat.le_antisymm
  · by_contra h
    have hlt : a' < a := Nat.lt_of_not_ge h
    exact (Nat.not_lt_of_ge ha'.2.2.1) (ha.2.2.2 a' ha'.1 hlt)
  · by_contra h
    have hlt : a < a' := Nat.lt_of_not_ge h
    exact (Nat.not_lt_of_ge ha.2.2.1) (ha'.2.2.2 a ha.1 hlt)

/-- The first AD2 implication: a budget at least
`M = choose |D| (R-1)` makes `k+1` the first safe agreement. -/
theorem firstAdjacent_isFirstSafeMCA
    (ev : D → F) (hev : Function.Injective ev)
    (k R budget : Nat) (hR : 0 < R)
    (hsize : k + R = Fintype.card D)
    (hgate :
      max (Nat.choose (Fintype.card D) (R - 1))
          ((Nat.choose (Fintype.card D) (R - 1)).choose 2) <
        Fintype.card F)
    (hbudget : Nat.choose (Fintype.card D) (R - 1) ≤ budget) :
    IsFirstSafeMCA (rsEval ev k : Set (D → F))
      k (Fintype.card D) budget (k + 1) := by
  refine ⟨by omega, by omega, ?_, ?_⟩
  · rw [B_MCA_rsEval_eq_choose_redundancy_pred
      ev hev k R hR hsize hgate]
    exact hbudget
  · intro a ha hlt
    omega

/-- The second AD2 implication: if
`choose |D| (R-2) <= budget < choose |D| (R-1)`, then `k+2` is the first
safe agreement. -/
theorem secondAdjacent_isFirstSafeMCA
    (ev : D → F) (hev : Function.Injective ev)
    (k R budget : Nat) (hR : 2 ≤ R)
    (hsize : k + R = Fintype.card D)
    (hgate :
      max (Nat.choose (Fintype.card D) (R - 1))
          ((Nat.choose (Fintype.card D) (R - 1)).choose 2) <
        Fintype.card F)
    (hbudgetLower : Nat.choose (Fintype.card D) (R - 2) ≤ budget)
    (hbudgetUpper : budget < Nat.choose (Fintype.card D) (R - 1)) :
    IsFirstSafeMCA (rsEval ev k : Set (D → F))
      k (Fintype.card D) budget (k + 2) := by
  refine ⟨by omega, by omega, ?_, ?_⟩
  · calc
      GrandeFinale.B_MCA (rsEval ev k : Set (D → F)) (k + 2) ≤
          Nat.choose (Fintype.card D) (k + 2) :=
        B_MCA_rsEval_le_choose ev hev k R hsize (k + 2) (by omega)
      _ = Nat.choose (Fintype.card D) (R - 2) := by
        apply Nat.choose_symm_of_eq_add
        omega
      _ ≤ budget := hbudgetLower
  · intro a ha hlt
    have haeq : a = k + 1 := by omega
    subst a
    rw [B_MCA_rsEval_eq_choose_redundancy_pred
      ev hev k R (by omega) hsize hgate]
    exact hbudgetUpper

/-- The two literal AD2 implications under the manuscript's common
`R >= 2` and field-separation hypotheses. -/
theorem exactFirstAdjacent_AD2
    (ev : D → F) (hev : Function.Injective ev)
    (k R budget : Nat) (hR : 2 ≤ R)
    (hsize : k + R = Fintype.card D)
    (hgate :
      max (Nat.choose (Fintype.card D) (R - 1))
          ((Nat.choose (Fintype.card D) (R - 1)).choose 2) <
        Fintype.card F) :
    (Nat.choose (Fintype.card D) (R - 1) ≤ budget →
      IsFirstSafeMCA (rsEval ev k : Set (D → F))
        k (Fintype.card D) budget (k + 1)) ∧
    (Nat.choose (Fintype.card D) (R - 2) ≤ budget →
      budget < Nat.choose (Fintype.card D) (R - 1) →
      IsFirstSafeMCA (rsEval ev k : Set (D → F))
        k (Fintype.card D) budget (k + 2)) := by
  constructor
  · exact firstAdjacent_isFirstSafeMCA
      ev hev k R budget (by omega) hsize hgate
  · exact secondAdjacent_isFirstSafeMCA
      ev hev k R budget hR hsize hgate

#print axioms isFirstSafeMCA_unique
#print axioms firstAdjacent_isFirstSafeMCA
#print axioms secondAdjacent_isFirstSafeMCA
#print axioms exactFirstAdjacent_AD2

end GrandeFinale.RSFirstAdjacentThreshold
