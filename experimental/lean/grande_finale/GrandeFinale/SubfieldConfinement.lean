import GrandeFinale.CollisionAwarePole

/-!
# Subfield confinement for base-valued Reed--Solomon lines

This module formalizes `thm:subfield-confinement-full` from
`experimental/asymptotic_rs_mca_frontiers.tex`.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.SubfieldConfinement

variable {B F D : Type*} [Field B] [Field F] [Algebra B F]

/-- Embed a base-field-valued word into the extension field. -/
def liftWord (u : D → B) : D → F :=
  fun x ↦ algebraMap B F (u x)

/-- Finite coefficient-vector presentation of degree-less-than-`k`
Reed--Solomon evaluations on a base-field domain. -/
def baseDomainRSEval (ev : D → B) (k : Nat) : Set (D → F) :=
  {u | ∃ coeff : Fin k → F, ∀ x,
    u x = ∑ i, coeff i * (algebraMap B F (ev x)) ^ (i : Nat)}

/-- The finite coefficient presentation is exactly the existing polynomial
`rsEval` submodule on the embedded evaluation domain. -/
theorem baseDomainRSEval_eq_rsEval (ev : D → B) (k : Nat) :
    baseDomainRSEval (F := F) ev k =
      (CollisionAwarePole.rsEval
        (fun x ↦ algebraMap B F (ev x)) k : Set (D → F)) := by
  ext u
  constructor
  · rintro ⟨coeff, hcoeff⟩
    change u ∈ CollisionAwarePole.rsEval
      (fun x ↦ algebraMap B F (ev x)) k
    rw [CollisionAwarePole.mem_rsEval]
    refine ⟨∑ i : Fin k, C (coeff i) * X ^ (i : Nat),
      Polynomial.degree_sum_fin_lt coeff, ?_⟩
    intro x
    rw [hcoeff x]
    simp [Polynomial.eval_finset_sum]
  · intro huRS
    change u ∈ CollisionAwarePole.rsEval
      (fun x ↦ algebraMap B F (ev x)) k at huRS
    rw [CollisionAwarePole.mem_rsEval] at huRS
    rcases huRS with ⟨p, hp, hu⟩
    refine ⟨fun i ↦ p.coeff i, ?_⟩
    intro x
    rw [hu x, Polynomial.eval_eq_sum]
    exact (Polynomial.sum_fin
      (f := fun n a ↦ a * (algebraMap B F (ev x)) ^ n)
      (by intro i; simp) hp).symm

/-! ## Base-coordinate functionals -/

/-- For a nonbase element `gamma`, extract its base and nonbase coordinates
with two base-linear functionals. -/
theorem exists_baseCoordinateFunctionals {gamma : F}
    (hgamma : gamma ∉ Set.range (algebraMap B F)) :
    ∃ L₀ L₁ : F →ₗ[B] B,
      L₀ 1 = 1 ∧ L₀ gamma = 0 ∧
      L₁ 1 = 0 ∧ L₁ gamma = 1 := by
  have hgammaSpan : gamma ∉ B ∙ (1 : F) := by
    intro hmem
    rcases Submodule.mem_span_singleton.mp hmem with ⟨b, hb⟩
    apply hgamma
    exact ⟨b, by simpa [Algebra.smul_def] using hb⟩
  obtain ⟨raw, hrawGamma, hrawSpan⟩ :=
    Submodule.exists_le_ker_of_notMem hgammaSpan
  let L₁ : F →ₗ[B] B := (raw gamma)⁻¹ • raw
  have hrawOne : raw 1 = 0 := by
    exact LinearMap.mem_ker.mp
      (hrawSpan (Submodule.mem_span_singleton_self (1 : F)))
  have hL₁One : L₁ 1 = 0 := by
    simp [L₁, hrawOne]
  have hL₁Gamma : L₁ gamma = 1 := by
    simp [L₁, hrawGamma]
  have hOneBot : (1 : F) ∉ (⊥ : Submodule B F) := by simp
  obtain ⟨T, _hT, hTOne⟩ :=
    LinearMap.exists_extend_of_notMem
      (0 : (⊥ : Submodule B F) →ₗ[B] B) hOneBot 1
  let L₀ : F →ₗ[B] B := T - (T gamma) • L₁
  have hL₀One : L₀ 1 = 1 := by
    simp [L₀, hTOne, hL₁One]
  have hL₀Gamma : L₀ gamma = 0 := by
    simp [L₀, hL₁Gamma]
  exact ⟨L₀, L₁, hL₀One, hL₀Gamma, hL₁One, hL₁Gamma⟩

