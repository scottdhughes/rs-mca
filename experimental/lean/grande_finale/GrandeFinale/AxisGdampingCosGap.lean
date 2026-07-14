import Mathlib

/-!
# Axis g-damping: the elementary cosine-gap inequality

This module is a **PROVED elementary lemma** feeding the axis (worst monomial-resonance)
spectral-gap lattice bound of
`experimental/notes/l1/axis_gdamping_lattice_bound.md`.

It proves the single real-analysis fact used to reduce the subgroup character gap
`32 - |G(s)|` to a lattice minimum:
`1 - cos(2 pi u) >= 8 u^2` for `|u| <= 1/2` (constant `8` is tight at `u = +-1/2`,
where `1 - cos(pi) = 2 = 8 * (1/2)^2`).

The remaining ingredients of the axis bound (the Cauchy-saddle coefficient estimate and the
exact lattice minima `M+`, `M-`) are **not** formalized here: the analytic saddle bound is
outside current Mathlib, and the exact lattice minimum is supplied by the external Sage/fplll +
PARI certificate `experimental/scripts/verify_axis_gdamping_lattice.sage`.  This module makes no
claim about MCA/list proximity safety or either official prize question.

Verified 0-sorry against Mathlib `v4.28.0`.
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

end GrandeFinale
