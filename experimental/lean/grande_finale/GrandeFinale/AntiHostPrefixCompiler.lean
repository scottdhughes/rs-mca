import Mathlib

/-!
# One-deeper locator prefix to anti-host MCA compiler: statement target

This module is an **UNPROVED STATEMENT TARGET** for
`experimental/notes/thresholds/one_deeper_prefix_anti_host_compiler.md`.
It records the complete finite compiler as a proposition without claiming a
Lean proof.

The target keeps the base field `B`, extension field `F`, exact locator-prefix
fiber, field-size gate, exact-support MCA incidence, challenge-restricted
numerator, and unrestricted rational-host exclusion visible.  In particular,
the host predicate imposes no monicity, coprimality, or reducedness condition.
-/

open scoped BigOperators Classical
open Polynomial

noncomputable section

namespace GrandeFinale
namespace AntiHostPrefixCompiler

set_option autoImplicit false

universe u v

variable {B : Type u} {F : Type v}
variable [Field B] [Fintype B] [DecidableEq B]
variable [Field F] [Fintype F] [DecidableEq F]
variable [Algebra B F] [FiniteDimensional B F]

/-! ## Locator-prefix input -/

/-- The monic locator polynomial `Q_S(X) = product_(x in S) (X - x)`. -/
def locator (S : Finset B) : B[X] :=
  ∏ x ∈ S, (X - C x)

/-- The first `s` coefficients below the leading term of a degree-`m` locator.
Index `i : Fin s` records the coefficient of `X^(m-(i+1))`. -/
def locatorPrefix (m s : Nat) (S : Finset B) : Fin s -> B :=
  fun i => (locator S).coeff (m - (i.1 + 1))

/-- The exact extension-field cardinality gate
`|F| > max {n + (k-1) choose(N,2), 1 + (n-m)N}`. -/
def FieldSizeGate (D : Finset B) (k m N : Nat) : Prop :=
  max (D.card + (k - 1) * Nat.choose N 2)
      (1 + (D.card - m) * N) < Fintype.card F

/-- Exact hypotheses on a depth-`m-k` locator-prefix fiber of `m`-subsets of
`D`, including `1 <= k < m < n`, `n = |D|`, and `N = |G|`. -/
def CompilerHypotheses (D : Finset B) (k m N : Nat)
    (G : Finset (Finset B)) (z : Fin (m - k) -> B) : Prop :=
  1 ≤ k ∧
    k < m ∧
    m < D.card ∧
    G.card = N ∧
    (∀ S ∈ G,
      S ⊆ D ∧
        S.card = m ∧
        locatorPrefix m (m - k) S = z) ∧
    FieldSizeGate (F := F) D k m N

/-! ## Reed-Solomon explanations and MCA bad slopes -/

/-- Evaluation of an `F`-polynomial on the base-field domain `D`, using the
specified algebra embedding `B -> F`. -/
def evalWord (D : Finset B) (p : F[X]) : D -> F :=
  fun x => p.eval (algebraMap B F (x : B))

/-- `RS_F(D,k)`, the evaluations on `D` of polynomials of degree `< k`. -/
def RSCode (D : Finset B) (k : Nat) : Set (D -> F) :=
  {c | ∃ p : F[X], p.degree < (k : WithBot Nat) ∧ c = evalWord D p}

/-- A word has a codeword explanation on every coordinate in `S`. -/
def ExplainedOn (D : Finset B) (C : Set (D -> F))
    (w : D -> F) (S : Finset B) : Prop :=
  ∃ c ∈ C, ∀ x : D, (x : B) ∈ S -> c x = w x

/-- The received pair is simultaneously explained on `S`. -/
def ExplainedPairOn (D : Finset B) (C : Set (D -> F))
    (r0 r1 : D -> F) (S : Finset B) : Prop :=
  ∃ c0 ∈ C, ∃ c1 ∈ C,
    (∀ x : D, (x : B) ∈ S -> c0 x = r0 x) ∧
      (∀ x : D, (x : B) ∈ S -> c1 x = r1 x)

/-- A finite slope is support-wise MCA-bad at agreement threshold `m`. -/
def MCABad (D : Finset B) (C : Set (D -> F))
    (r0 r1 : D -> F) (m : Nat) (gamma : F) : Prop :=
  ∃ S : Finset B,
    S ⊆ D ∧
      m ≤ S.card ∧
      ExplainedOn D C (fun x => r0 x + gamma * r1 x) S ∧
      ¬ ExplainedPairOn D C r0 r1 S

/-- MCA-bad slopes on one received line after restriction to `Gamma`. -/
noncomputable def restrictedMCABadSlopes (D : Finset B)
    (C : Set (D -> F)) (Gamma : Finset F) (r0 r1 : D -> F)
    (m : Nat) : Finset F :=
  Gamma.filter fun gamma => MCABad D C r0 r1 m gamma

/-- The challenge-restricted MCA numerator, maximized over received pairs. -/
noncomputable def B_MCA_challenge (D : Finset B) (C : Set (D -> F))
    (m : Nat) (Gamma : Finset F) : Nat :=
  Finset.univ.sup fun r : (D -> F) × (D -> F) =>
    (restrictedMCABadSlopes D C Gamma r.1 r.2 m).card

