import Mathlib

/-!
# Field-independent balanced-core transverse-secant charging

This module formalizes the finite injection at the heart of
`experimental/notes/thresholds/ray_compiler_balanced_core.md`.

For each `(κ+1)`-subset `T` of a fixed chart, the augmented minor is an
affine function `A(T) + γ * B(T)`. A transverse slope is charged to a subset
where this affine function is nonzero and vanishes at the slope. A nonzero
affine function has at most one root, so the charge is injective and

```
#slopes <= choose (#U) (κ+1).
```

The module also proves the geometric bridge. MDS coefficient uniqueness on
every `κ`-subset localizes any sufficiently large transverse source set to a
transverse `(κ+1)`-subset. Its final entry point derives the count directly
from source-shaped supported witnesses. The theorem is field-independent.
-/

namespace SyndromeSecant.BalancedCoreTransverseSecant

open Finset BigOperators

variable {F Coord : Type*} [Field F]

/-- An affine secant equation indexed by a coordinate subset. -/
def affineSecant (A B : Finset Coord → F)
    (T : Finset Coord) (γ : F) : F :=
  A T + γ * B T

/-- The indexed affine secant is not the zero polynomial. -/
def nondegenerate (A B : Finset Coord → F)
    (T : Finset Coord) : Prop :=
  A T ≠ 0 ∨ B T ≠ 0

theorem affineSecant_root_unique
    {a b γ δ : F} (hnon : a ≠ 0 ∨ b ≠ 0)
    (hγ : a + γ * b = 0) (hδ : a + δ * b = 0) :
    γ = δ := by
  by_cases hb : b = 0
  · have ha : a ≠ 0 := by
      rcases hnon with ha | hbnon
      · exact ha
      · exact (hbnon hb).elim
    rw [hb, mul_zero, add_zero] at hγ
    exact (ha hγ).elim
  · have hmul : (γ - δ) * b = 0 := by
      linear_combination hγ - hδ
    exact sub_eq_zero.mp ((mul_eq_zero.mp hmul).resolve_right hb)

