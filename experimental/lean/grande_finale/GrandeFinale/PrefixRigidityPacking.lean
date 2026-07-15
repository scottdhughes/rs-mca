import GrandeFinale.BC
import GrandeFinale.PrefixPigeonhole

/-!
# Prefix rigidity and the exact Johnson packing cap

This module formalizes the finite part of `prop:prefix-rigidity-full` from
`experimental/asymptotic_rs_mca_frontiers.tex`.  It constructs Johnson spheres
and balls on a uniform finite-set slice, proves their exact binomial volume,
uses locator-prefix rigidity to separate the balls around one coefficient
fiber, and derives both the product and natural-division forms of the packing
cap in equation (4.4).
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.PrefixRigidityPacking

/-! ## Exact Johnson spheres and balls -/

variable {α : Type*} [DecidableEq α]

/-- The Johnson sphere of radius `i` about `M` inside the uniform slice of
subsets of `D` having cardinality `M.card`. -/
def johnsonSphere (D M : Finset α) (i : Nat) : Finset (Finset α) :=
  (D.powersetCard M.card).filter fun S ↦ (M \ S).card = i

/-- The closed Johnson ball of radius `t` about `M` inside the same uniform
slice. -/
def johnsonBall (D M : Finset α) (t : Nat) : Finset (Finset α) :=
  (D.powersetCard M.card).filter fun S ↦ (M \ S).card ≤ t

theorem mem_johnsonSphere {D M S : Finset α} {i : Nat} :
    S ∈ johnsonSphere D M i ↔
      S ⊆ D ∧ S.card = M.card ∧ (M \ S).card = i := by
  simp [johnsonSphere, and_assoc]

theorem mem_johnsonBall {D M S : Finset α} {t : Nat} :
    S ∈ johnsonBall D M t ↔
      S ⊆ D ∧ S.card = M.card ∧ (M \ S).card ≤ t := by
  simp [johnsonBall, and_assoc]

/-- Delete `A` from `M` and insert the disjoint set `B`. -/
def johnsonMove (M A B : Finset α) : Finset α :=
  (M \ A) ∪ B

private theorem center_sdiff_johnsonMove
    {M A B : Finset α} (hAM : A ⊆ M) (hBM : Disjoint B M) :
    M \ johnsonMove M A B = A := by
  ext x
  simp only [johnsonMove, Finset.mem_sdiff, Finset.mem_union]
  constructor
  · rintro ⟨hxM, hnot⟩
    by_contra hxA
    exact hnot (Or.inl ⟨hxM, hxA⟩)
  · intro hxA
    have hxM := hAM hxA
    refine ⟨hxM, ?_⟩
    rintro (hxMA | hxB)
    · exact hxMA.2 hxA
    · exact (Finset.disjoint_left.mp hBM hxB hxM)

private theorem johnsonMove_sdiff_center
    {M A B : Finset α} (hBM : Disjoint B M) :
    johnsonMove M A B \ M = B := by
  ext x
  simp only [johnsonMove, Finset.mem_sdiff, Finset.mem_union]
  constructor
  · rintro ⟨hxMA | hxB, hxnotM⟩
    · exact (hxnotM hxMA.1).elim
    · exact hxB
  · intro hxB
    refine ⟨Or.inr hxB, ?_⟩
    exact fun hxM ↦ Finset.disjoint_left.mp hBM hxB hxM

private theorem johnsonMove_mem_sphere
    {D M A B : Finset α} {i : Nat} (hMD : M ⊆ D)
    (hA : A ∈ M.powersetCard i) (hB : B ∈ (D \ M).powersetCard i) :
    johnsonMove M A B ∈ johnsonSphere D M i := by
  obtain ⟨hAM, hAcard⟩ := Finset.mem_powersetCard.mp hA
  obtain ⟨hBDM, hBcard⟩ := Finset.mem_powersetCard.mp hB
  have hBM : Disjoint B M := Finset.disjoint_left.mpr fun x hxB hxM ↦
    (Finset.mem_sdiff.mp (hBDM hxB)).2 hxM
  apply mem_johnsonSphere.mpr
  refine ⟨Finset.union_subset (Finset.sdiff_subset.trans hMD)
    (hBDM.trans Finset.sdiff_subset), ?_, ?_⟩
  · rw [johnsonMove, Finset.card_union_of_disjoint]
    · rw [Finset.card_sdiff_of_subset hAM, hAcard, hBcard]
      have hi : i ≤ M.card := hAcard ▸ Finset.card_le_card hAM
      omega
    · exact Finset.disjoint_left.mpr fun x hxMA hxB ↦
        Finset.disjoint_left.mp hBM hxB (Finset.mem_sdiff.mp hxMA).1
  · rw [center_sdiff_johnsonMove hAM hBM, hAcard]

