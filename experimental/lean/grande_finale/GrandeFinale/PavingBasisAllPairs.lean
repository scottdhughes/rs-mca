import GrandeFinale.DirectionDistanceAllPairs

/-!
# All-pair paving-basis multiplicity compiler

This module contains only **UNPROVED STATEMENT TARGETS**.  It records the
augmented basis census, local paving charge, one-owner condition, and the
direction/deep-hole all-pair conclusions.  Definitions typechecking here do
not constitute a Lean proof of the mathematical note.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace PavingBasisAllPairs

open DirectionDistanceAllPairs

set_option autoImplicit false

universe u v w

variable {D : Type u} {F : Type v} {W : Type w}
variable {kappa : Nat}
variable [Fintype D] [DecidableEq D]
variable [Field F] [DecidableEq F]
variable [AddCommGroup W] [Module F W]

abbrev Pair (D : Type u) (F : Type v) := SlopeErrorPair D F

/-- Coordinates of `[b0 b1 G]`: two hosted lifts and `kappa` kernel columns. -/
abbrev AugmentedCoordinate (kappa : Nat) := Fin 2 ⊕ Fin kappa

def augmentedRow (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (x : D) : AugmentedCoordinate kappa -> F :=
  fun coordinate =>
    match coordinate with
    | Sum.inl index => if index = (0 : Fin 2) then b0 x else b1 x
    | Sum.inr index => g index x

def zeroSet (z : D -> F) : Finset D :=
  Finset.univ.filter fun x => z x = 0

def rowSpan (A : D -> AugmentedCoordinate kappa -> F) (I : Finset D) :
    Submodule F (AugmentedCoordinate kappa -> F) :=
  Submodule.span F (A '' (I : Set D))

def rowRank (A : D -> AugmentedCoordinate kappa -> F) (I : Finset D) : Nat :=
  Module.finrank F (rowSpan A I)

def basisSubsets (A : D -> AugmentedCoordinate kappa -> F) :
    Finset (Finset D) :=
  Finset.univ.filter fun I : Finset D =>
    I.card = kappa + 1 ∧ rowRank A I = kappa + 1

def basisCensus (A : D -> AugmentedCoordinate kappa -> F) : Nat :=
  (basisSubsets A).card

def localBasisCensus (A : D -> AugmentedCoordinate kappa -> F)
    (z : D -> F) : Nat :=
  ((basisSubsets A).filter fun I => I ⊆ zeroSet z).card

def ceilDiv (numerator denominator : Nat) : Nat :=
  (numerator + denominator - 1) / denominator

/-- Natural subtraction is the positive part `(d-w)_+`. -/
def directionCharge (N kappa d weight : Nat) : Nat :=
  ceilDiv ((d - weight) * Nat.choose (N - weight) kappa) (kappa + 1)

def pavingCharge (N kappa d weight : Nat) : Nat :=
  max (Nat.choose (N - weight - 1) kappa)
    (directionCharge N kappa d weight)

def HostedLifts (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) : Prop :=
  H b0 = y0 ∧ H b1 = y1

def DirectionDistance (H : (D -> F) →ₗ[F] W) (y1 : W) (d : Nat) : Prop :=
  ∃ v : D -> F, H v = y1 ∧ weight v = d ∧
    ∀ z : D -> F, H z = y1 -> d ≤ weight z

def KernelBasis (H : (D -> F) →ₗ[F] W)
    (g : Fin kappa -> D -> F) : Prop :=
  LinearIndependent F g ∧
    ∀ z : D -> F, H z = 0 ↔ z ∈ Submodule.span F (Set.range g)

def PavingBasisHypotheses (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  Fintype.card D = R + kappa ∧
    0 < kappa ∧ t < R ∧ d ≤ R ∧
    BasicPairHypotheses H y0 y1 P t ∧
    HostedLifts H y0 y1 b0 b1 ∧
    DirectionDistance H y1 d ∧
    PairTransverse H y0 y1 P ∧
    KernelDistanceAtLeast H (R + 1) ∧
    KernelBasis H g

def EverySmallRowSetIndependent
    (A : D -> AugmentedCoordinate kappa -> F) : Prop :=
  ∀ I : Finset D, I.card ≤ kappa -> rowRank A I = I.card

def LocalRankConclusion (A : D -> AugmentedCoordinate kappa -> F)
    (P : Finset (Pair D F)) : Prop :=
  EverySmallRowSetIndependent A ∧
    ∀ p ∈ P, rowRank A (zeroSet p.2) = kappa + 1

def LocalChargeConclusion (A : D -> AugmentedCoordinate kappa -> F)
    (P : Finset (Pair D F)) (d : Nat) : Prop :=
  let N := Fintype.card D
  ∀ p ∈ P,
    pavingCharge N kappa d (weight p.2) ≤ localBasisCensus A p.2

def OnePairPerBasis (A : D -> AugmentedCoordinate kappa -> F)
    (P : Finset (Pair D F)) : Prop :=
  ∀ I ∈ basisSubsets A, ∀ p ∈ P, I ⊆ zeroSet p.2 ->
    ∀ q ∈ P, I ⊆ zeroSet q.2 -> p = q

def AllPairPavingConclusion (A : D -> AugmentedCoordinate kappa -> F)
    (P : Finset (Pair D F)) (t d : Nat) : Prop :=
  let N := Fintype.card D
  let beta := basisCensus A
  let uniformCharge := pavingCharge N kappa d t
  (∑ p ∈ P, pavingCharge N kappa d (weight p.2)) ≤ beta ∧
    beta ≤ Nat.choose N (kappa + 1) ∧
    P.card * uniformCharge ≤ beta ∧
    P.card ≤ beta / uniformCharge ∧
    P.card ≤ Nat.choose N (kappa + 1) / uniformCharge ∧
    P.card ≤ Nat.choose N (kappa + 1) /
      Nat.choose (N - t - 1) kappa

def DeepHoleConclusion (A : D -> AugmentedCoordinate kappa -> F)
    (P : Finset (Pair D F)) (t : Nat) : Prop :=
  let N := Fintype.card D
  let beta := basisCensus A
  (∑ p ∈ P, Nat.choose (N - weight p.2) (kappa + 1)) ≤ beta ∧
    beta ≤ Nat.choose N (kappa + 1) ∧
    P.card * Nat.choose (N - t) (kappa + 1) ≤ beta ∧
    P.card ≤ beta / Nat.choose (N - t) (kappa + 1) ∧
    P.card ≤ Nat.choose N (kappa + 1) /
      Nat.choose (N - t) (kappa + 1)

/-! ## Source-to-local targets -/

/-- **UNPROVED STATEMENT TARGET (transversality forces local rank).** -/
def localRankFromTransversalityTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  PavingBasisHypotheses H y0 y1 b0 b1 g P R t d ->
    LocalRankConclusion (augmentedRow b0 b1 g) P

/-- **UNPROVED STATEMENT TARGET (paving and direction local charges).** -/
def localPavingChargeTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  PavingBasisHypotheses H y0 y1 b0 b1 g P R t d ->
    LocalChargeConclusion (augmentedRow b0 b1 g) P d

/-- **UNPROVED STATEMENT TARGET (one normalized pair-owner per basis).** -/
def onePairPerBasisTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  PavingBasisHypotheses H y0 y1 b0 b1 g P R t d ->
    OnePairPerBasis (augmentedRow b0 b1 g) P

/-! ## Compiler targets -/

/-- **UNPROVED STATEMENT TARGET (PB1--PB3, complete pair set).** -/
def allPairPavingBasisTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  PavingBasisHypotheses H y0 y1 b0 b1 g P R t d ->
    AllPairPavingConclusion (augmentedRow b0 b1 g) P t d

/-- **UNPROVED STATEMENT TARGET (PB4--PB5, `d=R`).** -/
def deepHoleAllPairPavingBasisTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin kappa -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  PavingBasisHypotheses H y0 y1 b0 b1 g P R t d ->
    d = R -> DeepHoleConclusion (augmentedRow b0 b1 g) P t

/-- **UNPROVED STATEMENT TARGET (correct uniform-charge monotonicity).** -/
def pavingChargeMonotonicityTarget (N kappa d t : Nat) : Prop :=
  ∀ weight ≤ t,
    pavingCharge N kappa d t ≤ pavingCharge N kappa d weight

/-- **UNPROVED STATEMENT TARGET (choice invariance of the basis census).** -/
def basisCensusChoiceInvariantTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 b0' b1' : D -> F)
    (g g' : Fin kappa -> D -> F) : Prop :=
  HostedLifts H y0 y1 b0 b1 -> KernelBasis H g ->
    HostedLifts H y0 y1 b0' b1' -> KernelBasis H g' ->
    basisCensus (augmentedRow b0 b1 g) =
      basisCensus (augmentedRow b0' b1' g')

/-- **UNPROVED STATEMENT TARGET (PB6, all pairs for `kappa=1`).** -/
def oneCircuitAllPairTarget
    (H : (D -> F) →ₗ[F] W) (y0 y1 : W)
    (b0 b1 : D -> F) (g : Fin 1 -> D -> F)
    (P : Finset (Pair D F)) (R t d : Nat) : Prop :=
  PavingBasisHypotheses H y0 y1 b0 b1 g P R t d ->
    P.card ≤ Nat.choose (R + 1) 2 / (R - t)

end PavingBasisAllPairs
end GrandeFinale
