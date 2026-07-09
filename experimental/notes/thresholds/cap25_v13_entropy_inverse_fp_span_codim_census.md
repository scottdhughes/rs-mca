# CAP25 v13: the twist span-codimension census — quantifying option 1 (the rho-genericity hypothesis) of PR #422 §2.4

Status: `CONVENTION` (§1 — the field/config grid, the four departure
families, round-robin balanced class assignment, deterministic contamination/
Hamming positions, the `excess_generic` baseline inherited from #421/#422
unchanged) / `MEASURED` (§2–§5 — every `dim_Fp V_T` / `codim` number in the
four family tables, the naive-law match/violation counts, the
`fill_j`/`fill_h`/`fill_m`/`fill_d` distributions, the three `excess_generic`
spot-check ties, all verifier-gated exact) / `PROVED-AT-TOYS` (§4 — the
per-subfield Frobenius^`d` law only, exhaustive zero-violation on one
enumerable config, the same epistemic status #422 uses for its own `c`-form
laws; the F2 `j=0` exact-equality is internal tamper machinery (T2), not a
note-level claim) / `AUDIT` (§6 — the N-column structural floor, a bookkeeping
observation, not a new mechanism) / `OPEN` (§7 — the asymptotic
extrapolation; every number in this note is a finite-toy measurement).

**Verifier:** `experimental/scripts/verify_entropy_inverse_fp_span_codim_census.py`
(zero-arg, stdlib-only, self-contained; `RESULT: PASS (862/862 checks)`,
exit 0; ~2 s, ~31 MB peak RSS **on the authoring box**, not gated;
best-effort `RLIMIT_AS` guard, default 2 GB, `FP_CODIM_AS_CAP_GB` tunes/
disables, never fatal on platforms that refuse the cap; `FP_CODIM_DATA_DIR`
overrides the data location). The `GF` finite-field class, `fp_span_dim`,
`moment_columns`, `gamma2`, `generic_cols`, and `decode` are copied verbatim
from PR #422's `verify_entropy_inverse_fp_span_cell.py`, and its
`census`/`gamma2_generic` are adapted (same algorithm, refactored
signatures; repo convention: standalone scripts, no cross-imports); new here
are the four rho families, the class enumerator, and the Frobenius^`d` law
check. Six tamper self-tests — five corruption catches plus one structural
sanity check (T4) — including a faked span-dimension fed through the live
gate, the uncapped-law cap validation, and the per-subfield law's
wrong-degree break.

**What this is / is not.** A **measurement-only** follow-on to PR #422
(`cap25_v13_entropy_inverse_fp_span_cell.md`, fetched read-only from branch
`thresholds-entropy-inverse-fp-span-cell`, **not yet merged into main**).
It answers #422 §6's `OPEN` item verbatim: *"measure `codim_Fp V_T` as a
function of the twist entropy of `rho` — quantify how much genericity a
`rho`-genericity hypothesis (option 1) would need to demand."* **It claims
no theorem.** Every law tested is reported with its exact match/violation
count; a refuted naive law is stated as a measurement, not smoothed over.
**Merge framing: an experimental measurement note, asymptotic lane only, no
finite claims.** It does **not** resolve `prob:entropy-inverse-q`, produce a
row-sharp `Q`, or touch any deployed finite row (§8).

Lineage `#414 -> #416 -> #417 -> #420 -> #421 -> #422 -> ` this packet. #422
found: for a projective weight `rho(T) subset c F_p^x`, `V_T = span_Fp{rho(t)
v_t}` is `F_p`-deficient in the ambient `K^R` while `rank_K` stays full, and
posed three ledger options in its §2.4: (1) a `rho`-genericity hypothesis,
(2) add the cell to the removal list, (3) restate alternative (b) over the
prime field. This packet sizes option 1.

---

## 1. Conventions `CONVENTION`

