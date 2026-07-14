import Mathlib

/-!
# Axis g-damping: elementary finite pieces

Two **PROVED 0-sorry** lemmas feeding the axis (worst monomial-resonance) spectral-gap lattice
bound of `experimental/notes/l1/axis_gdamping_lattice_bound.md`:

1. `cos_lower_bound` — the real-analysis fact `1 - cos(2 pi u) >= 8 u^2` for `|u| <= 1/2`
   (constant `8` tight at `u = +-1/2`), used to reduce the subgroup character gap
   `32 - |G(s)|` to a lattice minimum.
2. `axis_kappa_arith` — the arithmetic assembly: given the two externally-certified hard inputs
   as hypotheses (`delta >= 1.6326865` from the Sage/fplll lattice minima `M+`, `M-`; and
   `logB <= 10.8228` from the analytic saddle bound), the numeric conclusion holds.

The two hard ingredients are **not** formalized: the analytic Cauchy-saddle coefficient estimate is
outside current Mathlib, and the exact lattice minimum has no Mathlib shortest-vector API; both are
supplied by the external certificate `experimental/scripts/verify_axis_gdamping_lattice.sage`.

Constant note: with the **exact** certified constants (`delta = 1.6326865391...`, `lambda = 0.9958595519...`,
`log2 B = 10.8227553355...`) the verifier computes `log2 kappa^2 = -76842.7789` (i.e. `<= -76842.78`),
cross-checked mpmath = Sage.  `axis_kappa_arith` below formalizes the assembly from **decimal-rounded**
hypotheses, which are looser, and therefore proves the slightly weaker but robust `<= -76842.7`.  Both
clear the requirement `<= -82.8` by ~76760 bits.  This module makes no claim about MCA/list proximity
safety or either official prize question.  Verified 0-sorry against Mathlib `v4.28.0`.
-/

open scoped BigOperators Classical

namespace GrandeFinale

/-- `1 - cos(2 pi u) >= 8 u^2` for `|u| <= 1/2`; the constant `8` is tight at `u = +-1/2`.
    Reduces (via `1 - cos(2 pi u) = 2 sin^2(pi u)`) to Jordan's inequality `sin(pi u) >= 2u`. -/
theorem cos_lower_bound (u : ℝ) (hu : |u| ≤ 1 / 2) :
    1 - Real.cos (2 * Real.pi * u) ≥ 8 * u ^ 2 := by
  have key : ∀ t : ℝ, 0 ≤ t → t ≤ 1 / 2 →
      1 - Real.cos (2 * Real.pi * t) ≥ 8 * t ^ 2 := by
    intro t ht0 ht1
    have hsin : 2 * t ≤ Real.sin (Real.pi * t) := by
      have h := Real.le_sin_mul (x := 2 * t) (by linarith) (by linarith)
      rwa [show Real.pi / 2 * (2 * t) = Real.pi * t by ring] at h
    have hcos : Real.cos (2 * Real.pi * t) = 2 * Real.cos (Real.pi * t) ^ 2 - 1 := by
      rw [show 2 * Real.pi * t = 2 * (Real.pi * t) by ring, Real.cos_two_mul]
    have hpyth : Real.sin (Real.pi * t) ^ 2 + Real.cos (Real.pi * t) ^ 2 = 1 :=
      Real.sin_sq_add_cos_sq _
    have h2 : 1 - Real.cos (2 * Real.pi * t) = 2 * Real.sin (Real.pi * t) ^ 2 := by
      rw [hcos]; nlinarith [hpyth]
    rw [ge_iff_le, h2]
    nlinarith [hsin, (by linarith : (0 : ℝ) ≤ 2 * t)]
  have e : |2 * Real.pi * u| = 2 * Real.pi * |u| := by
    rw [abs_mul, abs_of_nonneg (by positivity : (0 : ℝ) ≤ 2 * Real.pi)]
  have habs : Real.cos (2 * Real.pi * u) = Real.cos (2 * Real.pi * |u|) := by
    rw [← Real.cos_abs (2 * Real.pi * u), e]
  rw [habs, ← sq_abs u]
  exact key |u| (abs_nonneg u) hu

/-- Arithmetic assembly of the axis g-damping bound `log2 kappa^2 = 2 logB - lam*2^16*delta/(2 log 2)`.
    Given the certified `delta >= 1.6326865` (Sage/fplll `M+`, `M-`), the saddle bound `logB <= 10.8228`,
    and the admissible window `lam in [0.995859, 1]`, the pure real-number inequality holds.  From these
    decimal-rounded hypotheses the safely-implied constant is `-76842.7`; the exact certified constants
    give `-76842.78` (see the module note). -/
theorem axis_kappa_arith
    (delta lam logB : ℝ)
    (hδ : delta ≥ 1.6326865)
    (hlam_lo : lam ≥ 0.995859)
    (hlam_hi : lam ≤ 1)
    (hB : logB ≤ 10.8228) :
    2 * logB - lam * (2 : ℝ) ^ 16 * delta / (2 * Real.log 2) ≤ -76842.7 := by
  have hlog_hi : Real.log 2 < 0.6931471808 := Real.log_two_lt_d9
  have h2L_pos : (0 : ℝ) < 2 * Real.log 2 := by
    have := Real.log_two_gt_d9; linarith
  have hnum : (106556.65653 : ℝ) ≤ lam * (2 : ℝ) ^ 16 * delta := by
    have e : (2 : ℝ) ^ 16 = 65536 := by norm_num
    rw [e]
    nlinarith [hlam_lo, hδ,
      mul_nonneg (by linarith : (0 : ℝ) ≤ lam - 0.995859)
                 (by linarith : (0 : ℝ) ≤ delta - 1.6326865)]
  have hfrac : (76864.37 : ℝ) ≤ lam * (2 : ℝ) ^ 16 * delta / (2 * Real.log 2) := by
    rw [le_div_iff₀ h2L_pos]
    nlinarith [hnum, hlog_hi]
  linarith [hfrac, hB]

end GrandeFinale
