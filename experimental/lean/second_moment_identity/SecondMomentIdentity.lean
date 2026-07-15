import Std.Tactic

/-!
# Curve second moments and L4 arithmetic gates

This module formalizes the finite combinatorial core of the Lane-C curve
second-moment packet:

* the second moment of finite fibers is the exact number of ordered pairs in a
  common fiber;
* the ordered-pair ledger splits into diagonal and off-diagonal terms;
* Cauchy--Schwarz holds for every finite list of natural fiber sizes;
* a p-fold cover has exactly p times the bucket mass;
* equivariant, weight-preserving twists preserve curve sums.

The deployed L4 transcendental ceilings remain checked by the companion Python
verifier.  This module records only their exact integer fixture and cleared
arithmetic gates.  It does not assert the measured residual law, a local limit,
or an asymptotic equidistribution theorem.

No `sorry`.  Stdlib only.
-/

namespace SecondMomentIdentity

/-! ## Fiber moments -/

/-- Total mass of a finite list of fiber sizes. -/
def sumList : List Nat → Nat
  | [] => 0
  | q :: qs => q + sumList qs

/-- Second moment of a finite list of fiber sizes. -/
def sumSq : List Nat → Nat
  | [] => 0
  | q :: qs => q * q + sumSq qs

/-- Largest fiber size, with value zero on the empty list. -/
def maxList : List Nat → Nat
  | [] => 0
  | q :: qs => Nat.max q (maxList qs)

/-- The elementary two-term inequality used by the list Cauchy--Schwarz proof. -/
theorem twice_mul_le_sq_add_sq (a b : Nat) :
    2 * (a * b) ≤ a * a + b * b := by
  have core (x d : Nat) :
      2 * (x * (x + d)) + d * d = x * x + (x + d) * (x + d) := by
    simp only [Nat.mul_add, Nat.add_mul, Nat.mul_succ, Nat.succ_mul,
      Nat.mul_zero, Nat.zero_mul]
    ac_rfl
  rcases Nat.le_total a b with hab | hba
  · obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hab
    have h := core a d
    omega
  · obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hba
    rw [Nat.mul_comm (b + d) b]
    have h := core b d
    omega

/-- Summed two-term inequality against a fixed head fiber. -/
theorem twice_head_sum_le (a : Nat) (qs : List Nat) :
    2 * (a * sumList qs) ≤ qs.length * (a * a) + sumSq qs := by
  induction qs with
  | nil => simp [sumList, sumSq]
  | cons q qs ih =>
      have hq := twice_mul_le_sq_add_sq a q
      simp only [sumList, sumSq, List.length_cons, Nat.succ_mul,
        Nat.mul_add, Nat.add_mul] at ih ⊢
      omega

/-- Natural-number Cauchy--Schwarz for a complete finite fiber table. -/
theorem cauchySchwarz (qs : List Nat) :
    sumList qs * sumList qs ≤ qs.length * sumSq qs := by
  induction qs with
  | nil => simp [sumList, sumSq]
  | cons q qs ih =>
      have hc := twice_head_sum_le q qs
      simp only [sumList, sumSq, List.length_cons, Nat.succ_mul,
        Nat.mul_add, Nat.add_mul] at ih hc ⊢
      simp only [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc] at ih hc ⊢
      omega

/-- Squaring reflects order on natural numbers. -/
theorem le_of_square_le_square {a b : Nat} (h : a * a ≤ b * b) : a ≤ b := by
  by_cases hab : a ≤ b
  · exact hab
  · have hba : b < a := by omega
    have hpos : 0 < a := Nat.zero_lt_of_lt hba
    have h₁ : b * b ≤ b * a := Nat.mul_le_mul_left b (Nat.le_of_lt hba)
    have h₂ : b * a < a * a := Nat.mul_lt_mul_of_pos_right hba hpos
    have hsq : b * b < a * a := Nat.lt_of_le_of_lt h₁ h₂
    exact False.elim (Nat.not_lt_of_ge h hsq)

/-- Cleared square-root compiler: an upper bound on `p M₂` bounds the mass. -/
theorem mass_le_of_secondMoment_ceiling (qs : List Nat) (B : Nat)
    (hM₂ : qs.length * sumSq qs ≤ B * B) :
    sumList qs ≤ B :=
  le_of_square_le_square (Nat.le_trans (cauchySchwarz qs) hM₂)