- **Grid.** Fields `{F27(3,3), F16(2,4), F64(2,6), F49(7,2), F125(5,3)}`
  (smallest-monic-irreducible `GF`; field self-tests gated: `q=p^k`, antilog
  bijective, `g` never in `F_p`, table-multiply matches log/antilog on the
  full `q x q` sweep, all five fields). `R in {3,4,5,6}`, `N in {12..16}`,
  `T=firstN`. To keep the packet small: a **primary point** `(R,N)=(4,16)`
  on every field, plus a full `R`-sweep and `N`-sweep **on F27 only** (12
  `(field,R,N)` points total for F1/F2/F4); F3 restricted to the
  composite-`k` fields `F16`/`F64` (§4) with a full `R`-sweep at `N=16`. No
  slice is enumerated for these grid points — `dim_Fp(V_T)` is the `F_p`-rank
  of the `N` raw weighted columns, independent of any slice weight-count `a`.
- **Four families.** F1 *m-class mixture*: `rho(t)` round-robin balanced
  over `m` distinct projective classes (ascending coset reps of `F_p^x` in
  `K^x`; `m=1..6` always available). F2 *epsilon-contamination*: the `c=1`
  class except the first `j` positions (nested in `j`, seed `777`) hold a
  generic `K^x` value. F3 *subfield-valued*: `rho(t)` generic (seeded) in a
  proper subfield's unit group `F_{p^d}^x < K^x`. F4 *Hamming perturbation*:
  the `c=1` class except the first `h` positions (nested) multiplied by the
  fixed non-`F_p` unit `g`. All four deterministic given their seed.
- **`excess_generic`.** Unchanged from #421/#422:
  `Gamma_2(moment curve) / Gamma_2(generic random K^R map, same shape, seeds
  11,23)`, used only at the three exhaustive spot-checks (§3), gated with
  the `offset_over_N > -0.25` balance guard where applicable.

---

## 2. F1 — m-class mixture: the naive additivity law is `MEASURED FALSE`

Hypothesis: `dim(m) = min(ambient, m*dim_1)`. **Gated result: `31/72`
matches, `41/72` violations — refuted in the majority of swept configs.**
Primary point (`R=4,N=16`), `dim(m)` for `m=1..6`:

| field | ambient | `dim(1..6)` |
|---|---:|---|
| F27 | 12 | `7, 11, 10, 11, 12, 12` |
| F16 | 16 | `9, 12, 14, 13, 13, 14` |
| F64 | 24 | `12, 14, 16, 15, 16, 16` |
| F49 | 8 | `7, 8, 8, 8, 8, 8` |
| F125 | 12 | `9, 11, 11, 11, 11, 11` |

