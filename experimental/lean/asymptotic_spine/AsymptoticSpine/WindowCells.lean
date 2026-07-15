import AsymptoticSpine.Window
import AsymptoticSpine.FirstMatch

namespace AsymptoticSpine

/-!
# C1--C8 window aggregation and activation handoff

This module completes the finite arithmetic layer of the B3 window-uniformity
audit.  `Window.lean` proves the single-cell Lemma-W/Lemma-B discharge.  Here
that result is:

* aggregated over the named finite family C1--C8;
* combined at the `LittleO` rate level for any finite list of cell rates;
* composed with the first-match budget bound across an activation threshold;
* accompanied by an exact slope-conserving handoff and a falsifier showing that
  an uncovered activation changes the paid count.

The source-specific facts that the C1--C8 formulas satisfy their local ratio
bounds remain explicit `WindowPayment` data.  Stirling/MVT bounds, frontier
interiority, C9 routing, and the primitive-Q atom are not asserted here.
-/

inductive EstablishedCell where
  | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8
  deriving DecidableEq, Repr

def establishedCells : List EstablishedCell :=
  [.c1, .c2, .c3, .c4, .c5, .c6, .c7, .c8]

theorem establishedCells_length : establishedCells.length = 8 := by decide
theorem establishedCells_nodup : establishedCells.Nodup := by decide

structure WindowPayment (barCenter : Nat) where
  atWindow : Nat
  atCenter : Nat
  ratio : Nat
  payment : Nat
  slide : atWindow ≤ ratio * atCenter
  centerPaid : atCenter ≤ payment * barCenter

def WindowPayment.multiplier {barCenter : Nat}
    (cert : WindowPayment barCenter) (referenceRatio : Nat) : Nat :=
  cert.ratio * cert.payment * referenceRatio

theorem WindowPayment.windowPaid {barAt barCenter referenceRatio : Nat}
    (cert : WindowPayment barCenter)
    (hreference : barCenter ≤ referenceRatio * barAt) :
    cert.atWindow ≤ cert.multiplier referenceRatio * barAt := by
  have h := discharge_principle cert.atWindow cert.atCenter barAt barCenter
    cert.ratio cert.payment referenceRatio cert.slide cert.centerPaid hreference
  simpa [WindowPayment.multiplier, Nat.mul_assoc] using h

theorem finiteFamily_windowPaid {α : Type}
    (barAt barCenter referenceRatio : Nat)
    (cert : α → WindowPayment barCenter)
    (hreference : barCenter ≤ referenceRatio * barAt) :
    ∀ cells : List α,
      listSum (cells.map (fun c => (cert c).atWindow))
        ≤ listSum (cells.map (fun c => (cert c).multiplier referenceRatio)) * barAt := by
  intro cells
  induction cells with
  | nil => simp
  | cons c cells ih =>
      have hc := (cert c).windowPaid hreference
      simpa only [List.map_cons, listSum_cons, Nat.add_mul] using
        Nat.add_le_add hc ih

theorem c1_c8_windowPaid
    (barAt barCenter referenceRatio : Nat)
    (cert : EstablishedCell → WindowPayment barCenter)
    (hreference : barCenter ≤ referenceRatio * barAt) :
    listSum (establishedCells.map (fun c => (cert c).atWindow))
      ≤ listSum (establishedCells.map
          (fun c => (cert c).multiplier referenceRatio)) * barAt :=
  finiteFamily_windowPaid barAt barCenter referenceRatio cert hreference establishedCells

theorem littleO_listSum :
    ∀ rates : List (Nat → Nat),
      (∀ rate ∈ rates, LittleO rate) →
      LittleO (fun n => listSum (rates.map (fun rate => rate n))) := by
  intro rates
  induction rates with
  | nil =>
      intro _
      unfold LittleO
      intro K
      exact ⟨0, fun n hn => by simp⟩
  | cons rate rates ih =>
      intro h
      have hr : LittleO rate := h rate List.mem_cons_self
      have hrs : ∀ f ∈ rates, LittleO f :=
        fun f hf => h f (List.mem_cons_of_mem rate hf)
      have ht := ih hrs
      simpa only [List.map_cons, listSum_cons] using
        littleO_add rate
          (fun n => listSum (rates.map (fun tailRate => tailRate n))) hr ht

