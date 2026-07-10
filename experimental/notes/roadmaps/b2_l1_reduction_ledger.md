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

## Status

The L1/b2 prize crux is reduced by an EXACT, verified chain to `(LS)` -- a one-sided SIGNED multilevel
large-sieve / inverse theorem for binomially-weighted cyclic moment maps, spanning the large-subgroup and
sub-`sqrt(p)` regimes over 17 levels. No existing tool provides it; no counterexample is known. This is the
irreducible open theorem for the L1/b2 (max-fiber / entropy-inverse) lane = Route-D frontier node #5
("KB max-fiber signed-e_m inverse, the Fourier side of the closure"). NOT a proof.