**Non-monotonicity, gated exact — and expected in kind, if not in shape.**
The `m`-class families are **not nested** in `m` (the round-robin assignment
`classes[i % m]` re-partitions every position when `m` changes), so `dim(m)`
has no a priori reason to be monotone; the finding is the measured shape,
not a paradox. And the shape is striking: F27 *dips* at `m=3` (`11->10`, `4`
columns of slack over `N=16`): a **third** class strictly shrinks the span
before recovering at `m=5`. F16/F64 dip `m=3->4` too, but sit at/past the
`ambient<=N` boundary (§6), so are not independent confirmations — F27's
dip alone has clear slack and is not explained by that floor. An
out-of-grid, **not machine-gated** check (`N=40`; a non-round-robin
*blocked* assignment) reproduced the same F27 sequence / qualitative
non-monotonicity, suggesting a genuine class-overlap effect rather than a
round-robin or small-`N` artifact — informal context, not a verified claim.
**F125 never fills within `m<=6`** (stuck at `codim=1` from `m=2` on, `31`
classes available); F49 alone saturates cleanly at `m=2` (full table in the
data JSON's `fill_summary`).

---

## 3. F2 — epsilon-contamination: fill is `MEASURED` gradual, not immediate

**The sharpest question for option 1: does one generic column already fill
the ambient (`j=1`)?** Gated `fill_j` over the 12 grid points (smallest
`j<=5` with `dim==ambient`, `None`=not filled): `{None: 5, j=5: 4, j=1: 1,
j=2: 1, j=3: 1}`. **Only one of twelve points fills at `j=1`, and it is the
field (F49) whose baseline `codim` was already `1`** — the one case with
nothing real left to fill. Primary point, `dim(j)` for `j=0..5`:

| field | ambient | `dim(0..5)` |
|---|---:|---|
| F27 | 12 | `7, 8, 9, 10, 11, 12` |
| F16 | 16 | `9, 10, 11, 12, 13, 13` |
| F64 | 24 | `12, 13, 14, 14, 15, 15` |
| F49 | 8 | `7, 8, 8, 8, 8, 8` |
| F125 | 12 | `9, 10, 11, 12, 12, 12` |

F27/F125 repair almost exactly **one dimension of codim per contaminated
column**; F16/F64 repair at a similar rate with occasional plateaus (not
strict monotone decrease). **Answer: fill is gradual, not a `j=1` cliff.**

**Tying codim to actual collision excess** (exhaustive spot-checks,
`excess_generic` gated):

| config | `j` | `dim`/`codim` | `excess_generic` |
|---|---:|---|---:|
| F27, R=4, N=12, a=7, signed | 0 | 7 / 5 | `25.636` |
| | 1 | 8 / 4 | `9.049` |
| | 2 | 9 / 3 | `3.379` |
| F16, R=3, N=12, a=6, unsigned | 0 | 5 / 7 | `47.231` |
| | 1 | 6 / 6 | `23.725` |

Each contaminated column removes one `codim` dimension *and* roughly
halves-to-thirds the collision excess — codim and excess gated strictly
co-decreasing over `j=0,1,2` (F27).

---

## 4. F3 — subfield-valued rho: exact law, ladder never fills

**Exact law, verified exhaustively (not merely dimension-measured).** For
`rho(t)` generic in `F_{p^d}^x < K^x`, the natural per-subfield
generalization of #422's `c=1` law (`x_t in F_p` and `rho(t) in F_{p^d}` are
both `Frob^d`-fixed, and `Frob^d` is `F_p`-linear in char `p`):

> `s_0 in F_{p^d}`  and  `s_{p^d j} = Frob^d(s_j) = s_j^{p^d}` whenever `p^d j < R`.

Checked exhaustively on **F16, `d=2`, `R=5`, `N=8`, `a=4`, unsigned** (full
`C(8,4)=70` slice): **`0` head violations, `0` Frobenius violations, `70/70`
pairs checked.** Load-bearing: the same census against the *wrong* degree
`d=1` breaks the head-containment law on `40/70` fibers.

**The dim ladder never fills within the tested range**, `fill_d=None` at
all 8 `(field,R)` points, `R` swept `3..6` at `N=16`:

| field | `R` | ambient | `dim` by `d` |
|---|---:|---:|---|
| F16 | 3 | 12 | `d1:5, d2:10` |
| F16 | 4 | 16 | `d1:9, d2:13` |
| F16 | 5 | 20 | `d1:9, d2:13` |
| F16 | 6 | 24 | `d1:11, d2:15` |
| F64 | 3 | 18 | `d1:6, d2:11, d3:14` |
| F64 | 4 | 24 | `d1:12, d2:16, d3:16` |
| F64 | 5 | 30 | `d1:12, d2:16, d3:16` |
| F64 | 6 | 36 | `d1:12, d2:16, d3:16` |

Ladder gated non-decreasing in `d` everywhere. F64's `d2->d3` plateau at
`R>=4` coincides with `dim` hitting `16=N` — the §6 structural floor, not a
new saturation; F64's `R=3` row (clear of that floor) shows genuine `d3`
gain (`7->4` codim). **Even `d=3` on F64 — half the extension degree, the
largest proper subfield available — leaves `codim=4` uncleared at `R=3`.**

---

## 5. F4 — Hamming perturbation: the multiplicative side confirms F2

Same question, multiplicatively: `h` columns multiplied by a fixed non-`F_p`
unit instead of a generic replacement. Gated `fill_h` over 12 points:
`{None: 11, h=1: 1}` — again the lone fill is F49's already-`codim`-`1`
point. Primary point, `dim(h)` for `h=0..3`:

| field | ambient | `dim(0..3)` |
|---|---:|---|
| F27 | 12 | `7, 8, 9, 10` |
| F16 | 16 | `9, 10, 11, 12` |
| F64 | 24 | `12, 13, 14, 14` |
| F49 | 8 | `7, 8, 8, 8` |
| F125 | 12 | `9, 10, 10, 10` |

Same roughly-one-dimension-per-column rate as F2, confirming the gradual-fill
answer via an independent (multiplicative, not replace) mechanism. Excess
tie (F1 family reused, F49 R=2 N=10 a=4 signed): `m=1`: `dim=3, codim=1,
excess_generic=15.116`; `m=2`: `dim=4, codim=0, excess_generic=2.576`.
**Caveat, `MEASURED`, not overclaimed:** `codim=0` here does **not** bring
`excess_generic` down to the `~1` generic baseline (#421/#422's own null was
`<=1.08`) — a spanning-but-low-entropy weight still carries `2.6x` residual
excess. `F_p`-span codim `0` is **necessary but not sufficient** for fully
generic collision statistics; correlated with excess (§3) but not
interchangeable with it.

---

## 6. The N-column structural floor, and verification `AUDIT`

Bookkeeping, not a new mechanism: `dim_Fp(V_T) <= min(N_real, ambient)`
always (a rank-of-`N_real`-vectors bound). One disclosure first: `T = firstN`
can only draw on the `q-1` nonzero field elements, so F16's `N16`-tagged
rows actually run on `N_real = 15` columns (the JSON's `N` field records the
request; the floor arithmetic here uses `N_real`). With that,
`ambient = R*k > N_real` forces `codim >= ambient - N_real` **regardless of
genericity**: it binds F64's primary point (`ambient=24>16`, floor `8`),
F27's `R=6` point (`ambient=18>16`, floor `2`), and **every F16 `R=4` row**
(`ambient=16 > N_real=15`, floor `1` — any F16 generic-twist codim there is
structurally forced, the same mechanism as F64's floor, not an accidental
rank deficiency); F27's `N=12` point sits exactly at the boundary (floor
`0`, no slack). The verifier's full-twist tamper control (T3 below)
therefore runs at `N=21,R=2` (comfortable slack everywhere: `ambient = 2k
<= 12` while `N_real >= 15` across the five fields). Rows in
the data JSON carry `ambient` and `N` alongside `codim` for this cross-check.

`862/862` checks, ~2 s, ~31 MB RSS. Recomputes every `dim_Fp`/`codim`/
`excess_generic` number from scratch and gates against the committed JSON
(exact ints, `1e-9` floats). Six tamper self-tests — five corruption
catches plus one structural sanity check (T4): (T1) a **faked
span-dimension fed through the live `geq` gate** with a freshly recomputed
`dim` against a corrupted expectation (must append a FAIL, which is then
retracted — exercises the actual gating pipeline, not an arithmetic
tautology); (T2) the **F2 `j=0`
control** is exact list-equal to the pure single-class weight (not just
dimension-equal), `j=1` must differ; (T3) a **full-twist control** gives
`codim=0` at `N=21,R=2` (see above for why the grid's own primary points are
unsuitable); (T4, structural sanity check) the **uncapped m-class law**
(`m*dim_1`, no `min(ambient,.)` cap) fails to match measured `dim` at every
instance it overshoots the ambient — a structural certainty
(`dim<=ambient<m*dim_1` there) validating the cap's presence, not a
corruption catch; (T5) the **F3 law wrong-degree break** (`d=1`
instead of `d=2` breaks head-containment on `40/70` fibers); (T6)
**codim/excess co-monotonicity** at spot-check A (both strictly decrease
`j=0->1->2`, ratio drop `>2x`).

---

## 7. Synthesis and OPEN `MEASURED` / `OPEN`

**Measured codim-vs-departure laws** (toy-exact; no asymptotic claim):