private theorem deleted_mem_powersetCard_of_mem_sphere
    {D M S : Finset α} {i : Nat} (hS : S ∈ johnsonSphere D M i) :
    M \ S ∈ M.powersetCard i := by
  exact Finset.mem_powersetCard.mpr
    ⟨Finset.sdiff_subset, (mem_johnsonSphere.mp hS).2.2⟩

private theorem inserted_mem_powersetCard_of_mem_sphere
    {D M S : Finset α} {i : Nat} (hS : S ∈ johnsonSphere D M i) :
    S \ M ∈ (D \ M).powersetCard i := by
  have hs := mem_johnsonSphere.mp hS
  apply Finset.mem_powersetCard.mpr
  refine ⟨?_, ?_⟩
  · intro x hx
    have hx' := Finset.mem_sdiff.mp hx
    exact Finset.mem_sdiff.mpr ⟨hs.1 hx'.1, hx'.2⟩
  · exact (Finset.card_sdiff_comm hs.2.1).trans hs.2.2

/-- A Johnson sphere is in bijection with a choice of `i` deleted center
points and `i` inserted complement points. -/
def johnsonSphereEquiv (D M : Finset α) (i : Nat) (hMD : M ⊆ D) :
    (↑(M.powersetCard i) × ↑((D \ M).powersetCard i)) ≃
      ↑(johnsonSphere D M i) where
  toFun p := ⟨johnsonMove M p.1 p.2,
    johnsonMove_mem_sphere hMD p.1.property p.2.property⟩
  invFun S :=
    ⟨⟨M \ S, deleted_mem_powersetCard_of_mem_sphere S.property⟩,
      ⟨S \ M, inserted_mem_powersetCard_of_mem_sphere S.property⟩⟩
  left_inv p := by
    have hAM := (Finset.mem_powersetCard.mp p.1.property).1
    have hBDM := (Finset.mem_powersetCard.mp p.2.property).1
    have hBM : Disjoint (p.2 : Finset α) M :=
      Finset.disjoint_left.mpr fun x hxB hxM ↦
        (Finset.mem_sdiff.mp (hBDM hxB)).2 hxM
    apply Prod.ext
    · apply Subtype.ext
      exact center_sdiff_johnsonMove hAM hBM
    · apply Subtype.ext
      exact johnsonMove_sdiff_center hBM
  right_inv S := by
    apply Subtype.ext
    ext x
    simp only [johnsonMove, Finset.mem_union, Finset.mem_sdiff]
    tauto

/-- Exact cardinality of a Johnson sphere. -/
theorem johnsonSphere_card (D M : Finset α) (i : Nat) (hMD : M ⊆ D) :
    (johnsonSphere D M i).card =
      M.card.choose i * (D.card - M.card).choose i := by
  have hcard := Fintype.card_congr (johnsonSphereEquiv D M i hMD)
  simpa [Finset.card_powersetCard, Finset.card_sdiff_of_subset hMD] using
    hcard.symm

theorem johnsonBall_eq_biUnion_spheres (D M : Finset α) (t : Nat) :
    johnsonBall D M t =
      (Finset.range (t + 1)).biUnion fun i ↦ johnsonSphere D M i := by
  ext S
  constructor
  · intro hS
    have hs := mem_johnsonBall.mp hS
    apply Finset.mem_biUnion.mpr
    exact ⟨(M \ S).card, Finset.mem_range.mpr (by omega),
      mem_johnsonSphere.mpr ⟨hs.1, hs.2.1, rfl⟩⟩
  · intro hS
    obtain ⟨i, hi, hSi⟩ := Finset.mem_biUnion.mp hS
    have hs := mem_johnsonSphere.mp hSi
    apply mem_johnsonBall.mpr
    exact ⟨hs.1, hs.2.1, by
      have := Finset.mem_range.mp hi
      omega⟩

