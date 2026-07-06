# L1: the character-sum inequality for `E_3` — the pair-cap, and why it is not sharp

- **Status:** PROVED (pair-cap, elementary/character-sum) + NEGATIVE DELIMITATION (character sums do
  NOT reach `E_3 <= ell-2`). Redirects to the rank route.
- **Agent/model:** Claude Opus 4.8, branch `scott/l1-e3-ceiling-open-chart`, 2026-07-06.
- **Verifier:** `../scripts/charsum_paircap.sage` (identity + cap + sharpness, on the witnesses).

## The character-sum object (Fourier over `mu_ell`)

`Gamma` constant-free, `deg <= ell-1`, `ell | p-1`, mixed. For a coset `b` and value `c`,
`N_b(c) = #{x in bH : Gamma(x)=c}`, so `mu_b = max_c N_b(c)`, `sum_c N_b(c)=ell`. Two points lie in
one coset iff their ratio is in `mu_ell`. Expanding this coset-indicator over `mu_ell` and summing:

**Proposition (pair-cap).** With `Delta_zeta(X) := Gamma(X) - Gamma(zeta X)` for `zeta in mu_ell`,
```
   sum_b sum_c N_b(c)(N_b(c)-1)  =  sum_{zeta in mu_ell, zeta != 1} #{x in F_p^* : Delta_zeta(x)=0}
                                 <=  (ell-1)(ell-2).
```
*Proof.* The ordered same-coset equal-value pair count is `sum_{zeta!=1} #{x: Gamma(x)=Gamma(zeta x)}`
(pair `(x, zeta x)`). For `zeta != 1`, `Delta_zeta != 0` (`Gamma` mixed ⟹ some `gamma_r(1-zeta^r) != 0`),
and `Delta_zeta = sum_r gamma_r(1-zeta^r) X^r` is constant-free, so `X | Delta_zeta` and it has at most
`ell-2` nonzero roots. Sum over the `ell-1` nontrivial `zeta`. ∎

**Verified** (`charsum_paircap.sage`): the two forms of `2C` agree exactly; `2C <= (ell-1)(ell-2)`
holds (witness `2C = 64, 82, 104` vs `90, 132, 240`); each single-`zeta` root count is `<= ell-2`.

## Why it is NOT sharp for `E_3 <= ell-2`

Since `mu_b >= 3 ⟹ mu_b(mu_b-1) >= 6`, the pair-cap gives only
```
   E_3  <=  (ell-1)(ell-2)/6 .
```
That is `15, 22, 40` at `ell = 11, 13, 17` — versus the true `ell-2 = 9, 11, 15`. The gap is a factor
`~2-3`, not a fixable constant. **The 2nd moment (all character-sum / Weil / Cauchy–Schwarz methods
bottom out here):** it sees fibers *quadratically and symmetrically over all values*, whereas `E_3` is
the *linear excess of the max fiber, coupled across cosets by a single low-degree `Gamma`*. Weil bounds
on `S(zeta,t)=sum_x e_p(t Delta_zeta(x))` are even worse here (error `~ (ell-2)sqrt(p)` swamps the
elementary degree bound, since `ell << p`).

## Verdict and redirect

**`E_3 <= ell-2` is a rank / realizability statement, not a character-sum inequality.** This
independently confirms the frontier note's own conclusion ("the missing ingredient is realizability —
a rank statement, not a moment statement"; the moment method has no bite past `m=4`). Consequences:
- **Upper-bound proof route = the rank one:** `E_3 <= ell-2 <=> dim(sum V_k) >= E_3 <=> dim Syz <= K`,
  with `dim(sum V_k) <= ell-2` already PROVED (`l1_e3_subspace_upper_bound.md`). Character sums do not
  shortcut this.
- **What the cyclotomic-rigidity theory IS good for:** the *extremal characterization* (which `Gamma`
  saturate `E_3 = ell-2`), via spectral / Gauss-sum-period (cyclotomic-scheme eigenvalue) methods — the
  tight side, matching the Blokhuis–Sziklai / Xiong–Yip rigidity, not the upper bound.

So the character-sum inequality is the pair-cap above; it is banked, and the sharp bound stays on the
rank/syzygy track (`dim Syz <= K`, the open `K>=3` chart).

## Reproducibility
```bash
sage experimental/scripts/charsum_paircap.sage
```
