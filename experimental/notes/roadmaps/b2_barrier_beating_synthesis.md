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

## c1-averaging cross-check (2026-07-10): marginal L2 tool + the Stepanov IMPORT BARRIER

Re-attacked the per-t/marginal side with a linear-coefficient average, then CROSS-CHECKED against
this note's converged verdict (crux is JOINT, not marginal). Net: a clean verified marginal tool that
does NOT advance the crux (reconciled below so future-me does not re-tread), plus ONE durable increment
— a method-internal reason the graph-energy literature cannot be imported for the E-a energy tail.

**The c1-averaging identity (exact).** Split the phase `c = c1*(linear) + g` (g = higher freqs). Then
`sum_{c1 in F_p} |S(H; c1*a+g)|^4 = p * T1(g)`, where
`T1(g) = sum_{h1+h2=h3+h4, hi in mu_n} e_p(g(h1)+g(h2)-g(h3)-g(h4)) = sum_s |F(s)|^2`,
`F(s)=sum_{h1+h2=s} e_p(g(h1)+g(h2))` = the additive energy of the GRAPH `Gamma_g={(h,g(h))}`.
Orthogonality in c1 collapses the 4th moment onto additive-energy quadruples; hence
`max_{c1}|S| <= (p*T1(g))^{1/4}`.

**RECONCILIATION with Thm 1 (no new content vs the marginal moment).** Averaging over g too,
`E_c |pi(c)|^4 = E_g[T1(g)]`. Thm 1 (s=2) gives `E_c|pi|^4 <= 3n^2`; the 07-10 numerics give
`T1(g) ~ 3n^2` PER primitive g (truncated block). So T1(g) is the per-g SLICE of the s=2 marginal
moment — bounded pointwise in the truncated regime, consistent, but MARGINAL. Per this note's converged
sufficiency verdict (ChatGPT+Claude+theorem-chase, lines above): the marginal 4th-moment / sup does NOT
close the conjecture — N depends on the JOINT high-cycle averages `M_lambda = q^{-w} sum_c prod_r pi(rc)^{m_r}`
(Thm 2/3), not marginals. So the c1-average is a TOOL, not an advance on the crux. (Route checked; marginal.)

**Adversarial validity in the truncated regime (07-10 scripts).** `b2_c1avg_adversarial.py`:
coordinate-ascent over coefficients (fixed generic exponents, deg << w) + resonant-g probe, p in
{12289,40961}. `T1(g)/2n^2` stays 1.5-1.6 for primitive g, r to 256; the ONLY blow-up is g factoring
through a sub-sqrt(p) subgroup (`d>=n/4`, quotient < sqrt p), which (i) is descent/first-match-removed
and (ii) has SMALL max|S| (1.4-2.3 sqrt n) — NOT a counterexample to the sup, just where the 4th-moment
PROXY overcounts. The refuted antisymmetric spike (sup-form disproof above) needs deg~n and is
UNREALIZABLE in the truncated block (deg-<w poly vanishing on n-2>w pts is 0) — consistent with the
ChatGPT "wrong-regime, moot" correction. Sharpened primitive condition: NOT "coprime exponents" but
"does not concentrate on a sub-sqrt(p) subgroup" (the BGK/sqrt-p line) — g CAN factor through a size-256
quotient and still collapse.

**DURABLE INCREMENT — the Stepanov import barrier (kills the graph-energy hope for E-a).** The natural
tool to bound the E-a additive-energy tail (E_d, and T1) is the subgroup graph-energy theorem
`E(f(G),g(G)) <= 16 m n^2 (m+n) |G|^{8/3}` (Vyugin-Makarychev, arXiv:1504.01354 Cor 2; `b2_graphenergy_litmap.py`).
PRIMARY-SOURCE READ: method is **STEPANOV's** (auxiliary polynomial + Bezout, eq. 11), and the degree
restriction `100(mn)^{3/2} < |G|` is STRUCTURAL — Stepanov bounds root count by `N <= deg(Psi)/D`, so the
auxiliary polynomial's degree must stay BELOW |G| (the root set) or the bound is trivial. Since our
conditions run to j=w and (mod n) exponents reach ~n >> |G|^{1/3}=n^{1/3}, we are irreducibly OUTSIDE the
window; the barrier is a METHOD-LIMIT, not a loose lemma. So the graph-energy literature CANNOT be imported
for E-a — the specific method-internal reason behind this note's repeated "growing-#conditions
equidistribution is genuinely NEW." (arXiv:2211.07739 Weil-sums-over-small-subgroups falls back on
Bourgain's `eta_n -> 0` term-by-term induction for exactly this reason.) TheoremSearch confirms no
r/degree-uniform graph-energy bound exists past `|G|^{1/3}`.

