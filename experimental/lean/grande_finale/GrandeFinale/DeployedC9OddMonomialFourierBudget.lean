import Mathlib

/-!
# Deployed C9 odd-monomial Fourier budget: statement target

This module is an **UNPROVED STATEMENT TARGET** for
`experimental/notes/thresholds/deployed_c9_odd_monomial_fourier_budget.md`.
It records the exact D2--D5 integer brackets, the finite pointwise-to-aggregate
odd-axis compiler, and the quadratic-method route cut.  It deliberately makes
no claim about first-match deletion, even or multimonomial modes, weighted
circles, a global maximum fiber, or either official prize question.
-/

open scoped BigOperators Classical

namespace GrandeFinale
namespace DeployedC9OddMonomialFourierBudget

set_option autoImplicit false

def p : Nat := 2130706433
def q : Nat := 131072
def w : Nat := 67471
def tMinus : Nat := 60000
def tPlus : Nat := 51566
def blockPairs : Nat := 8
def gaussLambda : Nat := 46160

def oddModeCount : Nat := 33736 * (p - 1)

def zeroMinus : Nat := Nat.choose q tMinus
def zeroPlus : Nat := Nat.choose q tPlus
def fullSlice : Nat := (zeroMinus * zeroPlus) ^ blockPairs

def oddMinus : Nat := Nat.choose (gaussLambda + tMinus - 1) tMinus
def oddPlus : Nat := Nat.choose (gaussLambda + tPlus - 1) tPlus
def oddPerMode : Nat := (oddMinus * oddPlus) ^ blockPairs
def oddBudget : Nat := oddModeCount * oddPerMode
def labeledBudget : Nat := Nat.factorial 16 * (fullSlice + oddBudget)

def pairBudget : Nat :=
  tMinus * (q - tMinus) + tPlus * (q - tPlus)
def pairGap : Nat := (w + 1) * q - pairBudget

def quadraticLambda : Nat := 2 * gaussLambda
def quadraticMinus : Nat :=
  Nat.choose (quadraticLambda + tMinus - 1) tMinus
def quadraticPlus : Nat :=
  Nat.choose (quadraticLambda + tPlus - 1) tPlus

/-- `e` is the maximal strict binary exponent for `num / den < 2^-e`. -/
def StrictBinaryBracket (num den e : Nat) : Prop :=
  num * 2 ^ e < den ∧ den ≤ num * 2 ^ (e + 1)

/-- `e` is the binary floor of the ratio `upper / lower`. -/
def BinaryRatioFloorBracket (lower upper e : Nat) : Prop :=
  lower * 2 ^ e ≤ upper ∧ upper < lower * 2 ^ (e + 1)

/-- **UNPROVED STATEMENT TARGET (exact finite certificate).**  These are the
literal arithmetic obligations D1--D5, the supporting two-block Plotkin cap,
and the exact quadratic nonpayment comparisons from the note. -/
def arithmeticCertificateTarget : Prop :=
  Nat.Prime p ∧
  q = 2 ^ 17 ∧
  p - 1 = 127 * 2 ^ 24 ∧
  oddModeCount = 71881512189952 ∧
  StrictBinaryBracket oddBudget (p ^ w) 472028 ∧
  StrictBinaryBracket oddBudget fullSlice 438163 ∧
  StrictBinaryBracket fullSlice (p ^ w) 33865 ∧
  StrictBinaryBracket labeledBudget (p ^ w) 33820 ∧
  pairBudget = 8364126396 ∧
  pairGap = 479563588 ∧
  18 * pairGap ≤ (w + 1) * q ∧
  (w + 1) * q < 19 * pairGap ∧
  zeroMinus < quadraticMinus ∧
  zeroPlus < quadraticPlus ∧
  BinaryRatioFloorBracket zeroMinus quadraticMinus 16937 ∧
  BinaryRatioFloorBracket zeroPlus quadraticPlus 8701

/-- **UNPROVED STATEMENT TARGET (odd-axis aggregate compiler).**  Once each
of the exactly indexed odd modes obeys the proved per-mode cycle-index bound,
their complete-slice absolute Fourier sum obeys the D2 and D3 payments. -/
def oddAxisAggregateTarget
    (fourierAbs : Fin oddModeCount → Nat) : Prop :=
  (∀ i, fourierAbs i ≤ oddPerMode) →
    let total := ∑ i, fourierAbs i
    total ≤ oddBudget ∧
      total * 2 ^ 472028 < p ^ w ∧
      total * 2 ^ 438163 < fullSlice

/-- **UNPROVED STATEMENT TARGET (quadratic route cut).**  The same absolute
Gauss-period plus uniform cycle-index method gives a majorant already larger
than the zero coefficient on both deployed block sizes. -/
def quadraticMethodRouteCutTarget : Prop :=
  zeroMinus < quadraticMinus ∧ zeroPlus < quadraticPlus

end DeployedC9OddMonomialFourierBudget
end GrandeFinale
