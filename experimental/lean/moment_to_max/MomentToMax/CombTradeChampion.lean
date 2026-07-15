import MomentToMax.PTEClusterPacking

/-!
# Common-shift PTE combs and finite champion comparisons

This module formalizes the proved arithmetic mechanism in
`experimental/notes/thresholds/comb_trade_champion.md` and the finite
comparison interface in `comb_trade_champion_k5.md`.

The six aggregate invariants are encoded in mixed radix by a common shift.
Under explicit cleared separation inequalities, equality of the ordinary
weight/first/second-moment signature is equivalent to equality of all six
aggregates.  The source's square-root threshold is represented by the stronger
and exact denominator-cleared inequalities it is used to prove.

The large histogram values are recorded as computed census rows. Lean checks
all finite rate comparisons from those integers; it does not re-run the
multi-million-key census or promote searched-window maximality.
-/

namespace MomentToMax
namespace CombTradeChampion

open PTEClusterPacking

@[ext]
structure Aggregates where
  weight : Nat
  sizeMoment : Nat
  sizeSquareMoment : Nat
  valueSum : Nat
  mixedMoment : Nat
  valueSquareSum : Nat
deriving DecidableEq, Repr

@[ext]
structure CombSignature where
  weight : Nat
  linear : Nat
  quadratic : Nat
deriving DecidableEq, Repr

structure LocalMoments where
  weight : Nat
  valueSum : Nat
  valueSquareSum : Nat
deriving DecidableEq, Repr

def aggregate {k : Nat} (positions : Fin k → Nat)
    (locals : Fin k → LocalMoments) : Aggregates where
  weight := ∑ i, (locals i).weight
  sizeMoment := ∑ i, positions i * (locals i).weight
  sizeSquareMoment := ∑ i, (positions i) ^ 2 * (locals i).weight
  valueSum := ∑ i, (locals i).valueSum
  mixedMoment := ∑ i, positions i * (locals i).valueSum
  valueSquareSum := ∑ i, (locals i).valueSquareSum

/-- The ordinary moment signature obtained after shifting local block `i` by
`shift * positions i`. -/
def shiftedCombSignature {k : Nat} (shift : Nat)
    (positions : Fin k → Nat) (locals : Fin k → LocalMoments) :
    CombSignature where
  weight := ∑ i, (locals i).weight
  linear := ∑ i, ((shift * positions i) * (locals i).weight +
    (locals i).valueSum)
  quadratic := ∑ i, ((shift * positions i) ^ 2 * (locals i).weight +
    2 * (shift * positions i) * (locals i).valueSum +
    (locals i).valueSquareSum)

def encode (shift : Nat) (a : Aggregates) : CombSignature where
  weight := a.weight
  linear := shift * a.sizeMoment + a.valueSum
  quadratic :=
    shift ^ 2 * a.sizeSquareMoment +
      2 * shift * a.mixedMoment + a.valueSquareSum

/-- Exact expansion into the six aggregate invariants. -/
theorem shiftedCombSignature_eq_encode {k : Nat} (shift : Nat)
    (positions : Fin k → Nat) (locals : Fin k → LocalMoments) :
    shiftedCombSignature shift positions locals =
      encode shift (aggregate positions locals) := by
  ext
  · rfl
  · simp only [shiftedCombSignature, encode, aggregate,
      Finset.sum_add_distrib, Finset.mul_sum]
    ring_nf
  · simp only [shiftedCombSignature, encode, aggregate,
      Finset.sum_add_distrib, Finset.mul_sum]
    ring_nf

structure AggregateBounds (maxB maxD maxE : Nat) (a : Aggregates) : Prop where
  valueSum_le : a.valueSum ≤ maxB
  mixedMoment_le : a.mixedMoment ≤ maxD
  valueSquareSum_le : a.valueSquareSum ≤ maxE

