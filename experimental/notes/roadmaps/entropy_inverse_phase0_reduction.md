# Entropy-inverse crux, Phase 0: reduce to step 5 + one algebraic bridge (2026-07-10)

Goal of Phase 0: collapse `prob:entropy-inverse-q` (`grande_finale.tex`, the dense-regime max-fiber / Rényi
inverse theorem = the `(PF)/(MA)` hypotheses of `rs_mca_entropy_frontiers.tex`) to a **single** open
additive-combinatorics statement, with every other step of its six-step skeleton either machine-checked or
stated as a precise conditional. This note does that. It does **not** prove step 5.

## The skeleton and Phase-0 status

`prob:entropy-inverse-q` dichotomy: `Γ_ℓ ≥ exp(ηNℓ)` ⟹ (a) positive-density piece in a removed algebraic
cell, or (b) a positive-density Vandermonde **rank defect**. Six-step proof (`rem:entropy-inverse-skeleton`):

| Step | Content | Phase-0 status |
|---|---|---|
| 1–2 | extract popular fibers → signed moment-trades | standard (setup) |
| 3 | Tao BCH/Vandermonde barrier kills low-support trades | our reciprocal-gap + `FrobeniusClosure` (in main, #466) |
| 4 | entropy-BSG → small-doubling trade population | standard-ish |
| **5** | **Green–Ruzsa/PFR structuralization → low-rank coset progression** | **OPEN — the single hard core** |
| **6** | **slice-derivative → per-column rank defect** | **stated below as a conditional bridge** |
| (b)-kill | Vandermonde columns of distinct points are independent | **MACHINE-CHECKED** — `VandermondeRank.columns_linearIndependent` |

**Step (b)-kill is now done** (`experimental/lean/powersum_rigidity/PowersumRigidity/VandermondeRank.lean`,
zero-`sorry`, `#print axioms = [propext, Classical.choice, Quot.sound]`): for `t ≤ R` distinct points and
nonzero weights, the scaled Vandermonde columns `v_i = ρ_i(1,y_i,…,y_i^{R-1})` are linearly independent, so
their span has dimension `t` (`no_low_dim`). Hence a positive-density (`t = Θ(n)`) subset of moment-curve
columns cannot lie in any `o(n)`-dimensional subspace — alternative (b) is impossible in the range `R = Θ(n)`.

## The slice-derivative lemma, as a precise conditional target (step 6)

Step 6 is the bridge from step-5's structure on trade **sums** to a rank defect on individual **columns**.
State it independently of step 5 (assume step-5's output, conclude (b)):

> **Slice-derivative lemma (target).** Let `T`, `R = Θ(N)`, `v_t = ρ(t)(1,t,…,t^{R-1})` as in
> `prob:entropy-inverse-q`. Suppose a positive-density family of balanced trades
> `{Y^{(α)} ∈ {-1,0,1}^T : α ∈ A}`, `|A| ≥ exp(-o(N))·(random count)`, has its sum-set
> `{Φ(Y^{(α)}) = Σ_t Y^{(α)}_t v_t : α ∈ A}` contained in a **rank-`r` coset progression** `P ⊆ K^R` with
> `r = o(N)` (the step-5 output). Then there is a positive-density set `U ⊆ T` with
> `rank_K span{v_t : t ∈ U} < min(|U|, R)`.

The name records the intended mechanism: **slice** the trade family along coordinates (fix all but a bounded
window of `T`), and take **discrete derivatives** (differences `Y^{(α)} − Y^{(β)}` of trades agreeing off a
slice). A difference supported on few coordinates has sum `Σ_{t∈slice}(Y^{(α)}_t − Y^{(β)}_t) v_t`, still
inside `P − P` (rank `2r`); ranging over the density of trades exhibits many such short combinations of the
`v_t` living in a rank-`o(N)` set, which is the column-level rank defect. The precise interface to pin is the
**exact form of the step-5 coset progression** `P` (rank, dimensions, torsion) — that is the one hypothesis
this lemma consumes and step 5 must produce.

## The resulting reduction (Phase-0 deliverable)

Given the slice-derivative lemma and the machine-checked (b)-kill, `prob:entropy-inverse-q` reduces to a
**single** statement — **step 5**: from a large Rényi collision excess at the exponential fiber scale
`exp(-Θ(n))`, extract a positive-density trade family whose sums lie in a rank-`o(N)` coset progression. This
is the exp-scale PFR / Rényi structuralization flagged in `rem:standard-inverse-gap` ("the missing point is the
scale"; standard PFR/GGMT24 is polynomial-scale). Phase 1 (reconnaissance: is the trade population
small-doubling → step 5, or free-energy-decaying → the direct Sidon bound of L869?) decides whether the
free-energy branch (analytic, character-sum, our lane) can carry the deployed rows or whether step-5 PFR is
unavoidable. The slice-derivative lemma itself is algebraic (moment-curve/Vandermonde) and attackable now,
conditional on the `P`-interface.
