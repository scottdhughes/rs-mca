# Problem (v2, sharpened): the crux `dim Syz ≤ K` for a level-set inequality

## Setup

Let `p` be a prime, `ℓ` an odd prime with `ℓ ∣ p−1`, and `Γ ∈ 𝔽_p[X]` nonzero with `Γ(0)=0`,
`deg Γ ≤ ℓ−1`. `𝔽_p^*` partitions into the `ℓ`-th-power cosets (fibers of `x ↦ x^ℓ`), each of
size `ℓ`. For a coset `C`, `μ(C) = max_λ #{x∈C : Γ(x)=λ}`, and `E₃ = Σ_C (μ(C)−2)₊`.

**Goal (open):** `E₃ ≤ ℓ − 2`. (Sharp; FALSE without the single-`Γ` hypothesis.)

## What is already PROVED (verified on 4 CAS engines: Sage/PARI/FLINT/Macaulay2) — you may assume these

For each excess coset (`μ_k ≥ 3`, `k=1..K`), fix a maximal level set `F_k` (size `μ_k`, value `c_k`);
`g_k = ∏_{x∈F_k}(X−x)` (deg `μ_k`), `h_k = (X^ℓ−w_k)/g_k` (deg `ℓ−μ_k`), `s_k = (Γ−c_k)/g_k`
(deg `≤ ℓ−1−μ_k`); `g_k h_k = X^ℓ−w_k`, `g_k s_k = Γ−c_k`. Let `V_k = h_k·𝔽_p[X]_{≤μ_k−2}`,
`Syz = {(q_k) : Σ h_k q_k = 0, deg q_k ≤ μ_k−2}`. Then `Σ dim V_k = E₃+K` and:

- **Upper half (PROVED, elementary):** `dim(ΣV_k) ≤ ℓ−2`, via the functional `L(A)=[X^{ℓ−1}](A·Γ)`:
  each `V_k ⊆ ker L` (degree count using `Γ = c_k + g_k s_k` and `g_k h_k = X^ℓ−w_k`), and `dim ker L = ℓ−2`.
- **Equivalence:** `E₃ ≤ ℓ−2  ⟺  dim(ΣV_k) ≥ E₃  ⟺  dim Syz ≤ K`. **So the ENTIRE problem reduces to
  proving `dim Syz ≤ K`.** This is the sole remaining goal.
- `K=2` is PROVED (pairwise-coprime `h_k` + degree bounds force `q_1=q_2=0`, `dim Syz=0`).

## Ruled-out approaches (do NOT retry — each verified to fail)

1. **Leading-coefficient injectivity fails:** the map `Syz → 𝔽_p^K`, `(q_k)↦(lc q_k)`, has nonzero
   kernel at extremal configs (the E₃-subset `{h_k X^d : d≤μ_k−3}` is dependent, rank `E₃−1` or `E₃−2`).
2. **The single-`Γ` structure is ESSENTIAL, not coprimality:** for arbitrary pairwise-coprime `h_k`,
   `dim Syz` can exceed `K` unboundedly (e.g. `h=X−1,X−2,X²−X−1`, `N=4`: `dim Syz ≥ 6 > 3`). A correct
   proof MUST use that all `F_k` are level sets of ONE `Γ` of degree `≤ ℓ−1`.
3. **The pencil / `s_k` conditions are DEPENDENT (add no constraint):** `Σ h_k q_k = 0 ⟹ Σ s_k q_k = 0`
   automatically (multiply by `Γ`: `Γ·Σh_k q_k = X^ℓ·Σs_k q_k + (deg ≤ ℓ−2)`), so imposing the pencil
   `Σ(h_k − t s_k)q_k = 0 ∀t` does not reduce `dim Syz` (verified: unchanged). Any relation obtained by
   multiplying the syzygy by a polynomial is such a dependent consequence.
4. **Second-moment / character-sum bounds are not sharp:** they give only `E₃ ≤ (ℓ−1)(ℓ−2)/6`.

## Structural facts that a proof likely must use (verified)

- **Pencil / geometry:** `X^ℓ − t·Γ − b_k(t) = g_k·(h_k − t·s_k)` with `b_k(t)=w_k−t c_k`; the `F_k`
  are common level sets of the pencil `{X^ℓ − t·Γ}`, i.e. fibers of `φ=(X^ℓ,Γ):x↦(x^ℓ,Γ(x))` of size
  `μ_k`. `E₃ ≤ ℓ−2` ⟺ `φ` has total fiber-excess `≤ ℓ−2`.
- **Exact rank criterion:** with `δ = dim(D∩Z)` (`D` = within-fiber-mean-zero, `Z` = kernel of the
  Vandermonde map on the `P=Σμ_k` fiber points), `dim Syz ≤ K ⟺ δ ≤ K`; at extremal configs `δ = K`
  exactly and `dim U = 2` where `U={A:deg≤ℓ−1, A constant on each F_k} = span{1,Γ}`.

## Request

Prove `dim Syz ≤ K` (equivalently `E₃ ≤ ℓ−2`) for `K ≥ 3`, using the single-`Γ` structure — e.g. a
rank/injectivity argument (find `K` functionals jointly injective on `Syz`, or a descent on `K`), or a
pencil/value-set (fiber-excess of `φ`) argument. A Lean-checkable proof is welcome; a prior faithful
Lean formalization of the statement + backbone (each coset has `ℓ` points, `(p−1)/ℓ` cosets, `μ≤ℓ`,
the upper half) already exists and can be assumed. Flag any additional hypothesis your proof needs.
