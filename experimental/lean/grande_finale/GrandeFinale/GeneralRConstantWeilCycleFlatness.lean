import Mathlib

/-!
# General-`R` constant-Weil cycle flatness: statement target

This module is an **UNPROVED STATEMENT TARGET** for
`experimental/notes/thresholds/general_r_constant_weil_cycle_flatness.md`.
It makes the finite certificate and asymptotic family claim type-check without
claiming a Lean proof.  The load-bearing classical mixed-Weil estimate remains
an explicit hypothesis.

The target deliberately keeps the packet's scope: odd-characteristic finite
fields, unweighted multiplicative cosets with planted deletion, polynomial
prefix depth `1 ≤ R < p`, fixed-density slices, the exact characteristic-cycle
factor, full effective span, full image, and residual max-fiber control.
-/

open scoped BigOperators
open Filter

noncomputable section

namespace GrandeFinale
namespace GeneralRConstantWeilCycleFlatness

set_option autoImplicit false

universe u

/-- A complex-valued additive character, kept elementary so the mixed-Weil
input is visible rather than hidden behind a library-specific duality API. -/
structure AdditiveCharacter (B : Type u) [AddMonoid B] where
  toFun : B → ℂ
  map_zero : toFun 0 = 1
  map_add : ∀ x y, toFun (x + y) = toFun x * toFun y
  norm_eq_one : ∀ x, ‖toFun x‖ = 1

instance {B : Type u} [AddMonoid B] :
    CoeFun (AdditiveCharacter B) (fun _ => B → ℂ) :=
  ⟨AdditiveCharacter.toFun⟩

variable {B : Type u} [Field B] [Fintype B] [DecidableEq B]

/-- The polynomial-prefix vector `g(t) = (t, t², ..., tᴿ)`. -/
def prefixVector (R : ℕ) (t : B) : Fin R → B :=
  fun i => t ^ (i.1 + 1)

/-- The prefix sum attached to a finite support. -/
def prefixSum (R : ℕ) (S : Finset B) : Fin R → B :=
  fun i => ∑ t ∈ S, t ^ (i.1 + 1)

/-- The fixed-composition Boolean slice `binom(T,m)`. -/
def slice (T : Finset B) (m : ℕ) : Finset (Finset B) :=
  T.powersetCard m

/-- Cardinality of one polynomial-prefix fiber. -/
def fiberCount (T : Finset B) (m R : ℕ) (z : Fin R → B) : ℕ :=
  ((slice T m).filter fun S => prefixSum R S = z).card

/-- Additive span of the translated prefix vectors.  Equality with `⊤` is the
packet's full-effective-span conclusion. -/
def differenceSpan (T : Finset B) (R : ℕ) : AddSubgroup (Fin R → B) :=
  AddSubgroup.closure
    {v | ∃ t ∈ T, ∃ t₀ ∈ T,
      v = prefixVector R t - prefixVector R t₀}

/-- A finite subset of the field is a multiplicative coset. -/
def IsMultiplicativeCoset (D : Finset B) : Prop :=
  ∃ (θ : Bˣ) (H : Subgroup Bˣ),
    ∀ t : B, t ∈ D ↔ ∃ h : Bˣ, h ∈ H ∧ t = ↑(θ * h)

/-- Polynomial phase in Fourier direction `a`. -/
def phasePolynomial (R : ℕ) (a : Fin R → B) (t : B) : B :=
  ∑ i, a i * t ^ (i.1 + 1)

/-- Power sum used in the characteristic-cycle decomposition. -/
def phaseSum (ψ : AdditiveCharacter B) (T : Finset B) (R j : ℕ)
    (a : Fin R → B) : ℂ :=
  ∑ t ∈ T, ψ (j • phasePolynomial R a t)

/-- The exact classical input used by the packet: a nontrivial additive
character and the `Λ` mixed-Weil bound for every nonzero direction and every
cycle index not divisible by the characteristic. -/
def MixedWeilInput (ψ : AdditiveCharacter B) (T : Finset B)
    (p R : ℕ) (Λ : ℝ) : Prop :=
  (∃ x : B, ψ x ≠ 1) ∧
    ∀ (a : Fin R → B), a ≠ 0 →
      ∀ j : ℕ, ¬p ∣ j → ‖phaseSum ψ T R j a‖ ≤ Λ

/-- Generalized binomial `binom(x+r-1,r)` as a finite rising product. -/
def risingBinom (x : ℝ) (r : ℕ) : ℝ :=
  (∏ i ∈ Finset.range r, (x + (i : ℝ))) / (r.factorial : ℝ)

/-- Exact finite relative-error certificate `ε_{R,*}` from the note. -/
def cycleError (Q R N p r : ℕ) (Λ : ℝ) : ℝ :=
  let β := ((N : ℝ) - Λ) / (p : ℝ)
  let L := r / p
  (((Q : ℝ) ^ R - 1) / (Nat.choose N r : ℝ)) *
    risingBinom Λ r * risingBinom (β + 1) L

/-- Exact average fiber size `binom(N,m)/Q^R`. -/
def averageFiber (T : Finset B) (m R : ℕ) : ℝ :=
  (Nat.choose T.card m : ℝ) / (Fintype.card B : ℝ) ^ R

/-- Uniform relative fiber estimate with error parameter `ε`. -/
def RelativeFiberBound (T : Finset B) (m R : ℕ) (ε : ℝ) : Prop :=
  ∀ z : Fin R → B,
    |(fiberCount T m R z : ℝ) - averageFiber T m R| ≤
      ε * averageFiber T m R

/-- Exact surjectivity of the realized polynomial-prefix image. -/
def FullImage (T : Finset B) (m R : ℕ) : Prop :=
  ∀ z : Fin R → B, ∃ S ∈ slice T m, prefixSum R S = z