- **m-class mixture:** the naive `min(ambient,m*dim_1)` law is false in
  `41/72` configs; non-monotone in `m` for at least one field with clear
  slack (F27); three of five fields do not reach full rank by `m<=6` at all.
- **epsilon-contamination / Hamming:** fill is **gradual**, roughly one
  `codim` dimension per contaminated/perturbed column; a single column
  fills the ambient in only `1/12` configs, and that sole case had almost
  nothing left to fill.
- **subfield ladder:** codim non-increasing in `d` but never reaches `0`
  within any tested proper subfield, including the largest available
  (F64 `d=3`, half the extension degree).
- **codim `0` is necessary but not sufficient** for generic-looking
  collision statistics (§5): a spanning-but-low-entropy weight can still
  carry several-fold excess over the `~1` generic baseline.

**One-sentence answer to the option-1 sizing question** (`MEASURED` at
toys; asymptotic extrapolation `OPEN`): a `rho`-genericity hypothesis needs
to exclude not merely the projective classes themselves but a substantial
measured neighborhood around each one — small unions of up to `6` classes,
weights differing from a class in a handful of coordinates (`j<=5`/`h<=3`
tested), and weights valued in any proper subfield up to half the extension
degree — none of which reliably restores full `F_p`-rank on this grid, so
the exclusion option 1 needs is comparable in reach to the deficiency
itself, not a thin measure-zero correction.

**OPEN — next measures.** (1) Push the `m`-class/`d`-ladder sweeps past
`N=16`/the structural floor, machine-gated, to separate genuine
non-monotonicity from boundary noise on F16/F64. (2) Extend F2/F4's `j`/`h`
range past `5`/`3` to find the actual fill point at the `7` points that
didn't fill here. (3) An asymptotic (`N,R -> infinity` jointly) reading of
the same four families, to turn this toy census into an actual bound on how
large option 1's exclusion set would need to be.

---

## 8. Weave and nonclaims `AUDIT`

- **PR #422 `cap25_v13_entropy_inverse_fp_span_cell.md`** (direct
  predecessor, not yet merged into main; fetched read-only from branch
  `thresholds-entropy-inverse-fp-span-cell`). Identified the `F_p`-span cell
  and posed the three-option ledger question in §2.4; this packet answers
  its §6 `OPEN` item ("twist span-codimension census") directly, and reuses
  its `excess_generic` baseline, its `GF`/`fp_span_dim`/`moment_columns`
  machinery (copied verbatim, cited in the script header), and its
  `offset_over_N > -0.25` balance guard unchanged.
- **The #422 review** (DannyExperiments, 2026-07-08). Credited there for the
  option-1/2/3 framing this packet sizes; this packet does not choose among
  the options, only measures how large option 1's exclusion would need to be.
- **PR #421 `cap25_v13_entropy_inverse_missing_cell_hunt` / PR #420
  `cap25_v13_entropy_inverse_toy_dichotomy`.** Upstream of #422; unaffected
  and not re-touched here.
- **This packet consumes no upper cell and instantiates no `U(1116048)`
  certificate.**

**Nonclaims.**

- Does **not** prove or refute `prob:entropy-inverse-q`, does **not** choose
  among #422's three ledger options, and does **not** claim the "measured
  neighborhood" of §7 is a complete or tight description of option 1's
  requirements — it is a lower-bound-flavored census (these departures don't
  fill), not an upper bound on what *would* suffice.
- **No finite claim of any kind:** nothing here touches `prob:row-sharp-q` /
  `def:q-row-atom`, certifies no deployed finite safe row, and instantiates
  no `U(a_0+1) <= B*` certificate at any deployed row. Asymptotic-lane only,
  exactly as #422 is.
- Every table in §2–§5 is a **toy measurement** (`N<=16`, `R<=6`) gated
  exactly by the verifier; no law is claimed beyond the swept grid, and a
  naive law that failed (§2) is reported as a finding, not smoothed over.
- The one out-of-grid check in §2 (`N=40`, blocked assignment) is
  explicitly **not machine-gated** — context only.
