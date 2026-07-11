# Paying the C7 projection-degree budgets on product leaves

## Status

`CONSUMER PINNED (AUDIT) / COLLAPSE-COUNT = BINOMIAL TAIL (PROVED) /
SATURATION-COUNT = BINOMIAL TAIL (PROVED) / BUDGET VERDICT: PARTIAL
(NOT PAYABLE BY ENUMERATION, PROVED; PAID ONLY VIA (FI)-ROUTING = #622/#625
OPEN) / CENSUS (MEASURED)`.

Research packet that pays — enumerates and bounds — the **two** C7
projection-degree budgets left by the span-face arc. Our **PR #625**
(`c7_routing_spectrum.md`, MASTER-2) and **PR #622**
(`se_on_admissible_leaves.md`, T3) proved that every `(S_E)`-violating
admissible leaf is **product/profile-structured** and splits across the two
printed components of the C7 cell (tex L2440–2454). Whatever the maintainer
decides on the #622/#625 ledger choice, **both** budgets are needed. This packet
supplies the missing enumeration: it identifies the exact budget consumer, proves
the count of collapse/saturation cells is a **binomial tail** — exponentially
many profiles — and reads that count against the printed accounting.

Every number below is recomputed by
`experimental/scripts/verify_c7_degree_enumeration.py` (stdlib-only, zero-arg,
`RESULT: PASS (233/233)`, ~3 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotics not proved from the toy), **AUDIT** (interface reading of the tex or
a sibling note), **WALL** (identified obstruction), **OPEN**.

**Credit.** The block-parabola family and the `(CF*)` identities are
**avdeevvadim's** (PR #558, integrated at `e190193`). The depth-`w` prefix-fibre
atlas (`Phi_w:binom(D,a)->B^w` total, `L<=p^w`, witness-exhaustive) is our **#536**
(`atlas_missing_witness.md`); the finding that the C7 collapse routing is an
**assumed enumerative input, not a theorem** is our **#539**
(`fi_full_image_primitive.md`); the Gap-2 span-collapse `=>` C5 field-descent
classification, **vacuous on admissible leaves** (`w<char`), is our **#545**
(`gap2_collapse_routing.md`); the `(S_E)`-on-admissible-leaves stratification and
`E+1` multiplicativity **T3** are our **#622**; and MASTER-2 with the two-cell
partition of `(S_E)`-violators is our **#625**. This packet consumes all five and
adds the enumeration of the two components at the degree scale the tex requires.

---

## HEADLINE (read first)

The two C7 budgets are the count of **effective-image-collapse** cells (`G_1`
large) and **saturation** cells (`Q_img` large). By MASTER-2 both quantities are
**products of per-block ratios `>= 1`** (T3), so exponential violation forces a
**positive fraction** of non-trivial blocks. The number of atlas profiles that
reach the threshold is therefore an **exact binomial tail**

```
   N_viol(k, theta) = sum_{j >= theta k} C(k, j),      theta = eps * p / ln p,
```

