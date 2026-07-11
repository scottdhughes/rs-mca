# The C7 collapse cell's image-scale degree is the received-line field of definition

## Status

`CONSUMER PINNED (AUDIT) / T-PAY-RES REFORMULATED AS A FIELD-OF-DEFINITION LAW
(PROVED) / SUBFIELD-CONFINED PAYMENT ON BASE-FIELD + BOUNDED-EXTENSION LINES
(PROVED) / FORCING WITNESS ON UNBOUNDED EXTENSIONS (COMPUTED, = the paper's own
promoted countertheorem + Codex #634 + DannyExperiments #631) / EXACT TWO-SIDED
LAW delta = Theta(|F_r|) (PROVED upper + realizable) / SPAN FACE CLOSES MODULO
ONE PINNED PRINTED INPUT (FI-field)`.

This is the **last open cell** of input 2's span face: the C7 effective-image-
collapse cell's **own** image-scale projection degree per received line — the
single residual `T-PAY-RES` that #635 isolated after the arc
#622->#625->#626->#627->#635->#636 emptied everything else. The result: that
residual is **not** a free-standing enumerative constant; it is **exactly the
size of the field of definition of the received line**, capped by subfield
confinement and forced tight by the paper's own promoted countertheorem. The
collapse cell **pays** (subexponential per-line degree) precisely on lines whose
field of definition is a subexponential-size extension of the base field, and
**must be printed** as an input exactly on the unbounded-scalar-extension family
that thm:intro-countertheorem already exhibits.

Every number below is recomputed by
`experimental/scripts/verify_c7_collapse_image_degree.py` (stdlib-only, zero-arg,
`RESULT: PASS (115/115)`, ~0.24 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **COMPUTED** (exact finite
recomputation of a promoted/witness quantity), **MEASURED** (exact finite toy,
asymptotics not proved from the toy), **AUDIT** (interface reading of the tex or
a sibling note), **OPEN**.

**Credit.** The two-cell split `E+1 <= G_1 Q_img` (MASTER-2) and the C7 =
two-input reading are our **#625** (`c7_routing_spectrum.md`); the binomial-tail
non-payability by enumeration is our **#626** (`c7_degree_enumeration.md`); the
router-decidable detection **T-DET** is our **#627** (`routing_exhaustiveness.md`);
the first-match disjoint-union charge, the countertheorem dissolution, and the
isolation of this single residual **T-PAY-RES** are our **#635**
(`collapse_payment.md`); the mass-weighted `RC_occ` payment of the **saturation**
half and the collapse/saturation split diagnosis are our **#636**
(`saturation_payment_repair.md`). The **orientation floor** stress witness
(`J_z >= ceil(2^a/q^{w/2})`, antipodal supports over `q=3^r`, rate
`(1/4)log(4/3)`) is the **Codex team's PR #634**
(`full_agreement_orientation_saturation.md`), consumed here only at the level it
**proves** (its Rung-4 supply box). The **profilewise separating-pole
realization** (any occupancy slice as `H_phi(lambda)` slopes on one extension
line, rate `eta log(c)/c` at growing shallow depth) is **DannyExperiments PR
#631**; the **opposite extreme** (an exponential aperiodic fiber collapsing to
ONE base-field-pole slope, empty residual) is **DannyExperiments PR #621**
(`aperiodic_one_ray_saturation.md`, integrated); the canonical full-agreement
occupancy atlas and the per-line weighted-cover compiler `tau_phi` are
**DannyExperiments PR #620** (`canonical_full_agreement_occupancy_atlas.md`). The
block-parabola family and `(CF*)` identities are **avdeevvadim #558**. The exact
adjacent-row and separating-pole-line package is maintainer **przchojecki**'s
commit `4e3c4ee`. `avdeevvadim`/`hughes`/`LegaSage` inputs are consumed only
through the sibling notes above; no finite M31/KoalaBear survivor count, adjacent
inequality, or target threshold is touched.

