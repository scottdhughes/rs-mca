import GrandeFinale.CollisionAwarePole

/-!
# Weighted Vandermonde parity checks for Reed--Solomon evaluation codes

This module constructs the barycentric weighted Vandermonde columns used by
the exact first-adjacent-row argument. Every subfamily of at most `R` columns
is linearly independent, the height-`R` parity map is surjective, and Lagrange
interpolation identifies its kernel exactly with the existing Reed--Solomon
evaluation code when `k + R = |D|`.
-/

open Matrix Polynomial
open scoped Classical

noncomputable section

namespace GrandeFinale.RSParityKernel

variable {F : Type*} [Field F]

/-- The usual nonzero barycentric weight attached to an evaluation point. -/
def barycentricWeight {D : Type*} [Fintype D] [DecidableEq D]
    (ev : D → F) (d : D) : F :=
  (∏ e ∈ (Finset.univ : Finset D).erase d, (ev d - ev e))⁻¹

theorem barycentricWeight_ne_zero {D : Type*} [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev) (d : D) :
    barycentricWeight ev d ≠ 0 := by
  apply inv_ne_zero
  apply Finset.prod_ne_zero_iff.mpr
  intro e he
  apply sub_ne_zero.mpr
  apply hev.ne
  exact (Finset.mem_erase.mp he).1.symm

/-- The `d`th barycentric weighted Vandermonde column of height `R`. -/
def weightedColumn {D : Type*} [Fintype D] [DecidableEq D]
    (ev : D → F) (R : Nat) (d : D) : Fin R → F :=
  fun j ↦ barycentricWeight ev d * ev d ^ (j : Nat)

/-- Scaled Vandermonde columns at `t ≤ R` distinct points are independent. -/
theorem scaledColumns_linearIndependent {t R : Nat} (htR : t ≤ R)
    (y : Fin t → F) (hy : Function.Injective y)
    (rho : Fin t → F) (hrho : ∀ i, rho i ≠ 0) :
    LinearIndependent F
      (fun i : Fin t ↦ fun j : Fin R ↦ rho i * y i ^ (j : Nat)) := by
  rw [Fintype.linearIndependent_iff]
  intro c hc
  set d : Fin t → F := fun i ↦ c i * rho i with hd
  have hMv : (Matrix.vandermonde y)ᵀ *ᵥ d = 0 := by
    funext j
    have hj := congrFun hc (Fin.castLE htR j)
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hj
    simp only [Matrix.mulVec, dotProduct, Matrix.transpose_apply,
      Matrix.vandermonde_apply, Pi.zero_apply]
    rw [← hj]
    refine Finset.sum_congr rfl (fun i _ ↦ ?_)
    rw [hd, Fin.val_castLE]
    ring
  have hdet : (Matrix.vandermonde y)ᵀ.det ≠ 0 := by
    rw [Matrix.det_transpose]
    exact Matrix.det_vandermonde_ne_zero_iff.mpr hy
  have hd0 : d = 0 := Matrix.eq_zero_of_mulVec_eq_zero hdet hMv
  intro i
  have hi : c i * rho i = 0 := by
    have := congrFun hd0 i
    rwa [hd, Pi.zero_apply] at this
  exact (mul_eq_zero.mp hi).resolve_right (hrho i)

