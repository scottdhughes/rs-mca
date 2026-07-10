# Asymptotic RS-MCA closed-ledger citation audit — 48 `FOUND-EXACT` / 3 `FOUND-WEAKER` / 0 `FOUND-AMBIGUOUS` / 3 `PHANTOM`

Status: `AUDIT` (citation-resolution over the 51 descriptive bracket-citations
of `thm:closed-ledger-package` plus the four definitional joints, at base
`7d72817`) / `FOUND-EXACT` (§3 — all C1–C8 payments resolve to real, verbatim
labels in `cap25_cap_v13_raw.tex` and `grande_finale.tex`) / `PHANTOM` (§2 — the
two C9 moduli manuscripts `Cho26ModuliSelf` / `Cho26ModuliFinal` exist nowhere
in the tree; C9's load-bearing routing payment resolves to them) /
`FOUND-WEAKER` (§4 — the three definitional joints B1/B3/B4 each import a source
result at a strictly weaker or differently-normalized form than the paper's use;
missing lemma named in each case).

**Verifier.** `experimental/scripts/verify_asymptotic_ledger_audit.py`
(zero-arg, stdlib-only, knobs `ALAUD_AS_CAP_GB` / `ALAUD_DATA_DIR`) — `RESULT:
PASS`: 63 located quotes byte-match within ±5 lines of their stated source line,
51 cell citations and 4 joints tallied, the quasicube derivation checked as
arithmetic, the moduli manuscripts confirmed absent, and 8 tamper self-tests
(corrupted quote, wrong line, fake label, mangled total, missing source,
moduli-flag, quasicube-exponent, steering-total) all rejected. Machine-readable map:
`experimental/data/asymptotic_rs_mca_closed_ledger_audit.json`.

**What this is.** A citation-resolution and *statement-level*-match audit of
`experimental/asymptotic_rs_mca.tex`. Its central `thm:closed-ledger-package`
(L106) proves closure by nine cell paragraphs `(C1)–(C9)` (L112–L128), each
citing existing results by *descriptive* bracket-names — `\cite[quotient-remainder,
quotient support, quotient-image, and bounded-census ledgers]{Cho26CapV13}` and
the like — never by `\label`. For each descriptive noun-phrase this note locates
the actual labeled result in the named source (file + line + verbatim head) and
classifies it `FOUND-EXACT` / `FOUND-WEAKER` / `FOUND-AMBIGUOUS` / `PHANTOM`.
This is the house #418 pattern — the Lean↔tex correspondence audit
(`experimental/notes/audits/lean_grande_finale_correspondence_audit.md`, every
declaration mapped to its actual label with FAITHFUL/DRIFT/PHANTOM verdicts)
transported from Lean declarations to LaTeX citations.

**What this is not.** NOT a re-proof. The internal correctness of the cited
proofs is not re-verified — only that a labeled result exists whose *statement*
covers the claimed payment at the claimed strength. The BSG and quasicube
literature theorems are not re-derived; only their stated forms are matched to
the standard statements (the boolean-difference *application* is verified as pure
logic). No judgement is offered on whether the absent moduli manuscripts, if
supplied, would close C9. This audit does not itself promote or block: it is
collaborative input to the maintainer's own promotion decision.

**Motivation.** The maintainer's `2026-07-09` agents-log entry for `7d72817`
(the commit adding the paper) names this as the next step, verbatim:

> Audit the cited closed-ledger package line by line against v13 raw and Grande
> Finale labels, then decide whether to promote this paper or merge its
> theorem/proof into the next main Paper D/towards-prize revision.

The same entry states the package is "consolidating the moduli-ledger drafts"
and asks that it be "accepted from `cap25_cap_v13_raw.tex`, `grande_finale.tex`,
and the moduli-ledger notes." Those moduli-ledger notes are the object of §2.

---

## 1. Headline `AUDIT`

| block | citations | verdict |
|---|---|---|
| C1 quotient-pullback | 8 | all `FOUND-EXACT` |
| C2 Chebyshev/dihedral | 3 | all `FOUND-EXACT` |
| C3 planted-block | 4 | all `FOUND-EXACT` |
| C4 tangent/deep-center | 3 | all `FOUND-EXACT` |
| C5 extension/descent | 7 | all `FOUND-EXACT` |
| C6 differential-locator/regular-rank | 6 | all `FOUND-EXACT` |
| C7 saturation/effective-image-collapse | 4 | all `FOUND-EXACT` |
| C8 balanced-core/split-pencil | 11 | all `FOUND-EXACT` |
| C9 Fourier/Sidon | 5 | 2 `FOUND-EXACT`, **3 `PHANTOM`** |
| **cells total** | **51** | **48 `FOUND-EXACT`, 3 `PHANTOM`** |
| B1 normalization | joint | `FOUND-WEAKER` |
| B2 cells vs removal list | joint | `STRUCTURAL` (consistent) |
| B3 window uniformity | joint | `FOUND-WEAKER` |
| B4 lower side | joint | `FOUND-WEAKER` |

Four-way tally over the 54 citation-resolution entries (51 cells + B1/B3/B4):
**48 `FOUND-EXACT`, 3 `FOUND-WEAKER`, 0 `FOUND-AMBIGUOUS`, 3 `PHANTOM`.** B2 is a
structural mapping, excluded from the four-way count.

The one-line reading: the algebro-geometric spine of the ledger (C1–C8) is
**faithfully cited** — the descriptive names resolve, usually verbatim, to real
labels in the two in-tree manuscripts. The single promotion-blocking gap is **C9**,
whose Fourier/Sidon *routing* payment is cited to two manuscripts that are not in
the repository; the three definitional joints B1/B3/B4 are `FOUND-WEAKER` in
named, repairable ways.

## 1b. Steering alignment — the mandated audit vocabulary (`eb42b82`) `REFERENCE`

While this audit was being assembled, the steering was rewritten
(`agents.md`, commit `eb42b82`, "Update agent priorities for asymptotic RS
MCA proof"): adversarial proof audits are now priority 2, and every attack
must end as `NO ISSUE` / `FIXED` / `OPEN GAP` / `COUNTEREXAMPLE_NEW_FLOOR`
with exact file/label references. This packet is that audit class for the
citation layer. Translation (gated in the data JSON `steering_alignment`
block):

| mandated verdict | count | composition |
|---|---:|---|
| `NO ISSUE` | 51 | 48 `FOUND-EXACT` cell citations + the B2 structural map + the BSG and quasicube checks (§C) |
| `OPEN GAP` | 6 | 3 `PHANTOM` (all C9/moduli, FINDING-1) + B1 normalization bridge + B3 window uniformity + B4 lower-side collision loss |
| `FIXED` | 0 | — |
| `COUNTEREXAMPLE_NEW_FLOOR` | 0 | — |

Against the steering's seven assigned failure modes: *missing cell in the
bad-line classification* → `NO ISSUE` (B2); *wrong field denominator or
base/extension-field ledger* → `OPEN GAP` (B1); *unsupported Fourier/Sidon
payment* → `OPEN GAP` (FINDING-1); *misuse of BSG or quasicube growth* →
`NO ISSUE` (§C); *incorrect first-match disjointization* and
*entropy-frontier algebra error* were **not attacked here** (out of
citation-audit scope; natural follow-up packets); *mismatch between
asymptotic proof and finite deployed rows* is partially covered — the
paper's own closing Remark scopes finite rows out, and the nearest audited
joint is B3.

The rewritten steering also **names the moduli manuscript's expected path**
— `experimental/rs_mca_moduli_ledger_final.tex` — which does **not** exist
in the tree at `eb42b82`. This sharpens FINDING-1 from "cited manuscripts
unlocatable" to "steering-referenced file absent": the one missing source
now has a definite expected location, and dropping the manuscript there
resolves C9's three `PHANTOM` citations in place.

## 2. `FINDING-1` — the C9 moduli manuscripts are absent `AUDIT`

Severity: **promotion-blocking for C9.** C9 (paper L128) cites, to
`\cite{Cho26ModuliFinal,Cho26ModuliSelf}`:

> The Sidon/Fourier operational cut, the split between Sidon-heavy and
> high-energy fibers, and the fact that major arcs route to algebraic cells while
> minor arcs are Fourier-flat are the moduli-ledger results of [...]. They are
> restated and used below in `\cref{def:sidon-paid,prop:energy-extract,thm:primitive-q}`.

Those two bibitems are `Cho26ModuliSelf` ("The Moduli Ledger for the Asymptotic
Reed–Solomon MCA Frontier") and `Cho26ModuliFinal` ("A Moduli Ledger for
RS–MCA"). **No file in the tree is either manuscript.** Evidence, all machine-checked
by the verifier's gate (f):

- No file named `*moduli*` exists anywhere under `experimental/` or `tex/`
  (excluding `.lake`).
- The manuscript titles (`Moduli Ledger for`, `Asymptotic Reed`) appear only
  inside `asymptotic_rs_mca.tex` itself (abstract + bibliography).
- The distinctive C9 vocabulary — `major arc`, `minor arc`, `operational cut`,
  `high-energy fiber`, `Moduli Ledger` — appears in **exactly one file**:
  `experimental/asymptotic_rs_mca.tex`. (`Sidon` and `Fourier-flat` do occur in
  `grande_finale.tex` and the threshold notes, but the *operational-cut / arc-routing*
  layer that C9 attributes to the moduli notes does not.)

This is independently corroborated by the #418 Lean audit, whose §3 header
records that `QEntropyInverse.lean` and `QFourierTao.lean` "cite labels and a
manuscript file that exist nowhere in the repo." The same phantom manuscript
surfaces there.

**Load-bearing check.** Is C9's phantom citation actually on the critical path,
or decorative? The paper's own primitive-Q chain is *conditional* on the
Fourier/Sidon cell being paid: `def:sidon-paid` (L196) defines the cell as paid,
`prop:energy-extract` (L202) *assumes* it paid, and `thm:primitive-q` (L236) is
stated "In every frontier primitive leaf with **paid** Fourier/Sidon cell." The
cell is paid, per C9, by the moduli-ledger *routing* result ("major arcs route to
algebraic cells"). The paper's §3–§4 re-derive the *energy-extraction* and
*BSG+quasicube* half of C9 in-line (so that content is not phantom — see §5), but
the **routing claim** — that every heavy fiber with large additive closure is an
already-paid algebraic major arc — is asserted at L200 and proved nowhere
in-tree; its authority is the missing moduli notes. C9 is therefore
`BLOCKED-BY-MISSING-SOURCE`, not merely mis-cited.

## 3. The nine cells `AUDIT` / `REFERENCE`

Every row below is a descriptive citation → resolved label (file:line), verbatim
head confirmed by the verifier. `Cho26CapV13` = `cap25_cap_v13_raw.tex`;
`Cho26Grande` = `grande_finale.tex`.

**C1 — quotient-pullback (8, all `FOUND-EXACT`).** quotient-remainder lower/support
ledger → `quotient-remainder deep-point lower ledger` (CapV13:945); divisor-union
support → `divisor-union quotient support ledger` (CapV13:1346); quotient-image →
`exact finite-parameter quotient image ledger` (CapV13:1872, verbatim);
affine/projective lcm → `affine lines as the degree-one lcm ledger` (CapV13:1914)
+ `exact projective quotient image ledger` (1955); pullback recursion →
`quotient-pullback recursion` (CapV13:6684); bounded census → `bounded quotient
census, exact arithmetic certificate` (CapV13:5970). Grande side: first-match
convention → `first-match upper ledger` (Grande:148); quotient status cell →
`top-stratum quotient sieve` (Grande:1268). *Provenance note:* the literally-named
`quotient paid status cell` label is `def:capf-quotient-status` at CapV13:5838,
i.e. in v13-raw rather than in Grande as the bracket suggests; Grande does isolate
the status via `prop:top-stratum-quotient-sieve` + `cor:primitive-coeff-exclusion`,
so the content is sound (attribution annotation only).

**C2 — Chebyshev/dihedral (3, all `FOUND-EXACT`).** `exact Chebyshev fibers on
$x$-coordinate twin-coset domains` (CapV13:3957); `torus uniformization of circle
codes` (CapV13:4010, transport also 5339); `deployed circle parameters:
Mersenne-31 with QM31` (CapV13:4083). *Note:* "dihedral" carries no standalone
label; the paper (L114) argues dihedral cells are quotient cells "paid by the same
downstairs-support and image ledgers" — a reduction, not a separate cited theorem.

**C3 — planted-block (4, all `FOUND-EXACT`).** `dyadic planted quotient profile`
(CapV13:6010); `planted quotient-core lower count` (CapV13:6060, verbatim);
`planted list budget windows` (CapV13:6207, verbatim); `bounded active quotient
order` (CapV13:6020, verbatim).

**C4 — tangent/deep-center (3, all `FOUND-EXACT`).** `high-agreement tangent exact
cell` (CapV13:5782) + `exact tangent cell` (5794); `split kernel sections are
tangent-borne` (CapV13:8902); Grande refinement `exact high-agreement tangent
cell` (Grande:481).

**C5 — extension/descent (7, all `FOUND-EXACT`).** `extension-pole deep-list floor`
(CapV13:529, verbatim); `extension-pole quotient-remainder floor` (CapV13:574);
`extension-line dimension--degree ledger` (CapV13:2855, verbatim); `subfield
confinement; refines` Cho26b (CapV13:3727); `certifying lines over extensions are
genuinely $\F$-valued` (CapV13:3748, + circle at 4113); Grande side `full-extension
cell target` (Grande:402) and `extension-valued distinct-slope rank-one floor`
(Grande:1546).

**C6 — differential-locator/regular-rank (6, all `FOUND-EXACT`).** `regular
closed-range Hankel packing` (CapV13:2166); `canonical exact-agreement rank-drop
ledger` (CapV13:2240, verbatim); `closed-ball rank-drop lcm` (CapV13:2280); `canonical
curve rank-drop ledger` (CapV13:2383); `exact arbitrary-residual image ledger`
(CapV13:3194); `scanner-checkable residual aperiodic ledger` (CapV13:2912).

**C7 — saturation/effective-image-collapse (4, all `FOUND-EXACT`).** Grande:
`exact saturation identity` (Grande:1811, verbatim) and `line-ray saturation
identity` (Grande:1867, verbatim). CapV13: `exact arbitrary-residual image ledger`
(3194) and `closed-ball residual exact image after paid-branch removal` (3231).

**C8 — balanced-core/split-pencil (11, all `FOUND-EXACT`).** Grande: `interpolation-lattice
split-pencil reduction` (1336), `near-rational lattice dichotomy` (1350),
`deficiency-one split-test eliminant` (1393, verbatim), `split annihilator dictionary`
(1414, verbatim), `split charts are tangent-borne` (1452), `the boundary profile is
Q` (1475), `interior base-field split-pencil floor` (1494), `moving-root bound for
one-parameter split pencils` (1735), `BC is settled on primitive one-parameter
locator pencils` (1764). CapV13 companion: the section `Rank-one and split-pencil
reduction of the safe side` (7627) with `near-rational dichotomy` (7916) and
`Split-pencil form of the balanced core` (8401).

**C9 — Fourier/Sidon (5: 2 `FOUND-EXACT`, 3 `PHANTOM`).** Grande, both exact:
`Fourier-flat leaves satisfy asymptotic Q` (`thm:fourier-flat-q`, Grande:916) and
`large-characteristic Fourier examples` (Grande:949, verbatim). Moduli, all
`PHANTOM` (source absent, §2): the Sidon/Fourier operational cut; the Sidon-heavy
vs high-energy split; the major-arc→algebraic-cell / minor-arc→Fourier-flat
routing.

## 4. The four definitional joints `AUDIT`

### B1 — normalization: `FOUND-WEAKER`

The paper's leaf (`def:primitive-leaf`, L149–L158) normalizes by the **actual
image**: `\Scal = im Φ`, `L = |\Scal|`, `\barN = M/L` (L157), and `\Gord_q =
L^{-1} Σ_{s∈\Scal}(|F_s|/\barN)^q` (L162). The cited "Fourier-flat Q section" of
Grande proves its bound in the **ambient** normalization instead:
`thm:fourier-flat-q` (Grande:916–922) concludes

> `max_ξ |{M : Ψ(M)=ξ}| ≤ exp(o(N)) · Q^{-w} \binom Nm`,

i.e. the max fiber is compared to `Q^{-w}\binom Nm` — the random-model mean over
the *full box* `E^w`, not over `im Ψ`. Grande's companion objects agree with the
ambient reading: `prob:entropy-inverse-q` (Grande:827) normalizes by `|K|^R`, and
`def:primitive-logmoment` (Grande:756) by `|B|^{-w}` (the prefix box), never by
`|im Φ|`.

So the cited section proves Q at the **ambient (Q^w = q^R-type) scale**, whereas
the paper's `\Gord` machinery runs at the **image scale** `L = |im Φ|`. The two
agree iff `|im Φ| = |K|^R · exp(o(N))` in-window (the image nearly fills the
ambient box). **Missing lemma:** that equality is not printed — equivalently, a
printed bridge that `log(M/L)` and `log(M/|K|^R)` differ by `o(N)` uniformly in
the frontier window. The integrated fp-span note
(`cap25_v13_entropy_inverse_fp_span_cell.md` §3, L346) independently flags this as
a wellformedness tension: with `R ≍ N` and `T ⊆ K`,
`log|Ω°| − R log|K| ≤ N log 3 − κN log N = −Θ(N log N) ≠ o(N)`, so the ambient
frontier normalization printed in `prob:entropy-inverse-q` is unreachable except
under the note's "two-field reading" (columns over a growing point field, byte-size
`O(1)` base field). The bridge B1 asks for is exactly that two-field reconciliation,
made explicit. `FOUND-WEAKER`.

### B2 — cells vs removal list: `STRUCTURAL` (consistent, no orphan)

Grande's `prob:entropy-inverse-q` carries the removal list at L839:

> the primitive residual model after **quotient pullbacks, Chebyshev/dihedral
> pullbacks, planted common blocks, tangent cells, extension cells,
> differential-locator low-defect cells, and saturation cells** have been removed.

These seven map cleanly onto **C1, C2, C3, C4, C5, C6, C7** respectively — no
L839 removal item lacks a C-cell home. The two paper cells with **no L839
antecedent** are the genuinely new top-level cells:

- **C8** (balanced-core / split-pencil) is *not* in the L839 list, but *is* in
  the companion residual-leaf list `def:frontier-mca-sequence` (Grande:2232:
  "quotient, planted, tangent, extension, Chebyshev, differential-locator,
  saturation, and **split-pencil** paid cells"). So C8 is a renamed promotion of
  an already-recognized Grande cell.
- **C9** (Fourier/Sidon) is absent from **both** Grande removal lists. It is the
  moduli-manuscript cell of §2 — new at the top level and sourced only to the
  absent notes.

### B3 — window uniformity: `FOUND-WEAKER`

`thm:frontier` (L135–L142) *assumes* "the closed paid ledger holds **uniformly in
every `o(n)`-window** around the crossing." The individual cited ledgers do not
prove this: `thm:capf-census`, `thm:capf-planted`, `def:primitive-logmoment`, and
the rest are stated at a **fixed** agreement `m = k+1+w` (fixed prefix depth `w`),
not uniformly over a moving `o(n)`-window. The honest reading is that
window-uniformity is a *hypothesis*, not a discharged lemma — and the paper is
faithful to Grande here: Grande's own closure theorem
`thm:asymptotic-rs-mca-closure-combined` (2297) makes the same move, concluding
the threshold identity only "**if** the same hypotheses hold uniformly for
agreements `a_n = K_n + g_n n + o(n)`" (Grande:2302). So the assumption is
imported consistently, but neither manuscript discharges it. **Missing lemma:** a
window-uniform restatement of the per-cell budgets (or an explicit note that the
uniformity assumption is imported verbatim from Grande, where it is equally a
hypothesis). `FOUND-WEAKER`.

### B4 — lower side: `FOUND-WEAKER`

The identity-prefix pole construction (L276–L287) is `FOUND-EXACT` as a
construction: it is verbatim Grande `prop:pole-line` (583) — same `f_α, g_α`, same
`ℓ_S(α) = U_z(α) − ζ` explanation condition. But the paper's justification of the
lower bound —

> Except for the usual collision loss in evaluating `ℓ_S(α)`, which is
> subexponential in **the standard pole-reservoir regime** —

is weaker than printed. The phrase "pole-reservoir regime" appears in **no**
source. `prop:pole-line` itself only *flags* the loss ("up to collisions in the
displayed evaluation map", Grande:599) and does not bound it. Grande's quantitative
floor `thm:simple-pole-list-floor` (243) *does* bound a collision loss via the
reservoir `F∖D` — but among `L` **list codewords** (`P_i − P_j` has ≤ k roots),
not among the `~\binom nm |B|^{-w}` **supports** `S ↦ ℓ_S(α) = ∏(α−t)` the paper
needs. Meanwhile v13-raw `lem:capff1-identity-prefix-floor` (6909) reaches the
*same* numerator `⌈\binom nm / |B|^w⌉` through a **collision-free injective** map
(`c_M = U_{z*} − Λ_M`, injectivity proved at L6936), then converts to MCA by
deep-point conversion. So the sound lower bound exists, but through a *different,
injective* construction than the pole map the paper credits. **Missing lemma:** a
printed subexponential bound on the fibers of `S ↦ ℓ_S(α)` at the frontier scale,
**or** a citation redirect to the injective identity-prefix floor + deep-point
conversion as the actual origin of the `exp(−o(n))` lower bound. `FOUND-WEAKER`.

## 5. External tools (C) `AUDIT`

Both are literature citations; the audit checks only that the *stated form*
matches the standard statement and that the boolean application is valid logic.

- **BSG** (`thm:bsg`, L214): energy form — `E(A) ≥ |A|^3/K` yields `A'⊆A` with
  `|A'| ≥ K^{-C}|A|`, `|A'−A'| ≤ K^C|A'|`, `C` absolute. This is the standard
  Balog–Szemerédi–Gowers energy statement. `MATCHES-STANDARD` (not re-proved).
- **Quasicube** (L218): MRSZ2020 / GMRSZ2020 — for `U ⊆ {0,1}^d`,
  `|P+Q+U| ≥ |P|^{1/2}|Q|^{1/2}|U|` for finite nonempty `P,Q ⊆ ℤ^d`.
  `MATCHES-STANDARD` (not re-proved).
- **Quasicube application** (`thm:quasicube` proof, L225): "Apply the quasicube
  theorem with `U=A`, `P=−A`, `Q={0}`." Verified here as pure logic: `|P| = |A|`,
  `|Q| = 1`, `|U| = |A|`; `P+Q+U = A−A`; so
  `|A−A| ≥ |A|^{1/2}·1^{1/2}·|A| = |A|^{3/2}`. The hypotheses `U ⊆ {0,1}^N` and
  `P,Q ⊆ ℤ^N` finite nonempty are all met. `VALID` (checked in the verifier at
  several `|A|` and with the concrete witness `A={0,1}`, `|A−A|=3 ≥ 2^{3/2}`).

The paper's §3–§4 (`Sidon cut`, `energy extraction`, `no large high-energy
boolean fiber`, `primitive Q`) chain these two tools in-paper; that half of C9 is
therefore not phantom — only the *arc-routing* that feeds `def:sidon-paid` is
(§2).

## 6. Promotion-readiness table (D) `AUDIT`

The maintainer asked for the table; the decision remains his. `NEEDS-X` names the
smallest addition that would move the row to `CLEAN`.

| unit | verdict | what it needs |
|---|---|---|
| C1 | `CLEAN` | — |
| C2 | `CLEAN` | (optional: a one-line dihedral→quotient reduction label) |
| C3 | `CLEAN` | — |
| C4 | `CLEAN` | — |
| C5 | `CLEAN` | — |
| C6 | `CLEAN` | — |
| C7 | `CLEAN` | — |
| C8 | `CLEAN` | — |
| C9 | `BLOCKED-BY-MISSING-SOURCE` | the two moduli manuscripts in-tree, **or** an in-paper proof of the major-arc→algebraic-cell routing that pays `def:sidon-paid` |
| B1 | `NEEDS-X` | a printed image=ambient(`q^R`) bridge: `\|im Φ\| = \|K\|^R·exp(o(N))` in-window (the fp-span §3 two-field reconciliation, stated) |
| B2 | `CLEAN` | — (C8/C9 correctly presented as new top-level cells) |
| B3 | `NEEDS-X` | a window-uniform restatement of the per-cell budgets, or an explicit "imported as a hypothesis from Grande" note |
| B4 | `NEEDS-X` | a printed pole-map collision-loss bound at frontier scale, or a citation redirect to `lem:capff1-identity-prefix-floor` + deep-point conversion |

**Single most promotion-relevant finding.** C9's load-bearing payment — the
routing that closes the Fourier/Sidon cell, on which `prop:energy-extract` and
`thm:primitive-q` depend — is cited to two manuscripts absent from the repository
(`Cho26ModuliSelf`, `Cho26ModuliFinal`), so it cannot be verified in-tree. The
maintainer's own log entry expects the package "accepted from ... the
moduli-ledger notes"; those notes are the missing piece. Everything else (C1–C8,
verbatim) is citation-clean; the three joints are `FOUND-WEAKER` in named,
local, repairable ways.

## 7. Nonclaims `AUDIT`

- Internal correctness of any cited proof was **not** re-verified. A
  `FOUND-EXACT` verdict means a labeled result exists whose *statement* covers the
  claimed payment at the claimed strength — not that its proof was checked.
- The BSG and quasicube theorems were **not** re-proved; only their stated forms
  were matched to standard statements. The boolean-difference *application* was
  verified as pure logic.
- `PHANTOM` for the C9 moduli citations records only that the cited source files
  are **absent from this tree**. It is not a claim that the results are false or
  unprovable, nor that supplying the manuscripts would (or would not) close C9.
- The four-way tally counts *citation resolutions*, not theorems. B2 is a
  structural mapping and is excluded from the four-way count.
- This note does not promote or merge anything. Per house style it lives under
  `experimental/notes/` labelled `AUDIT`; the promotion/merge decision is the
  maintainer's, and this table is input to it.
