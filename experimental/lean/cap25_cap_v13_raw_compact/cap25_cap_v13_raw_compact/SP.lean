import cap25_cap_v13_raw_compact.Floor

/-!
# Input SP: primitive shift pairs and the prefix-collision link

This file develops the structural, *provable* content attached to the paper's Residual
Input **SP** (primitive shift-pair control).  SP itself is an open counting conjecture
(a bound on the primitive shift-pair contribution to the second-moment collision ledger),
so it cannot be settled here.  What *can* be settled unconditionally, and is proved in this
file, is the structural fact that motivates isolating SP inside the prefix (Q) ledger:

> a **shift-pair collision** — two sets with equal first `w` power sums — is exactly a
> **prefix collision** — two sets with equal identity-prefix `Φ_w` image.

This is the paper's observation (`def:primitive-shift-pair`, `rem:sp-audit`) that primitive
shift pairs are the residual configurations of the prefix count: in the deployed regime the
characteristic is far larger than the depth `w`, so Newton's identities convert equal power
sums into equal elementary symmetric functions, i.e. into equal locator prefixes.

Definitions and results:

* `RSMCA.psumF k M` — the `k`-th power-sum moment `∑_{x ∈ M} x^k`.
* `RSMCA.shiftPairColl w A A'` — a **shift-pair collision at depth `w`**: `A, A'` disjoint
  with equal power sums `p_1, …, p_w` (`def:primitive-shift-pair`, without the primitivity
  qualifier, which removes quotient-pullback strata and is what SP bounds).
* `RSMCA.newton_field` — Newton's identity for a finite set of field elements.
* `RSMCA.shiftpair_esymm_eq` — equal power sums `1..w` force equal elementary symmetric
  functions `e_1, …, e_w`, provided `1, …, w` are invertible (char `= 0` or `> w`).
* `RSMCA.shiftpair_prefix_collision` / `RSMCA.shiftpair_same_prefix` — hence a shift-pair
  collision of two `m`-sets is a collision of the identity-prefix map `pre` (`Φ_w`).
-/

open Polynomial Finset
open scoped Classical

namespace RSMCA

variable {B : Type*} [Field B]

/-- The `k`-th power-sum moment of a finite set: `p_k(M) = ∑_{x ∈ M} x^k`. -/
def psumF (k : ℕ) (M : Finset B) : B := ∑ x ∈ M, x ^ k

