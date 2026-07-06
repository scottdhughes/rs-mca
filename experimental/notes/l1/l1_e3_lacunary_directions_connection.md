# L1: the prime-`ell` frontier is (very likely) Rédei–Szőnyi directions in multiplicative form

- **Status:** LITERATURE FIND / CONJECTURAL BRIDGE + PROOF-ROUTE LEAD. Not proved; the
  additive→multiplicative transfer is not yet worked out.
- **Agent/model:** Claude Opus 4.8, branch `scott/l1-e3-ceiling-open-chart`, 2026-07-06.
- **Sources:** `../../literature/` (Ball lacunary notes; ABF 2026/680; Kam26; syndrome-space).

## The evidence (why this is not a coincidence)

The classical theory of **fully-reducible lacunary polynomials** (Rédei 1970; Lovász–Schrijver;
Blokhuis–Brouwer–Szőnyi; Blokhuis–Ball–Brouwer–Storme–Szőnyi; Gács; Szőnyi; see Ball's survey)
studies functions `f : F_q -> F_q` via the **number of directions** `N` they determine, and finds
a rigid spectrum of possible `N`. Two nontrivial critical values:
1. **`(q+3)/2`** — the least `N>1`; achieved by `f = X^{(q+1)/2}` (Ball Example 1; Rédei;
   Lovász–Schrijver characterization).
2. **`ceil(2(q-1)/3)+1`** — the next value up (Gács, *On a generalization of Rédei's theorem*,
   Combinatorica 2003): if `N > (p+3)/2` then `N >= ceil(2(p-1)/3)+1`.

The rs-mca prime-`ell` frontier work **independently rediscovered both**:
- corrected law `m*(ell) = (ell+3)/2`  ⟷  `(q+3)/2`;
- **refuted** conjecture `ceil(2ell/3)`  ⟷  Gács `ceil(2(p-1)/3)`.

Hitting *both* critical values of the Rédei–Gács direction spectrum by chance is implausible.
Combined with the identical algebra (below), this strongly indicates the frontier and the KEY
LEMMA live inside the lacunary-polynomial theory.

## The algebraic dictionary (exact structural match)

| lacunary-polynomial theory | our L1 / KEY LEMMA setup |
|---|---|
| fully-reducible `f = X^n g(X) + h(X)`, `gcd(g,h)=1` | coset locator `X^ell - w_k = g_k h_k` (fiber × co-fiber locators) |
| "gap" / second degree `k = max(g°,h°)` | fiber size `mu_k` (excess `mu_k-2`) |
| driving divisibility **`f | (Xg+h)(h'g - g'h)`** (Ball p.6) | the tool we lack for `dim Syz <= K` |
| Rédei polynomial `Prod (X + aY - f(a))` | `Prod` over coset points / the incidence system |
| directions `N` | listing threshold / `top-m` |

The Wronskian `h'g - g'h` of the fiber/co-fiber split is exactly a syzygy-type object; the
classical proof that a fully-reducible lacunary polynomial forces a large gap is the archetype of
the bound we want (`E_3 <= ell-2`, equivalently `dim Syz <= K`).

## Proof-route lead

Attack `dim Syz <= K` (equivalently `dim(sum V_k) >= E_3`, equivalently `E_3 <= ell-2`) by
importing the lacunary-polynomial method:
1. Assemble the Rédei polynomial / the fully-reducible object `X^ell g + h` attached to `Gamma`
   and the cosets, matching `g_k h_k = X^ell - w_k`.
2. Apply the divisibility `f | (Xg + h)(h'g - g'h)` and the degree/derivative bookkeeping that
   powers Rédei Thm 1.1 and the Blokhuis–Ball classification (Ball Thm 1.9/1.14).
3. Read off the second-degree (gap) bound — this should be `E_3 <= ell-2`.

The **caveat** (do not skip): the classical theorems are stated for **additive** subfields
`F_s` (`x -> x^{p^e}`, `AG(2,q)`), while ours is **multiplicative** (`x -> x^ell`, `ell | p-1`,
`mu_ell`). The *engine* (fully-reducible lacunary polynomials + Wronskian divisibility) is more
general than the additive statements, but the transfer must be done explicitly; the numerology
match is evidence it goes through, not a proof.

## Novelty positioning (for the paper; honor "check prior lit, no overclaim")

- The **near-capacity failure theme is NOT novel**: Kam26 (arXiv 2604.09724) and KKH26
  (eprint 2026/782) already prove proximity gaps fail near capacity over prime fields (both in
  ABF's references). Position Paper A / the rs-mca thesis against these; do not claim the failure
  direction as ours alone. Our specific `(ell+3)/2` listing law + `E_3` level-set mechanism is not
  in Kam26 (which is `O(1/log n)`-below-capacity, no roots-of-unity/level-set structure).
- The **combinatorics of `(ell+3)/2`/`E_3<=ell-2` is classical** (Rédei–Szőnyi–Ball). If the bridge
  is real, our contribution is (i) *identifying* the SNARK proximity-gap/MCA frontier as a
  multiplicative directions problem, and (ii) any genuinely new multiplicative transfer — NOT the
  underlying bound. Cite Rédei/Szőnyi/Ball/Gács; frame as "the frontier is governed by classical
  lacunary-polynomial theory," which is itself a valuable and defensible novelty.

## Next steps
1. Read Ball's survey §1.2–1.4 + the `f|(Xg+h)(h'g-g'h)` proof in detail against our `g_k,h_k`.
2. Test numerically whether the Rédei polynomial of a `Gamma`-coset configuration reproduces the
   direction-count / gap predicted by the classical bounds (a decisive check of the bridge).
3. If it transfers: draft the multiplicative lacunary lemma and (re)route to Aristotle with the
   classical method as scaffolding.
