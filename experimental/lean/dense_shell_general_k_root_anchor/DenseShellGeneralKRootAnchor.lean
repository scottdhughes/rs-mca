/-!
# Dense-shell general-K root deletion: algebraic compiler

This stdlib-only module formalizes the exact algebraic steps in
`experimental/notes/thresholds/dense_shell_general_k_root_anchor.md`.
The analytic source supplies the wordwise identity `q_1 = 1/4`; the first
theorem proves that any wordwise constant decoration factors from every finite
decorated charge, uniformly in all remaining decorations.

The second block formalizes the pointwise ternary cancellation compiler and
the parity-repaired paired positive-charge identity.  It uses neither a sign
law nor a finite census.
-/

namespace DenseShellGeneralKRootAnchor

set_option autoImplicit false

/-! ## Constant-decoration compiler -/

structure ChargeLaws (R : Type) [Zero R] [OfNat R 1] [Add R] [Mul R] : Prop where
  mul_assoc : ∀ a b c : R, (a * b) * c = a * (b * c)
  mul_comm : ∀ a b : R, a * b = b * a
  mul_add : ∀ a b c : R, a * (b + c) = a * b + a * c
  mul_zero : ∀ a : R, a * 0 = 0

def listProduct {R : Type} [OfNat R 1] [Mul R] : List R → R
  | [] => 1
  | x :: xs => x * listProduct xs

def listSum {R : Type} [Zero R] [Add R] : List R → R
  | [] => 0
  | x :: xs => x + listSum xs

def decoratedProduct {R : Type} [OfNat R 1] [Mul R]
    (drift : Nat → R) (K : List Nat) : R :=
  listProduct (K.map drift)

def totalDecoratedCharge {R A : Type} [Zero R] [OfNat R 1] [Add R] [Mul R]
    (leaves : List A) (weight : A → R) (drift : A → Nat → R)
    (K : List Nat) : R :=
  listSum (leaves.map (fun x => weight x * decoratedProduct (drift x) K))

/-- If one decoration is the same scalar `c` on every leaf, it factors from
the entire finite decorated charge, uniformly in the remaining list `K`.
The dense-shell source has `c = 1/4` at scan position one. -/
theorem constant_decoration_deletion
    {R A : Type} [Zero R] [OfNat R 1] [Add R] [Mul R]
    (laws : ChargeLaws R)
    (leaves : List A) (weight : A → R) (drift : A → Nat → R)
    (k : Nat) (K : List Nat) (c : R)
    (hconst : ∀ x ∈ leaves, drift x k = c) :
    totalDecoratedCharge leaves weight drift (k :: K) =
      c * totalDecoratedCharge leaves weight drift K := by
  induction leaves with
  | nil =>
      change 0 = c * 0
      exact (laws.mul_zero c).symm
  | cons x xs ih =>
      have hx : drift x k = c := hconst x (by simp)
      have hxs : ∀ y ∈ xs, drift y k = c := by
        intro y hy
        exact hconst y (by simp [hy])
      change
        weight x * (drift x k * decoratedProduct (drift x) K) +
            totalDecoratedCharge xs weight drift (k :: K) =
          c * (weight x * decoratedProduct (drift x) K +
            totalDecoratedCharge xs weight drift K)
      rw [hx, ih hxs, laws.mul_add]
      congr 1
      rw [← laws.mul_assoc, laws.mul_comm (weight x) c, laws.mul_assoc]

/-! ## Ternary class pairing and repaired charge arithmetic -/

structure AddCommMonoidLaws (R : Type) [Zero R] [Add R] : Prop where
  add_assoc : ∀ a b c : R, (a + b) + c = a + (b + c)
  add_comm : ∀ a b : R, a + b = b + a
  add_zero : ∀ a : R, a + 0 = a
  zero_add : ∀ a : R, 0 + a = a

def mappedSum {R A : Type} [Zero R] [Add R]
    (xs : List A) (f : A → R) : R :=
  listSum (xs.map f)

theorem add_shuffle {R : Type} [Zero R] [Add R]
    (laws : AddCommMonoidLaws R) (a b c d : R) :
    (a + b) + (c + d) = (a + c) + (b + d) := by
  calc
    (a + b) + (c + d) = a + (b + (c + d)) := laws.add_assoc a b (c + d)
    _ = a + ((b + c) + d) := by rw [laws.add_assoc b c d]
    _ = a + ((c + b) + d) := by rw [laws.add_comm b c]
    _ = a + (c + (b + d)) := by rw [laws.add_assoc c b d]
    _ = (a + c) + (b + d) := (laws.add_assoc a c (b + d)).symm

theorem add_swap_middle {R : Type} [Zero R] [Add R]
    (laws : AddCommMonoidLaws R) (a b c : R) :
    (a + b) + c = (a + c) + b := by
  calc
    (a + b) + c = a + (b + c) := laws.add_assoc a b c
    _ = a + (c + b) := by rw [laws.add_comm b c]
    _ = (a + c) + b := (laws.add_assoc a c b).symm

/-- Summing the pointwise ternary relation over the base support class makes
the top-digit class sum cancel the base class sum exactly. -/
theorem paired_class_sums_cancel
    {R A : Type} [Zero R] [Add R]
    (laws : AddCommMonoidLaws R)
    (base : List A) (minus center plus : A → R)
    (hlocal : ∀ x ∈ base, (minus x + center x) + plus x = 0) :
    mappedSum base (fun x => minus x + plus x) +
        mappedSum base center = 0 := by
  induction base with
  | nil =>
      change 0 + 0 = 0
      exact laws.zero_add 0
  | cons x xs ih =>
      have hx : (minus x + center x) + plus x = 0 := hlocal x (by simp)
      have hxs : ∀ y ∈ xs, (minus y + center y) + plus y = 0 := by
        intro y hy
        exact hlocal y (by simp [hy])
      have htail := ih hxs
      change
        listSum (List.map (fun y => minus y + plus y) xs) +
          listSum (List.map center xs) = 0 at htail
      simp only [mappedSum, List.map_cons, listSum]
      rw [add_shuffle laws (minus x + plus x)
          (listSum (List.map (fun x => minus x + plus x) xs))
          (center x) (listSum (List.map center xs))]
      rw [add_swap_middle laws (minus x) (plus x) (center x)]
      rw [hx, htail, laws.zero_add]

/-- The denominator-cleared repaired interface: if
`2 Omega_X = M_X + Sigma_X` for both classes and the class sums cancel, then
the paired positive charge is exactly half the paired absolute mass. -/
theorem paired_positive_charge_cleared
    {R : Type} [Zero R] [Add R]
    (laws : AddCommMonoidLaws R)
    (omegaU omegaV massU massV sigmaU sigmaV : R)
    (hU : omegaU + omegaU = massU + sigmaU)
    (hV : omegaV + omegaV = massV + sigmaV)
    (hcancel : sigmaU + sigmaV = 0) :
    (omegaU + omegaV) + (omegaU + omegaV) = massU + massV := by
  rw [add_shuffle laws omegaU omegaV omegaU omegaV]
  rw [hU, hV]
  rw [add_shuffle laws massU sigmaU massV sigmaV]
  rw [hcancel, laws.add_zero]

end DenseShellGeneralKRootAnchor
