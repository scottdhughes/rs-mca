import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: rational-map fiber floors and the genus-one / ECFFT rows (`sec:ecfft`, `sec:answers-isogeny`)

Skeletons (proofs `sorry`) for the rational-map generalization of the fiber lemma and
its ECFFT/genus-one consequences in

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

A *rationally smooth* domain uses a rational map `ψ = f/g` (`f, g ∈ B[X]` coprime,
`a = deg f > e = deg g ≥ 0`, `g` nonvanishing on `D`); it is `(ψ, a)`-smooth if every
nonempty fiber has exactly `a` elements.  The FFTree domains of ECFFT are `(ψ, 2)`-smooth
of degree type `(a, e) = (2, 1)` for each `2`-isogeny's `x`-coordinate map.

Formalized here:

* `prop_rational_floor` — `prop:rational-floor`: the unified `(a, e)` fiber floor,
  producing a list of `≥ C(N, ℓ)/|B|` codewords of `RS[F, D, k'+1]` with
  `k' = aℓ − 2(a−e)` at radius `1 − aℓ/n`, from the word
  `u_z = (f^ℓ + z·f^{ℓ−1}g)|_D`.
* `cor_ecfft_onestep` — `cor:ecfft-onestep`: every ECFFT row `(a,e) = (2,1)` has an
  unsafe first staircase step: `ε_ca(C, 1 − ρ − 2/n) > (1/2k)(1 − n/q)`.
* `prop_graded_rational_floor` — `prop:graded-rational-floor`: graded prefix floors on
  every rational scale, giving a macroscopic unsafe band.
* `cor_ecfft_macroscopic` — `cor:ecfft-macroscopic`: the resulting macroscopic universal
  cap for genus-one rows.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- `(ψ, a)`-smoothness of a domain for a rational map `ψ = f/g` (`def:rational-smooth`):
`g` is nonvanishing on `D` and every fiber of `x ↦ f(x)/g(x)` has exactly `a` elements. -/
def RationalSmooth (dom : ι → F) (f g : Polynomial F) (a : ℕ) : Prop :=
  (∀ i, g.eval (dom i) ≠ 0) ∧ DomSmooth dom (fun x => f.eval x / g.eval x) a

/-- **`prop:rational-floor` — rational-map fiber floor, unified `(a, e)` form.**

