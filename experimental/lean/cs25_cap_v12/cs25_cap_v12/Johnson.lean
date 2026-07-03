import cs25_cap_v12.Main

set_option maxHeartbeats 8000000

/-!
# The elementary Johnson list bound

This file formalizes the combinatorial core of the paper's

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*,

**elementary Johnson list bound, uniform in the interleaving arity**
(`thm:johnson-list`).

The paper states the bound for lists of codewords of `RS[F,D,k]^{≡m}`, but the
proof only uses that *two distinct listed codewords column-agree on at most `k-1`
coordinates*.  We therefore formalize the sharp abstract statement: given `L`
agreement sets `S₀,…,S_{L-1} ⊆ D` (`|D| = n`), each of size `≥ a`, with pairwise
intersections `≤ k-1`, if `a² > (k-1)n` then

  `L ≤ n·(a-k+1) / (a² - (k-1)n)`.

The proof is a double count of the degree function `deg(x) = #{i : x ∈ Sᵢ}`,
combined with the Cauchy–Schwarz bound `(∑ deg)² ≤ n·∑ deg²`
(`Finset.sq_sum_le_card_mul_sum_sq`).
-/

namespace RSCap

open Classical BigOperators

variable {D : Type*} [Fintype D] [DecidableEq D]

/-
**Double count of the total degree.**  `∑ₓ #{i : x ∈ Sᵢ} = ∑ᵢ |Sᵢ|`.
-/
theorem sum_deg_eq {L : ℕ} (S : Fin L → Finset D) :
    ∑ x : D, (Finset.univ.filter (fun i : Fin L => x ∈ S i)).card
      = ∑ i, (S i).card := by
  simp +decide only [Finset.card_filter];
  rw [ Finset.sum_comm, Finset.sum_congr rfl ] ; aesop

/-
**Double count of the squared degree.**
`∑ₓ (#{i : x ∈ Sᵢ})² = ∑ᵢ ∑ⱼ |Sᵢ ∩ Sⱼ|`.
-/
theorem sum_deg_sq_eq {L : ℕ} (S : Fin L → Finset D) :
    ∑ x : D, ((Finset.univ.filter (fun i : Fin L => x ∈ S i)).card) ^ 2
      = ∑ i, ∑ j, ((S i ∩ S j).card) := by
  simp +decide only [Finset.card_filter, pow_two];
  simp +decide only [Finset.sum_mul _ _ _, Finset.mul_sum];
  rw [ Finset.sum_comm, Finset.sum_congr rfl ] ; intros ; rw [ Finset.sum_comm ] ; simp +decide ;
  simp +decide only [Finset.inter_comm]

