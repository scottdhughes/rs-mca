import Mathlib

/-!
# Bounded multiplicity of an off-diagonal multiplicative-energy fiber

Over a field `K` in which `2, 3, 5` are invertible, fix `P D1 D3 D5 : K` with
`D1 ≠ 0`.  Consider quadruples `(x1, x2, x3, x4)` satisfying

* `x1 * x2 = P`  and  `x3 * x4 = P`,
* `(x1 + x2) - (x3 + x4) = D1`,
* `(x1^3 + x2^3) - (x3^3 + x4^3) = D3`,
* `(x1^5 + x2^5) - (x3^5 + x4^5) = D5`.

The main results are `OffdiagMultiplicity.solutions_finite` (the solution set is
finite) and `OffdiagMultiplicity.solutions_ncard_le` (its cardinality is `≤ 16`).

## Proof outline

With `s = x1 + x2`, `t = x3 + x4`, Newton's identities give
`x1^3 + x2^3 = s^3 - 3 P s` and `x1^5 + x2^5 = s^5 - 5 P s^3 + 5 P^2 s`
(and similarly for `x3, x4`).  Eliminating `P` from the three difference
equations produces a single quartic in `q := s + t = x1+x2+x3+x4`:

`45 D1^2 q^4 - (30 D1^4 + 60 D1 D3) q^2 + (D1^6 - 20 D1^3 D3 - 80 D3^2 + 144 D1 D5) = 0`,

with nonzero leading coefficient `45 D1^2` (`q_quartic`).  Hence `q` takes at most
`4` values.  For each `q`, the sum `s = (q + D1) / 2` is determined (`2` invertible),
so `x1` (resp. `x3`) is a root of the monic quadratic `X^2 - s X + P` (resp.
`X^2 - t X + P`), each with at most `2` roots, while `x2 = s - x1` and `x4 = t - x3`
are determined.  Thus the map `(x1,x2,x3,x4) ↦ (q, x1, x3)` is injective on the
solution set, with image inside a finite set of cardinality `≤ 4 * 2 * 2 = 16`.
-/

open Polynomial

namespace OffdiagMultiplicity

attribute [local instance] Classical.propDecidable

variable {K : Type*} [Field K]

/-- The four defining constraints for a quadruple `(x1, x2, x3, x4)` given the
fixed data `P, D1, D3, D5`. -/
def Constraints (P D1 D3 D5 x1 x2 x3 x4 : K) : Prop :=
  x1 * x2 = P ∧ x3 * x4 = P ∧
  (x1 + x2) - (x3 + x4) = D1 ∧
  (x1 ^ 3 + x2 ^ 3) - (x3 ^ 3 + x4 ^ 3) = D3 ∧
  (x1 ^ 5 + x2 ^ 5) - (x3 ^ 5 + x4 ^ 5) = D5

/-! ### The core algebraic identity -/

/-- **Core algebraic lemma.**  Under the constraints, the total sum
`q = x1 + x2 + x3 + x4` satisfies an explicit quartic with leading coefficient
`45 D1^2`.  This is a polynomial consequence of the equal-product condition
`x1 * x2 = x3 * x4` after eliminating `P` via Newton's identities. -/
lemma q_quartic {P D1 D3 D5 x1 x2 x3 x4 : K}
    (h : Constraints P D1 D3 D5 x1 x2 x3 x4) :
    45 * D1 ^ 2 * (x1 + x2 + x3 + x4) ^ 4
      - (30 * D1 ^ 4 + 60 * D1 * D3) * (x1 + x2 + x3 + x4) ^ 2
      + (D1 ^ 6 - 20 * D1 ^ 3 * D3 - 80 * D3 ^ 2 + 144 * D1 * D5) = 0 := by
  obtain ⟨hx12, hx34, hd1, hd3, hd5⟩ := h
  have hpp : x1 * x2 = x3 * x4 := hx12.trans hx34.symm
  subst hd1; subst hd3; subst hd5
  linear_combination
    (720 * (x1 + x2) * (x3 + x4) *
      (x1 ^ 2 + x1 * x2 + x2 ^ 2 - x3 ^ 2 - x3 * x4 - x4 ^ 2)) * hpp

