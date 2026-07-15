import MomentToMax.PowerWeightedConcentrationFloor

/-!
# PTE cluster-packing: exact Boolean signatures and finite certificates

This module formalizes the finite algebra from
`experimental/notes/thresholds/pte_cluster_packing_frontier.md`.

A block is indexed by `Fin n`; a Boolean mask chooses a subset.  Its
degree-two signature records weight, first moment, and second moment.  The
module proves affine collision invariance and therefore invariance of the
semantic image size and maximum fibre.  It also supplies an executable sorted
histogram and checks the note's named fourteen-point champion exactly.

The finite integer tensor arithmetic below does not assert the source note's
local-CLT step.  Optimizer symmetry, a limiting rate, and the value of the
global supremum remain outside this module.
-/

namespace MomentToMax
namespace PTEClusterPacking

abbrev Mask (n : Nat) := Fin (2 ^ n)

@[ext]
structure Signature where
  weight : Nat
  linear : Int
  quadratic : Int
deriving DecidableEq, Repr

def selected {n : Nat} (x : Mask n) : Finset (Fin n) :=
  Finset.univ.filter fun i => x.val.testBit i.val

def weight {n : Nat} (x : Mask n) : Nat :=
  (selected x).card

def firstMoment {n : Nat} (v : Fin n → Int) (x : Mask n) : Int :=
  ∑ i ∈ selected x, v i

def secondMoment {n : Nat} (v : Fin n → Int) (x : Mask n) : Int :=
  ∑ i ∈ selected x, (v i) ^ 2

def signature {n : Nat} (v : Fin n → Int) (x : Mask n) : Signature where
  weight := weight x
  linear := firstMoment v x
  quadratic := secondMoment v x

def affineBlock {n : Nat} (a c : Int) (v : Fin n → Int) : Fin n → Int :=
  fun i => a * v i + c

theorem firstMoment_affine {n : Nat} (a c : Int) (v : Fin n → Int)
    (x : Mask n) :
    firstMoment (affineBlock a c v) x =
      a * firstMoment v x + c * (weight x : Int) := by
  simp only [firstMoment, affineBlock, weight]
  calc
    ∑ i ∈ selected x, (a * v i + c) =
        ∑ i ∈ selected x, (a * v i) + ∑ _i ∈ selected x, c := by
          rw [Finset.sum_add_distrib]
    _ = a * (∑ i ∈ selected x, v i) + c * ((selected x).card : Int) := by
          simp [Finset.mul_sum, mul_comm]

theorem secondMoment_affine {n : Nat} (a c : Int) (v : Fin n → Int)
    (x : Mask n) :
    secondMoment (affineBlock a c v) x =
      a ^ 2 * secondMoment v x +
        (2 * a * c) * firstMoment v x +
        c ^ 2 * (weight x : Int) := by
  simp only [secondMoment, affineBlock, firstMoment, weight]
  calc
    ∑ i ∈ selected x, (a * v i + c) ^ 2 =
        ∑ i ∈ selected x,
          (a ^ 2 * (v i) ^ 2 + (2 * a * c) * v i + c ^ 2) := by
            apply Finset.sum_congr rfl
            intro i hi
            ring
    _ = a ^ 2 * (∑ i ∈ selected x, (v i) ^ 2) +
          (2 * a * c) * (∑ i ∈ selected x, v i) +
          c ^ 2 * ((selected x).card : Int) := by
            simp [Finset.mul_sum, Finset.sum_add_distrib, mul_comm]

def transformSignature (a c : Int) (s : Signature) : Signature where
  weight := s.weight
  linear := a * s.linear + c * (s.weight : Int)
  quadratic :=
    a ^ 2 * s.quadratic + (2 * a * c) * s.linear +
      c ^ 2 * (s.weight : Int)

theorem signature_affine {n : Nat} (a c : Int) (v : Fin n → Int)
    (x : Mask n) :
    signature (affineBlock a c v) x =
      transformSignature a c (signature v x) := by
  ext
  · rfl
  · exact firstMoment_affine a c v x
  · exact secondMoment_affine a c v x

