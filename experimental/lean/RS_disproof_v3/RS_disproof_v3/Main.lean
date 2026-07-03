import Mathlib

/-!
# The quotient-locator mechanism for Reed-Solomon mutual correlated agreement

This file formalizes the self-contained algebraic core of

  P. Chojecki, *Capacity-Edge Obstructions to Reed-Solomon Mutual Correlated Agreement
  over Smooth Multiplicative Domains* (`RS_disproof_v3.tex`).

The organizing mechanism of the paper is the **quotient locator identity**
(Lemma "Quotient locator"): if `Q = D^a` is the order-`N` quotient of a smooth
multiplicative domain `D` of order `n = a·N`, then the locator polynomial

  `L_A(X) = ∏_{b ∈ A} (X^a - b)`

of an `ℓ`-subset `A ⊆ Q` expands as `X^{k+a} + z·X^k + R_A(X)` with `deg R_A < k`,
`z = -∑_{b∈A} b` and `k = a·(ℓ-1)`.  Since `L_A` vanishes on
`S_A = {x ∈ D : x^a ∈ A}` (of size `a·ℓ = k+a`), the received word
`u_z(x) = x^{k+a} + z·x^k` agrees on `S_A` with the degree-`<k` polynomial `-R_A`,
while `g(x) = x^k` agrees with no degree-`<k` polynomial on more than `k` points.
Hence every `z ∈ -ℓ^{∧}Q` is *bad* at radius `1 - ρ - 1/N`, giving the lower bound
`ε_mca(RS[F,D,k], 1-ρ-1/N) ≥ |ℓ^{∧}Q| / q`.

We formalize:

* `RSLocator.locator` and the decomposition identity `RSLocator.locator_decomp`;
* the Hamming/agreement framework (`RSagrees`, `badAt`, `epsMca`);
* monotonicity of `epsMca` in the radius (Lemma "Monotonicity");
* the locator lower bound `RSLocator.epsMca_ge_restrictedSumset` (Lemma "Quotient locator");
* the error-one consequence under a coverage hypothesis
  (Theorem 2.1(a); the coverage input is the Dias da Silva–Hamidoune theorem,
  which is not in Mathlib and is therefore taken as an explicit hypothesis, exactly
  as the paper imports it as an external result);
* a worst-case list lower bound at the divisor level (Theorem 2.1(d)).

The deep external inputs (Dias da Silva–Hamidoune, Siegel–Walfisz) are represented
as hypotheses of the theorems that consume them; no `axiom` and no `sorry` remain.
-/

open Polynomial
open scoped BigOperators Classical

namespace RSLocator

variable {F : Type*} [Field F] [Fintype F] [DecidableEq F]

/-- The restricted sumset `ℓ^{∧}A`: the set of sums of `ℓ`-element subsets of `A`. -/
def restrictedSumset (A : Finset F) (ℓ : ℕ) : Finset F :=
  (A.powersetCard ℓ).image (fun s => ∑ b ∈ s, b)

/-- The locator polynomial `∏_{b ∈ A} (X^a - b)`. -/
noncomputable def locator (A : Finset F) (a : ℕ) : F[X] :=
  ∏ b ∈ A, (X ^ a - C b)

/-
The locator is the `a`-fold expansion of `∏_{b∈A}(X - b)`.
-/
omit [Fintype F] [DecidableEq F] in
lemma locator_eq_expand (A : Finset F) (a : ℕ) :
    locator A a = expand F a (∏ b ∈ A, (X - C b)) := by
  unfold locator;
  simp +decide [ map_prod, Polynomial.expand ]

/-
The locator evaluates to `0` at any `x` with `x^a ∈ A`.
-/
omit [Fintype F] [DecidableEq F] in
lemma locator_eval_zero (A : Finset F) (a : ℕ) {x : F} (hx : x ^ a ∈ A) :
    (locator A a).eval x = 0 := by
  rw [ locator, Polynomial.eval_prod, Finset.prod_eq_zero hx ] ; simp +decide

