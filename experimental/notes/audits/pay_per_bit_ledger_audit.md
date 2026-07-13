# Pay-per-bit ledger audit: the three quoted records, the board, and the interval

## Status

`AUDIT of the "Pay-per-bit framing" paragraph added to readme.md and
site/index.html at fe93bb5 / all three quoted records verbatim-checked
against their in-tree sources at fe93bb5 / RESULT: MATCHES on all three,
zero print corrections forced / plus a board-to-bits classification of the
35 packets in the current open wave and the just-integrated c23dcaa wave
(#699-#735), and the current two-sided delta*_C(2^-128) bracket picture.
Not theorem-shaped: AUDIT, no Lean stub.`

## 0. The steering paragraph, verbatim, with its anchor

Added at commit `fe93bb59dff3d022f66a097208e17c27e1e0deb4` ("Add pay-per-bit
framing to site and README"), `readme.md` lines 12-22:

> **Pay-per-bit framing.** If the Proximity Prize is allocated pro-rata by
> soundness-gap bits, our current results are naturally scored by certified bits
> above the `2^-128` target at an audited radius and denominator. Paper D v12 gives
> the cleanest broad record: in its cap range it proves `epsilon_mca > 2^-86`,
> which is at least **42 bits above** the target throughout the full prize field
> envelope. The strongest finite numerator record on the site is the
> Cycle116/119 `F_17^32` row, about **32.82 bits above** target, while the exact
> tangent-staircase gate gives a narrow but fully structural 6/7 transition. A
> pay-per-bit rule would therefore reward both kinds of progress: larger certified
> bit margins and, more importantly, certificates that push the unsafe radius
> lower or close the interval for `delta*_C(2^-128)`.

The companion sentence in `site/index.html` line 559 (`warning-line` div)
states the same three numbers and is checked as a duplicate-consistency
anchor below.

## Verdict table

| # | Record | Claim | Verdict | Primary anchor |
|---|---|---|---|---|
| 1a | Paper D v12 cap | `epsilon_mca > 2^-86`, i.e. >=42 bits above `2^-128`, throughout the prize field envelope | **MATCHES** | `tex/cs25_cap_v12.tex:3542-3573` (`cor:grand`), numerics at `:3582` |
| 1b | Cycle116/119 `F_17^32` row | `52,747,567,092/17^32 > 2^-128`, about +32.82 bits | **MATCHES** (computation-dependent, flagged in-tree) | `site/data/rate-leaderboards.json:574-576,620-622`; `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md` |
| 1c | Tangent-staircase gate | "narrow but fully structural 6/7 transition" | **MATCHES** | `experimental/data/tangent/tangent_staircase_summary.md:34-70` |

No print correction is forced on any of the three. All three numbers are
recomputed exactly (Python `Fraction`/`Decimal`, no floating-point shortcuts)
by `experimental/scripts/verify_pay_per_bit_ledger_audit.py --check`.

---

## 1. The three records, in detail

### 1(a) Paper D v12: `epsilon_mca > 2^-86` — MATCHES

**Where it is printed.** The abstract states it first (`tex/cs25_cap_v12.tex:61`,
"On the unsafe side we prove a field-size-universal cap... `>= 2^-86 >> 2^-128`
throughout the printed near-capacity band"), the informal Theorem 1.1 restates
it (`:88`, "`emca(C,delta)>2^-86>>2^-128`"), and the formal statement is
**Corollary `cor:grand`** ("universal field-size cap for the challenge
envelope"), `tex/cs25_cap_v12.tex:3542-3573`:

```
Let rho in {1/2,1/4,1/8,1/16} and set N_rho:=1024 (rho in {1/2,1/4,1/8}),
N_{1/16}:=2048. Let F be any finite field with q<2^256, let B<=F be any
subfield, let D<=B^x be a multiplicative coset of order n with N_rho | n,
and let k=rho n<=2^40. Then C=RS[F,D,k] satisfies

  emca(C,delta) > (1/2k)(1-n/q) >= 2^-86 >> 2^-128

for every delta in [1-rho-2/N_rho, 1-rho).
```

The exact numeric derivation is at `:3582`: `n<=k/rho<=16k<=2^44` (since
`k<=2^40`), so `(1/2k)(1-n/q) >= 1/(2k(n+1)) > 2^-86`, using `1-n/q>=1/(n+1)`
(as `D subseteq F^x` forces `n<=q-1`).

**Exact recheck (integer, no floats).** Worst case is the largest `k` and `n`
allowed by the hypotheses: `k=2^40`, `n=16k=2^44`. Then
`2k(n+1) = 2*2^40*(2^44+1) = 2^85+2^41`, which is `< 2^86` (since
`2^41 < 2^85`), so `1/(2k(n+1)) > 2^-86` exactly. `128-86=42` (trivial). Both
checked as exact big-integer inequalities in the verifier (`--check` items
`paperD_integer_inequality`, `paperD_bit_gap`).

**"Throughout the full prize field envelope."** The envelope, as ABF define
the grand MCA challenge (`tex/cs25_cap_v12.tex:78`), is `rho in
{1/2,1/4,1/8,1/16}`, `k<=2^40`, `|F|<2^256` — exactly `cor:grand`'s
hypotheses (`q<2^256`, that same `rho` set, `k=rho n<=2^40`), so the "full
prize field envelope" phrase is accurate: the bound holds for *every* field
in the challenge's parameter space, not one instantiation. One caveat worth
flagging (not a correction): `cor:grand` also requires `N_rho | n` (domain
order divisible by 1024, resp. 2048) — a genuine extra printed hypothesis
that is not spelled out in the bare ABF envelope sentence, though it is the
ordinary "smooth"/FFT-friendly-domain condition this entire line of work
assumes. The readme does not claim otherwise ("in its cap range" already
scopes the delta-window), so this is filed as a caveat, not a mismatch.

**Direction.** This is an *unsafe-side* (failure) bound: it proves
`emca(C,delta)` exceeds `2^-86` near capacity, i.e. it establishes
`delta*_C(2^-128) <= 1-rho-2^-9` (resp. `2^-10` at `rho=1/16`) — a **cap**, not
a safety certificate. The "42 bits above target" language is exactly the size
of a *proven violation* margin, consistent with the pay-per-bit paragraph's
own framing (bits above target, either direction).

**Observation, not a correction.** The same corollary's last sentence gives a
sharper *conditional* number: "If `q>=2n`, the lower bound improves to
`>=2^-42`" — that is **86 bits** above target, a strictly better pay-per-bit
number, but conditional on the field being at least double the domain size
(not "throughout the full envelope"). The readme's quoted `2^-86`/42-bit
number is the correct one to cite as the *unconditional*, envelope-wide
record; `2^-42`/86-bit is available as a sharper number for rows that happen
to satisfy `q>=2n`, worth a future footnote but not a correction to the
present text.

### 1(b) Cycle116/119 `F_17^32` row — MATCHES

**Where it is printed.** `site/data/rate-leaderboards.json:574-576` and
`:620-622`, `site/data/frontier.json:40,69`, and `site/index.html:609,
2622-2623,2668-2669` all print `"nBad": "52747567092"`,
`"failureMarginBits": 32.82` for the two Cycle116 (agreement 262) and Cycle119
(agreement 263) rows over `F_17^32`. The underlying finite claim —
`LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092` at `delta=125/256` (agreement
`262/512`) — is in `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md:24,53`
and `experimental/SUMMARY.md:261-263`, giving
`epsilon_mca(C,125/256) >= 52,747,567,092/17^32 > 2^-128`.

**Exact recompute.** `bad = 52747567092`, `q = 17^32 =
2367911594760467245844106297320951247361`. `gcd(bad,q)=1` (17 does not
divide `bad`), so the fraction is already reduced:

```
epsilon_row = 52747567092 / 2367911594760467245844106297320951247361
            ~= 2.2275986657912297e-29
```

Cross-multiplied integer check: `bad * 2^128 > q`, confirming
`epsilon_row > 2^-128` exactly (no floating point). The bit margin, computed
at 50-digit `Decimal` precision as `128 + log2(epsilon_row)`:

```
log2(epsilon_row)      = -95.1804254180804657694648312620999981000589756996662425931802
bits_above_target       =  128 + log2(epsilon_row)
                        =   32.8195745819195342305351687379000018999410243003337574068198
round(bits_above_target, 2) = 32.82
```

which matches the printed `32.82` exactly to the printed precision. Verifier
item `cycle_row_bit_margin`.

**Caveat already flagged in-tree (not new).** The `nonclaims` field alongside
every one of these JSON rows already states: "The exact `52,747,567,092`
numerator and `+32.82` bit margin still import the Cycle84 finite count" —
i.e. this specific number is computation-dependent, not (yet) an
independently-reverified integer certificate the way the tangent-staircase
gate (1c) is. The readme calls it "the strongest finite numerator record on
the site," not a theorem, so this is consistent — MATCHES, with the
conditionality noted for completeness.

**Direction.** Also an unsafe-side finite obstruction: a proof that this one
row's error at agreement 262/263 exceeds `2^-128` by 32.82 bits, at `delta =
125/256` (Cycle116) resp. the sharper `249/512` (Cycle119).

### 1(c) The exact tangent-staircase gate: "6/7 transition" — MATCHES

**Where it is printed.** `experimental/data/tangent/tangent_staircase_summary.md:34-70`
("Consequence for the `F_17^32`, `n=512`, `k=256` row"), backed by the
theorem in `experimental/notes/high_agreement/tangent_staircase.tex`
(moving-root tangent floor, `thm:moving-root-tangent-floor`, plus the matching
upper bound once `3a-2n>=k`). Also cross-listed on the site as row
`tangent506-exact-gate`: `"nBad": "7 at a=506; 6 at a=507"`,
`"marginLabel": "exact 6/7 gate"` (`site/data/rate-leaderboards.json:702-716`).

**What the "6/7" object precisely is.** For `C=RS[GF(17^32),H,256]`, `|H|=512`,
the target integer budget is `floor(17^32/2^128) = 6` bad slopes. The exact
staircase range (`3a-2n>=k`, i.e. `a>=ceil((2n+k)/3)=427`) covers agreements
506 and 507, where `LD_sw(C,a) = n-a+1 = 513-a` exactly:

```
LD_sw(C,506) = 7   -> 7 > 6  -> unsafe: epsilon_mca > 2^-128
LD_sw(C,507) = 6   -> 6 <= 6 -> exactly at budget: safe
```

So "6/7" is the literal pair of integer bad-slope counts (`LD_sw` values)
straddling the target budget at the two *consecutive* agreements 506 and 507
— the tightest possible finite-slope pinning: the largest safe integer
Hamming radius is 5 (normalized `5/512`), and integer radius 6 (`6/512 =
3/256`) is already unsafe, under the finite-slope support-wise MCA
convention.

**Exact recheck.** `floor(17^32 // 2^128) = 6` (exact integer floordiv);
`513-506=7`, `513-507=6`; `3*506-2*512=494>=256` and `3*507-2*512=497>=256`
(both inside the exact range); `ceil((2*512+256)/3)=427<=506`. All exact
integer arithmetic, verifier item `tangent_staircase_recompute`.

**"Narrow but fully structural."** *Narrow*: a single integer-agreement step
(506 to 507). *Fully structural*: the theorem is an unconditional finite
combinatorial statement (moving-root construction for the lower bound,
common-code-line residual-budget argument for the matching upper bound in
this range) that "does not use smoothness" and is "independent of
quotient-periodic structure" (`tangent_staircase.tex` header) — unlike 1(b),
it does **not** import the Cycle84 finite count. Of the three records, this
is the one that most literally "closes the interval for `delta*_C`" (for this
one row, under this one convention): it pins the row's safe/unsafe boundary
to a single grid step, unconditionally.

---

## 2. Board-to-bits map: the c23dcaa wave and the current open wave

Applying the pay-per-bit rule to all 35 packets — the 24 PRs manually
integrated at `c23dcaa` (`#699`-`#722`) and the 11 open packets
(`#723,#725,#727`-`#735`) — against the four buckets: **(i)** moves a
certified bit margin, **(ii)** pushes the unsafe radius lower, **(iii)**
narrows/contributes to closing the `delta*_C(2^-128)` interval via one of
agents.md's five hard inputs (1 atlas, 2 image-scale MI/MA or Sidon, 3
residual ray compiler, 4 profile-envelope comparison, 5 lower reserve), or
**(iv)** none (infrastructure, audit-only, or a different prize sub-problem).

**Headline, stated honestly up front: zero of the 35 packets are (i) or
(ii).** None directly moves a printed certified bit margin or a printed
unsafe radius. 24 are **(iii)** (route-cuts, structural reductions, or proved
sub-theorems narrowing one of the five hard inputs, without yet changing a
printed number); 11 are **(iv)** (audits/reconciliations, or packets serving
the *Grand List* deployed-row problem, which is a different ABF challenge
from the MCA threshold `delta*_C` this rule scores). This matches the
maintainer's own framing that "more importantly" certificates should push the
radius or close the interval — on the evidence of this wave, that next step
has not happened yet; the wave is (necessarily) preparatory.

Author key: **ours** = GitHub `holmbuar` (the account this program ships PRs
under); **external** = a named outside collaborator, credited per packet.

### 2.1 The c23dcaa wave (`#699`-`#722`, integrated; manual-integration commit `c23dcaa0514c72d195f1c5eb163500150ff637bd`)

| PR | author | category | one-line |
|---|---|---|---|
| #699 | ours | (iii) input 5 | O5c list route PAID for quotient/Euclidean-remainder/Chebyshev classes; coupling lemma: no profile-list reaches O7; deep-remainder OPEN |
| #700 | ours | (iv) | repairs own #691 T1 (refuted-as-printed, corrected T1'); defends the (note-level, no-tex-consumer) `rho*` program; no bit/radius movement |
| #701 | ours | (iii) input 2 | proves #696's energy lift is denominator-blind — route-cut, no pincer exists |
| #702 | external (DannyExperiments) | (iv) | interleaved-list shell compression, one-row max — Grand List row bound (different prize sub-problem), not `delta*_C` |
| #703 | external (DannyExperiments) | (iv) | excludes affine rank <=14 from the Grand List one-row wall — same sub-problem as #702 |
| #704 | external (DannyExperiments) | (iii) input 3 | transverse all-parameter extension of the A6 line-section compiler (one line/one chart) |
| #705 | ours | (iv) | stacked-trade census hardens the `rho*` lower end (0.160847) from "best found" to a `k<=5` family ceiling — bracket-hardening, no tex consumer yet |
| #706 | ours | (iv) | AUDIT: 42 atlas anchors verified current, NO PRINT CHANGE — confirms the A6 wave does *not* touch hard input 1's (A2) coverage obligation despite superficial similarity |
| #707 | ours | (iii) input 5 | fixed-rate identity crossings are `o(n)` from `k+1`; upper-half secant ceiling is one — localizes O7 |
| #708 | ours | (iii) input 2 (predecessor) | roots order-two Fourier-band failures in a heavy realized boundary fiber; owner payment left open (later generalized by #716) |
| #709 | ours | (iv) | reconciliation note recording the `rho*` bracket + supersession map (superseded same day by #727) |
| #710 | ours | (iii) input 5 | proves the combined two-regime lower reserve `max{P,E}` |
| #711 | ours | (iii) input 2 | Theorem H: the two-band habitat is denominator-blind — route-cut, decided-negative for the habitat shortcut |
| #712 | ours | (iii) input 5 | builds the deep-remainder partial-occupancy atlas; field-drop route DECIDED NEGATIVE (Theorem DR); same-evening correction below (#714) |
| #713 | ours | (iii) input 1 | `(CAT)` atlas ledger: exhaustion composes (PROVED unconditional); full summation blocked at `{C3,C7,C8,C9}`, shown to collapse into inputs 1/2/3/4 + one census |
| #714 | external (DannyExperiments) | (iii) input 5 | COUNTEREXAMPLE to #712's instance-level no-list verdict (`F_169` witness: guaranteed list 6 > identity floor 1) — deep-remainder REOPENS as payable |
| #715 | external (latifkasuli) | (iii) input 3 | re-records the tier-4 census target on the deduplicated `\|LineRay\|` count (`prob:saturated-bc`); proves free parts + a model correction; target itself stays OPEN |
| #716 | external (avdeevvadim) | (iii) input 2 | owner-rooted dense-band localization: banks 7 finite reductions and states the charge-preserving signed-or-semantic dichotomy; primitive Sidon payment itself OPEN |
| #717 | ours | (iii) input 2 | heavy syndrome fibers are admissible rooted packets on the locator-prefix chart — #716's hereditary hypothesis drops there (CONDITIONAL on (A2) + an extension) |
| #718 | ours | (iii) input 2 | extends `R=2` image-scale flatness to growing characteristic (removes the bounded-`N/p` hypothesis); conditional only on a classical mixed-Weil import |
| #719 | external (DannyExperiments) | (iii) input 5 | signed local-minority fixed-composition Q: pays exact equal-block profiles (deployed cap 153); declares the exact next mixed-sign wall |
| #720 | external (DannyExperiments) | (iv) | Grand List projective-line lift wall — different prize sub-problem, isolates the exact remaining object (a global binary hyperplane lift) |
| #721 | external (DannyExperiments) | (iii) input 3 | canonical reduced rational-host compiler: witness-exhaustive incidence bijection for denominator degree `d>1` (score `0/2` on the global question) |
| #722 | external (DannyExperiments) | (iv) | rank-15 locator-saturation normal form for the Grand List row; eliminates no `M` |

### 2.2 The current open wave (`#723,#725,#727`-`#735`, unmerged; pinned at the head SHAs below)

| PR | head SHA | author | category | one-line |
|---|---|---|---|---|
| #723 | `95a1902` | ours | (iii) input 2 | two-regime census of #716's four clauses: ablating clause (iii) (first-match mask) alone restores absolute q-gain growth (EXPERIMENTAL, 42 instances) |
| #725 | `4bffb1d` | ours | (iii) input 1 | C3 planted census: row-independent generator types PAID exactly; row-dependent reading PAID negative (`binom(n,b)`, non-censusable); `(CAT)` blocked set shrinks `{C3,C7,C8,C9}->{C7,C8,C9}`; first Lean stub under the new rule |
| #727 | `c6d09ae` | ours | (iv) | reconciliation of all five hard inputs after the c23dcaa wave; `rho*` bracket survives unmoved (used as a cross-check source for this audit, credited) |
| #728 | `837054d` | ours | (iii) input 2 | PROVES first-match pruning bounds the signed band-excess on one family (`-> 0` for `q<4.199`; unpruned grows for `q>2.709`); integer window `{3,4}` exact |
| #729 | `cb9993b` | ours | (iii) input 2 | PROVES a chart-free pruned signed bound on every finite abelian group/chart/band/`q>=2`; closes the dictionary to #716 exactly for pruned nonsemantic packets |
| #730 | `539d8f0` | ours | (iii) input 3 | COUNTEREXAMPLE: general section-nonpositive rational-host extraction is FALSE; exact iff criterion + thin non-host stratum; cites `hyp:ray-compiler` directly |
| #731 | `6032044` | ours | (iv) | AUDIT of avdeevvadim's owner-rooted machinery: one local gap (kappa factor omitted, Cor 5.1), FIXED-proposal; five attacks NO ISSUE |
| #732 | `c5d1ede` | ours | (iii) input 2 | PROVES #716's charge conditions are free for positive-rooted packets; reduces the decomposition step to a named cardinality/concentration question |
| #733 | `a744375` | external (DannyExperiments) | (iv) | raises the `M=218` rank-15 degree floor `4792->4828` for the Grand List row |
| #734 | `abec030` | external (DannyExperiments) | (iii) input 3 | anti-host prefix compiler: explicitly constructs slope-rich lines with no rational-host presentation — positive-side complement to #730 |
| #735 | `f94d870` | ours | (iii) input 2 | PROVES heavy prefix fibers emit #716's semantic precursors on three classes, plus a 17,609-fiber zero-counterexample census |

**Totals.** 24 (iii) / 11 (iv) / 0 (i) / 0 (ii). Authorship: 23 ours, 12
external (DannyExperiments 10, avdeevvadim 1, latifkasuli 1 — each credited
per-row above). By hard input (packets counted as (iii), i.e. actually
narrowing that input; `#706` audits hard input 1 but is category (iv) —
its verdict is NO PRINT CHANGE, so it is not counted as a narrowing packet
here even though it is about input 1): input 1 (`#713,#725`), input 2
(`#701,#708,#711,#716,#717,#718,#723,#728,#729,#732,#735`), input 3
(`#704,#715,#721,#730,#734`), input 4 (none this wave — see section 3), input
5 (`#699,#707,#710,#712,#714,#719`). Input 2 is where the wave concentrated,
and `#728`/`#729`/`#732`/`#735` are its strongest entries: each is a *proved*
theorem (not just a route-cut or census), progressively discharging the
signed side of #716's dichotomy down to a residual of heavy-fiber emission +
decomposition concentration + a large-`q` Sidon estimate.

---

## 3. The interval statement: where bits come from next

Two genuinely different objects both bear on `delta*_C(2^-128)`, at two
different scales, and neither is currently a tightenable *numeric* bracket on
that exact quantity without further proof:

**(A) The deployed two-sided bracket — an actual numeric interval on a real
row's `delta*_C`.** `tex/cs25_cap_v12.tex:95-102`, Theorem `thm:informal-sandwich`
("two-sided deployed intervals"), for the KoalaBear-sextic row at its stated
target `2^-128` (rate `rho=1/2`):

```
delta*_C in [1/6, 15331/32768]   unconditionally           (ratio 2.81)
delta*_C in [1/4, 15331/32768]   modulo one import (BCIKS20) (ratio 1.87, "within a factor smaller than two")
```

(`(1-rho)/3=1/6`, `(1-rho)/2=1/4` at `rho=1/2`; `15331/32768=0.467864990234375`,
verified `32768=2^15`.) Sources for each edge, and what would tighten it:

- *Lower (safe) edge.* `1/6` comes from the self-contained deep-regime
  theorem (MCA safe below a third of minimum distance); `1/4` needs the
  imported BCIKS20 half-distance proximity-gap theorem (an "import-free
  alternative" via a self-contained half-Johnson CA bound is noted as
  available in the abstract but does not by itself reach `1/4` without
  its own hypotheses). Tightening past `1/4` toward capacity is exactly
  Open Problem `prob:band` (`tex/cs25_cap_v12.tex:114`): "prove a
  correlated-agreement theorem crossing toward capacity" between the
  half-distance frontier and the unsafe frontier — the paper's own name for
  this gap, the *aperiodic band problem*.
- *Upper (unsafe) edge.* `15331/32768` is the exact deployed-parameter
  scanner output (`thm:sandwich2`/`tab:scanner2`), sharper than the generic
  envelope-wide gap formula of `cor:grand` because it is computed at the
  KoalaBear row's actual `n`. Tightening it downward (more unsafe, closer to
  the safe edge) requires "a new floor construction beating the
  graded-prefix envelope" — the same Open Problem `prob:band`, other side.

**(B) The asymptotic frontier relation — a conditional identity, not
(yet) a bracket.** `experimental/asymptotic_rs_mca_frontiers.tex:1038-1046`,
eq. (1.10):

```
delta_n* = 1 - rho_n - g*(rho_n, beta_n) + o(1),
g*(r,b) = sup{g in [0,1-r] : H_2(r+g) >= b g}
```

This is the formula agents.md names as the asymptotic resolution target. It
is *conditional*: it requires (i) an interior right-crossing of the
target-crossing function, (ii) that "the exact safe and unsafe tests furnish
agreements `a_{+-,n}=k_n+1+g_{T,n}n+o(n)`" (`:1033-1034`), and, for the closed
form actually used, (iii) `log(1+B_n^*)=o(n)`. Once those hypotheses are
discharged for a given row/envelope, the "interval" collapses to a single
asymptotic value — there is no numeric bracket to narrow here so much as a
hypothesis to prove. That is precisely agents.md's five-hard-input checklist
(section 2 above): discharging inputs 1-3 is what turns condition (ii) from
an assumption into a theorem, input 4 is the completeness of the profile
envelope used to state (i)/(iii) in general, and input 5 is the unsafe-side
comparison that supplies the "exact... unsafe tests" half of (ii).

**(C) The `rho*` image-face bracket — an upstream research constant, not
(yet) a `delta*_C` bracket.** `rho* in [0.160847, 0.405465]`
(`experimental/notes/thresholds/post_sweep_bracket_reconciliation.md` section 1,
confirmed unmoved by `experimental/notes/thresholds/post_sweep_reconciliation_c23dcaa.md`
section 6 / PR `#727`): lower end `0.160847` is the `b=24` stacked-trade
census champion, hardened by `#705` to a `k<=5` family ceiling; upper end
`0.405465=ln(3/2)` is DannyExperiments' `#668` canonical-transversal VC
compression bound. Both ends are unconditional *for the stacked-trade
family/VC-compression method*, but — per
`experimental/notes/thresholds/image_face_print_audit.md:1-26` — this is
explicitly "a note-level research abstraction that never entered the
manuscript": the `rho*`/ILO-moment/census/VC vocabulary has **no `tex`
consumer**, and the tex's own hard input 2 ("image-scale MI and MA or a
direct Sidon payment") remains open. Reported here because it is the closest
thing on the tree to a maintained two-sided numeric bracket in this research
program besides (A), but it should not be read as currently bounding
`delta*_C(2^-128)` — it is necessary-not-sufficient scaffolding for hard
input 2. Tightening either end means beating the `b=24`/`k<=5` census (lower)
or improving on the VC-compression argument (upper); *connecting* it to
`delta*_C` at all is an open wiring problem, not addressed by any packet in
section 2.

**Net "where bits come from next."** At the deployed/finite scale (A), it is
Open Problem `prob:band` on both sides. At the general/asymptotic scale (B),
it is agents.md's five hard inputs, and section 2 shows most of this wave's
real proof content lands on input 2 (`#717,#728,#729,#732,#735` in
particular chip real, proved structure off the signed-or-semantic
dichotomy), with the primitive Sidon/heavy-fiber-emission/concentration
residual still open. (C) is adjacent scaffolding for input 2 that has not yet
been wired to either (A) or (B).

---

## Files

- Note: `experimental/notes/audits/pay_per_bit_ledger_audit.md` (this).
- Verifier: `experimental/scripts/verify_pay_per_bit_ledger_audit.py`
  (stdlib-only, deterministic, `<60s`; `--check` recomputes every bit-margin
  number in section 1 by exact `Fraction`/high-precision `Decimal`
  arithmetic, checks every locally-cited file path exists, checks every
  open-wave PR's primary note file exists at its pinned head SHA via
  `git cat-file`, and validates the section-2 table's structure and totals
  against the JSON certificate; `--tamper-selftest` mutates one anchor, one
  numeric constant, and one JSON total and confirms detection).
- Certificate: `experimental/data/certificates/pay-per-bit-ledger-audit/certificate.json`.

## Nonclaims

This audit does not re-derive any cited theorem or note; every number is
checked against its printed/committed source, not rebuilt from first
principles. It does not decide the primitive Sidon payment, the
signed-or-semantic dichotomy, the deep-remainder scaling question, the Grand
List projective lift, or any other open route named in section 2 — it only
classifies existing packets under the pay-per-bit rule. Section 2's
classification is a one-line summary of each packet's own claim and is not a
substitute for reading the packet; where a packet's own scope note
(Nonclaims/Risk-limits) is more conservative than this table's one-liner, the
packet's own text controls. No `tex`/`pdf` file is touched by this packet.