theorem transformSignature_injective (a c : Int) (ha : a ≠ 0) :
    Function.Injective (transformSignature a c) := by
  intro s t h
  have hw0 := congrArg (fun u : Signature => u.weight) h
  have hw : s.weight = t.weight := by
    simpa [transformSignature] using hw0
  have hl0 : a * s.linear + c * (s.weight : Int) =
      a * t.linear + c * (t.weight : Int) :=
    congrArg (fun u : Signature => u.linear) h
  have hlmul : a * s.linear = a * t.linear := by
    simpa [hw] using hl0
  have hl : s.linear = t.linear := mul_left_cancel₀ ha hlmul
  have hq0 :
      a ^ 2 * s.quadratic + (2 * a * c) * s.linear +
          c ^ 2 * (s.weight : Int) =
        a ^ 2 * t.quadratic + (2 * a * c) * t.linear +
          c ^ 2 * (t.weight : Int) :=
    congrArg (fun u : Signature => u.quadratic) h
  have hqmul : a ^ 2 * s.quadratic = a ^ 2 * t.quadratic := by
    simpa [hw, hl] using hq0
  have hq : s.quadratic = t.quadratic :=
    mul_left_cancel₀ (pow_ne_zero 2 ha) hqmul
  exact Signature.ext hw hl hq

theorem signature_affine_eq_iff {n : Nat} (a c : Int) (ha : a ≠ 0)
    (v : Fin n → Int) (x y : Mask n) :
    signature (affineBlock a c v) x =
        signature (affineBlock a c v) y ↔
      signature v x = signature v y := by
  rw [signature_affine, signature_affine]
  exact (transformSignature_injective a c ha).eq_iff

def semanticImageSize {n : Nat} (v : Fin n → Int) : Nat :=
  ((Fintype.elems : Finset (Mask n)).image (signature v)).card

def fibreSizeAt {n : Nat} (v : Fin n → Int) (x : Mask n) : Nat :=
  ((Fintype.elems : Finset (Mask n)).filter
    fun y => signature v y = signature v x).card

def semanticMaxFibre {n : Nat} (v : Fin n → Int) : Nat :=
  (Fintype.elems : Finset (Mask n)).sup (fibreSizeAt v)

theorem fibreSizeAt_affine {n : Nat} (a c : Int) (ha : a ≠ 0)
    (v : Fin n → Int) (x : Mask n) :
    fibreSizeAt (affineBlock a c v) x = fibreSizeAt v x := by
  unfold fibreSizeAt
  congr 1
  ext y
  simp only [Finset.mem_filter, Fintype.complete, true_and]
  exact signature_affine_eq_iff a c ha v y x

theorem semanticMaxFibre_affine {n : Nat} (a c : Int) (ha : a ≠ 0)
    (v : Fin n → Int) :
    semanticMaxFibre (affineBlock a c v) = semanticMaxFibre v := by
  unfold semanticMaxFibre
  apply Finset.sup_congr rfl
  intro x hx
  exact fibreSizeAt_affine a c ha v x

theorem semanticImageSize_affine {n : Nat} (a c : Int) (ha : a ≠ 0)
    (v : Fin n → Int) :
    semanticImageSize (affineBlock a c v) = semanticImageSize v := by
  unfold semanticImageSize
  have himage :
      (Fintype.elems : Finset (Mask n)).image
          (signature (affineBlock a c v)) =
        ((Fintype.elems : Finset (Mask n)).image (signature v)).image
          (transformSignature a c) := by
    ext s
    simp only [Finset.mem_image, Fintype.complete, true_and]
    constructor
    · rintro ⟨x, rfl⟩
      exact ⟨signature v x, ⟨x, rfl⟩, (signature_affine a c v x).symm⟩
    · rintro ⟨t, ⟨x, rfl⟩, rfl⟩
      exact ⟨x, signature_affine a c v x⟩
  rw [himage]
  exact Finset.card_image_of_injective _
    (transformSignature_injective a c ha)

/-! ## Finite collision-deficit and codimension-three compilers -/

def setSignature (S : Finset Int) : Signature where
  weight := S.card
  linear := ∑ x ∈ S, x
  quadratic := ∑ x ∈ S, x ^ 2

def addSignature (s t : Signature) : Signature where
  weight := s.weight + t.weight
  linear := s.linear + t.linear
  quadratic := s.quadratic + t.quadratic