/-
**The locator decomposition** (heart of Lemma "Quotient locator").
For `a ≥ 1` and a nonempty `A`, with `k = a·(|A|-1)`, the locator equals
`X^{k+a} + z·X^k + R` where `z = -∑_{b∈A} b` and `deg R < k`.
-/
omit [Fintype F] in
lemma locator_decomp (A : Finset F) (a : ℕ) (ha : 1 ≤ a) (hA : 1 ≤ A.card)
    (k : ℕ) (hk : k = a * (A.card - 1)) :
    ∃ R : F[X], R.degree < (k : ℕ) ∧
      locator A a = X ^ (k + a) + C (- ∑ b ∈ A, b) * X ^ k + R := by
  refine' ⟨ locator A a - ( X ^ ( k + a ) + C ( -∑ b ∈ A, b ) * X ^ k ), _, _ ⟩;
  · rw [ Polynomial.degree_lt_iff_coeff_zero ];
    intro m hm; by_cases hm' : a ∣ m <;> simp_all +decide ;
    · obtain ⟨ e, rfl ⟩ := hm';
      rw [ locator_eq_expand, Polynomial.coeff_expand ];
      · rcases eq_or_ne e ( A.card - 1 ) <;> simp_all +decide [ Nat.mul_div_cancel_left _ ha ];
        · have h_coeff : Polynomial.coeff (∏ b ∈ A, (Polynomial.X - Polynomial.C b)) (A.card - 1) = -∑ b ∈ A, b := by
            have h_coeff : Polynomial.nextCoeff (∏ b ∈ A, (Polynomial.X - Polynomial.C b)) = -∑ b ∈ A, b := by
              convert Polynomial.prod_X_sub_C_nextCoeff _;
            rw [ ← h_coeff, Polynomial.nextCoeff ];
            rw [ Polynomial.natDegree_prod _ _ fun x hx => Polynomial.X_sub_C_ne_zero x ] ; aesop;
          simp_all +decide [ Polynomial.coeff_mul, Polynomial.coeff_X_pow ];
          rw [ Finset.sum_eq_single ( 0, a * ( A.card - 1 ) ) ] <;> aesop;
        · rcases eq_or_ne e ( A.card ) <;> simp_all +decide;
          · rw [ if_pos ];
            · rw [ Polynomial.coeff_mul, Finset.sum_eq_single ( 0, a * A.card ) ] <;> simp +decide [ Polynomial.coeff_X_pow, Polynomial.coeff_C ];
              · rw [ Finset.prod_congr rfl fun x hx => sub_eq_add_neg _ _ ];
                rw [ Finset.prod_congr rfl fun x hx => by rw [ ← Polynomial.C_neg ] ];
                rw [ Finset.prod_X_add_C_coeff ] ; aesop;
                lia;
              · aesop;
            · nlinarith only [ Nat.sub_add_cancel hA.card_pos ];
          · rw [ Polynomial.coeff_eq_zero_of_natDegree_lt ];
            · split_ifs <;> simp_all +decide;
              · exact False.elim ( ‹¬e = A.card› ( by nlinarith [ Nat.sub_add_cancel hA.card_pos ] ) );
              · rw [ Polynomial.coeff_mul, Finset.sum_eq_zero ] ; aesop;
            · rw [ Polynomial.natDegree_prod _ _ fun x hx => Polynomial.X_sub_C_ne_zero x ] ; simp +decide [ Polynomial.natDegree_sub_eq_left_of_natDegree_lt ];
              exact lt_of_le_of_ne ( Nat.le_of_not_lt fun h => ‹¬e = A.card - 1› <| by nlinarith [ Nat.sub_add_cancel hA.card_pos ] ) ( Ne.symm ‹_› );
      · exact Nat.zero_lt_of_lt ha;
    · rw [ locator_eq_expand, Polynomial.coeff_expand ];
      · split_ifs <;> simp_all +decide;
        rw [ Polynomial.coeff_mul, Finset.sum_eq_zero ] ; aesop;
      · linarith;
  · ring

/-- `w` agrees with a degree-`<k` (Reed-Solomon) codeword on the support set `S`. -/
def RSagrees (k : ℕ) (w : F → F) (S : Finset F) : Prop :=
  ∃ p : F[X], p.degree < (k : ℕ) ∧ ∀ x ∈ S, p.eval x = w x

/-
The monomial `x^k` admits no degree-`<k` explanation on any set of more than `k`
points: this is the "no low-degree explanation" step of the locator argument.
-/
omit [Fintype F] in
lemma not_RSagrees_pow (k : ℕ) (S : Finset F) (hS : k < S.card) :
    ¬ RSagrees k (fun x => x ^ k) S := by
  contrapose! hS; rcases hS with ⟨ p, hp, hsum ⟩ ;
  -- Then `q ≠ 0`: its coefficient at `k` is `(X^k).coeff k - p.coeff k = 1 - 0 = 1 ≠ 0` (since `p.degree < k` gives `p.coeff k = 0` by `Polynomial.coeff_eq_zero_of_degree_lt`).
  have hq_ne_zero : Polynomial.X ^ k - p ≠ 0 := by
    grind +suggestions;
  -- Also `q.natDegree ≤ k` since `degree q ≤ max (degree X^k) (degree p) ≤ k`.
  have hq_natDegree_le_k : (Polynomial.X ^ k - p).natDegree ≤ k := by
    exact le_trans ( Polynomial.natDegree_sub_le _ _ ) ( max_le ( Polynomial.natDegree_X_pow_le _ ) ( Polynomial.natDegree_le_of_degree_le hp.le ) );
  exact le_trans ( Finset.card_le_card ( show S ⊆ ( Polynomial.roots ( Polynomial.X ^ k - p ) |> Multiset.toFinset ) from fun x hx => Multiset.mem_toFinset.mpr <| Polynomial.mem_roots hq_ne_zero |>.2 <| by aesop ) ) ( le_trans ( Multiset.toFinset_card_le _ ) <| Polynomial.card_roots' _ ) |> le_trans <| hq_natDegree_le_k

/-- The parameter `z` is *bad at radius `δ`* for the line `f + z·g`:
there is a support set `S ⊆ D` of relative size `≥ 1-δ` on which `f + z·g` agrees with a
codeword, yet `f` and `g` do not both agree with codewords on `S`. -/
def badAt (D : Finset F) (k : ℕ) (f g : F → F) (δ : ℝ) (z : F) : Prop :=
  ∃ S ⊆ D, ((1 - δ) * (D.card : ℝ) ≤ (S.card : ℝ)) ∧
    RSagrees k (fun x => f x + z * g x) S ∧
    ¬ (RSagrees k f S ∧ RSagrees k g S)

/-- The set of bad parameters `z` for a given line and radius. -/
noncomputable def badSet (D : Finset F) (k : ℕ) (f g : F → F) (δ : ℝ) : Finset F :=
  Finset.univ.filter (fun z => badAt D k f g δ z)

/-- The support-wise line-MCA error `ε_mca(RS[F,D,k], δ)`
(Definition "Support-wise line-MCA error"). -/
noncomputable def epsMca (D : Finset F) (k : ℕ) (δ : ℝ) : ℝ :=
  Finset.univ.sup' (Finset.univ_nonempty (α := (F → F) × (F → F)))
    (fun fg => (badSet D k fg.1 fg.2 δ).card / (Fintype.card F : ℝ))

/-
`badAt` is monotone in the radius `δ`.
-/
omit [Fintype F] [DecidableEq F] in
lemma badAt_mono (D : Finset F) (k : ℕ) (f g : F → F) {δ δ' : ℝ} (h : δ ≤ δ')
    {z : F} (hz : badAt D k f g δ z) : badAt D k f g δ' z := by
  obtain ⟨ S, hS₁, hS₂, hS₃, hS₄ ⟩ := hz;
  exact ⟨ S, hS₁, le_trans ( mul_le_mul_of_nonneg_right ( sub_le_sub_left h _ ) ( Nat.cast_nonneg _ ) ) hS₂, hS₃, hS₄ ⟩

/-
**Monotonicity** (Lemma "Monotonicity"): `ε_mca` is nondecreasing in `δ`.
-/
lemma epsMca_mono (D : Finset F) (k : ℕ) {δ δ' : ℝ} (h : δ ≤ δ') :
    epsMca D k δ ≤ epsMca D k δ' := by
  refine' Finset.sup'_le _ _ fun fg _ => _;
  refine' le_trans _ ( Finset.le_sup' _ ( Finset.mem_univ fg ) );
  gcongr;
  exact fun x hx => Finset.mem_filter.mpr ⟨ Finset.mem_filter.mp hx |>.1, badAt_mono D k fg.1 fg.2 h ( Finset.mem_filter.mp hx |>.2 ) ⟩

