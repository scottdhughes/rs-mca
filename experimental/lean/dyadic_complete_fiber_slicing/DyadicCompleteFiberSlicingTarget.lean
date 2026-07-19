import Mathlib

/-!
# Dyadic complete-fiber slicing: Lean formalization

This file records the general source-realized complete-fiber intersection
theorem from
`experimental/notes/l2/dyadic_complete_fiber_slicing_route_cut.md`.

The paper proof is given in that note.  The general intersection theorem is
now proved below.  The total order is part of the data because it canonically
selects the first `m` agreement points for every list polynomial.

The local classical `DecidableEq F` instance is an elaboration device for
finite-set intersection and filtering; it is constructed from `F` and does
not add a theorem hypothesis.  The public theorem retains the source's exact
field, subgroup, order, degree, agreement, divisor, received-word, and
distinctness wrapper.
-/

namespace DyadicCompleteFiberSlicing

noncomputable section

variable {F : Type*} [Field F]
local instance : DecidableEq F := Classical.decEq F

/-- Agreement points of `P` with the arbitrary received word `U` on `H`. -/
noncomputable def agreementSet
    (H : Subgroup Fˣ) [Fintype H] (U : H → F) (P : Polynomial F) : Finset H := by
  classical
  exact Finset.univ.filter fun x => P.eval ((x : Fˣ) : F) = U x

/-- The first exactly `m` agreement points in the fixed total order. -/
noncomputable def canonicalSupport
    (H : Subgroup Fˣ) [Fintype H] [LinearOrder H]
    (m : Nat) (U : H → F) (P : Polynomial F) : Finset H := by
  classical
  exact (agreementSet H U P).filter fun x =>
    ((agreementSet H U P).filter fun y => y < x).card < m

/-- The canonical first-`m` support contains only genuine agreement points.
The intersection theorem needs this containment, not the exact-cardinality
property of the canonical support. -/
private theorem canonicalSupport_subset_agreementSet
    (H : Subgroup Fˣ) [Fintype H] [LinearOrder H]
    (m : Nat) (U : H → F) (P : Polynomial F) :
    canonicalSupport H m U P ⊆ agreementSet H U P := by
  intro x hx
  exact (Finset.mem_filter.mp hx).1

/-- Membership in the received-word list at degree bound `K` and agreement `m`. -/
def inReceivedList
    (H : Subgroup Fˣ) [Fintype H]
    (K m : Nat) (U : H → F) (P : Polynomial F) : Prop :=
  P.natDegree < K ∧ m ≤ (agreementSet H U P).card

/-- The image `Q_c` of the power map `x ↦ x^c` on `H`. -/
noncomputable def powerImage
    (H : Subgroup Fˣ) [Fintype H] (c : Nat) : Finset F := by
  classical
  exact Finset.univ.image fun x : H => ((x : Fˣ) : F) ^ c

/-- Power-map image values whose complete fibers lie in `S`. -/
noncomputable def completeFiberSet
    (H : Subgroup Fˣ) [Fintype H] (c : Nat) (S : Finset H) : Finset F := by
  classical
  exact (powerImage H c).filter fun y =>
    ∀ x : H, ((x : Fˣ) : F) ^ c = y → x ∈ S

/-- Every nonempty power-map fiber has cardinality `c` when `c` divides the
order of the finite multiplicative subgroup.  Mathlib supplies both inputs:
finite subgroups of units in a domain are cyclic, and the `c`-power homomorphism
on a finite cyclic group has kernel cardinality `gcd(|H|,c)`. -/
private theorem powerFiber_card
    (H : Subgroup Fˣ) [Fintype H]
    (n c : Nat) (hcard : Fintype.card H = n) (hc : c ∣ n)
    {y : F} (hy : y ∈ powerImage H c) :
    ((Finset.univ : Finset H).filter fun x : H =>
      ((x : Fˣ) : F) ^ c = y).card = c := by
  classical
  change y ∈ Finset.image (fun x : H => ((x : Fˣ) : F) ^ c) Finset.univ at hy
  obtain ⟨a, _ha, rfl⟩ := Finset.mem_image.mp hy
  let f : H →* H := powMonoidHom c
  have hFibers := MonoidHom.card_fiber_eq_of_mem_range f
    (x := f a) (y := 1) ⟨a, rfl⟩ ⟨1, by simp⟩
  have hKer : Nat.card f.ker = c := by
    rw [show Nat.card f.ker = (Nat.card H).gcd c from
      IsCyclic.card_powMonoidHom_ker H c]
    rw [Nat.card_eq_fintype_card, hcard]
    exact Nat.gcd_eq_right hc
  have hOne : ((Finset.univ : Finset H).filter fun x => f x = 1).card = c := by
    rw [← Fintype.card_subtype]
    simpa [Nat.card_eq_fintype_card, MonoidHom.mem_ker] using hKer
  have hGroup : ((Finset.univ : Finset H).filter fun x => f x = f a).card = c :=
    hFibers.trans hOne
  have hsets :
      ((Finset.univ : Finset H).filter fun x : H =>
        ((x : Fˣ) : F) ^ c = (((a : Fˣ) : F) ^ c)) =
      ((Finset.univ : Finset H).filter fun x => f x = f a) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, f, powMonoidHom_apply]
    constructor
    · intro h
      apply Subtype.ext
      apply Units.ext
      simpa using h
    · intro h
      have hu : ((x ^ c : H) : Fˣ) = ((a ^ c : H) : Fˣ) :=
        congrArg (fun z : H => (z : Fˣ)) h
      exact Units.ext_iff.mp hu
  rw [hsets]
  exact hGroup