Let `dom` be `(ψ, a)`-smooth over `B` with `ψ = f/g` of degree type `(a, e)`,
`a > e ≥ 0`, `N = n/a`, and `2 ≤ ℓ ≤ N − 1`.  With `k' = aℓ − 2(a − e)`, some slope
`z ∈ B` makes the word `u_z(x) = f(x)^ℓ + z·f(x)^{ℓ−1}·g(x)` carry a list of at least
`C(N, ℓ)/|B|` distinct codewords of `RS[F, D, k'+1]` at radius `1 − aℓ/n` (i.e. at
agreement `aℓ = k' + 2(a − e)`). -/
theorem prop_rational_floor (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {a e N k' ℓ : ℕ}
    (hfB : ∀ n, f.coeff n ∈ B) (hgB : ∀ n, g.coeff n ∈ B)
    (hae : e < a) (hfdeg : f.natDegree = a) (hgdeg : g.natDegree = e)
    (haN : a * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g a)
    (hℓlo : 2 ≤ ℓ) (hℓhi : ℓ ≤ N - 1) (hk' : k' = a * ℓ - 2 * (a - e)) :
    ∃ (z : F) (_ : z ∈ B) (L : ℕ),
      (Nat.choose N ℓ : ℝ) / (Fintype.card B : ℝ) ≤ (L : ℝ) ∧
      HasList (RSpoly dom (k' + 1))
        (1 - (a * ℓ : ℝ) / Fintype.card ι)
        (fun i => (f.eval (dom i)) ^ ℓ + z * (f.eval (dom i)) ^ (ℓ - 1) * g.eval (dom i)) L := by
  sorry

/-- **`cor:ecfft-onestep` — every ECFFT row has an unsafe first staircase step.**

For an ECFFT domain that is `(ψ, 2)`-smooth over `B` (degree type `(2, 1)`), with
`C = RS[F, D, k]`, `2 ∣ k`, `ρ = k/n ∈ [1/16, 1/2]`, `n < q < 2^256`, `n ≥ 2^12`, and
`ℓ = (k+2)/2 ≤ N − 1`, the field-size count `C(n/2, (k+2)/2) ≥ |B|·(q/k + 1)` holds,
and consequently the correlated-agreement error exceeds the threshold at the first
staircase step: `ε_ca(C, 1 − ρ − 2/n) > (1/2k)(1 − n/q)`. -/
theorem cor_ecfft_onestep (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {N k ℓ : ℕ}
    (hfB : ∀ n, f.coeff n ∈ B) (hgB : ∀ n, g.coeff n ∈ B)
    (hfdeg : f.natDegree = 2) (hgdeg : g.natDegree = 1)
    (h2N : 2 * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g 2)
    (hk : 0 < k) (hkeven : Even k) (hℓ : ℓ = (k + 2) / 2) (hℓN : ℓ ≤ N - 1)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose (Fintype.card ι / 2) ((k + 2) / 2) : ℝ)) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k)
          (1 - (k : ℝ) / Fintype.card ι - 2 / Fintype.card ι)
          (1 - (k : ℝ) / Fintype.card ι - 2 / Fintype.card ι) := by
  sorry

/-- **`prop:graded-rational-floor` — graded prefix floors on rational scales.**

At every admissible scale, the graded prefix construction (heaviest-prefix locator
combined with the rational fiber map) produces a received word whose list at the
corresponding radius has size at least the graded prefix count `H`, giving a lower
bound `ε_ca(C, δ) ≥ 𝓔_{q,k}(H)` across a macroscopic band of radii `δ`.  Stated here
abstractly via `HasList` and the deep-list floor `ecaFloor`. -/
theorem prop_graded_rational_floor (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {a e N k : ℕ}
    (hae : e < a) (hfdeg : f.natDegree = a) (hgdeg : g.natDegree = e)
    (haN : a * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g a)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F) (hk : 0 < k)
    (δ : ℝ) (H : ℕ) (hH : 1 ≤ H)
    (hlist : ∃ U : ι → F, HasList (RSpoly dom (k + 1)) δ U H)
    (hδ : 1 - (k : ℝ) / Fintype.card ι ≤ 1) :
    ecaFloor (Fintype.card F) (Fintype.card ι) k H ≤ ecaErr (RSpoly dom k) δ δ := by
  sorry

/-- **`cor:ecfft-macroscopic` — macroscopic universal cap for genus-one rows.**

Assembling `prop_graded_rational_floor` over the graded band gives that the
correlated-agreement error of a genus-one (ECFFT) row exceeds the half-inverse
dimension threshold not just at one step but throughout a macroscopic sub-capacity
band `δ ∈ [1 − ρ − Δ, 1 − ρ)` of width `Δ` bounded below by an absolute constant
times the code rate. -/
theorem cor_ecfft_macroscopic (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (f g : Polynomial F) {N k : ℕ}
    (hfdeg : f.natDegree = 2) (hgdeg : g.natDegree = 1)
    (h2N : 2 * N = Fintype.card ι) (hsmooth : RationalSmooth dom f g 2)
    (hk : 0 < k) (hkeven : Even k)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose (Fintype.card ι / 2) ((k + 2) / 2) : ℝ))
    (Δ : ℝ) (hΔ : 0 < Δ)
    (δ : ℝ) (hδlo : 1 - (k : ℝ) / Fintype.card ι - Δ ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < emcaErr (RSpoly dom k) δ := by
  sorry

end RSCap
