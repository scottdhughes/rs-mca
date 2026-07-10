# Lean-verified Frobenius-closure primitive backing PR #451's C9 fiber bound (2026-07-10)

Status: `PROVED` (Lean, zero-`sorry`). Module: `experimental/lean/powersum_rigidity/PowersumRigidity/FrobeniusClosure.lean`
(builds under `leanprover/lean4:v4.31.0`; `#print axioms` on all four theorems = `[propext, Classical.choice,
Quot.sound]` only). This machine-checks the exact step PR #451 invokes as "the standard cyclic-code dimension
mechanism," and exhibits it as the same primitive that drives this package's Mersenne reciprocal-gap theorem.

## The shared step

PR #451 (`asymptotic_c9_frobenius_cyclotomic_defect.md`, Theorem 1) bounds a primitive-leaf fiber by
`|Omega ∩ Phi^{-1}(y)| <= p^{d_p(N,I)}`, `d_p(N,I) = N - |Z_p(N,I)|`, `Z_p(N,I)` the Frobenius closure of the
syndrome interval `I`. Its load-bearing step: the fiber-difference polynomial `f_x(X) = sum_i e_i X^i` has
coefficients `e_i in F_p`, so
    **`f_x(zeta^{p k}) = f_x(zeta^{k})^p`**,
whence a root at `zeta^k` forces a root at `zeta^{pk}` — the root set is Frobenius-closed, `G_Z = prod_{k in Z_p}(X - zeta^k)`
divides `f_x`, and `deg f_x < N` leaves `d_p` free coefficients (`p^{d_p}` polynomials).

That boxed identity is a special case of one characteristic-`p` primitive (`FrobeniusClosure.sum_smul_pow`):
for `F_p`-coefficients (`(a i)^p = a i`),
    **`(sum_i a i * omega i)^p = sum_i a i * (omega i)^p`.**

## The two specialisations (both machine-checked)

| lane | `a i` | `omega i` | Lean lemma |
|---|---|---|---|
| **PR #451** (general Frobenius) | `coeff_i in F_p` | `zeta^{i k}` | `eval_pow : f(x^p) = f(x)^p`; `root_pow : f(x)=0 -> f(x^p)=0` |
| **this package** (order-2 Frobenius) | `1` | `x^j` | `psum_pow : (sum_{x in B} x^j)^p = sum x^{jp}` |

`FrobeniusInversion.psum_inv_eq_psum_pow` (L5) is `psum_pow` specialised on `mu_{p+1}` via `x^p = x^{-1}` — the
*inversion* (order-2) Frobenius, which upgrades the dimension count to the sharper reciprocal-gap **coset
structure theorem** (`mersenne_reciprocal_gap`: a `t`-null block of size `<= 2t+1` is a `mu_b`-coset). So:

- **PR #451** uses the general `x -> x^p` Frobenius closure to bound fiber DIMENSION (`p=5`, dyadic `N=2^s`).
- **this package** uses the `p ≡ -1` (order-2) Frobenius closure to pin block STRUCTURE (`mu_b`-coset).

Both are the same closure primitive; `FrobeniusClosure.lean` gives it a zero-`sorry` proof and both corollaries.
`root_pow` is precisely PR #451's "its root set is Frobenius invariant" step, now machine-checked.

## Scope

This formalises the cyclic-code-dimension *closure step* (the Frobenius-invariance of `F_p`-roots), not the full
Theorem 1 (the divisibility `G_Z | f_x` and the `p^{d_p}` count are standard degree bookkeeping downstream of it),
and not any C9 payment (C9 is refuted as a literal standalone, avdeevvadim #444). Offered as rigorous backing for
the mechanism shared by PR #451 and this package's reciprocal-gap theorem. Complements PR #465 (the `e_m`-side
major-arc value-set map, where the `mu_d`-invariant arcs are exactly the Frobenius-closed/coset family).