/--
PROVED complete-fiber intersection theorem.

Exact hypotheses: an arbitrary field; a finite multiplicative subgroup `H`
of order `n`; `1 ≤ K ≤ m ≤ n`; a fixed total order on `H`; an
arbitrary received word; two distinct degree-`< K` list polynomials with at
least `m` agreements; and a divisor `c ∣ n`. The conclusion is the complete
fiber intersection ceiling `floor((K-1)/c)` for their canonical first-`m`
supports.
-/
theorem completeFiberIntersection
    (H : Subgroup Fˣ) [Fintype H] [LinearOrder H]
    (n K m c : Nat)
    (hcard : Fintype.card H = n)
    (hrange : 1 ≤ K ∧ K ≤ m ∧ m ≤ n)
    (hc : c ∣ n)
    (U : H → F)
    (P Q : Polynomial F)
    (hP : inReceivedList H K m U P)
    (hQ : inReceivedList H K m U Q)
    (hne : P ≠ Q) :
    ((completeFiberSet H c (canonicalSupport H m U P)) ∩
      completeFiberSet H c (canonicalSupport H m U Q)).card ≤
      (K - 1) / c := by
  classical
  let common :=
    (completeFiberSet H c (canonicalSupport H m U P)) ∩
      completeFiberSet H c (canonicalSupport H m U Q)
  let g : H → F := fun x => ((x : Fˣ) : F) ^ c
  let points := (Finset.univ : Finset H).filter fun x => g x ∈ common
  have common_mem_powerImage {y : F} (hy : y ∈ common) : y ∈ powerImage H c := by
    have hyP : y ∈ completeFiberSet H c (canonicalSupport H m U P) :=
      (Finset.mem_inter.mp hy).1
    exact (Finset.mem_filter.mp hyP).1
  have fiber_card {y : F} (hy : y ∈ common) :
      ((Finset.univ : Finset H).filter fun x => g x = y).card = c := by
    exact powerFiber_card H n c hcard hc (common_mem_powerImage hy)
  have hpoints : points.card = common.card * c := by
    calc
      points.card = ∑ y ∈ common,
          ((Finset.univ : Finset H).filter fun x => g x = y).card := by
            exact (Finset.sum_card_fiberwise_eq_card_filter
              (Finset.univ : Finset H) common g).symm
      _ = common.card * c := Finset.sum_const_nat fun y hy => fiber_card hy
  let incl : H ↪ F :=
    { toFun := fun x => ((x : Fˣ) : F)
      inj' := by
        intro x y hxy
        apply Subtype.ext
        exact Units.ext hxy }
  let fieldPoints := points.map incl
  have hfieldPointsRoots : fieldPoints.val ⊆ (P - Q).roots := by
    intro z hz
    obtain ⟨x, hxpoints, rfl⟩ := Finset.mem_map.mp hz
    have hxCommon : g x ∈ common := (Finset.mem_filter.mp hxpoints).2
    have hxCompleteP : x ∈ canonicalSupport H m U P := by
      have hyP : g x ∈ completeFiberSet H c (canonicalSupport H m U P) :=
        (Finset.mem_inter.mp hxCommon).1
      exact (Finset.mem_filter.mp hyP).2 x rfl
    have hxCompleteQ : x ∈ canonicalSupport H m U Q := by
      have hyQ : g x ∈ completeFiberSet H c (canonicalSupport H m U Q) :=
        (Finset.mem_inter.mp hxCommon).2
      exact (Finset.mem_filter.mp hyQ).2 x rfl
    have hxAgreeP : x ∈ agreementSet H U P :=
      canonicalSupport_subset_agreementSet H m U P hxCompleteP
    have hxAgreeQ : x ∈ agreementSet H U Q :=
      canonicalSupport_subset_agreementSet H m U Q hxCompleteQ
    have hEvalP : P.eval (((x : H) : Fˣ) : F) = U x :=
      (Finset.mem_filter.mp hxAgreeP).2
    have hEvalQ : Q.eval (((x : H) : Fˣ) : F) = U x :=
      (Finset.mem_filter.mp hxAgreeQ).2
    have hEvalP' : P.eval (incl x) = U x := by
      simpa [incl] using hEvalP
    have hEvalQ' : Q.eval (incl x) = U x := by
      simpa [incl] using hEvalQ
    apply (Polynomial.mem_roots (sub_ne_zero.mpr hne)).2
    simp [Polynomial.IsRoot, Polynomial.eval_sub, hEvalP', hEvalQ']
  have hrootCard : points.card ≤ (P - Q).natDegree := by
    have h := Polynomial.card_le_degree_of_subset_roots hfieldPointsRoots
    simpa [fieldPoints] using h
  have hdegree : (P - Q).natDegree ≤ K - 1 := by
    have hsub := Polynomial.natDegree_sub_le P Q
    have hPdeg : P.natDegree < K := hP.1
    have hQdeg : Q.natDegree < K := hQ.1
    omega
  have hmul : common.card * c ≤ K - 1 := by
    rw [← hpoints]
    exact hrootCard.trans hdegree
  have hcpos : 0 < c := by
    by_contra hcnot
    have hczero : c = 0 := Nat.eq_zero_of_not_pos hcnot
    subst c
    simp at hc
    omega
  change common.card ≤ (K - 1) / c
  exact (Nat.le_div_iff_mul_le hcpos).2 hmul

end

end DyadicCompleteFiberSlicing
