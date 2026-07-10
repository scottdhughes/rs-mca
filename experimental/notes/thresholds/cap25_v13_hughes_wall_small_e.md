# CAP25 v13: Hughes Route-D terminal wall at small side sizes

**Status:** WITNESSES PROVED / EXACT PINS / ANALYSIS — deployed wall stays **OPEN**.

This packet is a contribution into Scott Hughes's Route-D program on the
KoalaBear row `a+ = 1116048` (v1–v54; STATUS + selected packets integrated at
commit `84b393e`, see `kb_qatom_route_d_STATUS.md`).  His chain — v51 **U2e**
unique bipartition, v53 **C_unique** terminal core, v54 **terminal star** —
reduced the pure-untyped residual card to a single open finite bound.  We pin
that bound exactly, re-derive his `e=2` close, exhibit the **first deployed-row
members of his terminal set `T`** (side sizes 3 and 4), and map the whole
side-size-parametric family with exact budget arithmetic.  No wall is closed
here; the map says precisely where a proof must and must not live.

## The wall, pinned (tree-anchored)

Deployed row: `p = 2130706433 = 2^31 − 2^24 + 1`, `n = 2^21`, subgroup index
`(p−1)/n = 1016` exactly, canonical domain `omega = 3^((p−1)/n)` (the
`prim_root` convention of `verify_kb_qatom_route_d_v54.py`; `g = 3`,
`omega = 1213133211`), prefix `I_{n'} = {0,…,n'−1}` with `n' = 1183520`,
side size `e = w+1 = 67472`, and

```text
T  =  { U ⊆ I_{n'} : |U| = e,  n'−1 ∈ U,  ∃ V ⊆ I_{n'}, |V| = e, V ≠ U,
        f_U − f_V a nonzero constant }          (f = monic locator)
WALL (OPEN, Hughes v54/STATUS):   |T| ≤ H2 = 77291948627
```

