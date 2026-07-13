# The Sidon-paired depth-1 fiber profile is an exponential staircase: staircase-concentration is DECIDED FALSE (the #732 max-fiber residual, refuted on its own class)

## Status

```text
Status: PROVED exact fiber-size classification (2-superincreasing / B[+-2] base,
        depth 1, a=B) + PROVED robust lower bound (every distinct-subset-sum
        "Sidon-paired" P) + PROVED (COUNTEREXAMPLE / route-cut) that the
        fiber-size profile is NOT staircase-concentrated in #732 Theorem B.2's
        sense.  DECIDES the CONCENTRATION clause negatively on the class it was
        hoped to hold on.
HARD INPUT 2 SERVED: the CONCENTRATION clause -- the last unproved clause of
        avdeevvadim's #716 charge-preserving semantic-or-signed dichotomy on the
        Sidon-paired depth-1 class, flagged by #732 Theorem B as its residual
        "staircase-concentration / max-fiber" hypothesis.  DECIDED.
Verdict per sub-question (route-scoped):
  (1) EXACT PROFILE.  For P a 2-superincreasing set (A_i > 2 sum_{j<i} A_j,
      equivalently B[+-2]-dissociated; e.g. A_i = 3^i, 5^i), T = P u (c-P),
      |T|=2B, a=B, c > 2 sum P, Phi = subset sum over Z:
         |Phi^{-1}(sigma)| = C(B - s, (B - s)/2),
      where s = #unpaired twin-pairs of any support in the fiber, and there are
      EXACTLY C(B, s) 2^s syndromes at unpaired-count s (s == B mod 2).  This
      recovers L = (3^B+1)/2 and M = C(2B,B) (#717 Sec 7 / #728) and the central
      fiber W = C(B, B/2) (#735 Thm 2) as the single s=0 term.
  (2) ROBUST LOWER BOUND.  For EVERY distinct-subset-sum P (the general
      "Sidon-paired" class, incl. non-superincreasing Conway-Guy sets), each
      s-subset R of [B] gives a DISTINCT syndrome sigma_R with
      |Phi^{-1}(sigma_R)| >= C(B - s, (B - s)/2); there are C(B, s) of them.
      Non-B[+-2] sets only make fibers LARGER (merging syndromes), never smaller.
  (3) CONCENTRATION DECIDED FALSE.  For every fixed eta in (0, ln(3/2)/2),
         #{sigma : |Phi^{-1}(sigma)| >= e^{eta N} M / L}  =  e^{Theta(N)},
      and   min over thresholds T_h of ( #{fiber >= T_h} + max{fiber < T_h} )
         =  e^{Theta(N)},   N = |T| = 2B.
      The profile is a dense exponential staircase (fibers 2^{B-s} at every
      exponential scale, with C(B,s)2^s of each): no threshold gives few heavy
      fibers AND subexponential light fibers.  #732's concentration hypothesis
      FAILS; #732 Prop 3.1's cardinality obstruction is realized by the ACTUAL
      atlas family, not an adversarial synthetic profile.  Intuition inverted:
      heavy fibers are exponentially ABUNDANT, not rare.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Every number below is
recomputed with exact integer arithmetic by
`experimental/scripts/verify_staircase_concentration_sidon_paired.py` (stdlib
only, deterministic, `RESULT: PASS (88/88)`, `--tamper-selftest` catches `3/3`,
< 0.1 s).  Brute-force fiber enumeration on four Sidon-paired domains (two
superincreasing `3^i`, `5^i`; two non-superincreasing Conway--Guy sets) is
cross-checked against the closed-form profile; the concentration counts are
tabulated to `B = 256` from the exact formula.  Machine-readable certificate:
`experimental/data/certificates/staircase-concentration-sidon-paired/staircase_concentration_sidon_paired.json`.
Lean statement stub: `experimental/lean/staircase_concentration_sidon_paired/`
(`lake build` succeeds; `native_decide` instances, no `sorry`, no mathlib).
No `.tex`/`.pdf` is edited.

## Interfaces

- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`).  The
  whole target is his: the **charge-preserving semantic-or-signed dichotomy**
  (Sec 6) with its "at most `e^{o(N)}` rooted packets" requirement, and
  **Prop 6.1** (the dichotomy implies same-owner semantic emission on a
  failure).  The residual clause this packet decides is exactly the packet-count
  bound his Sec 6 states as "part of the theorem": the number of packets must be
  subexponential.  We show that on the Sidon-paired class the natural
  (fiber-indexed) packet count is provably exponential.