/-! ## Coefficientwise projection and same-support transfer -/

/-- Applying a base-linear functional coefficientwise preserves the
base-domain Reed--Solomon code. -/
theorem baseDomainRSEval_projection
    (ev : D → B) (k : Nat) (L : F →ₗ[B] B) {c : D → F}
    (hc : c ∈ baseDomainRSEval (F := F) ev k) :
    (fun x ↦ algebraMap B F (L (c x))) ∈
      baseDomainRSEval (F := F) ev k := by
  rcases hc with ⟨coeff, hcoeff⟩
  refine ⟨fun i ↦ algebraMap B F (L (coeff i)), ?_⟩
  intro x
  change algebraMap B F (L (c x)) =
    ∑ i, algebraMap B F (L (coeff i)) *
      (algebraMap B F (ev x)) ^ (i : Nat)
  rw [hcoeff x]
  have hterm (i : Fin k) :
      coeff i * (algebraMap B F (ev x)) ^ (i : Nat) =
        (ev x ^ (i : Nat)) • coeff i := by
    simp [Algebra.smul_def, map_pow, mul_comm]
  simp only [map_sum]
  apply Finset.sum_congr rfl
  intro i _hi
  rw [hterm i, map_smul]
  simp [map_pow, mul_comm]

/-- A nonbase slope explaining a base-valued line point forces pair
explanation on the same support. -/
theorem baseDomainRSEval_explainedPair_of_nonbase
    (ev : D → B) (k : Nat) (u₀ u₁ : D → B)
    {gamma : F} (hgamma : gamma ∉ Set.range (algebraMap B F))
    (S : Finset D)
    (hexplained :
      Explained (baseDomainRSEval (F := F) ev k)
        (fun x ↦ liftWord (F := F) u₀ x +
          gamma * liftWord (F := F) u₁ x) S) :
    ExplainedPair (baseDomainRSEval (F := F) ev k)
      (liftWord (F := F) u₀) (liftWord (F := F) u₁) S := by
  rcases hexplained with ⟨c, hc, hagree⟩
  obtain ⟨L₀, L₁, hL₀One, hL₀Gamma, hL₁One, hL₁Gamma⟩ :=
    exists_baseCoordinateFunctionals hgamma
  let c₀ : D → F := fun x ↦ algebraMap B F (L₀ (c x))
  let c₁ : D → F := fun x ↦ algebraMap B F (L₁ (c x))
  have hc₀ : c₀ ∈ baseDomainRSEval (F := F) ev k :=
    baseDomainRSEval_projection ev k L₀ hc
  have hc₁ : c₁ ∈ baseDomainRSEval (F := F) ev k :=
    baseDomainRSEval_projection ev k L₁ hc
  refine ⟨c₀, hc₀, c₁, hc₁, ?_, ?_⟩
  · intro x hx
    have hcLine :
        c x = (u₀ x) • (1 : F) + (u₁ x) • gamma := by
      rw [hagree x hx]
      simp [liftWord, Algebra.smul_def, mul_comm]
    have hcoord :
        L₀ (c x) = u₀ x := by
      rw [hcLine, map_add, map_smul, map_smul, hL₀One, hL₀Gamma]
      simp
    exact congrArg (algebraMap B F) hcoord
  · intro x hx
    have hcLine :
        c x = (u₀ x) • (1 : F) + (u₁ x) • gamma := by
      rw [hagree x hx]
      simp [liftWord, Algebra.smul_def, mul_comm]
    have hcoord :
        L₁ (c x) = u₁ x := by
      rw [hcLine, map_add, map_smul, map_smul, hL₁One, hL₁Gamma]
      simp
    exact congrArg (algebraMap B F) hcoord

