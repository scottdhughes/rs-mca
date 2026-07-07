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

## Round (d) -- 4th-moment reduction `S2off <= O(np)` [RETRACTED as a proof route, see round (e)] (2026-07-07)

> **RETRACTION (round e, adversarial model round + independently re-verified `b2_sp_resonance_check.py`):**
> the target `S2off <= O(np)` with an ABSOLUTE constant is **FALSE**, and the route is fatally LOSSY.
> Resonant monomials `c = e_{j0}` (`f_c = x^{j0}`, `j0` odd) give `S2off = (d-1) n p (1+o(1))`, `d = gcd(j0, p-1)`
> (verified: `x^15 -> 14.15 np`, `x^21 -> 21 np`, `x^31 -> 25.3 np`, matching `d-1`). At DEPLOYED params
> `p-1 = 2^24 * 127`, `n = 2^21`, so `m' = 1016 = 2^3 * 127`, `d_max = 127`, and `S2off ~ 126 np`. Propagating
> the SHARP `S2off` through the Cauchy-Schwarz step gives only `M = |pi_odd| <= sqrt(p + n sqrt(127 p)) =
> n^{0.952} > n^{0.905}` -- FAILS the T15 threshold. The Cauchy-Schwarz `sig2 = sum_i |Pi_i|^2` step loses a
> factor `sqrt(m')` exactly at resonances (all `|Pi_i|` equal). My round-(d) "numerics `S2off/np ~ 1`" was a
> SAMPLING MISS: coordinate ascent on DENSE `c` never finds the isolated SPARSE optimum `x^{j0}` (same failure
> mode as the earlier sup-form overclaims). **Round (d) is a documented dead-end; the reduction identities
> below are correct, but the 2nd-moment/S2off proxy CANNOT prove the sup bound.** T15 (round c) is UNAFFECTED
> and still LIVE -- see round (e). (Also: the stated `J(y,y')` had a spurious prefactor; correct is
> `J(y,y') = pi(c'')`, `c''_j = c_j(y^j - y'^j)`, no `e_p(...)` factor. Non-load-bearing.)

The sup bound (round c) is here reduced -- by a chain of PROVED identities -- to a single 4th-moment. All
identities verified (`b2_sp_2ndmoment_route.py`); but the resulting estimate is false/lossy (see retraction).