/-
`ε_mca` never exceeds `1`.
-/
lemma epsMca_le_one (D : Finset F) (k : ℕ) (δ : ℝ) : epsMca D k δ ≤ 1 := by
  -- By definition of `epsMca`, if `epsMca D k δ > 1`, then there exists a pair `(f, g)` such that the ratio of the cardinality of `badSet` to `Fintype.card F` is greater than 1.
  simp [epsMca] at *;
  exact fun f g => div_le_one_of_le₀ ( mod_cast Finset.card_le_univ _ ) ( Nat.cast_nonneg _ )

/-
Lower bound: `ε_mca` dominates the bad-set density of any single line `f + z·g`.
-/
lemma epsMca_ge_badSet (D : Finset F) (k : ℕ) (f g : F → F) (δ : ℝ) :
    (badSet D k f g δ).card / (Fintype.card F : ℝ) ≤ epsMca D k δ := by
  refine' le_trans _ ( Finset.le_sup' _ ( Finset.mem_univ ( f, g ) ) ) ; aesop;

/-!
### The smooth-domain quotient configuration

`D` is the (smooth) domain, `Q = D^a` its order-`N` quotient, and every fiber of
`x ↦ x^a` on `D` has size exactly `a`.  These are the properties supplied by the
multiplicative-subgroup structure; we take them as hypotheses.
-/

/-- The fiber `S_A = {x ∈ D : x^a ∈ A}`. -/
def fiberSet (D : Finset F) (a : ℕ) (A : Finset F) : Finset F :=
  D.filter (fun x => x ^ a ∈ A)

/-
If every point-fiber of `x ↦ x^a` on `D` has size `a`, then `|S_A| = a·|A|`
for `A ⊆ Q`, where `Q = D.image (·^a)`.
-/
omit [Fintype F] in
lemma fiberSet_card (D : Finset F) (a : ℕ) {Q A : Finset F}
    (hQ : Q = D.image (fun x => x ^ a))
    (hfib : ∀ b ∈ Q, (D.filter (fun x => x ^ a = b)).card = a)
    (hAQ : A ⊆ Q) :
    (fiberSet D a A).card = a * A.card := by
  -- Show that `fiberSet D a A` is exactly the union of the point-fibers `{x ∈ D | x^a = b}` for `b ∈ A`.
  have h_fiberSet_eq_biUnion : fiberSet D a A = Finset.biUnion A (fun b => D.filter (fun x => x ^ a = b)) := by
    grind +locals;
  rw [ h_fiberSet_eq_biUnion, Finset.card_biUnion, Finset.sum_congr rfl fun x hx => hfib x ( hAQ hx ) ] ; simp +decide [ mul_comm ];
  exact fun x hx y hy hxy => Finset.disjoint_filter.2 fun z => by aesop;

