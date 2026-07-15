import SyndromeSecant.BalancedCoreTransverseSecant

/-!
# Exact syndrome–secant compiler instance and balanced-core theorem

The package exports the general field-independent fixed-chart theorem from
`SyndromeSecant.BalancedCoreTransverseSecant`. This root file also retains the
original finite executable regression instance for hard inputs (a)/(c).

Legacy source labels (frontiers draft):
- thm:syndrome-secant-exact L1607
- eq:transverse-secant-count L1615 (tag 3.3)
- eq:exact-secant-numerator L1621 (tag 3.4)

Finite regression instance:
- t=1 over F_5², with parity columns (1,x);
- per-E uniqueness for empty and singleton supports;
- exact Θ count 5 for the displayed line;
- dual `native_decide` / `decide` checks.

No `sorry`. The general theorem uses Mathlib; the executable instance remains
an isolated finite regression fixture.
-/

namespace SyndromeSecant

-- Hard inputs (a)/(c): transverse secant incidence count.

def q : Nat := 5

def add (x y : Nat) : Nat := (x + y) % q
def mul (x y : Nat) : Nat := (x * y) % q

def y0 : Nat × Nat := (1, 1)
def y1 : Nat × Nat := (0, 1)

def linePt (γ : Nat) : Nat × Nat :=
  (add y0.1 (mul γ y1.1), add y0.2 (mul γ y1.2))

/-- V_∅ = {0}. -/
def inVEmpty (v : Nat × Nat) : Bool := v.1 == 0 && v.2 == 0

/-- V_{{x}} = span{(1,x)}. -/
def inVPoint (x : Nat) (v : Nat × Nat) : Bool := v.2 == mul v.1 x

def transverse (inV : Nat × Nat → Bool) : Bool :=
  !(inV y0 && inV y1)

def hitsEmpty (γ : Nat) : Bool :=
  inVEmpty (linePt γ) && transverse inVEmpty

def hitsPoint (x γ : Nat) : Bool :=
  inVPoint x (linePt γ) && transverse (inVPoint x)

def gammas : List Nat := [0, 1, 2, 3, 4]
def points : List Nat := [0, 1, 2, 3, 4]

/-- Count γ with hitsEmpty. -/
def countEmpty : Nat :=
  gammas.foldl (fun acc γ => if hitsEmpty γ then acc + 1 else acc) 0

/-- Count γ with hitsPoint x. -/
def countPoint (x : Nat) : Nat :=
  gammas.foldl (fun acc γ => if hitsPoint x γ then acc + 1 else acc) 0

/-- γ is in Θ if it hits empty or some singleton. -/
def inTheta (γ : Nat) : Bool :=
  hitsEmpty γ ||
    points.foldl (fun acc x => acc || hitsPoint x γ) false

def Theta : Nat :=
  gammas.foldl (fun acc γ => if inTheta γ then acc + 1 else acc) 0

/-! ## Per-E uniqueness (thm:syndrome-secant-exact fixed-E clause) -/

theorem countEmpty_le_1 : countEmpty ≤ 1 := by native_decide
theorem countEmpty_value : countEmpty = 0 := by native_decide

theorem countPoint0_le_1 : countPoint 0 ≤ 1 := by native_decide
theorem countPoint1_le_1 : countPoint 1 ≤ 1 := by native_decide
theorem countPoint2_le_1 : countPoint 2 ≤ 1 := by native_decide
theorem countPoint3_le_1 : countPoint 3 ≤ 1 := by native_decide
theorem countPoint4_le_1 : countPoint 4 ≤ 1 := by native_decide

theorem countPoint0_value : countPoint 0 = 1 := by native_decide
theorem countPoint1_value : countPoint 1 = 1 := by native_decide
theorem countPoint2_value : countPoint 2 = 1 := by native_decide
theorem countPoint3_value : countPoint 3 = 1 := by native_decide
theorem countPoint4_value : countPoint 4 = 1 := by native_decide

/-! ## Exact Θ_t count for this (y0,y1) -/

theorem Theta_value : Theta = 5 := by native_decide
theorem Theta_full : Theta = q := by native_decide

/-- Explicit which γ hits which singleton E={x}: γ = x-1 mod 5 for our y. -/
theorem hits_0_at_4 : hitsPoint 0 4 = true := by native_decide
theorem hits_1_at_0 : hitsPoint 1 0 = true := by native_decide
theorem hits_2_at_1 : hitsPoint 2 1 = true := by native_decide
theorem hits_3_at_2 : hitsPoint 3 2 = true := by native_decide
theorem hits_4_at_3 : hitsPoint 4 3 = true := by native_decide

/-- Transverse non-containment for the generators vs V_{{0}}. -/
theorem transverse_pt0 : transverse (inVPoint 0) = true := by native_decide

/-! ## Dual via `decide` -/

theorem countEmpty_le_1' : countEmpty ≤ 1 := by decide
theorem countPoint0_le_1' : countPoint 0 ≤ 1 := by decide
theorem Theta_value' : Theta = 5 := by decide
theorem hits_0_at_4' : hitsPoint 0 4 = true := by decide
theorem hits_1_at_0' : hitsPoint 1 0 = true := by decide

end SyndromeSecant
