import Mathlib

/-!
# All-LineRay affine-core set-pair theorem: statement target

This module is an **UNPROVED STATEMENT TARGET** for
`experimental/notes/thresholds/all_lineray_affine_core_set_pair.md`.
It makes the field-general all-pair theorem and its direct LineRay
specialization type-check without claiming a Lean proof.

The target deliberately counts every distinct `(slope,error)` pair.  Its
LineRay specialization therefore counts every `(slope,codeword)` pair,
including multiple codewords at one slope; no witness selector occurs in the
definitions below.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace AllLineRayAffineCore

set_option autoImplicit false

universe u v w

variable {D : Type u} {F : Type v} {W : Type w}
variable [Fintype D] [DecidableEq D]
variable [Field F] [DecidableEq F]
variable [AddCommGroup W] [Module F W]

/-! ## Supports, distance, and the all-pair affine core -/

/-- The finite support of a word. -/
def wordSupport (e : D → F) : Finset D :=
  Finset.univ.filter fun x => e x ≠ 0

/-- Hamming weight on the finite coordinate set `D`. -/
def weight (e : D → F) : ℕ :=
  (wordSupport e).card

/-- A word is supported inside the supplied coordinate set. -/
def SupportedIn (S : Finset D) (e : D → F) : Prop :=
  ∀ x, x ∉ S → e x = 0

/-- A syndrome has a lift supported inside the support of `e`. -/
def InSupportImage (H : (D → F) →ₗ[F] W) (e : D → F) (y : W) : Prop :=
  ∃ z : D → F, SupportedIn (wordSupport e) z ∧ H z = y

/-- The kernel of `H` has minimum distance strictly greater than `t`, written
without choosing or computing a minimum-weight kernel word. -/
def KernelDistanceAbove (H : (D → F) →ₗ[F] W) (t : ℕ) : Prop :=
  ∀ z : D → F, H z = 0 → z ≠ 0 → t < weight z

/-- All pairwise error differences in a finite indexed family. -/
def errorDifferences {I : Type*} (P : Finset I) (err : I → D → F) :
    Set (D → F) :=
  {z | ∃ i ∈ P, ∃ j ∈ P, z = err i - err j}

/-- The direction space of the affine hull of all errors in `P`. -/
def affineDirectionSpan {I : Type*} (P : Finset I) (err : I → D → F) :
    Submodule F (D → F) :=
  Submodule.span F (errorDifferences P err)

/-- The affine-core dimension `s` of all errors in `P`. -/
def affineDim {I : Type*} (P : Finset I) (err : I → D → F) : ℕ :=
  Module.finrank F (affineDirectionSpan P err)

/-- The largest error weight in `P`; it is `0` for the empty family. -/
def maxWeight {I : Type*} (P : Finset I) (err : I → D → F) : ℕ :=
  P.sup fun i => weight (err i)

/-! ## Complete `(slope,error)` pair theorem -/

/-- The exact hypotheses for a finite set of distinct `(slope,error)` pairs.
Distinctness is carried by the `Finset` itself.  The last conjunct is the
support-wise transversality condition
`{y₀,y₁} ⊈ H(F^support(error))`. -/
def PairHypotheses (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (F × (D → F))) (t : ℕ) : Prop :=
  y₁ ≠ 0 ∧
    (∀ p ∈ P, H p.2 = y₀ + p.1 • y₁) ∧
    (∀ p ∈ P, weight p.2 ≤ t) ∧
    KernelDistanceAbove H t ∧
    (∀ p ∈ P,
      ¬ (InSupportImage H p.2 y₀ ∧ InSupportImage H p.2 y₁))

/-- The nonuniform Bollobás charge and the two binomial cardinality bounds
claimed for a finite indexed error family. -/
def AffineCoreConclusion {I : Type*} (P : Finset I)
    (err : I → D → F) : Prop :=
  let s := affineDim P err
  let w := maxWeight P err
  (∑ i ∈ P, ((Nat.choose (s + weight (err i)) s : ℚ)⁻¹)) ≤ 1 ∧
    P.card ≤ Nat.choose (s + w) s ∧
    Nat.choose (s + w) s ≤ Nat.choose (Fintype.card D) s

/-- The all-pair conclusion specialized to literal `(slope,error)` pairs. -/
def PairConclusion (P : Finset (F × (D → F))) : Prop :=
  AffineCoreConclusion P fun p => p.2

/-- **UNPROVED STATEMENT TARGET (all-pair form).**  Every finite family of
distinct `(slope,error)` pairs satisfying the syndrome-line, weight,
kernel-distance, and support-transversality hypotheses obeys the exact
nonuniform charge and both binomial bounds. -/
def theoremTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (F × (D → F))) (t : ℕ) : Prop :=
  PairHypotheses H y₀ y₁ P t → PairConclusion P

