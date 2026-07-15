import Mathlib

/-!
# Exchange-excess simple-pole separation

This module formalizes the finite algebraic kernel and weighted-pole average
from
`experimental/notes/thresholds/exchange_excess_pole_separation.md`.

For equal-cardinality supports `S,T`, a shared locator prefix is used through
its exact cancellation consequence

```
natDegree (locator S - locator T) + (w + 1) <= m.
```

After the common intersection locator is removed, the reduced gap has degree
at most `|(S \ T)| - (w+1)`. Hence at most that many off-domain poles can
make the two locators collide. The module also double-counts an arbitrary
finite pair family and proves the floor-average witness
`C_alpha <= totalExcess / numberOfPoles`.

No large low-excess subfamily is asserted. The later MCA received-line and
challenge-shear compilers remain separate from this finite pole theorem.
-/

namespace SyndromeLine.ExchangeExcessPoleSeparation

open Finset Polynomial BigOperators

variable {F : Type*} [Field F] [DecidableEq F]

/-- The monic support locator `Q_S(X) = product_(x in S) (X-x)`. -/
noncomputable def locator (S : Finset F) : F[X] :=
  ∏ x ∈ S, (X - C x)

/-- The reduced locator gap after removing the common support core. -/
noncomputable def reducedGap (S T : Finset F) : F[X] :=
  locator (S \ T) - locator (T \ S)

/-- Johnson exchange distance for equal-cardinality supports. -/
def exchangeDistance (S T : Finset F) : ℕ :=
  (S \ T).card

/-- Excess above the prefix-rigidity minimum exchange `w+1`. -/
def exchangeExcess (w : ℕ) (S T : Finset F) : ℕ :=
  exchangeDistance S T - (w + 1)

/--
The exact degree-cancellation consequence of sharing the depth-`w` locator
prefix in an `m`-slice.
-/
def prefixDegreeCancellation (m w : ℕ) (S T : Finset F) : Prop :=
  (locator S - locator T).natDegree + (w + 1) ≤ m

omit [DecidableEq F] in
theorem locator_monic (S : Finset F) : (locator S).Monic := by
  exact Polynomial.monic_prod_of_monic _ _ fun x _ =>
    Polynomial.monic_X_sub_C x

omit [DecidableEq F] in
theorem locator_natDegree (S : Finset F) :
    (locator S).natDegree = S.card := by
  rw [locator, Polynomial.natDegree_prod_of_monic]
  · simp
  · exact fun x _ => Polynomial.monic_X_sub_C x

omit [DecidableEq F] in
theorem locator_injective :
    Function.Injective (locator (F := F)) := by
  intro S T h
  have hroots : S.val = T.val := by
    unfold locator at h
    apply_fun Polynomial.roots at h
    simpa [Polynomial.roots_prod_X_sub_C] using h
  exact Finset.val_inj.mp hroots

/--
The first `w` coefficients below the leading degree `m`.
-/
noncomputable def locatorPrefix (m w : ℕ) (S : Finset F) :
    Fin w → F :=
  fun i => (locator S).coeff (m - (i.1 + 1))

omit [DecidableEq F] in
/--
Literal shared-prefix equality implies the exact degree-cancellation premise.
-/
theorem prefixDegreeCancellation_of_prefix_eq
    (m w : ℕ) (S T : Finset F)
    (hw : w + 1 ≤ m)
    (hS : S.card = m) (hT : T.card = m)
    (hprefix : locatorPrefix m w S = locatorPrefix m w T) :
    prefixDegreeCancellation m w S T := by
  unfold prefixDegreeCancellation
  have hdeg :
      (locator S - locator T).natDegree ≤ m - (w + 1) := by
    apply Polynomial.natDegree_le_iff_coeff_eq_zero.mpr
    intro N hN
    by_cases hNm : N = m
    · subst N
      have hcS : (locator S).coeff m = 1 := by
        rw [← hS, ← locator_natDegree]
        exact (locator_monic S).coeff_natDegree
      have hcT : (locator T).coeff m = 1 := by
        rw [← hT, ← locator_natDegree]
        exact (locator_monic T).coeff_natDegree
      simp [Polynomial.coeff_sub, hcS, hcT]
    · by_cases hmN : m < N
      · have hdS : (locator S).natDegree < N := by
          rw [locator_natDegree, hS]
          exact hmN
        have hdT : (locator T).natDegree < N := by
          rw [locator_natDegree, hT]
          exact hmN
        simp [Polynomial.coeff_sub,
          Polynomial.coeff_eq_zero_of_natDegree_lt hdS,
          Polynomial.coeff_eq_zero_of_natDegree_lt hdT]
      · have hNm_lt : N < m := by omega
        let i : Fin w := ⟨m - N - 1, by omega⟩
        have hi : m - (i.1 + 1) = N := by
          dsimp [i]
          omega
        have hc := congrFun hprefix i
        unfold locatorPrefix at hc
        rw [hi] at hc
        simp [Polynomial.coeff_sub, hc]
  omega

