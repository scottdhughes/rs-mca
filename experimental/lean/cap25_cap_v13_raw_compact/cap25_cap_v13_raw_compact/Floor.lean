import Mathlib

/-!
# Reed–Solomon codes, list decoding, and the identity-prefix floor

This file develops the *structural* theory behind the deployed unsafe certificates of
the paper "The Reed–Solomon MCA Frontier for the Proximity Prize":

* Reed–Solomon codes `RS[F, D, K]` as evaluation words `D → F`;
* the list `List(C, 1 - m/n, U)` at agreement threshold `m`;
* the **identity-prefix floor lemma** (`RSMCA.identity_floor`): a `𝔹`-valued received
  word whose list is at least `⌊binom(n,m) / |𝔹|^{m-K}⌋`.

Throughout, `𝔹 ⊆ 𝔽` are finite fields modelled by an algebra `[Algebra B F]` of finite
fields (the base field `B` and the sampling field `F`), and `D : Finset B` is the
evaluation domain (`D ⊆ 𝔹`), of size `n = D.card`.
-/

open Polynomial Finset

namespace RSMCA

variable {B F : Type*} [Field B] [Field F] [Algebra B F]
  [Fintype B] [Fintype F] [DecidableEq F] [DecidableEq B]

/-- The Reed–Solomon code `RS[F, D, K]`: words `c : D → F` that are the evaluation on
`D` (viewed inside `F`) of some polynomial over `F` of degree `< K`. -/
def RS (D : Finset B) (K : ℕ) : Set (D → F) :=
  { c | ∃ P : F[X], P.degree < (K : WithBot ℕ) ∧
      ∀ x : D, c x = P.eval (algebraMap B F (x : B)) }

/-- Number of positions of `D` on which a codeword `c` agrees with the received word `U`. -/
def agreeCard {D : Finset B} (U c : D → F) : ℕ :=
  (Finset.univ.filter (fun x : D => c x = U x)).card

/-- The decoding list `List(RS[F,D,K], 1 - m/n, U)`: codewords agreeing with `U` on at
least `m` positions. -/
def listSet (D : Finset B) (K m : ℕ) (U : D → F) : Set (D → F) :=
  { c | c ∈ (RS D K : Set (D → F)) ∧ m ≤ agreeCard U c }

/-- The locator polynomial `Λ_M = ∏_{x ∈ M} (X - x)` over the base field `B`. -/
noncomputable def loc (M : Finset B) : B[X] := ∏ x ∈ M, (X - C x)

/-- The prefix of `Λ_M`: its coefficients at degrees `K, K+1, …, m-1`. -/
noncomputable def pre (K m : ℕ) (M : Finset B) : Fin (m - K) → B :=
  fun i => (loc M).coeff (K + (i : ℕ))

/-- The prefix received word polynomial `P_z = X^m + ∑_i z_i X^{K+i}`. -/
noncomputable def Pz (K m : ℕ) (z : Fin (m - K) → B) : B[X] :=
  X ^ m + ∑ i, C (z i) * X ^ (K + (i : ℕ))

/-- The candidate codeword polynomial `P_z - Λ_M` over `B`. -/
noncomputable def cpoly (K m : ℕ) (z : Fin (m - K) → B) (M : Finset B) : B[X] :=
  Pz K m z - loc M

/-- The `B`-valued received word associated to a prefix `z`. -/
noncomputable def recv (D : Finset B) (K m : ℕ) (z : Fin (m - K) → B) : D → F :=
  fun x => algebraMap B F ((Pz K m z).eval (x : B))

/-- The codeword produced from `M` (in the prefix fiber of `z`). -/
noncomputable def code (D : Finset B) (K m : ℕ) (z : Fin (m - K) → B) (M : Finset B) : D → F :=
  fun x => algebraMap B F ((cpoly K m z M).eval (x : B))

/-- The prefix fiber over `z`: `m`-subsets of `D` with prescribed locator prefix `z`. -/
noncomputable def fiber (D : Finset B) (K m : ℕ) (z : Fin (m - K) → B) : Finset (Finset B) :=
  (D.powersetCard m).filter (fun M => pre K m M = z)

/-- The locator polynomial is monic. -/
lemma loc_monic (M : Finset B) : (loc M).Monic :=
  monic_prod_of_monic _ _ (fun i _ => monic_X_sub_C i)

/-- The locator polynomial has degree equal to `|M|`. -/
lemma loc_natDegree (M : Finset B) : (loc M).natDegree = M.card := by
  rw [loc, natDegree_prod_of_monic _ _ (fun i (_ : i ∈ M) => monic_X_sub_C i)]
  simp