/--
Every certified slope chooses a nonzero affine secant minor, and no minor can
receive two slopes. Hence slopes inject into `(kappa+1)`-subsets of the chart.
-/
theorem slope_card_le_choose_of_affine_charge
    [DecidableEq Coord]
    (U : Finset Coord) (κ : ℕ)
    (A B : Finset Coord → F) (slopes : Finset F)
    (hcert : ∀ γ ∈ slopes,
      ∃ T ∈ U.powersetCard (κ + 1),
        nondegenerate A B T ∧ affineSecant A B T γ = 0) :
    slopes.card ≤ Nat.choose U.card (κ + 1) := by
  classical
  let Slope := {γ : F // γ ∈ slopes}
  let Minor := {T : Finset Coord // T ∈ U.powersetCard (κ + 1)}
  letI : Fintype Minor :=
    Fintype.ofFinset (U.powersetCard (κ + 1)) (fun _ => Iff.rfl)
  have hcert' : ∀ γ : Slope,
      ∃ T : Minor,
        nondegenerate A B T.1 ∧ affineSecant A B T.1 γ.1 = 0 := by
    intro γ
    obtain ⟨T, hT, hnon, hroot⟩ := hcert γ.1 γ.2
    exact ⟨⟨T, hT⟩, hnon, hroot⟩
  choose charge hnon hroot using hcert'
  have hinj : Function.Injective charge := by
    intro γ δ hcharge
    apply Subtype.ext
    have hT : (charge γ).1 = (charge δ).1 :=
      congrArg Subtype.val hcharge
    have hnon' := hnon γ
    have hγ := hroot γ
    have hδ := hroot δ
    rw [hT] at hγ hnon'
    exact affineSecant_root_unique hnon' hγ hδ
  have hcard : Fintype.card Slope ≤ Fintype.card Minor :=
    Fintype.card_le_of_injective charge hinj
  simpa [Slope, Minor] using hcard

/--
The source theorem's displayed form when the chart has cardinality
`R + kappa`.
-/
theorem transverseSecant_card_le
    [DecidableEq Coord]
    (U : Finset Coord) (R κ : ℕ)
    (A B : Finset Coord → F) (slopes : Finset F)
    (hU : U.card = R + κ)
    (hcert : ∀ γ ∈ slopes,
      ∃ T ∈ U.powersetCard (κ + 1),
        nondegenerate A B T ∧ affineSecant A B T γ = 0) :
    slopes.card ≤ Nat.choose (R + κ) (κ + 1) := by
  simpa [hU] using
    slope_card_le_choose_of_affine_charge U κ A B slopes hcert

/--
Single-circuit specialization `kappa=1`: the bound is
`choose (R+1) 2`.
-/
theorem singleCircuit_card_le
    [DecidableEq Coord]
    (U : Finset Coord) (R : ℕ)
    (A B : Finset Coord → F) (slopes : Finset F)
    (hU : U.card = R + 1)
    (hcert : ∀ γ ∈ slopes,
      ∃ T ∈ U.powersetCard 2,
        nondegenerate A B T ∧ affineSecant A B T γ = 0) :
    slopes.card ≤ Nat.choose (R + 1) 2 := by
  simpa using transverseSecant_card_le U R 1 A B slopes hU hcert

/-! ## Kernel-row formulation -/

/-- Pairing a kernel-generator row with a coefficient vector. -/
def kernelDot {κ : ℕ} (row : Coord → Fin κ → F)
    (x : Coord) (c : Fin κ → F) : F :=
  ∑ i, row x i * c i

/-- A coordinate function lies in the restricted kernel-column span on `T`. -/
def inKernelSpanOn {κ : ℕ} (row : Coord → Fin κ → F)
    (T : Finset Coord) (b : Coord → F) : Prop :=
  ∃ c : Fin κ → F, ∀ x ∈ T, b x + kernelDot row x c = 0

/-- The two fixed lifts are transverse on `T`. -/
def transverseOn {κ : ℕ} (row : Coord → Fin κ → F)
    (T : Finset Coord) (b0 b1 : Coord → F) : Prop :=
  ¬(inKernelSpanOn row T b0 ∧ inKernelSpanOn row T b1)

/-- The moving line has a kernel-corrected representative vanishing on `T`. -/
def lineConsistentOn {κ : ℕ} (row : Coord → Fin κ → F)
    (T : Finset Coord) (b0 b1 : Coord → F) (γ : F) : Prop :=
  ∃ c : Fin κ → F, ∀ x ∈ T,
    b0 x + γ * b1 x + kernelDot row x c = 0

theorem kernelDot_sub {κ : ℕ} (row : Coord → Fin κ → F)
    (x : Coord) (c d : Fin κ → F) :
    kernelDot row x (fun i => c i - d i) =
      kernelDot row x c - kernelDot row x d := by
  simp [kernelDot, mul_sub, Finset.sum_sub_distrib]

theorem kernelDot_smul {κ : ℕ} (row : Coord → Fin κ → F)
    (x : Coord) (r : F) (c : Fin κ → F) :
    kernelDot row x (fun i => r * c i) =
      r * kernelDot row x c := by
  simp [kernelDot, Finset.mul_sum, mul_left_comm]

/--
A transverse `(kappa+1)`-subset is consistent with at most one finite slope.
This is the determinant-root uniqueness argument in kernel-row form.
-/
theorem lineConsistentOn_unique_of_transverse
    {κ : ℕ} (row : Coord → Fin κ → F)
    (T : Finset Coord) (b0 b1 : Coord → F) {γ δ : F}
    (htrans : transverseOn row T b0 b1)
    (hγ : lineConsistentOn row T b0 b1 γ)
    (hδ : lineConsistentOn row T b0 b1 δ) :
    γ = δ := by
  by_contra hne
  have hgd : γ - δ ≠ 0 := sub_ne_zero.mpr hne
  obtain ⟨c, hc⟩ := hγ
  obtain ⟨d, hd⟩ := hδ
  let e : Fin κ → F := fun i => (γ - δ)⁻¹ * (c i - d i)
  have hb1 : inKernelSpanOn row T b1 := by
    refine ⟨e, ?_⟩
    intro x hx
    have hc' := hc x hx
    have hd' := hd x hx
    have hsub :
        (γ - δ) * b1 x +
          (kernelDot row x c - kernelDot row x d) = 0 := by
      linear_combination hc' - hd'
    rw [show kernelDot row x e =
      (γ - δ)⁻¹ *
        (kernelDot row x c - kernelDot row x d) by
          rw [show e = fun i => (γ - δ)⁻¹ * (c i - d i) by rfl,
            kernelDot_smul, kernelDot_sub]]
    calc
      b1 x + (γ - δ)⁻¹ *
          (kernelDot row x c - kernelDot row x d) =
        (γ - δ)⁻¹ * ((γ - δ) * b1 x +
          (kernelDot row x c - kernelDot row x d)) := by
            field_simp
      _ = 0 := by rw [hsub, mul_zero]
  have hb0 : inKernelSpanOn row T b0 := by
    obtain ⟨e, he⟩ := hb1
    let f : Fin κ → F := fun i => c i - γ * e i
    refine ⟨f, ?_⟩
    intro x hx
    have hc' := hc x hx
    have he' := he x hx
    rw [show kernelDot row x f =
      kernelDot row x c - γ * kernelDot row x e by
        rw [show f = fun i => c i - γ * e i by rfl,
          kernelDot_sub, kernelDot_smul]]
    linear_combination hc' - γ * he'
  exact htrans ⟨hb0, hb1⟩

/-- Coefficient vectors are uniquely determined by their kernel-row values on `K`. -/
def kernelCoefficientsUniqueOn {κ : ℕ} (row : Coord → Fin κ → F)
    (K : Finset Coord) : Prop :=
  ∀ c d : Fin κ → F,
    (∀ x ∈ K, kernelDot row x c = kernelDot row x d) → c = d

/-- The kernel-row MDS property needed on a fixed chart. -/
def mdsKernelOn {κ : ℕ} (U : Finset Coord)
    (row : Coord → Fin κ → F) : Prop :=
  ∀ K ∈ U.powersetCard κ, kernelCoefficientsUniqueOn row K

/--
The MDS bridge: if kernel coefficients are unique on every `κ`-subset of the
chart, then every transverse source set of size at least `κ+1` contains a
transverse `(κ+1)`-subset. The proof fixes a `κ`-point base and shows that,
if every one-point extension were degenerate, coefficient uniqueness would
extend the same two kernel representations across the whole source set.
-/
theorem exists_transverse_subset_of_mds
    [DecidableEq Coord] {κ : ℕ}
    (U S : Finset Coord) (row : Coord → Fin κ → F)
    (b0 b1 : Coord → F)
    (hSU : S ⊆ U) (hcard : κ + 1 ≤ S.card)
    (hmds : mdsKernelOn U row)
    (htrans : transverseOn row S b0 b1) :
    ∃ T ∈ U.powersetCard (κ + 1),
      T ⊆ S ∧ transverseOn row T b0 b1 := by
  classical
  by_contra hnone
  have hdeg : ∀ T : Finset Coord, T ⊆ S → T.card = κ + 1 →
      inKernelSpanOn row T b0 ∧ inKernelSpanOn row T b1 := by
    intro T hTS hTcard
    have hntrans : ¬transverseOn row T b0 b1 := by
      intro hTtrans
      apply hnone
      exact ⟨T, Finset.mem_powersetCard.mpr ⟨hTS.trans hSU, hTcard⟩,
        hTS, hTtrans⟩
    exact not_not.mp (by simpa [transverseOn] using hntrans)
  obtain ⟨K, hKS, hKcard⟩ :=
    Finset.exists_subset_card_eq (show κ ≤ S.card by omega)
  have hKU : K ⊆ U := hKS.trans hSU
  have hKpow : K ∈ U.powersetCard κ :=
    Finset.mem_powersetCard.mpr ⟨hKU, hKcard⟩
  have hnotSK : ¬S ⊆ K := by
    intro hSK
    have := Finset.card_le_card hSK
    omega
  obtain ⟨x0, hx0S, hx0K⟩ := Finset.not_subset.mp hnotSK
  have hx0U : x0 ∈ U := hSU hx0S
  have hT0S : insert x0 K ⊆ S :=
    Finset.insert_subset_iff.mpr ⟨hx0S, hKS⟩
  have hT0card : (insert x0 K).card = κ + 1 := by
    rw [Finset.card_insert_of_notMem hx0K, hKcard]
  obtain ⟨⟨c0, hc0⟩, ⟨c1, hc1⟩⟩ :=
    hdeg (insert x0 K) hT0S hT0card
  have hb0 : inKernelSpanOn row S b0 := by
    refine ⟨c0, ?_⟩
    intro y hyS
    by_cases hyK : y ∈ K
    · exact hc0 y (Finset.mem_insert_of_mem hyK)
    · have hyU : y ∈ U := hSU hyS
      have hTyS : insert y K ⊆ S :=
        Finset.insert_subset_iff.mpr ⟨hyS, hKS⟩
      have hTycard : (insert y K).card = κ + 1 := by
        rw [Finset.card_insert_of_notMem hyK, hKcard]
      obtain ⟨d0, hd0⟩ := (hdeg (insert y K) hTyS hTycard).1
      have hcd : c0 = d0 := hmds K hKpow c0 d0 (by
        intro x hxK
        have hc := hc0 x (Finset.mem_insert_of_mem hxK)
        have hd := hd0 x (Finset.mem_insert_of_mem hxK)
        linear_combination hc - hd)
      simpa [hcd] using hd0 y (Finset.mem_insert_self y K)
  have hb1 : inKernelSpanOn row S b1 := by
    refine ⟨c1, ?_⟩
    intro y hyS
    by_cases hyK : y ∈ K
    · exact hc1 y (Finset.mem_insert_of_mem hyK)
    · have hyU : y ∈ U := hSU hyS
      have hTyS : insert y K ⊆ S :=
        Finset.insert_subset_iff.mpr ⟨hyS, hKS⟩
      have hTycard : (insert y K).card = κ + 1 := by
        rw [Finset.card_insert_of_notMem hyK, hKcard]
      obtain ⟨d1, hd1⟩ := (hdeg (insert y K) hTyS hTycard).2
      have hcd : c1 = d1 := hmds K hKpow c1 d1 (by
        intro x hxK
        have hc := hc1 x (Finset.mem_insert_of_mem hxK)
        have hd := hd1 x (Finset.mem_insert_of_mem hxK)
        linear_combination hc - hd)
      simpa [hcd] using hd1 y (Finset.mem_insert_self y K)
  exact htrans ⟨hb0, hb1⟩

/--
Field-independent transverse-secant count in kernel-row form. The certificate
premise is exactly the proof's nondegenerate-minor output: every slope admits a
transverse `(kappa+1)`-subset on which the moving line is consistent.
-/
theorem transverseSecant_card_le_of_kernel_certificate
    [DecidableEq Coord] {κ : ℕ}
    (U : Finset Coord) (row : Coord → Fin κ → F)
    (b0 b1 : Coord → F) (slopes : Finset F)
    (hcert : ∀ γ ∈ slopes,
      ∃ T ∈ U.powersetCard (κ + 1),
        transverseOn row T b0 b1 ∧ lineConsistentOn row T b0 b1 γ) :
    slopes.card ≤ Nat.choose U.card (κ + 1) := by
  classical
  let Slope := {γ : F // γ ∈ slopes}
  let Minor := {T : Finset Coord // T ∈ U.powersetCard (κ + 1)}
  letI : Fintype Minor :=
    Fintype.ofFinset (U.powersetCard (κ + 1)) (fun _ => Iff.rfl)
  have hcert' : ∀ γ : Slope,
      ∃ T : Minor,
        transverseOn row T.1 b0 b1 ∧ lineConsistentOn row T.1 b0 b1 γ.1 := by
    intro γ
    obtain ⟨T, hT, htrans, hline⟩ := hcert γ.1 γ.2
    exact ⟨⟨T, hT⟩, htrans, hline⟩
  choose charge htrans hline using hcert'
  have hinj : Function.Injective charge := by
    intro γ δ hcharge
    apply Subtype.ext
    have hT : (charge γ).1 = (charge δ).1 :=
      congrArg Subtype.val hcharge
    have htrans' := htrans γ
    have hγ := hline γ
    have hδ := hline δ
    rw [hT] at htrans' hγ
    exact lineConsistentOn_unique_of_transverse
      row (charge δ).1 b0 b1 htrans' hγ hδ
  have hcard : Fintype.card Slope ≤ Fintype.card Minor :=
    Fintype.card_le_of_injective charge hinj
  simpa [Slope, Minor] using hcard

/--
Fixed-chart balanced-core transverse-secant theorem. A source slope supplies a
transverse line-consistency set of size at least `κ+1`; the MDS kernel property
localizes it to a charged `(κ+1)`-subset, and root uniqueness makes the charge
injective.
-/
theorem transverseSecant_card_le_of_mds_source
    [DecidableEq Coord] {κ : ℕ}
    (U : Finset Coord) (row : Coord → Fin κ → F)
    (b0 b1 : Coord → F) (slopes : Finset F)
    (hmds : mdsKernelOn U row)
    (hsource : ∀ γ ∈ slopes,
      ∃ S : Finset Coord,
        S ⊆ U ∧ κ + 1 ≤ S.card ∧
          transverseOn row S b0 b1 ∧ lineConsistentOn row S b0 b1 γ) :
    slopes.card ≤ Nat.choose U.card (κ + 1) := by
  apply transverseSecant_card_le_of_kernel_certificate U row b0 b1 slopes
  intro γ hγ
  obtain ⟨S, hSU, hScard, hStrans, hSline⟩ := hsource γ hγ
  obtain ⟨T, hTpow, hTS, hTtrans⟩ :=
    exists_transverse_subset_of_mds U S row b0 b1 hSU hScard hmds hStrans
  refine ⟨T, hTpow, hTtrans, ?_⟩
  obtain ⟨c, hc⟩ := hSline
  exact ⟨c, fun x hx => hc x (hTS hx)⟩

/-- The source theorem's displayed cardinality when `#U = R+κ`. -/
theorem balancedCore_transverseSecant_card_le
    [DecidableEq Coord] {κ : ℕ}
    (U : Finset Coord) (R : ℕ) (row : Coord → Fin κ → F)
    (b0 b1 : Coord → F) (slopes : Finset F)
    (hU : U.card = R + κ)
    (hmds : mdsKernelOn U row)
    (hsource : ∀ γ ∈ slopes,
      ∃ S : Finset Coord,
        S ⊆ U ∧ κ + 1 ≤ S.card ∧
          transverseOn row S b0 b1 ∧ lineConsistentOn row S b0 b1 γ) :
    slopes.card ≤ Nat.choose (R + κ) (κ + 1) := by
  simpa [hU] using
    transverseSecant_card_le_of_mds_source U row b0 b1 slopes hmds hsource

/--
Source-shaped form. Each slope supplies an error support `E ⊆ U` of size at
most `t`, a kernel coefficient vector making the moving lift vanish on
`U \ E`, and transversality on that zero set. The inequalities
`#U = R+κ` and `t < R` force at least `κ+1` zero coordinates.
-/
theorem balancedCore_transverseSecant_card_le_of_supported_witness
    [DecidableEq Coord] {κ : ℕ}
    (U : Finset Coord) (R t : ℕ) (row : Coord → Fin κ → F)
    (b0 b1 : Coord → F) (slopes : Finset F)
    (hU : U.card = R + κ) (ht : t < R)
    (hmds : mdsKernelOn U row)
    (hwitness : ∀ γ ∈ slopes,
      ∃ E : Finset Coord, ∃ c : Fin κ → F,
        E ⊆ U ∧ E.card ≤ t ∧ transverseOn row (U \ E) b0 b1 ∧
          ∀ x ∈ U \ E,
            b0 x + γ * b1 x + kernelDot row x c = 0) :
    slopes.card ≤ Nat.choose (R + κ) (κ + 1) := by
  apply balancedCore_transverseSecant_card_le U R row b0 b1 slopes hU hmds
  intro γ hγ
  obtain ⟨E, c, hEU, hEcard, htrans, hline⟩ := hwitness γ hγ
  refine ⟨U \ E, Finset.sdiff_subset, ?_, htrans, ⟨c, hline⟩⟩
  have hEUcard : E.card ≤ U.card := Finset.card_le_card hEU
  rw [Finset.card_sdiff, Finset.inter_eq_left.mpr hEU, hU]
  omega

#print axioms affineSecant_root_unique
#print axioms slope_card_le_choose_of_affine_charge
#print axioms transverseSecant_card_le
#print axioms singleCircuit_card_le
#print axioms lineConsistentOn_unique_of_transverse
#print axioms transverseSecant_card_le_of_kernel_certificate
#print axioms exists_transverse_subset_of_mds
#print axioms transverseSecant_card_le_of_mds_source
#print axioms balancedCore_transverseSecant_card_le
#print axioms balancedCore_transverseSecant_card_le_of_supported_witness

end SyndromeSecant.BalancedCoreTransverseSecant
