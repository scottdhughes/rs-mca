import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat
open scoped Classical
open scoped Pointwise

set_option maxHeartbeats 8000000
set_option maxRecDepth 4000
set_option synthInstance.maxHeartbeats 20000
set_option synthInstance.maxSize 128

set_option relaxedAutoImplicit false
set_option autoImplicit false

set_option grind.warning false

/-!
# Preliminaries for the universal field-size cap paper

This file formalizes the definitional core of the *Preliminaries* section of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*,

together with the two elementary structural results stated there:

* `RSCap.eca_le_emca` — Fact 4.5 (cf. `\cite[Fact 4.5]{ABF26}`): the correlated
  agreement (CA) error is bounded by the mutual correlated agreement (MCA) error,
  `ε_ca(C,δ) ≤ ε_mca(C,δ)`.
* `RSCap.emca_mono` — Lemma (support-wise MCA monotonicity): `δ ↦ ε_mca(C,δ)` is
  nondecreasing.

We work over an arbitrary finite alphabet field `F` and a finite index type `ι`
playing the role of the evaluation domain `D` (so `n = Fintype.card ι`).  Words are
functions `ι → F` (the paper's `F^n`).  A code is any set `C ⊆ (ι → F)`; the two
results above do not use linearity, so we state them for arbitrary `C`.

All error quantities are the exact probabilistic maxima of the paper: a maximum,
over all pairs `(f₁, f₂)`, of the probability over a uniformly random slope `γ ∈ F`
that `γ` is CA-bad / MCA-bad for the pair.
-/

namespace RSCap

open Classical

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- Number of coordinates on which `u` and `v` differ. -/
noncomputable def numDiff (u v : ι → F) : ℕ :=
  (Finset.univ.filter (fun i => u i ≠ v i)).card

/-- Relative Hamming distance `Δ(u,v) = |{i : u i ≠ v i}| / n`. -/
noncomputable def relDist (u v : ι → F) : ℝ :=
  (numDiff u v : ℝ) / (Fintype.card ι)

/-- Column (2-interleaved) relative distance
`Δ₂((u₁,u₂),(v₁,v₂)) = |{i : u₁ i ≠ v₁ i ∨ u₂ i ≠ v₂ i}| / n`. -/
noncomputable def relDist2 (u1 u2 v1 v2 : ι → F) : ℝ :=
  ((Finset.univ.filter (fun i => u1 i ≠ v1 i ∨ u2 i ≠ v2 i)).card : ℝ)
    / (Fintype.card ι)

/-- `u` is `δ`-close to the code `C`, i.e. `Δ(u,C) ≤ δ`. -/
def caClose (C : Set (ι → F)) (δ : ℝ) (u : ι → F) : Prop :=
  ∃ c ∈ C, relDist u c ≤ δ

/-- The pair `(u₁,u₂)` is `δ`-close to the interleaved code `C^{≡2}`,
i.e. `Δ₂((u₁,u₂),C^{≡2}) ≤ δ`. -/
def intClose (C : Set (ι → F)) (δ : ℝ) (u1 u2 : ι → F) : Prop :=
  ∃ c1 ∈ C, ∃ c2 ∈ C, relDist2 u1 u2 c1 c2 ≤ δ

/-- `γ` is **CA-bad** for `(f₁,f₂)` at radii `(δ_fld, δ_int)`
(Definition 2.1, correlated agreement error). -/
def caBad (C : Set (ι → F)) (δfld δint : ℝ) (f1 f2 : ι → F) (γ : F) : Prop :=
  caClose C δfld (fun i => f1 i + γ * f2 i) ∧ ¬ intClose C δint f1 f2

/-- `γ` is **MCA-bad** for `(f₁,f₂)` at radius `δ`
(Definition 2.2, support-wise mutual correlated agreement error): some large
support `S` explains `f₁ + γ f₂`, but the same `S` does not simultaneously
explain `f₁` and `f₂`. -/
def mcaBad (C : Set (ι → F)) (δ : ℝ) (f1 f2 : ι → F) (γ : F) : Prop :=
  ∃ S : Finset ι, ((1 - δ) * (Fintype.card ι) ≤ (S.card : ℝ)) ∧
    (∃ c ∈ C, ∀ i ∈ S, f1 i + γ * f2 i = c i) ∧
    ¬ (∃ c1 ∈ C, ∃ c2 ∈ C, ∀ i ∈ S, f1 i = c1 i ∧ f2 i = c2 i)

/-- Probability over a uniformly random `γ ∈ F` that the predicate `P` holds. -/
noncomputable def prob (P : F → Prop) : ℝ :=
  ((Finset.univ.filter (fun γ => P γ)).card : ℝ) / (Fintype.card F)

/-- Nonemptiness witness for the maximization over pairs `(f₁,f₂)`. -/
theorem pairs_nonempty :
    (Finset.univ : Finset ((ι → F) × (ι → F))).Nonempty :=
  ⟨((fun _ => 0), (fun _ => 0)), Finset.mem_univ _⟩

/-- Correlated agreement error `ε_ca(C, δ_fld, δ_int)`, the maximum over pairs of
the probability of a CA-bad slope (Definition 2.1). -/
noncomputable def ecaErr (C : Set (ι → F)) (δfld δint : ℝ) : ℝ :=
  Finset.univ.sup' pairs_nonempty
    (fun p : (ι → F) × (ι → F) => prob (fun γ => caBad C δfld δint p.1 p.2 γ))

/-- No-proximity-loss CA error `ε_ca(C,δ) := ε_ca(C,δ,δ)`. -/
noncomputable def ecaErrDiag (C : Set (ι → F)) (δ : ℝ) : ℝ := ecaErr C δ δ

/-- Mutual correlated agreement error `ε_mca(C, δ)` (Definition 2.2). -/
noncomputable def emcaErr (C : Set (ι → F)) (δ : ℝ) : ℝ :=
  Finset.univ.sup' pairs_nonempty
    (fun p : (ι → F) × (ι → F) => prob (fun γ => mcaBad C δ p.1 p.2 γ))

/-- Challenge threshold `δ*_C(ε*)` (Definition 2.3), with the convention
`sup ∅ = 0`. -/
noncomputable def dStar (C : Set (ι → F)) (ρ εstar : ℝ) : ℝ :=
  sSup {δ : ℝ | 0 < δ ∧ δ < 1 - ρ ∧ emcaErr C δ ≤ εstar}

/-
Monotonicity of `prob` under pointwise implication of predicates.
-/
omit [Field F] in
theorem prob_mono {P Q : F → Prop} (h : ∀ γ, P γ → Q γ) : prob P ≤ prob Q := by
  exact div_le_div_of_nonneg_right ( mod_cast Finset.card_le_card fun x hx => by aesop ) ( Nat.cast_nonneg _ )

/-
Whenever `γ` is CA-bad for `(f₁,f₂)` at the diagonal radius `δ`, it is also
MCA-bad for the same pair at radius `δ`.
-/
omit [Fintype F] in
theorem caBad_diag_imp_mcaBad (C : Set (ι → F)) (δ : ℝ) (f1 f2 : ι → F) (γ : F)
    (h : caBad C δ δ f1 f2 γ) : mcaBad C δ f1 f2 γ := by
  obtain ⟨c, hc⟩ := h.left;
  refine' ⟨ Finset.univ.filter fun i => f1 i + γ * f2 i = c i, _, ⟨ c, hc.1, _ ⟩, _ ⟩ <;> simp_all +decide [ relDist ];
  · by_cases h : Fintype.card ι = 0 <;> simp_all +decide [ numDiff ];
    rw [ div_le_iff₀ ( by positivity ) ] at hc;
    rw [ show ( Finset.univ.filter fun i => f1 i + γ * f2 i = c i ) = Finset.univ \ ( Finset.univ.filter fun i => ¬f1 i + γ * f2 i = c i ) by ext; simp +decide, Finset.card_sdiff ] ; simp +decide [ Finset.card_univ ];
    rw [ Nat.cast_sub ( le_trans ( Finset.card_le_univ _ ) ( by simp +decide ) ) ] ; linarith;
  · intro c1 hc1 c2 hc2
    by_contra h_contra
    push_neg at h_contra;
    have h_interleaved_diff : (Finset.univ.filter (fun i => f1 i ≠ c1 i ∨ f2 i ≠ c2 i)).card ≤ (Finset.univ.filter (fun i => f1 i + γ * f2 i ≠ c i)).card := by
      exact Finset.card_le_card fun i hi => by specialize h_contra i; aesop;
    refine' h.2 ⟨ c1, hc1, c2, hc2, _ ⟩;
    refine' le_trans _ hc.2;
    exact div_le_div_of_nonneg_right ( mod_cast h_interleaved_diff ) ( Nat.cast_nonneg _ )

/-
**Fact 4.5** (`\cite[Fact 4.5]{ABF26}`): the correlated agreement error is
bounded by the mutual correlated agreement error.
-/
theorem eca_le_emca (C : Set (ι → F)) (δ : ℝ) :
    ecaErrDiag C δ ≤ emcaErr C δ := by
  apply_rules [ Finset.sup'_le ];
  · exact ⟨ ⟨ 0, 0 ⟩, Finset.mem_univ _ ⟩;
  · intro p hp
    apply le_trans (prob_mono (fun γ hγ => caBad_diag_imp_mcaBad C δ p.1 p.2 γ hγ));
    exact Finset.le_sup' ( fun p : ( ι → F ) × ( ι → F ) => prob ( fun γ => mcaBad C δ p.1 p.2 γ ) ) hp

/-
If `γ` is MCA-bad at radius `δ`, it is MCA-bad at any larger radius `δ'`.
-/
omit [Fintype F] in
theorem mcaBad_mono (C : Set (ι → F)) {δ δ' : ℝ} (hle : δ ≤ δ')
    (f1 f2 : ι → F) (γ : F) (h : mcaBad C δ f1 f2 γ) : mcaBad C δ' f1 f2 γ := by
  obtain ⟨ S, hS₁, hS₂, hS₃ ⟩ := h;
  exact ⟨ S, by nlinarith [ show ( S.card : ℝ ) ≤ Fintype.card ι by exact_mod_cast Finset.card_le_univ S ], hS₂, hS₃ ⟩

/-
**Support-wise MCA monotonicity**: `δ ↦ ε_mca(C,δ)` is nondecreasing.
-/
theorem emca_mono (C : Set (ι → F)) {δ δ' : ℝ} (hle : δ ≤ δ') :
    emcaErr C δ ≤ emcaErr C δ' := by
  refine' Finset.sup'_le _ _ _;
  intro p hp;
  refine' le_trans _ ( Finset.le_sup' _ hp );
  exact prob_mono fun γ hγ => mcaBad_mono C hle p.1 p.2 γ hγ

/-!
## The CA deep-list floor function (Corollary, deep-list trigger and ceiling)

The quantitative deep-list floors of the paper all produce the same rational
lower bound on the CA / MCA error, namely `𝓔_{q,k}(L) = L(q-n)/(q(q-n+kL))`.
The following three facts (Corollary *deep-list trigger and ceiling*) are pure
statements about this function and do not use the Reed–Solomon machinery, so we
state them for real parameters `q, n, k, L` with the natural positivity
hypotheses (`0 < q`, `n < q`, `0 < k`, `0 < L`).
-/

/-- The deep-list CA/MCA error floor `𝓔_{q,k}(L) = L(q-n)/(q(q-n+kL))`. -/
noncomputable def ecaFloor (q n k L : ℝ) : ℝ := L * (q - n) / (q * (q - n + k * L))

/-
`𝓔_{q,k}(L)` is nondecreasing in `L`.
-/
theorem ecaFloor_mono {q n k : ℝ} (hq : 0 < q) (hqn : n < q) (hk : 0 < k)
    {L1 L2 : ℝ} (hL1 : 0 < L1) (hle : L1 ≤ L2) :
    ecaFloor q n k L1 ≤ ecaFloor q n k L2 := by
  rw [ ecaFloor, ecaFloor, div_le_div_iff₀ ] <;> nlinarith [ mul_pos hq ( sub_pos.2 hqn ), mul_pos hq hk, mul_pos hk ( sub_pos.2 hqn ), mul_le_mul_of_nonneg_left hle <| sub_nonneg.2 hqn.le ]

/-
Trigger inequality: `𝓔_{q,k}(L) > (1/(2k))(1 - n/q)` iff `L > (q-n)/k`.
-/
theorem ecaFloor_trigger {q n k L : ℝ} (hq : 0 < q) (hqn : n < q) (hk : 0 < k)
    (hL : 0 < L) :
    (q - n) / (2 * k * q) < ecaFloor q n k L ↔ (q - n) / k < L := by
  unfold ecaFloor;
  rw [ div_lt_div_iff₀ ];
  · rw [ div_lt_iff₀ hk ] ; exact ⟨ fun h => by nlinarith [ mul_pos hq ( sub_pos.mpr hqn ), mul_pos hq hk, mul_pos hq hL, mul_pos hk hL ], fun h => by nlinarith [ mul_pos hq ( sub_pos.mpr hqn ), mul_pos hq hk, mul_pos hq hL, mul_pos hk hL ] ⟩ ;
  · positivity;
  · nlinarith [ mul_pos hk hL ]

/-
Ceiling: `𝓔_{q,k}(L) < (1/k)(1 - n/q)` for every finite `L`, the limiting
value as `L → ∞`.
-/
theorem ecaFloor_lt {q n k L : ℝ} (hq : 0 < q) (hqn : n < q) (hk : 0 < k)
    (hL : 0 < L) :
    ecaFloor q n k L < (q - n) / (k * q) := by
  unfold ecaFloor;
  rw [ div_lt_div_iff₀ ] <;> nlinarith [ mul_pos hq hL, mul_pos hq ( sub_pos.mpr hqn ), mul_pos hq hk, mul_pos ( sub_pos.mpr hqn ) hL, mul_pos ( sub_pos.mpr hqn ) hk, mul_pos ( sub_pos.mpr hqn ) ( mul_pos hL hk ) ]

/-!
## Bounds on the challenge threshold `δ*_C(ε*)`

The two facts from the paragraph following Definition 2.3, translating
certificates of unsafety / safety at a radius into bounds on the supremum
`δ*_C(ε*)` under the `sup ∅ = 0` convention.
-/

/-
If every radius `δ ∈ [δ₀, 1-ρ)` is unsafe at target `ε*`
(`ε* < ε_mca(C,δ)`), then `δ*_C(ε*) ≤ δ₀`.
-/
theorem dStar_le {C : Set (ι → F)} {ρ εstar δ0 : ℝ} (hδ0 : 0 ≤ δ0)
    (h : ∀ δ, δ0 ≤ δ → δ < 1 - ρ → εstar < emcaErr C δ) :
    dStar C ρ εstar ≤ δ0 := by
  by_cases h_nonempty : {δ : ℝ | 0 < δ ∧ δ < 1 - ρ ∧ emcaErr C δ ≤ εstar}.Nonempty <;> simp_all +decide [ dStar ];
  · exact csSup_le h_nonempty fun δ hδ => le_of_not_gt fun hδ' => not_le_of_gt ( h δ hδ'.le hδ.2.1 ) hδ.2.2;
  · rw [ Set.not_nonempty_iff_eq_empty.mp h_nonempty, Real.sSup_empty ] ; linarith