theorem setSignature_union {A B : Finset Int} (hdisj : Disjoint A B) :
    setSignature (A ∪ B) =
      addSignature (setSignature A) (setSignature B) := by
  ext
  · exact Finset.card_union_of_disjoint hdisj
  · exact Finset.sum_union hdisj
  · exact Finset.sum_union hdisj

/-- Adding a common outside complement to both sides of a degree-two PTE trade
preserves the collision.  This is the algebraic input used by the deletion
certificate below. -/
theorem common_complement_preserves_trade
    {P Q C : Finset Int} (htrade : setSignature P = setSignature Q)
    (hCP : Disjoint C P) (hCQ : Disjoint C Q) :
    setSignature (C ∪ P) = setSignature (C ∪ Q) := by
  calc
    setSignature (C ∪ P) =
        addSignature (setSignature C) (setSignature P) :=
      setSignature_union hCP
    _ = addSignature (setSignature C) (setSignature Q) := by
      rw [htrade]
    _ = setSignature (C ∪ Q) := (setSignature_union hCQ).symm

/-! ### Unconditional Vandermonde codimension-three cap -/

def indicator (b : Bool) : Int := if b then 1 else 0

theorem indicator_injective : Function.Injective indicator := by
  intro a b h
  cases a <;> cases b <;> simp_all [indicator]

theorem vandermonde_three_unique
    (x0 x1 x2 a0 a1 a2 b0 b1 b2 : Int)
    (hx01 : x0 ≠ x1) (hx02 : x0 ≠ x2) (hx12 : x1 ≠ x2)
    (h0 : a0 + a1 + a2 = b0 + b1 + b2)
    (h1 : x0 * a0 + x1 * a1 + x2 * a2 =
      x0 * b0 + x1 * b1 + x2 * b2)
    (h2 : x0 ^ 2 * a0 + x1 ^ 2 * a1 + x2 ^ 2 * a2 =
      x0 ^ 2 * b0 + x1 ^ 2 * b1 + x2 ^ 2 * b2) :
    a0 = b0 ∧ a1 = b1 ∧ a2 = b2 := by
  have hd0 : ((x0 - x1) * (x0 - x2)) * (a0 - b0) = 0 := by
    linear_combination (x1 * x2) * h0 - (x1 + x2) * h1 + h2
  have hd1 : ((x1 - x0) * (x1 - x2)) * (a1 - b1) = 0 := by
    linear_combination (x0 * x2) * h0 - (x0 + x2) * h1 + h2
  have hd2 : ((x2 - x0) * (x2 - x1)) * (a2 - b2) = 0 := by
    linear_combination (x0 * x1) * h0 - (x0 + x1) * h1 + h2
  have ha0 : a0 - b0 = 0 :=
    (mul_eq_zero.mp hd0).resolve_left
      (mul_ne_zero (sub_ne_zero.mpr hx01) (sub_ne_zero.mpr hx02))
  have ha1 : a1 - b1 = 0 :=
    (mul_eq_zero.mp hd1).resolve_left
      (mul_ne_zero (sub_ne_zero.mpr hx01.symm) (sub_ne_zero.mpr hx12))
  have ha2 : a2 - b2 = 0 :=
    (mul_eq_zero.mp hd2).resolve_left
      (mul_ne_zero (sub_ne_zero.mpr hx02.symm) (sub_ne_zero.mpr hx12.symm))
  exact ⟨sub_eq_zero.mp ha0, sub_eq_zero.mp ha1, sub_eq_zero.mp ha2⟩

def maskWeight {ι : Type} [Fintype ι] (x : ι → Bool) : Int :=
  ∑ i, indicator (x i)

def maskMoment {ι : Type} [Fintype ι] (v : ι → Int)
    (x : ι → Bool) : Int :=
  ∑ i, v i * indicator (x i)

structure SplitSignature where
  mass : Int
  linear : Int
  quadratic : Int
deriving DecidableEq

def splitSignature {n : Nat} (headValues : Fin 3 → Int)
    (tailValues : Fin n → Int)
    (x : (Fin 3 → Bool) × (Fin n → Bool)) : SplitSignature where
  mass := maskWeight x.1 + maskWeight x.2
  linear := maskMoment headValues x.1 + maskMoment tailValues x.2
  quadratic := maskMoment (fun i => (headValues i) ^ 2) x.1 +
    maskMoment (fun i => (tailValues i) ^ 2) x.2

