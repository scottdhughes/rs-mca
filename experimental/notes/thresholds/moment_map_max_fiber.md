# The degree-2 moment-map max-fiber rate is log 2

## Status

`R1 SETUP (AUDIT from #643/#623) / R2 phi* = log 2 PROVED — the question
"is phi* < log 2?" is DECIDED: NO / R3 EXACT CENSUS fstar(interval,b) to b=36,
three-level pigeonhole chain (COMPUTED) / R4 POLY-LOSS RECONCILED: fstar =
Theta(2^b / b^{9/2}), local-CLT + det G = b^9/2160 (MEASURED; effective
exponent ~5 over b<=36) / R5 CONSEQUENCE FOR #643's BRACKET: rho* <= phi* = log2
is tight at the top; the phi*-route to a sub-log2 rho* upper bound is DEAD
(PROVED)`.

This packet takes the **named open wall** of our just-shipped PR #643
(`pte_cluster_packing_frontier.md`, R4.4): *bound `phi* = sup_b (log fstar)/b`,
the max exponential fiber-growth rate of the degree-2 moment map; is it
`< log 2`?* #643 left the bracket `phi* in [0.1932, log 2]` open and conjectured
`phi*` was "a moderate finite constant, plausibly ~0.18-0.25."

**One-line verdict. `phi* = log 2` exactly.** The answer to "is `phi* < log 2`?"
is **NO**; a sub-`log2` upper bound is impossible. #643's "moderate constant"
reading is **REFUTED**: the plain interval `{0,1,...,b-1}` already gives
`phi(b) = 0.1932, 0.2677, 0.3003, 0.3534` at `b = 16, 24, 28, 36` — monotone,
no plateau — and an **elementary pigeonhole bound proves `phi(interval,b) ->
log 2`** at rate `>= log2 - 6(ln b)/b`. The measured "moderate" values were a
pre-asymptotic artifact: the deficit is only **polynomial**
(`fstar = Theta(2^b / b^{9/2})`, a `b^{-9/2}` loss, not an exponential one),
so `phi(b) -> log 2` glacially, `~ log2 - (9/2)(ln b)/b`.

Every number below is recomputed by
`experimental/scripts/verify_moment_map_max_fiber.py` (stdlib-only, zero-arg,
`RESULT: PASS (39/39)`, runtime ~12 s under `ulimit -v 2097152`). Exact `fstar` beyond
`b=30` (to the `b=36` memory ceiling; `b=38` exceeds 2 GB) lives in
`experimental/scripts/repro_moment_map_max_fiber.py` (documented runtime). The
`R2` proof needs **no** computation — it is closed-form and elementary.

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exhaustive
exact enumeration), **MEASURED** (exact finite objects, limit/rate read off or
supported by a stated-but-not-fully-verified theorem), **REFUTED**, **AUDIT**
(cross-reference), **OPEN**.

**Credit.** Built directly on **our #643** (`pte_cluster_packing_frontier.md`:
the `phi*` wall itself, Lemma C `fstar <= 2^{b-3}`, Prop D `rho <= phi =>
rho* <= phi*`, `fstar` super-multiplicativity / Fekete, and the measured
`phi(b)` sequence `0.0866..0.1932`) and **our #623**
(`pte_extremality_image_face.md`: the degree-2 moment map
`Phi(S) = (|S|, sum S, sum S^2)` and its fiber algebra). The minimal degree-2
PTE trade support 6 is **scottdhughes #564** (`w_a_star_pte_lemma.md`); it is
cited for context but **not used** — the `R2` proof does not go through trades.
The linear-form anticoncentration context (distinct integers force only a
*polynomial* max atom for `sum eps_i v_i`) is the classical **Erdos-Moser /
Sarkozy-Szemeredi** circle; the `R4` local-limit refinement invokes the standard
multidimensional lattice local CLT (Bhattacharya-Rao, *Normal Approximation and
Asymptotic Expansions*).

---

## R1 — setup (AUDIT extraction from #643/#623)