/-! ### The quartic polynomial and its root count -/

/-- The quartic (as a polynomial in the total sum) forced by the constraints. -/
noncomputable def qPoly (D1 D3 D5 : K) : K[X] :=
  C (45 * D1 ^ 2) * X ^ 4
    + C (-(30 * D1 ^ 4 + 60 * D1 * D3)) * X ^ 2
    + C (D1 ^ 6 - 20 * D1 ^ 3 * D3 - 80 * D3 ^ 2 + 144 * D1 * D5)

lemma qPoly_coeff_four (D1 D3 D5 : K) : (qPoly D1 D3 D5).coeff 4 = 45 * D1 ^ 2 := by
  unfold qPoly
  simp only [coeff_add, coeff_C_mul, coeff_X_pow, coeff_C]
  norm_num

lemma qPoly_ne_zero {D1 D3 D5 : K} (h45 : (45 : K) ≠ 0) (hD1 : D1 ≠ 0) :
    qPoly D1 D3 D5 ≠ 0 := by
  intro h
  have hc := qPoly_coeff_four D1 D3 D5
  rw [h, coeff_zero] at hc
  exact (mul_ne_zero h45 (pow_ne_zero 2 hD1)) hc.symm

lemma qPoly_natDegree_le (D1 D3 D5 : K) : (qPoly D1 D3 D5).natDegree ≤ 4 := by
  unfold qPoly
  compute_degree!