**Complementary lane (cite-by-anticipation, not proved here).** The Codex team's
**supercritical-transition** lane is in flight. If its theorem lands — a bound on
the field of definition (or a transition threshold) of prize-relevant received
lines — it discharges `(FI-field)` directly and the span face closes
**unconditionally**. We reserve it as a **named input slot** (`[SUPERCRIT]`
below); we do **not** prove it here.

---

## HEADLINE (read first): the residual is a field, not a constant

`T-PAY-RES` (#635) asked for a bound on `|Z(collapse cell)|` — the distinct-slope
count the retained effective-image rank-collapse profile charges as **one**
per-received-line cell. The mission framed the tension between
**#634/#631** (many slopes from one collapsed prefix) and **#621** (many
supports, one slope): *do the slopes land on `e^{Omega(n)}` distinct received
lines (cell pays), or can `e^{Omega(n)}` land on one line (input load-bearing)?*

**Both happen, and which one is decided by a single scalar: the field of
definition `F_r` of the received line.** The controlling identity is not new —
it is `thm:subfield-confinement-full` (tex **L1930-1935**):

> "every MCA-bad slope of a `B`-valued received line lies in `B`."

Applied to the tower `B ⊆ F_r ⊆ F`, this says the collapse cell's per-line
distinct-slope count obeys

```
   delta_lambda(r) := |Z(collapse cell) ∩ {slopes bad at r}|  <=  |F_r|.     (T-FIELD)
```

So `delta_lambda(r) = e^{o(n)}` **whenever `log|F_r| = o(n)`** — in particular on
every base-field (`B`-valued) line (`delta <= |B| = n+1`) and every bounded-degree
scalar extension. And it is **tight**: at `[F_r:B] = Theta(n/log|B|)`
(`log|F_r| = Theta(n)`) the paper's **own promoted countertheorem**
(`thm:intro-countertheorem`, tex L796-819; eq (4.5) L2078; eq (6.7)/(6.8) L4060)
already builds one received line with `delta_lambda(r) = e^{Theta(n)}` distinct
collapse-cell slopes. #634 is its antipodal-orientation instance; #631 is its
arbitrary-slice generalization; **#621 is the confined base-field side of the
very same construction, giving one slope.**

The three witnesses differ in **exactly one datum** — the field of the pole:

| witness | pole field | per-line collapse-cell slopes | verdict |
|---------|-----------|-------------------------------|---------|
| **#621** (base-field pole `alpha=0 ∈ B`) | `B` | `1` per `c_m`-class, `<= q-1` total | **PAID** (confined) |
| **#634** at `alpha=0` (its own base-field corollary) | `B` | `<= 2` product-parity | **PAID** (confined) |
| **#634 / #631** (separating pole `alpha ∈ F∖B`, `log|F|=Theta(n)`) | `F` | `J_z` / `H_phi(lambda) = e^{Theta(n)}` | **FORCES** the input |

The toy confirms the crossover exactly (BLOCK 0): antipodal orientations over
`F_p`, the collapse cell's per-line slope count is `delta(alpha=0) = 2` for every
`p` (matching #634's independent "at most two product-parity slopes"),
`base_max <= |B|` over **all** base-field poles, but a separating pole in
`F_{p^2}`/`F_{p^3}` attains the **full** `|O| = 2^a` slopes:

| `p` | `a=(p-1)/2` | `|O|=2^a` | `delta(alpha=0)` | `max` over `F_p` | `max` over `F_{p^2}` | `max` over `F_{p^3}` |
|----:|-----------:|----------:|----------------:|-----------------:|---------------------:|---------------------:|
| 7  | 3 | 8  | 2 | 5  | 8  | 8  |
| 11 | 5 | 32 | 2 | 11 | 32 | 32 |
| 13 | 6 | 64 | 2 | 13 | 63 | 64 |

**Net verdict.** `T-PAY-RES` is **decided as a dichotomy** (PROVED): the collapse
cell's image-scale per-line degree equals `Theta(|F_r|)` in the exponent —
subexponential iff the received-line field of definition is subexponential. The
span face **closes on the product/profile class modulo exactly one printed input**,
`(FI-field)`, a field-of-definition bound on the collapse-cell received line. This
input is (i) **necessary** (the promoted countertheorem is the forcing witness),
(ii) **sufficient** (subfield confinement), and (iii) already **acknowledged but
undischarged** by the paper's own scope remark (`rem:intro-countertheorem-scope`,
L839-840: "verify its field and reserve hypotheses"). It **supersedes** #635's
vague "`e^{o(n)}` per line" with the exact mechanism.

