# CAP25 v13: the finite-field lift-class cost model is unpayable — the ledger's decline is necessity, not caution (KB-MCA a=1116048)

Status: `REFERENCE` (§0 — the ledger's own named open statement + its `F_17`
replay `757/193/20/737` vs `w*p=17`, reproduced by an independent `Q(zeta_n)`
engine) / `PROVED` (§1 the `w=1` exact structure theorem `exact-class <->
c in {-1,0,1}^{n/2}`, class size `C(z,(j-h+z)/2)`, byte-exact on 6 toys; §2 the
deployment big-int chain from the ledger's **own** terminal-16 lemma) /
`REFUTATION` (§3 — the headline: keep-one-per-target is **not** a row-indexed
deduction, two independent arguments, exact margins `2^2090812.77` /
`2^2090815.35`) / `MEASURED` (§4 twist-primitivity of the removed mass, exact toy
enumeration) / `REDUCED` (§5 — the cost model **is** an exact cyclotomic
subset-sum count; the computation is what refutes payability) / `SCALING` (§6 the
`tau` vs `avg_fiber` grid, anchored at `(17,16,8,3) tau=0.4107` = PR #416's
`M_gen` exactly).

**Verifier:** `experimental/scripts/verify_liftclass_cost_model_refuted.py`
(zero-arg, stdlib-only, ~37 s, `RESULT: PASS (81/81 checks)`, exit 0): merges the
four finished `lane_liftclass` research scripts and gates **every** shipped
number — the exact deployed-row integer chain (`t*p`, `w*p`, `B*`, `B_rem`,
`K_raw=4807520`, `K_rem=4805007`, `(n/2)*w`, `binom(16,7)=11440`,
`binom(32,14)`), the `F_17` replay `757/193/20/737` via **two** prefix
conventions (locator low-coeff and power-sum, byte-identical), the `w=1`
size-histogram identity on six toys, the big-int deployment log-scale ledger
(`tau_bound=2^-22.2534`, `avg=2^35.7352`, removed classes/supports), both
refutation margins, the five-row twist-primitivity table, the `tau`-vs-`avg`
grid with the `(17,16,8,3)=5286/12870` anchor, and **seven** tamper self-tests
(including one that fakes a payable bound). Cross-validated against the
integrated `kb_mca_1116048_first_match_ledger_v1.md`.

**What this is / is not.** This does **not** prove `U(1116048) <= B*`, the KB-MCA
first-safe agreement, the row-sharp Q atom (`def:q-row-atom`), or any adjacent
safe row. It closes **one named open model** — the ledger's "finite-field
lift-class cost model" — **negatively**: it proves that the ledger's declined
"tempting stronger route" (keep one exact lift class per finite target, charge
the rest to generated-field at cost `w*p`) can **never** be a row-indexed
payment, at the deployed row and structurally. The ledger's own decline of that
route was therefore **necessity**, not conservatism. Every claim carries a label.

---

## 0. The named open statement and its own replay `REFERENCE`

The integrated first-match ledger (`kb_mca_1116048_first_match_ledger_v1.md`)
records, verbatim, its declined route and names the missing model. At the
exact-lift fiber bound (L409–414):

> This is deliberately **not** deducted as a finite-field first-match payment in
> this packet. The tempting argument "remove all but one honest lift class per
> finite prefix value at cost `w*p`" does not match the current image-cell
> semantics: row-coordinate cells do not bound the number of finite prefix values
> or raw supports. **A valid finite-field lift-class cost model remains a separate
> target.**

The Q2 "tempting stronger route" is stated again at L806–820, with the crux at
L818–820 (verbatim):

> This packet does not mark that route as proved: the assignment depends on the
> finite target and its retained exact lift class, while **a row-indexed `w*p`
> image-cell count does not by itself bound the number of removed exact lift
> classes or raw supports.**

The ledger backs the crux with a direct `F_17` replay (L823–832), taking the
primitive finite target `z=1` in `F_17`, `D=<3>` (so `n=16`), `j=8`, `w=1`:

```text
finite fiber size over z=1:                757
number of exact Q(zeta_16) lift classes:   193
largest exact lift class:                   20
non-retained supports after keeping largest exact class: 737
w*p:                                        17
```

An **independent** `Q(zeta_16)` engine (`liftclass_engine.py`, exact
`Z[zeta_16]` arithmetic with `zeta^8=-1`, no shared code with the ledger
verifier) reproduces the whole quadruple, `C(16,8)=12870`, and `w*p=17` — under
**both** the ledger's locator low-coefficient convention **and** the
power-sum convention (byte-identical fibers; `verify` §REFERENCE). The single
removed target already shows the obstruction in miniature: `737` removed
supports (over `192` non-retained classes) versus `w*p=17` image cells.

The ledger repeats the non-payability as four Nonclaims (L964–971): it does not
prove finite-field lift-class removal at cost `w*p` for prefix-vector fibers,
does not prove support-multiplicity bounds for non-retained generated-prefix
exact lift classes, does not prove primitive-heavy-orbit exclusion, and does not
bound raw support multiplicity inside a generated-field image cell. L517 lists
the same "finite-field lift-class cost model" among the inputs the row still
needs. This packet resolves that named model.

---

## 1. The `w=1` cost model is exactly the `{-1,0,1}^{n/2}` lattice `PROVED`

The cost model has a closed structure at depth `w=1`. Take the sum-of-roots
coefficient `P_1(S) = sum_{a in S} zeta_n^a` as the exact prefix (Newton-
equivalent to the leading locator coefficient). Since `zeta_n^{b+n/2} = -zeta_n^b`
with `h := n/2`, the exact class of `S` is the vector `c in {-1,0,1}^h`,

```text
c_b = [b in S] - [b + h in S],   0 <= b < h.
```

The number of `j`-subsets realizing a given `c` (its class size) is

```text
size(c) = C(z, (j - h + z)/2),    z = #{b : c_b = 0},
```

proved by counting: the `h - z` nonzero coordinates each force one element of
a `+-1` pair, and the remaining `(j-h+z)/2` fully-included pairs are chosen
among the `z` free pairs. It is valid when `j - h + z` is even and
`0 <= (j-h+z)/2 <= z`, and the largest class
over all `c` is

```text
max class = C(h, j/2) = C(n/2, j/2).
```

`verify` §PROVED-structure confirms this by the **full size-histogram identity**
(the multiset of measured class sizes equals the multiset predicted by the
`c`-parametrization) on six toys — byte-exact, `measured == predicted`:

| `(p,n,j)` | # classes | max class `= C(n/2,j/2)` |
|---|---:|---:|
| `(17,16,8)` | 3281 | 70 `= C(8,4)` |
| `(97,16,8)` | 3281 | 70 |
| `(17,16,6)` | 3025 | 56 `= C(8,3)` |
| `(41,8,4)` | 41 | 6 `= C(4,2)` |
| `(17,8,4)` | 41 | 6 |
| `(97,16,4)` | 1233 | 28 `= C(8,2)` |

The count is independent of `p` (the two `n=16,j=8` rows agree exactly): the
`w=1` model is a purely cyclotomic subset-sum census, not a finite-field one.
This is the exact object the ledger's cost model asks to price.

---

## 2. The deployment bound from the ledger's own terminal-16 lemma `PROVED`

The ledger proves (its "Exact-lift fiber bound", L372–406, restated L859–888)
that since `w = 67471 >= 2^16`, prefix agreement forces the mask difference to be
divisible by `(X^n-1)/(X^16-1)`, so each **exact** honest prefix fiber varies only
by whole terminal cosets of size `n/16`, and with `floor(j/131072)=7`,

```text
largest exact lift class <= max_{0<=q<=7} C(16,q) = C(16,7) = 11440.
```

Feed **only** this single proved input into the deployed-row constants
`p=2130706433`, `N=2^21`, `J=981104`, `w=67471`, `B*=274980728111395087` (all
gated exact in `verify` §CONSTANTS, matching the ledger integer-for-integer,
including `K_raw=4807520` and `K_rem=4805007`). Then (`verify` §PROVED-deployment,
big-int, log-scale):

```text
avg finite prefix fiber  = C(N,J) / p^w = 2^35.7352   (~ B_rem/K_rem; see note)
tau_bound = 11440 * p^w / C(N,J)        = 2^-22.2534 ~ 2.0e-7          [o(1)]
```

So keep-largest retains at most `tau <= 2.0 x 10^-7` of each fiber, and every
finite fiber splits into at least `avg/11440 = 2^22.2534 ~ 5.0 x 10^6` exact lift
classes. The removed part is therefore essentially the entire mass:

```text
total exact lift classes  >= C(N,J)/11440           = 2^2090859.7980
removed classes (keep one) >= C(N,J)/11440 - p^w     = 2^2090859.7980
removed raw supports       >= C(N,J)*(1 - tau_bound) = 2^2090873.2798  (~ full)
```

Note on `avg`: `avg = C/p^w` is exact (a rational, `log2 = 35.7352`). The
ledger's headline `avg ~ B*/K_rem` is an **approximation**, not an identity; the
exact relation is `K_rem = floor(B_rem * p^w / C)` with `B_rem = B* - t*p`, i.e.
`avg ~ B_rem/K_rem` (`verify` gates the exact floor and the `~1.0` ratio).

---

## 3. REFUTATION: keep-one-per-target is not a row-indexed payment `REFUTATION`

The route the ledger declined would price the removal by a **row-indexed** count
`poly(w,p,n,m)` — the branch-7 image-cell semantics, where a payment is a number
of `(row, slope)` or `(z,d)` cells, all bounded by the per-fiber budget `B*`.
Two independent arguments show no such payment exists.

**(i) Structural — the normalization is indexed by the finite target group, not
by rows.** "Keep one exact class per finite target" makes an **independent
keep-one decision at every nonempty finite target** `z`. The number of such
targets is the image of `Phi_w` in `F_p^w`, at most `p^w = 2^2090837.5`, and at
deployment essentially all of them carry `>= 2` exact lift classes (`avg/11440 =
2^22.25` classes per fiber). A per-target normalization is therefore a function
on a set of size `~p^w`; a row-indexed deduction is a function on `<= t` rows and
`<= p` slopes, bounded by `B* = 2^57.9`. The indexing sets differ by

```text
STRUCTURAL margin = p^w / B* = 2^2090779.6.
```

No amount of row-coordinate bookkeeping can encode a choice at `2^2090837.5`
independent targets. This is exactly the ledger's own "row-coordinate cells do
not bound the number of finite prefix values" (§0), made quantitative.

**(ii) Quantitative — the removed count exceeds every available payment.** The
keep-largest rule removes, at the deployed row,

```text
removed exact lift classes >= C/11440 - p^w = 2^2090859.80
removed raw supports        >= C*(1 - tau)   = 2^2090873.28
```

Every row-indexed budget the ledger can offer is tiny by comparison — the
branch-7 image cells `t*p = 2^47.03`, the Q2 heavy-prefix cover `w*p = 2^47.03`,
the `(n/2)*w = 2^36.04` heavy-prefix cells, and even the **entire** per-fiber
budget `B* = 2^57.93`. The refutation margins are

```text
removed classes / t*p = 2^2090812.77      (classes vs the largest image budget)
removed supports / B*  = 2^2090815.35      (supports vs the whole per-fiber budget)
```

Both are astronomically positive. The removal is unpayable by `~2^2,090,813`,
whether measured in exact lift classes against `t*p` or in raw supports against
`B*`. (`verify` §REFUTATION gates both margins and the strict inequalities
`removed > t*p`, `removed > B*`.)

---

## 4. The removed mass is twist-primitive: Q2 folding cannot reach it `MEASURED`

One might hope the ledger's **paid** Q2 machinery already removes this mass for
free. Q2 folding (the ledger's twist-stabilizer descent, L641–735) descends only
classes with a **nontrivial** twist-stabilizer. A removed class with trivial
stabilizer is twist-**primitive** and is provably unreachable by any paid Q2
branch. Direct stabilizer census of the removed (non-largest) classes
(`verify` §MEASURED):

| `(p,n,j,w)` | # removed classes | primitive-class frac | primitive-support frac |
|---|---:|---:|---:|
| `(17,16,8,1)` | 3264 | 1.0000 | 1.0000 |
| `(17,16,8,2)` | 12168 | 0.9980 | 0.9974 |
| `(17,16,8,3)` | 7576 | 0.9968 | 0.9958 |
| `(97,16,8,1)` | 12433 | 0.9967 | 0.9959 |
| `(97,16,8,2)` | 5890 | 0.9954 | 0.9954 |

`99.54%–100%` of the removed classes (and of the removed support mass) are
twist-primitive across the toy table. There is no payable fraction hiding beyond
what branch-7 / Q2 already grant: the keep-largest removal is essentially
disjoint from the stabilized mass that Q2 folding can pay.

---

## 5. The cost model reduces to an exact cyclotomic subset-sum count `REDUCED`

The "cost model" is not an unknown analytic quantity: it **is** an exact
cyclotomic subset-sum count, fully computable.

- At `w=1` it is the `{-1,0,1}^{n/2}` lattice census of §1, with class sizes
  `C(z,(j-h+z)/2)` in closed form.
- At deployment it is the `2`-adic terminal-coset count: the ledger's
  terminal-16 lemma (§2) is precisely the instance
  `largest class = max_{q<=7} C(16,q)`.

Because the count is computable, the refutation is not a gap: the computation
**is** the obstruction. Evaluating the model returns `tau <= 2e-7` and
`removed >= 2^2090859.80`, and those exact values are what make the row-indexed
payment impossible (§3). A cost model that could be paid would have to return a
poly-sized removed count; the true count is super-polynomial by construction.

---

## 6. Scaling: the toy win is a small-`w` artifact `SCALING`

The `tau` vs `avg_fiber` grid (`verify` §SCALING, power-sum prefix) shows the
retained fraction collapsing as fibers coarsen:

```text
(p17,n16,j8): w1: avg=757.06, tau=0.030   w2: avg=44.53, tau=0.043   w3: avg=2.64, tau=0.411
(p97,n16,j8): w1: avg=132.68, tau=0.017   w2: avg=1.84,  tau=0.542   w3: avg=1.02, tau=0.983
(p17,n8,j4):  w1: avg=4.12,   tau=0.543   w2: avg=1.01,  tau=1.000
(p41,n8,j4):  w1: avg=1.71,   tau=0.586   w2: avg=1.00,  tau=1.000
(p97,n8,j4):  w1: avg=1.52,   tau=0.657   w2: avg=1.00,  tau=1.000
```

At **fixed** `(n,j)`, `tau` rises monotonically with `w` (coarser prefix, smaller
fibers, near-injective at large `w`); equivalently `tau` **falls** as `avg_fiber`
rises. The anchor `(17,16,8,3)` gives `tau = 5286/12870 = 0.4107` — **exactly**
PR #416's `M_gen` retained mass (the branch-7 generated-field keep-largest mask;
`verify` gates the exact fraction). A big `tau` is a coarse-fiber, small-`w`
regime. Deployment sits at the opposite extreme: `avg_fiber = 2^35.7`,
`tau = 2e-7`. PR #416's viable `tau=0.4107` is a **small-`w` toy artifact** that
does not survive to the deployed depth `w=67471`.

---

## 7. Consequences `ANALYSIS`

State carefully.

**(i) The ledger's decline is necessity.** The ledger declined the keep-one route
as "not matched to the image-cell semantics" (§0). §3 upgrades that from a
scoping caution to a theorem: no row-indexed payment can exist, structurally
(margin `2^2090779.6`) and quantitatively (margin `2^2090812.77`). The ledger's
named open "finite-field lift-class cost model" is closed **negatively**. The
four Nonclaims at L964–971 are now consequences, not open items.

**(ii) PR #416's conditional headline resolves negatively at deployment.** PR
#416 (`cap25_v13_q_eq_masked_participation_ratio`, OPEN) proves that its `M_gen`
support mask brings the masked triangle **below** budget where the raw route is
overstrong — **explicitly conditional** (§8, `CONDITIONAL`) on the ledger's
still-open lift-class support-removal cost model ever being paid. This packet
resolves that condition: the cost model is **unpayable**, so `M_gen`'s `tau<1`
win does **not** transfer to the deployed row. At deployment `tau -> o(1)`, and
the keep-largest residual is exactly the sparse-heavy regime that #416's **own
§7 falsifier** rules out ("a mask that isolates a sparse-heavy primitive fiber
falsifies the route"). **PR #416 remains correct as stated** — it claimed only
the conditional and even named the falsifier that fires here; this packet
resolves the condition against the route. Relationship: resolves-condition-of,
**non-correcting**.

**(iii) The support-masking shortcut to row-sharp Q is dead.** The masked crux
`PR(E_Q) <= nu*_masked` (PR #414 / #416) stays meaningful **only for masks the
ledger actually pays** — image-cell-level masks (branch-7 `t*p`, Q2 quotient
descent), **not** support-level keep-largest. The open target therefore remains
the **direct** primitive-orbit flatness certificate (`def:q-row-atom`,
`prob:row-sharp-q` in `grande_finale.tex`), unshortcut by support masking. This
packet removes one tempting bypass; it does not touch the direct target.

---

## 8. Weave — relation to the lineage and current v13 PRs `AUDIT`

- **Ledger `kb_mca_1116048_first_match_ledger_v1.md` (integrated).** Source of
  the named open statement (L409–414, L517), the crux (L818–820), the `F_17`
  replay (L826–832), the terminal-16 lemma (L406, L888), the `(z,d)`
  heavy-prefix indexing and `(n/2)*w=70748471296` (L776–785), and the Q2 folding
  theorem (L641–735). Every quote and constant here is verbatim/line-provenanced
  and gated exact by the verifier. This packet closes the ledger's named model
  negatively; it corrects nothing in the ledger (the ledger was already careful
  to decline the route).
- **PR #416 `cap25_v13_q_eq_masked_participation_ratio` (OPEN, branch
  `thresholds-eq-masked-participation-ratio`).** Resolves-condition-of,
  non-correcting: this packet answers #416's §8 `CONDITIONAL` — the `M_gen`
  support-removal payment the ledger does not grant — in the **negative**, and
  lands the deployed residual in #416's §7 sparse-heavy falsifier. The
  `(17,16,8,3) tau=0.4107` anchor is #416's `M_gen` value, gated exact.
- **PR #414 `cap25_v13_q_em_inverse_participation_ratio` (OPEN, grandparent).**
  The `(STAR) <=> PR <= nu*` equivalence PR that #416 follows; this packet is a
  cousin closure in the same lineage, cutting the support-masking bypass to the
  same masked-PR target.
- **PR #413 `cap25_v13_signed_em_masked_residual_audit` (integrated
  `e83962ae`).** Masked-object source (`E_Q` on `P_Q`). What survives its route
  is `E_Q` for **paid** masks — image-cell-level, per §7(iii); this packet marks
  the support-level mask as the part that does not survive.
- **PR #412 `cap25_v13_q_pw2_concentration_floor` (integrated).** Margins-style
  route-cut sibling: #412 kills every second-moment (`r=2`) route per-stratum
  with exact margins and leaves the crux at the signed-`e_m` inverse; this packet
  kills the support-masking route to the same crux with exact margins. Same
  register, complementary obstruction.
- **`rem:mass-aware-logmoment` (`grande_finale.tex` L966).** The deployment
  keep-largest residual (`tau <= 2e-7`) is exactly this remark's sparse-heavy
  regime: after first-match deletion the primitive residual has mass `tau < 1`,
  so a full-mass moment lower bound may not be imported unless `tau=1` is proved
  separately. Here `tau -> o(1)`, so the remark's caveat is not just possible but
  forced — matching #416's §7 falsifier precondition. In the current-tex
  framing this deployed residual is exactly the sparse-heavy primitive fiber
  that a proof of the primitive entropic inverse theorem
  (`prob:entropy-inverse-q`, skeleton `rem:entropy-inverse-skeleton`) must
  name as an explicit residual cell; this packet exhibits its deployed
  instance at `tau -> o(1)`.
- **`def:q-row-atom` (L2043), `prob:row-sharp-q` (L2177).** The direct target
  that stays open after this bypass is removed (§7(iii)).
- Current v13 threshold PRs (`#372/#374`, `#366/#384`, `#380`, `#369/#378/#383`,
  `#376/#375`): unchanged; this packet consumes no upper cell and instantiates no
  `U(1116048)` certificate.

---

## 9. Nonclaims

- This note does **not** prove `U(1116048) <= B*`, the KB-MCA first-safe
  agreement, or any adjacent safe row.
- This note does **not** prove the row-sharp Q atom (`def:q-row-atom`), the
  masked PR bound `PR(E_Q) <= nu*_masked`, or primitive-orbit flatness.
- This note does **not** correct PR #416, #414, #413, #412, or the ledger; it
  resolves #416's stated condition negatively and closes the ledger's named open
  model.
- The refutation is of a **payment route** (row-indexed keep-one-per-target lift-
  class removal), not of the exact-lift terminal-16 bound itself, which remains
  a valid `Q(zeta_n)` fiber bound and is used here as the input to §2.
- The toy grid (§1, §4, §6) is exact enumeration at `n <= 16`; the deployment
  numbers (§2, §3) are exact big-integer arithmetic at the deployed row. No claim
  interpolates between them beyond the stated monotone `tau`-vs-`w` trend.
