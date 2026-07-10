# Asymptotic RS-MCA profile-envelope draft — line-by-line audit

Status: `AUDIT`. Base commit `2acc7be` ("Promote profile-envelope asymptotic RS
MCA draft"). Target: `experimental/asymptotic_rs_mca.tex`, audited against
`experimental/cap25_cap_v13_raw.tex` (`Cho26CapV13`) and
`experimental/grande_finale.tex` (`Cho26Grande`).

Mandated vocabulary (`agents.md`, `eb42b82`): every claim ends as
`NO ISSUE` / `FIXED` / `OPEN GAP` / `COUNTEREXAMPLE_NEW_FLOOR` with tree-anchored
`file:label` / `file:line` references.

This packet is the successor to the two integrated pre-promotion audits of the
OLD compact draft — the closed-ledger citation audit
(`experimental/notes/asymptotic_rs_mca_closed_ledger_audit.md`) and the in-paper
proof audit (`experimental/notes/asymptotic_rs_mca_proof_audit_r2.md`). The
maintainer's ask, verbatim (ledger entry "Promoted profile-envelope replacement
draft"): *"Audit the new obstruction proof and the profile-envelope theorem
statement line by line ... check that every claimed cell payment is cited at the
right natural profile scale and that RC is not silently inferred from
support-pair estimates."* Both named traps are the spine of Half (B) below.

**Verifier.** `experimental/scripts/verify_profile_envelope_audit.py` (zero-arg,
stdlib-only, ~7 s) — `RESULT: PASS`: **13/13 gates, 12/12 live tamper tests**.
It rebuilds the smallest finite instances of the obstruction family in
`GF(11^2)`, `GF(11^4)`, `GF(13^2)`, `GF(17^2)`, `GF(23^2)` and gates every
checkable integer (fiber sizes, additive energies, difference-set sizes,
distinct MCA-slope counts, asymptotic scales), byte-checks the 25 resolved
citation heads in the two source manuscripts, and confirms the structural claims
(RC guard clauses, target-reserve placement, moduli-phantom absence). Data JSON:
`experimental/data/cap25_v13_profile_envelope_audit.json`.

---

## 0. Headline

The promoted draft is a **conditional profile-envelope compiler**. Its two
*unconditional* outputs are (i) the smooth-quotient/Sidon/MCA **obstruction**
(`thm:polynomial-obstruction`) and (ii) the high-energy Boolean-fiber
elimination (BSG + quasicube). The frontier formula is recovered only as the
**identity-dominant specialization** under explicit hypotheses.

- **Half (A) — the obstruction is a correct construction.** Every claimed number
  reproduces exactly at finite instances (verifier gates GA1–GA8). It is a
  genuine counterexample to identity-dominance, exactly as the paper intends —
  **no error found in the construction.** Verdict: `NO ISSUE` across all
  sub-claims.
- **Half (B) — the two named traps are correctly handled.** Cell payments are
  cited at their **natural profile scale** `barN_lambda = |Omega^0_lambda|
  |B_lambda|^{-R_lambda}`, never silently at the identity scale (the obstruction
  is itself the proof that this distinction is exponential). RC is **explicitly
  quarantined** from support-pair/max-fiber estimates by `def:ray-compiler`
  (L192) and `rem:q-sp-no-ray` (L695). Verdict on both traps: `NO ISSUE`.
- **The new draft repairs four of the five gaps the two predecessor audits
  flagged** (`FIXED`: C9 phantom moduli, B1 image-vs-ambient scale, A6 add-back,
  B4/A9 pole-collision loss).
- **Two new `OPEN GAP`s** (both minor, both repairable, neither fatal): the
  abstract's `target-reserve` hypothesis is never defined in the body (F-1); the
  CapV13 half of the C8 citation bottoms out in an *open problem*
  `prob:capfp-split` (F-2). One imported hypothesis (window uniformity) remains
  `OPEN GAP` as before.
- **No `COUNTEREXAMPLE_NEW_FLOOR`.** The obstruction is the paper's own intended
  counterexample; nothing here refutes a printed paper claim.

### Verdict tally

| verdict | count | items |
|---|---:|---|
| `NO ISSUE` | 13 | GA1–GA8 obstruction sub-claims; profile-scale trap; RC trap; identity-dominance consistency; frontier entropy algebra; collision-aware algebra |
| `FIXED` | 4 | C9 phantom moduli; B1 image/ambient scale; A6 add-back; B4/A9 pole-collision loss |
| `OPEN GAP` | 3 | F-1 target-reserve undefined in body; F-2 C8/CapV13 open-problem citation; B3 window uniformity (imported hypothesis, not discharged) |
| `COUNTEREXAMPLE_NEW_FLOOR` | 0 | — |

---

## 1. Half (A) — the obstruction proof, line by line

`thm:polynomial-obstruction` (L491–551) fixes `0<alpha<1/2`, `p` odd prime,
`n=2(p-1)`, `B_0=F_p`, `B=F_{p^2}`, `H<=B^x` of order `n`, `theta` a generator,
`D=theta H`; even `a` with `a/n->alpha`, `w` = largest even
`<= log_{|B|} binom(n,a)`, `k=a-w-1`. Each claimed quantity was rebuilt with
exact field arithmetic and gated.

| step (paper) | claim | verifier gate | verdict |
|---|---|---|---|
| L554–558 setup | `H^2=B_0^x`, squaring 2-to-1 on `D`, `D^2=theta^2 B_0^x`, order-4 roots of `1+X^2` lie in `H` (disjoint from the coset `D`) | GA1 (`GF(11^2)`: `\|D\|=20`, all square-fibers size 2, `D^2=theta^2 F_11^x`, 0 order-4 roots in `D`) | `NO ISSUE` |
| L563–566 locator | `Q_{S_E}=prod(X^2-y)`: odd-gap coeffs vanish, gap-`2j` coeff lies in `theta^{2j}B_0`; hence `<= p^{w/2}` prefixes | GA2 (all 210 supports at `p=11`; odd coeffs `=0`, `q_{2j}·theta^{-2j} in F_p`) | `NO ISSUE` |
| eq (5.2) | `log\|B\|=O(log n)`, `p>a`, `w=Theta(n/log n)`, `1<=barN_1<\|B\|^2` | GA8 (`p` up to 2003: `barN_1 in [1,\|B\|^2)` exact; `w` even; `w·log n/n` in a bounded band) | `NO ISSUE` |
| eq (5.3) fiber | `\|F_z\| >= binom(n/2,a/2) p^{-w/2} = exp((h(alpha)/4+o(1))n)` | GA3 (pigeonhole: `p=11 L=20`, `13 L=61`, `17 L=472`, `23 L=327/946`, each `>= ceil(barN_sq)`); GA8 (`(1/n)ln barN_sq -> h(0.4)/4=0.1683`) | `NO ISSUE` |
| L513–522 not id-dominant | `barN_sq = exp((h(alpha)/4)n)` while `barN_1 = e^{o(n)}`, so `Eprof_n(a) >= barN_sq` dominates | GA8 (`(1/n)ln barN_1 -> 0`; `ln(barN_sq/barN_1)/n -> h(alpha)/4>0`, ratio `-> inf`) | `NO ISSUE` (see finite-size note below) |
| eq (5.4) Sidon | `Delta(F_z) <= e^{-sigma n}` and `liminf (1/nr) log Gsid_{r,sigma} >= h(alpha)/4` | GA4 (`Delta(F_z)` = `0.128, 0.054, 0.015, 0.0074, 0.0039` — strictly decreasing toward 0; `Delta·L = O(1)` = Sidon scale) | `NO ISSUE` |
| eq (5.5)–(5.6) MCA | ext `F` with `\|F\|-n>k·binom(\|F_z\|,2)` gives `>= \|F_z\|` distinct MCA-bad slopes | GA5 (`GF(11^4)`: `20` distinct `gamma_S`, each a genuine MCA-bad witness; `P_S` deg `<=k`, divided difference deg `<k`; ext cond `14621>950`) | `NO ISSUE` |
| `cor:circle-obstruction` (L615) | diagonal equivalence to `RS_F(D,k)`; `k=2u+1`, both spaces dim `2u+1`; `(1+t^2)!=0` on `D` | GA7 (`k=5=2u+1`, `dim{f_0+y f_1}=5=k`, `1+t^2!=0` on all of `D`) | `NO ISSUE` |
| stabilizer remark (L642) | deleted support `{x_0} u {roots}` has trivial mult. stabilizer; Sidon-heavy fiber persists; `binom(n,a+1)\|B\|^{-w}=e^{o(n)}` | GA6 (`p=11`: stabilizer `={1}` incl. `-1` fails; fiber `12 >= ceil(11.45)`; `Delta` small; quasicube holds) | `NO ISSUE` |
| §4 BSG+quasicube | `\|A-A\| >= \|A\|^{3/2}` for every Boolean `A`; large fiber forces low energy | GA3/GA4/GA6 (`\|F_z - F_z\| >= ceil(\|F_z\|^{3/2})` in every instance, incl. the deleted-support fiber) | `NO ISSUE` (matches predecessor A4) |

**Finite-size note (not a defect).** The asymptotic separation
`barN_sq >> barN_1` is an `exp(Omega(n))` statement whose `o(n)` term is really
`O(log p)`; at the smallest enumerable `n` this term is not yet negligible, so
`barN_sq/barN_1` is non-monotone and even `<1` at some `(p,a)` with `w` capped at
2 (e.g. `p=13,a=10` gives ratio `0.9`). The separation is unambiguous exactly
where `w` first reaches 4: `p=23, a=14, w=4` gives `barN_1 = 1.47`,
`barN_sq = 322` — **ratio 219** — and GA8 shows `ln(ratio)/n -> h(alpha)/4` as
`p` grows. This is an artifact of finite scale, not of the construction, and is
recorded so a reader is not surprised by the small-`n` numbers.

**Half (A) verdict: `NO ISSUE`.** The obstruction, the circle corollary, and the
stabilizer-deletion remark are a correct construction. Every finite instance
reproduces; every asymptotic scale converges to the printed exponent.

---

## 2. Half (B) — profile-envelope statement, citations, RC, hypotheses

### 2.1 Trap 1 — "every cell payment at the right natural profile scale": `NO ISSUE`

The draft's payment convention is scale-correct by construction:

- The natural profile average is defined once, `barN_lambda = |Omega^0_lambda|
  |B_lambda|^{-R_lambda}` (L104–105), and the envelope
  `Eprof_n(a) = 1 + (n-a+1) + sup sum_lambda barN_lambda` (eq 1.1, L112) sums
  those **per-profile** averages at each profile's **own** coefficient field
  `B_lambda` and prefix depth `R_lambda`.
- `def:cells` (L132): *"A nonprimitive algebraic cell is paid ... if its
  **distinct-slope image** is at most its printed **natural-profile budget** ...
  Only in an identity-dominant window may this be specialized to the identity
  budget."* `thm:closed-ledger-package` (L206) repeats: *"every profile is
  charged at its natural scale in eqref{eq:profile-envelope}."*
- The obstruction is precisely the theorem that this matters: the square-quotient
  cell's natural scale `barN_sq = binom(n/2,a/2)|B_0|^{-w/2}` is
  `exp((h(alpha)/4)n)`, exponentially above the identity scale `barN_1`. Charging
  it at the identity scale would undercount by `exp(Omega(n))`. GA8 gates the gap.

Citation resolution (subagent sweep + spot byte-checks, all confirmed in-source,
zero line drift from the predecessor map): the 12 bracket citations of
`thm:closed-ledger-package` resolve to **real labels at natural-profile (a) or
exact-slope (c) scale** — e.g. C1 `thm:exact-quotient-image-lcm-ledger`
(`CapV13:1872`, exact image count), C3 `thm:capf-planted` (`CapV13:6060`,
own-order `binom(n/M-1,k/M)`), C4/C6 exact distinct-slope/degree counts, C8
`prop:base-field-floor` (`Grande:1494`, literal `binom·|B|^{-(d_1-1)}`), C9
`thm:fourier-flat-q` (`Grande:916`). None charges a cell at the identity scale.
`NO ISSUE`.

One scale nuance worth recording (not a defect): C1's
`prop:divisor-union-support-ledger` (`CapV13:1346`) is a **raw support count**
(scale d), and C7's `thm:saturation` (`Grande:1811`) is a support→ray **bridge**
identity. The paper never treats these support counts *as* slope counts — the
binding payment in `def:cells` is the distinct-slope image, and the support→slope
conversion is quarantined into RC (see 2.2). Consistent.

### 2.2 Trap 2 — "RC not silently inferred from support-pair estimates": `NO ISSUE`

The draft is scrupulous here; the trap is explicitly guarded in three places
(verifier GB4 gates their presence):

- `def:ray-compiler` (L192–199) **defines** RC and then adds the guard: *"A
  max-fiber or support-pair estimate alone is **not RC**: it counts supports or
  pairs, not the image of the witness incidence in slope space."*
- `rem:q-sp-no-ray` (L695–701): *"The preceding lemma is a support-pair
  identity, **not a ray compiler**. Keeping the same fibers `N(s)`, an abstract
  incidence can assign distinct slopes to selected supports or assign one slope
  to all of them without changing `max_s N(s)` or `sum_s N(s)^2`. An RS numerator
  bound therefore requires the additional algebraic projection estimate RC."*
- `thm:upper` proof (L712–719) uses this honestly: primitive leaves give Q
  (`thm:primitive-q`) → add-back (`lem:addback`) → the SP second moment
  (`lem:q-sp`) — and then *"By `rem:q-sp-no-ray`, this **does not itself bound
  slopes**. **RC supplies** the required slope-image estimate."* RC is a named,
  separate hypothesis of both `thm:upper` (L704) and `thm:frontier` condition (i)
  (L273).

I traced every use of `N(s)`/second-moment/support-pair in the compiler and
found **no step where a distinct-slope (numerator) conclusion is drawn from a
support-pair or max-fiber count without RC**. The lower-bound constructions
(`thm:polynomial-obstruction`, `prop:collision-aware-lower`) produce genuinely
distinct slopes `P_S(lambda)` directly (GA5 confirms 20 distinct values), never
from a support count. `NO ISSUE` — in fact `rem:q-sp-no-ray` was *added* to make
this non-inference explicit, which is a strength.

Honest-scope corollary: RC is a **hypothesis**, not discharged for
higher-dimensional residual charts (the C8 line L171: *"Every higher-dimensional
residual chart requires a direct distinct-ray estimate"*, and the closing remark
L798 lists *"a higher-dimensional transverse-ray compiler"* as a remaining
requirement). `thm:upper`/`thm:frontier` are therefore correctly `CONDITIONAL`
on RC.

### 2.3 Predecessor gaps repaired by the new draft: 4 × `FIXED`

| old finding | old verdict | new-draft state | verdict |
|---|---|---|---|
| C9 Sidon routing cited to absent moduli manuscripts `Cho26ModuliSelf/Final` (closed-ledger audit §2, FINDING-1) | `PHANTOM` | Moduli citations **removed entirely** (bibliography now 6 real entries, GB3); the Sidon cut / energy extraction / BSG+quasicube are **proved in-paper** §3–§4; C9 cites only real `Grande:916,949` for supporting Fourier-flat context | `FIXED` |
| B1 image (`L=\|im Phi\|`) vs ambient (`Q^{-w}binom Nm`) normalization mismatch in the cited Fourier-flat Q | `FOUND-WEAKER` | The in-paper primitive-Q chain (`lem:moment-max`→`thm:primitive-q`) runs **consistently at the image scale** `barN=M/L`; the residual-to-full bridge `M_lambda/L_lambda <= exp(o(n)) barN_lambda` is now a **printed hypothesis** of `def:closed-ledger` (L179–183); the draft explicitly flags the caveat at L244–246 | `FIXED` |
| A6 `lem:addback` presents an uncited profile decomposition as proved | `OPEN GAP` | `lem:addback` (L668) now derives its bound **from** *"the residual-to-full comparison in `def:closed-ledger`"* + the stated `exp(o(n))`-many-profiles hypothesis — honestly `CONDITIONAL`, no longer asserted | `FIXED` |
| B4/A9 lower-side "pole-reservoir regime" collision loss asserted with no proof/citation | `FOUND-WEAKER`/`OPEN GAP` | Replaced by `prop:collision-aware-lower` (L723) with an **explicit quantitative bound** eq (7.1) `ceil(L(q-n)/(q-n+k(L-1)))` via Cauchy–Schwarz; the unsupported phrase "pole-reservoir" is **gone**; eq (7.1) is byte-for-byte `Grande` `thm:simple-pole-list-floor` (`Grande:243`) and matches the averaging at `Grande:1567` | `FIXED` |

Verifier support: GB1 checks the eq (7.1) Cauchy–Schwarz algebra identity and
that the formula reproduces the GA5 instance exactly (`ceil(20·14621/14716)=20` =
the 20 distinct slopes found). GB3 confirms the moduli phantom is absent and the
three collision-aware source labels exist at their lines.

### 2.4 New findings (this audit)

#### F-1 — `target-reserve` hypothesis named in the abstract but undefined in the body: `OPEN GAP`

The abstract (L51) promises *"the identity formula is recovered only under
explicit identity-dominance and **target-reserve** hypotheses."* But
`target-reserve` **appears nowhere else in the paper** (verifier GB5:
`target-reserve` count = 1, in the abstract only; 0 in the body). By contrast
`identity-dominant` **is** defined (`\emph{identity-dominant}`, L119) and used
consistently (L141, L209, L299, L314, L327, L521, L794).

The load-bearing content the name should attach to is present and consistent —
`thm:frontier` condition (i) (L273) `kappa_n Eprof_n(a_{+,n}) <= T_n` with
`T_n=floor(eps_n|F_n|)` (L263), and `tau_n=(1/n)log_2(1+T_n)` (L301) — i.e. the
target budget reserving room above the envelope. This is a **naming/exposition**
gap, not a mathematical error: a reader cannot locate the hypothesis the abstract
names.

**Repair.** Christen condition (i)'s `kappa_n Eprof_n(a_{+,n}) <= T_n` (or the
`T_n=exp(o(n))` premise of eq 1.4) as the *target-reserve* hypothesis with a
one-line labelled definition, or drop the word from the abstract.