/-! ## Exact displayed witnesses -/

/-- A slope, exact support, and explaining polynomial. -/
structure WitnessData (B : Type u) (F : Type v) where
  slope : F
  support : Finset B
  explanation : F[X]

/-- The agreement set of `w` with `p` on `D` is exactly `S`. -/
def ExactAgreement (D : Finset B) (w : D -> F)
    (p : F[X]) (S : Finset B) : Prop :=
  ∀ x : D, w x = evalWord D p x ↔ (x : B) ∈ S

/-- Membership in the exact-`m`, support-wise MCA witness incidence. -/
def ExactSupportWiseMCAWitness (D : Finset B) (k m : Nat)
    (r0 r1 : D -> F) (w : WitnessData B F) : Prop :=
  w.support ⊆ D ∧
    w.support.card = m ∧
    w.explanation.degree < (k : WithBot Nat) ∧
    ExactAgreement D
      (fun x => r0 x + w.slope * r1 x) w.explanation w.support ∧
    ¬ ExplainedPairOn D (RSCode D k) r0 r1 w.support

/-- The displayed map `S |-> (gamma_S,S,h_S)`. -/
def displayedWitness {G : Finset (Finset B)}
    (slope : G -> F) (explanation : G -> F[X])
    (S : G) : WitnessData B F where
  slope := slope S
  support := S.1
  explanation := explanation S

/-- Every displayed explanation pair `(gamma_S,h_S)` has retained-support
occupancy one inside the displayed witness cell. -/
def RetainedSupportOccupancyOne {G : Finset (Finset B)}
    (slope : G -> F) (explanation : G -> F[X]) : Prop :=
  Function.Injective fun S => (slope S, explanation S)

/-! ## Rational-host exclusion and challenge translation -/

/-- A rational-host presentation `r1 = c - T/L` in the complete degree range
`1 <= d = deg L <= n-m-2`, with `deg c < k`, `deg T < d`, and no pole on `D`.
There are deliberately no normalization or coprimality hypotheses. -/
def HasRationalHostPresentation (D : Finset B) (k m : Nat)
    (r1 : D -> F) : Prop :=
  ∃ (c T L : F[X]) (d : Nat),
    c.degree < (k : WithBot Nat) ∧
      L.degree = (d : WithBot Nat) ∧
      1 ≤ d ∧
      d ≤ D.card - m - 2 ∧
      T.degree < (d : WithBot Nat) ∧
      (∀ x : D, evalWord D L x ≠ 0) ∧
      (∀ x : D,
        r1 x = evalWord D c x - evalWord D T x / evalWord D L x)

/-- The exact challenge-set consequence: a shear of the displayed line attains
`ceil(N*|Gamma|/|F|)` bad challenged slopes, and hence so does the maximized
challenge numerator. -/
def ChallengeLowerBound (D : Finset B) (k m N : Nat)
    (r0 r1 : D -> F) : Prop :=
  let C := RSCode (F := F) D k
  ∀ Gamma : Finset F, Gamma.Nonempty ->
    (∃ delta : F,
      (N * Gamma.card) ⌈/⌉ Fintype.card F ≤
        (restrictedMCABadSlopes D C Gamma
          (fun x => r0 x + delta * r1 x) r1 m).card) ∧
      (N * Gamma.card) ⌈/⌉ Fintype.card F ≤
        B_MCA_challenge D C m Gamma

/-- The complete conclusion of the finite one-deeper prefix compiler. -/
def CompilerConclusion (D : Finset B) (k m N : Nat)
    (G : Finset (Finset B)) : Prop :=
  ∃ (r0 r1 : D -> F) (slope : G -> F) (explanation : G -> F[X]),
    Function.Injective (displayedWitness slope explanation) ∧
      Function.Injective slope ∧
      RetainedSupportOccupancyOne slope explanation ∧
      (∀ S : G,
        ExactSupportWiseMCAWitness D k m r0 r1
          (displayedWitness slope explanation S) ∧
        ¬ ExplainedOn D (RSCode D k) r1 S.1) ∧
      ChallengeLowerBound D k m N r0 r1 ∧
      ¬ HasRationalHostPresentation D k m r1

/-- **UNPROVED STATEMENT TARGET.**  A depth-`m-k` locator-prefix fiber of
`N` distinct `m`-subsets, over a finite extension satisfying the exact
field-size gate, compiles to `N` distinct exact-agreement, support-wise
nontrivial MCA slopes with occupancy one, the exact challenge-density lower
bound, and no rational-host presentation for any
`1 <= deg L <= |D|-m-2`. -/
def theoremTarget (D : Finset B) (k m N : Nat)
    (G : Finset (Finset B)) (z : Fin (m - k) -> B) : Prop :=
  CompilerHypotheses (F := F) D k m N G z ->
    CompilerConclusion (F := F) D k m N G

end AntiHostPrefixCompiler
end GrandeFinale
