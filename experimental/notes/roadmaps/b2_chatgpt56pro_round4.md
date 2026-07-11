ROUND 4 — the correct target. Your round-3 scale correction was right: the object to bound is not any centered
square-root cancellation but directly the multiplicative worst-case list size. I verified the arithmetic
(v_p(p^n(N−μ))=n−w, so the centered sum lives at scale p^n; a p^{n/2} target was my error). So please attack the
RIGHT statement below. It is a genuinely open, $1M-adjacent list-decoding bound; think hard, be rigorous, flag
every gap, and give numerically checkable inequalities. A real proof idea or a precise reduction to a named
theorem beats a survey; do not re-derive the ruled-out approaches.

## THE TARGET (worst-case multiplicative list size / binary MDS codewords)

p prime, n=2^k, n | p−1; μ_n = {a∈F_p: a^n=1}, |μ_n|=n. For v∈F_p^w,
    N(v) = #{ S⊆μ_n : |S|=m, Σ_{a∈S} a^j = v_j for j=1..w }  =  #{ BINARY weight-m codewords of the cyclic
    [n, n−w, w+1] Reed–Solomon/MDS code, in coset v }.
Let μ = C(n,m)/p^w (the average fiber). PROVE, for a fixed absolute K:
    N(v) ≤ n^K · max(1, μ)   for all v.      (equivalently N_max ≤ n^{O(1)} in the deployed window where μ is poly)
Deployment: n=2^21, p=2^31−2^24+1≈2^31 (≈1016 n), w=67471, m≈0.468 n, μ≈n^{1.7}. TARGET N_max ≤ n^3.

## The sharp parameter is the BIT DEFICIT, not any aspect ratio

Δ := log₂C(n,m) − w log₂p = log₂ μ. Deployment is polynomial-scale because w log₂p / n ≈ 0.997 — a KNIFE EDGE:
γ = (w+1)/n = 0.03217 vs the information-theoretic cap γ_cap = H₂(m/n)·log_p 2 = 0.03227 (worst weight n/2:
μ_{n/2}~n^{300}). Deployment sits ~200 powers of p below the cap. Any proof must live at this knife edge.

## What is ESTABLISHED / VERIFIED (use freely; do not re-derive)

- The MDS weight distribution counts ALL F_p-weight-m codewords (~C(n,m)p^{m−d}); our N(v) counts the BINARY
  ones — a p^{−(m−d)}-sparse subset. The binary/0-1 restriction IS the hard part; MacWilliams weight enumeration
  does NOT capture it. The complete-weight-enumerator identity
      N(v) = p^{−(w+1)} Σ_{s∈F_p} Σ_{t∈F_p^w} ψ(−sm − t·v) ∏_{a∈μ_n}(1 + ψ(s + Σ_j t_j a^j))
  is exact and is the same exponential sum as every other formulation (Hankel–Gauss, Fourier). No support-only
  Fourier decay helps: |cos(π y/p)|^n = 1−o(1) at deployment. Genuine joint phase cancellation is required.
- MOMENT route: N_max ≤ (Σ_v N(v)^r)^{1/r}, and Σ_v N(v)^r = Γ_r = #{r-tuples of m-subsets with a common
  syndrome}. To reach N_max ≤ n^K μ one needs r ≈ w log p / (K log n) ≈ 10^5/K, with Γ_r ≤ e^{o(n)}·(random) —
  i.e. an r-fold Vinogradov / primitive-collision-moment bound at LARGE r. This is the crux in moment form.

## RULED OUT (verified — do not propose)
- Any absolute-value / magnitude method (L^2, L^{2k} restriction, Halász): sign-blind; Cauchy–Schwarz loses
  p^{w/2}; the needed cancellation is signed.
- Per-frequency Weil for deg-w subgroup sums: vacuous since w=67471 > √p≈46340 (the "head-depth" wall, w≤21–22).
- Rudnev / high-dim incidences: only F_p^2, F_p^3, blocked at dim w≥4.
- BSG/Freiman: the fibers are nearly-Sidon (large doubling); structure theorems vacuous.
- Hankel–Gauss rank-by-rank cancellation (CHG): false uniformly (counterexample at w=n−2) AND wrong-scaled.

## YOUR TASK — prove N(v) ≤ n^K max(1,μ). Pick the strongest; be concrete.

(A) MOMENT / Γ_r at the knife edge. Bound Γ_r = Σ_v N(v)^r ≤ (r-dependent) · μ^{r−1} C(n,m) for r ≈ w log p/log n,
    exploiting that Δ is barely positive. The r-fold collision Γ_r counts r-tuples of m-subsets of μ_n with equal
    first w power sums; the trades (differences) kill w power sums (support ≥ w+2, Vandermonde). Is there an
    efficient-congruencing / decoupling / nested-efficient r-fold bound for the SUBGROUP moment curve that
    beats the trivial μ^{r−1}C(n,m)·(large) — using the specific arithmetic (n=2^k, the KoalaBear p, w<√... )?
(B) DIRECT binary list-decoding. Bound the number of BINARY (0/1) weight-m codewords of the [n,n−w,w+1] RS code
    directly: e.g. a Johnson-type / Elias–Bassalygo argument using the code's distance w+1 together with the
    0/1 constraint; or a polynomial method / Croot–Lev–Pach slice-rank bound on {S: e_1(S)=..=e_w(S)=0}; or an
    entropy / container argument for sparse solution sets of a linear system with moment-curve coefficients.
    Does the distance w+1 (large, ~0.03n) force list size poly at the deployed agreement?
(C) A genuinely new route to N ≤ n^K μ, or a proof the deployed instance is polynomial that uses the knife-edge
    Δ>0 essentially.
(D) If N_max can exceed n^{O(1)} at deployment, give the explicit family — a set of m-subsets of μ_n with an
    anomalously large common (p_1,…,p_w).

Deliver the single most promising line as a concrete inequality with the exact exponent, the role of the bit
deficit Δ, an honest gap statement, and a small (p,n,w) computation I can run to test the key step.
