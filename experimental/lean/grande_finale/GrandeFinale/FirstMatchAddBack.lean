import GrandeFinale.ExactProfileCompiler

/-!
# First-match summation and exact weighted profile add-back

This module formalizes the finite combinatorial and arithmetic content of
`lem:first-match-bound`, `prop:first-match-sum-detail`,
`lem:exact-profile-addback`, and `lem:profile-summation` in
`experimental/asymptotic_rs_mca_frontiers.tex`.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.FirstMatchAddBack

/-! ## Ordered first-match disjointization -/

/-- The part of cell `i` assigned to its least-index occurrence. -/
def firstMatchCell
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α) (i : ι) : Finset α :=
  (E i).filter fun x ↦
    i ∈ idx ∧ ∀ j ∈ idx, x ∈ E j → i ≤ j

@[simp]
theorem mem_firstMatchCell
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α) (i : ι) (x : α) :
    x ∈ firstMatchCell idx E i ↔
      x ∈ E i ∧ i ∈ idx ∧ ∀ j ∈ idx, x ∈ E j → i ≤ j := by
  simp [firstMatchCell]

/-- Distinct ordered cells receive disjoint first-match parts. -/
theorem firstMatchCell_disjoint
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α)
    {i j : ι} (hij : i ≠ j) :
    Disjoint (firstMatchCell idx E i) (firstMatchCell idx E j) := by
  rw [Finset.disjoint_left]
  intro x hxi hxj
  rw [mem_firstMatchCell] at hxi hxj
  exact hij (le_antisymm
    (hxi.2.2 j hxj.2.1 hxj.1)
    (hxj.2.2 i hxi.2.1 hxi.1))

/-- The first-match parts form a pairwise-disjoint family. -/
theorem firstMatchCell_pairwiseDisjoint
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α) :
    (idx : Set ι).PairwiseDisjoint (firstMatchCell idx E) := by
  intro i _ j _ hij
  exact firstMatchCell_disjoint idx E hij

/-- First-match removal preserves the union of the original ordered cells. -/
theorem biUnion_firstMatchCell_eq
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α) :
    idx.biUnion (firstMatchCell idx E) = idx.biUnion E := by
  ext x
  constructor
  · intro hx
    rcases Finset.mem_biUnion.mp hx with ⟨i, hi, hxi⟩
    exact Finset.mem_biUnion.mpr
      ⟨i, hi, (mem_firstMatchCell idx E i x).mp hxi |>.1⟩
  · intro hx
    rcases Finset.mem_biUnion.mp hx with ⟨i₀, hi₀, hxi₀⟩
    let candidates := idx.filter fun i ↦ x ∈ E i
    have hcandidates : candidates.Nonempty :=
      ⟨i₀, by simp [candidates, hi₀, hxi₀]⟩
    let i := candidates.min' hcandidates
    have hiCandidates : i ∈ candidates := by
      exact Finset.min'_mem candidates hcandidates
    have hi : i ∈ idx := (Finset.mem_filter.mp hiCandidates).1
    have hxi : x ∈ E i := (Finset.mem_filter.mp hiCandidates).2
    refine Finset.mem_biUnion.mpr ⟨i, hi, ?_⟩
    rw [mem_firstMatchCell]
    refine ⟨hxi, hi, ?_⟩
    intro j hj hxj
    have hjCandidates : j ∈ candidates := by
      exact Finset.mem_filter.mpr ⟨hj, hxj⟩
    simpa [i] using Finset.min'_le candidates j hjCandidates

/-- The sum of first-match cardinalities is exactly the distinct union size. -/
theorem sum_card_firstMatchCell_eq
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α) :
    ∑ i ∈ idx, (firstMatchCell idx E i).card =
      (idx.biUnion E).card := by
  calc
    ∑ i ∈ idx, (firstMatchCell idx E i).card =
        (idx.biUnion (firstMatchCell idx E)).card :=
      (Finset.card_biUnion (firstMatchCell_pairwiseDisjoint idx E)).symm
    _ = (idx.biUnion E).card := by rw [biUnion_firstMatchCell_eq]