private theorem pairwiseDisjoint_johnsonSpheres (D M : Finset α) (t : Nat) :
    ((Finset.range (t + 1) : Finset Nat) : Set Nat).PairwiseDisjoint
      (johnsonSphere D M) := by
  intro i _hi j _hj hij
  apply Finset.disjoint_left.mpr
  intro S hSi hSj
  have hi := (mem_johnsonSphere.mp hSi).2.2
  have hj := (mem_johnsonSphere.mp hSj).2.2
  exact hij (hi.symm.trans hj)

/-- Exact cardinality of a closed Johnson ball. -/
theorem johnsonBall_card (D M : Finset α) (t : Nat) (hMD : M ⊆ D) :
    (johnsonBall D M t).card =
      ∑ i ∈ Finset.range (t + 1),
        M.card.choose i * (D.card - M.card).choose i := by
  rw [johnsonBall_eq_biUnion_spheres,
    Finset.card_biUnion (pairwiseDisjoint_johnsonSpheres D M t)]
  exact Finset.sum_congr rfl fun i _hi ↦ johnsonSphere_card D M i hMD

theorem johnsonBall_subset_powersetCard
    (D M : Finset α) (t : Nat) :
    johnsonBall D M t ⊆ D.powersetCard M.card := by
  intro S hS
  have hs := mem_johnsonBall.mp hS
  exact Finset.mem_powersetCard.mpr ⟨hs.1, hs.2.1⟩

