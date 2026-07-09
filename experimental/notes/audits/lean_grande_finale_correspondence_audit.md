# Grande Finale Lean ↔ `grande_finale.tex` correspondence audit — 93 FAITHFUL / 13 DRIFT / 1 STRONGER, 0 `sorry`

Status: `AUDIT` (textual Lean↔tex correspondence over 112 declarations at
`b99b2c4`) / `VERIFIED-CLEAN` (§2 — `GrandeFinale.lean` + `BC.lean` +
`Frontier.lean`, 78 declarations, zero discrepancies) / `DRIFT-FOUND` (§3 —
`QEntropyInverse.lean` + `QFourierTao.lean` cite labels and a manuscript file
that exist nowhere in the repo; the underlying math is real and retargeted
below) / `WEAKER-THAN-STATED` (§4 — `SP.lean`'s `sp_from_q` / `sp_from_q_normalized`
state a bound provably weaker than their own proof establishes; fix
recommended, not applied).

**Motivation.** The maintainer's `2026-07-08` agents-log entry for
`b99b2c4` ("Grande Finale Lean package normalization") names this as the next
step, verbatim:

> Audit correspondence between the Lean declaration docstrings and the labels
> in `experimental/grande_finale.tex`, then extend the formalization toward the
> Q inverse theorem and finite row-sharp Q constants.

This note discharges the audit half. The extension half is scoped in §7.

## 0. Scope `AUDIT`

- **Textual only.** `lake build` was **not** run. The package requires a
  Mathlib-pinned toolchain that is unavailable here, and the package's own
  `README.md` / `FORMALIZATION_SUMMARY.md` forbid casual builds. Every verdict
  is from reading `.lean` and `.tex` side by side. No proof was kernel-checked.
- **`native_decide` constants** were cross-checked by hand against the tex's
  printed decimals (all 12 match, §6). They were **not** re-executed.
- Per-claim status labels throughout: **F** FAITHFUL, **D** DRIFT (label or
  provenance wrong, content sound), **S** STRONGER-THAN-TEX (documented),
  **W** WEAKER-THAN-TEX, **N** NO-TEX-COUNTERPART (honest, no label claimed).
- Verifier: `experimental/scripts/verify_lean_correspondence_audit.py`
  (zero-arg, stdlib-only, `RESULT: PASS`).

## 1. Headline `AUDIT`

| file | decls | verdict |
|---|---|---|
| `GrandeFinale.lean` | 39 | all F — `VERIFIED-CLEAN` |
| `GrandeFinale/BC.lean` | 25 | all F — `VERIFIED-CLEAN` (`conj:BC` in file header only) |
| `GrandeFinale/Frontier.lean` | 14 | all F — `VERIFIED-CLEAN` (phantom sibling file in header only) |
| `GrandeFinale/SP.lean` | 19 | 16 F, 1 S (`prefix_rigidity`), 2 D+W (`sp_from_q`, `sp_from_q_normalized`) |
| `GrandeFinale/QEntropyInverse.lean` | 5 | all D — `DRIFT-FOUND`, systemic |
| `GrandeFinale/QFourierTao.lean` | 5 | all D — `DRIFT-FOUND`, systemic |
| `GrandeFinale/QPrimitiveCollision.lean` | 5 | 5 N — honest; file header phantom |
| **total** | **112** | **93 F, 13 D, 1 S, 5 N** |

Declaration count rule: lines matching `^theorem` / `^lemma` / `^def` /
`^noncomputable def`. `Main.lean` has 0 such declarations. 12 declarations use
`native_decide`; 0 use `sorry`, `admit`, or a custom `axiom` (§5).

## 2. `VERIFIED-CLEAN` trio — 78 declarations, zero discrepancies

`GrandeFinale.lean`, `BC.lean`, and `Frontier.lean` each cite only real,
existing `grande_finale.tex` labels, and each declaration's content matches the
cited label. Full rows in §8 (tables 1, 2, 4). Two header-level footnotes, both
harmless:

- `Frontier.lean`'s file header names a source `grande_finale_bc_attempt.tex`
  that **does not exist** in the repo. Every individual `Frontier.lean`
  declaration still cites real labels inside `grande_finale.tex`. Citation
  hygiene, not content — the note flags it so the verifier can pin it.
