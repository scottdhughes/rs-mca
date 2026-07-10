# B3 window uniformity of the closed paid ledger — scope and discharge

Status line (mandated vocabulary): **FIXED** for the established cells
(C1–C8: the window slide is discharged by elementary window arithmetic supplied
and verified below) / **OPEN GAP** for the inherited residual (C9 routing and the
primitive-Q atom), where windowing is shown to add *no new* obstruction.

Lineage: this note is the B3 lane of the PR #433 closed-ledger citation audit
(`experimental/notes/asymptotic_rs_mca_closed_ledger_audit.md`, §4 joint B3,
`FOUND-WEAKER`). B3 there reads:

> `thm:frontier` *assumes* "the closed paid ledger holds **uniformly in every
> `o(n)`-window** around the crossing." The individual cited ledgers do not prove
> this: `thm:capf-census`, `thm:capf-planted`, `def:primitive-logmoment`, and the
> rest are stated at a **fixed** agreement `m = k+1+w` … the honest reading is
> that window-uniformity is a *hypothesis*, not a discharged lemma. **Missing
> lemma:** a window-uniform restatement of the per-cell budgets.

This note supplies that missing lemma for the established cells and names exactly
what is left. It is **note-only**: it does not edit
`experimental/asymptotic_rs_mca.tex` (three edit streams #439/#441/#442 already
touch it; see "Interaction with open PRs").

Every claim below carries one of `PROVED` / `LEMMA` / `AUDIT` / `OPEN`.

---

## 0. Objects and notation `AUDIT`

All labels are `\label` names in the source tex.

- Paper: `experimental/asymptotic_rs_mca.tex`. Reference scale
  `\barN_{n,a} = \binom{n}{a}\,|\B|^{-w}`, `w = a-k-1` (paper L67–L70,
  `def:primitive-leaf` L149–L158). Crossing `a_n=(\rho+g^*)n+o(n)`,
  `g^*(\rho,\beta)=\sup\{g\in[0,1-\rho]:H_2(\rho+g)\ge\beta g\}` (paper L73).
  Closure `thm:closed-ledger-package` (L105) → upper bound `thm:upper` (L262) →
  frontier `thm:frontier` (L135). Cells `(C1)–(C9)` in `def:closed-ledger` (L89).
- Grande (`grande_finale.tex`): closure `thm:asymptotic-rs-mca-closure-combined`
  (2297), frontier sequence `def:frontier-mca-sequence` (2215), primitive moment
  `def:primitive-logmoment` (756), moment equivalence `thm:logmoment-equivalence`
  (773), entropic atom `prob:entropy-inverse-q` (827), Fourier-flat
  `thm:fourier-flat-q` (916), moving-root `thm:bc-moving-root` (1735),
  `cor:bc-one-pencil` (1764), pole line `prop:pole-line` (583).
- v13 raw (`cap25_cap_v13_raw.tex`): census `thm:capf-census` (5970) +
  `lem:capf-census-identity` (5953); planted `thm:capf-planted` (6060),
  `prop:capf-dyadic-planted` (6175), profile `def:capf-qprofile` (6010),
  `prop:capf-qprofile` (6020); quotient safe-sum `def:capf-quotient-status` (5838)
  + `prop:capf-quotient-safe-sum` (5858); tangent `def:capf-tangent-cell` (5782),
  `prop:capf-tangent` (5794); extension `prop:capf-extension` (5866),
  `thm:extension-line-dimension-degree-ledger` (2856); Hankel/rank-drop
  `thm:regular-closed-ball-hankel-packing` (2167).

Where the paper consumes a cell at a **window-varying** agreement: `thm:frontier`
proof (L289–L296) evaluates `thm:upper` at `a_n=(\rho+g)n+o(n)` and then slides
"`o(n)` agreements to absorb the `\exp(o(n))` ledger overhead" (L295). Sliding the
agreement is exactly re-invoking `thm:closed-ledger-package` / `thm:upper` at every
`a` in a window around `a_n`. That is the only place window-uniformity is used, and
it is a **local `o(n)` slide** (the separate `g\to g^*` sweep is handled by
continuity of `H_2`, not by uniformity).

---

## 1. The formal uniformity condition `LEMMA` (definition)

Fix a window half-width `\psi_n = o(n)` and set
`W_n = \{a\in\mathbb Z : |a-a_n|\le\psi_n\}`.

> **Definition (window-uniform closure).** The closed paid ledger holds *uniformly
> on `W_n`* if there is a **single** sequence `\eps_n\to 0` (not depending on
> `a\in W_n`) with, for every `a\in W_n`,
> `B^{\rm MCA}_{C_n}(a) \le \exp(n\eps_n)\,\barN_{n,a}`.   (LC-unif)

