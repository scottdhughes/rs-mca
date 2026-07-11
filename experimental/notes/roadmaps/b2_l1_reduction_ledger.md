# L1/b2 crux: the verified reduction ledger (clean deliverable, 2026-07-10)

Referee-facing capstone of the 07-10 review cycle (3 external rounds: ChatGPT-5.6 x2 + Codex gpt-5.6-sol,
every load-bearing claim re-verified numerically here). Full working log: `b2_l1_crux_milestone.md`;
prompts/reviews in `experimental/notes/audits/chatgpt56_*.txt`, `codex56_flip_review.txt`; verification
scripts `experimental/scripts/b2_*verify*.py`, `b2_secant_*.py`, `b2_LS_levels.py`.

## Object and target

`mu_n` = order-`n` subgroup of `F_p^*`, `n=2^a`, `n|p-1`, `gamma=log_p(n)~0.68` (large subgroup, `n>sqrt p`).
`Phi(x)=(x,...,x^w)`, `F(S)=sum_{x in S}Phi(x)`, `nu(v)=#{|S|=m: F(S)=v}`, `mu=C(n,m)/p^w`, `N=nu(0)`.
Deployed: `n=2^21`, `w=67471` (`w/n~0.03`), `m~rho n`, `p~2^31`. Reformulation: the indicator of `S` lies in
the cyclic `[n,n-w,w+1]` MDS/RS code `C = {x: prod_{j=1..w}(Z-zeta^j) | X_S(Z)}`; `N = #{binary weight-m
codewords of C}`. **TARGET (E-b): `N <= n^3`.**

## The exact reduction chain (every step VERIFIED)

| # | Step | Statement | Verified |
|---|------|-----------|----------|
| 1 | Cycle expansion | `N = sum_{lambda|-m} ((-1)^{m-l}/z_lambda) M_lambda`, `M_lambda=q^{-w}sum_c prod_r pi(rc)^{m_r}`. (NB `q^{-w}sum_c pi(c)^m` = ordered-tuple count, NOT N.) | p=5 counterexample |
| 2 | Low-cycle vanishing | `M_lambda=0` if `l(lambda)<=w` (Vandermonde) => only `>w`-cycle partitions contribute | brute n=small |
| 3 | Descent | `mu_2`-symmetric `S=-S` biject (via `x^2`) with `U in mu_{n/2}`; `N_prim = N - 1[2|m]N(n/2,m/2,floor(w/2))` | n=64,m=8: N_prim=0 |
| 4 | Rotation | `p_j(zeta S)=zeta^j p_j(S)`; `N_prim=n*#free orbits`. (Orbit sizes are `n/2^k` on the dyadic strata `W_k`, NOT all `n`.) | v=(0,1) has orbit n/2 |
| 5 | L^2 too coarse | `Delta_2 >= (Q/(Q-1))(N-mu)^2`; a spike countermodel kills L^2+rotation | exact + abstract |
| 6 | Secant shadow | `N <= [n(n-1)/m(n-m)](mu + sqrt(Delta_sec/n(n-1)))`, `Delta_sec=sum_{v in D_1}(nu(v)-mu)^2` | n=64: bound holds |
| 7 | Block obstruction | unconditional `Delta_sec=O(n^2 mu)` is FALSE: `mu_q` cosets (`q=2^s>w, q|m`) inflate fibers | n=16,p=257: ratio 12.77 |
| 8 | Antipodal flip | primitive `S` has `>=s+1` broken pairs (`s=ceil(w/2)`); `N_prim C(s+1,2) <= sum_{D_2^-}nu`, `\|D_2^-\|=n(n-2)/2` | Vandermonde |
| 9 | Reduces to (LS) | major-arc peel `x->x^2` grows the alphabet `{0,1}->{0,1,2}->...->{0,..,2^l}` (NOT Boolean); E-b <= a signed multilevel large-sieve | Z_1=258 weighted-ternary |

## (LS): the single open theorem

With `A_D = |D_2^-|^{-1} sum_{v in D_2^-} nu(v)`, the exact peeled identity is
`A_D = mu + (root minor arc) + sum_{l=1}^{16} (level-l minor arc)`, and `N_prim <= n^3` follows from
```
(LS)   Re[ (1/|D_2^-|) sum_{c in m_0} nu-hat(c) K-bar(c)  +  sum_{l=1}^{L-1} sum_{c in m_l} P_l(c) ]
       <=  (4.3e4 - 1) * C(n,m),        L=17 levels,   ~2500*C(n,m)/level suffices.
```
- `m_l` = frequencies with nonzero odd part at level `l`; `P_l(c) = [t^m] prod_{y in mu_{n_l}} (1+t e_p(sum_j c_j y^j))^{2^l}` (binomially-weighted multiset, alphabet `{0,..,2^l}`).
- `K(c)=(sigma(c)^2-sigma(2c)-n)/2`, `sigma(c)=sum_a e_p(-2 sum_{j odd}c_j a^j)`.

**Per-level regime (`b2_LS_levels.py`):** all 17 levels have per-frequency Weil TRIVIAL (`w_l sqrt(p) >> n_l`).
Levels 0-5 are LARGE subgroups (`gamma_l 0.68->0.52`); levels 6-16 are sub-`sqrt(p)` BGK small subgroups
(`gamma_l -> 0.16`); multiplicity `2^l` grows across the cascade. So (LS) is a signed-cancellation estimate
spanning BOTH exponential-sum regimes with weighted alphabets. **`(LS)` is quantitatively ~ the primitive
bound itself** (Codex Sec 7: `N_prim <= [|D_2^-|/C(s+1,2)] A_D`) -- it contains nearly all the difficulty.

## Rule-out ledger (all VERIFIED dead for the deployed regime)

