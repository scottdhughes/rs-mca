import GrandeFinale.LargestFiberMoment

/-!
# Exact finite profile compiler

This module formalizes the finite incidence, moment-payment, and first-match
arithmetic in `thm:exact-finite-profile-compiler` of
`experimental/asymptotic_rs_mca_frontiers.tex`.
-/

open scoped BigOperators

noncomputable section

namespace GrandeFinale.ExactProfileCompiler

open GrandeFinale.LargestFiberMoment

/-! ## Finite incidence double counting -/

/-- Counting a finite bipartite incidence relation by either coordinate gives
the same total. -/
theorem sum_left_degrees_eq_sum_right_degrees
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (Z : Finset α) (P : Finset β) (I : α → β → Prop)
    [DecidableRel I] :
    ∑ z ∈ Z, (P.filter fun p ↦ I z p).card =
      ∑ p ∈ P, (Z.filter fun z ↦ I z p).card := by
  simp_rw [Finset.card_eq_sum_ones, Finset.sum_filter]
  rw [Finset.sum_comm]

/-- If every left vertex has degree at least `H` and every right vertex has
degree at most `J`, then `H * |Z| <= J * |P|`. -/
theorem incidence_double_count
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (Z : Finset α) (P : Finset β) (I : α → β → Prop)
    [DecidableRel I] (H J : Nat)
    (hleft : ∀ z ∈ Z, H ≤ (P.filter fun p ↦ I z p).card)
    (hright : ∀ p ∈ P, (Z.filter fun z ↦ I z p).card ≤ J) :
    H * Z.card ≤ J * P.card := by
  calc
    H * Z.card = ∑ _z ∈ Z, H := by simp [Nat.mul_comm]
    _ ≤ ∑ z ∈ Z, (P.filter fun p ↦ I z p).card :=
      Finset.sum_le_sum hleft
    _ = ∑ p ∈ P, (Z.filter fun z ↦ I z p).card :=
      sum_left_degrees_eq_sum_right_degrees Z P I
    _ ≤ ∑ _p ∈ P, J := Finset.sum_le_sum hright
    _ = J * P.card := by simp [Nat.mul_comm]

/-! ## Exact moment root and primitive-cell payment (FC1) -/

/-- The residual moment normalized by the full support-slice mean. Residual
counts need not sum to the mean times the residual support size. -/
def residualMoment {σ : Type*}
    (S : Finset σ) (Q : σ → Nat) (barN : ℝ) (q : Nat) : ℝ :=
  (∑ s ∈ S, ((Q s : ℝ) / barN) ^ q) / S.card

/-- A residual moment normalized by a positive full-slice mean controls every
residual fiber by the corresponding exact moment root. -/
theorem fiber_le_barN_mul_momentRoot
    {σ : Type*} {S : Finset σ} {Q : σ → Nat}
    (barN : ℝ) (hbarN : 0 < barN)
    (q : Nat) (hq : 1 ≤ q) {s : σ} (hs : s ∈ S) :
    (Q s : ℝ) ≤
      barN *
        ((S.card : ℝ) * residualMoment S Q barN q) ^
          ((q : ℝ)⁻¹) := by
  have hS : S.Nonempty := ⟨s, hs⟩
  have hflat := QFourierTao.q_flatness_from_collision
    S (fun t ↦ (Q t : ℝ))
    (fun _ _ ↦ Nat.cast_nonneg _)
    barN hbarN
    (S.card : ℝ) (by exact_mod_cast hS.card_pos)
    q hq (residualMoment S Q barN q)
    (by
      simp [residualMoment, QFourierTao.collisionMoment,
        div_eq_inv_mul])
    hs
  simpa [mul_comm] using hflat