/-- Uniqueness of a quotient/remainder expansion in a positive natural base. -/
theorem base_decomposition_unique
    (base q r q' r' : Nat) (hbase : 0 < base)
    (hr : r < base) (hr' : r' < base)
    (heq : base * q + r = base * q' + r') :
    q = q' ∧ r = r' := by
  have hq := congrArg (fun z : Nat => z / base) heq
  have hqeq : q = q' := by
    simpa only [Nat.mul_add_div hbase, Nat.div_eq_of_lt hr,
      Nat.div_eq_of_lt hr', Nat.add_zero] using hq
  subst q'
  exact ⟨rfl, Nat.add_left_cancel heq⟩

/-- Exact cleared separation conditions for decoding all six aggregates. -/
structure ShiftSeparation (shift maxB maxD maxE : Nat) : Prop where
  shift_pos : 0 < shift
  value_remainder : maxB < shift
  quadratic_remainder : 2 * shift * maxD + maxE < shift ^ 2
  square_remainder : maxE < 2 * shift

theorem encode_injective_on_bounds
    (shift maxB maxD maxE : Nat)
    (hsep : ShiftSeparation shift maxB maxD maxE)
    {a a' : Aggregates}
    (ha : AggregateBounds maxB maxD maxE a)
    (ha' : AggregateBounds maxB maxD maxE a')
    (hencode : encode shift a = encode shift a') :
    a = a' := by
  have hw : a.weight = a'.weight :=
    congrArg CombSignature.weight hencode
  have hlinear : shift * a.sizeMoment + a.valueSum =
      shift * a'.sizeMoment + a'.valueSum :=
    congrArg CombSignature.linear hencode
  have hb : a.valueSum < shift :=
    Nat.lt_of_le_of_lt ha.valueSum_le hsep.value_remainder
  have hb' : a'.valueSum < shift :=
    Nat.lt_of_le_of_lt ha'.valueSum_le hsep.value_remainder
  rcases base_decomposition_unique shift a.sizeMoment a.valueSum
      a'.sizeMoment a'.valueSum hsep.shift_pos hb hb' hlinear with
    ⟨hA, hB⟩
  have hquadratic :
      shift ^ 2 * a.sizeSquareMoment +
          (2 * shift * a.mixedMoment + a.valueSquareSum) =
        shift ^ 2 * a'.sizeSquareMoment +
          (2 * shift * a'.mixedMoment + a'.valueSquareSum) := by
    simpa [encode, Nat.add_assoc] using congrArg CombSignature.quadratic hencode
  have hrem :
      2 * shift * a.mixedMoment + a.valueSquareSum < shift ^ 2 :=
    Nat.lt_of_le_of_lt
      (Nat.add_le_add
        (Nat.mul_le_mul_left (2 * shift) ha.mixedMoment_le)
        ha.valueSquareSum_le)
      hsep.quadratic_remainder
  have hrem' :
      2 * shift * a'.mixedMoment + a'.valueSquareSum < shift ^ 2 :=
    Nat.lt_of_le_of_lt
      (Nat.add_le_add
        (Nat.mul_le_mul_left (2 * shift) ha'.mixedMoment_le)
        ha'.valueSquareSum_le)
      hsep.quadratic_remainder
  have hshiftSq : 0 < shift ^ 2 := pow_pos hsep.shift_pos 2
  rcases base_decomposition_unique (shift ^ 2)
      a.sizeSquareMoment
      (2 * shift * a.mixedMoment + a.valueSquareSum)
      a'.sizeSquareMoment
      (2 * shift * a'.mixedMoment + a'.valueSquareSum)
      hshiftSq hrem hrem' hquadratic with ⟨hC, hDE⟩
  have he : a.valueSquareSum < 2 * shift :=
    Nat.lt_of_le_of_lt ha.valueSquareSum_le hsep.square_remainder
  have he' : a'.valueSquareSum < 2 * shift :=
    Nat.lt_of_le_of_lt ha'.valueSquareSum_le hsep.square_remainder
  have hbaseTwo : 0 < 2 * shift := Nat.mul_pos (by decide) hsep.shift_pos
  rcases base_decomposition_unique (2 * shift)
      a.mixedMoment a.valueSquareSum
      a'.mixedMoment a'.valueSquareSum
      hbaseTwo he he' hDE with ⟨hD, hE⟩
  exact Aggregates.ext hw hA hC hB hD hE

theorem encode_eq_iff_of_bounds
    (shift maxB maxD maxE : Nat)
    (hsep : ShiftSeparation shift maxB maxD maxE)
    {a a' : Aggregates}
    (ha : AggregateBounds maxB maxD maxE a)
    (ha' : AggregateBounds maxB maxD maxE a') :
    encode shift a = encode shift a' ↔ a = a' := by
  constructor
  · exact encode_injective_on_bounds shift maxB maxD maxE hsep ha ha'
  · intro h
    rw [h]

/-! ## The minimal Prouhet gadget and the k=4 cleared threshold -/

def leftTrade : Finset Int := {1, 2, 6}
def rightTrade : Finset Int := {0, 4, 5}
def prouhetGadget : Finset Int := {0, 1, 2, 4, 5, 6}

theorem minimalProuhet_trade :
    setSignature leftTrade = setSignature rightTrade := by
  native_decide

theorem minimalProuhet_disjoint : Disjoint leftTrade rightTrade := by
  native_decide

theorem prouhet_gadget_values :
    prouhetGadget.card = 6 ∧
      (∑ x ∈ prouhetGadget, x) = 18 ∧
      (∑ x ∈ prouhetGadget, x ^ 2) = 82 := by
  native_decide

/-- The note's printed threshold `s₀=219` implies every cleared separation
inequality needed by the decoder for `maxB=72,maxD=108,maxE=328`. -/
theorem prouhet_k4_shiftSeparation (shift : Nat) (hshift : 219 < shift) :
    ShiftSeparation shift 72 108 328 := by
  constructor
  · omega
  · omega
  · nlinarith
  · omega

theorem prouhet_k4_collision_iff
    (shift : Nat) (hshift : 219 < shift)
    {a a' : Aggregates}
    (ha : AggregateBounds 72 108 328 a)
    (ha' : AggregateBounds 72 108 328 a') :
    encode shift a = encode shift a' ↔ a = a' :=
  encode_eq_iff_of_bounds shift 72 108 328
    (prouhet_k4_shiftSeparation shift hshift) ha ha'

/-! ## Computed census rows and exact cleared rate comparisons -/

structure CensusRow where
  blockSize : Nat
  maxFibre : Nat
  imageSize : Nat
deriving DecidableEq, Repr

def CensusRow.objective (r : CensusRow) : Nat :=
  r.maxFibre * r.imageSize

/-- `clearedRateBeats x y` is the denominator-cleared comparison
`log(objective x)/x.blockSize > log(objective y)/y.blockSize`. -/
def clearedRateBeats (x y : CensusRow) : Prop :=
  x.objective ^ y.blockSize > y.objective ^ x.blockSize

def k2Row : CensusRow := ⟨12, 4, 3863⟩
def k3Row : CensusRow := ⟨18, 23, 162075⟩
def championRow : CensusRow := ⟨24, 190, 4192627⟩
def k5FlatRow : CensusRow := ⟨30, 2072, 57376057⟩
def k5WindowRow : CensusRow := ⟨30, 760, 171764913⟩

theorem champion_counts :
    championRow.maxFibre = 190 ∧
      championRow.imageSize = 4192627 ∧
      championRow.objective = 796599130 := by
  decide

theorem k5_flat_counts :
    k5FlatRow.maxFibre = 2072 ∧
      k5FlatRow.imageSize = 57376057 ∧
      k5FlatRow.objective = 118883190104 := by
  decide

theorem champion_beats_k2 : clearedRateBeats championRow k2Row := by
  unfold clearedRateBeats
  native_decide

theorem champion_beats_k3 : clearedRateBeats championRow k3Row := by
  unfold clearedRateBeats
  native_decide

theorem champion_beats_k5_flat :
    clearedRateBeats championRow k5FlatRow := by
  unfold clearedRateBeats
  native_decide

theorem champion_beats_k5_window :
    clearedRateBeats championRow k5WindowRow := by
  unfold clearedRateBeats
  native_decide

theorem k5_window_beats_k5_flat :
    clearedRateBeats k5WindowRow k5FlatRow := by
  unfold clearedRateBeats
  native_decide

def reportedRows : List CensusRow :=
  [k2Row, k3Row, championRow, k5FlatRow, k5WindowRow]

/-- Exact finite ceiling for the five reported census rows.  This is not a
claim about unsearched weight sequences. -/
theorem champion_ceiling_on_reportedRows :
    ∀ r ∈ reportedRows,
      r = championRow ∨ ¬clearedRateBeats r championRow := by
  unfold reportedRows clearedRateBeats
  native_decide

/-- The finite ceiling compiler: once a census proves every searched row has
cleared rate at most the named k=4 row, the maximum of that finite family is
the champion. -/
theorem finite_ceiling_of_pointwise
    {ι : Type} [Fintype ι] (rows : ι → CensusRow)
    (hbound : ∀ i, rows i = championRow ∨
      ¬clearedRateBeats (rows i) championRow) :
    ∀ i, rows i = championRow ∨
      ¬clearedRateBeats (rows i) championRow :=
  hbound

#print axioms shiftedCombSignature_eq_encode
#print axioms base_decomposition_unique
#print axioms encode_injective_on_bounds
#print axioms encode_eq_iff_of_bounds
#print axioms minimalProuhet_trade
#print axioms prouhet_k4_shiftSeparation
#print axioms prouhet_k4_collision_iff
#print axioms champion_beats_k5_flat
#print axioms champion_beats_k5_window
#print axioms champion_ceiling_on_reportedRows
#print axioms finite_ceiling_of_pointwise

end CombTradeChampion
end MomentToMax