A **block** is a set `V = {v_1,...,v_b}` of `b` distinct integers. For `S ⊆ V`
the **signature** under the degree-2 moment map is
```
    sig(S) = ( w, s, q ) = ( |S|,  sum_{x in S} x,  sum_{x in S} x^2 ).
```
Its **fibers** partition the `2^b` subsets. The **max fiber** and the two rates
are
```
    fstar(V) = max_{(w,s,q)} #{ S ⊆ V : sig(S) = (w,s,q) },
    phi(V)   = (log fstar(V)) / b ,     phi(b) = max_{|V|=b} phi(V) ,
    phi*     = sup_b phi(b) .
```
`phi*` is a genuine supremum-equal-limit: `fstar` is super-multiplicative under
the no-carry tensor product (`F(b1+b2) >= F(b1) F(b2)`, `F(b)=max_{|V|=b}
fstar(V)`, #643 / Fekete), so `phi* = lim_b phi(b)` (AUDIT, #643). Affine maps
`x -> ax+b` (`a != 0`) preserve `fstar` (#643 Lemma A), so `phi` depends only on
the affine class of `V`.

Prior state (#643): `fstar(V) <= 2^{b-3}` (Lemma C, codim-3 slice) gives
`phi(b) <= (1-3/b) log 2 -> log 2`; trivial recursions `fstar(b) <= 2 fstar(b-1)`
and Littlewood-Offord `fstar <= C(b, b/2)` also give only `-> log 2`; measured
`phi(b) = 0.0866, 0.1493, 0.1775, 0.1932` at `b = 8,12,14,16` (increasing lower
bounds from a symmetric diameter-capped search). **Open:** is `phi* < log 2`?

---

## R2 — Theorem: `phi* = log 2` (PROVED)

> **Theorem.** `phi* = log 2`. Equivalently, the max exponential fiber-growth
> rate of the degree-2 moment map equals `log 2`; there is **no** sub-`log2`
> upper bound.

The proof is a two-line squeeze. The upper half is trivial; the lower half is a
pigeonhole against the **polynomial** signature box of a dense block.

**Upper bound (ceiling).** Every block has `fstar(V) <= 2^b` (there are only
`2^b` subsets), so `phi(b) <= log 2` for every `b`, hence `phi* <= log 2`.
(#643's Lemma C sharpens this to `phi(b) <= (1-3/b)\log 2`; either suffices.)

**Lower bound (the new input).** Fix the **interval block** `V_b = {0,1,...,b-1}`.
Every subset `S ⊆ V_b` has a signature `(w,s,q)` confined to the integer box
```
    0 <= w <= b ,   0 <= s <= sum_{i<b} i = b(b-1)/2 ,
    0 <= q <= sum_{i<b} i^2 = (b-1)b(2b-1)/6 .
```
Hence the number of *distinct* signatures satisfies
```
    L1(V_b) <= B(b) := (b+1)( 1 + b(b-1)/2 )( 1 + (b-1)b(2b-1)/6 ).     (box)
```
The `2^b` subsets fall into at most `L1(V_b) <= B(b)` fibers, so by pigeonhole
**some** fiber has at least the average size:
```
    fstar(V_b)  >=  2^b / L1(V_b)  >=  2^b / B(b) .                     (phole)
```
Now `B(b)` is a fixed cubic-times-quadratic-times-linear polynomial. Bounding
each factor for `b >= 2` (`1 + b(b-1)/2 <= b^2/2`, `1 + (b-1)b(2b-1)/6 <= b^3/3`,
and `(b+1) b^5 / 6 < b^6`) gives the clean closed form
```
    B(b)  <=  (b+1) b^5 / 6  <  b^6           (all b >= 2).            (Bbound)
```
Therefore, for every `b >= 2`,
```
    fstar(V_b) > 2^b / b^6,      phi(V_b) = (log fstar(V_b))/b  >  log 2 - 6 (ln b)/b.
```
Since `6(ln b)/b -> 0`, `phi(V_b) -> log 2`, so
`phi* = sup_b phi(b) >= limsup_b phi(V_b) = log 2`.

Combining, `log 2 <= phi* <= log 2`, i.e. **`phi* = log 2`.** ∎

**Two remarks on the proof.**

1. *Nothing is special about the interval except that it minimizes the box.*
   Among `b` distinct non-negative integers, `{0,...,b-1}` simultaneously
   minimizes `sum v` and `sum v^2`, hence minimizes `B(b)` — it is exactly the
   block giving the **strongest** pigeonhole lower bound. The same argument runs
   for any block of diameter `O(b)`: `B = O(b^6)`, so `phi -> log 2`. Density,
   not any trade structure, is what forces the rate up.

2. *The bound is honestly loose but the rate is right.* `(phole)` uses only that
   the codomain box is polynomial; it ignores that fibers are far from equal.
   The true `fstar` is polynomially larger than `2^b/L1` and the true `L1` is
   polynomially smaller than `B(b)` — see R3/R4 — but all three quantities share
   the exponential rate `log 2`, which is all the theorem needs.

**Consequence (decides #643's wall and conjecture).**
`phi* = log 2` **REFUTES** the hope of a sub-`log2` upper bound and **REFUTES**
#643's census-backed conjecture that `phi*` is "a moderate finite constant
~0.18-0.25." The bracket `[0.1932, log 2]` collapses to the single point
`log 2` at the top.

---

## R3 — exact census and the three-level chain (COMPUTED)

Exact `fstar(V_b)`, `L1(V_b)` by the signature DP (verifier BLOCK 2/3; `b<=30`
in the verifier, `b<=36` in the repro — `b=38` exceeds the 2 GB cap at ~42 s,
the honest exact ceiling). The proof's three quantities are all exhibited and
the chain `2^b/B(b) <= 2^b/L1 <= fstar <= 2^{b-3}` is checked to hold exactly:

| b | fstar(interval) | L1(interval) | B(b) box | 2^b/B(b) | 2^b/L1 | phi(b)=log fstar/b |
|---|-----------------|--------------|----------|----------|--------|--------------------|
| 8  | 2      | 247       | 36 801     | ~0.0   | 1.04    | 0.0866 |
| 12 | 5      | 3 067     | 441 597    | ~0.0   | 1.34    | 0.1341 |
| 16 | 22     | 23 635    | 2 552 737  | ~0.0   | 2.77    | 0.1932 |
| 20 | 98     | 110 627   | 9 911 181  | 0.11   | 9.48    | 0.2292 |
| 24 | 617    | 372 727   | 29 950 625 | 0.56   | 45.0    | 0.2677 |
| 28 | 4 481  | 1 014 423 | 76 178 621 | 3.52   | 264.6   | 0.3003 |
| 32 | 36 410 | 2 380 489 | ~1.71e8    | 25.1   | 1 804   | 0.3282 |
| 36 | 334 669| 5 008 473 | ~3.48e8    | 197.4  | 13 721  | 0.3534 |

Read-offs (all COMPUTED):

- **`phi(interval,b)` is monotone increasing with no plateau**, `0.0866 ->
  0.3534` across `b = 8..36`, already `> 0.35` — decisively past #643's
  "~0.18-0.25" ceiling, and it agrees *exactly* with #643's measured champions
  at `b=8` (`0.0866`) and `b=16` (`0.1932`), so the interval is the natural
  max-fiber family (it is not optimal at every `b` — at `b=12` a hole-block
  reaches `fstar=6 > 5` — but it is a valid witness and that is all R2 needs).
- **The rigorous pigeonhole `2^b/B(b)` becomes non-vacuous at `b=28`** (value
  `3.52 > 1`) and climbs (`197` at `b=36`); its exponent
  `log(2^b/B(b))/b = log2 - (log B(b))/b` rises through `0.045, 0.101, 0.147` at
  `b=28,32,36`, tracking toward `log 2` exactly as the theorem predicts (slowly,
  because `B(b) ~ b^6/6`).
- **The chain `2^b/B(b) <= 2^b/L1 <= fstar <= 2^{b-3}` holds at every tested
  `b`** (verifier asserts each inequality), exhibiting the theorem's squeeze on
  exact objects.

The max fiber sits at the **central weight `w=b/2`** (two symmetric argmax
fibers, e.g. `b=16`: `fstar=22` at `(8,64,680)` and its reflection) — the
central-lattice-point picture that R4 quantifies. (MEASURED structure.)

---

## R4 — reconciliation: poly-loss, not exponential-defect (MEASURED)

This is the single reconciliation #643 flagged as most valuable: do the small-`b`
measurements (`phi ~ 0.19`) reflect an **exponential defect** (`phi -> c < log2`)
or a slowly-vanishing **polynomial loss** (`phi -> log2`)? R2 already proves it
is poly-loss. R4 pins the **exact polynomial exponent**.

**Claim (MEASURED / local-CLT).** `fstar(V_b) = Theta( 2^b / b^{9/2} )`, i.e. the
deficit `D_b := b\log2 - \log fstar(V_b) = (9/2)\ln b + O(1)`.

*Heuristic derivation.* Writing `S` via indicators `eps_i in {0,1}` uniform,
`fstar/2^b` is the **max atom** of the joint law of
`X = sum_i eps_i (1, i, i^2) in Z^3`. This is a sum of independent, uniformly
bounded (after the `x=b t` rescaling) lattice vectors with covariance
`Sigma = (1/4) G`, where `G_{jk} = sum_{i<b} i^{j+k}` (`j,k in {0,1,2}`). Two
exact facts (verifier BLOCK 4):

- **`det G = b^9 / 2160 * (1 + o(1))`.** With `i ~ b t` one has
  `G_{jk} ~ b^{j+k+1}/(j+k+1)`, so `G ~ b * D H D` with `D=diag(1,b,b^2)` and `H`
  the `3x3` Hilbert matrix `H_{jk}=1/(j+k+1)`, `det H = 1/2160`. The exact ratio
  `det G / (b^9/2160)` is `0.985, 0.996, 0.9991, 0.9998, 0.99994` at
  `b=20,40,80,160,320` — clean convergence to 1.
- **Covolume of the increment lattice `L = <(1,i,i^2)>` is 2** (verifier:
  `gcd` of `3x3` minors `= 2` for `b=4,6,8,10`), the single congruence
  `q ≡ s (mod 2)` (from `i^2 ≡ i mod 2`).

The multidimensional **local (lattice) CLT** for sums of independent uniformly
bounded integer vectors (standard; e.g. Bhattacharya-Rao) gives the max atom at
the mean lattice point as
```
    max atom  ~  covol(L) / ( (2 pi)^{3/2} sqrt(det Sigma) )
              =  2 / ( (2 pi)^{3/2} sqrt(det G / 64) ) ,
```
so `fstar(V_b) ~ 2^{b+4} / ((2 pi)^{3/2} sqrt(det G)) ~ (const) * 2^b / b^{9/2}`.

*Evidence.* The verifier compares `fstar` to this leading-order prediction: the
ratio `fstar / clt_pred` stays of order 1 across `b=8..36` (verifier bounds it in
`[0.9, 2.1]`; it drifts from `~1.8` down to `~1.1` as sub-leading terms settle),
and the `b^9`-scaling `b -> b+2` growth factor `4*(26/28)^{9/2} = 2.87` is matched
both by the CLT prediction (`2.86`, verifier BLOCK 4) and by the exact `fstar`
ratio (`4481/1552 = 2.89`), to `<1%`. A least-squares fit of the exact deficit
`D_b = b\log2 - \log fstar` against `alpha \ln b - beta` over `b=8..36` gives
`alpha ~ 5.0` (last-half `5.06`), consistent with the local-CLT `9/2 = 4.5` up
to the finite-range `O(1/\ln b)` correction and the off-center-lattice
fluctuation. Either value is a **bounded constant**, so `D_b = O(\ln b)` and
`phi(b) -> log 2`. (The exact `9/2` is not labeled PROVED — it needs a two-sided
lattice local-CLT with error control; see R6.)

**Reconciliation verdict (MEASURED, decisive): POLY-LOSS.** The `b<=16`
measurements looked like "a constant ~0.19" only because the `b^{-9/2}` factor
dominates until astronomically large `b`: the poly correction `(9/2)\ln b / b`
is `~0.78 > log 2` at `b=16`, so it swamps the rate entirely in the measured
range and only washes out as `~(\ln b)/b`. There is **no** exponential defect.

*Where the exponential loss would have had to come from (U2 answer).* For
distinct integers `v_i in {0,..,b-1}` the **linear** form `sum eps_i v_i` alone
has variance `~b^3/12`, so by a 1-D lattice local CLT its max atom is only
`~2^b b^{-3/2}` (the Erdos-Moser / Sarkozy-Szemeredi polynomial anticoncentration
for distinct values). Fixing the weight too, the `(w,s)`-fiber is `~2^b b^{-2}`
(covariance det `~b^4`); adding the **quadratic** coordinate `q = sum eps_i v_i^2`
is one more lattice dimension of scale `b^2` (covariance det jumps `b^4 -> b^9`),
which multiplies the max atom by only `~b^{-5/2}`, giving `~2^b b^{-9/2}`. Every
step is a **polynomial** factor — the second moment never buys an exponential
defect. The joint degree-2 fiber of a dense block is `2^b / poly(b)`; the
sub-`log2` hope had no mechanism.

---

## R5 — consequence for #643's `rho*` bracket (PROVED) + contrast (MEASURED)

**The `phi*`-route to a sub-`log2` `rho*` upper bound is DEAD.** #643 proved
`rho <= phi` (Prop D), hence `rho* <= phi*`. With `phi* = log 2` this says
`rho* <= log 2` is **exactly** the `phi*` ceiling and is **tight at the top** —
one cannot bound `rho*` below `log 2` by bounding `phi*`, because `phi* = log 2`.
Any sub-`log2` upper bound on the PTE-cluster packing rate `rho*` must therefore
come from the **deficit rate** `gamma = log2 - lambda` (the `L1` loss), *not*
from the max-fiber rate. This redirects #643's open wall: the interesting
quantity is `inf gamma` along the `rho`-optimizers, not `phi*` (now closed).
(PROVED, modulo #643's Prop D which we re-cite.)

`phi* = log2` does **not** move `rho*`'s lower bound: the interval has `L1` only
polynomial, so `lambda(V_b) = (\log L1)/b -> 0` and `rho(V_b) = phi + lambda -
log2 -> 0`. The interval maximizes `fstar` but is terrible for `rho`; the
`rho`-champion (#643's `b=14` block, `rho=0.156659`) is a different, spread-out
object. So #643's honest `rho*` bracket `[0.156659, log 2]` stands, with the
**upper end now identified as exactly `phi* = log 2`** and the lower end
untouched.

**Contrast family (MEASURED, why density is essential).** Spreading the points
kills `fstar`: for the **squares** `{0,1,4,...,(b-1)^2}` (diameter `~b^2`),
`phi(squares,b) = 0.0000, 0.0578, 0.0495, 0.0687` at `b=10,12,14,16` versus
`phi(interval,b) = 0.1099, 0.1341, 0.1713, 0.1932`. The squares' box `B` is
`~b^9` (`w * s * q ~ b * b^3 * b^5`, since `q <= sum i^4 ~ b^5`), larger than the
interval's `b^6` but still polynomial, so the squares *also*
have `phi -> log 2` eventually — but far more slowly. Density minimizes the box
and maximizes the pre-asymptotic rate; the interval is the extreme case.

---

## R6 — honest residuals (OPEN)

1. **The exact `9/2` exponent is MEASURED, not PROVED.** R2 gives the rate
   `log 2` rigorously and cheaply; the refinement `fstar = Theta(2^b/b^{9/2})`
   rests on the multidimensional lattice local CLT, whose two-sided form with
   uniform error control over the shrinking lattice cell I state but do not
   verify in full here. The exact-arithmetic evidence (det G ratio, growth-factor
   match, `alpha ~ 5`) is strong but the fitted exponent `~5.0` sits slightly
   above `4.5`, an unexplained finite-range gap (sub-leading `\ln\ln`? the
   `O(1)` argmax offset from the mean?) — the least-certain quantitative claim.
2. **Is the interval exactly `phi`-optimal at each `b`?** No (at `b=12` a
   hole-block beats it, `fstar=6>5`). The exact `phi(b) = max_V phi(V)` sequence
   and its optimizers are not computed here — irrelevant to `phi* = log2` (the
   interval is a sufficient witness) but open as a structure question.
3. **`inf gamma` (the redirected `rho*` wall).** R5 shows the live question for
   the packing rate is the deficit rate along `rho`-optimizers, not `phi*`. Not
   attacked here.

---

## Summary

```
    QUESTION (#643 R4.4):   is phi* < log 2 ?
    ANSWER:                 NO.  phi* = log 2  (PROVED, elementary pigeonhole).

    proof:   log2 - 6(ln b)/b  <  phi(interval,b)  <=  phi(b)  <=  (1-3/b)log2
             both sides -> log2, so phi* = sup_b phi(b) = log 2.
    rate:    fstar(interval,b) = Theta(2^b / b^{9/2})  (MEASURED poly-loss;
             det G = b^9/2160, covolume 2, local CLT) -- NOT an exponential defect.
    fallout: rho* <= phi* = log2 is tight at the top; the phi*-route to a
             sub-log2 rho* bound is DEAD -- redirect to the deficit rate gamma.
```