/-- The support-pair identity and the largest-fiber bound give
`|P| <= W * max Q`. -/
theorem pairCount_le_total_mul_max
    {σ : Type*} {S : Finset σ} (Q : σ → Nat)
    {smax : σ}
    (hmax : ∀ s ∈ S, Q s ≤ Q smax)
    (W pairCount : Nat)
    (hsum : ∑ s ∈ S, Q s = W)
    (hpairs : pairCount = ∑ s ∈ S, Q s ^ 2) :
    pairCount ≤ W * Q smax := by
  rw [hpairs]
  calc
    ∑ s ∈ S, Q s ^ 2 ≤ ∑ s ∈ S, Q smax * Q s := by
      apply Finset.sum_le_sum
      intro s hs
      simpa [pow_two, Nat.mul_comm] using
        Nat.mul_le_mul_right (Q s) (hmax s hs)
    _ = Q smax * ∑ s ∈ S, Q s := by rw [Finset.mul_sum]
    _ = W * Q smax := by rw [hsum, Nat.mul_comm]

/-- Exact primitive-cell budget (FC1). The displayed natural floor is literal:
no asymptotic or polynomial loss is introduced. -/
theorem primitiveCell_slope_card_le_floor
    {α β σ : Type*}
    [DecidableEq α] [DecidableEq β]
    (Z : Finset α) (P : Finset β) (I : α → β → Prop)
    [DecidableRel I]
    (S : Finset σ) (Q : σ → Nat) {smax : σ}
    (hsmax : smax ∈ S) (hmax : ∀ s ∈ S, Q s ≤ Q smax)
    (W H J q : Nat) (barN : ℝ)
    (hbarN : 0 < barN) (hH : 0 < H) (hq : 2 ≤ q)
    (hsum : ∑ s ∈ S, Q s = W)
    (hpairs : P.card = ∑ s ∈ S, Q s ^ 2)
    (hleft : ∀ z ∈ Z, H ≤ (P.filter fun p ↦ I z p).card)
    (hright : ∀ p ∈ P, (Z.filter fun z ↦ I z p).card ≤ J) :
    Z.card ≤
      ⌊(((J : ℝ) * W) / H) *
          barN *
          ((S.card : ℝ) *
            residualMoment S Q barN q) ^
              ((q : ℝ)⁻¹)⌋₊ := by
  have hpairMax : P.card ≤ W * Q smax :=
    pairCount_le_total_mul_max Q hmax W P.card hsum hpairs
  have hincidence : H * Z.card ≤ J * P.card :=
    incidence_double_count Z P I H J hleft hright
  have hnat : H * Z.card ≤ J * (W * Q smax) :=
    hincidence.trans (Nat.mul_le_mul_left J hpairMax)
  have hreal :
      (H : ℝ) * Z.card ≤ (J : ℝ) * ((W : ℝ) * Q smax) := by
    exact_mod_cast hnat
  let root : ℝ :=
    ((S.card : ℝ) *
      residualMoment S Q barN q) ^ ((q : ℝ)⁻¹)
  have hQmax :
      (Q smax : ℝ) ≤ barN * root := by
    exact fiber_le_barN_mul_momentRoot barN hbarN q (by omega) hsmax
  have hmul :
      (H : ℝ) * Z.card ≤
        (J : ℝ) * W *
          (barN * root) := by
    have := hreal.trans
      (mul_le_mul_of_nonneg_left
        (mul_le_mul_of_nonneg_left hQmax (Nat.cast_nonneg W))
        (Nat.cast_nonneg J))
    simpa [mul_assoc] using this
  have hbound :
      (Z.card : ℝ) ≤
        (((J : ℝ) * W) / H) *
          barN * root := by
    calc
      (Z.card : ℝ) ≤
          ((J : ℝ) * W *
            (barN * root)) / H :=
        (le_div_iff₀ (by exact_mod_cast hH)).2 (by
          simpa [mul_assoc, mul_comm, mul_left_comm] using hmul)
      _ = (((J : ℝ) * W) / H) *
          barN * root := by ring
  have hmomentNonneg :
      0 ≤ residualMoment S Q barN q := by
    unfold residualMoment
    positivity
  have hrootNonneg : 0 ≤ root := by
    exact Real.rpow_nonneg
      (mul_nonneg (Nat.cast_nonneg S.card) hmomentNonneg) _
  apply (Nat.le_floor_iff (by
    exact mul_nonneg
      (mul_nonneg (div_nonneg
        (mul_nonneg (Nat.cast_nonneg J) (Nat.cast_nonneg W))
        (Nat.cast_nonneg H)) hbarN.le) hrootNonneg)).2
  exact hbound