/-- Leading coefficient of the locator polynomial. -/
lemma loc_coeff_card (M : Finset B) : (loc M).coeff M.card = 1 := by
  have := (loc_monic M).coeff_natDegree
  rwa [loc_natDegree] at this

/-- The locator vanishes at each point of `M`. -/
lemma loc_eval_eq_zero {M : Finset B} {a : B} (ha : a ∈ M) : (loc M).eval a = 0 := by
  simp only [loc, eval_prod]
  refine Finset.prod_eq_zero ha ?_
  simp

/-- The multiset of roots of the locator is exactly `M`. -/
lemma loc_roots (M : Finset B) : (loc M).roots = M.val :=
  roots_prod_X_sub_C M

/-- The locator determines `M`. -/
lemma loc_injective : Function.Injective (loc : Finset B → B[X]) := by
  intro M M' h
  have : M.val = M'.val := by rw [← loc_roots, ← loc_roots, h]
  exact Finset.val_injective this

/-- Coefficient of `P_z` at the leading degree `m` (assuming `K ≤ m`), namely `1`. -/
lemma Pz_coeff_top (K m : ℕ) (hKm : K ≤ m) (z : Fin (m - K) → B) :
    (Pz K m z).coeff m = 1 := by
  simp only [Pz, coeff_add, coeff_X_pow, finset_sum_coeff, coeff_C_mul]
  have hs : (∑ x : Fin (m - K), (if (m = K + (x : ℕ)) then z x else (0 : B))) = 0 :=
    Finset.sum_eq_zero fun x _ => by simp [show ¬(m = K + (x : ℕ)) by have := x.2; omega]
  simp [hs]

/-- Coefficient of `P_z` at degree `K + i` equals `z i`. -/
lemma Pz_coeff_mid (K m : ℕ) (hKm : K ≤ m) (z : Fin (m - K) → B) (i : Fin (m - K)) :
    (Pz K m z).coeff (K + (i : ℕ)) = z i := by
  simp only [Pz, coeff_add, coeff_X_pow, finset_sum_coeff, coeff_C_mul]
  have hxm : ¬ (K + (i : ℕ) = m) := by have := i.2; omega
  rw [if_neg hxm, zero_add, Finset.sum_eq_single i]
  · simp
  · intro j _ hj
    have hcond : ¬ (K + (i : ℕ) = K + (j : ℕ)) := fun h => hj (Fin.ext (by omega))
    rw [if_neg hcond, mul_zero]
  · intro h; exact absurd (Finset.mem_univ i) h

/-- `P_z` has no coefficients above degree `m`. -/
lemma Pz_coeff_high (K m : ℕ) (hKm : K ≤ m) (z : Fin (m - K) → B) {j : ℕ}
    (hj : m < j) : (Pz K m z).coeff j = 0 := by
  simp only [Pz, coeff_add, coeff_X_pow, finset_sum_coeff, coeff_C_mul]
  have hxm : ¬ (j = m) := by omega
  rw [if_neg hxm, zero_add]
  apply Finset.sum_eq_zero
  intro i _
  have hne : ¬ (j = K + (i : ℕ)) := by have := i.2; omega
  simp [hne]

/-- For `M` in the fiber of `z`, the candidate polynomial has degree `< K`. -/
lemma cpoly_degree {K m : ℕ} (hKm : K ≤ m) (D : Finset B)
    (z : Fin (m - K) → B) {M : Finset B} (hM : M ∈ fiber D K m z) :
    (cpoly K m z M).degree < (K : WithBot ℕ) := by
  rw [degree_lt_iff_coeff_zero]
  intro j hj
  have hMmem := (Finset.mem_filter.mp hM)
  have hcard : M.card = m := (Finset.mem_powersetCard.mp hMmem.1).2
  have hpre : pre K m M = z := hMmem.2
  simp only [cpoly, coeff_sub]
  rcases lt_trichotomy j m with hjm | hjm | hjm
  · -- K ≤ j < m : j = K + i
    obtain ⟨i, hi⟩ : ∃ i : Fin (m - K), (K + (i : ℕ)) = j := by
      refine ⟨⟨j - K, by omega⟩, by simp; omega⟩
    rw [← hi, Pz_coeff_mid K m hKm z i]
    have hz : (loc M).coeff (K + (i : ℕ)) = z i := by
      have := congrArg (fun f => f i) hpre; simpa [pre] using this
    rw [hz]; ring
  · rw [hjm, Pz_coeff_top K m hKm z]
    have : (loc M).coeff m = 1 := by rw [← hcard]; exact loc_coeff_card M
    rw [this]; ring
  · rw [Pz_coeff_high K m hKm z hjm]
    have : (loc M).coeff j = 0 := by
      apply coeff_eq_zero_of_natDegree_lt
      rw [loc_natDegree, hcard]; exact hjm
    rw [this]; ring

