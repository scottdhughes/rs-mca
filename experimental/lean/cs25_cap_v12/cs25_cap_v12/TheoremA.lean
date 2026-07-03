import cs25_cap_v12.Main

/-!
# Theorem A: the deep-point list-to-CA conversion

This file assembles the previously formalized *polynomial engine* of the deep-list
floor (`RSCap.poly_deep_list_bucket_bound`, `RSCap.simple_pole_far`) together with
the error definitions (`RSCap.ecaErr`, `RSCap.ecaFloor`) into the paper's central
structural theorem:

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*, **Theorem A**
  (deep-point list-to-CA conversion).

We model a Reed–Solomon code by polynomial evaluation on an injective evaluation
domain `dom : ι → F` (so `n = |ι|` and the domain is `D = range dom ⊆ F`), degree
`< k`.  The headline result `RSCap.ecaFloor_le_ecaErr_deep_list` says: if there is
a received word `U` carrying a list of `L` distinct polynomials of degree `< k+1`
that are all `δ`-close to `U` on `D` (in the *integral* deep regime `a = n - f > k`),
then the correlated-agreement error of `RS[F,D,k]` at radius `δ` is at least the
deep-list floor `𝓔_{q,k}(L) = ecaFloor q n k L`.  This is exactly the probabilistic
lower bound `ε_ca ≥ 𝓔_{q,k}(L)` at the heart of Theorem A; the contrapositive turns
list mass into a list-size bound.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The Reed–Solomon code `RS[F, D, k]` with evaluation domain `D = range dom`
(`dom : ι → F`) and degree bound `< k`: the words `i ↦ Q(dom i)` for `deg Q < k`. -/
def RSpoly (dom : ι → F) (k : ℕ) : Set (ι → F) :=
  {c | ∃ Q : Polynomial F, Q.degree < (k : WithBot ℕ) ∧ ∀ i, c i = Q.eval (dom i)}

/-
**Closeness from agreement on a large support.**  If a word `w` differs from
the codeword `i ↦ Q(dom i)` (for `deg Q < k`) on at most `δ·n` coordinates, then
`w` is `δ`-close to `RS[F, D, k]`.
-/
theorem caClose_of_codeword_agree (dom : ι → F) (k : ℕ) (δ : ℝ)
    (w : ι → F) (Q : Polynomial F) (hQ : Q.degree < (k : WithBot ℕ))
    (hn : 0 < (Fintype.card ι : ℝ))
    (hagree : ((Finset.univ.filter (fun x => w x ≠ Q.eval (dom x))).card : ℝ)
      ≤ δ * Fintype.card ι) :
    caClose (RSpoly dom k) δ w := by
  refine' ⟨ fun i => Q.eval ( dom i ), _, _ ⟩;
  · exact ⟨ Q, hQ, fun i => rfl ⟩;
  · exact div_le_iff₀ hn |>.2 hagree