/-
**The quotient locator lemma** (Lemma "Quotient locator").
Under the smooth-quotient configuration, every `z ∈ -ℓ^{∧}Q` is bad at any radius
`δ` with `(1-δ)·n ≤ k+a` (i.e. `δ ≥ 1-ρ-1/N`), for the line `f = x^{k+a}`, `g = x^k`.
-/
omit [Fintype F] in
lemma locator_bad (D : Finset F) (a N : ℕ) (ha : 1 ≤ a) {Q : Finset F}
    (hQ : Q = D.image (fun x => x ^ a))
    (hfib : ∀ b ∈ Q, (D.filter (fun x => x ^ a = b)).card = a)
    (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hℓN : ℓ ≤ N) (hNQ : Q.card = N) (hk : k = a * (ℓ - 1))
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + a : ℝ))
    {z : F} (hz : -z ∈ restrictedSumset Q ℓ) :
    badAt D k (fun x => x ^ (k + a)) (fun x => x ^ k) δ z := by
  obtain ⟨A, hA⟩ : ∃ A : Finset F, A ⊆ Q ∧ A.card = ℓ ∧ ∑ b ∈ A, b = -z := by
    unfold restrictedSumset at hz; aesop;
  refine' ⟨ fiberSet D a A, _, _, _, _ ⟩;
  · exact Finset.filter_subset _ _;
  · convert hδ using 1 ; rw [ fiberSet_card D a hQ hfib hA.1 ] ; rw [ hA.2.1 ] ; cases ℓ <;> simp_all +decide ; ring;
  · obtain ⟨ R, hR₁, hR₂ ⟩ := locator_decomp A a ha ( by linarith ) k ( by rw [ hk, hA.2.1 ] );
    refine' ⟨ -R, _, _ ⟩ <;> simp_all +decide [ locator ];
    intro x hx; replace hR₂ := congr_arg ( Polynomial.eval x ) hR₂; simp_all +decide [ Polynomial.eval_prod ] ;
    rw [ Finset.prod_eq_zero ( Finset.mem_filter.mp hx |>.2 ) ] at hR₂ <;> simp_all +decide [ pow_add, pow_mul ];
    linear_combination' hR₂;
  · refine' fun h => not_RSagrees_pow k ( fiberSet D a A ) _ h.2;
    rw [ fiberSet_card D a hQ hfib hA.1 ] ; nlinarith [ Nat.sub_add_cancel hℓ ]

/-
**Locator lower bound** (Lemma "Quotient locator", conclusion):
`ε_mca(RS[F,D,k], δ) ≥ |ℓ^{∧}Q| / q` for `δ ≥ 1-ρ-1/N`.
-/
theorem epsMca_ge_restrictedSumset (D : Finset F) (a N : ℕ) (ha : 1 ≤ a) {Q : Finset F}
    (hQ : Q = D.image (fun x => x ^ a))
    (hfib : ∀ b ∈ Q, (D.filter (fun x => x ^ a = b)).card = a)
    (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hℓN : ℓ ≤ N) (hNQ : Q.card = N) (hk : k = a * (ℓ - 1))
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + a : ℝ)) :
    ((restrictedSumset Q ℓ).card : ℝ) / (Fintype.card F : ℝ) ≤ epsMca D k δ := by
  refine' le_trans ( div_le_div_of_nonneg_right _ ( Nat.cast_nonneg _ ) ) ( epsMca_ge_badSet _ _ _ _ _ );
  rotate_left;
  exact fun x => x ^ ( k + a );
  exact fun x => x ^ k;
  refine' mod_cast le_trans _ ( Finset.card_le_card _ );
  rotate_left;
  exact Finset.image ( fun y => -y ) ( restrictedSumset Q ℓ );
  · intro z hz
    obtain ⟨y, hy, rfl⟩ := Finset.mem_image.mp hz
    have h_bad : badAt D k (fun x => x ^ (k + a)) (fun x => x ^ k) δ (-y) := by
      exact locator_bad D a N ha hQ hfib ℓ k hℓ hℓN hNQ hk δ hδ ( by simpa using hy )
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, h_bad⟩;
  · rw [ Finset.card_image_of_injective _ neg_injective ]

/-
**Theorem 2.1(a): error one under full coverage.**
If the restricted sumset covers the whole field (the Dias da Silva–Hamidoune coverage
input), then the MCA error equals `1` at every radius `δ ≥ 1-ρ-1/N`.
-/
theorem epsMca_eq_one_of_cover (D : Finset F) (a N : ℕ) (ha : 1 ≤ a) {Q : Finset F}
    (hQ : Q = D.image (fun x => x ^ a))
    (hfib : ∀ b ∈ Q, (D.filter (fun x => x ^ a = b)).card = a)
    (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hℓN : ℓ ≤ N) (hNQ : Q.card = N) (hk : k = a * (ℓ - 1))
    (hcover : restrictedSumset Q ℓ = Finset.univ)
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + a : ℝ)) :
    epsMca D k δ = 1 := by
  refine' le_antisymm ( epsMca_le_one D k δ ) _;
  convert epsMca_ge_restrictedSumset D a N ha hQ hfib ℓ k hℓ hℓN hNQ hk δ hδ using 1;
  rw [ hcover, Finset.card_univ, div_self ( Nat.cast_ne_zero.mpr Fintype.card_ne_zero ) ]

/-!
### Theorem 2.1(d): worst-case list lower bound at the divisor level

