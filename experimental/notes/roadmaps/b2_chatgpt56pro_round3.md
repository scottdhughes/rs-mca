ROUND 3. Your Hankel–Gauss reduction was excellent AND your refutation of Eq. 29 / rank-by-rank CHG was
correct — I independently verified BOTH: (i) the exact reduction (interpolation reformulation, sparse-layer
annihilation Σ_{supp λ=T}G_v=p^d for |T|≤d, rank(A_λ)=|supp| for |supp|≤d, full-rank Gauss evaluation, and your
determinant reciprocity χ(det A_λ)χ(det B_λ)=χ(∏λ_a)); and (ii) the counterexample — I re-derived Σ_{A≠0}G_v =
p^n N(v) − p^{n−1}R(v) and computed N,R directly at (17,8,6,7): the full-rank layer differs by (p−1)p^{n−1} =
16·17^7 between two syndromes while every fiber has size ≤1, exceeding Eq. 29 by 33×. So the uniform rank-by-rank
route is dead. Now I need the RIGHT intermediate theorem for the DEPLOYED regime. Be rigorous, flag gaps, give
checkable inequalities; a real proof or a precise reduction beats a survey.

## What the counterexample and a numerical sweep tell us

The counterexample lives at c/n≈0.9 (w=n−2, so r_*=2−n<0, d=1). DEPLOYMENT is the opposite extreme:
    n=2^21, p=KoalaBear≈2^31, w=67471, c=w+1=67472, d=n−w−1, so c/n≈0.032 and r_*=n−2w−2≈n (the surviving
    rank window [r_*,d] is a NARROW band of width c near the top).
I computed the CHG ratio R_max=max_{v,r}|T_r(v)|/p^{n+(r_*−r)/2} on toys: it GROWS monotonically with c/n
(R_max ≈ 7 at c/n=0.33, 9 at 0.40, 39 at 0.50, and VIOLATES at c/n≈0.9). So the failure is a large-aspect-ratio
phenomenon; the deployed small-aspect-ratio band is untested but plausibly benign. THE QUESTION IS WHETHER
SMALL c/n RESCUES IT, and via what mechanism.

## The correct object (your Gaussian completion)

After centering, N(v)−μ = p^{−n} Σ_{r=r_*}^{d} T_r(v), and the natural Fourier-transformable measure couples
ALL rank defects h: 𝔉_β = Σ_{h=0}^{c} τ^h 𝓕_{β,h}, whose transform is supported on polynomial squares
P(X)=−T(X)^2 (deg T≤w) — the "square-cone" / Veronese resonance. That resonance carries the coherent term
~ p^{(n+c)/2} N(v). The full statement needed is a JOINT rank-and-boundary cancellation over zero-sets Z (|Z|≤w)
and nullities h:
    Σ_{Z⊆μ_n, |Z|≤w} Σ_h τ^h 𝓢_{Z,h}^{cent}(v)  =  p^n(N(v)−μ),   with target |·| ≤ p^{n/2+O(1)}.
Isolating one (Z,h) is false; the cancellation is joint.

## Where I believe the right machinery lives (from a literature sweep)

- NOT generic Katz / Denef–Sperber: the phase has positive-dimensional Morse–Bott critical manifolds
  (crit locus x_a=ε_a/(2T_t(a)) with Σε_a q(a)=2β, ε∈{±1}^n indexed by fiber subsets), so Newton-polyhedron
  nondegeneracy fails. Generic smoothness/transversality bounds do NOT apply.
- YES the moment-of-L-functions toolbox: summing Gauss sums of quadratic FORMS over a rank stratification is
  exactly the 4th/cubic-moment-of-Dirichlet-L computation (rank-r form F: Σ_x e_p(F)=t·g_p^r·p^{n−r}; sums over
  forms organized by radical/rank). This is the analytic mechanism that could produce the joint cancellation.
- Independent route: N(0) is the number of binary weight-m codewords of the cyclic [n,n−w,w+1] RS/MDS code, so
  a MacWilliams / dual-weight-distribution identity might compute N(v) with the aspect ratio built in.

## YOUR TASK — pick the strongest, make it concrete

(A) DEPLOYMENT-SPECIFIC coupled bound. Using c/n=γ small, prove Σ_{Z,h} τ^h 𝓢_{Z,h}^{cent}(v) = O(p^{n/2+Cγn}) or
    similar, i.e. show the Veronese square-cone coherent term p^{(n+c)/2}N(v) is cancelled by the boundary/rank-
    defect terms down to p^{n/2+O(1)} WHEN c/n is small. Where exactly does small γ enter — is it that the number
    of nonempty critical manifolds (fiber subsets contributing to a given P=−T^2) is ≤ p^{O(c)}, so their total
    mass is p^{(n+c)/2}·p^{O(c)}·p^{−?}, and centering + the ∑_h τ^h alternation kills the leading c-scale?
    Give the explicit bookkeeping and the sharp exponent as a function of γ; identify the threshold γ* below
    which N_max ≤ n^{O(1)} follows.
(B) MOMENT/QUADRATIC-FORM route. Organize S_v by the radical/rank of A_λ using Σ_x e_p(F)=t g_p^r p^{n−r}, and
    carry out the joint sum over rank strata as in a 4th-moment-of-L-functions computation. Does the main term
    reproduce p^n(N(v)−μ) with a power-saving error at small γ?
(C) MACWILLIAMS route. Write N(v) via the dual weight enumerator of the RS/MDS code and see whether the
    aspect ratio gives the poly bound directly, bypassing the Hankel–Gauss sum.
(D) If small γ does NOT rescue it (a critical manifold survives with mass ≥ p^{n/2+ω(1)} even at γ→0), exhibit
    the deployed-regime obstruction explicitly — that would be a genuine barrier, or a counterexample to the
    deployed bound itself.

Deliver: the sharp exponent as a function of γ=c/n and the threshold γ* (or a proof that no threshold helps),
the explicit role small γ plays, and a small (p,n,w) computation I can run to test the γ-dependence. This
aspect-ratio question is the whole game now.