/-
**The simple-pole auxiliary word is far from the interleaved code.**  For a
pole `α ∉ D` and a deep radius (`k < (1-δ)·n`), the auxiliary slope word
`g_α(x) = -(x-α)⁻¹` cannot be jointly explained on any support of size `> k`: a
degree-`< k` polynomial matching `g_α` at `> k` domain points would make
`(X-α)·G+1` a degree-`≤ k` polynomial with `> k` roots, contradicting
`simple_pole_far`.  Hence `(f, g_α)` is not `δ`-close to `RS[F,D,k]^{≡2}` for any
`f`.
-/
theorem not_intClose_simple_pole (dom : ι → F) (hdom : Function.Injective dom)
    (k : ℕ) (δ : ℝ) (α : F) (hα : ∀ i, dom i ≠ α)
    (hak : (k : ℝ) < (1 - δ) * Fintype.card ι)
    (f : ι → F) :
    ¬ intClose (RSpoly dom k) δ f (fun x => -(dom x - α)⁻¹) := by
  refine' fun ⟨ c1, hc1, c2, hc2, h ⟩ => _;
  -- Let `T` be the set of indices where `f i = c1 i` and `-(dom i - α)⁻¹ = c2 i`.
  set T := Finset.univ.filter (fun i => f i = c1 i ∧ -(dom i - α)⁻¹ = c2 i) with hT_def
  have hT_card : T.card > k := by
    -- By definition of `relDist2`, we know that `relDist2 f (fun x => -(dom x - α)⁻¹) c1 c2 ≤ δ` implies that the number of indices where `f i ≠ c1 i` or `-(dom i - α)⁻¹ ≠ c2 i` is at most `δ * Fintype.card ι`.
    have hT_card : (Finset.univ.filter (fun i => f i ≠ c1 i ∨ -(dom i - α)⁻¹ ≠ c2 i)).card ≤ δ * Fintype.card ι := by
      convert mul_le_mul_of_nonneg_right h ( Nat.cast_nonneg ( Fintype.card ι ) ) using 1 ; norm_num [ relDist2 ] ; ring!;
      rw [ mul_assoc, mul_inv_cancel₀ ( Nat.cast_ne_zero.mpr <| Nat.ne_of_gt <| Fintype.card_pos_iff.mpr ⟨ Classical.choose <| Finset.card_pos.mp <| show 0 < Fintype.card ι from Nat.pos_of_ne_zero <| by rintro h; norm_num [ h ] at hak; linarith ⟩ ), mul_one ] ; congr ; ext ; ring;
    have := Finset.card_add_card_compl ( Finset.filter ( fun i => f i ≠ c1 i ∨ - ( dom i - α ) ⁻¹ ≠ c2 i ) Finset.univ ) ; simp_all +decide;
    exact_mod_cast ( by nlinarith [ ( by norm_cast : ( Finset.card ( Finset.filter ( fun i => ¬f i = c1 i ∨ ¬- ( dom i - α ) ⁻¹ = c2 i ) Finset.univ ) : ℝ ) + Finset.card ( Finset.filter ( fun i => f i = c1 i ∧ - ( dom i - α ) ⁻¹ = c2 i ) Finset.univ ) = Fintype.card ι ) ] : ( k : ℝ ) < Finset.card ( Finset.filter ( fun i => f i = c1 i ∧ - ( dom i - α ) ⁻¹ = c2 i ) Finset.univ ) );
  -- On `T`, `-(dom i - α)⁻¹ = G.eval (dom i)`. Since `dom i ≠ α` (hα), `dom i - α ≠ 0`, so multiply: `(dom i - α) * G.eval (dom i) + 1 = 0`.
  obtain ⟨G, hG⟩ : ∃ G : Polynomial F, G.degree < (k : WithBot ℕ) ∧ ∀ i, c2 i = G.eval (dom i) := by
    finiteness
  have hT_eq : ∀ i ∈ T, (dom i - α) * G.eval (dom i) + 1 = 0 := by
    grind;
  -- By `simple_pole_far α G` (needs `G.natDegree < k`), the latter set has card `≤ k`.
  have hT_card_le : (Finset.univ.filter (fun x => (x - α) * G.eval x + 1 = 0)).card ≤ k := by
    convert simple_pole_far α G _ using 1;
    by_cases hG_zero : G = 0 <;> simp_all +decide [ Polynomial.degree_eq_natDegree ];
    exact Nat.pos_of_ne_zero ( by rintro rfl; exact absurd hT_card ( by simp +decide [ sub_eq_zero, hα ] ) );
  exact hT_card.not_ge ( le_trans ( by rw [ ← Finset.card_image_of_injective _ hdom ] ; exact Finset.card_le_card ( fun x hx => by aesop ) ) hT_card_le )

