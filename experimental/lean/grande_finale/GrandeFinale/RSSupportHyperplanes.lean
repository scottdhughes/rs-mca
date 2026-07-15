import GrandeFinale.RSParityKernel
import GrandeFinale.SyndromeLine

/-!
# Exact syndrome hyperplanes from Reed--Solomon supports

This module identifies the syndrome span of a finite error support with the
span of its barycentric weighted Vandermonde columns. Exact `(R-1)` supports
therefore produce codimension-one syndrome hyperplanes, and the MDS column
property proves that distinct exact supports produce distinct hyperplanes.
-/

open scoped Classical

noncomputable section

namespace GrandeFinale.RSSupportHyperplanes

open GrandeFinale.RSParityKernel
open GrandeFinale.SyndromeLine

variable {D F : Type*} [Field F] [Fintype D] [DecidableEq D]

/-- The weighted Vandermonde column span indexed by a finite support. -/
def supportColumnSpan (ev : D → F) (R : Nat) (E : Finset D) :
    Submodule F (Fin R → F) :=
  Submodule.span F (Set.range fun d : E ↦ weightedColumn ev R d)

/-- The syndrome image of errors supported on `E` is exactly the span of the
weighted columns indexed by `E`. -/
theorem syndromeSpan_parityCheck_eq_supportColumnSpan
    (ev : D → F) (R : Nat) (E : Finset D) :
    syndromeSpan (parityCheck ev R) (E : Set D) =
      supportColumnSpan ev R E := by
  apply le_antisymm
  · rintro y ⟨e, he, rfl⟩
    change parityCheck ev R e ∈ supportColumnSpan ev R E
    rw [parityCheck, Fintype.linearCombination_apply]
    apply Submodule.sum_mem
    intro d _hd
    by_cases hdE : d ∈ E
    · apply Submodule.smul_mem
      apply Submodule.subset_span
      exact ⟨⟨d, hdE⟩, rfl⟩
    · have hed0 : e d = 0 := he d (by simpa using hdE)
      simp [hed0]
  · apply Submodule.span_le.mpr
    rintro y ⟨d, rfl⟩
    refine ⟨Pi.single d.1 1, ?_, ?_⟩
    · intro x hx
      have hxd : x ≠ d.1 := by
        intro h
        subst x
        exact hx d.2
      simp [hxd]
    · simp [parityCheck]

/-- The support-column span has dimension equal to the support cardinality as
long as the support has at most `R` points. -/
theorem supportColumnSpan_finrank
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (E : Finset D) (hER : E.card ≤ R) :
    Module.finrank F (supportColumnSpan ev R E) = E.card := by
  unfold supportColumnSpan
  rw [finrank_span_eq_card
    (weightedColumns_linearIndependent ev hev R E hER), Fintype.card_coe]

/-- A support with fewer than `R` points spans a proper syndrome subspace. -/
theorem supportColumnSpan_lt_top
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (E : Finset D) (hER : E.card < R) :
    supportColumnSpan ev R E < ⊤ := by
  apply Submodule.lt_top_of_finrank_lt_finrank
  rw [supportColumnSpan_finrank ev hev R E hER.le,
    Module.finrank_fin_fun F]
  exact hER

/-- Every exact `(R-1)` support is the kernel of a nonzero syndrome
functional. -/
theorem exists_supportFunctional
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (hR : 0 < R) (E : Finset D) (hE : E.card = R - 1) :
    ∃ ell : (Fin R → F) →ₗ[F] F, ell ≠ 0 ∧
      syndromeSpan (parityCheck ev R) (E : Set D) = LinearMap.ker ell := by
  have hER : E.card < R := by omega
  obtain ⟨ell, hell, hle⟩ :=
    (supportColumnSpan ev R E).exists_le_ker_of_lt_top
      (supportColumnSpan_lt_top ev hev R E hER)
  refine ⟨ell, hell, ?_⟩
  rw [syndromeSpan_parityCheck_eq_supportColumnSpan]
  apply Submodule.eq_of_le_of_finrank_eq hle
  have hkerRank := Module.Dual.finrank_ker_add_one_of_ne_zero hell
  have hspanRank := supportColumnSpan_finrank ev hev R E hER.le
  have hambient : Module.finrank F (Fin R → F) = R :=
    Module.finrank_fin_fun F
  rw [hambient] at hkerRank
  rw [hspanRank]
  omega

