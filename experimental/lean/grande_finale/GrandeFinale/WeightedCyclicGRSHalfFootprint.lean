import Mathlib

/-!
# Weighted cyclic-GRS half-footprint compiler: partial statement targets

This module contains **UNPROVED STATEMENT TARGETS** matching
`experimental/notes/thresholds/weighted_cyclic_grs_half_footprint_compiler.md`.
Every target is a `Prop` definition.  No Lean proof is claimed.

The field `F` below is the code alphabet (deployed `F_{p^6}`), not
necessarily the prime field.  The quotient is represented by a multiplicative
`MonoidHom`; `Q` has no field
structure here.  Thus the formal interface cannot silently treat `x |-> x^L`
as Frobenius or treat `mu_q` as a subfield.  The compiler targets retain the
arbitrary nonzero GRS multipliers, the forward source normalization, realization
of every linear `Phi`, and the discrepancy/nonvanishing identity.  The final
target is only the conditional core-root budget; it contains no occupancy or
parent-routing conclusion.  The discrepancy target records the scalar
identity and its zero/root consequences, but does not yet formalize the
existence and uniqueness of the complement interpolant or the summed weighted
agreement formula.  The core target records only the conditional inequality;
the exact-footprint specialization is not separately formalized here.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace WeightedCyclicGRSHalfFootprint

set_option autoImplicit false

universe u v w

/-! ## Finite coefficient spaces -/

/-- Coefficients of a polynomial of degree strictly less than `n`. -/
abbrev Coeffs (F : Type u) (n : ℕ) := Fin n → F

/-- Evaluation of a bounded coefficient vector. -/
def evalCoeffs {F : Type u} [Field F] {n : ℕ} (c : Coeffs F n) (x : F) : F :=
  ∑ i : Fin n, c i * x ^ (i : ℕ)

/-- Coefficient truncation of an ordinary polynomial. -/
def coeffVector {F : Type u} [Field F] (n : ℕ) (f : Polynomial F) : Coeffs F n :=
  fun i => f.coeff (i : ℕ)

/-- A coefficient vector is the zero polynomial. -/
def VectorZero {F : Type u} [Field F] {n : ℕ} (c : Coeffs F n) : Prop :=
  ∀ i, c i = 0

/-! ## Literal multiplicative quotient data -/