- `BC.lean`'s module header (L9) cites `` `conj:BC` `` (phantom). Every one of
  the 25 `BC.lean` declarations cites a real `thm:*` / `prop:*` / `cor:*` /
  `def:*` label. Header-only drift.

## 3. `DRIFT-FOUND` (systemic) — `QEntropyInverse.lean` + `QFourierTao.lean`

Every declaration in these two files cites either the nonexistent label
`` `conj:Q` `` / `` `lem:log-moment-to-q` `` / `` `cor:asymp-q-fourier-tao` `` /
`` `thm:primitive-log-collision` `` or an unlabeled "§1"/"§4" of a manuscript
`q_fourier_tao_finish_patch.tex` that **does not exist** in the repo. The tex's
own §5 title is "Proper Theorems for the **Former** Q/BC/SP Cells": Q/BC/SP were
conjectures under those labels before a restructuring, and the docstrings were
never updated. The mathematics is sound and traceable. Retarget map:

### 3a. Phantom label / file → real `grande_finale.tex` target

| phantom cited (nowhere in tex) | cited in | real tex label / anchor | tex line |
|---|---|---|---|
| `conj:Q` | `QEntropyInverse.lean`, `QFourierTao.lean`, `SP.lean` | `thm:moment-q` + `thm:logmoment-equivalence` + open `prob:entropy-inverse-q` | 725 / 773 |
| `conj:SP` | `SP.lean` (×4) | `thm:q-implies-sp`, `thm:sp-proper` | 1889 |
| `conj:BC` | `BC.lean` (header) | `thm:bc-proper`, `thm:q-proper` | — |
| `thm:asymptotic` | `SP.lean` | `thm:asymptotic-rs-mca-closure-combined` | 2297 |
| `lem:log-moment-to-q` | `QFourierTao.lean` (×4) | `prop:moment-sandwich`, `thm:moment-q` | 709 / 725 |
| `cor:asymp-q-fourier-tao` | `QFourierTao.lean` (×2) | `thm:moment-q` exponentiated, `R_Q` constant (Conclusion) | 725 / 2339 |
| `thm:primitive-log-collision` | `QFourierTao.lean` (×4), `QPrimitiveCollision.lean` | `def:primitive-logmoment`, `thm:logmoment-equivalence` | 756 / 773 |
| file `q_fourier_tao_finish_patch.tex` | `QFourierTao.lean`, `QPrimitiveCollision.lean` (headers) | folded into `grande_finale.tex` §5 | — |
| file `grande_finale_bc_attempt.tex` | `Frontier.lean` (header) | content lives in `grande_finale.tex` BC section | — |

`thm:asymptotic` warrants care: the string `thm:asymptotic` occurs in the tex,
but **only** as a prefix of `thm:asymptotic-rs-mca-closure-combined`. As a
complete label token it is absent. The verifier uses a boundary-aware match so
a phantom prefix is not miscounted as present.

### 3b. Per-declaration content trace (real math, wrong citation)

| decl | file | real tex content | tex line |
|---|---|---|---|
| `collision_moment_le_of_max` | `QEntropyInverse.lean` | converse of `thm:logmoment-equivalence` + `def:primitive-logmoment` | 773 / 756 |
| `halfMoment_linearIndependent`, `halfMoment_subset_rank` | `QEntropyInverse.lean` | `prop:vandermonde-kills-low-rank` | 876 |
| `log_moment_to_max` | `QFourierTao.lean` | `prop:moment-sandwich` mechanism | 709 |
| `collisionMoment` (def) | `QFourierTao.lean` | `def:primitive-logmoment`'s `Γ_r^prim` | 756 |
| `log_moment_to_max_gamma` | `QFourierTao.lean` | `thm:moment-q` + forward `thm:logmoment-equivalence` | 725 / 773 |
| `q_flatness_from_collision` | `QFourierTao.lean` | `thm:moment-q` exponentiated + `R_Q` constant | 725 / 2339 |
| `q_flatness_bit_certificate` | `QFourierTao.lean` | inequality shared by `thm:moment-q` / `prop:q-moment-order-floor` / `prob:row-sharp-q` | 725 / 2093 / 2177 |