/-- Exact per-line first-match budget summation. -/
theorem firstMatch_union_card_le_sum_budget
    {α ι : Type*} [DecidableEq α] [LinearOrder ι]
    (idx : Finset ι) (E : ι → Finset α) (U : ι → Nat)
    (hU : ∀ i ∈ idx, (firstMatchCell idx E i).card ≤ U i) :
    (idx.biUnion E).card ≤ ∑ i ∈ idx, U i := by
  rw [← sum_card_firstMatchCell_eq idx E]
  exact Finset.sum_le_sum hU

/-! ## Exact finite profile-family and overlap bounds -/

/-- The finite core of subexponential profile summation: family size times a
uniform budget bounds the union. -/
theorem profileUnion_card_le_family_mul_budget
    {α ι : Type*} [DecidableEq α]
    (idx : Finset ι) (E : ι → Finset α) (B : Nat)
    (hE : ∀ i ∈ idx, (E i).card ≤ B) :
    (idx.biUnion E).card ≤ idx.card * B := by
  calc
    (idx.biUnion E).card ≤ ∑ i ∈ idx, (E i).card :=
      Finset.card_biUnion_le
    _ ≤ ∑ _i ∈ idx, B := Finset.sum_le_sum hE
    _ = idx.card * B := by simp

/-- Maximum number of full profile slices containing one support. -/
def overlapMultiplicity
    {α ι : Type*} [DecidableEq α]
    (idx : Finset ι) (slice : ι → Finset α) : Nat :=
  (idx.biUnion slice).sup fun x ↦
    (idx.filter fun i ↦ x ∈ slice i).card

/-- Full profile masses add back with their exact maximum overlap factor. -/
theorem sum_slice_card_le_overlap_mul_union_card
    {α ι : Type*} [DecidableEq α]
    (idx : Finset ι) (slice : ι → Finset α) :
    ∑ i ∈ idx, (slice i).card ≤
      overlapMultiplicity idx slice * (idx.biUnion slice).card := by
  let Ω := idx.biUnion slice
  calc
    ∑ i ∈ idx, (slice i).card =
        ∑ i ∈ idx, (Ω.filter fun x ↦ x ∈ slice i).card := by
      apply Finset.sum_congr rfl
      intro i hi
      have heq : Ω.filter (fun x ↦ x ∈ slice i) = slice i := by
        ext x
        constructor
        · intro hx
          exact (Finset.mem_filter.mp hx).2
        · intro hx
          exact Finset.mem_filter.mpr
            ⟨Finset.mem_biUnion.mpr ⟨i, hi, hx⟩, hx⟩
      rw [heq]
    _ = ∑ x ∈ Ω, (idx.filter fun i ↦ x ∈ slice i).card :=
      ExactProfileCompiler.sum_left_degrees_eq_sum_right_degrees
        idx Ω (fun i x ↦ x ∈ slice i)
    _ ≤ ∑ _x ∈ Ω, overlapMultiplicity idx slice := by
      apply Finset.sum_le_sum
      intro x hx
      exact Finset.le_sup
        (f := fun x ↦ (idx.filter fun i ↦ x ∈ slice i).card) hx
    _ = overlapMultiplicity idx slice * Ω.card := by
      simp [Nat.mul_comm]

/-- A nonempty pairwise-disjoint family has overlap multiplicity exactly one,
as in the partition specialization of AB3. -/
theorem overlapMultiplicity_eq_one_of_pairwiseDisjoint
    {α ι : Type*} [DecidableEq α]
    (idx : Finset ι) (slice : ι → Finset α)
    (hunion : (idx.biUnion slice).Nonempty)
    (hdisj : (idx : Set ι).PairwiseDisjoint slice) :
    overlapMultiplicity idx slice = 1 := by
  apply Nat.le_antisymm
  · unfold overlapMultiplicity
    apply Finset.sup_le
    intro x _hx
    rw [Finset.card_le_one]
    intro i hi j hj
    by_contra hij
    have hd : Disjoint (slice i) (slice j) :=
      hdisj (Finset.mem_filter.mp hi).1
        (Finset.mem_filter.mp hj).1 hij
    exact (Finset.disjoint_left.mp hd)
      (Finset.mem_filter.mp hi).2 (Finset.mem_filter.mp hj).2
  · rcases hunion with ⟨x, hx⟩
    rcases Finset.mem_biUnion.mp hx with ⟨i, hi, hxi⟩
    calc
      1 ≤ (idx.filter fun j ↦ x ∈ slice j).card :=
        Finset.one_le_card.mpr
          ⟨i, Finset.mem_filter.mpr ⟨hi, hxi⟩⟩
      _ ≤ overlapMultiplicity idx slice := by
        exact Finset.le_sup
          (f := fun x ↦ (idx.filter fun j ↦ x ∈ slice j).card) hx