theorem splitSignature_head_injective {n : Nat}
    (headValues : Fin 3 → Int) (tailValues : Fin n → Int)
    (h01 : headValues 0 ≠ headValues 1)
    (h02 : headValues 0 ≠ headValues 2)
    (h12 : headValues 1 ≠ headValues 2)
    {x y : (Fin 3 → Bool) × (Fin n → Bool)}
    (htail : x.2 = y.2)
    (hsig : splitSignature headValues tailValues x =
      splitSignature headValues tailValues y) :
    x = y := by
  have hm0 := congrArg SplitSignature.mass hsig
  have hm1 := congrArg SplitSignature.linear hsig
  have hm2 := congrArg SplitSignature.quadratic hsig
  have hb0 : maskWeight x.1 = maskWeight y.1 := by
    simp only [splitSignature] at hm0
    rw [htail] at hm0
    exact add_right_cancel hm0
  have h0 :
      indicator (x.1 0) + indicator (x.1 1) + indicator (x.1 2) =
        indicator (y.1 0) + indicator (y.1 1) + indicator (y.1 2) := by
    simpa [maskWeight, Fin.sum_univ_succ, add_assoc] using hb0
  have hb1 : maskMoment headValues x.1 = maskMoment headValues y.1 := by
    simp only [splitSignature] at hm1
    rw [htail] at hm1
    exact add_right_cancel hm1
  have h1 :
      headValues 0 * indicator (x.1 0) +
          headValues 1 * indicator (x.1 1) +
          headValues 2 * indicator (x.1 2) =
        headValues 0 * indicator (y.1 0) +
          headValues 1 * indicator (y.1 1) +
          headValues 2 * indicator (y.1 2) := by
    simpa [maskMoment, Fin.sum_univ_succ, add_assoc] using hb1
  have hb2 :
      maskMoment (fun i => (headValues i) ^ 2) x.1 =
        maskMoment (fun i => (headValues i) ^ 2) y.1 := by
    simp only [splitSignature] at hm2
    rw [htail] at hm2
    exact add_right_cancel hm2
  have h2 :
      (headValues 0) ^ 2 * indicator (x.1 0) +
          (headValues 1) ^ 2 * indicator (x.1 1) +
          (headValues 2) ^ 2 * indicator (x.1 2) =
        (headValues 0) ^ 2 * indicator (y.1 0) +
          (headValues 1) ^ 2 * indicator (y.1 1) +
          (headValues 2) ^ 2 * indicator (y.1 2) := by
    simpa [maskMoment, Fin.sum_univ_succ, add_assoc] using hb2
  rcases vandermonde_three_unique
      (headValues 0) (headValues 1) (headValues 2)
      (indicator (x.1 0)) (indicator (x.1 1)) (indicator (x.1 2))
      (indicator (y.1 0)) (indicator (y.1 1)) (indicator (y.1 2))
      h01 h02 h12 h0 h1 h2 with ⟨e0, e1, e2⟩
  have hhead : x.1 = y.1 := by
    funext i
    fin_cases i
    · exact indicator_injective e0
    · exact indicator_injective e1
    · exact indicator_injective e2
  exact Prod.ext hhead htail

def splitFibre {n : Nat} (headValues : Fin 3 → Int)
    (tailValues : Fin n → Int) (s : SplitSignature) :
    Finset ((Fin 3 → Bool) × (Fin n → Bool)) :=
  Finset.univ.filter fun x => splitSignature headValues tailValues x = s

theorem splitFibre_card_le_pow {n : Nat}
    (headValues : Fin 3 → Int) (tailValues : Fin n → Int)
    (h01 : headValues 0 ≠ headValues 1)
    (h02 : headValues 0 ≠ headValues 2)
    (h12 : headValues 1 ≠ headValues 2)
    (s : SplitSignature) :
    (splitFibre headValues tailValues s).card ≤ 2 ^ n := by
  have hle := Finset.card_le_card_of_injOn Prod.snd
    (s := splitFibre headValues tailValues s)
    (t := (Finset.univ : Finset (Fin n → Bool)))
    (by
      intro x hx
      exact Finset.mem_univ _)
    (by
      intro x hx y hy htail
      exact splitSignature_head_injective headValues tailValues
        h01 h02 h12 htail
        ((Finset.mem_filter.mp hx).2.trans
          (Finset.mem_filter.mp hy).2.symm))
  simpa [Fintype.card_fun] using hle

