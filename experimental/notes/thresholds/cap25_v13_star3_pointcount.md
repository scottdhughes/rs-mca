# CAP25 v13: the point-count P <= H2 for the star3 sub-wall

**Status:** CHARACTER-SUM SETUP EXACT / PRINCIPAL-FREQUENCY = LOAD (PROVED) /
completion-loss ledger MEASURED / obstruction quantified (ANALYSIS) — the
point-count `P <= H2` and hence the sub-wall `star3` stay **OPEN**.

This packet works the analytic core of the single missing input for Scott
Hughes's smallest honest sub-wall.  PR #482 proved the incidence reduction
`|T(n',3)| <= P` and recast `star3` as the point-count `P <= H2`; here we
(1) write `P` as an explicit additive-character double sum and verify the setup
reproduces the exact integer `P` on toys, against both a brute `arc^5`
enumeration and #482's fiber dictionary; (2) prove that the **principal
frequency** `(u,v)=(0,0)` of that expansion contributes *exactly* #479's
heuristic "load" `0.5515·H2`, turning `P <= H2` into an explicit bound on a
single non-principal incomplete-character sum with budget `0.4485·H2`;
(3) bank a route-cut ledger with exact constants (Cauchy–Schwarz loses `5862x`,
arc→group relaxation recovers the trivial `9.06`, pointwise completion loses
`~p^2`); (4) measure the frequency split on toys — the relative error shrinks
with scale toward #482's `~1%`.  No sub-wall is closed.  Everything is
downstream of Hughes's v51–v54 chain and #479/#482's pins.

## The object, recalled (source of truth: #482 R1/R2, its verifier)

Deployed KB row: `p = 2130706433 = 2^31 − 2^24 + 1`, `n = 2^21`, subgroup index
`(p−1)/n = 1016`, canonical `omega = 3^{(p−1)/n}`, arc
`I_{n'} = {omega^0,…,omega^{n'−1}}`, `n' = 1183520`, terminal point
`zeta = omega^{n'−1}`.  Write `A := I_{n'−1} = {omega^0,…,omega^{n'−2}}` (the
arc minus `zeta`), `|A| = n'−1 = 1183519`.  From #482:

```text
P := #{ ({x,y}, {a,b,c}) : {x,y}⊆A a pair, {a,b,c}⊆A a triple,
        e1{a,b,c} = e1{x,y,zeta},  e2{a,b,c} = e2{x,y,zeta} }
   = #{ 3-subset {a,b,c}⊆A : the forced quadratic
        X^2 − (s−zeta)X + (q − zeta·s + zeta^2),  (s,q) = (e1,e2){a,b,c},
        splits into two distinct points x,y of A }.                    [#482 R1/R2]
(star3)   |T(n',3)| <= P <= H2  ⟹  |T(n',3)| <= H2 = 77291948627.       [OPEN]
```

By #482 R1 each non-terminal triple is the partner of at most one terminal pair,
so the two displays agree.  Trivial bound `P` heuristic value `≈ 0.55·H2`
(below), slack `≈ 1.81x`.

## Rung 1 — exact character-sum setup (EXACT)

Let `psi(z) = e_p(z) = exp(2πi z / p)`.  Count **ordered** tuples
`(a,b,c,x,y) ∈ A^5` with `a,b,c` distinct and `x,y` distinct satisfying the
linear `a+b+c = x+y+zeta` and the quadratic `ab+ac+bc = xy + zeta(x+y)`.
Opening both constraints with additive characters (`[w=0] = p^{-1}Σ_u psi(uw)`)
and separating the `a,b,c` block from the `x,y` block:

```text
P_ord = (1/p^2) Σ_{u,v ∈ F_p}  psi(−u·zeta) · T3(u,v) · T2(u,v),
  T3(u,v) = Σ_{ordered distinct a,b,c ∈ A}  psi( u·e1(a,b,c) + v·e2(a,b,c) ),
  T2(u,v) = Σ_{ordered distinct x,y ∈ A}    psi( −u(x+y) − v(xy + zeta(x+y)) ),
and   P = P_ord / 12
```

