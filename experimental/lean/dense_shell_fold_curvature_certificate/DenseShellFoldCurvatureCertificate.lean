import Std.Tactic

/-!
# Dense-shell FOLD weighted-curvature certificate

This stdlib-only module kernel-checks the exact linear-arithmetic compiler in
`experimental/notes/thresholds/dense_shell_fold_curvature_certificate.md`.
It proves the 17-drop weighted summation-by-parts identity, the exact cleared
FOLD equivalence, the sharper concave-drop implication, the oriented third-
difference sign convention, and the quadratic-profile arithmetic.

The module does not assert that the realized dense-shell profile satisfies
monotonicity or the curvature hypotheses.  Full FOLD remains open.
-/

namespace DenseShellFoldCurvatureCertificate

set_option autoImplicit false

def spread17
    (p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 : Int) : Int :=
  p0 + p1 + p2 + p3 + p4 + p5 + p6 + p7 +
    p8 + p9 + p10 + p11 + p12 + p13 + p14 + p15

def weightedCurvature18
    (p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 : Int) : Int :=
  15 * (p2 - 2 * p1 + p0) +
  28 * (p3 - 2 * p2 + p1) +
  39 * (p4 - 2 * p3 + p2) +
  48 * (p5 - 2 * p4 + p3) +
  55 * (p6 - 2 * p5 + p4) +
  60 * (p7 - 2 * p6 + p5) +
  63 * (p8 - 2 * p7 + p6) +
  64 * (p9 - 2 * p8 + p7) +
  63 * (p10 - 2 * p9 + p8) +
  60 * (p11 - 2 * p10 + p9) +
  55 * (p12 - 2 * p11 + p10) +
  48 * (p13 - 2 * p12 + p11) +
  39 * (p14 - 2 * p13 + p12) +
  28 * (p15 - 2 * p14 + p13) +
  15 * (p16 - 2 * p15 + p14)

/-- Exact weighted summation by parts for all 17-drop vectors. -/
theorem weighted_curvature_identity
    (p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 : Int) :
    2 * spread17 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 =
      17 * p0 + 15 * p16 -
        weightedCurvature18 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 := by
  simp only [spread17, weightedCurvature18]
  omega

/-- Once the endpoint spreads are sums of oriented nonnegative drops, the
`57/50` fold is exactly equivalent to the weighted-curvature certificate. -/
theorem fold_iff_weighted_curvature
    (p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 : Int) :
    50 *
        (spread17 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 + p16) <=
      57 * spread17 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 ↔
    7 * weightedCurvature18 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 <=
      119 * p0 + 5 * p16 := by
  simp only [spread17, weightedCurvature18]
  omega

/-- The aggregate concave-curvature condition gives the sharper `17/15`
cleared fold.  Pointwise nonpositive curvatures imply `hK` below. -/
theorem fold_17_15_from_curvature_sum
    (p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 : Int)
    (hp0 : 0 <= p0)
    (hK : weightedCurvature18 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 <= 0) :
    15 *
        (spread17 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 + p16) <=
      17 * spread17 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 := by
  have hId := weighted_curvature_identity
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16
  simp only [spread17, weightedCurvature18] at hK hId ⊢
  omega

/-- Positive spread transports the sharper `17/15` bound to `57/50`. -/
theorem fold_57_50_from_17_15 (S p16 : Int)
    (hS : 0 <= S) (h1715 : 15 * (S + p16) <= 17 * S) :
    50 * (S + p16) <= 57 * S := by
  omega

/-- Positive weights preserve pointwise nonpositivity. -/
theorem weighted_sum_of_nonpositive_curvatures
    (k0 k1 k2 k3 k4 k5 k6 k7 k8 k9 k10 k11 k12 k13 k14 : Int)
    (h0 : k0 <= 0) (h1 : k1 <= 0) (h2 : k2 <= 0)
    (h3 : k3 <= 0) (h4 : k4 <= 0) (h5 : k5 <= 0)
    (h6 : k6 <= 0) (h7 : k7 <= 0) (h8 : k8 <= 0)
    (h9 : k9 <= 0) (h10 : k10 <= 0) (h11 : k11 <= 0)
    (h12 : k12 <= 0) (h13 : k13 <= 0) (h14 : k14 <= 0) :
    15*k0 + 28*k1 + 39*k2 + 48*k3 + 55*k4 +
      60*k5 + 63*k6 + 64*k7 + 63*k8 + 60*k9 +
      55*k10 + 48*k11 + 39*k12 + 28*k13 + 15*k14 <= 0 := by
  omega

/-- For decreasing profiles, drop curvature is minus the third forward
difference. -/
theorem decreasing_curvature_eq_neg_third_difference
    (L0 L1 L2 L3 : Int) :
    (L2 - L3) - 2 * (L1 - L2) + (L0 - L1) =
      -(L3 - 3*L2 + 3*L1 - L0) := by
  omega

/-- The increasing orientation reverses the preceding sign. -/
theorem increasing_curvature_eq_third_difference
    (L0 L1 L2 L3 : Int) :
    (L3 - L2) - 2 * (L2 - L1) + (L1 - L0) =
      L3 - 3*L2 + 3*L1 - L0 := by
  omega

theorem curvature_weight_sum :
    15 + 28 + 39 + 48 + 55 + 60 + 63 + 64 +
      63 + 60 + 55 + 48 + 39 + 28 + 15 = (680 : Nat) := by
  decide

/-- Odd-drop sums for `L_i=A-C i^2`. -/
theorem quadratic_window_sums (C : Int) :
    C + 3*C + 5*C + 7*C + 9*C + 11*C + 13*C + 15*C +
        17*C + 19*C + 21*C + 23*C + 25*C + 27*C + 29*C + 31*C = 256*C ∧
    C + 3*C + 5*C + 7*C + 9*C + 11*C + 13*C + 15*C +
        17*C + 19*C + 21*C + 23*C + 25*C + 27*C + 29*C + 31*C + 33*C = 289*C := by
  constructor <;> omega

theorem quadratic_ratio_below_fold : 289 * 50 < 57 * 256 := by
  decide

end DenseShellFoldCurvatureCertificate
