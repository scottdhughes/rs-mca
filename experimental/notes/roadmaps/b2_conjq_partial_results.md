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