- **#717**
  (`experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md`).  Its
  depth-`R` locator/power-sum prefix chart (`eq:exact-power-sum-map`,
  `M = C(N,a)`), its Johnson bound (Thm 4.1), and its **Sec 7 superincreasing
  witness** (`A_i = 5^i`, `C = 2 sum A_i + 1`, `T = {A_i} u {C-A_i}`, `a=B`,
  `Phi = sum`) are the exact chart and ground-truth scalars (`W = C(B,B/2)`,
  `L = (3^B+1)/2`) recovered here as the `s=0` term of the exact profile.
- **#729**
  (`experimental/notes/thresholds/general_pruned_signed_bound.md`).  Its density
  criterion `q_+(chart) = 1/(3/2 - logM/logL)` and layer-cake piece-split are
  the machinery whose piece count this packet computes exactly.  For this family
  `logM/logL = 2 log2 / log3 = 1.2619`, so `q_+ = 1/(3/2 - 1.2619) = 4.199`
  (matching #728/#729's asymptotic `q_+ = 4.199`): the signed clause is
  discharged for pruned pieces at `q <= 4.199`, but the LIGHT part of this
  profile is not subexponentially pruned (part 3).
- **#732**
  (`experimental/notes/thresholds/charge_preserving_split_decomposition.md`).
  Its **Theorem B** ("the split is #716's decomposition IFF the positive profile
  is staircase-concentrated") and its **Prop 3.1** ("a heavy fiber + flat
  exponential tail forces `min_{T_h} pieces = e^{Omega(N)}`") are the precise
  statement and obstruction this packet resolves.  Theorem A (fourth condition
  free) and the per-piece charge conditions are unaffected -- they are correct;
  it is the GLOBAL concentration hypothesis, which #732 left open (and its
  Sec 3/5 prose called the superincreasing family "concentrated", on the
  strength of small-`B` tables `B <= 8`), that we DECIDE -- negatively.  The
  small-`B` appearance of concentration is a crossover artifact (Sec 4).
- **#735**
  (`experimental/notes/thresholds/heavy_fiber_planted_emission.md`).  Its
  **Theorem 2** (central fiber `Phi^{-1}((B/2)c)` = the `C(B,B/2)` complete
  twin-pair unions, for any distinct-subset-sum `P`) is the `s=0` slice of the
  exact profile here and is re-verified on all four domains.  Its scope note --
  "per-fiber emission is closed; the GLOBAL profile count remains #732's open
  max-fiber question" -- is exactly the question this packet answers.

Classical facts used (named, not re-derived): a distinct-subset-sum
(dissociated) set has all `2^B` subset sums distinct, equivalently
`sum eps_i A_i = 0` with `eps in {-1,0,1}^B` forces `eps = 0`; the strictly
stronger **B[+-2]** property (`sum delta_i A_i = 0`, `delta in {-2,...,2}^B`
forces `delta = 0`) is implied by 2-superincreasing growth and is what upgrades
the lower bound to the exact formula.

---

## 1. Setup and the pair-coordinate parametrization

Fix `P = {A_1, ..., A_B}` distinct-subset-sum over `Z`, `c > 2 sum P`, and

```text
T = P u (c - P),   |T| = 2B,   a = B,   Phi(S) = sum_{t in S} t   (over Z).
```

Twin pairs are `{A_i, c - A_i}`, `i in [B]`.  A support `S` (an `a`-subset of
`T`, `M = C(2B,B)` of them) meets pair `i` in one of four ways, giving a
4-coloring of `[B]`:

```text
E (empty),  X (low-only: A_i in S),  Y (high-only: c-A_i in S),  W (both).
```

Write `n_0=|E|, n_L=|X|, n_H=|Y|, n_B=|W|`.  Size `a=B` gives
`n_L + n_H + 2 n_B = B`, and with `n_0 = B - n_L - n_H - n_B` this forces
`n_0 = n_B` (`#empty = #both`).  The syndrome is

```text
Phi(S) = (n_H + n_B) c  +  ( sum_{i in X} A_i  -  sum_{j in Y} A_j ),
```

because a `both` pair contributes `A_i + (c - A_i) = c` (its `A_i` cancels), a
`high-only` pair contributes `c - A_j`, a `low-only` pair contributes `A_i`.
Set `k = n_H + n_B` (the c-count) and `D = sum_X A - sum_Y A` (the **signed
unpaired residual**).  Since `|D| <= sum P < c/2`, the pair `(k, D)` is read off
`sigma = kc + D` uniquely: `k = round(sigma/c)`, `D = sigma - kc`.  Encode
`(X,Y)` by `eps in {-1,0,1}^B` (`eps_i = +1` on `X`, `-1` on `Y`, `0` on
`E u W`); then `D = sum_i eps_i A_i` and `|supp eps| = n_L + n_H = s`, the
**unpaired count**.  The counting constraint fixes `n_B = (B - s)/2` and
`k = (B + n_H - n_L)/2`; in particular `s == B (mod 2)`.

---

## 2. The exact fiber-size classification (Theorem 1, PROVED)

### Theorem 1 (exact profile, B[+-2] base)

Let `P` be **B[+-2]-dissociated** (`sum delta_i A_i = 0`, `delta in {-2,..,2}^B`
=> `delta = 0`; implied by `A_i > 2 sum_{j<i} A_j`).  Then for every syndrome
`sigma` with fiber support pattern of unpaired count `s`,

```text
|Phi^{-1}(sigma)| = C(B - s, (B - s)/2),
```

and the number of syndromes with unpaired count `s` is `C(B, s) 2^s` (`s == B`
mod 2, `0 <= s <= B`).  Consequently

```text
L = sum_{s == B (2)} C(B,s) 2^s = (3^B + 1)/2,      M = sum_s [C(B,s)2^s] C(B-s,(B-s)/2) = C(2B,B).
```

**Proof.**  Fix `sigma <-> (k, D) <-> eps`.  By B[+-2]-dissociativity the value
`D = sum eps_i A_i` determines `eps` uniquely, hence `X = {eps=+1}` and
`Y = {eps=-1}` (so `n_L, n_H`, and `s = |supp eps|`) are **forced**; the only
freedom left in a support with syndrome `sigma` is which `n_B = (B-s)/2` of the
remaining `B - s` pairs are `both` (`W`) versus `empty` (`E`).  That is
`C(B-s, (B-s)/2)` supports.  (Uniqueness of `eps` given `D`: two disjoint
`(X,Y), (X',Y')` with equal signed sum give `delta_i = [X]-[Y]-[X']+[Y'] in
{-2,..,2}`, so B[+-2] forces `(X,Y)=(X',Y')`.)  Distinct `eps` give distinct
`(k,D)` hence distinct `sigma`, so the level-`s` syndrome count is
`#{eps : |supp eps| = s} = C(B,s)2^s`.  The two identities are then
`sum_s C(B,s)2^s = 3^B` split by parity `(=> (3^B+1)/2` for `B` even), and
`sum_{a-subsets} 1 = C(2B,B)`.  `square`

