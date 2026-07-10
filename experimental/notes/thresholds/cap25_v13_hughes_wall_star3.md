# CAP25 v13: the star3 sub-wall of Hughes's Route-D terminal wall

**Status:** ★3 RESTATED (EXACT) / REDUCTION PROVED / MODEL VALIDATED (MEASURED) /
knife-edge quantified (ANALYSIS) — the sub-wall ★3 itself stays **OPEN**.

This packet continues our engagement (PR #468, PR #479) with Scott Hughes's
Route-D program on the KoalaBear row.  PR #479 pinned his terminal wall
`|T| <= H2` at the deployed row, exhibited the first deployed members of `T`,
and named the **smallest honest sub-wall** `★3` at side size `e_s = 3`.  Here we
(1) restate `★3` with every object explicit and reproduce #479's witness count
and the `9.0612` factor exactly; (2) prove a clean incidence reduction that
recasts the open core of `★3` as a single point-count `P <= H2`; (3) validate
the birthday-load model against **exact** sociable fractions across a KB-shape
toy ladder — the model tracks the true fraction to a few percent (much tighter
than #479's "within 2x"), locating the exact scale at which the analogous
fraction bound fails; (4) bank the obstruction, the smallest undecided
statement, and a falsifier target.  No sub-wall is closed.  Everything
structural is downstream of Hughes's v51–v54 chain and #479's pins.

## ★3, restated with every object explicit (EXACT)

Deployed KB row (source of truth: `verify_kb_qatom_route_d_v54.py`, #479's
`verify_hughes_wall_small_e.py`): prime `p = 2130706433 = 2^31 − 2^24 + 1`,
`n = 2^21`, generator `g = 3`, canonical root of unity
`omega = 3^{(p−1)/n} = 1213133211` (order `n`), subgroup index `(p−1)/n = 1016`,
arc `I_{n'} = {omega^0, …, omega^{n'−1}}` with `n' = 1183520`, terminal point
`zeta := omega^{n'−1}`.  Because `omega^{n/2} = −1` and
`n'−1 = n/2 + 134943`, one has `zeta = −omega^{134943}`.

- A **terminal pair** is an unordered `{x, y}` of two distinct arc points with
  indices in `I_{n'−1} = {0, …, n'−2}` (i.e. `x, y ∈ arc \ {zeta}`).  It names
  the **terminal 3-set** `U = {x, y, zeta}` (side size `e_s = 3`, contains
  `zeta`).  There are exactly `C(n'−1, 2) = 700358019921` terminal pairs.
- The **monic locator** of a 3-set `W = {a, b, c}` is
  `f_W(X) = (X−a)(X−b)(X−c) = X^3 − e_1 X^2 + e_2 X − e_3` with
  `e_1 = a+b+c`, `e_2 = ab+ac+bc`, `e_3 = abc`.  Its **high signature** is the
  coefficient pair `(e_1, e_2)` (the `X^2, X^1` data); `e_3` is the constant.
- A **free-1 partner triple** of `U` is a 3-subset `V ⊆ I_{n'}`, `|V| = 3`,
  `V ≠ U`, with `f_U − f_V` a nonzero constant — i.e. `V` is a triple of arc
  points with `e_1(V) = e_1(U)`, `e_2(V) = e_2(U)`, and `e_3(V) ≠ e_3(U)`.
- The counting measure: `|T(n',3)|` counts terminal 3-sets `U` (equivalently
  terminal pairs `{x,y}`) that admit **at least one** free-1 partner triple.

```text
(★3)   |T(n',3)| <= H2 = 77291948627         [OPEN]
       H2 = floor(e·p / 1860),  e = 67472 deployed side size (#479 pin F1)
       trivial bound (Hughes v53/v54, #479 L2):  |T(n',3)| <= C(n'−1,2)
       exact deficit:  C(n'−1,2) / H2 = 700358019921 / 77291948627 = 9.0612
       equivalently:   admissible fraction  |T|/C(n'−1,2)  <=  1/9.0612 = 0.110361
```

Reproduction (verifier, exact integers): `C(n'−1,2) = 700358019921`,
`H2 = 77291948627`, `C(n'−1,2)/H2 = 9.061203…`, target fraction
`H2/C(n'−1,2) = 0.110361`.  #479's deployed witnesses give `|T(n',3)| >= 8`
(re-verified here by locator expansion on the canonical arc from #479's witness
index pairs, independent of its certificate), so the honest range is
`8 <= |T(n',3)| <= 700358019921` and `★3` asks to pull the upper end down by the
factor `9.0612`.

### Two exact characterizations (PROVED)

- **C1 (fiber ≥ 2).**  For a terminal set `U`, `U ∈ T(n',3)` **iff** the fiber
  `Phi(e_1,e_2) := { arc 3-sets W : high(W) = high(U) }` has `|Phi| >= 2`.  A
  monic cubic is determined by its three coefficients, so any `W ≠ U` with
  `high(W) = high(U)` automatically has `e_3(W) ≠ e_3(U)`, hence `f_U − f_W` is
  a nonzero constant; and by #479's L2 (terminal uniqueness) `U` is the unique
  terminal member of `Phi`, so the partner is non-terminal.  ("Sociable" pair =
  fiber `>= 2`; "lonely" pair = fiber `= 1`.)
- **C2 (equal power sums).**  By Newton's identities, `e_1(V) = e_1(U)` and
  `e_2(V) = e_2(U)` **iff** `V` and `U` have equal sum and equal sum of squares:
  `a+b+c = x+y+zeta` and `a^2+b^2+c^2 = x^2+y^2+zeta^2`.  So a free-1 partner is
  exactly a second arc-triple sharing the first two power sums with `{x,y,zeta}`
  — a degree-2 Prouhet–Tarry–Escott collision constrained to the arc.

## The incidence reduction (PROVED): ★3 ⟸ `P <= H2`

Define the **incidence count**
```text
P := #{ (terminal pair {x,y}, non-terminal arc-triple {a,b,c}) :
        e_1{a,b,c} = e_1{x,y,zeta},  e_2{a,b,c} = e_2{x,y,zeta} }.
```

- **R1 (partner forces the pair).**  A high `(s,q)` determines at most one
  terminal pair: `x+y = s − zeta` and `xy = q − zeta·(s − zeta)`, so `{x,y}` are
  the roots of `X^2 − (s−zeta) X + (q − zeta s + zeta^2)`.  Hence each
  non-terminal arc-triple `{a,b,c}` (with its high `(s,q)`) is the partner of at
  most one terminal pair.
- **R2 (reduction).**  Every sociable pair contributes at least one incidence,
  so `|T(n',3)| <= P`.  And by R1,
  `P = #{ non-terminal arc-triples {a,b,c} whose forced quadratic
  X^2 − (s−zeta) X + (q − zeta s + zeta^2) splits into two distinct arc points
  ≠ zeta with e_3 differing }`.

Therefore **`P <= H2` implies `★3`**, and `P` is a single incidence /
affine-variety point count on `arc^5` cut by one linear and one quadratic
symmetric equation — no `min`/fiber structure, the natural object for an
analytic (character-sum) attack.  `P` is also directly measurable: on toys `P`
is exactly #479's `partner_pairs`.  Heuristic value
`P ≈ C(n'−1,2)·lambda ≈ 0.55·H2` (below), so the reduction target has the same
`~1.9x` slack as `★3` itself — proving `P <= H2` is a (slightly stronger,
cleaner) sufficient route, not a free win.

**Model.**  With `lambda := C(n'−1,3)/p^2` (expected free-1 partners per
terminal pair, highs modelled uniform on `F_p^2`):
`E|T| = C(n'−1,2)·(1 − exp(−lambda))`, `E P = C(n'−1,2)·lambda`.
Deployed: `lambda = 0.060859`, `1 − exp(−lambda) = 0.059044 = 1/16.94`, so
`E|T| = 0.535·H2` and `E P = C(n'−1,2)·lambda = 0.5515·H2` (the latter is
exactly #479's load).  The admissible fraction is predicted `0.0590`, a factor
**`0.110361 / 0.059044 = 1.869` below the target**.  `★3` is heuristically
**true with ~1.87x slack** (and `P <= H2` with ~1.81x slack) — a knife-edge, as
#479 flagged.

## Toy ladder: exact sociable fractions vs the model (MEASURED)

Exhaustive `e_s = 3` scans on KB-shape arcs (`t = 9n/16`, step 1), each row an
exact integer census of all `C(t,3)` triples.  `frac = |T|/C(t−1,2)`,
`f/tgt = frac / 0.110361`, `lambda = C(t−1,3)/p^2`, `m/f = (1−e^{−lambda})/frac`.
`|T| <= P` holds on **every** row (R2 live-checked).  Gradient cross-check at
`n=64, t=36` reproduces PR #468's table byte-for-byte.

| regime | n | q | p | t | \|T\| | P | frac | f/tgt | lambda | m/f |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| crossing | 512 | 21 | 10753 | 288 | 1320 | 1331 | 0.03216 | 0.291 | 0.03372 | 1.031 |
| crossing | 1024 | 18 | 18433 | 576 | 14434 | 15103 | 0.08747 | 0.793 | 0.09277 | 1.013 |
| crossing | 1280 | 18 | 23041 | 720 | 27860 | 29431 | 0.10793 | **0.978** | 0.11620 | 1.016 |
| crossing | 1536 | 17 | 26113 | 864 | 54098 | 58394 | **0.14544** | **1.318** | 0.15655 | 0.996 |
| dense | 384 | 9 | 3457 | 216 | 2892 | 3074 | **0.12571** | **1.139** | 0.13667 | 1.016 |
| dense | 768 | 10 | 7681 | 432 | 18566 | 20643 | **0.20036** | **1.816** | 0.22460 | 1.004 |
| mid-sparse | 1024 | 64 | 65537 | 576 | 1216 | 1219 | 0.00737 | 0.067 | 0.00734 | 0.992 |
| mid-sparse | 2048 | 65 | 133121 | 1152 | 9380 | 9460 | 0.01417 | 0.128 | 0.01430 | 1.002 |
| deployed-like | 1024 | 1027 | 1051649 | 576 | 6 | 6 | 0.00004 | 0.0003 | 0.00003 | — |
| deployed-like | 2048 | 1026 | 2101249 | 1152 | 31 | 31 | 0.00005 | 0.0004 | 0.00006 | — |

**Reads.**

- **Model fidelity is excellent and stable.**  Where counts are statistically
  meaningful (`|T| >= ~10^3`), `m/f ∈ [0.99, 1.03]` across sparsity
  `q ∈ [9, 65]` and across `t ∈ [216, 1152]`.  The true sociable fraction tracks
  `1 − exp(−lambda)` to a few percent — materially tighter than the #479 "within
  2x" claim.  `P/C(t−1,2) ≈ lambda` likewise (e.g. `n=1280`: `0.11402` vs
  `0.11620`), confirming `P` is the expected-incidence object.
- **The crossing is bracketed.**  Along the fixed-sparsity `q≈17–18` family the
  fraction climbs `0.087 → 0.108 → 0.145`, crossing the target `0.110361`
  between `n=1280` (`f/tgt = 0.978`) and `n=1536` (`f/tgt = 1.318`).  At fixed
  `q`, `lambda ∝ n(1+o(1))`, so the KB-shape sociable fraction equals the target
  at `lambda* = 0.116939 = 1.921·lambda_deployed`, i.e. **arc size `~1.92x`
  deployed** (crossing scale `n* ≈ 1.92·2^21 ≈ 4.0·10^6`; deployed
  `n = 2^21 = 2.10·10^6 = 0.52·n*`).
- **Over-target fractions occur only for dense / oversized arcs, never at
  deployed sparsity.**  Rows with `f/tgt > 1` (bold) are all dense (`q ≤ 10`) or
  ~2x-oversized (`n=1536`).  Every deployed-like row (`q ≈ 1016`) has fraction
  `~10^{-4}`, three orders below the target, exactly on model.  **No red flag:
  the sub-wall analogue is false above the crossing scale and comfortably true
  at deployed scale.**  These over-target rows are not counterexamples to `★3`
  (whose `H2` is deployment-specific); they exactly quantify how much collision
  load the deployed row has in hand (`1/0.52 ≈ 1.9x`).

### Antipodal subfamily (PROVED sliver, MEASURED)

#479's witnesses use the antipodal partner form `V = {a, −a, c}` (L5:
`e_1 = c`, `e_2 = −a^2`, `e_3 = −a^2 c`).  These `A3 ⊆ T(n',3)` are a genuine
proved subfamily but a **sparse sliver**: on the `n=1024, q=18` toy
(`|T| = 14434`), only **21** sociable pairs have an antipodal-shaped partner,
i.e. a fraction `0.00145` (`~1.5·10^{-3}`) of `T`.  (#479 needed `1.4·10^8`
trials to find 8
antipodal witnesses at deployed scale, consistent with antipodal being
`~10^{-3}` of `T`.)  The overwhelming majority of `T` are **generic** power-sum
collisions with no coset structure — which is exactly why the structured routes
(coset classification #479 L3, antipodal recursion) cannot close `★3`, and why
the residual is a birthday-collision count.

## Obstruction, smallest undecided statement, falsifier (ANALYSIS)

- **Why `★3` is hard (knife-edge).**  (i) *Scale-sensitivity*: the admissible
  fraction is `~1 − exp(−lambda(n))` with `lambda(n) ∝ n` at fixed sparsity; it
  crosses the target at `~1.92x` deployed size, so `★3` holds with only `1.87x`
  fractional slack and is genuinely **false** for KB-shape arcs a factor `~2`
  larger (or denser).  A proof must be sharp to better than `1.9x` *and* must use
  that deployed `n` lies below the crossing `n*`.  (ii) *Analytic*: in
  `P = (main term C(n'−1,2)·lambda from the zero frequency) + (off-frequency arc
  sums)`, the arc is an **interval** `{omega^0, …, omega^{n'−1}}` of density
  `0.5625` in `mu_n`, not a subgroup; there are `~p^2` frequencies, and bounding
  the incomplete character sums over an interval loses a constant that at these
  parameters exceeds the `1.9x` slack (#479's finding; structurally, an interval
  lacks the exact orthogonality a subgroup gives).  Character-sum completion is
  just short.
- **Smallest undecided statement.**  `P <= H2 = 77291948627` (incidence count of
  `(terminal pair, non-terminal partner)` at the KB row).  It implies `★3`,
  hence the `e_s = 3` sub-wall; heuristic value `E P ≈ 0.55·H2`.  Equivalently:
  the admissible fraction `|T(n',3)|/C(n'−1,2) <= 0.110361`.
- **Falsifier target.**  A KB-shape arc at deployed sparsity (`q ≈ 1016`) with
  admissible fraction `> 0.110361`.  The validated model predicts this requires
  `n > n* ≈ 4.0·10^6`, beyond the deployed `n = 2^21`; exhibiting one at
  `n <= 2^21` would refute both the model and the sub-wall.  None exists in the
  exhaustively scanned range.

## Reconciliation with #479 and Hughes's chain

Hughes's reduction (v51 U2e → v53 C_unique → v54 terminal star) and #479's pins
F1–F4 and lemmas L1–L6 stand untouched and are used as-is.  This packet adds:
(i) the fiber/power-sum characterizations C1–C2 make `★3` a clean collision
count; (ii) the reduction R1–R2 recasts its open core as a single incidence
bound `P <= H2` amenable to analytic attack; (iii) the exact toy ladder upgrades
#479's model calibration from "within 2x" to "few-percent, stable across
sparsity and size", locates the crossing scale `n* ≈ 1.92·2^21`, and confirms
the deployed row sits `~1.9x` below it — no counterexample, sub-wall
model-supported; (iv) the antipodal subfamily is measured to be a `~10^{-3}`
sliver, so the residual is genuinely generic.  Everything non-arithmetic here is
downstream of Hughes's structure theorems and #479's terminal-star restatement.

## Non-claims

- Does **not** prove `★3` (`|T(n',3)| <= H2`) or `P <= H2`; both stay OPEN.
  The `e_s = 3` sub-wall and the deployed wall `|T(n',67472)| <= H2` remain OPEN.
- Does **not** refute any Hughes or #479 claim.  The over-target toy fractions
  are for dense / oversized KB-shape arcs and are **not** counterexamples to
  `★3` (H2 is deployment-specific); they are the model behaving correctly.
- The model `1 − exp(−lambda)` is a heuristic.  Its fidelity is measured on toys
  with `t <= 1152`; the deployed `t ≈ 1.18·10^6` is a `~10^3x` extrapolation.
  Only the integer counts, `|T| <= P`, and the arithmetic gates are PROVED;
  every `lambda`/model/crossing-scale number is ANALYSIS.
- The reduction `|T| <= P` and R1 are field-exact and general; the crossing
  scale and `1.9x` slack are model quantities.
- Witness lower bounds and antipodal measurements are for the canonical `omega`
  arc only (F4).

## Reproducibility

Zero-argument, stdlib-only, deterministic full replay (constants, incidence
reduction spot-checks, exact toy ladder, antipodal count, arithmetic gates)
against the checked-in certificate, plus live tamper tests:

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_hughes_wall_star3.py
```

Certificate: `experimental/data/cap25_v13_hughes_wall_star3.json`.