/-
If a single sub-capacity radius `δ₁ < 1-ρ` is safe at target `ε*`
(`ε_mca(C,δ₁) ≤ ε*`), then `δ*_C(ε*) ≥ δ₁`.
-/
theorem le_dStar {C : Set (ι → F)} {ρ εstar δ1 : ℝ} (h1 : 0 < δ1) (h2 : δ1 < 1 - ρ)
    (h3 : emcaErr C δ1 ≤ εstar) : δ1 ≤ dStar C ρ εstar := by
  apply le_csSup;
  · exact ⟨ 1 - ρ, fun δ hδ => hδ.2.1.le ⟩;
  · exact ⟨ h1, h2, h3 ⟩

/-!
## The Cauchy–Schwarz bucket-counting core of the deep-list floor

The quantitative deep-list floor (Proposition *quantitative deep-list floor*)
rests on a single elementary counting inequality.  After choosing a good pole
`α`, the `L` polynomial values `P_i(α)` fall into `V.card` distinct value
buckets with multiplicities `mult v`.  These satisfy `∑ mult = L` and, by the
bound on colliding pairs, `∑ mult² ≤ L + kL(L-1)/(q-n)`.  Cauchy–Schwarz
(`sq_sum_le_card_mul_sum_sq`) then forces the number of distinct buckets to be
at least `L(q-n)/(q-n+kL)`, which is exactly `q` times the floor `𝓔_{q,k}(L)`.

