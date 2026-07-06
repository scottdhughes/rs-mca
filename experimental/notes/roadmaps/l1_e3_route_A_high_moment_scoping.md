# Route A scoping: the high-moment (`Gamma_r`) hierarchy for `E_3 <= ell-2`

- **Status:** SCOPING (tools + literature + CAS). 2026-07-06.
- **Verifier:** `../scripts/moment_hierarchy_e3.sage`. Library: `../../literature/high-moment-charsum/`.

## The reduction (exact)

`M_r := sum_b sum_c N_b(c)^r = #{(x_1,...,x_r) in (F_p^*)^r : x_1^ell=...=x_r^ell, Gamma(x_1)=...=Gamma(x_r)}`
-- the **r-fold coincidence count** (an explicit `F_p`-variety point count / character sum). Since
`mu_b = max_c N_b(c)`, `(sum_c N_b(c)^r)^{1/r} -> mu_b`, so
`B_r := sum_b ((sum_c N_b(c)^r)^{1/r} - 2)_+  ↓  E_3`  as `r -> inf`.
`E_3 <= ell-2` follows once a **provable bound on `M_r`** makes `B_r <= ell-2`.

## CAS findings (`moment_hierarchy_e3.sage`)

- **`r*` is small at toy scale:** `B_r` reaches `E_3` (`=ell-2` at saturators) by **`r ~ 8-16`** for
  `ell=11,17` (not `10^5`; the paper's `r*~10^5` is the *deployed* scale `ell~2^21`). So the hierarchy
  is a genuinely **finite** route for the sub-problem.
- **`L^r -> L^infty` transition visible:** max-fiber is `28%` of `M_r` at `r=2`, `100%` by `r=8`
  (why the 2nd moment / pair-cap provably misses it).
- **Extremal vs random cleanly separated:** random `Gamma` has `B_4 ~ 0.9`, `B_8 ~ 0.03` (collapses),
  extremal stays at `E_3`. The moment gap IS the obstruction, computably.

## The one open sub-problem

**Bound `M_r` (r-fold coincidence count) sharply enough at `r ~ ell` that `B_r <= ell-2` for ALL
mixed `Gamma`.** At `r=2` this is the elementary pair-cap `<= (ell-1)(ell-2)` (proved, not sharp).
At `r ~ ell` the naive per-frequency Weil bound hits the `sqrt(p)` barrier (CAP25 Rem 16.10). Beating
it needs the *cyclotomic / index* structure of `Gamma` restricted to `mu_ell`-cosets.

## Literature toolkit (`../../literature/high-moment-charsum/`)

- **Wan, *Index bounds for character sums of polynomials*** -- improves Weil for polynomials of small
  **index** (cyclotomic structure); directly applicable to `M_r`, whose summand `Gamma` on the coset
  `x^ell=w` is exactly index-structured. **First tool to try.**
- **Kowalski, *Exponential sums over small subgroups, revisited* (BGK)** -- additive-combinatorics
  bounds for exponential sums over multiplicative subgroups (`mu_ell`). The route to the **inverse
  theorem** (CAP25 lines 7543, 8144) if index bounds fall short.
- **Cesarano-Matera, *value sets of (cyclotomic-mapping) polynomials* I/II + probabilistic** -- the
  moment framework for value-set / fiber distributions of `x -> x^ell`-structured polynomials; the
  closest published analog of our `Gamma_r`.

## What it would take (concrete plan)

1. Write `M_r` as an explicit character sum over `mu_ell^{r-1} x (additive freq)^{r-1}`, exposing the
   **index** of `Gamma` on each coset.  Tool: Sage/PARI, cross-check exact `M_r` (already have).
2. Apply **Wan's index bound** to the inner sums; get `M_r <= main + index-improved error`. Check
   (CAS) whether it yields `B_r <= ell-2` at `r ~ ell` for the toy cases.  Tool: PARI (`lfun`,
   char sums), **python-flint/Arb** for *rigorous* moment enclosures (referee-grade).
3. If the index bound is insufficient, escalate to **BGK additive combinatorics** (Kowalski) for the
   inverse theorem: large `M_r` => structured (quotient-stabilizer) support.
4. Cross-check any bound on a second engine (Oscar arithmetic-Galois of the coincidence variety;
   PARI ⟂ Sage), and on larger `ell` via the research CPU box / RunPod.

**Feasibility.** Promising, genuine analytic-NT research (your wheelhouse). The Wan-index step is a
concrete, self-contained first move with a computable pass/fail at toy `ell`. Tools: all in hand
(PARI, flint/Arb, Sage, Oscar). No new tooling; a technique (index-bound / additive-combinatorics)
that neither we nor CAP25 has applied to this exact `M_r`.