lemma qPoly_roots_card_le (D1 D3 D5 : K) :
    (qPoly D1 D3 D5).roots.toFinset.card ≤ 4 :=
  (Multiset.toFinset_card_le _).trans
    ((Polynomial.card_roots' _).trans (qPoly_natDegree_le D1 D3 D5))

lemma qPoly_eval (D1 D3 D5 a : K) :
    (qPoly D1 D3 D5).eval a
      = 45 * D1 ^ 2 * a ^ 4 - (30 * D1 ^ 4 + 60 * D1 * D3) * a ^ 2
        + (D1 ^ 6 - 20 * D1 ^ 3 * D3 - 80 * D3 ^ 2 + 144 * D1 * D5) := by
  simp only [qPoly, eval_add, eval_mul, eval_C, eval_pow, eval_X]
  ring

/-! ### The quadratic factor and its root count -/

/-- The monic quadratic `X^2 - s X + p` whose roots recover an unordered pair with
sum `s` and product `p`. -/
noncomputable def quadFactor (s p : K) : K[X] := X ^ 2 - C s * X + C p

lemma quadFactor_coeff_two (s p : K) : (quadFactor s p).coeff 2 = 1 := by
  unfold quadFactor
  simp only [coeff_add, coeff_sub, coeff_C_mul, coeff_X_pow, coeff_X, coeff_C]
  norm_num

lemma quadFactor_ne_zero (s p : K) : quadFactor s p ≠ 0 := by
  intro h
  have hc := quadFactor_coeff_two s p
  rw [h, coeff_zero] at hc
  exact one_ne_zero hc.symm

lemma quadFactor_natDegree_le (s p : K) : (quadFactor s p).natDegree ≤ 2 := by
  unfold quadFactor
  compute_degree!

lemma quadFactor_roots_card_le (s p : K) :
    (quadFactor s p).roots.toFinset.card ≤ 2 :=
  (Multiset.toFinset_card_le _).trans
    ((Polynomial.card_roots' _).trans (quadFactor_natDegree_le s p))

lemma quadFactor_eval (s p a : K) : (quadFactor s p).eval a = a ^ 2 - s * a + p := by
  simp only [quadFactor, eval_add, eval_sub, eval_mul, eval_pow, eval_C, eval_X]

/-! ### The solution set, the injection, and the target finite set -/

/-- The set of solution quadruples, as a subset of `K⁴`. -/
def solutionSet (P D1 D3 D5 : K) : Set (K × K × K × K) :=
  {x | Constraints P D1 D3 D5 x.1 x.2.1 x.2.2.1 x.2.2.2}

/-- The map `(x1,x2,x3,x4) ↦ (x1+x2+x3+x4, x1, x3)`. -/
def sumFst3 : (K × K × K × K) → (K × K × K) :=
  fun x => (x.1 + x.2.1 + x.2.2.1 + x.2.2.2, x.1, x.2.2.1)

/-- The finite set that contains the image of the injection: for each root `Q` of
the quartic, the singleton `{Q}` paired with the (`≤ 2`)-element root sets of the
two quadratics `X^2 - ((Q±D1)/2) X + P`. -/
noncomputable def targetFinset (P D1 D3 D5 : K) : Finset (K × K × K) :=
  (qPoly D1 D3 D5).roots.toFinset.biUnion
    (fun Q => {Q} ×ˢ ((quadFactor ((Q + D1) / 2) P).roots.toFinset
                       ×ˢ (quadFactor ((Q - D1) / 2) P).roots.toFinset))

/-- `45 ≠ 0` follows from `3 ≠ 0` and `5 ≠ 0`. -/
lemma fortyfive_ne (h3 : (3 : K) ≠ 0) (h5 : (5 : K) ≠ 0) : (45 : K) ≠ 0 := by
  have h : (45 : K) = 3 * 3 * 5 := by norm_num
  rw [h]; exact mul_ne_zero (mul_ne_zero h3 h3) h5

lemma targetFinset_card_le {P D1 D3 D5 : K} :
    (targetFinset P D1 D3 D5).card ≤ 16 := by
  refine (Finset.card_biUnion_le).trans ?_
  refine (Finset.sum_le_sum (g := fun _ => 4) (fun Q _ => ?_)).trans ?_
  · rw [Finset.card_product, Finset.card_product, Finset.card_singleton, one_mul]
    calc (quadFactor ((Q + D1) / 2) P).roots.toFinset.card
            * (quadFactor ((Q - D1) / 2) P).roots.toFinset.card
        ≤ 2 * 2 :=
          Nat.mul_le_mul (quadFactor_roots_card_le _ _) (quadFactor_roots_card_le _ _)
      _ = 4 := by norm_num
  · rw [Finset.sum_const, smul_eq_mul]
    have hRq := qPoly_roots_card_le D1 D3 D5
    omega

lemma sumFst3_injOn {P D1 D3 D5 : K} (h2 : (2 : K) ≠ 0) :
    Set.InjOn (sumFst3 : (K × K × K × K) → _) (solutionSet P D1 D3 D5) := by
  rintro ⟨a1, a2, a3, a4⟩ ha ⟨b1, b2, b3, b4⟩ hb hab
  simp only [solutionSet, Set.mem_setOf_eq, Constraints] at ha hb
  obtain ⟨_, _, had1, _, _⟩ := ha
  obtain ⟨_, _, hbd1, _, _⟩ := hb
  simp only [sumFst3, Prod.mk.injEq] at hab
  obtain ⟨hsum, h1eq, h3eq⟩ := hab
  have ha2 : a2 = b2 := by
    have h : (2 : K) * a2 = 2 * b2 := by
      linear_combination hsum + had1 - hbd1 - 2 * h1eq
    exact mul_left_cancel₀ h2 h
  have ha4 : a4 = b4 := by linear_combination hsum - ha2 - h1eq - h3eq
  simp only [Prod.mk.injEq]
  exact ⟨h1eq, ha2, h3eq, ha4⟩

lemma image_subset_targetFinset {P D1 D3 D5 : K}
    (h2 : (2 : K) ≠ 0) (h3 : (3 : K) ≠ 0) (h5 : (5 : K) ≠ 0) (hD1 : D1 ≠ 0) :
    (sumFst3 : (K × K × K × K) → _) '' (solutionSet P D1 D3 D5)
      ⊆ ↑(targetFinset P D1 D3 D5) := by
  rintro _ ⟨⟨x1, x2, x3, x4⟩, hx, rfl⟩
  simp only [solutionSet, Set.mem_setOf_eq, Constraints] at hx
  obtain ⟨hx12, hx34, hxd1, hxd3, hxd5⟩ := hx
  have h45 : (45 : K) ≠ 0 := fortyfive_ne h3 h5
  rw [Finset.mem_coe]
  show ((x1 + x2 + x3 + x4, x1, x3) : K × K × K) ∈ targetFinset P D1 D3 D5
  unfold targetFinset
  rw [Finset.mem_biUnion]
  refine ⟨x1 + x2 + x3 + x4, ?_, ?_⟩
  · -- q = x1+x2+x3+x4 is a root of the quartic
    rw [Multiset.mem_toFinset, Polynomial.mem_roots']
    refine ⟨qPoly_ne_zero h45 hD1, ?_⟩
    show (qPoly D1 D3 D5).eval (x1 + x2 + x3 + x4) = 0
    rw [qPoly_eval]
    linear_combination q_quartic (P := P) ⟨hx12, hx34, hxd1, hxd3, hxd5⟩
  · refine Finset.mem_product.mpr
      ⟨Finset.mem_singleton.mpr rfl, Finset.mem_product.mpr ⟨?_, ?_⟩⟩
    · -- x1 is a root of X^2 - ((q+D1)/2) X + P
      rw [Multiset.mem_toFinset, Polynomial.mem_roots']
      refine ⟨quadFactor_ne_zero _ _, ?_⟩
      show (quadFactor ((x1 + x2 + x3 + x4 + D1) / 2) P).eval x1 = 0
      rw [quadFactor_eval]
      have hs : (x1 + x2 + x3 + x4 + D1) / 2 = x1 + x2 := by
        rw [div_eq_iff h2]; linear_combination -hxd1
      rw [hs, ← hx12]; ring
    · -- x3 is a root of X^2 - ((q-D1)/2) X + P
      rw [Multiset.mem_toFinset, Polynomial.mem_roots']
      refine ⟨quadFactor_ne_zero _ _, ?_⟩
      show (quadFactor ((x1 + x2 + x3 + x4 - D1) / 2) P).eval x3 = 0
      rw [quadFactor_eval]
      have ht : (x1 + x2 + x3 + x4 - D1) / 2 = x3 + x4 := by
        rw [div_eq_iff h2]; linear_combination hxd1
      rw [ht, ← hx34]; ring

/-! ### Main results -/

/-- **The solution set is finite.** -/
theorem solutions_finite {P D1 D3 D5 : K}
    (h2 : (2 : K) ≠ 0) (h3 : (3 : K) ≠ 0) (h5 : (5 : K) ≠ 0) (hD1 : D1 ≠ 0) :
    (solutionSet P D1 D3 D5).Finite :=
  Set.Finite.of_finite_image
    ((targetFinset P D1 D3 D5).finite_toSet.subset
      (image_subset_targetFinset h2 h3 h5 hD1))
    (sumFst3_injOn h2)

/-- **Bounded multiplicity: the off-diagonal fiber has at most `16` solutions.** -/
theorem solutions_ncard_le {P D1 D3 D5 : K}
    (h2 : (2 : K) ≠ 0) (h3 : (3 : K) ≠ 0) (h5 : (5 : K) ≠ 0) (hD1 : D1 ≠ 0) :
    (solutionSet P D1 D3 D5).ncard ≤ 16 := by
  have hinj := sumFst3_injOn (P := P) (D1 := D1) (D3 := D3) (D5 := D5) h2
  have himg := image_subset_targetFinset (P := P) (D1 := D1) (D3 := D3) (D5 := D5) h2 h3 h5 hD1
  calc (solutionSet P D1 D3 D5).ncard
      = (sumFst3 '' (solutionSet P D1 D3 D5)).ncard := hinj.ncard_image.symm
    _ ≤ (↑(targetFinset P D1 D3 D5) : Set (K × K × K)).ncard :=
        Set.ncard_le_ncard himg (targetFinset P D1 D3 D5).finite_toSet
    _ = (targetFinset P D1 D3 D5).card := Set.ncard_coe_finset _
    _ ≤ 16 := targetFinset_card_le

end OffdiagMultiplicity