/-- Same-support transfer stated directly for the package's existing
polynomial Reed--Solomon submodule. -/
theorem rsEval_explainedPair_of_nonbase
    (ev : D → B) (k : Nat) (u₀ u₁ : D → B)
    {gamma : F} (hgamma : gamma ∉ Set.range (algebraMap B F))
    (S : Finset D)
    (hexplained :
      Explained
        (CollisionAwarePole.rsEval
          (fun x ↦ algebraMap B F (ev x)) k)
        (fun x ↦ liftWord (F := F) u₀ x +
          gamma * liftWord (F := F) u₁ x) S) :
    ExplainedPair
      (CollisionAwarePole.rsEval
        (fun x ↦ algebraMap B F (ev x)) k)
      (liftWord (F := F) u₀) (liftWord (F := F) u₁) S := by
  rw [← baseDomainRSEval_eq_rsEval] at hexplained ⊢
  exact baseDomainRSEval_explainedPair_of_nonbase
    ev k u₀ u₁ hgamma S hexplained

/-! ## MCA subfield confinement -/

/-- Every MCA-bad slope of a base-valued received line lies in the base
field. -/
theorem rsEval_mcaBad_slope_mem_base
    (ev : D → B) (k a : Nat) (u₀ u₁ : D → B) {gamma : F}
    (hbad :
      MCABad
        (CollisionAwarePole.rsEval
          (fun x ↦ algebraMap B F (ev x)) k)
        (liftWord (F := F) u₀) (liftWord (F := F) u₁) a gamma) :
    gamma ∈ Set.range (algebraMap B F) := by
  by_contra hgamma
  rcases hbad with ⟨S, _ha, hexplained, hnotPair⟩
  exact hnotPair
    (rsEval_explainedPair_of_nonbase
      ev k u₀ u₁ hgamma S hexplained)

/-- The finite bad-slope set of a base-valued line has cardinality at most the
base-field size. -/
theorem rsEval_mcaBadSlopes_card_le_base
    [Fintype B] [Fintype F] [DecidableEq F]
    (ev : D → B) (k a : Nat) (u₀ u₁ : D → B) :
    ((Finset.univ : Finset F).filter fun gamma ↦
      MCABad
        (CollisionAwarePole.rsEval
          (fun x ↦ algebraMap B F (ev x)) k)
        (liftWord (F := F) u₀) (liftWord (F := F) u₁) a gamma).card ≤
      Fintype.card B := by
  let bad : Finset F :=
    (Finset.univ : Finset F).filter fun gamma ↦
      MCABad
        (CollisionAwarePole.rsEval
          (fun x ↦ algebraMap B F (ev x)) k)
        (liftWord (F := F) u₀) (liftWord (F := F) u₁) a gamma
  have hsubset :
      bad ⊆ (Finset.univ : Finset B).image (algebraMap B F) := by
    intro gamma hgamma
    have hbase := rsEval_mcaBad_slope_mem_base ev k a u₀ u₁
      (Finset.mem_filter.mp hgamma).2
    rcases hbase with ⟨b, rfl⟩
    exact Finset.mem_image.mpr ⟨b, Finset.mem_univ b, rfl⟩
  calc
    bad.card ≤ ((Finset.univ : Finset B).image (algebraMap B F)).card :=
      Finset.card_le_card hsubset
    _ ≤ (Finset.univ : Finset B).card := Finset.card_image_le
    _ = Fintype.card B := Finset.card_univ

#print axioms baseDomainRSEval_eq_rsEval
#print axioms exists_baseCoordinateFunctionals
#print axioms baseDomainRSEval_projection
#print axioms rsEval_explainedPair_of_nonbase
#print axioms rsEval_mcaBad_slope_mem_base
#print axioms rsEval_mcaBadSlopes_card_le_base

end GrandeFinale.SubfieldConfinement