with `N = pk` and exponential rate `h(theta)` (for `theta > 1/2`) or `ln 2` (for
`theta <= 1/2`) — **always strictly positive**. So there are `e^{Omega(N)}`
collapse profiles and `e^{Omega(N)}` saturation profiles. This is
**exponentially many profiles**, which **busts the load-bearing hypothesis** of
the printed budget: the profile envelope `E_n(a)` (tex `eq:profile-envelope`,
L857–862) collapses its sum to its maximum **only** "with subexponentially many
profiles" (**tex L869–870**). Feeding the collapse profiles into `E_n` with their
singleton-fiber occupancy (`Nbar = 1`, the #609 escape) makes the sum exceed the
identity term — **exactly "the countertheorem" named at tex L889**.

**Net verdict: PARTIAL, and the two components are symmetric.** The count
**provably exceeds** the printed enumeration budget on the deep product/profile
class (rate `> 0`, PROVED). The only escape is **(FI)/first-match routing** (tex
L877–881): each collapse profile fails `(FI)` and is assigned to an earlier
profile and deleted before the envelope sum is taken. That routing is the
**assumed enumerative input** (#539/#622/#625), **unchanged** — but this packet
now equips it with an **exact lower bound** `e^{(rate/p)N}` on the number of
profiles the routing must remove, and proves that the tex's own **entropy-loss
lemmas do not pay it** (they need a support-count reduction; Gap-1 collapse has
**full support**, so `lem:planted-entropy`/`lem:quotient-entropy` are
inapplicable). Collapse is moreover **typical, not rare**: a random product leaf
already collapses at rate `(ln p)/(2p)` (its expected non-trivial-block count is
`k/2`), so the collapse cell cannot be dismissed as measure-zero.

---

## Rung 1 — THE TWO ASSUMED INPUTS, verbatim (AUDIT)

`\paragraph{Saturation and effective-image-collapse cells.}` (tex L2440–2454) is
one paragraph carrying **two** load-bearing enumerative inputs.

> **[saturation, L2440–2452]** "The exact projections are those of
> `\cref{def:explanation-occupancy}`… MCA counts the final slope image, and **the
> occupancy or image–fiber bound must replace an uncorrected support count**. The
> cell is constructible in the projective locator and explanation incidence,
> **but its projection degree remains an enumerative input**." (**L2451–2452**)
>
> **[effective-image collapse, L2453–2454]** "*Effective-image collapse* is the
> related event that **a boundary map reaches exponentially fewer boundary values
> than its ambient codomain contains**."

Both events share the same enumerative status (#539). The image-scale vocabulary
(chart 9.1, `def:explanation-occupancy`, `def:primitive-q`) fixes the two
quantities this packet must bound:

- **collapse** = failure of `(FI): L >= e^{-o(N)} A` (**tex L4844**, `L875`);
  `G_1 = A_eff/L` is the collapse ratio.
- **saturation** = failure of primitive-Q, `max_s f_s <= e^{o(N)} Nbar^img`
  (**`def:primitive-q`, L4918**); `Q_img = L*Mx` is the image-normalized max-fiber
  ratio.

---

## Rung 2 — THE EXACT BUDGET CONSUMER (AUDIT, the deliverable-(C) anchor)

**The consumer is the profile envelope `E_n(a)`** and its sum-equals-max rule.
`def` `eq:profile-envelope` (**tex L857–862**):

```
   E_n(a) = 1 + (n - a + 1)
              + sup_{(r0,r1)}  sum_{lambda in Lambda(r0,r1;a)} ( 1 + Nbar_lambda ),
   Nbar_lambda = |Omega^0_lambda| / L_lambda   (average full-slice fiber, IMAGE scale).
```

The load-bearing sentence (**tex L869–870**):

> "With **subexponentially many profiles**, the sum and maximum have the same
> exponential scale."

and the failure mode it guards against (**tex L889–890**):

> "**The countertheorem is exactly a row for which a quotient profile in `E_n` is
> exponentially larger than the ambient identity term.**"

Condition **(A2)** (**tex L905–907**) is what consumes `E_n`: "A first-match atlas
covers every bad-slope witness and has **`e^{o(n)}` profiles**. The total
**distinct-slope** contribution of its algebraic cells is at most
`e^{o(n)} E_n(a_n)`." The occupancy machinery that would pay a cell is
`lem:exact-occupancy-compiler` (**tex L5673–5698**),

```
   |Z(C)| <= floor(|C| / H)      if every retained occupancy nu_C(rho) >= H,   (RC1)
   |Z(C)| <= #{ S : exists gamma,h, (gamma,S,h) in C },                        (RC2)
```

and `prop:saturation-payment` (**tex L4726–4739**): a saturation cell "is paid if
the projection… has a **proved lower fiber bound**… An **upper bound on the
number of profile lifts goes in the wrong direction**."

**So the C7 budget consumes, per component, a count with a specific scale:**

| component | consumer sentence | quantity the budget needs |
|-----------|-------------------|---------------------------|
| collapse (L2453) | `E_n` sum≈max needs **`e^{o(n)}` profiles** (L869) + `(FI)` before ambient scale (L871–881) | the **number of collapse profiles** must be `e^{o(n)}`, or each must be `(FI)`-routed out |
| saturation (L2452) | `RC1`/`prop:saturation-payment`: a **uniform lower occupancy bound `H`** | the **projection degree** = the fiber size `nu_C(rho)`; needs `H >= ` the cell multiplicity |

This is the "different quantity than a cell count" flag the mission anticipated:
the collapse consumer needs the **profile count** to be `e^{o(n)}` (a count), the
saturation consumer needs a **lower occupancy bound** (a mass/fiber bound). We
follow the tex on both and report each separately below.

The shallow-prefix atlas of **#536** (`Phi_w:binom(D,a)->B^w`, `L<=p^w`) already
pays this **when `(a-k-1)log|B| = o(n)`** (then `L = e^{o(n)}` cells). The product
leaves are **deep**: `w = R_prod = 2k = Theta(N)`, so `p^w = e^{Theta(N)}` cells —
outside #536's shallow regime. That is precisely the gap the C7 input names.
(BLOCK 7 recomputes both regimes: shallow `logL/N -> 0`; deep rate
`2 ln p / p > 0`.)

---

## Rung 3 — THE COUNT THEOREMS (PROVED)

Fix an odd prime `p`, block count `k`, `N = pk`. A **product/profile leaf** is an
assignment of a block type to each of the `k` blocks (T3: these are all the
`(S_E)`-violators, #622). Per-block invariants (verifier BLOCK 0, exact Fraction):

| block | measure | `A_eff,i` | `L_i` | `G_1^{(i)}` | `Q_img^{(i)}` | `E_i+1` |
|-------|---------|-----------|-------|-------------|---------------|---------|
| **T** trivial/full | uniform on `p` | `p` | `p` | `1` | `1` | `1` |
| **C** parabola collapse | uniform on `p` | `p^2` | `p` | `p` | `1` | `p` |
| **S** heavy-atom sat. (`a=2/5`) | `(a,·)` on `p=5` | `5` | `5` | `1` | `2` | `5/4` |

By MASTER-2 + T3 (verifier BLOCK 1, multiplicative through `k=4`, exact):
`G_1 = prod_i G_1^{(i)}`, `Q_img = prod_i Q_img^{(i)}`, `E+1 = prod_i (E_i+1)`.

### T-COLLAPSE (PROVED). The collapse count is a binomial tail.

A leaf with `j` type-C blocks has `G_1 = p^{j}`. Hence
`G_1 >= e^{eps N}  <=>  p^{j} >= e^{eps p k}  <=>  j >= theta k`,
`theta = eps p / ln p` (verifier BLOCK 3(i), `ceil(theta k)` equals the exact
integer threshold on every test). Therefore

```
   #{ collapse profiles } = N_coll(k, theta) = sum_{j >= theta k} C(k, j),
   (1/k) ln N_coll  -->  h(theta)  (theta > 1/2)   or   ln 2  (theta <= 1/2),
```

both **strictly positive** for `theta in (0,1)`; per `N` the rate is `>0/p`
(verifier BLOCK 3(ii)–(iii): rate matched to `h(theta)`/`ln 2` within `0.02` at
`k=2000`, and `rate/N > 0` confirmed). **So there are `e^{Omega(N)}` collapse
profiles.** PROVED.

Exact tail counts (verifier BLOCK 3, `p=3`):

| `k` | `theta` | `N_coll` (exact) | `~ e^{·}` | rate `/k` |
|----|--------|------------------|-----------|-----------|
| 20 | 0.60 | 263950 | `e^{12.48}` | 0.6242 |
| 40 | 0.60 | 147437500478 | `e^{25.72}` | 0.6429 |
| 40 | 0.75 | 1221246132 | `e^{20.92}` | 0.5231 |

### T-SATURATION (PROVED). The saturation count is the same binomial tail.

A leaf with `j` type-S blocks (per-block ratio `q = Q_img^{(i)} > 1`) has
`Q_img = q^{j}`. Hence `Q_img >= e^{eps N}  <=>  j >= (eps p / ln q) k`, the same
binomial-tail structure with `theta_Q = eps p / ln q`. `#{saturation profiles} =
sum_{j >= theta_Q k} C(k,j) = e^{Omega(N)}` (verifier BLOCK 1/2 pin the per-block
`q` exactly; BLOCK 6 enumerates the mixed `{T,C,S}^k` census). PROVED, symmetric
to T-COLLAPSE.

### T-TYPICAL (PROVED). Collapse is typical, not rare.

A random product leaf (each block C-or-not with equal weight) has `E[j] = k/2`, so
`G_1 = p^{k/2} = e^{(ln p)/(2p) N}` (verifier BLOCK 4). The **typical** collapse
rate is `(ln p)/(2p)`:

| `p` | typical rate `(ln p)/(2p)` | max rate `(ln p)/p` (all-C) |
|----|----------------------------|------------------------------|
| 3 | 0.1831 | 0.3662 |
| 5 | 0.1609 | 0.3219 |
| 7 | 0.1390 | 0.2780 |

For any threshold `eps` **below** the typical rate (`theta < 1/2`) a **majority**
of product profiles collapse (verifier BLOCK 4: `frac > 1/2`); above it, collapse
is a rare upper tail of rate `h(theta)` — but still `e^{Omega(N)}` in absolute
count. Either way the collapse cell is **not** measure-zero.

---

## Rung 4 — BUDGET COMPARISON: the verdict (PROVED-negative + PARTIAL)

### Why the printed enumeration budget is NOT paid (PROVED).

1. **Profile count busts L869.** `N_coll = e^{Omega(N)}` is **not** `e^{o(n)}`, so
   the profile envelope's sum-equals-max rule (tex L869) is **unavailable** on the
   product/profile class. PROVED (BLOCK 3, BLOCK 7(d)).

2. **Admitting them makes the countertheorem.** The collapse leaves have
   **singleton fibers**, `Nbar_lambda = |Omega^0|/L = p^k / p^k = 1` (the #609
   escape; verifier BLOCK 5). So the envelope contribution
   `sum_lambda (1 + Nbar_lambda) = 2 N_coll = e^{Omega(N)}` **exceeds the identity
   term** `(n - a + 1) ~ N` — this is **literally "the countertheorem"** of
   tex L889 (verifier BLOCK 5: `env > identity^3`, exponential vs linear). PROVED.

3. **The occupancy payment cannot help.** `RC1` needs a **uniform** lower
   occupancy `H`; the collapse leaf has `H = min occupancy = 1` (no compression,
   `|Z| = |C|` via RC2), and the heavy-atom saturation leaf has a **light tail**
   whose min occupancy is also `1` (verifier BLOCK 5). `prop:saturation-payment`'s
   "lower fiber bound" is therefore `H = 1` on exactly the violators. PROVED.

4. **The entropy-loss lemmas do not apply.** `lem:planted-entropy` (tex L2513) and
   `lem:quotient-entropy` (tex L2526) pay a cell by an **exponential support-count
   reduction** (`binom(n-b,a-b)` for a positive-density planted/quotient block).
   But Gap-1 collapse is a **chart/image** phenomenon with **full support** (all
   `p^k` configurations are realized, singleton fibers), so **no** support-count
   is reduced: the placement multiplicity `C(k, theta k) = e^{h(theta) k/... }`
   is **uncompensated** (verifier BLOCK 7(c): parabola net rate `> 0`). This is
   the precise reason C7 is a **separate** assumed input beyond the entropy
   lemmas. PROVED.

### What IS paid (the routed sub-class, the paper's design).

The paper's escape is **(FI)/first-match routing** (tex L877–881): a leaf that
fails `(FI)` is "**assigned by the first-match rule to an earlier profile so that
its slopes and all witnesses above them are removed from the later residual**."
Every block-parabola / heavy-atom product **does** fail its clause (`(FI)` for
collapse, primitive-Q for saturation), so **if** the routing is enumeratively
exhaustive, the `e^{Omega(N)}` profiles are deleted **before** the envelope sum
and the budget holds. That exhaustiveness is exactly

> **routing = spectrum (#622 Rung 3 / #625).** Every `(S_E)`-violating admissible
> leaf is caught by first-match and routed to a C7 component. **OPEN / WALL.**

### Verdict per component.

| component | verdict | statement |
|-----------|---------|-----------|
| **(A) collapse** | **PARTIAL** | count `N_coll = sum_{j>=theta k} C(k,j) = e^{Omega(N)}` (T-COLLAPSE, **PROVED**) **exceeds** the `e^{o(n)}` profile budget (L869) and realizes the countertheorem (L889) with singleton-fiber `Nbar=1` (**PROVED**); the entropy lemmas do not pay it (full support, **PROVED**). **NOT PAYABLE by direct envelope enumeration.** PAID **only** on the `(FI)`-routed sub-class; residual = routing exhaustiveness (#622/#625, OPEN), now with the exact lower bound `e^{(rate/p)N}` on profiles the routing must remove. |
| **(B) saturation** | **PARTIAL** | count is the **same** binomial tail `sum_{j>=theta_Q k} C(k,j) = e^{Omega(N)}` (T-SATURATION, **PROVED**); the required **uniform lower occupancy** `H` (`RC1`/`prop:saturation-payment`) is defeated by the light tail (`H=1`, **PROVED**). **NOT PAYABLE by the printed occupancy bound.** PAID **only** on the max-fiber-Q-routed sub-class (`def:primitive-q`); residual = the same routing exhaustiveness. |

**Both** budgets reduce to the **single** open statement (routing exhaustiveness),
consistent with #625's "two assumed inputs, inter-reducible modulo max-fiber Q."
Neither is an independent unpaid item; the residual is **one** conjecture.

---

## Rung 5 — CENSUS (MEASURED, verifier BLOCK 6)

Exhaustive enumeration of `{C,T}^k` (collapse) and `{T,C,S}^k` (mixed), exact.

**(a) Collapse fraction** `#{leaves with #C >= theta k} / 2^k`, matched to
`N_coll(k,theta)/2^k` byte-for-byte:

| `k` | `theta=0.5` | `theta=0.75` |
|----|-------------|--------------|
| 4  | 11/16 = 0.688 | 5/16 = 0.312 |
| 6  | 42/64 = 0.656 | 7/64 = 0.109 |
| 8  | 163/256 = 0.637 | 37/256 = 0.145 |
| 10 | 638/1024 = 0.623 | 56/1024 = 0.055 |

At `theta = 1/2` (the typical rate) the fraction sits above `1/2` and drifts down
toward `1/2` — the finite-`k` signature of "collapse is typical." At
`theta = 3/4` it decays like the binomial tail `e^{-(ln2 - h(3/4))k}`.

**(b) Direct-vs-multiplicative agreement.** For every leaf in `{T,C,S}^k`
(`k=3,4,5`; `3^k` leaves) the tensor-measure `(G_1, Q_img, E+1)` computed from the
explicit product measure equals the product of per-block invariants, and MASTER-2
`E+1 <= G_1 Q_img` holds (verifier BLOCK 6, all `3^5 = 243` leaves at `k=5`).

**(c) Single admissible leaves stay safe** (reproduces #622 BLOCK 7 exactly):

| `p` | `N` | `R` | `m` | `L` | `A_eff` | `E` | `log(1+E)/N` |
|----|----|----|----|----|--------|-----|--------------|
| 3 | 2 | 1 | 1 | 2 | 3  | 1/2  | 0.203 |
| 5 | 3 | 2 | 2 | 3 | 25 | 22/3 | 0.707 |
| 7 | 4 | 2 | 2 | 6 | 49 | 43/6 | 0.525 |

`Q_img = 1` (uniform image), `E` polynomial — no single admissible leaf reaches
the divergence. The exponential violation is a `k`-fold product only.

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| C7 = two assumed inputs (saturation L2452 + collapse L2453) | verbatim extraction | **AUDIT** |
| consumer = profile envelope `E_n`, sum≈max needs `e^{o(n)}` profiles (L869) | which quantity | **AUDIT** |
| MASTER-2 `E+1 = A_eff P_2 <= G_1 Q_img`, blockwise & in product | Hölder `P_2<=Mx` | **PROVED** (BLOCK 0/1) |
| `G_1, Q_img, E+1` multiplicative over blocks (T3) | tensor, exact | **PROVED** (BLOCK 1) |
| collapse count `= sum_{j>=theta k} C(k,j)`, rate `h(theta)`/`ln2 > 0` | binomial tail | **PROVED** (BLOCK 3) |
| saturation count = same binomial tail, `theta_Q = eps p/ln q` | binomial tail | **PROVED** (BLOCK 2/6) |
| collapse is TYPICAL (rate `(ln p)/(2p)`), not measure-zero | mode `k/2` | **PROVED** (BLOCK 4) |
| count `e^{Omega(N)}` busts L869; countertheorem via `Nbar=1` (#609) | L889 verbatim | **PROVED** (BLOCK 5) |
| `RC1`/`prop:saturation-payment` defeated (`H=1`, light tail) | no compression | **PROVED** (BLOCK 5) |
| entropy lemmas inapplicable (full support, no support reduction) | net rate `>0` | **PROVED** (BLOCK 7) |
| Gap-2 span-collapse `=>` C5, vacuous on admissible (`w<p`) | not our residue | **AUDIT** (#545) |
| shallow-prefix atlas pays (`L=e^{o(n)}`); product leaves are deep (`w=2k`) | #536 regime split | **PROVED/AUDIT** (BLOCK 7) |
| **budget (A) collapse** | count exceeds; PAID only via `(FI)`-routing | **PARTIAL** |
| **budget (B) saturation** | count exceeds; PAID only via max-fiber-Q routing | **PARTIAL** |
| routing exhaustiveness (the single residual for BOTH) | #622/#625 conjecture | **OPEN / WALL** |

**Proposed ledger entry (for the maintainer).** *The C7 cell (L2440–2454) carries
two assumed enumerative inputs; both are consumed by the profile envelope `E_n`
(L857–862), whose sum-equals-max reduction requires `e^{o(n)}` profiles (L869). On
the product/profile class that carries every `(S_E)`-violator (#622 T3, #625
MASTER-2), the number of profiles reaching collapse `G_1 >= e^{eps N}` (resp.
saturation `Q_img >= e^{eps N}`) is the exact binomial tail
`sum_{j >= (eps p/ln p) k} C(k,j) = e^{Omega(N)}` — exponentially many. Direct
envelope enumeration therefore cannot pay either budget: admitting the profiles
with their singleton-fiber occupancy `Nbar=1` (the #609 escape) makes the envelope
exceed the identity term, which is precisely the countertheorem of L889; and the
tex's entropy-loss lemmas (L2513/L2526) do not apply because Gap-1 collapse has
full support (no support-count reduction). Both budgets are payable only by the
`(FI)`/first-match routing of L877–881, whose exhaustiveness is the routing =
spectrum conjecture (#622/#625). This packet does not discharge that conjecture;
it (i) pins the exact consumer, (ii) proves the count is a positive-rate binomial
tail (so the routing must remove `e^{Omega(N)}` profiles — an exact lower bound on
the obligation), (iii) proves collapse is typical, not rare, and (iv) proves the
entropy lemmas cannot substitute. Print the C7 projection-degree budget as: the
`(FI)`/max-fiber-Q routing removes the binomial-tail profile family before the
`E_n` sum — equivalently, prove routing = spectrum. This is an OPEN input.*

### The 2–3 steps the PI should re-derive

1. **The count (T-COLLAPSE).** `G_1 = prod_i G_1^{(i)}` is multiplicative (T3), so
   `G_1 = p^{#C}` and `G_1 >= e^{eps N} <=> #C >= theta k`, `theta = eps p/ln p`.
   The number of block-type profiles at that threshold is `sum_{j>=theta k}C(k,j)`,
   a binomial tail of positive rate `h(theta)` (or `ln 2`). Same for `Q_img` with
   `theta_Q = eps p/ln q`. One line each.
2. **The consumer + the bust (Rung 2/4).** `E_n`'s sum equals its max **only**
   with subexponentially many profiles (L869). The tail is `e^{Omega(N)}` profiles;
   with singleton-fiber `Nbar=1` (#609) they contribute `2 e^{Omega(N)} >` identity
   term = the countertheorem (L889). The entropy lemmas (L2513/L2526) need a
   support reduction; the parabola has full support, so they don't apply.
3. **The residual.** The only payment is `(FI)`/first-match routing (L877); its
   exhaustiveness is routing = spectrum (#622/#625). This packet gives the exact
   lower bound `e^{(rate/p)N}` on the number of profiles that routing must catch.

---

## What closes if both budgets are paid

If routing = spectrum is proved (both budgets paid), the span face closes
**unconditionally** on the product/profile class: every `(S_E)`-violator is routed
out before the primitive step, so every primitive first-match residual satisfies
`(S_E)` (#625 T-A), hence `(FI)` (`(S_E) => (FI)`, #614), hence the span face
`L >= e^{-o(N)} A_eff`. Combined with #622 T1 (branch-1 leaves have the span face
free) and #545 (Gap-2 span-collapse is C5, vacuous on admissible `w<p`), this is
the **full unconditional closure chain** for input 2's span face:

```
   single admissible leaf  --T1-->  (S_E) free, span face free (branch-1)
   Gap-2 span-collapse     --#545-> C5 field-descent, vacuous on admissible
   Gap-1 collapse products --THIS--> binomial-tail family, routed by (FI) [needs routing=spectrum]
   heavy-atom sat. products --THIS--> same family, routed by max-fiber Q  [needs routing=spectrum]
```

with the single open link the routing-exhaustiveness conjecture, whose obligation
this packet has now quantified (`e^{Omega(N)}` profiles, positive rate).

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_c7_degree_enumeration.py   # RESULT: PASS (233/233)
```