/-! ## Exact weighted profile add-back (AB1--AB3) -/

/-- AB1: nonempty-image profile scales absorb the additive one exactly. -/
theorem weightedProfileAddBack_ab1
    {ι : Type*}
    (idx : Finset ι) (M L : ι → Nat) (U κ : ι → ℝ)
    (hLpos : ∀ i ∈ idx, 0 < L i)
    (hLM : ∀ i ∈ idx, L i ≤ M i)
    (hκ : ∀ i ∈ idx, 0 ≤ κ i)
    (hU : ∀ i ∈ idx,
      U i ≤ κ i * (1 + (M i : ℝ) / L i)) :
    ∑ i ∈ idx, U i ≤
      2 * ∑ i ∈ idx, κ i * (M i : ℝ) / L i := by
  calc
    ∑ i ∈ idx, U i ≤
        ∑ i ∈ idx, κ i * (1 + (M i : ℝ) / L i) :=
      Finset.sum_le_sum hU
    _ ≤ ∑ i ∈ idx, 2 * (κ i * (M i : ℝ) / L i) := by
      apply Finset.sum_le_sum
      intro i hi
      have hLreal : (0 : ℝ) < L i := by exact_mod_cast hLpos i hi
      have hLMreal : (L i : ℝ) ≤ M i := by exact_mod_cast hLM i hi
      have hratio : (1 : ℝ) ≤ (M i : ℝ) / L i :=
        (le_div_iff₀ hLreal).2 (by simpa using hLMreal)
      calc
        κ i * (1 + (M i : ℝ) / L i) ≤
            κ i * ((M i : ℝ) / L i + (M i : ℝ) / L i) :=
          mul_le_mul_of_nonneg_left
            (by
              simpa [add_comm] using
                add_le_add_right hratio ((M i : ℝ) / L i))
            (hκ i hi)
        _ = 2 * (κ i * (M i : ℝ) / L i) := by ring
    _ = 2 * ∑ i ∈ idx, κ i * (M i : ℝ) / L i := by
      rw [Finset.mul_sum]

/-- AB2: rewrite each image denominator using the common target size and its
exact coverage factor. -/
theorem weightedProfileAddBack_ab2
    {ι : Type*}
    (idx : Finset ι) (M L : ι → Nat) (U κ : ι → ℝ) (A : Nat)
    (hA : 0 < A)
    (hLpos : ∀ i ∈ idx, 0 < L i)
    (hLM : ∀ i ∈ idx, L i ≤ M i)
    (hκ : ∀ i ∈ idx, 0 ≤ κ i)
    (hU : ∀ i ∈ idx,
      U i ≤ κ i * (1 + (M i : ℝ) / L i)) :
    ∑ i ∈ idx, U i ≤
      (2 / (A : ℝ)) *
        ∑ i ∈ idx,
          κ i * ((A : ℝ) / L i) * (M i : ℝ) := by
  have hab1 := weightedProfileAddBack_ab1 idx M L U κ hLpos hLM hκ hU
  have hAreal : (0 : ℝ) < A := by exact_mod_cast hA
  have hsum :
      (∑ i ∈ idx, κ i * (M i : ℝ) / L i) =
        (1 / (A : ℝ)) *
          ∑ i ∈ idx, κ i * ((A : ℝ) / L i) * (M i : ℝ) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    have hLreal : (0 : ℝ) < L i := by exact_mod_cast hLpos i hi
    field_simp [ne_of_gt hAreal, ne_of_gt hLreal]
  calc
    ∑ i ∈ idx, U i ≤
        2 * ∑ i ∈ idx, κ i * (M i : ℝ) / L i := hab1
    _ = (2 / (A : ℝ)) *
        ∑ i ∈ idx, κ i * ((A : ℝ) / L i) * (M i : ℝ) := by
      rw [hsum]
      ring

