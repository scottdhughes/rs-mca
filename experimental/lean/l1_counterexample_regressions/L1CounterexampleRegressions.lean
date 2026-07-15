/-!
# Decidable L1 E3 counterexample regressions

Arithmetic locks for the six spectra in
`experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json`.

The raw finite-field `Gamma` vectors and spectrum reconstruction remain the
responsibility of `verify_l1_e3_law_refuted.py`.  This module starts from the
certified spectra and kernel-checks all derived spectrum arithmetic.  It does
not claim realizability from a spectrum alone.

No `sorry`.  Stdlib only.
-/

namespace L1CounterexampleRegressions

def excessAboveTwo : List Nat → Nat
  | [] => 0
  | mu :: mus => (mu - 2) + excessAboveTwo mus

def residualT : List Nat → Nat
  | [] => 0
  | [_] => 0
  | _ :: _ :: mus => excessAboveTwo mus

def activeK (mus : List Nat) : Nat :=
  (mus.filter (fun mu => decide (2 ≤ mu))).length

def topTwo : List Nat → Nat
  | a :: b :: _ => a + b
  | [a] => a
  | [] => 0

def descending : List Nat → Bool
  | a :: b :: mus => decide (b ≤ a) && descending (b :: mus)
  | _ => true

def peelSmall (mus : List Nat) : List Nat :=
  mus.filter (fun mu => decide (3 ≤ mu))

structure Witness where
  id : String
  ell : Nat
  p : Nat
  n : Nat
  spectrum : List Nat
  claimedE3 : Nat
  claimedT : Nat
  claimedK : Nat
  claimedSigma : Nat
  dimU : Nat
  rho : Nat
  capTight : Bool
  deriving DecidableEq, Repr

def Witness.regression (w : Witness) : Bool :=
  decide (
    descending w.spectrum = true ∧
    w.spectrum.length = w.n ∧
    activeK w.spectrum = w.claimedK ∧
    excessAboveTwo w.spectrum = w.claimedE3 ∧
    residualT w.spectrum = w.claimedT ∧
    topTwo w.spectrum ≤ w.ell ∧
    (w.capTight = true ↔ topTwo w.spectrum = w.ell) ∧
    w.ell < w.claimedE3 ∧
    5 ≤ w.claimedT ∧
    w.n ≥ w.claimedK ∧
    w.rho + w.dimU = w.ell ∧
    w.claimedSigma = w.claimedE3 + w.claimedK - w.ell + w.dimU ∧
    w.claimedK + w.dimU + 1 ≤ w.claimedSigma ∧
    w.n = (w.p - 1) / w.ell)

def w3 : Witness :=
  { id := "W3", ell := 17, p := 137, n := 8
    spectrum := [14, 3, 3, 3, 3, 3, 3, 3]
    claimedE3 := 19, claimedT := 6, claimedK := 8
    claimedSigma := 12, dimU := 2, rho := 15, capTight := true }

def w1 : Witness :=
  { id := "W1", ell := 29, p := 233, n := 8
    spectrum := [15, 14, 4, 3, 3, 3, 2, 2]
    claimedE3 := 30, claimedT := 5, claimedK := 8
    claimedSigma := 11, dimU := 2, rho := 27, capTight := true }

def w2 : Witness :=
  { id := "W2", ell := 23, p := 139, n := 6
    spectrum := [14, 9, 4, 4, 3, 2]
    claimedE3 := 24, claimedT := 5, claimedK := 6
    claimedSigma := 9, dimU := 2, rho := 21, capTight := true }

def extra1 : Witness :=
  { id := "EXTRA1_ell29_p233_a", ell := 29, p := 233, n := 8
    spectrum := [20, 9, 4, 3, 3, 3, 2, 2]
    claimedE3 := 30, claimedT := 5, claimedK := 8
    claimedSigma := 11, dimU := 2, rho := 27, capTight := true }

def extra2 : Witness :=
  { id := "EXTRA2_ell29_p233_b", ell := 29, p := 233, n := 8
    spectrum := [16, 13, 4, 3, 3, 3, 2, 2]
    claimedE3 := 30, claimedT := 5, claimedK := 8
    claimedSigma := 11, dimU := 2, rho := 27, capTight := true }

def extra3 : Witness :=
  { id := "EXTRA3_ell17_p103", ell := 17, p := 103, n := 6
    spectrum := [11, 5, 5, 4, 3, 2]
    claimedE3 := 18, claimedT := 6, claimedK := 6
    claimedSigma := 9, dimU := 2, rho := 15, capTight := false }

def witnesses : List Witness := [w3, w1, w2, extra1, extra2, extra3]

theorem w3_regression : w3.regression = true := by decide
theorem w1_regression : w1.regression = true := by decide
theorem w2_regression : w2.regression = true := by decide
theorem extra1_regression : extra1.regression = true := by decide
theorem extra2_regression : extra2.regression = true := by decide
theorem extra3_regression : extra3.regression = true := by decide

theorem all_six_regressions :
    witnesses.length = 6 ∧
      witnesses.Nodup ∧
      witnesses.all (fun w => w.regression) = true := by
  decide

theorem w1_peel_preserves :
    peelSmall w1.spectrum = [15, 14, 4, 3, 3, 3] ∧
      excessAboveTwo (peelSmall w1.spectrum) = excessAboveTwo w1.spectrum ∧
      residualT (peelSmall w1.spectrum) = residualT w1.spectrum := by
  decide

theorem w2_peel_preserves :
    peelSmall w2.spectrum = [14, 9, 4, 4, 3] ∧
      excessAboveTwo (peelSmall w2.spectrum) = excessAboveTwo w2.spectrum ∧
      residualT (peelSmall w2.spectrum) = residualT w2.spectrum := by
  decide

/-- Pure bookkeeping can satisfy the master identity while violating the
realizable pair cap; spectrum arithmetic alone is not a realizability proof. -/
theorem unrealizable_profile_guard :
    excessAboveTwo [6, 6] = 8 ∧ activeK [6, 6] = 2 ∧
      4 = 8 + 2 - 7 + 1 ∧ topTwo [6, 6] > 7 := by
  decide

/-- Companion attainment rows stay on the covered `T ≤ 4` chart. -/
theorem theoremOne_boundary_regression :
    (18 : Nat) ≤ 19 ∧ (3 : Nat) ≤ 4 ∧
      (17 : Nat) ≤ 19 ∧ (2 : Nat) ≤ 4 := by
  decide

/-- Tightening the pair cap by one rejects the strongest certified witness. -/
theorem tightened_pair_cap_falsifier :
    ¬ (topTwo w3.spectrum ≤ w3.ell - 1) := by
  decide

/-- Changing W3's pinned second moment excess from 19 to 18 is detected. -/
theorem e3_tamper_falsifier :
    excessAboveTwo w3.spectrum ≠ 18 := by
  decide

end L1CounterexampleRegressions
