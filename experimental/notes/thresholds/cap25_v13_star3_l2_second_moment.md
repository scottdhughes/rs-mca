# CAP25 v13: the L2 / second-moment estimate for the star3 sub-wall

**Status:** L2 PARSEVAL IDENTITIES EXACT (PROVED) / CAUCHY–SCHWARZ = #484 CUT (a)
WITH UNCONDITIONAL 5515·H2 FLOOR (PROVED) / large-sieve "few large frequencies"
premise fails for T2 (MEASURED) / phase-essentiality wall (ANALYSIS) — the
point-count `P <= H2` and hence the sub-wall `star3` stay **OPEN**.

This packet works the analytic opening PR #484 named — the **second-moment /
large-sieve** over the frequency family — for Scott Hughes's smallest honest
sub-wall.  PR #482 reduced `star3` to a point count `P <= H2`; PR #484 wrote `P`
as an additive-character double sum, proved its principal frequency is exactly
#479's load `0.5515·H2`, and reduced `star3` to a non-principal budget
`|P_err| <= 0.4485·H2`.  #484 cut naive family Cauchy–Schwarz as "dead by `5862x`"
and asked whether a genuine second-moment / large-sieve bound could supply the
average square-root cancellation the budget needs.  Here we (1) compute the two
exact `L2` second moments over the frequency group `F_p^2` **in closed form**
via Parseval, verified to the integer on toys; (2) prove the Cauchy–Schwarz route
*across the two factors* `T3, T2` is #484's cut (a) — Fourier-dual identical —
and that its output is **`>= 5515·H2` for every collision profile**, an
unconditional floor set by the irreducible triple-count diagonal (PTE-type
rigidity gains only `~6%`); (3) measure that the large-sieve premise "large `|T2|`
lives on few frequencies" **fails** — the `|T2|^2` mass is quasi-equidistributed,
so no dyadic split escapes the floor; (4) bank the wall: the `psi(-u·zeta)` phase
is load-bearing, so `star3` needs *signed* cancellation, not any absolute-value
second moment.  No sub-wall is closed.  Everything is downstream of Hughes's
v51–v54 chain and #479/#482/#484's pins.

## The object, recalled (source of truth: #484 R1/R2, its verifier)

Deployed KB row: `p = 2130706433 = 2^31 − 2^24 + 1`, `n = 2^21`, subgroup index
`(p−1)/n = 1016`, canonical `omega`, arc `A := I_{n'−1} = {omega^0,…,omega^{n'−2}}`,
`|A| = n'−1 = 1183519`, `zeta = omega^{n'−1}`.  From #484 (all EXACT/PROVED):

```text
P_ord = (1/p^2) Σ_{u,v ∈ F_p} psi(−u·zeta) · T3(u,v) · T2(u,v),   P = P_ord/12,
  T3(u,v) = Σ_{ordered distinct a,b,c ∈ A}  psi( u·e1(a,b,c) + v·e2(a,b,c) ),
  T2(u,v) = Σ_{ordered distinct x,y ∈ A}    psi( −u(x+y) − v(xy + zeta(x+y)) ),
P_main := [P_ord at (0,0)]/12 = C(n'−1,2)·C(n'−1,3)/p^2 = 0.551457·H2   (PROVED),
(star3)  P <= H2 = 77291948627   ⟸   |P_err| <= H2 − P_main = 0.448543·H2
                                                 = 34668731738.         [OPEN]
```

with `C(n'−1,2) = 700358019921`, `C(n'−1,3) = 276295207554280719`,
`p^2 = 4539909903627583489`.  #484's named opening: a second-moment / large-sieve
bound on `Σ_{(u,v)≠0}|T3 T2|` supplying `⟨|T3 T2|⟩ ≲ 5.383·H2` per frequency.

## Rung 1 — the two exact L2 second moments (PROVED)

Both `T3` and `T2` are Fourier transforms (over the frequency group `F_p^2`) of
symmetric-function histograms, so Parseval evaluates their total `L2` mass over
all frequencies to an exact collision count.

**T2 second moment — closed form.**  Write `T2(u,v) = 2 Σ_{unordered {x,y}⊆A}
psi(−u(x+y) − v(xy+zeta(x+y)))`; the phase depends only on `(x+y, xy)` (an affine
image of `(alpha, xy)` with `alpha = x+y`).  Since a pair is determined by its
sum and product, **pairs have no nontrivial collision**, and Parseval gives, with
`D2 = (n'−1)(n'−2)`,