Free-1 means the monic locators agree on the coefficients of
`X^{e−1},…,X^1` (v51 statement; operationally the high signature of the v54
and PR #468 verifiers).  Under v53 + v54, `|H_unt| ≤ |T|`; with the v45/v46
`M_pad ≤ 2` accounting (`930·H2 ≤ e·p/2`) this closes the residual card, the
last piece of `A_SP ≤ t·p` on this path.  Alternate close: `|R2| ≤ e·p`.

### Faithfulness pins (resolving the PR #468 T-definition discussion)

- **F1 (H2 is a fixed constant).** `H2 = ⌊e·p/(2·31·30)⌋ = 77291948627` with
  `e = 67472` the *deployed* side size (v45; `e·p = 143763024447376`).  In the
  side-size-parametric family below the budget does **not** rescale to
  `⌊e_s·p/1860⌋`.
- **F2 (direction).** v54's `|H_unt| = |T|` display is loose; the proved
  content is the star injection `H ↦ U_*`, giving `|H_unt| ≤ |T|`.  The chain
  only consumes **upper bounds on `|T|`**; equality is neither established nor
  needed.
- **F3 (partner structure is automatic).** Distinct equal-high sets are
  automatically disjoint, and partners of terminal sets are automatically
  non-terminal (lemmas below), so the bare definition of `T` above is already
  the right object.
- **F4 (generator convention).** `T` is read on the canonical `omega`-arc.
  PR #468 proved phase invariance and exhausted all primitive steps at its toy
  rows; the witnesses below are canonical-`omega` (the antipodal mechanism is
  step-universal — the antipode sits `n/2` positions away in every odd-step
  arc — but per-step witnesses are only claimed where verified).

## Structural lemmas (PROVED)

- **L1 (disjointness, any e, any field).** If `U ≠ V` share the high then
  `f_U − f_V` is a nonzero constant, so `f_U, f_V` share no roots and
  `U ∩ V = ∅`.  (Implicit in v25/v51 and the PR #468 scan gates.)
- **L2 (terminal uniqueness, any e).** Each high `h` has at most one terminal
  e-set: a monic locator through `zeta = omega^{n'−1}` with high `h` has
  constant term forced to `−(zeta^e + Σ_i h_i zeta^i)`.  Hence
  `|T| ≤ C(n'−1, e−1)`, partners of terminal sets are non-terminal, and
  Hughes's star center is the unique terminal holder of its high.  (Cleanup of
  the v53/v54 disjointness route; live-checked on every toy row below.)
- **L3 (coset classification on the deployed arc).** For `d | n`, `d > 1`, a
  `mu_d`-coset lies inside `I_{n'}` iff `d = 2` and its base index is
  `< n' − n/2 = 134944`: the complement window has length `n − n' = 913632 ≥
  n/d` for every `d ≥ 4`, while the `d = 2` spacing `n/2 = 1048576` exceeds
  it.  So the only coset-structured free-1 pairs on the arc are the antipodal
  `e = 2` family — the algebraic family behind Hughes's `e = 2` saturation
  dies at `e ≥ 3`, and small-e witnesses must (and do) use looser structure.
- **L4/L5 (witness families).** Antipodal quadruples satisfy
  `f = X^4 − (u1²+u2²)X² + u1²u2²`: equal square-sums with distinct
  square-pairs give free-1 pairs at `e = 4`; `V = {a, −a, c}` has
  `(e_1, e_2, e_3) = (c, −a², −a²c)`, giving the `e = 3` family by solving
  `c = zeta+x+y ∈ arc`, `a² = −(zeta(x+y)+xy) ∈ mu_{n/2}`.
- **L6 (e = 2 close, credit v48/v50).** `|T(t,2)| ≤ p ≤ H2` for all
  `t ≤ n'` — the `e = 2` high is the single coefficient `e_1`.  Note
  `p ≤ H2 ⟺ e_deployed ≥ 1860`: Hughes's `e = 2` close is
  deployment-dependent through `H2`, not a pure side-size-2 fact.

## Deployed-row witnesses (PROVED): `|T(n',3)| ≥ 8`, `|T(n',4)| ≥ 1972`

First explicit members of `T` at the true deployed row (canonical `omega`),
each verified by exact locator expansion (equal `X^{e−1}..X^1` coefficients,
distinct constants, disjoint, terminal, all indices `< n'`).  They exist
because `n' − n/2 = 134944 > 0`: the arc holds antipodal pairs, and
`zeta = −omega^{134943}`.

| # | U (indices, e=3) | V | (c_U, c_V) |
|---|---|---|---|
| 1 | [5, 1139380, 1183519] | [119016, 461783, 1167592] | (458032479, 1299732752) |
| 2 | [10, 116655, 1183519] | [34790, 64920, 1083366] | (469279472, 1946922722) |
| 3 | [10, 1066874, 1183519] | [41609, 1001501, 1090185] | (1366566111, 582422575) |
| 4 | [34, 217618, 1183519] | [13556, 80622, 1062132] | (1960725159, 882944447) |
| 5 | [80, 1145533, 1183519] | [111789, 655859, 1160365] | (517033234, 1553864369) |
| 6 | [86, 932197, 1183519] | [103106, 858291, 1151682] | (1182782072, 1223621537) |
| 7 | [115, 155875, 1183519] | [124298, 541768, 1172874] | (1091739384, 463207942) |
| 8 | [120, 624144, 1183519] | [44846, 695508, 1093422] | (388875875, 437321737) |

(`V` rows carry one antipodal pair, e.g. row 1: `1167592 − 119016 = 2^20`.)

| # | U (indices, e=4) | V | (c_U, c_V) |
|---|---|---|---|
| 1 | [44091, 134943, 1092667, 1183519] | [0, 8860, 1048576, 1057436] | (811564160, 388808602) |
| 2 | [15932, 134943, 1064508, 1183519] | [0, 17763, 1048576, 1066339] | (394262891, 882391434) |
| 3 | [116458, 134943, 1165034, 1183519] | [0, 50090, 1048576, 1098666] | (429017364, 1572709181) |
| 4 | [31651, 134943, 1080227, 1183519] | [0, 73243, 1048576, 1121819] | (775401708, 1804842149) |
| 5 | [73586, 134943, 1122162, 1183519] | [0, 101758, 1048576, 1150334] | (561966306, 3962352) |
| 6 | [112411, 134943, 1160987, 1183519] | [0, 104656, 1048576, 1153232] | (1350200308, 1038073207) |
| 7 | [17560, 134943, 1066136, 1183519] | [0, 115751, 1048576, 1164327] | (1175577701, 427712301) |
| 8 | [13278, 134943, 1061854, 1183519] | [0, 119643, 1048576, 1168219] | (47414359, 527358269) |
| 9 | [70111, 134943, 1118687, 1183519] | [0, 124336, 1048576, 1172912] | (135923474, 991711737) |
| 10 | [77576, 134943, 1126152, 1183519] | [1, 13953, 1048577, 1062529] | (620268201, 1613765913) |
| 11 | [27799, 134943, 1076375, 1183519] | [1, 19582, 1048577, 1068158] | (2062081643, 788608618) |
| 12 | [60775, 134943, 1109351, 1183519] | [1, 25885, 1048577, 1074461] | (249005185, 1701019539) |

Searches are deterministic and cheap relative to the model rates: 12 distinct
`e = 4` centers within 160,827 square-pair probes; 8 `e = 3` witnesses within
142,639,044 `(x,y)` trials (cap 150M).

**Family scan (PROVED count + deployed-scale calibration).**  An exact
partner census over the first 2000 antipodal centers `U(j2) =
{omega^134943, zeta, ±omega^{j2}}` (each partnered `j2` exactly verified by
locator expansion, distinct `U` per `j2`):

```text
partnered: 1972 / 2000   ⇒   |T(n',4)| ≥ 1972          (PROVED)
measured rate 0.986000  vs  model rate 1 − exp(−λ) = 0.986062,
λ = (134943·134942/2)/p = 4.2725   (partner-pair load per center)
```

Three-decimal agreement between the load model and the true deployed row —
the model's strongest calibration point, measured exactly where the wall
lives.  **Consequence:** the `T = 0` nulls of v54's dense toys and PR #468's
sparse toy arcs do not persist at deployed scale for small side sizes; the
`e = 4` family is 98.6% partner-saturated, and any hope of closing small-e
cases by vanishing is dead, exactly as the load model predicts.

## Exact budget arithmetic (PROVED as integer facts)

| quantity | value | meaning |
|---|---:|---|
| `H2` | 77291948627 | `⌊e·p/1860⌋`, fixed budget |
| `C(n'−1,2)` | 700358019921 | terminal-injection bound at `e_s=3` (L2) |
| `C(n'−1,2)/H2` | 9.0612 | exact deficit of the trivial bound at `e_s=3` |
| `p²/H2` | 5.87e7 | deficit of the v48 coefficient bound at `e_s=3` |
| `H2/p` | 36.28 | why `e_s=2` closes (`⟺ e ≥ 1860`) |
| `H2/(n'−1)` | 65306.9 | `e_s=2` close survives even full saturation |

**Birthday-load model** (ANALYSIS): model `E[T](e_s) ≈ C(n'−1,e_s−1)·(1 −
exp(−λ))`, `λ = C(n'−1,e_s)/p^{e_s−1}`; for `e_s ≥ 3`, `λ < 1` and
`E[T] ≈ load(e_s) = C(n'−1,e_s−1)·C(n'−1,e_s)/p^{e_s−1}`.  Load values are
exact rationals; every `load(e_s) vs H2` comparison below is an exact integer
gate.

| e_s | load | load/H2 | > H2? |
|---:|---:|---:|---|
| 2 | 3.89e+08 | 0.0050 | no (saturated regime; `T ≤ n'−1` anyway) |
| 3 | 4.2623e+10 | **0.5515** | **no — but only 1.8x slack** |
| 4 | 2.3350e+12 | 30.21 | yes |
| 5 | 7.68e+13 | 993.0 | yes |
| 10 | 2.06e+19 | 2.67e+08 | yes |
| 26 | 5.28e+24 | 6.83e+13 (`≈ 2^46·H2`) | yes — peak |
| 59 | 9.83e+10 | 1.272 | yes — last over |
| 60 | 1.83e+10 | 0.2362 | no — reentry |
| 70 | 154.8 | 2.0e−09 | no |
| 80 | 7.5e−08 | 9.7e−19 | no |

Overload band exactly `e_s ∈ [4, 59]`.  At the chain's own case
`e_s = e = 67472`: `C(n'−1,e−1)·C(n'−1,e)` has 746,679 bits versus
`p^{e−1}` at 2,090,838 bits — exact gate `load < 2^−1344158`.  **The wall the
chain actually needs is heuristically true with 1.34 million bits of margin,
and the predicted truth mechanism is total paucity (`|T| = 0`), not a tight
count.**

## Toy ladder (MEASURED, exhaustive, KB-shape `t = 9n/16`)

Gradient cross-check, `n = 64, t = 36`, step 1 — matches PR #468's table
exactly (independent implementation):

| q | e | T meas | pairs | model E[T] |
|---:|---:|---:|---:|---:|
| 4 | 3 | 55 | 58 | 56.13 |
| 18 | 3 | 4 | 4 | 2.92 |
| 67..1017 | 3 | 0 | 0 | ≤ 0.21 |
| 4 | 4 | 11 | 11 | 20.16 |
| 18..1017 | 4 | 0 | 0 | ≤ 0.22 |

New sparse-index rows at and beside the exact KB index `q = 1016`:

| block | q | p | t | e | steps | T per step | model/step |
|---|---:|---:|---:|---:|---|---|---:|
| n128 all-steps | 1014 | 129793 | 72 | 3 | all 64 units | all 0 | 0.0084 |
| n256 | 1015 | 259841 | 144 | 3 | 1,3 | 0, 0 | 0.072 |
| **n512 (exact KB index)** | **1016** | 520193 | 288 | 3 | 1,3,5 | **0, 1, 0** | 0.591 |
| **n1024 onset** | 1014 | 1038337 | 576 | 3 | 1,3 | **4, 4** | 4.824 |
| n128 | 1014 | 129793 | 72 | 4 | 1,3 | 0, 0 | 2.5e−05 |
| n256 | 1015 | 259841 | 144 | 4 | 1 | 0 | 4.5e−04 |

The `T > 0` onset at sparse KB-like index appears exactly where the model
predicts (first nonzero at load ≈ 0.6, count 4 at load ≈ 4.8, both steps).
Calibration across all exhaustive rows: model within ~2x, excellent at
`e = 3`.  PR #468's zeros are birthday underload, not sparse-arc magic.

## Rung-2 report: where the e=2 method breaks at e=3

Hughes's `e_s = 2` close is `|T| ≤ #highs = p ≤ H2`.  At `e_s = 3` the high
space is `p²` with `p²/H2 = 5.87e7` — the coefficient count is dead (his v48
already refuted its unrestricted form).  The terminal structure (L2) improves
it to `|T(n',3)| ≤ C(n'−1,2) = 700358019921`, leaving deficit **exactly
9.0612**.  The atomic open sub-statement is now:

```text
(★3)  at most a 1/9.0612 fraction of terminal pairs {x,y} ⊆ I_{n'−1}
      admit a free-1 partner triple            (model: 0.0590 ≈ 1/16.9)
```

We found no proof of (★3): fiber decompositions by `e_1` fail (partner fibers
are ~1.3e8-sized versus ~329 terminal pairs per fiber, so `min`/Cauchy–Schwarz
give nothing below the trivial bound), and character-sum completion over the
`t/n = 0.564` arc of a `p^{0.677}`-sized subgroup loses more than the 9.06
factor at these parameters.  Model margin (0.55 of budget) is within model
error (±2x): **`e_s = 3` truth is genuinely uncertain — a knife-edge
instance, and the smallest honest sub-wall.**  Label: OPEN.

## Honest wall and steering (ANALYSIS)

- No uniform-in-`e_s` bound `|T(n',e_s)| ≤ H2` can be proved: it is
  heuristically **false** throughout `e_s ∈ [4, 59]` (30x over budget already
  at `e_s = 4`, where we exhibit witnesses at deployed scale).
- The chain's case `e = 67472` sits deep in the paucity regime
  (`load < 2^−1344158`).  A proof should target **vanishing/paucity specific
  to large side size** — e.g. no free-1 pair of disjoint 67472-sets on the
  arc at all — rather than a counting bound that would also have to be false
  in the mid-band if uniform.  The coset family (L3) is not an obstruction:
  it dies at `e_s ≥ 3`; recursion of the antipodal mechanism into `mu_{n/2}`
  is also load-dead at `e = 67472` (pair entropy 218,937 bits versus
  1,045,785 denominator bits).
- Smallest candidate-counterexample families that survive the sweep: generic
  birthday collisions in the mid-band (`e_s ∈ [4,59]`) — abundant but
  irrelevant to the chain; at `e = 67472` no surviving family is known, and
  the model predicts none exists.

## Reconciliation with the v51–v54 chain

Hughes's reduction stands untouched and is used as-is: v51 (U2e) + v53
(C_unique, `N_C = 1`) + v54 (terminal star) give `|H_unt| ≤ |T|`, so the
residual card needs exactly `|T| ≤ H2` at `(n', e) = (1183520, 67472)` — the
statement pinned above, with H2 fixed by v45's `M_pad ≤ 2` payment.  This
packet plugs in as follows: (i) the faithfulness pins F1–F4 fix the
definitional edges the STATUS line leaves implicit, in the direction his
chain consumes; (ii) the `e_s`-parametric map shows his `e = 2` close and his
open `e > 2` line are not two points on one curve — the family is
heuristically false in the mid-band `[4, 59]` and true with astronomical
margin at his actual `e = 67472` — so the wall should be attacked as a
large-`e` paucity theorem, where the truth has 1.34 million bits of heuristic
room, not via side-size induction; (iii) the deployed witnesses at
`e_s ∈ {3,4}` calibrate what "false in the mid-band" means concretely and
retire any strategy premised on small-`e_s` vanishing; (iv) his terminal-star
insight is what makes all of this measurable — `T` is exactly the right
finite object, and our L2 restatement (unique terminal set per high) is a
direct corollary of his v53 max-forcing plus v25 disjointness.  Everything
here that is not arithmetic is downstream of his structure theorems.

## Non-claims

- Does **not** prove `|T| ≤ H2` at any open side size (3, 4, …, 67472); the
  deployed wall remains OPEN.
- Does **not** refute any Hughes claim: the chain needs only `e = 67472`, and
  no claim of his covers `e_s ∈ [3, 59]`.  The mid-band overload is a model
  prediction, **not** a COUNTEREXAMPLE verdict: witnesses prove
  `|T(n',4)| ≥ 1972`, far below `H2`, and no `|T| > H2` is claimed anywhere.
- Witness lower bounds are for the canonical `omega` arc only (F4).
- The load model is a heuristic; its calibration is measured on toys with
  ~2x scatter at `e = 4`.  Model numbers are labeled ANALYSIS; only the
  integer gates are PROVED.
- Does not prove `A_SP ≤ t·p`, `|R2| ≤ e·p`, `U ≤ B*`, or anything about
  other rows.

## Reproducibility

Zero-argument, stdlib-only, deterministic full replay (toy ladder, both
witness searches, all arithmetic gates) against the checked-in certificate,
plus 11 live tamper tests:

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_hughes_wall_small_e.py
```

Reference run: `RESULT: PASS (671/671 checks; tampers 13/13)`, ~55 s wall
time, peak RSS 220 MiB.  Certificate:
`experimental/data/cap25_v13_hughes_wall_small_e.json`.  Regenerate with
`--generate` (maintainer only).  Ladder totals: 99,613,782 subset
evaluations + 142.6M cheap witness trials + 36.6M family-scan lookups,
chunked, under `RLIMIT_AS` 2 GiB.
