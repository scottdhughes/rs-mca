import L1Threshold.CollapseEdgeCompactPacket

namespace L1Threshold

/-!
# W3 collapse-edge affine/rule/mechanism bridge

This module names the finite bridge certified by the compact W3 collapse-edge
packet:

1. the compact dot-product rows certify the affine intercept/slope data;
2. the compact modular arithmetic rows certify the stored edge-rule kind
   (`always`, `never`, or `atShift`) from `intercept + t * slope = 0`;
3. the origin summary certifies that the stored edge-rule packet has zero
   mismatches and the expected six-case/two-family shape;
4. the rule-derived graph mechanism recomputes active edges from the stored
   `atShift` rules and proves the matching/triangle collapse pattern; and
5. the finite structural wrapper gives alternate contribution `<= 1`, in fact
   exactly `1`, for all six dangerous `(missing,stray)=(2,1)` cases.

This is still a finite certificate chain over the stored W3 packet. It is not a
symbolic W3 lemma and does not reconstruct the W3 basis polynomials.
-/

namespace CollapseEdgeAffineRuleBridge

theorem affineOriginRowsCertified :
    CollapseEdgeOriginDot.allRowsOK = true
      ∧ CollapseEdgeOriginArithmetic.allRowsOK = true
      ∧ CollapseEdgeOriginDot.edgeRows.length = 6528
      ∧ CollapseEdgeOriginArithmetic.edgeRows.length = 6528 := by
  exact
    And.intro CollapseEdgeOriginDot.edgeOriginDotAllRowsOK
      (And.intro CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK
        (And.intro CollapseEdgeOriginDot.edgeOriginDotRowCount
          CollapseEdgeOriginArithmetic.edgeOriginArithmeticRowCount))

theorem storedRulePacketCertified :
    CollapseEdgeOriginSummary.allCasesOK = true
      ∧ CollapseEdgeOriginSummary.edgeRulesAudited = 6528
      ∧ CollapseEdgeOriginSummary.mismatchCount = 0
      ∧ CollapseEdgeOriginSummary.allCases.map
          (fun c => (c.family, c.quotientA, c.quotientB, c.shift)) =
        [(CollapseEdgeOriginSummary.Family.v7, 83, 96, 67),
         (CollapseEdgeOriginSummary.Family.v7, 83, 96, 103),
         (CollapseEdgeOriginSummary.Family.v7, 83, 96, 111),
         (CollapseEdgeOriginSummary.Family.v11, 105, 38, 17),
         (CollapseEdgeOriginSummary.Family.v11, 105, 38, 20),
         (CollapseEdgeOriginSummary.Family.v11, 105, 38, 121)] := by
  exact
    And.intro CollapseEdgeOriginSummary.originSummaryAllCasesOK
      (And.intro CollapseEdgeOriginSummary.originSummaryEdgeRulesAudited
        (And.intro CollapseEdgeOriginSummary.originSummaryNoMismatches
          CollapseEdgeOriginSummary.originSummaryTwoFamilies))

theorem ruleMechanismCertified :
    CollapseEdgeGraphMechanism.allEdgeRuleMechanismsOK = true
      ∧ CollapseEdgeCertificate.allCases.all
          CollapseEdgeGraphMechanism.nonSurvivorRuleCosetsMatchingOnly = true
      ∧ CollapseEdgeCertificate.allCases.all
          CollapseEdgeGraphMechanism.caseHasUniqueRuleSurvivorTriangle = true := by
  exact
    And.intro CollapseEdgeGraphMechanism.allEdgeRuleMechanismsCertified
      (And.intro CollapseEdgeGraphMechanism.allNonSurvivorRuleAlternatesMatchingOnly
        CollapseEdgeGraphMechanism.allCasesHaveRuleSurvivorTriangle)

theorem dangerousContributionCertified :
    CollapseEdgeStructuralLemma.allDangerousCasesCollapse = true
      ∧ CollapseEdgeStructuralLemma.allDangerousCasesHaveUniqueSurvivor = true
      ∧ CollapseEdgeCertificate.allCases.map CollapseEdgeCertificate.alternateContribution =
          [1, 1, 1, 1, 1, 1] := by
  exact
    And.intro CollapseEdgeStructuralLemma.dangerousPatternForcesAlternateCollapse
      (And.intro CollapseEdgeStructuralLemma.dangerousPatternForcesUniqueCoset37Survivor
        CollapseEdgeCertificate.collapseEdgeAllAlternateContributionsExact)

theorem affineRulesToAlternateCollapseBridge :
    CollapseEdgeOriginDot.allRowsOK = true
      ∧ CollapseEdgeOriginArithmetic.allRowsOK = true
      ∧ CollapseEdgeOriginSummary.mismatchCount = 0
      ∧ CollapseEdgeOriginSummary.edgeRulesAudited = 6528
      ∧ CollapseEdgeGraphMechanism.allEdgeRuleMechanismsOK = true
      ∧ CollapseEdgeStructuralLemma.allDangerousCasesCollapse = true
      ∧ CollapseEdgeCertificate.allCases.map CollapseEdgeCertificate.alternateContribution =
          [1, 1, 1, 1, 1, 1] := by
  exact
    And.intro CollapseEdgeOriginDot.edgeOriginDotAllRowsOK
      (And.intro CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK
        (And.intro CollapseEdgeOriginSummary.originSummaryNoMismatches
          (And.intro CollapseEdgeOriginSummary.originSummaryEdgeRulesAudited
            (And.intro CollapseEdgeGraphMechanism.allEdgeRuleMechanismsCertified
              (And.intro CollapseEdgeStructuralLemma.dangerousPatternForcesAlternateCollapse
                CollapseEdgeCertificate.collapseEdgeAllAlternateContributionsExact)))))

#print axioms affineOriginRowsCertified
#print axioms storedRulePacketCertified
#print axioms ruleMechanismCertified
#print axioms dangerousContributionCertified
#print axioms affineRulesToAlternateCollapseBridge

end CollapseEdgeAffineRuleBridge
end L1Threshold
