import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: locator fibers and the map-smooth fiber lemma (`sec:fiber`, `sec:map-smooth`)

Skeletons for the fiber-construction results of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

These are the constructions that supply the list-mass input (`hfiber`) consumed by
`RSCap.universal_cap_of_fiber_list` in `MainCap.lean`.  All proofs are left as
`sorry`; the statements are intended to be faithful and directly reusable.

Formalized here (all as `theorem … := by sorry`):

* `lem_fiber_ii` — `lem:fiber`(ii): the multiplicative-coset power-map construction.
  For a base field `B ⊆ F`, an injective `B`-valued domain `dom` that is
  `(x ↦ xᵃ, a)`-smooth of order `N = n/a`, and `a ∣ k`, some slope value `z ∈ B`
  yields a received word `u_z = (xᵏ⁺²ᵃ + z·xᵏ⁺ᵃ)` carrying `≥ C(N, ℓ₂)/|B|`
  distinct codewords of `RS[F, D, k+1]` at radius `1 − ρ − 2/N`.
* `lem_phi_fiber_ii` — `lem:phi-fiber`(ii): the divisibility-free generalization to a
  general `(φ, a)`-smooth domain, with `ℓ₂ = ⌊k/a⌋ + 2`, `A₂ = a·ℓ₂`.
* `thm_phi_cap` — `thm:phi-cap`: the universal cap for map-smooth domains, assembling
  `lem_phi_fiber_ii` with Theorem A (`RSCap.deep_list_size_le`).

The pure fiber constructions are `B`-valued; the slope `z = −e₁(A)` is an elementary
symmetric function of a subset `A` of the quotient domain `Q = φ(D)`, hence lies in
`B`, and the pigeonhole is over `B` rather than `F`.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- **`lem:fiber`(ii) — locator fibers are lists (multiplicative coset).**

Let `B ⊆ F`, let `dom : ι → F` be an injective, `B`-valued evaluation domain of
size `n = |ι|` that is `(x ↦ xᵃ, a)`-smooth with quotient order `N = n/a` (so
`a·N = n`), and suppose `a ∣ k` with `ℓ₂ = ρN + 2 ≤ N` (here `ρ = k/n`, so
`ρN = k/a`).  Then there is a slope value `z ∈ B` such that the received word
`u_z(x) = xᵏ⁺²ᵃ + z·xᵏ⁺ᵃ` carries a decoding list of at least `C(N, ℓ₂)/|B|`
pairwise-distinct codewords of `RS[F, D, k+1]` at radius `1 − ρ − 2/N`; equivalently
at radius `1 − (k+2a)/n`.

This is exactly the list-mass hypothesis consumed by
`RSCap.universal_cap_of_fiber_list`. -/
theorem lem_fiber_ii (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    {a N k ℓ₂ : ℕ} (ha : 0 < a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => x ^ a) a)
    (hak : a ∣ k) (hℓ₂ : ℓ₂ = k / a + 2) (hℓ₂N : ℓ₂ ≤ N) :
    ∃ (z : F) (_ : z ∈ B) (L : ℕ),
      (Nat.choose N ℓ₂ : ℝ) / (Fintype.card B : ℝ) ≤ (L : ℝ) ∧
      HasList (RSpoly dom (k + 1))
        (1 - (k : ℝ) / Fintype.card ι - 2 / N)
        (fun i => (dom i) ^ (k + 2 * a) + z * (dom i) ^ (k + a)) L := by
  sorry

/-- **`lem:phi-fiber`(ii) — divisibility-free map-smooth fiber lemma.**

Generalizes `lem_fiber_ii` from the power map to an arbitrary `(φ, a)`-smooth,
`B`-valued domain, and removes the hypothesis `a ∣ k`.  With `ℓ₂ = ⌊k/a⌋ + 2` and
`A₂ = a·ℓ₂ ∈ [k+a+1, k+2a]`, some slope `z ∈ B` makes
`u_z(x) = φ(x)^{ℓ₂} + z·φ(x)^{ℓ₂−1}` carry `≥ C(N, ℓ₂)/|B|` distinct codewords of
`RS[F, D, k+1]` at radius `1 − A₂/n`.  Here `φ` is (the evaluation of) a polynomial
of degree `a`. -/
theorem lem_phi_fiber_ii (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (φ : Polynomial F) {a N k ℓ₂ A₂ : ℕ}
    (ha : 0 < a) (hφdeg : φ.natDegree = a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) a)
    (hℓ₂ : ℓ₂ = k / a + 2) (hℓ₂N : ℓ₂ ≤ N - 1) (hA₂ : A₂ = a * ℓ₂) :
    ∃ (z : F) (_ : z ∈ B) (L : ℕ),
      (Nat.choose N ℓ₂ : ℝ) / (Fintype.card B : ℝ) ≤ (L : ℝ) ∧
      HasList (RSpoly dom (k + 1))
        (1 - (A₂ : ℝ) / Fintype.card ι)
        (fun i => (φ.eval (dom i)) ^ ℓ₂ + z * (φ.eval (dom i)) ^ (ℓ₂ - 1)) L := by
  sorry

/-- **`thm:phi-cap` — universal cap for map-smooth domains.**

Under the field-size hypothesis `(eq:hyp-phi)` `C(N, ℓ₂) ≥ |B|·(q/k + 1)` and the
map-smoothness of `lem_phi_fiber_ii`, the correlated-agreement error of
`C = RS[F, D, k]` exceeds the half-inverse-dimension threshold at every deep radius
`δ ∈ [1 − A₂/n, 1 − ρ − 1/n]`.  This is the `(φ, a)`-smooth analogue of the main
theorem `thm:main` and specializes to it when `φ = Xᵃ`, `D` a multiplicative coset,
and `a ∣ k`. -/
theorem thm_phi_cap (dom : ι → F) (hdom : Function.Injective dom)
    (B : Subfield F) [Fintype B] (hdomB : ∀ i, dom i ∈ B)
    (φ : Polynomial F) {a N k ℓ₂ A₂ : ℕ}
    (hk : 0 < k) (ha : 0 < a) (hφdeg : φ.natDegree = a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth dom (fun x => φ.eval x) a)
    (hℓ₂ : ℓ₂ = k / a + 2) (hℓ₂N : ℓ₂ ≤ N - 1) (hA₂ : A₂ = a * ℓ₂)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose N ℓ₂ : ℝ))
    (δ : ℝ) (hδlo : 1 - (A₂ : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ ≤ 1 - (k : ℝ) / Fintype.card ι - 1 / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < ecaErr (RSpoly dom k) δ δ := by
  sorry

end RSCap
