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

## Bridge probe (2026-07-06, `../scripts/bridge_probe_directions.sage`)

First numerical probe, witnesses vs matched random `Gamma`:
- **NOT literal additive directions:** `N_add(Gamma) = p` exactly at every witness (deg `Gamma << p`
  ⟹ it determines all additive slopes). The classical additive-directions theorem does not apply
  off-the-shelf; the correspondence is the **multiplicative/dual** version.
- **Extremals are astronomically special (rigidity fingerprint):** random dense `Gamma` have
  `E_3 ~ 0` (essentially no coset gets a size->=3 fiber; coincidence count `C ~ 6-14`), while the
  frontier witnesses saturate `E_3 = ell-2` with `C = 64-104` (~10x). Value-set size is mildly
  smaller only at `ell=17,p=103` (51 vs ~65). Conclusion: the specialness is real and extreme,
  consistent with a lacunary/rigidity theorem, but keyed to the **multiplicative** coset structure.

**Verdict:** bridge confirmed at the *phenomenon* level (rigidity of a rare special `Gamma`),
refuted at the *literal additive-directions* level. The dictionary is multiplicative.

## Multiplicative Rédei polynomial — BUILT (2026-07-06, `../scripts/multiplicative_redei.sage`)

Constructed `R(W,T) = Res_X(X^ell - W, T - Gamma(X)) = prod_{x^ell=W}(T - Gamma(x))` in `F_p[W,T]`
(`deg_T = ell`, `deg_W = ell-1`). Results:
- **Bridge is constructively real:** every concentrated coset (`mu_b>=2`) IS a root of
  `D(W)=disc_T R(W,T)` (verified TRUE, witness + random). The level-set problem = the repeated-root
  locus of ONE bivariate polynomial — the classical directions setup, achieved multiplicatively.
- **Plain discriminant is too coarse for `E_3`:** `deg D = 100`, and its root orders track the
  QUADRATIC coincidence count `sum C(f,2)`, not the LINEAR excess `E_3 = sum (mu-2)_+`. `E_3` is a
  max-per-coset quantity; the discriminant is symmetric in all fibers. So `deg D` does NOT give
  `ell-2`; a finer readout is needed.
- **Right fully-reducible sub-object identified:** fixing a value `c`,
  `R(W,c) = prod_{x:Gamma(x)=c}(W - x^ell)` is fully reducible in `W` with root multiplicities =
  fiber sizes of value `c`; concentration is the `zeta`-rotation coincidence `Gamma(X) = Gamma(zeta X)`,
  `zeta in mu_ell`. This rotational structure is exactly the domain of **Ball Thm 1.9**
  (`f = X^{q/s} g + h`, `gcd(g,h)=1`). That is the specific transfer target.

**Honest status:** the constructive bridge is established; extracting `E_3 <= ell-2` from it is the
open research step — apply Ball Thm 1.9 / the `f|(Xg+h)(h'g-g'h)` mechanism to the fully-reducible
`R(W,c)` / `zeta`-rotation object (not the coarse discriminant). The library now has the full-proof
sources (Ball–Weiner book, BBBSSz 1999, Gács 2003) to do this.

## Thm 1.9 applied to R(W,c): additive theory does NOT transfer; Carlitz–McConnel is the right tool

`../scripts/redei_RWc_structure.sage`: for each excess coset's modal value `c`,
`R(W,c) = Res_X(Gamma(X)-c, W - X^ell) = prod_{Gamma(x)=c}(W - x^ell)` is fully reducible with
root multiplicities = the value-`c` fiber sizes (VERIFIED: `c=301 -> [5]`, `c=215 -> [4,1,1]`, ...).
**But `deg_W R(W,c) = ell-1 << p`, so it is NOT a Frobenius `W^p g + h` object** — Ball Thm 1.9's
hypothesis (`x -> x^p`, `X^p - X = prod(X-a)`) fails. The additive lacunary/directions theory does
NOT literally transfer: our structure is Kummer (`ell | p-1`, multiplicative), not Artin–Schreier /
Frobenius (`p^e`, additive).

**The correct engine is the MULTIPLICATIVE (cyclotomic) analog — the Carlitz–McConnel theorem and
its recent extensions.** Carlitz–McConnel: if the difference quotients of `f: F_q -> F_q` all lie in
a proper multiplicative subgroup of `F_q^*`, then `f` is a monomial (Frobenius-linear). Recent work
extends this to difference quotients in **unions of cosets of a multiplicative subgroup**
(= cyclotomic classes = our cosets of `mu_ell`): Xiong–Yip (arXiv 2604.04126), Asgarli–Yip,
Blokhuis–Sziklai. This is literally the "directions restricted to `mu_ell`-cosets" rigidity our
`E_3 <= ell-2` needs. Library: `../../literature/cyclotomic-directions/`.

## Next steps
1. Read Ball's survey §1.2–1.4 + the `f|(Xg+h)(h'g-g'h)` proof in detail against our `g_k,h_k`.
2. Test numerically whether the Rédei polynomial of a `Gamma`-coset configuration reproduces the
   direction-count / gap predicted by the classical bounds (a decisive check of the bridge).
3. If it transfers: draft the multiplicative lacunary lemma and (re)route to Aristotle with the
   classical method as scaffolding.