`QPrimitiveCollision.lean`'s five declarations are `DRIFT-FOUND` at the **file
header only** (it too names `q_fourier_tao_finish_patch.tex` and
`thm:primitive-log-collision`). Each of the five declarations is honestly
`NO-TEX-COUNTERPART` (§8 table 7): none re-asserts a specific nonexistent label
at the theorem level; they describe themselves against the informal six-step
`rem:entropy-inverse-skeleton` sketch or against `SP.prefix_rigidity`.

## 4. `WEAKER-THAN-STATED` — `SP.lean` `sp_from_q` / `sp_from_q_normalized`

This is the one non-cosmetic finding. Both theorems state a conclusion
**strictly weaker** than what their own proof establishes.

- Stated (L249): `∑ z ∈ s, f z * (f z - 1) ≤ RQ * (Nsub ^ 2 / Bw)`.
- The proof's internal `key` step (L254) derives the sharp identity
  `Nsub * (RQ * Nsub / Bw - 1) = RQ * (Nsub ^ 2 / Bw) - Nsub`, then the final
  `linarith` (L255) **discards** the `- Nsub` term.
- The tex's `thm:q-implies-sp` (L1889, "Q discharges the shift-pair ledger")
  keeps the sharp form: `Σ_e P_e ≤ (κ - 1/F̄) · C(n,m) · F̄`. The Lean statement
  drops exactly the `- 1/F̄` (i.e. `- Nsub`) correction that its proof already has.
- The header cites `` `conj:Q` ``, `` `conj:SP` ``, `` `thm:asymptotic` `` —
  all phantom. The real label `thm:q-implies-sp` is cited **nowhere** in `SP.lean`.

**Recommended fix (RECOMMENDED, NOT APPLIED here).** Tighten the stated
conclusion to the sharp form the proof already produces, and retarget the
citation:

```
    ∑ z ∈ s, f z * (f z - 1) ≤ RQ * (Nsub ^ 2 / Bw) - Nsub
```

with the docstring citing `thm:q-implies-sp` (tex L1889) in place of the three
phantom labels; propagate the same `- Nsub` tightening through
`sp_from_q_normalized`. Not applied in this packet: a statement change forces
kernel re-elaboration, and no Mathlib-pinned build environment is available
(the package `README.md` forbids casual builds). The numeric gap is negligible
at the deployed rows (`Nsub ≪ Nsub² / Bw` per `prop:proper-q-gap`), but it is a
real mismatch against the literal printed statement. `pair_census_le_of_max_fiber`
shares the same phantom section header (`D`), but its content is faithful.

`SP.lean`'s top-of-file module docstring never mentions the Q⟹SP section at
all, though that section is ~70 lines of the file — an independent
documentation-drift symptom consistent with the section being bolted on after
the header was last edited.

`prefix_rigidity` (`S`, STRONGER-THAN-TEX) is a separate, honest item: the tex
states rigidity for two `m`-subsets; the Lean docstring explicitly notes the
`M'.card = m` hypothesis "turns out to be unnecessary for the conclusion and is
omitted." A flagged generalization, not drift.

## 5. `sorry` / `admit` / `axiom` inventory `VERIFIED-CLEAN`

```
grep -rnE '\bsorry\b|\badmit\b|\baxiom\b' experimental/lean/grande_finale --include=*.lean
```

**Zero matches** across all 8 files (`GrandeFinale.lean`, `Main.lean`, and the
six `GrandeFinale/*.lean` modules). No `sorry`, no bare `admit`, no custom
`axiom`. 12 declarations use `native_decide` (a trusted computational-reflection
tactic, distinct from `sorry`, but a different trust boundary than pure term
reduction). The 12 numeric claims are cross-checked in §6.

## 6. `native_decide` numeric constants — 12 / 12 match the tex `AUDIT`

Each `native_decide` literal was matched to the tex's printed decimal. All 12
agree. The two field primes `pKB = 2130706433` and `pM31 = 2147483647` appear
in the tex symbolically (as `p_KB`, `p_M31`), not as literal digits, so they are
excluded from the digit cross-check.