```text
Σ_{u,v} |T2(u,v)|^2  =  p^2 · #{(x,y),(x',y') ordered : x+y=x'+y', xy=x'y'}
                     =  2 p^2 D2  =  4 p^2 C(n'−1,2)            (EXACT).
Deployed:  Σ|T2|^2 = 2 p^2 (n'−1)(n'−2) = 12718249242897409229416610737476.
Non-principal (drop (0,0), T2(0,0)=D2):  Σ_{(u,v)≠0}|T2|^2 = D2(2p^2 − D2).
```

**T3 second moment — the collision energy.**  With `T3(u,v) = 6 Σ_{3-sets S⊆A}
psi(u·e1(S)+v·e2(S))` and `M(h) := #{3-sets of A with high h=(e1,e2)}`,

```text
Σ_{u,v} |T3(u,v)|^2  =  36 p^2 · Σ_h M(h)^2,   Σ_h M(h)^2 = C(n'−1,3) + 2 L3,
```

where `L3` = number of unordered equal-high 3-set pairs (a degree-2
Prouhet–Tarry–Escott collision count on the arc, #482 C2).  The **diagonal**
`Σ_h M(h) = C(n'−1,3)` is an unconditional lower bound on `Σ_h M(h)^2` (each
`M(h) ≥` its own contribution), i.e. `S := Σ_h M(h)^2 ≥ C(n'−1,3)` always, with
equality iff no two arc-triples share a high.  Non-principal
`Σ_{(u,v)≠0}|T3|^2 = 36(p^2 S − C(n'−1,3)^2)` (since `T3(0,0) = D3 = 6C(n'−1,3)`).

**Verification (to the integer).**  On KB-shape toy arcs the direct complex
`Σ_{u,v}|T3|^2`, `Σ_{u,v}|T2|^2` (and their non-principal parts) equal the closed
forms exactly:

| p | t | `\|A\|` | `S = Σ M^2` | `L3` | `Σ\|T3\|^2 = 36p^2 S` | `Σ\|T2\|^2 = 2p^2 D2` |
|---:|---:|---:|---:|---:|---:|---:|
| 17 | 9 | 8 | 58 | 1 | 603432 | 32368 |
| 97 | 18 | 17 | 716 | 18 | 242526384 | 5118496 |
| 257 | 27 | 26 | 2666 | 33 | 6339118824 | 85863700 |

## Rung 1/2 — Cauchy–Schwarz across (T3,T2) IS #484's cut (a), and its floor (PROVED)

Cauchy–Schwarz across the two factors, applied to the non-principal sum (the
principal term is `P_main`, extracted exactly), gives

```text
|P_err| <= (1/12p^2) √(Σ_{(u,v)≠0}|T3|^2) · √(Σ_{(u,v)≠0}|T2|^2)
        =  √(C(n'−1,2)·(S − C(n'−1,3)^2/p^2)) · √(1 − D2/2p^2).      (†)
```

The `12p^2` cancels exactly against the `36·2` in the two Parseval identities.
Dropping the `√(1 − D2/2p^2)` (which is `1 − 7.7·10^{-8}` at the deployed row)
gives the **centered high-space Cauchy–Schwarz** `√(C(n'−1,2)·(S − C(n'−1,3)^2/p^2))`,
and its *uncentered* form `√(C(n'−1,2)·S)` is byte-for-byte #484's cut (a):

```text
√(C(n'−1,2)·S)  = 453080737874835 = 5861.94·H2          (= #484 cut (a), "5862x")
```

So **the `T3/T2` factorization does not escape #484's cut — it is the same
Cauchy–Schwarz, viewed over frequency space instead of high space** (Fourier
duality; relation `(†)` is verified on every toy row to `<10^{-6}` relative).
Extracting the principal frequency (= centering `M` about its mean) improves the
constant by only `~3%`:

```text
centered, modelled S = C3 + C3^2/p^2 :  √(C(n'−1,2)·C(n'−1,3)) = 439892673815304 = 5691.31·H2
```

**Unconditional floor (PROVED).**  Because `S ≥ C(n'−1,3)` for *every* collision
profile, the Cauchy–Schwarz output `(†)` obeys

```text
|P_err|_CS  >=  √( C(n'−1,2)·(C(n'−1,3) − C(n'−1,3)^2/p^2) )·√(1−D2/2p^2)
            =  426296814343656  =  5515.41·H2  =  12296·(0.4485·H2 budget).
```

The route is **dead by `≥ 12296x`, unconditionally** — and the barrier is *not*
collision abundance.  The off-diagonal `2L3 ≈ C(n'−1,3)^2/p^2` is only `0.0609`
of the diagonal, so killing **all** off-diagonals (perfect PTE-type rigidity,
`S → C(n'−1,3)`) moves the constant `5861.94·H2 → 5515.41·H2`, a `5.91%` gain.
The `√(C(n'−1,3))` diagonal — the sheer count of arc-triples — is irreducible.
Note the Cauchy–Schwarz output `5515·H2` is even **worse than the trivial bound**
`P ≤ C(n'−1,2) = 9.0612·H2` (#479 L2): the `L2` route buys nothing over trivial.

## Rung 2 — the large-sieve "few large frequencies" premise fails for T2 (MEASURED)

The large-sieve refinement would split the family by `|T2|` level sets — few
large frequencies (bounded `T3` mass) plus many small frequencies (average
cancellation).  The degree-2 factor has the bilinear shape

```text
T2_full(u,v) = Σ_{x∈A} psi(−w x)·G(w + v x),  w = u+v·zeta,  G(c)=Σ_{y∈A} psi(−c y),
on v=0:  T2(u,0) = G(u)^2 − G(2u)          (G = incomplete arc character sum).
```

But the premise is false: the `|T2|^2` mass is **quasi-equidistributed**, with no
sparse heavy set to isolate.  Measured over all `p^2` frequencies (exact
non-principal total `= D2(2p^2−D2)`, matched to the integer):

| p | t | axis-set share | top-`2p` share | freq. fraction holding ½ the mass |
|---:|---:|---:|---:|---:|
| 17 | 9 | 0.1111 | 0.3092 | 0.219 |
| 97 | 18 | 0.0293 | 0.1170 | 0.166 |
| 257 | 27 | 0.0062 | 0.0601 | 0.167 |

Half the non-principal `L2` mass is spread over `~17%` of **all** `p^2`
frequencies (stable with arc size); the axis-set share is small and **shrinks**
(`0.111 → 0.029 → 0.006`), and the top-`2p` share falls (`0.309 → 0.117 →
0.060`).  There is no `O(p)`-sized heavy set — so a dyadic "few large × bounded +
many small × cancellation" split has no small part to gain from, and **any
reweighting of absolute values inherits the `5515·H2` diagonal floor of Rung 1.**

## Rung 4 — the absolute-value route is dead and growing (MEASURED)

The phase-free pointwise sum `Σ_{(u,v)≠0}|T3||T2|/(12p^2)` — the largest anything
that bounds `Σ|T3 T2|` can hope to control — overshoots the budget by a factor
**growing with arc size** (toy budget analogue `0.8134·P_main`, from the deployed
`0.4485/0.5515` split):

| p | t | `Σ_{≠0}\|T3\|\|T2\|/(12p^2)` | `P_main` | ratio to `P_main` | × over budget |
|---:|---:|---:|---:|---:|---:|
| 17 | 9 | 27.485 | 5.426 | 5.07 | 6.23 |
| 97 | 18 | 229.68 | 9.829 | 23.4 | 28.7 |
| 257 | 27 | 699.01 | 12.79 | 54.6 | 67.2 |

This is #484's route-cut (c) — the pointwise/triangle loss — now confirmed to
grow through the arc and re-established as a statement about the **whole
absolute-value family**: no bound on `Σ|T3 T2|` (weighted or not, as long as it
is the absolute value) can reach `0.4485·H2`, because the second moment floors at
`5515·H2` (Rung 1) and the phase-free sum overshoots and grows (here).

## Rung 5 — obstruction, smallest statement, falsifier (ANALYSIS)

- **Exact obstruction (the wall).**  The `psi(−u·zeta)` twist is *load-bearing*.
  Every absolute-value second-moment / large-sieve estimate is ruled out: the
  `L2` second moment is exactly the dead Cauchy–Schwarz (`5515–5862·H2`,
  Rung 1), the `|T2|` level sets carry no sparse heavy mass to dyadically exploit
  (Rung 2), and the phase-free sum overshoots and grows (Rung 4).  What remains —
  and what `star3` actually requires — is **signed** cancellation:

  ```text
  Σ_{(u,v)≠(0,0)} psi(−u·zeta)·T3(u,v)·T2(u,v)  =  12 p^2 · P_err,
  ```

  i.e. a Weil/Kloosterman-type bound for the two-parameter frequency family with
  the additive twist intact.  The second moment (which discards the phase) cannot
  see it; this sharpens #484's cuts (a),(c) into a statement over the entire
  family.
- **Smallest sufficient statement.**  `|Σ_{(u,v)≠0} psi(−u·zeta) T3 T2| ≤
  0.4485·12·p^2·H2`, an average `|T3 T2| ≲ 5.383·H2` per frequency *with the sign
  from `psi(−u·zeta)`* — square-root cancellation of the **signed** family, the
  one input neither pointwise (#484 (c)) nor second-moment (this packet) methods
  supply.
- **Scaling in the side size `e` (the terminal wall).**  The same obstruction is
  categorical at general `e`: the `e`-fold analogue's second moment carries the
  diagonal floor `√(C(n'−1,e−1)·C(n'−1,e))`, astronomically large across the
  overload band `e ∈ [4,59]` (#479) and hopelessly loose at the chain-relevant
  `e = 67472`, where #479's load `< 2^{−1344158}` predicts total paucity
  (`|T| = 0`).  A second moment can never certify vanishing — confirming #479's
  steering that the terminal wall must be attacked as a **large-`e` paucity
  theorem**, not a counting/`L2` bound.
- **Falsifier.**  A KB-shape arc at deployed sparsity (`q ≈ 1016`) on which the
  *signed* family sum exceeds `0.4485·12·p^2·H2`-analogue — equivalently `P > H2`
  (#484's falsifier).  None exists in the scanned range; the shrinking relative
  error of #484 is consistent with the signed sum staying small.

## Reconciliation with #484, #482, #479 and Hughes's chain

Hughes's reduction (v51 U2e → v53 C_unique → v54 terminal star), #479's pins
F1–F4 / L1–L6, #482's incidence reduction R1–R2 and characterizations C1–C2, and
#484's character-sum setup + principal-frequency identity + route-cut ledger all
stand untouched and are used as-is.  This packet adds: (i) the two **exact `L2`
Parseval second moments** (Rung 1) — `Σ|T2|^2 = 2p^2 D2` in closed form, and
`Σ|T3|^2 = 36 p^2 Σ_h M(h)^2` with the collision-energy structure and its
diagonal floor; (ii) the **PROVED identification** of Cauchy–Schwarz-across-(T3,T2)
with #484's cut (a) (Fourier duality, relation `(†)` verified on toys), and its
**unconditional `5515·H2` floor** — answering #484's explicit question "does this
factorization escape the cut?" with *no, provably, and PTE rigidity gains only
`~6%`"*; (iii) the MEASURED refutation of the large-sieve concentration premise
for `T2`; (iv) the phase-essentiality wall, sharpening #484's (a),(c) into a
family-wide statement that redirects the search to signed cancellation.  This is a
contribution into Hughes's Route-D program; if a trace-function input is ever
used for the signed bound, his `mersenne_reciprocal_gap` offer context (via #434)
is the natural interface.  Everything non-arithmetic is downstream of his
structure theorems and #479/#482/#484's reductions.

## Non-claims

- Does **not** prove `star3` (`|T(n',3)| <= H2`), `P <= H2`, or the deployed wall
  `|T(n',67472)| <= H2`; all stay OPEN.  The `L2` route is shown **dead**, not
  successful — this packet closes off an approach, it does not close the sub-wall.
- Does **not** obtain any bound `P_err <= c·H2` with `c` below the trivial `8.51`
  (`= 9.0612 − 0.5515`); the Cauchy–Schwarz output (`5515–5862·H2`) is worse than
  trivial.  The only PROVED inequality direction here is a **lower** bound on the
  method's output (the `5515·H2` floor), showing it cannot reach the budget.
- Does **not** refute any Hughes, #479, #482, or #484 claim.  It confirms and
  sharpens #484's cuts (a) and (c).
- PROVED: the two `L2` identities (exact, verified to the integer on toys) and the
  Cauchy–Schwarz floor (`S ≥ C(n'−1,3)`, an exact integer inequality).  MEASURED:
  the `|T2|` non-concentration and the growing pointwise overshoot, on toys with
  `t ≤ 27`; the deployed `t ≈ 1.18·10^6` is a `~10^4x` extrapolation.  ANALYSIS:
  the phase-essentiality wall and the `e`-scaling remark.
- The signed-cancellation input named in Rung 5 is stated, **not** established.
- Measurements are on the canonical `omega` arc (#479 F4).

## Reproducibility

Zero-argument, stdlib-only, deterministic full replay (deployed exact integer
identities and Cauchy–Schwarz floor, the `L2` Parseval identities on tiny arcs,
the `|T2|` level-set profile, the absolute-value overshoot, the #484
cross-checks) against the checked-in certificate, plus live tamper tests:

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_star3_l2_second_moment.py
```

Reference run: `RESULT: PASS (126/126 checks; tampers 18/18)`, ~57 s, peak RSS
19 MiB.  Certificate: `experimental/data/cap25_v13_star3_l2_second_moment.json`.
Regenerate with `--generate` (maintainer only).