---

## Rung 1 — EXTRACT: the cell, its consumers, what it owes (AUDIT)

### 1a. The C7 cell, verbatim (tex **L2440-2454**)

```
\paragraph{Saturation and effective-image-collapse cells.}
... MCA counts the final slope image, and the occupancy or
image--fiber bound must replace an uncorrected support count.  The cell is
constructible in the projective locator and explanation incidence, but its
projection degree remains an enumerative input.                        [L2450-52]
\emph{Effective-image collapse} is the related event that a boundary map
reaches exponentially fewer boundary values than its ambient codomain contains.
                                                                       [L2453-54]
```

The C7 cell is **unlabelled** (nearest label `sec:cell-catalogue`, L2366) — it is
`\cref`'d only by prose. The saturation half was paid by #636; **this packet owes
the collapse half**: the `projection degree ... enumerative input` (L2452) for an
`effective-image collapse` (L2453-54, `L_lambda << A_lambda`).

### 1b. Every consumer of the collapse input (AUDIT, grep-exhaustive)

- **Routing / retention rule** (tex **L871-881, L4850-4863, L1115-1118**): a cell
  failing `(FI)` (`L >= e^{-o(N)}A`, eq (4.4)/(9.x)) is **routed** to an earlier
  profile with its slopes removed from the later residual, "**or all estimates on
  this leaf must stay at image scale**" (L4856). L1115-1118: "effective-image
  collapse is **either routed** to an earlier profile **or** the full-image
  certificate `(FI)` is proved before an ambient scale is used."