/-
**The simple-pole line point is close.**  For a pole `α ∉ D`, a received word
`U`, and a list polynomial `P` of degree `< k+1` agreeing with `U` on all but
`≤ δ·n` domain points, the line point with slope `P(α)`,
`x ↦ U(x)/(x-α) + P(α)·(-(x-α)⁻¹)`, is `δ`-close to `RS[F,D,k]`.  Indeed on the
agreement support it equals `(P(x)-P(α))/(x-α)`, the restriction of the
degree-`< k` quotient polynomial.
-/
omit [Fintype F] in
theorem caClose_simple_pole_line (dom : ι → F) (k : ℕ) (δ : ℝ) (α : F)
    (hα : ∀ i, dom i ≠ α) (hn : 0 < (Fintype.card ι : ℝ))
    (U : ι → F) (P : Polynomial F) (hPdeg : P.degree ≤ (k : WithBot ℕ))
    (hclose : ((Finset.univ.filter (fun x => P.eval (dom x) ≠ U x)).card : ℝ)
      ≤ δ * Fintype.card ι) :
    caClose (RSpoly dom k) δ
      (fun x => U x / (dom x - α) + (P.eval α) * (-(dom x - α)⁻¹)) := by
  -- Let $v = P(\alpha)$. The polynomial $P - C v$ has root $\alpha$, so $(X - C \alpha)$ divides $(P - C v)$.
  set v := P.eval α
  set Q : Polynomial F := (P - Polynomial.C v) /ₘ (Polynomial.X - Polynomial.C α);
  refine' ⟨ fun x => Q.eval ( dom x ), ⟨ Q, _, _ ⟩, _ ⟩;
  · by_cases hP : P - Polynomial.C v = 0;
    · simp +zetaDelta at *;
      simp +decide [ hP ];
    · have := Polynomial.degree_divByMonic_lt ( P - Polynomial.C v ) ( Polynomial.monic_X_sub_C α );
      exact lt_of_lt_of_le ( this hP ( Polynomial.degree_X_sub_C α ▸ by simp +decide ) ) ( Polynomial.degree_sub_le _ _ |> le_trans <| max_le hPdeg ( Polynomial.degree_C_le.trans <| by simp +decide ) );
  · exact fun _ => rfl;
  · -- On the set where `P.eval (dom x) = U x` (agreement of P with U), for `dom x ≠ α` (hα) we have:
    have h_agree : ∀ x, P.eval (dom x) = U x → (U x / (dom x - α) + v * (-(dom x - α)⁻¹)) = Q.eval (dom x) := by
      intro x hx
      have h_div : (P - Polynomial.C v).eval (dom x) = (dom x - α) * Q.eval (dom x) := by
        have h_div : (P - Polynomial.C v) = (Polynomial.X - Polynomial.C α) * Q := by
          rw [ Polynomial.mul_divByMonic_eq_iff_isRoot.mpr ] ; aesop;
        simpa using congr_arg ( Polynomial.eval ( dom x ) ) h_div;
      simp_all +decide [ sub_eq_iff_eq_add ];
      grind +splitImp;
    refine' div_le_of_le_mul₀ _ _ _ <;> try positivity;
    · nlinarith;
    · refine' le_trans _ hclose;
      exact_mod_cast Finset.card_le_card fun x hx => by contrapose! hx; aesop;

/-
**Theorem A, probabilistic form (deep-point list-to-CA conversion).**  Let
`C = RS[F, D, k]` on an injective domain `dom : ι → F` with `n = |ι| < q = |F|`.
Suppose a received word `U` carries a list of `L ≥ 1` pairwise-distinct
polynomials `P₀, …, P_{L-1}` of degree `< k+1`, each agreeing with `U` on all but
`≤ δ·n` domain points, and that the radius is deep-integral (`k < (1-δ)·n`).
Then the correlated-agreement error satisfies

  `𝓔_{q,k}(L) = ecaFloor q n k L ≤ ε_ca(C, δ)`.

