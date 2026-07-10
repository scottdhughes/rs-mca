# L1 / b2 prize crux: consolidated reduction, ruled-out routes, and the E-b sub-lemma (2026-07-10)

**Status.** Milestone consolidation, POST ChatGPT-5.6 external review (2026-07-10, all claims re-verified
numerically -- `experimental/scripts/b2_chatgpt56_review_verify.py`; prompt in `experimental/notes/audits/
chatgpt56_Eb_prompt.txt`). The L1/b2 (conj:Q / imgfib) prize crux reduces by an EXACT chain to a
p-sensitive concentration (E-b). **Review outcome: 3 corrections (the raw pi^m formula = tuple count not
subset count; not all nonzero fibers have orbit n; the descent-carrier lead REFUTED by an exact n=64,p=449
instance) + the global L^2 is provably too coarse + a NEW sharper target: the secant-shadow local variance
`Delta_sec = O(n^2 mu)` (Sec 7).** Corrections applied inline below. NOT a proof.
Companion (full working log): `b2_barrier_beating_synthesis.md`. Verification scripts: `experimental/scripts/b2_*.py`.

## 1. The object

`K = F_p` (KoalaBear; `mu_n subset F_p` since `v2(p-1) >= 21 = a`, `n = 2^a`, `|mu_n| = n = p^{0.678}` --
a LARGE subgroup in a small field). The prize crux reduces (holmbuar conj:Q ledger + this repo) to the
fiber count
```
N(n,m,w) = #{ S subset mu_n : |S| = m,  p_j(S) := sum_{s in S} s^j = 0 for all j = 1..w }.
```
Deployed row: `n = 2^21`, `w = 67471` (`w/n ~ 0.032`), `m ~ rho n`, `p ~ 2^31`. Conjecture: `N <= n^3`
(equivalently the primitive count `N_prim <= n^3`), which certifies the target prize bound.

## 2. The exact reduction chain (all steps PROVED; see synthesis note for proofs)

1. **Li-Wan sieve / cycle expansion.** With `pi(c) = sum_{a in mu_n} e_p(c . phi(a))`, `phi(a)=(a^j)_{j=1..w}`,
   `c in F_p^w`. **CORRECTION (ChatGPT-5.6 review, VERIFIED):** `q^{-w} sum_c pi(c)^m` is NOT N -- it counts
   ORDERED m-tuples WITH REPETITION (verified p=5,n=4,m=2,w=1: N_subset=2 but the formula = 4 = # ordered
   pairs). The correct subset object is the elementary-symmetric coefficient
   `nu-hat(c) = [t^m] prod_{a in mu_n} (1 + t e_p(f_c(a)))`, `N = q^{-w} sum_c nu-hat(c)`; equivalently the
   cycle/Newton expansion `N = sum_{lambda |- m} ((-1)^{m-l(lambda)}/z_lambda) M_lambda`,
   `M_lambda = q^{-w} sum_c prod_r pi(rc)^{m_r}` (THIS is correct, and is what the repo machinery uses).
2. **Low-cycle vanishing (Thm 3).** `M_lambda = 0` whenever `l(lambda) <= w` (Vandermonde in the distinct
   values). So `N = sum_{l(lambda) > w} (...)`: only partitions with MORE THAN w cycles contribute.
3. **Descent (RIGOROUS, re-derived 07-10).** For `n = 2^a`, a mu_2-symmetric fiber element `S = -S` is a
   union of `{a,-a}` pairs; with `u = t^2` (the 2:1 square map `mu_n -> mu_{n/2}`), `p_{2i}(S) = 2 p_i(U)`
   and all odd power sums vanish, so symmetric fibers biject with `{U subset mu_{n/2}: |U|=m/2, p_i(U)=0,
   i<=floor(w/2)}`. Hence the EXACT descent
   `N_prim = N - 1[2|m] N(n/2, m/2, floor(w/2))`, and `N_prim` = the primitive (free-mu_2-orbit) count.
   (Numerically confirmed: n=16,m=8,w=3,p=97 -> N=6, all 6 mu_2-symmetric, N_prim=0.)
