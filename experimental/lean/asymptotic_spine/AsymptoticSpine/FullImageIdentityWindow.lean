import AsymptoticSpine.EffectiveClosure

namespace AsymptoticSpine

/-!
# Primitive full-image and identity-dominance windows

This module formalizes the exact finite arithmetic extracted in
`experimental/notes/thresholds/fi_full_image_primitive.md` and
`experimental/notes/thresholds/envelope_identity_window.md`.

The full-image part separates the realized-image/effective-span gap from the
effective-span/ambient gap and proves their composition. The identity-window
part clears the field-drop denominator: `lambda = lambdaNum/lambdaDen`.
It proves the lower/upper window union, its exact strict complement, global
coverage when `lambda=1`, and the field-drop crossing wall.

As elsewhere in this stdlib-only package, exponential rates are represented by
finite multiplicative losses and cleared inequalities. The module does not
prove deep span-collapse routing, asymptotic subexponentiality, or the upper
envelope reduction to quotient competitors.
-/

/-! ## The two-gap full-image certificate -/

/-- Ambient full-image certificate with a printed finite loss:
`ambientSize ≤ loss * realizedSize`. -/
def FullImageCertificate
    (realizedSize ambientSize loss : Nat) : Prop :=
  ambientSize ≤ loss * realizedSize

/-- The three finite scales `L ≤ A_eff ≤ A`. -/
structure ImageScaleTower where
  realizedSize : Nat
  effectiveSize : Nat
  ambientSize : Nat
  realized_le_effective : realizedSize ≤ effectiveSize
  effective_le_ambient : effectiveSize ≤ ambientSize

/-- Gap 1 and Gap 2 compose to the ambient full-image certificate. -/
theorem fullImage_of_two_gap_certificates
    (realizedSize effectiveSize ambientSize gapOneLoss gapTwoLoss : Nat)
    (hgapOne : effectiveSize ≤ gapOneLoss * realizedSize)
    (hgapTwo : ambientSize ≤ gapTwoLoss * effectiveSize) :
    FullImageCertificate realizedSize ambientSize (gapTwoLoss * gapOneLoss) := by
  unfold FullImageCertificate
  calc
    ambientSize ≤ gapTwoLoss * effectiveSize := hgapTwo
    _ ≤ gapTwoLoss * (gapOneLoss * realizedSize) :=
      Nat.mul_le_mul_left gapTwoLoss hgapOne
    _ = (gapTwoLoss * gapOneLoss) * realizedSize := by
      rw [Nat.mul_assoc]

/-- Conversely, an ambient certificate gives each weaker scale certificate. -/
theorem fullImage_implies_effective_certificate
    (tower : ImageScaleTower) (loss : Nat)
    (hfull : FullImageCertificate tower.realizedSize tower.ambientSize loss) :
    tower.effectiveSize ≤ loss * tower.realizedSize :=
  Nat.le_trans tower.effective_le_ambient hfull

/-- Shallow-prefix automatic full image: if the entire ambient target fits in
the printed loss and the realized image is nonempty, no filling estimate is
needed. -/
theorem shallow_ambient_to_fullImage
    (realizedSize ambientSize loss : Nat)
    (hrealized : 1 ≤ realizedSize) (hambient : ambientSize ≤ loss) :
    FullImageCertificate realizedSize ambientSize loss := by
  unfold FullImageCertificate
  calc
    ambientSize ≤ loss := hambient
    _ = loss * 1 := by rw [Nat.mul_one]
    _ ≤ loss * realizedSize := Nat.mul_le_mul_left loss hrealized

/-- Ambient max-fiber flatness certifies full image by pigeonhole. -/
theorem ambientFlatness_certifies_fullImage
    (realizedSize ambientSize mass maxFiber loss : Nat)
    (hmax : 0 < maxFiber)
    (hmass : mass ≤ realizedSize * maxFiber)
    (hflat : ambientSize * maxFiber ≤ loss * mass) :
    FullImageCertificate realizedSize ambientSize loss := by
  unfold FullImageCertificate
  have hcancel : maxFiber * ambientSize ≤
      maxFiber * (loss * realizedSize) := by
    calc
      maxFiber * ambientSize = ambientSize * maxFiber := Nat.mul_comm _ _
      _ ≤ loss * mass := hflat
      _ ≤ loss * (realizedSize * maxFiber) :=
        Nat.mul_le_mul_left loss hmass
      _ = maxFiber * (loss * realizedSize) := by
        simp [Nat.mul_comm, Nat.mul_left_comm]
  exact Nat.le_of_mul_le_mul_left hcancel hmax