(`6` orderings of the partner triple × `2` of the terminal pair; the pair is
unique per triple by R1, and equal-high 3-sets are automatically disjoint by
#479 L1, so no cross-overlap term is needed).  `T3` carries the genuine
3-variable symmetric quadratic `e2 = ab+ac+bc`; `T2` completes to a shifted
bilinear form `Σ psi(−β x'y')` after `x' = x + α/β`, `α = u+v·zeta`, `β = v`.
**Both are incomplete** because `A` is an *interval* in the cyclic index group,
not a subgroup — this is where the arc structure enters.

**Verification (to the integer).**  On tiny arcs the double sum reproduces `P`
exactly, matching both a brute `A^5` count and #482's fiber dictionary:

| p | t | P (fiber) | 12·P | P_ord (brute A^5) | P_ord (char sum) |
|---:|---:|---:|---:|---:|---:|
| 17 | 9 | 2 | 24 | 24 | 24 (im `<1e-6`) |
| 97 | 18 | 7 | 84 | 84 | 84 (im `<1e-6`) |

The setup — signs, the `psi(−u·zeta)` phase, the distinctness, the `/12` — is
correct.

## Rung 1/2 — the principal frequency IS the load (PROVED), and the exact target

The `(u,v)=(0,0)` term of `P_ord` is `(1/p^2)·T3(0,0)·T2(0,0)
= (1/p^2)·(n'−1)(n'−2)(n'−3)·(n'−1)(n'−2)`, so

```text
P_main := [P_ord at (0,0)]/12 = C(n'−1,2)·C(n'−1,3) / p^2       (EXACT rational)
        = 700358019921 · 276295207554280719 / p^2
        = 42623216888.4581…  =  0.551457·H2            (floor 42623216888)
```

This is #479's heuristic **load** `4.2623e10 = 0.5515·H2` — now identified as the
*exact principal frequency* of an exact expansion, not a model number.  Hence

```text
P <= H2   ⟺   P_err := (1/12p^2) Σ_{(u,v)≠(0,0)} psi(−u zeta) T3(u,v) T2(u,v)
                     <=  H2 − P_main  =  34668731738.54…  =  0.448543·H2.
```

So `star3` reduces, with the linear-plus-quadratic constraints handled exactly,
to a single **explicit bound on the non-principal incomplete-character sum**:
the `~p^2` off-frequencies must together stay under `0.4485·H2`.  This is the
cleanest precise form of the open core — the entire content of `star3` is one
incomplete-sum inequality with a stated numeric budget.

## Rung 2 — route-cut ledger (with exact constants)

Every elementary route was pushed to an exact number and dies; the slack is only
`1.9x`, so any log-factor or Cauchy–Schwarz loss kills it, and it does.

- **(a) Cauchy–Schwarz / L2-energy — dead by `5862x`.**  `P = ⟨τ, Φ_A⟩` with
  `τ` the indicator of terminal-realizable highs (`Σ τ = C(n'−1,2) = 7.0e11` by
  R1 injectivity) and `Φ_A(h)` the count of arc-triples with high `h`.  Then
  `P <= √(Σ τ) · √(Σ_h Φ_A(h)^2)`.  At the deployed row
  `Σ_h Φ_A(h)^2 ≈ C(n'−1,3) + C(n'−1,3)^2/p^2 = 2.93e17` (diagonal-dominated —
  mean occupancy `< 1`), giving `√(C2·E2) = 4.53e14 = 5862·H2`.  C–S discards
  that `τ` lives on `7.0e11` of the `p^2 = 4.5e18` highs; **dead by ~5862x.**
- **(b) arc→group relaxation — recovers the trivial `9.06`.**  Replacing the
  interval `A` by the full group `mu_n` multiplies the count by
  `1/density^5 = 1/0.5643^5 = 17.47`, sending `P_main` to
  `0.5515·17.47 = 9.63 ≈` the trivial deficit `9.0612`.  Every relaxation that
  drops joint interval-membership of **both** forced roots recovers `≥ 9.06`:
  the whole `>9x` saving over trivial is the **interval discrepancy of the two
  roots** and nothing else.  (Relaxing "both roots in `A`" to "one root in `A`",
  or "roots in the whole field", likewise returns `≫ H2`; the two-roots-in-
  interval constraint is irreducible.)
- **(c) pointwise completion — dead by `~p^2` (measured).**  The triangle
  inequality `|P_err| <= (1/12p^2) Σ_{(u,v)≠0}|T3||T2|` overshoots the true
  `|P_err|` by a factor that is essentially `p`-*independent while the true error
  decays as `1/p^2`* at fixed arc, i.e. the loss grows like `~p^2` (see the
  sweep below).  At deployed `p ≈ 2.1e9` this is a loss of order `10^{18}`,
  astronomically past the `1.9x` slack.  Only genuine cancellation among the
  `~p^2` frequencies — not any pointwise/Polya–Vinogradov bound — can close it.

## Rung 3 — the partial result (CONDITIONAL) and why no `c < 9.06` is free

We obtain **no unconditional `P <= c·H2` with `c < 9.06`**: every route in the
ledger that drops the interval structure returns `≥ 9.06` (b), and every
pointwise completion returns `≫ H2` (c).  The honest partial is the conditional

```text
P <= H2  (hence star3)   ⟸   Σ_{(u,v)≠(0,0)} psi(−u zeta) T3 T2  ≤  12 p^2 (H2 − P_main)
                                                                 =  0.4485·12·p^2·H2,
```

with `P_main = 0.5515·H2` proved exactly.  The smallest sufficient standard
input is a **square-root-cancellation-on-average** estimate for the
arc-restricted symmetric sums `T3, T2` (an `L2`/large-sieve bound over the
`(u,v)`-family, not a pointwise one) strong enough to hold the non-principal
mass under `0.4485·H2`.  Quantitatively the needed average size is
`⟨|T3 T2|⟩ ≲ 5.4·H2·(1/p^2-normalised)` — i.e. the family must exhibit
cancellation of the same order the second moment of `Φ_A` predicts.

## Rung 4 — measured frequency split and cross-check (MEASURED)

Exact recompute on tiny arcs (`P` by fiber dictionary; `P_main`, `P_err`, and
the pointwise bound by the full `(u,v)` sum).  Two trends are robust.

**Relative error shrinks with scale** (growing KB-shape arc `t = 9n/16`):

| p | t | P | P_main | P_err | \|P_err\|/P_main | pointwise loss |
|---:|---:|---:|---:|---:|---:|---:|
| 17 | 9 | 2 | 5.426 | −3.426 | 0.631 | 8.0x |
| 97 | 18 | 7 | 9.829 | −2.829 | 0.288 | 81.2x |
| 241 | 27 | 16 | 14.549 | +1.451 | 0.100 | 484.6x |

The relative non-principal error falls `0.63 → 0.29 → 0.10` as the arc grows,
extrapolating toward the `~1%` #482 measured at larger deployed-like rows (its
`n=1280`: `P/C(t−1,2)=0.11402` vs `lambda=0.11620`).  The **sign** of `P_err` is
*not* one-sided (negative at `t=9,18`, positive at `t=27`): at tiny counts it is
fluctuation; the principal density term dominates and the interval discrepancy is
a shrinking correction — **no suppression law is claimed.**

