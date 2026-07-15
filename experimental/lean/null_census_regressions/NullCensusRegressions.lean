import Std.Tactic

/-!
# Championship and corridor null-census guards

Denominator-cleared arithmetic locks for the computed rows in
`championship_census_b19_26.md` and `corridor_interior_hunt.md`.

These theorems say only that the stored exact `(b,f,L)` rows remain below the
named thresholds. They do not turn a time-boxed or subclass-exhaustive search
into a global nonexistence theorem.

No `sorry`. Stdlib only.
-/

namespace NullCensusRegressions

structure CensusRow where
  b : Nat
  fstar : Nat
  image : Nat
  deriving DecidableEq, Repr

def CensusRow.product (r : CensusRow) : Nat := r.fstar * r.image

def champion : CensusRow := ⟨18, 30, 151275⟩

/-- Cleared comparison of rates:
`(fL)^(1/b) < (fChamp LChamp)^(1/18)`. -/
def belowChampion (r : CensusRow) : Bool :=
  decide (
    r.product ^ champion.b < champion.product ^ r.b)

/-- Cleared corridor threshold `(fL)^(1/b) < 2^(4/3)`. -/
def belowCorridor (r : CensusRow) : Bool :=
  decide (
    r.product ^ 3 < 2 ^ (4 * r.b))

def championshipRows : List CensusRow :=
  [⟨19, 35, 231262⟩, ⟨20, 36, 508381⟩, ⟨21, 46, 736714⟩,
   ⟨22, 96, 1056451⟩, ⟨23, 66, 2405852⟩, ⟨24, 104, 3727586⟩,
   ⟨25, 133, 4997920⟩, ⟨26, 266, 6181859⟩]

def corridorRows : List CensusRow :=
  [⟨20, 30, 605100⟩, ⟨19, 32, 250614⟩, ⟨20, 38, 372969⟩,
   ⟨21, 49, 511034⟩,
   ⟨20, 40, 474533⟩, ⟨20, 40, 473763⟩, ⟨20, 98, 110627⟩,
   ⟨18, 34, 75413⟩, ⟨24, 442, 561409⟩,
   ⟨10, 3, 980⟩, ⟨10, 3, 737⟩,
   ⟨16, 37, 5811⟩, ⟨20, 253, 12719⟩, ⟨22, 776, 16647⟩,
   ⟨20, 30, 573373⟩]

def allBelowChampion (rows : List CensusRow) : Bool :=
  rows.all belowChampion

def allBelowCorridor (rows : List CensusRow) : Bool :=
  rows.all belowCorridor

theorem championship_null_guard :
    championshipRows.length = 8 ∧ championshipRows.Nodup ∧
      allBelowChampion championshipRows = true := by
  native_decide

theorem championship_rows_below_corridor :
    allBelowCorridor championshipRows = true := by
  native_decide

theorem corridor_hunt_null_guard :
    corridorRows.length = 15 ∧ corridorRows.Nodup ∧
      allBelowCorridor corridorRows = true ∧
      allBelowChampion corridorRows = true := by
  native_decide

/-- The record row cannot satisfy the strict "below record" predicate. -/
theorem strict_champion_falsifier : belowChampion champion = false := by
  native_decide

/-- A row on the corridor wall is rejected by the strict null predicate. -/
theorem corridor_wall_falsifier :
    belowCorridor ⟨3, 1, 16⟩ = false := by
  native_decide

/-- Raising the b=19 stored product far enough trips the championship guard. -/
theorem corrupted_championship_falsifier :
    belowChampion ⟨19, 100, 231262⟩ = false := by
  native_decide

end NullCensusRegressions