4. **Rotation structure (Thm B).** `p_j(zeta S) = zeta^j p_j(S)`. `N_prim = n * (# free mu_n-orbits)`,
   `n | N_prim` -- CORRECT (statement about zero solutions with trivial stabilizer). **CORRECTION
   (ChatGPT-5.6, VERIFIED):** it is FALSE that every `v != 0` has a size-n orbit -- `Stab(v) = mu_{gcd(n,
   {j: v_j != 0})}`, so e.g. `v=(0,1,0,..)` (only even-index support) is fixed by mu_2, orbit n/2. Correct
   dyadic stratification: `W_k = {v: v_j=0 unless 2^k | j}`; `v in W_k \ W_{k+1}` has stabilizer 2^k, orbit
   n/2^k. Energy: `E = N^2 + sum_{k>=0} (n/2^k) sum_{orbits in W_k\W_{k+1}} nu^2`. **The short-orbit
   (even-frequency) strata are exactly where the dyadic resonances live** -- consistent with this session's
   "coupling lives in mixed/even-frequency c" finding.
5. **p-sensitivity (Thm D).** `N <= n^3` holds ONLY because the deployed mean `= C(n,m)/p^w ~ 2^{35.7} <= n^3`;
   for small p at the same (n,m,w), `N >> n^3`. Any proof MUST use p large (mean small): a p-blind /
   purely structural bound is IMPOSSIBLE.

## 3. The crux, sharpened to one inequality (E-b)

Combining 4 + 5: the conjecture `N_prim <= n^3` is the statement that the ROTATION-FIXED fiber `nu(0) = N`
is NOT atypically large relative to the typical fiber, i.e.
```
   E-b:   nu(0)  <=  poly(n) * mean,     mean = C(n,m)/p^w.
```
The additive energy `E` controls the AVERAGE `nu(v)^2` (E is near its random value `~ C(n,m)^2/p^w`; the
tail `E - E_0 = sum_{d>w} C(n-2d,m-d) E_d` is the "E-a" piece, dominated by the large-d bulk -- see rule-out
3). The difficulty is the TRANSFER from the average to the specific rotation-fixed `nu(0)`. Empirically
`nu(0)/mean` has median exactly 1 (Thm D) -- nu(0) IS typical -- so E-b is believed true (~2^41 slack);
the open problem is PROVING the transfer.

## 4. Four approach-classes RULED OUT (2026-07-10 session)

1. **Marginal / sup exponential-sum bounds** (incl. the c1-average). `max_c |pi(c)|` and the c1-averaged
   4th moment are MARGINAL; the c1-average is exactly the per-g slice of the proved moment law Thm 1.
   N depends on the JOINT high-cycle averages `M_lambda`, not marginals. INSUFFICIENT.