The point of B3 is that "`\exp(o(n))`" in the single-agreement closure
`thm:upper` a priori hides an `a`-dependent rate `\eps_n(a)`; (LC-unif) demands one
`\eps_n` for the whole window. Decompose the single-agreement proof of `thm:upper`
(paper L270–L272) cell by cell and require each piece to be window-uniform:

- **(U0) reference coherence.** `\barN_{n,a}=\exp(\pm n\eps^0_n)\,\barN_{n,a_n}`
  for all `a\in W_n`, some `\eps^0_n\to0`. (Pure arithmetic; §2.)
- **(U1) cell-count coherence.** The number of first-match cells/sub-cells is
  `\exp(n\eps^1_n)` uniformly on `W_n`. (Bounded complexity + census; §3, C-count.)
- **(U2) per-cell budget coherence.** For each family `C_j` a rate `\eps^j_n\to0`
  with `U_{C_j}(n,a)\le\exp(n\eps^j_n)\,\barN_{n,a}` for all `a\in W_n`. (§3 table.)
- **(U3) primitive-residual coherence.** `\max_s N^{\rm prim}_a(s)\le
  \exp(n\eps^p_n)\,\barN_{n,a}` uniformly on `W_n`. (§4.)

Finitely many families ⇒ `\eps_n:=\eps^0_n+\eps^1_n+\max_j\eps^j_n+\eps^p_n\to0`
gives (LC-unif). So (LC-unif) ⇔ (U0)∧(U1)∧(U2)∧(U3). What must hold uniformly is
therefore: **the reference scale, the cell count, each per-cell rate function, and
the primitive max-fiber rate** — not any shared multiplicative constant and not
monotonicity of the total (the total need not be monotone; each *piece* only needs
`o(n)` log-variation).

The engine that discharges (U0) and reduces (U2) to a triviality is:

> **Lemma W (window coherence of the reference scale). `PROVED`.**
> Let `a_n/n\to c\in(0,1)`, let `\psi_n=o(n)`, and let `\beta_n=\log_2|\B_n|` be
> bounded (`\beta_n\to\beta<\infty`). Then
> `\sup_{a\in W_n}\bigl|\log_2\barN_{n,a}-\log_2\barN_{n,a_n}\bigr| = o(n).`
>
> *Proof.* Write `\barN_{n,a}=\binom na|\B|^{-(a-k-1)}`, so
> `\log_2\barN_{n,a}-\log_2\barN_{n,a_n} =
> \bigl[\log_2\binom na-\log_2\binom n{a_n}\bigr]-(a-a_n)\beta_n.`
> For the subfield term, `|a-a_n|\le\psi_n` and `\beta_n=O(1)` give
> `|(a-a_n)\beta_n|\le\psi_n\beta_n=o(n)`. For the binomial term, by the Stirling
> bound `\log_2\binom nx=nH_2(x/n)+O(\log n)` uniformly for `1\le x\le n-1`, and by
> the mean value theorem `H_2(a/n)-H_2(a_n/n)=H_2'(\xi)\,(a-a_n)/n` for some `\xi`
> between `a/n` and `a_n/n`. Because `a_n/n\to c\in(0,1)` and `\psi_n=o(n)`, every
> such `\xi` lies in a fixed compact subinterval `[c/2,\,(1+c)/2]\subset(0,1)` for
> large `n`, where `|H_2'|\le C_c<\infty`. Hence
> `|\log_2\binom na-\log_2\binom n{a_n}|\le n\,C_c\,|a-a_n|/n + O(\log n)
> = C_c\,\psi_n+O(\log n)=o(n)`. Summing the two `o(n)` bounds proves the claim. ∎

Lemma W needs `c\in(0,1)` **strictly** (frontier interior) and `\beta_n=O(1)`;
both are guaranteed at the frontier when `\beta>0` (see falsifier F1/F3 in §5 and
gate G5 in §6: `\beta>0\Rightarrow g^*<1-\rho\Rightarrow c=\rho+g^*<1`, and
`c\ge\rho>0`).