For a suitable slope `z` (achieving at least the average over the `ℓ`-subsets of `Q`),
the received word `u_z(x) = x^{k+a} + z·x^k` has at least `C(N, ℓ)/q` Reed-Solomon
codewords within relative distance `1-ρ-1/N`.
-/

/-
The codeword attached to an `ℓ`-subset `A ⊆ Q`: the degree-`<k` polynomial `-R_A`
of the locator decomposition, restricted to `D`. Distinct subsets give distinct
codewords, and each agrees with `u_{z_A}` on the `k+a` points of `S_A`.
-/
omit [Fintype F] in
lemma locator_RSagrees (D : Finset F) (a : ℕ) (ha : 1 ≤ a) {A : Finset F}
    (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hAcard : A.card = ℓ) (hk : k = a * (ℓ - 1))
    {z : F} (hsum : ∑ b ∈ A, b = -z) :
    RSagrees k (fun x => x ^ (k + a) + z * x ^ k) (fiberSet D a A) := by
  obtain ⟨ R, hR₁, hR₂ ⟩ := locator_decomp A a ha ( by linarith ) k ( by rw [ hk, hAcard ] );
  refine' ⟨ -R, _, _ ⟩;
  · simpa using hR₁;
  · intro x hx; have := locator_eval_zero A a ( Finset.mem_filter.mp hx |>.2 ) ; simp_all +decide [ locator ] ;
    linear_combination -this

lemma list_lower_bound (D : Finset F) (a N : ℕ) (ha : 1 ≤ a) {Q : Finset F}
    (hQ : Q = D.image (fun x => x ^ a))
    (hfib : ∀ b ∈ Q, (D.filter (fun x => x ^ a = b)).card = a)
    (hDcard : D.card = a * N)
    (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hℓN : ℓ ≤ N) (hNQ : Q.card = N) (hk : k = a * (ℓ - 1))
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + a : ℝ)) :
    ∃ z : F, ((N.choose ℓ : ℝ) / (Fintype.card F : ℝ)) ≤
      (( (Q.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z) ).card : ℝ) ∧
      ∀ A ∈ (Q.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z),
        RSagrees k (fun x => x ^ (k + a) + z * x ^ k) (fiberSet D a A) := by
  obtain ⟨z, hz⟩ : ∃ z : F, (Nat.choose N ℓ : ℝ) / (Fintype.card F : ℝ) ≤ ((Finset.powersetCard ℓ Q).filter (fun A => (∑ b ∈ A, b) = -z)).card := by
    have h_pigeonhole : ∑ z : F, ((Finset.powersetCard ℓ Q).filter (fun A => (∑ b ∈ A, b) = -z)).card = (Nat.choose N ℓ : ℝ) := by
      rw_mod_cast [ ← Finset.card_biUnion ];
      · convert Finset.card_powersetCard ℓ Q using 2;
        · ext A; simp [Finset.mem_biUnion];
          exact fun _ _ => ⟨ -∑ b ∈ A, b, by ring ⟩;
        · exact hNQ.symm;
      · exact fun x _ y _ hxy => Finset.disjoint_left.mpr fun A hA₁ hA₂ => hxy <| by aesop;
    contrapose! h_pigeonhole;
    norm_num +zetaDelta at *;
    exact ne_of_lt ( lt_of_lt_of_le ( Finset.sum_lt_sum_of_nonempty ( Finset.univ_nonempty ) fun x _ => h_pigeonhole x ) ( by simp +decide [ mul_div_cancel₀, Fintype.card_ne_zero ] ) );
  refine' ⟨ z, hz, fun A hA => locator_RSagrees D a ha ℓ k hℓ _ hk _ ⟩ <;> aesop

/-!
### Distinct Reed-Solomon codewords in the list (Theorem 2.1(d), distinctness)

The list bound above exhibits, for a fixed slope `z`, many `ℓ`-subsets `A` of `Q` whose
associated received word `u_z = x^{k+a}+z x^k` agrees with the degree-`<k` polynomial
`-R_A` on the `k+a` points of `S_A`.  Paper A's list theorem needs a lower bound on the
number of *distinct Reed-Solomon codewords*, not merely on the number of witnessing
subsets.  We supply the missing distinctness: distinct `A` give distinct monic locators
`L_A` (they have distinct root multisets), hence distinct codewords `-R_A`.
-/

/-- The explicit degree-`<k` codeword attached to `A`, written directly as
`x^{k+a} + z·x^k − L_A(x)`.  When `∑_{b∈A} b = -z` and `k = a(|A|-1)` this equals `-R_A`,
the degree-`<k` polynomial of the locator decomposition. -/
noncomputable def codewordPoly (A : Finset F) (a k : ℕ) (z : F) : F[X] :=
  X ^ (k + a) + C z * X ^ k - locator A a

