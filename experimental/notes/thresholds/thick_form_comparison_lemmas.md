# Thick-form comparison lemmas for the minimal phase supplement

## Status

`(L1-cmp)^thick RE-DERIVED: STRICT-WEAKNESS SURVIVES (AUDIT) /
(L2-cmp)^thick RE-DERIVED: ORTHOGONALITY TRANSFERS (PROVED)`.

DannyExperiments' **PR #629** (`agent/minimal-phase-multiplicity-repair`, head
`62b1d764454004a935f3f14c094e61d6e1567780`, OPEN upstream, consumed here at that
SHA) proved the **set-dodged** supplement `(S_E)` of our **PR #614**
(`minimal_phase_supplement.md`) *insufficient*: the character frame controls the
`r_A`-multiplicity-**weighted** trace, not unweighted band energy, and his GF(16)
weighted-RS regression has set-dodged band energy **zero** while `L/Q =
e^{-Omega(N)}`. His repair installs the **multiplicity-thick** supplement (his
`(C4)/(C5)`). We validated and adopted that correction on the PR
(`issuecomment-4945602578`).

The full-spectrum chain (#622/#625/#626/#627/#635/#636) uses no band
decomposition and is unaffected. What #629 did **not** re-derive is the two
**comparison lemmas**, proved in #614 for the *set-dodged* form only:

- **(L1-cmp)** `(S_E)` is strictly weaker than scottdhughes's signed multilevel
  large sieve `(LS)` (#564);
- **(L2-cmp)** `(S_E)` is orthogonal to the LegaSage C9 max-fiber razor (#585):
  a razor **NO** does not decide the image clause (witness: the block-parabola).

This packet re-derives both against the thick form `(S_E)^thick`. Every number
is recomputed by `experimental/scripts/verify_thick_form_comparison.py`
(stdlib-only, `RESULT: PASS (27/27)`, ~2 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **COMPUTED** (exact finite
witness in the verifier), **MEASURED** (exact finite toy, asymptotics not proved
from it), **AUDIT** (interface reading of a sibling note / of `(LS)`'s stated
form), **OPEN**.

Credit. The thick correction `(C1)-(C6)` is **DannyExperiments' PR #629**
(consumed at the head SHA above). `(LS)` is **scottdhughes' PR #564**. The
block-parabola family and `(CF1)/(CF2)/(CF3)` are **avdeevvadim's PR #558**. The
set-dodged `(S_E)`, the master identity, and the two original comparison lemmas
are our **PR #614** (built on **#609** `frame_image_completion.md`).

---

## R1 — exact statements consumed (verbatim anchors)

All line numbers are in the worktree tip `8264eae` (pre-#629), except `(C1)-(C6)`
which are quoted from the #629 diff at head
`62b1d764454004a935f3f14c094e61d6e1567780`.

**Frame Gram matrix and its norm** — `asymptotic_primitive_profile_character_frame_v1.md`:

- `K_A(gamma,gamma') = hat_mu(gamma' gamma^{-1})` (**L91**); `kappa := ||K_A||_op`.
- `(CF1)`: `|F_z| <= M ||K_A||_op / |A| = (L ||K_A||_op / |A|) barN` (**L97-99**).
- `(CF2)`: `|A| >= exp(-o(N)) L` and `||K_A||_op <= exp(o(N))` (**L105-107**).
- `(CF3)` converse guardrail: `||K_A||_op >= |A| mu(z)` (**L154**), hence
  `L ||K_A||_op / |A| >= L max_z mu(z)` (**L162**). Taking `z = argmax` and
  `max_z mu(z) >= 1/L` gives `kappa >= a/L`, i.e. **`a <= kappa L`** — the leak.

**Old set-dodged supplement `(S_E)`** — `minimal_phase_supplement.md` **L118-122**:

> aggregate dodged-band spectral energy is subexponential,
> `Sum_{chi in V_g^ \ (A-A)} |hat_mu(chi)|^2 <= e^{o(N)}`,

with master identity `E = Sum_{chi != 0} |hat_mu(chi)|^2 = A_eff*P2 - 1` and
`L >= A_eff/(1+E)` (**L104-113**, `(MASTER)`; PROVED, verifier BLOCK A).

**Thick supplement `(S_E)^thick`** — #629 diff, `minimal_phase_supplement.md`
new hunk (the `(C1)-(C5)` block). Write `a = |A|`, `kappa = ||K_A||_op`,
`r_A(xi) = #{(gamma,gamma') in A^2 : gamma'-gamma = xi}`. For `tau >= 1`,

```text
D_tau(A)  = { xi != 0 : r_A(xi) >= a/tau }               (thick band)
Sigma_tau = Sum_{xi != 0, r_A(xi) < a/tau} |hat_mu(xi)|^2 (thin-band energy)

(C1)  tr(K_A^2) = Sum_xi r_A(xi) |hat_mu(xi)|^2 <= kappa*a
(C2)  Sum_{xi in A-A} |hat_mu(xi)|^2 <= kappa*a <= kappa^2*L
(C3)  Q <= kappa^2*L^2 + (1+sigma)*L                     (=> only L = Q^{1/2} e^{o(N)})
(C4)  if Sigma_tau <= sigma:  E_nt <= tau*kappa + sigma,  L >= Q/(1 + tau*kappa + sigma)
(C5)  if also a >= L/eta:     max_z mu(z) <= eta*kappa*(1 + tau*kappa + sigma)/Q
```

> **`(S_E)^thick` (the live supplement, #629).** *There is a subexponential
> threshold `tau = e^{o(N)}` for which the multiplicity-dodged (thin-band) energy
> `Sigma_tau <= e^{o(N)}`.* Given the frame (`kappa = e^{o(N)}` from `(CF2)`) and
> the image density (`eta = e^{o(N)}`), `(C4)/(C5)` then deliver both the image
> clause and the ambient max-fiber output.

The energy on the **thick** band is free: for `xi in D_tau(A)`,
`|hat_mu(xi)|^2 <= (tau/a) r_A(xi) |hat_mu(xi)|^2`, so by `(C1)`
`Sum_{D_tau} |hat_mu|^2 <= (tau/a) tr(K_A^2) <= tau*kappa`. Thus
`E_nt = Sum_{D_tau} + Sigma_tau <= tau*kappa + Sigma_tau` — this is `(C4)`,
recomputed in verifier BLOCK D.

**`(LS)`** — scottdhughes #564, as read in
`experimental/notes/audits/character_frame_hypothesis_audit.md` **L191, L194-205**:
an **ambient** (`p^w`-normalized) **signed multilevel large sieve** that
**requires** `p^{w/2}` (square-root) cancellation — "every absolute-value method
is provably sign-blind here" — targeting the **sharp polynomial** `N <= n^3`.
It is signed and sharp; `(S_E)`/`(S_E)^thick` are absolute (`L^2`,
magnitude-squared) and only subexponential.

**Razor predicate** — LegaSage #585, as read in `minimal_phase_supplement.md`
**L211-224** and `character_frame_hypothesis_audit.md` **L192**: the
**image-normalized max-fiber** question — *does a near-Sidon exp-large `R=2`
fiber exist?* A razor **NO** = no such fiber = `max_s f_s <= e^{o(N)} barN^img`
(image-normalized Q holds). It is blind to the span-normalized image size `L`
vs `A_eff`.

`(C1)-(C6)` are reproduced (weighted-trace identity, the `(C2)/(C3)` leak, the
`(C4)/(C5)` sufficiency, and the GF(16) regression) in verifier BLOCKS B-E; they
match #629 exactly (`gf16_rank=14`, `gf16_weight4_image=1365`).

---

## R2 — (L1-cmp)^thick: `(S_E)^thick` vs `(LS)` — STRICT-WEAKNESS SURVIVES (AUDIT)

**Verdict.** `(S_E)^thick` remains **strictly weaker** than `(LS)`. The thickening
moves the object strictly **up** the lattice toward `(LS)` (it now controls the
low-multiplicity interior the set-dodged form missed) but **not all the way**:

```text
  set-dodged (S_E)   <   (S_E)^thick   <   (LS)
     (insufficient,      (the live         (signed, sharp,
      #629)              supplement)        square-root cancellation)
```

### R2.1 `(LS) => (S_E)^thick` — holds, by the SAME reduction as the set-dodged form (AUDIT)

The concern the thick form raises: `Sigma_tau` selects its band by the
`r_A`-multiplicities of the frame `A`, which `(LS)` (a statement about `mu`
alone) never sees. **This does not break the implication**, because `Sigma_tau`
is *unweighted* energy on a *subset* of the nontrivial band:

```text
Sigma_tau = Sum_{xi != 0, r_A(xi) < a/tau} |hat_mu(xi)|^2
         <= Sum_{xi != 0} |hat_mu(xi)|^2  =  E      for every A and every tau.
```

(Verifier BLOCK G: `Sigma_tau <= E` over 270 random `(mu, A, tau)`.) Hence

```text
(LS) => E <= e^{o(N)}   ==>   Sigma_tau <= E <= e^{o(N)}   (take tau = 1),
```

so **`(LS) => (S_E)^thick` reduces to exactly the old `(LS) => (S_E)` claim** of
#614 §3.1 — no new burden. That claim is itself **AUDIT**: it reads `(LS)`'s
sharp signed control (or, under the large-sieve-inequality reading, its ambient
`Sum |hat_mu|^2` bound) as dominating the crude absolute `L^2` energy `E`. The
thickening is *monotone below `(LS)`* and inherits this status unchanged. Label:
**AUDIT** (unchanged from #614 §3.1; the multiplicity weighting is inert here
because the thin band is a subset of the full band).

### R2.2 `(S_E)^thick =/=> (LS)` — REFUTED by an exact witness (COMPUTED)

Where #614 §3.1 merely asserted "the reverse fails," the thick form is refuted
by a concrete family (verifier BLOCK F). Take `G = Z_n`, `H = d*Z_n` the index-`d`
subgroup, `mu` **uniform on `H`**. Then

```text
hat_mu = indicator of H^perp   (H^perp = multiples of n/d, |H^perp| = d),
E = Sum_{chi != 0} |hat_mu|^2 = |H^perp| - 1 = d - 1.
```

- **`(S_E)^thick` side (COMPUTED).** `E = d-1`. For the scaling family
  `G = Z_{d^s}` (any fixed `d`, `s -> inf`, `N ~ s`), `E = d-1` is **constant**,
  hence `e^{o(N)}`; so `Sigma_tau <= E = e^{o(N)}` for every `A, tau` — the thick
  supplement holds (indeed the image is large, `L = |H| = Q/d`, so this is a
  *good* profile). Verifier BLOCK F: `E = d-1` exactly for
  `(n,d) in {(9,3),(8,2),(25,5),(27,3),(16,2),(49,7)}`.
- **`(LS)` side (AUDIT).** At each nontrivial `chi in H^perp`, `|hat_mu(chi)| = 1
  = p^0` — the **maximum**, zero decay; and the matched-sign sum over `H^perp`
  equals `|H^perp| = d`, versus the `sqrt(d)` a `p^{w/2}` cancellation would
  force. The subgroup measure is the canonical **coherent** object; it maximally
  violates `(LS)`'s stated square-root-cancellation requirement. Verifier BLOCK
  F prints `coherent = d >> sqrt(d)` and `max|hat_nt| = 1` on every row.

So a legitimate, well-imaged profile satisfies `(S_E)^thick` yet violates `(LS)`.
**`(S_E)^thick =/=> (LS)`.** Label: **REFUTED** — COMPUTED on the `(S_E)^thick`
side, AUDIT on the `(LS)`-violation side (it rests on `(LS)`'s stated
sqrt-cancellation form, not on #564's primary text).

### R2.3 the thickening is strictly between the two endpoints

`(S_E)^thick => (S_E)^set-dodged` (the outside-`A-A` band is a subset of the thin
band, so `Sum_{outside A-A} <= Sigma_tau`), and the converse fails by #629's
leak — see R4 / BLOCK I. Combined with R2.1-R2.2:
`set-dodged < thick < (LS)`, all three strict. **Net R2 verdict: strict-weakness
SURVIVES the thickening.** Overall label **AUDIT** (one direction rests on
`(LS)`'s audit reading), with the refutation direction now witness-backed —
a strict upgrade over #614's bare assertion.

---

## R3 — (L2-cmp)^thick: `(S_E)^thick` vs the C9 razor — ORTHOGONALITY TRANSFERS (PROVED)

**Verdict.** A razor **NO** still does **not** imply `(S_E)^thick`: the #614
block-parabola witness transfers verbatim, and *more robustly* than before,
because its thick split is exactly computable and its failure of `(S_E)^thick` is
forced for **every** frame `A` and threshold `tau`.

### R3.1 the block-parabola thick split (PROVED / COMPUTED)

The block-parabola profile has `A_eff = p^{2k}`, `L = M = p^k`, `E = p^k - 1`,
with per-block Gauss factor `phi(a,b)` satisfying `phi(0,0)=1`, `phi(a,0)=0`
(`a != 0`), `|phi(a,b != 0)| = p^{-1/2}` (verifier BLOCK 1 of the #614 verifier;
reused). The frame the razor pairs with it is avdeev's packing
`A_k = {(a_1,0,...,a_k,0)}` (the `b=0` subspace), with `K_{A_k} = I`,
`kappa = 1`, `|A_k| = p^k = L`, `kappa_frame = 1` (#609; #614 BLOCK 5).

Its multiplicities are exact: `A_k - A_k = {b=0 subspace}`, a subgroup of order
`p^k`, so

```text
r_A(xi) = p^k   if every b_i = 0 ;   r_A(xi) = 0   otherwise.
```

But **every** energy-carrying character of the parabola has some `b_i != 0`
(else a block contributes `phi(a_i,0) = 0` and kills `hat_mu`). Therefore:

```text
thick band D_tau(A_k) = {b=0 subspace}  carries ZERO energy
   (there hat_mu = prod phi(a_i,0) = 0 for xi != 0),
thin band              carries the FULL energy  Sigma_tau = E = p^k - 1.
```

Verifier BLOCK H, `(p,k) in {(3,1),(3,2),(5,1),(5,2),(7,1),(3,3)}`: `thick_E =
0` (numerically `~1e-32`), `thin_E = p^k - 1` exactly. So `(S_E)^thick` is
**violated** (`Sigma_tau` exponential) for every subexponential `tau`, while the
parabola is a razor **NO** (all fibers size 1, `max_s f_s = 1 = barN^img`,
`kappa_img = 1`) and the image collapses (`L/A_eff = p^{-k}`). **Razor NO
=/=> `(S_E)^thick`.** Label: **PROVED** (exact multiplicities) / **MEASURED**
(finite `(p,k)` grid; the `p^k` closed forms are proved).

### R3.2 no frame `A` rescues the witness (PROVED)

The conclusion does not depend on the choice `A_k`. Suppose some frame `A`
placed a positive fraction of the parabola's energy on its **thick** band. By
`(C1)`,

```text
kappa*a >= Sum_{D_tau(A)} r_A(xi)|hat_mu|^2 >= (a/tau) Sum_{D_tau(A)} |hat_mu|^2
        = (a/tau)(E - Sigma_tau),
```

so `kappa*tau >= E - Sigma_tau`. Hence if `Sigma_tau = e^{o(N)}` (thin route
controlled) then `kappa*tau >= E - e^{o(N)} = e^{Theta(N)}`, forcing
`kappa` or `tau` exponential — violating the `(S_E)^thick` requirement
`kappa, tau = e^{o(N)}`. **Either way `(S_E)^thick` fails.** This is precisely
the contrapositive of #629's `(C4)` sufficiency (`(S_E)^thick => image clause`,
and the parabola violates the image clause), now made concrete: the block
parabola violates `(S_E)^thick` **for all `A, tau`**, so the razor-NO /
image-collapse coexistence is frame-independent. Label: **PROVED**.

### R3.3 orthogonality is intact

The razor is an image-normalized max-fiber (`max mu`) predicate; `(S_E)^thick`
is a span-normalized spectral-energy-plus-multiplicity predicate. They are
separated by the #609 factor `A_eff/L`, exactly as the set-dodged form was
(#614 §3.2). The block-parabola populates the `(razor NO, (S_E)^thick fail)`
corner; nothing in the razor bounds `Sigma_tau`, and nothing in `Sigma_tau`
bounds `max mu`. **Orthogonality TRANSFERS.** Label: **PROVED** for the named
direction (razor NO =/=> `(S_E)^thick`); full four-corner independence is
**AUDIT** (as in #614).

---

## R4 — reproduced numbers (consumed checks)

`experimental/scripts/verify_thick_form_comparison.py`, `RESULT: PASS (27/27)`:

| block | content | key numbers |
|-------|---------|-------------|
| A | master identity `L >= A_eff/(1+E)`, `E = A_eff*P2 - 1` | Parseval + CS, uniform `E=0` |
| B | `(C1)` `tr(K_A^2) = Sum_xi r_A(xi)|hat|^2 <= kappa*a` | exact identity, `Z_5..Z_11` |
| C | `(C2)/(C3)` leak `kappa*a <= kappa^2*L`, `kappa >= a/L` | the square-root-scale loss |
| D | `(C4)/(C5)` thick sufficiency | `E_nt <= tau*kappa+Sigma_tau`, `L >= Q/(1+..)` |
| E | `(C6)` GF(16) RS regression | `rank=14`, `image=C(15,4)=1365`, `Q=2^14=16384`, `log2(L/Q)=-3.5853`, `h(1/4)=0.8113`, coeff `-0.1887` |
| F | R2 subgroup witness | `E=d-1`; coherent sum `= d`; `sqrt(d)`; `max|hat_nt|=1` |
| G | R2 monotone `Sigma_tau <= E` | 270 `(mu,A,tau)` trials |
| H | R3 block-parabola thick split | `thick_E ~ 1e-32`, `thin_E = p^k-1`, `kappa_img=1`, `L/A_eff=p^{-k}` |
| I | lattice: set-dodged `<` thick | Singer `{1,2,4} in Z_7`: `A-A=Z_7`, `r_A=1`, set-dodged `=0`, `Sigma_tau=E=2.5` |

Danny's `verify_minimal_phase_multiplicity_repair.py` was additionally run
verbatim from a scratch copy as a consumed cross-check: `RESULT: PASS`,
`gf16_rank=14`, `gf16_weight4_image=1365` — matching BLOCK E.

**#629's leak, hand-checkable (BLOCK I).** The Singer difference set
`A = {1,2,4} subset Z_7` has `A-A = Z_7` (every nonzero difference once,
`r_A(xi)=1`), so the set-dodged band (outside `A-A`) is **empty**: set-dodged
energy is `0` for *every* measure. But every nonzero character is thin
(`r_A = 1 < a/tau`), so `Sigma_tau = E`. A measure with `E > 0` (e.g. supported
on `{0,1}`, `E = 2.5`) then **satisfies set-dodged (`=0`) yet violates thick** —
the GF(16) phenomenon in seven points. This certifies `set-dodged < thick`
strictly.

---

## R5 — paste-ready replacement for §3.1-§3.2 of `minimal_phase_supplement.md`

Apply **on top of #629** (which owns that note; do not edit it here). Replace the
two subsections `### 3.1 ...(LS)...` and `### 3.2 ...razor...` and their two
Verdict-ledger rows with the following. It uses `(S_E)^thick` throughout and
leaves the retracted set-dodged `(S_E)` only as the historical lower endpoint.

<!-- BEGIN drop-in: thick-form comparison lemmas (replaces old 3.1 + 3.2) -->

### 3.1 `(S_E)^thick` vs hughes `(LS)` (#564): STILL STRICTLY WEAKER

With the supplement corrected to the multiplicity-thick `(S_E)^thick` (#629
`(C4)/(C5)`: some `tau=e^{o(N)}` with thin-band energy
`Sigma_tau = Sum_{xi!=0, r_A(xi)<a/tau}|hat_mu(xi)|^2 <= e^{o(N)}`), the lattice
is `set-dodged < (S_E)^thick < (LS)`, all strict.

- `(LS) => (S_E)^thick` (AUDIT). The thin band is a **subset** of the nontrivial
  band, so `Sigma_tau <= E` for every `A,tau`; the implication reduces to the
  old `(LS) => E <= e^{o(N)}` — the multiplicity weighting is inert. Same status
  as before the correction.
- `(S_E)^thick =/=> (LS)` (REFUTED, witness). A subgroup-uniform profile
  `mu = 1_H/|H|` on `G=Z_n`, `H=d*Z_n`, has `hat_mu = 1_{H^perp}`, so
  `E = d-1 = e^{o(N)}` (constant on the family `Z_{d^s}`) — `(S_E)^thick` holds —
  yet `|hat_mu(chi)| = 1` and the matched-sign sum `= d >> sqrt(d)`, maximally
  violating `(LS)`'s square-root cancellation.

So the image clause still needs **far less than `(LS)`**: subexponential
multiplicity-dodged energy, not sharp signed cancellation. `(S_E)^thick < (LS)`.

### 3.2 `(S_E)^thick` vs the LegaSage C9 razor (#585): ORTHOGONAL, razor NO =/=> `(S_E)^thick`

> **A razor NO does NOT imply `(S_E)^thick` (PROVED).** For the block-parabola
> with avdeev's `b=0` packing `A_k` (`kappa_frame=1`), the difference
> multiplicities are `r_A(xi)=p^k` on the `b=0` subspace and `0` elsewhere, while
> *all* energy sits on characters with some `b_i!=0`. Hence the thick band
> carries **zero** energy and `Sigma_tau = E = p^k-1` is exponential for every
> `tau`. The parabola is a razor **NO** (fibers size 1, `kappa_img=1`) yet
> collapses the image (`L/A_eff = p^{-k}`) and violates `(S_E)^thick`.
> Frame-independently: if any `A` made the energy thick, `(C1)` forces
> `kappa*tau >= E`, again failing `(S_E)^thick`. The razor's image
> normalization is blind to the span-scale collapse.

(Replace the two Verdict-ledger rows accordingly:)

```text
| (S_E)^thick < (LS) strictly weaker | (LS)=>thick monotone (thin subset); subgroup witness thick =/=> (LS) | AUDIT |
| razor NO =/=> (S_E)^thick | block-parabola: razor-NO, thick-band energy 0, Sigma_tau=E exp, all A | PROVED |
```

<!-- END drop-in -->

---

## The 2-3 steps the PI should hand-re-derive

1. **`(LS)`'s exact form (both R2 directions hinge on it).** We read `(LS)` from
   the audit summary (`character_frame_hypothesis_audit.md` L191, L194-205), not
   from #564's primary statement. `(LS) => (S_E)^thick` needs `(LS)` to dominate
   absolute `L^2` energy; the refutation needs a coherent measure to violate
   `(LS)`. If #564's actual object is a pure signed statement that neither bounds
   nor is bounded by absolute energy, the verdict could shift from "strictly
   weaker" to "incomparable." Confirm which.
2. **The reading of `(S_E)^thick` as `Sigma_tau <= e^{o(N)}` (unweighted energy
   on the multiplicity-selected thin band), not a weighted-trace bound.** We take
   #629's `(C4)` definition; the *weighted* trace `tr(K_A^2)` is a frame
   consequence `(C1)`, not a supplement, so it cannot be the object being
   supplied. Confirm this is the intended thick supplement.
3. **The block-parabola frame in R3.** The clean "thick energy `=0`" computation
   is specific to `A_k` (`b=0` packing); the verdict is frame-independent via the
   `kappa*tau >= E` argument (R3.2). Confirm the `kappa*tau >= E` step and that
   `A_k` is the razor's canonical frame for this witness.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_thick_form_comparison.py   # RESULT: PASS (27/27)
```