> **Lemma B (window coherence of a bounded-complexity budget). `PROVED`.**
> Suppose a cell budget has the form
> `U(n,a)=\sum_{i=1}^{P(n)} \binom{n}{\phi_i(a)}\binom{A_i}{\psi_i(a)}\,\Delta_i\,
> |\B|^{e_i}`, where `P(n)=\exp(o(n))`, the `\Delta_i,e_i` are `a`-independent
> bounded-complexity data, and each internal argument `\phi_i,\psi_i` is an
> integer-valued affine (or piecewise-affine with `\exp(o(n))` pieces) function of
> `a` whose value stays in `[\alpha n,(1-\alpha)n]` for a fixed `\alpha>0`
> throughout `W_n`. Then `\sup_{a\in W_n}|\log_2 U(n,a)-\log_2 U(n,a_n)|=o(n)`.
>
> *Proof.* By the same Stirling+MVT estimate as Lemma W applied to each binomial
> factor (interior argument ⇒ `|H_2'|=O(1)`), each summand has `o(n)`
> log-variation across `W_n`; the `a`-independent factors `\Delta_i|\B|^{e_i}`
> contribute nothing; and a `\log P(n)=o(n)` term absorbs the number of summands.
> A piecewise-affine `\phi_i` adds only `\exp(o(n))` breakpoints, each contributing
> a bounded jump, hence still `o(n)`. ∎

> **Remark (cell activation across the window). `LEMMA`.** Lemma B assumes each
> binomial argument stays in `[\alpha n,(1-\alpha)n]` *throughout* `W_n`, i.e. the
> cell is uniformly active on the window. A cell can instead **activate/deactivate**
> as `a` crosses a fixed threshold (tangent range boundary `3(n-a)=n-k`; quotient
> activation `\sigma<M`): its budget jumps `0\leftrightarrow\mathrm{poly}(n)`, an
> unbounded *log*-jump that Lemma B does not cover. Two facts contain this. (i)
> The thresholds are `O(1)` fixed points (tangent) or `\exp(o(n))`-many
> census-bounded points (quotient); the `o(n)` window straddles at most
> `\exp(o(n))` of them. (ii) At a straddle, the *total* is conserved: by first
> match (`lem:first-match`, paper L81) a slope leaving a deactivating cell is
> reassigned to the next covering cell, so the **total** `B^{\rm MCA}` does not
> jump even though an individual cell budget does. Hence the discharge is applied
> to the **total** `T(n,a)=\sum_jU_{C_j}(n,a)+\mathrm{prim}(n,a)`: on the
> uniformly-active part Lemma B gives `o(n)` log-variation, and the `\exp(o(n))`
> straddle hand-offs are slope-conserving, so `T` inherits `o(n)` log-variation
> across `W_n`. Generic frontier rows (crossing `a_n\ne` any activation threshold)
> straddle *none* for large `n`, and the per-cell reading is already clean.