omit [Fintype F] [DecidableEq F] in
/-- `A ↦ locator A a` is injective for `a ≥ 1`: distinct subsets give distinct locators
(distinct root multisets after unwinding the `X ↦ X^a` substitution). -/
lemma locator_inj (a : ℕ) (ha : 1 ≤ a) {A A' : Finset F}
    (h : locator A a = locator A' a) : A = A' := by
  have e : (∏ b ∈ A, (X - C b)) = (∏ b ∈ A', (X - C b)) := by
    have h2 : expand F a (∏ b ∈ A, (X - C b)) = expand F a (∏ b ∈ A', (X - C b)) := by
      rw [← locator_eq_expand, ← locator_eq_expand]; exact h
    exact Polynomial.expand_injective ha h2
  have hr := congrArg Polynomial.roots e
  rw [Polynomial.roots_prod_X_sub_C, Polynomial.roots_prod_X_sub_C] at hr
  exact Finset.val_injective hr

omit [Fintype F] [DecidableEq F] in
/-- Hence `A ↦ codewordPoly A a k z` is injective for `a ≥ 1`. -/
lemma codewordPoly_inj (a k : ℕ) (ha : 1 ≤ a) {z : F} {A A' : Finset F}
    (h : codewordPoly A a k z = codewordPoly A' a k z) : A = A' := by
  apply locator_inj a ha
  have : locator A a = locator A' a := by
    have := h; unfold codewordPoly at this; linear_combination -this
  exact this

omit [Fintype F] in
/-- The codeword `codewordPoly A a k z` is a genuine Reed-Solomon codeword (degree `<k`)
agreeing with `u_z = x^{k+a}+z x^k` on the whole fiber `S_A`, whenever `∑_{b∈A} b = -z`
and `k = a(|A|-1)`. -/
lemma codewordPoly_spec (D : Finset F) (a : ℕ) (ha : 1 ≤ a) {A : Finset F} (ℓ k : ℕ)
    (hℓ : 1 ≤ ℓ) (hAcard : A.card = ℓ) (hk : k = a * (ℓ - 1)) {z : F}
    (hsum : ∑ b ∈ A, b = -z) :
    (codewordPoly A a k z).degree < (k : ℕ) ∧
      ∀ x ∈ fiberSet D a A, (codewordPoly A a k z).eval x = x ^ (k + a) + z * x ^ k := by
  obtain ⟨R, hR₁, hR₂⟩ := locator_decomp A a ha (by linarith) k (by rw [hk, hAcard])
  have hz : (- ∑ b ∈ A, b) = z := by rw [hsum]; ring
  constructor
  · have : codewordPoly A a k z = -R := by
      unfold codewordPoly; rw [hR₂, ← hz]; ring
    rw [this]; simpa using hR₁
  · intro x hx
    have hL := locator_eval_zero A a (Finset.mem_filter.mp hx).2
    unfold codewordPoly; simp only [eval_sub, eval_add, eval_mul, eval_pow, eval_X, eval_C]
    rw [hL]; ring

/-- **Theorem 2.1(d), with distinctness.**  For a suitable slope `z`, the received word
`u_z(x) = x^{k+a} + z x^k` has at least `C(N, ℓ)/q` *distinct* Reed-Solomon codewords
(degree `<k`) of `RS[F,D,k]`, each agreeing with `u_z` on a support set `S ⊆ D` of size
`k+a ≥ (1-δ)|D|`, i.e. within relative distance `δ = 1 - ρ - 1/N`.  This upgrades
`list_lower_bound` from a count of witnessing subsets to a lower bound on distinct
codewords, matching the list statement of Paper A. -/
theorem list_lower_bound_distinct (D : Finset F) (a N : ℕ) (ha : 1 ≤ a) {Q : Finset F}
    (hQ : Q = D.image (fun x => x ^ a))
    (hfib : ∀ b ∈ Q, (D.filter (fun x => x ^ a = b)).card = a)
    (hDcard : D.card = a * N)
    (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hℓN : ℓ ≤ N) (hNQ : Q.card = N) (hk : k = a * (ℓ - 1))
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + a : ℝ)) :
    ∃ z : F, ∃ T : Finset F[X],
      ((N.choose ℓ : ℝ) / (Fintype.card F : ℝ)) ≤ (T.card : ℝ) ∧
      ∀ p ∈ T, p.degree < (k : ℕ) ∧
        ∃ S ⊆ D, ((1 - δ) * (D.card : ℝ) ≤ (S.card : ℝ)) ∧
          ∀ x ∈ S, p.eval x = x ^ (k + a) + z * x ^ k := by
  obtain ⟨z, hcard, -⟩ := list_lower_bound D a N ha hQ hfib hDcard ℓ k hℓ hℓN hNQ hk δ hδ
  set filt := (Q.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z) with hfilt
  refine ⟨z, filt.image (fun A => codewordPoly A a k z), ?_, ?_⟩
  · rw [Finset.card_image_of_injOn]
    · exact hcard
    · exact fun A _ A' _ h => codewordPoly_inj a k ha h
  · intro p hp
    rw [Finset.mem_image] at hp
    obtain ⟨A, hA, rfl⟩ := hp
    rw [hfilt, Finset.mem_filter, Finset.mem_powersetCard] at hA
    obtain ⟨⟨hAQ, hAcard⟩, hAsum⟩ := hA
    obtain ⟨hdeg, hagree⟩ := codewordPoly_spec D a ha ℓ k hℓ hAcard hk hAsum
    refine ⟨hdeg, fiberSet D a A, Finset.filter_subset _ _, ?_, hagree⟩
    have hSc : (fiberSet D a A).card = a * ℓ := by
      rw [fiberSet_card D a hQ hfib hAQ, hAcard]
    have hka : k + a = a * ℓ := by
      subst hk
      rcases ℓ with _ | m
      · exact absurd hℓ (by norm_num)
      · simp [Nat.mul_succ]
    have hcardeq : (fiberSet D a A).card = k + a := by rw [hSc, hka]
    rw [hcardeq]; exact_mod_cast hδ

/-!
### The full-domain specialization (`a = 1`)

With `a = 1` and `Q = D` the quotient configuration holds for *any* finite domain `D`
(each fiber of `x ↦ x^1 = x` is a singleton), so the hypotheses are non-vacuous.  This is
precisely the setting of Theorem 2.1(b,c): the full multiplicative domain, where the RS rate
is `ρ = k/n` with `k = ℓ - 1` and `n = |D|`.
-/

/-
On the full domain (`a = 1`, `Q = D`), if the restricted sumset `ℓ^{∧}D` covers the
whole field then the MCA error is `1` at every radius `δ ≥ 1 - ρ - 1/n`
(Theorem 2.1(b,c) mechanism).
-/
theorem epsMca_eq_one_of_cover_full (D : Finset F) (ℓ k : ℕ) (hℓ : 1 ≤ ℓ) (hℓD : ℓ ≤ D.card)
    (hk : k = ℓ - 1) (hcover : restrictedSumset D ℓ = Finset.univ)
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + 1 : ℝ)) :
    epsMca D k δ = 1 := by
  convert epsMca_eq_one_of_cover D 1 D.card ( by norm_num ) ( by aesop ) ( fun b hb => ?_ ) ℓ k hℓ hℓD rfl ?_ hcover δ ?_ using 1;
  · exact Finset.card_eq_one.mpr ⟨ b, by aesop ⟩;
  · rw [ hk, one_mul ];
  · exact_mod_cast hδ

/-
On the full domain (`a = 1`, `Q = D`), some received word `x^{k+1} + z·x^k` has at
least `C(n, ℓ)/q` Reed-Solomon codewords within relative distance `1 - ρ - 1/n`
(Theorem 2.1(d) mechanism).
-/
theorem list_lower_bound_full (D : Finset F) (ℓ k : ℕ) (hℓ : 1 ≤ ℓ)
    (hk : k = ℓ - 1)
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + 1 : ℝ)) :
    ∃ z : F, ((D.card.choose ℓ : ℝ) / (Fintype.card F : ℝ)) ≤
      (( (D.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z) ).card : ℝ) ∧
      ∀ A ∈ (D.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z),
        RSagrees k (fun x => x ^ (k + 1) + z * x ^ k) (fiberSet D 1 A) := by
  obtain ⟨z, hz⟩ : ∃ z : F, ((D.card.choose ℓ : ℝ) / (Fintype.card F : ℝ)) ≤ (( (D.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z) ).card : ℝ) := by
    have h_avg : ∃ z : F, ((D.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z)).card ≥ ((D.card.choose ℓ) : ℝ) / (Fintype.card F : ℝ) := by
      have h_sum : ∑ z : F, ((D.powersetCard ℓ).filter (fun A => (∑ b ∈ A, b) = -z)).card = (D.card.choose ℓ) := by
        rw [ ← Finset.card_biUnion ];
        · convert Finset.card_powersetCard ℓ D using 2;
          ext A; simp +decide [ eq_comm ] ;
          exact fun _ _ => ⟨ -∑ b ∈ A, b, neg_neg _ ⟩;
        · exact fun x _ y _ hxy => Finset.disjoint_left.mpr fun A hA hA' => hxy <| by aesop;
      contrapose! h_sum;
      have := Finset.sum_lt_sum_of_nonempty ( Finset.univ_nonempty ) fun z _ => h_sum z; simp_all +decide ;
      rw [ mul_div_cancel₀ ] at this <;> norm_cast at * ; aesop;
      exact Fintype.card_ne_zero;
    exact h_avg;
  refine' ⟨ z, hz, fun A hA => _ ⟩;
  convert locator_RSagrees D 1 ( by norm_num ) ℓ k hℓ ( ?_ ) ( ?_ ) _ using 1 <;> simp_all +decide

