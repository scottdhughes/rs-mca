import AsymptoticSpine.ProfileEnvelope
import AsymptoticSpine.StaircaseDeep
import AsymptoticSpine.EffectiveClosure
import AsymptoticSpine.AddBack

namespace AsymptoticSpine

/-!
# Regression locks for the asymptotic proof spine

This module restates the principal public theorem interface and one executable
fixture from each of four established proof modules.  It adds no mathematical
hypothesis and no new source-paper claim.  Its purpose is deliberately
mechanical: package upgrades must continue to elaborate the exact interfaces
below and replay the finite certificates.
-/

/-- Lock the complete conditional profile-envelope frontier interface. -/
theorem profileEnvelope_regression_lock
    (bad : Nat → Nat)
    (target lower n first aMinus aPlus : Nat)
    (nonprimitive primitiveRay primitivePaid
      nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget : Nat)
    (hanti : ∀ a b, a ≤ b → bad b ≤ bad a)
    (hfirst : IsFirstSafe bad target lower n first)
    (hminus : lower ≤ aMinus) (hplus : lower ≤ aPlus)
    (hplusn : aPlus ≤ n)
    (hlower : target < bad aMinus)
    (hcompiler :
      ProfileCompilerInputs (bad aPlus) nonprimitive primitiveRay primitivePaid
        nonprimitiveBudget sidonBudget profileEnvelope
        compilerLoss identityLoss identityBudget target) :
    (aMinus < first ∧ first ≤ aPlus) ∧
      (n - aPlus ≤ n - first ∧ n - first < n - aMinus) :=
  profile_frontier_bracket bad target lower n first aMinus aPlus
    nonprimitive primitiveRay primitivePaid nonprimitiveBudget sidonBudget
    profileEnvelope compilerLoss identityLoss identityBudget hanti hfirst
    hminus hplus hplusn hlower hcompiler

/-- Lock the general deep-regime incidence-ledger compiler. -/
theorem staircaseDeep_regression_lock {Pair : Type}
    (M : FinitePairEnumeration Pair)
    (badCount : Pair → Nat) (n a d : Nat)
    (ha : a ≤ n) (hdeep : 3 * (n - a) ≤ d - 1)
    (incidenceLedger : ∀ p ∈ M.pairs, a ≤ n → 3 * (n - a) ≤ d - 1 →
      DeepPairCertificate (n - a) (badCount p)) :
    badSlopeNumerator M badCount ≤ n - a + 1 :=
  deep_regime_upper M badCount n a d ha hdeep incidenceLedger

/-- Lock the general prefix/residual effective-closure bridge. -/
theorem effectiveClosure_regression_lock {Support Slope Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (imageSize effectiveSize average loss : Nat)
    (haverage : b.fullSlice.length ≤ imageSize * average)
    (himage : imageSize ≤ effectiveSize)
    (hloss : effectiveSize ≤ loss) :
    DirectRC c.slopes.length loss average :=
  prefixResidualClosure_to_directRC b z c hchart imageSize effectiveSize
    average loss haverage himage hloss

/-- Lock the general first-match add-back sufficiency theorem. -/
theorem addBack_regression_lock
    (S : List Nat) (fam : List Leaf) (Y C C' Mtot : Nat)
    (h : ProfileNonDegen S fam Y C C' Mtot) :
    globalMax S fam * Y ≤ C * C' * Mtot :=
  addback_sufficiency S fam Y C C' Mtot h

/-! The following locks replay one exact fixture from each module. -/

/-- Re-enumerate the exact GF(11^2) profile census. -/
theorem profileEnvelope_fixture_lock :
    gf11SquareSupports.Nodup ∧
    gf11SquareSupports.length = 210 ∧
    gf11SquareFibres =
      [20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19] ∧
    listMax gf11SquareFibres = 20 ∧
    ceilDiv 210 11 = 20 :=
  gf11_square_profile_certificate

/-- Replay the exact dense-root staircase fixture. -/
theorem staircaseDeep_fixture_lock : 3 = 2 + 1 ∧ 3 ≤ 2 + 1 :=
  dense_root_toy_exact

/-- Replay the exact direct residual-closure fixture. -/
theorem effectiveClosure_fixture_lock : DirectRC 2 4 2 :=
  directRC_toy

/-- Replay the exact nondegenerate add-back fixture through the general theorem. -/
theorem addBack_fixture_lock :
    globalMax ndS ndFam * 2 ≤ 1 * 1 * 4 :=
  addback_example_via_theorem

#print axioms profileEnvelope_regression_lock
#print axioms staircaseDeep_regression_lock
#print axioms effectiveClosure_regression_lock
#print axioms addBack_regression_lock
#print axioms profileEnvelope_fixture_lock
#print axioms staircaseDeep_fixture_lock
#print axioms effectiveClosure_fixture_lock
#print axioms addBack_fixture_lock

end AsymptoticSpine