**Discharge principle (the "missing lemma" of B3). `PROVED`.** If the
single-agreement payment `U_{C_j}(n,a_n)\le\exp(o(n))\barN_{n,a_n}` holds (this is
the *content of single-agreement closure* `thm:closed-ledger-package`, taken as
given here — it is #433's object, not re-proved), **and** `U_{C_j}` satisfies the
hypotheses of Lemma B, then for all `a\in W_n`
`U_{C_j}(n,a)\overset{\text{Lem B}}{\le}\exp(o(n))U_{C_j}(n,a_n)
\le\exp(o(n))\barN_{n,a_n}\overset{\text{Lem W}}{\le}\exp(o(n))\barN_{n,a}`,
which is (U2) for `C_j`. So **window-uniformity of a cell is free whenever its
budget is a bounded-complexity `(n,a)`-formula valid on an `a`-interval** — no new
mathematics beyond the single-agreement payment. The whole B3 question reduces to:
*is each cell's budget such a formula?* §3 checks this cell by cell.

---

## 2. Why "stated at fixed `m`" is inessential `AUDIT`

The B3 finding notes the source theorems are *instantiated* at a fixed
`m=k+1+w`. Inspection shows every one is in fact stated on an **`a`-interval**, and
the instantiation is only where the finite deployed certificate is printed:

- `prop:capf-tangent` (5794) holds for **all** `A` with `3(n-A)\le n-k`
  (an interval), with exact budget `n-A+1`.
- `def:capf-quotient-status` / `prop:capf-quotient-safe-sum` (5838/5858) define
  `U_{\rm sum}(n,A,\mathcal C)` for **all** `A\ge k`.
- `thm:capf-planted` (6060) holds for **all** `\sigma` with `1\le\sigma<M`, with a
  count `\binom{n/M-1}{k/M}` that does not depend on `\sigma` at all.
- `def:primitive-logmoment` (756) and `thm:logmoment-equivalence` (773) are stated
  for general `(n,m,w,r)` with the side condition `w\log|\B|/r=o(n)`.
- `thm:fourier-flat-q` (916) gives `\le\exp(o(N))Q^{-w}\binom Nm` for the general
  leaf `(N,m,w)`.

Thus "fixed `m`" is a presentational artifact of the finite-certificate print-out
(`thm:capf-census` 5970 and `prop:capf-dyadic-planted` 6175 are `2^{128}` scale
tables — finite-row objects, **not** the asymptotic budget). The asymptotic budget
formulas are interval-valued, so Lemma B applies. `AUDIT`

---

## 3. Per-cell table `AUDIT`

Verdicts: **UNIFORM-BY-INSPECTION** (budget an explicit continuous/monotone
`(n,a)`-function or `a`-independent — window uniformity is immediate given
single-agreement payment), **UNIFORM-WITH-PROOF** (needs Lemma W / Lemma B / the
census cell-count bound), **NOT-ESTABLISHED** (source fixes `a`, hides an
`a`-dependence, or the source is absent).

| Cell | Source label(s) | Budget form `U(n,a)` | `a`-dependence | Verdict |
|---|---|---|---|---|
| **C1** quotient-pullback | `def:capf-quotient-status` (5838), `prop:capf-quotient-safe-sum` (5858), `thm:exact-quotient-image-lcm-ledger` (1873), `thm:capf-census` (5970)+`lem:capf-census-identity` (5953), `prop:capf-qprofile` (6020) | `U_{\rm sum}=\sum_{c\in\mathcal C}\sum_{B=A}^n\binom{n/c}{\lfloor B/c\rfloor}\binom{n-c\lfloor B/c\rfloor}{B-c\lfloor B/c\rfloor}` | monotone ↓ in `A`; `\le n\cdot\max_B(\cdot)`; active `c` count bounded by census | **UNIFORM-WITH-PROOF** (Lemma B on each `\binom{}{}`; `\le n` terms = `\exp(o(n))`; census caps `|\mathcal C|=O(1)`) |
| **C2** Chebyshev/dihedral | `exact Chebyshev fibers` (3957), `torus uniformization` (4010); paper L114 reduction | inherits C1 downstairs-support/image budget | as C1 (extra bounded monodromy factor) | **UNIFORM-WITH-PROOF** (reduces to C1) |
| **C3** planted-block | `thm:capf-planted` (6060), `def:capf-qprofile` (6010), `prop:capf-dyadic-planted` (6175) | `\binom{n/M-1}{k/M}` per active `M` | **`a`-independent** (constant on `1\le\sigma<M`); dyadic-monotone in scale | **UNIFORM-BY-INSPECTION** (flat in `a`; bounded active `M`) |
| **C4** tangent/deep-center | `def:capf-tangent-cell` (5782), `prop:capf-tangent` (5794), Grande `exact high-agreement tangent cell` (481) | `n-A+1` on `3(n-A)\le n-k` | explicit **linear, monotone ↓**, on a full `A`-interval | **UNIFORM-BY-INSPECTION** |
| **C5** extension/descent | `prop:capf-extension` (5866), `thm:extension-line-dimension-degree-ledger` (2856), `cor:extension-pole-deep-list-floor` (530) | `\Delta_Y|\B|^{e_Y}` (safe side) / `\mathrm{ExtPole}(q_{\rm line},q_{\rm gen},\kappa,L)` | **`a`-independent** (chart degree/dimension, field sizes) | **UNIFORM-BY-INSPECTION** |
| **C6** differential-locator / rank-drop | `thm:regular-closed-ball-hankel-packing` (2167), `cor:canonical-regular-closed-ball-hankel-packing` (2303), `exact arbitrary-residual image ledger` (3194) | `\mathrm{poly}(n)` Hankel-minor / rank-drop degree counts | polynomial, `a` only through bounded rank/degree | **UNIFORM-BY-INSPECTION** (`\mathrm{poly}(n)=\exp(o(n))` at any `a`) |
| **C7** saturation / image-collapse | Grande `exact saturation identity` (1811), `line-ray saturation identity` (1867); v13 residual-image (3194, 3231) | **exact identity** image-count `=` (not `\le`) | identities hold at **every** `a` | **UNIFORM-BY-INSPECTION** (equalities are `a`-uniform) |
| **C8** balanced-core / split-pencil | `thm:bc-moving-root` (1735), `cor:bc-one-pencil` (1764), `interpolation-lattice split-pencil reduction` (1336) | `\lfloor (n-g)/(\omega-g)\rfloor`, `\omega=n-a`, per pencil; `\le|\F|^{r_1+r_2}` pencils | explicit; `=O(1)` per pencil at frontier (`\omega=\Theta(n)`) | **UNIFORM-BY-INSPECTION** (per-pencil `O(1)`, eventually constant across `W_n`) |
| **C9** Fourier/Sidon | paper `def:sidon-paid` (196); Grande `thm:fourier-flat-q` (916), `def:fourier-flat-prefix-leaf` (896); **routing** → `Cho26ModuliSelf`,`Cho26ModuliFinal` (absent) | Fourier-flat budget `\exp(o(N))Q^{-w}\binom Nm` (window-explicit); **routing** budget: none in-tree | Fourier-flat part interval-valued; routing part unsourced | **NOT-ESTABLISHED** (routing phantom — FINDING-1 of #433; *not* a window defect) |

Adjacent (not `(Cj)` cells but consumed at window-varying `a`):

| Item | Source | Status |
|---|---|---|
| **U3** primitive residual | `thm:primitive-q` (paper 236) via `def:primitive-logmoment` (756), `thm:logmoment-equivalence` (773), `prob:entropy-inverse-q` (827), `thm:primitive-q-closure-module` (Grande 2252) | **NOT-ESTABLISHED-BUT-FREE**: `prob:entropy-inverse-q` is *already* stated uniformly `\forall R\in[\kappa N,\kappa^{-1}N]` (827, "for every fixed `\alpha,\kappa,\eta`… with `\kappa N\le R\le\kappa^{-1}N`"). Since `R=w=a-k-1` and `w/n\to g^*\in(0,1-\rho)`, the window lies in a fixed `R`-band, so window-uniformity is *built into the atom*. The atom itself is unproved (the pre-existing gap), and the side condition `w\log|\B|/r=o(n)` is window-stable by Lemma W. Windowing adds nothing. |
| **Lower side** (B4) | `prop:pole-line` (Grande 583); collision loss redirected to `lem:capff1-identity-prefix-floor` (v13 6909) | window scale is again `\binom nm|\B|^{-w}` (same Lemma-W arithmetic). The *collision-loss* subexponential bound is **#442's lane** (B4). Window-uniformity of the count itself: UNIFORM-WITH-PROOF (Lemma W). |

**Tally over the nine cells:** UNIFORM-BY-INSPECTION **6** (C3,C4,C5,C6,C7,C8);
UNIFORM-WITH-PROOF **2** (C1,C2); NOT-ESTABLISHED **1** (C9, and it is FINDING-1's
phantom-source gap, not a window gap). Cell count (U1): `9` families × census-bounded
sub-cells `=\exp(o(n))` — **UNIFORM-BY-INSPECTION** via `prop:capf-qprofile`
(6020): `\sigma\ge n/256\Rightarrow` active dyadic quotient order `N=n/M\le128`,
constant in `n`.

---

## 4. Primitive residual window-uniformity in detail `AUDIT`

`thm:frontier` uses primitive Q through `lem:addback` (paper 246, **#441's lane**),
which upgrades the primitive max-fiber bound `thm:primitive-q` to the full
prefix-boundary count. Two window facts:

1. **The atom is pre-windowed.** `prob:entropy-inverse-q` (827) quantifies "*for
   every fixed `\alpha,\kappa,\eta>0` and `A<\infty`, with `\kappa N\le R\le
   \kappa^{-1}N`*". The prefix depth `R=w` moves by `o(n)` across `W_n` while
   `w/n\to g^*` keeps `R\in[\kappa N,\kappa^{-1}N]` for a fixed `\kappa`. Hence a
   single `(\alpha,\kappa,\eta,A)` choice covers the whole window; the atom's own
   statement is uniform in exactly the parameter that the window varies.
2. **The reduction is window-stable.** `thm:logmoment-equivalence` (773) needs
   `w\log|\B|/r=o(n)`; with `w=\Theta(n)`, `\log|\B|=O(1)`, `r=r(n)\to\infty`
   this is `o(n)` at every `a\in W_n` simultaneously. `lem:largest-fiber-to-excess-closure`
   (Grande 2236) uses the same side condition.

Therefore U3 is not an *additional* window hypothesis: assuming
`prob:entropy-inverse-q` at all (which the paper does, via C9/`thm:primitive-q`)
already yields it uniformly on `W_n`. The genuine open object is the atom itself
(`prob:entropy-inverse-q`), which is the pre-existing gap, unchanged by windowing.

---

## 5. Named residual assumption and falsifier `OPEN`

> **Assumption `ass:window-uniform-ledger` (residual after B3 discharge).**
> Single-agreement closure holds at the crossing: there is `\eps'_n\to0` with
> `\sum_{j=1}^{9}U_{C_j}(n,a_n)+\max_s N^{\rm prim}_{a_n}(s)\le
> \exp(n\eps'_n)\,\barN_{n,a_n}` at the single agreement `a=a_n`.

Given `ass:window-uniform-ledger`, §1–§4 **prove** (LC-unif): windowing is free.
`ass:window-uniform-ledger` is *not new* — it is exactly the single-agreement
`thm:closed-ledger-package` (paper 105), whose C1–C8 citations #433 rated
`FOUND-EXACT` and whose C9 routing + primitive-Q atom #433 rated the pre-existing
`OPEN GAP`s (FINDING-1 + `prob:entropy-inverse-q`). So the residual after B3 is:

- **R-C9 `OPEN`.** The single-agreement C9 routing payment ("major arcs route to
  algebraic cells") is sourced only to the absent `Cho26ModuliSelf`/`Cho26ModuliFinal`.
  (Windowing is free for the in-tree `thm:fourier-flat-q` part.) Owner: FINDING-1
  of #433 / the C9 moduli-source lane, **not** this note.
- **R-atom `OPEN`.** `prob:entropy-inverse-q` is unproved. Windowing is free (§4).
  Owner: the primitive-inverse-theorem lane, **not** this note.

**Explicit falsifiers** (each is a live gate + tamper in the verifier):

- **F1 (interior).** If `a_n/n\to c` with `c\to1` (i.e. `\beta\to0`, so
  `g^*\to1-\rho`), `H_2'(\xi)\to+\infty` at the window and Lemma W fails: the
  binomial ratio across an `o(n)` window need not be `\exp(o(n))`. *Falsifier:*
  exhibit a frontier row with `\beta_n\to0` where `\binom n{a_n+\psi_n}/\binom
  n{a_n}` is not `\exp(o(n))` for some `\psi_n=o(n)`. (Guard: `\beta>0`.)
- **F2 (window scale).** If the slide is `\Theta(n)` rather than `o(n)`, the
  normalized log-ratio converges to `H_2(c+\theta)-H_2(c)\ne0` (a fixed nonzero
  constant, e.g. `-0.0897` at `c=0.6,\theta=0.1`) and (LC-unif) is false.
  *Falsifier:* any use of the ledger that slides the agreement by `\ge\delta n`
  for fixed `\delta>0`. (Guard: the frontier proof slides only `o(n)`.)
- **F3 (bounded base).** If `\log_2|\B_n|` is unbounded with
  `(a-a_n)\log_2|\B_n|\ne o(n)` on `W_n`, the subfield factor `|\B|^{-(a-a_n)}` is
  not `\exp(o(n))` and Lemma W fails. *Falsifier:* a row with `\beta_n\to\infty`
  fast enough that `\psi_n\beta_n\ne o(n)`. (Guard: `\beta_n=O(1)` at the frontier.)
- **F4 (bounded cell count).** If active quotient orders were unbounded in `n`
  (`prop:capf-qprofile` failing), (U1) breaks. *Falsifier:* a domain with
  `\Omega(n)` simultaneously active dyadic scales at slack `\sigma=\Theta(n)`.
- **F5 (spike-free / conserved budget).** Cell *activation* (`0\leftrightarrow
  \mathrm{poly}`) is not itself a falsifier — first match conserves the total
  across a straddle (activation remark, §1). A genuine falsifier is a cell whose
  *total* contribution jumps by `\exp(\Omega(n))` across an `o(n)` window **without**
  a first-match counterpart absorbing it, i.e. a printed budget that is neither a
  bounded-complexity `(n,a)`-formula on its active interval nor slope-conserving at
  its activation threshold. *Falsifier search over C1–C8: none found* — every
  budget is binomial/polynomial/linear/constant on an `a`-interval, and every
  activation threshold is first-match-covered.

If none of F1–F5 fires (the frontier regime: `\beta>0`, `o(n)` slide, bounded base,
census-bounded cells, bounded-complexity budgets), B3 is discharged.

---

## 6. Verifier `AUDIT`

`experimental/scripts/verify_asymptotic_window_uniformity.py` (stdlib-only,
zero-arg, best-effort `RLIMIT_AS` 2 GB, chunked, exact big-int binomials where
feasible; `lgamma` cross-check at larger `n` is labeled and capped). Live gates:

- **G1 Lemma W / binomial part.** Exact `\binom{n}{a\pm d}/\binom na` for
  shrinking `o(n)` windows `d=\lceil n^\theta\rceil`, `\theta\in\{0.7,0.6,0.5\}`,
  `c\in\{0.3,0.5,0.7\}`, `n\in\{10^4,4\cdot10^4,1.6\cdot10^5\}`; assert the exact
  `(1/n)\log_2` ratio matches the `H_2(c+d/n)-H_2(c)` surrogate within the
  Stirling tolerance `(\log_2 n+4)/n` and the surrogate strictly collapses toward
  `0` (`\to0` signature of an `o(n)` window).
- **G2 Lemma W / subfield part.** `(1/n)\,d\,\log_2|\B|=\beta\,n^{\theta-1}\to0`
  for `\beta\in\{1,8,31,128\}`, `d=\lceil n^{0.6}\rceil` (exact rational,
  ratio-collapse).
- **G3 combined `\barN` ratio** (G1×G2, exact big-int).
- **G4 Stirling/entropy identity.** `|\log_2\binom na-nH_2(a/n)|\le C\log_2 n`
  (validates `thm:frontier` L292 expansion; exact big-int vs `H_2`).
- **G5 frontier interior.** `g^*(\rho,\beta)` by exact monotone scan; assert
  `\rho+g^*<1` strictly for `\beta>0`, `=1` at `\beta=0` (boundary).
- **G6 per-cell budget window-stability.** C3 planted flat-in-`\sigma` (exact
  equality); census `A_2=(3^{n_1}-1)/2` strictly increasing (exact);
  `prop:capf-dyadic-planted` injective monotonicity
  `\binom{N-1}{\rho N}\le\binom{2N-1}{2\rho N}` (exact); C4 `n-A+1` and C8
  `\lfloor n/(n-a)\rfloor` `o(n)` log-variation across `W_n` (exact).
- **G7 cell-count bound.** active dyadic `M` count `\le\log_2(1/\eta)+1`,
  constant in `n` (`prop:capf-qprofile`).

Tamper self-tests (each threads a corrupted value through a live gate; must be
rejected): **T1** `\theta=1.0` (`\Theta(n)` slide, F2) → G1; **T2** `c=0.98`
near-1 interior (F1) → G1; **T3** `\beta_n=n` unbounded base (F3) → G2; **T4**
census value off by one (breaks monotonicity) → G6; **T5** wrong entropy
(`H_3` for `H_2`) → G4; **T6** C8 budget forced to grow `\propto n` → G6; **T7**
`\rho+g^*=1` boundary (F1/`\beta=0`) → G5. (7 tampers ≥ 5.)

Recorded run (2026-07-09, this branch): **`RESULT: PASS` — real gates 34/34,
tamper tests 8/8** (7 corruptions rejected + 1 positive control kept), ~5.5 s,
under the 2 GB `RLIMIT_AS` cap. Every cap is printed by the script.

---

## 7. Proposed tex delta (NOT applied — note-only) `AUDIT`

If a maintainer wants B3 reflected in `asymptotic_rs_mca.tex` (owned by #439; do
not stack a fourth edit stream), the minimal precise change is:

1. **After `thm:closed-ledger-package`**, add one lemma (no new hypotheses):
   *"(Window slide is free.) If the closed paid ledger holds at the single
   agreement `a_n` with rate `\eps'_n`, and `\rho+g^*\in(0,1)`, `\log_2|\B_n|=O(1)`,
   then it holds uniformly on every `o(n)`-window `W_n` around `a_n`."* Proof:
   Lemma W + Lemma B + the discharge principle of §1.
2. **In `thm:frontier`**, replace the hypothesis "*the closed paid ledger holds
   uniformly in every `o(n)`-window*" with "*the closed paid ledger holds at the
   crossing `a_n`*" and cite the new lemma for the slide. This removes B3 as an
   independent hypothesis, leaving only the C9-routing and `prob:entropy-inverse-q`
   inputs that #439/#433 already expose.
3. Optionally record `ass:window-uniform-ledger` (§5) as the residual and point its
   two `OPEN` children at FINDING-1 and the atom.

This is a *strict weakening* of the assumption set (window → single point), which
is why it is worth doing, but it is #439's call to land.

---

## 8. Interaction with open PRs `AUDIT`

- **#439** (`codex/asymptotic-b1-image-normalization-v1`) **owns `thm:frontier`
  and `thm:closed-ledger-package` wording.** It has already turned
  `thm:closed-ledger-package` into a *Conditional* package that "*assume[s] the
  cited (C1)–(C8) payments hold uniformly in the asymptotic frontier window*" and
  introduced `ass:image-normalized-sidon-input`. **This note is the analysis
  behind that assumption:** it shows the "(C1)–(C8) uniform in the window" clause
  is *free given single-agreement closure* (FIXED via Lemma W/B), so #439's
  assumption can later be weakened to single-point closure per §7. No tex overlap.
- **#441** (`thresholds-addback-decomposition`) **owns `lem:addback`** (paper 246),
  the primitive→full add-back that this note's U3 feeds into. Window-uniformity of
  U3 is argued here (§4) to be free given the atom; the add-back *magnitude* is
  #441's object. Disjoint blocks.
- **#442** (`thresholds-lowerside-collision-free-reroute`) **owns the lower side**
  (paper L276–L287, B4). This note only observes the lower count rides the same
  Lemma-W arithmetic; the collision-loss bound is #442's. Disjoint blocks.
- **#433** (`thresholds-asymptotic-ledger-audit`) is the **lineage**: B3 =
  `FOUND-WEAKER`, "missing lemma: a window-uniform restatement of the per-cell
  budgets." This note supplies that restatement for C1–C8 and inherits #433's C9
  (FINDING-1) and atom `OPEN GAP`s unchanged.
- **#435** (in-paper proof audit, "8 no-issue, 2 open gaps") is adjacent; its open
  gaps are the same C9/atom pair, consistent with §5.

No edit to `asymptotic_rs_mca.tex` here; the four streams above keep the tex
single-owner per block.

---

## 9. Nonclaims `AUDIT`

- **Not** a proof of single-agreement closure `thm:closed-ledger-package`. That is
  taken as given (it is #433's citation object); this note only proves it *slides*.
- **Not** a proof of `prob:entropy-inverse-q` (the primitive-Q atom) or of the C9
  routing claim. Those remain `OPEN` (owners named in §5/§8); windowing is shown
  free, which is a *strictly weaker* statement than proving them.
- **Not** an edit to the tex, to Papers A–D, or to any other lane's file.
- Lemma W / Lemma B are elementary Stirling+MVT facts; the contribution is
  *scoping* (identifying that B3 reduces to them) and *verifying* the per-cell
  budget forms, not deep additive combinatorics.
- The verifier checks the **arithmetic** of the window slide and the **shape** of
  each cited budget; it does not re-derive the algebro-geometric cell counts
  themselves (their statement-level existence is #433's `FOUND-EXACT`).
- The finite `2^{128}` census/planted tables (`thm:capf-census`,
  `prop:capf-dyadic-planted`) are cited only for their **monotonicity**, not as
  asymptotic budgets; no finite-row margin claim is made.

## 10. Claim-label ledger

| # | Claim | Label |
|---|---|---|
| 1 | (LC-unif) ⇔ (U0)∧(U1)∧(U2)∧(U3) | `PROVED` (decomposition, §1) |
| 2 | Lemma W: `\barN` moves by `\exp(o(n))` on an `o(n)`-window (interior, bounded base) | `PROVED` |
| 3 | Lemma B: bounded-complexity budgets have `o(n)` log-variation on `W_n` | `PROVED` |
| 4 | Discharge principle: single-agreement payment + Lemma B ⇒ (U2) | `PROVED` |
| 5 | Source budgets C1–C8 are bounded-complexity `(n,a)`-formulas on `a`-intervals | `AUDIT` (§2, §3) |
| 6 | Per-cell verdicts (6 by-inspection / 2 with-proof / 1 not-established) | `AUDIT` |
| 7 | U3 window-uniformity is built into `prob:entropy-inverse-q`'s `R`-range | `AUDIT` |
| 8 | `\beta>0 \Rightarrow \rho+g^*<1` (frontier interior guard) | `PROVED` (verified G5) |
| 9 | `ass:window-uniform-ledger` reduces exactly to single-agreement closure | `AUDIT` |
| 10 | Residual R-C9 (routing phantom) and R-atom remain open; windowing adds nothing | `OPEN` |
| 11 | Falsifiers F1–F5 gated in the verifier | `AUDIT` |

**Bottom line.** B3's window-uniformity is **FIXED** for the established cells:
the `o(n)` window slide is elementary arithmetic (Lemma W + Lemma B), free given
single-agreement closure, because every C1–C8 budget is a bounded-complexity
`(n,a)`-formula valid on an `a`-interval and the reference scale `\barN` moves by
`\exp(o(n))`. The only residual is the pre-existing single-agreement **OPEN GAP**s
(C9 routing = FINDING-1; `prob:entropy-inverse-q` atom), and windowing neither
creates nor worsens them. Net: B3 is removed from the list of *independent*
load-bearing gaps and demoted to a corollary of single-agreement closure.
