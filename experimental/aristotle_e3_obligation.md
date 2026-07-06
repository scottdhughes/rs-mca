# Problem: a level-set inequality for a low-degree polynomial on multiplicative cosets

## Setup

Let `p` be a prime and let `ℓ` be an odd prime with `ℓ ∣ p − 1`. Work in the field `𝔽_p`.
The multiplicative group `𝔽_p^*` is partitioned into `n = (p−1)/ℓ` cosets of the subgroup
`μ_ℓ` of `ℓ`-th roots of unity; each coset `C` is a fiber of the map `x ↦ x^ℓ` and has exactly
`ℓ` elements (all sharing one value `w_C := x^ℓ`).

Let `Γ ∈ 𝔽_p[X]` be a nonzero polynomial with **no constant term** and `deg Γ ≤ ℓ − 1`:
`Γ(X) = Σ_{r=1}^{ℓ−1} γ_r X^r`.

For each coset `C`, define the maximal level-set size of `Γ` on `C`:
`μ(C) := max_{λ ∈ 𝔽_p} #{ x ∈ C : Γ(x) = λ }`  (so `1 ≤ μ(C) ≤ ℓ`).

Define `E₃ := Σ_C (μ(C) − 2)_+`  (sum over all `n` cosets; `(t)_+ = max(t,0)`).

## Theorem to prove

**`E₃ ≤ ℓ − 2`.**

(This is sharp: there exist `Γ` with `E₃ = ℓ − 2`. It is FALSE for arbitrary configurations of
"fibers"; the hypothesis that a single polynomial `Γ` of degree `≤ ℓ−1` realizes all the level
sets simultaneously is essential.)

## Known reduction and partial progress (may be used or ignored)

Call a coset `C` *excess* if `μ(C) ≥ 3`; let `C_1,…,C_K` be the excess cosets and write
`μ_k = μ(C_k)`, so `E₃ = Σ_k (μ_k − 2)`. For an excess coset `C_k`, let `F_k ⊆ C_k` be a level
set of size `μ_k` with common value `c_k`, and set
- `g_k = ∏_{x∈F_k}(X − x)`  (degree `μ_k`, the *fiber locator*),
- `h_k = (X^ℓ − w_{C_k}) / g_k`  (degree `ℓ − μ_k`, the *co-fiber locator*; the division is exact
  because the `ℓ` points of `C_k` are exactly the roots of `X^ℓ − w_{C_k}`),
- `V_k = h_k · 𝔽_p[X]_{≤ μ_k − 2} ⊆ 𝔽_p[X]_{≤ ℓ − 2}`  (so `dim V_k = μ_k − 1`).

Then `Σ_k dim V_k = E₃ + K`, and one has the equivalence
`E₃ ≤ ℓ − 2  ⟺  dim(V_1 + ⋯ + V_K) ≥ E₃`.

**Upper half (already proved).** `dim(V_1 + ⋯ + V_K) ≤ ℓ − 2.`
*Proof.* Let `L : 𝔽_p[X]_{≤ ℓ−2} → 𝔽_p`, `L(A) = [X^{ℓ−1}](A·Γ)` (the coefficient of `X^{ℓ−1}`
in the product). `L ≠ 0` (if `j` is least with `γ_j ≠ 0`, `L(X^{ℓ−1−j}) = γ_j ≠ 0`), so
`ker L` has dimension `ℓ − 2`. Since `Γ` is constant `= c_k` on `F_k`, `g_k ∣ (Γ − c_k)`; write
`Γ = c_k + g_k q_k`, `deg q_k ≤ (ℓ−1) − μ_k`. Using `g_k h_k = X^ℓ − w_{C_k}`, for `0 ≤ d ≤ μ_k−2`,
`h_k X^d Γ = c_k h_k X^d + (X^ℓ − w_{C_k}) q_k X^d`; both parts have zero `X^{ℓ−1}`-coefficient by
degree count (`deg(h_k X^d) ≤ ℓ−2`; `deg(q_k X^d) ≤ ℓ−3`). Hence every `V_k ⊆ ker L` and
`dim(ΣV_k) ≤ ℓ − 2`. ∎

**Remaining crux (open).** It therefore suffices to prove `dim(V_1 + ⋯ + V_K) ≥ E₃`, equivalently
that the degree-bounded syzygy module
`Syz = { (q_1,…,q_K) : Σ_k h_k q_k = 0, deg q_k ≤ μ_k − 2 }`
has `dim Syz ≤ K`.

Known facts about `Syz`:
- **`K = 2`: proved.** The `h_k` are pairwise coprime (co-fibers of distinct cosets have disjoint
  root sets), and `h_1 q_1 = h_2 q_2` with `gcd(h_1,h_2)=1` and `deg q_i ≤ μ_i − 2 < deg h_j`
  forces `q_1 = q_2 = 0`, so `dim Syz = 0`.
- The bound `dim Syz ≤ K` is **sharp** (equality occurs).
- Computationally, `Syz` admits a triangular/"staircase" basis: ordering fibers by size, the
  generators are indexed by monomials `X^d` in the leading blocks, each extending uniquely.

## Request

Prove `E₃ ≤ ℓ − 2` (for all valid `p, ℓ, Γ`). A proof of the remaining crux `dim Syz ≤ K`
(equivalently `dim(ΣV_k) ≥ E₃`) suffices and is the preferred route; a Lean-formalizable
argument is welcome. Please flag any additional hypothesis your proof requires.