/-- AB3: uniform payment and coverage factors combine with the exact
full-slice overlap multiplicity. -/
theorem weightedProfileAddBack_ab3
    {α ι : Type*} [DecidableEq α]
    (idx : Finset ι) (slice : ι → Finset α) (L : ι → Nat)
    (U κCell : ι → ℝ) (A : Nat) (κ η : ℝ)
    (hA : 0 < A)
    (hLpos : ∀ i ∈ idx, 0 < L i)
    (hLM : ∀ i ∈ idx, L i ≤ (slice i).card)
    (hκCell : ∀ i ∈ idx, 0 ≤ κCell i)
    (hU : ∀ i ∈ idx,
      U i ≤ κCell i * (1 + ((slice i).card : ℝ) / L i))
    (hκ : 0 ≤ κ) (hη : 0 ≤ η)
    (hκBound : ∀ i ∈ idx, κCell i ≤ κ)
    (hηBound : ∀ i ∈ idx, (A : ℝ) / L i ≤ η) :
    ∑ i ∈ idx, U i ≤
      (2 * κ * η * (overlapMultiplicity idx slice : ℝ) *
        ((idx.biUnion slice).card : ℝ)) / A := by
  have hab2 := weightedProfileAddBack_ab2
    idx (fun i ↦ (slice i).card) L U κCell A
    hA hLpos hLM hκCell hU
  have hweighted :
      (∑ i ∈ idx,
        κCell i * ((A : ℝ) / L i) * ((slice i).card : ℝ)) ≤
        κ * η * (overlapMultiplicity idx slice : ℝ) *
          ((idx.biUnion slice).card : ℝ) := by
    calc
      (∑ i ∈ idx,
          κCell i * ((A : ℝ) / L i) * ((slice i).card : ℝ)) ≤
          ∑ i ∈ idx, κ * η * ((slice i).card : ℝ) := by
        apply Finset.sum_le_sum
        intro i hi
        have hcoverage : 0 ≤ (A : ℝ) / L i :=
          div_nonneg (Nat.cast_nonneg A) (Nat.cast_nonneg (L i))
        have hfactor :
            κCell i * ((A : ℝ) / L i) ≤ κ * η :=
          mul_le_mul (hκBound i hi) (hηBound i hi) hcoverage hκ
        exact mul_le_mul_of_nonneg_right hfactor (Nat.cast_nonneg _)
      _ = κ * η * ∑ i ∈ idx, ((slice i).card : ℝ) := by
        rw [Finset.mul_sum]
      _ ≤ κ * η *
          ((overlapMultiplicity idx slice : ℝ) *
            ((idx.biUnion slice).card : ℝ)) := by
        apply mul_le_mul_of_nonneg_left
        · exact_mod_cast sum_slice_card_le_overlap_mul_union_card idx slice
        · exact mul_nonneg hκ hη
      _ = κ * η * (overlapMultiplicity idx slice : ℝ) *
          ((idx.biUnion slice).card : ℝ) := by ring
  calc
    ∑ i ∈ idx, U i ≤
        (2 / (A : ℝ)) *
          ∑ i ∈ idx,
            κCell i * ((A : ℝ) / L i) * ((slice i).card : ℝ) := hab2
    _ ≤ (2 / (A : ℝ)) *
        (κ * η * (overlapMultiplicity idx slice : ℝ) *
          ((idx.biUnion slice).card : ℝ)) := by
      exact mul_le_mul_of_nonneg_left hweighted (by positivity)
    _ = (2 * κ * η * (overlapMultiplicity idx slice : ℝ) *
          ((idx.biUnion slice).card : ℝ)) / A := by ring

#print axioms sum_card_firstMatchCell_eq
#print axioms firstMatch_union_card_le_sum_budget
#print axioms profileUnion_card_le_family_mul_budget
#print axioms sum_slice_card_le_overlap_mul_union_card
#print axioms overlapMultiplicity_eq_one_of_pairwiseDisjoint
#print axioms weightedProfileAddBack_ab1
#print axioms weightedProfileAddBack_ab2
#print axioms weightedProfileAddBack_ab3

end GrandeFinale.FirstMatchAddBack