/-!
### Theorem 2.1(c): the cyclotomic sieve density obstruction

Part (c) of the main theorem asserts that for each prize rate there are *infinitely many*
primes `p` carrying a power-of-two subgroup `Q ≤ 𝔽_p^×` of order `N = Θ_ρ(log p)` with

  `ε_mca(RS[𝔽_p, Q, ρN], 1-ρ-1/N) ≥ (log₂ p)^{-6}`,

an inverse-polynomial (hence non-negligible) bad-slope density at logarithmic subgroup size.

The engine is the paper's **cyclotomic sieve theorem** (`thm:sieve`).  Its only external
input is the **Siegel–Walfisz theorem** (prime counting in arithmetic progressions), which is
not in Mathlib; the value-family, granularity and norm-collision counting steps then produce,
for infinitely many primes `p`, an order-`N` subgroup `Q` with restricted-sumset density
`|ℓ^∧Q| ≥ p / (log₂ p)^6` at `ℓ = ρN+1`.  Exactly as the paper *imports* Siegel–Walfisz, we
take this density conclusion as the hypothesis `hsieve` and prove the MCA obstruction of
Theorem 2.1(c) from it, via the quotient-locator lower bound `epsMca_ge_restrictedSumset`
(specialised to the full domain `a = 1`, `D = Q`, as the paper does).
-/