/-- A **shift-pair collision at depth `w`**: two disjoint finite sets with equal power sums
`p_1, …, p_w`.  (`def:primitive-shift-pair`; the *primitive* qualifier, which removes
quotient-pullback and common-divisor strata, is exactly what SP is asked to bound and is
not imposed here.) -/
def shiftPairColl (w : ℕ) (A A' : Finset B) : Prop :=
  Disjoint A A' ∧ ∀ j, 1 ≤ j → j ≤ w → psumF j A = psumF j A'

/-- **Newton's identity** for a finite set `M` of field elements:
`k · e_k(M) = (-1)^{k+1} ∑_{i<k} (-1)^i e_i(M) p_{k-i}(M)`, where `e` is the elementary
symmetric function (`Multiset.esymm`) and `p` the power sum. -/
theorem newton_field (M : Finset B) (k : ℕ) :
    (k : B) * M.val.esymm k =
      (-1) ^ (k + 1) * ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
        (-1) ^ a.1 * M.val.esymm a.1 * psumF a.2 M := by
  -- Apply the algebra homomorphism `MvPolynomial.aeval (fun i : ↥M => (i : B))` to both sides.
  have h_aeval : MvPolynomial.aeval (fun i : ↥M => (i : B)) (MvPolynomial.esymm (↥M) B k) = (M.val.esymm k) := by
    convert MvPolynomial.aeval_esymm_eq_multiset_esymm _ _ _ _;
    refine' Multiset.eq_of_le_of_card_le ( Multiset.le_iff_count.mpr _ ) _;
    · intro x; by_cases hx : x ∈ M <;> simp_all +decide [ Multiset.count_map ] ;
      rw [ Multiset.count_eq_one_of_mem ];
      · exact Multiset.card_pos_iff_exists_mem.mpr ⟨ ⟨ x, hx ⟩, Multiset.mem_filter.mpr ⟨ Multiset.mem_attach _ _, rfl ⟩ ⟩;
      · exact Finset.nodup _;
      · exact hx;
    · simp +decide;
      convert M.card_attach.le;
  have h_aeval_sum : MvPolynomial.aeval (fun i : ↥M => (i : B)) (∑ a ∈ antidiagonal k with a.1 < k, (-1) ^ a.1 * MvPolynomial.esymm (↥M) B a.1 * MvPolynomial.psum (↥M) B a.2) = ∑ a ∈ antidiagonal k with a.1 < k, (-1) ^ a.1 * (M.val.esymm a.1) * (psumF a.2 M) := by
    have h_aeval_sum : ∀ a ∈ antidiagonal k, MvPolynomial.aeval (fun i : ↥M => (i : B)) (MvPolynomial.esymm (↥M) B a.1) = (M.val.esymm a.1) := by
      intro a ha; rw [ MvPolynomial.aeval_esymm_eq_multiset_esymm ] ; simp +decide [ Finset.univ_eq_attach ] ;
      congr;
      exact Multiset.attach_map_val _;
    simp +decide [ psumF, MvPolynomial.psum ];
    refine' Finset.sum_congr rfl fun x hx => _;
    refine' congr_arg₂ _ ( congr_arg₂ _ rfl ( h_aeval_sum x ( Finset.mem_filter.mp hx |>.1 ) ) ) ( Finset.sum_bij ( fun x _ => x.val ) _ _ _ _ ) <;> simp +decide;
  rw [ ← h_aeval, ← h_aeval_sum ];
  convert congr_arg ( MvPolynomial.aeval ( fun i : ↥M => ( i : B ) ) ) ( MvPolynomial.mul_esymm_eq_sum ( ↥M ) B k ) using 1; all_goals simp +decide [ MvPolynomial.aeval_def ]

/-- **Shift pairs collapse the elementary symmetric functions.** If the power sums
`p_1, …, p_w` of `A` and `A'` agree and each of `1, …, w` is invertible in `B` (which holds
in characteristic `0` or `> w`), then the elementary symmetric functions `e_0, …, e_w`
agree. -/
theorem shiftpair_esymm_eq (w : ℕ) (A A' : Finset B)
    (hchar : ∀ k, 1 ≤ k → k ≤ w → (k : B) ≠ 0)
    (hmom : ∀ j, 1 ≤ j → j ≤ w → psumF j A = psumF j A') :
    ∀ j, j ≤ w → A.val.esymm j = A'.val.esymm j := by
  intro j hj
  induction' j using Nat.strong_induction_on with j ih;
  by_cases hj0 : 0 < j;
  · have h_eq : (j : B) * A.val.esymm j = (-1) ^ (j + 1) * ∑ a ∈ (Finset.antidiagonal j).filter (fun a => a.1 < j), (-1) ^ a.1 * A.val.esymm a.1 * psumF a.2 A := by
      convert newton_field A j using 1;
    have h_eq' : (j : B) * A'.val.esymm j = (-1) ^ (j + 1) * ∑ a ∈ (Finset.antidiagonal j).filter (fun a => a.1 < j), (-1) ^ a.1 * A'.val.esymm a.1 * psumF a.2 A' := by
      convert newton_field A' j using 1;
    refine' mul_left_cancel₀ ( hchar j hj0 hj ) _;
    rw [ h_eq, h_eq' ];
    refine' congr_arg _ ( Finset.sum_congr rfl fun x hx => _ );
    rw [ ih x.1 ( by aesop ) ( by linarith [ Finset.mem_filter.mp hx, Finset.mem_antidiagonal.mp ( Finset.mem_filter.mp hx |>.1 ) ] ), hmom x.2 ( by linarith [ Finset.mem_filter.mp hx, Finset.mem_antidiagonal.mp ( Finset.mem_filter.mp hx |>.1 ) ] ) ( by linarith [ Finset.mem_filter.mp hx, Finset.mem_antidiagonal.mp ( Finset.mem_filter.mp hx |>.1 ) ] ) ];
  · simp +decide [ Multiset.esymm ];
    interval_cases j ; simp +decide

/-- **Shift-pair collisions are prefix collisions (coefficient form).** For two `m`-sets
`A, A'` (`m = A.card = A'.card`) with equal power sums `p_1, …, p_w` and characteristic
`> w`, the top `w` coefficients of the locator polynomials `Λ_A, Λ_{A'}` agree:
`Λ_A.coeff (m - j) = Λ_{A'}.coeff (m - j)` for `1 ≤ j ≤ w`.  These are exactly the prefix
coordinates read by the identity-prefix map `Φ_w`. -/
theorem shiftpair_prefix_collision (w : ℕ) (A A' : Finset B)
    (hchar : ∀ k, 1 ≤ k → k ≤ w → (k : B) ≠ 0)
    (hcard : A.card = A'.card) (hwcard : w ≤ A.card)
    (hmom : ∀ j, 1 ≤ j → j ≤ w → psumF j A = psumF j A') :
    ∀ j, 1 ≤ j → j ≤ w →
      (loc A).coeff (A.card - j) = (loc A').coeff (A'.card - j) := by
  intro j hj1 hjw
  have h_coeff_A : (loc A).coeff (A.card - j) = (-1) ^ j * A.val.esymm j := by
    convert Multiset.prod_X_sub_C_coeff A.val ( show A.card - j ≤ A.card from Nat.sub_le _ _ ) using 1;
    simp +decide [ Nat.sub_sub_self ( show j ≤ A.card from by linarith ) ]
  have h_coeff_A' : (loc A').coeff (A'.card - j) = (-1) ^ j * A'.val.esymm j := by
    have := Multiset.prod_X_sub_C_coeff A'.val ( show A'.card - j ≤ A'.card from Nat.sub_le _ _ );
    convert this using 2 <;> norm_num [ Nat.sub_sub_self ( show j ≤ #A' from by linarith ) ]
  rw [h_coeff_A, h_coeff_A', shiftpair_esymm_eq w A A' hchar hmom j (by
  exact hjw)]

/-- **Shift-pair collisions are prefix-map collisions.** For `K + w = m = A.card = A'.card`
with characteristic `> w`, a shift-pair collision at depth `w` of two `m`-sets makes them
land in the same fiber of the identity-prefix map `pre K m` (the map `Φ_w` of the Q
ledger). -/
theorem shiftpair_same_prefix (K m : ℕ) (A A' : Finset B)
    (hKm : K ≤ m) (hchar : ∀ k, 1 ≤ k → k ≤ m - K → (k : B) ≠ 0)
    (hcardA : A.card = m) (hcardA' : A'.card = m)
    (hcoll : shiftPairColl (m - K) A A') :
    pre K m A = pre K m A' := by
  ext i;
  have := shiftpair_prefix_collision ( m - K ) A A' hchar ( by linarith ) ( by omega ) hcoll.2;
  convert this ( m - ( K + i ) ) ( Nat.sub_pos_of_lt ( by linarith [ Fin.is_lt i, Nat.sub_add_cancel hKm ] ) ) ( Nat.sub_le_of_le_add ( by linarith [ Fin.is_lt i, Nat.sub_add_cancel hKm ] ) ) using 1 <;> simp +decide [ * ];
  · rw [ Nat.sub_sub_self ( by linarith [ Fin.is_lt i, Nat.sub_add_cancel hKm ] ) ];
    rfl;
  · rw [ Nat.sub_sub_self ( by linarith [ Fin.is_lt i, Nat.sub_add_cancel hKm ] ) ];
    rfl

end RSMCA
