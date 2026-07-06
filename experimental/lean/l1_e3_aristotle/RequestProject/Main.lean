import Mathlib

open scoped BigOperators
open scoped Classical
open Polynomial

set_option maxHeartbeats 4000000

/-!
# A level-set inequality for a low-degree polynomial on multiplicative cosets

Let `p` be a prime and `ℓ` an odd prime with `ℓ ∣ p - 1`.  Work in the field `𝔽_p = ZMod p`.
The multiplicative group `𝔽_p^*` is partitioned into `n = (p-1)/ℓ` cosets of the subgroup
`μ_ℓ` of `ℓ`-th roots of unity; each coset is a fiber of `x ↦ x^ℓ` and has exactly `ℓ`
elements sharing one value `w = x^ℓ`.

For a nonzero polynomial `Γ` with no constant term and `deg Γ ≤ ℓ - 1`, and each coset `C`
(indexed by its common power `w`), we set

  `μ(C) := max_{λ} #{ x ∈ C : Γ(x) = λ }`   (so `1 ≤ μ(C) ≤ ℓ`),

and define

  `E₃ := Σ_C (μ(C) - 2)`   (truncated `ℕ`-subtraction realises `(·)_+`).

The theorem to prove is `E₃ ≤ ℓ - 2`.
-/

namespace CosetLevelSet

variable {p ℓ : ℕ} [Fact p.Prime]

/-- The coset of `𝔽_p^*` consisting of the nonzero `x` with `x ^ ℓ = w`
(a fiber of `x ↦ x ^ ℓ`). -/
def cosetF (p ℓ : ℕ) [Fact p.Prime] (w : ZMod p) : Finset (ZMod p) :=
  Finset.univ.filter (fun x => x ≠ 0 ∧ x ^ ℓ = w)

/-- `μ(C)`: the maximal level-set size of `Γ` on the coset with power `w`, i.e.
`max_{λ} #{ x ∈ C : Γ(x) = λ }`. -/
noncomputable def levelMax (p ℓ : ℕ) [Fact p.Prime] (Γ : (ZMod p)[X]) (w : ZMod p) : ℕ :=
  Finset.univ.sup (fun lam : ZMod p =>
    ((cosetF p ℓ w).filter (fun x => Γ.eval x = lam)).card)

/-- The set of nonzero `ℓ`-th powers, i.e. the set of common values `w = x^ℓ`
indexing the cosets. -/
def powersF (p ℓ : ℕ) [Fact p.Prime] : Finset (ZMod p) :=
  (Finset.univ.filter (fun x : ZMod p => x ≠ 0)).image (fun x => x ^ ℓ)

/-- `E₃ := Σ_C (μ(C) - 2)_+` over all cosets `C` (indexed by nonzero `ℓ`-th powers `w`);
truncated `ℕ`-subtraction realises the positive part. -/
noncomputable def E3 (p ℓ : ℕ) [Fact p.Prime] (Γ : (ZMod p)[X]) : ℕ :=
  ∑ w ∈ powersF p ℓ, (levelMax p ℓ Γ w - 2)

/-- The level-set maximum on any coset is at most the size of the coset. -/
lemma levelMax_le_card (Γ : (ZMod p)[X]) (w : ZMod p) :
    levelMax p ℓ Γ w ≤ (cosetF p ℓ w).card := by
  unfold levelMax
  refine Finset.sup_le ?_
  intro lam _
  exact Finset.card_filter_le _ _