/-- Max-fiber control for every first-match residual (indeed every subslice). -/
def ResidualFiberBound (T : Finset B) (m R : ℕ) (ε : ℝ) : Prop :=
  ∀ Ω : Finset (Finset B), Ω ⊆ slice T m →
    ∀ z : Fin R → B,
      (((Ω.filter fun S => prefixSum R S = z).card : ℕ) : ℝ) ≤
        (1 + ε) * averageFiber T m R

/-- All finite-row hypotheses, including every field, coset, deletion,
characteristic, prefix-depth, and mixed-Weil condition used in the proof. -/
def FiniteHypotheses (D P T : Finset B) (ψ : AdditiveCharacter B)
    (p m R : ℕ) (C₀ Λ : ℝ) : Prop :=
  Nat.Prime p ∧ p ≠ 2 ∧ CharP B p ∧
    1 ≤ R ∧ R < p ∧ m ≤ T.card ∧
    IsMultiplicativeCoset D ∧ T = D \ P ∧
    Λ = C₀ * ((R : ℝ) + 1) * Real.sqrt (Fintype.card B : ℝ) + P.card ∧
    MixedWeilInput ψ T p R Λ

/-- The finite theorem claimed by the packet. -/
def FiniteConclusion (T : Finset B) (m R p : ℕ) (Λ : ℝ) : Prop :=
  let r := min m (T.card - m)
  let ε := cycleError (Fintype.card B) R T.card p r Λ
  differenceSpan T R = ⊤ ∧
    RelativeFiberBound T m R ε ∧
    (ε < 1 → FullImage T m R) ∧
    ResidualFiberBound T m R ε

/-- **UNPROVED STATEMENT TARGET (finite form).**  For `1 ≤ Λ < N`, the exact
cycle coefficient implies full span, the `ε_{R,*}` Fourier bound, full image
when `ε_{R,*}<1`, and the inherited residual max-fiber bound. -/
def finiteTheoremTarget (D P T : Finset B) (ψ : AdditiveCharacter B)
    (p m R : ℕ) (C₀ Λ : ℝ) : Prop :=
  FiniteHypotheses D P T ψ p m R C₀ Λ ∧
      1 ≤ Λ ∧ Λ < T.card →
    FiniteConclusion T m R p Λ

/-- Natural-log binary entropy. -/
def binaryEntropy (x : ℝ) : ℝ :=
  -x * Real.log x - (1 - x) * Real.log (1 - x)

/-- The note's entropy margin, written as an infimum over the compact density
interval (equal to its displayed minimum). -/
def entropyMargin (α lam : ℝ) : ℝ :=
  sInf ((fun x =>
    binaryEntropy x - (x + lam) * binaryEntropy (x / (x + lam))) ''
      Set.Icc α (1 / 2 : ℝ))

/-- Per-row field-size plus characteristic-cycle penalty. -/
def rowPenalty (Q R N p : ℕ) : ℝ :=
  (R : ℝ) * Real.log (Q : ℝ) / (N : ℝ) +
    3 * Real.log 2 / (2 * (p : ℝ))

/-- Operational form of the strict `limsup < δ` gate: an eventually uniform
positive margin below `δ`. -/
def StrictEntropyGate (Q R N p : ℕ → ℕ) (α lam : ℝ) : Prop :=
  ∃ η : ℝ, 0 < η ∧
    ∀ᶠ ν in atTop,
      rowPenalty (Q ν) (R ν) (N ν) (p ν) ≤
        entropyMargin α lam - η

/-- **UNPROVED STATEMENT TARGET (asymptotic form).**  This is the packet's
full family theorem in the eventually-uniform-margin form equivalent to its
strict limsup gate.  It includes fixed density, `Λ/N ≤ λ < 1/2`, full target
`B_ν^{R_ν}`, exponential equidistribution, exact realized image, and every
residual max-fiber bound. -/
def asymptoticTheoremTarget
    (BFam : ℕ → Type u)
    [∀ ν, Field (BFam ν)] [∀ ν, Fintype (BFam ν)]
    [∀ ν, DecidableEq (BFam ν)]
    (D P T : ∀ ν, Finset (BFam ν))
    (ψ : ∀ ν, AdditiveCharacter (BFam ν))
    (p m R : ℕ → ℕ) (C₀ α lam : ℝ) (Λ : ℕ → ℝ) : Prop :=
  let Q : ℕ → ℕ := fun ν => Fintype.card (BFam ν)
  let N : ℕ → ℕ := fun ν => (T ν).card
  0 < C₀ ∧ 0 < α ∧ α < 1 / 2 ∧ 0 < lam ∧ lam < 1 / 2 ∧
    Tendsto N atTop atTop ∧
    (∀ ν, FiniteHypotheses (D ν) (P ν) (T ν) (ψ ν)
      (p ν) (m ν) (R ν) C₀ (Λ ν)) ∧
    (∀ᶠ ν in atTop,
      α ≤ (m ν : ℝ) / (N ν : ℝ) ∧
      (m ν : ℝ) / (N ν : ℝ) ≤ 1 - α ∧
      Λ ν / (N ν : ℝ) ≤ lam) ∧
    StrictEntropyGate Q R N p α lam →
  ∃ c : ℝ, 0 < c ∧
    ∀ᶠ ν in atTop,
      differenceSpan (T ν) (R ν) = ⊤ ∧
      RelativeFiberBound (T ν) (m ν) (R ν)
        (Real.exp (-c * (N ν : ℝ))) ∧
      FullImage (T ν) (m ν) (R ν) ∧
      ResidualFiberBound (T ν) (m ν) (R ν)
        (Real.exp (-c * (N ν : ℝ)))

end GeneralRConstantWeilCycleFlatness
end GrandeFinale
