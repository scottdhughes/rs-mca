# Asymptotic RS-MCA in-paper proof audit (round 2) — 8 `NO ISSUE` / 2 `OPEN GAP` / 0 `FIXED` / 0 `COUNTEREXAMPLE_NEW_FLOOR`

Status: `AUDIT` (adversarial line-by-line attack on the ten in-paper proofs of
`experimental/asymptotic_rs_mca.tex`, at base `eb42b82`) / `NO ISSUE` (§A1, A2,
A3, A4, A5, A7, A8, A10 — eight printed steps survive a genuine attempt to break
them) / `OPEN GAP` (§A6 `lem:addback` uncited profile decomposition; §A9 the
pole-construction collision caveat). No `FIXED`, no `COUNTEREXAMPLE_NEW_FLOOR`.

**Verifier.** `experimental/scripts/verify_asymptotic_proof_audit_r2.py`
(zero-arg, stdlib-only, knobs `PAUD_AS_CAP_GB` / `PAUD_DATA_DIR`) — `RESULT:
PASS`: 28 located quotes byte-match within ±5 lines of their stated source line;
the four-way verdict tally (8/0/2/0) is self-consistent and every attack verdict
uses the mandated vocabulary; and six numeric checks recompute independently —
the A1 first-match toy, the A2 moment-max inequalities+squeeze, the A3 σ
block-diagonal, the A4 BSG+quasicube contradiction, the A9 pole-line polynomial
division over `F_p`, and the A10 Stirling / `g*(ρ,β)` crossing table — plus 9
tamper self-tests (corrupted quote, wrong line, mangled total, bad verdict
vocabulary, missing source, wrong `g*`, broken toy count, wrong pole-line `ζ*`,
unnamed OPEN GAP) all rejected. Machine-readable map:
`experimental/data/asymptotic_rs_mca_proof_audit_r2.json`.

**What this is.** An adversarial audit of the proofs
`experimental/asymptotic_rs_mca.tex` prints *itself*: `lem:first-match` (L81),
`lem:moment-max` (L165), `prop:energy-extract` (L202),
`thm:quasicube`+`prop:no-high-energy` (L220/L228), `thm:primitive-q` (L236),
`lem:addback` (L246), `lem:q-sp` (L254), `thm:upper` (L262), the identity-prefix
pole construction (L276), and `thm:frontier` (L289). Each is attacked with a
mandated verdict `NO ISSUE` / `FIXED` / `OPEN GAP` / `COUNTEREXAMPLE_NEW_FLOOR`
and exact file+line references; every numeric assertion is gated.

**What this is not.** NOT a re-proof of the imported closed-ledger package, of
Balog–Szemerédi–Gowers, or of the quasicube theorem — their internal correctness
is out of scope. NOT the citation audit: that is the complement packet **#433**
(`thresholds-asymptotic-ledger-audit`,
`experimental/notes/asymptotic_rs_mca_closed_ledger_audit.md`), which resolved
the `(C1)–(C9)` bracket-citations of `thm:closed-ledger-package` and the four
definitional joints. This packet offers **no promotion verdict**; the
promotion/merge decision is the maintainer's.

**Motivation and weave.** #433 closed its steering-alignment table by recording,
verbatim, that two of the steering's seven assigned failure modes were **not
attacked** there: *"'incorrect first-match disjointization' and
'entropy-frontier algebra error' were **not attacked here** (out of
citation-audit scope; natural follow-up packets)."* This packet is exactly those
two follow-ups — `lem:first-match` (§A1) and `thm:frontier` (§A10) — together
with the whole remaining in-paper proof chain. The steering (`agents.md`,
`eb42b82`, "Update agent priorities for asymptotic RS MCA proof") makes
adversarial proof audits priority 2 with the four-way vocabulary and exact
file/label references; this is that audit class for the paper's own proofs. Two
of the ten attacks land as `OPEN GAP`, and both connect to #433's `FOUND-WEAKER`
joints: §A6 extends B3 (a Grande hypothesis imported as if discharged) and §A9
is the in-paper reflection of B4 (the pole-map collision loss).

---

## 1. Headline `AUDIT`