/-- Distinct exact `(R-1)` supports have distinct weighted column spans. -/
theorem supportColumnSpan_injective_of_card_eq
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (hR : 0 < R) {E E' : Finset D}
    (hE : E.card = R - 1) (hE' : E'.card = R - 1)
    (hspan : supportColumnSpan ev R E = supportColumnSpan ev R E') :
    E = E' := by
  by_contra hne
  have hnsub : ¬ E' ⊆ E := by
    intro hsub
    have heq : E' = E := Finset.eq_of_subset_of_card_le hsub (by omega)
    exact hne heq.symm
  obtain ⟨x, hxE', hxE⟩ : ∃ x, x ∈ E' ∧ x ∉ E := by
    by_contra h
    apply hnsub
    intro x hxE'
    by_contra hxE
    apply h
    exact ⟨x, hxE', hxE⟩
  have hss : E ⊂ E ∪ E' := Finset.ssubset_iff_subset_ne.mpr
    ⟨Finset.subset_union_left, by
      intro heq
      apply hxE
      rw [heq]
      exact Finset.mem_union_right E hxE'⟩
  have hunion : R ≤ (E ∪ E').card := by
    have hlt := Finset.card_lt_card hss
    omega
  obtain ⟨T, hTsub, hTcard⟩ :=
    Finset.exists_subset_card_eq (s := E ∪ E') (n := R) hunion
  have hTtop : supportColumnSpan ev R T = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    rw [supportColumnSpan_finrank ev hev R T (by omega), hTcard,
      Module.finrank_fin_fun F]
  have hTE : supportColumnSpan ev R T ≤ supportColumnSpan ev R E := by
    apply Submodule.span_le.mpr
    rintro y ⟨t, rfl⟩
    have htunion := hTsub t.2
    rw [Finset.mem_union] at htunion
    rcases htunion with htE | htE'
    · exact Submodule.subset_span ⟨⟨t.1, htE⟩, rfl⟩
    · rw [hspan]
      exact Submodule.subset_span ⟨⟨t.1, htE'⟩, rfl⟩
  have hEtop : supportColumnSpan ev R E = ⊤ := by
    apply top_unique
    rw [← hTtop]
    exact hTE
  exact (ne_of_lt (supportColumnSpan_lt_top ev hev R E (by omega))) hEtop

/-- Distinct exact `(R-1)` supports have distinct syndrome hyperplanes. -/
theorem syndromeSpan_injective_of_card_eq
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (hR : 0 < R) {E E' : Finset D}
    (hE : E.card = R - 1) (hE' : E'.card = R - 1)
    (hspan : syndromeSpan (parityCheck ev R) (E : Set D) =
      syndromeSpan (parityCheck ev R) (E' : Set D)) :
    E = E' := by
  apply supportColumnSpan_injective_of_card_eq ev hev R hR hE hE'
  simpa only [syndromeSpan_parityCheck_eq_supportColumnSpan] using hspan

/-- The exact `(R-1)` supports have a family of nonzero functionals with
pairwise-distinct kernels equal to their syndrome spans. -/
theorem exists_distinct_supportHyperplanes
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (hR : 0 < R) :
    ∃ ell : {E : Finset D // E.card = R - 1} → (Fin R → F) →ₗ[F] F,
      (∀ E, ell E ≠ 0) ∧
      Function.Injective (fun E ↦ LinearMap.ker (ell E)) ∧
      (∀ E, syndromeSpan (parityCheck ev R) (E.1 : Set D) =
        LinearMap.ker (ell E)) := by
  classical
  choose ell hell hspan using fun E : {E : Finset D // E.card = R - 1} ↦
    exists_supportFunctional ev hev R hR E.1 E.2
  refine ⟨ell, hell, ?_, hspan⟩
  intro E E' hker
  apply Subtype.ext
  apply syndromeSpan_injective_of_card_eq ev hev R hR E.2 E'.2
  calc
    syndromeSpan (parityCheck ev R) (E.1 : Set D) =
        LinearMap.ker (ell E) := hspan E
    _ = LinearMap.ker (ell E') := hker
    _ = syndromeSpan (parityCheck ev R) (E'.1 : Set D) := (hspan E').symm

#print axioms syndromeSpan_parityCheck_eq_supportColumnSpan
#print axioms exists_supportFunctional
#print axioms syndromeSpan_injective_of_card_eq
#print axioms exists_distinct_supportHyperplanes

end GrandeFinale.RSSupportHyperplanes