| constant | value | `.lean` file | tex line |
|---|---|---|---|
| `BstarKB` | `274980728111395087` | `GrandeFinale.lean` | 211 |
| `BstarM31` | `16777215` | `GrandeFinale.lean` | 214 |
| `M_KB_a0` | `138634741058327852652` | `GrandeFinale.lean` | 232 |
| `M_KB_a0p` | `57198030366` | `GrandeFinale.lean` | 232 |
| `M_M31_a0` | `4281388998575706` | `GrandeFinale.lean` | 233 |
| `M_M31_a0p` | `1752700` | `GrandeFinale.lean` | 233 |
| `M31_watch` mass | `12769758` | `GrandeFinale.lean` | 236 |
| `bc` pencil numerator | `2097152` | `BC.lean` | 181 |
| `bc` KB `ω = n − m` | `980104` | `BC.lean` | 1774 |
| `bc` M31 `ω = n − m` | `980128` | `BC.lean` | 1775 |
| `mode17` null `N₉(0)` | `672` | `Frontier.lean` | 997 |
| `mode17` nonnull `N₉(s)` | `673` | `Frontier.lean` | 997 |

## 7. Coverage gaps (ranked by effort-to-value) `AUDIT`

Substantive tex results within the package's scope with no Lean counterpart.
Survey-only / analytic items expected to stay unformalized are listed last.

1. **`prop:q-moment-order-floor` / `prop:q-exact-target` (L2061–2118)** — the
   finite row-sharp Q constant tables (moment-order floors
   `94196` / `94991` / `641593` / `680397`; bit margins
   `22.1969` / `22.0109` / `3.2589` / `3.0730`). Trivial `native_decide`
   arithmetic, the cheapest gap, and the maintainer's stated "finite row-sharp
   Q constants" frontier.
2. **`thm:gf-deep-mca` / `prop:exact-tangent-cell` / `thm:gf-mca-from-ca` /
   `thm:subfield-confinement` (L434–546)** — four self-contained combinatorial
   "broad safe anchor" theorems, same elementary Hamming-distance style already
   machine-checked in `GrandeFinale.lean`. Best effort-to-value among the
   theorems.
3. **`thm:head-flatness` / `cor:head-q` (L1095–1150)** — the proved Weil-bound
   partial progress toward Q (`w ≤ 21–22` unconditional). The maintainer's
   "extend toward the Q inverse theorem" frontier.
4. **`thm:q-implies-sp` / `prop:q-sp-frontier-closure` (L1889–1925, L2277–2295)**
   — nearly covered; the §4 `sp_from_q` tightening + citation fix closes it
   almost for free.