The proof: pick a good pole `α ∈ F ∖ D` via `poly_deep_list_bucket_bound`, at which
the `L` interpolation values `Pᵢ(α)` take at least `L(q-n)/(q-n+kL)` distinct
values; each distinct value is a CA-bad slope for the simple-pole pair
`(U(·)/(·-α), -(·-α)⁻¹)` by `caClose_simple_pole_line` and
`not_intClose_simple_pole`; dividing by `q` gives the floor.
-/
theorem ecaFloor_le_ecaErr_deep_list {k L : ℕ} (hL : 1 ≤ L)
    (dom : ι → F) (hdom : Function.Injective dom) (δ : ℝ)
    (U : ι → F) (P : Fin L → Polynomial F)
    (hPdeg : ∀ i, (P i).degree ≤ (k : WithBot ℕ))
    (hPdist : ∀ i j, i ≠ j → P i ≠ P j)
    (hclose : ∀ i, ((Finset.univ.filter (fun x => (P i).eval (dom x) ≠ U x)).card : ℝ)
      ≤ δ * Fintype.card ι)
    (hak : (k : ℝ) < (1 - δ) * Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k L ≤ ecaErr (RSpoly dom k) δ δ := by
  have h_Ω : ∃ α : F, α ∉ Finset.image dom Finset.univ ∧
    (L : ℝ) * ((Fintype.card F - Fintype.card ι) : ℝ) / ((Fintype.card F - Fintype.card ι) + (k : ℝ) * L)
      ≤ ((Finset.univ.image (fun i => (P i).eval α)).card : ℝ) := by
        obtain ⟨α, hα⟩ : ∃ α ∈ Finset.univ \ Finset.image dom Finset.univ, (L : ℝ) * (Finset.univ \ Finset.image dom Finset.univ).card / ((Finset.univ \ Finset.image dom Finset.univ).card + k * L) ≤ ((Finset.univ.image (fun i => (P i).eval α)).card : ℝ) := by
          convert poly_deep_list_bucket_bound hL P _ _ _ _;
          · refine' Finset.card_pos.mp _;
            simp +decide [ Finset.card_sdiff, Finset.card_image_of_injective _ hdom ];
            exact_mod_cast hq;
          · exact fun i j => le_trans ( Polynomial.natDegree_sub_le _ _ ) ( max_le ( Polynomial.natDegree_le_of_degree_le ( hPdeg i ) ) ( Polynomial.natDegree_le_of_degree_le ( hPdeg j ) ) );
          · exact hPdist;
        simp_all +decide [ Finset.card_sdiff, Finset.card_image_of_injective _ hdom ];
        exact ⟨ α, hα.1, by simpa only [ Nat.cast_sub hq.le ] using hα.2 ⟩;
  obtain ⟨α, hα_not_mem, hα_card⟩ := h_Ω
  have h_caBad : ∀ v ∈ Finset.image (fun i => (P i).eval α) Finset.univ, caBad (RSpoly dom k) δ δ (fun x => U x / (dom x - α)) (fun x => -(dom x - α)⁻¹) v := by
    rintro v hv
    obtain ⟨i, hi⟩ : ∃ i : Fin L, v = (P i).eval α := by
      grind;
    refine' ⟨ _, _ ⟩;
    · convert caClose_simple_pole_line dom k δ α _ _ U ( P i ) ( hPdeg i ) ( hclose i ) using 1;
      · aesop;
      · exact fun i hi => hα_not_mem <| hi ▸ Finset.mem_image_of_mem _ ( Finset.mem_univ _ );
      · contrapose! hak; aesop;
    · apply not_intClose_simple_pole dom hdom k δ α (by
      exact fun i hi => hα_not_mem <| hi ▸ Finset.mem_image_of_mem _ ( Finset.mem_univ _ )) (by
      exact hak) (fun x => U x / (dom x - α));
  have h_prob : prob (fun γ => caBad (RSpoly dom k) δ δ (fun x => U x / (dom x - α)) (fun x => -(dom x - α)⁻¹) γ) ≥ ((Finset.univ.image (fun i => (P i).eval α)).card : ℝ) / (Fintype.card F) := by
    exact div_le_div_of_nonneg_right ( mod_cast Finset.card_le_card fun x hx => by aesop ) ( Nat.cast_nonneg _ );
  refine' le_trans _ ( h_prob.trans _ );
  · convert div_le_div_of_nonneg_right hα_card ( Nat.cast_nonneg ( Fintype.card F ) ) using 1;
    rw [ecaFloor, mul_comm]; grind;
  · exact Finset.le_sup' ( fun p : ( ι → F ) × ( ι → F ) => prob ( fun γ => caBad ( RSpoly dom k ) δ δ p.1 p.2 γ ) ) ( Finset.mem_univ ( ( fun x => U x / ( dom x - α ) ), fun x => - ( dom x - α ) ⁻¹ ) )

/-
**Theorem A, list-size form (deep-point list-to-CA conversion).**  The
contrapositive of `ecaFloor_le_ecaErr_deep_list`: in the deep-integral regime,
if the correlated-agreement error of `C = RS[F,D,k]` at radius `δ` is small,
`ε_ca(C,δ) ≤ η·(1/k - n/(kq))` for some `η < 1` (the paper's `η ∈ [0,1)`;
the hypothesis `0 ≤ η` turned out to be unnecessary), then any list of `L`
distinct degree-`< k+1` polynomials `δ`-close to a common received word `U`
satisfies `L ≤ q·ε_ca(C,δ)/(1-η)`.  (Taking the maximum over `U` and lists,
this is the list-size bound `Lst(RS[F,D,k+1],δ) ≤ ⌈q·ε_ca/(1-η)⌉` of Theorem A.)
-/
theorem deep_list_size_le {k L : ℕ} (hk : 0 < k) (hL : 1 ≤ L)
    (dom : ι → F) (hdom : Function.Injective dom) (δ : ℝ)
    (U : ι → F) (P : Fin L → Polynomial F)
    (hPdeg : ∀ i, (P i).degree ≤ (k : WithBot ℕ))
    (hPdist : ∀ i j, i ≠ j → P i ≠ P j)
    (hclose : ∀ i, ((Finset.univ.filter (fun x => (P i).eval (dom x) ≠ U x)).card : ℝ)
      ≤ δ * Fintype.card ι)
    (hak : (k : ℝ) < (1 - δ) * Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    {η : ℝ} (hη1 : η < 1)
    (hε : ecaErr (RSpoly dom k) δ δ
      ≤ η * (1 / (k : ℝ) - (Fintype.card ι : ℝ) / ((k : ℝ) * (Fintype.card F : ℝ)))) :
    (L : ℝ) ≤ (Fintype.card F : ℝ) * ecaErr (RSpoly dom k) δ δ / (1 - η) := by
  rw [ le_div_iff₀ ( by linarith ) ];
  have := ecaFloor_le_ecaErr_deep_list hL dom hdom δ U P hPdeg hPdist hclose hak hq;
  unfold ecaFloor at this;
  rw [ div_le_iff₀ ] at this;
  · field_simp at hε;
    nlinarith [ show ( k : ℝ ) > 0 by positivity, show ( L : ℝ ) ≥ 1 by norm_cast, show ( Fintype.card F : ℝ ) > Fintype.card ι by exact_mod_cast hq, mul_le_mul_of_nonneg_left ( show ( k : ℝ ) ≥ 1 by norm_cast ) ( show ( 0 : ℝ ) ≤ Fintype.card F by positivity ), mul_le_mul_of_nonneg_left ( show ( L : ℝ ) ≥ 1 by norm_cast ) ( show ( 0 : ℝ ) ≤ Fintype.card F by positivity ) ];
  · exact mul_pos ( Nat.cast_pos.mpr ( Fintype.card_pos ) ) ( add_pos_of_pos_of_nonneg ( sub_pos.mpr hq ) ( mul_nonneg ( Nat.cast_nonneg _ ) ( Nat.cast_nonneg _ ) ) )

end RSCap