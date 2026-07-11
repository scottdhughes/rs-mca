# routing = spectrum: (S_E) versus the C7 collapse cell

## Status

`C7 EXTRACTED (AUDIT) / MASTER-2 (PROVED) / TWO-CELL ROUTING (PROVED) /
NARROW FORM REFUTED (PROVED-negative) / ENUMERATIVE DEGREE = WALL (OPEN)`.

Research packet attacking the **routing = spectrum conjecture** — the named wall
at the close of our **PR #622** (`se_on_admissible_leaves.md`), and the single
statement whose proof would close input 2's span face unconditionally:

> **Conjecture (routing = spectrum, #622 Rung 3).** Every `(S_E)`-violating
> admissible leaf is non-primitive: it is caught by first-match and routed to the
> C7 effective-image-collapse cell. Equivalently, every primitive residual
> satisfies `(S_E)`.

Every number below is recomputed by
`experimental/scripts/verify_c7_routing_spectrum.py` (stdlib-only, zero-arg,
`RESULT: PASS (731/731)`, ~0.09 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotics not proved from the toy), **AUDIT** (interface reading of the tex or
a sibling note), **WALL** (identified obstruction), **OPEN**.

**Credit.** The block-parabola family and the `(CF*)` identities are
**avdeevvadim's** (PR #558, integrated at `e190193`). The J2 magnitude-blindness
impossibility is our **#609** (`frame_image_completion.md`); the master identity
`L >= A_eff/(1+E)` and the minimal supplement `(S_E)` are our **#614**
(`minimal_phase_supplement.md`); the finding that the C7 collapse routing is an
**assumed enumerative input, not a theorem** is our **#539**
(`fi_full_image_primitive.md`); the `(S_E)`-on-admissible-leaves stratification,
T3 multiplicativity, and this conjecture are our **#622**
(`se_on_admissible_leaves.md`). The Frobenius-closure classification of the
*span*-collapse (Gap-2) sub-case is our **gap2 lane** (`gap2_collapse_routing.md`),
consumed here to separate Gap-2 (→ C5) from the Gap-1 image collapse (→ C7) that
is this packet's object.

---

## HEADLINE (read first): routing = spectrum is TRUE with the RIGHT cell, and the
## sharpened statement is a one-line theorem

The conjecture is **correct in substance but mis-addressed in the letter.** The
one inequality that carries the whole packet is, with `P_2 = sum_z mu(z)^2`,
`E = A_eff P_2 - 1` (#614 Parseval), `L = |image|`, `Mx = max_z mu(z)`:

```
   E + 1  =  A_eff * P_2  <=  A_eff * Mx  =  (A_eff/L) * (L * Mx)  =  G_1 * Q_img.   (MASTER-2)
```

Here `G_1 := A_eff/L` is the **Gap-1 image-collapse ratio** (`(FI)` <=> `G_1 <=
e^{o(N)}`) and `Q_img := L * Mx` is the **image-normalized max-fiber ratio**
(primitive-Q <=> `Q_img <= e^{o(N)}`, `def:primitive-q` tex L4912). The single
step `P_2 <= Mx` is Hölder (`sum mu^2 <= max mu * sum mu`, `sum mu = 1`).

Therefore **large dodged-band energy forces `G_1` large OR `Q_img` large** —
**effective-image collapse OR saturation** — and these are exactly the **two
printed components of the C7 cell** (tex L2440–2454): the *effective-image
collapse* line (L2453–2454) and the *saturation* line (L2440–2452). So:

- **Operative form PROVED.** Every primitive first-match residual satisfies
  `(S_E)`: it pays max-fiber Q (`Q_img <= e^{o}`, `def:primitive-q`) and carries
  `(FI)` (`G_1 <= e^{o}`, supplied by the C7-collapse routing — else it is
  retained as a rank-collapse profile), and MASTER-2 then gives `E+1 <= e^{o}`
  for **free**. `(S_E)` is a **corollary of the two payments the leaf must make
  anyway**, not a new input.

- **Literal form REFUTED.** "Routed to the C7 *effective-image-collapse* cell"
  names the **wrong one of C7's two components** for half the violators. The
  **heavy-atom class** violates `(S_E)` with `G_1 = 1` (image is **full**, `(FI)`
  holds, *no* effective-image collapse) — it is caught by the **saturation**
  component instead. The block-parabola (pure collapse, `G_1 = p^k`, `Q_img = 1`)
  and the heavy-atom (pure saturation, `G_1 = 1`, `Q_img` exponential) are a
  **dual pair**: both violate `(S_E)`, routing sends them to the **two different**
  C7 components. Naming only the collapse component is the imprecision.

- **The crux the wall hides (rung 2), resolved.** `E` large forces `P_2` large
  (concentration) — but concentration **bifurcates**, and `E` does **not**
  determine `L`. The two collapse modes genuinely **diverge**, and that
  divergence *is* the finding: `C7`'s **printed trigger** (L2453, "exponentially
  fewer boundary values than its ambient codomain") is **image-size collapse**
  (`G_1`), **not** max-atom concentration; the max-atom / heavy-fiber mode is the
  **separate** saturation line (L2452, "occupancy or image–fiber bound"), whose
  projection degree is a **separate** assumed input.

**Net verdict: PARTIAL.** The operative conjecture is a theorem given the paper's
own two exclusions; the literal wording is corrected to *both* C7 components; the
genuinely open residual is **unchanged** — the C7 **projection-degree enumerative
budget** (for *both* components), which a spectral argument does not pay. What
this packet buys the ledger: `(S_E)`, `(FI)`, and `¬(C7-collapse)` **coincide on
the primitive class** (proved), so #622's "print the C7 budget **or** `(S_E)`" is
**vindicated and sharpened** — they are inter-reducible modulo max-fiber Q — with
the correction that the C7 cell is **two** assumed inputs, not one, and the
saturation input is load-bearing (the heavy-atom needs it).

---

## Rung 1 — EXACT STATEMENT (AUDIT, verbatim tex anchors)

### 1.1 The C7 cell, verbatim (tex L2440–2454)

`\paragraph{Saturation and effective-image-collapse cells.}` — one paragraph,
**two** displayed events, **two** assumed enumerative inputs:

> **[saturation, L2440–2452]** "The exact projections are those of
> `\cref{def:explanation-occupancy}`: a raw witness first maps to its explanation
> state `(gamma,h)` and then to its slope `gamma`. Removing common codeword,
> quotient, and planted factors may identify many raw witnesses or many
> explanation states, but distinct explaining polynomials can still occur at one
> slope. Thus *saturation* means passing through these displayed images with
> their actual fiber cardinalities... MCA counts the final slope image, and **the
> occupancy or image–fiber bound must replace an uncorrected support count**. The
> cell is constructible in the projective locator and explanation incidence,
> **but its projection degree remains an enumerative input**."
>
> **[effective-image collapse, L2453–2454]** "*Effective-image collapse* is the
> related event that **a boundary map reaches exponentially fewer boundary values
> than its ambient codomain contains**."

The **assumed enumerative input** is the sentence at **L2451–2452** ("its
projection degree remains an enumerative input"). It governs the *saturation*
event as printed; the *effective-image-collapse* event (L2453–2454) is the
"related event" that shares the same enumerative status (this is #539's reading,
and `def:closed-ledger` item L4 at **L1115–1116** states the routing branch as a
hypothesis: "effective-image collapse is either routed to an earlier profile or
`(FI)` is proved before an ambient scale is used").

The image-scale definitions (chart 9.1, tex L4818–L4863) fix the vocabulary:
`Phi(x) = sum_t x_t (t, t^2, ..., t^R)` (**L4818**, the *single global* power-sum
map when `R < char`), `L = |Phi(Omega)|`, `A = |B^R|`, `barN^img = M/L`; the
**full-image certificate** `(FI): L >= e^{-o(N)} A` (**L4844**), and "an
*effective-image collapse* is the failure of this comparison; it must be retained
as an effective-image rank-collapse profile, or handled throughout with image
normalization" (**L4850–4863**).

### 1.2 The first-match order (tex L5180–5182, verbatim)

> "The first-match order is: **algebraic major arcs first, then a separately
> certified Sidon/Fourier cell, and only then the high-energy primitive inverse
> step.** Naming a large low-energy fiber a cell does not pay it."

So a leaf reaches the **primitive** payment (high-energy inverse step) only after
the algebraic arcs (C1 quotient L2374, C5 field-descent L2422) and the
Sidon/Fourier cell have fired. Crucially, `def:primitive-first-match-residual`
(**L4804–4812**) says the three words have separate content and:

> "*primitive* means that the row-specific quotient, planted, field-descent,
> rank, and **ray-saturation** certificates named by the atlas have all been
> applied... it **does not assume the Fourier, Sidon, max-fiber, or ray
> estimates that will be imposed below**."

Read against MASTER-2 this is decisive: a primitive residual has had the
**ray-saturation** (C7-saturation) and **rank / field-descent** (collapse-type)
exclusions **applied**, but the **max-fiber Q** analytic bound is still to be
**paid**. Both factors of MASTER-2 are thus objects the atlas already tracks.

### 1.3 The conjecture, formalized

For an admissible profile `mu` on `V_g`, `|V_g| = A_eff`, write
`E(mu) = A_eff * sum_z mu(z)^2 - 1`. Then:

- **(narrow)** `E(mu) >= e^{Omega(N)}` `=>` `mu` is caught, before the primitive
  payment, by the C7 **effective-image-collapse** component (`G_1 >= e^{Omega}`).
- **(operative)** every primitive first-match residual has `E <= e^{o(N)}`.
- **(two-cell, this packet)** `E(mu) >= e^{Omega(N)}` `=>` `G_1 >= e^{Omega(N/2)}`
  **or** `Q_img >= e^{Omega(N/2)}` — caught by C7-collapse **or** C7-saturation.

Rung 2 proves (two-cell); Rung 3 derives (operative) from it and the paper's own
exclusions; Rung 4 refutes (narrow) by the heavy-atom witness.

---

## Rung 2 — STRUCTURE THEOREM: MASTER-2 and the two collapse modes (PROVED)

### 2.1 MASTER-2 (PROVED, one line)

With `mu` a probability profile on `V_g`, `P_2 = sum_z mu(z)^2`,
`E + 1 = A_eff P_2` (#614 Parseval), `L = |supp mu|`, `Mx = max_z mu(z)`:

```
   E + 1  =  A_eff P_2  =  A_eff sum_z mu(z)^2
          <=  A_eff (max_z mu(z)) (sum_z mu(z))            [ Hölder, sum mu = 1 ]
          =   A_eff * Mx
          =   (A_eff / L) * (L * Mx)
          =   G_1 * Q_img.                                                (MASTER-2)
```

The only inequality is `P_2 <= Mx`, i.e. `sum mu^2 <= max mu`. Equality iff `mu`
is uniform on its support (then `P_2 = Mx = 1/L`). **PROVED.** Verifier BLOCK 1
recomputes `E+1 <= G_1 Q_img` on 42 measures with planted atoms; BLOCK 0
recomputes the Parseval form `E+1 = A_eff P_2` and the #614 master
`L >= A_eff/(1+E)` on 198 measures (equality for uniform).

### 2.2 The E-vs-L crux: which collapse mode does C7's trigger detect? (PROVED)

`E` large means `A_eff P_2` large, i.e. `P_2 >> 1/A_eff` (collision probability
exceeds uniform by an exponential factor). This is **concentration**. The task's
sharp question: does `E` large force `L` **small** (image-size collapse), or only
`P_2` large (which could be a **heavy atom on a full image**)? MASTER-2 answers
exactly:

| quantity | meaning | C7 component | primitive-obstruction |
|----------|---------|--------------|-----------------------|
| `G_1 = A_eff/L` | **image-size** collapse: fewer image values than the span | **effective-image collapse** (tex **L2453**) | `¬(FI)`: leaf locked to image scale |
| `Q_img = L*Mx` | **heavy fiber** / occupancy: an atom above the image mean | **saturation** (tex **L2452**) | `¬`primitive-Q: max-fiber violation |

`E` large forces the **product** `G_1 Q_img` large, hence at least one factor
large — but **not** a specific one. `E` does **not** determine `L`: the two
extremes below both have `E = C_0 - 1` yet **opposite** image verdicts.

- **Block-parabola — PURE COLLAPSE (`G_1` carries `E`, `Q_img = 1`).** Uniform on
  a small image: `L = p^k`, `A_eff = p^{2k}`, `Mx = 1/p^k`. Then `G_1 = p^k`,
  `Q_img = p^k * p^{-k} = 1`, and MASTER-2 is **equality**
  `E+1 = p^k = G_1 * Q_img`. `(FI)` **fails** (`G_1` exponential); max-fiber Q
  **passes** (singleton fibers, the #609 escape). Verifier BLOCK 2: image built
  as `{(t,t^2)}^k ⊂ (F_p^2)^k`, `|S| = p^k`, `rank_{F_p} = 2k`, all rows tight.

- **Heavy-atom — PURE SATURATION (`Q_img` carries `E`, `G_1 = 1`).** Atom mass
  `a ≈ A_eff^{-1/4}` at `z*`, the rest spread uniformly over the **entire** span:
  `L = A_eff` (**full image**, `(FI)` holds with equality, `G_1 = 1`),
  `Mx = a`, `Q_img = A_eff * a ≈ A_eff^{3/4}` (exponential). Then
  `E = A_eff P_2 - 1 ≈ A_eff^{1/2} - 1` (exponential, **violates `(S_E)`**), while
  MASTER-2 is **slack** (`E+1 < G_1 Q_img`, because `P_2 < Mx` on a spread tail).
  Verifier BLOCK 3, exact for `A_eff ∈ {16,81,256,625}`:

  | `A_eff` | atom `a` | `L` | `G_1` | `Q_img` | `E` (exact) | `(S_E)` | `(FI)` | max-fiber Q |
  |--------|---------|-----|-------|---------|-----|---------|--------|-------------|
  | 16  | 1/2 | 16  | 1 | 8   | 49/15 ≈ 3.27   | fail | HOLD | fail |
  | 81  | 1/3 | 81  | 1 | 27  | 169/20 = 8.45  | fail | HOLD | fail |
  | 256 | 1/4 | 256 | 1 | 64  | 1323/85 ≈ 15.56| fail | HOLD | fail |
  | 625 | 1/5 | 625 | 1 | 125 | 961/39 ≈ 24.64 | fail | HOLD | fail |

  (`a = round(A_eff^{3/4})/A_eff`; `Q_img = L·a = round(A_eff^{3/4})` exact; `E`
  grows like `A_eff^{1/2}`, exponential in `N` — all four rows fail `(S_E)`.)

**Resolution of the crux (PROVED).** C7's **printed** trigger — "exponentially
fewer boundary values than its ambient codomain" — is `G_1 = A_eff/L` large =
**image-size collapse**, the *block-parabola* mode. The *heavy-atom* mode is
`Q_img` large = a **fiber heavier than the image mean** = the **saturation**
event, C7's **other** printed line. **`E` large ⟺ (`G_1` large OR `Q_img`
large)**; the modes are distinct (the two witnesses realize each alone) and the
divergence is exactly the saturation-vs-collapse split. This is where a sloppy
"E large ⟹ image collapses" argument would hide a false step: it silently
assumes uniformity (`P_2 = Mx`), which fails on the heavy-atom.

---

## Rung 3 — THE TWO-CELL ROUTING THEOREM + the equivalence modulo Q (PROVED)

### T-A (PROVED). Primitive residual `=>` `(S_E)`, given its own two payments.

Let `mu` be a primitive first-match residual that has (i) survived C7-collapse
routing, so it carries `(FI)`: `G_1 = A_eff/L <= e^{o(N)}` (else it is retained as
an effective-image rank-collapse profile, chart 9.1 **L4850**; an ambient/span
formulation is "permitted only when ... `(FI)` has already been certified",
`def:primitive-q` **L4934** — a non-`(FI)` leaf is not primitive at span scale);
and (ii) satisfies its max-fiber Q payment,
`Q_img = L Mx <= e^{o(N)}` (`def:primitive-q` L4912). Then by MASTER-2

```
   E + 1  <=  G_1 * Q_img  <=  e^{o(N)} * e^{o(N)}  =  e^{o(N)},
```

so `(S_E)` holds. **PROVED.** Thus `(S_E)` is **not an independent hypothesis**:
it is a **corollary of the two payments** the primitive leaf must make anyway
(the image clause and max-fiber Q). Verifier BLOCK 5 (244 checks): for every test
measure, `(G_1 <= B) ∧ (Q_img <= B) => E+1 <= B^2`, and the sharp
`E+1 <= G_1 Q_img`; BLOCK 5 also confirms the primitive-class form directly
(if both ratios `<= t` then `E+1 <= t^2`, no breach over the uniform family).

### T-B (PROVED). Equivalence modulo max-fiber Q: `(S_E) <=> (FI)` on primitives.

- `(S_E) => (FI)`, **unconditional** (#614 master): `L >= A_eff/(1+E) >= e^{-o}
  A_eff`. Verifier BLOCK 6, `L (1+E) >= A_eff` on all measures.
- `(FI) + `max-fiber Q` => (S_E)`, this packet (MASTER-2): `E+1 <= G_1 Q_img`.

So **given max-fiber Q** (the primitive-Q payment / the frame's `EF5`, #609/#614),
`(S_E)` and `(FI)` are **equivalent**. Off that class they **diverge**, and the
gap is **exactly** the max-fiber-Q failure: the heavy-atom has `(FI)` (`G_1=1`)
but not `(S_E)` (`E` large) precisely because it **fails** max-fiber Q (`Q_img`
exponential). **PROVED.** Verifier BLOCK 6: the heavy-atom witness realizes the
`(FI)`-yet-not-`(S_E)` gap and it is the `Q_img`-large event.

### T-C (PROVED, structural). The divergence is a PRODUCT phenomenon (T3 of #622).

`E + 1 = A_eff P_2` is **multiplicative** over independent product factors
(`E(X×Y)+1 = (E_X+1)(E_Y+1)`), and MASTER-2 **tensorizes**: `G_1 = ∏ G_1^{(i)}`,
`Q_img = ∏ Q_img^{(i)}`, so `E+1 <= G_1 Q_img` blockwise and in the product. A
single admissible power-sum leaf (global chart, `R < char`, non-Artin–Schreier)
has `E` **polynomial** (`(S_E)` holds, #622 T3), so it never reaches the
divergence: both `G_1` and `Q_img` are subexponential on it. The divergence needs
a `k`-fold PRODUCT:

- **collapse product** = block-parabola (each block `L_i = p < p^2 = A_eff,i`):
  `G_1 = p^k` exponential, `Q_img = 1` → C7-**collapse**.
- **saturation product** = heavy-atom per block (each block **full** image
  `L_i = p = A_eff,i` but a heavy atom): `G_1 = 1`, `Q_img = (p a)^k` exponential
  → C7-**saturation**. Verifier BLOCK 4: `p=5`, `a=2/5`, `E+1 = (5/4)^k` exact
  (multiplicative), `L = p^k = A_eff` (full), `Q_img = (2)^k`, `G_1 = 1`.

**Both** are `k`-fold products with `R_prod = 2k >= char` (fail `(A5)` `R<char`,
#622); neither is a single admissible primitive leaf. The two products are a
**dual pair** distinguishing C7's two components. **PROVED / MEASURED.**

### The degree payment (rung-3 target): what is proved, what is not (WALL)

MASTER-2 proves the **trigger logic** is exhaustive: the `(S_E)`-violators are
partitioned (up to the `e^{o}` band) into C7-collapse (`G_1`) and C7-saturation
(`Q_img`). It does **not** pay the **projection degree** — *how many* leaves land
in each component at each degree, charged within `e^{o(n)} E_n(a_n)` in
first-match. That count is the C7 enumerative input (both L2452 saturation and
L2453 collapse), and it is **untouched** by a spectral argument. Partial
reductions that DO hold:

- **Gap-2 sub-case is already paid elsewhere.** The *span*-collapse component of
  effective-image collapse (`dim_{F_p} V_g < Rf`, `A_eff << A`) is **not** a C7
  enumerative input: by `gap2_collapse_routing.md` it is a Frobenius-closure
  relation = the C5 field-descent cell, an *earlier* first-match profile, and it
  is **vacuous** on admissible leaves (`w < p`). This packet's C7 residue is the
  **Gap-1** collapse `L << A_eff` **with** `A_eff = A` (the block-parabola), which
  C5 does **not** catch.
- **Only products reach it (T-C).** Single admissible leaves satisfy `(S_E)`, so
  the C7 degree question is confined to `k`-fold product / profile leaves.

**Honest residual (WALL).** The C7 projection-degree budget for the Gap-1
collapse products **and** the saturation products — the `def:explanation-occupancy`
fiber count (L2452) — remains the assumed enumerative input, as in #539/#622.
MASTER-2 shows *what* must be counted (two components) and that a single spectral
hypothesis `(S_E)` **certifies the collapse component** (`(S_E) => (FI)`), but it
does not enumerate the atlas.

---

## Rung 4 — FALSIFIER: the heavy-atom refutes the NARROW form (PROVED-negative)

The narrow conjecture — "`(S_E)`-violator ⟹ caught by C7 **effective-image
collapse**" — is **false**. Witness (verifier BLOCK 3, exact; `A_eff = 256`):

```
   mu(z*) = 1/4,   mu(z) = (3/4)/255 = 1/340 for the other 255 points z.
   L = 256 = A_eff  (FULL image)      G_1 = 1        ->  (FI) HOLDS, NO collapse
   Mx = 1/4                           Q_img = 64     ->  max-fiber Q FAILS
   P_2 = 11/170                       E = 1323/85 ≈ 15.56  ->  (S_E) FAILS
```

This profile **violates `(S_E)`** yet has `G_1 = 1`: it is **not** an
effective-image collapse (its boundary map reaches the **full** `A_eff` boundary
values — the exact negation of C7's L2453 trigger). So it **escapes** the
effective-image-collapse cell. It is caught by the **saturation** cell instead
(`Q_img = 64` exponential = a fiber `64×` above the image mean). **The narrow form
is refuted; the two-cell form survives** — the violator is routed to C7, just to
the *saturation* component, not the *collapse* component.

This is **not** a counterexample to the paper's **need**: the heavy-atom
**satisfies** `(FI)` (`L = A_eff`), so its span face is fine; and it fails
max-fiber Q, so the paper's saturation routing removes it before the primitive
payment. It is a counterexample to the **letter** of the conjecture (which cell),
decisive for the ledger wording: `(S_E)`-violation is **strictly broader** than
image collapse, and the extra breadth is the saturation class. **PROVED-negative.**

Contrast — is there a violator escaping **both** components (`G_1 = 1` **and**
`Q_img <= e^{o}`)? **No** (MASTER-2): `G_1 Q_img >= E+1`, so `G_1 = e^{o}` and
`Q_img = e^{o}` force `E = e^{o}` (`(S_E)` holds). There is **no third mode**. The
two-cell partition of `(S_E)`-violators is **exhaustive** (verifier BLOCK 5).

---

## Rung 5 — CENSUS (exact, verifier-recomputed)

`E = A_eff P_2 - 1` exact via `fractions.Fraction`. Three regimes, one dichotomy.

**(a) Single admissible power-sum leaves** (global chart `Phi(S)=(p_1..p_R)`,
`R < p`, `A_eff = p^R`; reproduces #622's census exactly — BLOCK 7):

| p | N | R | m | L | A_eff | E | `G_1` | `Q_img` | mode |
|---|---|---|---|---|-------|---|-------|---------|------|
| 3 | 2 | 1 | 1 | 2 | 3 | 1/2 | 3/2 | 1 | subexp (both) |
| 5 | 2 | 1 | 1 | 2 | 5 | 3/2 | 5/2 | 1 | subexp |
| 5 | 3 | 1 | 2 | 3 | 5 | 2/3 | 5/3 | 1 | subexp |
| 5 | 3 | 2 | 2 | 3 | 25 | 22/3 | 25/3 | 1 | subexp |
| 7 | 3 | 1 | 2 | 3 | 7 | 4/3 | 7/3 | 1 | subexp |
| 7 | 4 | 2 | 2 | 6 | 49 | 43/6 | 49/6 | 1 | subexp |
| 7 | 5 | 2 | 2 | 10 | 49 | 39/10 | 49/10 | 1 | subexp |

All uniform-on-image (`Q_img = 1`), `E` polynomial — `(S_E)` holds, never at the
divergence. `E` matches #622 byte-for-byte.

**(b) Collapse products (block-parabola)** — PURE COLLAPSE, MASTER-2 **tight**
(BLOCK 2):

| p | k | N=pk | L=p^k | A_eff=p^{2k} | E=p^k−1 | `G_1` | `Q_img` | `E+1 = G_1 Q_img` | rate log(1+E)/N |
|---|---|------|-------|--------------|---------|-------|---------|-------------------|------------------|
| 3 | 1 | 3  | 3   | 9      | 2    | 3   | 1 | 3 = 3·1 | 0.366 |
| 3 | 2 | 6  | 9   | 81     | 8    | 9   | 1 | 9 | 0.366 |
| 3 | 4 | 12 | 81  | 6561   | 80   | 81  | 1 | 81 | 0.366 |
| 5 | 4 | 20 | 625 | 390625 | 624  | 625 | 1 | 625 | 0.322 |
| 7 | 4 | 28 | 2401| 5764801| 2400 | 2401| 1 | 2401 | 0.278 |

**(c) Saturation products (heavy-atom per block)** — PURE SATURATION, MASTER-2
**slack** (BLOCK 4, `p=5`, `a=2/5`):

| k | A_eff=5^k | L=5^k | `G_1` | `Q_img=(pa)^k=2^k` | E+1=(5/4)^k | mode |
|---|-----------|-------|-------|--------------------|-------------|------|
| 1 | 5    | 5    | 1 | 2  | 5/4      | full image, `(FI)` holds |
| 2 | 25   | 25   | 1 | 4  | 25/16    | full image |
| 3 | 125  | 125  | 1 | 8  | 125/64   | full image |
| 4 | 625  | 625  | 1 | 16 | 625/256  | full image |

Rate `log(E1+1) = log(5/4) > 0` per block ⇒ `E+1 = (5/4)^k → ∞` (violates
`(S_E)`) with `G_1 = 1` throughout (**never** an effective-image collapse). This
is the product-scale twin of the single heavy-atom, and the dual of (b).

**Dichotomy (BLOCK 5, 244 checks):** across all test measures,
`E+1 <= max(G_1,Q_img)^2` and `E+1 <= G_1 Q_img`; both ratios subexponential ⟹
`(S_E)`. No leaf escapes both cells.

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| C7 = two components (saturation L2452 + effective-image collapse L2453), each an assumed enumerative input | verbatim extraction | **AUDIT** |
| MASTER-2: `E+1 = A_eff P_2 <= G_1 * Q_img` | Hölder `P_2 <= Mx` | **PROVED** (BLOCK 1) |
| C7's printed trigger = image-size collapse `G_1`; saturation `Q_img` is the other line | which mode E forces | **PROVED/AUDIT** (BLOCK 2/3) |
| two collapse modes distinct: parabola (`G_1`, tight) vs heavy-atom (`Q_img`, slack) | dual pair | **PROVED/MEASURED** (BLOCK 2/3/4) |
| **operative form: primitive residual `=> (S_E)`** (given its (FI)+max-fiber Q payments) | MASTER-2 | **PROVED** (BLOCK 5) |
| `(S_E) <=> (FI)` modulo max-fiber Q; `(S_E) => (FI)` unconditional | T-B | **PROVED** (BLOCK 6) |
| **narrow form REFUTED**: heavy-atom violates `(S_E)`, `G_1=1`, escapes collapse cell | routed to saturation instead | **PROVED-negative** (BLOCK 3) |
| no third mode: `G_1,Q_img` both subexp `=> E` subexp | exhaustive partition | **PROVED** (BLOCK 5) |
| divergence is a `k`-fold PRODUCT (single leaves `(S_E)`-safe) | multiplicativity, T3 #622 | **PROVED** (BLOCK 4/7) |
| Gap-2 span-collapse sub-case → C5 (not C7), vacuous on admissible | gap2 lane | **AUDIT** |
| C7 projection-degree budget (both components) for Gap-1 collapse + saturation products | the enumerative input | **OPEN / WALL** |

**Proposed ledger entry (for the maintainer).** *Refining #622's ledger choice.
The routing = spectrum conjecture is a theorem in its operative form and needs a
two-word correction in its literal form. (i) `(S_E)` is not an independent input:
on any primitive first-match residual, `E+1 <= (A_eff/L)(L·max mu) = G_1 Q_img`,
so the image clause `(FI)` (`G_1 <= e^{o}`) and the max-fiber Q payment
(`Q_img <= e^{o}`) — both already required — give `(S_E)` for free
(`c7_routing_spectrum.md`, MASTER-2). (ii) Modulo max-fiber Q, `(S_E) <=> (FI)`
(`(S_E) => (FI)` is unconditional, #614). (iii) The C7 cell (L2440–2454) is TWO
assumed enumerative inputs — the saturation occupancy degree (L2452) and the
effective-image-collapse projection degree (L2453) — and BOTH are load-bearing:
the block-parabola triggers the collapse degree, and a heavy-atom-with-spread-tail
profile violates `(S_E)` with a FULL image (`L = A_eff`, `(FI)` holds) and is
caught only by the saturation degree, so naming only the collapse cell (as #622's
conjecture did) misses half the `(S_E)`-violators. Print the C7 projection-degree
budget for BOTH components as the open input; then `(S_E)` follows, and it may be
printed as the spectral CERTIFICATE of the collapse component only (it does not
replace the saturation payment). This is an OPEN input, not an established fact —
the packet proves the trigger logic is exhaustive and reduces the count to
products, but does not enumerate the atlas.*

### The 2–3 steps the PI should re-derive

1. **MASTER-2 (2.1).** `E+1 = A_eff sum mu^2 <= A_eff max mu = (A_eff/L)(L max mu)
   = G_1 Q_img`; the only step is `sum mu^2 <= max mu` (Hölder). Equality iff `mu`
   uniform on its support (the block-parabola). This one line is the whole rung.
2. **The two witnesses (2.2, Rung 4).** Block-parabola: `G_1 = p^k`, `Q_img = 1`,
   MASTER-2 tight — pure image collapse, C7's L2453 trigger. Heavy-atom: `G_1 =
   1` (`(FI)` holds, full image), `Q_img ≈ A_eff^{3/4}`, MASTER-2 slack — pure
   saturation, C7's L2452 line. Same `(S_E)`-violation, opposite image verdict:
   `E` does NOT determine `L`. This refutes the narrow form and pins the crux.
3. **T-A / T-B (Rung 3).** primitive residual (`(FI)` + max-fiber Q) `=> (S_E)`
   by MASTER-2; and `(S_E) <=> (FI)` modulo max-fiber Q (with `(S_E) => (FI)`
   unconditional, #614). Hence `(S_E)`, `(FI)`, `¬(C7-collapse)` coincide on the
   primitive class; the residual open object is the C7 projection-degree count,
   for BOTH components, confined to product leaves (T3).

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_c7_routing_spectrum.py   # RESULT: PASS (731/731)
```
