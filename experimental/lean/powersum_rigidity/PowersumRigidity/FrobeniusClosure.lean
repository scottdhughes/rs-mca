import Mathlib
import PowersumRigidity.FrobeniusInversion

/-!
# The Frobenius closure primitive shared by the reciprocal-gap theorem and PR #451

Both the Mersenne reciprocal-gap theorem of this package
(`FrobeniusInversion.mersenne_reciprocal_gap`) and the cyclotomic-defect fiber
bound of upstream PR #451 (`asymptotic_c9_frobenius_cyclotomic_defect.md`,
Theorem 1) rest on one characteristic-`p` primitive: for coefficients `a i`
fixed by the Frobenius `x ↦ x ^ p` (`(a i) ^ p = a i`, i.e. lying in the prime
field `F_p`),

`(∑ i ∈ s, a i * ω i) ^ p = ∑ i ∈ s, a i * (ω i) ^ p`.

This is `sum_smul_pow` below. Its two specialisations:

* **This package (order-2 Frobenius).** Take `a = 1`, `ω = (· ^ j)`: this is the
  power-sum Frobenius identity `p_j(B) ^ p = p_{jp}(B)` (`psum_pow`).
  `FrobeniusInversion.psum_inv_eq_psum_pow` (L5) is exactly this, then
  specialised on `μ_{p+1}` via `x ^ p = x⁻¹` — the *inversion* (order-2)
  Frobenius that drives the reciprocal-gap coset rigidity.

* **PR #451 (general Frobenius).** Take `a i = coeff_i ∈ F_p`, `ω i = ζ^{i k}`:
  this is PR #451's Theorem-1 evaluation step
  `f_x(ζ^{p k}) = f_x(ζ^{k}) ^ p`, i.e. `eval_pow` / `root_pow` below — an
  `F_p`-polynomial's root set is closed under `x ↦ x ^ p` (Frobenius closure),
  the *"standard cyclic-code dimension"* step PR #451 invokes. This module
  supplies a machine-checked (zero-`sorry`) proof of that step, backing the
  cyclic-code-dimension mechanism common to both lanes.

## Main results

* `FrobeniusClosure.sum_smul_pow` — the shared primitive.
* `FrobeniusClosure.psum_pow` — the power-sum Frobenius identity `p_j ^ p = p_{jp}`
  (the reciprocal-gap / order-2 specialisation, `a = 1`).
* `FrobeniusClosure.eval_pow` — `f(x^p) = f(x)^p` for `F_p`-coefficient `f`
  (PR #451's Theorem-1 evaluation step).
* `FrobeniusClosure.root_pow` — Frobenius closure of the root set: a root's
  `p`-th power is again a root (PR #451's "root set is Frobenius invariant").
-/

open Finset Polynomial

namespace FrobeniusClosure

attribute [local instance] Classical.propDecidable

variable {K : Type*} [Field K] {p : ℕ} [Fact (Nat.Prime p)] [CharP K p]

/-- **The shared Frobenius primitive.** In characteristic `p`, if each coefficient
`a i` is fixed by Frobenius (`(a i) ^ p = a i`, i.e. in the prime field `F_p`),
then the `p`-th power distributes coefficient-wise:
`(∑ i ∈ s, a i * ω i) ^ p = ∑ i ∈ s, a i * (ω i) ^ p`. -/
theorem sum_smul_pow {ι : Type*} (s : Finset ι) (a ω : ι → K)
    (ha : ∀ i ∈ s, a i ^ p = a i) :
    (∑ i ∈ s, a i * ω i) ^ p = ∑ i ∈ s, a i * ω i ^ p := by
  rw [sum_pow_char]
  refine Finset.sum_congr rfl fun i hi => ?_
  rw [mul_pow, ha i hi]

/-- **Power-sum Frobenius identity** `p_j(B) ^ p = p_{jp}(B)` — the `a = 1`,
`ω = (· ^ j)` case of `sum_smul_pow`.  `FrobeniusInversion.psum_inv_eq_psum_pow`
(L5) is this identity specialised on `μ_{p+1}` via `x ^ p = x⁻¹`, the order-2
Frobenius that yields the reciprocal-gap coset rigidity. -/
theorem psum_pow (B : Finset K) (j : ℕ) :
    (∑ x ∈ B, x ^ j) ^ p = ∑ x ∈ B, x ^ (j * p) := by
  rw [sum_pow_char]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [pow_mul]

/-- **PR #451 Theorem-1 evaluation step.**  For a polynomial `f` whose
coefficients are fixed by Frobenius (`(f.coeff i) ^ p = f.coeff i`, i.e. lie in
`F_p`), the `p`-power Frobenius commutes with evaluation: `f(x ^ p) = f(x) ^ p`. -/
theorem eval_pow (f : K[X]) (hf : ∀ i, f.coeff i ^ p = f.coeff i) (x : K) :
    f.eval (x ^ p) = f.eval x ^ p := by
  conv_rhs => rw [eval_eq_sum_range]
  rw [eval_eq_sum_range, sum_pow_char]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [mul_pow, hf i, pow_right_comm]

/-- **Frobenius closure of the root set (PR #451).**  If `f` has `F_p`
coefficients and `x` is a root, then `x ^ p` is also a root.  Iterating,
`f` vanishes on the whole Frobenius orbit of any root — the closure
`Z_p(N,I)` in PR #451's Theorem 1, whence the cyclic-code dimension count. -/
theorem root_pow (f : K[X]) (hf : ∀ i, f.coeff i ^ p = f.coeff i) {x : K}
    (hx : f.eval x = 0) : f.eval (x ^ p) = 0 := by
  rw [eval_pow f hf x, hx, zero_pow (Fact.out : Nat.Prime p).pos.ne']

end FrobeniusClosure
