import Mathlib

/-!
# Rank-16 left-kernel / shortened-dual / Forney: scaffold contracts

This module contains **SCAFFOLD DEFINITIONS AND EXACT CERTIFICATE DATA
CONTRACTS ONLY** for
`experimental/notes/l2/rank16_left_kernel_forney_route_cut.md`.

It deliberately does not state the kernel isomorphisms, rank/nullity formulas,
or Forney-index formulas as Lean propositions. A faithful formalization of
those results must first construct the actual finite-dimensional evaluation
spaces, shortened submodules, sum maps, quotient dual, transpose map, and a
certified row-reduced polynomial-syzygy basis. Treating their dimensions or
Forney indices as unrelated natural-number inputs would not encode the prose
theorem.

There are no theorem declarations, axioms, or source-selection claims here.
In particular, this file does not prove that a deployed violating list exists,
that selected supports with full union exist, or that the deployed endpoint
`h = 1` is source-realized. The closed arithmetic contracts and expected
`F_31` output record only what the external dependency-free verifier checks.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace Rank16LeftKernelForney

set_option autoImplicit false

universe u v

variable {F : Type u} [Field F] [DecidableEq F]

/-! ## Literal selected-support scaffold -/

/-- The union of a finite family of selected supports. -/
def selectedUnion {t : Nat} (S : Fin t -> Finset F) : Finset F :=
  Finset.univ.biUnion S

/-- Exact source-side hypotheses from the prose theorem.

The common received word and agreement premise are explicit data. No kernel,
rank, nullity, quotient, or Forney-index conclusion is attached to this
predicate in the present scaffold. -/
def SelectedSupportHypotheses (t K m n e sigma : Nat) (H : Finset F)
    (u : F -> F) (P : Fin t -> Polynomial F) (S : Fin t -> Finset F) : Prop :=
  2 <= t ∧
    1 <= K ∧
    K <= m ∧
    m <= n ∧
    H.card = n ∧
    sigma = m - K ∧
    (selectedUnion S).card = m + e ∧
    (∀ i,
      P i ∈ Polynomial.degreeLT F K ∧
        S i ⊆ H ∧
        (S i).card = m ∧
        ∀ x ∈ S i, (P i).eval x = u x) ∧
    ∀ i j, i ≠ j -> P i ≠ P j ∧ S i ≠ S j

/-- Bundled selected-support data satisfying the literal hypotheses. This is
an input scaffold, not an existence assertion. -/
structure SelectedSupportScaffold where
  t : Nat
  K : Nat
  m : Nat
  n : Nat
  e : Nat
  sigma : Nat
  H : Finset F
  received : F -> F
  listed : Fin t -> Polynomial F
  supports : Fin t -> Finset F
  hypotheses :
    SelectedSupportHypotheses t K m n e sigma H received listed supports

/-! ## Honest post-selection predicates -/

section CommonSyndrome

variable {V : Type v} [AddCommGroup V] [Module F V]

/-- The actual post-selection common-syndrome premise: one nonzero functional
annihilates one specified shortened span. No codimension is inferred here. -/
def CommonSyndromePremise (phi : V →ₗ[F] F)
    (shortenedSpan : Submodule F V) : Prop :=
  phi ≠ 0 ∧ ∀ z ∈ shortenedSpan, phi z = 0

end CommonSyndrome

/-- Monic equal-degree locators with a Bezout identity, the polynomial form of
`gcd(E_0,...,E_{t-1}) = 1`. -/
def LocatorHypotheses {t : Nat} (E : Fin t -> Polynomial F) (e : Nat) : Prop :=
  (∀ i, (E i).Monic ∧ (E i).natDegree = e) ∧
    ∃ A : Fin t -> Polynomial F, ∑ i, E i * A i = 1

/-- A literal tuple in the bounded locator-syzygy set at truncation `sigma`.
No basis, row-reducedness, predictable-degree property, or dimension formula
is postulated. -/
def BoundedLocatorSyzygy {t : Nat} (E : Fin t -> Polynomial F) (sigma : Nat)
    (A : Fin t -> Polynomial F) : Prop :=
  (∀ i, A i ∈ Polynomial.degreeLT F sigma) ∧
    ∑ i, E i * A i = 0

/-! ## Closed arithmetic scaffold contracts -/

/-- Closed deployed arithmetic replayed by the Python verifier. This contract
does not assert the existence of a deployed full-union tuple with `h = 1`. -/
def deployedArithmeticContract : Prop :=
  1_116_047 - 1_048_576 = 67_471 ∧
    2_097_152 - 1_116_047 = 981_105 ∧
    16 * 1_116_047 - 2_097_152 = 15_759_600 ∧
    15 * 1_048_576 = 15_728_640 ∧
    15 * 1_048_576 - 1 = 15_728_639 ∧
    15 * 67_471 - 981_105 = 30_960 ∧
    15 * 67_471 - 981_105 + 1 = 30_961 ∧
    67_471 + 1 = 67_472

/-- Closed elementary arithmetic behind the `F_31` transcript. Matrix ranks
and the Forney profile are expected external-verifier data below, not claims
derived by these numeral equalities. -/
def f31ArithmeticContract : Prop :=
  Nat.choose 30 16 = 145_422_675 ∧
    (Nat.choose 30 16 + 30) / 31 = 4_691_055 ∧
    16 * 16 - 30 = 226 ∧
    15 * 15 = 225 ∧
    225 - 224 = 1 ∧
    226 - 224 = 2

/-! ## Expected external-verifier output -/

/-- Data shape of the pinned `F_31` verifier result. This structure carries
expected output only; it is not a theorem that a matrix has these ranks. -/
structure F31VerifierOutput where
  fullListSize : Nat
  supportCount : Nat
  zeroSumSupportCount : Nat
  unionSize : Nat
  exactAgreementSupportCount : Nat
  affineRank : Nat
  affineDeterminant : Nat
  commonSyndromeDegree : Nat
  commonSyndromeValue : Nat
  complementLocatorSpan : Nat
  shortenedDualCodimension : Nat
  macaulayRanks : List Nat
  macaulayNullities : List Nat
  forneyProfile : List Nat
  matrixRows : Nat
  matrixColumns : Nat
  matrixRank : Nat
  rightNullity : Nat
  leftNullity : Nat

/-- Exact expected output mirrored from the pinned JSON/transcript. The Python
verifier, not this definition, reconstructs and checks the fixture. -/
def expectedF31VerifierOutput : F31VerifierOutput where
  fullListSize := 4_691_055
  supportCount := 16
  zeroSumSupportCount := 16
  unionSize := 30
  exactAgreementSupportCount := 16
  affineRank := 15
  affineDeterminant := 2
  commonSyndromeDegree := 13
  commonSyndromeValue := 1
  complementLocatorSpan := 14
  shortenedDualCodimension := 1
  macaulayRanks := [14, 16, 17]
  macaulayNullities := [2, 16, 31]
  forneyProfile := [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
  matrixRows := 226
  matrixColumns := 225
  matrixRank := 224
  rightNullity := 1
  leftNullity := 2

end Rank16LeftKernelForney
end GrandeFinale
