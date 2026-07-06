# L1 KEY LEMMA `E_3 <= ell-2`: upper structural half PROVED, crux reduced to bounded syzygies

- **Status:** PROVED (upper bound `dim(sum V_k) <= ell-2`, elementary; numerically verified on
  the shipped witnesses + a 2024-Gamma sweep; **pending independent review before promotion**)
  / OPEN (remaining crux `dim(sum V_k) >= E_3`).
- **Agent/model:** Claude Opus 4.8, branch `scott/l1-e3-ceiling-open-chart`.
- **Date:** 2026-07-06.
- **Builds on:** `l1_prime_ell_frontier_corrected.md` §3 second-pass (i) (the subspace form of
  the KEY LEMMA) and `l1_e3_ceiling_independent_audit.md` (independent audit + extremal locus).
  This is L1-lane new work (not an edit of the frontier note or Papers A–D).

## Setup (from the frontier note)

`ell` odd prime, `ell | p-1`, `H = mu_ell`, cosets `bH` partition `F_p^*`, `Gamma` constant-free
of degree `<= ell-1`, mixed. For each coset with maximal fiber `F_k` of size `mu_k >= 3`,
shared value `c_k`, coset label `w_k = b^ell`:

- `g_k = prod_{x in F_k}(X-x)` (fiber locator, `deg mu_k`);
- `h_k = prod_{x in coset\F_k}(X-x)` (co-fiber locator, `deg ell-mu_k`);
- `V_k = h_k * F_p[X]_{<= mu_k-2}  subset  F_p[X]_{<= ell-2}`,  `dim V_k = mu_k-1`;
- `E_3 = sum_k (mu_k-2)`,  `K = #{excess cosets}`,  `sum_k dim V_k = E_3 + K`.

The frontier note's reduction: **`E_3 <= ell-2  <=>  dim(sum_k V_k) >= E_3`**.

## Theorem (upper structural half). `dim(sum_k V_k) <= ell-2`.

Let `L: F_p[X]_{<= ell-2} -> F_p` be the functional `L(A) = [X^{ell-1}](A * Gamma)` (coefficient
of `X^{ell-1}` in the product). Since `Gamma != 0`, `L != 0`: if `j` is the least index with
`gamma_j != 0`, then `L(X^{ell-1-j}) = gamma_j != 0` and `ell-1-j <= ell-2`. Hence
`W := ker L` has `dim W = ell-2`.