/-- The second moment is at most the maximum fiber times the total mass. -/
theorem sumSq_le_max_mul_sum (qs : List Nat) :
    sumSq qs ≤ maxList qs * sumList qs := by
  induction qs with
  | nil => simp [sumSq, maxList, sumList]
  | cons q qs ih =>
      have hq : q * q ≤ Nat.max q (maxList qs) * q :=
        Nat.mul_le_mul_right q (Nat.le_max_left q (maxList qs))
      have ht : sumSq qs ≤ Nat.max q (maxList qs) * sumList qs :=
        Nat.le_trans ih
          (Nat.mul_le_mul_right (sumList qs)
            (Nat.le_max_right q (maxList qs)))
      simpa only [sumSq, maxList, sumList, Nat.mul_add] using
        Nat.add_le_add hq ht

/-! ## Exact ordered-pair count and the shift-pair ledger -/

/-- Ordered Cartesian product of two finite list enumerations. -/
def orderedPairs (xs : List α) (ys : List β) : List (α × β) :=
  match xs with
  | [] => []
  | x :: xs => ys.map (fun y => (x, y)) ++ orderedPairs xs ys

theorem orderedPairs_length (xs : List α) (ys : List β) :
    (orderedPairs xs ys).length = xs.length * ys.length := by
  induction xs with
  | nil => simp [orderedPairs]
  | cons x xs ih =>
      simp [orderedPairs, ih, Nat.succ_mul, Nat.add_comm]

/-- Concatenate the ordered pairs belonging to each indexed curve fiber. -/
def curveOrderedPairs : List (List α) → List (α × α)
  | [] => []
  | fiber :: fibers =>
      orderedPairs fiber fiber ++ curveOrderedPairs fibers

/-- Fiber-size table extracted from explicit finite fiber enumerations. -/
def fiberSizes (fibers : List (List α)) : List Nat :=
  fibers.map List.length

/-- Exact curve second moment: common-fiber ordered pairs are counted by M₂. -/
theorem curveSecondMoment_eq_orderedPairs (fibers : List (List α)) :
    (curveOrderedPairs fibers).length = sumSq (fiberSizes fibers) := by
  induction fibers with
  | nil => simp [curveOrderedPairs, fiberSizes, sumSq]
  | cons fiber fibers ih =>
      simp [curveOrderedPairs, fiberSizes, sumSq, orderedPairs_length, ih]

/-- Off-diagonal ordered pairs, the finite shift-pair ledger. -/
def offDiagonalPairs : List Nat → Nat
  | [] => 0
  | q :: qs => q * (q - 1) + offDiagonalPairs qs

theorem square_eq_diagonal_add_offDiagonal (q : Nat) :
    q * q = q + q * (q - 1) := by
  cases q with
  | zero => simp
  | succ k => simp [Nat.mul_succ, Nat.add_comm]

/-- M₂ is the diagonal mass plus the off-diagonal shift-pair contribution. -/
theorem secondMoment_diagonal_offDiagonal (qs : List Nat) :
    sumSq qs = sumList qs + offDiagonalPairs qs := by
  induction qs with
  | nil => simp [sumSq, sumList, offDiagonalPairs]
  | cons q qs ih =>
      rw [sumSq, sumList, offDiagonalPairs,
        square_eq_diagonal_add_offDiagonal q, ih]
      omega

/-! ## Exact p-fold averaging -/

/-- Replace each bucket weight by exactly `p` copies. -/
def repeatEach (p : Nat) : List Nat → List Nat
  | [] => []
  | q :: qs => List.replicate p q ++ repeatEach p qs

theorem sumList_append (xs ys : List Nat) :
    sumList (xs ++ ys) = sumList xs + sumList ys := by
  induction xs with
  | nil => simp [sumList]
  | cons x xs ih => simp [sumList, ih, Nat.add_assoc]

theorem sumList_replicate (p q : Nat) :
    sumList (List.replicate p q) = p * q := by
  induction p with
  | zero => simp [sumList]
  | succ p ih => simp [sumList, ih, Nat.succ_mul, Nat.add_comm]

/-- Exact p-to-one cover identity: the total curve sum is p times total mass. -/
theorem pFold_average_identity (p : Nat) (weights : List Nat) :
    sumList (repeatEach p weights) = p * sumList weights := by
  induction weights with
  | nil => simp [repeatEach, sumList]
  | cons q weights ih =>
      simp [repeatEach, sumList_append, sumList_replicate, ih, sumList,
        Nat.mul_add]

/-! ## Twist equivariance and orbit constancy -/

/-- Weighted sum along a finite enumeration of curve parameters. -/
def curveSum (theta : Y → S → Z) (weight : Z → Nat) (y : Y) : List S → Nat
  | [] => 0
  | s :: ss => weight (theta y s) + curveSum theta weight y ss

