import cs25_cap_v12.BlueprintCommon

/-!
# Blueprint: circle codes, Chebyshev fibers, and torus uniformization (`sec:circle-geometry`, `sec:answers-stereo`)

Skeletons (proofs `sorry`) for the circle-code section of

  P. Chojecki, *Universal Field-Size Caps and a Two-Sided Sandwich for Mutual
  Correlated Agreement on Smooth Reed–Solomon Domains*.

Throughout, `F ⊇ F_{p²}` is a finite field containing an element `i` with `i² = −1`.
The `x`-coordinate map on the norm-one torus is `χ(u) = (u + u⁻¹)/2`, and the
Chebyshev polynomials `T_a` (Mathlib's `Polynomial.Chebyshev.T`) satisfy the
semiconjugacy `T_a(χ(u)) = χ(uᵃ)`.  Twin cosets `𝒟 = gH ∪ g⁻¹H` give `x`-coordinate
domains `D = χ(𝒟)` on which `T_a` is `(T_a, a)`-smooth.

Formalized here:

* `chebyshev_semiconjugacy` — the Chebyshev semiconjugacy `T_a(χ(u)) = χ(uᵃ)`.
* `lem_cheb_fibers` — `lem:cheb-fibers`: an `x`-coordinate twin-coset domain is
  `(T_a, a)`-smooth (`DomSmooth`).
* `circleCode` and `lem_circle_rs` — `lem:circle-rs`: the degree-`≤ w` circle code
  equals a diagonally twisted Reed–Solomon code `RS[F, E', 2w+1]` on the torus domain,
  hence has identical list sizes and CA/MCA errors.
* `cor_circle_grand` — `cor:circle-grand`: the universal cap for circle-FRI line-round
  rows.
* `lem_stereographic` — `lem:stereographic`: the stereographic uniformization,
  requiring no `i`, giving circle codes over every challenge field.
-/

namespace RSCap

open Classical Polynomial

variable {ι F : Type*} [Fintype ι] [Field F] [Fintype F]

/-- The `x`-coordinate (Chebyshev/torus projection) map `χ(u) = (u + u⁻¹)/2`. -/
noncomputable def chi (u : F) : F := (u + u⁻¹) / 2

/-- **Chebyshev semiconjugacy** `T_a(χ(u)) = χ(uᵃ)` for `u ≠ 0`.  This is the identity
underlying the tower structure of circle-FRI line rounds. -/
theorem chebyshev_semiconjugacy (u : F) (hu : u ≠ 0) (a : ℕ) :
    (Polynomial.Chebyshev.T F (a : ℤ)).eval (chi u) = chi (u ^ a) := by
  sorry

/-- **`lem:cheb-fibers` — exact Chebyshev fibers on `x`-coordinate twin-coset domains.**

If `dom` is the `x`-coordinate image `χ ∘ (torus twin-coset domain)` and `a ∣ M`
satisfies the twin-coset scale condition, then `dom` is `(T_a, a)`-smooth: every fiber
of `x ↦ T_a(x)` over the domain has exactly `a` elements.  Phrased via `DomSmooth` with
the Chebyshev evaluation map. -/
theorem lem_cheb_fibers (dom : ι → F) (hdom : Function.Injective dom)
    (torus : ι → F) (htorus : ∀ i, torus i ≠ 0)
    (hdomχ : ∀ i, dom i = chi (torus i)) {a : ℕ} (ha : 0 < a)
    (htwin : ∀ i, (Finset.univ.filter (fun j => (torus j) ^ a = (torus i) ^ a ∨
        (torus j) ^ a = ((torus i) ^ a)⁻¹)).card = 2 * a) :
    DomSmooth dom (fun x => (Polynomial.Chebyshev.T F (a : ℤ)).eval x) a := by
  sorry

/-- The degree-`≤ w` circle code `𝒞_w(F, E)` on a set of circle points `pt`, using the
canonical free-module form `f₀(x) + y·f₁(x)` with `deg f₀ ≤ w`, `deg f₁ ≤ w − 1`. -/
def circleCode (pt : ι → F × F) (w : ℕ) : Set (ι → F) :=
  {c | ∃ f0 f1 : Polynomial F, f0.degree ≤ (w : WithBot ℕ) ∧
        f1.degree < (w : WithBot ℕ) ∧
        ∀ i, c i = f0.eval (pt i).1 + (pt i).2 * f1.eval (pt i).1}

/-- **`lem:circle-rs` — torus uniformization of circle codes.**

With `i ∈ F`, `i² = −1`, the coordinate `u = x + iy` sends the circle point `pt i` to
the torus point `torus i`; then the degree-`≤ w` circle code equals the diagonally
twisted Reed–Solomon code `RS[F, E', 2w+1]` on the torus domain, the twist being
`t i = (torus i)^(−w)`.  Consequently the two codes have identical list sizes and
identical `ε_ca`, `ε_mca` at every radius. -/
theorem lem_circle_rs (pt : ι → F × F) (torus : ι → F) (w : ℕ)
    (i_unit : F) (hi : i_unit ^ 2 = -1)
    (hcircle : ∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1)
    (htorus : ∀ j, torus j = (pt j).1 + i_unit * (pt j).2) (htne : ∀ j, torus j ≠ 0) :
    circleCode pt w
      = (fun c i => (torus i) ^ (-(w : ℤ)) * c i) '' RSpoly torus (2 * w + 1) := by
  sorry

/-- **`cor:circle-grand` — universal circle-row cap.**

Assembling `lem_circle_rs` (list-size equality) with the map-smooth universal cap on
the torus domain, every circle-FRI line-round row is unsafe at its first staircase
step: for `C = 𝒞_w(F, E)` of odd RS dimension `k = 2w+1` under the field-size
hypothesis, `ε_mca(C, δ)` exceeds the threshold across the deep band.  Stated here for
the uniformized RS code. -/
theorem cor_circle_grand (torus : ι → F) (hdom : Function.Injective torus)
    (B : Subfield F) [Fintype B] {w N a k : ℕ}
    (hk : k = 2 * w + 1) (ha : 0 < a) (haN : a * N = Fintype.card ι)
    (hsmooth : DomSmooth torus (fun x => x ^ a) a)
    (hq : (Fintype.card ι : ℝ) < Fintype.card F)
    (hyp : (Fintype.card B : ℝ) * ((Fintype.card F : ℝ) / k + 1)
        ≤ (Nat.choose N (k / a + 2) : ℝ))
    (δ : ℝ) (hδlo : 1 - (a * (k / a + 2) : ℝ) / Fintype.card ι ≤ δ)
    (hδhi : δ < 1 - (k : ℝ) / Fintype.card ι) :
    (1 / (2 * (k : ℝ))) * (1 - (Fintype.card ι : ℝ) / (Fintype.card F))
      < emcaErr (RSpoly torus k) δ := by
  sorry

/-- **`lem:stereographic` — stereographic uniformization, no `i` required.**

Over every finite field of odd characteristic, the stereographic map identifies the
degree-`≤ w` circle code with a Reed–Solomon code on the stereographic-image domain
`s(E)`, without needing `i ∈ F`.  This yields circle codes (and their universal caps)
over every challenge field.  Stated as an equality of the circle code with a twisted
RS code under an explicit stereographic domain `sdom`. -/
theorem lem_stereographic (pt : ι → F × F) (w : ℕ)
    (hchar : (2 : F) ≠ 0)
    (hcircle : ∀ j, (pt j).1 ^ 2 + (pt j).2 ^ 2 = 1)
    (sdom : ι → F) (twist : ι → F) (htw : ∀ i, twist i ≠ 0) :
    circleCode pt w = (fun c i => twist i * c i) '' RSpoly sdom (2 * w + 1) := by
  sorry

end RSCap
