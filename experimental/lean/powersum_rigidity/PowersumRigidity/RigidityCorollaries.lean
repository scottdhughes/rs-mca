import PowersumRigidity.Basic

/-!
# Corollaries of power-sum rigidity

Two short machine-checked anchors for the RS-MCA research package.

* `RigidityCorollaries.pte_rigidity` (Prouhet–Tarry–Escott / `E_d = 0`): over a
  field `K` in which `1, …, d` are invertible, two *disjoint* `Finset`s of size
  `d ≥ 1` cannot share all of their power sums `p_1, …, p_d`.  This is a direct
  corollary of `PowersumRigidity.powersum_rigidity`.

* `RigidityCorollaries.const_on_large_set` (degree cap for freezing): a
  polynomial that takes a single value `v` on a `Finset S` larger than its degree
  is the constant polynomial `C v`.
-/

open Finset Polynomial

namespace RigidityCorollaries

variable {K : Type*} [Field K]

/-- **PTE rigidity / `E_d = 0`.** Over a field `K` in which `1, …, d` are
invertible, two disjoint size-`d` finsets (`d ≥ 1`) cannot have equal power sums
`p_1, …, p_d`.  Equivalently: the elementary Prouhet–Tarry–Escott equal-power-sum
system of length `d` has no solution by two disjoint value sets of size `d`. -/
theorem pte_rigidity {d : ℕ} (hd : 1 ≤ d) (A B : Finset K)
    (hA : A.card = d) (hB : B.card = d) (hchar : ∀ k, 1 ≤ k → k ≤ d → (k : K) ≠ 0)
    (hdisj : Disjoint A B)
    (hp : ∀ j, 1 ≤ j → j ≤ d → (∑ a ∈ A, a ^ j) = (∑ b ∈ B, b ^ j)) : False := by
  -- Bridge `Finset.sum` to the `Multiset.map … |>.sum` form used by
  -- `powersum_rigidity` (these are definitionally equal).
  have hpe : ∀ j, 1 ≤ j → j ≤ d →
      (A.val.map (· ^ j)).sum = (B.val.map (· ^ j)).sum :=
    fun j hj1 hj2 => hp j hj1 hj2
  -- Power-sum rigidity forces the underlying multisets, hence the finsets, equal.
  have hval : A.val = B.val :=
    PowersumRigidity.powersum_rigidity A.val B.val hA hB hchar hpe
  have hAB : A = B := Finset.val_injective hval
  -- A set disjoint from itself is empty, contradicting `card = d ≥ 1`.
  subst hAB
  have hempty : A = ∅ := (Finset.disjoint_self_iff_empty A).mp hdisj
  rw [hempty, Finset.card_empty] at hA
  omega

/-- **Degree cap for freezing.** If a polynomial `f : K[X]` takes the same value
`v` on a `Finset S` whose cardinality exceeds `f.natDegree`, then `f` is the
constant polynomial `C v`.  (`f - C v` would otherwise be a nonzero polynomial
with more roots than its degree.) -/
theorem const_on_large_set {f : Polynomial K} {v : K} {S : Finset K}
    (hcard : f.natDegree < S.card) (hconst : ∀ x ∈ S, f.eval x = v) :
    f = Polynomial.C v := by
  classical
  rw [← sub_eq_zero]
  set g := f - Polynomial.C v with hg
  by_contra hg0
  -- Every point of `S` is a root of `g = f - C v`.
  have hroots : ∀ x ∈ S, g.eval x = 0 := by
    intro x hx
    rw [hg, Polynomial.eval_sub, Polynomial.eval_C, hconst x hx, sub_self]
  -- Hence `S` embeds into the (finite) root set of the nonzero polynomial `g`.
  have hsub : S ⊆ g.roots.toFinset := by
    intro x hx
    rw [Multiset.mem_toFinset, Polynomial.mem_roots']
    exact ⟨hg0, hroots x hx⟩
  have h1 : S.card ≤ g.roots.toFinset.card := Finset.card_le_card hsub
  have h2 : g.roots.toFinset.card ≤ Multiset.card g.roots := Multiset.toFinset_card_le g.roots
  have h3 : Multiset.card g.roots ≤ g.natDegree := Polynomial.card_roots' g
  have h4 : g.natDegree = f.natDegree := by rw [hg]; exact Polynomial.natDegree_sub_C
  omega

end RigidityCorollaries
