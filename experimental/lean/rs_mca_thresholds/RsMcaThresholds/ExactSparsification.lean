import GrandeFinale

/-!
# Exact sparsification of the mutual layer

This file formalizes the exact sparsification theorem and its
challenge-restricted form from experimental/rs_mca_thresholds.tex. It reuses
the support-wise CA/MCA predicates from the Grande Finale package.
-/

open scoped BigOperators Classical

noncomputable section

namespace RsMcaThresholds
namespace ExactSparsification

set_option autoImplicit false

universe u v

variable {F : Type u} {D : Type v}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

local notation "Word" => D → F

/-- A pair is column-far at agreement `a` when it is not simultaneously
explained on any support of cardinality at least `a`. -/
def ColumnFar (C : Submodule F Word) (f₀ f₁ : Word) (a : ℕ) : Prop :=
  ∀ S : Finset D, a ≤ S.card →
    ¬ GrandeFinale.ExplainedPair (C : Set Word) f₀ f₁ S

/-- The finite support of a word. -/
def wordSupport (f : Word) : Finset D :=
  Finset.univ.filter fun x => f x ≠ 0

/-- The union of the two coordinate supports of a received pair. -/
def pairSupport (f₀ f₁ : Word) : Finset D :=
  wordSupport f₀ ∪ wordSupport f₁

/-- The sparse class at agreement `a`. -/
def SparseAt (f₀ f₁ : Word) (a : ℕ) : Prop :=
  (pairSupport f₀ f₁).card ≤ Fintype.card D - a

/-- MCA-bad slopes restricted to a finite challenge set. -/
def restrictedMCABadSlopes (Γ : Finset F) (C : Submodule F Word)
    (f₀ f₁ : Word) (a : ℕ) : Finset F :=
  Γ.filter fun γ => GrandeFinale.MCABad (C : Set Word) f₀ f₁ a γ

/-- CA-bad slopes restricted to a finite challenge set. -/
def restrictedCABadSlopes (Γ : Finset F) (C : Submodule F Word)
    (f₀ f₁ : Word) (a : ℕ) : Finset F :=
  Γ.filter fun γ => GrandeFinale.CABad (C : Set Word) f₀ f₁ a γ

/-- Challenge-restricted MCA numerator. -/
noncomputable def B_MCA_challenge (Γ : Finset F) (C : Submodule F Word)
    (a : ℕ) : ℕ :=
  Finset.univ.sup fun p : Word × Word =>
    (restrictedMCABadSlopes Γ C p.1 p.2 a).card

/-- Challenge-restricted CA numerator. -/
noncomputable def B_CA_challenge (Γ : Finset F) (C : Submodule F Word)
    (a : ℕ) : ℕ :=
  Finset.univ.sup fun p : Word × Word =>
    (restrictedCABadSlopes Γ C p.1 p.2 a).card