**Scripts banked (07-10, verified p in {12289,40961}):** `experimental/scripts/b2_c1avg_adversarial.py`,
`experimental/scripts/b2_graphenergy_litmap.py`. Net position UNCHANGED: crux = the JOINT high-cycle
weighted-diagonal equidistribution (E-a) + v=0 fiber transfer (E-b); marginal/sup tools (incl. c1-average)
are insufficient; Stepanov/graph-energy import is barred by a degree cap our regime exceeds.

## E-a first-tail scout (2026-07-10): tail terms are p-INDEPENDENT char-0 PTE counts over Z/n

Went at the ACTUAL crux (E-a additive-energy tail) instead of the marginal c1 route. Scripts:
`experimental/scripts/b2_Ea_firsttail.py`, `experimental/scripts/b2_Ea_pindep.py`. Object:
`E_d = #{disjoint A,B subset mu_n, |A|=|B|=d, p_j(A)=p_j(B) for j<=w}` (per-d additive-energy tail;
`E = C(n,m) + sum_{d>w} C(n-2d,m-d) E_d`; PTE rigidity already proved: E_d=0 for d<=w).

**FINDING (verified n=16, w in {2,3}, primes p=1 mod 16 up to 577).** For p above a TINY threshold,
`E_{w+1}(p)` is EXACTLY p-INDEPENDENT:
- w=3: E_4(p) = 12 for ALL p in {97,113,...,577}; only p=17 (near-full-group) inflates to 252.
- w=2: E_3(p) = 0 for all p>=113; p=17->704, p=97->32 (collision excess draining out).
Mechanism (clean, verified): at large p, `p_j(A)=p_j(B) mod p` (via the fixed zeta->z) forces equality
in char 0 in Z[zeta_n] (a nonzero difference has bounded norm => divisible by only finitely many primes),
so `E_d = ` a characteristic-0 PROUHET-TARRY-ESCOTT count over the roots of unity `mu_n ~ Z/n`; the mod-p
collision excess vanishes for p above a small threshold. **Decomposition: E_d(p) = PTE_d(Z/n) [p-independent]
+ collision_excess_d(p).**

**Why it matters + the caveat.** (+) For the terms where the char-0 baseline dominates, this converts the
E-a tail from an ANALYTIC subgroup-equidistribution problem (BARRED by the Stepanov degree cap above) into
a COMBINATORIAL PTE / vanishing-sums-of-roots-of-unity count over Z/n -- a different, possibly more
tractable theory (Conway-Jones, Mann, cyclotomic vanishing) that the Stepanov cap does not touch. It also
REFINES Thm D: the p-sensitivity is confined to the collision excess (+ the m-weighted assembly + the
energy->max-fiber transfer E-b), NOT the individual small-d tail terms. (-) CAVEAT (load-bearing):
verified only for the FIRST tail term at SMALL n (d=4). At deployment d=w+1 ~ 67471 is LARGE; the char-0
threshold plausibly GROWS with d (power sums of ~d roots of unity have larger coordinates => more primes
can divide a nonzero difference), so p-independence at deployed (n,w,p) is NOT established for large d.
The sparsity (E_5=E_6=0 for w=3) is w/n-dependent (w=2, smaller w/n closer to deployed 0.032, has a
FULLER tail) and must NOT be extrapolated. Promising LEAD, not a proof ingredient.

**Next concrete step:** push n=32,64 and track where E_d(p) stabilizes vs d -- does the char-0 threshold
grow with d? That tests the large-d caveat and tells us whether the PTE-over-Z/n reduction reaches the
deployed tail band or only its small-d edge. If the threshold stays below deployed p even for large d,
E-a becomes a cyclotomic-combinatorics problem, sidestepping the analytic barrier entirely.