/-! ## Two-level slope-fiber target -/

/-- The subfamily of pairs carried by one slope. -/
def slopeFiber (P : Finset (F × (D → F))) (γ : F) :
    Finset (F × (D → F)) :=
  P.filter fun p => p.1 = γ

/-- `R` is a subfamily of `P` containing exactly one pair above every slope
that occurs in `P`. -/
def OnePerSlope (P R : Finset (F × (D → F))) : Prop :=
  R ⊆ P ∧
    ∀ γ ∈ P.image (fun p => p.1),
      ∃! p, p ∈ R ∧ p.1 = γ

/-- The two-level rational charge.  The outer factor is the affine-core
charge of the chosen representative, while the inner sum is the complete
all-pair charge of its slope fiber. -/
def nestedRationalCharge (P R : Finset (F × (D → F)))
    (err : (F × (D → F)) → D → F) : ℚ :=
  let r := affineDim R err
  ∑ p ∈ R,
    ((Nat.choose (r + weight (err p)) r : ℚ)⁻¹) *
      (let Q := slopeFiber P p.1
       let sγ := affineDim Q err
       ∑ q ∈ Q,
         ((Nat.choose (sγ + weight (err q)) sγ : ℚ)⁻¹))

/-- The largest same-slope affine-core binomial cap, maximized only over
slopes that actually occur in `P`.  It is `0` for the empty family. -/
def maxSlopeFiberCap (P : Finset (F × (D → F)))
    (err : (F × (D → F)) → D → F) : ℕ :=
  (P.image (fun p => p.1)).sup fun γ =>
    let Q := slopeFiber P γ
    let sγ := affineDim Q err
    let wγ := maxWeight Q err
    Nat.choose (sγ + wγ) sγ

/-- The sum of the same-slope direction spaces over all slopes occurring in
`P`.  This is the `sum_gamma A_gamma` term in (TL3)--(TL4). -/
def slopeFiberDirectionSum (P : Finset (F × (D → F)))
    (err : (F × (D → F)) → D → F) : Submodule F (D → F) :=
  ∑ γ ∈ P.image (fun p => p.1),
    affineDirectionSpan (slopeFiber P γ) err

/-- The exact selector-plus-fibers direction-space identity (TL3). -/
def TwoLevelDirectionDecomposition (P R : Finset (F × (D → F)))
    (err : (F × (D → F)) → D → F) : Prop :=
  affineDirectionSpan P err =
    affineDirectionSpan R err + slopeFiberDirectionSum P err

/-- The rank and kernel-intersection identities in (TL4). -/
def TwoLevelKernelDecomposition (H : (D → F) →ₗ[F] W)
    (P R : Finset (F × (D → F)))
    (err : (F × (D → F)) → D → F) : Prop :=
  Module.finrank F ↥(affineDirectionSpan R err ⊓ LinearMap.ker H) + 1 =
      affineDim R err ∧
    affineDirectionSpan P err ⊓ LinearMap.ker H =
      (affineDirectionSpan R err ⊓ LinearMap.ker H) +
        slopeFiberDirectionSum P err

/-- Nested charge and product-cardinality conclusion for an arbitrary error
map on the pair indices.  The outer maximum weight is computed on `R`, not on
the full family. -/
def TwoLevelConclusion (P R : Finset (F × (D → F)))
    (err : (F × (D → F)) → D → F) : Prop :=
  let r := affineDim R err
  let w := maxWeight R err
  nestedRationalCharge P R err ≤ 1 ∧
    P.card ≤ Nat.choose (r + w) r * maxSlopeFiberCap P err

/-- The two-level conclusion for literal `(slope,error)` pairs. -/
def PairTwoLevelConclusion (P R : Finset (F × (D → F))) : Prop :=
  TwoLevelConclusion P R fun p => p.2

/-- **UNPROVED STATEMENT TARGET (two-level pair form).**  Choose one actual
pair per occurring slope, charge those representatives by their affine core,
and charge every complete same-slope fiber by its own affine core.  The nested
rational charge is at most one and the full pair count obeys the corresponding
product bound. -/
def pairTwoLevelTheoremTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P R : Finset (F × (D → F))) (t : ℕ) : Prop :=
  PairHypotheses H y₀ y₁ P t →
    OnePerSlope P R →
    PairTwoLevelConclusion P R

/-- **UNPROVED STATEMENT TARGET (pair TL3).**  One representative per slope
gives the exact selector-plus-fibers decomposition of the full direction
space. -/
def pairDirectionDecompositionTarget (P R : Finset (F × (D → F))) : Prop :=
  OnePerSlope P R →
    TwoLevelDirectionDecomposition P R fun p => p.2