/-- Challenge-restricted sparse mutual numerator. -/
noncomputable def sparseMutualChallenge (Γ : Finset F)
    (C : Submodule F Word) (a : ℕ) : ℕ :=
  Finset.univ.sup fun p : Word × Word =>
    if SparseAt p.1 p.2 a
    then (restrictedMCABadSlopes Γ C p.1 p.2 a).card
    else 0

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- Negating column-farness produces a common explaining support. -/
theorem not_columnFar_iff (C : Submodule F Word) (f₀ f₁ : Word) (a : ℕ) :
    ¬ ColumnFar C f₀ f₁ a ↔
      ∃ S : Finset D, a ≤ S.card ∧
        GrandeFinale.ExplainedPair (C : Set Word) f₀ f₁ S := by
  simp [ColumnFar]

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- Translating a word by a codeword preserves explanation on every support. -/
theorem explained_sub_mem_iff (C : Submodule F Word) (f c : Word)
    (hc : c ∈ C) (S : Finset D) :
    GrandeFinale.Explained (C : Set Word) (f - c) S ↔
      GrandeFinale.Explained (C : Set Word) f S := by
  constructor
  · rintro ⟨h, hhC, hh⟩
    refine ⟨h + c, C.add_mem hhC hc, ?_⟩
    intro x hx
    change h x + c x = f x
    rw [hh x hx]
    exact sub_add_cancel _ _
  · rintro ⟨h, hhC, hh⟩
    refine ⟨h - c, C.sub_mem hhC hc, ?_⟩
    intro x hx
    change h x - c x = f x - c x
    rw [hh x hx]

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- Translating both coordinates preserves simultaneous explanation. -/
theorem explainedPair_sub_mem_iff (C : Submodule F Word)
    (f₀ f₁ c₀ c₁ : Word) (hc₀ : c₀ ∈ C) (hc₁ : c₁ ∈ C)
    (S : Finset D) :
    GrandeFinale.ExplainedPair (C : Set Word) (f₀ - c₀) (f₁ - c₁) S ↔
      GrandeFinale.ExplainedPair (C : Set Word) f₀ f₁ S := by
  constructor
  · rintro ⟨h₀, hh₀C, h₁, hh₁C, hh₀, hh₁⟩
    refine ⟨h₀ + c₀, C.add_mem hh₀C hc₀, h₁ + c₁,
      C.add_mem hh₁C hc₁, ?_, ?_⟩
    · intro x hx
      change h₀ x + c₀ x = f₀ x
      rw [hh₀ x hx]
      exact sub_add_cancel _ _
    · intro x hx
      change h₁ x + c₁ x = f₁ x
      rw [hh₁ x hx]
      exact sub_add_cancel _ _
  · rintro ⟨h₀, hh₀C, h₁, hh₁C, hh₀, hh₁⟩
    refine ⟨h₀ - c₀, C.sub_mem hh₀C hc₀, h₁ - c₁,
      C.sub_mem hh₁C hc₁, ?_, ?_⟩
    · intro x hx
      change h₀ x - c₀ x = f₀ x - c₀ x
      rw [hh₀ x hx]
    · intro x hx
      change h₁ x - c₁ x = f₁ x - c₁ x
      rw [hh₁ x hx]

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- Translating a pair preserves line explanation at each slope and support. -/
theorem lineExplained_sub_mem_iff (C : Submodule F Word)
    (f₀ f₁ c₀ c₁ : Word) (hc₀ : c₀ ∈ C) (hc₁ : c₁ ∈ C)
    (γ : F) (S : Finset D) :
    GrandeFinale.Explained (C : Set Word)
        (fun x => (f₀ - c₀) x + γ * (f₁ - c₁) x) S ↔
      GrandeFinale.Explained (C : Set Word)
        (fun x => f₀ x + γ * f₁ x) S := by
  constructor
  · rintro ⟨h, hhC, hh⟩
    refine ⟨h + (c₀ + γ • c₁),
      C.add_mem hhC (C.add_mem hc₀ (C.smul_mem γ hc₁)), ?_⟩
    intro x hx
    change h x + (c₀ x + γ * c₁ x) = f₀ x + γ * f₁ x
    have heq := hh x hx
    change h x = (f₀ x - c₀ x) + γ * (f₁ x - c₁ x) at heq
    rw [heq]
    ring
  · rintro ⟨h, hhC, hh⟩
    refine ⟨h - (c₀ + γ • c₁),
      C.sub_mem hhC (C.add_mem hc₀ (C.smul_mem γ hc₁)), ?_⟩
    intro x hx
    change h x - (c₀ x + γ * c₁ x) =
      (f₀ x - c₀ x) + γ * (f₁ x - c₁ x)
    have heq := hh x hx
    change h x = f₀ x + γ * f₁ x at heq
    rw [heq]
    ring

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- Codeword-pair translation preserves the exact MCA-bad predicate. -/
theorem mcaBad_sub_mem_iff (C : Submodule F Word)
    (f₀ f₁ c₀ c₁ : Word) (hc₀ : c₀ ∈ C) (hc₁ : c₁ ∈ C)
    (a : ℕ) (γ : F) :
    GrandeFinale.MCABad (C : Set Word) (f₀ - c₀) (f₁ - c₁) a γ ↔
      GrandeFinale.MCABad (C : Set Word) f₀ f₁ a γ := by
  constructor
  · rintro ⟨S, hS, hline, hpair⟩
    refine ⟨S, hS,
      (lineExplained_sub_mem_iff C f₀ f₁ c₀ c₁ hc₀ hc₁ γ S).mp hline, ?_⟩
    intro hp
    exact hpair <|
      (explainedPair_sub_mem_iff C f₀ f₁ c₀ c₁ hc₀ hc₁ S).mpr hp
  · rintro ⟨S, hS, hline, hpair⟩
    refine ⟨S, hS,
      (lineExplained_sub_mem_iff C f₀ f₁ c₀ c₁ hc₀ hc₁ γ S).mpr hline, ?_⟩
    intro hp
    exact hpair <|
      (explainedPair_sub_mem_iff C f₀ f₁ c₀ c₁ hc₀ hc₁ S).mp hp

