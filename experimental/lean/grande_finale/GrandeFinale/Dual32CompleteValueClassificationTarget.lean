import Mathlib

/-!
# Statement target: complete classification of deployed 32-valued phases

This file states the complete classification matching the accompanying note and
exact certificate. The affine-monomial converse is Lean-certified below; the
forward rigidity implication remains the explicit statement target. This file
is not imported by `GrandeFinale.lean`.
-/

namespace GrandeFinale

open Polynomial

private abbrev Dual32Field := ZMod 2130706433

private instance : Fact (Nat.Prime 2130706433) := ⟨by native_decide⟩

private def dual32Domain : Finset Dual32Field :=
  Finset.univ.filter (fun x => x ^ (2097152 : Nat) = 1)

private noncomputable def dual32DomainEquivRoots :
    {x // x ∈ dual32Domain} ≃ rootsOfUnity 2097152 Dual32Field where
  toFun x := ⟨Units.mk0 x.1 (by
      intro hx
      have hxpow := (Finset.mem_filter.mp x.2).2
      rw [hx, zero_pow (by norm_num : (2097152 : Nat) ≠ 0)] at hxpow
      exact zero_ne_one hxpow), by
    ext
    exact (Finset.mem_filter.mp x.2).2⟩
  invFun x := ⟨x.1.1, by
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _, ?_⟩
    change x.1.1 ^ (2097152 : Nat) = 1
    simpa only [Units.val_pow_eq_pow_val, Units.val_one] using congrArg Units.val x.2⟩
  left_inv x := by ext; rfl
  right_inv x := by ext; rfl

private theorem dual32_power_image_card :
    (dual32Domain.image fun x => x ^ (65536 : Nat)).card = 32 := by
  let G := rootsOfUnity 2097152 Dual32Field
  haveI : NeZero (2130706433 - 1) := ⟨by norm_num⟩
  haveI : HasEnoughRootsOfUnity Dual32Field 2097152 :=
    HasEnoughRootsOfUnity.of_dvd Dual32Field (by norm_num : 2097152 ∣ 2130706433 - 1)
  have hGcard : Nat.card G = 2097152 :=
    HasEnoughRootsOfUnity.natCard_rootsOfUnity Dual32Field 2097152
  have hrange : Nat.card (powMonoidHom 65536 : G →* G).range = 32 := by
    rw [IsCyclic.card_powMonoidHom_range, hGcard]
    norm_num
  let e := dual32DomainEquivRoots
  let j : G → Dual32Field := fun x => x.1.1
  have hj : Function.Injective j := fun _ _ h => by ext; exact h
  let p : G → G := fun x => x ^ (65536 : Nat)
  have hcardp : (Finset.univ.image p).card = 32 := by
    rw [← Set.toFinset_range]
    rw [Set.toFinset_card]
    have hrangeEquiv : Set.range p ≃ (powMonoidHom 65536 : G →* G).range := by
      apply Equiv.setCongr
      ext y
      simp [p]
    rw [← Nat.card_eq_fintype_card, Nat.card_congr hrangeEquiv, hrange]
  calc
    (dual32Domain.image fun x => x ^ (65536 : Nat)).card =
        (Finset.univ.image fun x : {x // x ∈ dual32Domain} => x.1 ^ (65536 : Nat)).card := by
          apply congrArg Finset.card
          ext y
          simp
    _ = (Finset.univ.image fun x : G => (e.symm x).1 ^ (65536 : Nat)).card := by
          congr 1
          ext y
          simp only [Finset.mem_image, Finset.mem_univ, true_and]
          constructor
          · rintro ⟨x, rfl⟩
            exact ⟨e x, by simp⟩
          · rintro ⟨x, rfl⟩
            exact ⟨e.symm x, by simp⟩
    _ = (Finset.univ.image (j ∘ p)).card := by
          rfl
    _ = (Finset.univ.image p).card := by
          rw [← Finset.image_image]
          exact Finset.card_image_of_injective _ hj
    _ = 32 := hcardp

private theorem affineMonomialNatDegree
    {F : Type} [Field F] (q : Nat) (hq : 0 < q) (a b : F) (ha : a ≠ 0) :
    (C a * X ^ q + C b).natDegree = q := by
  calc
    (C a * X ^ q + C b).natDegree = (C a * X ^ q).natDegree :=
      natDegree_add_eq_left_of_natDegree_lt (by
        rw [natDegree_C, natDegree_C_mul_X_pow q a ha]
        exact hq)
    _ = q := natDegree_C_mul_X_pow q a ha

theorem dual32_affine_monomial_positive_degree
    (a b : Dual32Field) (ha : a ≠ 0) :
    0 < (C a * X ^ (65536 : Nat) + C b).natDegree := by
  have hdegree : (C a * X ^ (65536 : Nat) + C b).natDegree = 65536 :=
    affineMonomialNatDegree 65536 (by norm_num) a b ha
  rw [hdegree]
  norm_num

theorem dual32_affine_power_image_card
    (a b : Dual32Field) (ha : a ≠ 0) :
    (dual32Domain.image fun x => a * x ^ (65536 : Nat) + b).card = 32 := by
  let affine : Dual32Field → Dual32Field := fun y => a * y + b
  have haffine : Function.Injective affine := by
    intro y z hyz
    apply mul_left_cancel₀ ha
    exact add_right_cancel hyz
  have himage :
      (dual32Domain.image fun x => a * x ^ (65536 : Nat) + b) =
      (dual32Domain.image fun x => x ^ (65536 : Nat)).image affine := by
    rw [Finset.image_image]
    rfl
  rw [himage, Finset.card_image_of_injective _ haffine, dual32_power_image_card]

theorem dual32_affine_monomial_image_card
    (a b : Dual32Field) (ha : a ≠ 0) :
    (dual32Domain.image fun x =>
      (C a * X ^ (65536 : Nat) + C b).eval x).card = 32 := by
  simpa only [eval_add, eval_mul, eval_C, eval_X_pow] using
    dual32_affine_power_image_card a b ha

theorem dual32_affine_monomial_converse
    (a b : Dual32Field) (ha : a ≠ 0) :
    0 < (C a * X ^ (65536 : Nat) + C b).natDegree ∧
      (dual32Domain.image fun x =>
        (C a * X ^ (65536 : Nat) + C b).eval x).card = 32 :=
  ⟨dual32_affine_monomial_positive_degree a b ha,
    dual32_affine_monomial_image_card a b ha⟩

theorem dual32_complete_value_classification_target
    (f : Polynomial Dual32Field)
    (hdegree : f.natDegree ≤ 67471) :
    (0 < f.natDegree ∧
        (dual32Domain.image fun x => f.eval x).card = 32) ↔
      ∃ a b : Dual32Field,
        a ≠ 0 ∧ f = C a * X ^ (65536 : Nat) + C b := by
  constructor
  · sorry
  · rintro ⟨a, b, ha, hf⟩
    rw [hf]
    exact dual32_affine_monomial_converse a b ha

end GrandeFinale
