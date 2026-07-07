# conj:Q / u2c_giant_tnull: a partial-results package (2026-07-07)

Clean statement of what is PROVED for the giant t-null / primitive max-fiber count, the exact
reformulations, and the single remaining open crux. Working log + numerics in
`b2_barrier_beating_synthesis.md`; all statements cross-checked (brute vs DP; two independent
frontier-model derivations; a TheoremSearch paper chase). Coordinates with holmbuar's
`cap25_v13_qfin_rung_audit.md`. Scope: `experimental/`, no claim beyond a partial result.

## The object
Prime `p`, `n = 2^k` with `n | p-1`, `mu_n = ` n-th roots of unity in `F_p^*` (deployed KoalaBear:
`|mu_n| = n = 2^21 = p^0.678`, a LARGE subgroup; `w ~ 67471`; `m ~ n/2 + w`; `mean := C(n,m)/p^w ~ 2^35.7`).
For `S subset mu_n`, `p_j(S) = sum_{a in S} a^j`. Set
    `N = N(n,m,w) = #{ S subset mu_n : |S| = m, p_1(S) = ... = p_w(S) = 0 in F_p }`.
Structured (coset-union) part removed by descent; `N_prim` = primitive part. **Target: `N_prim <= n^3`.**

## PROVED theorems

**T1 (Reformulations).** The following count the same `N` (Newton, `w < p`):
(i) monic degree-`m` divisors of `X^n - 1` over `F_p` with the top `w` non-leading coefficients zero
(a coefficient gap below the lead); (ii) Boolean (`{0,1}`) weight-`m` codewords of the length-`n`
`F_p`-cyclic BCH code with defining zeros `{1,...,w}` (dim `n-w`, min-distance `>= w+1`); (iii)
`m`-subsets of `mu_n` that are exact `F_p`-quadrature for `deg <= w`, `Q(0)=0`.

**T2 (Li-Wan cycle expansion + low-cycle vanishing).** With `pi(c) = sum_{a in mu_n} e_p(sum_{j=1}^w c_j a^j)`,
    `N = sum_{lambda |- m} ((-1)^{m-ell(lambda)}/z_lambda) M_lambda`, `M_lambda = #{x in mu_n^{ell}: sum_i lambda_i x_i^j = 0, j=1..w} = p^{-w} sum_c prod_r pi(rc)^{m_r}`.
And `M_lambda = 0` whenever `ell(lambda) <= w` (Vandermonde in the distinct values forces positive-integer
aggregate weights to vanish mod p; needs `char > m`). Hence `N = sum_{ell(lambda) > w} (...)`: **only
partitions with more than `w` cycles contribute.** (In particular `N = 0` for `m <= w`.)

**T3 (Exact descent).** `N_struct(n,m,w) = 1[2|m] N(n/2, m/2, floor(w/2))`, and for `n = 2^k` the
structured solutions are exactly the `(-1)`-invariant (`S=-S`) ones = the nontrivial-stabilizer ones. So
`N_prim = N(n,m,w) - 1[2|m] N(n/2,m/2,floor(w/2))` counts the free-`mu_n`-orbit (trivial-stabilizer) `S`.

**T4 (Divisibility).** For `n = 2^k`, `n | N_prim`, and `N_prim = n * (#free mu_n-orbits)`. Hence
    **`N_prim <= n^3  <=>  #free orbits <= n^2`.**

**T5 (Odd moment law, uniform in the number of frequencies).** For any exponent set `J` containing the
initial odd block `{1,3,...,2s-1}` and `char > 2s`,
    `J_s(J; mu_n) := #{a,b in mu_n^s : sum a_i^j = sum b_i^j, all j in J} <= (2s-1)!! n^s`,
uniformly in `|J|`. Equivalently `E_c |pi_J(c)|^{2s} <= (2s-1)!! n^s`. (Proof: substitute `x_{s+i} = -b_i`
using `-1 in mu_n`; odd power sums of the `2s` values vanish, so `prod(T - x_i)` is EVEN, roots pair
`{h,-h}`; `(2s-1)!!` pairings times `n^s`.) Matches numerics `1, 2.96, 15.17, 101.87 ~ 1,3,15,105`.
False for arbitrary sparse `J` (`J={1}` gives additive energy `n^{4-1/gamma}`) -- the initial-block
hypothesis is essential.

