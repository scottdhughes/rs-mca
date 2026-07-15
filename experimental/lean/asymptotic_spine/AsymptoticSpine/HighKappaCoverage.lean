import AsymptoticSpine.EffectiveClosure

namespace AsymptoticSpine

/-!
# Kernel-dimension-independent shallow-prefix coverage

This module makes explicit the finite routing statement extracted in
`experimental/notes/thresholds/a4_covers_high_kappa.md`.

A residual balanced-core chart carries a kernel-dimension label, but the
shallow-prefix closure route uses only ambient-slice data: a reindexed prefix
fiber, residual inclusion, the `(SE2)` support injection, and a bound on the
effective image size. The exact `DirectRC` and `A6RayCondition` conclusions
therefore hold uniformly for every kernel-dimension label.

The module does not prove that a family is asymptotically shallow, does not
turn a finite power bound into an `exp(o(n))` statement, and does not prove the
deep-prefix `(MI)`/`(MA)` character-sum payment.
-/

/-- Exact ambient-slice inputs for the shallow-prefix closure route.

The source bound `A_eff ≤ |B|^w` is represented by
`effectiveSize ≤ baseSize ^ prefixDepth`. All fields belong to the ambient
full slice, not to an individual residual chart. -/
structure ShallowPrefixClosureBounds (fullMass : Nat) where
  baseSize : Nat
  prefixDepth : Nat
  imageSize : Nat
  effectiveSize : Nat
  average : Nat
  mass_le_image_average : fullMass ≤ imageSize * average
  image_le_effective : imageSize ≤ effectiveSize
  effective_le_prefixPower : effectiveSize ≤ baseSize ^ prefixDepth

/-- A direct `(RC)` proposition carrying a residual kernel-dimension label.
The definition deliberately erases the label: this records that `κ` is routing
metadata, not an input to the closure inequality. -/
def KernelIndependentDirectRC (_kernelDim bad loss average : Nat) : Prop :=
  DirectRC bad loss average

/-- The labelled proposition is definitionally the ordinary direct `(RC)`
bound, for every kernel dimension. -/
theorem kernelIndependentDirectRC_iff
    (kernelDim bad loss average : Nat) :
    KernelIndependentDirectRC kernelDim bad loss average ↔
      DirectRC bad loss average :=
  Iff.rfl

/--
**Finite high-`κ` coverage.** A residual chart inside the reindexed ambient
prefix fiber satisfies the shallow direct `(RC)` bound. The residual kernel
dimension occurs only as a label in the conclusion; no inequality or
cardinality hypothesis depends on it.
-/
theorem balancedCoreShallowClosure_to_directRC
    {Support Slope Eff Raw : Type} [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (bounds : ShallowPrefixClosureBounds b.fullSlice.length)
    (kernelDim : Nat) :
    KernelIndependentDirectRC kernelDim c.slopes.length
      (bounds.baseSize ^ bounds.prefixDepth) bounds.average := by
  unfold KernelIndependentDirectRC
  exact prefixResidualClosure_to_directRC b z c hchart bounds.imageSize
    bounds.effectiveSize bounds.average
    (bounds.baseSize ^ bounds.prefixDepth)
    bounds.mass_le_image_average bounds.image_le_effective
    bounds.effective_le_prefixPower

/-- The same ambient shallow-prefix certificate pays every possible residual
kernel dimension, including dimensions growing with external parameters. -/
theorem balancedCoreShallowClosure_all_kernelDimensions
    {Support Slope Eff Raw : Type} [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (bounds : ShallowPrefixClosureBounds b.fullSlice.length) :
    ∀ kernelDim : Nat,
      KernelIndependentDirectRC kernelDim c.slopes.length
        (bounds.baseSize ^ bounds.prefixDepth) bounds.average := by
  intro kernelDim
  exact balancedCoreShallowClosure_to_directRC b z c hchart bounds kernelDim

/-- The `κ`-free shallow closure reaches admissibility condition `(A6)`
through its direct `(RC)` disjunct. -/
theorem balancedCoreShallowClosure_to_A6
    {Support Slope Eff Raw : Type} [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (bounds : ShallowPrefixClosureBounds b.fullSlice.length)
    (kernelDim : Nat) (directProfileBound : Prop) :
    A6RayCondition
      (KernelIndependentDirectRC kernelDim c.slopes.length
        (bounds.baseSize ^ bounds.prefixDepth) bounds.average)
      directProfileBound :=
  Or.inl (balancedCoreShallowClosure_to_directRC b z c hchart bounds kernelDim)

/-- Uniform `(A6)` routing for all kernel-dimension labels. -/
theorem balancedCoreShallowClosure_to_A6_all_kernelDimensions
    {Support Slope Eff Raw : Type} [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (bounds : ShallowPrefixClosureBounds b.fullSlice.length)
    (directProfileBound : Prop) :
    ∀ kernelDim : Nat,
      A6RayCondition
        (KernelIndependentDirectRC kernelDim c.slopes.length
          (bounds.baseSize ^ bounds.prefixDepth) bounds.average)
        directProfileBound := by
  intro kernelDim
  exact balancedCoreShallowClosure_to_A6 b z c hchart bounds kernelDim
    directProfileBound

/-! ## Exact finite smoke test -/

def highKappaToySE2 : SE2Certificate Nat Nat where
  supports := [1, 3]
  slopes := [7, 9]
  supportOf := fun γ => if γ = 7 then 1 else 3
  supports_nodup := by decide
  slopes_nodup := by decide
  chosen_sublist := by decide

def highKappaToyBounds :
    ShallowPrefixClosureBounds affineToyBridge.fullSlice.length where
  baseSize := 2
  prefixDepth := 2
  imageSize := 3
  effectiveSize := 4
  average := 2
  mass_le_image_average := by decide
  image_le_effective := by decide
  effective_le_prefixPower := by decide

/-- One ambient certificate pays the toy chart even with an arbitrarily large
printed kernel-dimension label. -/
theorem highKappaToy_largeLabel :
    KernelIndependentDirectRC 1000000 highKappaToySE2.slopes.length 4 2 := by
  exact balancedCoreShallowClosure_to_directRC affineToyBridge 1 highKappaToySE2
    (by decide) highKappaToyBounds 1000000

#print axioms kernelIndependentDirectRC_iff
#print axioms balancedCoreShallowClosure_to_directRC
#print axioms balancedCoreShallowClosure_all_kernelDimensions
#print axioms balancedCoreShallowClosure_to_A6
#print axioms balancedCoreShallowClosure_to_A6_all_kernelDimensions
#print axioms highKappaToy_largeLabel

end AsymptoticSpine