theorem c1_c8_rates_littleO
    (rate : EstablishedCell → Nat → Nat)
    (h : ∀ cell ∈ establishedCells, LittleO (rate cell)) :
    LittleO (fun n =>
      listSum (establishedCells.map (fun cell => rate cell n))) := by
  have hall : ∀ f ∈ establishedCells.map rate, LittleO f := by
    intro f hf
    rcases List.mem_map.mp hf with ⟨cell, hcell, rfl⟩
    exact h cell hcell
  have hs := littleO_listSum (establishedCells.map rate) hall
  simpa only [List.map_map, Function.comp_def] using hs

def assignedCount (leaves : List (List Nat)) : Nat :=
  leaves.flatten.length

def activationBefore (moved left right : List Nat) : List (List Nat) :=
  [moved ++ left, right]

def activationAfter (moved left right : List Nat) : List (List Nat) :=
  [left, moved ++ right]

theorem activation_flatten_perm (moved left right : List Nat) :
    (activationBefore moved left right).flatten.Perm
      (activationAfter moved left right).flatten := by
  simp only [activationBefore, activationAfter, List.flatten_cons,
    List.flatten_nil, List.append_nil]
  simpa only [List.append_assoc] using
    (List.perm_append_comm (l₁ := moved) (l₂ := left)).append_right right

theorem activation_handoff_preserves_assignedCount
    (moved left right : List Nat) :
    assignedCount (activationBefore moved left right) =
      assignedCount (activationAfter moved left right) := by
  exact (activation_flatten_perm moved left right).length_eq

theorem activation_handoff_preserves_budgetSum
    (moved left right : List Nat) :
    listSum ((activationBefore moved left right).map List.length) =
      listSum ((activationAfter moved left right).map List.length) := by
  rw [← length_flatten, ← length_flatten]
  exact activation_handoff_preserves_assignedCount moved left right

theorem firstMatch_handoff_common_cap
    (cellsBefore cellsAfter : List (List Nat))
    (budgetBefore budgetAfter : List Nat)
    (hlenBefore : cellsBefore.length ≤ budgetBefore.length)
    (hcapBefore :
      ∀ p ∈ (cellsBefore.map List.length).zip budgetBefore, p.1 ≤ p.2)
    (hlenAfter : cellsAfter.length ≤ budgetAfter.length)
    (hcapAfter :
      ∀ p ∈ (cellsAfter.map List.length).zip budgetAfter, p.1 ≤ p.2)
    (hconserve : listSum budgetBefore = listSum budgetAfter) :
    firstMatchCount cellsBefore ≤ listSum budgetBefore ∧
      firstMatchCount cellsAfter ≤ listSum budgetBefore := by
  constructor
  · exact firstMatch_le_sum_budgets cellsBefore budgetBefore
      hlenBefore hcapBefore
  · have h := firstMatch_le_sum_budgets cellsAfter budgetAfter
      hlenAfter hcapAfter
    rw [← hconserve] at h
    exact h

theorem activation_handoff_example :
    assignedCount (activationBefore [1, 2] [3, 4] [5, 6]) =
        assignedCount (activationAfter [1, 2] [3, 4] [5, 6])
      ∧ assignedCount (activationBefore [1, 2] [3, 4] [5, 6]) = 6 := by
  constructor
  · exact activation_handoff_preserves_assignedCount [1, 2] [3, 4] [5, 6]
  · decide

theorem uncovered_activation_falsifier :
    assignedCount [[1, 2], [3]] = 3 ∧
      assignedCount [[1, 2], [3, 4]] = 4 ∧
      assignedCount [[1, 2], [3]] ≠ assignedCount [[1, 2], [3, 4]] := by
  decide

end AsymptoticSpine