/-
**Elementary Johnson list bound (abstract combinatorial core, `thm:johnson-list`).**
Given `L ≥ 1` agreement sets `Sᵢ ⊆ D` (`n := |D|`) with `|Sᵢ| ≥ a` and pairwise
intersection `≤ k-1`, if `a² > (k-1)n` then `L ≤ n(a-k+1)/(a²-(k-1)n)`.
-/
theorem johnson_list_bound {L : ℕ} (hL : 1 ≤ L) (k a : ℕ) (hk : 1 ≤ k)
    (S : Fin L → Finset D)
    (ha : ∀ i, a ≤ (S i).card)
    (hinter : ∀ i j, i ≠ j → ((S i) ∩ (S j)).card ≤ k - 1)
    (hpos : ((k : ℝ) - 1) * (Fintype.card D) < (a : ℝ) ^ 2) :
    (L : ℝ) ≤ (Fintype.card D : ℝ) * ((a : ℝ) - k + 1)
      / ((a : ℝ) ^ 2 - ((k : ℝ) - 1) * (Fintype.card D)) := by
  -- Set T := ∑ x : D, (Finset.univ.filter (fun i : Fin L => x ∈ S i)).card
  set T := ∑ x : D, (Finset.univ.filter (fun i : Fin L => x ∈ S i)).card with hT_def;
  -- From `sum_deg_sq_eq` and `sum_deg_eq`, we get $T^2 \leq n \sum_{x} d(x)^2 \leq n(T + L(L-1)(k-1))$.
  have hT_sq : (T : ℝ)^2 ≤ (Fintype.card D : ℝ) * (T + L * (L - 1) * (k - 1)) := by
    have hT_sq : (T : ℝ)^2 ≤ (Fintype.card D : ℝ) * (∑ i : Fin L, ∑ j : Fin L, ((S i ∩ S j).card : ℝ)) := by
      have hT_sq : (T : ℝ)^2 ≤ (Fintype.card D : ℝ) * (∑ x ∈ Finset.univ, ((Finset.univ.filter (fun i : Fin L => x ∈ S i)).card : ℝ)^2) := by
        have hT_sq : ∀ (u : D → ℝ), (∑ x : D, u x)^2 ≤ (Fintype.card D : ℝ) * ∑ x : D, u x^2 := by
          intro u; have := Finset.univ.sum_le_sum fun x _ => pow_two_nonneg ( u x - ( ∑ y, u y ) / Fintype.card D ) ; simp_all +decide [ sub_sq, Finset.sum_add_distrib, Finset.mul_sum _ _ _ ] ;
          by_cases h : Fintype.card D = 0 <;> simp_all +decide [ ← Finset.mul_sum _ _ _, ← Finset.sum_mul ];
          · rw [ Fintype.card_eq_zero_iff ] at h ; aesop;
          · nlinarith [ mul_div_cancel₀ ( ∑ i, u i ) ( Nat.cast_ne_zero.mpr h ) ];
        aesop;
      convert hT_sq using 2;
      convert sum_deg_sq_eq S |> Eq.symm using 2 ; norm_cast;
    -- By `sum_deg_eq`, we know that $\sum_{i} |S_i| = T$.
    have hT_sum : ∑ i : Fin L, ((S i).card : ℝ) = T := by
      simp +zetaDelta at *;
      rw_mod_cast [ sum_deg_eq ];
    -- By `hinter`, we know that $\sum_{i \neq j} |S_i \cap S_j| \leq L(L-1)(k-1)$.
    have h_inter_sum : ∑ i : Fin L, ∑ j ∈ Finset.univ.erase i, ((S i ∩ S j).card : ℝ) ≤ L * (L - 1) * (k - 1) := by
      refine' le_trans ( Finset.sum_le_sum fun i hi => Finset.sum_le_sum fun j hj => Nat.cast_le.mpr ( hinter i j ( by aesop ) ) ) _ ; norm_num [ Nat.cast_sub hk ] ; ring_nf ;
      cases L <;> norm_num at * ; nlinarith;
    simp_all +decide;
    exact hT_sq.trans ( mul_le_mul_of_nonneg_left ( by linarith ) ( Nat.cast_nonneg _ ) );
  -- Since $T \geq L \cdot a$, we have $L \cdot a \leq T$.
  have hT_ge_La : (L * a : ℝ) ≤ T := by
    norm_cast;
    rw [ hT_def, sum_deg_eq ] ; exact le_trans ( by simp +decide [ Finset.sum_const ] ) ( Finset.sum_le_sum fun i _ => ha i );
  rw [ le_div_iff₀ ];
  · rcases L with ( _ | L ) <;> norm_num at *;
    by_cases h_case : (L + 1) * a ≤ (Fintype.card D : ℝ);
    · rcases k with ( _ | _ | k ) <;> norm_num at *;
      · nlinarith;
      · norm_cast at *;
        rw [ Int.subNatNat_eq_coe, Int.subNatNat_eq_coe ] ; push_cast ; nlinarith only [ h_case, hpos, mul_nonneg ( Nat.zero_le L ) ( Nat.zero_le k ) ];
    · nlinarith [ sq_nonneg ( T - ( L + 1 ) * a : ℝ ) ];
  · linarith

end RSCap