import GrandeFinale.ExactPrefixList

/-!
# Coefficient-prefix pigeonhole floor

This module formalizes the coefficient-prefix map and the literal finite
pigeonhole list-size floor in `prop:exact-prefix-list` of
`experimental/asymptotic_rs_mca_frontiers.tex`.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale.PrefixPigeonhole

variable {B : Type*} [Field B]

/-- Coefficients in degrees `K, ..., m - 1`, ordered from low to high. This is
the reverse ordering of the displayed leading-coefficient prefix in the
source. -/
def coefficientPrefix (K m : Nat) (P : B[X]) : Fin (m - K) → B :=
  fun i ↦ P.coeff (K + (i : Nat))

/-- The monic degree-`m` polynomial with prescribed coefficient prefix. -/
def prefixPolynomial (K m : Nat) (z : Fin (m - K) → B) : B[X] :=
  X ^ m + ∑ i, C (z i) * X ^ (K + (i : Nat))

/-- The family of `m`-subsets of `D` with coefficient prefix `z`. -/
def coefficientFiber
    (D : Finset B) (K m : Nat) (z : Fin (m - K) → B) : Finset (Finset B) :=
  (D.powersetCard m).filter fun S ↦
    coefficientPrefix K m (SP.locator S) = z

/-- The finite support family represented by the cancellation predicate used
by `ExactPrefixList.prefixSupportSet`. -/
def prefixSupportFinset
    (D : Finset B) (U : B[X]) (K m : Nat) : Finset (Finset B) :=
  (D.powersetCard m).filter fun S ↦
    (U - SP.locator S).degree < (K : WithBot Nat)

/-- The corresponding finite list of polynomials. -/
def listedPolynomials
    (D : Finset B) (U : B[X]) (K m : Nat) : Finset B[X] :=
  (prefixSupportFinset D U K m).image fun S ↦ U - SP.locator S

theorem prefixPolynomial_coeff_top
    (K m : Nat) (hKm : K ≤ m) (z : Fin (m - K) → B) :
    (prefixPolynomial K m z).coeff m = 1 := by
  simp only [prefixPolynomial, coeff_add, coeff_X_pow, finset_sum_coeff,
    coeff_C_mul]
  have hsum :
      (∑ i : Fin (m - K),
        if m = K + (i : Nat) then z i else (0 : B)) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    rw [if_neg]
    intro h
    have hi := i.isLt
    omega
  simp [hsum]

theorem prefixPolynomial_coeff_mid
    (K m : Nat) (hKm : K ≤ m) (z : Fin (m - K) → B)
    (i : Fin (m - K)) :
    (prefixPolynomial K m z).coeff (K + (i : Nat)) = z i := by
  simp only [prefixPolynomial, coeff_add, coeff_X_pow, finset_sum_coeff,
    coeff_C_mul]
  have hneTop : K + (i : Nat) ≠ m := by
    have hi := i.isLt
    omega
  rw [if_neg hneTop, zero_add, Finset.sum_eq_single i]
  · simp
  · intro j _ hji
    have hne : K + (i : Nat) ≠ K + (j : Nat) := by
      intro h
      apply hji
      ext
      omega
    rw [if_neg hne, mul_zero]
  · intro h
    exact absurd (Finset.mem_univ i) h

theorem prefixPolynomial_coeff_high
    (K m : Nat) (hKm : K ≤ m) (z : Fin (m - K) → B)
    {j : Nat} (hj : m < j) :
    (prefixPolynomial K m z).coeff j = 0 := by
  simp only [prefixPolynomial, coeff_add, coeff_X_pow, finset_sum_coeff,
    coeff_C_mul]
  have hneTop : j ≠ m := by omega
  rw [if_neg hneTop, zero_add]
  apply Finset.sum_eq_zero
  intro i _
  have hne : j ≠ K + (i : Nat) := by
    have hi := i.isLt
    omega
  simp [hne]

/-- The explicit prefix polynomial is monic of degree `m`. -/
theorem prefixPolynomial_isMonicOfDegree
    (K m : Nat) (hKm : K ≤ m) (z : Fin (m - K) → B) :
    (prefixPolynomial K m z).IsMonicOfDegree m := by
  rw [Polynomial.isMonicOfDegree_iff]
  refine ⟨?_, prefixPolynomial_coeff_top K m hKm z⟩
  rw [Polynomial.natDegree_le_iff_coeff_eq_zero]
  intro j hj
  exact prefixPolynomial_coeff_high K m hKm z hj

/-- The prescribed coordinates are exactly the prefix of the explicit monic
polynomial. -/
theorem coefficientPrefix_prefixPolynomial
    (K m : Nat) (hKm : K ≤ m) (z : Fin (m - K) → B) :
    coefficientPrefix K m (prefixPolynomial K m z) = z := by
  funext i
  exact prefixPolynomial_coeff_mid K m hKm z i