omit [Fintype F] in
/-- A common explaining support becomes a sparse pair after translation. -/
theorem sparseAt_sub_mem_of_explained
    (f₀ f₁ c₀ c₁ : Word) (S : Finset D) (a : ℕ)
    (hS : a ≤ S.card) (h₀ : ∀ x ∈ S, c₀ x = f₀ x) (h₁ : ∀ x ∈ S, c₁ x = f₁ x) :
    SparseAt (f₀ - c₀) (f₁ - c₁) a := by
  have hsupp :
      pairSupport (f₀ - c₀) (f₁ - c₁) ⊆ Finset.univ \ S := by
    intro x hx
    rw [Finset.mem_sdiff]
    refine ⟨Finset.mem_univ x, ?_⟩
    intro hxS
    rcases Finset.mem_union.mp hx with hx₀ | hx₁
    · have hne : (f₀ - c₀) x ≠ 0 :=
        (Finset.mem_filter.mp hx₀).2
      apply hne
      change f₀ x - c₀ x = 0
      rw [h₀ x hxS]
      simp
    · have hne : (f₁ - c₁) x ≠ 0 :=
        (Finset.mem_filter.mp hx₁).2
      apply hne
      change f₁ x - c₁ x = 0
      rw [h₁ x hxS]
      simp
  unfold SparseAt
  calc
    (pairSupport (f₀ - c₀) (f₁ - c₁)).card
        ≤ (Finset.univ \ S).card := Finset.card_le_card hsupp
    _ = (Finset.univ : Finset D).card - S.card := by
      rw [Finset.card_sdiff]
      simp
    _ = Fintype.card D - S.card := by simp
    _ ≤ Fintype.card D - a := Nat.sub_le_sub_left hS _

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- On a column-far pair MCA-badness and CA-badness coincide. -/
theorem restrictedMCA_eq_restrictedCA_of_columnFar
    (Γ : Finset F) (C : Submodule F Word) (f₀ f₁ : Word) (a : ℕ)
    (hfar : ColumnFar C f₀ f₁ a) :
    restrictedMCABadSlopes Γ C f₀ f₁ a =
      restrictedCABadSlopes Γ C f₀ f₁ a := by
  ext γ
  simp only [restrictedMCABadSlopes, restrictedCABadSlopes,
    Finset.mem_filter]
  constructor
  · rintro ⟨hγ, S, hS, hline, -⟩
    exact ⟨hγ, ⟨⟨S, hS, hline⟩, hfar⟩⟩
  · rintro ⟨hγ, hca⟩
    exact ⟨hγ, GrandeFinale.CABad_imp_MCABad hca⟩

omit [DecidableEq F] in
theorem B_CA_challenge_le_B_MCA_challenge (Γ : Finset F)
    (C : Submodule F Word) (a : ℕ) :
    B_CA_challenge Γ C a ≤ B_MCA_challenge Γ C a := by
  refine Finset.sup_le ?_
  intro p hp
  calc
    (restrictedCABadSlopes Γ C p.1 p.2 a).card
        ≤ (restrictedMCABadSlopes Γ C p.1 p.2 a).card := by
          apply Finset.card_le_card
          intro γ hγ
          simp only [restrictedCABadSlopes, restrictedMCABadSlopes,
            Finset.mem_filter] at hγ ⊢
          exact ⟨hγ.1, GrandeFinale.CABad_imp_MCABad hγ.2⟩
    _ ≤ B_MCA_challenge Γ C a := by
      unfold B_MCA_challenge
      exact Finset.le_sup
        (s := (Finset.univ : Finset (Word × Word)))
        (f := fun q : Word × Word =>
          (restrictedMCABadSlopes Γ C q.1 q.2 a).card) hp

theorem sparseMutualChallenge_le_B_MCA_challenge (Γ : Finset F)
    (C : Submodule F Word) (a : ℕ) :
    sparseMutualChallenge Γ C a ≤ B_MCA_challenge Γ C a := by
  unfold sparseMutualChallenge
  refine Finset.sup_le ?_
  intro p hp
  by_cases hsparse : SparseAt p.1 p.2 a
  · simp only [hsparse, if_true]
    unfold B_MCA_challenge
    exact Finset.le_sup
      (s := (Finset.univ : Finset (Word × Word)))
      (f := fun q : Word × Word =>
        (restrictedMCABadSlopes Γ C q.1 q.2 a).card) hp
  · simp [hsparse]