/-- A degree-`< K` codeword over `B` maps into `RS[F, D, K]`. -/
lemma code_mem_RS {K m : ℕ} (hKm : K ≤ m) (D : Finset B)
    (z : Fin (m - K) → B) {M : Finset B} (hM : M ∈ fiber D K m z) :
    code (F := F) D K m z M ∈ (RS D K : Set (D → F)) := by
  refine ⟨(cpoly K m z M).map (algebraMap B F), ?_, ?_⟩
  · rw [degree_map_eq_of_injective (algebraMap B F).injective]
    exact cpoly_degree hKm D z hM
  · intro x
    simp only [code, eval_map, eval₂_at_apply]

/-- The produced codeword agrees with the received word on all of `M`, hence on `≥ m`
positions. -/
lemma code_agrees {K m : ℕ} (D : Finset B) (z : Fin (m - K) → B) {M : Finset B}
    (hM : M ∈ fiber D K m z) :
    m ≤ agreeCard (recv (F := F) D K m z) (code (F := F) D K m z M) := by
  have hMmem := Finset.mem_powersetCard.mp (Finset.mem_filter.mp hM).1
  have hMD : M ⊆ D := hMmem.1
  have hcard : M.card = m := hMmem.2
  set A := (Finset.univ : Finset D).filter
      (fun x : D => code (F := F) D K m z M x = recv (F := F) D K m z x) with hA
  have hMsub : M ⊆ A.image (fun x : D => x.1) := by
    intro a ha
    rw [Finset.mem_image]
    refine ⟨⟨a, hMD ha⟩, ?_, rfl⟩
    rw [hA, Finset.mem_filter]
    refine ⟨Finset.mem_univ _, ?_⟩
    show algebraMap B F ((cpoly K m z M).eval (a : B))
        = algebraMap B F ((Pz K m z).eval (a : B))
    rw [cpoly, eval_sub, loc_eval_eq_zero ha, sub_zero]
  calc m = M.card := hcard.symm
    _ ≤ (A.image (fun x : D => x.1)).card := Finset.card_le_card hMsub
    _ ≤ A.card := Finset.card_image_le
    _ = agreeCard (recv (F := F) D K m z) (code (F := F) D K m z M) := rfl

