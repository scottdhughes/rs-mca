# PTE extremality on the image-normalized R=2 face

## Status

`RUNG-1 PROBLEM PINNED (both readings) / RUNG-2 2-POINT-OPTIMALITY REFUTED
(COMPUTED) / RUNG-3 STRUCTURAL THEOREM PROVED + QUANTITATIVE MATCHING BOUND
OPEN (named wall) / RUNG-4 STABILITY MEASURED / RUNG-5 CENSUS COMPUTED`.

Research packet testing the convergence hypothesis that **Prouhet/PTE-type
products are extremal for the image-normalized near-Sidon / max-fiber tradeoff
at `R=2`**.  Verdict, in one line: **the extremal *structure* is PTE (proved
exactly), but the minimal two-point Prouhet block is *not* rate-optimal
(refuted); denser degree-2 PTE clusters strictly beat it on both the fiber-rate
and the energy axes, and the exact optimum is an open PTE-cluster packing
frontier.**

Every number below is recomputed by
`experimental/scripts/verify_pte_extremality.py` (stdlib-only, zero-arg,
`RESULT: PASS (45/45)`, ~13 s / 142 MB under `ulimit -v 2097152`).

Label key: **PROVED** (exact hand derivation), **COMPUTED** (exhaustive exact
enumeration), **MEASURED** (exact finite toy, asymptotic read off but not proved
from the toy), **AUDIT** (cross-reference), **OPEN**.

**Credit.** The convergence this packet adjudicates comes from three lineages:
**#534** (`balanced_core_kappa_growth.md`, the Prouhet-Thue-Morse family as the
extremal for the per-chart *secant count* `C(R+k,k+1) ~ 2^{0.97n}` on the
agreement/kernel side); **scottdhughes #564** (the equal-power-sum wall on the
ambient/signed side, and the **canonical star-PTE trade lemma** `w_a_star_pte
_lemma.md` / `star_pte_support_bound.md` — the fiber-algebra fact this packet
makes literal on the image face); **Codex #615** (`c9_r2_near_sidon_razor.md`,
the exact two-moment Prouhet product instantiating a positive `f/barN` rate).
The `R=2` razor predicate and its readings are the **LegaSage #585** chain; the
image-vs-span normalization map is **holmbuar #614**
(`minimal_phase_supplement.md`).  **Boundary:** the AMBIENT/SIGNED `(LS)`
large-sieve crux is scottdhughes's corner (#564); this packet works the
image-normalized face only and cites his trade identification without touching
`(LS)`.

---

## Rung 1 — the exact extremal problem (PROVED / AUDIT extraction from #615)

The sharpest current formulation is #615's setup (`eq:exact-power-sum-map`,
`eq:image-ambient-scales`).  Fix a ground set `T` of distinct points in a prime
field (characteristic `> 2`, no-carry), a fixed-weight slice
`Omega = binom(T, m)`, and the **two-moment map**

```
    Phi(S) = ( sum_{t in S} t ,  sum_{t in S} t^2 ) ,     R = 2.
```

Scales: `M = |Omega|`, `L = |Phi(Omega)|` (realized image),
`barN = M/L` (**image-normalized** ambient scale — this is #614's image face,
`barN = M/L`, *not* the span scale `M/|B|^R`).  Fibers `F_s = Phi^{-1}(s)`,
`f_s = |F_s|`, `f = max_s f_s`.  Additive energy of a fiber
`E(F) = #{(S_1,S_2,S_3,S_4) in F^4 : 1_{S_1}+1_{S_2} = 1_{S_3}+1_{S_4}}`
(indicator vectors in `Z^T`), density `Delta(F) = E(F)/f^3`.

**Extremal problem.** Maximize the **image-normalized fiber-rate**

```
    rho = log( f / barN ) / N       ( = log( f_max / f_avg ) / N ,  since barN = f_avg )
```