**T6 (PTE rigidity).** With the additive energy `E = sum_v nu(v)^2 = sum_{d>=0} C(n-2d,m-d) E_d`,
`E_d = #{disjoint A,B subset mu_n, |A|=|B|=d, p_j(A)=p_j(B), j=1..w}`, one has `E_d = 0 for 1 <= d <= w`
(same Newton argument as T2). So the energy `E = C(n,m) + sum_{d>w} C(n-2d,m-d) E_d`.
> **[Machine-checked, Lean 4 / Mathlib]** The algebraic engine of T6 (and of T2's low-cycle vanishing) is
> *power-sum rigidity*: over any field where `1,...,d` are invertible (char `0` or `> d`; deployed `d <= w << p`),
> two size-`d` multisets with equal power sums `p_1,...,p_d` are equal. Formalized zero-`sorry`, axioms
> `[propext, Classical.choice, Quot.sound]` only, as `PowersumRigidity.powersum_rigidity` in
> `experimental/lean/powersum_rigidity/` (Lean `v4.31.0`, Mathlib `9a9483a`). Independently rebuilt + axiom-checked.
> This discharges `E_d = 0` for `1 <= d <= w`: equal `p_1..p_d` force `A = B` as multisets, but `A,B` disjoint
> and nonempty is a contradiction. (Newton's identities `mul_esymm_eq_sum` + Vieta `prod_X_sub_X_eq_sum_esymm`.)

**T7 (Concentration, not rigidity -- p-sensitivity).** `N_prim <= n^3` is NOT combinatorial: for small `p`
at the same `(n,m,w)`, `N_prim >> n^3`; empirically `N_prim/mean` has median exactly `1`. The bound holds
only because in the deployed window `mean = C(n,m)/p^w <= n^3`. Any proof must be `p`-sensitive.

## The single OPEN crux
Reduce to the additive energy (T6). Two pieces remain:
- **(E-a) Excess-energy bound:** `|E - C(n,m)^2/p^w| <= n^{O(1)} p^w`, i.e. bound the `d>w` tail
  `sum_{d>w} C(n-2d,m-d)(E_d - E_d^{rand})`. The first tail term `E_{w+1}` is itself a max-fiber/value-set
  count (a degree-`(w+1)` locator `g_B` on `mu_n` with a full-size fiber `g_B(x) = -c`) -- self-similar to
  conj:Q. This is a high-degree equidistribution over `mu_n`, UNIFORM in the number of conditions `w` --
  confirmed genuinely NEW (not covered by VMVT [fixed degree], Bourgain-Chang [bounded #monomials], or
  Cheong-Matchett Wood-Zaman arXiv:1210.0456 [fixed #conditions, d->inf]).
- **(E-b) Fiber transfer:** `E >= nu(0)^2 = N^2`, so an energy bound alone gives only `N <= mean * p^{w/2}`
  (the sqrt(p^w) barrier). The `mu_n`-rotation fixes `v=0`, so `nu(0)=N` hoards free orbits; must show `v=0`
  is not anomalously heavy beyond the descent-symmetric part.

## Honest calibration
Morally certain (both models + numerics): `N_prim = (1+o(1)) mean`, fluctuation `~ sqrt(mean) ~ 2^18 << n^3
= 2^63` (~`2^41` slack). The difficulty is entirely a rigorous high-degree joint-equidistribution input
over `mu_n`, uniform in `w`; every classical tool caps out at a fixed number of conditions. Candidate
routes: Stepanov on the value-set/divisor form; large-sieve/dual over the BCH code; a p-adic/Ax-Katz
congruence for `N mod (powers of p)`; efficient-congruencing adapted to `mu_n`. Nearest published leads:
Cheong-Matchett Wood-Zaman 1210.0456, Dae San Kim 0807.4671, Koh-Pham-Shen-Vinh 1803.03351.

## Update (2026-07-07): the crux REDUCES to Littlewood-Offord slice-mixing (n-loss suffices)

External-model contribution, all load-bearing claims RE-VERIFIED here:
- **T8 (primitive defect, PROVED+verified):** if S is primitive (not (-1)-invariant) then `|S cap -S| <= m-w-1`,
  i.e. S breaks `s >= w+1` opposite-pairs. Proof: `Delta_eta(X)=Q_S(X)-eta^{-m}Q_S(eta X)` has the top w+1
  coeffs zero (the gap), so deg <= m-w-1; it vanishes on `S cap eta^{-1}S`. (eta=-1.) Verified: all 32
  primitive sols at (17,16,2,10) have s>=3.
- **T9 (exact ternary reduction, PROVED):** via a square-root section `b_v^2=v` on `mu_{n/2}`, each S <->
  `(y_v,h_v) in {-1,0,1}, y_v^2+h_v^2=1`, with `sum y_v=delta`, `sum y_v v^r=0 (r<=floor(w/2))`,
  `sum h_v b_v v^r=0 (r<=ceil(w/2)-1)`; `N_prim = #{h != 0}`. Singletons U (odd constraints p_j(U)=0, j odd
  <=w) x double-pairs D (even constraints `2p_r(D)=-p_r(U^2)`).
- **T10 (dimension bound, PROVED+verified TIGHT):** `M_lambda <= w! * n^{ell(lambda)-w}` (Bezout: the last
  ell-w vars free, first w have a 0-dim'l fiber by the Vandermonde-at-infinity argument). Right dimension,
  but the `w!` misses the `(n/p)^w` density factor -- fatal alone.
- **KEY REDUCTION (verified identity `sum_s 2^s C(N0,s)C(N0-s,(N0-s+delta)/2) = C(n,m)`):** IF the two
  half-slice estimates hold -- `A_s <= L_o(s) 2^s C(N0,s)/p^{q_o}` (odd/singleton) and `B(U) <= L_e(s)
  C(N0-s,..)/p^{q_e}` (even/double, uniform in the deleted W=U^2) -- with product loss `L = max L_o L_e`,
  then `N_prim <= L * C(n,m)/p^w = L * mean`. Deployed: `mean ~ 2^35.7`, so **`L <= n=2^21` gives
  `N_prim <= 2^56.7 < 2^63 = n^3`** (even `L <= n^{1.3}` closes it).

**The crux is now: two LITTLEWOOD-OFFORD / anticoncentration slice-mixing estimates for the moment curve
over `mu_{n/2}`, with only an n-loss.** A developed area (Halasz, Tao-Vu, Nguyen-Vu inverse LO); much
sharper than the marginal pi(c) moments (which give only (ell-1)!! n^{ell/2}, too large after 1/z_lambda).
This is the most tractable form of the crux to date.

## Correction + clarification (2026-07-07, d>w tail attack, both claims VERIFIED)

Third model contribution (independent). IMPORTANT correction: the additive-energy route (Reduction E)
is PROVABLY INSUFFICIENT, and the crux is now crystal clear.
- **T11 (Prop 1, PROVED+verified): exact energy->fiber transfer + a sqrt(M) CEILING.** Removing the main
  term BEFORE Cauchy-Schwarz: `|N - mean| <= sqrt(E - E0_rand)`, `E >= E0_rand = M^2/p^w`, and `E >= M`
  (integer fibers, nu^2>=nu). Verified (n=16,w=2,m=10: |N-mean|=4.29 <= sqrt(E-E0)=28.56). **But this
  CANNOT reach n^3:** the diagonal energy term is M = C(n,m), so `sqrt(E-E0) >~ sqrt(M)` which at deployed
  scale is astronomically >> n^3. Any E-a bound `E-E0 <= n^{O(1)} p^w` yields only `N <= mean * p^{w/2}` --
  the sqrt(p^w) barrier is STRUCTURAL (the Cauchy-Schwarz sqrt(#frequencies)). **So E-a and E-b do NOT
  combine; the 2nd moment / additive energy is dead** (corrects the earlier "positive route" framing).
- **Consequence — the LO reduction (T8-T10) is the SURVIVING route** precisely because it bounds the COUNTS
  A_s, B(U) POINTWISE (Littlewood-Offord anticoncentration), NOT via energy -- so it sidesteps the sqrt(M)
  ceiling. If the pointwise LO bounds hold with product loss L <= n, then `N_prim <= L*mean ~ 2^56.7 < n^3`,
  BELOW the energy ceiling. A_s, B(U) are themselves many-condition subset counts (the same crux, cleaner).
- **The one genuine missing ingredient (both routes reduce to it):** direct anticoncentration / signed
  cancellation, NOT the second moment. Signed form: `|sum_{t != 0} e_m({e_p(f_t(a))}_{a in mu_n})| <=
  n^{O(1)} p^w`. No |A(t)| bound helps (typical |A(t)| ~ sqrt(M)); Weil per-frequency is w*sqrt(p) > n.
- **T12 (Theorem 2, PROVED+verified): E_{w+1} = 2*#{U subset mu_n, |U|=2(w+1) : P_U + gamma is a perfect
  square for some gamma != 0}** (polynomial-Pell: `Qhat^2 - P_U = gamma`). Verified (n=12,w=2: E_3=168=2*84).
  Unconditional `E_{w+1} <= 30*C(n,w+1)` (each deg-(w+1) locator has <= n/(w+1)=31 full fibers). Off the
  critical path (energy tail dead) but a clean self-similar minimal-value-set object.
- **T13 (PROVED): N = # weight-m BINARY codewords of a generalized Reed-Solomon [n, n-w, w+1] MDS code**
  (H = [a^j], Vandermonde minors nonzero); MDS distance w+1, Newton sharpens to E_d=0 for d<=w.

**NET (3 models cross-checked):** energy route DEAD (T11); surviving route = pointwise Littlewood-Offord
anticoncentration on A_s,B(U) with n-loss (T8-T10), equivalently signed cancellation of the e_m frequency
sum. Both = anticoncentration/equidistribution of subset counts on the moment curve of the subgroup,
uniform in #conditions = a clean generalization of Pach arXiv:2505.12496 (full-group single-sum case).
Morally certain (~2^41 slack); genuinely open. The crux is now a single, sharply-stated anticoncentration.

## TheoremSearch exploration + Rodgers chase (2026-07-07)

Explored the tool from the OUTPUT side (searching the objects our proofs produced). Leads found
(flat /search + /graph/paper work; pagerank/embedding error server-side):
- **arXiv:2304.13801** (Prop 3.4): disjoint subsets A,B of a multiplicative subgroup (d|q-1) with equal
  sums -- closest published analogue of E_d (PTE over a subgroup).
- **arXiv:1108.1852** minimal value sets over F_q, + Carlitz-Lewis-Mills-Wan -- for bounding E_{w+1}
  (#{deg-(w+1) maps on mu_n with two full fibers}).
- **arXiv:1906.08818 "Pell surfaces" / 0801.3011** -- polynomial Pell x^2-gy^2=1 over F_q[x] = our T12
  perfect-square/polynomial-Pell object.
- **arXiv:2504.21816 (2025) / 1812.00901** -- RS/MDS minimum-weight codeword enumeration = T13.
- **arXiv:1609.02967 (Rodgers) Thm 7.1 / Cor 7.2** -- THE key hit: symmetric-group-character x Dirichlet-
  character sums `sum_f X^{lambda'}(f) chi(f)` cancel with sqrt-savings.

**Rodgers chase verdict: does NOT transfer (fixed n,h, q->inf, O_{n,m} constants -- same fixed-degree/large-q
wall), BUT the mechanism is the key structural insight.** Rodgers gets the symmetric-function-character-sum
cancellation via KATZ EQUIDISTRIBUTION of the Frobenii Theta_chi in PU(M-2) -- his family is the
MULTIPLICATIVE characters chi mod T^m, which has BIG monodromy. Our T(c)=e_m(...) is the same
symmetric-function object, but our dual family is the ADDITIVE frequencies c, whose monodromy is ABELIAN
(blind) -- exactly why additive routes stall. **NEW ROUTE (2): reformulate the fiber count via a
MULTIPLICATIVE-character / big-monodromy family so a Katz/Rodgers-type equidistribution supplies the
cancellation the abelian additive family cannot.** Round-(a) model attack now running on Routes 1 (LO n-loss),
2 (multiplicative big-monodromy), 3 (transplant Pach Lemma 2.3), 4 (minimal value sets for E_{w+1}).

## Round (a) — the crux distilled to ONE estimate; Route 2 killed (2026-07-07, both claims verified)

Focused model attack. Two rigorous negatives + one clean distillation:
- **Result A (PROVED+verified): Route 2 (multiplicative reformulation) is DEAD.** N = p^{-w} sum_{chi in U_1-hat}
  e_m({chi(1-aX)}), U_1 = 1+X F_p[X]/(X^{w+1}). BUT for w<p, U_1 is elementary abelian ((1+cX)^p=1 mod
  X^{w+1}, verified p=7..17) and log-linearizes: chi_t(1-aX)=e_p(f_c(a)) with c_j=-t_j/j. So the
  multiplicative family IS the additive family reindexed -- same abelian rank-1 Artin-Schreier sheaves,
  ZERO extra cancellation. The structure turns non-abelian only when w>=p (verified fails at w=9,p=7) --
  the small-p regime where the concentration is FALSE. So the Rodgers/Katz big-monodromy hope is a mirage
  here. Route 2 closed.
- **Result B (PROVED+verified): no purely combinatorial method reaches n^3.** N <= Johnson/anticode bound
  A(n,w+1,m) <= C(n,m-e+1)/C(m,e-1), e=ceil((w+1)/2) (verified N<=Johnson on toys). Deployed: Johnson saves
  only ~3.15 bits/constraint (~10%); reaching n^3 needs ~31 bits/constraint. A(n,w+1,m) is p-INDEPENDENT
  while mean & target are not, and by Gilbert-Varshamov A >= 2^{1.66e6} >>> n^3. **So NO code/packing/
  design/LP argument can EVER give n^3 -- the savings MUST be F_p equidistribution (signed cancellation).**
- **Result C (PROVED reduction): all routes reduce to ONE object -- large values of the subgroup sum.**
  Both half-slices (Route 1), the chi-sum (Route 2=additive), and Pach's Li-Wan terms (Route 3) all reduce
  to controlling `pi(c) = sum_{a in mu_n} e_p(f_c(a))`. Pach's Lemma 2.3 fails because it needs the FULL group
  (nontrivial char sums to 0); over mu_n (density p^-0.32) pi(c) != 0 for c != 0 -- that missing vanishing
  IS the wall.
- **Result D (the distilled crux) -- Hypothesis SP:** for s ~ n/4, `sum_{c != 0} |pi_odd(c)|^s <= n^{O(1)} n^s`
  (a large-values / thin-spectrum bound). SP => N_prim <= n^{O(1)} * mean; need only L <= 2^{27.3}, poly-n
  suffices. **The single missing ingredient: a poly-loss high-moment (s~n/4) large-values bound, at a SINGLE
  fixed prime p, for the subgroup sum with GROWING degree w ~ sqrt(p).** Every tool fails at one hinge (Weil:
  degree growing; BGK: fixed degree; Katz/Rodgers: bounded conductor q->inf; Li-Wan/Pach: full group).
  Believed OPEN. Concrete next step: prove SP for the REDUCED spectrum after removing the 2-power/square
  exponent terms (the n=2^k defect that N_prim's subtraction targets).

**Two corrections flagged (verify/patch):** (1) the LO reduction's per-s bound `A_s <= L_o 2^s C(n/2,s)/p^{w/2}`
is NOT uniform in s (false for s <~ 1.47 w_o where the random value < 1); holds only in the dominant band
s ~ n/4 -- a gap in the T8-T10 reduction to patch (patchable). (2) The operative multiplicative slack is
`n^3/mean = 2^{27.3}` (need L <= 2^27.3), NOT the earlier "~2^41"; correct the calibration.

**NET (maximal distillation):** every alternative route provably reduces to, or is dead against, ONE open
estimate -- Hypothesis SP, a large-values bound for exponential sums over the LARGE subgroup mu_n with
sqrt(q)-degree phase at fixed p. This is the sharp, isolated, currently-open crux. The attack: SP on the
2-power-reduced spectrum.

## Round (b) -- SP anatomized: moments are DEAD, the crux is the near-n large spectrum (2026-07-07)

Self-derived (not delegated), all load-bearing claims exact-checked or numerically verified here.
Structural facts first (both PROVED):
- **pi_odd is a Fourier transform.** With the odd moment curve `Phi: mu_n -> F_p^{w_odd}, a |-> (a^j)_{j odd<=w}`,
  `pi_odd(c) = sum_{a in mu_n} e_p(<c,Phi(a)>) = mu_hat(c)`, `mu = sum_a delta_{Phi(a)}`. So SP is an
  ANTICONCENTRATION statement on the large Fourier spectrum of the subgroup pushed onto the moment curve.
- **The proved moment law T5 IS the 2s-th spectral moment.** `sum_c |pi_odd(c)|^{2s} = p^{w_odd} J_s(J_odd;mu_n)
  <= p^{w_odd}(2s-1)!! n^s` exactly (Phi injective via the j=1 coordinate => Parseval `sum_c|pi|^2 = p^{w_odd} n`).

**T14 (PROVED, exact-exponent, `b2_metaprompt` arithmetic re-run): the moment method CANNOT prove SP.**
By Holder, `sum_{c!=0}|pi_odd|^s <= (sum_c|pi|^{2s})^{1/2}(#c)^{1/2} <= p^{w_odd}((2s-1)!!)^{1/2} n^{s/2}`.
At deployed `(p~2^31, n=2^21, w_odd~33735, s=n/4)` this bound is `2^{11,415,495}` while the SP target
`n^3 n^s = 2^{11,010,111}` -- an **OVERSHOOT of `2^{405,384} = n^{~19,300}`.** The population inflation
`p^{w_odd}=2^{1,045,785}` is only partly cancelled by the `(2s/en)^{s/2}` decay `2^{-640,338}`. So SP is
STRICTLY stronger than the sharp moment law (which we own): moments control the AVERAGE tail (sub-Gaussian,
variance n, over the full `p^{w_odd}` population) but SP needs the near-n tail to be `n^{O(1)}` -- an
INVERSE/structural bound on the large spectrum, not an average. **This is exactly parallel to T11 (energy
dead): the two "cheap" analytic methods (2nd moment/energy AND all higher moments) are both provably
insufficient; the savings must come from the algebraic STRUCTURE of the large-value c.** (Script:
`b2_sp_large_spectrum.py`; T14 is exponent arithmetic, regime-independent.)

**The sharpened crux -- minimal-value-set dictionary (PROVED direction + numerics).** `|pi_odd(c)| >= (1-delta)n`
forces `f_c` (degree `<= w`) to have a SMALL/CONCENTRATED value set on `mu_n` (most a map into a tiny arc).
So the near-n large spectrum = degree-`<=w` MINIMAL-VALUE-SET polynomials on the subgroup `mu_n` -- the
Carlitz-Lewis-Mills-Wan regime (cf. 1108.1852, Dae San Kim), now over a SUBGROUP with GROWING degree w.
SP holds iff this near-n set is a bounded union of `O(n^{O(1)})` algebraic families each of size `~p=poly(n)`.

**Numerics (`b2_sp_large_spectrum.py`, `b2_sp_structured_vs_random.py`) -- SP SUPPORTED, with regime caveat:**
- n/2-level spectrum is NOT thin: `#{c!=0:|pi_odd|>=n/2} ~ 0.045 p^{w_odd}` (positive fraction) -- so SP lives
  entirely on the s~n/4 moment being dominated by the NEAR-n tail, not the n/2 tail. (n=16,w_odd=2 exact.)
- **Random c concentrate BELOW n and further as n grows:** `rand_max/n = 0.9, 0.72, 0.5` and
  `rand_99.9/n = 0.76, 0.56, 0.40` for `n=16,32,64` (w_odd=4,8,16). The generic near-n spectrum THINS with n.
- **Structured families reach ~n ONLY in the (non-representative) near-FULL block** (`w_odd ~ n/2`): the spike
  `c=t*(1,..,1)` hits `0.8-0.98 n` for `n<=64, w_odd=n/2`. **SUPERSEDED by round (c): this is a FULL-BLOCK
  ARTIFACT.** In the regime-representative TRUNCATED block (`w_odd/(n/2) ~ 0.03` = deployed `w/n`), the spike
  is NOT near n -- it drops to `0.13-0.20 n ~ sqrt(p)` (round c). The fiber bound (deg `f_c <= w`, each value
  hit `<= w` times) forbids single-value domination when `w << n`, so the spike cannot concentrate. Read
  round (b)'s near-n picture through round (c)'s correction: at deployed truncation ALL c (random + spike)
  sit at `~sqrt(p) << n`.
- CAVEAT (regime-first): round-(b) numerics used near-full blocks (NOT representative). Round (c) fixes the
  regime (`w_odd/(n/2) ~ 0.03`); see there for the deployed-representative behavior.

**Descent link (OPEN, NOT yet established -- flagged honestly, do not build on it).** Tempting: the dominant
spike concentrates `f_c` on the 2-torsion pair `{1,-1}` (`g(a)=sum_{j odd<=w}a^j` is large only when `a^2~1`),
and `N_prim = N - 1[2|m]N(n/2,..)` subtracts the `S=-S` part (T3). BUT these are on OPPOSITE sides of the
Li-Wan duality -- `{1,-1}` is a single coset on the FREQUENCY/`c` side, while `S=-S` is a pairing condition on
the SUBSET side -- so the connection is NOT tight and may be a coincidence of small toys. Status: an
unverified heuristic, not a lead to lean on. (To settle it one would need the spike's contribution traced
through the full plethystic sum `N = sum_lambda (+-1/z_lambda) p^{-w} sum_c prod_r pi(rc)^{m_r}`, not done.)

**The well-posed concrete next step (ii).** Independent of the descent heuristic, T14 + the dictionary reduce
SP to a clean, literature-connected COUNTING problem:
    **bound `#{ c in F_p^{w_odd}, c != 0 : f_c has value set of size <= n/K on mu_n }` by `n^{O(1)} K^{O(1)}`,**
i.e. count degree-`<=w` polynomials with a `K`-fold-concentrated value distribution on the subgroup `mu_n`.
This is Carlitz-Lewis-Mills-Wan minimal-value-set theory (over `F_q`: minimal value set forces the poly into a
thin algebraic family) transplanted to a SUBGROUP and to GROWING degree `w`. Tools that could bite (unlike the
dead moment/energy methods): Stepanov's method on `{x in mu_n : f_c(x) = v}`; the value-set structure theorems
of CLMW/1108.1852; Weil restriction of the fiber curves. This is the sharpest OPEN form of the crux.

**NET round (b):** SP's two cheap analytic routes -- 2nd moment/energy (T11) AND all higher moments (T14) --
are BOTH provably dead (overshoot `n^{~19,300}`). The surviving route is INVERSE/structural: the near-n large
spectrum is (numerically) confined to few structured minimal-value-set families while random c fall away
(`rand_max/n: 0.9->0.5` as `n:16->64`), so SP is supported and reduces to the CLMW-type subgroup value-set
count (ii). The crux is now a concrete algebraic-geometry counting problem over a subgroup, not an analytic
estimate in the void. (Regime caveat: numerics `n<=64`; deployed `n=2^21`.)

## Round (c) -- SP REDUCES TO A UNIFORM SUP BOUND (crude count); the min-value-set concern EVAPORATES (2026-07-07)

The single cleanest advance so far. Self-derived + verified (`b2_sp_sup_reduction.py`).

**T15 (PROVED reduction, exact-exponent): SP follows from a UNIFORM SUP bound.** Let `M = max_{c!=0}
|pi_odd(c)|`. Trivially `sum_{c!=0}|pi_odd(c)|^s <= (#c) M^s <= p^{w_odd} M^s`. This beats the SP target
`n^{O(1)} n^s = p^{gamma s + O(1)}` as soon as
    **`log_p M <= gamma - w_odd/s =: theta*`**,  deployed `theta* = 0.678 - 0.0643 = 0.6137`, i.e.
    **SP  <==  `M = max_{c!=0}|pi_odd(c)| <= p^{0.6137} = n^{0.905}`.**
So the high-moment large-values estimate collapses to a SINGLE incomplete-character-sum SUP bound -- a far
more standard object. (With `M ~ sqrt(p)` the crude `L = sum_{c!=0}|pi_odd|^s / n^s` is `~ p^{-0.11 s} << 1`,
astronomically inside the operative slack `L <= 2^{27.3}` -- the reduction is not delicate.)

**The min-value-set worry of round (b) EVAPORATES -- and here's WHY (structural).** A value-set reduction
for `f_c` on `mu_n` would need `f_c` to factor through a power map `x |-> x^d` with `d | n` (so `f_c` is
constant on cosets of `mu_{n/d}`). But `n = 2^k`, so a nontrivial `d | n` is EVEN, forcing EVEN exponents --
while `pi_odd` is supported on ODD frequencies. Odd `d | 2^k` means `d=1` (no reduction). **So no
odd-supported `f_c` has a minimal value set: the oddness (inherited from the primitive/initial-block
structure, T5) STRUCTURALLY BLOCKS the only mechanism that could push `M` up to `sqrt(w n)`.** Hence `M ~
sqrt(p)`, not `sqrt(w n)`.

**Numerics (`b2_sp_sup_reduction.py`, adversarial coordinate ascent from spike/geometric/random, REGIME-
REPRESENTATIVE `w_odd/(n/2) ~ 0.03`):** the true `M` tracks `sqrt(p)`:
    `M/sqrt(p) in [0.9, 1.9]` across `n=512,1024,2048` (`p` up to 41 K); `M/n` SHRINKS `0.21 -> 0.15 -> 0.10`.
    `M/sqrt(w n)` DECREASES (`1.17 -> 0.84 -> 0.58`) -- confirming `M ~ sqrt(p)` (not `sqrt(w n)`).
Threshold headroom is a factor `p^{theta*-1/2} = n^{0.168} = 2^{3.5} ~ 11.5` in the CONSTANT `C` (`M <= C
sqrt(p)`); the observed `C ~ 1-2`. Comfortable.

**Honest status of the remaining gap.** The sup bound `M <= n^{0.905}` is still NOT Weil-accessible: Weil per
multiplicative character gives `|pi_odd| <= (1/m') * m' * w sqrt(p) = w sqrt(p) = n^{1.501}` -- WORSE than the
trivial `n`. So a proof must beat trivial by `n^{0.1}` using the subgroup structure (small index `m'=(p-1)/n
=127`), NOT generic Weil. Candidate: the 2nd-moment-over-characters identity `sum_{psi triv on mu_n}|S(psi,c)|^2
= m' sum_{x/y in mu_n} e_p(f_c(x)-f_c(y))` (a coset-restricted autocorrelation of `f_c`), which may give `M <=
sqrt(m') sqrt(p) * (deg factor)` if the diagonal dominates -- OPEN. This is the one clean estimate to prove now.

**NET (rounds a-c):** every route reduces to ONE object, and that object is now the SHARPEST/most-standard it
has been: a uniform sup bound `max_{c!=0}|pi_odd(c)| <= n^{0.905}` for an incomplete character sum over the
large subgroup `mu_n` with a degree-`w` ODD phase -- and (i) the crude count then gives SP with room to spare
(T15), (ii) the odd-support provably kills the minimal-value-set inflation, (iii) numerics put the truth at
`~sqrt(p) = n^{0.74}`, comfortably inside. The crux is a single sub-trivial character-sum bound; Weil is the
wrong tool (degree growing), the subgroup small-index structure is the right one. Still OPEN, now maximally
concrete.

## Round (d) -- conj:Q collapses to ONE 4th-moment estimate `S2off <= O(np)` (2026-07-07)

The sup bound (round c) is itself reduced -- by a chain of PROVED identities -- to a single clean 4th-moment.
All steps verified (`b2_sp_2ndmoment_route.py`).

**T16 (PROVED reduction chain). Define** `T_a(c) = sum_{y in F_p^*} e_p(f_c(ay) - f_c(y))` for `a in mu_n`
(a COMPLETE degree-`<=w` additive character sum; `T_1 = p-1`). Then:
1. **Coset-sum identity (PROVED):** `|pi_odd(c)|^2 <= sig2(c) := sum_{a in mu_n} T_a(c) = sum_{i=1}^{m'}|Pi_i|^2`,
   where `Pi_i = sum_{z in coset_i} e_p(f_c(z))` are the sums of `f_c`'s phase over the `m'=(p-1)/n` cosets of
   `mu_n` in `F_p^*` (`Pi_1 = pi_odd(c)`). [`sum_a T_a = sum_i|Pi_i|^2 >= 0`, and `|Pi_1|^2 <= sum_i|Pi_i|^2`.]
2. **a=1 split + Cauchy-Schwarz (PROVED):** `sig2 = (p-1) + sum_{a != 1} T_a <= (p-1) + sqrt((n-1) * S2off)`,
   where **`S2off := sum_{a in mu_n, a != 1} |T_a(c)|^2`** is the 4th moment with the trivial diagonal removed.
3. **THE ONE OPEN ESTIMATE:** `S2off <= K n p` with `K = O(1)`. Then `M^2 = |pi_odd|^2 <= sig2 <= p + n sqrt(Kp)`,
   so `M <= n^{0.87} < n^{0.905}` (T15 threshold) `=> SP => N_prim <= n^{O(1)} mean <= n^3`. **conj:Q DONE.**

**Numerics (adversarial-max c, coordinate ascent, regime-representative `w_odd/(n/2)~0.03`):**
    `S2off/(np) = 1.0 - 1.2` across `n=512,1024,2048` (K ~ 1); the CS-implied PROVABLE sup bound
    `sqrt((p-1)+sqrt((n-1)S2off))` is `n^{0.88}` at n=512, **improving to `n^{0.81}` at n=2048** -- under the
    `n^{0.905}` target and DECREASING toward `sqrt(p)`. Median `|T_a| ~ sqrt(p)`; the only large `T_a` is the
    trivial `a=1` term. The Weil `w`-factor does NOT materialize off-diagonal.

**Status of `S2off <= O(np)` (the sole remaining gap).** NOT Weil-provable: per-term Weil `|T_a|^2 <= (w-1)^2 p`
gives `S2off <= n w^2 p` -- overshoot `w^2 = 2^{33}`. So it needs CANCELLATION/averaging over `a in mu_n`. Its
structure is a genuine 4th moment: `sum_a |T_a|^2 = sum_{y,y'} e_p(f_c(y')-f_c(y)) sum_{a in mu_n}
e_p(f_c(ay)-f_c(ay'))`; the `y=y'` diagonal contributes exactly `np`, and `S2off <= O(np)` asserts the
off-diagonal (`y' != y`) is `O(np)` too -- a square-root-cancellation statement for a subgroup-averaged
additive-energy sum. This is the clean self-contained sub-lemma to (a) hand a focused model round, (b) gamble
to Aristotle, (c) attempt directly (Bombieri/Weil for the inner subgroup curve sum + summation by parts over
`y,y'`). It is the LAST domino.

**NET (rounds a-d): the entire conj:Q reduces, by PROVED steps, to `S2off = sum_{a in mu_n, a!=1}
|sum_{y in F_p^*} e_p(f_c(ay)-f_c(y))|^2 <= O(np)`** -- a single, clean, uniform-in-`c` 4th-moment
(subgroup-averaged additive energy) estimate, numerically `~np` (constant `~1`). Every other route is dead
(energy T11, moments T14) or reduces here. This is the sharpest and most self-contained the crux has ever been.