/-- Exact common-core factorization. -/
theorem locator_diff_factor (S T : Finset F) :
    locator S - locator T =
      locator (S ∩ T) * reducedGap S T := by
  have hS :
      locator S = locator (S ∩ T) * locator (S \ T) := by
    unfold locator
    rw [← Finset.prod_union
      (Finset.disjoint_right.mpr fun x hx => by aesop)]
    congr
    ext x
    by_cases hx : x ∈ T <;> simp [hx]
  have hT :
      locator T = locator (S ∩ T) * locator (T \ S) := by
    unfold locator
    rw [← Finset.prod_union]
    · congr
      ext x
      by_cases hx : x ∈ S <;> simp [hx]
    · exact Finset.disjoint_left.mpr fun x hx₁ hx₂ =>
        (Finset.mem_sdiff.mp hx₂).2
          (Finset.mem_inter.mp hx₁).1
  rw [hS, hT, ← mul_sub, reducedGap]

theorem reducedGap_ne_zero {S T : Finset F}
    (hST : S ≠ T) :
    reducedGap S T ≠ 0 := by
  intro hzero
  have hloc :
      locator (S \ T) = locator (T \ S) :=
    sub_eq_zero.mp hzero
  have hdiff : S \ T = T \ S := locator_injective hloc
  apply hST
  ext x
  by_cases hxS : x ∈ S <;> by_cases hxT : x ∈ T <;>
    simp_all

/--
Theorem 2.1 degree statement: the reduced-gap degree is bounded by exchange
excess.
-/
theorem reducedGap_natDegree_le_exchangeExcess
    (m w : ℕ) (S T : Finset F)
    (hS : S.card = m) (hST : S ≠ T)
    (hprefix : prefixDegreeCancellation m w S T) :
    (reducedGap S T).natDegree ≤ exchangeExcess w S T := by
  have hred : reducedGap S T ≠ 0 := reducedGap_ne_zero hST
  have hcore : locator (S ∩ T) ≠ 0 := (locator_monic _).ne_zero
  have hfactor := locator_diff_factor S T
  unfold prefixDegreeCancellation at hprefix
  rw [hfactor, Polynomial.natDegree_mul'
    (mul_ne_zero (Polynomial.leadingCoeff_ne_zero.mpr hcore)
      (Polynomial.leadingCoeff_ne_zero.mpr hred)),
    locator_natDegree] at hprefix
  have hcard := Finset.card_inter_add_card_sdiff S T
  simp only [exchangeExcess, exchangeDistance] at *
  omega

section FiniteField

variable [Fintype F]

/-- Off-domain poles at which two locators collide. -/
noncomputable def offDomainCollisions
    (D S T : Finset F) : Finset F :=
  (Finset.univ \ D).filter fun α =>
    (locator S).eval α = (locator T).eval α

omit [Fintype F] in
theorem eval_locator_inter_ne_zero
    {D S T : Finset F} {α : F}
    (hS : S ⊆ D) (hα : α ∉ D) :
    (locator (S ∩ T)).eval α ≠ 0 := by
  classical
  rw [locator, Polynomial.eval_prod]
  simp only [Polynomial.eval_sub, Polynomial.eval_X, Polynomial.eval_C]
  apply Finset.prod_ne_zero_iff.mpr
  intro x hx
  have hxD : x ∈ D := hS (Finset.mem_inter.mp hx).1
  have hαx : α ≠ x := by
    intro h
    apply hα
    simpa [h] using hxD
  exact sub_ne_zero.mpr hαx

omit [Fintype F] in
theorem collision_mem_reducedGap_roots
    {D S T : Finset F} {α : F}
    (hS : S ⊆ D) (hST : S ≠ T)
    (hαD : α ∉ D)
    (hcollision : (locator S).eval α = (locator T).eval α) :
    α ∈ (reducedGap S T).roots := by
  have hred : reducedGap S T ≠ 0 := reducedGap_ne_zero hST
  rw [Polynomial.mem_roots hred]
  have hzero : (locator S - locator T).eval α = 0 := by
    simp [Polynomial.eval_sub, hcollision]
  have hfactor := congrArg (Polynomial.eval α)
    (locator_diff_factor S T)
  simp only [Polynomial.eval_mul] at hfactor
  have hprod :
      (locator (S ∩ T)).eval α * (reducedGap S T).eval α = 0 := by
    rw [← hfactor]
    exact hzero
  exact (mul_eq_zero.mp hprod).resolve_left
    (eval_locator_inter_ne_zero hS hαD)

