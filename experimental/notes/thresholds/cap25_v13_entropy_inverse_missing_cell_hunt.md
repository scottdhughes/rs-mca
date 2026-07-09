# CAP25 v13: planted-structure missing-cell hunt for the primitive entropic inverse atom — the L828 escape clause returns ZERO candidates at toy scale

Status: `REFERENCE` (§0 — the atom's escape clause, removal list, frontier
normalization side condition, two alternatives, and Sidon/free-energy dichotomy
quoted verbatim with line refs) / `CONVENTION` (§1 — the baseline-relative
`excess_ratio`, the ES guard, and every removal-list cell's operational toy
definition, each tex-pinned; inherited from and consistent with PR #420) /
`MEASURED` (§2 the money table; §3 the headline null; §5 AP invisibility; §6 the
`w->p` ride-along; §7 the natural-trade attribution) / `ANALYSIS` (§4 the core
tension — why excess and large-family never co-occur off the caught cells) /
`AUDIT` (§8 the validated normalization guard; §9 the fidelity limits — the
`R=w` wall and the not-instantiable cells) / `OPEN` (§11 next measures).

**Verifier:** `experimental/scripts/verify_entropy_inverse_missing_cell_hunt.py`
(zero-arg, stdlib-only, self-contained, `RESULT: PASS (199/199 checks)`, exit 0,
~17 s, 311 MB RSS, `RLIMIT_AS` 2 GB). One script that **recomputes from scratch** —
fiber census, `Gamma_ell` by two code paths (power-sum census and DFT/Parseval),
the baseline-relative `excess_ratio`, the dyadic-level trades with exact
finite-population Shannon entropies and free-energy slope, the Vandermonde
rank-defect, and the multiplicative cell classifier — then gates every recomputed
number against the three committed data JSONs (exact on integers / rationals /
strings / bools, `1e-9` on floats). It recomputes both positive controls, the
negative control, the anchor AP / GP / composite / both heavy-fiber traps, the
`mu_16` and AP `w`-sweeps at `w in {1,3,5}`, the anchor natural-trade attribution,
the dual paths (Newton, Parseval, classifier exponent-vs-element view), the
normalization-trap monotonicity, and six tamper self-tests.

**What this is / is not.** This is **instrumentation**, consistent with the atom,
**not** a proof of cell-list completeness and **not** a claim on
`prob:entropy-inverse-q`. It is the sibling / follow-on to PR #420's toy dichotomy
instrumentation: #420 measured that the atom's robust Sidon/free-energy branch
reads `NEITHER` on the *natural* `mu_n` family; this packet asks the complementary
question — the atom's **escape clause** (L828): *is there a missing obstruction
cell?* — by **planting** candidate structures (arithmetic progressions, geometric
progressions, Sidon sets, coset unions, two-subgroup composites, shift towers,
single-heaviest-fiber families) and testing whether any generates genuine
collision excess while escaping every removal-list cell **and** passing the
frontier normalization. At toy scale (`N <= 18`), **none does**: every plant with
real excess is either **caught** by a removal-list cell or **killed** by the
`log|Omega^circ| - R log|K| = o(N)` side condition. This is measured completeness
support for the atom's alternative **(a)** at toy scale — not a proof — and it
names the two corners the toy cannot reach as the residual hunt space (§9, §11).
Every claim carries a label. Conventions are inherited verbatim from PR #420 and
extended here, never contradicted.

---

## 0. The atom, its escape clause, and the removal list `REFERENCE`

The maintainer's Q1 atom is the standalone additive-combinatorics statement
`prob:entropy-inverse-q` in `experimental/grande_finale.tex` (L827). Its opening
sentence contains the **escape clause** this packet hunts (L828, verbatim):

> Prove the following standalone additive-combinatorics statement, or identify the
> extra obstruction cell that must be added to the first-match ledger.

The **removal list** — the bounded-complexity algebraic cells the primitive
residual model `Omega^circ` is taken *after* (L839, verbatim):

> and let \(\Omega^\circ\subseteq\Omega\) be the primitive residual model after
> quotient pullbacks, Chebyshev/dihedral pullbacks, planted common blocks, tangent
> cells, extension cells, differential-locator low-defect cells, and saturation
> cells have been removed.

The **frontier normalization side condition** (L840–842, verbatim) — the guard
every candidate must pass, and the trap that kills single-fiber families:

> Assume the frontier normalization \[ \log|\Omega^\circ|-R\log|\K|=o(N). \]

The collision-excess trigger `Gamma_ell >= exp(eta N ell)` (L855–857) then forces
one of two alternatives (L861–867, verbatim):

> (a) A positive-density restriction of the datum lies in one of the
> bounded-complexity algebraic cells already removed above.
> (b) There is a positive-density set \(U\subseteq T\) for which
> \(\operatorname{rank}_{\K}\Span\{v_t:t\in U\}<\min(|U|,R)\).

and the robust proof form (L869, verbatim; the object PR #420 instruments):

> The robust proof form may pass through an additional Sidon/free-energy branch:
> either level-typical star trades have entropy-small difference
> \(H(Y-Y')\le H(Y)+o(N)\), leading by entropic BSG/PFR and a slice-derivative
> lemma to the rank-defect alternative above, or else the free-energy decay of
> \(Y-Y'\) bounds that level's contribution to \(\Gamma_\ell\) by
> \(\exp(-\Omega(N\ell))\).

A **candidate missing cell** would be a planted family with (i) genuine collision
excess, (ii) an entropy-small-doubling / ES trade population, (iii) escaping every
removal-list cell, and (iv) passing the normalization. This note reports **zero**
such candidates over the planted catalog at toy scale.

---

## 1. Conventions — baseline-relative excess, ES guard, cell defs `CONVENTION`

Every operationalization is inherited from PR #420 (same power-sum syndrome
`Psi(M)=(sum y,...,sum y^w)`, dyadic level `j=floor(log2(N/mean))`, trade
base-support rule, exact finite-population Shannon entropy, `R=w` collision-moment
normalization, `DOUB_C=0.10` / `DECAY_C=0.05` thresholds). This packet adds three
load-bearing conventions.

- **Baseline-relative `excess_ratio` (the false-positive fix).** Raw `Gamma_2` and
  `rho_max` inflate by **Poisson sub-sampling** whenever `|Omega^circ| < p^w` — a
  small family scatters `C` supports into `p^w` bins and the empty bins make the
  occupied ones look heavy. Excess must be measured **relative to a same-size
  uniform-random baseline**. For `C` balls in `p^w` bins the exact multinomial
  second moment is `E[Gamma_2] = p^w/C + (C-1)/C`, so
  `excess_ratio = Gamma_2 / (p^w/C + (C-1)/C)`. `excess_ratio >> 1` is structure;
  `excess_ratio ~ 1` is random. This flips the negative control from raw
  `rho_max = 14.5` (would falsely read as heavy structure) to `excess_ratio = 0.94`
  (correctly random). The `excess` flag fires at `excess_ratio > 1.3`.
- **ES guard.** A level counts toward the entropy-small-doubling branch only if it
  carries a genuine population: **`>= 8` distinct trades and `H(Y) >= 1` bit**.
  Without the guard a single trade is trivially "small-doubling" (`gap ~ 0`) and
  would spuriously fire ES on a degenerate one-fiber level.
- **Normalization guard.** `norm_ok` iff `gap/N = (log2|Omega^circ| - w log2 p)/N
  > -0.25` (a toy stand-in for `o(N)`). A family whose `|Omega^circ|` has collapsed
  fails this — the classic false positive.

**Removal-list cells, operational toy definitions (each tex-pinned).** A support is
carried as a set of field elements `V subset F_p`, so the classifier is
domain-agnostic (multiplicative `T=mu_n` and additive `T=AP` alike); where the
exponent view exists it is used as a **dual path**.

| cell (L839) | operational toy test | tex pin |
|---|---|---|
| quotient pullback | `V` is a union of `H`-cosets: `V*g == V` for `g = gen(H)`, proper `H < F_p^*` (equivalently coeff-scale `s(L_V) > 1`) | `prop:sp-pullback` L1189, `lem:coeff-scale` L1217 |
| Chebyshev/dihedral | `V` invariant under an inversion-reflection `x -> c*x^{-1}` for some `c` | `thm:near-rational` L1350 |
| planted common block | all members share a fixed block `P` (support intersection `|P| >= 1`) | `thm:head-flatness` L1095 |
| differential-locator | `rank_{F_p} Span{v_t : t in U} < min(|U|,R)` — alternative (b); toy `R=w` | `prop:vandermonde-kills-low-rank` L876 |
| tangent / extension / saturation | not instantiable in the pure `Psi` subset-sum toy (see §9) | `prop:exact-tangent-cell`, `prop:extension-cell-target`, `thm:saturation` |

---

## 2. FINDING 0 (money table): every real-excess plant is caught or killed `MEASURED`

Full catalog. `excess_ratio > 1.3` = genuine excess (bold); `gap/N` with `!` =
normalization-killed (`norm_ok` false); `caught` = removal-list verdict.

| plant | `(p,N,m,w)` | `excess_ratio` | best rel-doub | ES? | `gap/N` | caught / verdict |
|---|---|---:|---:|:--:|---:|:--|
| **PC1** coset-union(c=2) | `17,16,8,3` | **4.339** | 0.807 | N | −0.383! | CAUGHT quotient+dihedral |
| **PC2** planted-block{0,1,2} | `17,16,8,3` | 0.878 | 0.914 | N | −0.121 | CAUGHT planted-block(3) |
| **NC** random-restrict f=0.1 | `17,16,8,3` | 0.941 | — | N | −0.116 | NONE (no excess) |
| RAW `mu_16` anchor | `17,16,8,3` | 0.823 | 0.932 | N | +0.087 | (planted-block(1) = lex artifact†) |
| H1 AP{0..15} @F31 | `31,16,8,3` | 0.929 | 0.876 | N | −0.076 | (planted-block(1) = lex artifact†) |
| H1 AP{0..17} @F37 | `37,18,9,3` | 1.024 | 0.922 | N | −0.003 | (lex artifact†) |
| H1 AP{0..11} @F31 (`w=2`) | `31,12,6,2` | 1.054 | 0.840 | N | −0.005 | NONE |
| H1c centered-AP @F31 | `31,16,8,3` | 0.929 | 0.876 | N | −0.076 | (lex artifact†) |
| H1b AP step-2 @F31 | `31,16,8,3` | 0.929 | 0.876 | N | −0.076 | (lex artifact†) |
| H3 GP(g=3,\|16\|) @F31 | `31,16,8,3` | 0.965 | 0.858 | N | −0.076 | (lex artifact†) |
| H3 GP(g=2,\|18\|) @F37 | `37,18,9,3` | 0.990 | 0.924 | N | −0.003 | (lex artifact†) |
| H2 Sidon\|5\| @F31 | `31,5,3,2` | 0.991 | — | N | −1.317! | NONE (killed) |
| H4 H3∪H5 comp @F31 | `31,8,4,2` | 0.933 | — | N | −0.472! | NONE (killed) |
| H5 shift-tower(h=5) @F31 | `31,10,5,2` | 0.799 | — | N | −0.193 | CAUGHT trade-quotient+dihedral |
| A H6∪H10(\|14\|) @F31 | `31,14,8,3` | 0.965 | 0.848 | N | −0.236 | CAUGHT trade-quotient |
| A H6∪H10(\|16\|) @F61 | `61,16,8,3` | 1.015 | 0.916 | N | −0.259! | CAUGHT planted-block+trade-quotient |
| **C** heavy-fiber AP{0..15} @F31 | `31,16,8,3` | **4.000** | — | N | −0.804! | KILLED by normalization |
| **C** heavy-fiber `mu_16` @F17 | `17,16,8,3` | **6.991** | — | N | −0.591! | KILLED by normalization |

**The pattern is exact:** every row with `excess_ratio > 1.3` (PC1 4.34; the two C
traps 4.00 / 6.99) is either **CAUGHT** (PC1 quotient+dihedral) or **KILLED** by the
normalization side condition (`gap/N < -0.25`). Every row that is *not* caught and
*is* normalization-OK has `excess_ratio ~ 1` — no excess. The two conditions
(real excess; large normalization-valid family) never co-occur off a caught cell.
`n_candidate_missing_cells = 0`.

† **Honesty note (`AUDIT`).** On the full / AP / GP families the classifier reports
`planted-block(1) = {0}`. This is a **lex-sampling artifact**: the family-cell test
intersects the first 6000 `m`-subsets, and for `C(16,8)` the first `C(15,7)=6435 >
6000` combinations in lexicographic order all contain the minimal element `0`, so
the intersection is trivially `{0}`. (On the two `@F37` rows, `N=18/m=9`, the same
mechanism gives `planted-block(2) = {0,1}`, since `C(16,7)=11440 > 6000`.) It is
**not** a genuine planted block (contrast
PC2, where `{0,1,2}` sits in *every* member by construction). It is immaterial to
the null: these rows carry no excess (`excess_ratio < 1.3`), so `candidate` is
already false, and a spurious catch only reinforces that.

---

## 3. FINDING 1 (headline): the escape clause returns ZERO candidates `MEASURED`

Over the entire planted catalog, at every tested toy, the atom's escape clause
("identify the extra obstruction cell") yields **no candidate**. Every plant
generating genuine collision excess is either

- **caught** by a removal-list cell — quotient / dihedral (PC1, shift-tower,
  two-subgroup composite), planted-block (PC2), operational defs tex-pinned at
  `prop:sp-pullback` L1189 / `lem:coeff-scale` L1217 / `thm:near-rational` L1350 /
  `thm:head-flatness` L1095; or

- **killed** by the frontier normalization side condition
  `log|Omega^circ| - R log|K| = o(N)` (the C heavy-fiber traps, H2 Sidon, H4
  composite — all `gap/N < -0.25`).

No planted family lands on the atom's alternative **(b)** (a positive-density rank
defect): the Vandermonde rank-defect is `0` at every trade-bearing level of every
plant (§9, the `R=w` wall). And no planted family exhibits an entropy-small-doubling
(ES) population: `any_ES` is false everywhere. This is measured completeness support
for the atom's alternative **(a)** — at toy scale, and only at toy scale.

---

## 4. FINDING 2 (the structural reason): excess ⟺ multiplicative-subgroup ⟺ small & caught `ANALYSIS`

Why do real excess and a large normalization-valid family never co-occur off the
caught cells? Because in the toy the two are structurally coupled through the
multiplicative subgroup lattice.

- **Excess requires multiplicative-subgroup identification.** Genuine power-sum
  collision excess arises when many `m`-subsets share a syndrome — which, over
  `F_p`, happens when the subsets are related by a multiplicative-subgroup /
  coset action that fixes the power sums. PC1 (coset union) has `excess_ratio 4.34`;
  its supports are *exactly* `H`-coset unions, so it is **caught** by the quotient
  cell. The C traps push this to the extreme (one PTE class, `excess_ratio 4.0`–`7.0`).
- **That structure shrinks the family.** A coset-union family or a single heaviest
  fiber has `|Omega^circ|` exponentially smaller than `C(n,m)`, so
  `gap/N << 0` — it **fails normalization**. PC1 `gap/N = -0.383`, C traps `-0.80` /
  `-0.59`.
- **Additive / composite structure at normalization-valid sizes is
  collision-neutral.** Arithmetic progressions, geometric progressions, generic
  two-subgroup composites and centered/step-2 APs all sit at `excess_ratio ~ 1`
  (0.93–1.05) — random-identical — while keeping a full normalization-valid family.
  They generate no power-sum excess to begin with.

So **large-family ∧ real-excess never co-occur** except on a caught cell. The escape
clause has nowhere to land: the only way to manufacture excess is to invoke exactly
the multiplicative-subgroup structure the removal list already prices.

---

## 5. FINDING 3: additive structure is invisible to both the excess hypothesis and alternative (b) `MEASURED`

Arithmetic progressions — the natural additive candidate for a *missing* (additive)
cell — produce **no** power-sum excess at any tested `(p,w)`: `excess_ratio` is
`0.93`–`1.05` across F31 / F37, `w in {2,3}` (H1, H1c, H1b rows), statistically
indistinguishable from a random domain. The mechanism is precise:

- Vandermonde / power-sum fibers collapse **only under multiplicative
  identification** (a subgroup action fixing `(sum y^k)_{k<=w}`). Additive shifts
  `y -> y+c` change the power sums **nonlinearly** (`sum(y+c)^k` mixes lower
  moments), so an AP produces no alternative syndrome coincidences.
- Additive structure also cannot trigger alternative **(b)**: `<= R` distinct AP
  points give a **full-rank** Vandermonde (`prop:vandermonde-kills-low-rank`),
  rank-defect `0` at every AP level (verifier-gated). Distinct points ⟹ full rank.

So additive structure is invisible to *both* the excess hypothesis *and* the
rank-defect alternative — which is exactly **why the removal list is purely
multiplicative / algebraic**. The one place a faint *real* additive signature
survives is in trade relative-doubling: at the anchor size, the AP family sits
slightly **below** a same-size random domain — rel-doubling `0.715` (AP) vs `0.747`
(random) at `w=1`, and `0.876` (AP) vs `0.946` (random) at `w=3`. This is the first
live calibration of an ES branch on an additive family; but both numbers are
`~0.7`–`0.9`, an order of magnitude away from the ES threshold (which needs
rel-doubling near the `gap <= 0.10*N` regime). Additive structure nudges the
doubling but comes nowhere near feeding the entropy-small-doubling branch.

---

## 6. FINDING 4: `w->p` ride-along — NEITHER is not a `w=3` artifact `MEASURED`

PR #420 read `NEITHER` at `w=3` only. Fourier-flatness (`thm:fourier-flat-q`) holds
for `w = o(sqrt p)`; at `p=17`, `sqrt p ~ 4.1`, so `w=3` sits near the flat edge and
`w >= 5` is past it. Sweeping `mu_16 @F17` over `w=1..7` and `AP @F31` over `w=1..6`:

| `mu_16 @F17` | `w=1` | `w=3` | `w=5` | `w=7` |
|---|---:|---:|---:|---:|
| `excess_ratio` | 0.999 | 0.823 | 0.991 | 1.000 |
| best rel-doubling | 0.742 | 0.932 | — | — |
| `rho_max` (raw) | 1.00 | 2.67 | 220.6 | 63767 |
| `Gamma_8` (raw) | 1.00 | 13.1 | 2.0e14 | 3.4e31 |
| min trade support | 4 | 8 | 16 | 16 |
| `2(w+1)` BCH | 4 | 8 | 12 | 16 |
| rank-defect | 0 | 0 | 0 | 0 |
| trade levels | 2 | 2 | 0 | 0 |

Past the Fourier-flat edge (`w >= 4`), the level-typical relative doubling **rises
toward 1.0** (`0.742 -> 0.969` at `w=4`) while `excess_ratio` stays `~ 1`; the
exploding raw `rho_max` / `Gamma_8` at `w >= 5` is **pure sub-sampling** (the
occupied band goes sparse — `trade levels -> 0` — it does not regrow with popular
structure). The minimum trade support saturates the `2(w+1)` BCH barrier at every
`w`, and the Vandermonde rank-defect is `0` everywhere. The AP side of the sweep is
identical in character (`excess_ratio ~ 1`, rank-defect `0`, `any_ES` false). PR
#420's `NEITHER` verdict is therefore **not** a `w=3` artifact: the popular band goes
sparse as `w -> p`, it does not regrow.

---

## 7. FINDING 5: natural-trade attribution — the toy excess is substantially cell-borne `MEASURED`

Applying the removal-list classifier to PR #420's *natural* anchor popular-level
star trades (`mu_16 @F17`, `RAW`), a substantial fraction are removal-list-borne —
direct measured support for alternative **(a)**:

| level `j` | trades | quotient-borne | dihedral-borne |
|---:|---:|---:|---:|
| `0` | 220 | 30.9% | 24.1% |
| `1` | 53 | 28.3% | 37.7% |

At `j=1`, `37.7%` of popular star trades are dihedral-borne and `28.3%` are
quotient-borne (`30.9% / 24.1%` at `j=0`). The natural toy popular excess is thus
substantially carried by the removal-list cells the atom already prices; the
**uncaught remainder** is BCH-saturated near-Sidon primitive residual (min support
`= 2(w+1)`, rank-defect `0`, no ES input) — precisely the object the robust route
is designed to handle, with no entropy-small-doubling to feed it. This is the
`ANALYSIS` §4 tension seen from the trade side: what excess there is, is cell-borne;
what is left over is pseudorandom.

---

## 8. FINDING 6: the normalization trap is a validated guard `AUDIT`

Single-heaviest-fiber families are the sharpest false-positive: restrict a domain to
its one heaviest power-sum fiber and it reaches `excess_ratio 4.0`–`7.0` *with*
(trivially) small within-class doubling — everything a candidate needs **except**
`|Omega^circ|`, which has collapsed. The frontier normalization kills them on the
atom's **own** hypothesis: `gap/N = -0.804` (AP heavy fiber) / `-0.591`
(`mu_16` heavy fiber), both `< -0.25`. The verifier asserts the monotonicity that
makes the guard principled: over the `k` heaviest fibers, the normalization gap is
**strictly increasing** in the cumulative member count (`k = 1,2,4,8`), so *fewer
members ⟹ more negative gap* — a single fiber is always the most negative, and the
guard is never accidentally passed by a genuinely large family. Showing the trap is
killed is what validates the side condition as more than a formality.

---

## 9. Fidelity limits — what the toy cannot test `AUDIT`

State honestly. Three removal-list cells are **not instantiable** in the pure `Psi`
subset-sum toy, and the fourth is **untriggerable** at `R=w`:

- **tangent / extension / saturation cells** are decoding-layer objects — a
  received-line / codeword-proximity object (`prop:exact-tangent-cell`),
  extension-valued slopes in a proper field extension (`prop:extension-cell-target`;
  the toy uses a **prime** field, so every locator splits over `F_p`), and an
  MCA-ray re-bundling count (`thm:saturation`). None has a shadow in a fiber census
  that counts raw supports over a prime field. The toy abstracts them away; it cannot
  confirm or deny a candidate hiding there.
- **the differential-locator cell is untriggerable at `R=w`** — the toy's
  `R=w` wall. Any `<= R` distinct points give a full-rank Vandermonde
  (`prop:vandermonde-kills-low-rank`), so the rank-defect (alternative (b)) is
  structurally `0` for every plant. Alternative **(b)** is **untestable until
  `R > w`**.

These scope what the toy CAN test: the multiplicative-algebraic cells (quotient,
dihedral, planted-block) and the additive candidate — all confirmed caught or
excess-neutral — but **not** alternative (b) and **not** the decoding-layer cells.
The measured null is a null over the instantiable cells at `R=w`, no more.

---

## 10. Guards and verification `AUDIT`

The verifier PASSES **199/199** checks in ~17 s (311 MB RSS, `RLIMIT_AS` 2 GB),
recomputing from scratch and gating against the committed data. Its dual-path
guards, each an independent code path:

- **Newton.** The power-sum syndrome fiber-size multiset equals the elementary-
  symmetric (locator) fiber-size multiset (`w < p`) — the fiber census is convention-
  independent.
- **Parseval.** `Gamma_2` by direct census (`p^w sum N^2 / C^2`) equals
  `1 + (sum_{t != 0}|E(t)|^2)/C^2` from the DFT of the fiber-count function, to
  `< 1e-7` on the anchor.
- **Classifier dual-view.** On 400 anchor supports, the exponent (`mu_n`, `+n/c` and
  `t-e`) tests agree with the field-element (multiplicative-coset, inversion) tests —
  `0/400` mismatch — and a full subgroup is quotient-caught with coeff-scale `> 1`
  while an AP is not (coeff-scale `= 1`).
- **Trap monotonicity.** The normalization gap is strictly increasing in cumulative
  member count; the single heaviest fiber fails `o(N)`.
- **Six tamper self-tests** (each must be caught): a perturbed anchor `Gamma_2`; a
  faked rank defect; the convention flip (raw `rho_max` would mis-flag NC while
  `excess_ratio` does not); a corrupted-fiber Parseval falsification; a corrupted
  Newton multiset; and a forced AP "candidate" blocked by `norm_ok`.

---

## 11. OPEN — next-measure list `OPEN`

The two corners the toy cannot reach (§9) are the residual hunt space; instrumentation
targets recorded as open:

- **Break the `R=w` wall.** Build a true moment-curve toy with `R > w` (received
  word `u + z v`, a decoding-layer object) so that alternative **(b)** and the
  differential-locator cell become **triggerable** — the only way to exercise the
  rank-defect alternative on a toy.
- **The large-subgroup normalization-valid excess corner.** Keep a small-index
  subgroup `mu_n` exponentially large (so `gap/N` stays `> -0.25`) while retaining
  real excess; test composite two-subgroup locators with coeff-scale `1` that the
  current quotient test does not catch. This is the one corner where a genuine
  missing cell could still hide.
- **Decoding-layer shadow (`u + z v`).** Instantiate the tangent / extension /
  saturation cells directly so the classifier can be exercised on the three cells the
  pure subset-sum toy abstracts away.

---

## 12. Weave and nonclaims `AUDIT`

- **`prob:entropy-inverse-q` (L827), escape clause (L828), removal list (L839),
  frontier normalization (L840), alternatives (L861), dichotomy (L869),
  `prop:vandermonde-kills-low-rank` (L876), `rem:mass-aware-logmoment` (L966).** The
  atom and the objects this note instruments; every quote is line-provenanced and the
  cell labels are gated present in the tex.
- **PR #420 `cap25_v13_entropy_inverse_toy_dichotomy` (sibling instrumentation).**
  The Lane 1 packet whose conventions this packet inherits verbatim (power-sum
  syndrome, dyadic level, trade base-support, exact finite entropy, `DOUB_C`/`DECAY_C`).
  #420 measured the robust Sidon/free-energy branch reads `NEITHER` on the natural
  family; this packet measures the complementary escape clause by planting structure,
  and finds zero candidate missing cells. It extends #420, never contradicts it.
- **#417 `cap25_v13_liftclass_cost_model_refuted` / #416
  `cap25_v13_q_eq_masked_participation_ratio`.** The lift-class removal pricing and
  the masked-participation object. This packet's alternative-(a) attribution (§7 —
  the toy excess is cell-borne) is the trade-side complement of #417's refutation.
- **Cell operational pins (`prop:sp-pullback` L1189, `lem:coeff-scale` L1217,
  `thm:near-rational` L1350, `thm:head-flatness` L1095).** The removal-list cells'
  deployed definitions; the toy classifier is a faithful small-scale shadow of each.

**Nonclaims.**

- This note does **not** prove the removal list is complete, does **not** prove or
  refute `prob:entropy-inverse-q`, and does **not** exhibit a positive-density rank
  defect (alternative (b)) or an entropy-small-doubling object at any scale.
- The zero-candidate result is **measured completeness support for alternative (a) at
  toy scale** (`N <= 18`, `R = w`), **not** a proof of cell-list completeness and
  **not** a claim on the atom. The two corners the toy cannot reach — `R > w` and the
  large-family normalization-valid excess — are named explicitly (§9, §11) as the
  residual hunt space.
- The `planted-block(1)` catches on the RAW / AP / GP rows are a **lex-sampling
  artifact** (§2 †), immaterial to the null.
- The baseline-relative `excess_ratio`, the ES guard, and `DOUB_C=0.10` /
  `DECAY_C=0.05` / `norm_ok` at `gap/N > -0.25` are conventions; the null is reported
  as robust to any `O(1)` choice, since every real-excess plant misses `norm_ok` by a
  wide margin or is caught outright.