/-- A coset (a fiber of `x ↦ x ^ ℓ`) has at most `ℓ` elements: it is contained in the
root set of `X ^ ℓ - w`, a nonzero polynomial of degree `ℓ`.
-/
lemma card_cosetF_le (hℓ : 0 < ℓ) (w : ZMod p) :
    (cosetF p ℓ w).card ≤ ℓ := by
  refine' le_trans ( Finset.card_le_card _ ) _;
  exact ( Polynomial.roots ( Polynomial.X ^ ℓ - Polynomial.C w ) |> Multiset.toFinset );
  · intro x hx; simp_all +decide [ cosetF ] ;
    exact ne_of_apply_ne Polynomial.natDegree ( by rw [ Polynomial.natDegree_sub_C ] ; aesop );
  · exact le_trans ( Multiset.toFinset_card_le _ ) ( le_trans ( Polynomial.card_roots' _ ) ( by erw [ Polynomial.natDegree_X_pow_sub_C ] ) )

/-- The level-set maximum on any coset is at most `ℓ`. -/
lemma levelMax_le_ell (hℓ : 0 < ℓ) (Γ : (ZMod p)[X]) (w : ZMod p) :
    levelMax p ℓ Γ w ≤ ℓ :=
  (levelMax_le_card Γ w).trans (card_cosetF_le hℓ w)

/-- Each nonempty fiber of `x ↦ x ^ ℓ` (a coset indexed by a nonzero `ℓ`-th power `w`)
has exactly `ℓ` elements. -/
lemma card_cosetF_eq (hdvd : ℓ ∣ p - 1) {w : ZMod p}
    (hw : w ∈ powersF p ℓ) : (cosetF p ℓ w).card = ℓ := by
  obtain ⟨x₀, hx₀⟩ : ∃ x₀ : ZMod p, x₀ ≠ 0 ∧ x₀ ^ ℓ = w := by
    unfold powersF at hw; aesop
  have h_bij : (Finset.image (fun ζ : ZMod p => x₀ * ζ) (Finset.filter (fun ζ => ζ ≠ 0 ∧ ζ ^ ℓ = 1) Finset.univ)) = cosetF p ℓ w := by
    ext; simp
    constructor <;> intro h <;> simp_all +decide [ cosetF ]
    · rcases h with ⟨ a, ⟨ ha₁, ha₂ ⟩, rfl ⟩ ; simp_all +decide [ mul_pow ]
    · refine' ⟨ ‹_› / x₀, _, _ ⟩ <;> simp_all +decide [ mul_div_cancel₀ ]
      rw [ div_pow, h.2, hx₀.2, div_self ] ; aesop
  have h_card_R : (Finset.filter (fun ζ : (ZMod p)ˣ => ζ ^ ℓ = 1) Finset.univ).card = ℓ := by
    have h_card_R : (Finset.filter (fun ζ : (ZMod p)ˣ => ζ ^ ℓ = 1) Finset.univ).card = Nat.gcd ℓ (Nat.card (ZMod p)ˣ) := by
      have h_card_R : ∀ {G : Type} [CommGroup G] [IsCyclic G] [Fintype G], (Finset.filter (fun ζ : G => ζ ^ ℓ = 1) Finset.univ).card = Nat.gcd ℓ (Nat.card G) := by
        intros G _ _ _; exact (by
        have := @IsCyclic.card_orderOf_eq_totient G
        have h_card_R : (Finset.filter (fun ζ : G => ζ ^ ℓ = 1) Finset.univ).card = ∑ d ∈ Nat.divisors (Nat.gcd ℓ (Nat.card G)), (Finset.filter (fun ζ : G => orderOf ζ = d) Finset.univ).card := by
          rw [ ← Finset.card_biUnion ]
          · congr with x ; simp +decide [ orderOf_dvd_iff_pow_eq_one ]
          · exact fun x hx y hy hxy => Finset.disjoint_left.mpr fun z hz₁ hz₂ => hxy <| by aesop
        simp_all +decide [ Nat.card_eq_fintype_card ]
        rw [ Finset.sum_congr rfl fun x hx => this <| Nat.dvd_trans ( Nat.dvd_of_mem_divisors hx ) <| Nat.gcd_dvd_right _ _ ] ; simp +decide [ Nat.sum_totient ])
      grind
    simp_all +decide [ Nat.card_eq_fintype_card ]
    exact Nat.gcd_eq_left ( by simpa [ Nat.totient_prime Fact.out ] using hdvd )
  rw [ ← h_bij, Finset.card_image_of_injective _ fun a b h => mul_left_cancel₀ hx₀.1 h ]
  convert h_card_R using 1
  refine' Finset.card_bij ( fun x hx => Units.mk0 x ( by aesop ) ) _ _ _ <;> simp +decide [ Units.ext_iff ]

/-- There are exactly `n = (p - 1)/ℓ` cosets (nonzero `ℓ`-th powers). -/
lemma card_powersF (hdvd : ℓ ∣ p - 1) :
    (powersF p ℓ).card = (p - 1) / ℓ := by
  -- The image of the power map on the nonzero elements of $ZMod p$ is exactly the set of nonzero $\ell$-th powers.
  have h_image : (powersF p ℓ) = Finset.image (fun x : (ZMod p)ˣ => (x : ZMod p) ^ ℓ) (Finset.univ : Finset (ZMod p)ˣ) := by
    ext; simp [powersF];
    constructor <;> rintro ⟨ a, ha ⟩;
    · exact ⟨ Units.mk0 a ha.1, by simpa [ Units.ext_iff ] using ha.2 ⟩;
    · exact ⟨ a, by simp, ha ⟩;
  -- The size of the image of the power map on the units is equal to the size of the group divided by the gcd of the group order and the exponent.
  have h_card_image : (Finset.image (fun x : (ZMod p)ˣ => x ^ ℓ) (Finset.univ : Finset (ZMod p)ˣ)).card = (Nat.card (ZMod p)ˣ) / Nat.gcd (Nat.card (ZMod p)ˣ) ℓ := by
    convert IsCyclic.card_powMonoidHom_range ( ZMod p )ˣ ℓ using 1;
    rw [ ← Nat.card_eq_finsetCard ] ; congr ; aesop;
  convert h_card_image using 1;
  · convert Finset.card_image_of_injective _ ( show Function.Injective ( fun x : ( ZMod p ) ˣ => ( x : ZMod p ) ) from fun a b h => by simpa [ Units.ext_iff ] using h ) using 1;
    convert congr_arg Finset.card h_image using 2 ; ext ; aesop;
  · simp +decide [ Nat.totient_prime Fact.out, Nat.gcd_eq_right hdvd ]

/-- **Main theorem.** `E₃ ≤ ℓ - 2`.

Status: the statement is fully formalised and validated computationally (see `NOTES.md`).
The proof reduces (see `NOTES.md`) to the *degree-bounded syzygy* crux
`dim (V_1 + ⋯ + V_K) ≥ E₃`, which the accompanying problem description itself flags as
open.  It is genuinely a global fact about a single polynomial `Γ`: the analogous claim
for arbitrary pairwise-coprime co-fibre locators is FALSE (a rank–nullity counterexample
is recorded in `NOTES.md`).  A complete Lean proof of this crux is not yet available, so
the main inequality is left as `sorry`; all surrounding setup and the partition-structure
lemmas (`card_cosetF_le`, `card_cosetF_eq`, `card_powersF`, `levelMax_le_ell`) are proved. -/
theorem E3_le (hℓ : ℓ.Prime) (hodd : Odd ℓ) (hdvd : ℓ ∣ p - 1)
    (Γ : (ZMod p)[X]) (hΓ : Γ ≠ 0) (hc0 : Γ.coeff 0 = 0) (hdeg : Γ.natDegree ≤ ℓ - 1) :
    E3 p ℓ Γ ≤ ℓ - 2 := by
  sorry

end CosetLevelSet