/--
Theorem 2.1 pole statement: at most `exchangeExcess` off-domain poles
collide.
-/
theorem offDomainCollisions_card_le_exchangeExcess
    (D : Finset F) (m w : ℕ) (S T : Finset F)
    (hSD : S ⊆ D) (hS : S.card = m) (hST : S ≠ T)
    (hprefix : prefixDegreeCancellation m w S T) :
    (offDomainCollisions D S T).card ≤ exchangeExcess w S T := by
  classical
  calc
    (offDomainCollisions D S T).card ≤
        (reducedGap S T).roots.toFinset.card := by
      apply Finset.card_le_card
      intro α hα
      have hmem := Finset.mem_filter.mp hα
      have hαD := (Finset.mem_sdiff.mp hmem.1).2
      exact Multiset.mem_toFinset.mpr
        (collision_mem_reducedGap_roots hSD hST hαD hmem.2)
    _ ≤ Multiset.card (reducedGap S T).roots :=
      Multiset.toFinset_card_le _
    _ ≤ (reducedGap S T).natDegree :=
      Polynomial.card_roots' _
    _ ≤ exchangeExcess w S T :=
      reducedGap_natDegree_le_exchangeExcess m w S T hS hST hprefix

/--
Literal shared-prefix version of the exchange-excess pole bound.
-/
theorem offDomainCollisions_card_le_exchangeExcess_of_prefix_eq
    (D : Finset F) (m w : ℕ) (S T : Finset F)
    (hw : w + 1 ≤ m)
    (hSD : S ⊆ D) (hS : S.card = m) (hT : T.card = m)
    (hST : S ≠ T)
    (hprefix : locatorPrefix m w S = locatorPrefix m w T) :
    (offDomainCollisions D S T).card ≤ exchangeExcess w S T :=
  offDomainCollisions_card_le_exchangeExcess
    D m w S T hSD hS hST
      (prefixDegreeCancellation_of_prefix_eq
        m w S T hw hS hT hprefix)

/-- Minimum exchange (`exchangeExcess = 0`) separates at every pole. -/
theorem minimum_exchange_separates
    (D : Finset F) (m w : ℕ) (S T : Finset F)
    (hSD : S ⊆ D) (hS : S.card = m) (hST : S ≠ T)
    (hprefix : prefixDegreeCancellation m w S T)
    (hmin : exchangeDistance S T = w + 1) :
    ∀ α ∉ D, (locator S).eval α ≠ (locator T).eval α := by
  classical
  have hcard :=
    offDomainCollisions_card_le_exchangeExcess
      D m w S T hSD hS hST hprefix
  have hzero : (offDomainCollisions D S T).card = 0 := by
    simpa [exchangeExcess, hmin] using hcard
  have hempty : offDomainCollisions D S T = ∅ :=
    Finset.card_eq_zero.mp hzero
  intro α hαD hcollision
  have hmem : α ∈ offDomainCollisions D S T := by
    simp [offDomainCollisions, hαD, hcollision]
  rw [hempty] at hmem
  simp at hmem

/--
Literal shared-prefix form of minimum-exchange separation.
-/
theorem minimum_exchange_separates_of_prefix_eq
    (D : Finset F) (m w : ℕ) (S T : Finset F)
    (hw : w + 1 ≤ m)
    (hSD : S ⊆ D) (hS : S.card = m) (hT : T.card = m)
    (hST : S ≠ T)
    (hprefix : locatorPrefix m w S = locatorPrefix m w T)
    (hmin : exchangeDistance S T = w + 1) :
    ∀ α ∉ D, (locator S).eval α ≠ (locator T).eval α :=
  minimum_exchange_separates D m w S T hSD hS hST
    (prefixDegreeCancellation_of_prefix_eq
      m w S T hw hS hT hprefix) hmin

/-! ## Generic finite weighted-pole double count -/

variable {Pole Pair : Type*}

noncomputable def collisionCountAt
    (pairs : Finset Pair) (collision : Pole → Pair → Prop)
    (α : Pole) : ℕ := by
  classical
  exact (pairs.filter fun e => collision α e).card

noncomputable def collisionCountForPair
    (poles : Finset Pole) (collision : Pole → Pair → Prop)
    (e : Pair) : ℕ := by
  classical
  exact (poles.filter fun α => collision α e).card

noncomputable def collisionMass
    (poles : Finset Pole) (pairs : Finset Pair)
    (collision : Pole → Pair → Prop) : ℕ :=
  ∑ α ∈ poles, collisionCountAt pairs collision α

