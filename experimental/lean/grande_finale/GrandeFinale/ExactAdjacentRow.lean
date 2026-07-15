import GrandeFinale.SyndromeLine

/-!
# Exact separating hyperplanes for the first adjacent row

This module formalizes the finite hyperplane-avoidance and syndrome-line
compiler used in the lower-bound half of
`thm:exact-first-adjacent-row` in
`experimental/asymptotic_rs_mca_frontiers.tex`.

For `M` distinct hyperplanes, the literal gate
`max M (Nat.choose M 2) < |F|` first chooses a direction outside all `M`
hyperplanes, then chooses an intercept outside the collision hyperplanes for
the `Nat.choose M 2` unordered pairs. The resulting affine line meets every
hyperplane transversely at a different finite slope.

The syndrome compiler turns such a family into `M` distinct support-wise
MCA-bad slopes using the exact definitions in `GrandeFinale.SyndromeLine`.
The Reed--Solomon weighted Vandermonde specialization, the exact support upper
bound, and the two threshold implications in (AD2) are separate statements;
they are not assumed by the separating-line theorem.
-/

open scoped Classical

noncomputable section

namespace GrandeFinale.ExactAdjacentRow

variable {ι F W : Type*} [Field F] [Fintype F]
  [AddCommGroup W] [Module F W] [Fintype ι] [LinearOrder ι]

/-- A family of `M` distinct functional kernels over a field larger than both
`M` and `choose M 2` admits an affine line whose transverse intersection
slopes are pairwise distinct. -/
theorem exists_separating_line
    (ell : ι → W →ₗ[F] F)
    (hell : ∀ i, ell i ≠ 0)
    (hker : Function.Injective fun i ↦ LinearMap.ker (ell i))
    (hcard : Fintype.card ι < Fintype.card F)
    (hpairs : (Fintype.card ι).choose 2 < Fintype.card F) :
    ∃ y0 y1 : W, ∃ slope : ι → F,
      Function.Injective slope ∧
      (∀ i, y0 + slope i • y1 ∈ LinearMap.ker (ell i)) ∧
      (∀ i, y1 ∉ LinearMap.ker (ell i)) := by
  classical
  have hproper : ∀ i, LinearMap.ker (ell i) ≠ ⊤ := by
    intro i
    rw [ne_eq, LinearMap.ker_eq_top]
    exact hell i
  have hcard' : ((Finset.univ : Finset ι).card : ENat) < ENat.card F := by
    simpa using hcard
  have hy1avoid := Submodule.iUnion_ssubset_of_forall_ne_top_of_card_lt
    (Finset.univ : Finset ι) (fun i ↦ LinearMap.ker (ell i)) hproper hcard'
  obtain ⟨y1, _hy1univ, hy1⟩ := Set.exists_of_ssubset hy1avoid
  have hy1ker : ∀ i, y1 ∉ LinearMap.ker (ell i) := by
    intro i hi
    apply hy1
    simp only [Set.mem_iUnion]
    exact ⟨i, Finset.mem_univ i, hi⟩
  have hy1val : ∀ i, ell i y1 ≠ 0 := by
    intro i hi
    exact hy1ker i (by simpa using hi)
  let norm : ι → W →ₗ[F] F := fun i ↦ (ell i y1)⁻¹ • ell i
  have hnormKer : ∀ i, LinearMap.ker (norm i) = LinearMap.ker (ell i) := by
    intro i
    exact LinearMap.ker_smul (ell i) (ell i y1)⁻¹ (inv_ne_zero (hy1val i))
  have hnormNe : ∀ {i j}, i ≠ j → norm i ≠ norm j := by
    intro i j hij heq
    apply hij
    apply hker
    change LinearMap.ker (ell i) = LinearMap.ker (ell j)
    rw [← hnormKer i, ← hnormKer j, heq]
  let pairs : Finset (Finset ι) :=
    (Finset.univ : Finset ι).powersetCard 2
  have hpairCard (P : ↑pairs) : P.1.card = 2 := by
    exact (Finset.mem_powersetCard.mp P.2).2
  have hpairNonempty (P : ↑pairs) : P.1.Nonempty := by
    apply Finset.card_pos.mp
    rw [hpairCard P]
    omega
  let lo : ↑pairs → ι := fun P ↦ P.1.min' (hpairNonempty P)
  let hi : ↑pairs → ι := fun P ↦ P.1.max' (hpairNonempty P)
  have hlohi (P : ↑pairs) : lo P < hi P := by
    dsimp [lo, hi]
    apply Finset.min'_lt_max'_of_card
    rw [hpairCard P]
    omega
  let collision : ↑pairs → Submodule F W := fun P ↦
    LinearMap.ker (norm (lo P) - norm (hi P))
  have hcollisionProper : ∀ P, collision P ≠ ⊤ := by
    intro P
    change LinearMap.ker (norm (lo P) - norm (hi P)) ≠ ⊤
    rw [ne_eq, LinearMap.ker_eq_top]
    exact sub_ne_zero.mpr (hnormNe (hlohi P).ne)
  have hpairs' : ((Finset.univ : Finset ↑pairs).card : ENat) < ENat.card F := by
    simpa [pairs, Finset.card_powersetCard] using hpairs
  have hy0avoid := Submodule.iUnion_ssubset_of_forall_ne_top_of_card_lt
    (Finset.univ : Finset ↑pairs) collision hcollisionProper hpairs'
  obtain ⟨y0, _hy0univ, hy0⟩ := Set.exists_of_ssubset hy0avoid
  have hy0ker : ∀ P, y0 ∉ collision P := by
    intro P hP
    apply hy0
    simp only [Set.mem_iUnion]
    exact ⟨P, Finset.mem_univ P, hP⟩
  have hnormValPair : ∀ P, norm (lo P) y0 ≠ norm (hi P) y0 := by
    intro P heq
    apply hy0ker P
    change (norm (lo P) - norm (hi P)) y0 = 0
    simp [heq]
  have hnormVal : ∀ {i j}, i ≠ j → norm i y0 ≠ norm j y0 := by
    intro i j hij heq
    let P : ↑pairs := ⟨{i, j}, by simp [pairs, hij]⟩
    apply hnormValPair P
    have hloMem : lo P ∈ ({i, j} : Finset ι) := by
      exact Finset.min'_mem P.1 (hpairNonempty P)
    have hhiMem : hi P ∈ ({i, j} : Finset ι) := by
      exact Finset.max'_mem P.1 (hpairNonempty P)
    simp only [Finset.mem_insert, Finset.mem_singleton] at hloMem hhiMem
    rcases hloMem with hlo | hlo <;> rcases hhiMem with hhi | hhi
    · exact False.elim ((hlohi P).ne (hlo.trans hhi.symm))
    · simpa [hlo, hhi] using heq
    · simpa [hlo, hhi] using heq.symm
    · exact False.elim ((hlohi P).ne (hlo.trans hhi.symm))
  let slope : ι → F := fun i ↦ -(ell i y0) / ell i y1
  refine ⟨y0, y1, slope, ?_, ?_, hy1ker⟩
  · intro i j hslope
    by_contra hij
    apply hnormVal hij
    have hdiv : ell i y0 / ell i y1 = ell j y0 / ell j y1 := by
      calc
        ell i y0 / ell i y1 = -slope i := by
          simp only [slope, neg_div, neg_neg]
        _ = -slope j := congrArg (fun x : F ↦ -x) hslope
        _ = ell j y0 / ell j y1 := by
          simp only [slope, neg_div, neg_neg]
    simpa [norm, div_eq_mul_inv, mul_comm] using hdiv
  · intro i
    change ell i (y0 + slope i • y1) = 0
    simp [slope, hy1val i]

