# The prime-`ell` MCA listing frontier is Redei-Szonyi "directions" in cyclotomic form

- **Status:** STANDALONE INSIGHT / NOVELTY NOTE. A structural bridge, not a proof of the open crux.
- **Agent/model:** Claude Opus 4.8, 2026-07-06. Verifications: `../scripts/*` (Sage/PARI/FLINT/M2).
- **One line:** the SNARK proximity-gap / MCA prime-`ell` listing frontier is the classical
  **Redei-Szonyi theory of directions and fully-reducible lacunary polynomials** transported from
  the additive (Frobenius) setting to the multiplicative (cyclotomic, `ell | p-1`) setting; its
  sharp rigidity is the **Carlitz-McConnel / cyclotomic-class** theory.

## The MCA object (setup)

`ell` odd prime, `ell | p-1`, `H = mu_ell <= F_p^*`; cosets `bH` partition `F_p^*`, each of size
`ell`. `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` constant-free, `deg <= ell-1`, mixed. Per coset,
`mu_b = max value-fiber of Gamma`; `top-m = ` sum of the `m` largest `mu_b`; a mixed full-petal
codeword **lists** iff `top-m >= 2ell`. At the onset `m = t+1` the corrected listing frontier is
`m*(ell) = (ell+3)/2` for every prime `ell >= 7` (refuting the earlier `ceil(2ell/3)` conjecture).

## The classical directions problem

For `f : F_q -> F_q`, the *directions* `D(f) = {(f(x)-f(y))/(x-y)}`. Redei-Megyesi: a set of `q`
points in `AG(2,q)` is a line or determines `>= (q+3)/2` directions; the number of directions has a
**rigid spectrum** with a gap. Two critical values:
- `(q+3)/2` -- the least nontrivial count, achieved by `f = X^{(q+1)/2}` (Ball, Example 1;
  characterized by Lovász-Schrijver).
- `ceil(2(q-1)/3)+1` -- the *next* value (Gacs, Combinatorica 2003): if `N > (p+3)/2` then
  `N >= ceil(2(p-1)/3)+1`. The band `((p+5)/2, 2(p-1)/3)` is empty.

## The dictionary (the bridge)

| MCA listing frontier | classical directions |
|---|---|
| corrected onset law `m*(ell) = (ell+3)/2` | least direction count `(q+3)/2` |
| **refuted** conjecture `ceil(2ell/3)` | **Gacs** next value `ceil(2(p-1)/3)` |
| coset locator `X^ell - w = g_k h_k` | fully-reducible `X^n g + h`, `gcd(g,h)=1` |
| fiber size `mu_k` | lacunary gap / second degree |
| co-fiber Wronskian `g_k' h_k - g_k h_k'` | driving divisibility `f | (Xg+h)(h'g-g'h)` |
| max-fiber excess `E_3 <= ell-2` | slope-count rigidity |

The rs-mca program independently rediscovered BOTH critical values of the Redei-Gacs spectrum
(`(ell+3)/2` and `ceil(2ell/3)`) -- overwhelming evidence the frontier IS the directions problem.
The construction of the multiplicative Redei polynomial `R(W,T) = Res_X(X^ell - W, T - Gamma(X))`
makes it explicit: coset concentration = repeated roots of `disc_T R` (verified).

## The correct rigidity home (multiplicative, not additive)

The transfer is **Kummer, not Frobenius**: `x -> x^ell` with `ell | p-1` is multiplicative, so the
additive lacunary theorems (built on `x -> x^{p^e}`, e.g. Ball's `f = X^{q/s}g+h`) do NOT literally
apply (verified: `R(W,c)` has degree `<< p`). The correct engine is the **cyclotomic-class /
Carlitz-McConnel** rigidity line:
- **Carlitz-McConnel:** if `(f(x)-f(y))/(x-y)` lies in a proper *multiplicative subgroup* of `F_q^*`,
  then `f = a x^{p^j} + b` (a monomial).
- **Xiong-Yip (2604.04126), Blokhuis-Sziklai, Asgarli-Yip:** unions of cosets (cyclotomic classes),
  the `(q+1)/2` threshold (= our `(ell+3)/2`), proved by **character sums + finite geometry**.
- `E_3 <= ell-2` <=> the level set `Gamma^{-1}(c)` cannot have two elements of ratio in `mu_ell`
  beyond the rigidity budget = the generalized-Paley / cyclotomic-scheme max-clique statement.

## Why this matters

1. **Novelty:** connects the SNARK proximity-gap / MCA frontier (a cryptography-driven object) to
   the classical Redei-Szonyi-Ball-Gacs finite geometry of directions -- a link absent from the
   rs-mca program and, to our knowledge, the literature. Reframes the whole prime-`ell` frontier.
2. **Correct technique:** it says the sharp bound is *cyclotomic rigidity* (character sums + finite
   geometry, Carlitz-McConnel style), NOT the additive Frobenius lacunary calculus -- and that the
   finite max-fiber inequality reduces to a **BGK-style additive-combinatorics inverse theorem**
   (verified: per-frequency character bounds cap at `sqrt(p)`; joint cancellation is required).
3. **Toward the crux:** if `E_3 <= ell-2` (CAP25 v13's named-open finite max-fiber inequality) is
   ever closed, the Carlitz-McConnel/cyclotomic-scheme rigidity is the most likely vehicle.

## Honest scope

This is a *reframing*, not a proof. The upper half `dim(sum V_k) <= ell-2` is proved (4-engine
cross-checked); the crux `E_3 <= ell-2` (`dim Syz <= K`, `K>=3`) remains open, as it is for CAP25
v13, holmbuar (#358, master identity + `T<=4` bound), and two Aristotle runs. The bridge's value is
directional: the right classical theory, the right technique, the right novelty framing.

## References (in `../../literature/`)
Ball, *Lacunary polynomials* + Ball-Weiner *Intro to Finite Geometry*; Blokhuis-Ball-Brouwer-Storme-Szonyi,
JCTA 86 (1999); Gacs, Combinatorica 23 (2003); Xiong-Yip, arXiv 2604.04126; Kowalski (BGK subgroup
exp. sums); Wan, index bounds. ABF 2026/680 (prize); Chojecki CAP25 v13.
