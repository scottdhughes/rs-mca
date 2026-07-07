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