theorem collisionMass_eq_sum_pair_counts
    (poles : Finset Pole) (pairs : Finset Pair)
    (collision : Pole → Pair → Prop) :
    collisionMass poles pairs collision =
      ∑ e ∈ pairs, collisionCountForPair poles collision e := by
  classical
  simp only [collisionMass, collisionCountAt, collisionCountForPair,
    Finset.card_eq_sum_ones, Finset.sum_filter]
  exact Finset.sum_comm

theorem collisionMass_le_totalExcess
    (poles : Finset Pole) (pairs : Finset Pair)
    (collision : Pole → Pair → Prop) (excess : Pair → ℕ)
    (hpair : ∀ e ∈ pairs,
      collisionCountForPair poles collision e ≤ excess e) :
    collisionMass poles pairs collision ≤ ∑ e ∈ pairs, excess e := by
  rw [collisionMass_eq_sum_pair_counts]
  exact Finset.sum_le_sum hpair

/--
Finite floor-average witness: some pole has collision count at most total
exchange excess divided by the number of poles.
-/
theorem exists_collisionCountAt_le_totalExcess_div
    (poles : Finset Pole) (pairs : Finset Pair)
    (collision : Pole → Pair → Prop) (excess : Pair → ℕ)
    (hpoles : poles.Nonempty)
    (hmass : collisionMass poles pairs collision ≤
      ∑ e ∈ pairs, excess e) :
    ∃ α ∈ poles,
      collisionCountAt pairs collision α ≤
        (∑ e ∈ pairs, excess e) / poles.card := by
  classical
  let E := ∑ e ∈ pairs, excess e
  change ∃ α ∈ poles, collisionCountAt pairs collision α ≤ E / poles.card
  change collisionMass poles pairs collision ≤ E at hmass
  by_contra h
  push_neg at h
  have hpoint : ∀ α ∈ poles,
      E / poles.card + 1 ≤ collisionCountAt pairs collision α := by
    intro α hα
    have := h α hα
    omega
  have hsum :
      poles.card * (E / poles.card + 1) ≤
        collisionMass poles pairs collision := by
    rw [collisionMass]
    calc
      poles.card * (E / poles.card + 1) =
          ∑ _α ∈ poles, (E / poles.card + 1) := by simp
      _ ≤ ∑ α ∈ poles, collisionCountAt pairs collision α :=
        Finset.sum_le_sum hpoint
  have hlt : E < poles.card * (E / poles.card + 1) :=
    Nat.lt_mul_div_succ E (Finset.card_pos.mpr hpoles)
  omega

/--
Equations (4)--(5) specialized to a finite locator-pair family.
-/
theorem exists_pole_with_exchange_average
    (D : Finset F) (m w : ℕ)
    (hwm : w + 1 ≤ m)
    (pairs : Finset (Finset F × Finset F))
    (hpole : (Finset.univ \ D).Nonempty)
    (hpairs : ∀ e ∈ pairs,
      e.1 ⊆ D ∧ e.1.card = m ∧ e.2.card = m ∧ e.1 ≠ e.2 ∧
        locatorPrefix m w e.1 = locatorPrefix m w e.2) :
    ∃ α ∈ (Finset.univ \ D),
      collisionCountAt pairs
          (fun α e => (locator e.1).eval α = (locator e.2).eval α) α ≤
        (∑ e ∈ pairs, exchangeExcess w e.1 e.2) /
          (Finset.univ \ D).card := by
  let poles := Finset.univ \ D
  let collision := fun α (e : Finset F × Finset F) =>
    (locator e.1).eval α = (locator e.2).eval α
  apply exists_collisionCountAt_le_totalExcess_div
    poles pairs collision (fun e => exchangeExcess w e.1 e.2) hpole
  apply collisionMass_le_totalExcess
  intro e he
  have h := hpairs e he
  calc
    collisionCountForPair poles collision e =
        (offDomainCollisions D e.1 e.2).card := by
      apply congrArg Finset.card
      ext α
      simp [poles, collision, offDomainCollisions]
    _ ≤ exchangeExcess w e.1 e.2 :=
      offDomainCollisions_card_le_exchangeExcess_of_prefix_eq
        D m w e.1 e.2 hwm h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

#print axioms locator_diff_factor
#print axioms reducedGap_natDegree_le_exchangeExcess
#print axioms offDomainCollisions_card_le_exchangeExcess
#print axioms offDomainCollisions_card_le_exchangeExcess_of_prefix_eq
#print axioms minimum_exchange_separates
#print axioms minimum_exchange_separates_of_prefix_eq
#print axioms collisionMass_le_totalExcess
#print axioms exists_collisionCountAt_le_totalExcess_div
#print axioms exists_pole_with_exchange_average

end FiniteField

end SyndromeLine.ExchangeExcessPoleSeparation