**Pointwise loss grows like `~p^2`** (fixed small arc `t = 9`, growing `p`):

| p | 17 | 97 | 193 | 257 |
|---|---:|---:|---:|---:|
| pointwise loss (bound/\|err\|) | 8.0x | 184x | 740x | 1308x |

The pointwise bound stays `~31` (`p`-independent) while `|P_err| ∝ 1/p^2`, so the
triangle-inequality loss `∝ p^2` — the frequencies cancel, the bound cannot see
it.  This is route-cut (c) made exact.

**Cross-check against #482 (exact `P`).**  The fiber count reproduces #482's
published `P` byte-for-byte on its own rows: gradient `q=4` `P=58`; ladder dense
`n=384` `P=3074`; crossing `n=512` `P=1331`; deployed-like `n=1024` `T=P=6`.
`|T| <= P` holds on every row.

## Rung 5 — obstruction, smallest statement, falsifier (ANALYSIS)

- **Exact obstruction.**  `P = P_main + P_err` with `P_main = 0.5515·H2` PROVED
  exactly; the open core is `P_err <= 0.4485·H2`, a bound on the `~p^2`
  non-principal frequencies of an incomplete-character sum whose incompleteness
  is exactly the arc being an **interval** (density `0.5643`) rather than a
  subgroup.  The whole difficulty is the joint interval-membership of the two
  forced roots (ledger (b)); every completion that ignores it loses `≫ 1.9x`
  (ledger (a),(c)).
