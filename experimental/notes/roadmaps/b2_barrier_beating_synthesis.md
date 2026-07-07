# b2 / conj:Q barrier-beating attack: the synthesis and the single open lemma (2026-07-07)

- **Status:** the barrier-beating attack, run to completion. Problem reduced to ONE precise,
  well-posed open lemma in a FAVORABLE regime; wrong tools cleared; strong numeric evidence true.
  NOT a proof. Supersedes the sparse-subgroup framing in `b2_sawin_route_crux.md` (that was wrong).
- **Companions:** `b2_literature_pioneer_verdict.md`, `b2_primitive_core_numerics.md`,
  `b2_sawin_route_crux.md`, holmbuar `cap25_v13_qfin_rung_audit.md`.

## The object, in final form (three exact reductions)

1. **Fourier duality collapses the "outer t-sum" to the fiber count itself** (Li-Wan sieve identity,
   arXiv:1507.06329 Lemma 3.1). Because psi is additive, `prod_{a in S} psi(P_t(a)) = psi(<p(S),t>)`,
   so `sum_{t in F_q^w} T(t) = q^w * f(0)` and
   ```
   f(0) = #{ S subset mu_n : |S|=m, p_j(S)=0 for all j in J }   (exactly),
   ```
   `J` = exponent support of the phase (`|J|=w`). The "cancellation of sum_{t != 0} T(t)" and the
   fiber-count bound are literally the SAME statement. (So neither per-x monodromy nor a per-t bound
   is the mechanism — the content is the arithmetic of this count.)
2. **Subfield descent** (memo 0.2, VERIFIED). `n=2^21` is a 2-power, so `mu_n` lies in the base/
   quadratic subfield: **KoalaBear `v2(p-1)=24 >= 21 => mu_n subset F_p`, `|mu_n|=p^0.678` (LARGER
   than sqrt p!)**; Mersenne-31 `mu_n subset F_{p^2}`, `(p^2)^0.339`. The earlier "hyper-sparse
   `n/q~2^-165`" claim was WRONG (used `F_{p^6}`). The real regime is a **large subgroup in a small
   field** — the most favorable setting for additive combinatorics.
3. **Coding/uncertainty lens.** `p_j(S) = sum_{k in S} zeta^{jk}` is the `F_p`-DFT of `1_S` on `Z/n`
   at frequency `j`. So `f(0) = #{ 0/1 weight-m vectors in the F_p-cyclic code with Fourier-zeros
   {1..w} }`. The conjecture = "this cyclic code has near-RANDOM binary-codeword count" (`C(n,m)/p^w`).

## What is RULED OUT

- **Sawin-Shusterman (horizontal short-sum):** slope `= w >> 1` violates their slopes<=1 hypothesis
  structurally (equivalence of categories on the slope>1 part). Dead.
- **Katz big-monodromy (framework a):** dead for TWO reasons — (i) sub-sqrt(q) blindness (etale
  methods control complete sums / full G_m, invisible to the subgroup below the Weil floor), and
  (ii) the t-family sheaf is a direct sum of rank-1 Artin-Schreier sheaves => ABELIAN monodromy =>
  no vertical cancellation beyond the orthogonality that just returns the count. Matches the
  [[feedback-transport-decorrelation-trap]] "FF global stats blind to local monodromy". Do NOT invest.