The `s = 0` term is the central fiber `C(B, B/2)` = #735 Thm 2 = #717 Sec 7's
`W`.  **Verification** (BLOCK A): brute-force enumeration for `A_i in {3^i, 5^i}`,
`B in {2,4,6,8}`, matches the size-multiplicity table exactly, e.g. `B=6`:
`{fiber 1: x64, 2: x240, 6: x60, 20: x1}`, `L=365`, `M=924`, central `= 20 =
C(6,3)`.

**The staircase.**  Fiber sizes are `2^{B}, 2^{B-2}, ...` (up to the standard
`C(2m,m) ~ 2^{2m}/sqrt(pi m)` factor) -- one at every even step down the
exponential scale, with `C(B,s)2^s` syndromes each.  The mean fiber is
`M/L ~ 2 (4/3)^B / sqrt(pi B)`, so fiber `>= M/L` iff `s <= B ln(3/2)/ln 2
= 0.585 B` (Sec 4).

---

## 3. Robust lower bound for every Sidon-paired P (Theorem 2, PROVED)

Non-superincreasing distinct-subset-sum sets are **not** B[+-2] (e.g.
`{3,5,6,7}`: `5-3 = 7-5`), so `D` no longer determines `eps` and some fibers
MERGE and grow.  The clean staircase is a lower bound.