theorem B_MCA_challenge_le_max (Γ : Finset F)
    (C : Submodule F Word) (a : ℕ) :
    B_MCA_challenge Γ C a ≤
      max (B_CA_challenge Γ C a) (sparseMutualChallenge Γ C a) := by
  refine Finset.sup_le ?_
  intro p hp
  by_cases hfar : ColumnFar C p.1 p.2 a
  · rw [restrictedMCA_eq_restrictedCA_of_columnFar Γ C p.1 p.2 a hfar]
    have hca :
        (restrictedCABadSlopes Γ C p.1 p.2 a).card ≤
          B_CA_challenge Γ C a := by
      unfold B_CA_challenge
      exact Finset.le_sup
        (s := (Finset.univ : Finset (Word × Word)))
        (f := fun q : Word × Word =>
          (restrictedCABadSlopes Γ C q.1 q.2 a).card) hp
    exact le_trans hca (Nat.le_max_left _ _)
  · rcases (not_columnFar_iff C p.1 p.2 a).mp hfar with
      ⟨S, hS, c₀, hc₀, c₁, hc₁, h₀, h₁⟩
    let e₀ : Word := p.1 - c₀
    let e₁ : Word := p.2 - c₁
    have hsparse : SparseAt e₀ e₁ a := by
      exact sparseAt_sub_mem_of_explained p.1 p.2 c₀ c₁ S a hS h₀ h₁
    have hbad :
        restrictedMCABadSlopes Γ C e₀ e₁ a =
          restrictedMCABadSlopes Γ C p.1 p.2 a := by
      ext γ
      simp only [restrictedMCABadSlopes, Finset.mem_filter]
      exact and_congr_right fun _ =>
        mcaBad_sub_mem_iff C p.1 p.2 c₀ c₁ hc₀ hc₁ a γ
    have hle :
        (restrictedMCABadSlopes Γ C e₀ e₁ a).card ≤
          sparseMutualChallenge Γ C a := by
      have hp' : (e₀, e₁) ∈ (Finset.univ : Finset (Word × Word)) :=
        Finset.mem_univ _
      have hsup := Finset.le_sup
        (s := (Finset.univ : Finset (Word × Word)))
        (f := fun q : Word × Word =>
          if SparseAt q.1 q.2 a
          then (restrictedMCABadSlopes Γ C q.1 q.2 a).card
          else 0) hp'
      simpa [sparseMutualChallenge, hsparse] using hsup
    rw [← hbad]
    exact le_trans hle (Nat.le_max_right _ _)

/-- Exact challenge-restricted sparsification identity (SP3). -/
theorem exact_sparsification_challenge (Γ : Finset F)
    (C : Submodule F Word) (a : ℕ) :
    B_MCA_challenge Γ C a =
      max (B_CA_challenge Γ C a) (sparseMutualChallenge Γ C a) := by
  apply le_antisymm
  · exact B_MCA_challenge_le_max Γ C a
  · exact max_le
      (B_CA_challenge_le_B_MCA_challenge Γ C a)
      (sparseMutualChallenge_le_B_MCA_challenge Γ C a)

/-- The full-field sparse mutual numerator from SP1. -/
noncomputable def sparseMutualNumerator (C : Submodule F Word)
    (a : ℕ) : ℕ :=
  sparseMutualChallenge Finset.univ C a

/-- Exact sparsification of the mutual layer (SP2). -/
theorem exact_sparsification (C : Submodule F Word) (a : ℕ) :
    GrandeFinale.B_MCA (C : Set Word) a =
      max (GrandeFinale.B_CA (C : Set Word) a)
        (sparseMutualNumerator C a) := by
  simpa [GrandeFinale.B_MCA, GrandeFinale.B_CA,
    B_MCA_challenge, B_CA_challenge, sparseMutualNumerator,
    restrictedMCABadSlopes, restrictedCABadSlopes] using
      exact_sparsification_challenge (Finset.univ : Finset F) C a

#print axioms exact_sparsification_challenge
#print axioms exact_sparsification

end ExactSparsification
end RsMcaThresholds
