import Mathlib

/-!
# The affine few-inner-product polynomial method

This module formalizes section 2 of
`cap25_v13_m31_chebyshev_entropy_inverse_shells.md`.  The affine subspace is
presented by an explicit `N`-parameter affine chart: each ambient coordinate is
a multivariate polynomial of total degree at most one.
-/

open scoped BigOperators
open Classical

namespace M31FewShell

noncomputable section

/-! ## The exact dimension of the bounded-total-degree polynomial space -/

/-- Add one slack coordinate to turn a bounded sum into an exact sum. -/
private def boundedFunEquivSucc (N s : ℕ) :
    {f : Fin N → ℕ // (∑ i, f i) ≤ s} ≃
      {g : Fin (N + 1) → ℕ // ∑ i, g i = s} where
  toFun f :=
    ⟨Fin.cons (s - ∑ i, f.1 i) f.1, by
      simp only [Fin.sum_univ_succ, Fin.cons_zero, Fin.cons_succ]
      exact Nat.sub_add_cancel f.2⟩
  invFun g :=
    ⟨Fin.tail g.1, by
      change (∑ i : Fin N, g.1 i.succ) ≤ s
      have hg := g.2
      rw [Fin.sum_univ_succ] at hg
      omega⟩
  left_inv f := by
    apply Subtype.ext
    funext i
    rfl
  right_inv g := by
    apply Subtype.ext
    funext i
    refine Fin.cases ?_ (fun j => ?_) i
    · change s - ∑ j : Fin N, g.1 j.succ = g.1 0
      have hg := g.2
      rw [Fin.sum_univ_succ] at hg
      omega
    · rfl

/-- Bounded exponent vectors are multisets of size `s` after adding a slack symbol. -/
private noncomputable def boundedExponentEquiv (N s : ℕ) :
    {d : Fin N →₀ ℕ // d.sum (fun _ e => e) ≤ s} ≃ Sym (Fin (N + 1)) s :=
  (Finsupp.equivFunOnFinite.subtypeEquiv (by
      intro d
      simp [Finsupp.sum_fintype])).trans <|
    (boundedFunEquivSucc N s).trans <|
      (Sym.equivNatSumOfFintype (Fin (N + 1)) s).symm

/-- Exact stars-and-bars dimension: degree-at-most-`s` polynomials in `N` variables. -/
theorem finrank_restrictTotalDegree (K : Type*) [Field K] (N s : ℕ) :
    Module.finrank K (MvPolynomial.restrictTotalDegree (Fin N) K s) =
      (N + s).choose s := by
  let S : Set (Fin N →₀ ℕ) := {d | d.sum (fun _ e => e) ≤ s}
  let e : S ≃ Sym (Fin (N + 1)) s := by
    simpa [S] using boundedExponentEquiv N s
  letI : Fintype S :=
    Fintype.ofEquiv (Sym (Fin (N + 1)) s) e.symm
  change Module.finrank K
    (MvPolynomial.restrictSupport K S) = _
  rw [Module.finrank_eq_card_basis
    (MvPolynomial.basisRestrictSupport K S)]
  calc
    Fintype.card S =
        Fintype.card (Sym (Fin (N + 1)) s) := Fintype.card_congr e
    _ = (N + s).choose s := by
      rw [Sym.card_sym_eq_choose]
      simp

/-! ## Diagonal evaluation and the polynomial-method bound -/

/-- A diagonal, nonzero evaluation matrix makes a polynomial family independent. -/
theorem linearIndependent_of_diagonal_eval
    {K ι σ : Type*} [Field K] [Fintype ι]
    (P : ι → MvPolynomial σ K) (u : ι → σ → K)
    (hoff : ∀ i j, i ≠ j → MvPolynomial.eval (u j) (P i) = 0)
    (hdiag : ∀ i, MvPolynomial.eval (u i) (P i) ≠ 0) :
    LinearIndependent K P := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro c hc i
  have he := congrArg (MvPolynomial.eval (u i)) hc
  have he' : ∑ j, c j * MvPolynomial.eval (u i) (P j) = 0 := by
    simpa using he
  rw [Finset.sum_eq_single i] at he'
  · exact (mul_eq_zero.mp he').resolve_right (hdiag i)
  · intro j _ hji
    simp [hoff j i hji]
  · simp

/-- The abstract polynomial-method rank bound. -/
theorem card_le_choose_of_diagonal_eval
    {K ι : Type*} [Field K] [Fintype ι]
    (N s : ℕ) (P : ι → MvPolynomial (Fin N) K)
    (u : ι → Fin N → K)
    (hdeg : ∀ i, (P i).totalDegree ≤ s)
    (hoff : ∀ i j, i ≠ j → MvPolynomial.eval (u j) (P i) = 0)
    (hdiag : ∀ i, MvPolynomial.eval (u i) (P i) ≠ 0) :
    Fintype.card ι ≤ (N + s).choose s := by
  let Q : ι → MvPolynomial.restrictTotalDegree (Fin N) K s :=
    fun i => ⟨P i, (MvPolynomial.mem_restrictTotalDegree (Fin N) s (P i)).2 (hdeg i)⟩
  have hP : LinearIndependent K P :=
    linearIndependent_of_diagonal_eval P u hoff hdiag
  have hQ : LinearIndependent K Q := by
    apply LinearIndependent.of_comp
      (MvPolynomial.restrictTotalDegree (Fin N) K s).subtype
    simpa [Q] using hP
  calc
    Fintype.card ι ≤ Module.finrank K
        (MvPolynomial.restrictTotalDegree (Fin N) K s) :=
      hQ.fintype_card_le_finrank
    _ = (N + s).choose s := finrank_restrictTotalDegree K N s

/-! ## The explicit affine few-inner-product lemma -/

/-- Finite dot product. -/
def dot {K : Type*} [CommRing K] {n : ℕ} (x y : Fin n → K) : K :=
  ∑ k, x k * y k

/--
Affine few-inner-product lemma with the shells indexed before mapping to the
field.  The root map need not be injective; repeated modular roots are harmless.
-/
theorem affine_few_inner_products
    {K ι τ : Type*} [Field K] [Fintype ι] [DecidableEq τ]
    (n N : ℕ) (x : ι → Fin n → K) (u : ι → Fin N → K)
    (coord : Fin n → MvPolynomial (Fin N) K)
    (hcoord_deg : ∀ k, (coord k).totalDegree ≤ 1)
    (hparam : ∀ A k, MvPolynomial.eval (u A) (coord k) = x A k)
    (shells : Finset τ) (root : τ → K)
    (hoff : ∀ A B, A ≠ B → ∃ t ∈ shells, dot (x A) (x B) = root t)
    (hdiag : ∀ A t, t ∈ shells → dot (x A) (x A) ≠ root t) :
    Fintype.card ι ≤ (N + shells.card).choose shells.card := by
  classical
  let ell : ι → MvPolynomial (Fin N) K := fun A =>
    ∑ k, MvPolynomial.C (x A k) * coord k
  let sep : ι → MvPolynomial (Fin N) K := fun A =>
    ∏ t ∈ shells, (ell A - MvPolynomial.C (root t))
  have hell_eval (A B : ι) :
      MvPolynomial.eval (u B) (ell A) = dot (x A) (x B) := by
    simp [ell, dot, hparam]
  have hell_deg (A : ι) : (ell A).totalDegree ≤ 1 := by
    calc
      (ell A).totalDegree ≤
          Finset.univ.sup (fun k =>
            (MvPolynomial.C (x A k) * coord k).totalDegree) := by
        exact MvPolynomial.totalDegree_finset_sum _ _
      _ ≤ 1 := by
        apply Finset.sup_le
        intro k hk
        exact (MvPolynomial.totalDegree_mul _ _).trans (by
          simpa using hcoord_deg k)
  have hsep_deg (A : ι) : (sep A).totalDegree ≤ shells.card := by
    calc
      (sep A).totalDegree ≤
          ∑ t ∈ shells, (ell A - MvPolynomial.C (root t)).totalDegree := by
        exact MvPolynomial.totalDegree_finset_prod shells
          (fun t => ell A - MvPolynomial.C (root t))
      _ ≤ ∑ _t ∈ shells, 1 := by
        exact Finset.sum_le_sum fun t ht =>
          (MvPolynomial.totalDegree_sub_C_le (ell A) (root t)).trans (hell_deg A)
      _ = shells.card := by simp
  apply card_le_choose_of_diagonal_eval N shells.card sep u hsep_deg
  · intro A B hAB
    rcases hoff A B hAB with ⟨t, ht, hroot⟩
    simp only [sep, map_prod, map_sub, hell_eval, MvPolynomial.eval_C]
    exact Finset.prod_eq_zero ht (sub_eq_zero.mpr hroot)
  · intro A
    simp only [sep, map_prod, map_sub, hell_eval, MvPolynomial.eval_C]
    exact Finset.prod_ne_zero_iff.mpr fun t ht =>
      sub_ne_zero.mpr (hdiag A t ht)

/-! ## Exact Boolean fixed-weight wrapper (`p > n`) -/

/-- Indicator vector of a finite support. -/
def booleanIndicator (K : Type*) [Zero K] [One K] {n : ℕ}
    (A : Finset (Fin n)) : Fin n → K := fun k => if k ∈ A then 1 else 0

/-- The distinct off-diagonal intersection sizes of a support family. -/
noncomputable def intersectionShells {ι : Type*} [Fintype ι] {n : ℕ}
    (A : ι → Finset (Fin n)) : Finset ℕ := by
  classical
  exact Finset.univ.offDiag.image fun IJ => (A IJ.1 ∩ A IJ.2).card

/-- Fixed-weight exchange counts, written as `m - |A ∩ B|`. -/
noncomputable def exchangeShells {ι : Type*} [Fintype ι] {n : ℕ}
    (m : ℕ) (A : ι → Finset (Fin n)) : Finset ℕ :=
  (intersectionShells A).image fun t => m - t

/-- Every intersection shell of an `m`-set family is at most `m`. -/
theorem intersectionShell_le_weight {ι : Type*} [Fintype ι] {n m : ℕ}
    (A : ι → Finset (Fin n)) (hweight : ∀ i, (A i).card = m)
    {t : ℕ} (ht : t ∈ intersectionShells A) : t ≤ m := by
  rw [intersectionShells, Finset.mem_image] at ht
  rcases ht with ⟨IJ, hIJ, rfl⟩
  rw [← hweight IJ.1]
  exact Finset.card_le_card Finset.inter_subset_left

/-- On a fixed-weight family, exchange and intersection shells have equal cardinality. -/
theorem exchangeShells_card_eq_intersectionShells
    {ι : Type*} [Fintype ι] {n m : ℕ}
    (A : ι → Finset (Fin n)) (hweight : ∀ i, (A i).card = m) :
    (exchangeShells m A).card = (intersectionShells A).card := by
  classical
  rw [exchangeShells, Finset.card_image_iff]
  intro a ha b hb hab
  have ham : a ≤ m := intersectionShell_le_weight A hweight ha
  have hbm : b ≤ m := intersectionShell_le_weight A hweight hb
  exact (tsub_right_inj ham hbm).mp hab

/-- Dot product of Boolean indicators equals the intersection cardinality. -/
theorem dot_booleanIndicator (p n : ℕ) (A B : Finset (Fin n)) :
    dot (booleanIndicator (ZMod p) A) (booleanIndicator (ZMod p) B) =
      ((A ∩ B).card : ZMod p) := by
  classical
  calc
    dot (booleanIndicator (ZMod p) A) (booleanIndicator (ZMod p) B) =
        ∑ k, if k ∈ A ∧ k ∈ B then (1 : ZMod p) else 0 := by
      apply Finset.sum_congr rfl
      intro k hk
      by_cases hkA : k ∈ A <;> by_cases hkB : k ∈ B <;>
        simp [booleanIndicator, hkA, hkB]
    _ = ∑ k ∈ A ∩ B, (1 : ZMod p) := by
      rw [← Finset.sum_filter]
      apply Finset.sum_congr
      · ext k
        simp
      · simp
    _ = ((A ∩ B).card : ZMod p) := by simp

/--
The fixed-weight Boolean affine lemma.  Its shell set is the actual set of
off-diagonal intersection sizes, and `n < p` separates every diagonal factor.
-/
theorem boolean_fixedWeight_affine_few_intersections
    (p n N m : ℕ) [Fact p.Prime]
    {ι : Type*} [Fintype ι]
    (A : ι → Finset (Fin n)) (hAinj : Function.Injective A)
    (hweight : ∀ i, (A i).card = m)
    (u : ι → Fin N → ZMod p)
    (coord : Fin n → MvPolynomial (Fin N) (ZMod p))
    (hcoord_deg : ∀ k, (coord k).totalDegree ≤ 1)
    (hparam : ∀ i k, MvPolynomial.eval (u i) (coord k) =
      booleanIndicator (ZMod p) (A i) k)
    (hp : n < p) :
    Fintype.card ι ≤
      (N + (intersectionShells A).card).choose (intersectionShells A).card := by
  classical
  apply affine_few_inner_products n N
      (fun i => booleanIndicator (ZMod p) (A i)) u coord hcoord_deg hparam
      (intersectionShells A) (fun t : ℕ => (t : ZMod p))
  · intro i j hij
    refine ⟨(A i ∩ A j).card, ?_, dot_booleanIndicator p n (A i) (A j)⟩
    exact Finset.mem_image.mpr ⟨(i, j), by simp [hij], rfl⟩
  · intro i t ht
    have htlt : t < m := by
      rw [intersectionShells, Finset.mem_image] at ht
      rcases ht with ⟨IJ, hIJ, rfl⟩
      have hne : IJ.1 ≠ IJ.2 := by simpa using hIJ
      have hle : (A IJ.1 ∩ A IJ.2).card ≤ m := by
        rw [← hweight IJ.1]
        exact Finset.card_le_card Finset.inter_subset_left
      apply lt_of_le_of_ne hle
      intro heq
      have hinter : A IJ.1 ∩ A IJ.2 = A IJ.1 := by
        apply Finset.eq_of_subset_of_card_le Finset.inter_subset_left
        rw [hweight IJ.1]
        exact le_of_eq heq.symm
      have hsub : A IJ.1 ⊆ A IJ.2 := Finset.inter_eq_left.mp hinter
      have hset : A IJ.1 = A IJ.2 := by
        apply Finset.eq_of_subset_of_card_le hsub
        rw [hweight IJ.1, hweight IJ.2]
      exact hne (hAinj hset)
    rw [dot_booleanIndicator]
    simp only [Finset.inter_self]
    rw [hweight i]
    intro hcast
    have hmle : m ≤ n := by
      calc
        m = (A i).card := (hweight i).symm
        _ ≤ Fintype.card (Fin n) := Finset.card_le_univ (A i)
        _ = n := Fintype.card_fin n
    have hmP : m < p := lt_of_le_of_lt hmle hp
    have htP : t < p := lt_trans htlt hmP
    exact (ne_of_gt htlt)
      (CharP.natCast_injOn_Iio (ZMod p) p hmP htP hcast)

/-! ## Exact fixed signed-profile wrapper (`p > 2n`) -/

/-- An entrywise signed vector with fixed counts of `+1` and `-1`. -/
def SignedProfile {n : ℕ} (v : Fin n → ℤ) (npos nneg : ℕ) : Prop :=
  (∀ i, v i = -1 ∨ v i = 0 ∨ v i = 1) ∧
  (Finset.univ.filter fun i => v i = 1).card = npos ∧
  (Finset.univ.filter fun i => v i = -1).card = nneg

/-- Integer dot product, named separately for cast lemmas. -/
def intDot {n : ℕ} (x y : Fin n → ℤ) : ℤ := ∑ k, x k * y k

/-- A signed profile has norm equal to the number of nonzero entries. -/
theorem signedProfile_norm {n npos nneg : ℕ} {v : Fin n → ℤ}
    (hv : SignedProfile v npos nneg) :
    intDot v v = ((npos + nneg : ℕ) : ℤ) := by
  classical
  rcases hv with ⟨hentry, hpos, hneg⟩
  calc
    intDot v v = ∑ i,
        ((if v i = 1 then 1 else 0) + (if v i = -1 then 1 else 0) : ℤ) := by
      apply Finset.sum_congr rfl
      intro i hi
      rcases hentry i with hminus | hzero | hplus
      · simp [hminus]
      · simp [hzero]
      · simp [hplus]
    _ = ((Finset.univ.filter fun i => v i = 1).card : ℤ) +
        ((Finset.univ.filter fun i => v i = -1).card : ℤ) := by
      rw [Finset.sum_add_distrib]
      simp
    _ = ((npos + nneg : ℕ) : ℤ) := by
      rw [hpos, hneg]
      norm_num

/-- Distinct equal-norm signed vectors have an integral dot-product gap in `[1,2n]`. -/
theorem signed_fixedNorm_gap {n : ℕ} (x y : Fin n → ℤ)
    (hx : ∀ i, x i = -1 ∨ x i = 0 ∨ x i = 1)
    (hy : ∀ i, y i = -1 ∨ y i = 0 ∨ y i = 1)
    (a : ℤ) (hnormx : intDot x x = a) (hnormy : intDot y y = a)
    (hne : x ≠ y) :
    1 ≤ a - intDot x y ∧ a - intDot x y ≤ 2 * (n : ℤ) := by
  have hsq : ∑ i, (x i - y i) ^ 2 = 2 * (a - intDot x y) := by
    calc
      ∑ i, (x i - y i) ^ 2 =
          ∑ i, (x i * x i + y i * y i - 2 * (x i * y i)) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = intDot x x + intDot y y - 2 * intDot x y := by
        simp only [intDot, Finset.sum_sub_distrib, Finset.sum_add_distrib]
        rw [← Finset.mul_sum]
      _ = 2 * (a - intDot x y) := by
        rw [hnormx, hnormy]
        ring
  have hdiff : ∃ i, x i ≠ y i := by
    by_contra h
    push_neg at h
    exact hne (funext h)
  obtain ⟨j, hj⟩ := hdiff
  have hjone : 1 ≤ (x j - y j) ^ 2 := by
    have hpos : 0 < (x j - y j) ^ 2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hj)
    omega
  have hsingle : (x j - y j) ^ 2 ≤ ∑ i, (x i - y i) ^ 2 := by
    exact Finset.single_le_sum (fun i _ => sq_nonneg (x i - y i)) (Finset.mem_univ j)
  have hcoord (i : Fin n) : (x i - y i) ^ 2 ≤ 4 := by
    rcases hx i with hxminus | hxzero | hxplus <;>
      rcases hy i with hyminus | hyzero | hyplus <;>
      norm_num [*]
  have hupper : ∑ i, (x i - y i) ^ 2 ≤ 4 * (n : ℤ) := by
    calc
      ∑ i, (x i - y i) ^ 2 ≤ ∑ _i : Fin n, (4 : ℤ) :=
        Finset.sum_le_sum fun i _ => hcoord i
      _ = 4 * (n : ℤ) := by simp [mul_comm]
  have hlower : 1 ≤ ∑ i, (x i - y i) ^ 2 := hjone.trans hsingle
  rw [hsq] at hlower hupper
  constructor <;> omega

/-- Actual distinct off-diagonal integer dot products of a signed family. -/
noncomputable def signedDotShells {ι : Type*} [Fintype ι] {n : ℕ}
    (v : ι → Fin n → ℤ) : Finset ℤ := by
  classical
  exact Finset.univ.offDiag.image fun AB => intDot (v AB.1) (v AB.2)

/-- Casting commutes with the finite integer dot product. -/
theorem dot_intCast (p n : ℕ) (x y : Fin n → ℤ) :
    dot (fun i => (x i : ZMod p)) (fun i => (y i : ZMod p)) =
      (intDot x y : ZMod p) := by
  simp [dot, intDot]

/--
The signed fixed-profile affine lemma with its exact integer shell set.  The
hypothesis `2n < p` is used only to keep the positive diagonal gaps nonzero.
-/
theorem signed_fixedProfile_affine_few_inner_products
    (p n N npos nneg : ℕ) [Fact p.Prime]
    {ι : Type*} [Fintype ι]
    (v : ι → Fin n → ℤ) (hv_inj : Function.Injective v)
    (hprofile : ∀ A, SignedProfile (v A) npos nneg)
    (u : ι → Fin N → ZMod p)
    (coord : Fin n → MvPolynomial (Fin N) (ZMod p))
    (hcoord_deg : ∀ k, (coord k).totalDegree ≤ 1)
    (hparam : ∀ A k, MvPolynomial.eval (u A) (coord k) = (v A k : ZMod p))
    (hp : 2 * n < p) :
    Fintype.card ι ≤
      (N + (signedDotShells v).card).choose (signedDotShells v).card := by
  classical
  apply affine_few_inner_products n N
      (fun A k => (v A k : ZMod p)) u coord hcoord_deg hparam
      (signedDotShells v) (fun z : ℤ => (z : ZMod p))
  · intro A B hAB
    refine ⟨intDot (v A) (v B), ?_, dot_intCast p n (v A) (v B)⟩
    exact Finset.mem_image.mpr ⟨(A, B), by simp [hAB], rfl⟩
  · intro A z hz
    rw [signedDotShells, Finset.mem_image] at hz
    rcases hz with ⟨CD, hCD, rfl⟩
    have hCDne : CD.1 ≠ CD.2 := by simpa using hCD
    have hvne : v CD.1 ≠ v CD.2 := fun h => hCDne (hv_inj h)
    let a : ℤ := ((npos + nneg : ℕ) : ℤ)
    have hnormA : intDot (v A) (v A) = a := signedProfile_norm (hprofile A)
    have hnormC : intDot (v CD.1) (v CD.1) = a := signedProfile_norm (hprofile CD.1)
    have hnormD : intDot (v CD.2) (v CD.2) = a := signedProfile_norm (hprofile CD.2)
    have hgap := signed_fixedNorm_gap (v CD.1) (v CD.2)
      (hprofile CD.1).1 (hprofile CD.2).1 a hnormC hnormD hvne
    rw [dot_intCast]
    intro heq
    let g : ℤ := a - intDot (v CD.1) (v CD.2)
    have hg0 : 0 ≤ g := by dsimp [g]; omega
    have hgP : g < (p : ℤ) := by
      have hpz : 2 * (n : ℤ) < (p : ℤ) := by exact_mod_cast hp
      dsimp [g]
      omega
    have hcastzero : (g : ZMod p) = 0 := by
      dsimp [g]
      rw [Int.cast_sub, ← hnormA]
      exact sub_eq_zero.mpr heq
    have hzeroP : (0 : ℤ) < (p : ℤ) := lt_of_le_of_lt hg0 hgP
    have hgeq : g = 0 :=
      CharP.intCast_injOn_Ico (ZMod p) p ⟨hg0, hgP⟩ ⟨le_rfl, hzeroP⟩
        (by simpa using hcastzero)
    dsimp [g] at hgeq
    omega

#print axioms finrank_restrictTotalDegree
#print axioms linearIndependent_of_diagonal_eval
#print axioms card_le_choose_of_diagonal_eval
#print axioms affine_few_inner_products
#print axioms dot_booleanIndicator
#print axioms intersectionShell_le_weight
#print axioms exchangeShells_card_eq_intersectionShells
#print axioms boolean_fixedWeight_affine_few_intersections
#print axioms signedProfile_norm
#print axioms signed_fixedNorm_gap
#print axioms dot_intCast
#print axioms signed_fixedProfile_affine_few_inner_products

end

end M31FewShell