We isolate this as a pure inequality over reals, with `qn` standing for the
positive quantity `q - n` (or `q - b` in the extension-pole variant), so that
the same lemma covers every simple-pole floor in the paper.
-/

/-
The sharp bucket count: with the collision bound `∑ mult² ≤ L + kL(L-1)/qn`,
the number of distinct buckets is at least `L·qn/(qn + k(L-1))`.
-/
theorem bucket_count_floor_sharp {α : Type*} (V : Finset α) (mult : α → ℝ)
    {L k qn : ℝ} (hqn : 0 < qn) (hk : 0 ≤ k) (hL : 1 ≤ L)
    (hsum : ∑ v ∈ V, mult v = L)
    (hsq : ∑ v ∈ V, (mult v) ^ 2 ≤ L + k * L * (L - 1) / qn) :
    L * qn / (qn + k * (L - 1)) ≤ (V.card : ℝ) := by
  -- By Cauchy–Schwarz, we have $(∑ v ∈ V, mult v)^2 ≤ V.card * ∑ v ∈ V, (mult v)^2$.
  have h_cauchy_schwarz : (∑ v ∈ V, mult v)^2 ≤ V.card * (∑ v ∈ V, (mult v)^2) := by
    have := Finset.sum_le_sum fun i ( hi : i ∈ V ) => mul_self_nonneg ( mult i - ( ∑ i ∈ V, mult i ) / V.card );
    simp_all +decide [ sub_mul, mul_sub ];
    by_cases hV : V = ∅ <;> simp_all +decide [ ← sq, ← Finset.mul_sum _ _ _, ← Finset.sum_mul ];
    nlinarith [ mul_div_cancel₀ L ( show ( V.card : ℝ ) ≠ 0 by exact Nat.cast_ne_zero.mpr ( Finset.card_ne_zero_of_mem ( Classical.choose_spec ( Finset.nonempty_of_ne_empty hV ) ) ) ) ];
  rw [ div_le_iff₀ ( by nlinarith ) ];
  simp_all +decide;
  rw [ add_div', le_div_iff₀ ] at hsq <;> nlinarith [ mul_le_mul_of_nonneg_left hL hqn.le ]

/-
The clean bucket count `L·qn/(qn + kL) ≤ V.card`, obtained from the sharp bound
by weakening `k(L-1)` to `kL`.  Multiplying by `1/q` this is exactly the floor
`𝓔_{q,k}(L)` of `ecaFloor` (with `qn = q - n`).
-/
theorem bucket_count_floor {α : Type*} (V : Finset α) (mult : α → ℝ)
    {L k qn : ℝ} (hqn : 0 < qn) (hk : 0 ≤ k) (hL : 1 ≤ L)
    (hsum : ∑ v ∈ V, mult v = L)
    (hsq : ∑ v ∈ V, (mult v) ^ 2 ≤ L + k * L * (L - 1) / qn) :
    L * qn / (qn + k * L) ≤ (V.card : ℝ) := by
  -- Clear denominators and finish with `nlinarith`.
  have h_nlinarith : L^2 ≤ V.card * (L + k * L * (L - 1) / qn) := by
    rw [ ← hsum ];
    have h_cauchy_schwarz : (∑ v ∈ V, mult v)^2 ≤ V.card * ∑ v ∈ V, mult v^2 :=
      sq_sum_le_card_mul_sum_sq
    exact h_cauchy_schwarz.trans ( mul_le_mul_of_nonneg_left ( by simpa only [ hsum ] using hsq ) ( Nat.cast_nonneg _ ) );
  field_simp;
  nlinarith [ mul_div_cancel₀ ( k * L * ( L - 1 ) ) hqn.ne', mul_le_mul_of_nonneg_left hL hqn.le, mul_le_mul_of_nonneg_left hL hk ]

/-
Bridge to `ecaFloor`: dividing the clean bucket count by the number `q` of
finite slopes turns the counting bound `bucket_count_floor` (with `qn = q - n`)
into the deep-list error floor `𝓔_{q,k}(L) = ecaFloor q n k L`.  Thus a received
line with `V.card` distinct value buckets among the `L` list values yields
`ecaFloor q n k L ≤ V.card / q`, the probabilistic lower bound of the
quantitative deep-list floor proposition.
-/
theorem ecaFloor_le_bucket_ratio {α : Type*} (V : Finset α) (mult : α → ℝ)
    {q n k L : ℝ} (hq : 0 < q) (hqn : n < q) (hk : 0 ≤ k) (hL : 1 ≤ L)
    (hsum : ∑ v ∈ V, mult v = L)
    (hsq : ∑ v ∈ V, (mult v) ^ 2 ≤ L + k * L * (L - 1) / (q - n)) :
    ecaFloor q n k L ≤ (V.card : ℝ) / q := by
  have hqn' : 0 < q - n := sub_pos.mpr hqn
  have hkL : 0 ≤ k * L := mul_nonneg hk (by linarith)
  have hden : 0 < q - n + k * L := by linarith
  have hb := bucket_count_floor V mult hqn' hk hL hsum hsq
  rw [ ecaFloor, div_le_div_iff₀ (mul_pos hq hden) hq ]
  rw [ div_le_iff₀ hden ] at hb
  nlinarith [ mul_pos hq hqn' ]

/-!
## Genuine extension-valuedness of the simple-pole witness line

The extension-pole deep-list floor (Corollary *extension-pole deep-list floor*)
chooses its simple pole `α` in `F ∖ B` for a proper subfield `B ⊇ D`, and the
crucial structural point is that the resulting pole vector
`((x - α)⁻¹)_{x ∈ D}` is *genuinely* extension-valued: it is not a scalar
multiple over `F` of any `B`-valued vector.  Equivalently, there is no nonzero
`lam ∈ F` making every `lam / (x - α)` lie in `B`.  The following two lemmas
formalize this; they are pure field theory and do not use the Reed–Solomon
machinery.
-/

/-
Two-point core: if `α ∉ B` and `x ≠ y` are two elements of `B`, then no nonzero
scalar `lam` can send both `1/(x-α)` and `1/(y-α)` into `B`.  Otherwise the
ratio `r = (y-α)/(x-α) ∈ B` with `r ≠ 1`, forcing `α = (r x - y)/(r - 1) ∈ B`,
a contradiction.
-/
omit [Fintype F] in
theorem pole_pair_not_subfield_valued (B : Subfield F) {α : F} (hα : α ∉ B)
    {x y : F} (hx : x ∈ B) (hy : y ∈ B) (hxy : x ≠ y)
    {lam : F} (hlam : lam ≠ 0)
    (hx' : lam / (x - α) ∈ B) (hy' : lam / (y - α) ∈ B) : False := by
  -- Let $r := (y-α)/(x-α)$. Observe $r = (λ/(x-α)) * (λ/(y-α))⁻¹$, which lies in $B$ since $B$ is closed under multiplication and inverse (of the nonzero element $λ/(y-α)$).
  set r : F := (lam / (x - α)) * (lam / (y - α))⁻¹
  have hr : r ∈ B := by
    exact B.mul_mem hx' ( B.inv_mem hy' );
  -- From $r = (y-α)/(x-α)$, we get $r*(x-α) = y-α$, i.e., $r*x - r*α = y - α$, so $r*x - y = α*(r-1)$, hence $α = (r*x - y)/(r-1)$.
  have hα_eq : α = (r * x - y) / (r - 1) := by
    grind;
  exact hα ( hα_eq ▸ B.div_mem ( B.sub_mem ( B.mul_mem hr hx ) hy ) ( B.sub_mem hr ( B.one_mem ) ) )

/-
The pole vector `((x - α)⁻¹)_{x ∈ D}` for `α ∉ B` and `D ⊆ B` with `|D| ≥ 2` is
not projectively `B`-valued: there is no nonzero scalar `lam` with every
`lam / (x - α) ∈ B`.  In particular the affine simple-pole witness line is
genuinely extension-valued, not a `B`-rational line viewed over `F`.
-/
omit [Fintype F] in
theorem pole_vector_not_projectively_subfield_valued (B : Subfield F) {α : F}
    (hα : α ∉ B) {D : Finset F} (hD : ∀ x ∈ D, x ∈ B) (hcard : 2 ≤ D.card) :
    ¬ ∃ lam : F, lam ≠ 0 ∧ ∀ x ∈ D, lam / (x - α) ∈ B := by
  obtain ⟨x, hx, y, hy, hxy⟩ : ∃ x ∈ D, ∃ y ∈ D, x ≠ y := by
    exact Finset.one_lt_card.1 hcard;
  exact fun ⟨ lam, hlam, hall ⟩ => pole_pair_not_subfield_valued B hα ( hD x hx ) ( hD y hy ) hxy hlam ( hall x hx ) ( hall y hy )

/-!
## The polynomial engine of the deep-list floor

The abstract bucket count `bucket_count_floor` is fed, in the proof of the
deep-point list-to-CA conversion (Theorem A) and of the quantitative deep-list
floor, by two genuinely polynomial facts about the simple-pole construction on a
Reed–Solomon code `C = RS[F, D, k]` (codewords are degree `< k+1` polynomials).
We formalize both here over the field `F`, identifying the evaluation domain with
a `Finset F` and polynomials with `Polynomial F`.
-/

open Polynomial

/-
**Simple-pole far condition.**  For any pole `α` and any polynomial `G` of degree
`< k`, the auxiliary line slope `g_α(x) = -1/(x-α)` can be matched by `G` at no
more than `k` points: the set of `x` with `(x-α)·G(x) + 1 = 0` has at most `k`
elements, because `(X-α)·G(X)+1` is a nonzero polynomial (value `1` at `α`) of
degree at most `k`.  This is what makes the simple-pole pair far from the
interleaved code.
-/
omit [Fintype ι] in
theorem simple_pole_far {k : ℕ} (α : F) (G : Polynomial F) (hG : G.natDegree < k) :
    (Finset.univ.filter (fun x : F => (x - α) * G.eval x + 1 = 0)).card ≤ k := by
  set p : Polynomial F := (X - C α) * G + 1 with hp
  have hpe : ∀ x : F, p.eval x = (x - α) * G.eval x + 1 := by
    intro x; simp [hp]
  have hpne : p ≠ 0 := by
    intro h
    have := hpe α
    rw [h] at this
    simp at this
  have hdeg : p.natDegree ≤ k := by
    have h1 : ((X - C α) * G).natDegree ≤ k := by
      calc ((X - C α) * G).natDegree ≤ (X - C α).natDegree + G.natDegree :=
            natDegree_mul_le
        _ ≤ 1 + G.natDegree := by
            have : (X - C α).natDegree ≤ 1 := by
              apply le_trans (natDegree_sub_le _ _)
              simp
            omega
        _ ≤ k := by omega
    calc p.natDegree ≤ max ((X - C α) * G).natDegree (1 : Polynomial F).natDegree :=
          natDegree_add_le _ _
      _ ≤ k := by simp [h1]
  have hsub : (Finset.univ.filter (fun x : F => (x - α) * G.eval x + 1 = 0)) ⊆ p.roots.toFinset := by
    intro x hx
    simp only [Finset.mem_filter] at hx
    rw [Multiset.mem_toFinset, mem_roots hpne]
    rw [IsRoot.def, hpe]
    exact hx.2
  calc (Finset.univ.filter (fun x : F => (x - α) * G.eval x + 1 = 0)).card
      ≤ p.roots.toFinset.card := Finset.card_le_card hsub
    _ ≤ p.roots.card := Multiset.toFinset_card_le _
    _ ≤ p.natDegree := p.card_roots'
    _ ≤ k := hdeg

/-
**Root bound for value collisions.**  Two distinct list polynomials `P i` and
`P j` (of difference degree at most `k`) agree at no more than `k` points of any
finite set `Ω`, because `P i - P j` is a nonzero polynomial of degree at most
`k`.
-/
omit [Fintype ι] [Fintype F] in
theorem poly_agree_le {k : ℕ} {Pi Pj : Polynomial F} (hne : Pi ≠ Pj)
    (hdeg : (Pi - Pj).natDegree ≤ k) (Ω : Finset F) :
    (Ω.filter (fun α => Pi.eval α = Pj.eval α)).card ≤ k := by
  have h_card_roots : (Finset.filter (fun α => Pi.eval α = Pj.eval α) Ω).card ≤ (Polynomial.roots (Pi - Pj)).toFinset.card := by
    refine Finset.card_le_card ?_;
    intro x hx; simp_all +decide [ sub_eq_iff_eq_add ] ;
  exact h_card_roots.trans ( le_trans ( Multiset.toFinset_card_le _ ) ( le_trans ( Polynomial.card_roots' _ ) hdeg ) )

/-
**Fiber square identity.**  For a function `f` on a finite type, the sum over
the distinct values `v` of the squared fiber sizes equals the number of ordered
pairs `(i,j)` with `f i = f j`.  This turns the collision count into the sum of
squared value multiplicities used by `bucket_count_floor`.
-/
theorem sum_sq_fiber_card_pairs {ι' : Type*} [Fintype ι'] {β : Type*} [DecidableEq β]
    (f : ι' → β) :
    ∑ v ∈ Finset.univ.image f, (Finset.univ.filter (fun i => f i = v)).card ^ 2
      = (Finset.univ.filter (fun p : ι' × ι' => f p.1 = f p.2)).card := by
  classical
  rw [Finset.card_filter, Fintype.sum_prod_type]
  rw [← Finset.sum_fiberwise_of_maps_to (g := f)
    (fun i _ => Finset.mem_image_of_mem f (Finset.mem_univ i))]
  refine Finset.sum_congr rfl (fun v hv => ?_)
  have hinner : ∀ i ∈ Finset.univ.filter (fun i => f i = v),
      (∑ j, if f i = f j then (1:ℕ) else 0) = (Finset.univ.filter (fun i => f i = v)).card := by
    intro i hi
    rw [(Finset.mem_filter.mp hi).2, Finset.card_filter]
    exact Finset.sum_congr rfl (fun j _ => if_congr eq_comm rfl rfl)
  rw [Finset.sum_congr rfl hinner, Finset.sum_const, sq, smul_eq_mul]

/-
**Polynomial deep-list bucket bound.**  Given `L ≥ 1` pairwise-distinct list
polynomials `P : Fin L → F[X]`, whose pairwise differences have degree at most
`k`, and a nonempty pole set `Ω`, there is a pole `α ∈ Ω` at which the number of
distinct interpolation values `P i (α)` — i.e. the number of distinct CA-bad
slopes produced by the simple-pole line at `α` — is at least
`L·|Ω| / (|Ω| + k·L)`.  This is the counting heart of the deep-point
list-to-CA conversion and the quantitative deep-list floor: dividing by the
number `q` of finite slopes yields the error floor `ecaFloor`.
-/
omit [Fintype F] in
theorem poly_deep_list_bucket_bound {k : ℕ} {L : ℕ} (hL : 1 ≤ L)
    (P : Fin L → Polynomial F) (Ω : Finset F) (hΩ : Ω.Nonempty)
    (hdeg : ∀ i j : Fin L, (P i - P j).natDegree ≤ k)
    (hdist : ∀ i j : Fin L, i ≠ j → P i ≠ P j) :
    ∃ α ∈ Ω, (L : ℝ) * (Ω.card : ℝ) / ((Ω.card : ℝ) + (k : ℝ) * (L : ℝ))
        ≤ ((Finset.univ.image (fun i => (P i).eval α)).card : ℝ) := by
  obtain ⟨α, hα⟩ : ∃ α ∈ Ω, (Finset.univ.filter (fun p : Fin L × Fin L => p.1 ≠ p.2 ∧ (P p.1).eval α = (P p.2).eval α)).card ≤ k * L * (L - 1) / (Ω.card : ℝ) := by
    have h_sum_collisions : ∑ α ∈ Ω, (Finset.univ.filter (fun p : Fin L × Fin L => p.1 ≠ p.2 ∧ (P p.1).eval α = (P p.2).eval α)).card ≤ k * L * (L - 1) := by
      have h_sum_coll : ∑ α ∈ Ω, (Finset.univ.filter (fun p : Fin L × Fin L => p.1 ≠ p.2 ∧ (P p.1).eval α = (P p.2).eval α)).card ≤ ∑ p ∈ Finset.univ.filter (fun p : Fin L × Fin L => p.1 ≠ p.2), (Finset.filter (fun α => (P p.1).eval α = (P p.2).eval α) Ω).card := by
        simp +decide only [Finset.card_filter];
        rw [ Finset.sum_comm, Finset.sum_filter ];
        exact Finset.sum_le_sum fun x _ => by split_ifs <;> simp +decide [ * ] ;
      refine' le_trans h_sum_coll ( le_trans ( Finset.sum_le_sum fun p hp => show Finset.card _ ≤ k from _ ) _ );
      · convert poly_agree_le ( hdist p.1 p.2 ( by aesop ) ) ( hdeg p.1 p.2 ) Ω using 1;
      · simp +decide [ mul_assoc, mul_comm ];
        rw [ show Finset.filter ( fun p : Fin L × Fin L => ¬p.1 = p.2 ) Finset.univ = Finset.univ.offDiag by ext; simp +decide ] ; simp +decide [ Finset.card_univ, mul_tsub ];
    contrapose! h_sum_collisions;
    convert Finset.sum_lt_sum_of_nonempty hΩ h_sum_collisions using 1;
    rw [ ← @Nat.cast_lt ℝ ] ; simp +decide [ mul_div_assoc ];
    rw [ mul_left_comm, mul_div_cancel₀ _ ( Nat.cast_ne_zero.mpr hΩ.card_pos.ne' ), Nat.cast_pred hL ];
  refine' ⟨ α, hα.1, _ ⟩;
  convert bucket_count_floor ( Finset.image ( fun i => eval α ( P i ) ) Finset.univ ) ( fun v => ( Finset.univ.filter ( fun i => eval α ( P i ) = v ) |> Finset.card : ℝ ) ) _ _ _ _ _ using 1;
  · exact Nat.cast_pos.mpr ( Finset.card_pos.mpr hΩ );
  · positivity;
  · norm_cast;
  · rw_mod_cast [ Finset.sum_image' ];
    rotate_left;
    use fun _ => 1; all_goals simp +decide;
  · convert add_le_add_left hα.2 L using 1;
    · convert sum_sq_fiber_card_pairs ( fun i : Fin L => eval α ( P i ) ) using 1;
      rw [ show ( Finset.filter ( fun p : Fin L × Fin L => eval α ( P p.1 ) = eval α ( P p.2 ) ) Finset.univ ) = Finset.filter ( fun p : Fin L × Fin L => p.1 ≠ p.2 ∧ eval α ( P p.1 ) = eval α ( P p.2 ) ) Finset.univ ∪ Finset.diag ( Finset.univ : Finset ( Fin L ) ) from ?_, Finset.card_union_of_disjoint ] <;> norm_num [ Finset.disjoint_left ];
      · norm_cast;
      · exact fun i j hij _ => hij;
      · grind;
    · ring

/-!
## Subfield confinement (Lemma, subfield confinement)

The deployed instantiations run the protocol over an extension `F/B` while keeping
the evaluation domain in the base field: `D ⊆ B`.  The *subfield-confinement*
lemma pins down where bad slopes can live for lines whose words are base-valued:
all (support-wise MCA-) bad slopes lie in `B`.  We model the extension `F/B` by two
finite fields with `[Algebra B F]` (a field embedding `B ↪ F`), the domain by a
map `dom : ι → B`, and the Reed–Solomon code over `F` with that domain.

The proof rests on the *support-transfer* principle: applying a `B`-linear
functional `F →ₗ[B] B` coefficientwise to a codeword yields another codeword
(because the evaluation points lie in the base field), so from a codeword
explaining `f + z·g` one recovers separate codewords explaining `f` and `g` on
the same support, whenever `1` and `z` are `B`-independent (i.e. `z ∉ B`).
-/

section SubfieldConfinement

variable {B : Type*} [Field B] [Algebra B F]

/-- The Reed–Solomon code over `F` with evaluation domain `dom : ι → B ⊆ F`
(via the embedding `algebraMap B F`) and degree `< k`. -/
def RSCodeF (dom : ι → B) (k : ℕ) : Set (ι → F) :=
  {w | ∃ p : Polynomial F, p.natDegree < k ∧ ∀ i, w i = p.eval (algebraMap B F (dom i))}

/-
**Functional existence.**  If `z ∉ B` (i.e. `z ∉ range (algebraMap B F)`), then
`1` and `z` are `B`-linearly independent, so for any target values `a, b ∈ B`
there is a `B`-linear functional `L : F →ₗ[B] B` with `L 1 = a` and `L z = b`.
-/
theorem exists_Blinear_functional {z : F} (hz : z ∉ Set.range (algebraMap B F))
    (a b : B) : ∃ L : F →ₗ[B] B, L 1 = a ∧ L z = b := by
  have h_lin_ind : LinearIndependent B ![1, z] := by
    refine' linearIndependent_fin2.mpr ⟨ _, _ ⟩;
    · aesop;
    · intro a ha; simp_all +decide [ Algebra.smul_def ] ;
      exact hz ( a⁻¹ ) ( by rw [ map_inv₀, inv_eq_of_mul_eq_one_right ha ] );
  obtain ⟨L, hL⟩ : ∃ L : (Submodule.span B {1, z}) →ₗ[B] B, L ⟨1, by
    exact Submodule.subset_span ( Set.mem_insert _ _ )⟩ = a ∧ L ⟨z, by
    exact Submodule.subset_span ( Set.mem_insert_of_mem _ ( Set.mem_singleton _ ) )⟩ = b := by
    have := h_lin_ind;
    rw [ Fintype.linearIndependent_iff ] at this;
    have h_basis : ∀ x ∈ Submodule.span B {1, z}, ∃ c1 c2 : B, x = c1 • 1 + c2 • z := by
      exact fun x hx => by rw [ Submodule.mem_span_pair ] at hx; tauto;
    have h_basis : ∀ x ∈ Submodule.span B {1, z}, ∃! (c : Fin 2 → B), x = ∑ i, c i • ![1, z] i := by
      intro x hx
      obtain ⟨c1, c2, hc⟩ := h_basis x hx
      use ![c1, c2];
      simp_all +decide [ Fin.sum_univ_two ];
      intro y hy; specialize this ( fun i => if i = 0 then y 0 - c1 else y 1 - c2 ) ; simp_all +decide [ sub_eq_iff_eq_add ] ;
      exact funext fun i => by fin_cases i <;> simp +decide [ this ( by rw [ sub_smul, sub_smul ] ; linear_combination' hy.symm ) ] ;
    choose! c hc hc' using h_basis;
    refine' ⟨ { toFun := fun x => c x 0 * a + c x 1 * b, map_add' := _, map_smul' := _ }, _, _ ⟩ <;> simp +decide [ Fin.sum_univ_two ] at *;
    · intro x hx y hy;
      have := hc' ( x + y ) ( Submodule.add_mem _ hx hy ) ( fun i => c x i + c y i ) ?_;
      · simp +decide [ ← this, add_mul, add_assoc, add_left_comm ];
      · convert congr_arg₂ ( · + · ) ( hc x hx ) ( hc y hy ) using 1 ; simp +decide [ add_smul ] ; ring;
    · intro m x hx
      have h_eq : m • x = (m * c x 0) • 1 + (m * c x 1) • z := by
        rw [ hc x hx, smul_add, smul_smul, smul_smul ];
        rw [ ← hc x hx ]
      generalize_proofs at *;
      rw [ ← hc' ( m • x ) ( Submodule.smul_mem _ _ hx ) ( fun i => m * c x i ) h_eq ] ; simp +decide [ mul_add, mul_assoc ];
    · specialize hc' 1 ( Submodule.subset_span ( Set.mem_insert _ _ ) ) ( fun i => if i = 0 then 1 else 0 ) ; simp +decide at hc';
      simp +decide [ ← hc' ];
    · specialize hc' z ( by exact Submodule.subset_span ( Set.mem_insert_of_mem _ ( Set.mem_singleton _ ) ) ) ( fun i => if i = 0 then 0 else 1 ) ; simp +decide [ Fin.sum_univ_two ] at hc';
      simp +decide [ ← hc' ]
  generalize_proofs at *;
  obtain ⟨ L', hL' ⟩ := L.exists_extend;
  exact ⟨ L', by simpa [ ← hL' ] using hL.1, by simpa [ ← hL' ] using hL.2 ⟩

/-
**Coefficientwise projection preserves RS membership.**  Applying a `B`-linear
functional `L : F →ₗ[B] B` coordinatewise to a codeword `c ∈ RS[F, dom, k]` yields
again a codeword: the evaluation points `algebraMap B F (dom i)` lie in the base
field, so `L (c i) = q.eval (algebraMap B F (dom i))` for the polynomial `q`
obtained by applying `L` to the coefficients of the underlying polynomial.
-/
omit [Fintype ι] [Fintype F] in
theorem RSCodeF_functional_proj (dom : ι → B) (k : ℕ) (L : F →ₗ[B] B) {c : ι → F}
    (hc : c ∈ RSCodeF (F := F) dom k) :
    (fun i => algebraMap B F (L (c i))) ∈ RSCodeF (F := F) dom k := by
  rcases hc with ⟨p, hp⟩;
  refine' ⟨ ∑ e ∈ Finset.range ( p.natDegree + 1 ), Polynomial.C ( ( Algebra.linearMap B F ) ( L ( p.coeff e ) ) ) * Polynomial.X ^ e, _, _ ⟩ <;> simp_all +decide [ Polynomial.eval_finset_sum ];
  · refine' lt_of_le_of_lt ( Polynomial.natDegree_sum_le _ _ ) ( lt_of_le_of_lt ( Finset.sup_le _ ) hp.1 );
    intro i hi; by_cases hi' : L ( p.coeff i ) = 0 <;> simp_all +decide ;
  · intro i; rw [ Polynomial.eval_eq_sum_range ] ; simp +decide ;
    refine' Finset.sum_congr rfl fun x hx => _;
    convert congr_arg ( algebraMap B F ) ( L.map_smul ( ( dom i ) ^ x ) ( p.coeff x ) ) using 1 <;> simp +decide [ mul_comm, Algebra.smul_def ]

/-
**Support transfer.**  If `z ∉ B` and a codeword `c` agrees with the line point
`f + z·g` (with `f, g` base-valued) on a support `S`, then there are codewords
`cf, cg` agreeing with `f` and `g` respectively on the same `S`.
-/
omit [Fintype ι] in
theorem RSCodeF_support_transfer (dom : ι → B) (k : ℕ) {z : F}
    (hz : z ∉ Set.range (algebraMap B F)) (f g : ι → B) (S : Finset ι)
    {c : ι → F} (hc : c ∈ RSCodeF (F := F) dom k)
    (hagree : ∀ i ∈ S,
      algebraMap B F (f i) + z * algebraMap B F (g i) = c i) :
    ∃ cf ∈ RSCodeF (F := F) dom k, ∃ cg ∈ RSCodeF (F := F) dom k,
      ∀ i ∈ S, algebraMap B F (f i) = cf i ∧ algebraMap B F (g i) = cg i := by
  --_Get _L_ and _M_ from `exists_Blinear_functional hz`.
  obtain ⟨L, hL⟩ : ∃ L : F →ₗ[B] B, L 1 = 1 ∧ L z = 0 := by
    convert exists_Blinear_functional hz 1 0
  obtain ⟨M, hM⟩ : ∃ M : F →ₗ[B] B, M 1 = 0 ∧ M z = 1 := by
    convert exists_Blinear_functional hz 0 1;
  refine ⟨fun i => algebraMap B F (L (c i)), RSCodeF_functional_proj dom k L hc,
    fun i => algebraMap B F (M (c i)), RSCodeF_functional_proj dom k M hc, fun i hi => ⟨?_, ?_⟩⟩
  · have hci : c i = (f i) • (1 : F) + (g i) • z := by
      rw [← hagree i hi, Algebra.algebraMap_eq_smul_one (f i),
        Algebra.algebraMap_eq_smul_one (g i), mul_smul_comm, mul_one]
    simp only [hci, map_add, map_smul, hL.1, hL.2]
    simp
  · have hci : c i = (f i) • (1 : F) + (g i) • z := by
      rw [← hagree i hi, Algebra.algebraMap_eq_smul_one (f i),
        Algebra.algebraMap_eq_smul_one (g i), mul_smul_comm, mul_one]
    simp only [hci, map_add, map_smul, hM.1, hM.2]
    simp

/-- **Subfield confinement (support-wise MCA form).**  For a base-valued pair
`(f, g)` (words in `B ⊆ F`) and the Reed–Solomon code over `F` with domain in `B`,
every MCA-bad slope lies in the base field `B`. -/
theorem subfield_confinement_mca (dom : ι → B) (k : ℕ) (δ : ℝ) (f g : ι → B)
    {z : F}
    (hbad : mcaBad (RSCodeF (F := F) dom k) δ
      (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) z) :
    z ∈ Set.range (algebraMap B F) := by
  by_contra hz
  obtain ⟨S, hS, ⟨c, hc, hagree⟩, hno⟩ := hbad
  refine hno ?_
  obtain ⟨cf, hcf, cg, hcg, htr⟩ :=
    RSCodeF_support_transfer dom k hz f g S hc hagree
  exact ⟨cf, hcf, cg, hcg, htr⟩

/-- **Subfield confinement (proximity-loss CA form, part (a)).**  With two radii
`δ_fld ≤ δ_int`, every CA-bad slope of a base-valued pair lies in the base
field `B`.  From `caClose` one extracts a support of size `≥ (1-δ_fld)·n`;
support-transfer then explains `f` and `g` on it, giving `intClose` at radius
`δ_fld ≤ δ_int`, contradicting CA-badness. -/
theorem subfield_confinement_ca (dom : ι → B) (k : ℕ) {δfld δint : ℝ}
    (hle : δfld ≤ δint) (f g : ι → B) {z : F}
    (hbad : caBad (RSCodeF (F := F) dom k) δfld δint
      (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) z) :
    z ∈ Set.range (algebraMap B F) := by
  by_contra hz
  obtain ⟨c, hc, hdist⟩ := hbad.1
  set S : Finset ι :=
    Finset.univ.filter (fun i => algebraMap B F (f i) + z * algebraMap B F (g i) = c i)
    with hSdef
  obtain ⟨cf, hcf, cg, hcg, htr⟩ :=
    RSCodeF_support_transfer dom k hz f g S hc (fun i hi => (Finset.mem_filter.1 hi).2)
  apply hbad.2
  refine ⟨cf, hcf, cg, hcg, ?_⟩
  have hsubset :
      (Finset.univ.filter (fun i =>
        algebraMap B F (f i) ≠ cf i ∨ algebraMap B F (g i) ≠ cg i))
      ⊆ Finset.univ.filter (fun i =>
        algebraMap B F (f i) + z * algebraMap B F (g i) ≠ c i) := by
    intro i hi
    rw [Finset.mem_filter] at hi ⊢
    refine ⟨Finset.mem_univ _, ?_⟩
    intro hcon
    have hiS : i ∈ S := by rw [hSdef, Finset.mem_filter]; exact ⟨Finset.mem_univ _, hcon⟩
    obtain ⟨e1, e2⟩ := htr i hiS
    rcases hi.2 with h | h
    · exact h e1
    · exact h e2
  have hcard := Finset.card_le_card hsubset
  calc relDist2 (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) cf cg
      ≤ relDist (fun i => algebraMap B F (f i) + z * algebraMap B F (g i)) c := by
        unfold relDist2 relDist numDiff
        gcongr
    _ ≤ δfld := hdist
    _ ≤ δint := hle

/-- **Density of the MCA-bad slope set of a base-valued pair.**  By confinement the
MCA-bad slopes all lie in `B`, so their density in `F` is at most `|B|/q`. -/
theorem subfield_confinement_mca_density [Fintype B] (dom : ι → B) (k : ℕ) (δ : ℝ)
    (f g : ι → B) :
    prob (fun z : F => mcaBad (RSCodeF (F := F) dom k) δ
      (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) z)
      ≤ (Fintype.card B : ℝ) / (Fintype.card F) := by
  have hsub : (Finset.univ.filter (fun z : F => mcaBad (RSCodeF (F := F) dom k) δ
      (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) z))
      ⊆ Finset.image (algebraMap B F) (Finset.univ : Finset B) := by
    intro z hz
    rw [Finset.mem_filter] at hz
    obtain ⟨a, ha⟩ := subfield_confinement_mca dom k δ f g hz.2
    exact Finset.mem_image.2 ⟨a, Finset.mem_univ _, ha⟩
  have hcard : (Finset.univ.filter (fun z : F => mcaBad (RSCodeF (F := F) dom k) δ
      (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) z)).card
      ≤ Fintype.card B := by
    calc _ ≤ (Finset.image (algebraMap B F) (Finset.univ : Finset B)).card :=
          Finset.card_le_card hsub
      _ ≤ (Finset.univ : Finset B).card := Finset.card_image_le
      _ = Fintype.card B := Finset.card_univ
  have hcardR : ((Finset.univ.filter (fun z : F => mcaBad (RSCodeF (F := F) dom k) δ
      (fun i => algebraMap B F (f i)) (fun i => algebraMap B F (g i)) z)).card : ℝ)
      ≤ (Fintype.card B : ℝ) := by exact_mod_cast hcard
  unfold prob
  gcongr

end SubfieldConfinement

end RSCap