subject to a **near-Sidon** energy constraint, over all admissible
configurations feeding the `R=2` image cell.  Two printed readings of
"near-Sidon" (state both, work the one #615 instantiates):

- **Reading A (multiplicative / ratio-to-Sidon-floor):** `E <= f^{2+o(1)}`,
  i.e. `E / f^2 <= e^{o(N)}`.  Equivalently the energy exponent
  `theta := log E / log f <= 2`.  **The 2-point Prouhet product VIOLATES this**
  (`E/(2f^2) ~ (1/2)(3/2)^k`, #615), so under Reading A the Prouhet block is
  *infeasible*, not extremal.
- **Reading B (#585 printed absolute / `o(1)`):** `Delta = E/f^3 <= e^{-sigma N}`
  for every fixed `sigma` below a threshold (the TeX low-energy cut).  The
  exponential cut **implies** `Delta - (2f-1)/f^2 -> 0`, but the converse is
  FALSE (the difference can vanish at subexponential speed), so the two
  conditions are one-way, not equivalent — correction due to Codex's post-#623
  consumer audit; the concrete positive-rate verdicts below satisfy both forms.
  **The 2-point Prouhet product SATISFIES this** (`Delta = (3/4)^k`).
  **Work Reading B; flag Reading A.**

**#615's Cut-2 collapse (AUDIT, decisive for the shape of the problem).** By the
Boolean-cube energy bound `E(F)^3 <= f^8` (de Dios Pont–Greenfeld–Ivanisvili–
Madrid), `Delta <= f^{-1/3}`; a positive-rate fiber has `f = e^{Theta(N)}`, so
`Delta <= e^{-Theta(N)}` **automatically**.  Hence under Reading B the near-Sidon
constraint is *free for any positive-rate configuration*, and the extremal
problem reduces to the unconstrained maximization of `rho` — a **single 1-D
frontier**, plus the energy deficit `delta = -log Delta / N` as a secondary
Pareto coordinate.  (Under Reading A the constraint bites hard and the extremal
object is a different, harder regime — see the flag at the end.)

### The image-normalization is the whole content (PROVED, verifier BLOCK 1)

`rho = log(f_max/f_avg)/N` is a **max-to-average fiber ratio**.  A dense
arithmetic progression `{0,...,N-1}` has an enormous max fiber but a *collapsed*
image (`L <= poly(N)`), so `f_max/f_avg ~ 1` and `rho ~ 0`
(verifier: `AP{0..15}` gives `rho = 0.129` finite-`N`, `-> 0` asymptotically as
the image collapse `(5 log N)/N` bites).  Extremal configurations must instead
keep the image **large** (few collisions) while carrying **one anomalous
fiber** — which is exactly the block structure below.

---

## The general product curve (PROVED closed form; verifier BLOCK 0, 1)

A **block** is a ground set `V` of size `b` (in `Z`, taken to a prime field with
no-carry `Q^i` spacing so that the global signature recovers the per-block
signatures, #615's device).  Let

- `mu(w)` = maximum collision multiplicity of `(sum,sumsq)` among weight-`w`
  subsets of `V`; `fstar = max_w mu(w)` (the block's best fiber);
- `D_w` = number of *distinct* `(sum,sumsq)` signatures at weight `w`;
  `P_V(x) = sum_w D_w x^w`, `L1 = P_V(1) = ` #distinct signatures `= 2^b - c`
  where `c` = collision deficit;
- `E1` = additive energy of the best fiber; `theta = log E1 / log fstar`.

Tensoring `V` (k independent no-carry copies) at balanced total weight `(b/2)k`
gives the exact finite-`k` rate, whose limit is the **closed form (symmetric `V`,
balanced saddle `x*=1`):**

```
    rho(V)   = ( log fstar + log L1 ) / b  -  log 2   =  (1/b) log( fstar * L1 / 2^b )
    delta(V) = ( 3 log fstar - log E1 ) / b
```

The exact max tensor fiber is `MF_k = ` max over weight-compositions of the
product of per-block multiplicities (a small DP); `fstar` is attained in the
tensor via the symmetric split `{w, b-w}`.  **Verifier BLOCK 1 proves the three
routes agree** to machine precision: asymptotic closed form `==` exact finite-`k`
DP rate `==` explicit geometric-`Q^i`-spacing brute force, on both the #615 block
and a second block, `k=1,2`.

**#615 block, recovered exactly (BLOCK 0):** `V = {0,1,2,4,5,6}`, best fiber the
unique collision `A={0,4,5}` / `B={1,2,6}` (sum 9, sumsq 41 — the only collision
among all 64 subsets), `P_V = (1,6,15,19,15,6,1)`, `L1 = 63`, `fstar = 2`,
`E1 = 6`.  Then `f = 2^k`, `E = 6^k`, `Delta = (3/4)^k`, `f/barN = 1.90, 3.83,
7.55` (`k=1,2,3`), and

```
    rho_Prouhet2 = log(63/32)/6 = 0.112900 ,   delta = log(4/3)/6 = 0.047947 ,
    theta = log 6 / log 2 = 2.585 ,   G := (fstar*L1)^{1/b} = 126^{1/6} = 2.2390 .
```

---

## Rung 2 — product optimization: the 2-point block is NOT optimal (COMPUTED, BLOCK 2/3)

Maximizing `rho(V) = (1/b) log(fstar * L1 / 2^b)` is maximizing the objective
`G(V) = (fstar * L1)^{1/b}` = (max fiber) × (#distinct fibers), per coordinate.
Exhaustive affine-canonical search over ground sets (`b = 6..12`, coordinate box
per size; `--box` widens it):

| b | best rho | fstar | E1 | theta | best V |
|---|---------:|------:|---:|------:|--------|
| 6  | 0.112900 | 2 | 6  | 2.585 | {0,1,2,4,5,6}  (= #615, the minimal trade) |
| 8  | 0.086154 | 2 | 6  | 2.585 | {0,1,2,3,6,7,8,9} |
| 9  | 0.117188 | 3 | 15 | 2.465 | {0,1,2,3,5,6,7,11,12} |
| 10 | 0.106485 | 3 | 15 | 2.465 | {0,1,2,3,6,7,8,10,12,13} |
| 12 | **0.131684** | 6 | 66 | **2.338** | {0,1,2,3,5,6,7,8,10,11,12,13} = {0..13}\{4,9} |

**Verdict (COMPUTED, REFUTED).** In the default search **40 blocks strictly beat**
the 2-point Prouhet rate `0.112900`.  The champion `V = {0..13}\{4,9}`
(`b=12`, `fstar=6`) has `rho = 0.131684 > 0.112900` **and** `theta = 2.338 <
2.585` **and** `delta = 0.0988 > 0.0479` — it **Pareto-dominates** the 2-point
block on *both* the fiber-rate and the near-Sidon energy axes simultaneously.
The champion is validated by the exact finite-`k` tensor (`rho_3 = 0.129944`,
`MF_3 = 216`), not merely the asymptotic formula.  Widening the box (`--box 3`)
holds the verdict (152 blocks beat 2-point) and pushes the `b=12` optimum to
`rho = 0.138069` at the clean **four-spaced-triples** block
`{0,1,2}∪{4,5,6}∪{10,11,12}∪{14,15,16}`; a dedicated symmetric search at `b=14`
(`V = {0..18}\{1,4,9,14,17}`, `fstar=12`) reaches `rho ~ 0.15`.

**Structured plateau (BLOCK 3).** The clean parametric family "`g` intervals of
length `ell`, gap `gap`" beats the 2-point rate and **plateaus** at
`G ~ 2.30`, `rho ~ 0.14`, `theta -> ~2.24` as `b` grows (`b=12,16,18,20` give
`rho = 0.132, 0.140, 0.137, 0.139`).  So `rho*` is a finite constant `> 0.13`,
**not** climbing toward the trivial cap.

**Why the 2-point block loses.** For a *clean* block (deficit `c = fstar-1`,
image maximal) `rho ~ log(fstar)/b` — the fiber doubling-rate per coordinate.
The minimal degree-2 trade needs `b >= 6` coordinates for one doubling
(`log2 fstar / b = 1/6`); a denser cluster packs more fiber per coordinate while
keeping the deficit sub-dominant, so it wins.  The 2-point block is the *cleanest*
(`c=1`) but the *least dense*; the optimum trades a little image for a lot of
fiber.

---

## Rung 3 — the general upper bound (PROVED structural theorem + OPEN matching bound)

### 3.1 What IS proved: PTE-universality of the R=2 face (PROVED, BLOCK 4/5)

> **Theorem (PTE-universality).** Every fiber of `Phi = (sum t, sum t^2)` at
> fixed cardinality is exactly an equal-cardinality, equal-`(p_1,p_2)` family.
> Removing the common core, any two members `S, S'` give disjoint equal-size
> parts `P = S'\S`, `Q = S\S'` with `p_1(P)=p_1(Q)`, `p_2(P)=p_2(Q)`
> (equivalently `e_1,e_2` equal, by Newton) — a **degree-2 PTE trade** with
> support `>= 6` (`>= 3` per side).

This is exactly **scottdhughes's canonical star-PTE trade lemma** (#564
`w_a_star_pte_lemma.md`) read on the image face.  Consequence: **every
configuration with positive image-normalized rate is PTE-structured** — the
extremal *arena* is PTE, not by convention but by the exact fiber algebra.  The
verifier checks this over 47 census trades (BLOCK 5) and 200 ground sets (BLOCK
4), and pins the minimal trade support at exactly 6.  This is the rigorous form
of "PTE products are extremal": **PTE structure is universal and necessary.**

**SCOPE CLARIFICATION (correction due to Codex's post-#623 consumer audit).**
The theorem is *pairwise*: for each pair `S, S'` in a fiber, removing *their*
pair-dependent common core `S ∩ S'` leaves a degree-2 PTE trade.  It does
**NOT** assert a single fiber-global core or a global product decomposition
`fiber = core × PTE-cluster`, and "PTE-structured family" must not be read as
a bounded-complexity atlas theorem.  Downstream consumers get the pairwise
reduction (any two positive-rate members differ by a PTE trade), nothing
stronger.

### 3.2 What is NOT proved: the quantitative matching bound (OPEN, named wall)

The abstract cap: `fstar` and `L1` are both collision-limited, giving
`fstar + L1 <= 2^b + 1` (PROVED, every design), hence by AM-GM
`G = (fstar L1)^{1/b} <= 2^{2-2/b}` and

```
    rho <= (1 - 2/b) log 2  ->  log 2 = 0.6931   (PROVED, but LOOSE).
```

The best construction (`rho ~ 0.13`–`0.15`) sits **far below** this cap
(gap `~ 0.45` at `b=12`): the cap is saturated only at the unrealizable
`fstar = L1 = 2^{b-1}`.  **The matching bound resists.**  The **named missing
inequality** (the honest wall) is a sharp bound on the **achievable `(fstar, L1)`
frontier** — equivalently

> the maximum fiber `F(b,c)` of the `R=2` moment map on `b` points with
> collision deficit `c`, i.e. the maximum *clean degree-2 PTE-cluster packing
> rate* `sup (log2 fstar)/b` over blocks whose only heavy collision is one fiber.

No closed form is known; the computational frontier plateaus at `rho ~ 0.15-0.16`.
Proving `F(b,c)` matches that plateau would upgrade Rung 3 from structural to
quantitative.  (Superadditivity / Fekete — verifier BLOCK 4 — guarantees the
per-point rate `rho*` is a well-defined `sup` over blocks, each asymptotically
achievable by tensoring, so the object is genuine, not a finite-size artifact.)

---

## Rung 4 — stability (MEASURED)

Because PTE-universality is *exact* (every fiber is a PTE trade family), the
usual stability question "do near-extremal configs contain approximate PTE
structure?" is trivially yes.  The **non-trivial** stability question is whether
near-extremal fibers are approximately **product/block-decomposable** (a union of
independent small trades) versus a single indecomposable cluster.  Measured on
the census: the rate-maximizing blocks found are **indecomposable near-AP
clusters with symmetric gaps** (e.g. `{0..13}\{4,9}`), *not* products of
2-point trades — evidence that the optimum is genuinely indecomposable, so the
"approximate product" form of stability is **false as stated** and would need
restating as "approximate PTE-cluster." `MEASURED`, not proved.

---

## Rung 5 — census (COMPUTED, BLOCK 5)

Exhaustive over `{0,...,N-1}` in a prime field, all weights `m`, all fibers of
`(sum, sum^2)`, `N <= 9` (`--nmax` deeper).  The extremal small-`N` excess rate
`log(f/barN)/N` reaches `0.109` at `N=9, m=4` (`f=3`); finite-`N` sits below the
asymptotic product rate as expected (the frontier is a *rate*, approached only by
tensoring).  **Every** extremal collision (47 trades over `N<=9`) is a degree-2
PTE trade — the census confirms the structure, not the limiting constant.  The
frontier touches the product curve exactly where a census fiber first factors
through a spaced block (the `N=8`, `m=3` fiber is the #615 `A/B` trade embedded).

---

## What this buys for #615's OPEN residual (AUDIT)

#615's razor leaves OPEN the *smooth/circle primitive first-match residual over
an exponentially large profile field*.  The value of PTE-universality: that
residual's "counterexample universe" is **not open** — by the theorem, any
positive-rate profile is PTE-structured, so the consumer (the #615 lane, *not*
this packet — we do not decide the residual) tests **one structural family (PTE
clusters) instead of an unrestricted universe** — in the *pairwise* sense of
the §3.1 scope clarification (every two members differ by a degree-2 PTE
trade), not as a bounded-complexity atlas of globally-decomposed products.
The refinement this packet
adds: the family to test is **not** just the minimal 2-point trade; it is the
full degree-2 PTE-cluster family (including the denser rate-optimal clusters),
because those are the true rate-carriers.  So the reduction "open universe ->
PTE family" holds; the family is broader than a single block, and its primitive/
first-match-reachability is the live question for that lane.

---

## Reading A flag (out of scope, stated for completeness)

Under Reading A (`theta <= 2`, multiplicatively near the Sidon floor) the energy
constraint binds: since `E(F) >= 2f^2 - f` always, `theta >= 2` with equality
only as `f -> infinity` on **Sidon** fibers.  The 2-point Prouhet tensor has
`theta = 2.585` fixed, so it never qualifies; the Reading-A extremal family is
**large Sidon-PTE clusters** (`fstar -> infinity`, `E1 ~ fstar^2` per block) — a
distinct and harder regime, flagged as OPEN.  #615 already notes its
construction is not multiplicatively near the literal Sidon floor; this is the
same observation.

---

## AMBIENT/SIGNED boundary

The signed `(LS)` large-sieve crux (equal-power-sum sums with signs) is
scottdhughes's ambient-side corner (#564); this packet makes no claim there and
uses his trade lemma only as the image-face fiber algebra.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/pte_extremality_image_face.md` (this).
- Verifier: `experimental/scripts/verify_pte_extremality.py`
  (`RESULT: PASS (45/45)`; BLOCK 0 #615 recompute, BLOCK 1 rate-machinery
  triple-agreement, BLOCK 2 optimization + refutation, BLOCK 3 objective/plateau,
  BLOCK 4 PTE-universality + cap + wall + superadditivity, BLOCK 5 census).
- Read-only inputs: #615 `c9_r2_near_sidon_razor.md`; #614
  `minimal_phase_supplement.md`; #534 `balanced_core_kappa_growth.md`;
  #564 `w_a_star_pte_lemma.md` / `star_pte_support_bound.md` (branch
  `pr-564-hughes`).

**Per-claim status.** Rung-1 problem + both readings = `PROVED`/`AUDIT`
(extracted from #615/#585/#614).  Product-curve closed form + triple-agreement =
`PROVED`.  2-point-optimality refutation + Pareto domination + plateau =
`COMPUTED` (exact enumeration).  PTE-universality theorem = `PROVED` (exact fiber
algebra = #564 trade lemma).  Analytic cap `(1-2/b)log2` = `PROVED` (loose).
Matching quantitative bound / `rho*` / the packing inequality = `OPEN` (named
wall).  Stability = `MEASURED`.  Census = `COMPUTED`.

**Flagged for PI re-derivation (2-3 steps).** (a) The closed form
`rho = (1/b) log(fstar L1 / 2^b)` from `M ~ 2^b` (balanced binomial), `L1 =
P_V(1)` (symmetric saddle `x*=1`), `f = fstar^k` (tensor) — verify against BLOCK
1's exact `k`-agreement.  (b) The refutation: recompute `rho` for `{0..13}\{4,9}`
and check `0.1317 > log(63/32)/6 = 0.1129` with `theta = 2.338 < 2.585` (BLOCK
2).  (c) PTE-universality: two colliding subsets of equal `(p_1,p_2)` have
sym-diff a disjoint equal-size equal-`(p_1,p_2)` pair (Newton `e_1,e_2`), minimal
support 6 (BLOCK 4/5) = #564's star-trade lemma.

**Exact vs heuristic.** All fiber counts, images, energies, and finite-`k` tensor
rates are exact integer / `Fraction` enumeration.  The asymptotic `rho`, `delta`,
`G`, and the `-> log 2` cap are elementary limits of the exact finite objects
(the single non-finite step, flagged).  No `.tex`/`.pdf` edited; no promotion
into the frontiers draft.