- **Smallest sufficient statement.**  A second-moment / large-sieve bound
  `Σ_{(u,v)≠0}|T3 T2| ≤ 0.4485·12 p^2 H2` for the two arc-restricted symmetric
  sums — square-root-cancellation *on average over the family*, the one input
  pointwise methods cannot supply.
- **Falsifier.**  A KB-shape arc at deployed sparsity (`q ≈ 1016`, `n <= 2^21`)
  with `P > H2`-analogue — equivalently `P_err > 0.4485·P_main`-analogue with the
  wrong sign and size.  #482's validated model puts the crossing at `~1.92x`
  deployed size; none exists in the exhaustively scanned range, and the shrinking
  relative error above is consistent with `P_err` staying a small correction at
  deployed scale.

## Reconciliation with #482, #479 and Hughes's chain

Hughes's reduction (v51 U2e → v53 C_unique → v54 terminal star), #479's pins
F1–F4 / lemmas L1–L6, and #482's incidence reduction R1–R2 and fiber/power-sum
characterizations C1–C2 stand untouched and are used as-is.  This packet adds:
(i) the explicit character-sum expression for `P` (Rung 1), verified to the
integer against #482's fiber count and a brute enumeration; (ii) the PROVED
identity that #479's *heuristic* load `0.5515·H2` is the *exact* principal
frequency, converting `star3` into one incomplete-sum inequality with budget
`0.4485·H2`; (iii) an exact-constant route-cut ledger (C–S `5862x`, arc→group
`9.06`, pointwise `~p^2`) that says precisely which analytic input is and is not
enough; (iv) a measured frequency split whose shrinking relative error matches
#482's calibration.  Everything non-arithmetic is downstream of Hughes's
structure theorems and #482's reduction.

## Non-claims

- Does **not** prove `P <= H2` or `star3` (`|T(n',3)| <= H2`); both stay OPEN,
  as does the deployed wall `|T(n',67472)| <= H2`.
- Does **not** obtain any unconditional `P <= c·H2` with `c < 9.06`; the only
  bound is the CONDITIONAL Rung-3 statement.  The `0.4485·H2` budget and the
  needed average cancellation are stated but **not** established.
- Does **not** refute any Hughes, #479, or #482 claim.  The positive `P_err` at
  `t=27` is a tiny-count fluctuation, not a counterexample; `P_err`'s sign is
  explicitly not claimed one-sided.
- Only the integer/rational gates and the `(0,0)`-frequency `= P_main` identity
  are PROVED.  The character-sum expression is EXACT (an identity, verified on
  toys); the frequency-split trends, the `~p^2` pointwise-loss law, and the
  extrapolation to `~1%` are MEASURED on toys with `t <= 27`; the deployed
  `t ≈ 1.18e6` is a `~10^4x` extrapolation.
- Measurements are on the canonical `omega` arc (#479 F4).

## Reproducibility

Zero-argument, stdlib-only, deterministic full replay (deployed exact
arithmetic, the character-sum identity on tiny arcs, the frequency split, the
#482 fiber cross-checks) against the checked-in certificate, plus live tamper
tests:

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_star3_pointcount.py
```

Reference run: `RESULT: PASS (121/121 checks; tampers 15/15)`, ~40 s, peak RSS
51 MiB.  Certificate: `experimental/data/cap25_v13_star3_pointcount.json`.
Regenerate with `--generate` (maintainer only).