**UPDATE (threshold-vs-d, `b2_Ea_threshvsd.py`): CAVEAT CONFIRMED -- the char-0 threshold GROWS with d.**
n=24,w=3: E_d stabilizes to its char-0 baseline at p>=193 (d=4), >=241 (d=5), but d=6,7 are STILL bouncing
at p=409 (the largest prime tested -- likely NOT stabilized, e.g. d=7: [864,288,288,480,48]). n=32,w=3:
p>=353 (d=4), >=641 (d=5, baseline 0 reached only at the last prime). So the threshold RISES with d
(power sums of ~d roots of unity => larger nonzero-difference norms => divisible by more primes). At
deployment d=w+1 ~ 67471, the threshold is plausibly ASTRONOMICAL, far above deployed p~2^31.
**Consequence: the pure char-0 PTE reduction does NOT reach the deployed large-d tail bulk; it controls
only the small-d EDGE (d just above w). The p-sensitivity (Thm D) reasserts in the bulk.** Lead #3
DOWNGRADED: "sidesteps the barrier" -> "controls the small-d edge; the large-d bulk stays p-sensitive/
analytic." (verify-first killed the strong form; the reduction survives only at the edge.)

**RESOLVED (decisive computation, `b2_energy_domination.py`): the energy tail is BULK-DOMINATED; the edge
is exponentially subdominant.** Log-space (lgamma) profile of the tail term `W_d * E_d`, W_d=C(n-2d,m-d),
E_d~C(n,d)C(n-d,d)/p^w (random model, valid at deployed large p), at deployed n=2^21, w=67471, p~2^31:
the argmax sits at `d* ~ 0.09-0.25 * n` (d*/w = 2.8 at rho=0.1, 6.5 at 0.3, 7.8 at 0.48) -- FAR above the
edge d=w+1. The edge term is **374,000 to 1,372,000 BITS smaller** than the dominant bulk term. So the
small-d edge (the ONLY place the char-0 PTE / vanishing-sums machinery applies) is ~2^{-10^6} below where
the energy lives, and **contributes NOTHING to bounding E-a.** LEAD #3 CLOSED: the vanishing-sums route
does not reach the deployed energy. The crux is entirely the large-d (d~0.1-0.25n) p-sensitive JOINT
high-cycle equidistribution over mu_n -- reconfirmed from a third direction (marginal c1 / Stepanov-barred
graph-energy / edge-subdominant PTE all point back to the same large-d bulk). Negative preserved
(Hard rule #4); do NOT re-open the small-d/char-0/vanishing-sums angle for the energy bound.

## Dilate-correlation probe (2026-07-10): bulk dilates DECORRELATE; moment is RESONANCE-dominated => E-b

Ran the on-crux experiment: does the joint object `M_lambda = q^{-w} sum_c prod_r pi(rc)^{m_r}` FACTOR
(dilates {pi(rc)} independent => product-structure proof route) or COUPLE? Scripts:
`b2_dilate_correlation.py`, `b2_dilate_Kgrowth2.py` (pi-table over F_p^w, w in {2,3}, n=16, p<=401,
dilates K to 40). Object: coupling `C^{(K)} = E_c[prod_{r=1}^K |pi(rc)|^2]/n^K` (=1 iff independent).

- **PAIRWISE:** C[1,k]=1.000 exactly (all p,k). pi(c),pi(kc) pairwise UNCORRELATED.
- **TYPICAL (median over c!=0):** C^{(K)}_med DECAYS to ~0 fast. For typical c the dilate product is
  << n^K: the BULK dilates DECORRELATE STRONGLY (near-independence, better than the small-K mean suggested).
- **full mean:** ~ e^{K log n} = n^K (EXP) -- but this is the c=0 MAIN TERM (pi(0)=n), which the conjecture
  SUBTRACTS (N_prim - mean = q^{-w} sum_{c!=0} T(c)). NOT the obstruction. (First Kgrowth included c=0 and
  was uninformative; corrected -- reviewer!=generator catch on my own probe.)
- **c!=0 mean:** erratic/unstable across p (0.0099 to 124 at K=40) = dominated by a few RESONANT c!=0 spikes
  (heavy tail); this is Thm D p-sensitivity surfacing in the joint object.

**VERDICT: the product route does NOT open, for an INSTRUCTIVE reason.** M_lambda is NOT bulk-controlled --
it is dominated by c=0 (main term, subtracted) + RESONANT c!=0 (heavy tail). The bulk dilates decorrelate;
the ENTIRE difficulty is the resonant/structured-c contribution = exactly the E-b obstruction (v=0 fiber
transfer / nu(0)=N hoarding) the note already named. So the joint-object attack REDUCES TO E-b with NO new
leverage, and RULES OUT "generic bulk coupling" as the obstruction (a real narrowing: the wall is
specifically the resonances, which the primitive descent must peel). 4th independent confirmation the crux
is E-b/resonant-transfer.

## Session 2026-07-10 net: crux = E-b (resonant/structured-c transfer); 4 approach-classes ruled out

The wall is `sum_{c!=0, resonant} prod_r pi(rc)^{m_r}` -- the resonant/structured-c (v=0 fiber) transfer,
after subtracting the c=0 main term. RULED OUT this session (all banked above): (1) marginal c1-average
(= per-g slice of Thm 1; insufficient, needs joint not marginal); (2) graph-energy import
(Vyugin-Makarychev/Stepanov, deg<=|G|^{1/3} cap, our w>>n^{1/3}); (3) PTE/vanishing-sums-over-Z/n
(controls only the char-0 small-d EDGE, which is ~2^{-10^6} energy-subdominant); (4) joint-object bulk
coupling (dilates decorrelate typically; moment is resonance-dominated). NEXT on-crux target: test whether
the primitive descent (N_prim = N - 1[2|m] N(n/2, m/2, floor(w/2))) actually BOUNDS the resonant-c
contribution -- i.e. recompute the c!=0 moment RESTRICTED to primitive (descent-peeled) c and check if THAT
is bounded/polynomial. That is the one unexamined component of the E-b machine, and directly on the crux.

## Primitive-resonance probe (2026-07-10): coupling is MIXED-c & p-sensitive; primitive slice is CLEAN

Ran the above. Script `b2_primitive_resonance.py` (w=3, n=16, p in {97,193}): split c!=0 into PRIMITIVE
(odd-freq support, c_2=0), STRUCTURED (even-freq only, c_1=c_3=0), and full; K-growth of the coupling
`C^{(K)} = E_{c-class}[prod_{r=1}^K|pi(rc)|^2]/n^K` to K=40.

**Analysis-error CORRECTED (reviewer!=generator on my own probe):** raw moment grows ~n^K even for
INDEPENDENT dilates (n^K is exponential in K), so the right object is C^{(K)}=moment/n^K, NOT log(moment)
vs K. Renormalized:
- **PRIMITIVE slice: C^{(K)} DECAYS below 1** (5.7e-9 at p=97, 1.6e-3 at p=193, K=40). The odd-frequency
  dilates are SUB-INDEPENDENT -- NO coupling/resonance on the primitive slice. (positive: if the descent
  isolates the primitive part, E-b is controlled there.)
- **STRUCTURED slice: also decays** (2.69 -> 6.3e-3). Bounded.
- **FULL c!=0: p-SENSITIVE and erratic** -- C^{(40)}=0.055 at p=97 but 80 at p=193 -- driven by the
  MIXED-frequency c (both odd and even support), since both pure slices decay. This is Thm-D p-sensitivity,
  now LOCALIZED to mixed-frequency c.

**VERDICT: refines E-b, does NOT close it.** The resonance/coupling obstruction lives in the MIXED-frequency
c and is p-sensitive; the pure primitive slice is clean (sub-independent). CAVEAT (load-bearing): "primitive
= c_2=0" is a PROXY for the descent-peeled part, NOT the actual set-descent; prior review flagged the
set<->frequency map is subtle (truncated odd block != (-1)-invariance), so this does not certify the descent.
Small-n (n=16) -- extrapolation to deployment is NOT justified (regime-representativeness). Net: E-b stands;
sharpened to "does the descent remove the mixed-frequency p-sensitive coupling?" -- a THEORETICAL question
now (the set-descent<->frequency map), beyond what small-n toy probes can resolve. STOP toy-probing here.

**Machinery found (vanishing-sums-of-roots-of-unity theory, for the edge; `b2_find_pte_fp.py`).** The E-a
small-d edge IS a simultaneous vanishing-sum-of-roots-of-unity system, controlled by classical structure
theory: Conway-Jones 1976 (arXiv:0911.2594 Thm 2.3), Lam-Leung (via 2508.16732 Lem 1), Dvornicich-Zannier
(vanishing-sum structure). Directly-relevant COUNTING results to chase: **arXiv:2108.10191** (Super Catalan
/ Fourier summation over a cyclic subgroup of F_q, Prop 4 -- power sums over mu_n exactly);
**arXiv:1702.02327** (counting n-subsets of F_q with PRESCRIBED POWER SUMS, Thm 4.1 -- the E_d-type count
directly); arXiv:1602.06715 Thm 2 (Kos-Lovasz: exact N_k(G) for cyclic G). The observed sparsity (E_5=E_6=0
for w=3) is EXPLAINED: minimal vanishing sums have constrained weights (2104.15057 Thm 8: minimal n-th-root
vanishing sums are full prime-p sums or have >=(p-1)(q-1)+(r-1)>=6 terms).

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