/-- `code z` is injective on the fiber of `z`. -/
lemma code_injOn {K m : ℕ} (D : Finset B) (hmn : m ≤ D.card) (z : Fin (m - K) → B) :
    Set.InjOn (code (F := F) D K m z) (fiber D K m z : Set (Finset B)) := by
  intro M hM M' hM' hcode
  simp only [Finset.mem_coe] at hM hM'
  by_contra hne
  have hcardM : (loc M).natDegree = m := by
    rw [loc_natDegree]; exact (Finset.mem_powersetCard.mp (Finset.mem_filter.mp hM).1).2
  have hcardM' : (loc M').natDegree = m := by
    rw [loc_natDegree]; exact (Finset.mem_powersetCard.mp (Finset.mem_filter.mp hM').1).2
  -- from equality of codewords, the locators agree on all of `D`
  have hvan : ∀ x ∈ D, (loc M' - loc M).eval x = 0 := by
    intro x hx
    have hxeq := congrArg (fun f => f (⟨x, hx⟩ : D)) hcode
    simp only [code] at hxeq
    have hev : (cpoly K m z M).eval x = (cpoly K m z M').eval x :=
      (algebraMap B F).injective hxeq
    simp only [cpoly, eval_sub] at hev
    have hll : (loc M).eval x = (loc M').eval x := sub_right_injective hev
    rw [eval_sub, ← hll, sub_self]
  have hp : loc M' - loc M ≠ 0 := by
    intro h
    rw [sub_eq_zero] at h
    exact hne (loc_injective h).symm
  have hdeg : (loc M' - loc M).degree < (m : WithBot ℕ) := by
    rw [degree_lt_iff_coeff_zero]
    intro j hj
    rw [coeff_sub]
    rcases Nat.lt_or_ge m j with hjm | hjm
    · rw [coeff_eq_zero_of_natDegree_lt (by rw [hcardM']; exact hjm),
          coeff_eq_zero_of_natDegree_lt (by rw [hcardM]; exact hjm), sub_zero]
    · have hjeq : j = m := le_antisymm hjm hj
      rw [hjeq, ← hcardM', (loc_monic M').coeff_natDegree, hcardM', ← hcardM,
          (loc_monic M).coeff_natDegree, sub_self]
  have hnatlt : (loc M' - loc M).natDegree < D.card :=
    lt_of_lt_of_le ((natDegree_lt_iff_degree_lt hp).mpr hdeg) hmn
  exact hp (eq_zero_of_natDegree_lt_card_of_eval_eq_zero' _ D hvan hnatlt)

/-- The image of the fiber under `code z` lands in the decoding list of `recv z`. -/
lemma code_image_subset {K m : ℕ} (hKm : K ≤ m) (D : Finset B)
    (z : Fin (m - K) → B) :
    (((fiber D K m z).image (code (F := F) D K m z)) : Set (D → F))
      ⊆ listSet D K m (recv (F := F) D K m z) := by
  intro c hc
  simp only [Finset.coe_image, Set.mem_image, Finset.mem_coe] at hc
  obtain ⟨M, hM, rfl⟩ := hc
  exact ⟨code_mem_RS hKm D z hM, code_agrees D z hM⟩

/-- **Pigeonhole for prefixes.** Some prefix `z` has a fiber of size at least
`⌊binom(n,m) / |𝔹|^{m-K}⌋`. -/
lemma exists_heavy_fiber (D : Finset B) (K m : ℕ) :
    ∃ z : Fin (m - K) → B,
      (D.card).choose m / (Fintype.card B) ^ (m - K) ≤ (fiber D K m z).card := by
  have hmap : ∀ M ∈ D.powersetCard m,
      pre K m M ∈ (Finset.univ : Finset (Fin (m - K) → B)) := fun _ _ => Finset.mem_univ _
  have hne : (Finset.univ : Finset (Fin (m - K) → B)).Nonempty := Finset.univ_nonempty
  have hmul : (Finset.univ : Finset (Fin (m - K) → B)).card
      * ((D.card).choose m / (Fintype.card B) ^ (m - K)) ≤ (D.powersetCard m).card := by
    rw [Finset.card_univ, Finset.card_powersetCard]
    have hcu : Fintype.card (Fin (m - K) → B) = (Fintype.card B) ^ (m - K) := by simp
    rw [hcu, mul_comm]
    exact Nat.div_mul_le_self _ _
  obtain ⟨z, _, hz⟩ := Finset.exists_le_card_fiber_of_mul_le_card_of_maps_to hmap hne hmul
  exact ⟨z, hz⟩

/-- **Identity-prefix floor.** For `1 ≤ K ≤ m ≤ n = |D|`, there is a `𝔹`-valued received
word whose Reed–Solomon list at agreement threshold `m` has size at least
`⌊binom(n,m) / |𝔹|^{m-K}⌋`.

This is the structural core (Lemma "identity-prefix floor") behind all four deployed
unsafe certificates. -/
theorem identity_floor (D : Finset B) (K m : ℕ) (hKm : K ≤ m)
    (hmn : m ≤ D.card) :
    ∃ Ub : D → B,
      (D.card).choose m / (Fintype.card B) ^ (m - K)
        ≤ (listSet D K m (fun x => algebraMap B F (Ub x))).ncard := by
  obtain ⟨z, hz⟩ := exists_heavy_fiber (B := B) D K m
  refine ⟨fun x => (Pz K m z).eval (x : B), ?_⟩
  have hrecv : (fun x : D => algebraMap B F ((Pz K m z).eval (x : B))) = recv (F := F) D K m z :=
    rfl
  rw [hrecv]
  have hsub := code_image_subset (F := F) hKm D z
  have hfin : (listSet D K m (recv (F := F) D K m z) : Set (D → F)).Finite := Set.toFinite _
  calc (D.card).choose m / (Fintype.card B) ^ (m - K)
        ≤ (fiber D K m z).card := hz
    _ = ((fiber D K m z).image (code (F := F) D K m z)).card :=
          (Finset.card_image_of_injOn (code_injOn D hmn z)).symm
    _ = (((fiber D K m z).image (code (F := F) D K m z) : Finset (D → F)) : Set (D → F)).ncard :=
          (Set.ncard_coe_finset _).symm
    _ ≤ (listSet D K m (recv (F := F) D K m z)).ncard := Set.ncard_le_ncard hsub hfin

end RSMCA