def signatureFibre {n : Nat} (v : Fin n → Int) (s : Signature) :
    Finset (Mask n) :=
  (Fintype.elems : Finset (Mask n)).filter fun x => signature v x = s

/-- A finite set of redundant representatives whose deletion preserves the
whole image.  A PTE trade supplies such a certificate by deleting one member
of every complement-indexed collision pair. -/
structure CollisionDeletionCertificate {α β : Type}
    [DecidableEq α] [DecidableEq β] (domain : Finset α) (f : α → β) where
  redundant : Finset α
  redundant_subset : redundant ⊆ domain
  image_after_deletion :
    ((domain \ redundant).image f) = domain.image f

theorem CollisionDeletionCertificate.image_card_add_redundant_le
    {α β : Type} [DecidableEq α] [DecidableEq β]
    {domain : Finset α} {f : α → β}
    (cert : CollisionDeletionCertificate domain f) :
    (domain.image f).card + cert.redundant.card ≤ domain.card := by
  calc
    (domain.image f).card + cert.redundant.card =
        ((domain \ cert.redundant).image f).card +
          cert.redundant.card := by rw [cert.image_after_deletion]
    _ ≤ (domain \ cert.redundant).card + cert.redundant.card :=
      Nat.add_le_add_right Finset.card_image_le _
    _ = (domain ∪ cert.redundant).card := by
      rw [Finset.card_sdiff_add_card]
    _ = domain.card := by
      rw [Finset.union_eq_left.mpr cert.redundant_subset]

theorem CollisionDeletionCertificate.deficit_ge_redundant
    {α β : Type} [DecidableEq α] [DecidableEq β]
    {domain : Finset α} {f : α → β}
    (cert : CollisionDeletionCertificate domain f) :
    cert.redundant.card ≤ domain.card - (domain.image f).card := by
  have h := cert.image_card_add_redundant_le
  omega

/-- A pointwise repair map constructs a deletion certificate.  This is the
abstract combinatorial heart of the source note's complement-indexed PTE
trade argument. -/
def collisionDeletionCertificateOfRepair
    {α β : Type} [DecidableEq α] [DecidableEq β]
    (domain redundant : Finset α) (f : α → β)
    (hsubset : redundant ⊆ domain) (repair : α → α)
    (hrepair : ∀ x ∈ redundant,
      repair x ∈ domain \ redundant ∧ f (repair x) = f x) :
    CollisionDeletionCertificate domain f where
  redundant := redundant
  redundant_subset := hsubset
  image_after_deletion := by
    ext y
    constructor
    · intro hy
      rcases Finset.mem_image.mp hy with ⟨x, hx, rfl⟩
      exact Finset.mem_image.mpr
        ⟨x, (Finset.mem_sdiff.mp hx).1, rfl⟩
    · intro hy
      rcases Finset.mem_image.mp hy with ⟨x, hx, rfl⟩
      by_cases hr : x ∈ redundant
      · exact Finset.mem_image.mpr
          ⟨repair x, hrepair x hr |>.1, hrepair x hr |>.2⟩
      · exact Finset.mem_image.mpr
          ⟨x, Finset.mem_sdiff.mpr ⟨hx, hr⟩, rfl⟩

/-- Source-shaped cleared trade-deficit conclusion.  The PTE construction has
one redundant right member for each of the `2^(b-2r)` outside complements. -/
theorem trade_deficit_of_deletion_certificate
    {α β : Type} [DecidableEq α] [DecidableEq β]
    {domain : Finset α} {f : α → β}
    (cert : CollisionDeletionCertificate domain f)
    (b r : Nat) (hcard : cert.redundant.card = 2 ^ (b - 2 * r)) :
    2 ^ (b - 2 * r) ≤ domain.card - (domain.image f).card := by
  rw [← hcard]
  exact cert.deficit_ge_redundant