| attack | target (label / line) | steering mode | verdict |
|---|---|---|---|
| A1 | `lem:first-match` L81–87 | incorrect first-match disjointization | `NO ISSUE` |
| A2 | `lem:moment-max` L165–178 | moment-to-max equivalence | `NO ISSUE` |
| A3 | `prop:energy-extract` L202–208 | unsupported Fourier/Sidon payment (σ-diagonal) | `NO ISSUE` |
| A4 | `thm:quasicube`+`prop:no-high-energy` L220–234 | misuse of BSG / quasicube | `NO ISSUE` |
| A5 | `thm:primitive-q` L236–242 | primitive-Q assembly | `NO ISSUE` |
| A6 | `lem:addback` L246–252 | compiler add-back (uncited decomposition) | **`OPEN GAP`** |
| A7 | `lem:q-sp` L254–260 | Q-to-SP inequality | `NO ISSUE` |
| A8 | `thm:upper` L262–272 | wrong field denominator / ledger | `NO ISSUE` |
| A9 | pole construction L276–287 | lower-side algebra + collision loss | **`OPEN GAP`** |
| A10 | `thm:frontier` proof L289–296 | entropy-frontier algebra error | `NO ISSUE` |

One-line reading: the paper's own analytic spine — moment-to-max, the Sidon cut,
the BSG+quasicube Boolean-fiber kill, the Q→SP bound, and the entropy-frontier
algebra — is **sound**. The two gaps are both *compiler/glue* steps that import a
Grande hypothesis as if it were a discharged theorem: the primitive→global
add-back (A6) and the lower-side collision loss (A9). Neither is a
counterexample; both are named, local, and repairable by redirect.

## 1b. Steering alignment — mandated vocabulary (`eb42b82`) `REFERENCE`

| mandated verdict | count | attacks |
|---|---:|---|
| `NO ISSUE` | 8 | A1, A2, A3, A4, A5, A7, A8, A10 |
| `OPEN GAP` | 2 | A6, A9 |
| `FIXED` | 0 | — |
| `COUNTEREXAMPLE_NEW_FLOOR` | 0 | — |

Against the steering's seven assigned modes: *incorrect first-match
disjointization* → `NO ISSUE` (A1); *entropy-frontier algebra error* → `NO ISSUE`
(A10); *misuse of BSG or quasicube growth* → `NO ISSUE` (A4); *unsupported
Fourier/Sidon payment* → `NO ISSUE` with a named repair (A3); *wrong field
denominator or base/extension-field ledger* → `NO ISSUE` (A8, `q_line` kept out
of the numerator); *missing cell in the bad-line classification* → out of scope
here (that is #433's B2, `NO ISSUE` there); *mismatch between asymptotic proof
and finite deployed rows* → touches A9 (the collision caveat is the asymptotic
side of the finite constants the closing Remark scopes out).

## 2. The eight `NO ISSUE` steps `AUDIT`

### A1 — `lem:first-match` disjointization: `NO ISSUE`

The lemma (L82) claims covered slopes contribute at most `Σ_j U_j`. Under
`def:cells` (L77–79) the budget `U_j` is *by definition* the number of slopes
whose **least-indexed** witness cell is `C_j`. The proof (L86) *"assign each bad
slope to the least-indexed cell containing a witness ... the j-th class is
contained in the projection of `C_j` after earlier cells have been removed"* is
airtight: first-match sends every covered slope to a unique cell, so the classes
**partition** the covered slopes and `Σ_j U_j` equals the total **exactly** — no
per-cell double count. The classic failure (a slope with witnesses in several
cells, budget counted per cell) is *avoided* precisely because the lemma sums
first-match budgets, not raw projection budgets; summing raw projections would
only over-count (still a valid upper bound, just loose). Verified on a 3-cell toy
with overlapping witnesses `g1∈{C1}`, `g2∈{C1,C2}`, `g3∈{C2,C3}`, `g4∈{C3}`,
`g5∈{C1,C2,C3}`: first-match budgets `(3,1,1)` sum to `5` = total, while raw
projection budgets `(3,3,3)` sum to `9`; and `projection(C_j) \ earlier` equals
the first-match class for every `j`. Whether the *imported* budgets are genuine
first-match budgets under the paper's cell order is #433 B2 (found structurally
consistent).

### A2 — `lem:moment-max` equivalence: `NO ISSUE`

