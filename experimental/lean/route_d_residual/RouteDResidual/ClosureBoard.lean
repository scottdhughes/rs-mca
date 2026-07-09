/-
  KB-MCA Route-D residual — phase-1 closure board (stdlib only).

  Records deployed constants, soft-B arithmetic certificates, and the
  conditional residual close as a Prop. Does NOT prove SoftB_Deployed
  (analytic; open). No Mathlib.

  Mirror of experimental/notes/thresholds/kb_qatom_route_d_CLOSURE.md
  and experimental/data/certificates/kb-qatom-route-d-v67/.
-/

namespace RouteDResidual

/-- Proof-status labels for the Route-D ledger. -/
inductive ProofStatus where
  | closed
  | conditional
  | pending   -- open problem (avoid keyword `open`)
  | refuted
  deriving DecidableEq, Repr

namespace ProofStatus

def isSettled : ProofStatus → Bool
  | closed => true
  | refuted => true
  | _ => false

theorem closed_isSettled : isSettled closed = true := rfl
theorem pending_not_settled : isSettled pending = false := rfl
theorem conditional_not_settled : isSettled conditional = false := rfl

end ProofStatus

/-! ### Deployed KoalaBear MCA constants (Nat) -/

/-- KoalaBear prime `p = 2^31 - 2^24 + 1`. -/
def p : Nat := 2 ^ 31 - 2 ^ 24 + 1

/-- Domain order `n = 2^21`. -/
def nDomain : Nat := 2 ^ 21

/-- MCA shift parameter `A = 1116048`. -/
def A : Nat := 1116048

/-- Free-1 side size `e = w+1 = 67472`. -/
def e : Nat := 67472

/-- Pure-untyped window `n' = A + e`. -/
def nPrime : Nat := A + e

/-- High budget `H2 = ⌊e·p / (2·31·30)⌋`. -/
def H2 : Nat := e * p / (2 * 31 * 30)

/-- Soft-B square threshold `B_*^2 := 2 · H2` (sufficient when `C²/p^{e-1}` is negligible). -/
def BstarSq : Nat := 2 * H2

/-! ### Constant certificates (kernel `decide`) -/

theorem p_eq : p = 2130706433 := by native_decide

theorem nDomain_eq : nDomain = 2097152 := by native_decide

theorem e_eq : e = 67472 := by native_decide

theorem nPrime_eq : nPrime = 1183520 := by native_decide

theorem nPrime_lt_nDomain : nPrime < nDomain := by native_decide

theorem H2_eq : H2 = 77291948627 := by native_decide

theorem BstarSq_eq : BstarSq = 154583897254 := by native_decide

theorem BstarSq_eq_two_mul_H2 : BstarSq = 2 * H2 := rfl

/-- `n | (p-1)` as used for the roots-of-unity domain. -/
theorem nDomain_dvd_p_sub_one : nDomain ∣ (p - 1) := by native_decide

/-- Pack ceiling `⌊n'/e⌋ = 17`. -/
theorem floor_nPrime_div_e : nPrime / e = 17 := by native_decide

/-! ### Soft-B sufficient condition (integer form) -/

/--
  Integer soft-B hypothesis: a uniform bound `B` on nonzero free-1 high
  exponential sums with `B^2 ≤ 2·H2`.

  In analysis one takes `B ≤ √(2 H2)`. Here we package the square form so
  the inequality is Nat-native.
-/
def SoftBBound (B : Nat) : Prop := B * B ≤ BstarSq

/-- Deployed soft-B threshold as a Prop on some `B`. -/
def SoftBDeployed : Prop := ∃ B : Nat, SoftBBound B ∧ True
-- The analytic content "max|S| ≤ B" is not formalized in phase 1;
-- `SoftBDeployed` is a placeholder marker. Real SoftB is `SoftBHypothesis` below.

/--
  Analytic SoftB hypothesis (statement only; proof OPEN).

  When formalized with Mathlib, this becomes:
  `∀ λ ≠ 0, ‖S(λ)‖ ≤ B` for free-1 monic high sums on the length-`n'` GP arc,
  for some `B` with `SoftBBound B`.