/-- Equivariance plus weight invariance gives equality of twisted curve sums. -/
theorem curveSum_twist
    (theta : Y → S → Z) (weight : Z → Nat)
    (twistY : Y → Y) (twistS : S → S) (twistZ : Z → Z)
    (hequiv : ∀ y s, theta (twistY y) (twistS s) = twistZ (theta y s))
    (hinvariant : ∀ z, weight (twistZ z) = weight z)
    (y : Y) (samples : List S) :
    curveSum theta weight (twistY y) (samples.map twistS) =
      curveSum theta weight y samples := by
  induction samples with
  | nil => simp [curveSum]
  | cons s samples ih =>
      simp [curveSum, hequiv, hinvariant, ih]

/-- A twist-stable parameter enumeration makes the curve sum orbit-constant. -/
theorem curveSum_orbit_constancy
    (theta : Y → S → Z) (weight : Z → Nat)
    (twistY : Y → Y) (twistS : S → S) (twistZ : Z → Z)
    (hequiv : ∀ y s, theta (twistY y) (twistS s) = twistZ (theta y s))
    (hinvariant : ∀ z, weight (twistZ z) = weight z)
    (samples : List S) (hstable : samples.map twistS = samples) (y : Y) :
    curveSum theta weight (twistY y) samples =
      curveSum theta weight y samples := by
  simpa only [hstable] using
    curveSum_twist theta weight twistY twistS twistZ
      hequiv hinvariant y samples

/-! ## Original finite regression examples -/

def Q : List Nat := [3, 2, 1]
def SP : Nat := sumSq Q
def total : Nat := sumList Q
def Qmax : Nat := maxList Q
def orderedPairsByFiber : Nat := 3 * 3 + 2 * 2 + 1 * 1

theorem SP_value : SP = 14 := by native_decide
theorem total_value : total = 6 := by native_decide
theorem Qmax_value : Qmax = 3 := by native_decide
theorem orderedPairs_value : orderedPairsByFiber = 14 := by native_decide
theorem second_moment_identity : SP = orderedPairsByFiber := by native_decide
theorem second_moment_bound : SP ≤ Qmax * total := by
  exact sumSq_le_max_mul_sum Q
theorem second_moment_bound_expanded : 14 ≤ 3 * 6 := by native_decide

def Q2 : List Nat := [2, 2, 2]
def SP2 : Nat := sumSq Q2
def total2 : Nat := sumList Q2
def Qmax2 : Nat := maxList Q2

theorem SP2_value : SP2 = 12 := by native_decide
theorem total2_value : total2 = 6 := by native_decide
theorem identity2 : SP2 = 2 * 2 + 2 * 2 + 2 * 2 := by native_decide
theorem bound2 : SP2 ≤ Qmax2 * total2 := by
  exact sumSq_le_max_mul_sum Q2

/-! ## Exact L4 fixture and cleared arithmetic pins -/

namespace L4

def n : Nat := 131072
def k : Nat := 65537
def m : Nat := 69753
def p : Nat := 2 ^ 31 - 2 ^ 24 + 1
def w : Nat := m - k
def complement : Nat := n - m
def depth : Nat := w + 1
def eMin : Nat := w + 2
def eMax : Nat := Nat.min m complement
def dominantE : Nat := 32632
def stratumCount : Nat := eMax - eMin + 1

theorem fixture :
    p = 2130706433 ∧ w = 4216 ∧ complement = 61319 ∧
      depth = 4217 ∧ eMin = 4218 ∧ eMax = 61319 := by
  native_decide

theorem dominantE_in_range : eMin ≤ dominantE ∧ dominantE < eMax := by
  native_decide

theorem stratumCount_value : stratumCount = 57102 := by
  native_decide

/-- Exact mini-row average pin from the source verifier. -/
theorem miniRow_average_pin : 195 = 13 * 15 := by
  native_decide

/-- The same average pin realized by the generic p-fold compiler. -/
theorem miniRow_pFold :
    sumList (repeatEach 13 [6, 4, 3, 2]) = 195 := by
  native_decide

/-- Row-A cleared Cauchy--Schwarz check: S₁² ≤ p M₂. -/
theorem rowA_cauchySchwarz : 21 * 21 ≤ 97 * 39 := by
  native_decide

/-- Row-B cleared Cauchy--Schwarz check: S₁² ≤ p M₂. -/
theorem rowB_cauchySchwarz : 48 * 48 ≤ 97 * 144 := by
  native_decide

end L4

end SecondMomentIdentity
