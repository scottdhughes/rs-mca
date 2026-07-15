import RazorbandWitness.NearSidonRazor

/-!
# Razor-band witness package

The package exports the exact two-moment near-Sidon counterexample and repaired
finite razor from `RazorbandWitness.NearSidonRazor`. This root file retains the
legacy universal tangent-floor executable instances.

Legacy source label: `prop:universal-tangent-floor` /
`eq:tangent-floor`, with finite lower bound
`B_{C,Γ}^{MCA}(a) ≥ min{|Γ|, n-a+1}`.

No `sorry`. The general razor module uses Mathlib; the tangent-floor examples
remain dual `native_decide` / `decide` regression fixtures. Neither component
closes the smooth/circle primitive razor band.
-/

namespace RazorbandWitness

/-- Serves K5 razor-band witness kernel (proved sub-fact; band closure open). -/

def minNat (x y : Nat) : Nat := if x ≤ y then x else y

/-- Toy 1. -/
def n1 : Nat := 7
def a1 : Nat := 4
def Gamma1 : Nat := 5
def floor1 : Nat := minNat Gamma1 (n1 - a1 + 1)

theorem floor1_value : floor1 = 4 := by native_decide
theorem floor1_expanded : minNat 5 (7 - 4 + 1) = 4 := by native_decide
theorem floor1_le_Gamma : floor1 ≤ Gamma1 := by native_decide
theorem floor1_le_redundancy : floor1 ≤ n1 - a1 + 1 := by native_decide

/-- Toy 2. -/
def n2 : Nat := 6
def a2 : Nat := 5
def Gamma2 : Nat := 2
def floor2 : Nat := minNat Gamma2 (n2 - a2 + 1)

theorem floor2_value : floor2 = 2 := by native_decide
theorem floor2_tight : floor2 = Gamma2 := by native_decide

/-- Toy 3. -/
def n3 : Nat := 8
def a3 : Nat := 6
def Gamma3 : Nat := 10
def floor3 : Nat := minNat Gamma3 (n3 - a3 + 1)

theorem floor3_value : floor3 = 3 := by native_decide
theorem floor3_is_redundancy : floor3 = n3 - a3 + 1 := by native_decide

/-- a ≥ k+1 shape: for k=2, a=4 is admissible on toy 1. -/
def k1 : Nat := 2
theorem a_ge_k_plus_1 : a1 ≥ k1 + 1 := by native_decide

/-- Positivity: floors are positive (nonempty witness lower bounds). -/
theorem floor1_pos : floor1 > 0 := by native_decide
theorem floor2_pos : floor2 > 0 := by native_decide
theorem floor3_pos : floor3 > 0 := by native_decide

/-! ## Dual via `decide` -/

theorem floor1_value' : floor1 = 4 := by decide
theorem floor2_value' : floor2 = 2 := by decide
theorem floor3_value' : floor3 = 3 := by decide
theorem a_ge_k_plus_1' : a1 ≥ k1 + 1 := by decide
theorem floor1_pos' : floor1 > 0 := by decide

end RazorbandWitness