/-- Every at-most-`R` subfamily of the weighted columns is independent. -/
theorem weightedColumns_linearIndependent {D : Type*}
    [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (s : Finset D) (hsR : s.card ≤ R) :
    LinearIndependent F (fun d : s ↦ weightedColumn ev R d) := by
  let e := (Fintype.equivFin s).symm
  have hy : Function.Injective
      (fun i : Fin (Fintype.card s) ↦ ev (e i)) := by
    intro i j hij
    apply e.injective
    apply Subtype.ext
    exact hev hij
  apply (linearIndependent_equiv e).mp
  simpa [e, Function.comp_def, weightedColumn] using
    (scaledColumns_linearIndependent (by simpa using hsR)
      (fun i : Fin (Fintype.card s) ↦ ev (e i))
      hy
      (fun i : Fin (Fintype.card s) ↦ barycentricWeight ev (e i))
      (fun i ↦ barycentricWeight_ne_zero ev hev (e i)))

/-- The barycentric weighted Vandermonde parity-check map of height `R`. -/
def parityCheck {D : Type*} [Fintype D] [DecidableEq D]
    (ev : D → F) (R : Nat) : (D → F) →ₗ[F] (Fin R → F) :=
  Fintype.linearCombination F (weightedColumn ev R)

/-- If the evaluation domain contains at least `R` points, the weighted
Vandermonde parity-check map has full range. -/
theorem parityCheck_surjective {D : Type*} [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev)
    (R : Nat) (hR : R ≤ Fintype.card D) :
    Function.Surjective (parityCheck ev R) := by
  apply LinearMap.range_eq_top.mp
  rw [parityCheck, Fintype.range_linearCombination]
  obtain ⟨s, _hs, hscard⟩ :=
    Finset.exists_subset_card_eq
      (s := (Finset.univ : Finset D)) (n := R) (by simpa using hR)
  have hli : LinearIndependent F (fun d : s ↦ weightedColumn ev R d) :=
    weightedColumns_linearIndependent ev hev R s (by omega)
  have hfin : Module.finrank F
      (Submodule.span F (Set.range fun d : s ↦ weightedColumn ev R d)) = R := by
    rw [finrank_span_eq_card hli, Fintype.card_coe, hscard]
  have htop :
      Submodule.span F (Set.range fun d : s ↦ weightedColumn ev R d) = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    simpa using hfin
  apply top_unique
  rw [← htop]
  apply Submodule.span_mono
  rintro x ⟨d, rfl⟩
  exact ⟨d.1, rfl⟩

/-- Every degree-`< k` polynomial has vanishing weighted moment in each of the
`R` parity rows when `k + R = |D|`. -/
theorem weighted_eval_moment_eq_zero {D : Type*}
    [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (P : F[X]) (hP : P.degree < (k : WithBot Nat)) (j : Fin R) :
    ∑ d : D, P.eval (ev d) * barycentricWeight ev d * ev d ^ (j : Nat) = 0 := by
  classical
  by_cases hP0 : P = 0
  · subst P
    simp
  let Q : F[X] := P * Polynomial.X ^ (j : Nat)
  have hPnat : P.natDegree < k :=
    (Polynomial.natDegree_lt_iff_degree_lt hP0).mpr hP
  have hQnat : Q.natDegree ≤ P.natDegree + (j : Nat) := by
    change (P * (Polynomial.X : F[X]) ^ (j : Nat)).natDegree ≤
      P.natDegree + (j : Nat)
    calc
      (P * (Polynomial.X : F[X]) ^ (j : Nat)).natDegree ≤
          P.natDegree + ((Polynomial.X : F[X]) ^ (j : Nat)).natDegree :=
        Polynomial.natDegree_mul_le
      _ = P.natDegree + (j : Nat) := by rw [Polynomial.natDegree_X_pow]
  have hQnatCard : Q.natDegree < Fintype.card D := by
    calc
      Q.natDegree ≤ P.natDegree + (j : Nat) := hQnat
      _ < k + R := Nat.add_lt_add hPnat j.isLt
      _ = Fintype.card D := hsize
  have hQ0 : Q ≠ 0 := by
    exact mul_ne_zero hP0 (pow_ne_zero _ Polynomial.X_ne_zero)
  have hQdeg : Q.degree < (Fintype.card D : WithBot Nat) :=
    (Polynomial.natDegree_lt_iff_degree_lt hQ0).mp hQnatCard
  have hQcoeff : Q.coeff (Fintype.card D - 1) = 0 := by
    apply Polynomial.coeff_eq_zero_of_natDegree_lt
    exact hQnat.trans_lt (by omega)
  have hlag := Lagrange.coeff_eq_sum
    (s := (Finset.univ : Finset D)) (v := ev) (P := Q)
    hev.injOn (by simpa using hQdeg)
  have hlag' :
      (∑ d : D, Q.eval (ev d) /
        ∏ e ∈ (Finset.univ : Finset D).erase d, (ev d - ev e)) = 0 := by
    have := hlag.symm
    simpa [hQcoeff] using this
  simpa [Q, barycentricWeight, div_eq_mul_inv, mul_assoc, mul_left_comm,
    mul_comm] using hlag'

/-- Evaluation words of degree `< k` are annihilated by the weighted parity
map of complementary height `R`. -/
theorem parityCheck_eval_eq_zero {D : Type*}
    [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (P : F[X]) (hP : P.degree < (k : WithBot Nat)) :
    parityCheck ev R (fun d ↦ P.eval (ev d)) = 0 := by
  ext j
  simp only [parityCheck, Fintype.linearCombination_apply, Finset.sum_apply,
    Pi.smul_apply, smul_eq_mul, Pi.zero_apply, weightedColumn]
  simpa only [mul_assoc] using
    weighted_eval_moment_eq_zero ev hev k R hsize P hP j

/-- The Reed--Solomon evaluation code is contained in the kernel of its
barycentric weighted Vandermonde parity map. -/
theorem rsEval_le_ker_parityCheck {D : Type*}
    [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D) :
    GrandeFinale.CollisionAwarePole.rsEval ev k ≤
      LinearMap.ker (parityCheck ev R) := by
  intro u hu
  obtain ⟨P, hP, huP⟩ :=
    (GrandeFinale.CollisionAwarePole.mem_rsEval).mp hu
  change parityCheck ev R u = 0
  rw [show u = fun d ↦ P.eval (ev d) by funext d; exact huP d]
  exact parityCheck_eval_eq_zero ev hev k R hsize P hP

/-- Evaluation of an arbitrary polynomial on the indexed domain. -/
def polynomialEvaluation {D : Type*} (ev : D → F) :
    F[X] →ₗ[F] (D → F) :=
  LinearMap.pi (fun d : D ↦ Polynomial.leval (ev d))

/-- Evaluation restricted to polynomials of degree `< k`. -/
def degreeLTEvaluation {D : Type*} (ev : D → F) (k : Nat) :
    Polynomial.degreeLT F k →ₗ[F] (D → F) :=
  (polynomialEvaluation ev).comp (Polynomial.degreeLT F k).subtype

/-- Distinct evaluation points determine every polynomial of degree `< k`
once the domain has at least `k` points. -/
theorem degreeLTEvaluation_injective {D : Type*} [Fintype D]
    (ev : D → F) (hev : Function.Injective ev)
    (k : Nat) (hk : k ≤ Fintype.card D) :
    Function.Injective (degreeLTEvaluation ev k) := by
  intro P Q hPQ
  apply Subtype.ext
  apply Polynomial.eq_of_degrees_lt_of_eval_index_eq
    (s := (Finset.univ : Finset D)) hev.injOn
  · exact (Polynomial.mem_degreeLT.mp P.2).trans_le
      (WithBot.coe_le_coe.mpr hk)
  · exact (Polynomial.mem_degreeLT.mp Q.2).trans_le
      (WithBot.coe_le_coe.mpr hk)
  · intro d _hd
    have hd := congrFun hPQ d
    simpa [degreeLTEvaluation, polynomialEvaluation] using hd

/-- The range of restricted evaluation is definitionally the existing
Reed--Solomon evaluation code. -/
theorem range_degreeLTEvaluation_eq_rsEval {D : Type*} [Fintype D]
    (ev : D → F) (k : Nat) :
    LinearMap.range (degreeLTEvaluation ev k) =
      GrandeFinale.CollisionAwarePole.rsEval ev k := by
  rw [degreeLTEvaluation, LinearMap.range_comp, Submodule.range_subtype]
  rfl

/-- The injective length-`|D|` evaluation code of dimension parameter `k` has
finrank exactly `k`. -/
theorem finrank_rsEval {D : Type*} [Fintype D]
    (ev : D → F) (hev : Function.Injective ev)
    (k : Nat) (hk : k ≤ Fintype.card D) :
    Module.finrank F (GrandeFinale.CollisionAwarePole.rsEval ev k) = k := by
  rw [← range_degreeLTEvaluation_eq_rsEval ev k,
    LinearMap.finrank_range_of_inj (degreeLTEvaluation_injective ev hev k hk)]
  calc
    Module.finrank F (Polynomial.degreeLT F k) =
        Module.finrank F (Fin k → F) :=
      (Polynomial.degreeLTEquiv F k).finrank_eq
    _ = k := Module.finrank_fin_fun F

/-- The weighted Vandermonde map is an exact parity check for the injective
Reed--Solomon evaluation code. -/
theorem ker_parityCheck_eq_rsEval {D : Type*}
    [Fintype D] [DecidableEq D]
    (ev : D → F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D) :
    LinearMap.ker (parityCheck ev R) =
      GrandeFinale.CollisionAwarePole.rsEval ev k := by
  have hk : k ≤ Fintype.card D := by omega
  have hR : R ≤ Fintype.card D := by omega
  have hsurj : Function.Surjective (parityCheck ev R) :=
    parityCheck_surjective ev hev R hR
  have hrange : Module.finrank F (LinearMap.range (parityCheck ev R)) = R := by
    rw [LinearMap.range_eq_top.mpr hsurj, finrank_top]
    exact Module.finrank_fin_fun F
  have hdom : Module.finrank F (D → F) = Fintype.card D :=
    Module.finrank_pi F
  have hker : Module.finrank F (LinearMap.ker (parityCheck ev R)) = k := by
    have hnull := LinearMap.finrank_range_add_finrank_ker (parityCheck ev R)
    rw [hrange, hdom] at hnull
    omega
  apply (Submodule.eq_of_le_of_finrank_eq
    (rsEval_le_ker_parityCheck ev hev k R hsize) ?_).symm
  rw [finrank_rsEval ev hev k hk, hker]

#print axioms weightedColumns_linearIndependent
#print axioms parityCheck_surjective
#print axioms rsEval_le_ker_parityCheck
#print axioms ker_parityCheck_eq_rsEval

end GrandeFinale.RSParityKernel