/-- Effective-scale max-fiber payment supplies Gap 1. -/
theorem effectivePayment_certifies_gapOne
    (realizedSize effectiveSize mass maxFiber loss : Nat)
    (hmax : 0 < maxFiber)
    (hmass : mass ≤ realizedSize * maxFiber)
    (hpayment : effectiveSize * maxFiber ≤ loss * mass) :
    effectiveSize ≤ loss * realizedSize := by
  have hcancel : maxFiber * effectiveSize ≤
      maxFiber * (loss * realizedSize) := by
    calc
      maxFiber * effectiveSize = effectiveSize * maxFiber := Nat.mul_comm _ _
      _ ≤ loss * mass := hpayment
      _ ≤ loss * (realizedSize * maxFiber) :=
        Nat.mul_le_mul_left loss hmass
      _ = maxFiber * (loss * realizedSize) := by
        simp [Nat.mul_comm, Nat.mul_left_comm]
  exact Nat.le_of_mul_le_mul_left hcancel hmax

/-! ## Denominator-cleared identity windows -/

/-- Cleared lower window
`s ≤ ((c-1)/(c-lambda)) h`, for
`lambda=lambdaNum/lambdaDen`. -/
def LowerIdentityWindow
    (foldDegree lambdaNum lambdaDen entropy prefixBits : Nat) : Prop :=
  prefixBits * (foldDegree * lambdaDen - lambdaNum) ≤
    entropy * ((foldDegree - 1) * lambdaDen)

/-- Cleared upper window `s ≥ h/lambda`. -/
def UpperIdentityWindow
    (lambdaNum lambdaDen entropy prefixBits : Nat) : Prop :=
  entropy * lambdaDen ≤ prefixBits * lambdaNum

/-- The exact union of lower and upper identity-dominant windows. -/
def IdentityDominanceWindow
    (foldDegree lambdaNum lambdaDen entropy prefixBits : Nat) : Prop :=
  LowerIdentityWindow foldDegree lambdaNum lambdaDen entropy prefixBits ∨
    UpperIdentityWindow lambdaNum lambdaDen entropy prefixBits

/-- The strict band between the two window edges. -/
def IdentityFailureBand
    (foldDegree lambdaNum lambdaDen entropy prefixBits : Nat) : Prop :=
  entropy * ((foldDegree - 1) * lambdaDen) <
      prefixBits * (foldDegree * lambdaDen - lambdaNum) ∧
    prefixBits * lambdaNum < entropy * lambdaDen

/-- The cleared identity windows and strict failure band are exact complements. -/
theorem identityWindow_iff_not_failureBand
    (foldDegree lambdaNum lambdaDen entropy prefixBits : Nat) :
    IdentityDominanceWindow foldDegree lambdaNum lambdaDen entropy prefixBits ↔
      ¬IdentityFailureBand foldDegree lambdaNum lambdaDen entropy prefixBits := by
  unfold IdentityDominanceWindow LowerIdentityWindow UpperIdentityWindow
    IdentityFailureBand
  omega

/-- Every parameter point lies in the window union or in its strict failure
band. -/
theorem identityWindow_or_failureBand
    (foldDegree lambdaNum lambdaDen entropy prefixBits : Nat) :
    IdentityDominanceWindow foldDegree lambdaNum lambdaDen entropy prefixBits ∨
      IdentityFailureBand foldDegree lambdaNum lambdaDen entropy prefixBits := by
  by_cases h : IdentityFailureBand foldDegree lambdaNum lambdaDen entropy prefixBits
  · exact Or.inr h
  · exact Or.inl ((identityWindow_iff_not_failureBand foldDegree lambdaNum lambdaDen
      entropy prefixBits).mpr h)