/-- **UNPROVED STATEMENT TARGET (pair TL4).**  With at least two slopes, the
selector direction loses exactly one dimension on intersection with `ker H`,
and the kernel part of the full direction space decomposes exactly. -/
def pairKernelDecompositionTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P R : Finset (F × (D → F))) (t : ℕ) : Prop :=
  PairHypotheses H y₀ y₁ P t →
    OnePerSlope P R →
    1 < (P.image (fun p => p.1)).card →
    TwoLevelKernelDecomposition H P R fun p => p.2

/-! ## Direct LineRay specialization -/

/-- Error attached to a LineRay pair `(gamma,c)` on the received line
`u + gamma v`: `e_(gamma,c) = u + gamma v - c`. -/
def lineRayError (u v : D → F) (p : F × (D → F)) : D → F :=
  u + p.1 • v - p.2

/-- Exact hypotheses for the residual LineRay family after the common-support
branch has been removed.  Every second component is a codeword in `ker H`,
and the final conjunct states the required transversality separately for every
retained `(slope,codeword)` pair. -/
def LineRayHypotheses (H : (D → F) →ₗ[F] W) (u v : D → F)
    (P : Finset (F × (D → F))) (t : ℕ) : Prop :=
  H v ≠ 0 ∧
    (∀ p ∈ P, H p.2 = 0) ∧
    (∀ p ∈ P, weight (lineRayError u v p) ≤ t) ∧
    KernelDistanceAbove H t ∧
    (∀ p ∈ P,
      ¬ (InSupportImage H (lineRayError u v p) (H u) ∧
        InSupportImage H (lineRayError u v p) (H v)))

/-- The all-pair affine-core conclusion for every LineRay
`(slope,codeword)` pair, with affine dimension computed from all corresponding
error vectors rather than one selected witness per slope. -/
def LineRayConclusion (u v : D → F)
    (P : Finset (F × (D → F))) : Prop :=
  AffineCoreConclusion P (lineRayError u v)

/-- **UNPROVED STATEMENT TARGET (LineRay form).**  A residual LineRay family
with `H v ≠ 0`, kernel distance above `t`, and no common-support witness has
cardinality at most `binom(s+w,s)` (as part of `LineRayConclusion`), while the
full nonuniform charge counts arbitrary same-slope codeword multiplicity. -/
def lineRayTheoremTarget (H : (D → F) →ₗ[F] W) (u v : D → F)
    (P : Finset (F × (D → F))) (t : ℕ) : Prop :=
  LineRayHypotheses H u v P t → LineRayConclusion u v P

/-- The two-level charge and product bound for literal LineRay
`(slope,codeword)` pairs, using their associated errors `u + gamma v - c` at
both levels. -/
def LineRayTwoLevelConclusion (u v : D → F)
    (P R : Finset (F × (D → F))) : Prop :=
  TwoLevelConclusion P R (lineRayError u v)

/-- **UNPROVED STATEMENT TARGET (two-level LineRay form).**  The outer core is
computed from one retained LineRay pair per slope and every inner core from
all retained codewords at that slope.  Arbitrary same-slope multiplicity is
therefore retained in both the nested charge and product cardinality bound. -/
def lineRayTwoLevelTheoremTarget (H : (D → F) →ₗ[F] W)
    (u v : D → F) (P R : Finset (F × (D → F))) (t : ℕ) : Prop :=
  LineRayHypotheses H u v P t →
    OnePerSlope P R →
    LineRayTwoLevelConclusion u v P R

/-- **UNPROVED STATEMENT TARGET (LineRay TL3).**  One retained pair per slope
gives the exact selector-plus-fibers decomposition for the LineRay errors. -/
def lineRayDirectionDecompositionTarget (u v : D → F)
    (P R : Finset (F × (D → F))) : Prop :=
  OnePerSlope P R →
    TwoLevelDirectionDecomposition P R (lineRayError u v)

/-- **UNPROVED STATEMENT TARGET (LineRay TL4).**  With at least two slopes,
the selector direction loses exactly one kernel dimension and the full
kernel-intersection decomposition is exact. -/
def lineRayKernelDecompositionTarget (H : (D → F) →ₗ[F] W)
    (u v : D → F) (P R : Finset (F × (D → F))) (t : ℕ) : Prop :=
  LineRayHypotheses H u v P t →
    OnePerSlope P R →
    1 < (P.image (fun p => p.1)).card →
    TwoLevelKernelDecomposition H P R (lineRayError u v)

end AllLineRayAffineCore
end GrandeFinale