/-- The same separating-line theorem under the paper's literal
`max M (choose M 2) < |F|` gate. -/
theorem exists_separating_line_of_max_lt
    (ell : ι → W →ₗ[F] F)
    (hell : ∀ i, ell i ≠ 0)
    (hker : Function.Injective fun i ↦ LinearMap.ker (ell i))
    (hgate : max (Fintype.card ι) ((Fintype.card ι).choose 2) <
      Fintype.card F) :
    ∃ y0 y1 : W, ∃ slope : ι → F,
      Function.Injective slope ∧
      (∀ i, y0 + slope i • y1 ∈ LinearMap.ker (ell i)) ∧
      (∀ i, y1 ∉ LinearMap.ker (ell i)) := by
  apply exists_separating_line ell hell hker
  · exact (Nat.le_max_left _ _).trans_lt hgate
  · exact (Nat.le_max_right _ _).trans_lt hgate

section SyndromeCompiler

open GrandeFinale.SyndromeLine

variable {D : Type*} [Fintype D] [DecidableEq D] [DecidableEq F]
  [Fintype W] [DecidableEq W]

omit [DecidableEq D] in
set_option maxHeartbeats 800000 in
/-- A separating family of syndrome hyperplanes contributes at least one
distinct transverse secant slope per family member. -/
theorem separatingHyperplanes_le_syndromeSecantNumerator
    (H : (D → F) →ₗ[F] W) (t : Nat)
    (errors : ι → Finset D) (herrors : ∀ i, (errors i).card ≤ t)
    (ell : ι → W →ₗ[F] F)
    (hell : ∀ i, ell i ≠ 0)
    (hker : Function.Injective fun i ↦ LinearMap.ker (ell i))
    (hspan : ∀ i, syndromeSpan H (errors i : Set D) = LinearMap.ker (ell i))
    (hcard : Fintype.card ι < Fintype.card F)
    (hpairs : (Fintype.card ι).choose 2 < Fintype.card F) :
    Fintype.card ι ≤ syndromeSecantNumerator H t := by
  obtain ⟨y0, y1, slope, hslope, hline, hy1⟩ :=
    exists_separating_line ell hell hker hcard hpairs
  let slopes : Finset F := Finset.univ.image slope
  have hmem : ∀ i, slope i ∈ transverseSecantSlopes H t y0 y1 := by
    intro i
    apply (mem_transverseSecantSlopes_iff H t y0 y1 (slope i)).mpr
    refine ⟨errors i, herrors i, ?_, ?_⟩
    · rw [hspan i]
      exact hline i
    · rintro ⟨_y0mem, hy1mem⟩
      apply hy1 i
      rw [← hspan i]
      exact hy1mem
  have hsub : slopes ⊆ transverseSecantSlopes H t y0 y1 := by
    intro gamma hgamma
    rcases Finset.mem_image.mp hgamma with ⟨i, _hi, rfl⟩
    exact hmem i
  calc
    Fintype.card ι = slopes.card := by
      rw [show slopes = Finset.univ.image slope by rfl,
        Finset.card_image_of_injective _ hslope, Finset.card_univ]
    _ ≤ (transverseSecantSlopes H t y0 y1).card :=
      Finset.card_le_card hsub
    _ ≤ syndromeSecantNumerator H t := by
      unfold syndromeSecantNumerator
      exact Finset.le_sup
        (f := fun p : W × W ↦ (transverseSecantSlopes H t p.1 p.2).card)
        (Finset.mem_univ (y0, y1))

