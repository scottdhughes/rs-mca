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

## Status (superseded above for the target; chain 1-6 unchanged)

The L1/b2 prize crux is reduced by an EXACT, verified chain to `(LS)` -- a one-sided SIGNED multilevel
large-sieve / inverse theorem for binomially-weighted cyclic moment maps, spanning the large-subgroup and
sub-`sqrt(p)` regimes over 17 levels. No existing tool provides it; no counterexample is known. This is the
irreducible open theorem for the L1/b2 (max-fiber / entropy-inverse) lane = Route-D frontier node #5
("KB max-fiber signed-e_m inverse, the Fourier side of the closure"). NOT a proof.
