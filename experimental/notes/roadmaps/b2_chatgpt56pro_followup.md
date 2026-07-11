FOLLOW-UP. Your Hankel–Gauss reduction of the max-fiber problem is excellent, and I have now INDEPENDENTLY
VERIFIED its exact steps from scratch (not via your scanner): the interpolation reformulation, the sparse-layer
annihilation Σ_{supp λ=T} G_v(λ)=p^d for |T|≤d, the rank identity rank(A_λ)=|supp λ| for |supp|≤d, and — new —
the full-rank Gauss evaluation and your determinant reciprocity. So the reduction is solid; the whole problem is
now the conjecture CHG, and specifically its cleanest case Eq 29 (full rank). I need you to attack Eq 29 hard,
or supply the twisted-Elkies lemma it needs. Be rigorous, flag every gap, give checkable inequalities.

## What is now EXACTLY established (verified)

For the deployed instance (n=2^21, p=KoalaBear≈2^31, w=67471, d=n−w−1, c=w+1, r_*=n−2w−2), after centering,
    N(v) − μ = p^{−n} Σ_{r=r_*}^{d} T_r(v),   T_r(v) = Σ_{rank A_λ=r}(G_v(λ) − Ḡ_m(λ)),
and CHG (|T_r(v)| ≤ p^{n+2+(r_*−r)/2}) suffices for N_max < 0.493 n^3. The FULL-RANK case r=d (Eq 29) is:

VERIFIED FULL-RANK STRUCTURE. For a full-support λ ∈ (F_p^*)^n with A_λ nonsingular (A_λ)_{ij}=Σ_a λ_a a^{i+j}
(1≤i,j≤d), the quadratic Gauss sum evaluates EXACTLY as
    G_v(λ) = p^{d/2} · χ(det A_λ) · ε · e_p(Φ_v(λ)),   Φ_v(λ) = γ_{v,λ} − (1/4) ℓ_{v,λ}^T A_λ^{−1} ℓ_{v,λ},
where χ is the quadratic (Legendre) character, ε a fixed 4th-root-of-unity Gauss factor, and (verified)
ℓ_{v,λ,i}=Σ_a λ_a(2g_v(a)−1)a^i, γ_{v,λ}=Σ_a λ_a(g_v(a)^2−g_v(a)), g_v the fixed interpolation polynomial
(so Φ_v is a quadratic function of the syndrome v). Your Hankel DUALITY holds EXACTLY (I verified it):
    χ(det A_λ) · χ(det B_λ) = χ(∏_a λ_a),   B_λ,uv = n^{−2} Σ_a λ_a^{−1} a^{u+v}  (0≤u,v≤w),  a (w+1)×(w+1) Hankel.
Hence χ(det A_λ) = χ(∏_a λ_a)·χ(det B_λ), and Eq 29 (|T_d(v)| ≤ p^{n+2−(w+1)/2}) is EQUIVALENT to square-root
cancellation (allowing a p^2 loss) in the mixed character sum over λ ∈ (F_p^*)^n:
    S_v := Σ_{λ ∈ (F_p^*)^n, det A_λ≠0}  [ ∏_{a∈H} χ(λ_a) ] · χ(det B_λ) · e_p(Φ_v(λ)),   centered over v,
        with the TARGET  | S_v − (v-average) | ≤ p^{n/2 + 2}.

Key structural facts about S_v:
- ∏_a χ(λ_a) is a SEPARABLE product of quadratic characters (one per coordinate λ_a).
- χ(det B_λ): B_λ is a (w+1)×(w+1) HANKEL of the "dual moments" M_k := Σ_a λ_a^{−1} a^k, k=0..2w (i.e. det B_λ
  is the order-(w+1) catalecticant/Hankel determinant of the moment sequence of λ^{−1}); it depends on λ ONLY
  through those 2w+1 dual moments.
- e_p(Φ_v(λ)): Φ_v is a Schur-complement expression; by the block identity M^T diag(λ) M = diag(A_λ, B_λ), it
  should be expressible via B_λ^{−1} (please make this explicit — it is the crux of the phase).

## YOUR TASK — attack Eq 29 / S_v (be concrete)

(A) Prove | S_v − avg | ≤ p^{n/2+O(1)}. Natural routes: (i) open ∏χ(λ_a) by moving to the DUAL moments M_k via
    additive characters, so S_v = Σ_{M∈F_p^{2w+1}} χ(det B(M)) e_p(Φ_v(M)) · G(M), where G(M) = Σ_{λ: dual-moments
    =M} ∏χ(λ_a) is a χ-twisted count of vectors with prescribed moments over μ_n — is G(M) itself a clean Gauss
    sum / does it have square-root size? (ii) Katz-style equidistribution / Deligne bounds for the character sum
    Σ_λ χ(det B_λ) e_p(phase): is the family {det B_λ} a nondegenerate one whose exponential/character sums obey
    √p^{#vars} cancellation? Identify the geometric hypothesis (smoothness / nondegeneracy of the catalecticant
    hypersurface {det B=0}) and whether it holds for the moment curve.
(B) The TWISTED ELKIES LEMMA directly: Elkies computes the (untwisted) additive Fourier transform of {Hankel of
    rank ≤ r} as p^r(ω_r − ω_{r−1}) (ω_j = #degree-j factors of the dual polynomial). Extend this to the
    Fourier transform of the χ(det)-WEIGHTED, additively-phased Hankel measure, with loss at most p^{O(1)},
    uniform in the order w+1. State it and prove it, or reduce it to a known equidistribution theorem.
(C) If square-root cancellation FAILS for S_v (e.g. the χ(det B) and phase conspire on a positive-dimensional
    stratum), identify that stratum explicitly — it would either refine CHG (a smaller surviving family) or,
    if it carries ≥ p^{n/2+ω(1)} mass, DISPROVE Eq 29 in this form. Give the stratum.

Constraints: make Φ_v explicit in terms of B_λ^{−1}; state the exact nondegeneracy hypothesis you need; give a
small (p,n,w) computation I can run to test the key inequality or the nondegeneracy. Prioritize a real proof
attempt or a precise reduction to a named theorem (Katz "Sommes exponentielles", Deligne Weil II, Fouvry–Katz,
Denef–Loeser) over restating the setup. This single √-cancellation is the whole prize.