### Theorem 2 (planted lower bound, any distinct-subset-sum P)

For `P` distinct-subset-sum and any `s` with `s == B (mod 2)`, `0 <= s <= B`, and
any `R subset [B]` with `|R| = s`, the syndrome

```text
sigma_R = ((B - s)/2) c  +  sum_{i in R} A_i
```

has `|Phi^{-1}(sigma_R)| >= C(B - s, (B - s)/2)`, and the `C(B, s)` syndromes
`{sigma_R : |R|=s}` are pairwise distinct.

**Proof.**  Take `X = R` (each `i in R` low-only), `Y = empty`, and any
`(B-s)/2`-subset of the remaining `B - s` pairs as `W` (`both`), the rest `E`.
Each is an `a=B` support with syndrome `((B-s)/2)c + sum_R A = sigma_R`; there
are `C(B-s,(B-s)/2)` of them.  Distinctness: `sigma_R = sigma_{R'}` with
`|R|=|R'|=s` forces (equal c-count, `|.|<c/2`) `sum_R A = sum_{R'} A`, hence
`R=R'` by distinct subset sums.  `square`

**Verification** (BLOCK B): for the Conway--Guy sets `{3,5,6,7}` (`B=4`) and
`{11,17,20,22,23,24}` (`B=6`) and base `2^i` (all distinct-subset-sum, none
B[+-2]): the central fiber is `C(B,B/2)` (re-verifies #735 Thm 2), the
`sigma_R` bound and distinctness hold, and each carries EXTRA intermediate
fibers above the clean staircase (`{3,5,6,7}` profile
`{1:x8, 2:x10, 3:x6, 4:x2, 5:x2, 6:x1}`, `L=29 < 41`) -- i.e. LESS concentrated,
never more.

---

## 4. Concentration is DECIDED FALSE (Theorem 3, COUNTEREXAMPLE)

Staircase-concentration (#732 Thm B.2) asks for a threshold `T_h` with BOTH
`#{sigma in b_+ : f(sigma) >= T_h} = e^{o(N)}` AND `max{f(sigma) : sigma in b_+,
f(sigma) < T_h} = e^{o(N)}`, where `f(sigma) = |Phi^{-1}(sigma)|`, `N = |T| = 2B`,
and `b_+` is the positive-rooted packet `f|_{omega_s>0}` (#732 Sec 1).
Equivalently the target theorem, on `f`: for every `eta > 0`,
`#{sigma : f(sigma) >= e^{eta N} M/L} = e^{o(N)}`.

**Scope of the decision (full profile vs. rooted `b_+`).**  Theorems 1-3 below
concern the FULL-chart profile `f = {|Phi^{-1}(sigma)|}` -- which is exactly
#732 **Prop 3.1**'s "positive fiber-size profile" and the object #732/#735
defer as "the GLOBAL profile count / #732's open max-fiber question" (#735
Nonclaims).  That object is decided here UNCONDITIONALLY (Thm 3).  #732 **Thm
B.2** adds the rooting restriction `sigma in b_+` (`omega_s>0`); the refutation
transfers to it for any rooting that retains a constant fraction of each
unpaired level `s` (the generic case, since a genuine failure `R_A(f) >= e^{eta
N}` needs `g` to correlate with the heavy structure, so `omega_s>0` on a
constant fraction of syndromes).  A fully rooting-independent refutation of Thm
B.2's exact quantifier -- ruling out EVERY admissible dual `g` whose `b_+`
happens to be concentrated -- is not claimed (Nonclaims); note that such a `g`
would already hand the dichotomy its semantic packet, so it is not an obstruction
to the dichotomy, only to this literal reading of Thm B.2.

### Theorem 3 (non-concentration, PROVED for B[+-2]; lower-bounded for all P)

For the B[+-2] class, and hence (Thm 2) for every distinct-subset-sum P:

```text
(a)  for every fixed eta in (0, ln(3/2)/2),
        #{sigma : f(sigma) >= e^{eta N} M/L}  =  e^{Theta(N)};
(b)  min over T_h of ( #{f >= T_h} + max{f < T_h} )  =  e^{Theta(N)}.
```

Both quantities are `e^{Theta(N)}`, not `e^{o(N)}`: the profile is NOT
staircase-concentrated, and #732 Theorem B.2's hypothesis is false on this
class.

**Proof (a).**  `f = C(B-s,(B-s)/2) ~ 2^{B-s}` and `M/L ~ 2(4/3)^B/sqrt(pi B)`,
so `f >= e^{eta N} M/L` iff `s <= s*(eta) := [B ln(3/2) - eta N]/ln 2 + O(log B)`
(`N=2B`); for `eta < ln(3/2)/2` this cutoff is `Theta(B) > 0`.  The count is
`sum_{s <= s*} C(B,s)2^s`, whose summand `C(B,s)2^s` increases up to `s = 2B/3`,
so for `s* < 2B/3` the sum is `Theta(C(B,s*)2^{s*}) = e^{Theta(B)}`.  (For
`eta >= ln(3/2)/2` there are NO heavy fibers, `= 0`; the theorem's "for every
`eta`" quantifier is refuted by any small `eta`.)  **Proof (b).**  Fibers are
strictly decreasing in `s`, so a threshold cuts at some `s_0`:
`#{f >= T_h} = sum_{s<=s_0} C(B,s)2^s` and `max{f<T_h} = 2^{B-s_0-2}(1+o(1))`.
The first term is `>= 2^{(H_2(s_0/B)+s_0/B)B}` (bits), the second
`>= 2^{B-s_0-O(log B)}`; their max is minimized near `H_2(beta)=1-2beta`
(`beta = s_0/B ~ 0.17`), giving `e^{Theta(B)}` at the balance and larger away
from it.  `square`

**Verification** (BLOCK C, exact formula to `B=256`).  `log2(#heavy)/B` and
`log2(minPieces)/B` stay bounded below by positive constants and rise toward
their limits, so neither is `e^{o(N)}`:

```text
 B     log2(M/L)   log2(#heavy, eta=.05)   rate    log2(minPieces)   rate
 8       1.97              6              0.750           4          0.500
 16      4.80             19              1.188          10          0.625
 32     10.95             42              1.313          23          0.719
 64     23.73             88              1.375          49          0.766
128     49.80            178              1.391         102          0.797
256    102.42            361              1.410         207          0.809
```

`minPieces(256) = 2^{207} > 256^{20}` and `#heavy(256,.05) = 2^{361} > 256^{20}`
(BLOCK C witnesses): both exceed any fixed polynomial in `N`.  Brute-force
`#heavy` matches the formula at `B in {4,6,8}` (BLOCK C consistency).

**Why the intuition inverts.**  One expects heavy fibers to be rare (few
syndromes where many configurations "stack").  Here fiber size depends ONLY on
the unpaired count `s`, and there are `C(B,s)2^s` syndromes at each `s`;
moderately-unpaired syndromes (`s = Theta(B)`) are exponentially NUMEROUS AND
carry exponentially LARGE fibers `2^{B-s}`.  Heavy fibers are abundant, which is
exactly why no threshold separates "few heavy" from "small light".  This is
#732 Prop 3.1's obstruction (`min(K,D)+1` pieces), realized by the actual atlas
family with `(K,D)` spread across the whole staircase rather than a single
plateau.

**Small-`B` crossover.**  At `B <= 8` the profile looks concentrated: `B=8`,
`eta -> 0` gives `#heavy = 113` and `minPieces = 21 = 1 + C(6,3)` (matching
#732 Sec 5's `1 + (a-2)`-scale tail), so the exponential growth is not yet
visible.  It is a crossover: by `B=32`, `minPieces = 2^{23}`.  #732's "the
superincreasing family is concentrated" reads off the pre-crossover table; the
asymptotics reverse it.

---

## 5. Consequence for the dichotomy (the composition does NOT close via this route)

The intended payoff was a composition corollary: **#729** (pruned pieces pay the
signed clause) + **#732** Thm A/B (four-condition decomposition) + **#735**
Thm 2 (semantic emission on the heavy fibers) + **this packet** (concentration)
`=>` the charge-preserving semantic-or-signed dichotomy, PROVED end-to-end on
the Sidon-paired depth-1 class.  Theorem 3 shows the last link is FALSE:

> **Corollary (route-cut, PROVED).**  On the Sidon-paired depth-1 class
> (`T = P u (c-P)`, `P` distinct-subset-sum, `a=B`, `c>2 sum P`, `Phi` = subset
> sum over `Z`, `q` in `[2, 4.199]`), the heavy/light + layer-cake split of
> #729/#732 does NOT realize #716 Sec 6's "at most `e^{o(N)}` packets": for any
> threshold the piece count is `e^{Theta(N)}` (Thm 3b).  Hence the
> #729/#732/#735 chain does not compose to a proof of the dichotomy on this
> class via that decomposition.

**The hypothesis union that WOULD have been required** (had concentration held),
printed in full so the missing link is visible: `P` distinct-subset-sum;
`c > 2 sum P`; depth-1 subset-sum chart over `Z`; `a = B`; `q in [2, q_+]` with
`q_+ = 1/(3/2 - logM/logL) = 4.199` (**#729** density criterion); positive
rooting `omega_s = Re conj((P_A g)(s))` with `||g||_{q'}=1` (**#716** Sec 2);
`(H1)-(H4)` heavy-fiber admissibility (**#717** Thm 5.1); four charge conditions
with band `A` (**#732** Thm A); **and** staircase-concentration of the positive
profile (**#732** Thm B.2) -- the one clause this packet shows is unsatisfiable
here.  What remains open is whether a DIFFERENT decomposition (not fiber-indexed
heavy/light) closes the dichotomy on this class -- e.g. routing the
moderately-unpaired fibers through the signed clause at `q <= 4.199` rather than
as semantic packets.  That is outside this packet (Nonclaims).

---

## 6. Boundary (honest scope)

- **`a != B`.**  The `n_0 = n_B` identity and the `C(B-s,(B-s)/2)` formula are
  `a=B`-specific.  Computed `a = B +- 2` profiles (BLOCK D) are still
  non-concentrated staircases whose `minPieces` grows (`a=B-2`: `16` at `B=8`,
  `57` at `B=10`), consistent with the same mechanism, but no `a != B` proof is
  claimed.  (Complementation `S <-> T\S` makes `a` and `2B-a` mirror images.)
- **General involution-symmetric `T`** (`T = c - T`, `P` NOT distinct-subset-sum).
  The central-fiber and staircase structure require the dissociativity of `P`;
  without it the `sigma_R` need not be distinct and fibers merge further.  The
  non-concentration only becomes stronger (larger fibers), but the exact formula
  and the clean `C(B,s)` distinct-`sigma_R` count are not claimed.
- **`Z` vs `Z_c`.**  Worked over `Z` (large `c`, no wraparound).  Over `Z_c`
  some syndromes are identified, only MERGING fibers -- concentration cannot
  improve.  `Z` is the conservative setting for a non-concentration claim.
- **`q > q_+ = 4.199`.**  The signed-clause discharge (#729) is only stated for
  `q <= q_+`; the route-cut Corollary is stated in that range.

## Nonclaims

- **NOT** a proof or refutation of #716's dichotomy itself.  We refute the
  #729/#732/#735 heavy/light-split ROUTE to it on this class (the concentration
  hypothesis is false); an alternative decomposition is not ruled out.
- The decision is UNCONDITIONAL for the full-chart profile `f` (#732 Prop 3.1's
  object).  For #732 Thm B.2's rooting-restricted count (`sigma in b_+`), the
  refutation is stated for rootings retaining a constant fraction per level; a
  proof that NO admissible dual `g` concentrates `b_+` is not claimed (Sec 4).
- **NOT** a correction to #732 Theorem A/B or its per-piece charge conditions
  (those are correct); only #732's Sec 3/5 prose calling the superincreasing
  family "concentrated" is overturned, as a small-`B` crossover artifact.  The
  quantitative Theorem B.2 IFF is exactly what we evaluate.
- **NOT** a proof of primitive Q / max-fiber flatness in general, A4, the signed
  minor-arc/Sidon inverse, or the Proximity Prize.  This is one class's
  max-fiber count, decided.
- Theorem 1 (exact formula, B[+-2]), Theorem 2 (lower bound, all
  distinct-subset-sum), Theorem 3 (non-concentration) are PROVED (elementary
  dissociativity + binomial asymptotics, reproduced by the verifier); the
  `a != B` and general-involution statements are EXPERIMENTAL boundary reports.
- Finite brute force is exhaustive only for `B <= 8`; the closed-form profile,
  the `q_+` value, and the concentration asymptotics are closed-form and
  tabulated to `B = 256`.

## Consumers

- **#716** (`primitive_signed_payment_barrier_v1.md` Sec 6 / Prop 6.1): the
  packet-count clause is decided negatively on the Sidon-paired class; a
  fiber-indexed decomposition cannot meet "`<= e^{o(N)}` packets" there.
- **#732** (`charge_preserving_split_decomposition.md`): its Theorem B.2 IFF is
  evaluated and its open branch (concentration when `L=e^{Theta(N)}`) is
  resolved FALSE for this family; Prop 3.1's obstruction is exhibited as
  realized, and the Sec 3/5 "concentrated" prose is corrected (crossover).
- **#735** (`heavy_fiber_planted_emission.md`): its Thm 2 central fiber is the
  `s=0` slice of the exact profile; its deferral of "the GLOBAL profile count"
  to #732's max-fiber question is answered (exponential).
- **#729** (`general_pruned_signed_bound.md`): `q_+ = 4.199` is recomputed; the
  light part of this profile is identified as the un-prunable (heavy-fiber)
  residual its Sec 3 flags.
- `asymptotic_rs_mca_frontiers.tex`: paste-ready as the counter-remark after
  #732's decomposition proposition -- on the Sidon-paired class the max-fiber
  profile is an exponential staircase, so the concentration hypothesis must be
  imported as a genuine (and here false) assumption, not inferred.
- Lean statement stub: `experimental/lean/staircase_concentration_sidon_paired/`
  (exact fiber formula `C(B-s,(B-s)/2)`, level count `C(B,s)2^s`, `L=(3^B+1)/2`,
  and the exponential `minPieces` lower bound; statements only, `lake build`
  succeeds, no `sorry`).

## Reproducibility

```bash
python3 experimental/scripts/verify_staircase_concentration_sidon_paired.py
# -> RESULT: PASS (88/88)
python3 experimental/scripts/verify_staircase_concentration_sidon_paired.py --tamper-selftest
# -> tamper-selftest: caught 3/3 ; then RESULT: PASS (88/88)
cd experimental/lean/staircase_concentration_sidon_paired && lake build
# -> Build completed successfully
```