- **2nd moment / naive moment hierarchy:** = holmbuar/Danny shift-pairs; controls only average
  flatness, not `f(0)`; needs `r~5886` (holmbuar #366). Dead.

## The correct architecture and the SINGLE open lemma

**Architecture:** Li-Wan distinct-coordinate sieve (exact) + a subgroup polynomial exponential-sum
bound that is **UNIFORM IN THE NUMBER OF MONOMIALS `r=|J|`**.

**The lemma (over `K=F_p` for KoalaBear, `|mu_n|=n=|K|^{0.678}`; `K=F_{p^2}` for Mersenne):**
```
exists delta>0 INDEPENDENT of |J|, s.t. max_{c != 0} | sum_{a in mu_n} psi(sum_{j in J} c_j a^j) | <= n * |K|^{-delta}.
Equivalently:  #{ S subset mu_n : |S|=m, p_j(S)=0, j in J } <= poly(n) * max(1, C(n,m)/|K|^{|J|}).
```
- **Base case `|J| in {1,2}`: a THEOREM** (Bourgain-Chang, "A Gauss sum estimate in arbitrary finite
  fields," CRAS 2006, Thm 2; prime-field subfield condition holds since `v2(p-1)=24`).
- **The genuinely open crux = the `r`-uniformity.** Every proven subgroup/Mordell bound (Bourgain
  "Mordell revisited" JAMS 2005; Bourgain-Chang; Cochrane-Pinner) has `delta = delta(r) -> 0` as the
  monomial count `r -> infinity`. Our `r = |J| = w ~ 6.7e4`. **No published theorem is uniform in `r`.**
  A per-`t` bound alone is also insufficient (needs `delta*m > w`); genuine structure of the count
  (the cyclic-code / Li-Wan arithmetic) must be used. This is the frontier: "subgroup exponential
  sums for polynomials with an unbounded number of monomials."

## Evidence and status

Numerics (this repo) show the target is very likely TRUE: fibers near-flat in the dense regime
(`E2/flat - 1 ~ 0.003`), degeneracy locus exactly `{t=0}`, `conc(max/mean)` small until the mean
drops below 1. The deployed regime is dense (mean fiber ~`2^35.7 << n^3=2^63`), so poly concentration
suffices with huge room. But the accessible scale cannot reach `w > w_0`, and the sharp bound is the
open lemma above.

## r-uniformity probe at SCALE (2026-07-07): the crux ingredient looks TRUE

`b2_runiform_probe.py` (numpy, n up to 65536 -- a thousandfold past the q^w-bound fiber DP)
computes the single subgroup sum `pi(c) = sum_{a in mu_n} e_p(sum_{j=1}^r c_j a^j)` over sampled c,
as the monomial count `r=|J|` grows. Result at n=4096 (p=12289, gamma=0.88, LARGE subgroup):
```
 r=|J|:   1     2     4     8    16    32    64   128   256   512  1024  2048
 max|pi|/sqrt(n): 1.13  2.26  2.60  2.58  2.36  2.29  2.62  2.24  2.20  2.67  2.15  2.69
```
`max|pi|/sqrt(n)` stays FLAT ~2.2-2.7 as `r` grows to `n/2` -- **sqrt(n) cancellation, UNIFORM in the
monomial count**, exactly the r-uniformity the memo flagged as the open obstruction. So the proven
Bourgain-Chang `delta=delta(r)->0` is a defect of the BOUNDS, not the truth; empirically
`delta ~ gamma/2` is r-uniform.

**Consequence — both obstructions may clear in the corrected large-subgroup regime.** With
`delta ~ gamma/2` (KoalaBear gamma=0.678 => delta~0.34) and `m ~ rho n`, `delta*m ~ 0.34*10^6 >> w=67471`,
so the Li-Wan sieve error condition `delta*m > w` (memo obstruction ii) is satisfied. The memo's
pessimism rested on (a) the lossy proven bounds and (b) the WRONG hyper-sparse regime; both are
corrected here. **So the architecture (Li-Wan sieve + r-uniform per-t bound) looks VIABLE, with
strong numeric support.**

**ADVERSARIAL CORRECTION (crucial).** Random-c sampling HID the worst case. The single-monomial probe
shows `|pi(e_j)|` is maximal at RESONANT `j | n`: `j=n/2` gives `|pi|=n` EXACTLY (no cancellation, since
`a^{n/2}=+-1`), `j=n/4` gives `0.86 n`, etc. So the FULL-sum r-uniformity is **FALSE** in worst case --
I did not overclaim from the random data (regime discipline held). BUT the bad `j` are exactly the
resonant `j | n` = the STRUCTURED / coset-union directions the descent SUBTRACTS. Restricting to the
PRIMITIVE part -- odd frequencies `j` coprime to `n` (where `x^j` PERMUTES `mu_n`) -- the worst case
is tame: single odd-monomial `0.40*sqrt(n)`, and sampled max over odd-support `c` stays FLAT at
`~3.0-3.6*sqrt(n)` as #odd-frequencies grows to 1024. **The PRIMITIVE r-uniformity holds worst-case**
(not just on average), and the primitive object IS the conjecture (`extras`, after coset-union peel).

**Structural reason (clean):** for odd `j`, `x^j` is a bijection of `mu_n`, so every single odd-monomial
sum equals the SAME subgroup Gauss sum `~sqrt(n)`; the resonances that kill even `j` are absent. This is
likely why the primitive/odd-frequency bound is r-uniform where the general one is not -- and it is a
cleaner, more tractable lemma.

**Corrected lemma:** `max_{c != 0 on ODD freqs} |sum_{a in mu_n} psi(sum_{j odd} c_j a^j)| <= C sqrt(n)`,
uniform in the number of odd frequencies. Numerically confirmed worst-case (n<=4096); the odd-j-permutes-
mu_n structure is the lever. Remaining: prove it (Mordell-over-subgroup restricted to coprime exponents),
verify the descent isolates exactly the even-j structured part, and check Li-Wan on the primitive part.

**Caveats:** sampled (400 c) not exhaustive worst-case; n<=4096 for the primitive probe; `delta*m>w`
heuristic. Strong worst-case evidence + a clean structural lever, not a proof.

## Three-front sharpening (2026-07-07): gamma-robust, algebraically isolated, Vinogradov-identified

**(1) gamma-dependence: ROBUST.** `b2_primitive_runiform.py` tests the primitive (odd-freq) worst case
across `gamma = log_p|mu_n| in {0.34, 0.5, 0.68, 0.85}` (0.34 = Mersenne deployed row in `F_{p^2}`;
0.68 = KoalaBear in `F_p`). `max|pi|/sqrt(n)` stays bounded `~2.5-4.3`, UNIFORM in r (to 512) AND across
gamma. Both deployed regimes pass; not a large-gamma artifact.

**(2) Algebraic isolation: PROVED.** If `M` is `mu_{2^s}`-symmetric then `p_j(M) = omega^j p_j(M)` for
`omega in mu_{2^s}`, so `p_j(M)=0` unless `2^s | j`. Hence the dual (frequency) variable stratifies by
`v_2(j)`: structured M at symmetry level s live only on frequencies with `v_2(j) >= s`, and the ODD
frequencies (`v_2=0`) vanish on EVERY structured M. So odd-frequency phases detect EXACTLY the primitive
(trivial-stabilizer) part = `extras`. Verified exactly (`s=1,2,3`: nonzero `p_j` only at `2^s | j`). This
rigorously justifies the primitive lemma and the even-j = structured / descent split.

**(3) Proof tool identified: Vinogradov mean value over the subgroup.** The moments of the primitive sum
are a Vinogradov system: `E_c |pi(c)|^{2k} = #{ a_i,b_i in mu_n : sum a_i^j = sum b_i^j, all odd j }`.
Numerically `E|pi|^2/n = 1.0` (diagonal), `E|pi|^4/n^2 ~ 2.9`, `E|pi|^6/n^3 ~ 14` -- above Gaussian
(2,6) but STABLE in r; the excess is exactly the `c=-a` (mu_2-symmetric) configs (`p_1=p_3=0` auto). So
`pi(c)` is `O(1)*Gaussian` uniformly in r, and the closing tool is **Vinogradov mean value / efficient
congruencing (Wooley / Bourgain-Demeter-Guth) for the ODD-power-sum system over the multiplicative
subgroup `mu_n subset F_p`, uniform in the degree**. This is far more concrete than "generic Bourgain-
Chang": a named, powerful machine, connection numerically validated.

**Net position:** the conjecture reduces to a Vinogradov-mean-value bound for odd-power-sums over `mu_n`,
uniform in degree, feeding the Li-Wan sieve -- with (2) PROVED, (1) robust across both deployed regimes,
and (3) the tool named and its moment structure validated. Remaining: the Vinogradov-over-subgroup
theorem itself (Wooley/BDG frontier) + rigorous Li-Wan assembly. Attemptable or cleanly posable.

## CORRECTION (2026-07-07, Vinogradov cite-vs-prove): the SUP form is FALSE

A rigorous literature assessment + my own verification REFUTE the sup form of the primitive lemma,
and expose that I conflated two INEQUIVALENT statements:
- **Sup form** `max_{c != 0} |pi(c)| <= C sqrt(n)`: **FALSE.** The odd monomials `{a^j : j odd}` span
  the odd functions on `mu_n` (dimension n/2). Taking the antisymmetric spike `f(a_0)=1, f(-a_0)=-1,
  else 0` gives an ODD-support `c != 0` with `pi(c) = (n-2)+2cos(2pi/p) ~ n` -- NO cancellation.
  **Verified** (n=16,p=17: `c=[15]*8`, `|pi|=15.87 ~ n`). My "primitive r-uniformity holds worst-case"
  was a SAMPLING ARTIFACT -- 300 random c miss this measure-zero structured spike. (2nd sampling
  miss in this attack; LESSON: sampling can NEVER certify a sup -- need a basis/algebraic argument.)
- **Moment / mean-value form** `E_c |pi|^{2s} = J_s(J;mu_n) ~ s! n^s`, uniform in r, for `s=O(1)/O(log)`:
  **TRUE and r-uniform** (this is what the `2.9, 14` moments actually show). It controls the
  AVERAGE/typical c (`|pi| ~ sqrt(n)` for all but few c), NOT the max.

**Why the moment method CANNOT reach the sup (rigorous, from the memo):** Markov gives
`#{c: |pi|>lambda} <= p^r J_s / lambda^{2s}`; to force `< 1` at `lambda = A sqrt(n)` needs `s >~ r/gamma`,
but `J_s` stays diagonal only BELOW the critical exponent `s_crit ~ r/gamma`; at `s=s_crit` the bound
degrades to the TRIVIAL `n`. So no diagonal-dominated moment reaches the sup for `r >~ log n`.

**Status of the reduction, corrected.** The clean "primitive sup bound => conjecture" path is BROKEN.
What survives: `f(0) - mean = q^-w sum_{c != 0} T(c)` is an AVERAGE over c, so the conjecture plausibly
needs the MOMENT form (typical control) PLUS a bound on the contribution of the few EXCEPTIONAL (spike)
c. The spikes are odd-support (primitive) and structured; whether their aggregate contribution is
`<= poly(n)*mean` is the NEW crux. So: (i) the moment form is a tractable "short research project" (not
a citation) via efficient congruencing over `mu_n` with the odd slice (Wooley's method is field-flexible;
control the mu_2-orbit excess uniformly in r up to s=O(log)); (ii) it must be COMBINED with an
exceptional-set / spike-count bound to close `f(0) <= poly*mean`. That combination is the honest open target.

**Nearest results (all NON-uniform in r):** VMVT main conj (BDG 2016 / Wooley) -- interval, fixed degree,
constant degrades in k; BGK/Bourgain-Chang/Shkredov subgroup sums -- power-saving `|H|^{1-delta}` not
`sqrt`, `delta(gamma)->0` as `gamma->0`; Cochrane-Pinner/Bourgain fewnomial -- saving degrades in #terms;
finite-field decoupling (2508.08377) -- fixed low dim / large q, mean value not sup. NONE is r-uniform.

## ChatGPT external review (2026-07-07): reframing + moment theorem PROVED; ALL claims verified here

Fed the full metaprompt to ChatGPT; it produced real mathematics, corrected two of our errors, and
proved new results. I re-verified every load-bearing claim numerically (reviewer!=generator):

**Our errors it corrected:**
- "Odd frequencies detect exactly N_prim" is FALSE. One-way (S=-S => odd p_j=0) holds, but the
  TRUNCATED odd block (only odd j<w, w<<n) does not characterize (-1)-invariance. Counterexample
  (VERIFIED): F_17, mu_16, S={1,3,13}: p_1(S)=0 but S != -S. So `b2_primitive_runiform` measured the
  wrong object. The EXACT descent `N_prim = N(n,m,w) - 1[2|m] N(n/2,m/2,floor(w/2))` still stands.
- Our earlier "sup form is FALSE" spike used the FULL odd block (deg up to n); in the deployed
  truncated block (deg P_c < w << n) an antisymmetric delta spike CANNOT be realized (a deg-<w poly
  vanishing on n-2>w points is 0). So the sup disproof was in the wrong regime -- but it is moot,
  since the averaged object is T(c)=e_m(...), not pi(c) (see below).

**PROVED (Thm 1, verified: moments 1,2.96,15.17,101.87 vs (2s-1)!!=1,3,15,105).** For J containing the
initial odd block {1,3,...,2s-1} and char>2s: `J_s(J;mu_n) <= (2s-1)!! n^s`, UNIFORM in |J|. Clean
Newton-pairing proof: substitute x_{s+i}=-b_i (uses -1 in mu_n), odd power sums of the 2s x's vanish
=> e_k=0 for odd k (Newton) => prod(T-x_i) is EVEN => roots pair {h,-h} => (2s-1)!! pairings * n^s.
Explains the 2.9/14 numerics as the mu_2-pairing (real-Gaussian) moments. NO efficient congruencing
needed -- much cleaner than our "short research project" framing. (False for arbitrary sparse J: J={1}
gives additive energy n^{4-1/gamma}; the initial-odd-block hypothesis is essential.)

**PROVED (Thm 2, exact cycle expansion; Thm 3, low-cycle vanishing -- VERIFIED: N=3=brute, M_lambda=0
for l<=w).** Li-Wan cycle index: `N = sum_{lambda|-m} ((-1)^{m-l(lambda)}/z_lambda) M_lambda`, where
`M_lambda = #{x in mu_n^{l} : sum_i lambda_i x_i^j = 0, j=1..w} = q^{-w} sum_c prod_r pi(rc)^{m_r}`.
**Thm 3:** if `l(lambda) <= w` then `M_lambda = 0` (Vandermonde in the distinct values forces all
aggregate weights D_nu=0, impossible since 0 < D_nu <= m < char). So `N = sum_{l(lambda) > w} (...)`:
ONLY partitions with MORE THAN w cycles contribute (deployed: > 67000 cycles). This is the precise
reframing and the exact obstruction to a moment route: T(c)'s average sees only high-cycle configs,
and depends on the JOINT process {pi(c),pi(2c),...,pi(mc)}, not the marginals Thm 1 controls.

**Sufficiency verdict (ChatGPT, concur): moment + exceptional does NOT close it.** N_prim is not the
odd-freq average (our error), and T(c) needs the mixed averages E_c prod pi(rc)^{m_r}, not marginals.
Exceptional-set count needed is ABSOLUTE (<= n^3/mean ~ 2^27) but moment bounds give a FRACTION.

**Rule-outs re-confirmed:** Sawin-Shusterman dead (slope w); Katz dead (abelian c-family for T(c),
robust to post-descent largeness); completed-sum gives only w*sqrt(q), trivial. VMVT/decoupling don't
apply (interval + fixed degree).

**NET / OPEN:** the conjecture `N_prim <= n^3` is OPEN, now EXACTLY reframed: prove a HIGH-CYCLE
(l(lambda)>w) WEIGHTED DIAGONAL equidistribution estimate `M_lambda = q^{-w} n^{l(lambda)} + cycle-index-
summable error` over `mu_n` (or the primitive signed-difference version). This is the crux -- not a
sqrt(n) bound for pi(c), not O(log n) moments. Cross-check pending vs Claude's independent take.

This is a precise, well-posed open problem in additive combinatorics (r-uniform subgroup exp-sums),
in a favorable large-subgroup/prime-field regime, base case known, strong evidence true. Realistic
routes to the proof: (i) attempt the `r`-uniform extension exploiting the specific cyclic structure
of `mu_n` (the count is over roots of unity `= Z/n`, not a generic subgroup — the Fourier-gap / cyclic-
code structure may give the uniformity generic subgroups lack); (ii) targeted search for post-2020
`r`-uniform subgroup-sum results; (iii) pose the exact lemma to the Bourgain-Chang school (Chang,
Konyagin, Shkredov) or the geometric side (Sawin). Coordinated with holmbuar's `conj:Q` ledger.
Deliverables banked: 4 validated scripts + 4 notes + this synthesis.

## Convergence: 2nd external model (Claude subagent) + TheoremSearch (2026-07-07)

**Claude attack CONVERGES with ChatGPT and adds results (all re-verified here):**
- **Thm B (VERIFIED, power-of-2 n): `n | N_prim`**, N_prim = n*(#free mu_n-orbits) (free orbit = trivial
  stabilizer, size n). So **Conjecture <=> #free orbits <= n^2** (verified 16,32,64; n=12 out of scope).
- **Thm D (sharpest takeaway): the bound is a CONCENTRATION statement, p-SENSITIVE, not rigidity.** For small
  p at the same (n,m,w), N_prim >> n^3 (up to 7e15 at n=64); N_prim/mean has median exactly 1. So N_prim<=n^3
  holds ONLY because deployed mean = C(n,m)/p^w ~ 2^35.7 <= n^3. Any proof must use that p is large (mean
  small); a p-blind structural/coding bound is IMPOSSIBLE.
- **Reduction E (positive route): additive energy.** E = sum_v nu(v)^2 = sum_d C(n-2d,m-d) E_d, E_d =
  #{disjoint A,B in mu_n, |A|=|B|=d, p_j(A)=p_j(B) for j<=w} = a Prouhet-Tarry-Escott/Vandermonde system over
  mu_n; E/E_0 ~ 1 (near-random), POSITIVE (defeats the signed-cancellation no-go). Crux splits: (E-a) excess
  energy E - E_0 <= n^{O(1)} p^w; (E-b) the v=0 fiber transfer (variance controls a TYPICAL fiber, but
  nu(0)=N hoards rotation orbits -- the sup-vs-average issue again). **Small-d rigid range E_d=0 for d<=d_0(w)
  is PROVABLE NOW** (same Vandermonde as low-cycle vanishing) -- a concrete first theorem.
- Calibration (both models): ~2^41 slack (|N_prim-mean|~sqrt(mean)~2^18 << n^3=2^63); morally certain.

**TheoremSearch citation leads (theoremsearch.com; 11.7M arXiv + Mathlib):**
- arXiv:1210.0456 Cheong-Matchett Wood-Zaman "Distribution of points on superelliptic curves", Lemma 3.3:
  count of polynomials with prescribed leading coefficients over F_q, MAIN TERM + O(q^{(d-sum s_i)/n+1}) error.
  Closest published analogue; chase whether its method gives the mu_n-restricted equidistribution input (E-a).
- arXiv:0807.4671 Dae San Kim -- code weight distribution as subset-sum with field-weighted constraint
  (sum nu_beta*beta=0) + Kloosterman power moments (the coding form).
- arXiv:1803.03351 Koh-Pham-Shen-Vinh -- subgroup product/energy expansion bounds (for E_d).

**NET (both models + search agree):** conjecture is a p-sensitive CONCENTRATION, morally certain; the single
open crux is a rigorous high-degree additive-energy / joint-equidistribution estimate over mu_n (E-a) plus
the v=0 fiber transfer (E-b). New provable pieces: n|N_prim, small-d PTE rigidity. Sharpest convergent state.

## Move (2): Cheong-Matchett Wood-Zaman does NOT transfer; PTE rigidity PROVED (2026-07-07)

Chased the top TheoremSearch lead (arXiv:1210.0456, Lemma 3.3, count of polynomials with prescribed
values). **Verdict: does NOT transfer.** Method = Mobius inversion + Euler product (not even Weil), with
the NUMBER OF CONDITIONS FIXED (l=q) and d->infinity; "cannot handle l growing with d." Our regime has
w~0.03n conditions GROWING with n -- the same fixed-vs-growing-conditions wall that kills VMVT (fixed
degree) and Bourgain-Chang (bounded #monomials). Third confirmation (now via a concrete paper) that the
growing-#conditions equidistribution is genuinely NEW, not in the literature.

**PROVED + VERIFIED (PTE rigidity): E_d = 0 for 1 <= d <= w.** If disjoint A,B subset mu_n have |A|=|B|=d<=w
and p_j(A)=p_j(B) for j=1..w, then p_1..p_d agree, so by Newton (char>d) the size-d monic polynomials
prod(X-a), prod(X-b) coincide => A=B => (disjoint) empty => d=0. Verified: n=12,w=2 -> E_1=E_2=0, E_3=168;
n=16,w=3 -> E_1=E_2=E_3=0, E_4=252. So the additive energy `E = C(n,m) + sum_{d>w} C(n-2d,m-d) E_d`: the
small-d terms vanish, and the **d>w TAIL dominates (~E_0 = C(n,m)^2/p^w) -- the tail IS crux (E-a).**

**Consolidated in-hand PROVED theorems** (the durable partial contribution): (1) Li-Wan cycle expansion +
low-cycle vanishing (only >w-cycle partitions contribute); (2) exact descent N_prim = N - 1[2|m]N(n/2,..);
(3) n | N_prim (=> conj iff #free orbits <= n^2), power-of-2 n; (4) moment law E_c|pi|^{2s} <= (2s-1)!! n^s
uniform in #freqs; (5) PTE rigidity E_d=0 for d<=w; (6) reformulations (divisor coeff-gap / BCH Boolean
codeword / F_p-quadrature); (7) it is a p-sensitive CONCENTRATION not rigidity (Thm D). OPEN crux: the
d>w additive-energy tail equidistribution over mu_n (E-a) + v=0 fiber transfer (E-b). Morally certain
(~2^41 slack), genuinely new equidistribution input, confirmed by 2 models + a theorem-search paper chase.
