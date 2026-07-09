# CAP25 v13: a closed-form sufficient band for the connectivity hypothesis
# `Conn_a` — closing the one item PR #428 left OPEN, via a Krawtchouk
# character-sum count of weight-`a` words per kernel coset

Status: `PROVED` (§2 the **MacWilliams identity** `N_a(x_0+C)*|C^perp| =
sum_{u in C^perp} chi(-<u,x_0>) K_a(wt u)`, a complete derivation, exact-tested
against direct enumeration; §3 the **head-word lemma** and the **sufficient-band
theorem** `Conn_a` holds when `mu > sum_{u in C^perp, u notin H} |K_a(wt u)|`,
a complete triangle-inequality argument; §6 the **hypothesis-free corollary** —
four of #428's ship configs have their `a` inside this proved band, so #428's
occupancy `= p^{-defect}` becomes **unconditional** there; §2 the **Parseval
second-moment identity** and §1 the **dual-dimension** identity `|C^perp| =
p^{dim_Fp V_T}`) / `DERIVED` (§5 the `F16@R4:N12` `a = 6` **interior hole** of
#428: identity (I) evaluates to an **exact character-sum cancellation**
`2*C(12,6) + err = 1848 - 1848 = 0`, so `N_6 = 0` at the uncovered coset — #428's
one anomalous hole promoted from measured to derived) / `PROVED-AT-TOYS` (the
`d(C) >= R+1` Vandermonde min-distance, verified exactly and sometimes strict) /
`MEASURED` (§4 the **sharpness** of the band — it equals the clean interval
`[R, N-R]` on the odd-`R` large-kernel unsigned toys, and is an exact **subset**
of #428's measured full-coverage band everywhere; the small-kernel / even-`R`
narrowing) / `OPEN` (§7 a proved closed-form interval; the signed and defect-`0`
configs' bands; `m >= 3`).

**Verifier:** `experimental/scripts/verify_entropy_inverse_fp_span_connectivity.py`
(zero-arg, stdlib-only, self-contained — no lane imports; `RESULT: PASS (308/308
checks)`, exit 0; ~8 s and ~16 MB peak RSS **on the authoring box** — timing and
RSS are environment-specific and deliberately not gated; best-effort `RLIMIT_AS`
guard, default 2 GB, tune or disable via `FP_CONN_AS_CAP_GB`, never fatal;
`FP_CONN_DATA_DIR` overrides the data location; `FP_CONN_DUMP` regenerates the
committed JSON from the run's own recomputation). One script that **recomputes
from scratch** — the finite-field arithmetic (smallest-irreducible modulus), the
moment-curve census, `dim_Fp V_T` / `dim_Fp D`, the **kernel code** `C = ker Phi`
and its **dual** `C^perp` (the `F_p`-row space of `Phi`) with its exact weight
enumerator, the `p`-ary Krawtchouk table, the MacWilliams coset count (I) exactly
(**integers** for `p = 2`, **`Z[omega]`** for `p = 3`), the head-aware sufficient
band, the derived `F16` hole, the Parseval identity, and the `d(C) >= R+1`
min-distance — then gates every recomputed number against the committed JSON
`experimental/data/cap25_v13_entropy_inverse_fp_span_connectivity.json` (exact on
ints / strings / bools, `1e-9` on floats). Dual path: the field multiply table vs
log/antilog (`F_27`, `F_32`). It contains an **independent brute-force** check
that the Krawtchouk equals the additive-character sum
`sum_{y: wt y = a} chi(<u,y>)`, a **soundness sweep** (band-`OK` implies `Conn_a`
true over 16 configs, zero false positives), and **six tamper self-tests**, each
threading a corrupted value through a live gate: dropping the head refinement
(the naive band is then vacuous and misses `F64-firstN`), a corrupted Krawtchouk
value (identity (I) breaks), a perturbed hole cancellation, forcing the `a = 6`
hole into the band (a soundness violation), a faked dual dimension (Parseval
breaks), and a faked weight-`R` codeword (violates `d(C) >= R+1`).

**What this is / is not.** This is a **theorem-level closure of the ONE item PR
#428 explicitly left `OPEN`** (its §4 / §8: "a closed form for the connectivity
threshold"). #428 proved the image-structure theorem *under* the connectivity
hypothesis `Conn_a` and verified `Conn_a` only by exhaustive census. This packet
supplies a **proved sufficient condition** for `Conn_a` — a clean inequality
between a main term and a Krawtchouk sum over the small dual code — that (i) is an
exact subset of #428's measured band, (ii) is **sharp** (`= [R, N-R]`) in the
large-kernel regime, (iii) **covers four of #428's seven ship configs**, turning
their occupancies `1/2, 1/2, 1/4, 1/4` into **hypothesis-free theorems**, and (iv)
**derives** #428's one anomalous interior hole as an exact character-sum
vanishing. It is **not** a proof or refutation of `prob:entropy-inverse-q`, **not**
a row-sharp / deployed-finite claim of any kind, and **not** a correction to #428
(it consumes #428's grid unchanged and extends it). **Merge framing: an
experimental/analysis note upgrading the #428 connectivity hypothesis from
`MEASURED` to a proved sufficient band, with four occupancies made unconditional
and one measured hole derived — asymptotic-lane only, no finite adjacent-row
progress claimed (§8 nonclaims).** Conventions are inherited from PR
#420/#421/#422/#428 and extended, never contradicted.

Lineage `#414 -> #416 -> #417 -> #420 -> #421 -> #422 -> #428 -> ` this packet.
PR #428 proved `image(Phi|_a) = Phi(x_0) + D` under `Conn_a`, occupancy
`= p^{-defect}`, and `image = W_c <=> defect = 0`, leaving the **closed-form
connectivity band** OPEN. This packet closes the sufficient direction.

---

## 0. What #428 left open, and the coding-theory restatement `REFERENCE`

The atom is `prob:entropy-inverse-q` in `experimental/grande_finale.tex` (L827;
escape clause L828, removal list L839, alternatives (a)/(b) L862/863,
`prop:vandermonde-kills-low-rank` L876 — present in main `b99b2c4`, gated as
committed constants by the verifier's provenance block, exactly as in #422/#428).
PR #422 identified the `F_p`-span cell; PR #428 computed the exact image under

> **`Conn_a`**: `image(Phi|_a) = ` the full coset `Phi(x_0) + D`, equivalently
> **every coset of the kernel code `C = ker Phi` of the correct head syndrome
> contains a weight-exactly-`a` word** (#428 §2.2, §4).

#428 verified `Conn_a` by census at all seven configs and left a closed form
`OPEN`. `Conn_a` is a **coset weight-distribution property** of the length-`N`
`F_p` code `C`; this packet resolves the *sufficient* direction with the
MacWilliams transform of `C`.

**Slice / scope.** For unsigned `p = 2` the slice is the weight-`a` words of
`F_2^N`; for signed `p = 3`, `{-1,0,1}` is **all** of `F_3`, so the slice is
**all** weight-`a` words of `F_3^N` (checked explicitly). This identification —
"exactly-`a` slice `=` weight-`a` words" — is **exact only for `p in {2,3}`**; for
`p >= 5` the signed alphabet `{+1,-1}` is a proper subset of `F_p^times` and the
Krawtchouk count below fails. **This packet is scoped to `p in {2,3}`**, matching
#428's shipped configs.

---

## 1. The kernel code, its dual, and the Krawtchouk polynomial `CONVENTION`

`Phi: F_p^N -> K^R` is `F_p`-linear (`N = |T|`); `C := ker Phi` is a length-`N`
code over `F_p`. Its dual `C^perp` is the `F_p`-**row space** of `Phi` (the matrix
`M[(j,b)][t] = ` the `b`-th `F_p`-coordinate of `v_t[j] = t^j`), so

> **`dim_Fp C^perp = dim_Fp V_T`, hence `|C^perp| = p^{dim_Fp V_T}`** (gated), and
> `dim_Fp C = N - dim_Fp V_T`.

`|C^perp|` is therefore **small** (`p^{dim V_T} <= p^{1 + k*#free}`; `64` to
`2187` at the configs), so the entire dual is enumerated exactly. The row
`(j = 0, b = 0)` of `M` is the constant `1` on every column, i.e. the **all-ones
word `1` is literally a dual codeword** — the head functional; this is load-bearing
in §3.

By `prop:vandermonde-kills-low-rank` any `R` columns are `K`-independent, hence
`F_p`-independent, so `C` has **minimum distance `d(C) >= R+1`** (`PROVED`). The
verifier recomputes `d(C)` exactly: it is `R+1` at some configs and **strictly
larger** at others (`d = 6 > R+1 = 5` at `F16@R4:N12`; `d = 5 > 4` at
`S-F27@R3:N10`) — the `F_p` min-distance genuinely differs from the `R+1`
`K`-rank barrier at small toys, and the verifier gates the exact values.

The `p`-ary **Krawtchouk polynomial** is
`K_a(w) = K_a(w; N, p) = sum_{j=0}^{a} (-1)^j (p-1)^{a-j} binom(w,j) binom(N-w,a-j)`,
and the identity underlying everything,

> `K_a(w) = sum_{y in F_p^N : wt(y) = a} chi(<u, y>)` for any `u` of weight `w`,

`chi` the standard additive character of `F_p`, is proved by the coordinate
factorization (`+ (p-1)` per zero coordinate of `u`, `-1` per nonzero) and is
**brute-force verified** in the script against the exhaustive complex sum for
`p in {2,3}` (zero mismatches).

---

## 2. The MacWilliams coset count `PROVED`

**Theorem 1 (exact coset count).** For every coset `x_0 + C` and every `a`,

> **(I)  `N_a(x_0 + C) * |C^perp| = sum_{u in C^perp} chi(-<u, x_0>) K_a(wt u)`,**

where `N_a(x_0 + C) = #{ y in x_0 + C : wt(y) = a }`.

*Proof.* The indicator of `C` is `[y in C] = (|C|/p^N) sum_{u in C^perp}
chi(<u,y>)` (characters of `F_p^N/C`). Then
`N_a(x_0+C) = sum_y [y - x_0 in C][wt y = a] = (|C|/p^N) sum_{u in C^perp}
chi(-<u,x_0>) sum_{y: wt y = a} chi(<u,y>)`, and the inner sum is `K_a(wt u)`
(§1); `|C|/p^N = 1/|C^perp|`. `∎`

The `u = 0` term is the **main term** `K_a(0) = binom(N,a)(p-1)^a` — the total
weight-`a` count divided across the `|C^perp|` cosets. **Identity (I) is
exact-tested**: for three-plus configs and `>= 3` distinct cosets each, the
character-sum count (evaluated in `Z` for `p = 2`, in `Z[omega]` with
`omega^2 = -1 - omega` for `p = 3`) equals the **directly enumerated** bucket
count of the census, to the integer.

**Theorem 1' (Parseval second moment).** `sum_{x} N_a(x+C)^2 =
(1/|C^perp|) sum_{u in C^perp} K_a(wt u)^2` (sum over the `|C^perp|` cosets).
*Proof.* Parseval for the transform `N_a = (1/|C^perp|) sum_u K_a(wt u)
chi(-<u,·>)` over `F_p^N/C`. `∎` Both sides are recomputed independently and
gated equal (`F32-2HP`, `F16@R4:N12`, and the signed `S27-1HP`). This is the
variance identity behind the concentration reading of §4.

---

## 3. The head-aware sufficient band `PROVED`

The naive route — bound `|N_a - main/|C^perp|| <= (1/|C^perp|) sum_{u != 0}
|K_a(wt u)|` and ask the main term to dominate — is **vacuous** for unsigned
`p = 2`: the all-ones dual word `1` has `K_a(N) = (-1)^a binom(N,a)`, so a
**single** term of the sum equals the entire main term, forcing the naive
inequality to fail always. The fix is that `1` carries the head **deterministically**.

**Head-word lemma (`p = 2`).** Every codeword of `C` has even weight (the head
coordinate of `Phi(c) = 0` is `sum_t c_t = 0`), so `1 in C^perp`; and the
relevant cosets are exactly those with `<1, x> = a bmod 2`. On such a coset the
`u = 1` term of (I) equals `(-1)^{-a}(-1)^a binom(N,a) = +binom(N,a) = ` main.
Hence the deterministic contribution is `2*main` and the true error omits `1`.
(For signed `p = 3` the head is free, all cosets are relevant, and `H = {0}`.)

**Theorem 2 (sufficient connectivity band).** `Conn_a` holds whenever

> **`mu > sum_{u in C^perp, u notin H} |K_a(wt u)|`,** where
> **unsigned `p = 2`:** `mu = 2*binom(N,a)`, `H = {0, 1}` (`1` = all-ones);
> **signed `p = 3`:** `mu = binom(N,a) * 2^a`, `H = {0}`.

*Proof.* On a relevant coset, (I) gives `N_a * |C^perp| = mu + sum_{u notin H}
chi(-<u,x_0>) K_a(wt u)`, whose second part has modulus `<= sum_{u notin H}
|K_a(wt u)|`. If `mu` exceeds it, `N_a > 0` for **every** relevant coset
simultaneously (the bound is uniform in `x_0`), which is exactly `Conn_a`. `∎`

The band is a **closed-form** inequality in the dual weight enumerator
`A_w^perp = #{u in C^perp : wt u = w}` (with the `w = N` all-ones pulled out):
`sum_{u notin H} |K_a(wt u)| = sum_{w} A_w^perp |K_a(w)| - |K_a(N)|`. The dual
enumerators are gated exactly; e.g. `F32-1HP` has `A^perp = {7:15, 8:15, 15:1}`,
so excluding the weight-`15` head leaves `err = 1050` against `mu = 12870`.

**Soundness (recomputed).** Over 16 configs and every `a`, the verifier confirms
**band-`OK` implies `Conn_a` true** with **zero** false positives (60-plus
nonvacuous cases) — the sufficient condition is sound, as the proof requires.

---

## 4. Band vs. measured: subset everywhere, sharp in the large-kernel regime `MEASURED`

Because Theorem 2 is a *sufficient* condition, its band is a **subset** of #428's
measured full-coverage band — verified at all five threshold configs. In the
**odd-`R` large-kernel unsigned** regime it is in fact **sharp**:

| config | `q` | `R` | `N` | `|C^perp|` | sufficient band | measured band | `[R, N-R]` |
|---|---:|---:|---:|---:|---|---|---|
| `U-F16@R3:N10` | `2^4` | 3 | 10 | 32 | `{3,4,5,6,7}` | `{3,4,5,6,7}` | `[3,7]` **=** |
| `U-F8@R3:N7`   | `2^3` | 3 | 7  | 16 | `{3,4}`       | `{3,4}`       | `[3,4]` **=** |
| `U-F16@R4:N12` | `2^4` | 4 | 12 | 512| `{}` (empty)  | `{5,7}`       | `[5,7]` hole at 6 |
| `S-F27@R3:N10` | `3^3` | 3 | 10 | 2187| `{}` (empty) | `{6,7,8}`     | signed |
| `S-F27@R3:N11` | `3^3` | 3 | 11 | 2187| `{}` (empty) | `{5,..,10}`   | signed |

On the two odd-`R` large-kernel unsigned rows the sufficient band **coincides**
with both the measured band and the clean interval `[R, N-R]`. Where it is empty
the reason is structural and honest: the expected words-per-coset
`M = binom(N,a)(p-1)^a / |C^perp|` is only `O(1)` (small kernel / even `R` /
signed with `dim V_T` near `N`), so **no** character-sum concentration bound can
be non-vacuous — the concentration threshold has not been reached at that `N`.
The signed toys and the even-`R` `F16@R4` are exactly those cases; the band there
is `MEASURED`-only, and a proved closed-form interval is `OPEN` (§7). Crucially,
the band **never claims an `a` outside the measured truth** (tamper T4).

---

## 5. The `F16@R4:N12` `a = 6` interior hole — derived `DERIVED`

#428 §4 recorded a single anomalous interior hole: at `F16@R4:N12` the band is
`{5,7}` with `a = 6` **missing** from `[R+1, N-R-1] = [5,7]`. This packet derives
it. Enumerating all `512` cosets, exactly **two** even (head-parity-`0`, hence
relevant) cosets carry **no** weight-`6` word. For such a coset, identity (I)
evaluates to an **exact cancellation**:

> `main (u = 0) = binom(12,6) = 924`; head term `(u = 1) = +924`; the remaining
> error `sum_{u notin H} chi(-<u,x_0>) K_6(wt u) = -1848`; so
> **`N_6 * |C^perp| = 2*924 + (-1848) = 0`, i.e. `N_6 = 0`.**

The character sum predicts the vacancy exactly: the deterministic `2*main` is
**exactly** annihilated by the Krawtchouk error at that specific coset — a genuine
`p = 2` cancellation, the small-kernel signature (`dim C = 3`, too few codewords
to re-balance the syndrome). A neighbouring covered even coset has `N_6 = 5 > 0`
for contrast. This converts #428's one measured anomaly into a **derived** exact
zero of the MacWilliams transform (verifier: `total = 0`, `Na = 0`, and the
perturbed cancellation `2*main + (err+1) != 0` fails — tamper T3).

---

## 6. Corollary: four #428 occupancies become hypothesis-free `PROVED`

The shipped `a` of four #428 configs lies **inside the proved band of Theorem 2**,
so `Conn_a` is a **theorem** there, and #428's occupancy `= p^{-defect}` (its
Theorem B) holds with **no measured hypothesis**:

| config (#428) | `p` | `N` | `a` | `defect` | `mu` | `err` | in band? | occupancy — now |
|---|---:|---:|---:|---:|---:|---:|:--:|---|
| `F64-firstN@R3` | 2 | 21 | 10 | 1 | `705432` | `17128` | **yes** | `1/2` **PROVED** |
| `F32-1HP@R3`    | 2 | 15 | 7  | 1 | `12870`  | `1050`  | **yes** | `1/2` **PROVED** |
| `F32-2HP@R3`    | 2 | 7  | 3  | 2 | `70`     | `42`    | **yes** | `1/4` **PROVED** |
| `F64-2HP@R3`    | 2 | 15 | 7  | 2 | `12870`  | `1050`  | **yes** | `1/4` **PROVED** |
| `U16o@R4`       | 2 | 15 | 8  | 0 | `12870`  | `23610` | no      | `1` (stays MEASURED) |
| `S27@R4`        | 3 | 14 | 7  | 0 | `439296` | `918918`| no      | `1` (stays MEASURED) |
| `S27-1HP@R3`    | 3 | 8  | 4  | 1 | `1120`   | `14640` | no      | `Conn` FAILS (as #428) |

So **all four of #428's `defect > 0` configs — the non-trivial half-and-quarter
occupancies — are now theorems**: `occupancy = p^{-defect}` there needs no census.
The two `defect = 0` configs (`U16o`, `S27`, occupancy `1`) sit in the small-`M`
regime and **stay `MEASURED`** — an honest split, and a clean one: the
trace-hyperplane structure that *creates* the defect also **shrinks `dim V_T`**,
enlarging `M` and letting the band bite exactly where the interesting occupancies
live. `S27-1HP` is correctly excluded — its `Conn` genuinely fails (#428).

The verifier recomputes each occupancy from the census and gates
`occupancy = p^{-defect}` together with `Conn_a` holding by the band, for the four
hypothesis-free configs.

---

## 7. OPEN — next-measure list `OPEN`

- **A proved closed-form interval.** The band equals `[R, N-R]` at the odd-`R`
  large-kernel unsigned toys, but proving `[a_-, a_+] subseteq` band in closed
  form needs a Krawtchouk magnitude bound `|K_a(w)|` uniform over the dual
  support — the concentration of `A_w^perp` near `(1-1/p)N`, where `|K_a|` is
  small, is measured but not yet bounded. The interval form is `MEASURED`.
- **Signed and defect-`0` bands.** For signed `p = 3` (`H = {0}`, no head boost)
  and the defect-`0` unsigned configs the band is empty at the toys; a config with
  `M` large enough for the signed band to bite (larger `N`, still exhaustively
  enumerable) would extend the hypothesis-free set.
- **`m >= 3` occupancies.** #428 realizes `defect in {0,1,2}`; a `defect = 3`
  config in the proved band would make occupancy `1/8` a theorem.
- **The `L2` route.** Parseval (§2) gives a Chebyshev sufficient band
  `sum_{u != 0} K_a(wt u)^2 < mu^2 / |C^perp|`; head-aware, it may reach further
  than the `L1` band in a middle regime — measured, not yet packaged.

---

## 8. Weave and nonclaims `AUDIT`

- **PR #428 `cap25_v13_entropy_inverse_fp_span_surjection` (direct predecessor).**
  Proved the image-structure theorem *under* `Conn_a`, verified `Conn_a` by
  census, and left the closed-form band `OPEN` (its §4, §8). This packet proves a
  sufficient band, derives #428's `F16` hole, and makes four of its occupancies
  unconditional. Every #428 datum it re-touches (`dim V_T`, `dim D`, `defect`,
  the seven configs, the five threshold bands) is **reproduced**, never
  contradicted; the single new object is the dual code `C^perp` and its Krawtchouk
  transform.
- **PR #422 and the #422 review (DannyExperiments, 2026-07-08).** The
  `prop:vandermonde-kills-low-rank` `R+1` barrier that #422 used for `rank_K` is
  here the **kernel-code minimum distance** governing the connectivity mechanism;
  the review's containment-plus-Cauchy–Schwarz sharpening is the same Parseval
  moment used in §2. Credited with thanks.
- **PRs #420/#421 and #414–#417.** The `excess`/baseline discipline, the `R > w`
  moment-curve reading, and the Vandermonde barrier are inherited unchanged.
- **This packet consumes no upper cell and instantiates no `U(1116048)`
  certificate.**

**Nonclaims.**

- This note does **not** prove or refute `prob:entropy-inverse-q`, and does **not**
  claim the removal list is incomplete as intended — it supplies a sufficient
  condition for the #428 cell's connectivity and leaves the three-option ledger
  resolution to the program.
- **No finite claim of any kind:** nothing here proves anything about
  `prob:row-sharp-q` / `def:q-row-atom`, certifies **no deployed finite safe row**,
  and instantiates **no `U(a_0+1) <= B*` certificate**. The deployed KoalaBear /
  Mersenne-31 rows are outside the mechanism (prime field, `F_p`-span `= K`-span,
  `defect = 0` degenerately; active prefix depth `R-1 < p`, no reducible columns).
  Asymptotic-lane only, `p in {2,3}` scope.
- **Theorem 1 (MacWilliams identity (I))**, **Theorem 1' (Parseval)**, the
  **head-word lemma**, and **Theorem 2 (sufficient band)** are complete
  unconditional arguments (`PROVED`), each with an exact numeric anchor. The
  **hypothesis-free corollary** (§6) is `PROVED` (band membership is proved, and
  the census confirms the resulting occupancy). The `F16` hole (§5) is `DERIVED`
  (an exact evaluation of (I) at a specific coset). The **band's sharpness** and
  its **subset** relation to #428's measured band (§4), and the **which-configs**
  split, are `MEASURED` (exact toy enumeration). The `d(C) >= R+1` min-distance is
  `PROVED` (Vandermonde); which configs attain equality is `MEASURED`. **No proved
  closed-form interval** and **no asymptotic simplification** are claimed beyond
  the exact dual-enumerator inequality.
- `C`, `C^perp`, `H`, the head refinement, and the config grid are conventions;
  the sufficient band, the derived hole, and the four hypothesis-free occupancies
  are robust to any `O(1)` choice, since each is an exact integer identity.