#### F-2 — C8's CapV13 companion citation bottoms out in an OPEN PROBLEM: `OPEN GAP`

The C8 paragraph (L238) cites *"`[rank-one and split-pencil reductions]
{Cho26CapV13}`"*. Its section (`CapV13:7627`) does contain proved reductions
(`lem:capfp-autodiv` 8405, `lem:capfp-unimodular` 8413, `prop:capfp-detrep`
8421), **but it terminates in an unproved `remark[Primitive split-pencil
formulation]` `\label{prob:capfp-split}` (`CapV13:8433`)** whose text literally
begins *"... **Prove** ..."* and whose target bound `<= e^{o(n)}max(1,binom(n,w)
q^{1-w})` uses the **ambient `q`** (scale (b)) and is *not established*. A sibling
`prob:capfp-balanced` (`CapV13:8380`) has the same character. GB3 byte-checks that
`prob:capfp-split` is indeed a `remark`/open problem at `CapV13:8433`.

Severity is **low**, for two independent reasons the paper already builds in:
(i) the paper writes *"**developed** in ..."* for this citation (L238), not
"proved" — the softer verb is exactly correct; (ii) the proved half of C8 is the
`Grande` moving-root theorem `thm:bc-moving-root` (`Grande:1735`) +
`cor:bc-one-pencil` (`Grande:1764`), and everything higher-dimensional is
explicitly deferred to **RC** (L171). So C8 does not *rest* on the open problem.

**Repair.** Narrow the CapV13 C8 sub-citation to the three proved lemmas
(`8405/8413/8421`), or annotate that its terminal `prob:capfp-split` is an open
problem targeting ambient scale (subsumed by RC), so no reader mistakes the
section for a complete proof.

(Incidental, not a finding: `thm:capfr1-near-rational-dichotomy` (`CapV13:7916`)
has a verbatim-content duplicate `thm:capfp-dichotomy` (`CapV13:8352`) — harmless
duplication in the source, noted for the maintainer.)

#### B3 — window uniformity remains an imported hypothesis: `OPEN GAP` (unchanged)

`thm:frontier` still assumes `kappa_n=exp(o(n))` dominating the compiler losses
*"uniformly in the window under consideration"* (L263). As the predecessor B3
recorded, the per-cell ledgers are stated at a **fixed** agreement, and Grande's
own `thm:asymptotic-rs-mca-closure-combined` (`Grande:2298`) makes the same
move — so the assumption is imported **consistently and honestly**, but neither
manuscript **discharges** it. No regression; still `OPEN GAP`.

### 2.5 Statement-level algebra checks: `NO ISSUE`

- **Frontier entropy algebra** (`thm:frontier` proof L761–786): `log_2 barN_{n,a}
  = n(H_2(rho+g)-beta g)+o(n)`; `F_n(g)` concave with `F_n(0)=H_2(rho)>0`; single
  crossing; superlevel set `[0,g*]`; target crossing `g_{T,n} -> g*` as
  `tau_n -> 0`. GB2 recomputes `g*(rho,beta)` at four `(rho,beta)` pairs and the
  target-crossing limit. Matches predecessor A10. `NO ISSUE`.
- **`lem:moment-max`, `lem:q-sp`, `lem:first-match`, BSG/quasicube** — unchanged
  from the OLD draft; predecessor proof audit found them `NO ISSUE` (A1, A2, A4,
  A7); the Boolean quasicube application is re-gated here (GA4). `NO ISSUE`.
- **`prop:collision-aware-lower` algebra** (L739–759): the pigeonhole `L`
  supports, the pole-averaging `sum m_i^2 <= L + kL(L-1)/(q-n)`, and Cauchy–Schwarz
  `L^2 <= M sum m_i^2` reproduce eq (7.1). GB1 verifies the identity. `NO ISSUE`.

---

## 3. Ready-to-paste ledger entries (proposed; NOT applied to the paper)

Per the ledger's file convention, proposed paper changes live here as
`Source / Status / Paper impact / Next action` blocks. Neither
`asymptotic_rs_mca.tex` nor its PDF is touched by this packet.

### Ledger entry F-1 (target-reserve)

- **Source:** profile-envelope audit `asymptotic_profile_envelope_audit.md` (F-1),
  verifier gate GB5.
- **Status:** `OPEN GAP` (naming/exposition; not a math error).
- **Paper impact:** The abstract (L51) names a *target-reserve* hypothesis that is
  never defined or labelled in the body; the load-bearing content is
  `thm:frontier` condition (i) `kappa_n Eprof_n(a_{+,n}) <= T_n` and the
  `T_n=exp(o(n))` premise of eq (1.4).
- **Next action:** Add a one-line labelled definition christening condition (i)
  (and/or the `T_n=exp(o(n))` premise) as *target-reserve*, or remove the word
  from the abstract so every named hypothesis resolves.

### Ledger entry F-2 (C8 CapV13 open-problem citation)

- **Source:** profile-envelope audit `asymptotic_profile_envelope_audit.md` (F-2),
  verifier gate GB3.
- **Status:** `OPEN GAP` (low severity; the paper's "developed" wording + RC
  deferral already contain it).
- **Paper impact:** The C8 bracket *"[rank-one and split-pencil reductions]
  {Cho26CapV13}"* (L238) points at a section whose deepest content is the
  **unproved** `prob:capfp-split` (`CapV13:8433`), target at ambient scale (b).
- **Next action:** Narrow the sub-citation to the proved lemmas
  (`CapV13:8405/8413/8421`), or annotate that `prob:capfp-split` is an open
  problem subsumed by RC. Optionally note the `7916`/`8352` duplicate theorem.

---

## 4. Nonclaims

- A `NO ISSUE` verdict means the printed step survived a genuine attempt to break
  it **under the paper's stated hypotheses**; it does **not** re-verify the
  internal proofs of the imported `Cho26CapV13`/`Cho26Grande` results, nor of BSG
  or the quasicube theorem (their **stated forms** and the Boolean **application**
  are checked; the application is gated exactly).
- A `FIXED` verdict records that the new draft **repairs** a gap the two
  predecessor audits flagged in the OLD draft; it does not certify that the
  resulting hypothesis is *discharged* — `def:closed-ledger`'s residual-to-full
  comparison, RC, and window uniformity remain **hypotheses**. The frontier
  theorem is `CONDITIONAL`, exactly as printed.
- The finite instances (`p in {11,13,17,23}`, `GF(11^4)`) are **illustrative
  replications** of the obstruction's integer content, not proofs of its
  asymptotic statements; they gate the specific arithmetic each step relies on.
  The `exp(-sigma n)` Sidon form and the `exp(Omega(n))` separation are
  asymptotic; they are evidenced at finite scale by the strictly decreasing
  `Delta(F_z)` and the `w=4` separation (ratio 219 at `p=23`), and by GA8's
  convergence `(1/n)ln barN_sq -> h(alpha)/4`.
- No `COUNTEREXAMPLE_NEW_FLOOR`: the obstruction is the paper's **own** intended
  counterexample to identity-dominance; this audit found no error refuting a
  printed paper claim.
- This note lives under `experimental/notes/audits/` labelled `AUDIT`; it makes
  **no** promotion or merge recommendation. That decision is the maintainer's;
  this packet is collaborative input to it.

## 5. Files

- note: `experimental/notes/audits/asymptotic_profile_envelope_audit.md` (this)
- verifier: `experimental/scripts/verify_profile_envelope_audit.py` (13 gates, 12
  tamper tests, ~7 s, `RESULT: PASS`)
- data: `experimental/data/cap25_v13_profile_envelope_audit.json`
- audited: `experimental/asymptotic_rs_mca.tex` `@2acc7be`, against
  `experimental/cap25_cap_v13_raw.tex`, `experimental/grande_finale.tex`
- predecessors (OLD draft): `experimental/notes/asymptotic_rs_mca_closed_ledger_audit.md`,
  `experimental/notes/asymptotic_rs_mca_proof_audit_r2.md`
