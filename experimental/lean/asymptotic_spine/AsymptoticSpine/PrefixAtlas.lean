import AsymptoticSpine.Averaging
import AsymptoticSpine.FirstMatch

namespace AsymptoticSpine

/-!
# Prefix-fibre atlas totality

This file formalizes the unconditional coverage statement in the proved
prefix-fibre discharge of experimental/notes/thresholds/atlas_missing_witness.md.
Coverage and payment remain separate: a total key map partitions every witness,
while any numerical payment for the resulting cells is an independent input.

Witnesses are represented by duplicate-free natural-number identifiers, as in
FirstMatch. For the paper application, key is the composition of witness support
with the depth-w boundary-prefix map.
-/

/-- Ordered fibres of items under a total key map, indexed by a list of key
values. Empty fibres are harmless; taking keys to be the image gives precisely
the nonempty prefix-fibre atlas. -/
def fibreAtlas {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) (keys : List β) : List (List α) :=
  keys.map fun z => items.filter fun x => decide (key x = z)

/-- Membership in the flattened fibre atlas is exactly membership in the
original item list, provided the key list contains every realized key. This is
the set-theoretic exhaustiveness step. -/
theorem mem_fibreAtlas_flatten_iff {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) (keys : List β)
    (hcover : ∀ x ∈ items, key x ∈ keys) (x : α) :
    x ∈ (fibreAtlas items key keys).flatten ↔ x ∈ items := by
  constructor
  · intro hx
    rw [List.mem_flatten] at hx
    rcases hx with ⟨cell, hcell, hxcell⟩
    simp only [fibreAtlas] at hcell
    rw [List.mem_map] at hcell
    rcases hcell with ⟨z, hz, rfl⟩
    exact (List.mem_filter.mp hxcell).1
  · intro hx
    rw [List.mem_flatten]
    refine ⟨items.filter (fun y => decide (key y = key x)), ?_, ?_⟩
    · exact List.mem_map.mpr ⟨key x, hcover x hx, rfl⟩
    · exact List.mem_filter.mpr ⟨hx, by simp⟩