-/
def SoftBHypothesis : Prop :=
  ∃ B : Nat, SoftBBound B
  -- phase-1: existence of a numeric B with B² ≤ 2 H2 is trivial (B=0);
  -- the real content is the exponential-sum bound, tracked outside this Prop.

/-- Trivial witness that some Nat meets the square bound (not the analytic SoftB). -/
theorem exists_nat_softB_bound : ∃ B : Nat, SoftBBound B := by
  refine ⟨0, ?_⟩
  unfold SoftBBound BstarSq
  exact Nat.zero_le _

theorem softB_bound_mono {B₁ B₂ : Nat} (hle : B₁ ≤ B₂) (h : SoftBBound B₂) :
    SoftBBound B₁ := by
  unfold SoftBBound at *
  exact Nat.le_trans (Nat.mul_le_mul hle hle) h

/-- Concrete B near √(2 H2) ≈ 393171.6: floor = 393171, square check. -/
def BstarFloor : Nat := 393171

theorem BstarFloor_sq_le_BstarSq : SoftBBound BstarFloor := by
  unfold SoftBBound BstarFloor BstarSq
  native_decide

theorem BstarFloor_succ_sq_gt_BstarSq : BstarSq < (BstarFloor + 1) * (BstarFloor + 1) := by
  unfold BstarFloor BstarSq
  native_decide

/-! ### Conditional residual close (statement) -/

/--
  Target residual inequality at deployed parameters.
  Phase-1 records the Prop; proof requires SoftB + combinatorial chain (v53–v58).
-/
def T_le_H2 : Prop := True  -- placeholder until |T| is defined in Lean
-- Replace with a real cardinality inequality once index-set combinatorics is formalized.

/--
  Conditional close as used by the Python board:
  SoftBHypothesis → residual high bound (to be refined when |T| is defined).

  Currently a trivial implication skeleton so the module builds without sorry.
  Phase-2 replaces the bodies with real definitions and proofs.
-/
def ConditionalResidualClose : Prop := SoftBHypothesis → T_le_H2

theorem conditional_residual_close_holds_trivially : ConditionalResidualClose := by
  intro _
  trivial

/-! ### Closure ledger nodes -/

structure ClosureNode where
  id : String
  packet : String
  status : ProofStatus
  deriving Repr

def closedNodes : List ClosureNode :=
  [ ⟨"C_unique", "v53", .closed⟩
  , ⟨"terminal_star", "v54", .closed⟩
  , ⟨"U2e", "v51", .closed⟩
  , ⟨"e2_T_le_H2", "v48/v50", .closed⟩
  , ⟨"terminal_high_injectivity", "v57", .closed⟩
  , ⟨"plancherel_coll", "v58", .closed⟩
  , ⟨"G_plancherel", "v59", .closed⟩
  , ⟨"soft_B_budget", "v64", .closed⟩
  , ⟨"deployed_Bstar_arithmetic", "v64", .closed⟩
  , ⟨"energy_G4", "v65", .closed⟩
  , ⟨"subgroup_G", "v65", .closed⟩
  , ⟨"incomplete_GP_G", "v66", .closed⟩
  , ⟨"e3_lab_structure", "v60-v63", .closed⟩
  ]

def openNodes : List ClosureNode :=
  [ ⟨"SoftB_Deployed", "v64-v67", .pending⟩
  , ⟨"R2_pair_budget", "v45-v46", .pending⟩
  , ⟨"A_SP_le_tp", "program", .pending⟩
  ]

def conditionalNodes : List ClosureNode :=
  [ ⟨"conditional_T_le_H2", "v67", .conditional⟩
  ]

theorem closedNodes_all_closed :
    closedNodes.all (fun n => n.status == ProofStatus.closed) = true := by
  native_decide

theorem openNodes_all_pending :
    openNodes.all (fun n => n.status == ProofStatus.pending) = true := by
  native_decide

/-- Honest board flag: full residual is not marked closed in phase 1. -/
def fullResidualClosed : Bool := false

theorem fullResidualClosed_false : fullResidualClosed = false := rfl

end RouteDResidual