/-- With syndrome surjectivity, the separating-hyperplane lower bound is a
literal lower bound for the existing support-wise MCA numerator. -/
theorem separatingHyperplanes_le_B_MCA
    (H : (D → F) →ₗ[F] W) (hH : Function.Surjective H)
    (a : Nat) (ha : a ≤ Fintype.card D)
    (errors : ι → Finset D)
    (herrors : ∀ i, (errors i).card ≤ Fintype.card D - a)
    (ell : ι → W →ₗ[F] F)
    (hell : ∀ i, ell i ≠ 0)
    (hker : Function.Injective fun i ↦ LinearMap.ker (ell i))
    (hspan : ∀ i, syndromeSpan H (errors i : Set D) = LinearMap.ker (ell i))
    (hcard : Fintype.card ι < Fintype.card F)
    (hpairs : (Fintype.card ι).choose 2 < Fintype.card F) :
    Fintype.card ι ≤ GrandeFinale.B_MCA (H.ker : Set (D → F)) a := by
  rw [B_MCA_eq_syndromeSecantNumerator H hH ha]
  exact separatingHyperplanes_le_syndromeSecantNumerator
    H (Fintype.card D - a) errors herrors ell hell hker hspan hcard hpairs

/-- Combining the separating construction with an exact support upper bound
gives numerator equality. -/
theorem B_MCA_eq_of_separatingHyperplanes
    (H : (D → F) →ₗ[F] W) (hH : Function.Surjective H)
    (a : Nat) (ha : a ≤ Fintype.card D)
    (errors : ι → Finset D)
    (herrors : ∀ i, (errors i).card ≤ Fintype.card D - a)
    (ell : ι → W →ₗ[F] F)
    (hell : ∀ i, ell i ≠ 0)
    (hker : Function.Injective fun i ↦ LinearMap.ker (ell i))
    (hspan : ∀ i, syndromeSpan H (errors i : Set D) = LinearMap.ker (ell i))
    (hcard : Fintype.card ι < Fintype.card F)
    (hpairs : (Fintype.card ι).choose 2 < Fintype.card F)
    (hupper : GrandeFinale.B_MCA (H.ker : Set (D → F)) a ≤ Fintype.card ι) :
    GrandeFinale.B_MCA (H.ker : Set (D → F)) a = Fintype.card ι := by
  apply Nat.le_antisymm hupper
  exact separatingHyperplanes_le_B_MCA H hH a ha errors herrors
    ell hell hker hspan hcard hpairs

end SyndromeCompiler

#print axioms exists_separating_line_of_max_lt
#print axioms separatingHyperplanes_le_syndromeSecantNumerator
#print axioms separatingHyperplanes_le_B_MCA
#print axioms B_MCA_eq_of_separatingHyperplanes

end GrandeFinale.ExactAdjacentRow