Both inequalities `L^{-1} R^q ≤ Γ_q ≤ R^q` (with `R = max_s |F_s|/N̄`) are elementary:
the upper bound replaces every summand by the maximum (`L` terms × `L⁻¹`), the
lower bound keeps one maximal summand. The q-th-root squeeze gives
`R·L^{-1/q} ≤ Γ_q^{1/q} ≤ R`, so `(1/q)log Γ_q` and `log R` differ by `≤
(1/q)log L`. The hypothesis `log L = o(Nq)` is **automatic** for any `q→∞`:
`L = |im Φ| ≤ M ≤ 2^N`, so `log L = O(N)` and `log L/(Nq) = O(1/q) → 0`. Hence
the `L⁻¹` factor is subexponential-in-`N` after the root and the stated
equivalence holds. Sanity: `Γ_1 ≡ 1` identically (verified on four profiles at
`q ∈ {1,2,5,10,25,40}`).

### A3 — `prop:energy-extract` σ-diagonal: `NO ISSUE` (with a named repair)

This is the subtlest step, and the one the steering's brief flagged as the likely
gap. The conclusion is **correct** and the σ-diagonalization **is constructible**
from the stated per-σ hypotheses. `def:sidon-paid` (L197) gives, for *every fixed*
`σ>0`, a null rate `ε_σ(N)/N → 0`. There is a genuine **non-uniformity**: as
`σ↓0` the Sidon-heavy set `{Δ(F_s) ≤ e^{-σN}}` grows toward *all* levels
(`Δ ≤ 1` always), so `Γ^sid_{q,σ} ↑ Γ^ord_q ≥ e^{ηNq}`, and therefore
`sup_σ ε_σ(N)/N` does **not** → 0. The paper's one-liner *"Letting σ↓0 slowly
along the sequence"* elides the fix, which is a standard **block-diagonal**: put
`σ_N = 1/k` on `N`-blocks `[N_k, N_{k+1})`, choosing `N_k` so that
`ε_{1/k}(N)/N ≤ 1/k` for `N ≥ N_k` (exists by the per-σ null rate). Then
*simultaneously* `ε_{σ_N}(N)/N → 0` (`Γ^sid` stays subexponential at the moving
`σ_N`) **and** `σ_N → 0` (so `σ_N·N = o(N)` and `e^{-σ_N N} = e^{-o(N)}`).
Crucially the `|F_s| ≥ e^{ηN-o(N)}N̄` bound is **σ-independent** (its `o(N)` is
`(log 2)/q`), so only the `Δ(F_s) > e^{-σN}` half needs the diagonal. **No
uniformity in σ is required** for the asymptotic `o(N)` conclusion. Verified: on
an adversarially non-uniform `a(σ,N)=C/(σ√N)` (per-σ null, blows up as `σ↓0`),
the block `σ_N = 1/k` keeps `a(σ_N,N) ≤ 1/k → 0` while `σ_N → 0` at five scales
up to `N = 10¹¹`. **Expository defect only:** a formalizer *must* supply the
block-diagonal; it is not automatic from a naïve reading of `def:sidon-paid`.

### A4 — BSG(`K=e^{o(N)}`) + quasicube: `NO ISSUE`