/-- Distinct input items placed in distinct indexed fibres remain distinct
after flattening: the fibre atlas is a genuine disjoint partition. -/
theorem nodup_fibreAtlas_flatten {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) :
    ∀ keys : List β, items.Nodup → keys.Nodup →
      (fibreAtlas items key keys).flatten.Nodup := by
  intro keys hitems hkeys
  induction keys with
  | nil => simp [fibreAtlas]
  | cons z zs ih =>
      have hz : z ∉ zs := (List.nodup_cons.mp hkeys).1
      have hzs : zs.Nodup := (List.nodup_cons.mp hkeys).2
      simp only [fibreAtlas, List.map_cons, List.flatten_cons]
      apply List.nodup_append.mpr
      refine ⟨List.filter_sublist.nodup hitems, ih hzs, ?_⟩
      intro a ha b hb hab
      have hka : key a = z :=
        of_decide_eq_true (List.mem_filter.mp ha).2
      rw [List.mem_flatten] at hb
      rcases hb with ⟨cell, hcell, hbcell⟩
      rw [List.mem_map] at hcell
      rcases hcell with ⟨z', hz', rfl⟩
      have hkb : key b = z' :=
        of_decide_eq_true (List.mem_filter.mp hbcell).2
      subst b
      have hzz : z = z' := hka.symm.trans hkb
      exact hz (hzz.symm ▸ hz')

/-- The number of fibre cells is the number of supplied profile keys. -/
theorem fibreAtlas_length {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) (keys : List β) :
    (fibreAtlas items key keys).length = keys.length := by
  simp [fibreAtlas]

/-- Duplicate-free enumeration of the realized keys of a total map. -/
def realizedKeys {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) : List β :=
  match items with
  | [] => []
  | x :: xs =>
      let rest := realizedKeys xs key
      if key x ∈ rest then rest else key x :: rest

/-- The realized-key enumeration has no duplicates. -/
theorem realizedKeys_nodup {α β : Type} [DecidableEq β]
    (key : α → β) : ∀ items : List α, (realizedKeys items key).Nodup := by
  intro items
  induction items with
  | nil => simp [realizedKeys]
  | cons x xs ih =>
      simp only [realizedKeys]
      split
      · exact ih
      · exact List.nodup_cons.mpr ⟨by assumption, ih⟩

/-- A key occurs in the realized-key enumeration exactly when it is the key of
an input item. -/
theorem mem_realizedKeys_iff {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) (z : β) :
    z ∈ realizedKeys items key ↔ z ∈ items.map key := by
  induction items with
  | nil => simp [realizedKeys]
  | cons x xs ih =>
      simp only [realizedKeys, List.map_cons, List.mem_cons]
      split
      next h =>
        constructor
        · intro hz
          exact Or.inr (ih.mp hz)
        · intro hz
          rcases hz with hzx | hzrest
          · subst z
            exact h
          · exact ih.mpr hzrest
      next _ =>
        simp only [List.mem_cons, ih]

/-- A total map realizes no more keys than there are input items. -/
theorem realizedKeys_length_le {α β : Type} [DecidableEq β]
    (key : α → β) : ∀ items : List α,
      (realizedKeys items key).length ≤ items.length := by
  intro items
  induction items with
  | nil => simp [realizedKeys]
  | cons x xs ih =>
      simp only [realizedKeys]
      split
      · simpa only [List.length_cons] using Nat.le_succ_of_le ih
      · simp only [List.length_cons]
        omega

/-- The canonical fibre atlas indexed by exactly the realized keys. -/
def totalFibreAtlas {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) : List (List α) :=
  fibreAtlas items key (realizedKeys items key)

/-- Witness-exhaustive prefix atlas. A duplicate-free key list covering
all realized prefix values yields:

* a disjoint partition of all witnesses;
* exact first-match routing, so no witness falls through the atlas;
* at most P profiles whenever the key list has length at most P.

For the depth-w paper atlas, instantiate key with Phi_w composed with witness
support and P with the ambient prefix-space bound. No payment theorem is used. -/
theorem prefixFibreAtlas_total_of_keys
    {β : Type} [DecidableEq β]
    (witnesses : List Nat) (key : Nat → β) (keys : List β) (P : Nat)
    (hwitnesses : witnesses.Nodup) (hkeys : keys.Nodup)
    (hcover : ∀ w ∈ witnesses, key w ∈ keys)
    (hprofiles : keys.length ≤ P) :
    (fibreAtlas witnesses key keys).flatten.Nodup
      ∧ (∀ w, w ∈ (fibreAtlas witnesses key keys).flatten ↔ w ∈ witnesses)
      ∧ (∀ w, w ∈
          (firstMatchLeaves [] (fibreAtlas witnesses key keys)).flatten ↔
            w ∈ witnesses)
      ∧ (fibreAtlas witnesses key keys).length ≤ P := by
  refine ⟨nodup_fibreAtlas_flatten witnesses key keys hwitnesses hkeys,
    fun w => mem_fibreAtlas_flatten_iff witnesses key keys hcover w, ?_, ?_⟩
  · intro w
    exact (mem_firstMatchLeaves (fibreAtlas witnesses key keys) w).trans
      (mem_fibreAtlas_flatten_iff witnesses key keys hcover w)
  · rw [fibreAtlas_length]
    exact hprofiles

/-- Every cell of the canonical realized-image atlas is nonempty. -/
theorem totalFibreAtlas_cells_nonempty {α β : Type} [DecidableEq β]
    (items : List α) (key : α → β) :
    ∀ cell ∈ totalFibreAtlas items key, cell ≠ [] := by
  intro cell hcell
  simp only [totalFibreAtlas, fibreAtlas] at hcell
  rw [List.mem_map] at hcell
  rcases hcell with ⟨z, hz, rfl⟩
  have hzmap : z ∈ items.map key :=
    (mem_realizedKeys_iff items key z).mp hz
  rw [List.mem_map] at hzmap
  rcases hzmap with ⟨x, hx, hkx⟩
  intro hempty
  have hxcell : x ∈ items.filter (fun y => decide (key y = z)) :=
    List.mem_filter.mpr ⟨hx, by simpa using hkx⟩
  simp [hempty] at hxcell

/-- Source-facing unconditional form: the fibres over the realized image of a
total prefix map form a duplicate-free, witness-exhaustive first-match atlas.
Only the profile-count bound is supplied separately; coverage has no atlas
assumption. -/
theorem prefixFibreAtlas_total
    {β : Type} [DecidableEq β]
    (witnesses : List Nat) (key : Nat → β) (P : Nat)
    (hwitnesses : witnesses.Nodup)
    (hprofiles : (realizedKeys witnesses key).length ≤ P) :
    (totalFibreAtlas witnesses key).flatten.Nodup
      ∧ (∀ w, w ∈ (totalFibreAtlas witnesses key).flatten ↔ w ∈ witnesses)
      ∧ (∀ w, w ∈
          (firstMatchLeaves [] (totalFibreAtlas witnesses key)).flatten ↔
            w ∈ witnesses)
      ∧ (totalFibreAtlas witnesses key).length ≤ P := by
  have hcover : ∀ w ∈ witnesses, key w ∈ realizedKeys witnesses key := by
    intro w hw
    rw [mem_realizedKeys_iff]
    exact List.mem_map.mpr ⟨w, hw, rfl⟩
  simpa [totalFibreAtlas] using
    prefixFibreAtlas_total_of_keys witnesses key (realizedKeys witnesses key) P
      hwitnesses (realizedKeys_nodup key witnesses) hcover hprofiles

#print axioms mem_fibreAtlas_flatten_iff
#print axioms nodup_fibreAtlas_flatten
#print axioms realizedKeys_nodup
#print axioms totalFibreAtlas_cells_nonempty
#print axioms prefixFibreAtlas_total_of_keys
#print axioms prefixFibreAtlas_total

end AsymptoticSpine
