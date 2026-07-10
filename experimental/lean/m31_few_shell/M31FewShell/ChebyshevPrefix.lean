import M31FewShell.AffineFewInnerProduct

/-!
# Chebyshev-prefix rank and one-shell cap

This module formalizes section 3 of
`cap25_v13_m31_chebyshev_entropy_inverse_shells.md`.
-/

open scoped BigOperators
open Polynomial

namespace M31FewShell

noncomputable section

/-- Polynomials with nonzero, strictly increasing prescribed degrees are linearly independent. -/
theorem polynomial_prefix_linearIndependent {F : Type*} [Field F]
    (P : ℕ → F[X]) (hPne : ∀ j, P j ≠ 0)
    (hPdeg : ∀ j, (P j).natDegree = j) (r : ℕ) :
    LinearIndependent F (fun j : Fin r ↦ P j) := by
  induction r with
  | zero => exact linearIndependent_empty_type
  | succ r ihr =>
      rw [linearIndependent_fin_succ']
      constructor
      · simpa [Fin.init_def] using ihr
      · have hspan :
            Submodule.span F (Set.range (Fin.init (fun j : Fin (r + 1) ↦ P j))) ≤
              LinearMap.ker (Polynomial.lcoeff F r) := by
          rw [Submodule.span_le]
          rintro q ⟨j, rfl⟩
          change (P (j : ℕ)).coeff r = 0
          rw [Polynomial.coeff_eq_zero_of_natDegree_lt]
          simp [hPdeg j]
        have hlead := Polynomial.leadingCoeff_ne_zero.mpr (hPne r)
        change (P r).coeff (P r).natDegree ≠ 0 at hlead
        rw [hPdeg r] at hlead
        intro hmem
        have hzero := hspan hmem
        rw [LinearMap.mem_ker, Polynomial.lcoeff_apply] at hzero
        exact hlead hzero

/-- Evaluation of a polynomial on a finite family of field points, as a linear map. -/
def evalOn {F ι : Type*} [Field F] (x : ι → F) : F[X] →ₗ[F] (ι → F) :=
  LinearMap.pi (fun i ↦ Polynomial.leval (x i))

@[simp] theorem evalOn_apply {F ι : Type*} [Field F] (x : ι → F) (p : F[X]) (i : ι) :
    evalOn x p i = p.eval (x i) := rfl

/-- Independent degree-at-most-`w` polynomials remain independent on more than `w` points. -/
theorem evaluation_linearIndependent {F : Type*} [Field F]
    {n r w : ℕ} (x : Fin n → F) (hx : Function.Injective x)
    (P : Fin r → F[X]) (hP : LinearIndependent F P)
    (hPdeg : ∀ j, (P j).natDegree ≤ w) (hw : w < n) :
    LinearIndependent F (fun j ↦ evalOn x (P j)) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro c hc j
  let p : F[X] := ∑ j, c j • P j
  have hpdeg : p.natDegree ≤ w := by
    dsimp [p]
    apply Polynomial.natDegree_sum_le_of_forall_le
    intro i hi
    exact (Polynomial.natDegree_smul_le _ _).trans (hPdeg i)
  have hpeval : ∀ i, p.eval (x i) = 0 := by
    intro i
    have hi := congrFun hc i
    dsimp [p]
    rw [Polynomial.eval_finset_sum]
    simpa [Polynomial.eval_smul, evalOn_apply] using hi
  have hpzero : p = 0 :=
    Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero p hx hpeval
      (hpdeg.trans_lt (by simpa using hw))
  exact (Fintype.linearIndependent_iff.mp hP c (by simpa [p] using hpzero) j)

/-- Evaluation matrix with polynomial rows and point columns. -/
def evalMatrix {F : Type*} [Field F] {n r : ℕ}
    (x : Fin n → F) (P : Fin r → F[X]) : Matrix (Fin r) (Fin n) F :=
  fun j i ↦ (P j).eval (x i)

@[simp] theorem evalMatrix_row {F : Type*} [Field F] {n r : ℕ}
    (x : Fin n → F) (P : Fin r → F[X]) :
    (evalMatrix x P).row = fun j ↦ evalOn x (P j) := rfl

/-- The evaluation matrix has full row rank under the degree and distinctness hypotheses. -/
theorem evalMatrix_rank {F : Type*} [Field F]
    {n r w : ℕ} (x : Fin n → F) (hx : Function.Injective x)
    (P : Fin r → F[X]) (hP : LinearIndependent F P)
    (hPdeg : ∀ j, (P j).natDegree ≤ w) (hw : w < n) :
    (evalMatrix x P).rank = r := by
  simpa [evalMatrix_row] using
    (evaluation_linearIndependent x hx P hP hPdeg hw).rank_matrix

/-- The matrix of the Chebyshev prefix `T₀,…,T_w` evaluated on the domain points. -/
def chebyshevEvalMatrix (F : Type*) [Field F] [NeZero (2 : F)] {n : ℕ}
    (x : Fin n → F) (w : ℕ) : Matrix (Fin (w + 1)) (Fin n) F :=
  evalMatrix x (fun j ↦ Polynomial.Chebyshev.T F (j : ℕ))

set_option maxHeartbeats 800000 in
/-- The initial Chebyshev polynomials are linearly independent when `2 ≠ 0`. -/
theorem chebyshev_linearIndependent (F : Type*) [Field F] [NeZero (2 : F)] (r : ℕ) :
    LinearIndependent F (fun j : Fin r ↦ Polynomial.Chebyshev.T F (j : ℕ)) := by
  let P : ℕ → F[X] := fun j => Polynomial.Chebyshev.T F j
  have hPne : ∀ j, P j ≠ 0 := fun j => Polynomial.Chebyshev.T_ne_zero F j
  have hPdeg : ∀ j, (P j).natDegree = j := by
    intro j
    simp [P]
  simpa [P] using polynomial_prefix_linearIndependent P hPne hPdeg r

/-- Section 3 rank statement: the Chebyshev prefix matrix has rank `w+1`. -/
theorem chebyshevEvalMatrix_rank (F : Type*) [Field F] [NeZero (2 : F)]
    {n : ℕ} (x : Fin n → F) (hx : Function.Injective x) (w : ℕ) (hw : w < n) :
    (chebyshevEvalMatrix F x w).rank = w + 1 := by
  apply evalMatrix_rank x hx
      (fun j : Fin (w + 1) ↦ Polynomial.Chebyshev.T F (j : ℕ))
      (chebyshev_linearIndependent F (w + 1)) (w := w)
  · intro j
    have hdeg : (Polynomial.Chebyshev.T F (j : ℕ)).natDegree = (j : ℕ) := by
      simp
    rw [hdeg]
    omega
  · exact hw

/-- Section 3 fiber-direction statement: the prefix kernel has dimension `n-w-1`. -/
theorem chebyshevMoment_ker_finrank (F : Type*) [Field F] [NeZero (2 : F)]
    {n : ℕ} (x : Fin n → F) (hx : Function.Injective x) (w : ℕ) (hw : w < n) :
    Module.finrank F (LinearMap.ker (chebyshevEvalMatrix F x w).mulVecLin) = n - w - 1 := by
  have hrank := chebyshevEvalMatrix_rank F x hx w hw
  have hranknull := LinearMap.finrank_range_add_finrank_ker
    (chebyshevEvalMatrix F x w).mulVecLin
  rw [← Matrix.rank] at hranknull
  rw [hrank, Module.finrank_pi, Fintype.card_fin] at hranknull
  omega

/-- A kernel basis supplies the affine chart for a nonempty Chebyshev fiber. -/
private theorem chebyshevBooleanFiber_fewShell_cap_nonempty
    (p n w m : ℕ) [Fact p.Prime] [NeZero (2 : ZMod p)]
    (x : Fin n → ZMod p) (hx : Function.Injective x) (hw : w < n)
    {ι : Type*} [Fintype ι] [Nonempty ι]
    (A : ι → Finset (Fin n)) (hAinj : Function.Injective A)
    (hweight : ∀ i, (A i).card = m)
    (z : Fin (w + 1) → ZMod p)
    (hprefix : ∀ i,
      (chebyshevEvalMatrix (ZMod p) x w).mulVecLin
        (booleanIndicator (ZMod p) (A i)) = z)
    (hp : n < p) :
    Fintype.card ι ≤
      Nat.choose (n - w - 1 + (exchangeShells m A).card)
        (exchangeShells m A).card := by
  classical
  let T := chebyshevEvalMatrix (ZMod p) x w
  let L := T.mulVecLin
  let W := LinearMap.ker L
  let b := Module.finBasis (ZMod p) W
  let i0 : ι := Classical.choice inferInstance
  let ind : ι → Fin n → ZMod p :=
    fun i => booleanIndicator (ZMod p) (A i)
  let d : ι → Fin n → ZMod p := fun i => ind i - ind i0
  have hdmem (i : ι) : d i ∈ W := by
    change (chebyshevEvalMatrix (ZMod p) x w).mulVecLin (d i) = 0
    dsimp [d]
    rw [Matrix.mulVec_sub]
    have hi : (chebyshevEvalMatrix (ZMod p) x w).mulVec (ind i) = z := by
      simpa only [ind] using hprefix i
    have hi0 : (chebyshevEvalMatrix (ZMod p) x w).mulVec (ind i0) = z := by
      simpa only [ind] using hprefix i0
    rw [hi, hi0, sub_self]
  let dv : ι → W := fun i => ⟨d i, hdmem i⟩
  let u : ι → Fin (Module.finrank (ZMod p) W) → ZMod p :=
    fun i r => b.repr (dv i) r
  let coord : Fin n → MvPolynomial (Fin (Module.finrank (ZMod p) W)) (ZMod p) :=
    fun k => MvPolynomial.C (ind i0 k) +
      ∑ r, MvPolynomial.C ((b r).1 k) * MvPolynomial.X r
  have hcoord_deg : ∀ k, (coord k).totalDegree ≤ 1 := by
    intro k
    dsimp [coord]
    refine (MvPolynomial.totalDegree_add _ _).trans ?_
    apply max_le
    · simp
    · calc
        (∑ r, MvPolynomial.C ((b r).1 k) * MvPolynomial.X r).totalDegree ≤
            Finset.univ.sup (fun r =>
              (MvPolynomial.C ((b r).1 k) * MvPolynomial.X r).totalDegree) := by
          exact MvPolynomial.totalDegree_finset_sum _ _
        _ ≤ 1 := by
          apply Finset.sup_le
          intro r hr
          exact (MvPolynomial.totalDegree_mul _ _).trans (by simp)
  have hparam : ∀ i k, MvPolynomial.eval (u i) (coord k) = ind i k := by
    intro i k
    have hrecon := b.sum_repr (dv i)
    have hk := congrArg (fun q : W => (W.subtype q) k) hrecon
    simp only [map_sum, map_smul, Finset.sum_apply, Pi.smul_apply,
      smul_eq_mul] at hk
    have hsum : ∑ r, u i r * (b r).1 k = d i k := by
      simpa only [u, dv] using hk
    calc
      MvPolynomial.eval (u i) (coord k) =
          ind i0 k + ∑ r, (b r).1 k * u i r := by
        simp [coord]
      _ = ind i0 k + d i k := by
        congr 1
        rw [← hsum]
        apply Finset.sum_congr rfl
        intro r hr
        exact mul_comm _ _
      _ = ind i k := by
        change ind i0 k + (ind i k - ind i0 k) = ind i k
        abel
  have hbound := boolean_fixedWeight_affine_few_intersections
    p n (Module.finrank (ZMod p) W) m A hAinj hweight u coord
      hcoord_deg hparam hp
  have hdim : Module.finrank (ZMod p) W = n - w - 1 := by
    dsimp [W, L, T]
    exact chebyshevMoment_ker_finrank (ZMod p) x hx w hw
  rw [hdim] at hbound
  rw [exchangeShells_card_eq_intersectionShells A hweight]
  exact hbound

/--
End-to-end Chebyshev-prefix specialization for every fixed-weight Boolean
fiber.  Empty fibers are immediate; a nonempty fiber is charted by a basis of
the prefix kernel and passed to the polynomial-method theorem.
-/
theorem chebyshevBooleanFiber_fewShell_cap
    (p n w m : ℕ) [Fact p.Prime] [NeZero (2 : ZMod p)]
    (x : Fin n → ZMod p) (hx : Function.Injective x) (hw : w < n)
    {ι : Type*} [Fintype ι]
    (A : ι → Finset (Fin n)) (hAinj : Function.Injective A)
    (hweight : ∀ i, (A i).card = m)
    (z : Fin (w + 1) → ZMod p)
    (hprefix : ∀ i,
      (chebyshevEvalMatrix (ZMod p) x w).mulVecLin
        (booleanIndicator (ZMod p) (A i)) = z)
    (hp : n < p) :
    Fintype.card ι ≤
      Nat.choose (n - w - 1 + (exchangeShells m A).card)
        (exchangeShells m A).card := by
  classical
  rcases isEmpty_or_nonempty ι with hι | hι
  · letI := hι
    rw [Fintype.card_eq_zero]
    exact Nat.zero_le _
  · letI := hι
    exact chebyshevBooleanFiber_fewShell_cap_nonempty
      p n w m x hx hw A hAinj hweight z hprefix hp

/-- Source-facing form: at most `s` exchange shells give the `choose (N+s) s` cap. -/
theorem chebyshevBooleanFiber_atMostShells_cap
    (p n w m s : ℕ) [Fact p.Prime] [NeZero (2 : ZMod p)]
    (x : Fin n → ZMod p) (hx : Function.Injective x) (hw : w < n)
    {ι : Type*} [Fintype ι]
    (A : ι → Finset (Fin n)) (hAinj : Function.Injective A)
    (hweight : ∀ i, (A i).card = m)
    (z : Fin (w + 1) → ZMod p)
    (hprefix : ∀ i,
      (chebyshevEvalMatrix (ZMod p) x w).mulVecLin
        (booleanIndicator (ZMod p) (A i)) = z)
    (hp : n < p) (hshells : (exchangeShells m A).card ≤ s) :
    Fintype.card ι ≤ Nat.choose (n - w - 1 + s) s := by
  have hcap := chebyshevBooleanFiber_fewShell_cap
    p n w m x hx hw A hAinj hweight z hprefix hp
  calc
    Fintype.card ι ≤ Nat.choose
        (n - w - 1 + (exchangeShells m A).card)
        (exchangeShells m A).card := hcap
    _ = Nat.choose
        (n - w - 1 + (exchangeShells m A).card) (n - w - 1) :=
      Nat.choose_symm_add.symm
    _ ≤ Nat.choose (n - w - 1 + s) (n - w - 1) :=
      Nat.choose_le_choose (n - w - 1)
        (Nat.add_le_add_left hshells (n - w - 1))
    _ = Nat.choose (n - w - 1 + s) s := Nat.choose_symm_add

/-- End-to-end one-shell cap for a Boolean Chebyshev prefix fiber. -/
theorem chebyshevBooleanFiber_oneShell_cap
    (p n w m : ℕ) [Fact p.Prime] [NeZero (2 : ZMod p)]
    (x : Fin n → ZMod p) (hx : Function.Injective x) (hw : w < n)
    {ι : Type*} [Fintype ι]
    (A : ι → Finset (Fin n)) (hAinj : Function.Injective A)
    (hweight : ∀ i, (A i).card = m)
    (z : Fin (w + 1) → ZMod p)
    (hprefix : ∀ i,
      (chebyshevEvalMatrix (ZMod p) x w).mulVecLin
        (booleanIndicator (ZMod p) (A i)) = z)
    (hp : n < p) (hone : (exchangeShells m A).card = 1) :
    Fintype.card ι ≤ n - w := by
  have hcap := chebyshevBooleanFiber_fewShell_cap
    p n w m x hx hw A hAinj hweight z hprefix hp
  rw [hone] at hcap
  have hsub : n - w - 1 + 1 = n - w := by omega
  simpa [hsub] using hcap

/-- Conditional connector: rewrite an already established affine bound by the kernel dimension. -/
theorem chebyshevPrefix_fewShell_cap_of_affineBound
    (F : Type*) [Field F] [NeZero (2 : F)]
    {n : ℕ} (x : Fin n → F) (hx : Function.Injective x) (w : ℕ) (hw : w < n)
    (s familySize : ℕ)
    (hfamily : familySize ≤ Nat.choose
      (Module.finrank F (LinearMap.ker (chebyshevEvalMatrix F x w).mulVecLin) + s) s) :
    familySize ≤ Nat.choose (n - w - 1 + s) s := by
  rw [chebyshevMoment_ker_finrank F x hx w hw] at hfamily
  exact hfamily

/-- Conditional connector: one shell simplifies an already established affine bound to `n-w`. -/
theorem chebyshevPrefix_oneShell_cap_of_affineBound
    (F : Type*) [Field F] [NeZero (2 : F)]
    {n : ℕ} (x : Fin n → F) (hx : Function.Injective x) (w : ℕ) (hw : w < n)
    (familySize : ℕ)
    (hfamily : familySize ≤ Nat.choose
      (Module.finrank F (LinearMap.ker (chebyshevEvalMatrix F x w).mulVecLin) + 1) 1) :
    familySize ≤ n - w := by
  rw [chebyshevMoment_ker_finrank F x hx w hw] at hfamily
  have hsub : n - w - 1 + 1 = n - w := by omega
  simpa [hsub] using hfamily

/-- The deployed M31 one-shell cap is exactly `2,029,705`. -/
theorem m31_oneShell_cap_eq : 2097152 - 67447 = 2029705 := by norm_num

/-- The deployed one-shell cap lies below the budget `2^24-1`. -/
theorem m31_oneShell_cap_lt_budget : 2029705 < 16777215 := by norm_num

/-- Exact deployed one-shell headroom. -/
theorem m31_oneShell_headroom : 16777215 - 2029705 = 14747510 := by norm_num

#print axioms polynomial_prefix_linearIndependent
#print axioms evaluation_linearIndependent
#print axioms evalMatrix_rank
#print axioms chebyshev_linearIndependent
#print axioms chebyshevEvalMatrix_rank
#print axioms chebyshevMoment_ker_finrank
#print axioms chebyshevBooleanFiber_fewShell_cap
#print axioms chebyshevBooleanFiber_atMostShells_cap
#print axioms chebyshevBooleanFiber_oneShell_cap
#print axioms chebyshevPrefix_fewShell_cap_of_affineBound
#print axioms chebyshevPrefix_oneShell_cap_of_affineBound
#print axioms m31_oneShell_cap_eq
#print axioms m31_oneShell_cap_lt_budget
#print axioms m31_oneShell_headroom

end

end M31FewShell