2. **Graph-energy import** (Vyugin-Makarychev, arXiv:1504.01354, `E(f(G),g(G)) <= 16 m n^2(m+n)|G|^{8/3}`).
   Primary source: STEPANOV's method; the `deg <= |G|^{1/3}` cap is structural (auxiliary-poly degree must
   stay below the root set |G|). Our conditions run to `j = w >> n^{1/3}`: irreducibly outside the window.
   BARRED (this is why 2211.07739 falls back on Bourgain's eta_n->0 induction).
3. **PTE / vanishing-sums-of-roots-of-unity over Z/n.** The tail terms `E_d` are, above a tiny prime
   threshold, p-INDEPENDENT char-0 PTE counts over the roots of unity (verified: E_4=12 flat over all
   p in [97,577]), controlled by Conway-Jones/Lam-Leung/Dvornicich-Zannier -- BUT the threshold GROWS with
   d, and the energy tail is BULK-dominated: the small-d edge (where the char-0/vanishing-sums machinery
   applies) is `~2^{-10^6}` below the dominant bulk term at deployment. ENERGY-SUBDOMINANT.
4. **Joint-object bulk coupling.** The dilated sums `{pi(rc)}` are pairwise-exactly and typically-strongly
   INDEPENDENT (median coupling decays); `M_lambda`'s difficulty is entirely the c=0 main term (subtracted)
   + the resonant/structured-c heavy tail = E-b itself. No generic bulk-coupling obstruction exists.

## 5. The one open lead (this session): primitive slice is CLEAN

Restricting the joint moment `C^{(K)} = E_c[prod_r |pi(rc)|^2]/n^K` to PRIMITIVE (odd-frequency, c_2=0) c:
`C^{(K)}` DECAYS below 1 (sub-independent) -- NO coupling on the odd-frequency slice. The p-sensitive
coupling lives in MIXED-frequency c. So E-b sharpened to "is nu(0)'s excess carried by mu_2-symmetric (descent-removed) configurations?"

**REFUTED (ChatGPT-5.6 review, VERIFIED).** The descent-carrier hypothesis is FALSE. Exact instance
n=64, p=449, w=2, m=7 (gamma=0.681, w/n=0.03125 -- both matching deployed): `N = 3584 = 64*56 > mu = 3081.4`,
and since `m=7` is ODD no `S=-S` exists, so ALL 3584 solutions are PRIMITIVE -- yet the global energy is
near-random (`E/(M^2/Q) - 1 = 3.16e-4`). So primitive positive excess coexists with near-random energy and
is NOT descent-removed. The Sec-5 lead is dead: the excess is a genuine primitive phenomenon, not a
descent artifact. (E-b still holds here -- `3584 < n^3 = 262144` -- it just is not proved by the descent line.)

## 6. Proved partial results (durable contribution)

Li-Wan cycle expansion + low-cycle vanishing (2); exact descent (3); `n | N_prim`, `N_prim = n * #free
orbits` (4); moment law `E_c|pi|^{2s} <= (2s-1)!! n^s` uniform in |J| (Thm 1); PTE rigidity `E_d = 0` for
`d <= w`; rotation-orbit energy decomposition (4); reformulations (BCH Boolean codeword / F_p-quadrature);
p-sensitivity Thm D. Plus the 4 rule-outs (Sec 4) and the primitive-slice lead (Sec 5).

## 7. Open sub-lemma (the target) -- REFRAMED by the ChatGPT-5.6 review (VERIFIED)

**Why global L^2 cannot work (exact obstruction).** With `Delta_2 = E - M^2/Q = sum_v (nu(v)-mu)^2`,
Cauchy-Schwarz on the Q-1 off-zero deviations gives the EXACT `Delta_2 >= (Q/(Q-1)) (N-mu)^2`, so
`N <= mu + sqrt((Q-1)/Q * Delta_2)` is the BEST global bound -- and an abstract countermodel (raise nu(0)
by L=n^3, lower L points on full orbits) shows global L^2 + rotation symmetry CANNOT prove E-b (the additive
error would have to be ~p^{-w}). Confirmed.

**THE NEW TARGET -- secant-shadow local variance (ChatGPT-5.6, VERIFIED).** Every zero solution casts an
injective "shadow" on the secant set `D_1 = {phi(b)-phi(a): a != b in mu_n}`, `|D_1| = n(n-1)`, via
`S, a in S, b not in S  ->  T=(S\{a}) u {b}`, `F(T)=phi(b)-phi(a)`. Injectivity of `(a,b)->phi(b)-phi(a)`
(recover a+b, b-a from the first two coords; needs w>=2) gives the EXACT transfer
```
   N <= [n(n-1)/(m(n-m))] * ( mu + sqrt( Delta_sec / (n(n-1)) ) ),
   Delta_sec = sum_{v in D_1} (nu(v)-mu)^2.
```
So **E-b follows from a POISSON-SCALE LOCAL VARIANCE `Delta_sec = O(n^2 mu)`** (then `N = O_rho(mu)`, far
stronger than n^3). This replaces the global variance over `Q=p^w` fibers with a LOCAL one over `n^2`
structured fibers on the secant variety of the moment curve. Fourier form: `hat(1_{D_1})(c) = |pi(c)|^2 - n`, so `Delta_sec` is the SIGNED CORRELATION
`sum_{c != 0} nu-hat(c)(|pi(c)|^2 - n)` -- a partial escape from rule-out 1 (a correlation, not a marginal).
r-swap amplification (`2r <= w`, Newton-injective) gives `D_r = C(n,r)C(n-r,r)` shadow fibers and a tighter
transfer constant. **Attack this first.**

**CORRECTION (ChatGPT-5.6 round 2, VERIFIED): the unconditional `Delta_sec = O(n^2 mu)` is FALSE.**
Dyadic block obstruction: for `q=2^s | n` with `q > w` and `q | m`, every union of `k=m/q` cosets of `mu_q`
is a zero solution (coset power sums vanish for j<q), inflating cross-coset secant fibers to
`nu(d_ab) >= B_{q,k} = C(n/q-2, m/q-1)`. When `B_{q,k} > mu` (SMALL entropy gap) this gives
`Delta_sec >= n(n-q)(B_{q,k}-mu)^2 >> n^2 mu`. VERIFIED n=16,p=257,w=2,m=8 (q=4): `Delta_sec/(n^2 mu)=12.77`
(matches the LB 12.54). **My earlier "regime-robust from 4 angles" evidence was REGIME-LIMITED** -- every
tested instance had `B_{q,k} << mu` (moderate theta), structurally blind to the obstruction. (2nd
regime-representativeness miss this session; cf. the PTE threshold. Lesson: my sweeps kept sampling the
easy theta regime -- MUST test the small-theta / B>mu corner.)

**BUT (a) negligible at DEPLOYMENT:** smallest `q>w` is `2^17`, so `L=n/q=16`, block fiber `<= C(14,7)=3432
<< sqrt(mu) ~ 2.4e5`, and needs `2^17 | m`. Also `N_{q,k} <= max(mu,p)` and `p=n^1.47 < n^3`, so blocks
can falsify `N=O(mu)` but NOT `N <= n^3`; at deployed `theta=1.7 > 1/gamma=1.47`, `mu>p` so blocks sit
below mu. **(b) The block solutions are `-1`-INVARIANT** (`-1 in mu_q`), hence IMPRIMITIVE -- the
primitive-only targets dodge them.

**REPAIRED TARGET -- antipodal-flip (ChatGPT-5.6 Sec 6), dodges the obstruction.** Every PRIMITIVE zero
solution has `>= s+1` broken antipodal pairs (`s=ceil(w/2)`, Vandermonde); flipping r of them (`2r<=s`)
lands in `D_r^- = {sum_{a in A}(Phi(-a)-Phi(a))}`, `|D_r^-| = 2^r C(n/2,r)`, giving
`N_prim C(s+1,r) <= sum_{v in D_r^-} nu(v)`. At deployment (r=2): `N_prim <= n^3` needs only the WEAK
average `|D_2^-|^{-1} sum_{D_2^-} nu <= 4.3e4 * mu` (NOT Poisson variance). Fourier kernel:
`hat(1_{D_2^-})(c) = (sigma(c)^2 - sigma(2c) - n)/2`, `sigma(c)=sum_a e_p(-2 sum_{j odd} c_j a^j)` --
odd-coeff-zero c => sigma=n => the even-coordinate DYADIC MAJOR ARCS, peeled recursively via x->x^2;
nonzero-odd-part c = the genuine minor arcs. **This is the corrected deployed target.** (`b2_chatgpt56_r2_verify.py`.)

**ROUND 3 (Codex gpt-5.6-sol, VERIFIED): the flip route does NOT close -- it reduces to a signed
MULTILEVEL large-sieve.** The major-arc peeling does NOT recurse to the same Boolean subset problem.
Setting `y=x^2`, the first major arc is `A_D = p^{-s} Z_1 + R_0`, `Z_1 = #{S: sum_x x^{2j}=0, j<=e=floor(w/2)}`,
and `Z_1` is a WEIGHTED TERNARY slice: `Z_1 = sum_{k_y in {0,1,2}, sum k_y=m, sum k_y y^j=0} 2^{#{k_y=1}}`
-- NOT the plain `mu_{n/2}` fiber count (VERIFIED n=16,p=97,m=8,e=2: Z_1=258 direct = 258 weighted-ternary,
vs plain-Boolean fiber = 2). Iterating, level `l` has ALPHABET `{0,...,2^l}` weighted by `prod C(2^l,k_y)`;
the exact peeled identity is `A_D = mu + p^{-w}/d sum_{m_0} nu-hat(c) K(c)-bar + p^{-w} sum_{l=1}^{L-1}
sum_{m_l} P_l(c)`, and E-b follows from the ONE-SIDED SIGNED estimate
`(LS): Re[ (1/d) sum_{m_0} nu-hat K-bar + sum_{l=1}^{L-1} sum_{m_l} P_l ] <= (4.3e4 - 1) C(n,m)`
(crude ~2500*C(n,m) per level suffices; L=17 levels at deployment, w=67471 -> w_17=0, VERIFIED). Codex Sec 7:
`N_prim <= [d/C(s+1,2)] A_D`, so (T) is quantitatively ~ the primitive bound itself -- "no soft Fourier
argument proves it; the shadow estimate contains nearly all the difficulty of the original theorem."
No counterexample to (T) found; the block family is `-1`-invariant so it does not inflate the two-flip fibers,
but the `q|m` exclusion is NOT stable under weighted descent, so structured mass can reappear at later levels.
Soft tools ALL fail (Codex Sec 6): Cauchy-Schwarz -> global Poisson variance (refuted by blocks); Weil
trivial (`w sqrt p >> n`); Parseval -> global collision energy; MDS -> `2^{n-w}`. **The single open theorem
is (LS): a signed large-sieve / inverse theorem for weighted cyclic moment maps, which no existing tool
provides.** Full review `experimental/notes/audits/codex56_flip_review.txt`, verify `b2_codex_r3_verify.py`.

**Marginal theorem (Sec 3, VERIFIED derivation):** `|nu(v)-mu| <= R_{w,l} = C(w*sqrt(p)+l-1, l)`,
`l=min(m,n-m)` (power-map Weil `|P_j(c)|<=w*sqrt(p)+2` + cycle-index e_l bound). Proves `(*)` at FIXED-w
fixed-density (`gamma>1/2`) but is trivial at deployed high-w (`w*sqrt(p) >> n`) -- the r-uniformity wall
again. Round-1/2 prompts + full reviews in `experimental/notes/audits/chatgpt56_*.txt`.

**Second route -- projective Radon identity (VERIFIED exact).** `N - mu = Q^{-1} sum_{[c] in P^{w-1}}
(p Z_[c] - M)`, `Z_[c] = #{S: sum_{s} f_c(s) = 0}` -- collapses the w-dim problem to 1-dim subset-sum
biases on projective lines; dyadic composition lines `f_c(x)=g(x^{2^k})` are genuine 2-adic MAJOR ARCS,
minor arcs need an averaged bias estimate + an inverse-Littlewood-Offord / list-recovery input.

**Framing (VERIFIED).** `p_j(S) = X_S(zeta^j)` where `X_S = sum 1[zeta^k in S] Z^k`; the constraints =
`prod_{j=1}^w (Z - zeta^j) | X_S(Z)`, i.e. `x in C`, the cyclic `[n, n-w, w+1]` MDS/RS code. So
`N = #{binary weight-m codewords of C}` and E-b = deterministic zero-error list-recovery for a fixed
cyclic RS code at the zero coset near capacity. NB (VERIFIED asymptotics): fixed `alpha=w/n=0.03, gamma=0.68`
forces `log_2 n <~ gamma H_2(rho)/alpha ~ 22.7`, so deployed is a FINITE near-capacity window, not a
fixed-ratio asymptotic family -- a theorem should be stated in the entropy gap `theta = log_n mu`.
