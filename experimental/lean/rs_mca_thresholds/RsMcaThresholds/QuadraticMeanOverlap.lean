import RsMcaThresholds.HalfDistanceSparse
import AsymptoticRsMcaFrontiers.Tangent
import Mathlib.LinearAlgebra.Lagrange

/-!
# Quadratic mean-overlap compiler

This file formalizes the finite incidence mechanism MO5--MO6 behind
`thm:quadratic-mean-overlap` in `experimental/rs_mca_thresholds.tex`.
-/

open scoped BigOperators Classical

noncomputable section

namespace RsMcaThresholds
namespace QuadraticMeanOverlap

set_option autoImplicit false

open ExactSparsification

universe u v w

variable {D : Type v} [Fintype D] [DecidableEq D]

/-- Double count of incidences between coordinates and a finite support
family. -/
theorem sum_degrees_eq {ι : Type w} [Fintype ι] [DecidableEq ι]
    (S : ι → Finset D) :
    ∑ x : D, (Finset.univ.filter fun i : ι => x ∈ S i).card =
      ∑ i : ι, (S i).card := by
  simp only [Finset.card_filter]
  rw [Finset.sum_comm, Finset.sum_congr rfl]
  intro i hi
  simp

/-- Double count of squared coordinate degrees as ordered support
intersections. -/
theorem sum_degrees_sq_eq {ι : Type w} [Fintype ι] [DecidableEq ι]
    (S : ι → Finset D) :
    ∑ x : D, ((Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2 =
      ∑ i : ι, ∑ j : ι, (S i ∩ S j).card := by
  simp only [Finset.card_filter, pow_two]
  simp only [Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm, Finset.sum_congr rfl]
  intro i hi
  rw [Finset.sum_comm]
  simp [Finset.inter_comm]

omit [Fintype D] in
/-- Exact diagonal/off-diagonal decomposition of the ordered intersection
sum. -/
theorem sum_intersections_decompose {ι : Type w}
    [Fintype ι] [DecidableEq ι] (S : ι → Finset D) :
    (∑ i : ι, ∑ j : ι, (S i ∩ S j).card) =
      (∑ i : ι, (S i).card) +
        ∑ i : ι, ∑ j ∈ Finset.univ.erase i, (S i ∩ S j).card := by
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i hi
  rw [← Finset.sum_erase_add Finset.univ
    (fun j : ι => (S i ∩ S j).card) (Finset.mem_univ i)]
  simp [Finset.inter_self, add_comm]

omit [Fintype D] in
/-- MO5: if every distinct pair intersects in at most `b` coordinates, the
ordered off-diagonal intersection mass is at most `L(L-1)b`. -/
theorem offDiagonal_intersections_le {ι : Type w}
    [Fintype ι] [DecidableEq ι] (S : ι → Finset D) (b : ℕ)
    (hinter : ∀ i j : ι, i ≠ j → (S i ∩ S j).card ≤ b) :
    (∑ i : ι, ∑ j ∈ Finset.univ.erase i, (S i ∩ S j).card) ≤
      Fintype.card ι * (Fintype.card ι - 1) * b := by
  calc
    (∑ i : ι, ∑ j ∈ Finset.univ.erase i, (S i ∩ S j).card)
        ≤ ∑ i : ι, ∑ _j ∈ Finset.univ.erase i, b := by
          apply Finset.sum_le_sum
          intro i hi
          apply Finset.sum_le_sum
          intro j hj
          exact hinter i j (by simpa using (Finset.mem_erase.mp hj).1.symm)
    _ = Fintype.card ι * (Fintype.card ι - 1) * b := by
      simp [Finset.card_erase_of_mem, Finset.card_univ]
      ring

/-- Finite Cauchy--Schwarz for coordinate degrees, converted back to an exact
natural-number inequality. -/
theorem square_total_degrees_le {ι : Type w}
    [Fintype ι] [DecidableEq ι] (S : ι → Finset D) :
    (∑ x : D, (Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2 ≤
      Fintype.card D *
        ∑ x : D, ((Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2 := by
  have hcs := Finset.sum_mul_sq_le_sq_mul_sq
    (Finset.univ : Finset D)
    (fun _ : D => (1 : ℝ))
    (fun x : D =>
      ((Finset.univ.filter fun i : ι => x ∈ S i).card : ℝ))
  have hreal :
      ((∑ x : D,
        (Finset.univ.filter fun i : ι => x ∈ S i).card : ℕ) : ℝ) ^ 2 ≤
        (Fintype.card D : ℝ) *
          ((∑ x : D,
            ((Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2 : ℕ) : ℝ) := by
    simpa using hcs
  exact_mod_cast hreal

/-- MO5--MO6 overlap forcing. If there are at least `r+2` exact
`(n-r)`-supports, the quadratic condition and failure of the deep range force
two supports to overlap in at least `k+r` coordinates. -/
theorem exists_large_overlap {ι : Type w}
    [Fintype ι] [DecidableEq ι]
    (k r : ℕ) (hr : r ≤ Fintype.card D)
    (hsize : r + 2 ≤ Fintype.card ι)
    (hquad :
      Fintype.card D * (k + r) ≤ (Fintype.card D - r) ^ 2)
    (hnotdeep : Fintype.card D - k < 3 * r)
    (S : ι → Finset D)
    (hcard : ∀ i, (S i).card = Fintype.card D - r) :
    ∃ i j : ι, i ≠ j ∧ k + r ≤ (S i ∩ S j).card := by
  by_contra hlarge
  push_neg at hlarge
  let L := Fintype.card ι
  let n := Fintype.card D
  let a := n - r
  let b := k + r - 1
  have hLpos : 0 < L := by omega
  have hnpos : 0 < n := by omega
  have hkrpos : 0 < k + r := by omega
  have hinter : ∀ i j : ι, i ≠ j → (S i ∩ S j).card ≤ b := by
    intro i j hij
    have := hlarge i j hij
    omega
  have htotal :
      (∑ x : D, (Finset.univ.filter fun i : ι => x ∈ S i).card) =
        L * a := by
    rw [sum_degrees_eq]
    simp [hcard, L, a, n]
  have hsecond :
      (∑ x : D,
        ((Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2) ≤
        L * a + L * (L - 1) * b := by
    rw [sum_degrees_sq_eq, sum_intersections_decompose]
    apply Nat.add_le_add
    · simp [hcard, L, a, n]
    · exact offDiagonal_intersections_le S b hinter
  have hcauchy :
      (L * a) ^ 2 ≤ n * (L * a + L * (L - 1) * b) := by
    calc
      (L * a) ^ 2 =
          (∑ x : D,
            (Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2 := by
              rw [htotal]
      _ ≤ n * ∑ x : D,
          ((Finset.univ.filter fun i : ι => x ∈ S i).card) ^ 2 := by
            simpa [n] using square_total_degrees_le S
      _ ≤ n * (L * a + L * (L - 1) * b) :=
        Nat.mul_le_mul_left n hsecond
  have hlower :
      n * (L * (L * (k + r))) ≤ (L * a) ^ 2 := by
    calc
      n * (L * (L * (k + r)))
          = L ^ 2 * (n * (k + r)) := by ring
      _ ≤ L ^ 2 * a ^ 2 := Nat.mul_le_mul_left _ hquad
      _ = (L * a) ^ 2 := by ring
  have hchain :
      n * (L * (L * (k + r))) ≤
        n * (L * (a + (L - 1) * b)) := by
    calc
      n * (L * (L * (k + r))) ≤ (L * a) ^ 2 := hlower
      _ ≤ n * (L * a + L * (L - 1) * b) := hcauchy
      _ = n * (L * (a + (L - 1) * b)) := by ring
  have hcancelN :
      L * (L * (k + r)) ≤ L * (a + (L - 1) * b) :=
    Nat.le_of_mul_le_mul_left hchain hnpos
  have hcancelL :
      L * (k + r) ≤ a + (L - 1) * b :=
    Nat.le_of_mul_le_mul_left hcancelN hLpos
  have hkr : k + r = b + 1 := by
    exact (Nat.sub_add_cancel hkrpos).symm
  have hL : L = (L - 1) + 1 := by omega
  have hmul : L * b = (L - 1) * b + b := by
    calc
      L * b = ((L - 1) + 1) * b :=
        congrArg (fun x : ℕ => x * b) hL
      _ = (L - 1) * b + b := by rw [Nat.add_mul, one_mul]
  rw [hkr, Nat.mul_add, mul_one, hmul] at hcancelL
  dsimp only [L, n, a, b] at *
  omega


/-- The literal arithmetic inequality in MO2. For a common support of
cardinality `c`, the quotient by the required cancellation-cell size is at
most `r+1`. -/
theorem large_overlap_quotient_le (n r c : ℕ)
    (hc : c ≤ n) :
    (n - c) / max 1 (n - r - c) ≤ r + 1 := by
  by_cases hac : n - r ≤ c
  · have hzero : n - r - c = 0 := Nat.sub_eq_zero_of_le hac
    simp [hzero]
    omega
  · have hca : c < n - r := Nat.lt_of_not_ge hac
    have hxpos : 0 < n - r - c := Nat.sub_pos_of_lt hca
    have hformula : n - c = r + (n - r - c) := by omega
    rw [max_eq_right (by omega)]
    apply Nat.div_le_of_le_mul
    rw [hformula]
    have hrmul : r ≤ (n - r - c) * r := by
      calc
        r = 1 * r := by simp
        _ ≤ (n - r - c) * r := Nat.mul_le_mul_right r hxpos
    nlinarith

omit [Fintype D] in
/-- Disjoint cancellation cells inside a finite ambient set satisfy the exact
multiplicative packing bound. -/
theorem card_mul_le_of_disjoint_cells {ι : Type w}
    [Fintype ι] [DecidableEq ι]
    (U : Finset D) (A : ι → Finset D) (m : ℕ)
    (hsub : ∀ i, A i ⊆ U)
    (hdisj : (↑(Finset.univ : Finset ι) : Set ι).PairwiseDisjoint A)
    (hcard : ∀ i, m ≤ (A i).card) :
    Fintype.card ι * m ≤ U.card := by
  let V := (Finset.univ : Finset ι).biUnion A
  have hVsub : V ⊆ U := by
    intro x hx
    rcases Finset.mem_biUnion.mp hx with ⟨i, hi, hxi⟩
    exact hsub i hxi
  calc
    Fintype.card ι * m = ∑ _i : ι, m := by simp
    _ ≤ ∑ i : ι, (A i).card :=
      Finset.sum_le_sum fun i hi => hcard i
    _ = V.card := by
      simpa [V] using (Finset.card_biUnion hdisj).symm
    _ ≤ U.card := Finset.card_le_card hVsub

/-- Abstract MO2 collapse from the disjoint cancellation cells constructed by
the coding-theoretic large-overlap argument. -/
theorem large_overlap_collapse_from_cells {ι : Type w}
    [Fintype ι] [DecidableEq ι]
    (r c : ℕ) (hc : c ≤ Fintype.card D)
    (C₀ : Finset D) (hCcard : C₀.card = c)
    (A : ι → Finset D)
    (hsub : ∀ i, A i ⊆ (Finset.univ : Finset D) \ C₀)
    (hdisj : (↑(Finset.univ : Finset ι) : Set ι).PairwiseDisjoint A)
    (hcard : ∀ i,
      max 1 (Fintype.card D - r - c) ≤ (A i).card) :
    Fintype.card ι ≤ r + 1 := by
  let m := max 1 (Fintype.card D - r - c)
  have hmpos : 0 < m := by simp [m]
  have hpack :
      Fintype.card ι * m ≤ ((Finset.univ : Finset D) \ C₀).card :=
    card_mul_le_of_disjoint_cells
      ((Finset.univ : Finset D) \ C₀) A m hsub hdisj hcard
  have hambient :
      ((Finset.univ : Finset D) \ C₀).card =
        Fintype.card D - c := by
    rw [Finset.card_sdiff]
    simp [hCcard]
  have hdiv :
      Fintype.card ι ≤ (Fintype.card D - c) / m := by
    apply (Nat.le_div_iff_mul_le hmpos).2
    simpa [hambient] using hpack
  exact hdiv.trans (by
    simpa [m] using
      large_overlap_quotient_le (Fintype.card D) r c hc)

/-! ## Coding-theoretic compiler interfaces -/


variable {F : Type u}
variable [Field F] [Fintype F] [DecidableEq F]

local notation "Word" => D → F

/-- An exact support witness for one MCA-bad slope. -/
def ExactBadSupport (C : Submodule F Word) (f₀ f₁ : Word)
    (a : ℕ) (γ : F) (S : Finset D) : Prop :=
  S.card = a ∧
    GrandeFinale.Explained (C : Set Word)
      (fun x => f₀ x + γ * f₁ x) S ∧
    ¬ GrandeFinale.ExplainedPair (C : Set Word) f₀ f₁ S

/-- Exact-agreement reduction interface used in the paper before MO5. -/
def HasExactSupportReduction (C : Submodule F Word) (a : ℕ) : Prop :=
  ∀ f₀ f₁ : Word, ∀ γ : F,
    GrandeFinale.MCABad (C : Set Word) f₀ f₁ a γ →
      ∃ S : Finset D, ExactBadSupport C f₀ f₁ a γ S

/-- Abstract MDS information-set property: every `k`-set supports unique
interpolation by a codeword. -/
def HasMDSInformationSets (C : Submodule F Word) (k : ℕ) : Prop :=
  ∀ K : Finset D, K.card = k →
    (∀ f : Word, ∃ c ∈ C, ∀ x ∈ K, c x = f x) ∧
    (∀ c ∈ C, ∀ d ∈ C, (∀ x ∈ K, c x = d x) → c = d)

omit [Fintype D] [Fintype F] [DecidableEq F] in
/-- Reed--Solomon evaluation on an injective domain has the MDS
information-set property on every `k`-coordinate set. -/
theorem rs_hasMDSInformationSets (dom : D → F)
    (hdom : Function.Injective dom) (k : ℕ) :
    HasMDSInformationSets (RSCap.RSpolySubmodule dom k) k := by
  intro K hKcard
  have hdomK : Set.InjOn dom K := hdom.injOn
  constructor
  · intro f
    let Q : Polynomial F := Lagrange.interpolate K dom f
    refine ⟨fun x => Q.eval (dom x), ?_, ?_⟩
    · change (fun x => Q.eval (dom x)) ∈ RSCap.RSpoly dom k
      refine ⟨Q, ?_, fun _ => rfl⟩
      dsimp only [Q]
      simpa [hKcard] using Lagrange.degree_interpolate_lt f hdomK
    · intro x hx
      exact Lagrange.eval_interpolate_at_node f hdomK hx
  · intro c hc d hd hcd
    change c ∈ RSCap.RSpoly dom k at hc
    change d ∈ RSCap.RSpoly dom k at hd
    rcases hc with ⟨P, hPdeg, hPc⟩
    rcases hd with ⟨Q, hQdeg, hQc⟩
    have hPdegK : P.degree < K.card := by
      simpa [hKcard] using hPdeg
    have hQdegK : Q.degree < K.card := by
      simpa [hKcard] using hQdeg
    have hPQ : P = Q :=
      Polynomial.eq_of_degrees_lt_of_eval_index_eq K hdomK
        hPdegK hQdegK (by
          intro x hx
          rw [← hPc x, ← hQc x]
          exact hcd x hx)
    funext x
    rw [hPc x, hQc x, hPQ]

omit [Fintype F] [DecidableEq F] [Fintype D] in
/-- Shrink a non-explanation on a large support to an exact support of any
cardinality `a ≥ k+1`. -/
theorem not_explained_shrink_exact
    (C : Submodule F Word) (k a : ℕ)
    (hinfo : HasMDSInformationSets C k)
    (hk : k + 1 ≤ a)
    (f : Word) (S : Finset D) (ha : a ≤ S.card)
    (hnot : ¬ GrandeFinale.Explained (C : Set Word) f S) :
    ∃ T : Finset D, T ⊆ S ∧ T.card = a ∧
      ¬ GrandeFinale.Explained (C : Set Word) f T := by
  have hkS : k ≤ S.card := by omega
  obtain ⟨K, hKS, hKcard⟩ :=
    Finset.exists_subset_card_eq (s := S) hkS
  obtain ⟨c, hc, hcK⟩ := (hinfo K hKcard).1 f
  have hex : ∃ x ∈ S, c x ≠ f x := by
    by_contra h
    push_neg at h
    exact hnot ⟨c, hc, h⟩
  rcases hex with ⟨x, hxS, hcx⟩
  have hxK : x ∉ K := by
    intro hxK
    exact hcx (hcK x hxK)
  let A : Finset D := insert x K
  have hAS : A ⊆ S := by
    intro y hy
    rcases Finset.mem_insert.mp hy with rfl | hyK
    · exact hxS
    · exact hKS hyK
  have hAcard : A.card = k + 1 := by
    simp [A, Finset.card_insert_of_notMem hxK, hKcard]
  have hremain :
      a - A.card ≤ (S \ A).card := by
    have hsdiff : (S \ A).card = S.card - A.card := by
      rw [Finset.card_sdiff]
      simp [Finset.inter_eq_left.mpr hAS]
    rw [hsdiff]
    exact Nat.sub_le_sub_right ha A.card
  obtain ⟨U, hUsub, hUcard⟩ :=
    Finset.exists_subset_card_eq (s := S \ A) hremain
  let T : Finset D := A ∪ U
  have hdisj : Disjoint A U := by
    rw [Finset.disjoint_left]
    intro y hyA hyU
    exact (Finset.mem_sdiff.mp (hUsub hyU)).2 hyA
  have hTS : T ⊆ S := by
    intro y hy
    rcases Finset.mem_union.mp hy with hyA | hyU
    · exact hAS hyA
    · exact (Finset.mem_sdiff.mp (hUsub hyU)).1
  have hTcard : T.card = a := by
    rw [Finset.card_union_of_disjoint hdisj, hUcard]
    omega
  refine ⟨T, hTS, hTcard, ?_⟩
  intro hT
  rcases hT with ⟨d, hd, hdT⟩
  have hcdK : ∀ y ∈ K, c y = d y := by
    intro y hyK
    rw [hcK y hyK, hdT y]
    exact Finset.mem_union_left U (Finset.mem_insert_of_mem hyK)
  have hcd : c = d := (hinfo K hKcard).2 c hc d hd hcdK
  apply hcx
  rw [hcd]
  exact hdT x (Finset.mem_union_left U (Finset.mem_insert_self x K))

omit [Fintype D] [Fintype F] [DecidableEq F] in
/-- The MDS information-set property supplies the exact-agreement reduction
interface used before MO5. -/
theorem hasExactSupportReduction_of_informationSets
    (C : Submodule F Word) (k a : ℕ)
    (hinfo : HasMDSInformationSets C k) (hk : k + 1 ≤ a) :
    HasExactSupportReduction C a := by
  intro f₀ f₁ γ hbad
  rcases hbad with ⟨S, ha, hline, hpair⟩
  by_cases h₀ :
      GrandeFinale.Explained (C : Set Word) f₀ S
  · have h₁ :
        ¬ GrandeFinale.Explained (C : Set Word) f₁ S := by
      intro h₁
      rcases h₀ with ⟨c₀, hc₀, hc₀S⟩
      rcases h₁ with ⟨c₁, hc₁, hc₁S⟩
      exact hpair ⟨c₀, hc₀, c₁, hc₁, hc₀S, hc₁S⟩
    obtain ⟨T, hTS, hTcard, hTnot⟩ :=
      not_explained_shrink_exact C k a hinfo hk f₁ S ha h₁
    refine ⟨T, hTcard, ?_, ?_⟩
    · rcases hline with ⟨c, hc, hcS⟩
      exact ⟨c, hc, fun x hx => hcS x (hTS hx)⟩
    · intro hpairT
      rcases hpairT with ⟨c₀, hc₀, c₁, hc₁, hc₀T, hc₁T⟩
      exact hTnot ⟨c₁, hc₁, hc₁T⟩
  · obtain ⟨T, hTS, hTcard, hTnot⟩ :=
      not_explained_shrink_exact C k a hinfo hk f₀ S ha h₀
    refine ⟨T, hTcard, ?_, ?_⟩
    · rcases hline with ⟨c, hc, hcS⟩
      exact ⟨c, hc, fun x hx => hcS x (hTS hx)⟩
    · intro hpairT
      rcases hpairT with ⟨c₀, hc₀, c₁, hc₁, hc₀T, hc₁T⟩
      exact hTnot ⟨c₀, hc₀, hc₀T⟩

/-- Deep-range upper interface used for the `3r ≤ n-k` branch. -/
def HasDeepUpper (C : Submodule F Word) (k r : ℕ) : Prop :=
  3 * r ≤ Fintype.card D - k →
    ∀ f₀ f₁ : Word,
      (restrictedMCABadSlopes (Finset.univ : Finset F) C f₀ f₁
        (Fintype.card D - r)).card ≤ r + 1

/-- The previously formalized exact deep-regime theorem discharges the
MO4 deep interface for an injective Reed--Solomon evaluation code. -/
theorem rs_hasDeepUpper (dom : D → F)
    (hdom : Function.Injective dom) (k r : ℕ)
    (hk : k ≤ Fintype.card D) (hn : 0 < Fintype.card D)
    (hr : r ≤ Fintype.card D) :
    HasDeepUpper (RSCap.RSpolySubmodule dom k) k r := by
  intro hdeep f₀ f₁
  have hB :
      GrandeFinale.B_MCA
          ((RSCap.RSpolySubmodule dom k : Submodule F Word) : Set Word)
          (Fintype.card D - r) ≤ r + 1 := by
    have hraw :=
      AsymptoticRsMcaFrontiers.Deep.B_MCA_le_deep
        (RSCap.RSpolySubmodule dom k)
        (d := Fintype.card D + 1 - k)
        (a := Fintype.card D - r)
        (RSCap.rs_min_weight dom hdom k) hn (Nat.sub_le _ _) (by omega)
    simpa [Nat.sub_sub_self hr] using hraw
  calc
    (restrictedMCABadSlopes (Finset.univ : Finset F)
        (RSCap.RSpolySubmodule dom k) f₀ f₁
        (Fintype.card D - r)).card
        ≤ GrandeFinale.B_MCA
            ((RSCap.RSpolySubmodule dom k : Submodule F Word) : Set Word)
            (Fintype.card D - r) := by
          exact Finset.le_sup
            (f := fun p : Word × Word =>
              ((Finset.univ : Finset F).filter fun γ =>
                GrandeFinale.MCABad
                  ((RSCap.RSpolySubmodule dom k : Submodule F Word) : Set Word)
                  p.1 p.2 (Fintype.card D - r) γ).card)
            (Finset.mem_univ (f₀, f₁))
    _ ≤ r + 1 := hB

/-- Large-overlap collapse interface MO1--MO2. Its conclusion is the full-field
bad-slope bound, so every challenge restriction inherits it. -/
def HasLargeOverlapCollapse (C : Submodule F Word) (k r : ℕ) : Prop :=
  ∀ f₀ f₁ : Word, ∀ γ η : F, ∀ S T : Finset D,
    γ ≠ η →
    ExactBadSupport C f₀ f₁ (Fintype.card D - r) γ S →
    ExactBadSupport C f₀ f₁ (Fintype.card D - r) η T →
    k + r ≤ (S ∩ T).card →
      (restrictedMCABadSlopes (Finset.univ : Finset F) C f₀ f₁
        (Fintype.card D - r)).card ≤ r + 1

/-- The MDS information-set property plus exact-support reduction proves the
large-overlap collapse interface MO1--MO2. -/
theorem hasLargeOverlapCollapse_of_informationSets
    (C : Submodule F Word) (k r : ℕ)
    (hr : r ≤ Fintype.card D)
    (hinfo : HasMDSInformationSets C k)
    (hexact : HasExactSupportReduction C (Fintype.card D - r)) :
    HasLargeOverlapCollapse C k r := by
  intro f₀ f₁ z w S T hzw hz hw hinter
  rcases hz with ⟨hScard, ⟨pZ, hpZC, hpZS⟩, hpairS⟩
  rcases hw with ⟨hTcard, ⟨pW, hpWC, hpWT⟩, hpairT⟩
  let c₁ : Word := (z - w)⁻¹ • (pZ - pW)
  let c₀ : Word := pZ - z • c₁
  have hc₁C : c₁ ∈ C :=
    C.smul_mem _ (C.sub_mem hpZC hpWC)
  have hc₀C : c₀ ∈ C :=
    C.sub_mem hpZC (C.smul_mem z hc₁C)
  have hcommonOn :
      ∀ x ∈ S ∩ T, c₀ x = f₀ x ∧ c₁ x = f₁ x := by
    intro x hx
    have hxS := (Finset.mem_inter.mp hx).1
    have hxT := (Finset.mem_inter.mp hx).2
    have hpZx := hpZS x hxS
    have hpWx := hpWT x hxT
    have hc₁x : c₁ x = f₁ x := by
      change (z - w)⁻¹ * (pZ x - pW x) = f₁ x
      rw [hpZx, hpWx]
      field_simp [sub_ne_zero.mpr hzw]
      ring
    have hc₀x : c₀ x = f₀ x := by
      change pZ x - z * c₁ x = f₀ x
      rw [hpZx, hc₁x]
      ring
    exact ⟨hc₀x, hc₁x⟩
  let C₀ : Finset D :=
    Finset.univ.filter fun x => c₀ x = f₀ x ∧ c₁ x = f₁ x
  have hSTsub : S ∩ T ⊆ C₀ := by
    intro x hx
    simp only [C₀, Finset.mem_filter, Finset.mem_univ, true_and]
    exact hcommonOn x hx
  have hC₀lower : k + r ≤ C₀.card :=
    hinter.trans (Finset.card_le_card hSTsub)
  have hC₀card : C₀.card ≤ Fintype.card D := by
    simpa using Finset.card_le_univ C₀
  let Z : Finset F :=
    restrictedMCABadSlopes (Finset.univ : Finset F) C f₀ f₁
      (Fintype.card D - r)
  let support : Z → Finset D := fun u =>
    Classical.choose
      (hexact f₀ f₁ u.1 (Finset.mem_filter.mp u.2).2)
  have hsupport :
      ∀ u : Z,
        ExactBadSupport C f₀ f₁ (Fintype.card D - r) u.1
          (support u) := fun u =>
    Classical.choose_spec
      (hexact f₀ f₁ u.1 (Finset.mem_filter.mp u.2).2)
  let p : Z → Word := fun u => (hsupport u).2.1.choose
  have hpC : ∀ u : Z, p u ∈ C := fun u =>
    (hsupport u).2.1.choose_spec.1
  have hpSupport :
      ∀ u : Z, ∀ x ∈ support u,
        p u x = f₀ x + u.1 * f₁ x := fun u =>
    (hsupport u).2.1.choose_spec.2
  have hpEq :
      ∀ u : Z, p u = c₀ + u.1 • c₁ := by
    intro u
    have hIcard : k ≤ (support u ∩ C₀).card := by
      have hunion :
          (support u ∪ C₀).card ≤ Fintype.card D := by
        simpa using Finset.card_le_univ (support u ∪ C₀)
      have hidentity :=
        Finset.card_union_add_card_inter (support u) C₀
      have hSu := (hsupport u).1
      omega
    obtain ⟨K, hKsub, hKcard⟩ :=
      Finset.exists_subset_card_eq
        (s := support u ∩ C₀) hIcard
    have hcandC : c₀ + u.1 • c₁ ∈ C :=
      C.add_mem hc₀C (C.smul_mem u.1 hc₁C)
    apply (hinfo K hKcard).2 (p u) (hpC u)
      (c₀ + u.1 • c₁) hcandC
    intro x hxK
    have hxI := hKsub hxK
    have hxSu := (Finset.mem_inter.mp hxI).1
    have hxC₀ := (Finset.mem_inter.mp hxI).2
    have hxcommon :=
      (Finset.mem_filter.mp hxC₀).2
    change p u x = c₀ x + u.1 * c₁ x
    rw [hpSupport u x hxSu, hxcommon.1, hxcommon.2]
  let cell : Z → Finset D := fun u => support u \ C₀
  have hcellSub :
      ∀ u : Z, cell u ⊆ (Finset.univ : Finset D) \ C₀ := by
    intro u x hx
    refine Finset.mem_sdiff.mpr ⟨Finset.mem_univ x, ?_⟩
    exact (Finset.mem_sdiff.mp hx).2
  have hcellNonempty : ∀ u : Z, (cell u).Nonempty := by
    intro u
    by_contra h
    rw [Finset.not_nonempty_iff_eq_empty] at h
    have hSuC₀ : support u ⊆ C₀ := by
      intro x hxSu
      by_contra hxC₀
      have hxcell : x ∈ cell u :=
        Finset.mem_sdiff.mpr ⟨hxSu, hxC₀⟩
      rw [h] at hxcell
      simp at hxcell
    apply (hsupport u).2.2
    refine ⟨c₀, hc₀C, c₁, hc₁C, ?_, ?_⟩
    · intro x hxSu
      exact (Finset.mem_filter.mp (hSuC₀ hxSu)).2.1
    · intro x hxSu
      exact (Finset.mem_filter.mp (hSuC₀ hxSu)).2.2
  have hcellCard :
      ∀ u : Z,
        max 1 (Fintype.card D - r - C₀.card) ≤ (cell u).card := by
    intro u
    apply max_le
    · exact (Finset.card_pos.mpr (hcellNonempty u))
    · have hsplit :=
        Finset.card_sdiff_add_card_inter (support u) C₀
      have hinterCard : (support u ∩ C₀).card ≤ C₀.card :=
        Finset.card_le_card (Finset.inter_subset_right)
      have hSu := (hsupport u).1
      dsimp only [cell]
      omega
  have hcellDisjoint :
      (↑(Finset.univ : Finset Z) : Set Z).PairwiseDisjoint cell := by
    intro u hu v hv huv
    change Disjoint (cell u) (cell v)
    rw [Finset.disjoint_left]
    intro x hxu hxv
    have hxuSu := (Finset.mem_sdiff.mp hxu).1
    have hxvSv := (Finset.mem_sdiff.mp hxv).1
    have hxuNot := (Finset.mem_sdiff.mp hxu).2
    have hueq :
        f₀ x + u.1 * f₁ x = c₀ x + u.1 * c₁ x := by
      calc
        f₀ x + u.1 * f₁ x = p u x :=
          (hpSupport u x hxuSu).symm
        _ = (c₀ + u.1 • c₁) x := congrFun (hpEq u) x
        _ = c₀ x + u.1 * c₁ x := rfl
    have hveq :
        f₀ x + v.1 * f₁ x = c₀ x + v.1 * c₁ x := by
      calc
        f₀ x + v.1 * f₁ x = p v x :=
          (hpSupport v x hxvSv).symm
        _ = (c₀ + v.1 • c₁) x := congrFun (hpEq v) x
        _ = c₀ x + v.1 * c₁ x := rfl
    have huvVal : u.1 ≠ v.1 := by
      intro h
      exact huv (Subtype.ext h)
    have hmul :
        (u.1 - v.1) * (f₁ x - c₁ x) = 0 := by
      linear_combination hueq - hveq
    have hres : f₁ x - c₁ x = 0 :=
      (mul_eq_zero.mp hmul).resolve_left (sub_ne_zero.mpr huvVal)
    have hc₁x : c₁ x = f₁ x := (sub_eq_zero.mp hres).symm
    rw [hc₁x] at hueq
    have hc₀x : c₀ x = f₀ x :=
      (add_right_cancel hueq).symm
    apply hxuNot
    simp only [C₀, Finset.mem_filter, Finset.mem_univ, true_and]
    exact ⟨hc₀x, hc₁x⟩
  have hcells :=
    large_overlap_collapse_from_cells r C₀.card hC₀card C₀ rfl
      cell hcellSub hcellDisjoint hcellCard
  simpa [Z] using hcells

/-- Universal tangent lower interface used for the equality in MO4. -/

def HasTangentLower (Γ : Finset F) (C : Submodule F Word) (r : ℕ) : Prop :=
  min Γ.card (r + 1) ≤
    B_MCA_challenge Γ C (Fintype.card D - r)

/-- The universal tangent construction supplies the MO4 lower interface for
Reed--Solomon codes in the exact-agreement range `k+1 ≤ n-r`. -/
theorem rs_hasTangentLower (Γ : Finset F) (dom : D → F)
    (hdom : Function.Injective dom) (k r : ℕ)
    (hr : r ≤ Fintype.card D)
    (hka : k + 1 ≤ Fintype.card D - r) :
    HasTangentLower Γ (RSCap.RSpolySubmodule dom k) r := by
  have hfloor :=
    AsymptoticRsMcaFrontiers.Tangent.tangent_floor
      (RSCap.RSpolySubmodule dom k) Γ
      (d := Fintype.card D + 1 - k)
      (a := Fintype.card D - r)
      (RSCap.rs_min_weight dom hdom k) (by omega)
      (Nat.sub_le _ _) (by omega)
  simpa [HasTangentLower, ExactSparsification.B_MCA_challenge,
    AsymptoticRsMcaFrontiers.Deep.B_MCA_challenge,
    ExactSparsification.restrictedMCABadSlopes,
    AsymptoticRsMcaFrontiers.Deep.challengeBadSlopes,
    Nat.sub_sub_self hr] using hfloor

omit [Fintype D] [DecidableEq D] [DecidableEq F] in
theorem restrictedMCA_subset_univ (Γ : Finset F)
    (C : Submodule F Word) (f₀ f₁ : Word) (a : ℕ) :
    restrictedMCABadSlopes Γ C f₀ f₁ a ⊆
      restrictedMCABadSlopes (Finset.univ : Finset F) C f₀ f₁ a := by
  intro γ hγ
  simp only [restrictedMCABadSlopes, Finset.mem_filter] at hγ ⊢
  exact ⟨Finset.mem_univ _, hγ.2⟩

/-- Challenge-restricted upper compiler from exact-support reduction,
deep-range control, large-overlap collapse, and the pure MO5--MO6 theorem. -/
theorem restrictedMCA_card_le_succ_of_quadratic
    (Γ : Finset F) (C : Submodule F Word) (k r : ℕ)
    (hr : r ≤ Fintype.card D)
    (hquad :
      Fintype.card D * (k + r) ≤ (Fintype.card D - r) ^ 2)
    (hexact : HasExactSupportReduction C (Fintype.card D - r))
    (hdeep : HasDeepUpper C k r)
    (hcollapse : HasLargeOverlapCollapse C k r)
    (f₀ f₁ : Word) :
    (restrictedMCABadSlopes Γ C f₀ f₁
      (Fintype.card D - r)).card ≤ r + 1 := by
  by_cases hdeepRange : 3 * r ≤ Fintype.card D - k
  · exact (Finset.card_le_card
      (restrictedMCA_subset_univ Γ C f₀ f₁
        (Fintype.card D - r))).trans
      (hdeep hdeepRange f₀ f₁)
  · let Z :=
      restrictedMCABadSlopes Γ C f₀ f₁ (Fintype.card D - r)
    change Z.card ≤ r + 1
    by_contra hlarge
    have hsize : r + 2 ≤ Z.card := by omega
    let support : Z → Finset D := fun z =>
      Classical.choose
        (hexact f₀ f₁ z.1 (Finset.mem_filter.mp z.2).2)
    have hsupport :
        ∀ z : Z,
          ExactBadSupport C f₀ f₁ (Fintype.card D - r) z.1
            (support z) := fun z =>
      Classical.choose_spec
        (hexact f₀ f₁ z.1 (Finset.mem_filter.mp z.2).2)
    have hover := exists_large_overlap k r hr
      (by simpa [Z] using hsize) hquad (by omega) support
      (fun z => (hsupport z).1)
    rcases hover with ⟨z, w, hzw, hinter⟩
    have hfull := hcollapse f₀ f₁ z.1 w.1 (support z) (support w)
      (by
        intro h
        apply hzw
        exact Subtype.ext h)
      (hsupport z) (hsupport w) hinter
    have hrestricted :
        Z.card ≤
          (restrictedMCABadSlopes (Finset.univ : Finset F) C f₀ f₁
            (Fintype.card D - r)).card :=
      Finset.card_le_card
        (restrictedMCA_subset_univ Γ C f₀ f₁
          (Fintype.card D - r))
    exact hlarge (hrestricted.trans hfull)

/-- Quadratic mean-overlap upper bound, including the challenge-card cap. -/
theorem quadratic_mean_overlap_upper
    (Γ : Finset F) (C : Submodule F Word) (k r : ℕ)
    (hr : r ≤ Fintype.card D)
    (hquad :
      Fintype.card D * (k + r) ≤ (Fintype.card D - r) ^ 2)
    (hexact : HasExactSupportReduction C (Fintype.card D - r))
    (hdeep : HasDeepUpper C k r)
    (hcollapse : HasLargeOverlapCollapse C k r) :
    B_MCA_challenge Γ C (Fintype.card D - r) ≤
      min Γ.card (r + 1) := by
  apply (Nat.le_min).2
  constructor
  · refine Finset.sup_le ?_
    intro p hp
    exact Finset.card_le_card (Finset.filter_subset _ _)
  · refine Finset.sup_le ?_
    intro p hp
    exact restrictedMCA_card_le_succ_of_quadratic Γ C k r hr hquad
      hexact hdeep hcollapse p.1 p.2

/-- Exact MO4 compiler. Once the three MDS upper interfaces and the universal
tangent floor are supplied, the challenge-restricted numerator is exactly
`min(|Γ|,r+1)`. -/
theorem quadratic_mean_overlap_exact
    (Γ : Finset F) (C : Submodule F Word) (k r : ℕ)
    (hr : r ≤ Fintype.card D)
    (hquad :
      Fintype.card D * (k + r) ≤ (Fintype.card D - r) ^ 2)
    (hexact : HasExactSupportReduction C (Fintype.card D - r))
    (hdeep : HasDeepUpper C k r)
    (hcollapse : HasLargeOverlapCollapse C k r)
    (htangent : HasTangentLower Γ C r) :
    B_MCA_challenge Γ C (Fintype.card D - r) =
      min Γ.card (r + 1) := by
  apply le_antisymm
  · exact quadratic_mean_overlap_upper Γ C k r hr hquad
      hexact hdeep hcollapse
  · exact htangent

/-- Exact quadratic mean-overlap theorem MO4 for an injective Reed--Solomon
evaluation code. All abstract compiler inputs are discharged here. -/
theorem rs_quadratic_mean_overlap_exact
    (Γ : Finset F) (dom : D → F) (hdom : Function.Injective dom)
    (k r : ℕ) (hr : r ≤ Fintype.card D)
    (hka : k + 1 ≤ Fintype.card D - r)
    (hquad :
      Fintype.card D * (k + r) ≤ (Fintype.card D - r) ^ 2) :
    B_MCA_challenge Γ (RSCap.RSpolySubmodule dom k)
        (Fintype.card D - r) = min Γ.card (r + 1) := by
  have hinfo :
      HasMDSInformationSets (RSCap.RSpolySubmodule dom k) k :=
    rs_hasMDSInformationSets dom hdom k
  have hexact :
      HasExactSupportReduction (RSCap.RSpolySubmodule dom k)
        (Fintype.card D - r) :=
    hasExactSupportReduction_of_informationSets
      (RSCap.RSpolySubmodule dom k) k (Fintype.card D - r) hinfo hka
  have hdeep :
      HasDeepUpper (RSCap.RSpolySubmodule dom k) k r :=
    rs_hasDeepUpper dom hdom k r (by omega) (by omega) hr
  have hcollapse :
      HasLargeOverlapCollapse (RSCap.RSpolySubmodule dom k) k r :=
    hasLargeOverlapCollapse_of_informationSets
      (RSCap.RSpolySubmodule dom k) k r hr hinfo hexact
  have htangent :
      HasTangentLower Γ (RSCap.RSpolySubmodule dom k) r :=
    rs_hasTangentLower Γ dom hdom k r hr hka
  exact quadratic_mean_overlap_exact Γ (RSCap.RSpolySubmodule dom k)
    k r hr hquad hexact hdeep hcollapse htangent

#print axioms exists_large_overlap
#print axioms quadratic_mean_overlap_upper
#print axioms quadratic_mean_overlap_exact
#print axioms rs_hasMDSInformationSets
#print axioms hasLargeOverlapCollapse_of_informationSets
#print axioms rs_quadratic_mean_overlap_exact

end QuadraticMeanOverlap
end RsMcaThresholds