/-- Equality of the explicit coefficient prefixes is equivalent to the exact
leading-cancellation predicate used by the list correspondence. -/
theorem coefficientPrefix_eq_iff_degree_sub_lt
    {K m : Nat} {U : B[X]} (hU : U.IsMonicOfDegree m)
    {S : Finset B} (hScard : S.card = m) :
    coefficientPrefix K m U = coefficientPrefix K m (SP.locator S) ↔
      (U - SP.locator S).degree < (K : WithBot Nat) := by
  constructor
  · intro hprefix
    rw [Polynomial.degree_lt_iff_coeff_zero]
    intro j hj
    rw [coeff_sub]
    rcases lt_trichotomy j m with hjm | hjm | hjm
    · obtain ⟨i, hi⟩ : ∃ i : Fin (m - K), K + (i : Nat) = j := by
        refine ⟨⟨j - K, (Nat.sub_lt_sub_iff_right hj).2 hjm⟩, ?_⟩
        exact Nat.add_sub_of_le hj
      have hcoeff := congrFun hprefix i
      simpa [coefficientPrefix, hi] using sub_eq_zero.mpr hcoeff
    · subst j
      have hUtop : U.coeff m = 1 := by
        rw [← hU.natDegree_eq]
        exact hU.monic.coeff_natDegree
      have hStop : (SP.locator S).coeff m = 1 := by
        rw [← hScard, ← SP.locator_natDegree]
        exact (SP.locator_monic S).coeff_natDegree
      rw [hUtop, hStop, sub_self]
    · have hUzero : U.coeff j = 0 := by
        apply Polynomial.coeff_eq_zero_of_natDegree_lt
        rw [hU.natDegree_eq]
        exact hjm
      have hSzero : (SP.locator S).coeff j = 0 := by
        apply Polynomial.coeff_eq_zero_of_natDegree_lt
        rw [SP.locator_natDegree, hScard]
        exact hjm
      rw [hUzero, hSzero, sub_zero]
  · intro hdegree
    funext i
    have hzero :
        (U - SP.locator S).coeff (K + (i : Nat)) = 0 :=
      ((Polynomial.degree_lt_iff_coeff_zero _ _).mp hdegree)
        (K + (i : Nat)) (by omega)
    exact sub_eq_zero.mp (by simpa [coeff_sub] using hzero)

/-- Membership in the explicit coefficient fiber is exactly membership in the
cancellation-defined prefix-support family. -/
theorem mem_coefficientFiber_iff_mem_prefixSupportFinset
    (D : Finset B) {K m : Nat} (hKm : K ≤ m)
    (z : Fin (m - K) → B) (S : Finset B) :
    S ∈ coefficientFiber D K m z ↔
      S ∈ prefixSupportFinset D (prefixPolynomial K m z) K m := by
  simp only [coefficientFiber, prefixSupportFinset, Finset.mem_filter,
    Finset.mem_powersetCard]
  constructor
  · rintro ⟨⟨hSD, hScard⟩, hprefix⟩
    refine ⟨⟨hSD, hScard⟩, ?_⟩
    apply (coefficientPrefix_eq_iff_degree_sub_lt
      (prefixPolynomial_isMonicOfDegree K m hKm z) hScard).mp
    rw [coefficientPrefix_prefixPolynomial K m hKm z, hprefix]
  · rintro ⟨⟨hSD, hScard⟩, hdegree⟩
    refine ⟨⟨hSD, hScard⟩, ?_⟩
    have hprefix := (coefficientPrefix_eq_iff_degree_sub_lt
      (prefixPolynomial_isMonicOfDegree K m hKm z) hScard).mpr hdegree
    rw [coefficientPrefix_prefixPolynomial K m hKm z] at hprefix
    exact hprefix.symm

/-- The cancellation-defined finite support family represents exactly the set
used by `ExactPrefixList`. -/
theorem mem_prefixSupportFinset_iff
    (D : Finset B) (U : B[X]) (K m : Nat) (S : Finset B) :
    S ∈ prefixSupportFinset D U K m ↔
      S ∈ ExactPrefixList.prefixSupportSet D U K m := by
  simp only [prefixSupportFinset, ExactPrefixList.prefixSupportSet,
    Finset.mem_filter, Finset.mem_powersetCard, Set.mem_setOf_eq]
  constructor
  · rintro ⟨⟨hSD, hScard⟩, hdegree⟩
    exact ⟨hSD, hScard, hdegree⟩
  · rintro ⟨hSD, hScard, hdegree⟩
    exact ⟨⟨hSD, hScard⟩, hdegree⟩

