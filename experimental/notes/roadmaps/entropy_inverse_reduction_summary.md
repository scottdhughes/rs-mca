# The entropy-inverse crux, reduced and scaffolded: a referee-facing summary (2026-07-10)

Status: `SCOPING` / `PARTIAL`. Consolidates the L1-terminal reduction program (Phases 0–2) for
`prob:entropy-inverse-q` — the single conditional input `(PF)/(MA)` on which the submission-track
`rs_mca_entropy_frontiers.tex` compiler rests — and places it against the active few-shell attack
(holmbuar #476, DannyExperiments #485–503). Purpose: give a referee (and the maintainer) one map of exactly
what stands between the conditional submission and an unconditional one, with the machine-checked scaffolding.

## The crux, and the one theorem it reduces to

`rs_mca_entropy_frontiers.tex` is honestly conditional: its profile-envelope compiler rests on five explicit
hypothesis classes, the deepest being `(PF)` prefix-flat / `(MA)` major-arc = the Fourier/Sidon payment =
`prob:entropy-inverse-q`. That problem is a **max-fiber theorem**: the depth-`w` power-sum prefix map
`Φ: Ω_m → E^w` has no fiber exceeding `exp(o(N))·mean` at the deployed depth `w = 67447` (M31) / `w ≈ 4096`
(KoalaBear), past the Weil threshold `w_0 ≈ 20–45`.

**The reduction (this program):** with the six-step skeleton (`rem:entropy-inverse-skeleton`) mapped, everything
except one step is machine-checked or bounded:

| step | content | status |
|---|---|---|
| 1–2 | popular fibers → signed moment-trades | setup |
| 3 | BCH/Vandermonde barrier kills low-support trades | **Lean, in main** (reciprocal-gap + `FrobeniusClosure`, #466) |
| (b)-kill | Vandermonde rank refutes the rank-defect alternative | **Lean, zero-`sorry`** (`VandermondeRank`, #501) |
| 6 | slice-derivative bridge | stated as a precise conditional (Phase 0) |
| 5 | exp-scale / many-shell structuralization | **the single remaining open core** |

The Li–Wan payment kernel `‖p_j‖ ≤ Λ ⟹ ‖e_m‖ ≤ C(Λ+m-1,m)` is also machine-checked (`PrefixFlatness`, #498).
So the entire conditional input reduces to **step 5**, and step 5 is the max-fiber theorem.

## The crux splits: few-shell (closed) + many-shell (open) — and the open half is the free-energy branch

The max-fiber theorem splits by the number of exchange shells a fiber uses:

- **Few-shell (`s = o(n)` shells): CLOSED** by holmbuar #476 at the deployed M31 depth, via the polynomial
  method (an affine few-inner-product lemma, `|F| ≤ C(N+s,s)`) + the Chebyshev-prefix rank fact (the `(w+1)×n`
  evaluation matrix has rank `w+1`). The one-shell M31 cap is paid outright (`max_z|F_z| ≤ n−w < B*`).
- **Many-shell (`Ω(n)` distinct shells): OPEN** — the named remaining crux (`CHEBYSHEV-MANY-SHELL-RESIDUAL`).

Two facts pin our position:

1. **The many-shell branch IS the free-energy branch.** Many shells = spread trades. Our Phase 1 measured the
   primitive residual trades and found them SPREAD (doubling constant `K = Θ(|Y|)`, not `O(1)`), so the L869
   dichotomy's small-doubling/PFR escape is not triggered — the load is on the free-energy branch. Phase 2
   confirmed the free-energy decay HOLDS numerically in the dense (deployed) regime (`Γ_ℓ/main → 1`, density-
   controlled), but showed that at the deployed `ℓ = (log N)^A` the decay is EQUIVALENT to the max-fiber
   theorem itself. So the many-shell/free-energy branch is genuinely ours, genuinely open, and our current
   analytic tools bottom out on it — it needs a new idea (a many-shell hypercontractivity / entropy inverse).
2. **holmbuar's primitive-PR refutation is our #465.** "The fold line carries `>98%` of the L² energy" is our
   result that the major arcs are `exp(Θ(n))`-many quotient/fold families; a many-shell proof must retain
   cross-stratum energy. Our major-arc structure fed that refutation.

## Machine-checked scaffolding (this terminal, all zero-`sorry`)

`experimental/lean/powersum_rigidity/PowersumRigidity/`:
`FrobeniusClosure` (#466, in main) — the Frobenius-closure primitive (step 3 / backs #451);
`PrefixFlatness` (#498) — the Li–Wan payment kernel;
`VandermondeRank` (#501) — the rank fact refuting the rank-defect alternative.
All build under `lean4:v4.31.0`, `#print axioms = [propext, Classical.choice, Quot.sound]`.

**Our existing Lean already backs TWO of holmbuar #476's few-shell steps** (the concrete `#501`/`pte_rigidity` ↔
`#476` bridge, no new Lean required):
- **Chebyshev-prefix rank** (#476: the `(w+1)×n` evaluation matrix has rank `w+1`) ← `VandermondeRank`'s
  Vandermonde-nonsingularity core (`columns_linearIndependent`, `det_vandermonde_ne_zero_iff`).
- **Same-fiber exchange `≥ w+1`** (#476: via Newton identities) ← `PowersumRigidity.RigidityCorollaries.pte_rigidity`
  (`D_d = 0` for `d ≤ w`, in main): disjoint size-`d` power-sum-matching families with `d ≤ w` cannot exist.

The one un-backed step is the **affine few-inner-product lemma** (`|F| ≤ C(N+s,s)`, polynomial method) — not in
Mathlib, a from-scratch formalization scoped below.

## What is proved vs open, and the honest bottom line

- **Proved / machine-checked:** the reduction to step 5; the (b)-kill; step 3; the payment kernel; the few-shell
  branch (holmbuar); the branch identification and numerical validation of the free-energy decay in the dense
  regime.
- **Open (the single wall):** step 5 = the **many-shell max-fiber theorem** at deployed depth, confirmed as the
  sole obstruction from three independent angles (direct moments / our T5→NG route-cut #448; the L869 dichotomy;
  the free-energy analysis). It is a genuine open problem in additive combinatorics / character sums.

The conditional submission and an unconditional one differ by exactly this one theorem on the many-shell branch.

## Next Lean target (scoped)

The affine few-inner-product lemma of #476 (`|F| ≤ C(N+s,s)` for a fixed-weight family with `s` off-diagonal
inner-product values) is **not in Mathlib**; it is a from-scratch polynomial-method formalization (degree-`s`
`MvPolynomial` space of dimension `C(N+s,s)`; the diagonal evaluation system `P_x(y) = δ_{xy}·(nonzero)` giving
linear independence). Formalizing it would machine-check the CLOSED few-shell branch and is the natural next
addition to the package, alongside `VandermondeRank`.