/-- The group-theoretic data used by the compiler.  `pi` is explicitly a
quotient homomorphism, the coordinate embeddings land in `F^*`, and every
fiber has exactly `L` elements.  No additive or field structure is put on
`Q`. -/
structure QuotientModel (F : Type u) (H : Type v) (Q : Type w)
    [Field F] [CommGroup H] [CommGroup Q] [Fintype H] [Fintype Q]
    [DecidableEq Q] (q L : ℕ) where
  pi : H →* Q
  xCoord : H →* Fˣ
  yCoord : Q →* Fˣ
  pi_surjective : Function.Surjective pi
  xCoord_injective : Function.Injective xCoord
  yCoord_injective : Function.Injective yCoord
  q_card : Fintype.card Q = q
  h_card : Fintype.card H = q * L
  fiber_card : ∀ y : Q, Fintype.card {x : H // pi x = y} = L
  power_compatibility : ∀ x : H,
    ((xCoord x : F) ^ L) = (yCoord (pi x) : F)
  q_root : ∀ y : Q, (yCoord y : F) ^ q = 1
  q_ne_zero : (q : F) ≠ 0

section Compiler

variable {F : Type u} {H : Type v} {Q : Type w}
variable [Field F] [CommGroup H] [CommGroup Q]
variable [Fintype H] [Fintype Q] [DecidableEq Q]
variable {q k L : ℕ}

/-- The unique degree-`<L` fiber representatives encode the normalized literal
received word `received x / multiplier x`. -/
def RepresentsWeightedSource (model : QuotientModel F H Q q L)
    (multiplier received : H → F) (u : Q → Coeffs F L) : Prop :=
  ∀ x : H,
    evalCoeffs (u (model.pi x)) (model.xCoord x : F) =
      received x / multiplier x

/-- The cyclic dual multiplier `(prod_{z!=y}(y-z))^-1 = y/q`. -/
def dualWeight (model : QuotientModel F H Q q L) (y : Q) : F :=
  (model.yCoord y : F) / (q : F)

/-- The `j`-th `W`-valued syndrome of the normalized source. -/
def syndrome (model : QuotientModel F H Q q L) (u : Q → Coeffs F L)
    (j : Fin k) : Coeffs F L :=
  fun r => ∑ y : Q,
    dualWeight model y * (model.yCoord y : F) ^ (j : ℕ) * u y r

/-- `Phi` is exactly the linear map induced by the source syndromes. -/
def InducesPhi (model : QuotientModel F H Q q L)
    (u : Q → Coeffs F L) (Phi : Coeffs F k →ₗ[F] Coeffs F L) : Prop :=
  ∀ (f : Coeffs F k) (r : Fin L),
    Phi f r = ∑ j : Fin k, f j * syndrome model u j r

/-- **UNPROVED STATEMENT TARGET: weighted source in both directions.**

When `q=2k`, every literal weighted received word has unique normalized fiber
representatives and induces a `Phi`.  Conversely, for every nonzero multiplier
vector and every linear `Phi`, a literal received word realizes that `Phi`.
The converse quantifies over the multipliers before `Phi`, so weight restoration
is part of the target rather than a post-hoc isometry slogan. -/
def compilerTarget (model : QuotientModel F H Q q L) : Prop :=
  q = 2 * k ∧
    (∀ (multiplier received : H → F),
      (∀ x, multiplier x ≠ 0) →
      ∃! u : Q → Coeffs F L,
        RepresentsWeightedSource model multiplier received u ∧
          ∃ Phi : Coeffs F k →ₗ[F] Coeffs F L, InducesPhi model u Phi) ∧
    ∀ (multiplier : H → F),
      (∀ x, multiplier x ≠ 0) →
      ∀ Phi : Coeffs F k →ₗ[F] Coeffs F L,
        ∃ (received : H → F) (u : Q → Coeffs F L),
          RepresentsWeightedSource model multiplier received u ∧
            InducesPhi model u Phi

/-! ## Exact half-footprint discrepancy -/

/-- `q_{J,y}(Z)=prod_{z in J\{y}}(Z-y_z)`. -/
def footprintLocator (model : QuotientModel F H Q q L)
    (J : Finset Q) (y : Q) : Polynomial F :=
  (J.erase y).prod fun z =>
    Polynomial.X - Polynomial.C (model.yCoord z : F)

/-- Value on one outer point of a coefficientwise degree-`<k` interpolant. -/
def outerValue (model : QuotientModel F H Q q L)
    (outer : Fin L → Coeffs F k) (y : Q) : Coeffs F L :=
  fun r => evalCoeffs (outer r) (model.yCoord y : F)

/-- The outer interpolant agrees with `u` away from `J`. -/
def MatchesComplement (model : QuotientModel F H Q q L)
    (u : Q → Coeffs F L) (J : Finset Q)
    (outer : Fin L → Coeffs F k) : Prop :=
  ∀ y, y ∉ J → outerValue model outer y = u y

/-- Roots inside the literal quotient fiber indexed by `y`. -/
noncomputable def fiberRoots (model : QuotientModel F H Q q L)
    (value : Coeffs F L) (y : Q) : Finset H := by
  classical
  exact Finset.univ.filter fun x =>
    model.pi x = y ∧ evalCoeffs value (model.xCoord x : F) = 0

/-- **UNPROVED PARTIAL STATEMENT TARGET: discrepancy, nonvanishing, and roots.**

For every half-footprint `J`, every `y in J`, and every coefficientwise outer
interpolant matching the complement, this states

`Phi(q_{J,y}) = (y/q) q_{J,y}(y) (u_y-P_{J,y})`.

It also states the exact zero/nonzero equivalence and equality of the two root
sets on the literal fiber.  It does not state existence/uniqueness of the
complement interpolant or the final summed agreement formula. -/
def discrepancyTarget (model : QuotientModel F H Q q L) : Prop :=
  q = 2 * k →
    ∀ (u : Q → Coeffs F L) (Phi : Coeffs F k →ₗ[F] Coeffs F L),
      InducesPhi model u Phi →
      ∀ (J : Finset Q), J.card = k →
        ∀ y ∈ J,
          ∀ outer : Fin L → Coeffs F k,
            MatchesComplement model u J outer →
              let locator := footprintLocator model J y
              let discrepancy : Coeffs F L :=
                fun r => u y r - outerValue model outer y r
              let output := Phi (coeffVector k locator)
              (∀ r : Fin L,
                output r =
                  dualWeight model y * locator.eval (model.yCoord y : F) *
                    discrepancy r) ∧
              (VectorZero output ↔ VectorZero discrepancy) ∧
              fiberRoots model output y = fiberRoots model discrepancy y

end Compiler

/-! ## Deployed core-root budget -/

/-- Deployed field and quotient constants. -/
def deployedPrime : ℕ := 2_130_706_433
def deployedLength : ℕ := 2_097_152
def deployedDimension : ℕ := 1_048_576
def deployedAgreement : ℕ := 1_116_047
def deployedOuterLength : ℕ := 64
def deployedOuterDimension : ℕ := 32
def deployedFiberLength : ℕ := 32_768
def deployedExcessAgreement : ℕ := 67_471
def deployedCoreSize : ℕ := 27
def deployedOwnerSize : ℕ := 5
def deployedRootBudget : ℕ := 32_767

section CoreRoot

variable {F : Type u} [Field F] [DecidableEq F]

/-- One monic linear locator factor. -/
def linearFactor (a : F) : Polynomial F :=
  Polynomial.X - Polynomial.C a

/-- `L_A`. -/
def setLocator (A : Finset F) : Polynomial F :=
  A.prod linearFactor

/-- `A_a=L_A/(Z-a)`, written as the product over `A\{a}`. -/
def ownerFactor (A : Finset F) (a : F) : Polynomial F :=
  (A.erase a).prod linearFactor

/-- Literal common roots for owner `a` and polynomial subspace `U`. -/
noncomputable def commonRoots (fiber : F → Finset F)
    (Phi : Polynomial F →ₗ[F] Polynomial F) (A : Finset F) (a : F)
    (U : Submodule F (Polynomial F)) : Finset F := by
  classical
  exact (fiber a).filter fun x =>
    ∀ P ∈ U, (Phi (ownerFactor A a * P)).eval x = 0

/-- **UNPROVED PARTIAL STATEMENT TARGET: conditional core-root budget.**

The hypotheses retain `|A|=27`, `U<=F[Z]_{<=5}`, `deg T<=4`, literal
`x^L=a` quotient fibers of size `L`, pairwise fiber disjointness, the core
memberships `(Z-a)T in U`, and nonvanishing of `Phi(L_A T)`.  The conclusion
is exactly `sum |Z_a(U)| <= L-1`.

This target contains no exact-footprint nonvanishing corollary, `d_loc`,
`g_loc`, `r_T`, `g_inner`, occupancy, parent recurrence, or official-score
conclusion. -/
def coreRootBudgetTarget (L : ℕ) (fiber : F → Finset F)
    (Phi : Polynomial F →ₗ[F] Polynomial F) (A S : Finset F)
    (U : Submodule F (Polynomial F)) (T : Polynomial F) : Prop :=
  0 < L →
    (64 : F) ≠ 0 →
    A.card = deployedCoreSize →
    S ⊆ A →
    (∀ a ∈ A, a ^ deployedOuterLength = 1) →
    (∀ a ∈ A, (fiber a).card = L) →
    (∀ a ∈ A, ∀ x ∈ fiber a, x ^ L = a) →
    (∀ a ∈ A, ∀ b ∈ A, a ≠ b → Disjoint (fiber a) (fiber b)) →
    (∀ P ∈ U, P.natDegree ≤ 5) →
    T.natDegree ≤ 4 →
    (∀ P : Polynomial F, P.natDegree < deployedOuterDimension →
      (Phi P).natDegree < L) →
    (∀ a ∈ S, linearFactor a * T ∈ U) →
    Phi (setLocator A * T) ≠ 0 →
    S.sum (fun a => (commonRoots fiber Phi A a U).card) ≤ L - 1

end CoreRoot

end WeightedCyclicGRSHalfFootprint
end GrandeFinale
