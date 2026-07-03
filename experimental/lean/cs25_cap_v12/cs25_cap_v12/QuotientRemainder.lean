import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: quotient-profile floors with remainder supports (`sec:quotient-remainder`)

Skeletons (proofs `sorry`) for the quotient-remainder / heaviest-prefix floor results of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

These floors extend the fiber lemma below the multiplicative grid: given a divisor
`c ∣ n` (with quotient order `N = n/c`) and an agreement value `A₀ = mc + s`, a
prefix-selected received word carries a list whose size is the *quotient-remainder
count* `M_{c,m,s} = C(N, m)·C(n − mc, s)` divided by a certificate weight `|B|^{wₒ}`.

Formalized here:

* `qrCount` — the count `M_{c,m,s} = C(N, m)·C(n − mc, s)`.
* `lem_quotient_remainder_prefix` — `lem:quotient-remainder-prefix`: the list-mass floor
  `|Lst(RS[F,D,K], 1 − A₀/n, U)| ≥ ⌈M_{c,m,s}/|B|^{wₒ}⌉`.
* `lem_heaviest_prefix_locator_floor` — `lem:heaviest-prefix-locator-floor`: the sharper
  heaviest-prefix count `H_{c,m,s}^K`, dominating the coarse certificate bound.
* `thm_quotient_remainder_deep_floor` — `thm:quotient-remainder-deep-floor`: the
  resulting deep-band error floor `ε_ca(C, δ) ≥ 𝓔_{q,k}(L)`.
* `cor_quotient_remainder_trigger` — `cor:quotient-remainder-trigger`.
* `cor_quantitative_first_grid_floor` — `cor:quantitative-first-grid-floor`: the
  unconditional first-grid floor `ε_ca(C, δ) ≥ 𝓔_{q,k}(C(n, k+1))` for any `n`-point
  domain.
* `cor_first_grid_cap` — `cor:first-grid-cap`.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The quotient-remainder count `M_{c,m,s} = C(N, m)·C(n − mc, s)`. -/
def qrCount (N n c m s : ℕ) : ℕ := Nat.choose N m * Nat.choose (n - m * c) s

/-- **`lem:quotient-remainder-prefix` — quotient-remainder prefix floor.**