/-- Full-domain (`a = 1`, `Q = D`) form of the quotient-locator lower bound: the MCA error
dominates the restricted-sumset density, `ε_mca(RS[F,D,k], δ) ≥ |ℓ^∧D| / q`, for every
radius `δ ≥ 1 - ρ - 1/n` (`k = ℓ - 1`, `n = |D|`). -/
theorem epsMca_ge_restrictedSumset_full (D : Finset F) (ℓ k : ℕ) (hℓ : 1 ≤ ℓ)
    (hℓD : ℓ ≤ D.card) (hk : k = ℓ - 1)
    (δ : ℝ) (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + 1 : ℝ)) :
    ((restrictedSumset D ℓ).card : ℝ) / (Fintype.card F : ℝ) ≤ epsMca D k δ := by
  have h := epsMca_ge_restrictedSumset (Q := D) D 1 D.card (by norm_num)
    (by simp) (fun b hb => by simp [pow_one, Finset.filter_eq', hb]) ℓ k hℓ hℓD rfl
    (by rw [hk, one_mul]) δ (by exact_mod_cast hδ)
  exact h

/-- The density reduction: if the restricted sumset is large, `|ℓ^∧D| ≥ q / C`, then the MCA
error is at least `1 / C`.  This is the step "the MCA statement follows from `lem:locator`
applied with `D = Q` and `a = 1`" in the proof of the cyclotomic sieve theorem. -/
theorem epsMca_ge_density_full (D : Finset F) (ℓ k : ℕ) (hℓ : 1 ≤ ℓ)
    (hℓD : ℓ ≤ D.card) (hk : k = ℓ - 1) (δ : ℝ)
    (hδ : (1 - δ) * (D.card : ℝ) ≤ (k + 1 : ℝ))
    (C : ℝ) (hC : 0 < C)
    (hdens : (Fintype.card F : ℝ) / C ≤ ((restrictedSumset D ℓ).card : ℝ)) :
    C⁻¹ ≤ epsMca D k δ := by
  have hmain := epsMca_ge_restrictedSumset_full D ℓ k hℓ hℓD hk δ hδ
  calc C⁻¹ = (Fintype.card F : ℝ) / C / (Fintype.card F : ℝ) := by field_simp
    _ ≤ ((restrictedSumset D ℓ).card : ℝ) / (Fintype.card F : ℝ) := by gcongr
    _ ≤ epsMca D k δ := hmain

/-- **Theorem 2.1(c) (cyclotomic sieve density obstruction).**
Given the density conclusion of the cyclotomic sieve theorem `hsieve` — for every bound `X`
there is a prime `p > X` carrying an order-`Q.card` subgroup `Q ≤ 𝔽_p^×` with restricted-sumset
density `|ℓ^∧Q| ≥ p / (log₂ p)^6` at `ℓ`, `k = ℓ - 1`, and radius `δ ≥ 1 - ρ - 1/N` — there
are infinitely many primes `p` for which the MCA error is at least `(log₂ p)^{-6}`, an
inverse-polynomial function of the security parameter `log₂ p`, hence non-negligible.

The hypothesis `hsieve` is precisely the output of the paper's sieve (whose sole external
input is Siegel–Walfisz, not available in Mathlib); the content proved here is the reduction
from that density to the MCA obstruction of the main theorem. -/
theorem thm_main_c
    (hsieve : ∀ X : ℝ, ∃ p : ℕ, Nat.Prime p ∧ X < (p : ℝ) ∧
      ∀ [Fact p.Prime], ∃ (Q : Finset (ZMod p)) (ℓ k : ℕ) (δ : ℝ),
        1 ≤ ℓ ∧ ℓ ≤ Q.card ∧ k = ℓ - 1 ∧
        (1 - δ) * (Q.card : ℝ) ≤ (k + 1 : ℝ) ∧
        (p : ℝ) / (Real.logb 2 p) ^ 6 ≤ ((restrictedSumset Q ℓ).card : ℝ)) :
    ∀ X : ℝ, ∃ p : ℕ, Nat.Prime p ∧ X < (p : ℝ) ∧
      ∀ [Fact p.Prime], ∃ (Q : Finset (ZMod p)) (k : ℕ) (δ : ℝ),
        ((Real.logb 2 p) ^ 6)⁻¹ ≤ epsMca Q k δ := by
  intro X
  obtain ⟨p, hp, hpX, hbody⟩ := hsieve X
  refine ⟨p, hp, hpX, ?_⟩
  intro _inst
  obtain ⟨Q, ℓ, k, δ, hℓ, hℓQ, hk, hδ, hdens⟩ := hbody
  refine ⟨Q, k, δ, ?_⟩
  have hFcard : (Fintype.card (ZMod p) : ℝ) = p := by rw [ZMod.card]
  have hC : (0 : ℝ) < (Real.logb 2 p) ^ 6 := by
    have h1 : (1 : ℝ) < p := by exact_mod_cast hp.one_lt
    have := Real.logb_pos (b := 2) (by norm_num) h1
    positivity
  refine epsMca_ge_density_full Q ℓ k hℓ hℓQ hk δ hδ ((Real.logb 2 p) ^ 6) hC ?_
  rw [hFcard]
  exact hdens

end RSLocator