/-! ## Available primitive budgets and first-match summation (FC2) -/

/-- A primitive cell may carry a moment budget, a direct slope budget, or both.
When both are present the paid budget is their minimum. -/
def mergedBudget : Option Nat → Option Nat → Nat
  | some u, some d => min u d
  | some u, none => u
  | none, some d => d
  | none, none => 0

/-- Certified budget alternatives for one primitive first-match cell. -/
structure PrimitiveCellBudget where
  actual : Nat
  moment : Option Nat
  direct : Option Nat
  available : moment.isSome ∨ direct.isSome
  momentSound : ∀ u, moment = some u → actual ≤ u
  directSound : ∀ d, direct = some d → actual ≤ d

/-- The available budget, or the minimum when both alternatives are certified,
bounds the actual primitive first-match cell. -/
theorem PrimitiveCellBudget.actual_le_merged (c : PrimitiveCellBudget) :
    c.actual ≤ mergedBudget c.moment c.direct := by
  cases hm : c.moment with
  | none =>
      cases hd : c.direct with
      | none =>
          have hav := c.available
          simp [hm, hd] at hav
      | some d =>
          simpa [mergedBudget, hm, hd] using c.directSound d hd
  | some u =>
      cases hd : c.direct with
      | none =>
          simpa [mergedBudget, hm, hd] using c.momentSound u hm
      | some d =>
          simp only [mergedBudget]
          exact le_min (c.momentSound u hm) (c.directSound d hd)

/-- Per-line FC2: a closed first-match ledger plus exact algebraic and primitive
cell budgets bounds the bad-slope count by their printed sum. -/
theorem profileCompiler_line_bound
    {ι τ : Type*}
    (A : Finset ι) (P : Finset τ)
    (algebraicActual algebraicBudget : ι → Nat)
    (primitive : τ → PrimitiveCellBudget)
    (badCount : Nat)
    (hledger :
      badCount ≤
        (∑ i ∈ A, algebraicActual i) +
          ∑ l ∈ P, (primitive l).actual)
    (halgebraic :
      ∀ i ∈ A, algebraicActual i ≤ algebraicBudget i) :
    badCount ≤
      (∑ i ∈ A, algebraicBudget i) +
        ∑ l ∈ P, mergedBudget (primitive l).moment (primitive l).direct := by
  refine hledger.trans (Nat.add_le_add (Finset.sum_le_sum halgebraic) ?_)
  exact Finset.sum_le_sum fun l _ ↦ (primitive l).actual_le_merged

/-- Maximizing the per-line FC2 estimate preserves the exact compiler bound. -/
theorem profileCompiler_max_bound
    {ρ : Type*} (lines : Finset ρ)
    (bad lineBudget : ρ → Nat)
    (hline : ∀ r ∈ lines, bad r ≤ lineBudget r) :
    lines.sup bad ≤ lines.sup lineBudget := by
  apply Finset.sup_le
  intro r hr
  exact (hline r hr).trans (Finset.le_sup hr)

#print axioms incidence_double_count
#print axioms primitiveCell_slope_card_le_floor
#print axioms PrimitiveCellBudget.actual_le_merged
#print axioms profileCompiler_line_bound
#print axioms profileCompiler_max_bound

end GrandeFinale.ExactProfileCompiler