/-- The finite polynomial list represents exactly the polynomial list set from
the exact correspondence. -/
theorem mem_listedPolynomials_iff
    (D : Finset B) (U : B[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m)
    (P : B[X]) :
    P ∈ listedPolynomials D U K m ↔
      P ∈ ExactPrefixList.listPolynomialSet D U K m := by
  constructor
  · intro hP
    obtain ⟨S, hS, rfl⟩ := Finset.mem_image.mp hP
    exact ExactPrefixList.prefixSupport_to_listPolynomial D U K m
      ((mem_prefixSupportFinset_iff D U K m S).mp hS)
  · intro hP
    obtain ⟨S, ⟨hS, hPform⟩, _⟩ :=
      (ExactPrefixList.listPolynomial_iff_existsUnique_prefixSupport
        D U hU hKpos hKm P).mp hP
    apply Finset.mem_image.mpr
    exact ⟨S, (mem_prefixSupportFinset_iff D U K m S).mpr hS, hPform.symm⟩

theorem coe_listedPolynomials_eq
    (D : Finset B) (U : B[X]) {K m : Nat}
    (hU : U.IsMonicOfDegree m) (hKpos : 0 < K) (hKm : K ≤ m) :
    (listedPolynomials D U K m : Set B[X]) =
      ExactPrefixList.listPolynomialSet D U K m := by
  ext P
  exact mem_listedPolynomials_iff D U hU hKpos hKm P

/-- Literal ceiling-form pigeonhole theorem for locator coefficient prefixes. -/
theorem exists_large_coefficientFiber
    [Fintype B] (D : Finset B) (K m : Nat) :
    ∃ z : Fin (m - K) → B,
      (D.card.choose m ⌈/⌉ (Fintype.card B) ^ (m - K)) ≤
        (coefficientFiber D K m z).card := by
  obtain ⟨z, _hzuniv, hz⟩ := GrandeFinale.prefix_witness_maxfiber
    (s := D.powersetCard m)
    (t := (Finset.univ : Finset (Fin (m - K) → B)))
    (f := fun S ↦ coefficientPrefix K m (SP.locator S))
    (fun _ _ ↦ Finset.mem_univ _)
    Finset.univ_nonempty
  refine ⟨z, ?_⟩
  rw [ceilDiv_le_iff_le_mul (by positivity)]
  simpa [coefficientFiber, Finset.card_powersetCard] using hz

/-- The explicit prefix polynomial has a complete finite list at least as
large as the literal coefficient-pigeonhole ceiling. -/
theorem prefixPolynomial_list_floor
    [Fintype B] (D : Finset B) {K m : Nat} (hKm : K ≤ m) :
    ∃ z : Fin (m - K) → B,
      (D.card.choose m ⌈/⌉ (Fintype.card B) ^ (m - K)) ≤
        (listedPolynomials D (prefixPolynomial K m z) K m).card := by
  obtain ⟨z, hz⟩ := exists_large_coefficientFiber D K m
  refine ⟨z, hz.trans_eq ?_⟩
  have hfiber :
      coefficientFiber D K m z =
        prefixSupportFinset D (prefixPolynomial K m z) K m := by
    ext S
    exact mem_coefficientFiber_iff_mem_prefixSupportFinset D hKm z S
  rw [hfiber, listedPolynomials]
  symm
  apply Finset.card_image_of_injOn
  intro S _ T _ hST
  apply SP.locator_injective
  exact sub_right_injective hST

/-- The list-size clause of `prop:exact-prefix-list`, with the manuscript's
literal ceiling represented by natural ceiling division. -/
theorem exists_prefix_list_floor
    [Fintype B] (D : Finset B) {K m : Nat}
    (hKpos : 0 < K) (hKm : K ≤ m) (_hmD : m ≤ D.card) :
    ∃ U : B[X], U.IsMonicOfDegree m ∧
      (D.card.choose m ⌈/⌉ (Fintype.card B) ^ (m - K)) ≤
        (ExactPrefixList.listPolynomialSet D U K m).ncard := by
  obtain ⟨z, hz⟩ := prefixPolynomial_list_floor D hKm
  let U := prefixPolynomial K m z
  have hU : U.IsMonicOfDegree m :=
    prefixPolynomial_isMonicOfDegree K m hKm z
  refine ⟨U, hU, ?_⟩
  have hset := coe_listedPolynomials_eq D U hU hKpos hKm
  rw [← hset, Set.ncard_coe_finset]
  exact hz

#print axioms coefficientPrefix_eq_iff_degree_sub_lt
#print axioms mem_coefficientFiber_iff_mem_prefixSupportFinset
#print axioms mem_listedPolynomials_iff
#print axioms exists_large_coefficientFiber
#print axioms prefixPolynomial_list_floor
#print axioms exists_prefix_list_floor

end GrandeFinale.PrefixPigeonhole
