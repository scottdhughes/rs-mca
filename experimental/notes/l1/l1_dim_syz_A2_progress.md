# L1 `dim Syz <= K` — A2 (2026-07-06): 3-engine verified + a realizability identity (redundant)

- **Status:** VERIFICATION + structural lead. No proof of the crux; the crux `dim Syz <= K` (K>=3) stays OPEN.
- **Crux (from `l1_e3_subspace_upper_bound.md`):** `Syz = {(q_k): sum h_k q_k=0, deg q_k<=mu_k-2}`,
  want `dim Syz <= K`. K=2 proved; tight (`=K` at saturators); FAILS for arbitrary pairwise-coprime
  `h_k` (needs the single-Gamma realizability).

## Scripts verified on THREE independent engines (dim Syz = K)
Sage (`syzygy_generators_e3.sage`), PARI (`syzygy_xcheck.gp`), and now **Macaulay2**
(`l1_syz_m2_crosscheck.m2`, data from `l1_syz_export_data.sage`) all give `dim Syz = K`,
`dim(sum V_k) = E_3`, at ell=11/13/17: K=4/7/6, E_3=9/11/15. Load-bearing computation is solid.

## Realizability identity found + verified (but redundant)
`l1_syz_gamma_identity.sage`. Using `g_k h_k = X^ell - w_k` and `Gamma = c_k + g_k s_k`
(`s_k=(Gamma-c_k)/g_k`): multiplying an h-syzygy by Gamma,
`Gamma*sum h_k q_k = sum c_k h_k q_k + X^ell*(sum q_k s_k) - sum w_k s_k q_k`,
and the degree-`>=ell` part forces **`sum_k q_k s_k = 0`**. VERIFIED: every h-syzygy is an s-syzygy at
all 3 saturators. **BUT redundant** — it is auto-satisfied (dim(h-syz AND s-syz) = dim(h-syz) = K), so
it does not cut the dimension. A valid rigidity the arbitrary configs lack, but not the closer.

## Next A2 leads (open)
1. **Leading-block staircase argument.** The syzygy basis is triangular/staircase (ell=11: q_0=1,X,X^2,X^3
   with the rest determined) -> dim Syz = #free leading monomials = K. Prove a syzygy is determined by
   its leading-block projection (the naive per-`q_k` leading-coeff map failed by 1-2; use the block).
2. **s-module / iterate.** Work with the lower-degree `s_k` (closer to Gamma); does the s-syzygy module
   have a cleaner structure that bounds the h-syzygies?
3. **Route a clean sub-lemma to Aristotle** once (1) or (2) isolates one (abstracted finite-field algebra).

## Alternative L1 route (from the thread-C lit dive)
For L1 a FINITE `r* ~ 8-16` suffices (route-A CAS finding), so the cohomological higher-moment method
(Hast-Matei singular-variety moments at fixed p via Quantitative Sheaf Theory, Sawin-Forey-Fresan-Kowalski)
could CLOSE L1 via `Gamma_r` -- a second, geometric route distinct from `dim Syz <= K`.

## A2 update — staircase pivot structure (`l1_syz_staircase.sage`)

Greedy pivots with **largest-fiber-first** ordering: `#pivots = E_3`, `#free = K` at all 3 saturators;
the K dependencies concentrate in the **smallest** fibers (the μ=3 fibers go entirely free; the largest
fibers are all pivots). Second fact: at the saturators `dim(ΣV_k) = E_3 = ℓ−2`, i.e. the `h_k X^d`
**span the whole `ker L = ker⟨·, rev Γ⟩`**. So the crux `dim(ΣV_k) ≥ E_3` is: *the largest-fiber-first
greedy selection produces `E_3` independent `h_k X^d`* — realizability-dependent (arbitrary configs give
rank `< E_3`). Mechanism (why the small fibers add only `K` dependencies) still not crisp; the clean
Aristotle sub-lemma is not yet isolated. Leads to try next: the dual functional space
`{m : ⟨h_k X^d, m⟩ = 0 ∀k,d}` (Prony/reciprocal condition; `L=rev Γ` is one such `m`) and whether
realizability caps its dimension at `ℓ−1−E_3`.

## A2 update — dual formulation (`l1_syz_dual.sage`, verified)

The crux `dim(ΣV_k) ≥ E_3` is dual to: the annihilator `A = {m ∈ 𝔽_p[X]_{≤ℓ-2} : ⟨h_k X^d, m⟩ = 0,
d≤μ_k-2, all k}` has `dim A ≤ ℓ-1-E_3`. Since `⟨h_k X^d, m⟩ = [X^{ℓ-1-d}](h_k·m*)` (m* = reverse of m),
this says **`h_k·m*` has a top-window coefficient gap at degrees `[ℓ+1-μ_k, ℓ-1]` for every k**.
`rev(Γ)` is an explicit solution, forced by the realizability identity
`h_k Γ = c_k h_k + (X^ℓ-w_k) s_k` (every term is out of that degree window). **VERIFIED at all 3
saturators: `dim A = 1 = ℓ-1-E_3` and `A = ⟨rev Γ⟩` exactly.**

So the clean sub-lemma to attack/route to Aristotle:
> A polynomial `m*` of degree `≤ ℓ-2` whose products `h_k·m*` all have the top-window gap
> `[ℓ+1-μ_k, ℓ-1]` (co-fiber locators `h_k` from a single Γ of degree `≤ ℓ-1`) spans, together with the
> `≤ ℓ-1-E_3` slack, only the line `⟨rev Γ⟩` — i.e. `dim A ≤ ℓ-1-E_3`.

This is a **reciprocal/Prony gap statement with an explicit distinguished solution** — arguably more
tractable than the primal syzygy count, and the mechanism (why rev Γ works) is now explicit.