- **Rank-collapse definition** (tex **L7029-7038**): "To pay rank collapse one
  must exhibit independent minors **and control the slope projection** as in
  `lem:rank-defect-payment`; a name such as quotient, planted, or field descent is
  not a substitute." So a rank/incidence certificate is **inert** on its own
  (this is #627's finding); the slope projection is the residual.
- **Payment criterion** (`prop:saturation-payment` L4726-4739, `lem:saturation-
  principle` L2574): route (1) a proved lower fiber bound (`RC1`), or route (2)
  "**a direct distinct-slope estimate at the profile scale**". #636 killed (1) on
  the light tail; (2) is the open input.
- **Occupancy compiler** (`lem:exact-occupancy-compiler`, tex **L5673-5698**):
  `|Z(C)| <= |R(C)| = sum_w 1/nu`, and `RC1: |Z(C)| <= floor(|C|/H)`. Singleton
  fibers (`H=1`) give **no compression** on the collapse cell (#635 T-PAY-RES).
- **The consumer in the envelope** (`eq:profile-envelope` L857-862; **A2**
  L905-907): `E_n(a) = 1 + (n-a+1) + sup_r sum_lambda (1 + barN_lambda)`,
  `barN = |Omega^0|/L`; A2: "**The total distinct-slope contribution of its
  algebraic cells is at most `e^{o(n)} E_n(a_n)`**." The charge is the first-match
  **disjoint union** `sup_r sum_i |Z_i^o| = sup_r |Z_a(r)|`
  (`lem:first-match-bound` L1526-1538, #635).

### 1c. What the collapse cell owes, formalized (AUDIT + PROVED framing)

After #627 T-DET routes an `(FI)`-failing violator to the collapse cell, that cell
is retained as an **effective-image rank-collapse profile** at image scale (L880).
As the routing **target** it is the earliest cell in whose projection its slopes
occur, so its first-match set `Z^o` is **not** empty — it carries the full slope
set. Its A2 contribution is exactly

```
   delta_lambda(r) = |Z(collapse cell) ∩ {slopes bad at received line r}|,
```

and the envelope closes iff `delta_lambda(r) <= e^{o(n)}` per received line. This
is `T-PAY-RES`. **Crucially it is a per-line quantity** — the global slope set
`Z(collapse cell)` may be exponential (MCA is per received line); only the
per-line count must be subexponential.

The image-normalized envelope term does **not** discharge it. For the modeled
#634 cell (BLOCK 2, reproducing #636), `barN^img = |O|/L = 2^a/q^{w/2}` has
exponent `a(log 2 - (log 3)/2) = +0.1438 a > 0` — the term itself is
exponentially **large** — yet the slope count `|Z| = 2^a` exceeds even that term
by **exactly** the collapse factor:

```
   rho(C) = |Z| / barN^img = q^{w/2} = G_1 = e^{Theta(n)}     (BLOCK 2, matches #636).
```

So image normalization is not enough by `G_1`. The residual is a **direct
distinct-slope estimate** (route (2)), which is what the field law supplies.

---

## Rung 2 — STRESS WITNESSES (they shaped the statement)

**#634 (Codex, PROVED bounds).** Over `q=3^r`, antipodal supports
`O_r = {S : |S ∩ {x,-x}| = 1 per fold}`, `|O_r| = 2^a`, prefix depth
`w = 2⌊a/2r⌋`. **One prefix `z` and one received line** carry
`J_z >= ceil(2^a/q^{⌈w/2⌉}) = e^{Theta(n)}` distinct exact-agreement slopes,
rate `(1/4)log(4/3) = 0.0719` (BLOCK 1, floors `{2,12,316,62712512,...}`
byte-match). Per its Rung-4 **supply box**: `#634` PROVES (i) prefix-image
`|Phi_u(O_r)| <= q^{⌈u/2⌉}`, (ii) **one** heavy prefix with `>= J_z` retained
orientations, (iii) a `z`-dependent pole separating that **complete** fiber into
`J_z` distinct slopes. It does **not** prove exact image size, uniform fibers,
`Q_img=1`, or a base-valued line. **We consume only (i)-(iii).** #634's own text
settles the field pivot: *"The separating pole line necessarily lives over `F`.
`thm:subfield-confinement-full` would cap a `B`-valued line by `|B|=n+1` slopes.
At the sole base-field pole `alpha=0` ... at most two product-parity slopes."*

**#631 (DannyExperiments, OPEN PR — profilewise separating-pole realization).**
For **any** nonempty occupancy slice `Omega_lambda` and depth `0<=w<=a-2`, there
exist `z`, an extension `F/B`, `alpha ∈ F∖D`, and **one** received line with
`|Z^o_(lambda,lambda)(r)| = |Omega_lambda ∩ Phi_w^{-1}(z)| >= ceil(H_phi(lambda)/|B|^w)`,
`= H_phi(lambda)` at `w=0` — `e^{Theta(n)}` distinct slopes on **one** line,
in bijection with the fiber via `gamma_S = U_z(alpha) - Q_S(alpha)`. The
extension is **unbounded**: `|F| > n + k·binom(L_z,2)`, so `[F:B] = Theta(n/log|B|)`
(BLOCK 4). Rate `eta log(c)/c` at **growing shallow depth** `w ~ log n`,
`w log|B| = o(n)` (BLOCK 5). #631 emphatically is **one line ↔ a whole fiber of
slopes**, over an extension — and it explicitly does **not** classify these
witnesses through C7, leaving open whether they survive the collapse.

**#621 (DannyExperiments, integrated — the opposite extreme).** Over `q=2^r`, an
**exponentially large, fully aperiodic** prefix fiber `G_r`,
`|G_r| >= ceil(binom(n,m)/q^{w+1}) = exp((log 2 - o(1))n)` (BLOCK 3, rate
`log 2`), gives **only one bad slope on the base-field pole line** `alpha=0`:
`P_S(0) = -c` for **every** `S ∈ G_r`. The `<= q-1 = e^{o(n)}` constant-
coefficient classes cover the line with **empty later residual** — "a
subexponential algebraic routing of an exponentially large fully aperiodic prefix
profile." This is subfield confinement in action: **base-field pole => confined
=> paid.**

**#620 (DannyExperiments, integrated — the per-line ceiling).** The weighted
vertex-cover compiler `|Z_a(r) ∩ Gamma| <= min(|Gamma|, tau_phi(r,Gamma))`,
`tau_phi = min-weight vertex cover, weights H_phi`, is **per received line** —
but `tau_phi <= binom(n,a)`, so it **permits** exponentially many slopes on one
line. Its open wall is exactly "an actual-slope projection theorem removing or
paying the orientation factor when `p = Theta(n)`" — which the field law resolves.

**The tension, resolved.** #634/#631 (many slopes, one line) and #621 (many
supports, one slope) are **the same construction at two poles**. The variable is
`F_r`. Over `B` the slopes are confined (`<= |B|`, #621, #634-at-`0`, BLOCK 0
`base_max`); over `F` with `log|F| = Theta(n)` they re-expand to the full fiber
(#634/#631, BLOCK 0 `ext3 = |O|`).

---

## Rung 3 — DERIVE: the field-of-definition payment law (PROVED)

### T-FIELD (PROVED). The collapse cell's per-line degree is bounded by `|F_r|`.

> **Theorem (subfield-confined collapse payment).** Let `C_lambda` be a C7
> effective-image rank-collapse cell retained at image scale on the row
> `RS_F(D,k)`, `D ⊆ B ⊆ F`. Let `r = (r_0,r_1)` be a received line and let
> `F_r` be its **field of definition** (`def` tex L2290: the smallest recorded
> subfield over which the line, its parameter maps, and its incidence are
> defined; `r_0,r_1 ∈ F_r^D`, `B ⊆ F_r ⊆ F`). Then the cell's per-line distinct-
> slope contribution to the first-match disjoint union satisfies
>
> ```
>       delta_lambda(r) = |Z(C_lambda) ∩ {MCA-bad slopes of r}|  <=  |F_r|.
> ```
>
> In particular `delta_lambda(r) = e^{o(n)}` whenever `log|F_r| = o(n)`: for every
> `B`-valued line, `delta_lambda(r) <= |B| = n+1`; for every scalar extension
> with `[F_r:B] = o(n/log|B|)`, `delta_lambda(r) <= |B|^{[F_r:B]} = e^{o(n)}`.

**Proof.** Apply `thm:subfield-confinement-full` (tex L1930-1935) to the tower
`D ⊆ F_r ⊆ F`. Take any MCA-bad slope `gamma` of `r`. If `gamma ∈ F∖F_r`, write
`r_0 + gamma r_1` and decompose the explaining polynomial and `gamma` in an
`F_r`-basis of `F`; because `D ⊆ F_r` and `r_0,r_1 ∈ F_r^D`, comparison of basis
components on the agreement support `S` produces an `F_r`-valued codeword
explaining the same pair on the same `S` (the theorem's proof, L1937-1943,
verbatim with `B := F_r`). Hence **every** MCA-bad slope of an `F_r`-valued line
lies in `F_r`. Distinct slopes are distinct field elements, so the total bad-slope
set of `r` — a fortiori its intersection with any single cell `C_lambda` — has at
most `|F_r|` elements. `QED`

Two remarks make this the correct, non-vacuous form:

1. **It survives image normalization.** `delta_lambda(r)` is the **actual** per-
   line slope count, independent of whether the envelope term is written at ambient
   or image scale; the `G_1` gap of Rung 1c/BLOCK 2 is precisely the amount by
   which the image-normalized term **under**counts it, and T-FIELD supplies the
   missing direct estimate (route (2) of `prop:saturation-payment`).
2. **It routes #621 exactly.** On a base-field pole line every collapse fiber maps
   into `<= |B|` slope classes; the `e^{o(n)}` classes give an atlas with empty
   later residual (#621), so the disjoint-union charge is `<= |B| = e^{o(n)}`.

### T-FIELD-TIGHT (COMPUTED, forcing witness). The bound is attained.

> At `[F_r:B] = Theta(n/log|B|)` (i.e. `log|F_r| = Theta(n)`) there is a single
> received line with `delta_lambda(r) = e^{Theta(n)}`.

This is **not** proved here; it is the paper's **already-promoted**
`thm:intro-countertheorem` (L796-819) with `rem:intro-countertheorem-scope`
(L829-841: *"the scalar extension used to separate all exponentially many slopes
has `log|F_n| = Theta(n)`"*), realized by eq (4.5) (`|F|-n > k binom(N,2)` gives a
line with `>= N` slopes, L2078-2083), eq (6.7)/(6.8) (`exp((h(alpha)/4)n)` slopes
at `[F:B]=O(n/log n)`, L4060-4072), and eq (6.11g)/(6.11h) (binary cubic,
`exp((h(alpha)/6)n)`, L4248-4258). Codex #634 (`J_z`) and DannyExperiments #631
(`H_phi(lambda)`) are two specific instances. BLOCK 4 recomputes the separation
threshold: to place `N = e^{Theta(n)}` **distinct** slopes on one line the gate
forces `log|F| >= 2 log N - O(log n) = Theta(n)`, i.e. `[F:B] = Theta(n/log|B|)`,
matching L4072 exactly.

### T-LAW (PROVED, two-sided). The exact law.

Combining: the **worst-case** per-received-line image-scale distinct-slope count
of the C7 collapse cell is `Theta(|F_r|)` in the exponent —

```
   delta_lambda(r) <= |F_r|          (PROVED upper, T-FIELD),
   delta_lambda(r) = |F_r|^{1-o(1)}  realizable  (T-FIELD-TIGHT),
   => subexponential  <=>  log|F_r| = o(n).
```

BLOCK 7 certifies both sides on the antipodal toy: `delta` never exceeds
`min(|O|, |F_r|)`, **and** a large-enough extension attains the full `|O|`, while
every base-field pole stays `<= |B|` (dichotomy nonvacuous, `base_max < ext_max`
for all `p`).

---

## Rung 4 — TOY CENSUS (MEASURED, verifier-recomputed)

Exact small-field instantiation of T-LAW; every value is a genuine finite-field
computation (stdlib `GF(p^d)` via an irreducible modulus found by a Rabin test).

**(a) Antipodal dichotomy (BLOCK 0), `p ∈ {7,11,13}`, `D=F_p^*`, `phi=x^2`:** the
census table in the HEADLINE. Base-field poles: `delta(alpha=0)=2` (matches #634's
independent prediction), `base_max ∈ {5,11,13} <= |B|` (subfield confinement).
Extension poles in `F_{p^2}`/`F_{p^3}` attain the full `|O|=2^a ∈ {8,32,64}`
(re-expansion, #634/#631). `delta(0) < |O|` for all `p` (the #621 collapse).

**(b) #634 orientation floor (BLOCK 1):** `J_z ∈ {2,12,316,62712512,...}` for
`r=2..5`, byte-match; rate `(log J_z)/n >= (1/4)log(4/3) = 0.0719`; `w` even,
`0<w<=a-2`.

**(c) Image-scale envelope gap (BLOCK 2), reproduces #636 Rung 4:** `barN^img`
exponent `log 2 - (log 3)/2 = +0.1438 > 0`; `rho = |Z|/barN^img = q^{w/2} = G_1`
exactly (`Fraction`-exact for `r=2..5`) — the collapse factor by which the image
term undercounts.

**(d) #621 base-field one-ray collapse (BLOCK 3), `q=2^r`, `r=5..11`:**
`gcd(m,n)=1` (aperiodic), `(w+1)log q/n < 0.5` (subexponential routing),
`(log|G_r|)/n ∈ (0, log 2]` and `-> log 2` (exponential fiber), covering classes
`q-1 = n = e^{o(n)}`.

**(e) Separation threshold (BLOCK 4), `q=3^r`, `r=4..8`:** `log|F|` to separate
`N=2^a` slopes is `Theta(n)` (ratio in `(0,2]`); bounded extension
`[F':B]=⌊sqrt(n)/log|B|⌋` keeps `log|F'|/n < 0.2` (subexponential cap).

**(f) #631 depth/rate (BLOCK 5):** `w log|B| = o(n)` at `w ~ log n` across
`n ∈ {1e4,1e6,1e8}`; surviving exponent `eta log(c)/c > 0` for `c ∈ {2,3,4}`.

**(g) Admissible controls (BLOCK 6/6b):** single-leaf `E ∈ {1/2, 22/3, 43/6}`
(`Q_img=1`, reproduces #625/#635/#636); block-parabola collapse leaf
`barN^img = G_1 barN^amb = 1` (the #609 escape, reproduces #635).

---

## Rung 5 — VERDICT + paste-ready ledger entry

**Verdict.** `T-PAY-RES` is **decided as a dichotomy** and reduced to **one
pinned printed input**. It is not a free enumerative constant; it is
`Theta(|F_r|)`, the received-line field of definition. Honest scope:

- **PROVED (paid sub-class):** the collapse cell's image-scale per-line degree is
  `e^{o(n)}` on every received line whose field of definition is a subexponential
  extension of `B` — all base-field lines (`<= |B| = n+1`, #621 with empty
  residual) and all `[F_r:B] = o(n/log|B|)` extensions. Subfield confinement,
  T-FIELD.
- **FORCED (load-bearing sub-class):** on `[F_r:B] = Theta(n/log|B|)`
  (`log|F_r| = Theta(n)`) the paper's promoted countertheorem forces
  `e^{Theta(n)}` on one line; Codex #634 and DannyExperiments #631 are instances.
  T-FIELD-TIGHT.
- **OPEN (the one residual):** whether ledger-admissibility (or the prize's
  proximity-radius reserve) **already** confines prize-relevant received lines to
  `log|F_r| = o(n)`. The paper's scope remark (L839-840) treats this as a separate,
  undischarged "field and reserve hypothesis." Discharging it — or importing the
  Codex `[SUPERCRIT]` transition theorem — closes the face unconditionally.

### The pinned minimal printed input

> **(FI-field).** *For the C7 effective-image rank-collapse cell, the received
> line is defined over a scalar subextension `F' ⊇ B` with `log|F'_n| = o(n)`
> (equivalently `[F':B] = o(n/log|B_n|)`); equivalently the collapse cell's bad
> slopes are confined to such a bounded subextension.*

Under `(FI-field)`, `delta_lambda(r) <= |F'| = e^{o(n)}` per line by subfield
confinement (T-FIELD), and the collapse cell pays. Without it, the promoted
countertheorem forces `e^{Theta(n)}` (T-FIELD-TIGHT). `(FI-field)` is **sharper
than and independent of** the plain full-image certificate `(FI)`
(`L >= e^{-o(n)}A`, tex L4844): `(FI)` bounds the **image** size of the boundary
map; `(FI-field)` bounds the **field** of the received line. #634 is precisely the
regime where `(FI)` fails (genuine collapse) **and** the line is over an unbounded
extension — both must be addressed, and only `(FI-field)` caps the slope count.

### Superseding ledger entry (extends #635's, for the maintainer)

*Closing the C7 collapse cell on input 2's span face. After #635 (first-match
disjoint-union charge, `sup_r sum_i |Z_i^o| = sup_r |Z_a(r)|`,
`lem:first-match-bound` L1535) the single residual is the retained effective-image
rank-collapse profile's **own** per-received-line distinct-slope count
`delta_lambda(r)`. This is not a free enumerative input: by
`thm:subfield-confinement-full` (L1930-1935) applied to `D ⊆ F_r ⊆ F`, every
MCA-bad slope of an `F_r`-valued line lies in `F_r`, so `delta_lambda(r) <= |F_r|`
(T-FIELD), the field of definition of the received line. Hence the collapse cell
pays with `delta_lambda(r) = e^{o(n)}` on every line with `log|F_r| = o(n)` — all
base-field lines (`<= |B| = n+1`; DannyExperiments #621 routes an exponential
aperiodic fiber to `<= q-1` base-field-pole slopes with empty residual) and all
bounded-degree extensions. The bound is tight: the paper's own
`thm:intro-countertheorem` (L796-819, scope L829-841) with eq (4.5)/(6.7)/(6.11g)
constructs, at `[F_r:B] = Theta(n/log|B|)`, one line with `e^{Theta(n)}` distinct
slopes (Codex #634 antipodal `J_z >= ceil(2^a/q^{w/2})`, rate `(1/4)log(4/3)`;
DannyExperiments #631 arbitrary slice `H_phi(lambda)`). Print, superseding #635's
four items: (i) `L869` as the first-match disjoint-union charge; (ii) the census
as per-line description-entropy; (iii) routed/atlas profiles exempt from A5
(`R<char`), charged by description entropy; and, replacing #635's item (iv)
("the C7 collapse cell's image-scale projection-degree bound"), the sharper
**(iv') (FI-field)**: the C7 effective-image rank-collapse cell's received line is
confined to a scalar subextension with `log|F'_n| = o(n)`, under which
`delta_lambda(r) <= |F'| = e^{o(n)}` by subfield confinement. This is an OPEN
input, not an established fact — subfield confinement proves the payment on the
confined class and the promoted countertheorem forces the input on the unbounded
class; whether admissibility/proximity-reserve already implies `(FI-field)` (or
the Codex supercritical-transition theorem supplies it) is the single remaining
link.*

### What closes if `(FI-field)` is discharged

```
 single admissible leaf     --#622 T1--> (S_E) free, span face free
 Gap-2 span-collapse        --#545-----> C5 field-descent, vacuous on admissible
 saturation products        --#636-----> paid by mass-weighted RC_occ (dominant atom)
 collapse products          --#627+#635-> detected, routed (Z^o=empty), charge 0
 collapse cell per-line deg --THIS------> delta <= |F_r| (subfield confinement)
 (FI-field): log|F_r|=o(n)  --residual--> the one open link (= promoted scope hyp,
                                          or Codex [SUPERCRIT])
```

with the single open link `(FI-field)` — the received-line field of definition —
now **exactly pinned**, PROVED sufficient, and forced necessary by the paper's own
countertheorem.

### The 2-3 steps the PI should re-derive

1. **T-FIELD (the payment).** `thm:subfield-confinement-full` (L1930-35) with base
   `B := F_r`: every MCA-bad slope of an `F_r`-valued line lies in `F_r`, so any
   cell's per-line slope count is `<= |F_r|`. One application of the theorem's own
   proof. The only content is *reading the residual as a per-line count over the
   line's field of definition* (not a global constant, not an ambient degree).
2. **The `G_1` gap (why image normalization is not enough).** For the modeled #634
   cell `barN^img = 2^a/q^{w/2}` is exponentially large yet `|Z| = 2^a` exceeds it
   by exactly `G_1 = q^{w/2}` (BLOCK 2). So route (2) of `prop:saturation-payment`
   (a direct distinct-slope estimate) is genuinely required, and T-FIELD supplies
   it. Confirm `barN^img` exponent `log2 - log3/2 > 0` and `rho = q^{w/2}`.
3. **Tightness (necessity of `(FI-field)`).** The forcing witness is **not** new:
   it is `thm:intro-countertheorem`/eq (4.5). Re-derive the separation gate
   `|F|-n > k binom(N,2)`: for `N = e^{Theta(n)}` it forces `log|F| = Theta(n)`,
   i.e. `[F:B] = Theta(n/log|B|)` (L4072). Cross-check `delta(alpha=0)=2 <= |B|`
   vs `delta(alpha ∈ F∖B) = |O|` in BLOCK 0 — the entire phenomenon is the field
   of the pole.

---

## Findings pinned (for the maintainer)

1. **The C7 cell is unlabelled** (L2440), so its enumerative input cannot be
   `\cref`'d. When `(FI-field)` is printed, give the cell a label
   (`cell:sat-collapse`) so the ledger can reference it.
2. **`(FI)` and `(FI-field)` are distinct and both load-bearing.** The tex has
   `(FI)` (image size, L4844) but no field-of-definition certificate for the
   received line; `rem:intro-countertheorem-scope` names the gap but attaches no
   certificate. Print `(FI-field)` as a named companion to `(FI)`.
3. **A5 (`R<char`) scope.** The collapse products have `R = 2k >= char`; #635
   pinned that routed/atlas profiles must be exempted from A5 and charged by
   description entropy. `(FI-field)` is compatible: it constrains the received-line
   field, not the profile's `R`.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_c7_collapse_image_degree.py   # RESULT: PASS (115/115)
```