/-- No field drop (`lambda=1`) makes the identity criterion global: the lower
window covers `s≤h` and the upper window covers `h≤s`. -/
theorem noFieldDrop_identityWindow
    (foldDegree lambdaDen entropy prefixBits : Nat) :
    IdentityDominanceWindow foldDegree lambdaDen lambdaDen entropy prefixBits := by
  unfold IdentityDominanceWindow LowerIdentityWindow UpperIdentityWindow
  rcases Nat.le_total prefixBits entropy with hle | hle
  · left
    have hedge : foldDegree * lambdaDen - lambdaDen =
        (foldDegree - 1) * lambdaDen := by
      rw [Nat.sub_mul]
      simp
    rw [hedge]
    exact Nat.mul_le_mul_right ((foldDegree - 1) * lambdaDen) hle
  · right
    exact Nat.mul_le_mul_right lambdaDen hle

/-- With a strict field drop and positive entropy, the zero-target crossing
`s=h` lies strictly inside the failure band for every folding degree at least
`2`. -/
theorem fieldDrop_crossing_failureBand
    (foldDegree lambdaNum lambdaDen entropy : Nat)
    (hfold : 2 ≤ foldDegree) (hdrop : lambdaNum < lambdaDen)
    (hentropy : 0 < entropy) :
    IdentityFailureBand foldDegree lambdaNum lambdaDen entropy entropy := by
  unfold IdentityFailureBand
  have hdegree : 1 ≤ foldDegree := Nat.le_trans (by decide) hfold
  have hvle : lambdaDen ≤ foldDegree * lambdaDen := by
    simpa using Nat.mul_le_mul_right lambdaDen hdegree
  have hedge : foldDegree * lambdaDen - lambdaDen =
      (foldDegree - 1) * lambdaDen := by
    rw [Nat.sub_mul]
    simp
  have hstrict : (foldDegree - 1) * lambdaDen <
      foldDegree * lambdaDen - lambdaNum := by
    omega
  constructor
  · exact Nat.mul_lt_mul_of_pos_left hstrict hentropy
  · exact Nat.mul_lt_mul_of_pos_left hdrop hentropy

/-- Hence the zero-target crossing is not identity-dominant on a field-drop
row. -/
theorem fieldDrop_crossing_not_identityWindow
    (foldDegree lambdaNum lambdaDen entropy : Nat)
    (hfold : 2 ≤ foldDegree) (hdrop : lambdaNum < lambdaDen)
    (hentropy : 0 < entropy) :
    ¬IdentityDominanceWindow foldDegree lambdaNum lambdaDen entropy entropy := by
  intro hwindow
  exact ((identityWindow_iff_not_failureBand foldDegree lambdaNum lambdaDen entropy
      entropy).mp hwindow)
    (fieldDrop_crossing_failureBand foldDegree lambdaNum lambdaDen entropy
      hfold hdrop hentropy)

/-- A target crossing that satisfies the lower edge is in the identity window.
The analytic task of locating that crossing is an explicit premise. -/
theorem targetCrossing_in_identityWindow_of_lower
    (foldDegree lambdaNum lambdaDen entropy prefixBits : Nat)
    (hlower : LowerIdentityWindow foldDegree lambdaNum lambdaDen entropy
      prefixBits) :
    IdentityDominanceWindow foldDegree lambdaNum lambdaDen entropy prefixBits :=
  Or.inl hlower

/-! ## Exact smoke tests -/

theorem twoGap_toy : FullImageCertificate 20 120 6 :=
  fullImage_of_two_gap_certificates 20 40 120 2 3 (by decide) (by decide)

theorem noFieldDrop_toy :
    IdentityDominanceWindow 2 7 7 11 13 :=
  noFieldDrop_identityWindow 2 7 11 13

theorem fieldDrop_crossing_toy :
    IdentityFailureBand 2 1 2 10 10 :=
  fieldDrop_crossing_failureBand 2 1 2 10 (by decide) (by decide) (by decide)

#print axioms fullImage_of_two_gap_certificates
#print axioms fullImage_implies_effective_certificate
#print axioms shallow_ambient_to_fullImage
#print axioms ambientFlatness_certifies_fullImage
#print axioms effectivePayment_certifies_gapOne
#print axioms identityWindow_iff_not_failureBand
#print axioms identityWindow_or_failureBand
#print axioms noFieldDrop_identityWindow
#print axioms fieldDrop_crossing_failureBand
#print axioms fieldDrop_crossing_not_identityWindow
#print axioms targetCrossing_in_identityWindow_of_lower

end AsymptoticSpine