/-- If the center distance is larger than twice the radius, the two closed
Johnson balls are disjoint. -/
theorem disjoint_johnsonBall_of_two_mul_lt
    (D M N : Finset α) (t : Nat) (hfar : 2 * t < (M \ N).card) :
    Disjoint (johnsonBall D M t) (johnsonBall D N t) := by
  apply Finset.disjoint_left.mpr
  intro S hSM hSN
  have hsM := mem_johnsonBall.mp hSM
  have hsN := mem_johnsonBall.mp hSN
  have hreverse : (S \ N).card = (N \ S).card :=
    Finset.card_sdiff_comm hsN.2.1
  have hsub : M \ N ⊆ (M \ S) ∪ (S \ N) := by
    intro x hx
    have hx' := Finset.mem_sdiff.mp hx
    by_cases hxS : x ∈ S
    · exact Finset.mem_union_right _ (Finset.mem_sdiff.mpr ⟨hxS, hx'.2⟩)
    · exact Finset.mem_union_left _ (Finset.mem_sdiff.mpr ⟨hx'.1, hxS⟩)
  have hcard := (Finset.card_le_card hsub).trans (Finset.card_union_le _ _)
  omega

/-- Pairwise center separation gives pairwise disjoint Johnson balls. -/
theorem pairwiseDisjoint_johnsonBall
    (D : Finset α) (Fib : Finset (Finset α)) (t : Nat)
    (hfar : ∀ M ∈ Fib, ∀ N ∈ Fib, M ≠ N → 2 * t < (M \ N).card) :
    (Fib : Set (Finset α)).PairwiseDisjoint fun M ↦ johnsonBall D M t := by
  intro M hM N hN hMN
  exact disjoint_johnsonBall_of_two_mul_lt D M N t
    (hfar M hM N hN hMN)

/-- The Johnson ball volume is positive because its radius-zero sphere is the
center alone. -/
theorem johnsonVolume_pos (n m t : Nat) :
    0 < ∑ i ∈ Finset.range (t + 1),
      m.choose i * (n - m).choose i := by
  have hzero : 0 ∈ Finset.range (t + 1) := by simp
  have hle := Finset.single_le_sum
    (s := Finset.range (t + 1))
    (f := fun i ↦ m.choose i * (n - m).choose i)
    (fun _ _ ↦ Nat.zero_le _) hzero
  simpa using hle

/-! ## Locator-prefix rigidity and packing -/

variable {B : Type*} [Field B]

theorem mem_coefficientFiber_data
    (D : Finset B) (K m : Nat) (z : Fin (m - K) → B) (S : Finset B) :
    S ∈ PrefixPigeonhole.coefficientFiber D K m z ↔
      S ⊆ D ∧ S.card = m ∧
        PrefixPigeonhole.coefficientPrefix K m (SP.locator S) = z := by
  simp [PrefixPigeonhole.coefficientFiber, and_assoc]

/-- Two distinct members of one coefficient fiber have Johnson distance at
least its depth plus one. -/
theorem coefficientFiber_johnsonDistance
    (D : Finset B) {K m : Nat} (hKm : K ≤ m)
    (z : Fin (m - K) → B) {S T : Finset B}
    (hS : S ∈ PrefixPigeonhole.coefficientFiber D K m z)
    (hT : T ∈ PrefixPigeonhole.coefficientFiber D K m z)
    (hne : S ≠ T) :
    m - K + 1 ≤ (S \ T).card := by
  have hs := (mem_coefficientFiber_data D K m z S).mp hS
  have ht := (mem_coefficientFiber_data D K m z T).mp hT
  have hlocS : (SP.locator S).IsMonicOfDegree m :=
    ⟨(SP.locator_natDegree S).trans hs.2.1, SP.locator_monic S⟩
  have hprefix :
      PrefixPigeonhole.coefficientPrefix K m (SP.locator S) =
        PrefixPigeonhole.coefficientPrefix K m (SP.locator T) :=
    hs.2.2.trans ht.2.2.symm
  have hdegree :=
    (PrefixPigeonhole.coefficientPrefix_eq_iff_degree_sub_lt
      hlocS ht.2.1).mp hprefix
  have hpoly : SP.locator S - SP.locator T ≠ 0 := by
    intro hzero
    apply hne
    apply SP.locator_injective
    exact sub_eq_zero.mp hzero
  have hnat : (SP.locator S - SP.locator T).natDegree < K :=
    (Polynomial.natDegree_lt_iff_degree_lt hpoly).mpr hdegree
  apply SP.prefix_rigidity m (m - K) S T hs.2.1 hne
  omega

/-- Radius `floor((m-K)/2)` Johnson balls around one coefficient fiber are
pairwise disjoint. -/
theorem coefficientFiber_johnsonBalls_pairwiseDisjoint
    (D : Finset B) {K m : Nat} (hKm : K ≤ m)
    (z : Fin (m - K) → B) :
    (PrefixPigeonhole.coefficientFiber D K m z : Set (Finset B)).PairwiseDisjoint
      fun S ↦ johnsonBall D S ((m - K) / 2) := by
  apply pairwiseDisjoint_johnsonBall
  intro S hS T hT hne
  have hrig := coefficientFiber_johnsonDistance D hKm z hS hT hne
  omega

/-- Multiplication form of the exact Johnson packing cap in equation (4.4). -/
theorem coefficientFiber_mul_johnsonVolume_le
    (D : Finset B) {K m : Nat} (hKm : K ≤ m)
    (z : Fin (m - K) → B) :
    (PrefixPigeonhole.coefficientFiber D K m z).card *
        (∑ i ∈ Finset.range ((m - K) / 2 + 1),
          m.choose i * (D.card - m).choose i) ≤
      D.card.choose m := by
  let Fib := PrefixPigeonhole.coefficientFiber D K m z
  let t := (m - K) / 2
  let V := ∑ i ∈ Finset.range (t + 1),
    m.choose i * (D.card - m).choose i
  have hpack : Fib.card * V ≤ (D.powersetCard m).card := by
    apply BC.johnson_packing Fib V (D.powersetCard m)
      (fun S ↦ johnsonBall D S t)
    · intro S hS
      have hs := (mem_coefficientFiber_data D K m z S).mp hS
      simpa [hs.2.1] using johnsonBall_subset_powersetCard D S t
    · intro S hS
      have hs := (mem_coefficientFiber_data D K m z S).mp hS
      simpa [V, hs.2.1] using johnsonBall_card D S t hs.1
    · exact coefficientFiber_johnsonBalls_pairwiseDisjoint D hKm z
  simpa [Fib, t, V, Finset.card_powersetCard] using hpack

/-- Displayed natural-division form of the exact Johnson packing cap. -/
theorem coefficientFiber_card_le_div_johnsonVolume
    (D : Finset B) {K m : Nat} (hKm : K ≤ m)
    (z : Fin (m - K) → B) :
    (PrefixPigeonhole.coefficientFiber D K m z).card ≤
      D.card.choose m /
        (∑ i ∈ Finset.range ((m - K) / 2 + 1),
          m.choose i * (D.card - m).choose i) := by
  apply (Nat.le_div_iff_mul_le
    (johnsonVolume_pos D.card m ((m - K) / 2))).mpr
  exact coefficientFiber_mul_johnsonVolume_le D hKm z

#print axioms johnsonSphere_card
#print axioms johnsonBall_card
#print axioms coefficientFiber_johnsonDistance
#print axioms coefficientFiber_mul_johnsonVolume_le
#print axioms coefficientFiber_card_le_div_johnsonVolume

end GrandeFinale.PrefixRigidityPacking
