import Mathlib

/-!
# Excess-one interior chart as a curve sum of prefix fibres

This module formalizes the exact finite decomposition in
`experimental/notes/thresholds/cap25_v13_bc_l4_interior_chart_to_q.md`.

At excess one, the first coefficient chooses a scalar `s`. The remaining
twisted prefix equations recursively force an ordinary depth-`(w+1)` prefix
on the explicit curve

```
phi 0 = s,
phi (j+1) = z (j+1) + (s - z 0) * phi j.
```

Partitioning valid supports by their first coefficient therefore gives an
exact sum of `|B|` ordinary prefix fibres. A uniform max-fibre bound then
pays the chart with the explicit factor `|B|`.

The deployed L4 arithmetic, heuristic curve equidistribution, non-planted
words, and deeper excess profiles are not consequences of this module.
-/

namespace SyndromeLine.InteriorChartCopyDecomposition

open Finset BigOperators

variable {B : Type*} [Field B]

/-- The explicit excess-one recurrence curve through prefix space. -/
def chartCurve (z : ℕ → B) (s : B) : ℕ → B
  | 0 => s
  | j + 1 => z (j + 1) + (s - z 0) * chartCurve z s j

/-- Equality of coefficient sequences through depth `w+1`, indexed `0..w`. -/
def prefixEq (w : ℕ) (a b : ℕ → B) : Prop :=
  ∀ j, j ≤ w → a j = b j

/-- The excess-one twisted prefix equations after eliminating the residual root. -/
def twistedPrefix (w : ℕ) (z a : ℕ → B) : Prop :=
  ∀ j, 1 ≤ j → j ≤ w →
    a j - (a 0 - z 0) * a (j - 1) = z j

/--
For a fixed first coefficient `s`, the twisted equations are exactly ordinary
prefix equality along `chartCurve z s`.
-/
theorem twistedPrefix_iff_prefixEq_chartCurve
    (w : ℕ) (z a : ℕ → B) (s : B) (h0 : a 0 = s) :
    twistedPrefix w z a ↔ prefixEq w a (chartCurve z s) := by
  constructor
  · intro htw j hj
    induction j with
    | zero =>
        simpa [chartCurve] using h0
    | succ j ih =>
        have heq := htw (j + 1) (by omega) hj
        have hprev := ih (by omega)
        simp only [Nat.add_sub_cancel] at heq
        rw [h0, hprev] at heq
        exact (sub_eq_iff_eq_add.mp heq).trans (by
          simp [chartCurve])
  · intro hp j hj1 hjw
    obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (n := j) (by omega)
    have hprev := hp k (by omega)
    have hnext := hp (k + 1) hjw
    change a (k + 1) - (a 0 - z 0) * a k = z (k + 1)
    rw [h0, hprev, hnext]
    simp [chartCurve]

variable {A : Type*}

/-- Supports satisfying the eliminated excess-one twisted equations. -/
noncomputable def validSupports
    (Ω : Finset A) (coeff : A → ℕ → B)
    (w : ℕ) (z : ℕ → B) : Finset A := by
  classical
  exact Ω.filter fun T => twistedPrefix w z (coeff T)

/-- An ordinary prefix fibre through depth `w+1`. -/
noncomputable def prefixFiber
    (Ω : Finset A) (coeff : A → ℕ → B)
    (w : ℕ) (v : ℕ → B) : Finset A := by
  classical
  exact Ω.filter fun T => prefixEq w (coeff T) v

variable [DecidableEq B]