**Claim: every `V_k subset W`.** Fix an excess coset. `Gamma` is constant `= c_k` on `F_k`, so
`g_k | (Gamma - c_k)`; write `Gamma = c_k + g_k q_k` with `deg q_k <= (ell-1) - mu_k`. Also
`g_k h_k = X^ell - w_k` (the coset's `ell` points are exactly the roots of `X^ell - w_k`). For
`0 <= d <= mu_k-2`,
```
h_k X^d Gamma = c_k h_k X^d + (X^ell - w_k) q_k X^d.
```
- `deg(h_k X^d) = (ell-mu_k)+d <= ell-2 < ell-1`, so `[X^{ell-1}](c_k h_k X^d) = 0`.
- `[X^{ell-1}]((X^ell-w_k) q_k X^d)`: the `X^ell`-part contributes `[X^{-1-d}](q_k)=0`; the
  `-w_k`-part needs the `X^{ell-1}` coefficient of `q_k X^d`, but
  `deg(q_k X^d) <= (ell-1-mu_k)+(mu_k-2) = ell-3 < ell-1`, so it is `0`.

Thus `L(h_k X^d) = 0` for all `d <= mu_k-2`, i.e. `V_k subset W`. Therefore
`sum_k V_k subset W` and `dim(sum_k V_k) <= dim W = ell-2`. ∎

**Numerical confirmation.** `verify_e3_upper_bound.sage` checks all three ingredients
(coset factorization, `g_k`-divisibility, and the `[X^{ell-1}]`-vanishing) directly on the
ell=11/13/17 witnesses (all PASS). `universal_dim_sweep_e3.sage` finds, over **2024 Gamma**
(random + solve-planted + anchors, ell in {7,11,13,17}), that `dim(sum V_k) <= ell-2` is never
violated, and the annihilating functional at every `dim = ell-2` anchor equals **`reverse(gamma)`**
exactly — which is `L` in coordinates (`[X^{ell-1}](A*Gamma) = <A, reverse(Gamma)>`). This is
what pointed to the proof.

## Consequence: the KEY LEMMA reduces to a bounded-syzygy lower bound

With `dim(sum V_k) <= ell-2` now unconditional, the direction
`[dim(sum V_k) >= E_3] => [E_3 <= dim <= ell-2]` is immediate. So the entire KEY LEMMA follows from:

> **Remaining crux (OPEN).** `dim(sum_k V_k) >= E_3`, equivalently the degree-bounded syzygy module
> ```
> Syz = { (q_1,...,q_K) : sum_k h_k q_k = 0,  deg q_k <= mu_k-2 }
> ```
> has `dim Syz <= K`  (since `dim(sum V_k) = sum dim V_k - dim Syz = (E_3+K) - dim Syz`).

**What is already known about `Syz`.**
- **Pairwise (K=2) is trivial: `dim Syz = 0`.** The `h_k` are pairwise coprime (co-fibers in
  distinct cosets have disjoint roots); `h_i q_i = h_j q_j` with `gcd(h_i,h_j)=1` and
  `deg q_i <= mu_i-2 < deg h_j` forces `q_i=q_j=0`. This recovers the note's proved K=2 case
  and confirms the obstruction is irreducibly `>=3`-way (matching the extremal-locus audit:
  all pairwise `delta=0`, joint `delta=K`).
- **The bound is tight:** at the `E_3=ell-2` saturators `dim Syz = K` exactly (verified).

So the open `K>=3` chart is precisely: **bound the degree-`(mu_k-2)` syzygy module of the
pairwise-coprime co-fiber locators `h_k` by `K`.** This is a concrete commutative-algebra target
(no fibers, no varying primes) with the base case done — a natural handoff to a syzygy/resultant
argument (or Aristotle/Codex on the clean sub-lemma).

## Syzygy generators, cross-check, and why realizability is essential (part a)

`syzygy_generators_e3.sage` computes an explicit basis of `Syz` at the saturators and finds
`dim Syz = K` with a **triangular / staircase basis**: ordering fibers by size, the generators are
indexed by monomials `X^d` in the leading block(s), each extending uniquely to a syzygy (e.g.
`ell=11 p=331`, K=4: the four generators have `q_0 = 1, X, X^2, X^3` with the other `q_k`
determined). This is the structure a leading-term proof of `dim Syz <= K` would exploit.

**Independent second-engine cross-check.** `syzygy_xcheck.gp` (PARI/GP, its own primitive root and
polynomial arithmetic) reproduces `dim(sum V_k) = E_3` and `dim Syz = K` at all three saturators —
matches Sage exactly.

**Realizability is ESSENTIAL (decides the hypothesis).** For *arbitrary* pairwise-coprime co-fiber
locators `h_k` (random distinct `w_k`, random `mu_k`-subsets, NOT level sets of a common `Gamma`),
`dim Syz <= K` FAILS badly — up to `dim Syz - K = +29` at `ell=13` (e.g. sizes `[10,12,6,11,12]`,
`E_3 = 41`). Reason: any config with `E_3 >= ell` forces `dim Syz > K` by pure dimension count
(`image ⊆ F_p[X]_{<=ell-2}`). So the bound is NOT a general fact about pairwise-coprime polynomials;
the hypothesis that a *single* `Gamma` of degree `<= ell-1` threads all the level sets (CRT rigidity)
is exactly what pulls `E_3` down to `<= ell-2`. The Aristotle obligation carries this hypothesis.

**Aristotle.** The KEY LEMMA (with the proven upper half and the `dim Syz <= K` crux) was submitted
to Aristotle abstracted as pure finite-field algebra: `experimental/aristotle_e3_obligation.md`,
project `70427d46-d108-4d03-8edd-bdf9594bb86f` (poll with `aristotle poll <id>`; output is a DRAFT to
re-verify).

## Reproducibility
```bash
sage experimental/scripts/verify_e3_upper_bound.sage        # proof-core check on witnesses
sage experimental/scripts/universal_dim_sweep_e3.sage       # 2024-Gamma sweep + annihilator=rev(Gamma)
sage experimental/scripts/syzygy_generators_e3.sage         # (a) syzygy generators + arbitrary-config stress
gp  -q experimental/scripts/syzygy_xcheck.gp                 # PARI/GP independent cross-check
```

## Honest scope
The upper bound `dim(sum V_k) <= ell-2` is a complete elementary proof (independent review still
advised before promoting to `tex/`). The KEY LEMMA itself is **not** proved: the crux
`dim(sum V_k) >= E_3` (equivalently `dim Syz <= K`) remains open for `K>=3`. No MCA / list /
protocol consequence is claimed here.