/-- If three dependent coordinates are uniquely reconstructed from the other
`n-3` bits on a signature fibre, that fibre has at most `2^(n-3)`
members.  The source's Vandermonde argument supplies exactly this injectivity
certificate for three distinct block values. -/
theorem fibre_card_le_codimension_three {n : Nat} (_hthree : 3 ≤ n)
    (v : Fin n → Int) (s : Signature)
    (encode : Mask n → Fin (2 ^ (n - 3)))
    (hinjective : Set.InjOn encode (signatureFibre v s : Set (Mask n))) :
    (signatureFibre v s).card ≤ 2 ^ (n - 3) := by
  have hle := Finset.card_le_card_of_injOn encode
    (s := signatureFibre v s)
    (t := (Finset.univ : Finset (Fin (2 ^ (n - 3)))))
    (by
      intro x hx
      show encode x ∈ (Finset.univ : Finset (Fin (2 ^ (n - 3))))
      exact Finset.mem_univ _)
    hinjective
  simpa using hle

/-- Cleared per-block consequence of the codimension-three fibre cap. -/
theorem packing_objective_le_of_codimension_three
    (b fstar imageSize : Nat) (_hthree : 3 ≤ b)
    (hfibre : fstar ≤ 2 ^ (b - 3)) (himage : imageSize ≤ 2 ^ b) :
    fstar * imageSize ≤ (2 ^ (b - 3)) * (2 ^ b) :=
  Nat.mul_le_mul hfibre himage

/-! ## Executable exact histogram -/

def signatureLe (s t : Signature) : Bool :=
  if s.weight < t.weight then true
  else if t.weight < s.weight then false
  else if s.linear < t.linear then true
  else if t.linear < s.linear then false
  else s.quadratic ≤ t.quadratic

structure RunState where
  previous : Option Signature := none
  current : Nat := 0
  maximum : Nat := 0
  distinct : Nat := 0

def RunState.step (st : RunState) (s : Signature) : RunState :=
  match st.previous with
  | none =>
      { previous := some s, current := 1, maximum := 1, distinct := 1 }
  | some t =>
      if s = t then
        { st with current := st.current + 1
                  maximum := Nat.max st.maximum (st.current + 1) }
      else
        { previous := some s, current := 1,
          maximum := Nat.max st.maximum 1, distinct := st.distinct + 1 }

def signatureList {n : Nat} (v : Fin n → Int) : List Signature :=
  List.ofFn fun x : Fin (2 ^ n) => signature v x

def packingStats {n : Nat} (v : Fin n → Int) : Nat × Nat :=
  let sorted := (signatureList v).mergeSort signatureLe
  let st := sorted.foldl RunState.step {}
  (st.maximum, st.distinct)

/-- The symmetric fourteen-point block from the source packet. -/
def champion : Fin 14 → Int :=
  ![0, 2, 3, 4, 5, 8, 9, 13, 14, 17, 18, 19, 20, 22]

/-- Exact exhaustive histogram: `fstar=12` and `L1=12239`. -/
theorem champion_packingStats : packingStats champion = (12, 12239) := by
  native_decide

def championObjectiveNumerator : Nat := 12 * 12239
def championObjectiveDenominator : Nat := 2 ^ 14

theorem champion_objective_values :
    championObjectiveNumerator = 146868 ∧
      championObjectiveDenominator = 16384 := by
  decide

theorem champion_objective_superunit :
    championObjectiveDenominator < championObjectiveNumerator := by
  decide

/-- The exact cleared tensor objective grows multiplicatively.  Connecting this
finite identity to the balanced-weight tensor limit is a separate local-CLT
premise in the source note. -/
theorem champion_tensor_objective (k : Nat) :
    (12 ^ k) * (12239 ^ k) = championObjectiveNumerator ^ k := by
  change (12 ^ k) * (12239 ^ k) = (12 * 12239) ^ k
  rw [Nat.mul_pow]

theorem champion_tensor_superunit {k : Nat} (hk : 0 < k) :
    championObjectiveDenominator ^ k <
      championObjectiveNumerator ^ k :=
  Nat.pow_lt_pow_left champion_objective_superunit (Nat.ne_of_gt hk)

#print axioms firstMoment_affine
#print axioms secondMoment_affine
#print axioms signature_affine_eq_iff
#print axioms common_complement_preserves_trade
#print axioms CollisionDeletionCertificate.deficit_ge_redundant
#print axioms vandermonde_three_unique
#print axioms splitFibre_card_le_pow
#print axioms semanticMaxFibre_affine
#print axioms semanticImageSize_affine
#print axioms champion_packingStats
#print axioms champion_tensor_objective
#print axioms champion_tensor_superunit

end PTEClusterPacking
end MomentToMax