1. Marginal / sup `|pi(c)|`, c1-averaged 4th moment -- N needs JOINT `M_lambda`, not marginals.
2. Graph-energy import (Vyugin-Makarychev/Stepanov) -- `deg<=|G|^{1/3}` structural cap, our `w>>n^{1/3}`.
3. PTE / vanishing-sums over `Z/n` -- controls only the char-0 small-`d` EDGE, `~2^{-10^6}` energy-subdominant.
4. Bulk coupling of dilates `{pi(rc)}` -- pairwise-exactly / typically independent; difficulty is c=0 + resonances.
5. Global `L^2` / Poisson variance -- `Delta_2 >= (Q/(Q-1))(N-mu)^2` + block countermodel.
6. Per-frequency Weil -- trivial at every cascade level (`w_l sqrt p >> n_l`).
7. Cauchy-Schwarz on (LS) -- returns to the refuted global collision energy; MDS gives only `2^{n-w}`.

## Relation to upstream secant work (reassessed 2026-07-10) — NO conflict, distinct object

"Secant" is heavily used upstream in a DIFFERENT lane. holmbuar #528/#534 + #560/#561 develop the
**transverse / syndrome-secant** of the RATIONAL NORMAL CURVE: counting bad SLOPES on a syndrome line
`y0 + gamma y1`, giving the MCA NUMERATOR (decoding badness) `= max transverse secant count` (#561
formalizes `thm:syndrome-secant-exact`), with the field-independent bound `C(R+kappa, kappa+1)` (#528).
That is the RC / balanced-core lane (hard input 3), the DECODING side.

**Ours is a different object**: the MOMENT-CURVE SECANT-SHADOW of the FIBER COUNT `nu` -- `D_1 =
{Phi(b)-Phi(a)}` used to transfer a bound onto `nu(0)=N` (max-fiber / Fourier side, Route-D node #5).
No conflict, not superseded: the syndrome-secant bound is VACUOUS on the residual `kappa=Theta(n)` cores
(#534: `C(R+k,k+1)=e^{Theta(n)}`), so the Fourier-side fiber approach here is exactly what those residuals
need. (Terminology: label ours "moment-curve secant-shadow of the fiber count" to avoid conflation.)

**Cross-lane insight (both lanes hit the SAME PTE wall).** #534's obstruction is a **Prouhet-Thue-Morse
residual family** (disjoint equal-size supports with EQUAL depth-`w` power sums, Prouhet's theorem), forcing
`kappa=k=Theta(n)`. That is the SAME equal/vanishing-power-sum structure as OUR dyadic block obstruction
(`mu_q` cosets, `q=2^s>w`, vanishing power sums to `w`) and the E-a additive-energy PTE tail. So the
equal-power-sum / PTE obstruction is UNIVERSAL across the prize -- it blocks the decoding-side secant route
(#534) and the Fourier-side secant-shadow (step 7 here) by the same mechanism. Any closing theorem (RC-side
(A4) Sidon payment, or our `(LS)`) must overcome this one PTE wall.

## UPDATE (ChatGPT-5.6 web round 3 + my robustness check, VERIFIED): antipodal/(LS) positive-peeling
## route REFUTED; the trimmed full-secant `(SV*)` is the new (better) target

The antipodal-flip route's "bound odd minor arc `O(n^2 mu)` + nonnegative even major peeling" DOES NOT close.
- **Refutation (verified 3 ways).** (a) My root-incidence framework (`b2_LS_incidence_framework.py`) is
  REGIME-LIMITED: `b2_LS_framework_robust.py` shows at small mu (n=24,p=193,mu=0.376) 96/552 generic
  secant targets are resonant (>5mu) -- resonance is NOT confined to the antipodal locus. (b) ChatGPT-5.6
  exact counterexample n=16,p=257,w=7,m=8: the even major arc `N_ev>=256` gives `p^-4 N_ev/mu >= 3.4e5`
  (>> 4.3e4 budget) yet the true `D_2^-` count is 0 (algebraic two-pole certificate) -- the odd minor arc
  CANCELS the major arc exactly (VERIFIED: all 256 one-per-antipodal-pair subsets have vanishing even
  moments). Positive/separate bounding destroys the essential cancellation. (3rd regime-miss this session.)

**NEW TARGET -- trimmed full-secant `(SV*)`.** Return to the FULL ordered secant `d_{a,b}=Phi(b)-Phi(a)`
(injective from the first 2 moments; `N_prim m(n-m) <= sum_{a!=b} nu-tilde(d)`, `nu-tilde = nu - beta`,
`beta` = the EXPLICITLY removed dyadic block zeros, `|B| < 1.3e4` at deployment => negligible). E-b follows
from the ONE-SIDED RMS bound
```
(SV*)   ( (1/n(n-1)) sum_{a!=b} (nu-tilde(d_{a,b}) - mu)_+^2 )^{1/2}  <=  (alpha/2) n^3,   alpha=m(n-m)/n(n-1)~rho(1-rho).
```
This permits `n^8`-scale one-sided variance vs the Poisson scale `n^2 mu ~ n^3.7` -- FOUR+ powers of n weaker,
`~10^3x` more first-moment slack than the antipodal r=2 target. **NO nonzero exact major arcs**: the Fourier
kernel is `K_sec(c)=|tau(c)|^2 - n`, and `|tau(c)|=n => f_c const on n>w points => f_c=0`. **Large-sieve
lever (VERIFIED, `verify_chatgpt_web2.py`): `p^-w sum_c |tau(c)|^{2h} <= h! n^h`** for `h<=w` (Newton), giving
`#{c: |tau(c)|>=lambda} <= p^w h! n^h / lambda^{2h}` -- a real handle on the exceptional spectrum.
**Numerically (SV*) holds with ~5 orders of magnitude of room** including the small-mu regime that broke
positive-peeling (`b2_SVstar_hardregime.py`: one-sided var ~3e4 vs budget ~1.9e9 at n=24,p=193).

**SCALING GATE PASSED (clean theta-controlled test, `b2_SVstar_invariant.py`).** The right invariant is
`var/(n^2 mu^2)` (since `var ~ n^2 mu^2` when fibers are relatively bounded, and `n^2 mu^2 = n^{2+2theta} <
n^8 iff theta < 3`; deployment `theta=1.7`). Across theta from -2.3 to +1.87, `var/(n^2 mu^2)` decreases
MONOTONICALLY: 9.3e5, 1.5e4, 380, 2.4, 0.71, 0.124, **0.008 at the deployment proxy (n=32,p=97,theta=1.87)**;
fibers concentrate (`max nu/mu: 1117 -> 1.13`). The earlier "n^9.55 / var/budget growing" was ENTIRELY the
small-mu (theta<0) corner -- the OPPOSITE of deployment. The test spans THROUGH deployment theta (favorable
region), and concentration only strengthens at deployment's far larger mu. So `(SV*)` holds at deployment
with `var ~ n^{5.4} << n^8` -- ENORMOUS room. (First target this session to survive a properly theta-controlled
hard-regime test.) Deployment n-scan at fixed theta is computationally infeasible (needs `p~2^{n/3}`,
`F_p^3 ~ 2^n`), so the theta-invariant is the correct evidence, not a raw n-scan.

**Open (the crux, now the sole remaining step):** couple the moment lever (11)/(12) to the fixed-weight
coefficient `nu-hat(c)` to PROVE `(SV*)`. The obstruction class is sharpened to a multi-coset negacyclic Littlewood family (two-spike
divisibility `prod_{j<s}(Z-zeta^{2j+1}) | (ternary 2-spike)`); a single quotient coset is ruled out by Plotkin
(<35 classes). Alternative algebraic form: the two-pole lacunary-divisor identity `T^m V B + T^{n-m} U A +
AB + UV = 0` (squarefree divisor pairs of `T^n-1`). Full review: `experimental/notes/audits/` (to add).

## TERMINAL REDUCTION MAP (2026-07-10): everything reduces to the additive-energy excess = subgroup VMVT

All ~6 provable routes (secant variance, antipodal-flip, LS, SV*, coupling, weighted-CS, MacWilliams,
dyadic-tower) reduce to ONE object: the CENTERED SECOND MOMENT / additive-energy excess
```
  Delta_energy = Sum_{c!=0} |nuhat(c)|^2 / p^w  =  E - C(n,m)^2/p^w  =  Sum_{d>w} C(n-2d,m-d) E_d,
  E_d = #{ disjoint A,B in mu_n : |A|=|B|=d, p_j(A)=p_j(B) for j<=w }  = a subgroup Vinogradov mean value.
```
Verified: `Sigma_c nuhat |tau|^2 = shadow count` exactly (coupling == direct shadow); SV* variance == a
bilinear form in nuhat with the same `|tau|^2-n` kernel. RULE-OUTS all confirmed: magnitude-coupling too
loose (loss ~ m^{4.8}); Cauchy-Schwarz -> global energy (refuted); MacWilliams blocked by the BOOLEAN
restriction (nuhat is a Boolean-weight-m count, NOT a linear-code enumerator); dyadic TOWER descent captures
only ~0.4% of Delta_energy (it is ~99.6% PRIMITIVE/odd-frequency -- our n=2^a structural edge does NOT close
it, consistent with the E-a bulk-domination). No external help.

**RE-OPENED TOOL (the attack, traced 2026-07-10):** the secant reduction turned the SUP (N = max-fiber,
VMVT-unreachable) into the MOMENT `Delta_energy` = subgroup VMVT. `E_d = J_{d,w}(mu_n; mod p)` (Vinogradov
mean value over `mu_n` for the w-dim moment curve). Our regime `d ~ 5w`: VMVT-SUBCRITICAL (`d << w^2/2`, so
integer-VMVT/BDG supercritical tools -- e.g. general-set VMVT arXiv:2001.08312 needing `s>=k(k+1)` -- do NOT
apply) but RANDOM-dominated (`d > 1.47w = d*gamma`, so `E_d ~ n^{2d}/p^w`). The random term is a MOD-P
collision term absent in integer VMVT, so bounding `E_d ~ random` == subgroup exp-sum equidistribution with
GROWING #monomials = the r-uniform-subgroup-cancellation frontier (same as ch.1 -- ~8 angles all land here).
**Closest PROVEN neighbor: Shkredov, arXiv:1802.09066 Thm 3** -- `T^+_{2^k}(Gamma) - |Gamma|^{2^{k+1}}/p <=
2^{3k^2}(C log^4 p)^{k-1}|Gamma|^{...}`, i.e. the subgroup ADDITIVE (w=1) energy IS "random + controlled
error", proven via efficient-congruencing-over-subgroups. **THE CRUX = the w-dimensional (moment-curve)
extension of Shkredov Thm 3.** Concrete, named, hard; proven w=1 template exists. Next attack: internalize
Shkredov's method and attempt the moment-curve lift.

## w=2 BASE CASE: PROOF SKELETON (2026-07-10, all inputs numerically verified)

The reduction's target `E^{(2)}_d = Sum_v nu_d(v)^2 <= C * C(n,d)^2/p^2` (mu_n additive energy on the PARABOLA
`{(x,x^2)}`) is PROVABLE for w=2 by Shkredov's Thm-3 machinery, lifted one dimension into F_p^2 where Rudnev's
incidence tool holds. Structure (each step verified, scripts `b2_w2_basecase/recursion/engine.py`):
1. TARGET confirmed: `E^{(2)}_d/random -> 1` as d grows (18.97,2.63,1.20,1.03,1.007,1.001 for d=2..10);
   equidistribution holds; d=2 is the rigid Sidon point.
2. RECURSION (verified, convolution form): `E^{(2)}_d = d^{-2}[ n E^{(2)}_{d-1} + Off ]`,
   `Off = p^{-2} Sum_c |nuhat_{d-1}(c)|^2 (|tau_2(c)|^2 - n)`, `tau_2(c)=Sum_{x in mu_n} e_p(c1 x + c2 x^2)`.
3. ENGINE = SIDON-OPTIMAL 4th moment (verified): `Sum_c |tau_2(c)|^2 = p^2 n` (Phi injective), and
   `Sum_c |tau_2(c)|^4 = p^2 * E_2(parabola) = 2 p^2 n^2` (the MINIMUM 4th moment -- the parabola is a
   Sidon/B_2 set). This is the strong large-sieve input Shkredov's method needs.
4. Cauchy-Schwarz + engine: `Off <= sqrt(2) n (E^{(2),4}_{d-1})^{1/2}`, introducing the next-higher energy;
   the ORDER-RECURSION on `E^{(2),4}` terminates at the Sidon 4th moment -- exactly Shkredov Thm 3's double
   recursion (in d and in energy-order k), which is PROVEN to close for w=1.

So E-b/SV* is PROVABLE at w=2 (genuine partial theorem), modulo the standard Shkredov error-bookkeeping.
VALIDATES THE METHOD: the max-fiber->moment reduction + adapted Shkredov recursion closes E-b whenever the
incidence engine exists (low w, F_p^2/F_p^3 = Rudnev's regime). w=3 (twisted cubic, still F_p^3, also Sidon)
should follow identically. Deployed w=67471 unchanged: needs high-dim (F_p^w) incidences = the frontier.

## w=3 EXTENDS (twisted cubic, verified); the WALL is precisely at w>=4 (high-dim incidences)

w=3 (moment curve = twisted cubic in F_p^3) closes by the IDENTICAL skeleton (`b2_w3_engine.py`): engine
`Sum_c|tau_3|^2 = p^3 n`, `Sum_c|tau_3|^4 = 2 p^3 n^2` (Sidon-optimal, verified ratios ~1 and ~2); same
convolution recursion (ratios 1.05-1.07). Twisted cubic is Sidon (3 power sums over-determine {a,b}),
still in Rudnev's F_p^3 regime.

**PRECISE WALL.** The moment curve {(x,...,x^w)} is Sidon for ALL w, so the ENGINE (4th moment = 2 p^w n^2)
exists at every w. What breaks at w>=4 is the ORDER-RECURSION: `Off <= sqrt(2) n (E^{(2),4}_{d-1})^{1/2}`
needs the 4-FOLD moment energy `E^{(2),4}` bounded ~random, which is a Vinogradov mean value over F_p^w and
requires point-plane/curve INCIDENCE bounds in F_p^w. Rudnev's incidence theorem exists in F_p^2/F_p^3 only,
so the method is UNCONDITIONAL for w<=3 and BLOCKED at w>=4 by the absence of high-dimensional finite-field
incidence bounds -- a named frontier in incidence geometry. Deployed w=67471 sits far past the wall.

**Net honest state (CORRECTED 2026-07-10 after auditing the scripts -- prior "PROVABLE THEOREM for w<=3" was
an OVERCLAIM).** Precise status of the w<=3 argument:
  - RIGOROUSLY PROVEN (all w >= 2, not just w<=3): the engine identities  sum_c|tau_w(c)|^2 = p^w n  and
    sum_c|tau_w(c)|^4 = p^w(2n^2-n)  -- Newton + orthogonality, exact integer counts verified. See
    `b2_engine_identity_proof.md` / `verify_engine_exact.py`. The engine is NOT the wall (it holds at every w).
  - NUMERICALLY VALIDATED ONLY (NOT rigorously carried out): the convolution recursion for the d-subset
    syndrome energy E_d^{(2)} (ratios ~1.0-1.07 in `b2_w{2,3}_recursion.py`) and the equidistribution/
    deviation bound (`b2_w2_basecase.py` literally says "Deviation = the proof's job"). The closure is
    asserted "by the same skeleton as Shkredov Thm 3" + a Rudnev F_p^2/F_p^3 incidence application that is
    NOT written out here.
  So w<=3 is a NUMERICALLY-VALIDATED SKELETON with a proven engine, NOT a completed theorem: the deviation
  bound is deferred (a "by the same X" deferral, which by our own discipline is not "complete"). To upgrade to
  a theorem one must carry out the Rudnev application and the order-recursion termination rigorously (a real
  task, not attempted under time pressure to avoid a self-blessed flawed proof). The deployed-row obstruction
  is unchanged: high-dim (F_p^{>=4}) moment-curve incidence bounds / the signed cancellation.

## Sharpened wall map (2026-07-10): TWO thresholds, and the L^2-vs-L^inf gap is the real crux

Direct numerical mapping of the syndrome-energy landscape (`b2_saddle2.py`, `b2_threshold.py`,
`b2_regime_rep.py`, `b2_decouple.py`), all at theta=1.7-reconciled deployment params (n=2^21, KoalaBear p,
w=67471 -> m~0.468n; the summary's "m=0.33n" is inconsistent with theta=1.7 and was corrected):

1. **Saddle localization.** The energy excess `Delta = Sum_{d>w} C(n-2d,m-d) E_d` is SHARPLY peaked at
   `d* ~ 0.33n` (90% mass in a width-~1500 window), effective fiber dimension `d*-w ~ n/2 ~ 5x10^5`. So the
   dominant layer is DENSE (a constant fraction of mu_n), NOT sparse. This KILLS the low-dim polynomial-fiber
   escape (fiber dim of the dominant layer is Theta(n), not O(1)): incidence geometry is sparse-set tech and
   cannot reach dimension Theta(n).

2. **TWO thresholds, cleanly separated.**
   - COLLISION threshold `C(n,d) = p^w`: below it syndromes are ~injective on d-subsets (diagonal-dominated);
     above it (large d, the dominant layer) collisions are forced.
   - EQUIDISTRIBUTION threshold `n = w*sqrt(p)` (Weil/completion cost): `b2_threshold.py` confirms
     excess/main collapses super-exponentially (10^3 -> 10^-16) as `r = n/(w sqrt(p))` crosses 1, universal
     across p=17,41,97. Deployed `r ~ 6.7x10^-4` -- ~1500x BELOW the equidistribution threshold.

3. **Decoupled finding (the important one).** Holding `C/p^w ~ 100` fixed (above collision) and driving r
   from 0.47 down to 0.0071 by growing n (`b2_decouple.py`), excess/main stays FLAT (~0.002-0.02, no growth).
   => In the ABOVE-COLLISION regime (where d* lives), the L^2 energy is controlled by C/p^w and is INDEPENDENT
   of r; the Weil/equidistribution wall does NOT bind the L^2 energy. The controlling mechanism is the Sidon
   4th moment (holds for ALL w), i.e. combinatorial smoothing, not degree-w character-sum equidistribution.
   The earlier "r<<1 -> catastrophe" is a BELOW-collision artifact (confounded: in a naive p-scan r and
   C/p^w drop together; decoupling removes it).

4. **The real wall = a SIGNED cancellation the L^2 energy cannot see.** L^2 control is NECESSARY but NOT
   SUFFICIENT. Target is `N_0 = #{m-subsets, syndrome 0} <= n^3`, with `N_0 - mu = p^{-w} Sum_{xi!=0} Nhat(xi)`,
   `Nhat(xi) = e_m({chi_xi(a)})` (m-th elementary symmetric of the curve-exp-sum values). EXPONENT ARITHMETIC
   (log_n units at deployment): `p^w = n^{~99568}`, `C(n,m) = n^{~99570}`, `mu = n^1.7`, target slack = n^{1.3}.
   - Energy bound `N_0 <= sqrt(E)` is HOPELESS: `E = Sum_c N_c^2 >= C(n,m)^2/p^w >> n^6` unconditionally.
   - Cauchy-Schwarz on `Sum_{xi!=0}|Nhat(xi)|` loses a factor `p^{w/2} = n^{~49784}`; the target slack is only
     n^{1.3}, so no L^2/energy bound (any rho) can be rescued by slack.
   - In the RANDOM model `N_0-mu ~ sqrt(C(n,m)/p^w) = sqrt(mu) = n^0.85` -- TINY -- but ONLY via cancellation
     among the p^w signed frequencies. Every ABSOLUTE-VALUE method (L^2, L^{2k}, restriction/extension) is
     SIGN-BLIND and forfeits exactly that p^{w/2} cancellation. So a restriction/large-sieve estimate that is
     merely an L^2->L^q amplification is NOT enough; the estimate must be SIGNED (one-sided inverse theorem).
   The only sign-aware crossings are per-frequency Weil (blocked: degree w=67471 > sqrt(p) ~ 46340) or a signed
   higher-moment cancellation (blocked: dimension w >= 4 incidences). Deployment is past BOTH -- degree AND
   dimension -- and tonight's L^2 control, though unconditional (Sidon, all w), sits on the WRONG side of the
   sign barrier: it certifies WHERE the difficulty is NOT (magnitude), leaving the signed cancellation as the
   whole game.

## Signed higher-moment identity: exact, tower-structured, but the hard part does NOT localize (2026-07-10)

Attack on the signed crux directly (`b2_signed_mech.py`, verified vs brute force in every case).

**Exact identity (building block).** With curve sum `S(eta) = Sum_{a in mu_n} e_p(eta . Phi(a))`, orthogonality
gives `(1/p^w) Sum_xi S(c_1 xi)...S(c_r xi) = #{(a_1..a_r) in mu_n^r : Sum_i c_i Phi(a_i) = 0}` =: M_{c_1..c_r}
(a signed subgroup power-sum solution count). Via Newton-Girard `Nhat(xi) = e_m({chi_xi(a)}) = Sum_{lambda|-m}
c_lambda Prod_i S(lambda_i xi)`, hence the TARGET is an exact signed sum
`N_0 = Sum_{lambda |- m} c_lambda M(lambda)`. Verified: `N_0 = (1/p^w) Sum_xi e_m({chi_xi(a)})` matches brute
force exactly (p=17/97, n=8/16, w=2/3). The SIGNS c_lambda carry the p^{w/2} cancellation; unsigned is the disaster.

**Low-order moments are rigid (no info).** M_c = 0 (c!=0); M_{c1,c2} = n if c1+c2=0 else 0 (Sidon collapse).
Information about N_0 lives only in HIGH order (large parts / many parts) -- not truncatable at low order.

**Tower/Mobius decomposition (real, exact).** Split frequencies by conductor down the dyadic tower of n=2^21.
Imprimitive xi (factors through a -> a^2, i.e. xi_j=0 for odd j) give `Nhat(xi) = e_m(doubled mu_{n/2} system)`
via b=a^2 (each b hit twice) -> the (n/2, w/2) level with TERNARY occupation (0/1/2 copies) = the low-weight
ternary-RS-codeword structure already in this ledger. So `p^w N_0^{(n,w)} = P(n,w) + T(n,w)`, T = tower term
reducing to (n/2,w/2), P = primitive residue. Recursion is clean; 22 levels for n=2^21.

**But the hard part does NOT localize (the negative result).** Numerically:
- The "primitive signed sum = 0" hope is FALSE (a lucky n=8,m=3 coincidence only).
- Imprimitive part is COHERENT (|sum|/abs ~ 0.98, ~no internal cancellation) -- tower-structured, small mass,
  provable.
- Primitive part is INCOHERENT: huge unsigned mass, STRONG internal (Weil-type) cancellation (|sum|/abs ~
  0.06 at w=2, 0.0009 at w=3 -- strengthens with w), leaving a residue P that is STABLE in w (identical
  -29488 at w=2 and w=3, p=97,n=16) -- it does NOT shrink into the tower.
So the tower ORGANIZES N_0 into 22 primitive residues P(n/2^i, w/2^i), each of which still requires the generic
signed (Weil-type) cancellation. No tower-recursion shortcut. This SHARPENS (LS): it must be a GENERIC signed
large-sieve, not a structural/tower identity -- consistent with the sign-barrier arithmetic above.

**Primitive residue P has a closed form + square-root cancellation CONFIRMED (b2_P_scaling.py).** Swapping
summation order: `Sum_{xi prim} e_p(xi.F(S)) = p^w 1_{F(S)=0} - p^{w/2} 1_{F(S)_even=0}`, so exactly
`P(n,w) = p^w N_0 - p^{w/2} N_0^{even}`, where N_0^{even} = #{m-subsets with the w/2 EVEN power sums = 0}.
Mean(P) = 0 (p^w mu = p^{w/2} mu_even = C(n,m)); |P| IS the joint fluctuation. Exact DP (n=32,w=2,m=6) over
p=97..1601 (r=1.6 down to 0.4, deep below equidist threshold): |P|/p stays ~const (~4e3), |P|/p^2 decays
38->2.4. So |P| ~ p^{w/2} * O(poly(n)) -- SQUARE-ROOT CANCELLATION HOLDS below threshold. The target
`N_0 <= n^3` needs exactly `|P| <~ sqrt(p^w C(n,m)) * poly = p^{w/2} * poly`; numerics say this is TRUE.
=> the direction is VIABLE; the obstruction is PROVING the square-root cancellation (the large-sieve), not
whether it holds. Open target sharpened to: prove `|P(n,w)| <~ p^{w/2} poly(n)` for the B_w-Sidon moment curve
over mu_n, in the regime w > sqrt(p) AND w >= 4 (past Weil AND incidences).

## Characteristic-zero structure: CAS-verified, and DEPLOYED char-0 count = 0 (2026-07-10)

Sage/CyclotomicField exact computation (`b2_char0.sage`), verified vs brute force in 12 cases (all match).
For n=2^k, Lam-Leung (vanishing sums of 2^k-th roots of unity = antipodal pairs) gives: p_1(S)=0 forces
S=-S (antipodal); then p_odd(S)=0 automatically and p_{2i}(S)=2 p_i(S^2), S^2 subset mu_{n/2}. Hence the
char-0 count obeys the EXACT halving recursion
   N_0^{(0)}(2^k, w, m) = [m even] * N_0^{(0)}(2^{k-1}, floor(w/2), m/2),   base N_0^{(0)}(.,0,m)=C(2^k,m).
This IS the dyadic tower, now identified as the ALGEBRAIC (char-0) backbone = the coherent/provable part.

**DEPLOYED: N_0^{(0)} = 0.** Tracing m: 981104 -> 490552 -> 245276 -> 122638 -> 61319 (ODD at level 5,
before w=67471 exhausts). So there are NO characteristic-zero solutions at all: 100% of N_0(F_p) ~ n^1.7 is
GENERIC mod-p vanishing (subsets S with Sum a^j == 0 mod p but the cyclotomic integer Sum a^j != 0).
CONSEQUENCE: rules out any char-0 / variety-point-count / lifting approach (nothing to lift). The target
N_0 <= n^3 is a PURELY ANALYTIC statement (a genuine large-sieve / signed cancellation), with zero algebraic
shortcut. Confirms why the primitive residue P carries everything and the difficulty cannot be localized.

## Bernoulli reformulation + inverse-Littlewood-Offord framing (Codex 5.6 attack, VERIFIED parts, 2026-07-10)

An adversarial Codex-5.6 pass produced two things worth keeping (each tagged verified/unverified):

- VERIFIED (I reproduced, `verify_codex_bernoulli.py`): the fixed-weight count can be traded for a BERNOULLI
  product measure. With X ~ Bernoulli(rho), rho = m/n, and S_rho := Pr(F(X)=0),
      N_0 <= S_rho / [ rho^m (1-rho)^{n-m} ],   and the cost ratio is <= sqrt(2n)  (binomial concentration).
  Confirmed in all tested cases (cost 2.7-7.2 vs sqrt(2n)=5.7-8.0). Since sqrt(2n) << n^3 slack, this is FREE.
  KEY GAIN: the Bernoulli characteristic function  prod_{a in mu_n} (1 - rho + rho e_p(xi.Phi(a)))  FACTORS
  over a (the elementary symmetric e_m does NOT). Hence |prod|^2 = prod_a [1 - 2 rho(1-rho)(1 - cos(2 pi
  xi.Phi(a)/p))]. This is exactly an ANTI-CONCENTRATION / inverse-Littlewood-Offord object for the vectors
  Phi(a) in F_p^w.

- NEW FRAMING (conceptual): the crux = "how concentrated can sum_a eps_a Phi(a) be at a single point of
  F_p^w?" at scale p^{-w} = exp(-Theta(n)). This connects to a MATURE toolbox unreachable from e_m: Halasz's
  inequality, Esseen concentration, Tao-Vu / Nguyen-Vu inverse theorems. Honest gap (Codex's and mine): those
  theorems detect atoms of POLYNOMIAL size; we need EXPONENTIAL scale exp(-Theta(n)). No off-the-shelf theorem
  (Codex found none; capacity-level RS results -- Doron-Venkitesh 2404.00206, Alrabiah-Guruswami-Li 2304.09445
  -- assume random evaluation points / larger fields, not the deterministic mu_n).

- Antipodal (C_y, eps_y) decoupling (matches our char-0 analysis): for pair {a,-a}, C_y=X_a+X_{-a} in {0,1,2}
  drives EVEN power sums, eps_y=X_a-X_{-a} in {-1,0,1} drives ODD ones; a (-1)-invariant config has eps_y=0
  hence zero odd syndrome, so the coset/antipodal obstruction is genuinely absent from the odd-syndrome part.

- UNVERIFIED / FLAGGED: Codex's numerical "falsifier" table (constant ~20) did NOT reproduce -- its (17,16,3,1)
  entry claims 176 hits; exhaustive recount gives 3840 (definitional mismatch). NOT trusted; not load-bearing
  (Codex also dismissed those toys). Cross-check that DID hold: Codex independently concluded uniform sqrt-
  cancellation for P is FALSE without hypotheses (matches our confounded-prefactor finding).

NET: the live target is now equivalently an inverse-Littlewood-Offord / Halasz anti-concentration bound for
the moment-curve vectors Phi(a) over mu_n at exponential scale -- a NEW toolbox for the same irreducible gap.

**Halasz MAGNITUDE route is sign-blind and BLOCKED -- verified (b2_halasz.py).** The Bernoulli factor obeys
|prod_a (1-rho+rho e_p(xi.Phi(a)))| <= exp(-rho(1-rho)(n - Re S(xi))), S(xi)=sum_{a in mu_n} e_p(xi.Phi(a)).
A magnitude (Halasz/Esseen) bound on the shadow needs sum_{xi!=0} exp(-rho(1-rho)(n-Re S(xi))) small; union
bound over the p^w frequencies requires n-Re S(xi) >= w log p / (rho(1-rho)) for the worst xi. Since
n-Re S <= 2n always, this is feasible ONLY when  w log p <= rho(1-rho) 2n  (equivalently w <~ n/(2 log p)).
Numerics: feasible at p=17 (6<8) but INFEASIBLE by p=97 (9>8, 14>8); deployment 1.45e6 > 1.04e6 (w=67471 >
n/(2 log p) ~ 48800) is deep past it -- a THIRD threshold deployment exceeds. And directly measured: the
magnitude sum overcounts the true SIGNED shadow deviation by 71x-500x (growing with w). CONCLUSION: taking
|prod_a| discards exactly the p^{w/2} cancellation; the anti-concentration reframe RELOCATES the sign wall,
it does not bypass it. Every magnitude-based tool (L^2, L^{2k}, restriction/extension, Halasz) is now ruled
out by ONE unified mechanism (sign-blindness + p^w frequency count). The reframe pays off ONLY via the SIGNED
inequality (Codex's (3)) = the same irreducible crux, now in inverse-LO language (needs a SIGNED inverse
Littlewood-Offord / local-limit theorem at exponential scale exp(-Theta(n))).

## PRIOR ART / connection to grande_finale (2026-07-11) -- honest repositioning

Discovered on 07-11 (should have checked FIRST): the repo's `experimental/lean/grande_finale/` (this L1 lane's
own formalization, 0 sorry / 0 axiom, builds) ALREADY formalizes the entire reduction chain of this node down
to ONE explicitly-open crux, and names it. Mapping to my session's language:
  - repo "conjecture Q / row-sharp Q atom / primitive q-collision moment Gamma_q^{prim} <= exp(o(n) q)"
    == my "primitive residue P / signed cancellation at exponential scale". SAME object.
  - `QFourierTao.lean`: proves the moment-to-max reduction `log max_s R(s) <= (w log|B| + log Gamma_q)/q`
    and (with QEntropyInverse `collision_moment_le_of_max`) the two-sided equivalence
    `Gamma_q^{prim} <= exp(o(n)q)  <=>  Q (prefix-flatness / max-fiber bound)`. Machine-checked.
  - `QPrimitiveCollision.lean`: the moment=collision identity, the Vandermonde rigidity `|M Delta M'| >= w+2`
    (== my B_w-Sidon symmetric-difference bound), prefix-injectivity on small sets. Machine-checked.
  - `QFourierTao.lean` docstring states VERBATIM that the deep input `thm:primitive-log-collision` "rests on an
    inverse Littlewood-Offord / Balog-Szemeredi-Gowers large-spectrum step ... a genuinely open ingredient and
    is NOT discharged here." == the inverse-LO framing I banked this session (credited to Codex) -- it was
    ALREADY the manuscript's blueprint.
  - `Frontier.lean`, `BC.lean`, `SP.lean`, `QFiniteTables.lean`: honest finite/decidable kernels + the marked
    open pieces (row-sharp Q atom, BC census). The crux is GENUINELY OPEN in the repo too.

HONEST REPOSITIONING of this session's work: it INDEPENDENTLY RE-DERIVED the established frontier (the
reduction, the inverse-LO framing, the Vandermonde rigidity) -- NOT novel. Per no-novelty-overclaim discipline,
default to "confirms/sharpens the recorded frontier," not "discovered." Genuinely ADDITIVE (pending check vs
the existing files, some may also be covered):
  - unified rule-out: EVERY magnitude method (L^2, L^2k, restriction, Halasz/anti-concentration) blocked by ONE
    mechanism (sign-blindness + p^w frequency count once w log p > rho(1-rho) 2n) -- a clean negative statement;
  - quantitative thresholds n >~ w sqrt(p) and w log p <= rho(1-rho) 2n that deployment exceeds;
  - char-0 N_0^{(0)} = 0 at deployment (Lam-Leung antipodal; may overlap slackMCA_v4/CharZeroFiber.lean);
  - Aristotle `energy_bound` (E_d <= 2C(n,d)^2/p^w) reduced to the single d>w additive-energy sorry (= same Q
    crux) WITH a Lean counterexample that the pointwise/max-fiber route CANNOT give the constant (p=13,n=12,w=2,
    d=3 fiber=4) -- independently confirms cancellation is essential;
  - Aristotle engine Lean proof (B_h-Sidon no-nontrivial-tuple) -- BUILDS clean (0 sorry); likely redundant with
    QPrimitiveCollision rigidity but a clean standalone certification.
NEXT: engage the EXISTING grande_finale frontier (the inverse-LO/BSG large-spectrum step for the primitive
collision moment) directly, instead of re-deriving the scaffolding.

## Consequence / consistency

This EXACTLY matches and independently re-derives the `(LS)` target below: the
missing tool is a one-sided multilevel LARGE-SIEVE / RESTRICTION estimate for the moment curve over mu_n
(L^2-of-coefficients -> L^inf/L^q-of-the-sum), spanning the large-subgroup (n > sqrt(p)) and sub-sqrt(p)
regimes. Tonight's two-threshold map says precisely WHY no single classical tool supplies it: any restriction
estimate must be simultaneously degree-agnostic (w > sqrt(p)) and dimension-agnostic (w >> 3), and the two
existing engines (Weil, Rudnev incidences) each require one of these small. The L^2 side is unconditional
(Sidon, all w); the entire difficulty is the amplification to L^inf. That is the irreducible open theorem.

## Status (superseded above for the target; chain 1-6 unchanged)

The L1/b2 prize crux is reduced by an EXACT, verified chain to `(LS)` -- a one-sided SIGNED multilevel
large-sieve / inverse theorem for binomially-weighted cyclic moment maps, spanning the large-subgroup and
sub-`sqrt(p)` regimes over 17 levels. No existing tool provides it; no counterexample is known. This is the
irreducible open theorem for the L1/b2 (max-fiber / entropy-inverse) lane = Route-D frontier node #5
("KB max-fiber signed-e_m inverse, the Fourier side of the closure"). NOT a proof.

## Engaging the grande_finale frontier directly (2026-07-11): Γ_r for r>=3, and Q3 assessment

Read the exact open target (`q_section.tex` conj:q-active + prop:q-moment-sandwich): with mu(z)=N_w(z)/C(n,m),
`Gamma_r := |B|^{w(r-1)} sum_z mu(z)^r`, and moment sandwich `log Gamma_r/(r-1) <= log R <= (log Gamma_r +
w log|B|)/r` (R = max/mean fiber ratio). r=2 is the proved exact second moment; the OPEN target is
`Gamma_r <= e^{o(n)}` for a fixed r >= 3. The manuscript's own diagnosis (Q5) matches this session exactly:
"the missing cancellation is JOINT cancellation across the whole character-tuple family," and per-frequency
Weil "stops at w <= 21-22" (= our w > sqrt(p) threshold). Frontier depth ~6.7e4.

**Tested the manuscript's proposed closing route Q3 (twist symmetry) -- `b2_Q3_twist.py` -- and it is NOT the
operative mechanism.** Q3 hopes: moment bounds make heavy fibers few (< n) => a heavy z has nontrivial twist
stabilizer (`z_j -> zeta^j z_j`) => quotient-pulled-back => already paid; primitive fibers stay light. Result
at accessible scales: the MAX fiber over PRIMITIVE (trivial-stabilizer) z essentially equals the GLOBAL max
(p=17,n=16,w=2,m=6: primitive-max 31 vs global 32; only the fully-stabilized z=0 is strictly larger), and the
top fibers are almost all primitive, forming FULL primitive twist-orbits at the near-max. So heaviness reaches
the primitive part -- it is NOT confined to stabilized/quotient fibers. Above collision the fibers are already
flat (max/mean ~ 1.1) but flatness is GENERIC (primitive ~ imprimitive), not via Q3 confinement.

CONSEQUENCE: Q3 is a conditional structural step (needs the moment bound Gamma_r first, somewhat circular) and
there is no confinement to lean on at accessible scales. The irreducible content stays the GENERIC signed
cancellation = Gamma_r (r>=3) = the inverse-LO/BSG large-spectrum step on the primitive collision moment. This
is the same crux from the fiber side; the structural descent routes (Q3 twist, char-0 tower) handle only the
periodic/quotient part, confirmed NOT to capture the heavy primitive fibers.

## Engaging LegaSage's #582 C9 razor with the Bernoulli/inverse-LO angle (2026-07-11)

#582 razor (REDUCED, closes C9 if proved): for T=mu_n, m=alpha n, Phi=(p_1,p_2), any fiber F of Boolean
indicator vectors {1_S : Phi(S)=v} on the 2-constraint slice of {0,1}^n has additive energy
E(F)=#{(S1,S2,S3,S4) in F^4 : 1_S1+1_S4 = 1_S2+1_S3}, Delta=E/|F|^3. Prove a large fiber cannot be near-Sidon:
Delta >= f^{-c} (c<1) or (stronger) Delta >= exp(-o(n)) for f >= exp(eta n). The razor's OWN suggested tools are
BSG / Fourier = our inverse-LO angle. Role in C9: per-fiber energy lower bound + a total-energy bound => max-fiber
bound (via W50 Lemma II). Near-Sidon = quadratic energy E ~ 2f^2; the razor needs SUPERquadratic E >= f^{3-c}.

**Probe (`b2_razor_probe.py`), largest mu_n fibers, energy exponent logE/logf** (extends LegaSage's N=14 toys):
  n=16 f=32:  E/f^2=2.00  logE/logf=2.20  (c=0.80)
  n=20 f=90:  E/f^2=2.28  logE/logf=2.18  (c=0.82)
  n=24 f=420: E/f^2=2.52  logE/logf=2.15  (c=0.85)
Largest fibers ARE above Sidon (form (a) holds with c~0.8-0.85), BUT the exponent DRIFTS DOWN toward 2 (c up
toward 1). E/f^2 grows (2.0->2.52) yet the excess exponent log(E/f^2)/log f shrinks (0.20->0.18->0.15). WARNING
SIGN: if the drift continues, the fixed-c razor (form a) fails asymptotically and the largest fibers approach
near-Sidon -- the reduction's feared case. NOT conclusive (3 small-n points; fibers not yet exp-large). NEXT:
Bernoulli/inverse-LO analysis of whether the moment-curve (Vandermonde) structure forces E/f^2 to keep growing
(razor holds) or lets it plateau/grow only sub-polynomially (razor form (a) fails, only form (b) could survive).