`thm:quasicube` (L221) is correct: with `U=A ⊆ {0,1}^N`, `P=-A`, `Q={0}`, one has
`P+Q+U = A-A` and `|A-A| ≥ |A|^{1/2}·1^{1/2}·|A| = |A|^{3/2}`. The energy-form BSG
bookkeeping (L233) survives the `o(N)` exponent: `C` absolute ⇒ `K^{±C} =
e^{±o(N)}`, so the `K^{-C}` loss keeps `|F'| ≥ e^{cN-o(N)}` (the linear `e^{cN}`
dominates the `o(N)` loss) and the `K^{+C}` inflation gives `|F'-F'| ≤
e^{o(N)}|F'|`. Quasicube then forces `|F'|^{3/2} ≤ e^{o(N)}|F'|`, i.e.
`|F'|^{1/2} ≤ e^{o(N)}` ⇒ `log|F'| ≤ o(N)`, contradicting `|F'| ≥ e^{cN-o(N)}`
for fixed `c>0` (`cN ≤ o(N)` is impossible). Ambient group is `Z^N` throughout;
BSG's subset `F' ⊆ F_N ⊆ {0,1}^N` stays in the Boolean cube, so quasicube still
applies. Verified numerically at `N ∈ {10⁸,10¹⁰,10¹²}` with `o(N)=√N·log N`: the
quasicube lower bound on `|F'-F'|` strictly exceeds the BSG upper bound.

### A5 — `thm:primitive-q` assembly: `NO ISSUE`

The chain is valid. Negation of *"max|F_s| ≤ exp(o(N))N̄"* is *"max|F_s| ≥
e^{ηN}N̄ for fixed η>0 along a subsequence"*; `lem:moment-max` upgrades this to
`Γ_q ≥ L⁻¹e^{ηNq} = e^{(η-o(1))Nq}` (using `log L = o(Nq)`); `prop:energy-extract`
extracts a fiber with `|F_s| ≥ e^{ηN-o(N)}N̄ = e^{cN-o(N)}` — the step *"because
log N̄ = o(N)"* (the frontier condition, `def:primitive-leaf` L157) is used
exactly here — and `E(F_s) ≥ |F_s|³e^{-o(N)}`, with `F_s ⊆ {0,1}^T`, `|T|=N`;
`prop:no-high-energy` is contradicted. A subsequence is legitimately a sequence
for `prop:no-high-energy`, and the "logarithmic q" is exactly the quantifier of
`def:sidon-paid`, so `prop:energy-extract`'s hypothesis is met. Notably the
paper's in-paper §3–§4 route (Sidon cut → BSG → quasicube) **discharges** what
Grande's `thm:primitive-q-closure-module` left conditional on the (still-open)
`prob:entropy-inverse-q`; the paper's primitive-Q half is therefore genuinely
stronger than the cited route, not circular.

### A7 — `lem:q-sp`: `NO ISSUE`

Elementary and correct: `Σ_s N(s)² ≤ (max_s N(s))·Σ_s N(s)` termwise, and with
`max N(s) ≤ κN̄`, `Σ N(s) = M` this gives `M⁻¹ Σ N(s)² ≤ κN̄`. (Not
Cauchy–Schwarz, but the correct `Σx² ≤ (max x)(Σx)`.) Matches Grande
`prop:q-sp-frontier-closure` verbatim. Verified on three profiles.

### A8 — `thm:upper` bookkeeping: `NO ISSUE`

Dimensionally consistent. The displayed bound `exp(o(n))·binom(n,a_n)·|B_n|^{-(a_n
- k_n - 1)}` is exactly `exp(o(n))N̄_{n,a_n}` because `w_n = a_n - k_n - 1`
(def L67–69), and it matches the lower construction's scale
`exp(-o(n))binom(n,m)|B|^{-w}` (L285) — the two-sided match is what makes the
frontier *sharp*. `q_line` is correctly kept **out** of this numerator bound: the
`ε_mca = B^MCA / q_line` normalization (L65) is deferred to `thm:frontier`, so the
field-ledger separation the steering mandates is respected. The assembly (paid
cells by closure + primitive by `thm:primitive-q`/`lem:addback` + SP by
`lem:q-sp` + first-match disjointization) is logically valid. **Caveat:**
`thm:upper` inherits the A6 gap — it is only as sound as the uncited
subexponential-profile decomposition inside `lem:addback`.

### A10 — `thm:frontier` entropy algebra: `NO ISSUE`

The Stirling identity (L292–293) `log₂ N̄_{n,a_n} = n(H₂(ρ+g) - βg) + o(n)` is
**exact**. Derivation: `log₂ binom(n,a_n) = n H₂(ρ+g) + o(n)` (since `a_n/n →
ρ+g` and `H₂` is Lipschitz on compacta, `n·H₂(a_n/n) = n H₂(ρ+g) + o(n)`); and
`-w_n β_n = -βg n + o(n)` with `w_n = a_n - k_n - 1 = gn + o(n)`. The rate
`φ(g) = H₂(ρ+g) - βg` is **concave** (`H₂` concave, `βg` linear) with
`φ(0) = H₂(ρ) > 0` and `φ(1-ρ) = -β(1-ρ) ≤ 0`, so it has a single crossing at
`g* = sup{g : φ(g) ≥ 0}` and the superlevel set is `[0, g*]`. Hence the two
branch signs are correct: `g > g* ⇒ φ < 0` (safe, `B^MCA ≤ exp(o(n))N̄ =
2^{-Ω(n)}`) and `g < g* ⇒ φ > 0` (unsafe, exponentially many bad slopes). The
`g → g*` two-sided limit gives `δ* = 1 - ρ - g*`. Verified: `g*` by bisection at
seven `(ρ,β)` pairs (`φ(g*) ~ 0` to `1e-6`, single crossing confirmed above and
below), and `(1/n)log₂ N̄ → φ(g)` as `n` grows to `10⁶`. The `β=0` boundary case
(`g* = 1-ρ`, `δ* = 0`) is included. The `g < g*` branch inherits the A9
lower-construction collision gap.

## 3. The two `OPEN GAP`s `AUDIT`

### A6 — `lem:addback` uncited profile decomposition: `OPEN GAP`

`lem:addback` (L246–252) upgrades per-leaf primitive Q (`thm:primitive-q`, a
bound *relative to each leaf's own scale N̄ = M/L*) to the **global** max-count
bound `max_s N(s) ≤ exp(o(n))N̄_{n,a_n}`. Its proof (L251) invokes two objects
**with no citation and no in-paper definition**: *"their normalized averages sum
to at most exp(o(n))N̄ **by the first-match profile decomposition**"* and
*"Summing over the **subexponential profile family** preserves the same scale."*

These correspond to Grande's `lem:subexponential-addback-closure`
(`grande_finale.tex:2266`), whose proof text the paper paraphrases. **But that
Grande lemma is itself conditional**: it reads *"**Suppose that**, in every
first-match leaf, the number of paid quotient/profile cells is `exp(o(n))`, each
paid cell contributes at most `exp(o(n))N̄_n` supports to any prefix syndrome,
..."* and its proof merely multiplies the *assumed* subexponential factors.
Grande's combined closure theorem `thm:asymptotic-rs-mca-closure-combined`
(`grande_finale.tex:2298`) again **supposes** these add-back hypotheses, and its
`rem:not-no-input-proof` states the equality *"remains conditional."* So the paper
presents as a **proved** lemma (complete with its own `\begin{proof}`) what the
source imports as a **hypothesis**. This is the same import-as-hypothesis pattern
#433 flagged for window-uniformity (B3), now for the add-back decomposition.

**Missing statement.** A proof (not an assumption) that the global first-match
prefix count `N(s)` decomposes into a family of primitive-leaf profiles such that
(i) the number of profiles / paid cells is `exp(o(n))` — the "subexponential
profile family" — and (ii) each contributes at the *global* scale `N̄_{n,a_n}`,
so that the per-leaf `thm:primitive-q` bound sums to `max_s N(s) ≤
exp(o(n))N̄_{n,a_n}`. **Repair:** either discharge the decomposition (bound the
number of first-match profiles by `exp(o(n))` and each at scale `N̄`), or restate
`lem:addback` as `CONDITIONAL` on the Grande add-back hypotheses, cited to
`lem:subexponential-addback-closure`.

### A9 — pole-construction collision caveat: `OPEN GAP` (algebra `NO ISSUE`)

The identity-prefix pole construction (L276–287) splits into two parts.

**(algebra — `NO ISSUE`.)** The pole-line identity *"f_α + ζ g_α is code-explained
on S exactly when ℓ_S(α) = U_z(α) - ζ"* (L283) is verified by polynomial
division. On `D`, `f_α + ζ g_α = (U_z(x) - ζ)/(x - α)`; setting `P(X) =
(X-α)(Q(X) - h(X)) + ρ` with `ρ = U_z(α) - ζ` forces `P = ℓ_S` (both monic degree
`m`, vanishing on `S`), and evaluating at `α` gives `ρ = ℓ_S(α)`, i.e. the stated
condition. The explaining polynomial
`h = (U_z - ℓ_S - (U_z(α) - ℓ_S(α)))/(X - α)` has degree `≤ k-1 < k` **because
`z` is the shared locator prefix**: `U_z` and `ℓ_S` share their top `w+1`
coefficients, so `deg(U_z - ℓ_S) ≤ m - w - 1 = k`, dropping to `≤ k-1` after
dividing by `(X-α)`. And `g_α = -1/(x-α)` is genuinely **not** degree-`<k` on any
`k+1` positions ((`(X-α)h + 1` would be a degree-`≤k` polynomial with `k+1`
roots). All three confirmed numerically over `F_p` (`p ∈ {97,101}`, three
instances, `ζ*` and `deg h` matched, and the "exactly when" verified by scanning
all `ζ ∈ F_p`).

**(collision loss — `OPEN GAP`.)** The lower bound
`B^MCA(m) ≥ exp(-o(n))binom(n,m)|B|^{-w}` (L285) requires the fibers of the
support-product map `S ↦ ℓ_S(α) = ∏_{t∈S}(α - t)` to be subexponential (distinct
supports must give mostly-distinct bad slopes `ζ_S = U_z(α) - ℓ_S(α)`). The paper
asserts this loss is *"subexponential in the standard pole-reservoir regime"* with
**no proof and no citation** — and the phrase "pole-reservoir regime" appears in
**no source file** (grep-confirmed by the verifier's absence in the sources; it
is unique to `asymptotic_rs_mca.tex:283`). This is the in-paper reflection of
**#433 B4** (`FOUND-WEAKER`): Grande `prop:pole-line` (`grande_finale.tex:583`)
only *flags* the collision loss without bounding it, and the sound lower bound in
fact comes from a **different, collision-free injective** construction —
`cap25_cap_v13_raw.tex` `lem:capff1-identity-prefix-floor` (L6909) and the
`c_M = U_{z*} - Λ_M` injective maps (L5119, L5260).

**Missing statement.** A printed subexponential bound on the fibers of
`S ↦ ∏_{t∈S}(α - t)` at frontier scale `binom(n,m)|B|^{-w}`. **Repair:** redirect
the lower bound to the collision-free injective identity-prefix floor
(`lem:capff1-identity-prefix-floor`) + deep-point conversion, which reaches the
same numerator injectively — the fix #433 B4 already recommended, confirmed here
from the proof side.

## 4. Relation to #433 `REFERENCE`

This packet is the strict complement of #433. #433 audited the *citation* layer
(does a labeled source result exist covering each `(C1)–(C9)` payment?) and found
`48 FOUND-EXACT / 3 FOUND-WEAKER / 3 PHANTOM`, with C9's moduli manuscripts
absent as the single promotion-blocker. This packet audits the *in-paper proofs*
and finds the analytic spine sound with two glue-layer gaps. The two audits
reinforce each other at the joints: A6 extends B3 (both: a Grande hypothesis
imported as if discharged), and A9 is the proof-side confirmation of B4 (the
pole-map collision loss; the injective floor is the real source). Neither packet
promotes or blocks; both are input to the maintainer's decision. Note that the
paper's own §3–§4 (Sidon/BSG/quasicube) is *stronger* than the Grande route it
partially replaces — it discharges primitive Q unconditionally (A5), where Grande
left it conditional on `prob:entropy-inverse-q`.

## 5. Nonclaims `AUDIT`

- A `NO ISSUE` verdict means the printed step survived a genuine attempt to break
  it under the paper's stated hypotheses; it is **not** a claim that the imported
  results feeding the step are themselves correct (that is #433 / the source
  manuscripts). A3 in particular is `NO ISSUE` on the *claim* with an explicit
  note that the printed *justification* is a one-liner needing the block-diagonal.
- The BSG and quasicube theorems were **not** re-proved (only their stated forms
  and the Boolean application checked); the imported closed-ledger package was
  **not** re-verified.
- The two `OPEN GAP`s record that a step is **stated-as-proved but actually
  conditional / unproven in-paper**; neither is a claim that the missing statement
  is false, and both are repairable by the named redirects. No
  `COUNTEREXAMPLE_NEW_FLOOR` was found — these are sound-or-conditional steps, not
  refutable ones.
- The numeric checks are **illustrative instantiations** (small toys, `F_p`
  division, entropy tables), not proofs of the asymptotic statements; they gate
  the specific arithmetic each attack relies on.
- This note lives under `experimental/notes/` labelled `AUDIT`; it makes no
  promotion or merge recommendation.