Let `B ⊆ F`, let `dom` be an injective `B`-valued multiplicative coset domain of order
`n`, let `K < n`, `c ∣ n`, `N = n/c`, and `A₀ = mc + s` with `0 ≤ s < c`, `0 ≤ m ≤ N`,
`A₀ ≥ K` (and `mc + s ≤ n` if `s > 0`).  Then, with certificate weight `wₒ`, there is a
`B`-valued received word `U` carrying a list of at least `⌈M_{c,m,s}/|B|^{wₒ}⌉`
distinct codewords of `RS[F, D, K]` at radius `1 − A₀/n`. -/
theorem lem_quotient_remainder_prefix (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {c N K m s A₀ wₒ : ℕ} (hc : 0 < c) (hcn : c ∣ Fintype.card ι)
    (hN : c * N = Fintype.card ι) (hsmooth : DomSmooth dom (fun x => x ^ c) c)
    (hK : K < Fintype.card ι) (hs : s < c) (hm : m ≤ N)
    (hA₀ : A₀ = m * c + s) (hA₀K : K ≤ A₀) (hA₀n : A₀ ≤ Fintype.card ι) :
    ∃ (U : ι → F) (_ : ∀ i, U i ∈ B) (L : ℕ),
      (qrCount N (Fintype.card ι) c m s : ℝ) / (Fintype.card B : ℝ) ^ wₒ ≤ (L : ℝ) ∧
      HasList (RSpoly dom K) (1 - (A₀ : ℝ) / Fintype.card ι) U L := by
  sorry

/-- **`lem:heaviest-prefix-locator-floor` — heaviest-prefix locator floor.**

Under the hypotheses of `lem_quotient_remainder_prefix`, there is a `B`-valued received
word whose list is at least the heaviest-prefix count `H` (a given lower bound
dominating the coarse `⌈M_{c,m,s}/|B|^{wₒ}⌉` certificate). -/
theorem lem_heaviest_prefix_locator_floor (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {c N K m s A₀ H wₒ : ℕ} (hc : 0 < c) (hcn : c ∣ Fintype.card ι)
    (hN : c * N = Fintype.card ι) (hsmooth : DomSmooth dom (fun x => x ^ c) c)
    (hK : K < Fintype.card ι) (hs : s < c) (hm : m ≤ N)
    (hA₀ : A₀ = m * c + s) (hA₀K : K ≤ A₀) (hA₀n : A₀ ≤ Fintype.card ι)
    (hHbound : (qrCount N (Fintype.card ι) c m s : ℝ) / (Fintype.card B : ℝ) ^ wₒ ≤ (H : ℝ)) :
    ∃ (U : ι → F) (_ : ∀ i, U i ∈ B), HasList (RSpoly dom K) (1 - (A₀ : ℝ) / Fintype.card ι) U H := by
  sorry

/-
**`thm:quotient-remainder-deep-floor` — deep-band quotient-remainder error floor.**

If a `B`-valued received word carries a list of `L ≥ 1` distinct degree-`< k+1`
codewords at agreement `A ∈ {k+1, …, n}` (deep), then the correlated-agreement error of
`C = RS[F, D, k]` is bounded below by the deep-list floor `𝓔_{q,k}(L)` at every radius
`δ ∈ [1 − A/n, 1 − k/n)`.  This is `thm:quotient-remainder-deep-floor` in the form that
combines the prefix floors above with Theorem A.
-/
theorem thm_quotient_remainder_deep_floor (dom : ι → F) (hdom : Function.Injective dom)
    {k A L : ℕ} (hk : 0 < k) (hL : 1 ≤ L) (hAlo : k < A) (hAn : A ≤ Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (U : ι → F) (hlist : HasList (RSpoly dom (k + 1)) (1 - (A : ℝ) / Fintype.card ι) U L)
    (δ : ℝ) (hδlo : 1 - (A : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k L ≤ ecaErr (RSpoly dom k) δ δ := by
  obtain ⟨ P, hP₁, hP₂, hP₃ ⟩ := hlist;
  -- For each `i`, membership `P i ∈ RSpoly dom (k+1)` gives (by `Classical.choice`) a polynomial `Q i : Polynomial F` with `(Q i).degree < ((k+1 : ℕ) : WithBot ℕ)` and `∀ x, P i x = (Q i).eval (dom x)`; hence `(Q i).degree ≤ (k : WithBot ℕ)` (since `degree < k+1` means `degree ≤ k`).
  obtain ⟨Q, hQ⟩ : ∃ Q : Fin L → Polynomial F, (∀ i, (Q i).degree ≤ (k : WithBot ℕ)) ∧ (∀ i x, P i x = (Q i).eval (dom x)) := by
    choose Q hQ₁ hQ₂ using hP₁;
    refine' ⟨ Q, _, _ ⟩ <;> simp_all +decide [ Polynomial.degree_le_iff_coeff_zero ];
    exact fun i m hm => Polynomial.coeff_eq_zero_of_degree_lt <| lt_of_lt_of_le ( hQ₁ i ) <| WithBot.coe_le_coe.mpr hm;
  apply RSCap.ecaFloor_le_ecaErr_deep_list hL dom hdom δ U Q;
  · exact hQ.1;
  · intro i j hij h; have := @hP₂ i j; simp_all +decide [ funext_iff ] ;
  · intro i
    specialize hP₃ i
    simp [relDist] at hP₃;
    rw [ div_le_iff₀ ( Nat.cast_pos.mpr <| Fintype.card_pos_iff.mpr ⟨ Classical.choose <| Finset.card_pos.mp <| show 0 < Fintype.card ι from by linarith ⟩ ) ] at hP₃;
    convert hP₃.trans ( mul_le_mul_of_nonneg_right hδlo <| Nat.cast_nonneg _ ) using 1;
    exact congr_arg _ ( congr_arg _ ( by ext; simp +decide [ hQ.2 i ] ; tauto ) );
  · nlinarith [ show ( k : ℝ ) + 1 ≤ A by norm_cast, show ( A : ℝ ) ≤ Fintype.card ι by norm_cast, div_mul_cancel₀ ( A : ℝ ) ( show ( Fintype.card ι : ℝ ) ≠ 0 by norm_cast; linarith ), div_mul_cancel₀ ( k : ℝ ) ( show ( Fintype.card ι : ℝ ) ≠ 0 by norm_cast; linarith ) ];
  · exact_mod_cast hq

/-
**`cor:quotient-remainder-trigger` — trigger for the quotient-remainder floor.**

If the quotient-remainder list size exceeds `(q − n)/k`, then the correlated-agreement
error of `C = RS[F, D, k]` exceeds the half-inverse-dimension threshold throughout the
deep band `δ ∈ [1 − A/n, 1 − k/n)`.
-/
theorem cor_quotient_remainder_trigger (dom : ι → F) (hdom : Function.Injective dom)
    {k A L : ℕ} (hk : 0 < k) (hAlo : k < A) (hAn : A ≤ Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (U : ι → F) (hlist : HasList (RSpoly dom (k + 1)) (1 - (A : ℝ) / Fintype.card ι) U L)
    (htrig : ((Fintype.card F : ℝ) - Fintype.card ι) / k < L)
    (δ : ℝ) (hδlo : 1 - (A : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k) δ δ := by
  refine' lt_of_lt_of_le _ ( RSCap.thm_quotient_remainder_deep_floor dom hdom hk _ hAlo hAn hq U hlist δ hδlo hδhi );
  · convert RSCap.ecaFloor_trigger _ _ _ _ |>.2 htrig using 1;
    · field_simp;
    · exact Nat.cast_pos.mpr ( Fintype.card_pos );
    · exact_mod_cast hq;
    · positivity;
    · exact lt_of_le_of_lt ( div_nonneg ( sub_nonneg.2 hq.le ) ( Nat.cast_nonneg _ ) ) htrig;
  · exact Nat.one_le_iff_ne_zero.mpr ( by rintro rfl; norm_num at htrig; exact absurd htrig ( by exact not_lt_of_ge ( div_nonneg ( sub_nonneg.mpr hq.le ) ( Nat.cast_nonneg _ ) ) ) )

/-- **`cor:quantitative-first-grid-floor` — unconditional first-grid floor.**

For any Reed–Solomon code `C = RS[F, D, k]` on an `n`-point domain (no smoothness),
the correlated-agreement error is at least the deep-list floor `𝓔_{q,k}(C(n, k+1))`
across the first grid band `δ ∈ [1 − (k+1)/n, 1 − k/n)`. -/
theorem cor_quantitative_first_grid_floor (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hk : 0 < k) (hkn : k < Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (δ : ℝ) (hδlo : 1 - (k + 1 : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k (Nat.choose (Fintype.card ι) (k + 1))
      ≤ ecaErr (RSpoly dom k) δ δ := by
  sorry

/-- **`cor:first-grid-cap` — first-grid cap.**

Let `c ∣ gcd(n, k)`; if `c > 1` assume `D` is a multiplicative coset, and if
`C(n/c, k/c + 1) ≥ q/k + 1`, then both `ε_ca` and `ε_mca` of `C = RS[F, D, k]` at the
grid radius `1 − (k+c)/n` exceed the half-inverse-dimension threshold.  For `c = 1` this
is the first closed grid point below capacity and needs no smoothness. -/
theorem cor_first_grid_cap (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {c N k : ℕ} (hk : 0 < k) (hkn : k < Fintype.card ι)
    (hc : 0 < c) (hcnk : c ∣ Nat.gcd (Fintype.card ι) k)
    (hN : c * N = Fintype.card ι) (hsmooth : DomSmooth dom (fun x => x ^ c) c)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card F : ℝ) / k + 1 ≤ (Nat.choose N (k / c + 1) : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
        < ecaErr (RSpoly dom k)
            (1 - (k + c : ℝ) / Fintype.card ι) (1 - (k + c : ℝ) / Fintype.card ι)
      ∧ (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
        < emcaErr (RSpoly dom k) (1 - (k + c : ℝ) / Fintype.card ι) := by
  sorry

end RSCap