/--
The slice with first coefficient `s` is exactly the ordinary prefix fibre at
`chartCurve z s`.
-/
theorem valid_slice_eq_prefixFiber
    (Ω : Finset A) (coeff : A → ℕ → B)
    (w : ℕ) (z : ℕ → B) (s : B) :
    (validSupports Ω coeff w z).filter (fun T => coeff T 0 = s) =
      prefixFiber Ω coeff w (chartCurve z s) := by
  classical
  ext T
  simp only [validSupports, prefixFiber, Finset.mem_filter]
  constructor
  · rintro ⟨⟨hT, htw⟩, h0⟩
    exact ⟨hT,
      (twistedPrefix_iff_prefixEq_chartCurve w z (coeff T) s h0).mp htw⟩
  · rintro ⟨hT, hp⟩
    have h0 : coeff T 0 = s := by
      have := hp 0 (Nat.zero_le w)
      simpa [chartCurve] using this
    exact ⟨⟨hT,
      (twistedPrefix_iff_prefixEq_chartCurve w z (coeff T) s h0).mpr hp⟩,
      h0⟩

variable [Fintype B]

/--
Exact interior-chart decomposition:
`#valid = sum_(s in B) #prefixFiber(chartCurve z s)`.
-/
theorem valid_card_eq_sum_curve_prefixFibers
    (Ω : Finset A) (coeff : A → ℕ → B)
    (w : ℕ) (z : ℕ → B) :
    (validSupports Ω coeff w z).card =
      ∑ s ∈ (Finset.univ : Finset B),
        (prefixFiber Ω coeff w (chartCurve z s)).card := by
  classical
  have hsum :=
    Finset.sum_card_fiberwise_eq_card_filter
      (validSupports Ω coeff w z) (Finset.univ : Finset B)
      (fun T => coeff T 0)
  have hall :
      (validSupports Ω coeff w z).filter
          (fun T => coeff T 0 ∈ (Finset.univ : Finset B)) =
        validSupports Ω coeff w z := by
    simp
  rw [hall] at hsum
  calc
    (validSupports Ω coeff w z).card =
        ∑ s ∈ (Finset.univ : Finset B),
          ((validSupports Ω coeff w z).filter
            (fun T => coeff T 0 = s)).card := hsum.symm
    _ = ∑ s ∈ (Finset.univ : Finset B),
          (prefixFiber Ω coeff w (chartCurve z s)).card := by
      apply Finset.sum_congr rfl
      intro s _
      rw [valid_slice_eq_prefixFiber]

/--
Discharge to a uniform ordinary-prefix max-fibre bound.
-/
theorem valid_card_le_fieldCard_mul_maxFiber
    (Ω : Finset A) (coeff : A → ℕ → B)
    (w : ℕ) (z : ℕ → B) (M : ℕ)
    (hmax : ∀ v : ℕ → B, (prefixFiber Ω coeff w v).card ≤ M) :
    (validSupports Ω coeff w z).card ≤ Fintype.card B * M := by
  rw [valid_card_eq_sum_curve_prefixFibers]
  calc
    ∑ s ∈ (Finset.univ : Finset B),
        (prefixFiber Ω coeff w (chartCurve z s)).card ≤
      ∑ _s ∈ (Finset.univ : Finset B), M := by
        exact Finset.sum_le_sum fun s _ => hmax (chartCurve z s)
    _ = Fintype.card B * M := by simp

/--
Ray-count compiler: if every ray has a valid support representative, the same
`|B| * maxFiber` bound applies to the ray count.
-/
theorem rayCount_le_fieldCard_mul_maxFiber
    (Ω : Finset A) (coeff : A → ℕ → B)
    (w : ℕ) (z : ℕ → B) (M rayCount : ℕ)
    (hrays : rayCount ≤ (validSupports Ω coeff w z).card)
    (hmax : ∀ v : ℕ → B, (prefixFiber Ω coeff w v).card ≤ M) :
    rayCount ≤ Fintype.card B * M :=
  hrays.trans (valid_card_le_fieldCard_mul_maxFiber Ω coeff w z M hmax)

#print axioms twistedPrefix_iff_prefixEq_chartCurve
#print axioms valid_slice_eq_prefixFiber
#print axioms valid_card_eq_sum_curve_prefixFibers
#print axioms valid_card_le_fieldCard_mul_maxFiber
#print axioms rayCount_le_fieldCard_mul_maxFiber

end SyndromeLine.InteriorChartCopyDecomposition
