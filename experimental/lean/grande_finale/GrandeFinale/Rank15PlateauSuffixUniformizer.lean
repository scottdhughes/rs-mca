import Mathlib

/-!
# Rank-15 plateau-suffix uniformizer: statement targets

This module contains only **UNPROVED STATEMENT TARGETS** for
`experimental/notes/l2/rank15_plateau_suffix_uniformizer.md`. It records the
literal universal set, the exact affine two-flat, the polynomial
locator-saturation normal form, the proper-section cap `q = 15`, and the
178-state conclusion without claiming a Lean proof.

The manuscript proof consumes the pending PR #746 `chi >= 8` graph certificate
and its ten `chi = 8` skeletons. That proof dependency is explicit in the note;
it is not redefined or claimed as a theorem here. The target is fixed at the
original `K = 1,048,576` (effective recurrence `c = 0`). It gives genuinely
new coverage on that slice and regression coverage on 384 already accepted
lower-degree rows because `F_p[X]_{<K-c}` is contained in `F_p[X]_{<K}`; it
does not replace the separate `c = 130,...,152` Grand Slam proof.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace Rank15PlateauSuffixUniformizer

set_option autoImplicit false

universe u

variable {F : Type u} [Field F] [DecidableEq F]

/-! ## Deployed constants -/

def evaluationCount : Nat := 2_097_152

def codeDimension : Nat := 1_048_576

def agreementThreshold : Nat := 1_116_047

def properSectionCap : Nat := 15

def plateauSuffixLower : Nat := 1_043_771

def plateauSuffixUpper : Nat := 1_043_948

def provedListCeiling : Nat := 217

def effectiveRecurrenceC : Nat := 0

/-! ## Literal affine-flat data -/

/-- The polynomial represented by the affine parameter point `(s,t)`. -/
def affinePolynomial (P0 V1 V2 : Polynomial F) (p : F × F) : Polynomial F :=
  P0 + Polynomial.C p.1 * V1 + Polynomial.C p.2 * V2

/-- Agreement coordinates of one literal affine parameter point. -/
def agreementCoordinates (H : Finset F) (U : F -> F)
    (P0 V1 V2 : Polynomial F) (p : F × F) : Finset F :=
  H.filter fun x => (affinePolynomial P0 V1 V2 p).eval x = U x

/-- The actual universal agreement set of the entire affine two-flat. -/
def universalSet (H : Finset F) (U : F -> F)
    (P0 V1 V2 : Polynomial F) : Finset F :=
  H.filter fun x =>
    P0.eval x = U x ∧ V1.eval x = 0 ∧ V2.eval x = 0

/-- The literal coordinate section of the supplied listed parameter set. -/
def coordinateSection (S : Finset (F × F)) (U : F -> F)
    (P0 V1 V2 : Polynomial F) (x : F) : Finset (F × F) :=
  S.filter fun p => (affinePolynomial P0 V1 V2 p).eval x = U x

/-- The two polynomial directions span an exact two-dimensional direction
space. -/
def IndependentDirections (V1 V2 : Polynomial F) : Prop :=
  ∀ alpha beta : F,
    Polynomial.C alpha * V1 + Polynomial.C beta * V2 = 0 →
      alpha = 0 ∧ beta = 0

/-- Bezout form of `gcd(A,B)=1`. -/
def CoprimePencil (A B : Polynomial F) : Prop :=
  ∃ R S : Polynomial F, R * A + S * B = 1

/-- Locator of a finite set of field points. -/
def locator (Z : Finset F) : Polynomial F :=
  Z.prod fun x => Polynomial.X - Polynomial.C x

/-- The imported rank-15 locator-saturation normal-form layer. -/
def LocatorSaturationNormalForm (Z : Finset F)
    (V1 V2 : Polynomial F) : Prop :=
  ∃ G A B : Polynomial F,
    G.Monic ∧
      CoprimePencil A B ∧
      IndependentDirections A B ∧
      V1 = locator Z * G * A ∧
      V2 = locator Z * G * B ∧
      max A.natDegree B.natDegree + G.natDegree <=
        codeDimension - 1 - Z.card

/-- Exact source hypotheses for the 178-state theorem target. The proper
section cap is imposed on the actual coordinate sections, not on a shadow
profile. -/
def PlateauSuffixHypotheses (H : Finset F) (U : F -> F)
    (P0 V1 V2 : Polynomial F) (S : Finset (F × F)) : Prop :=
  let Z := universalSet H U P0 V1 V2
  H.card = evaluationCount ∧
    P0.natDegree < codeDimension ∧
    V1.natDegree < codeDimension ∧
    V2.natDegree < codeDimension ∧
    IndependentDirections V1 V2 ∧
    plateauSuffixLower <= Z.card ∧
    Z.card <= plateauSuffixUpper ∧
    LocatorSaturationNormalForm Z V1 V2 ∧
    (∀ p ∈ S,
      agreementThreshold <= (agreementCoordinates H U P0 V1 V2 p).card) ∧
    ∀ x ∈ H, x ∉ Z →
      (coordinateSection S U P0 V1 V2 x).card <= properSectionCap

/-- **UNPROVED STATEMENT TARGET.** Every finite listed subset of an exact
affine two-flat satisfying the actual-universal-set normal form and `q = 15`
proper-section cap has at most 217 points on the 178-state suffix. -/
def theoremTarget (H : Finset F) (U : F -> F)
    (P0 V1 V2 : Polynomial F) (S : Finset (F × F)) : Prop :=
  PlateauSuffixHypotheses H U P0 V1 V2 S →
    S.card <= provedListCeiling

/-! ## Exact arithmetic consequences -/

/-- **UNPROVED STATEMENT TARGET.** The exact dimension-15 recurrence endpoint
and remaining target gap produced by the 178-state local ceiling. -/
def recurrenceEndpointTarget : Prop :=
  284_377_931_860_724_492 - 283_039_300_733_528_044 =
      1_338_631_127_196_448 ∧
    283_039_300_733_528_044 - 274_854_110_496_187_592 =
      8_185_190_237_340_452

/-- Exact relaxed margins in the ordered cases `t = 210,...,218`. -/
def leftBoundaryMargins : List Int :=
  [-8_054, -8_054, -3_249, -3_249, -1_705, -6_510, -6_510,
    -1_705, 1_403]

/-- **UNPROVED STATEMENT TARGET.** The exact left boundary remains outside
the theorem: the ordered `t = 210,...,217` margins are negative and only
`t = 218` has positive relaxed margin, namely 1,403. -/
def leftBoundaryTarget : Prop :=
  leftBoundaryMargins =
      [-8_054, -8_054, -3_249, -3_249, -1_705, -6_510, -6_510,
        -1_705, 1_403] ∧
    (∀ i : Nat, i < 8 →
      ∃ x : Int, leftBoundaryMargins[i]? = some x ∧ x < 0) ∧
    leftBoundaryMargins[8]? = some 1_403

end Rank15PlateauSuffixUniformizer
end GrandeFinale
