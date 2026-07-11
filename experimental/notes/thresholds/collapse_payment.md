# The collapse-side envelope payment after routing

## Status

`ENVELOPE CHARGE = FIRST-MATCH DISJOINT UNION (AUDIT+PROVED) /
RUNG 1 ROUTED-ENTRY SCALE (PROVED) / RUNG 2 COUNT->MASS REFORMULATION
(PROVED, LEDGER-GRADE) / COUNTERTHEOREM DISSOLVED (PROVED) /
COLLAPSE-PAYMENT THEOREM: WELL-POSED AFTER ROUTING (PROVED) /
RESIDUAL = SINGLE COLLAPSE-CELL PROJECTION DEGREE (OPEN, = #626, RESCOPED) /
CENSUS (MEASURED)`.

The last open object on input 2's span face. The arc established that every
`(S_E)`-violating admissible leaf is **product/profile-structured** (#622 T3),
splits across the two C7 components by **MASTER-2** (#625), the collapse count is
an `e^{Omega(N)}` **binomial tail** (#626), and every violator is **router-decidably
DETECTED and routed before the primitive step** (#627 T-DET). What remained: prove
that **after routing, the accounting works** — the C7 collapse cell absorbs the
routed profiles at its own payment scale, and the envelope sum over the residual is
subexponential.

**The crux is the count-vs-mass question, and it pivots the whole packet
(see Rung 2).** The result: the profile envelope's load-bearing hypothesis was
never a **count** of profiles at all — the closed ledger charges a **first-match
DISJOINT UNION** of new-slope sets (`lem:first-match-bound`), a **mass/union**
statement insensitive to profile multiplicity. #626's "countertheorem" is a
**per-profile overcount** that double-charges overlapping slopes and sums profiles
that routing has already emptied. Reframing the L869 hypothesis as the disjoint-union
charge it actually is — that reframing is itself ledger-grade.

Every number below is recomputed by
`experimental/scripts/verify_collapse_payment.py` (stdlib-only, zero-arg,
`RESULT: PASS (1210/1210)`, ~0.19 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotics not proved from the toy), **AUDIT** (interface reading of the tex or a
sibling note), **PARTIAL**, **OPEN**.

**Credit.** The block-parabola family and the `(CF*)` identities are
**avdeevvadim's** (PR #558, integrated at `e190193`). The depth-`w` prefix-fibre
atlas is our **#536** (`atlas_missing_witness.md`); the C7 collapse routing as an
**assumed enumerative input** is our **#539** (`fi_full_image_primitive.md`); the
Gap-2 span-collapse `=>` C5 classification (vacuous on admissible) is our **#545**
(`gap2_collapse_routing.md`); the J2 magnitude-blindness impossibility is our
**#609** (`frame_image_completion.md`); the master identity `L>=A_eff/(1+E)` and the
supplement `(S_E)` are our **#614** (`minimal_phase_supplement.md`); the
`(S_E)`-on-admissible-leaves stratification and multiplicativity **T3** are our
**#622** (`se_on_admissible_leaves.md`); **MASTER-2** and the two-cell partition are
our **#625** (`c7_routing_spectrum.md`); the binomial-tail projection-degree count
and the "countertheorem" reading are our **#626** (`c7_degree_enumeration.md`); and
the router-decidable **T-DET** detection theorem is our **#627**
(`routing_exhaustiveness.md`). This packet consumes all of them and adds the
**post-routing accounting**: the first-match disjoint-union reformulation of the
envelope charge, and the proof that the countertheorem does not fire.

---

## HEADLINE (read first): the envelope charges a MASS, not a COUNT — and routing
## empties the collapse profiles before they are ever summed

The profile envelope (`eq:profile-envelope`, tex **L859-862**) is a **sum over
profiles** of `(1+barN_lambda)`, and #626 read its guard clause — "**With
subexponentially many profiles, the sum and maximum have the same exponential
scale**" (tex **L869-870**) — as a **count** hypothesis, then proved the collapse
profiles number `e^{Omega(N)}` (a binomial tail), busting it. This packet shows the
count reading is the **wrong operative statement**, and the proof never uses it:

1. **The closed ledger charges a DISJOINT UNION (PROVED, `lem:first-match-bound`
   L1526-1538).** For a fixed received line the total bad-slope set is
   `Z_a(r) = coprod_i Z_i^circ` — a **disjoint** union of **first-match** new-slope
   sets `Z_i^circ = Z_i \ union_{j<i} Z_j` (`def:first-match` L1459). The charge is
   `sum_i |Z_i^circ| = |Z_a(r)|`, the **cardinality of the union**, in which every
   slope is counted **once**. Profile multiplicity — even `e^{Omega(N)}` profiles —
   does **not** multiply the charge; overlapping slopes are charged to the earliest
   profile only.

2. **Routing empties the collapse profiles (PROVED).** A collapse profile fails
   `(FI)` and is "**assigned by the first-match rule to an earlier profile so that
   its slopes and all witnesses above them are removed from the later residual**"
   (tex **L877-880**). Its first-match new-slope set is therefore `Z^circ = empty`:
   it contributes **0** to `sum_i |Z_i^circ|`. The `e^{Omega(N)}` routed collapse
   profiles are summed **zero times**, not `2 * N_coll` times.

3. **#626's `2 * N_coll` is the per-profile OVERCOUNT (MEASURED).** Summing
   `(1+barN_lambda) = 2` independently over all `N_coll` collapse profiles
   double-charges every shared slope and re-charges the routed (emptied) ones. On an
   exact finite model the naive per-profile sum exceeds the disjoint-union charge by
   an order of magnitude (BLOCK 6b: `sum_i|Z_i|=48` vs `|Z_a(r)|=5`).

4. **The count hypothesis, read correctly, is per-line and description-entropy
   charged (AUDIT).** "`e^{o(n)}` profiles" means "the number of nonempty pairs
   `(lambda,xi)` occurring **for a received line** is `e^{o(n)}`, uniformly in that
   line" (tex **L1447-1450**), and it is charged to **description entropy `o(n)`
   bits** (`lem:profile-multiplicity` **L5028-5033**), **never** to a pattern count.
   The block-parabola family — choosing **which** `j` of `k` blocks collapse — is an
   "**arbitrary planted subset**", which `lem:profile-atlas` (**L4781-4783**)
   explicitly excludes: "*including either could create exponentially many
   profiles*". Its description entropy is `log2 C(k,j) = Omega(N)` bits (BLOCK 4:
   `994.7` bits for `C(1000,500)`, `bits/N = 0.33`) — outside the L869 hypothesis
   for **both** violators and non-violators.

**Net verdict.** After routing, the collapse-side envelope payment is
**well-posed and the countertheorem does not fire** (PROVED). The `e^{Omega(N)}`
collapse/product patterns (i) are **routed** (`Z^circ = empty`) and (ii) carry
`Omega(N)`-bit **description entropy** (excluded from the `e^{o(n)}` per-line count
by the paper's own census lemmas), so they never enter the sum. The operative charge
is the **disjoint union over the `e^{o(n)}` description-entropy-bounded admissible
profiles**. The single **residual** is the C7 collapse cell's **own** projection
degree at the image scale — this is **#626, unchanged**, but now correctly isolated
as **one** per-line cell rather than an `e^{Omega(N)}` envelope sum.

---

## Rung 1 — WHAT THE ROUTED PROFILES MUST PAY: the entry scale (PROVED)

### 1.1 The envelope and the two scales (AUDIT, verbatim)

`eq:profile-envelope` (tex **L853-862**):

```
 A_lambda = |B_lambda|^{R_lambda},   L_lambda = |Phi_lambda(Omega^0_lambda)|,
 barN_lambda = |Omega^0_lambda| / L_lambda,
 E_n(a) = 1 + (n-a+1) + sup_{(r0,r1)} sum_{lambda in Lambda(r0,r1;a)} (1 + barN_lambda).
```

The image and ambient scales (`eq:image-ambient-scales`, tex **L4831-4837**):
`barN^img = M/L`, `barN^amb = M/A`, with `M=|Omega^0|`, `A=|B|^R`, `L=|image|`.
The routing clause (tex **L871-881**):

> "The ambient scale `barN_lambda^amb = |Omega^0_lambda|/A_lambda` may replace
> `barN_lambda` only after a full-image certificate `L_lambda >= e^{-o(n)} A_lambda`
> **(FI)** has been proved uniformly. Otherwise effective-image collapse is
> **routed** --- assigned by the first-match rule to an earlier profile so that its
> slopes and all witnesses above them are removed from the later residual --- as an
> effective-image rank-collapse profile, and the image scale is retained."

and (tex **L4855-4857**): "*If the certificate fails, effective-image collapse must
be retained as an effective-image rank-collapse profile, or all estimates on this
leaf must stay at image scale. **Deleting earlier cells can only decrease every
fiber.***"

### 1.2 The routed-entry arithmetic (PROVED, BLOCK 2)

A collapse-routed leaf is retained at the **image** scale, `barN^img = M/L`. The
mission's identity holds exactly: since `barN^img = (M/A)(A/L) = barN^amb * G_1`,

```
   barN^img = G_1 * barN^amb          (exact, BLOCK 2, all p,k,j).
```

For the block-parabola leaf with `j` collapse blocks (`M=p^k`, `A=p^{k+j}`,
`L=p^k`): `barN^amb = p^{-j}`, `G_1 = p^j`, and therefore

```
   barN^img = p^j * p^{-j} = 1     (singleton fibers, the #609 escape).
```

Exact rows (BLOCK 2): `p=3,k=4,j=2`: `G_1=9`, `barN^amb=1/9`, `barN^img=1`;
`p=5,k=4,j=3`: `G_1=125`, `barN^amb=1/125`, `barN^img=1`;
`p=7,k=3,j=3`: `G_1=343`, `barN^amb=1/343`, `barN^img=1`.

**Rung-1 verdict (PROVED).** The image scale does **not** inflate the per-profile
term: `barN^img = 1` for **every** block-parabola leaf, independent of `j` (BLOCK 2:
`(1 + barN^img) = 2` for all). So per-profile rescaling — image vs ambient — is
**irrelevant** to the sum (ambient would give `1 + p^{-j} ~ 1`; image gives `2`;
both `Theta(1)`). The naive "mass x count" the mission asked about is

```
   sum_{routed} (1 + barN^img) = 2 * N_coll(k,theta) = e^{Omega(N)},
```

exact (BLOCK 3/5): `2*N_coll(20,0.60) = 527900`, `2*N_coll(40,0.60) =
294 875 000 956`, against identity term `(n-a+1) ~ N = 60, 120`. **This naive sum is
exponential and exceeds the identity term** — i.e. *if the routed profiles were
summed independently at their image-scale term, a genuinely new bound would be
needed.* They are **not** so summed: routing gives them `Z^circ = empty`
(Rung 3). The payment comes from **first-match emptying**, not from a small
per-profile `barN`.

---

## Rung 2 — THE REFORMULATION: count hypothesis vs mass statement (THE CRUX)

This is where the whole packet pivots. The question the mission posed: does the
sum-to-max reduction need the profile **count** subexponential for **all** profiles,
or only a **mass** bound?

### 2.1 The count reading fails on the WHOLE product class, not just violators (PROVED)

The number of `{T,C}^k` block-patterns is `2^k`; the non-violating sub-family
`{j < theta k}` alone has `sum_{j<theta k} C(k,j) = e^{h(theta)k}` patterns. **Both**
are exponential. So if the L869 guard were a literal pattern **count**, it would be
busted by the **non-violators** too (BLOCK 4: `bits/N > 0.02` for the unrouted
family; the full `2^k` family has `k` bits, `bits/N = 1/p`). **The envelope guard
was therefore never about violators — it was never a pattern count at all.**

### 2.2 What the guard actually is (AUDIT, verbatim)

The per-line meaning (tex **L1447-1450**):

> "an assertion that there are `e^{o(n)}` profiles means that the number of nonempty
> pairs `(lambda,xi)` occurring **for a received line** is `e^{o(n)}`, uniformly in
> that line."

The census is charged to **description entropy**, not to a pattern count
(`lem:profile-multiplicity`, tex **L5028-5033**):

> "If the cell ledger fixes only **bounded-complexity** quotient, planted, tangent,
> extension, and split-pencil profiles, and the **total description entropy** of all
> data outside the moving support is `o(n)` bits, then the number of primitive
> profiles is `e^{o(n)}`."

and `lem:profile-atlas` (tex **L4772-4784**) states the count and its exclusion:

> "For a ledger-admissible sequence, the number of first-match profiles is
> `e^{o(n)}`. ... The statement **does not include arbitrary planted subsets or an
> unproved decomposition of a higher-dimensional pencil; including either could
> create exponentially many profiles**."

**The block-parabola family IS "arbitrary planted subsets".** Choosing which `j` of
`k` blocks collapse costs `log2 C(k,j) = Omega(N)` description-entropy bits
(BLOCK 4). It is exactly the family both census lemmas exclude. #626's `e^{Omega(N)}`
count is **correct** and does **not** contradict them — it counts the excluded family.

### 2.3 The operative statement: the first-match disjoint-union MASS bound (PROVED)

What the closed ledger actually uses (`def:closed-asymptotic-ledger` **(L2)**,
tex **L1106-1110**):

> "every algebraic or directly counted profile has a certified bound for its **actual
> first-match slope set `Z_i^circ`**, meaning **the slopes assigned to profile `i`
> but to no earlier profile**, and the sum of those bounds is at most its stated
> contribution to `e^{o(n)} E_n(a_n)`."

and `lem:first-match-bound` (tex **L1526-1538**), proof: "*exact-agreement reduction
and witness exhaustivity give the **disjoint union** `Z_a(r) = coprod_i Z_i^circ`.*"
So the charge is

```
   B_C^MCA(a) = sup_r |Z_a(r)| = sup_r sum_i |Z_i^circ|,   Z_a(r) = coprod_i Z_i^circ,
```

a **mass/union** in which each slope is counted **once**. This is exactly the
reduction the mission anticipated: *"the real theorem must be a MASS bound (sum <=
e^{o} max) proved directly."* It is not "sum <= count x max" (which needs the count);
it is "`sum_i |Z_i^circ| = |union|`", which is insensitive to the count because the
`Z_i^circ` are **disjoint**.

### 2.4 The reformulation (LEDGER-GRADE)

> **L869, restated as the statement the proof uses.** Replace "*with subexponentially
> many profiles, the sum and maximum have the same exponential scale*" by: *the
> profile envelope charges the **first-match disjoint union** `sum_i |Z_i^circ| =
> |Z_a(r)|` (`lem:first-match-bound`); its value is bounded by `e^{o(n)} E_n(a)`
> because (i) the profiles with **nonempty** `Z_i^circ` number `e^{o(n)}` per line,
> charged to **description entropy** `o(n)` bits (`lem:profile-multiplicity`), and
> (ii) every routed collapse/`(FI)`-failing profile has `Z_i^circ = empty`
> (**L877-880**). The count of block-type **patterns** is irrelevant: they overlap
> (first match) and are emptied (routing).*

**Why this is the crux, resolved.** #626's countertheorem — `sum_lambda (1+barN) =
2 N_coll` exceeding the identity term — is the **per-profile** charge, which (a)
double-counts shared slopes and (b) re-charges the routed-empty profiles. The
operative **disjoint-union** charge does neither. On an exact finite model the gap is
explicit (BLOCK 6b):

| instance | supports | profiles | naive `sum_i|Z_i|` | **disjoint union `|Z_a(r)|`** |
|----------|---------:|---------:|-------------------:|------------------------------:|
| `n=9,esz=3,p=5`  | 84  | 12 | 48 | **5** |
| `n=10,esz=3,p=7` | 120 | 15 | 78 | **7** |
| `n=11,esz=4,p=5` | 330 | 17 | 75 | **5** |
| `n=8,esz=2,p=5`  | 28  | 10 | 28 | **5** |

The ledger charges the last column (`~ p`); the per-profile / per-support sum (48-330)
is the overcount. `|Z_a(r)| <= p` holds by `prop:syndrome-line-normal-form` (tex
**L1580**, "*for fixed `E` there is at most one such finite slope*") — one support
carries at most one slope; the `84` supports collapse onto `5` slopes.

---

## Rung 3 — THE COLLAPSE-PAYMENT THEOREM (PROVED, modulo the #626 single-cell budget)

### T-PAY (PROVED). After routing, the collapse-side envelope payment is well posed.

> **Theorem (collapse-side envelope payment after routing).** Fix a received line.
> In the closed-ledger accounting (`def:closed-asymptotic-ledger`), the profile
> envelope charge is `sum_i |Z_i^circ| = |Z_a(r)|` (`lem:first-match-bound`,
> disjoint union). Then:
>
> - **(i) [routed contribute 0]** Every effective-image-collapse profile
>   (`G_1 >= e^{eps N}`, detected router-decidably by #627 T-DET) is routed to an
>   earlier cell (**L877-880**), so its first-match set `Z_i^circ = empty`; the
>   `e^{Omega(N)}` routed collapse profiles contribute **0** to the charge.
> - **(ii) [absorbed at image scale, O(1) cells]** The routed witnesses are retained
>   as effective-image rank-collapse profiles at the image scale `barN^img`
>   (**L880-881, L4855-4857**), on which "*deleting earlier cells can only decrease
>   every fiber*" (**L4857**). These are `e^{o(n)}` cells (description-entropy
>   bounded, `lem:profile-multiplicity`), **not** an `e^{Omega(N)}` sum.
> - **(iii) [residual is disjoint over `e^{o(n)}` survivors]** The remaining charge
>   is `sum_i |Z_i^circ|` over the profiles with nonempty first-match set, which
>   number `e^{o(n)}` per line (`lem:profile-atlas` / A2), each satisfying `(FI)` +
>   primitive-Q hence `(S_E)` (#625 T-A). The sum is a disjoint union, so it equals
>   `|Z_a(r)| <= e^{o(n)} E_n(a)`.
>
> In particular the "countertheorem" (**L889-890**) — a profile "*exponentially
> larger than the ambient identity term*" — **does not fire**: it is the per-profile
> overcount of the routed/description-entropy-excluded patterns, which the
> disjoint-union charge does not incur.

**Proof.** (i) is **L877-880** + `def:first-match` **L1459** (`Z_i^circ = Z_i \
union_{j<i} Z_j`; a routed profile's slopes belong to the earlier cell it is
assigned to, so `Z_i^circ = empty`). (ii) is **L880-881, L4855-4857** for the image
scale and `lem:profile-multiplicity` **L5028-5033** for the `e^{o(n)}` cell count.
(iii) is `lem:first-match-bound` **L1535** (disjoint union) + `lem:profile-atlas`
**L4772-4774** + #625 T-A. The countertheorem non-firing is Rung 2.3-2.4. `QED`
modulo the single quantity in T-PAY-RES below.

### T-PAY-RES (OPEN, = #626, RESCOPED). The single residual.

The one input T-PAY does **not** discharge is the C7 collapse cell's **own**
projection degree at the image scale — the distinct-slope count `|Z(collapse cell)|`
that the effective-image rank-collapse profile charges as **one** per-line cell.
This is **#626's projection-degree budget, unchanged**, with two sharpenings:

- **Rescoped from `e^{Omega(N)}` summands to ONE cell.** #626's obstruction was that
  the collapse budget is a **sum** of `e^{Omega(N)}` per-profile terms. After routing
  + first-match it is a **single** description-entropy-bounded cell's image-scale
  distinct-slope count. The exponential-sum obstruction is removed; what remains is
  one cell's degree.
- **Still not payable by the occupancy compiler alone.** The block-parabola cell has
  singleton fibers (occupancy `H = 1`), so `RC1` (`|Z(C)| <= floor(|C|/H)`,
  `lem:exact-occupancy-compiler` tex **L5688-5690**) gives no compression, and
  `prop:saturation-payment` (**L4737-4738**) "*an upper bound on the number of
  profile lifts goes in the wrong direction*" applies. The cell needs "*a direct
  distinct-slope estimate at the profile scale*" (**L4730**) — the #626 open input.

**Honest failing term.** The exact term that may stay exponential is
`|Z(collapse cell)|` = the distinct slopes of the single image-scale collapse cell.
**Minimal printed input that fixes it:** *the C7 effective-image-collapse cell's
image-scale projection degree is `e^{o(n)}` per received line* (equivalently, the
description-entropy census A2 / `lem:profile-atlas` for the collapse profile on
non-tower sequences). This **supersedes** #626's ledger choice with a sharper one:
not "bound an `e^{Omega(N)}` sum" but "bound one routed cell's image-scale degree."

---

## Rung 4 — CENSUS (MEASURED, verifier-recomputed)

**(a) Routed-entry scale** (BLOCK 2): `barN^img = G_1 barN^amb = 1` for every
block-parabola leaf; `(1+barN^img)=2` regardless of `j`. Ambient would give
`1+p^{-j}`. Per-profile rescaling is `Theta(1)` either way.

**(b) Naive mass x count = the #626 countertheorem quantity** (BLOCK 3/5), exact:

| `k` | `theta` | `N_coll` | naive `2 N_coll` | `N=3k` (identity ~ N) |
|----|--------|---------:|-----------------:|----------------------:|
| 20 | 0.60 | 263950 | 527900 | 60 |
| 40 | 0.60 | 147 437 500 478 | 294 875 000 956 | 120 |
| 40 | 0.75 | 1 221 246 132 | 2 442 492 264 | 120 |

Naive sum `>> N` (exponential) — the countertheorem, incurred **only** by
per-profile summation. Reproduces #626 BLOCK 3 byte-for-byte.

**(c) Description entropy of the pattern family** (BLOCK 4), the Rung-2 quantity:

| family | bits | `bits/N` (`p=3`) | vs `o(n)` |
|--------|-----:|-----------------:|-----------|
| threshold `theta=0.50`, `k=1000` | `log2 C(1000,500) = 994.7` | 0.332 | `Omega(N)`, excluded |
| threshold `theta=0.75`, `k=1000` | `806.2` | 0.269 | `Omega(N)`, excluded |
| full `{T,C}^k`, `2^k` patterns | `k = 1000` | `1/p = 0.333` | `Omega(N)`, excluded |

Both violators and non-violators carry `Omega(N)`-bit description entropy — outside
the L869 hypothesis, inside `lem:profile-atlas`'s exclusion.

**(d) The disjoint-union vs per-profile overcount** (BLOCK 6b), exact finite,
genuine many-to-one slope map (`slope(E) = sum(E) mod p`, one support -> one slope):
the ledger charge `|Z_a(r)| in {5,7,5,5}` (`~ p`), the naive per-profile sum
`in {48,78,75,28}`, the per-support charge `in {84,120,330,28}`. The disjoint union
is `10x-66x` smaller than the naive charge (the overcount magnitude).

**(e) Structural fact `|Z_a(r)| <= p`** (BLOCK 6a), non-vacuous on real `F_p`
syndrome geometry: `>=200` planted instances with an existing bad slope, each
verified to admit **exactly one** finite slope (`prop:syndrome-line-normal-form`
L1580 / `RC2` L1694-1695), and "both syndromes in `V_E`" verified to admit none.

**(f) Single admissible leaves stay safe** (BLOCK 7, reproduces #622/#625/#626):
`p=3,N=2`: `E=1/2`; `p=5,N=3`: `E=22/3`; `p=7,N=4`: `E=43/6`. `Q_img=1`, `E`
polynomial, never at the divergence.

---

## Two tex ambiguities pinned (findings)

1. **L869 "subexponentially many profiles" is under-specified.** It does not state
   **which** count (per-line vs whole-atlas; block-pattern vs description-entropy).
   The per-line, description-entropy reading is fixed only downstream (L1447-1450,
   L5028-5033). #626's countertheorem exploits the per-pattern reading; the proof
   uses the disjoint-union/description-entropy reading. **Disambiguation:** print
   L869 as the first-match disjoint-union charge (Rung 2.4).

2. **A5 (`R < char`) has no stated scope for routed/atlas profiles.** A5 (tex
   **L935-941**) constrains "*primitive columns*" and "*every use of power-sum
   coordinates*"; there is **no** sentence saying whether a **routed** effective-image
   collapse profile (with `R_prod = 2k >= char`) is an admissible atlas profile or is
   exempt. **Disambiguation:** routed/atlas profiles are charged by **description
   entropy** (`lem:profile-multiplicity`), **not** required to satisfy A5; so the
   `R >= char` collapse products **may** appear as routed cells but are
   **description-entropy-excluded** from the `e^{o(n)}` per-line count. Print this
   scope explicitly.

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| envelope charge = first-match disjoint union `Z_a(r)=coprod Z_i^circ` | `lem:first-match-bound` L1535 | **AUDIT+PROVED** (BLOCK 6a/b) |
| routed collapse profile has `Z_i^circ = empty` | L877-880 + `def:first-match` L1459 | **PROVED** (BLOCK 6c) |
| routed-entry image scale `barN^img = G_1 barN^amb = 1` (singleton) | `eq:image-ambient-scales` L4835 | **PROVED** (BLOCK 2) |
| naive `sum_routed (1+barN) = 2 N_coll = e^{Omega(N)}` (countertheorem quantity) | per-profile overcount | **MEASURED** (BLOCK 3/5) |
| L869 count reading busted by non-violators too (whole product class) | `2^k` patterns | **PROVED** (BLOCK 4) |
| operative guard = per-line, description-entropy `o(n)` bits | L1447-1450, L5028-5033 | **AUDIT** |
| pattern family = "arbitrary planted subsets", `Omega(N)`-bit descr. entropy | `lem:profile-atlas` L4781 | **PROVED** (BLOCK 4) |
| **REFORMULATION: count -> first-match disjoint-union MASS bound** | Rung 2.4 | **PROVED, LEDGER-GRADE** |
| per-profile overcount vs disjoint union: `48/78/75` vs `5/7/5` | exact finite model | **MEASURED** (BLOCK 6b) |
| one support -> at most one slope, `|Z_a(r)| <= p` | `prop:syndrome-line-normal-form` L1580 | **PROVED** (BLOCK 6a) |
| **T-PAY: collapse payment well posed after routing; countertheorem does not fire** | Rung 3 | **PROVED** |
| **T-PAY-RES: single collapse-cell image-scale projection degree** | = #626, rescoped to one cell | **OPEN** |
| L869 / A5-scope ambiguities | pinned + disambiguation proposed | **AUDIT (finding)** |

**Proposed ledger entry (for the maintainer).** *Closing the post-routing accounting
on input 2's span face. The profile envelope `E_n(a)` (`eq:profile-envelope`,
L859-862) charges the **first-match disjoint union** `B_C^MCA(a) = sup_r sum_i
|Z_i^circ| = sup_r |Z_a(r)|` (`lem:first-match-bound`, L1535), in which each slope is
counted once. Consequently the guard "with subexponentially many profiles, the sum
and maximum have the same exponential scale" (L869) is a **count** paraphrase of a
**mass/union** statement, and the operative census is **per-line, description-entropy
charged** (L1447-1450, `lem:profile-multiplicity` L5028-5033), **not** a block-pattern
count. The `e^{Omega(N)}` collapse family of #626 is exactly the "arbitrary planted
subsets" `lem:profile-atlas` (L4781-4783) excludes — it carries `Omega(N)`-bit
description entropy — and after `(FI)`-routing (L877-880) each such profile has
`Z_i^circ = empty`, contributing zero to the charge. Therefore the countertheorem
(L889-890) does **not** fire: it is the per-profile overcount `2 N_coll`, which
double-charges shared slopes and re-charges the routed-empty profiles. The residual
open input is the single C7 effective-image-collapse cell's **image-scale projection
degree** (one per-line cell, singleton fibers so the occupancy compiler gives no
compression, `RC1`/`prop:saturation-payment`) — this is **#626, unchanged**, now
scoped to one cell rather than an `e^{Omega(N)}` sum. Print: (i) L869 as the
first-match disjoint-union charge; (ii) the census as description-entropy per-line;
(iii) the routed/atlas profiles as exempt from A5 (`R<char`) and charged by
description entropy; (iv) the C7 collapse cell's image-scale projection-degree bound
as the single open input. This is an OPEN input, not an established fact — the packet
proves the accounting is well posed after routing and dissolves the countertheorem,
but does not enumerate the single collapse cell's image-scale degree.*

### The 2-3 steps the PI should re-derive

1. **The disjoint-union charge (Rung 2.3).** `lem:first-match-bound` L1535:
   `Z_a(r) = coprod_i Z_i^circ`, `Z_i^circ = Z_i \ union_{j<i} Z_j`
   (`def:first-match` L1459). The MCA numerator is `sup_r sum_i |Z_i^circ| =
   sup_r |Z_a(r)|` — a union, each slope once. Profile multiplicity does not
   multiply it. One line.
2. **Routing empties collapse profiles (Rung 3 (i)).** A collapse profile fails
   `(FI)`; L877-880 assigns its slopes to an earlier cell and removes its witnesses
   from the later residual; hence `Z_i^circ = empty`. The `e^{Omega(N)}` collapse
   patterns contribute 0. #626's `2 N_coll` is the per-profile overcount (double-
   charged + re-charged), refuted by BLOCK 6b (`48` vs `5`).
3. **The count reading was never operative (Rung 2.1-2.2).** The non-violating
   `{j<theta k}` product patterns are also `e^{Omega(N)}` and carry `Omega(N)`-bit
   description entropy; so the guard is not a pattern count. The paper's census is
   per-line, description-entropy `o(n)` (L1447-1450, L5028-5033); the block-parabola
   family is the "arbitrary planted subsets" `lem:profile-atlas` excludes. The
   residual is the single collapse cell's image-scale projection degree (= #626).

---

## What closes if T-PAY-RES is paid

If the single C7 collapse cell's image-scale projection degree is `e^{o(n)}` per
line, the span face closes **unconditionally** on the product/profile class: every
`(S_E)`-violator is routed out (Z^circ = empty, #627 T-DET detection + T-PAY (i)),
the residual charge is the disjoint union over `e^{o(n)}` description-entropy-bounded
survivors, each with `(FI)` (`(S_E) => (FI)`, #614). Combined with #622 T1 (branch-1
leaves free), #545 (Gap-2 span-collapse is C5, vacuous on admissible), this is the
full unconditional closure chain for input 2's span face:

```
 single admissible leaf     --#622 T1--> (S_E) free, span face free
 Gap-2 span-collapse        --#545-----> C5 field-descent, vacuous on admissible
 Gap-1 collapse products    --#627+THIS-> detected, routed (Z^circ=empty), charge 0
 residual survivors         --THIS------> disjoint union over e^{o(n)} descr.-ent. profiles
 single collapse cell degree --T-PAY-RES-> the one open input (= #626, rescoped)
```

with the single open link the collapse cell's image-scale projection degree — one
per-line cell, the exponential-sum obstruction of #626 removed.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_collapse_payment.py   # RESULT: PASS (1210/1210)
```