5. **`prop:lattice-split` (L1336–1348)** — the `(W,N)`-module bijection under
   the whole BC program. `BC.lean` currently black-boxes it via an assumed
   injective map (`bc_dimension_bound`'s `hφ : Set.InjOn φ census`); formalizing
   it upgrades several conditional BC kernels to closed results.
6. **`cor:identity-prefix-unsafe` (L291–315)** — composes `prop:prefix-witness`
   + `thm:simple-pole-list-floor` (both already formalized) into one statement;
   a nearly-free composition gap.

Reasonable to skip (need heavy external input): `thm:no-old-band` (Linnik),
`def:fourier-flat-prefix-leaf` / `thm:fourier-flat-q` /
`cor:large-characteristic-fourier-examples` (Weil + Li–Wan sieve),
`lem:entropy-bookkeeping` / `thm:unsafe-envelope` (Stirling/entropy), and the
`§Conditional Asymptotic Closure` chain (asymptotic; its antecedent
`prob:entropy-inverse-q` is the central open problem, honestly left open).

## 8. Full 112-row correspondence table

Legend: **F** FAITHFUL, **D** DRIFT, **S** STRONGER, **W** WEAKER,
**N** NO-TEX-COUNTERPART.

### Table 1 — `GrandeFinale.lean` (39 decls, all F) `VERIFIED-CLEAN`

| decl | claimed tex label | verdict | note |
|---|---|---|---|
| `integer_budget_le` | `lem:integer-budget` | F | exact, tex L128–144 |
| `integer_budget_lt` | `lem:integer-budget` | F | strict form, exact |
| `first_match_ledger` | `lem:first-match-ledger` | F | disjoint-cover counting kernel; `def:first-match-ledger` has no Lean `def` (only the lemma is kernelized) |
| `Explained` (def) | `def:ca-mca` | F | matches tex L95 |
| `ExplainedPair` (def) | `def:ca-mca` | F | matches tex L95 |
| `MCABad` (def) | `def:ca-mca` | F | matches tex L97 (same witness `S`) |
| `CABad` (def) | `def:ca-mca` | F | matches tex L97 |
| `CABad_imp_MCABad` | `lem:basic-staircase` (pt 1) | F | matches tex L110–122 |
| `MCABad_antitone` | `lem:basic-staircase` (pt 2) | F | monotonicity |
| `B_MCA`, `B_CA` (defs) | `def:staircase` | F | matches tex L124–126 |
| `B_CA_le_B_MCA` | `lem:basic-staircase` | F | |
| `emca`, `eca` (defs) | `def:ca-mca` | F | matches tex L101–107 |
| `eca_le_emca` | `lem:basic-staircase` | F | |
| `distinct_value_floor` | `thm:simple-pole-list-floor`, `thm:fiber-to-slope` | F | Cauchy–Schwarz kernel = tex L275–288 |
| `nat_ceil_div_le` | (helper) | F | produces the `⌈…⌉` form |
| `exists_le_average` | `thm:fiber-to-slope`, `thm:simple-pole-list-floor` | F | averaging kernel, tex L275, L629 |
| `prefix_witness_maxfiber` | `prop:prefix-witness` | F | pigeonhole, tex L567–581 |
| `moment_upper` | `prop:moment-sandwich` | F | `Γ_r ≤ R^{r-1}` half, tex L714–717 |
| `moment_lower` | `prop:moment-sandwich`, `thm:moment-q` | F | `max ≤ (Σμ^r)^{1/r}` half |
| `moment_q_finite` | `thm:moment-q` | F | `R^r ≤ base^w·Γ_r`, tex L737–744 |
| `Certificates.pKB`, `pM31` (defs) | (numeric constants) | F | KoalaBear / Mersenne-31 primes, consistent usage |
| `Certificates.BstarKB`, `BstarM31` (+`_eq`) | `prop:finite-packet-consequences` (L208–215) | F | `274980728111395087` / `16777215` exact |
| `Certificates.M_KB_a0`, `M_KB_a0p`, `M_M31_a0`, `M_M31_a0p` | `rem:finite-artifacts` (L226–237) | F | all four exact |
| `Certificates.KB_unsafe`, `KB_adjacent_lower_fails`, `M31_unsafe`, `M31_adjacent_lower_fails` | `prop:finite-packet-consequences` | F | exact `M(a0)>B*` / `M(a0+1)≤B*` |
| `Certificates.M31_watch` | `prop:rung-veto` | F | `12769758 < 16777215`, tex L369 |

### Table 2 — `GrandeFinale/BC.lean` (25 decls, all F) `VERIFIED-CLEAN`

| decl | claimed tex label | verdict | note |
|---|---|---|---|
| `slope_elimination_unique` | `prop:slope-elimination` | F | tex L1320–1334 |
| `nearRational_dim_count` | `thm:near-rational` | F | dimension identity, tex L1374–1378 |
| `nearRational_binomial_count` | `thm:near-rational` | F | binomial-count kernel, tex L1359 |
| `codeword_agreement_unique` | `thm:near-rational` (uniqueness) | F | MDS/RS decoding-uniqueness kernel |
| `near_rational_line_algebra` | `cor:near-rational-line` | F | tex L1386–1390 |
| `support_sub_card_le` | `cor:near-rational-line` | F | Hamming subadditivity kernel |
| `split_test_remainder_zero` | `thm:deficiency-one-eliminant` | F | proof step tex L1411 |
| `deficiency_one_degree_bound` | `thm:deficiency-one-eliminant` | F | degree bound tex L1403 |
| `split_chart_tangent_slope_bound` | `prop:split-chart-tangent` | F | tex L1453–1473 |
| `base_field_floor_count` | `prop:base-field-floor` | F | census-counting identity, scoped partial |
| `poly_root_count_bound` | `prop:rank-one-distinct-slope-floor` | F | root-count bound |
| `distinct_value_lower` | `prop:rank-one-distinct-slope-floor` | F | tex L1560–1568 |
| `pole_averaging_select` | `prop:rank-one-distinct-slope-floor`, `prop:rank-one-floor` | F | averaging kernel |
| `bc_moving_root` | `thm:bc-moving-root` | F | disjoint-incidence abstraction, tex L1749–1762 |
| `bc_moving_root_div` | `thm:bc-moving-root`, `cor:bc-one-pencil` | F | |
| `bc_one_pencil_floor_KB` | `cor:bc-one-pencil` | F | `2097152/980104=2`, tex L1774 |
| `bc_one_pencil_floor_M31` | `cor:bc-one-pencil` | F | `2097152/980128=2`, tex L1775 |
| `commonDPart` (def) | `def:projective-locator-pencil` | F | `gcd(gcd A B) lamD` = `gcd(A,B,Λ_D)` |
| `commonDPart_dvd_pencil` | `def:projective-locator-pencil` | F | slightly stronger (divisibility) |
| `bc_dimension_bound` | `thm:bc-proper` | F | `|F|^{r1+r2}` half only, scoped |
| `saturation_identity` | `thm:saturation` | F | first identity tex L1812–1815 |
| `raw_bc_single_ray` | `cor:raw-bc-fails` | F | tex L1844–1849 |
| `line_ray_saturation` | `prop:line-ray-saturation` | F | tex L1868–1873 |
| `johnson_packing` | `thm:q-proper` | F | disjoint-uniform-packing kernel, tex L1688–1690 |
| `sp_stratum_bound` | `thm:sp-proper` | F | injective-encoding argument, tex L1953 |

### Table 3 — `GrandeFinale/SP.lean` (19 decls) `WEAKER-THAN-STATED`

| decl | claimed tex label | verdict | note |
|---|---|---|---|
| `descendedDepth` (def) | `prop:sp-pullback` | F | `⌈(w+1)/c⌉-1`, tex L1192 |
| `sp_pullback_depth` | `prop:sp-pullback` | F | iff, tex L1198–1202 |
| `coeffScale`, `coeffScalePair` (defs) | `def:coefficient-scale` | F | tex L1205–1215 |
| `dvd_coeffScale` | `lem:coeff-scale` | F | gcd-arithmetic leg only, scoped |
| `dvd_coeffScalePair` | (supports `lem:coeff-scale`) | F | |
| `binomial_coeffScale` | `cor:primitive-coeff-exclusion` | F | tex L1261–1266 |
| `ceilDiv_of_dvd` | (helper) | F | |
| `top_stratum_depth` | `prop:top-stratum-quotient-sieve` | F | proves the `≤` used downstream |
| `locator`, `locator_monic`, `locator_natDegree`, `locator_injective` | (support) | F | standard `ℓ_S` facts |
| `locator_diff_factor` | `prop:second-moment`, `prop:prefix-rigidity` | F | tex L673–677 |
| `prefix_rigidity` | `prop:prefix-rigidity` | **S** | STRONGER-THAN-TEX, documented: `M'.card = m` hypothesis explicitly omitted as unnecessary |
| `pair_census_le_of_max_fiber` | *(header cites `conj:Q`⟹`conj:SP`)* | **D** | phantom section header; content faithful |
| `sp_from_q` | *(header cites `conj:Q`, `conj:SP`, `thm:asymptotic`)* | **D+W** | phantom labels; real target `thm:q-implies-sp` (L1889) uncited; statement drops the proof's own `- Nsub` term (§4) |
| `sp_from_q_normalized` | *(same header)* | **D+W** | same, `Γ₂`-normalized form |
| `gamma2_ledger_split` | `prop:gamma2-ledger` | F | algebra kernel, scoped |

### Table 4 — `GrandeFinale/Frontier.lean` (14 decls, all F) `VERIFIED-CLEAN`

| decl | claimed tex label | verdict | note |
|---|---|---|---|
| `composite_prefix_descend`, `composite_prefix_gen_series` | `prop:composite-descend` | F | tex L1074–1093 |
| `mode17Fiber` (def), `mode17_null`, `mode17_nonnull`, `mode17_null_not_max` | `prop:mode-null-false` | F | `672` / `673` exact, tex L997–1000, `native_decide` |
| `q_atom_cell_ledger` | `prob:row-sharp-q` | F | trivial ledger step, scoped |
| `bc_chart_audit` | `prob:saturated-bc` | F | disjoint paid/pencil audit arithmetic |
| `extension_chart_pos_dim_exceeds`, `extension_chart_zero_dim` | `prop:extension-cell-target` | F | tex L419, L422–426 |
| `koalabear_mca_p_gt_Hext`, `koalabear_list_p_gt_Hext`, `mersenne31_mca_p_gt_Hext`, `mersenne31_list_p_gt_Hext` | `prop:extension-cell-target` | F | `4807520`/`4226236`/`9`/`8`, tex L409–418 |

Header footnote: `Frontier.lean` cites `grande_finale_bc_attempt.tex`
(nonexistent). All declarations cite real labels; header-only.

### Table 5 — `GrandeFinale/QEntropyInverse.lean` (5 decls, all D) `DRIFT-FOUND`

| decl | claimed | verdict | real target |
|---|---|---|---|
| `collision_moment_le_of_max` | `conj:Q`; "§1" of nonexistent patch | D | converse `thm:logmoment-equivalence` (L773) + `def:primitive-logmoment` (L756) |
| `halfMoment_eq_diagonal_mul_vandermonde` | "§4" (no label) | D | supporting linear-algebra fact |
| `halfMoment_det` | "§4" (no label) | D | same |
| `halfMoment_linearIndependent` | "§4" (no label) | D | `prop:vandermonde-kills-low-rank` (L876) |
| `halfMoment_subset_rank` | "§4" (no label) | D | generalizes `prop:vandermonde-kills-low-rank` to arbitrary submodules |

### Table 6 — `GrandeFinale/QFourierTao.lean` (5 decls, all D) `DRIFT-FOUND`

| decl | claimed | verdict | real target |
|---|---|---|---|
| `log_moment_to_max` | `lem:log-moment-to-q` (phantom) | D | `prop:moment-sandwich` mechanism (L714–723) |
| `collisionMoment` (def) | (patch-file def) | D | `def:primitive-logmoment`'s `Γ_r^prim` (L767–770) |
| `log_moment_to_max_gamma` | `lem:log-moment-to-q` (phantom) | D | `thm:moment-q` (L737–744) + forward `thm:logmoment-equivalence` (L788–804) |
| `q_flatness_from_collision` | `cor:asymp-q-fourier-tao` (phantom) | D | `thm:moment-q` exponentiated + `R_Q=(|B|^w Γ_q)^{1/q}` (Conclusion L2339) |
| `q_flatness_bit_certificate` | `lem:log-moment-to-q` (phantom) | D | bit-certificate inequality in `thm:moment-q` (L740–743), `prop:q-moment-order-floor` (L2094–2096), `prob:row-sharp-q` (L2185–2188) |

File header names `q_fourier_tao_finish_patch.tex` (nonexistent) and its three
phantom labels.

### Table 7 — `GrandeFinale/QPrimitiveCollision.lean` (5 decls, 5 N) — file header D

| decl | claimed | verdict | note |
|---|---|---|---|
| `collision_count_identity` | quotes "§'Expand the q-collision moment'" (not in tex) | N | moment↔tuple-count identity; no specific label claimed |
| `moment_poly_vanishing` | none | N | linear-algebra kernel |
| `trade_designed_distance` | "Tao uncertainty / BCH" (informal, `rem:entropy-inverse-skeleton` step 3, L963) | N | no `\label` claimed |
| `prefix_collision_rigidity` | cross-refs Lean `SP.prefix_rigidity` | N | sharper `w+2` vs `w+1` in a moment model; does not claim tex identity |
| `prefix_injective_on_small` | none | N | corollary of the above |

File header names `thm:primitive-log-collision` and
`q_fourier_tao_finish_patch.tex` (both nonexistent). No individual declaration
re-asserts a nonexistent label at the theorem level.
