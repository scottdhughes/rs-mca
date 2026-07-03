import cs25_cap_v12.TheoremA

set_option maxHeartbeats 8000000

/-!
# The universal cap: the main reduction (`thm:main`)

This file formalizes the core reduction of the paper's headline

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*, **universal cap**
  (`thm:main`).

The proof of `thm:main` combines two ingredients:

* **Theorem A** (`RSCap.deep_list_size_le`, already formalized in `TheoremA.lean`):
  in the deep regime, a small correlated-agreement error forces a small list.
* **The fiber lemma** (`lem:fiber`, *locator fibers are lists*): the multiplicative
  coset construction producing, for a suitable base-valued received word, a list of
  `≥ C(N,ℓ₂)/|B|` distinct low-degree codewords.

Here we formalize the reduction itself: **assuming the fiber-list output**
(stated as the hypothesis `hfiber`, exactly what `lem:fiber` provides), together
with the field-size hypothesis `(eq:hyp)`, Theorem A yields the universal cap

  `(1/2k)(1 - n/q) < ε_ca(RS[F,D,k], δ)`.

The fiber lemma itself (the elementary-symmetric / power-map coset construction
supplying `hfiber`) is the remaining input; it is the only unformalized step of
`thm:main`, and is isolated cleanly here as `hfiber`.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-
**Universal cap, main reduction (`thm:main`).**  Let `C = RS[F,D,k]` on an
injective evaluation domain `dom`, with `n = |ι| < q = |F|` and `k < (1-δ)n`
(deep-integral radius).  Suppose the field-size hypothesis `(eq:hyp)`
`|B|·(q/k + 1) ≤ C(N,ℓ₂)` holds, and that the fiber lemma supplies a received word
`U` carrying a list of `L` pairwise-distinct polynomials of degree `≤ k`, all
`δ`-close to `U`, with `C(N,ℓ₂)/|B| ≤ L`.  Then

  `(1/2k)(1 - n/q) < ε_ca(RS[F,D,k], δ)`.

Equivalently, at every such radius the correlated-agreement error strictly exceeds
the half-inverse-dimension threshold: no such radius is `ε*`-admissible for
`ε* ≤ (1/2k)(1 - n/q)`.
-/
theorem universal_cap_of_fiber_list
    (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hk : 0 < k) (δ : ℝ)
    (hak : (k : ℝ) < (1 - δ) * Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    {N ℓ Bc : ℕ} (hBc : 0 < Bc)
    (hyp : (Bc : ℝ) * ((Fintype.card F : ℝ) / k + 1) ≤ (Nat.choose N ℓ : ℝ))
    (hfiber : ∃ (U : ι → F) (L : ℕ) (P : Fin L → Polynomial F),
        1 ≤ L ∧ (∀ i, (P i).degree ≤ (k : WithBot ℕ)) ∧
        (∀ i j, i ≠ j → P i ≠ P j) ∧
        (∀ i, ((Finset.univ.filter (fun x => (P i).eval (dom x) ≠ U x)).card : ℝ)
          ≤ δ * Fintype.card ι) ∧
        (Nat.choose N ℓ : ℝ) / (Bc : ℝ) ≤ (L : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k) δ δ := by
  obtain ⟨ U, L, P, hL, hPdeg, hPdist, hclose, hLge ⟩ := hfiber;
  contrapose! hLge;
  refine' lt_of_le_of_lt ( deep_list_size_le hk hL dom hdom δ U P hPdeg hPdist hclose hak hq _ _ ) _;
  exact 1 / 2;
  · norm_num;
  · convert hLge using 1 ; ring;
  · field_simp at *;
    nlinarith [ ( by norm_cast : ( 1 : ℝ ) ≤ Bc ), ( by norm_cast : ( 1 : ℝ ) ≤ k ) ]

/-- **Universal cap, mutual form (`thm:main`, MCA conclusion).**  Under the same
hypotheses as `universal_cap_of_fiber_list`, the *mutual* correlated-agreement
error exceeds the threshold: `(1/2k)(1 - n/q) < ε_mca(RS[F,D,k], δ)`.  This
follows by `RSCap.eca_le_emca` (`ε_ca ≤ ε_mca`) from the CA form, and is the
conclusion consumed by the grand-challenge corollaries. -/
theorem universal_cap_emca_of_fiber_list
    (dom : ι → F) (hdom : Function.Injective dom)
    {k : ℕ} (hk : 0 < k) (δ : ℝ)
    (hak : (k : ℝ) < (1 - δ) * Fintype.card ι)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    {N ℓ Bc : ℕ} (hBc : 0 < Bc)
    (hyp : (Bc : ℝ) * ((Fintype.card F : ℝ) / k + 1) ≤ (Nat.choose N ℓ : ℝ))
    (hfiber : ∃ (U : ι → F) (L : ℕ) (P : Fin L → Polynomial F),
        1 ≤ L ∧ (∀ i, (P i).degree ≤ (k : WithBot ℕ)) ∧
        (∀ i j, i ≠ j → P i ≠ P j) ∧
        (∀ i, ((Finset.univ.filter (fun x => (P i).eval (dom x) ≠ U x)).card : ℝ)
          ≤ δ * Fintype.card ι) ∧
        (Nat.choose N ℓ : ℝ) / (Bc : ℝ) ≤ (L : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < emcaErr (RSpoly dom k) δ := by
  exact lt_of_lt_of_le
    (universal_cap_of_fiber_list dom hdom hk δ hak hq hBc hyp hfiber)
    (eca_le_emca (RSpoly dom k) δ)

end RSCap