**T16 (PROVED reduction chain). Define** `T_a(c) = sum_{y in F_p^*} e_p(f_c(ay) - f_c(y))` for `a in mu_n`
(a COMPLETE degree-`<=w` additive character sum; `T_1 = p-1`). Then:
1. **Coset-sum identity (PROVED):** `|pi_odd(c)|^2 <= sig2(c) := sum_{a in mu_n} T_a(c) = sum_{i=1}^{m'}|Pi_i|^2`,
   where `Pi_i = sum_{z in coset_i} e_p(f_c(z))` are the sums of `f_c`'s phase over the `m'=(p-1)/n` cosets of
   `mu_n` in `F_p^*` (`Pi_1 = pi_odd(c)`). [`sum_a T_a = sum_i|Pi_i|^2 >= 0`, and `|Pi_1|^2 <= sum_i|Pi_i|^2`.]
2. **a=1 split + Cauchy-Schwarz (PROVED):** `sig2 = (p-1) + sum_{a != 1} T_a <= (p-1) + sqrt((n-1) * S2off)`,
   where **`S2off := sum_{a in mu_n, a != 1} |T_a(c)|^2`** is the 4th moment with the trivial diagonal removed.
3. **[FALSE -- see retraction] The proposed estimate:** `S2off <= K n p` with `K = O(1)`. Would give `M^2 =
   |pi_odd|^2 <= sig2 <= p + n sqrt(Kp)`, `M <= n^{0.87}`. But `K` is NOT `O(1)` (`~d_max=127` deployed), so the
   sharp version yields only `M <= n^{0.952}` -- insufficient. The route is dead; identities 1-2 remain correct.

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

**NET (round d, CORRECTED by round e):** the 2nd-moment/`S2off` route is DEAD -- it loses `sqrt(m')` at
resonant monomials and cannot prove the sup bound (`S2off <= O(np)` is false; sharp `S2off ~ 126 np` deployed
gives only `M <= n^{0.952}`). The LIVE reduction remains T15 (round c): conj:Q `<== max_{c!=0}|pi_odd(c)| <=
n^{0.905}`, which must be proved DIRECTLY (resonance-stable), not via the S2off proxy. See round (e).

## Round (e) -- adversarial correction: back to the DIRECT sup bound, via sparse-subgroup sums (2026-07-07)

A focused model round (self-contained, abstracted) adversarially broke round (d) and re-centered the crux.
All its claims INDEPENDENTLY re-verified here (`b2_sp_resonance_check.py`).

**What broke (verified):** `S2off` is inflated by resonant monomials to `(d-1)np`, `d = gcd(j0,p-1)`, so the
Cauchy-Schwarz route through `sig2 = sum_i|Pi_i|^2` is lossy by `sqrt(m')`. Deployed `m'=1016`, odd part `127`,
so the route caps at `M <= n^{0.952}` -- above the `n^{0.905}` needed. DEAD.

**What SURVIVES and is the real target -- T15 (round c), reaffirmed:**
    **conj:Q  <==  `M := max_{c != 0} |pi_odd(c)| = max_{c} |sum_{a in mu_n} e_p(f_c(a))| <= n^{0.905}`.**
This is RESONANCE-STABLE: at the resonant `c = e_{j0}`, `a -> a^{j0}` PERMUTES `mu_n` (`j0` odd, `gcd(j0,2^k)=1`),
so `pi_odd(e_{j0}) = sum_{b in mu_n} e_p(b)` = a fixed subgroup Gauss period, `|pi_odd| <= ~sqrt(p) << n^{0.905}`.
Verified: at every resonant monomial `|pi_odd|/sqrt(p) <= 0.23` and `|pi_odd|/n^{0.905} <= 0.34`. So the sup
bound holds with margin (`~sqrt(p) = n^{0.74}`, headroom `~n^{0.16}`), resonances included -- only the S2off
PROXY was inflated.

**The correct tool (model round + concurring): a SPARSE-POLYNOMIAL / LARGE-SUBGROUP exponential-sum bound.**
`pi_odd(c) = sum_{a in mu_n} e_p(f_c(a))`, `f_c` is `w_odd`-SPARSE (only `w_odd` monomials, odd exponents) of
degree `<= w ~ sqrt(p)`, summed over a subgroup `mu_n` of size `n > sqrt(p)`. The needed `|pi_odd| <= n^{1-delta}`
is exactly the regime of **Bourgain-Cochrane-Pinner / Bourgain-Chang / Karatsuba / Shkredov sparse-subgroup-sum
bounds** (which are sensitive to sparsity `w_odd` and subgroup size `n`, NOT to the degree `w` per se -- so they
sidestep the "degree growing" Weil wall). This is resonance-stable by construction (bounds `|pi_odd|` directly).
NEXT: check the quantitative reach of BCP/Karatsuba for a `w_odd~sqrt(p)`-sparse phase over `mu_n` with
`|mu_n|=p^{0.68}`; the question is whether they deliver `n^{1-delta}` with `delta` large enough (`>= 0.095`).

**Methodology fix (banked):** "adversarial max via coordinate ascent on dense `c`" MISSES sparse resonant
optima -- it explores only the dense basin. Any future sup-bound numerics MUST include the sparse monomial /
few-term families explicitly (they are the true extremizers of `S2off`, though NOT of `|pi_odd|`).

**NET (rounds a-e):** conj:Q reduces (T15, LIVE, resonance-stable) to the DIRECT sup bound
`max_{c!=0}|pi_odd(c)| <= n^{0.905}` for a `sqrt(p)`-sparse phase over the large subgroup `mu_n`; the moment
(T14), energy (T11), and 2nd-moment/S2off (round d) proxies are ALL dead (each inflated or lossy). The one
live tool is a sparse-polynomial subgroup-sum bound (BCP/Karatsuba/Shkredov). Numerics: truth `|pi_odd| ~
sqrt(p) = n^{0.74}`, comfortably inside `n^{0.905}`. Still OPEN; the target is now correctly identified and
resonance-stable.

## Cross-check vs holmbuar's grande_finale (upstream, synced 2026-07-07)

Reconciled this track against holmbuar's `experimental/grande_finale.tex` + `grande_finale_work/` +
`notes/thresholds/cap25_v13_qfin_rung_routes_dead.md` + `data/.../kb_mca_conjq_route_margins_v1.json` (merged
to origin/main). **No conflict; strong mutual corroboration; the two tracks are DUAL/complementary.**

- **"SP" is an OVERLOADED name across the two tracks -- they are DIFFERENT objects (do not conflate):**
  - **holmbuar SP = "Shift-Pair"** (`sp_w(e;D')`, `prop:q-second-moment`, `prop:gamma2-ledger`): the primitive
    PTE/shift-pair CENSUS = the exact `L^2` prefix-fiber (SECOND-MOMENT) stratification = the PRIMAL/energy side.
    This is my T6 (PTE `E_d`) + T11 (energy `E` = diagonal + shift-pair strata). Their `thm:q-implies-sp` is
    ONE-WAY (`grande_finale.tex:2051`: "a max-fiber Q would discharge SP, NOT that SP proves Q"): `Q => ShiftPair`.
  - **my SP = "Hypothesis SP"** (rounds a-c): an exponential-sum LARGE-VALUES bound, reduced (T15) to the sup
    bound `max|pi_odd| <= n^{0.905}` = the DUAL/character-sum side. My `SP => Q` is a different object; NO
    circularity with their one-way `Q => ShiftPair`.
- **Independent corroboration (same conclusions, different formulae):**
  - their H1 anticode cap `|Fib_w(z)| <= C(n,m-w)/C(m,w)` DEAD at all 5 rungs  ==  my Result B (packing dead).
  - their `thm:moment-q` (low-moment bridge) DEAD  ==  my T14 (moments dead).
  - their "fixed moments cannot fit the adjacent margins" / SP census still conjectural  ==  my T11 (energy dead,
    `sqrt(M)` ceiling) + round(d) retraction (2nd/4th-moment proxies lossy).
  - their `prop:proper-q-gap` `2^{1.66e6}` allowed bits vs `2^{22.2}` budget  ==  my Result B bit-budget.
  - their `prop:prefix-rigidity` (distinct fiber members differ in `>= w+1`)  ==  my T8 + the **machine-checked
    `powersum_rigidity`** Lean anchor (T6 core). My Lean file is a formal certificate for THEIR rigidity lemma too.
- **SHARED barrier (the key point):** `grande_finale.tex:1022` bounds the coset power-sum character sums by
  **`w sqrt(p)` via Weil** ("deg_y(g(alpha y^d)) <= wd < p, Weil gives w sqrt(p)") -- the SAME degree-growing
  `w sqrt(p) = n^{1.5}` wall my sup bound hits. Both tracks are stuck at Weil-`w sqrt(p)`; conj:Q needs to beat it.
  **My value-add over the shared wall:** (i) T15 crude count shows the SUP bound (not full equidistribution)
  SUFFICES; (ii) resonance-stability -- `|pi_odd|` stays `~sqrt(p)` where the 2nd-moment proxies blow up;
  (iii) the sparse-subgroup-sum (BCP/Karatsuba) angle to sub-Weil, which the primal shift-pair track does not use.
- **NET:** holmbuar works the PRIMAL (shift-pair/second-moment census, `Q => SP`); I work the DUAL (character-sum
  sup bound, `SP_mine => Q`). Both reduce conj:Q to beating the `w sqrt(p)` Weil wall at the deployed depth; both
  OPEN there. The active target is identical to `grande_finale.tex`'s "row-sharp Q atom" (`def:q-row-atom`).

## Round (f) -- frontier-model round on the sup bound: routes mapped, the RESONANCE-STABLE 4th-moment fixes round (d) (2026-07-07)

A focused frontier-model round on `max_{c!=0}|pi_odd(c)| <= n^{0.905}`; all load-bearing claims re-verified here
(`b2_sp_mechanism_probe.py`, `b2_sp_completion_wscaling.py`). Verdict: sup bound is very plausibly TRUE, but
provably NOT reachable by generic Weil/completion, standard high-moment/VMVT, or the existing Bourgain/OSV
induction at the deployed sparsity `r ~ 3.4e4`. The one live route is a resonance-stable subgroup 4th-moment.

**Setup corrections (model, adopted):** `|J_odd| = (w+1)/2 = 33736` (NOT 33735); `sqrt(p) = 46159.575`, so
`w = 67471 = 1.462 sqrt(p)` -- `w` is a genuine constant multiple of `sqrt p`, not `~sqrt p` loosely. Target
`n^{0.905} = 526108 = p^{0.61329}`; subgroup is `n = p^{3/7 + eps}`, `eps = gamma - 3/7 = 0.24910`.

**PROVED (model, verified): monomials are harmless.** For `f = c x^j` (`j` odd), `a -> a^j` permutes `G = mu_n`,
so `pi(c x^j) = sum_{a in G} e_p(ca)` = a Gauss period of index `m' = 1016`, whence
    `|pi(c x^j)| <= (1 + (m'-1) sqrt p)/m' < 46115 = n^{0.738}`.
Clean, unconditional, and confirms resonance-stability (the dangerous complete-sum `127`-resonances do NOT
create large `pi` on `G`, because odd exponentiation permutes `G`).

**PROVED-asymptotic (model): the exponent is exactly at the OSV binomial threshold, but not a fixed-p certificate.**
Ostafe-Shparlinski-Voloch give, for `|G| = tau >= p^{3/7+eps}`, `S(G;f) << tau p^{-eta_d(eps)}`; base savings
`eta_1 = eta_2 = 7 eps/27 = 0.06458`. For BINOMIALS `S(G; a x^m + b x^n) << tau^{20/27} p^{1/9} = n^{0.904702}` --
just below `n^{0.905}`, BUT the slack is only `526108/523831 = 1.0043`, so any implied constant `> 1.0043` loses
it: an asymptotic exponent, NOT a deployed-prime certificate. For `r`-term phases the recursion COLLAPSES
factorially: `eta_3 = 0.01384` (`n^{0.980}`), `eta_4 = 0.00176` (`n^{0.997}`), ... `eta_r -> 0`; at `r = 33736`
the saving is effectively zero. **OSV/Bourgain induction is dead for the full dense odd phase.**

**PROVED obstruction (model): standard Holder/VMVT cannot reach the target for large `r`.** Even granting a
PERFECT diagonal mean-value `Q_K(E;G) << n^K`, the Holder framework gives only `|S(G;f)| << n^{1 - gamma/(2r) +
o(1/r)}`; at `r = 33736` this is `n^{0.99999}`. The diagonal term + the `p^r` coefficient-space factor kill any
`0.095` saving. **Mean-value / decoupling / efficient-congruencing route is DEAD.**

**PROVED obstruction (model): completion to a sparse complete sum is out of reach.** Generic Weil gives
`|S(chi, f_c)| <= w sqrt p > p` (no saving); Cochrane-Pinner sparse improvements need a product-of-exponents
condition, and for the full odd set the geometric mean of exponents `~ 24822` exceeds the C-P nontriviality
threshold `sqrt(p)/4 = 11540` by an exponential-in-`r` margin. **Sparse-complete-sum route is DEAD.**
  - MY numerics (`b2_sp_mechanism_probe.py`, `_completion_wscaling.py`) refine this: for TYPICAL (dense-basin) `c`,
    `max_psi |S(psi,c)|/sqrt p ~ 1.4-2.4`, roughly CONSTANT as `w: 16 -> 66` (`<< sqrt(w)`), i.e. the completed
    sums are empirically `~2 sqrt p` in the dense basin (mechanism M1). BUT this is random-`c` sampling; Weil-sharp
    adversarial `c` for `S(triv,c)` almost surely exist (round-d lesson), so M1 is NOT a proved worst-case fact and
    completion is not salvaged. Recorded as an OPEN empirical curiosity, not a route.

**THE LIVE ROUTE (model route 7, VERIFIED) -- resonance-stable subgroup autocorrelation; this REPAIRS round (d).**
Define the SUBGROUP-internal autocorrelation (sum over `G`, NOT over `F_p^*` -- that was round (d)'s fatal error):
    `T_a^G(c) = sum_{y in G} e_p(f_c(ay) - f_c(y))`, `a in G`.
Then (PROVED identity, numerically confirmed) `|pi_odd(c)|^2 = sum_{a in G} T_a^G(c)`, and by Cauchy
    `|pi_odd(c)|^4 <= n * sum_{a in G} |T_a^G(c)|^2`.
So the sup bound `|pi_odd| <= n^{0.905}` follows from **the ONE estimate**
    **`sum_{a in G} |T_a^G(c)|^2 <= n^{2.62}`  (== `8.17 n p`; RMS `<= 2.86 sqrt p`), uniform in `c != 0`.**
This is RESONANCE-STABLE by construction: every odd exponent is invertible mod `n = 2^k`, so the `127`-resonances
(which poisoned round (d)'s `F_p^*` sum) do NOT appear in the internal `a in G` sum. **Verified
(`_completion_wscaling.py` Part B):** the identity holds exactly; `sum_{a in G}|T_a^G|^2/(np) = 0.06-0.17` and
`/n^{2.62} = 0.018-0.041` -- under threshold with ~25-50x margin -- and IDENTICAL for dense `c` and resonant
monomials (true resonance-stability, unlike round (d)). For monomials `|T_a^G| <= sqrt p + O(1)` gives
`sum <= n^2 + (n-1)p ~ 8.18x` under threshold unconditionally.
  - **The open ingredient:** prove `sum_{a in G} |T_a^G|^2 <= n^{2.62}` WITHOUT completing each `T_a^G` (completion
    reinjects the `w sqrt p` wall) and WITHOUT bounding `T_a^G` by the sup `M` (circular, gives only `n^{0.952}`).
    Trivial bound is `n^3` (each `|T_a^G| <= n`); target beats it by `n^{0.38}`; truth is `~n p = n^{2.47}` (beats
    trivial by `n^{0.53}`), so margin `~n^{0.15}`. It is a genuine 4th-moment over the SUBGROUP, `a,y,y' in G` --
    the model's proposed "inverse theorem for biased odd low-degree phases on the 2-power subgroup."

**NET (round f):** the crux is now the cleanest and most correctly-scoped it has been: prove the RESONANCE-STABLE
subgroup 4th moment `sum_{a in G}|T_a^G(c)|^2 <= n^{2.62}` (fixes round (d)'s `F_p^*`->`G` error). Everything else
(generic Weil, completion/sparse-complete-sum, mean-value/VMVT, OSV `r`-term induction) is PROVED dead at `r ~ 3.4e4`.
Monomials + binomials are handled; the barrier is purely the dense high-`r` phase, and the target beats trivial by
only `n^{0.38}` with `n^{0.15}` numerical margin. Still OPEN; needs a subgroup inverse/structure theorem.

## Round (g) -- attack (1): the subgroup 4th moment IS a multiplicative-energy sum; DIAGONAL DOMINANCE (2026-07-07)

Direct attack on `sum_{a in G}|T_a^G|^2 <= n^{2.62}`. `T_a^G(c) = sum_{y in G} phi(ay) conj(phi(y))` is the
AUTOCORRELATION of `phi := e_p o f_c` on the group `G`, so Wiener-Khinchin gives THREE EXACT equal forms
(all verified `F1==direct==F2` on n=128, `b2_sp_subgroup_4moment.py`):
- **(F1)** `sum_{a in G}|T_a^G|^2 = (1/n) sum_{xi in Ghat} |phihat(xi)|^4`, `phihat(xi_t) = sum_{x in G} conj(chi_t(x)) e_p(f_c(x))`
  (4th moment of the `G`-Fourier spectrum; `phihat(xi_0) = pi_odd(c)`). Computable as `(1/n) sum_t |FFT(phi)_t|^4`.
- **(F2)** `= sum_{x1 x2 = x3 x4, x_i in G} e_p(f_c(x1)+f_c(x2)-f_c(x3)-f_c(x4))` -- a MULTIPLICATIVE-ENERGY
  weighted exponential sum (Bourgain-Garaev regime; `G = mu_n` has `|G| = p^{0.68} > sqrt p`).
- **(F3)** `= sum_{u in G}|R_u(c)|^2`, `R_u = sum_{x in G} e_p(f_c(x) + f_c(u/x))` (`R = phi *conv phi` on `Z/n`).

**KEY STRUCTURAL FINDING -- DIAGONAL DOMINANCE (verified).** Split F2 by the multiplicative-energy diagonal
`{x3,x4} = {x1,x2}` (`2n^2 - n` solutions, all phase `1`):
    `sum_{a in G}|T_a^G|^2 = (2 n^2 - n) + OffDiag(c)`.
The diagonal `2 n^2` sits at `n^2 * 2 << n^{2.62}` (margin `n^{0.62}`) -- it needs NO cancellation. And numerically
the off-diagonal is TINY and often NEGATIVE (net cancellation below the diagonal):
    `|OffDiag| / n^{2.62} <= 0.01`, decreasing with n (n=2048 dense: `-2e-4`; adversarial-on-the-4moment: `+3e-3`,
    shrinking `0.088 -> 0.010 -> 0.005 -> 0.003` for `n=128..2048`).
So the ENTIRE remaining task is: **`OffDiag(c) = sum_{x1x2=x3x4, {x1,x2}!={x3,x4}} e_p(f_c(x1)+f_c(x2)-f_c(x3)-f_c(x4))
<= n^{2.62}`, uniform in c** -- a `3`-variable (`x,y,z in G`, `x4 = xy/z`) multiplicative-energy sum needing only
`n^{0.38}` cancellation from `~n^3` terms; observed cancellation is `~n^{1.5}` (far more than needed).

**Two live sub-routes (numerically viable):**
1. **Bourgain-Garaev on OffDiag directly:** a power-saving bound for the multiplicative-energy exp-sum over a
   subgroup of size `> sqrt p` with additive phase `f_c`. Only `n^{0.38}` saving needed -- weak.
2. **Sup of `R_u` (F3):** `max_{u in G}|R_u| <= n^{0.81} => sum_u|R_u|^2 <= n * n^{1.62} = n^{2.62}`. `R_u` is a
   KLOOSTERMAN-type subgroup sum of the Laurent phase `f_c(x)+f_c(u/x)` (poles order `w` at `0,infty`).
   Numerics: `max_u|R_u| ~ n^{0.70-0.79}` (dense/monomial), `<= n^{0.85}` adversarial at small n, trending to
   `n^{0.70}` -- under the `n^{0.81}` bar for the deployed-size n. (Tighter target than `pi_odd`'s `n^{0.905}`,
   but Kloosterman structure may help; ties to Fouvry-Kowalski-Michel / Bourgain-Garaev Kloosterman-over-subgroup.)

**Adversary fix (vs round d):** the coordinate ascent here maximizes `sum_{a in G}|T_a^G|^2` ITSELF (the correct
adversary for this object), not `|pi_odd|`; it stays under threshold (`<= 0.19`, decreasing to `0.02`) AND gives
the same value for dense and resonant-monomial c -- resonance-stability confirmed against the right adversary.

**NET (round g):** `sum_{a in G}|T_a^G|^2 <= n^{2.62}` reduces (PROVED split) to `OffDiag(c) <= n^{2.62}`, the
off-diagonal MULTIPLICATIVE-ENERGY exponential sum -- diagonal is free (`2n^2`). This is a clean Bourgain-Garaev
target needing only `n^{0.38}` saving, with two viable sub-routes (direct energy bound; or `max_u|R_u| <= n^{0.81}`).
Numerics: massive margin (off-diagonal `~n^{1.5}` cancellation observed vs `n^{0.38}` needed). Still OPEN but now a
standard-shaped multiplicative-energy / Kloosterman-subgroup estimate, not an unstructured sup bound.

## Round (h) -- frontier-model round on OffDiag: monomials PROVED, coefficient-space L^2 PROVED, obstruction razor-sharp (2026-07-07)

Model round on `OffDiag(c) <= n^{2.62}`. Returned TWO genuine theorems (both re-verified here) + a precisely
pinned obstruction. `OffDiag(c) = sum_{Q in Q} e_p(c . Delta(Q))`, `Q =` off-diagonal mult-energy quadruples
`{x1 x2 = x3 x4, {x1,x2} != {x3,x4}}`, `Delta_j(Q) = x1^j+x2^j-x3^j-x4^j`.

**T17 (PROVED -- monomials satisfy the target with fixed-prime room).** For `f = lambda x^j` (`j` odd,
`lambda != 0`): sub `z = x^j` (permutes `G`), `v = u^j`, so `R_u = sum_{z in G} e_p(lambda z + lambda v/z)`;
completing over the `m'=1016` cosets, each inner sum is a twisted Kloosterman sum `<= 2 sqrt p` (Weil). Hence
`max_u |R_u| <= 2 sqrt p = 2^{16.49} < n^{0.81} = 2^{17.01}`, and `OffDiag(lambda x^j) <= sum_u|R_u|^2 - (2n^2-n)
<= 4 n p = 2^{53.99} < n^{2.62} = 2^{55.02}`. **PROVED, deployed-checked.**

**T18 (PROVED + VERIFIED -- coefficient-space `L^2`; bounded multiplicity; mean-zero).** The fiber of
`Q -> (Delta_1, Delta_3, Delta_5)` (just the FIRST THREE odd power-sum differences) has size `<= 16`: from
`Delta_1 = s - t != 0` (`s = x1+x2`, `t = x3+x4`, `P = x1 x2 = x3 x4`), Newton for `p_3, p_5` gives a quadratic
in `q^2 = (s+t)^2` (coeffs in `Delta_1, Delta_3, Delta_5`), so `q` has `<= 4` values, then `s,t,P` fixed and each
pair `<= 2` ordered roots `=> <= 16`. Therefore
    `(1/p^{|Jodd|}) sum_c |OffDiag(c)|^2 = #{Q,Q': Delta(Q)=Delta(Q')} <= 16 |Q| <= 16 n^3`,
so `Pr_c(|OffDiag(c)| > n^{2.62}) <= 16 n^{-2.24} = 1.1e-13`, and `sum_c OffDiag(c) = #{Q: Delta(Q)=0} = 0`
(off-diagonal forbids `Delta_1 = 0`) -- **exact mean-zero**. **VERIFIED (`b2_sp_offdiag_fibers.py`):** max fiber
`= 16` exactly (n=64,128), `coll/n^3 <= 7.85 < 16`, `#{Delta=0} = 0`. So the target holds GENERICALLY (all but a
`1e-13` fraction of `c`) with bounded-multiplicity structure -- it is NOT a large algebraically-degenerate family.

**Both remaining sub-routes now PROVED-DEAD for general `c` (model):**
- **Kloosterman sub-route (2) is DEAD for general `c`:** completing `R_u(c)` gives a Laurent phase of pole order
  `w` at `0,infty`, so Weil gives only `2 w sqrt p = 6.2e9 >> n` (worse than trivial). A sheaf 2nd-moment with
  conductor loss `w^A` beats `n^{2.62}` only if `A < 0.196`; ordinary conductor estimates have `A >= 1`. So FKM/
  Deligne needs a degree-free/resonance-stable input, not sharper bookkeeping. (Works ONLY for monomials, T17,
  where the Laurent phase collapses to a genuine 2-term Kloosterman.)
- **Bourgain sparse-orbit gives a power saving but factorially too small:** `OffDiag <<_r n^{3 - Delta(r)}`,
  `Delta(r) = 2 eta(r)/gamma`, but `eta(r) ~ exp(-C r (1/eps + log r))`. Target needs `eta >= 0.38 gamma/2 =
  0.1288`; at `r = 33736` the saving is astronomically below. Same factorial collapse as OSV (round f).

**The obstruction, razor-sharp (PROVED exact-spike exclusion; OPEN approximate-spike).** Sufficient spectral
condition: `max_t |phihat_t| <= n^{0.81}` (`phihat_t = sum_{x in G} chi_t(x)^{-1} e_p(f_c(x))`, `phihat_0 = pi_odd`),
i.e. NO multiplicative character `chi_t` of `G` correlates with `e_p(f_c)` beyond `n^{-0.19} = 6.3%` of trivial
mass. **EXACT spikes are impossible:** `e_p(f_c) = xi chi_t` on `G` forces (since `gcd(p,n)=1`) `chi_t` trivial,
then `f_c` constant on `n > w` points `=> f_c = 0 => c = 0`. So the ONLY missing ingredient is:
    **`max_{c != 0} max_t | sum_{x in G} chi_t(x)^{-1} e_p(f_c(x)) | <= n^{0.81}`**
-- a quantitative APPROXIMATE-multiplicative-character-spike exclusion (an inverse theorem) for the odd low-degree
additive phase `e_p(f_c)` on the `2`-power subgroup `G`. Current tech proves it generically (T18), for monomials
(T17), and asymptotically-with-tiny-saving (Bourgain), but cannot exclude a rare `c` with `6.3%` character bias.

**Setup precision (model):** the clean `|pi_odd| <= n^{0.905}` needs `OffDiag <= n^{2.62} - (2n^2 - n)`; the
diagonal is `0.0241%` of `n^{2.62}` deployed, harmless given the upstream `p^{0.6137}` crude-count slack.

**NET (round h):** the barrier is now mapped to the millimeter -- `OffDiag <= n^{2.62}` is PROVED for monomials
(T17), PROVED generic with bounded multiplicity + mean-zero (T18, `Pr(bad) <= 1e-13`), and the ONLY gap is a rare
exceptional `c` with a `>6.3%` multiplicative-character correlation; both the Kloosterman and Bourgain-orbit
routes to excluding it are PROVED insufficient at `r = 33736`. The missing piece is a genuine quantitative inverse
theorem (approximate-spike exclusion) -- a hard open problem in its own right, but the conjecture is now known to
be true for all but a `1e-13` fraction of coefficient directions. This is the frontier; consistent with the
barrier being the genuine hard core of the EF prize (both this DUAL track and holmbuar's PRIMAL shift-pair track
converge here).

## Round (i) -- DYADIC DESCENT up the 2-power tower: numerical GREEN LIGHT for a novel proof route (2026-07-07)

Attacking the inverse-theorem crux `max_t |phihat_t| <= n^{0.81}` via a route that uses the ONE thing making
`G = mu_{2^k}` special -- its 2-power structure -- which no generic sum-product/Bourgain method exploits.

**The structure (exact).** The nested tower `G_9 subset ... subset G_k = G`, `G_j = mu_{2^j} = <z_j>`, has
`phihat_{G_j}(chi_t) = DFT(phi_j)_t`, `phi_j[m] = e_p(f_c(z_j^m))`. The tower is EXACTLY the FFT
decimation-in-time butterfly: `phi_{G_{j-1}} =` even subsamples of `phi_{G_j}`, and
`phihat_{G_j}(t) = A_t + omega^t B_t` with `A = DFT_even` (over `G_{j-1}`), `B = DFT_odd` (over the coset
`zeta G_{j-1}`). So an INDUCTIVE proof of `max_t|phihat_{G_j}| <= (2^j)^{theta}` needs the per-level ratio
`rho_j := max_t|phihat_{G_j}| / max_t|phihat_{G_{j-1}}|` to satisfy `rho_j <= 2^{theta}` (geometric-mean sense).
Target `theta = 0.81 => 2^{0.81} = 1.753`.

**Numerics (`b2_sp_dyadic_descent.py`, deployed prime, tower `j = 9..18`, 128 odd exps):** GREEN.
- **Per-level ratio `rho(up)` mean `= 1.46 - 1.54`** (dense 1.459, monomial 1.476, adversarial 1.544) --
  comfortably below `2^{0.81} = 1.75`. Range: dense `[1.36, 1.60]` (all under), adversarial `[1.35, 2.10]`
  (one level touches `2.10`, so a HARD-CAP per-level induction fails, but the geometric mean is what governs).
- **The self-similar exponent `log_{2^j} max|phihat_{G_j}|` is STABLE at `~0.60`** across the whole tower
  (dense 0.647 -> 0.595; adversarial 0.639 -> 0.626), i.e. `max|phihat_{G_j}| ~ (2^j)^{0.60}` -- the geometric
  mean of the `rho`'s is `2^{0.60} < 2^{0.81}`, with MARGIN. The exponent does NOT drift up as `j` grows.
- `max|phihat|/sqrt(N_j) ~ 2.5 - 4.8` (slowly growing), consistent with exponent `0.60`. Butterfly cancellation
  `|phihat|/(|A|+|B|) ~ 0.83 - 1.0` (the two half-spectra peak at different frequencies -- that is WHY `rho ~ 1.46`,
  not `2`).

**Verdict + what a proof needs.** The 2-power dyadic descent is the FIRST route not proved-dead; numerics say the
sup bound is dyadically SELF-SIMILAR with effective exponent `~0.60 << 0.81`, so an AMORTIZED/averaged descent
(not a hard per-level cap -- adversarial `rho` occasionally hits `~2.1`) is viable. A proof needs: (i) a per-level
LEMMA `max_t|phihat_{G_j}| <= 2^{theta} max_t|phihat_{G_{j-1}}|` in an averaged/`L^p`-amortized form with
`theta < 0.81` (the butterfly `A_t, B_t` peak-separation is the mechanism -- must be made quantitative and
uniform in `c`); (ii) a BASE CASE bound on a small `G_{j0}` (small subgroup, possibly Weil-accessible). This is a
concrete, novel, non-dead proof strategy -- unlike Bourgain-orbit/OSV (which collapse at `r = 33736`), it does not
see `r` at all, only the tower height `k = 21`. CAVEAT (regime-first): tested `j <= 18`, 128 terms; deployed
`k = 21`, `w_odd = 33736` -- the exponent stability across `j = 9..18` is the signal, not a proof; larger runs
(bigger `k`, deployed-scale `w_odd`) should confirm the `~0.60` self-similar exponent and the mean `rho < 1.75`.

**NET (round i):** the inverse-theorem crux has a live, novel proof STRATEGY -- dyadic descent up the 2-power
tower (the FFT butterfly), numerically self-similar at exponent `~0.60` (target `0.81`, margin) with mean
per-level growth `~1.46 < 1.75`. The missing analytic inputs are the averaged per-level butterfly lemma + a
small-subgroup base case. This is the first crack that is not a dead proxy; it exploits the 2-power structure
directly. Still OPEN, but for the first time there is a route whose obstruction is a concrete lemma rather than a
factorial-in-`r` collapse.

**Correction (round i.1, `b2_sp_energy_descent.py`): the "descend on `L^4`" idea is REFUTED (diagonal-dominated).**
Tempting to descend on the 4th moment `E(G_j) = (1/2^j) sum_t|phihat_{G_j}|^4` (= the round-g/h mult-energy,
a positive additive quantity). But `E(G_j) ~ 2(2^j)^2` is DIAGONAL-DOMINATED (round g), so the per-level ratio
is trivially `kappa = E(G_j)/E(G_{j-1}) = 4.00` (geo-mean 3.99-4.00, exponent `theta_E -> 2.0`) -- the diagonal
doubling, carrying NO information about the sup bound / OffDiag. So `L^4` descent is uninformative; the working
descent object is the SUP `max_t|phihat_{G_j}|` (ratio `1.46`, round i) or the signed OffDiag directly (small,
harder to track). **Corrected (i): the per-level lemma is a SUP peak-separation statement** --
    `max_t |A_t + omega^t B_t| <= 2^{theta} max_t max(|A_t|,|B_t|)`, `theta < 0.81`, uniform in `c`,
where `A = phihat_{G_{j-1}}` (subgroup) and `B = phihat^{(zeta)}_{G_{j-1}}` (coset, phase `f_c(zeta y)`). The
mechanism (verified `cancel ~ 0.9`) is that the two half-spectra `A, B` PEAK AT DIFFERENT frequencies, i.e. the
phases `f_c(y)` and `f_c(zeta y)` have DECORRELATED `G_{j-1}`-spectra. Proving that decorrelation, uniformly in
`c`, is the concrete (i). The `sqrt(p)` base-case split (BGK small subgroup at `mu_{2^15}`) is UNAFFECTED by
this correction (it is about where the descent starts, not the descent object).

## Round (j) -- attacking the per-level lemma via the difference phase; T18 machine-checked (2026-07-07)

**T18 now MACHINE-CHECKED (Lean 4 / Mathlib, independently re-verified).** `OffdiagMultiplicity.solutions_ncard_le`:
over any field with `2,3,5 != 0` and `D1 != 0`, the off-diagonal fiber `{(x1,x2,x3,x4): x1x2=x3x4=P, sum-diff=D1,
p3-diff=D3, p5-diff=D5}` has `ncard <= 16`. Zero `sorry`; axioms `[propext, Classical.choice, Quot.sound]`. Core
lemma `q_quartic`: `q=x1+x2+x3+x4` satisfies the explicit quartic with leading coeff `45 D1^2 != 0` (a single
`linear_combination` off `x1x2=x3x4`, Newton implicit via `ring`), then `Polynomial.card_roots'` + injection
counting. File `experimental/lean/powersum_rigidity/PowersumRigidity/OffdiagMultiplicity.lean`. Second machine-
checked anchor (with `powersum_rigidity`) -- T18's `L^2`/`Pr(bad)<=1e-13` result now rests on a verified core.

**Attack (1) -- difference phase `g(y) = f_c(zeta y) - f_c(y)`. Honest mixed result (`b2_sp_difference_phase.py`).**
The per-level lemma reduces (PROVED) to spectral NON-concentration of `g`: `B = A conv (spectrum of e_p(g))`, so
`A,B` peak together (ratio -> 2) iff `e_p(g)` is spectrally concentrated; exactly-concentrated (`g` const) forces
`c = 0` (`g = sum_i c_i(zeta^i-1) y^i`, deg `<= w < 2^{j-1}`). Findings:
- **DEAD END: `zeta^i - 1` gives NO free simplification.** The magnitudes `|zeta^i - 1|` are ~uniform in `[0,p)`
  (median `~p/2`), and `g` is SELF-SIMILAR to `f_c`: `exp(max|ghat|) = 0.60-0.61 ~ exp(max|phihat_{f_c}|) = 0.60`
  (dense/monomial). No support reduction, no lower degree. So mining the `zeta`-structure does not make `g` easier;
  the descent is a PURE INDUCTION over the odd-phase class, not a reduction to a smaller problem. (For the
  `f_c`-adversarial `c`, `g` is slightly SIMPLER, `0.602 < 0.623` -- the worst `c` for `f_c` is not worst for `g`.)
- **REAL STRUCTURE: the induction is NON-CIRCULAR via a peaked/spread DICHOTOMY.** Peak-coincidence
  `|B[argmax|A|]| / max|B| = 0.32 - 0.39` (peaks well-separated -- WHY `rho ~ 1.3-1.6`). Mechanism: if `A` is
  PEAKED at `s*`, then `B[s*] ~ A[s*] * ghat_0 / 2^{j-1} + (conv tail)`, and `ghat_0 = sum_y e_p(g(y))` is bounded
  by the INDUCTIVE HYPOTHESIS applied to the odd phase `g` -- so `B` is small at `A`'s peak (separation). If `A` is
  SPREAD, `max|A|` is already small. This dichotomy is genuine (uses the hypothesis on `g`, which is in-class), so
  the descent does NOT circularly assume its conclusion.
- **The remaining analytic gap (concrete):** the CONVOLUTION TAIL `B[s*] = (1/2^{j-1}) sum_r A_r ghat_{s*-r}`.
  Naive `sup * L^1` gives `(2^{j-1})^{theta+0.5}` (too weak); `sup * L^2`/Cauchy-Schwarz gives the trivial
  `2^{j-1}`. Closing (i) needs an `L^p`-refined / restricted convolution bound coupling the inductive bounds on
  `A` (spectrum of `f_c`) and `ghat` (spectrum of `g`) -- NOT a free consequence of the level-`(j-1)` sup bound.
  This is the precise open sub-lemma of the descent.

**NET (round j):** T18 is machine-checked (2nd anchor). The dyadic descent's per-level lemma is now dissected: the
`zeta^i-1` structure gives no free simplification (`g` self-similar), but the descent is a legitimate non-circular
induction driven by a peaked/spread dichotomy; the single remaining analytic gap is an `L^p`-refined convolution-
tail bound `B = A conv ghat` at `A`'s peak. That -- plus the `sqrt(p)` BGK base case -- are the two concrete open
sub-lemmas of the first non-dead route to the crux.

## Round (k) -- per-level lemma REFUTED (dyadic aliasing); GOAL survives via the degree cap (2026-07-07)

Frontier-model round on the per-level butterfly lemma: **the lemma is FALSE as stated** -- counterexample
independently VERIFIED here at FULL DEPLOYED SCALE (`b2_sp_aliasing_check.py`; feasible because the killer `c`
is 2-sparse, so `n = 2^21` is directly computable).

**The counterexample (PROVED + verified, deployed scale).** `f = x - x^{65537}` (`65537 = 1 + 2^16`, both
exponents odd `<= w`). On `G_j`, `j <= 16`: `x^{2^16} = 1`, so `f == 0` IDENTICALLY (verified on all `2^16`
points of `G_16`). The phase is constant on SEVEN tower levels (`j = 9..16`); the butterfly ratio is exactly
`2` there; the sup itself is `N_j` (exponent `1.0`). So NO `theta < 1` holds uniformly: the per-level lemma as
stated is dead. **Mechanism: DYADIC ALIASING of the exponent set mod `2^j`** -- only `c`'s image
`C^(j)_a = sum_{i = a mod 2^j} c_i` matters on `G_j`, and at `j = 16` the reduction has kernel dim
`>= 33736 - 2^15 = 968`. My round-(j) claim "`g` const `=> c = 0`" is valid only for `j >= 18` (`w < 2^{j-1}`);
setup error acknowledged. (Round-(i) numerics missed this because the 128 test exponents lay in `[1,255]` --
no aliased pairs above level 7. THIRD sparse-extremizer sampling miss; adversary catalogs must now include
dyadically-aliased families.)

**Birth scale (PROVED).** All exponents `<= w = 67471 < 2^17` are DISTINCT mod `2^17`, so `C^(17) = c != 0`:
every nonzero `c` is "born" by level `j_0(c) <= 17`, and on `G_17` a nonzero reduced polynomial of degree
`<= w < 2^17` cannot vanish identically. Aliasing lives only on levels `j <= 16`.

**THE DEGREE CAP (our addition, PROVED) -- the GOAL survives exact aliasing.** If `f_c` is constant on
`S subset G` then `f_c - const` has `|S| <= deg f_c <= w` roots, so the exact-freeze mass is
**`<= w = 67471 = n^{0.7639}` at EVERY level and for EVERY `c`.** Exact aliasing therefore CANNOT break the
top-level goal `max_t|phihat_G| <= n^{0.81}`; it breaks only the uniform per-level INDUCTION. Verified at
deployed scale: `f = x - x^{65537}` gives `max_t|phihat_{G_21}| = 68702 = n^{0.7651}` (frozen coset `2^16`
+ noise), UNDER the goal `n^{0.81} = 131984` with margin `1.92x`. Depth-15 multi-pair freeze gives less
(`n^{0.718}`, mass `2^15`) -- the cap binds exactly at depth 16.
**Consequence: the TRUE extremizers of the sup are the dyadically-aliased `c` at exponent `~0.765`** -- not
the generic `~0.60` my earlier adversarial numerics saw. The goal's real margin is a FACTOR `~1.9`, not
`n^{0.16}`. (T15's `n^{0.905}` sup target has more room: `n^{0.7651} << n^{0.905}`, margin `~18x`.)

**Model's proved obstructions (adopted):**
- **`L^p`-Young route DEAD:** using only Parseval + the inductive sup bound, Young/interpolation is minimized
  at `p = 2` and returns the trivial `N'`. No scalar `L^p` spectral norm closes the tail.
- **Flatness alone is INSUFFICIENT (functional-analytic model):** there exist unit-modulus `U, V` with flat
  spectra (`sup ~ N^{0.81}`), small `ghat_0`, yet aligned peaks (ratio `2 - o(1)`). So Parseval + sup + small
  `ghat_0` cannot prove peak-separation -- the proof MUST use the arithmetic of `e_p(f_c)`, not Fourier
  statistics.
- **Conditional form:** peak-coherence bound `|Re(omega^s A_s conj(B_s))| <= eta M^2` uniformly gives
  `theta(eta) = log_2(2 + 2 eta)/2`; `theta < 0.81` needs `eta < 0.537`.

**Repaired route (the surviving induction).** (1) ALIAS-DEPTH FILTRATION: for `j < j_0(c)` the phase is
constant (trivial levels, tracked exactly, capped by the degree bound); (2) BIRTH-SCALE estimate at
`j = j_0(c) <= 17`: the newly-born reduced phase on `G_{j_0}` contributes frozen mass `<= w` plus a fresh-coset
sum; (3) ACTIVE-LEVEL peak-coherence (`eta < 0.537`) for `j > j_0` -- where the model's obstruction says the
input must be arithmetic (an inverse theorem excluding same-frequency peak alignment of `e_p(f_c(y))` and
`e_p(f_c(zeta y))` on alias-free levels). Numerically the active-level behavior after birth is ratio `~1.0`
(the frozen mass stays constant while fresh cosets add cancelling noise) -- consistent with the goal margin.

**NET (round k):** the naive dyadic descent is dead (aliasing), but the refutation IMPROVED the state: the true
extremal family is now identified and PROVABLY capped (`<= w`, degree bound) BELOW the goal with factor-2
margin; the top-level goal survives all exact-aliasing attacks at deployed scale; and the surviving open piece
is (as in round h, now localized to alias-free levels `j >= 17`) a quantitative approximate-spike / peak-
coherence inverse theorem with explicit constant `eta < 0.537`. The crux keeps its shape -- approximate spikes
-- but the exact-spike sector is now completely closed by the degree cap.

## Round (l) -- peak-coherence estimate REFUTED (frozen-fiber family); the DEGREE-BUDGET picture crystallizes (2026-07-07)

Model round on the alias-free peak-coherence estimate: **REFUTED**, by an explicit admissible family --
independently VERIFIED here at FULL DEPLOYED SCALE (`b2_sp_frozen_fiber_check.py`; 3-sparse `c`).

**The counterexample (PROVED + verified).** `f_lambda(x) = lambda x (x^D - 1)(x^D - alpha)`, `D = 2^15`,
`alpha = z20^D` (order 32); exponents `{1, 32769, 65537}` all odd `<= w`. On `H = G_19` (level `j = 20`,
alias-free: `deg f = 65537 < N'/2`): writing `q = y^D in mu_16`, `f(y) = lambda y (q-1)(q-alpha)` and
`f(zeta y) = lambda zeta y (alpha q - 1) alpha (q - 1)` -- BOTH vanish exactly on the fiber `q = 1` of size
`D = 2^15` (verified: exactly 32768 zeros on each half). The zeta-dilation does NOT decorrelate: it PRESERVES
the common exact-zero fiber. A second-moment argument over `lambda` (collision count `<= 15 * 15D`) yields
`lambda` with outside-sums `<= sqrt(450 D)`, so `|A_0|, |B_0| >= D - sqrt(450D) > N'^{0.76}` at the SAME
frequency `s* = 0` with coherence `Re(A_0 conj(B_0)) > 0.53 max^2`. Verified: `|A_0| = 32415, |B_0| = 32430
> 22227 = N'^{0.76}`, coherence `= 1.000`. Same construction works at `j = 18, 19, 20` (certified ratios
`> 0.92, 0.82, 0.66`). **So large same-frequency peaks CAN be coherent at alias-free levels; the `N'^{0.76}`
threshold is too low; the heuristic "correlation => log-rigidity => shift decorrelates" is false.**

**But the GOAL survives AGAIN, at the same scale (verified).** On `G_21` the same `f` freezes TWO fibers
(`q = 1` and `q = alpha`, `q in mu_64`): frozen mass exactly `2^16 = 65536 ~ deg f` (the degree budget).
Top-level `max_t|phihat_{G_21}| = 65369 = n^{0.7617} < n^{0.81}` -- margin `2.02x`. Level-20 sup
`= |G_20|^{0.7992}`, still (barely) under `0.81`.

**THE CRYSTALLIZED PICTURE -- the DEGREE BUDGET governs.** Every extremal construction found so far (dyadic-
aliased pairs round (k): `n^{0.7651}`; frozen fibers round (l): `n^{0.7617}`; certified caps: exact-freeze
`<= deg f <= w` ALWAYS) tops out at the SAME scale `~w = n^{0.764}`. The structure family is now explicit:
    `f(x) = x P(x^D)` with `P` vanishing at consecutive `zeta^D`-translates -- common-fiber freezing,
    whose TOTAL top-level contribution is degree-budgeted at `<= w`.
**Working conjecture (DB):** `max_{c != 0} max_t |phihat_G(chi_t)| <= C w polylog = C n^{0.764+o(1)}` -- the
degree budget is the fundamental invariant; the `n^{0.81}` goal then holds with factor-`~2` room. All verified
data (generic `0.60`, aliased `0.765`, frozen-fiber `0.762`) is consistent with DB.

**Repaired open target (model, adopted -- the sharp remaining statement).** A per-level induction only needs
coherence control for DANGEROUS peaks: `M > 2^{-0.19} N'^{0.81}` (smaller peaks tolerate the trivial factor 2).
The missing theorem is the INVERSE statement:
    **large coherent same-frequency peaks at alias-free levels are either (a) produced by the `x P(x^D)`
    common-fiber structure -- whose total contribution is degree-budgeted (`<= w`) and harmless at top scale --
    or (b) obey a true arithmetic decorrelation estimate.**
This is a classification/inverse theorem with the obstruction family EXPLICITLY identified -- research-grade
open, but maximally structured: the enemy is named (`x P(x^D)` freezing), capped (degree budget), and every
other mechanism must decorrelate.

**NET (round l):** third refutation round, third time the GOAL survives at `~n^{0.764}`. The saga has converged
to: (DB) the degree budget governs the sup; extremals are freeze constructions capped at `w`; the open core is
the freeze-or-decorrelate inverse theorem. Every refutation has come from a degree-budgeted freeze -- none has
approached `0.81`. The partial-results package (T1-T18, rounds a-l, 2 Lean anchors) now contains a complete
map of this barrier: every cheap route provably dead, every extremal family identified and capped, one sharply-
stated inverse theorem remaining.

## Round (m) -- n^0.81 spectral target REFUTED (pigeonhole approximate-freeze); crux returns to SP-large-values, now calibrated (2026-07-07)

Model round on DB: **DB and the `n^{0.81}` spectral target are REFUTED (PROVED, non-constructive)** -- every
arithmetic step independently verified (`b2_sp_pigeonhole_freeze.py`; the construction is a pigeonhole existence
proof, so verification = the proof's arithmetic, exact to the bit).

**The construction (PROVED, verified).** `V` = admissible odd polynomials (`r = 33736` dims, `r log2 p =
1,045,434` bits). Evaluation on one representative per `{x,-x}` pair of `H = G_19` is INJECTIVE (odd `f`
vanishing on `R` vanishes on `H`, `2^19` points `> deg <= w`). Partition `F_p` into `Q = 15` boxes: pattern
space `= 2^18 log2 15 = 1,024,168` bits `< 1,045,434` (margin exactly `21,266` bits). Pigeonhole: two distinct
polys share every box; their difference `f != 0` has `|f(x)|_p <= ceil(p/15)` on ALL of `G_19` -- an
**APPROXIMATE FREEZE of a `2^19`-point subgroup (`7.8 w` points!) by a degree-`<= w` polynomial.** Pairing
(`f` odd) gives `A_H >= 2^19 cos(24 deg) = 478,960.9`, and quotient-Parseval over `G/H` lifts it:
    `max_chi |phihat(chi)| >= 478,960 = n^{0.89855} > 3.63 * n^{0.81}`.  **`n^{0.81}` DEAD. DB DEAD.**

**What failed in DB:** the degree cap controls EXACT fibers (`<= w` roots); but the COEFFICIENT DIMENSION
(`r log2 p` bits) controls APPROXIMATE fibers, and it is large enough to confine `f` to a `p/15`-interval on
`2^19` points. Degree/root-counting (Stepanov included) cannot see this; it is a geometry-of-numbers/coding
phenomenon. (Capacity check, verified: `G_20` worst-case freeze is impossible -- `Q <= 3` by the bit budget and
`cos(2pi/3) < 0`, so the GUARANTEED construction tops out at `G_19`/`n^{0.8986}`.)

**Our push (P1, HEURISTIC, arithmetic verified): the T15 sup target `n^{0.905}` is PRESUMED DEAD too.** The
guaranteed construction sits just UNDER it (`478,960 < 526,108`, margin `1.098x`), but AVERAGE-case coherence
(typical same-box difference ~ triangular, `E[cos] = sinc^2(pi/Q)`) fits `G_20` at `Q = 3` in the bit budget
(`830,977 < 1,045,434`) with `E[cos] = 0.684`, giving heuristically `pi_odd ~ 0.684 * 2^20 = 717,140 =
n^{0.9263} > n^{0.905}`. Not a proof (average-case is not pigeonhole-guaranteed), but the sup route should be
treated as dead: no sup threshold below `~n^{0.93}` is safe.

**Our push (P2, verified exponent arithmetic): the ESCAPE -- freeze families are measure-tiny; SP-large-values
SURVIVES them.** The freeze-family count is calibrated by the pigeonhole margin (`~2^{21,266}` classes). Its
contribution to the SP moment (`s = n/4`, worst extremal `V = n^{0.9263}`) is `21,266 + 0.9263 s log2 n =
10,216,571` bits vs target `s log2 n + 3 log2 n = 11,010,111` bits -- **793,540 bits UNDER: negligible.** So
the freeze phenomenon kills every SUP-based sufficient condition but NOT the original Hypothesis SP
(round (a), Result D): `sum_{c != 0} |pi_odd(c)|^s <= n^{O(1)} n^s`.

**THE REPAIRED CRUX (full circle, but sharply calibrated): a LARGE-VALUES CAPACITY bound.** Let
`N(V) = #{c != 0 : |pi_odd(c)| >= V}`. SP needs `N(V) <= n^{O(1)} (n/V)^s`-type decay. The pigeonhole gives the
LOWER bound `N(n^{0.8986}) >= 2^{21,266}`; the natural conjecture (FREEZE-CAPACITY DUALITY) is that the
pigeonhole bit-budget is essentially TIGHT:
    **`N(rho n) <~ 2^{r log2 p - (coherent-mass bits for rho)}`** -- i.e. large `|pi_odd|` REQUIRES approximate
freezing, and freezing costs bits linearly in the frozen mass. Under this, SP holds with enormous room (count
decay `2^{-rho n}` crushes `V^s` gains). CODING REFRAME: the evaluation code `{(f_c(x))_{x in G}} subset F_p^n`
is a `p`-ary code of dimension `r` (T13's dual side); `N(V)` is its LEE/ARC-WEIGHT distribution near the
minimum -- the crux is a lee-weight-distribution / list-decoding-capacity theorem for this GRS-type code.

**NET (round m):** the sup-bound program (rounds c-l) is definitively closed: `n^{0.81}` refuted (proved),
`n^{0.905}` heuristically unreachable; the crux returns to Hypothesis SP in its ORIGINAL large-values form,
now with (i) the extremal mechanism identified (pigeonhole approximate-freezes), (ii) its guaranteed extremal
verified (`n^{0.8986}`), (iii) its count calibrated (`2^{21,266}`), (iv) proof that these families cannot break
SP (793K bits of room), and (v) the needed theorem named: freeze-capacity duality / Lee-weight distribution of
the odd-evaluation code. The barrier is a capacity statement, not a cancellation statement -- a genuinely
different (and more structured) kind of open problem than where this started.

**Round (m.1) -- the SP open window QUANTIFIED (verified exponent arithmetic).** SP requires the large-values
ledger bound `N(rho n) <= e^{(n/4) ln(1/rho) + O(ln n)}`. Computing where this is already settled:
- `rho < 0.251`: the FULL population `p^{w_odd}` fits inside the SP budget -- nothing to prove.
- `rho > 0.731`: the PROVED T5 moment law (`E|pi|^{2s} <= (2s-1)!! n^s`, optimized `s' = rho^2 n/2`, Gaussian
  tail `e^{-rho^2 n/2}`) already thins the population SP-sufficiently.
- **OPEN WINDOW: `rho in (0.251, 0.731)`** -- SP holds iff `N(rho n) <= e^{(n/4) ln(1/rho)}` there.
Known constructions sit FAR inside budget: pigeonhole-`G_19` (`rho = 0.228`, count `e^{14,740}` vs budget
`e^{774,225}`: room 759,484 nats -- and it is below the window anyway); heuristic `G_20`-freeze (`rho = 0.342`,
count `e^{148,650}` vs `e^{562,595}`: room 413,945 nats). **The entire conj:Q dual crux is now: show that no
more than `(1/rho)^{n/4}` coefficient vectors achieve coherence fraction `rho` on `mu_n`, for
`rho in (0.251, 0.731)`** -- with the capacity heuristic (freezing costs `>~ 1` bit per frozen point,
`count <~ 2^{r log2 p - rho n}`) giving it with enormous room (`2^{-rho n}` vs the needed `rho^{n/4}`).

## Round (n) -- window sharpened, GRS form exact, and the PIVOT: SP is heuristically FALSE (code is Lee-random-like) (2026-07-07)

Model round on the capacity window + OUR decisive experiment. All model arithmetic INDEPENDENTLY VERIFIED
(exact agreement): moment-law crossovers, delta correction, Cramer rates, random-code window.

**Verified refinements (model, all PROVED):**
- **Window narrowed:** the exact optimized moment bound `min_s p^r (2s-1)!! n^s/(rho n)^{2s}` closes
  `rho in (0.251, 0.300861]` and the upper endpoint; OPEN window is `(0.300861, 0.731050)` (verified to 6 digits).
- **Exact GRS form:** after +-pairing, `c -> (x_z P_c(z))_{z in mu_{2^20}}` is a GRS code, length `m = 2^20`,
  dim `r = 33736`; any `r` coordinates determine `c`. `N(rho)` = Lee/cosine-ledger of this code. A rigorous
  MDS/arc counting bound follows but saves only on the `r`-scale -- PROVED insufficient (needs `n`-scale).
- **CORRECTION to our round-(m) clipboard claim (owned):** "any tiny explicit delta > 0 closes the window" is
  FALSE. Closing needs `delta_bits >= 0.52854` (at `rho = 0.6824`) -- large-deviation strength, not tiny.
  (The capacity heuristic's `~1.5` bits/point would still suffice IF provable -- but it is not "tiny".)
- **Logical correction (adopted):** the pigeonhole freeze lower-bounds the max over QUOTIENT characters, not
  the trivial `pi(c)` (unfrozen cosets could cancel); large trivial-`pi` from freezing is heuristic-only.
- **Compression obstruction (PROVED):** reconstruction-from-`r`-coordinates arguments cap at `r I_cos(rho) ~
  9,051` nats of savings at `rho = 0.5` vs the `~361,231` needed. MDS information cannot close the window.

**THE DECISIVE EXPERIMENT (ours, `b2_sp_code_vs_random_ledger.py`): the code is LEE-RANDOM-LIKE.** Exact
enumeration of the ENTIRE code at `(n,p,w_odd) = (16,97,2), (32,97,3), (16,257,2)` vs the iid-uniform-phase
random model: ledger ratios `F_code/F_random = 0.89 - 1.29` across `rho in [0.3, 0.7]`, no systematic thinning.
**So the random-code Cramer heuristic applies, and (verified arithmetic) `ln N_random(rho) = r ln p - m
I_cos(rho)` EXCEEDS the SP budget `(n/4) ln(1/rho)` throughout `rho in (0.303, 0.642)`** (at `rho = 0.5`:
`443,327` vs `363,409` nats). Estimated SP overshoot at the dominating `rho* ~ 0.47`: `~e^{81,000}`.
    **CONCLUSION (heuristic, empirically supported at toy scale): Hypothesis SP -- the large-values /
    absolute-value sufficient condition, in ALL its forms (crude count, sup bounds, capacity ledger) -- is
    FALSE at deployed parameters.** Not merely unprovable: the medium-bias (`rho ~ 0.3-0.6`) codewords of a
    random-like code are genuinely too numerous. (CAVEAT: toy `r/m` ratios `0.19-0.25` vs deployed `0.032`;
    matching held across all tested configs and both `p`; a deployed-ratio test would need larger toys.)

**STRATEGIC PIVOT (the honest endpoint of the dual absolute-value program).** Rounds (a)-(n) have now
established, with proofs, verified extremals, and a falsifiable experiment: every absolute-value route to
conj:Q on the dual side -- moments (T14), energy (T11), 2nd-moment proxies (round d), sup bounds (rounds c-m),
capacity ledgers (round m-n) -- is either proved dead or heuristically false. **The surviving dual route is the
SIGNED sum** (exactly as flagged in rounds (a) line-3 and (d)): the alternating plethystic/e_m structure
`sum_{c != 0} T(c)`, `T(c) = e_m({e_p(f_c(a))})`, whose cancellation is REAL (conj:Q is morally certain, the
mean is tiny) but invisible to any `|.|`-bound. Alternatively: the primal census route (holmbuar's shift-pair
track). What this saga contributes to either: the complete extremal map (freeze families, random-like Lee
statistics, the exact GRS formulation), the proved moment law + window bounds, two Lean-verified anchors, and
the definitive knowledge of WHICH sufficient conditions cannot work -- a fence around the real problem.

**NET (round n): the dual analytic program is COMPLETE as a map: conj:Q's dual crux requires SIGNED
cancellation; no absolute-value statement suffices (SP heuristically false, verified random-like ledger).**
This is a genuine and citable structural finding about the prize barrier itself.
