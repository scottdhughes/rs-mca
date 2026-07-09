# L1: the `ell = 23` `k3` late record STABILIZES; candidate growth-law route-cuts

**Type: EXACT-COMPUTATION (exhaustive-up-to-rotation-gauge `max k3`, no sampling; coverage
stated) + METHOD/MEASURED (the record-process / search-depth confound; two named growth-law
candidates refuted, one class left OPEN) + REFINEMENT (of the integrated k3 packet; supersedes
one stale citation in the integrated `m19`-pin note). Non-superseding of any proof. Modifies NO
integrated file.**

**Result (one line).** The integrated packet
`experimental/notes/l1/l1_k3_growth_refutation.md` (integrated `e83962ae`, was PR #410) flagged
its own `ell = 23` `k3 = 7` record (`p = 1657`, `n = 72`) as a **late record at the largest
tested prime** — explicitly OPEN-ended (§3A: *"**the right object is `sup` over `p`, and it
remains OPEN at every `ell`**"*). Extending that `ell`'s exhaustive-up-to-gauge scan **`21 -> 29` primes**
(`p` to `4463`) closes the open end: the **`15` exhaustive primes after the record** (`n = 84..194`)
**all give `k3 <= 5`**, so the record is **STABILIZED-in-range** — a converged `sup` lower bound,
not a first-hit. Along the way `ell = 29` deepens `12 -> 21` primes (`k3 = 7` recurs a **4th** time,
`n = 138`) and a new `ell = 31` grid is measured; a **record-process / search-depth confound** is
made explicit (the apparent `ell = 37..73` plateau near `k3 = 9` is UNMEASURED, not deceleration);
and two named candidate growth laws are **route-cut dead** with a third left OPEN. Every new `k3`
is cross-verified through the integrated verifier's own `gauge_max_k3` (dual code path): **31/31
rows MATCH**. The integrated scan JSON is **untouched**; the new rows ship in a separate file.

**Companion data + verifier (both new; integrated files unmodified).**
`experimental/data/certificates/l1-e3-law/l1_k3_growth_r3_extension.json` (31 rows + analysis
blocks); `experimental/scripts/verify_l1_k3_record_stabilization.py` (zero-arg, stdlib, `< ~90s`;
imports the integrated `gauge_max_k3` as an independent engine; opt-in `--full` cross-checks all
`24` new rows live, `~10 min`). Each data row also carries a non-canonical `tri` field — a winning
drop-exponent orbit representative, in the same generator convention as the integrated rows;
alternate maximizers exist, and `tri` is NOT independently gated — the sole load-bearing, gated
quantity per row is `k3`.

**Notation** (inherited verbatim from the integrated notes). `ell` odd prime, `ell | p-1`,
`n = (p-1)/ell` cosets of `H = mu_ell`; `k3` = number of tail cosets whose max fiber is `>= 3` in
the fat-tail `[ell-3, 3^{k3}]` family; **exhaustive-up-to-gauge `max k3`** = the exact maximum over
all `C(ell,3)/ell` rotation-orbit drop reps and all `q` (`P^2`-concurrency), NO early exit — the
integrated packet's own object and method. The Lemma-R ceiling is `floor((2ell-5)/3)`; the
cyclotomic-pair cap is `2(ell-1)/3` (both PROVED in the integrated packet). All arithmetic exact
over `F_p`, stdlib only.

**Status legend.** EXACT-COMPUTATION (exhaustive, coverage stated) / METHOD/MEASURED (exact data,
methodological reading, no theorem claimed) / REFINEMENT (updates a citation in an integrated
note; the cited note's own theorems are untouched).

---

## 1. [EXACT-COMPUTATION] The `ell = 23` late record STABILIZES

The integrated note names the tension precisely. §2: the `ell = 23` row is *"a **new `ell = 23`
record** (`5 -> 7`), set at the LARGEST prime R2 tested for that `ell` — a *late* record"*.
§3A: *"`ell = 23`'s record arrives at its LARGEST tested prime (`p = 1657` ...) and drops back to
`5` at the very next prime"*, and, as the standing caution, *"**the right object is `sup` over
`p`, and it remains OPEN at every `ell`**"* / *"**late records are possible at any `ell`**"*. The
record was therefore a certified lower bound whose open end was, by the note's own hygiene,
unresolved.

**Resolution (exact).** Extending the exhaustive-up-to-gauge scan for `ell = 23` from the
integrated `21` primes to **`29`** (all eligible primes `p = 23n+1` through `p = 4463`, `n = 194`):

```
 n :  ... 62  72   84  86 102 104 110 132 134 140 144 146 162 170 174 176 194
 p :  ... 1427 1657 1933 ...                                              4463
 k3:  ... 5    7    5   5   5   5   5   4   5   5   5   4   5   5   5   5   5
```

The record sits at `n = 72` (`p = 1657`, `k3 = 7`). The **`15` exhaustive primes after it**
(`n = 84..194`, `p` up to `4463`) **all give `k3 <= 5`** (the `7` of the integrated `n = 84..134`
window's own tail is re-confirmed here, and `8` new primes `n = 140..194` extend it). So `ell = 23`
is downgraded from OPEN-ended to **STABILIZED-in-range**: its table value `7` is now a *converged*
`sup` lower bound over the tested range, not a first-hit at the frontier. This directly answers
the open end the integrated note flagged for this `ell`. (It remains, as any per-prime scan is,
finite — the `sup` over *all* `p` is still formally OPEN; what changes is that the specific
"record at the largest tested prime" caution no longer applies to `ell = 23`.)

## 2. [EXACT-COMPUTATION] `ell = 29` deepened; a new `ell = 31` grid

- **`ell = 29`: `12 -> 21` primes** (`p` to `4583`). `max k3 = 7` holds; `k3 = 7` now recurs a
  **4th** time, at `n = 138` (`p = 4003`) — joining `n = 8, 44, 68` — with no new record. The
  `k3 = 7`-at-`n=8` peak-then-recur pattern the integrated note describes is confirmed deeper.
- **`ell = 31`: a new grid** (`ell = 31` is absent from the integrated scan JSON — it was
  gate-3/build-time only there). Seven exhaustive primes `n = 22..60` give `k3 = [7,5,6,6,7,7,6]`;
  with the integrated build-time `n = 10, 12` (both `7`) this is `9` distinct primes, `max k3 = 7`,
  `k3 = 7` recurring at `n = 22, 48, 52`. No new record.

## 3. [METHOD/MEASURED] Record-process / search-depth confound

"Record stabilized" and "search went deep" are almost perfectly **confounded** across the
integrated table, and saying so is a measured, not interpretive, observation:

- Every `ell` tested at only **`1`–`3`** exhaustive primes — `37, 41, 47, 59, 61, 67, 71, 73` —
  has its record **at its last tested point**. That is open-ended *by construction*: the scan
  stopped exactly where it last found something new.
- Only the deeply-searched `ell in {17,19,23,29,43,53}` (`44, 80, 29, 21, 9, 6` primes — the last
  two of which are *this* packet's contribution) have gone deep enough for a record to *stabilize
  before* the deepest point tested.

Consequence: the apparent `ell = 37..73` **plateau near `k3 = 9` is UNMEASURED — not evidence of
deceleration**; each of those values is a first-or-second-try lower bound on `sup_p k3`. This
sharpens the integrated §3A `sup`-over-`p` / spike-process framing, and it cuts any growth-law fit
across the full `ell = 11..73` range (most of the high-`ell` table is unconverged data).

## 4. [METHOD/MEASURED] Candidate growth-law route-cuts (exact)

Working from the integrated exhaustive-gauge table (`max k3 = 4,4,7,6,7,7,7,7,7,8,7,11,9` at
`ell = 11..59`, then `9` at `61/67/71/73`; the integrated note marks its `ell = 67` entry `>= 9` —
a witness-realized lower bound under thin coverage, per its own row text — folded here as `9`,
which does not affect the A/B/C verdicts: `ell = 67` sits mid-plateau with `61/71/73` all exactly
`9`; ceiling `= floor((2ell-5)/3)`): two named closed-form candidates are **refuted** and one
class stays **OPEN** — each with its falsifier data.

- **(A) `max k3` = a constant fraction of the Lemma-R ceiling — DEAD.** The ratio
  `max k3 / floor((2ell-5)/3)` **falls `4.18x`**, from `4/5 = 0.800` (`ell = 11`) to
  `9/47 = 0.191` (`ell = 73`). It is refuted on the **well-searched points alone**
  (`ell = 11,17,19,23,29`: `0.80, 0.78, 0.55, 0.54, 0.41` — a clean monotone-ish fall, no
  under-searched tail required).
- **(B) bounded additive gap `ceiling - max k3` — DEAD** (an additive restatement of the integrated
  packet's already-refuted `O(1)` cap). The gap **grows `1 -> 38`** (`ell = 11 -> 73`), roughly
  linear in `ell`. The softer `gap ~ c*sqrt(ell)` is dead too: `gap/sqrt(ell)` climbs
  `0.30 -> 4.45` (max at `ell = 73`; the `ell = 71` value is `4.27`) — a `~15x` rise, not flat.
- **(C) sub-linear `Theta(ell^alpha)` (`0 < alpha < 1`, plausibly `1/2`) vs `Theta(log ell)` —
  OPEN.** Indistinguishable on `ell <= 73`: normalized `k3/sqrt(ell)` and `k3/log ell` spread only
  `1.66x` / `1.78x` (versus the raw `k3/ell` spread `3.34x`), both far flatter than the
  ceiling-ratio — consistent with sub-linear growth but unable to separate `sqrt`-like from
  `log`-like. The two curves diverge by `2x`+ only near `ell ~ 150`–`300`, and pinning it needs
  real depth there (dozens of primes, not `1`–`3`) — beyond this grid. (Heuristic float
  normalization; NO growth *order* is claimed.)

## 5. [REFINEMENT] Supersedes the stale `ell = 23` `k3` citation in the `m19`-pin note

`experimental/notes/l1/l1_m19_pin_excess3_atlas.md` (integrated `e83962ae`, was PR #399) still
carries the **pre-R2** `ell = 23` value in three places: the "empirical max `k3`" column of its §5
`k3`-cap table reads `5` for `ell = 23`; its §5 CORRECTED-2026-07-07 growth sequence prints the
`ell = 23` entry as `5` (`4,4,7,6,5,7,7,7,7,8,7,11,9` at `ell = 11..59`, 5th entry); and,
separately, its §6 "Extended null evidence" prose reads *"`<= 6` for `ell in {19,23}`"* (verbatim
§6, describing its older ~12-prime window). The
current exhaustive-gauge picture is **`max k3 = 7`** for `ell = 23` (the late `p = 1657` record,
now STABILIZED per §1). This packet **supersedes that stale `ell = 23` value**: read
`ell = 23 -> 7` in all three places. Everything else in that note is **UNAFFECTED** — in particular the hypothesis `H_19`, the
Spine Theorem, and the conditional theorem `H_19 => m*(19) = 9` do not touch the `ell = 23` value
(the `ell = 23 -> 7` entry still obeys both PROVED caps `7 <= 13` and `7 <= 14`, so the caps'
integers and the pin's structure are untouched).

## 6. Verifier contract

`experimental/scripts/verify_l1_k3_record_stabilization.py` — zero-arg, stdlib, deterministic,
exit `0` iff all pass, `< ~90s`. Gates: **(1)** DUAL CODE PATH — imports the integrated
`gauge_max_k3` and live-cross-checks a fast spot set (`ell = 31`, `n = 36` and the `n = 48`
`k3 = 7` recurrence), and asserts every stored `k3` obeys BOTH PROVED caps; **(2)** the integrated
scan JSON is **UNTOUCHED** (`180` rows, `by_ell[23] = 21` ending `n = 134`, no `ell = 31`, the
`(23,72) -> 7` record and the `ell = 19` deep null intact); **(3)** the `7` "reconfirms-integrated"
rows match the integrated `k3`; **(4)** the STABILIZATION (`ell = 23` combined `29` primes, `15`
past `n = 72` all `k3 <= 5`) and `ell = 29`/`31` deepening — with row eligibility
(`p = ell*n + 1`, prime), the depth ties (`ell = 23` to `p = 4463`, `ell = 29` to `p = 4583`), the
exact `ell = 31` prime grid, and the build-time `n = 10, 12` rows gated against the integrated
verifier's own `FULL_TABLE` constants (the integrated scan JSON has no `ell = 31` rows); **(5)**
the §4 base table first re-sourced entry-by-entry from the integrated artifacts (scan JSON + the
integrated verifier's `FULL_TABLE` / witness constants; `ell = 67` asserted witness-folded
`>= 9 -> 9`), then the route-cut numbers recomputed EXACTLY (ratios/gaps via `Fraction`; spreads
via float); **(6)** the
§3 confound partition, cross-checked against the integrated JSON's thin coverage; **(7)** `>= 4`
tamper self-tests (cap-violating `k3`, a synthetic `204`-row copy of the integrated JSON fed to
the same untouched-checker gate 2 runs, a broken stabilization row, a flattened base table) — each
REJECTED. Opt-in `--full` live-cross-checks all `24` new rows
through `gauge_max_k3` (`~10 min`; already run offline: `31/31` MATCH, `0` mismatch; lane spot
points `(23,4463)/(29,2437)/(29,3307)` reproduced).

## 7. Concurrent-work weave (relationship labels; no dependency taken)

- **`l1_k3_growth_refutation.md` (integrated `e83962ae`, was PR #410).** **Refined, not modified:**
  its `ell = 23` §2/§3A open-endedness caution is RESOLVED (§1); its `ell = 29` recurrence deepened
  and a new `ell = 31` grid added (§2); its `sup`-over-`p` framing sharpened into the measured
  confound (§3); its "the `k3` growth law is OPEN" note given explicit route-cuts (§4). Its scan
  JSON, note, and verifier are byte-for-byte untouched; the new rows live in a separate file.
- **`l1_m19_pin_excess3_atlas.md` (integrated `e83962ae`, was PR #399).** **Superseded-in-part:**
  its §5/§6 pre-R2 `ell = 23` `k3 = 5` citation is updated to `7` (§5 here); `H_19` / Spine /
  conditional theorem UNAFFECTED.

## Refs

- `experimental/notes/l1/l1_k3_growth_refutation.md` (integrated, was PR #410 — the refined
  packet; `k3` object, method, PROVED caps, §3A caution quoted here).
- `experimental/data/certificates/l1-e3-law/l1_k3_growth_r2_scan.json` (integrated, was PR #410 —
  `180` rows; NOT modified; its `gauge_max_k3` engine, via the verifier, is this packet's
  cross-check).
- `experimental/scripts/verify_l1_k3_growth_refutation.py` (integrated, was PR #410 — its
  `gauge_max_k3` is imported as the independent dual-code-path engine).
- `experimental/notes/l1/l1_m19_pin_excess3_atlas.md` (integrated, was PR #399 — the stale
  `ell = 23` `k3 = 5` citation superseded, §5 here; pin/spine untouched).
- `experimental/data/certificates/l1-e3-law/l1_k3_growth_r3_extension.json` (this packet — `31`
  rows + stabilization / confound / route-cut analysis blocks; consumed by every gate).
