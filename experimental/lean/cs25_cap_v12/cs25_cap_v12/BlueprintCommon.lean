import cs25_cap_v12.TheoremA

/-!
# Common scaffolding for the blueprint / skeleton files

This file collects a few reusable notions that the *blueprint* files
(`Fiber`, `QuotientRemainder`, `QuotientLedgers`, `AperiodicHankel`, `CircleCode`,
`ECFFT`, `InterleavingTransfer`) share.  Those files state — as skeletons with
`sorry` — the results of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*,

that were not yet formalized in the main development (`Main.lean`, `TheoremA.lean`,
`MainCap.lean`, …).  They are deliberately kept independent and reusable so that
each headline statement can be discharged later on its own.

The central shared notion is `RSCap.HasList C δ U L`: a received word `U` carries a
"decoding list" of at least `L` pairwise-distinct codewords of `C`, each within
relative distance `δ`.  This is the paper's `|Lst(C, δ, U)| ≥ L`, and it is exactly
the input consumed by the deep-list floor (`RSCap.ecaFloor_le_ecaErr_deep_list`,
Theorem A) and by the universal-cap reduction (`RSCap.universal_cap_of_fiber_list`).
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- `HasList C δ U L`: the received word `U` admits a decoding list of at least `L`
pairwise-distinct codewords of `C`, each within relative Hamming distance `δ`.
This is the paper's list-size lower bound `|Lst(C, δ, U)| ≥ L`. -/
def HasList (C : Set (ι → F)) (δ : ℝ) (U : ι → F) (L : ℕ) : Prop :=
  ∃ P : Fin L → (ι → F),
    (∀ i, P i ∈ C) ∧ Function.Injective P ∧ (∀ i, relDist U (P i) ≤ δ)

omit [Field F] [Fintype F] in
/-- Monotonicity of `HasList` in the list length: a length-`L` list contains a
length-`L'` sublist for any `L' ≤ L`. -/
theorem HasList.mono {C : Set (ι → F)} {δ : ℝ} {U : ι → F} {L L' : ℕ}
    (hLL : L' ≤ L) (h : HasList C δ U L) : HasList C δ U L' := by
  obtain ⟨P, hmem, hinj, hclose⟩ := h
  refine ⟨fun i => P ⟨i, lt_of_lt_of_le i.2 hLL⟩, ?_, ?_, ?_⟩
  · intro i; exact hmem _
  · intro i j hij
    have : (⟨i, lt_of_lt_of_le i.2 hLL⟩ : Fin L) = ⟨j, lt_of_lt_of_le j.2 hLL⟩ := hinj hij
    exact Fin.ext (by simpa using congrArg Fin.val this)
  · intro i; exact hclose _

omit [Field F] [Fintype F] in
/-- Monotonicity of `HasList` in the radius: enlarging `δ` keeps every list. -/
theorem HasList.mono_radius {C : Set (ι → F)} {δ δ' : ℝ} {U : ι → F} {L : ℕ}
    (hδ : δ ≤ δ') (h : HasList C δ U L) : HasList C δ' U L := by
  obtain ⟨P, hmem, hinj, hclose⟩ := h
  exact ⟨P, hmem, hinj, fun i => le_trans (hclose i) hδ⟩

/-- A domain map `dom : ι → F` is `(φ, a)`-smooth if every fiber of the composite
`φ ∘ dom` (as a subset of the index set) has exactly `a` elements.  This is the
paper's notion of a `(φ, a)`-smooth evaluation domain (`def:map-smooth`,
`def:rational-smooth`), transported to the index type. -/
def DomSmooth (dom : ι → F) (φ : F → F) (a : ℕ) : Prop :=
  ∀ i : ι, (Finset.univ.filter (fun j => φ (dom j) = φ (dom i))).card = a

/-- The `s`-fold interleaved code `C^{≡s}` as a code over the index type `ι × Fin s`:
a word is a codeword iff each of its `s` rows lies in `C`.  Because `ecaErr` /
`emcaErr` are generic in the index type, the paper's interleaving-transfer statement
(`lem:inter`) can be phrased directly with this code. -/
def interleave (C : Set (ι → F)) (s : ℕ) : Set (ι × Fin s → F) :=
  {w | ∀ t : Fin s, (fun i => w (i, t)) ∈ C}

end RSCap
