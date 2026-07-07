import L1Threshold.CollapseEdgeCertificate

namespace L1Threshold

/-!
# W3 collapse-edge graph-mechanism certificate

This module factors the W3 collapse-edge finite certificate through a smaller
graph mechanism:

* every non-survivor alternate coset is matching-only, so it has no component
  of size at least three;
* the survivor coset has exactly the triangle `[17,36,130]` as its only large
  component;
* therefore the alternate contribution is exactly `1`.

The second half of the file repeats the matching/triangle checks directly from
the stored `always / never / atShift` edge rules by recomputing active edges at
the certified shift. This is the finite edge-rule mechanism behind the stored
component certificate.

This is still a finite graph certificate over the stored cases. It does not
reconstruct the underlying `GF(137)` edge arithmetic and does not prove a
symbolic W3 lemma.
-/

namespace CollapseEdgeGraphMechanism

set_option maxRecDepth 1000000
set_option maxHeartbeats 2000000

open CollapseEdgeCertificate

def survivorCosetW : Nat := 37

def survivorTriangle : List Nat := [17, 36, 130]

def endpointCount (x : Nat) (edges : List (Nat × Nat)) : Nat :=
  edges.foldl
    (fun acc e => if e.1 == x || e.2 == x then acc + 1 else acc)
    0

def edgePresent (a b : Nat) (edges : List (Nat × Nat)) : Bool :=
  edges.any (fun e => (e.1 == a && e.2 == b) || (e.1 == b && e.2 == a))

def cosetActiveEdgesFromRules (shift : Nat) (coset : CosetCert) : List (Nat × Nat) :=
  activeEdgesFromRules shift coset.edgeRules

def matchingEdgesOn (points : List Nat) (edges : List (Nat × Nat)) : Bool :=
  points.all (fun p => decide (endpointCount p edges <= 1))

def inSurvivorTriangle (x : Nat) : Bool :=
  contains survivorTriangle x

def edgeAvoidsTriangleBoundary (e : Nat × Nat) : Bool :=
  let aIn := inSurvivorTriangle e.1
  let bIn := inSurvivorTriangle e.2
  (aIn && bIn) || (!aIn && !bIn)

def outsideTriangleEdges (edges : List (Nat × Nat)) : List (Nat × Nat) :=
  edges.filter (fun e => (!inSurvivorTriangle e.1) && (!inSurvivorTriangle e.2))

def triangleEdgesActive (edges : List (Nat × Nat)) : Bool :=
  edgePresent 17 36 edges && edgePresent 17 130 edges && edgePresent 36 130 edges

def componentSmall (component : List Nat) : Bool :=
  decide (component.length <= 2)

def cosetMatchingOnly (coset : CosetCert) : Bool :=
  coset.components.all componentSmall

def survivorCoset (coset : CosetCert) : Bool :=
  coset.cosetW == survivorCosetW

def cosetRuleMatchingOnly (shift : Nat) (coset : CosetCert) : Bool :=
  matchingEdgesOn coset.points (cosetActiveEdgesFromRules shift coset)

def nonSurvivorRuleCosetsMatchingOnly (caseCert : CaseCert) : Bool :=
  caseCert.alternateCosets.all
    (fun coset => survivorCoset coset || cosetRuleMatchingOnly caseCert.shift coset)

def survivorRuleTriangleOnly (shift : Nat) (coset : CosetCert) : Bool :=
  let active := cosetActiveEdgesFromRules shift coset
  survivorCoset coset
    && triangleEdgesActive active
    && active.all edgeAvoidsTriangleBoundary
    && matchingEdgesOn
      (coset.points.filter (fun p => !inSurvivorTriangle p))
      (outsideTriangleEdges active)

def caseHasUniqueRuleSurvivorTriangle (caseCert : CaseCert) : Bool :=
  ((caseCert.alternateCosets.filter survivorCoset).all
      (fun coset => survivorRuleTriangleOnly caseCert.shift coset))
    && (caseCert.alternateCosets.filter survivorCoset).length == 1

def nonSurvivorCosetsMatchingOnly (caseCert : CaseCert) : Bool :=
  caseCert.alternateCosets.all
    (fun coset => survivorCoset coset || cosetMatchingOnly coset)

def cosetLargeComponents (coset : CosetCert) : List (List Nat) :=
  largeComponents coset.components

def survivorTriangleOnly (coset : CosetCert) : Bool :=
  survivorCoset coset && (cosetLargeComponents coset == [survivorTriangle])

def caseHasUniqueSurvivorTriangle (caseCert : CaseCert) : Bool :=
  ((caseCert.alternateCosets.filter survivorCoset).all survivorTriangleOnly)
    && (caseCert.alternateCosets.filter survivorCoset).length == 1

def graphMechanismOK (caseCert : CaseCert) : Bool :=
  (caseCert.headMissing == 2)
    && (caseCert.headStray == 1)
    && nonSurvivorCosetsMatchingOnly caseCert
    && caseHasUniqueSurvivorTriangle caseCert
    && (alternateContribution caseCert == 1)

def edgeRuleMechanismOK (caseCert : CaseCert) : Bool :=
  (caseCert.headMissing == 2)
    && (caseCert.headStray == 1)
    && checkCase caseCert
    && nonSurvivorRuleCosetsMatchingOnly caseCert
    && caseHasUniqueRuleSurvivorTriangle caseCert
    && (alternateContribution caseCert == 1)

def allGraphMechanismsOK : Bool :=
  allCases.all graphMechanismOK

def allEdgeRuleMechanismsOK : Bool :=
  allCases.all edgeRuleMechanismOK

theorem allNonSurvivorAlternatesMatchingOnly :
    allCases.all nonSurvivorCosetsMatchingOnly = true := by
  decide

theorem allCasesHaveUniqueSurvivorTriangle :
    allCases.all caseHasUniqueSurvivorTriangle = true := by
  decide

theorem allNonSurvivorRuleAlternatesMatchingOnly :
    allCases.all nonSurvivorRuleCosetsMatchingOnly = true := by
  decide

theorem allCasesHaveRuleSurvivorTriangle :
    allCases.all caseHasUniqueRuleSurvivorTriangle = true := by
  decide

theorem allGraphMechanismsCertified :
    allGraphMechanismsOK = true := by
  decide

theorem allEdgeRuleMechanismsCertified :
    allEdgeRuleMechanismsOK = true := by
  decide

theorem graphMechanismAlternateContributionsExact :
    allCases.map alternateContribution = [1, 1, 1, 1, 1, 1] := by
  decide

#print axioms allNonSurvivorAlternatesMatchingOnly
#print axioms allCasesHaveUniqueSurvivorTriangle
#print axioms allNonSurvivorRuleAlternatesMatchingOnly
#print axioms allCasesHaveRuleSurvivorTriangle
#print axioms allGraphMechanismsCertified
#print axioms allEdgeRuleMechanismsCertified
#print axioms graphMechanismAlternateContributionsExact

end CollapseEdgeGraphMechanism
end L1Threshold
