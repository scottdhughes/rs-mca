# CAP25 v13 masked: the residual `E_Q` participation ratio — support masking passes the M31-list budget at the #413 row where raw is overstrong (KB-MCA a=1116048)

Status: `REDUCED` (§2 — the PR #414 equivalence `(STAR) <=> PR <= nu*` transfers
**verbatim** to the masked residual `E_Q`, exact algebra, for `K_Q >= 1`) /
`MEASURED`+`CONDITIONAL` (§1 headline `#413` row — the masked triangle fits the
budget where raw fails **iff** the ledger's still-open lift-class support-removal
cost model is ever paid: the `tau<1` win is exactly the payment the ledger does
NOT grant, §8) / `MEASURED` (§3 the survives-vs-breaks dichotomy incl. the
not-a-projection witness, §5 the four-mask / five-toy grid, §6 the floor factors,
§7 the falsifier — all exact toy enumeration) / `PROVED` (§3 what survives: Fourier
inversion, Parseval, the Cauchy–Schwarz flip, the trivial-support floor, Hermitian
symmetry) / `CAVEAT` (§4 — the entire toy win is the `tau<1` mass factor in raw-avg
units; the instance of `rem:mass-aware-logmoment`) / `OPEN≡crux` (§6 — the masked
PR bound `PR(E_Q) <= nu*_masked` itself, the tighter variant PR #414 names open) /
`REFERENCE` (§0/§6 the integrated ledger + parent-floor constants).

**Verifier:** `experimental/scripts/verify_q_eq_masked_participation_ratio.py`
(zero-arg, stdlib-only, ~17 s, `RESULT: PASS (61/61 checks)`, exit 0): merges the
three finished `lane_eq_masked` research scripts and gates **every** shipped number —
the exact big-int deployment ledger + `M31`-list budget `16777215/1993678`, the four
support masks at the decisive `#413` row `(17,16,8,3)`, the `#413` printed constant
`10.472846` (witness-vs-lemma), the `(STAR)_masked <=> PR <= nu*` algebraic
equivalence per mask, the equivalence-flip scan, the not-a-character-projection
witness (`4880/4912` frequency-mixed), Parseval on every mask (relerr `<= 3.8e-15`),
the five-toy PR grid, the masked `p^{w/2}` floor factors, the over-pruning falsifier,
and seven tamper self-tests. Cross-validated against the integrated
`kb_mca_1116048_first_match_ledger_v1.md`, `cap25_v13_signed_em_masked_residual_audit.md`
(was #413), and `cap25_v13_q_pw2_concentration_floor.md` (was #412).

This is the **masked-residual follow-on** to the OPEN PR #414
(`cap25_v13_q_em_inverse_participation_ratio`, branch
`thresholds-em-inverse-participation-ratio`): it answers the **tighter masked variant
that #414 explicitly leaves open** ("the masked-residual PR analog — the participation
ratio of `E_Q` on `P_Q` against the same `nu*` ledger — is the tighter open variant
that the audit's repaired target names"). It does **not** prove `U(1116048) <= B*`,
the row-sharp Q atom, or the masked PR bound; it transfers the equivalence to `E_Q`,
measures the dichotomy, and reports — as a **first-class caveat, not a footnote** —
that the toy "win" is a `tau<1` raw-avg-units artifact. **And the headline is
CONDITIONAL (§8):** `M_gen`'s `tau<1` is produced by exactly the support-removal
payment the ledger does **not** grant — branch 7's proved deduction is the
image-cell count (`cost <= t*p`), while keep-largest-lift-class support removal is
the ledger's separate, still-open finite lift-class cost model — so the masked
triangle route fits the budget where raw fails **iff** that cost model is ever
paid; this packet pins that precise dependency of the masked route. Every claim
carries a label.

---

## 0. Setup and the masked object  `REFERENCE` (imported-proved) + `REDUCED`

Over `F_p`, `D = mu_n subset F_p^*`, prefix map `Phi_w(S) = (p_1,...,p_w) mod p`
(power sums; Newton-equivalent since `char = p > w`). Raw family = all `C(n,m)`
`m`-subsets, `N(z) = |Phi_w^{-1}(z)|`, and by `prop:fourier-audit` (grande_finale.tex,
Hughes's identity) `E(t) = sum_{|M|=m} psi(t.Phi_w(M)) = e_m(v_t)`.

The masked-residual audit (`cap25_v13_signed_em_masked_residual_audit.md`, integrated
e83962ae, was PR #413; §3) names the theorem-facing object **after first-match
deletion**: the pruned primitive Q residual family `P_Q` and its masked coefficient

```
E_Q(t) = sum_{M in P_Q} psi(t . Phi_w(M)),   N_Q(z) = |{M in P_Q : Phi_w(M) = z}|,   T_Q = |P_Q|.
```

Fourier inversion (audit §3, verbatim) — the reduction's engine, which holds for the
masked family exactly as for the raw one because `N_Q >= 0` is just another
fiber-count function:

```
p^w N_Q(z) = T_Q + sum_{t != 0} psi(-t . z) E_Q(t).        (masked inversion)
Gamma2^Q := p^w sum_z N_Q(z)^2 / T_Q^2  (>= 1),
||E_Q||_2^2 = sum_{t!=0}|E_Q(t)|^2 = T_Q^2 (Gamma2^Q - 1).  (masked Parseval, exact)
```

**Toy masks** (§8 — faithful reconstructions of the ledger first-match branches, not
the deployed ledger). `M_quot` = branch-4 quotient-periodic cell (remove `S = -S`);
`M_gen` = branch-7 generated-field collision removal (per finite fiber keep only the
**largest exact `Z[zeta_n]` lift class**, charge the rest to generated-field);
`M_both` = both. `tau := T_Q/C` is the retained mass. All Parseval identities hold to
relerr `<= 3.8e-15` on every mask (`verify` §5).

---

## 1. HEADLINE: support masking passes the budget at the #413 row  `MEASURED`+`CONDITIONAL` (exact enumeration, `verify` §3; condition = §8)

The audit's own toy counterexample is `p=17, D=F_17^* (n=16), m=8, w=3`
(`C(16,8)=12870`, `p^w=4913`). The raw route is **overstrong** there, reproducing
`#413`'s three printed numbers to the digit (`verify` §3):

```
R_true = p^w max_z N(z) / C = 4913*7/12870 = 34391/12870 = 2.672183   (< 8.4152 budget)
raw primitive L1 triangle  = 1 + L1_prim/C = 10.472846                (> 8.4152 budget)
```

so `2.672 < 8.4152 < 10.473`: the true max-fiber ratio fits the `M31`-list budget
`16777215/1993678 = 8.4152079724` (`prop:q-exact-target`) while the raw signed-L1
triangle certificate exceeds it — the raw `(STAR)` is a **sufficient, not equivalent**
route (audit §4).

**Support-side generated-field masking repairs exactly this gap.** Measured triangle
constants in **raw-avg units** `(T_Q + ||E_Q||_1)/C`, all four masks (`verify` §2/§3):

| mask | first-match branch | `T_Q` | `tau` | `R_rawavg` | triangle (total) | triangle (primitive) | vs `8.4152` |
|---|---|---:|---:|---:|---:|---:|:--|
| RAW    | —                     | 12870 | 1.0000 | 2.672183 | 10.5798 | 10.4728 | **> budget** (overstrong) |
| `M_quot` | 4 quotient-periodic | 12800 | 0.9946 | 1.908702 | 11.8916 | 11.7871 | **> budget (WORSE)** |
| `M_gen`  | 7 generated-field   |  5286 | 0.4107 | 2.290443 |  6.0713 |  5.9668 | **< budget (VIABLE)** |
| `M_both` | 4 then 7            |  5256 | 0.4084 | 0.763481 |  6.1624 |  6.0635 | **< budget** |

Reading: `M_gen` pulls the primitive triangle from `10.4728` (raw, over budget) to
`5.967` (`6.071` total) — **below** `8.4152`, viable **exactly where the raw route is
overstrong**. The **frequency-quotient mask alone WORSENS it** to `11.89`: removing
the 2-periodic cell (only `1 - tau = 70/12870 ~ 0.5%` of supports) strips low-frequency
mass and raises the residual average. The mask that helps is the **support-side
generated-field** one, not the frequency-quotient one — the audit's repaired target
(§8) is support-side, and this is why.

Two scope lines on this headline. (i) **CONDITIONAL** (§8): the `M_gen` removal is
exactly the support-removal payment the integrated ledger does **not** grant —
branch 7's proved deduction is the image-cell count, not support removal — so the
fit holds **iff** the ledger's still-open lift-class support-removal cost model is
ever paid. (ii) **Cross-row calibration:** the toy separation is scored against the
**M31-list** multiplier `8.4152` (the `p = 2^31-1` row of `prop:q-exact-target`),
while §4's deployment `nu*_ref,masked` uses the **KB a=1116048** constants
(`K_rem = 4805007`) — a cross-row usage inherited from #413's own F_17 framing,
which likewise scores its F_17 toy against the M31-list budget.

---

## 2. REDUCED: the PR #414 equivalence transfers verbatim to `E_Q`  `REDUCED` (exact algebra, `verify` §2)

PR #414 proved, for the raw spectrum `Rhat(t) = e_m(v_t)`, the exact algebraic
equivalence `(STAR) <=> PR(Rhat) <= nu* = (Krem-1)^2/(Gamma2-1)`. Its only inputs are
**Parseval** and the **Cauchy–Schwarz division** — both basis identities that hold for
`E_Q` verbatim (§0). So the reduction transfers with the substitutions

```
C(n,m) -> T_Q = tau*C,     K_rem -> K_Q = K_rem/tau,     Gamma2 -> Gamma2^Q,
||E_Q||_2^2 = T_Q^2(Gamma2^Q - 1)  (exact),
```

giving, on the masked spectrum,

```
(STAR)_masked   sum_{t!=0}|E_Q(t)| <= (K_Q - 1) T_Q
        <==>    PR(E_Q) := ||E_Q||_1^2 / ||E_Q||_2^2  <=  nu*_masked := (K_Q - 1)^2 / (Gamma2^Q - 1).
```

The biconditional is valid **for `K_Q >= 1`** (both sides of the L¹ inequality must
be nonnegative before squaring; for `K_Q < 1` the left side is unconditionally false
while the right can still hold — a vacuity edge only). Always true in scope:
`K_Q = K_rem/tau >= K_rem` at deployment (`tau <= 1`) and `K_Q in [8.4152, 20.6057]`
across the §2 masks (`verify` §2 gates it).

`K_Q = K_rem/tau` because the masked family carries mass `tau*C` at budget `K_rem*avg`,
so the per-fiber budget multiplier relative to the **masked** average is `K_rem/tau`.
The equivalence is exact for any `Gamma2^Q`; verified per mask at the decisive row and
across a `K`-scan (`verify` §2/§4 — `(STAR)_masked` and `PR<=nu*` agree at every
scanned `K`, flip together between `K=13.78` and `K=15` for `M_gen`). This is the
`REDUCED` headline: **the #414 reformulation is stable under first-match masking** —
the theorem-facing masked object is a Fourier participation-ratio / effective-support
bound on `E_Q`, exactly as for the raw coefficient.

---

## 3. Survives-vs-breaks dichotomy: `E_Q` is NOT a character projection  `PROVED` + `MEASURED` (`verify` §5)

**What survives (`PROVED`, structural).** Every ingredient of the §2 reduction is a
statement about the nonnegative count function `N_Q` and its DFT, so it holds for the
masked family verbatim: (i) **Fourier inversion** (§0 masked inversion); (ii)
**Parseval** `||E_Q||_2^2 = T_Q^2(Gamma2^Q-1)` (gated on every mask, relerr `<=
3.8e-15`, `verify` §5); (iii) the **Cauchy–Schwarz flip** (the `||.||_1^2/||.||_2^2`
division of §2); (iv) the **trivial-support floor** (`|supp| = p^w-1` recovers the
`p^{w/2}` floor, §6); (v) **Hermitian symmetry** `E_Q(-t) = conj(E_Q(t))` (`N_Q`
real). The **reduction is basis-level and mask-agnostic.**

**What breaks (`MEASURED`).** The *per-direction identity* `E(t) = e_m(v_t)` does
**not** survive: `E_Q` is `e_m` minus the DFT of the removed mass, spread over **all**
frequencies. If the mask were a character (frequency) projection, `E_Q(t)` would be
`e_m(v_t)` on surviving directions and `0` elsewhere, i.e. `|E_Q(t)| in {0, |e_m(v_t)|}`
for every `t`. Measured at `(17,16,8,3)`, `M_gen` vs RAW over the `4912` nonzero
directions (`verify` §5):

```
projection-consistent (|E_Q| in {0,|E|}):        32
frequency-MIXED (0 < |E_Q| != |E|):            4880   <-- impossible for a character projection
mass BORN (|E|=0 but |E_Q|>0):                    0   <-- a projection can only kill, never create
```

So `E_Q` is **genuinely support-side**: `4880` of `4912` directions have shifted
magnitude. **Consequence:** PR #414's per-direction structural tools are properties of
the *raw* coefficient `e_m(v_t)` (which is the `m`-subset-sum concentration of the
value-sequence `(f_t(a))_{a in mu_n}`) — its **L1** value-distribution reduction, its
**L2** quotient self-similarity, its **L3** monomial collapse, its full-group `w=1`
cyclotomic collapse `|e_m|=1`, and the whole Littlewood–Offord dictionary — and their
shared hypothesis `E(t)=e_m(v_t)` is **measured false on `E_Q`** (4880/4912). None
transfer; the masked object must be controlled by the participation-ratio bound of §2
**directly on `E_Q`**, not by any raw-coefficient identity. The engine (Parseval)
survives; the per-direction dictionary does not.

---

## 4. FIRST-CLASS CAVEAT: the win is the `tau<1` mass factor in raw-avg units  `CAVEAT` (`rem:mass-aware-logmoment` instance, `verify` §6)

**This section is not a footnote.** The `M_gen` "win" of §1 is entirely the retained
mass factor `tau < 1`, and it appears **only in raw-avg units** (dividing by `C`, not
by the masked count `T_Q`). In the **intrinsic masked-avg / PR units** that the bound
of §2 actually lives in, masking makes the object **worse** (`verify` §6):

```
                              RAW        M_gen
participation ratio PR(E_Q)   666.52  -> 2519.95     (RAISED)
effective support PR/(p^w-1)   0.1357 ->    0.5130   (RAISED)
triangle (masked-avg) 1+L1/T_Q 10.580 ->   14.782    (RAISED, >> 8.4152 budget)
triangle (raw-avg)  (T_Q+L1)/C 10.580 ->    6.071    (LOWERED -- the only unit that "passes")
```

and at toy scale the masked reference budget **overshoots the whole spectrum**:

```
nu*_masked(M_gen) = (K_Q-1)^2/(Gamma2^Q-1) = 5038.98  >  ndir = 4912   => PR-bound VACUOUS at toy scale.
```

So the **toy-informative object is the triangle constant** (raw-avg units, §1), not
the PR bound. The **deployment-scale statement** is `PR(E_Q) <= nu*_masked` with

```
nu*_ref,masked = (K_rem/tau - 1)^2,   of p^w - 1 = 2^2090837.544547 nonzero directions.
tau = 1  =>  (K_rem-1)^2 = 23088082660036 = 2^44.392214.
```

The deployment `tau` is `Theta(1)` and — sharper than "unknown" (§8) — **UNPAID**:
the mass `M_gen` removes is exactly the support-removal payment the ledger refuses to
grant (branch 7's proved deduction is the image-cell count `<= t*p`, not support
removal; the keep-largest rule is the ledger's still-open "finite-field lift-class
cost model"), and the toy shows the removal can reach `1 - tau ~ 0.59` (§1). So the
`tau < 1` factor entering the raw-avg triangle is not a deduction the deployed ledger
owns — §1's headline is CONDITIONAL on exactly that payment (§0/§8). Two further
precision points. (i) `nu*_ref,masked = (K_rem/tau - 1)^2` is the **NUMERATOR** of
`nu*_masked = (K_Q-1)^2/(Gamma2^Q-1)`: comparing it alone to the direction count
implicitly assumes `Gamma2^Q - 1 = Omega(1)`; if `Gamma2^Q - 1` is instead tiny,
`nu*_masked` only grows — and in the extreme regime `Gamma2^Q - 1 <=
nu*_ref,masked/(p^w-1)` the §6 `L^2` dichotomy already closes `(STAR)_masked`
outright by trivial-support Cauchy–Schwarz, so that regime is covered either way.
(ii) The mass factor does **not** make the bound vacuous at deployment: for any
`tau in [0.1, 1]` the numerator stays `2^44.4`–`2^51.1` (`verify` §1), **negligible
against the `p^w - 1 = 2^2090837.54` directions** whatever the exact retained mass.
The toy vacuity is therefore a pure **small-scale artifact** — the toy's direction
count is only `4912` and `Gamma2^Q-1` only `0.075`, so the tau-inflated `K_Q` tips
`nu*_masked` over `ndir`; at deployment `ndir` is astronomically large and no
`Theta(1)` `tau` comes close. **The caveat is about units, not vacuity:** the
mass-aware object is the intrinsic PR/effective-support bound (which masking
*worsens*), and the toy "win" lives only in the raw-avg triangle. This **is**
`rem:mass-aware-logmoment` (grande_finale.tex, added e83962ae), quoted verbatim:

> After first-match deletion, the primitive residual family may have total mass
> `tau<1` relative to all `m`-subsets. Consequently a proof of `prob:entropy-inverse-q`
> may not import a full-mass lower bound such as `Gamma_r^prim >= 1` unless `tau=1`
> is separately proved.

Here the `tau < 1` factor is exactly what lets the *raw-avg* triangle "pass" while the
*intrinsic* PR/effective-support object worsens — a bookkeeping mirage unless the
mass-aware unit is fixed first. Any `Gamma2^Q`/PR ledger evaluated on `P_Q` must be
stated in masked-avg units and carry its `tau`.

---

## 5. MEASURED grid: `PR` raw vs `M_gen` across five toys  `MEASURED` (`verify` §6)

Participation ratio, RAW vs the support-side generated-field mask (`verify` §6):

| p | n | m | w | domain | `PR` raw | `PR` `M_gen` | `M_gen` `tau` | prim share raw → `M_gen` |
|---|---|---|---|---|---:|---:|---:|:--|
| 17 | 16 | 8 | 3 | `F_17^*` full group  | 666.52 | 2519.95 | 0.4107 | 0.989 → 0.982 |
| 17 |  8 | 4 | 2 | `mu_8 < F_17^*`      | 127.78 |  127.78 | 1.0000 | 0.834 → 0.834 |
| 41 |  8 | 4 | 2 | `mu_8 < F_41^*`      | 737.01 |  737.01 | 1.0000 | 0.928 → 0.928 |
| 97 | 16 | 8 | 1 | `mu_16 < F_97^*`     |  20.50 |   53.51 | 0.1198 | 1.000 → 1.000 |
| 97 | 16 | 8 | 2 | `mu_16 < F_97^*`     | 843.25 | 3055.45 | 0.5133 | 0.920 → 0.957 |

Two measured facts:

1. **`M_gen` is INERT (`tau=1`) exactly on the proper-subgroup `n=8` rows** and large
   on the full-group / large-field rows. On `mu_8 < F_17^*` and `mu_8 < F_41^*` every
   finite prefix fiber carries a **single** exact `Z[zeta_8]` lift class (no finite
   lift-collisions), so "keep the largest exact class" keeps everything: `PR` is
   unchanged. Finite lift-collisions — and hence a nontrivial `M_gen` — appear only at
   the full group `(17,16,8,3)` and at the large field `mu_16 < F_97^*`.
2. **The `83–93%` primitive Fourier share SURVIVES masking.** At `(97,16,8,2)` the
   primitive stratum's share of the `L^1` mass **rises** `0.920 -> 0.957` under `M_gen`
   (generated-field removal takes mass partly off the primitive stratum), and at the
   decisive full-group row it stays `~0.98`. The primitive frequency stratum — measured
   in PR #414 §5 as `83–93%` of the raw mass — **remains the wall** after masking. So
   masking the already-paid quotient/collision cells does not relocate the obstruction;
   the primitive spectrum still carries it.

---

## 6. ROUTE-CUT: the masked dead-route table and the masked crux  `MEASURED` + `OPEN≡crux` (`verify` §7)

Adding the **masked column** to the parent packet's dead-route ladder (deployed row):

| route | object | raw status (was #412/#414) | masked status |
|---|---|---|---|
| `L^2` / `r=2` / Plancherel | `||E||_2` floor | DEAD by `1,045,396.58` bits | **INHERITED** — floor `= sqrt((p^w-1)(Gamma2^Q-1)) ~= p^{w/2} sqrt(Gamma2^Q-1)`; masking changes only `sqrt(Gamma2^Q-1)` (`0.371 -> 0.274` at the row) |
| `L-infinity` / uniform per-direction | `beta*` | DEAD by `2,090,815.35` bits (energy dichotomy) | **INHERITED** via the same `max >= RMS` dichotomy |
| sparsity / `PR <= nu*_masked` | `||E_Q||_0` (eff. support) | OPEN (raw crux, #414) | **OPEN — THE MASKED CRUX** |

**Masked `L^2`/Plancherel is dead (INHERITED).** The trivial-support Cauchy–Schwarz
bound is `||E_Q||_1/T_Q <= sqrt((p^w-1)(Gamma2^Q-1))` (exact form). Its
mask-independent factor is `sqrt(p^w-1) = p^{w/2} sqrt(1-p^-w) ~= p^{w/2}` — the
`~=` is off by exactly `sqrt(p^w/(p^w-1))`, rel `1.0e-4` at the toy (`26.006` exact
vs `26.009` in the `p^{w/2}` form) and rel `~2^-2090838` at deployment. Masking
rescales only the `sqrt(Gamma2^Q-1)` factor — exactly (`verify` §7):

```
mask      sqrt(Gamma2^Q-1)   floorRHS = sqrt((p^w-1)(Gamma2^Q-1))   (sqrt(p^w-1) = 70.086 ~= p^{w/2} = 70.093)
RAW           0.3711                  26.006
M_quot        0.3677                  25.767
M_gen         0.2745                  19.242
M_both        0.2671                  18.718
```

The `sqrt(p^w-1) ~= p^{w/2}` scaling is **inherited unchanged** (mask-independent).
At deployment the masked `L^2` route
is dead by **essentially the parent `1,045,396.58`-bit margin** unless masking drives
`Gamma2^Q - 1 <= nu*_ref/(p^w-1) ~ 2^{-2090793}` — in which case trivial-support
Cauchy–Schwarz already closes `(STAR)_masked` outright (the same dichotomy as PR #414
§3). **Masked `L-infinity`** dies via the identical energy floor `max|E_Q|/T_Q >=
sqrt((Gamma2^Q-1)/(p^w-1))`.

Therefore, exactly as in the raw case, `PR(E_Q) <= nu*_masked` is **the sole
non-floor-bound route** — the masked crux, and precisely the tighter variant PR #414
leaves `OPEN`. The win must come from **sparsity** (few large masked directions) plus
**cancellation** (most negligible), not any single-direction or second-moment estimate.

---

## 7. FALSIFIER / boundary: the mask must not produce a sparse-heavy residual  `MEASURED` + structural (`verify` §8)

The support-mask cannot be pushed arbitrarily. **Over-pruning** to the single largest
honest exact-lift class — collapsing all retained mass onto one primitive fiber —
gives the worst possible spectrum (`verify` §8):

```
single largest exact class, all mass on ONE fiber z0:
PR(E_Q) = 4912 = p^w - 1   (FULL support delta spectrum, effsupp = 1.0000),
triangle(masked-avg) = 1 + ||E_Q||_1/T_Q = 4913 = p^w   (maximal; every route vacuous),
Gamma2^Q - 1 huge  =>  nu*_masked = (K_Q-1)^2/(Gamma2^Q-1) tiny  =>  PR >> nu*_masked for any finite K.
```

A delta in support space is a **flat** (full-support) spectrum in frequency space:
`PR` hits its ceiling `p^w-1`. So the mask must leave a **dense-heavy** residual fiber,
not a sparse-heavy one. This is a genuine precondition, and it is exactly the
hypothesis `rem:mass-aware-logmoment` flags — quoted verbatim:

> The finite proof route should therefore use an off-diagonal or falling-factorial
> collision moment, **prove a dense-heavy-fiber hypothesis before invoking ordinary
> moments, or name sparse-heavy primitive fibers as an explicit residual cell.**

`MEASURED` (the falsifier spectrum) + the structural statement: the masked PR route
is contingent on the residual being dense-heavy; an over-aggressive first-match mask
that isolates a sparse-heavy primitive fiber **falsifies** the route, and such fibers
must be charged to their own residual cell rather than left in `P_Q`.

---

## 8. HONEST SCOPE: the masks MODEL, not REPLICATE, the deployed ledger  `MEASURED` (scope)

The four toy masks are **faithful reconstructions of two ledger first-match branches**,
verified against `kb_mca_1116048_first_match_ledger_v1.md` ("First-match branches"):

- **`M_quot` = branch 4** ("quotient-periodic or divisor-stabilized"): remove the
  2-periodic supports `S = -S` (the `c=2` quotient cell of `def:coefficient-scale`,
  subsuming `c=4,8` for even `m`).
- **`M_gen` = branch 7** ("base generated-field collision"): per finite fiber keep only
  the **largest exact `Z[zeta_n]` lift class**, charge the rest to generated-field.
  This is the ledger's own **largest-honest-class worst-case model** — the ledger's
  `F_17` replay (`n=16`, `D=<3>`, `j=8`, `w=1`, target `z=1`) records `finite fiber
  size 757`, `193 exact lift classes`, **`largest exact lift class: 20`**,
  `non-retained supports after keeping largest exact class: 737`, exactly the
  keep-the-largest / charge-the-rest rule `M_gen` implements.

**The ledger presents that same F_17 replay as its counterexample to this removal
being PAID** ("This is a real support-vs-image obstruction, not just a missing
phrase."): the `737` non-retained supports stand against only `w*p = 17`
generated-field image cells. The keep-largest rule is the ledger's own "tempting
stronger route" — "for each finite target `z`, retain one exact lifted prefix class
and send every other exact lifted class over the same `z` to generated-prefix
collisions" — and the ledger **explicitly declines to mark it proved**: "This packet
does not mark that route as proved", because "a row-indexed `w*p` image-cell count
does not by itself bound the number of removed exact lift classes or raw supports";
"their support multiplicity is not paid by the image-cell count" (all verbatim,
grep-verified). Branch 7's PROVED deduction is the **image-cell count**
("generated-field collision image cells, cost <= t*p"); `M_gen`'s support-side
removal is the ledger's separate, still-open missing item — the "finite-field
lift-class cost model if exact-lift bounds are to be used". **So the toy `tau < 1`
is NOT a paid deduction, and §1's headline is CONDITIONAL on exactly that payment:**
the masked triangle route fits the budget where raw fails **iff** the lift-class
support-removal cost model is ever paid. This packet pins that precise dependency
of the masked route.

**Scope, explicit.** These **model, do not replicate**, the deployed ledger. The
deployment runs at `n=2^21`, `w=67471`, with the full ten-branch first-match order and
the exact `Z[zeta_{2^21}]` lift arithmetic; the toys reconstruct branches 4 and 7 on
small `mu_n` at `w in {1,2,3}`. The toy measurements (§1/§5) are illustrative of the
**mechanism** (support-side masking repairs the raw overstrong route; the quotient cell
alone does not; the primitive stratum persists), and the §4 caveat about the intrinsic
PR object is a **general** consequence of `tau < 1` that applies at deployment too. The
masked PR bound at deployment (§6) is stated, not proved.

---

## 9. Weave  `AUDIT`

Previously-open cited PRs were integrated at e83962ae (byte-identical); PR #414 is
still OPEN (this packet is its follow-on). Citations by repo path / branch.

- **Parent — PR #414 (OPEN)** — `cap25_v13_q_em_inverse_participation_ratio.md`,
  branch `thresholds-em-inverse-participation-ratio` @`54f8129` — *extends its named
  open variant*. #414 reduced the raw `(STAR)` to `PR(Rhat) <= nu*` and flagged as its
  tighter open variant "the participation ratio of `E_Q` on `P_Q` against the same
  `nu*` ledger". **This packet is that variant**, made concrete: §2 transfers the
  equivalence verbatim to `E_Q`, §3 shows the mask is support-side (so #414's raw L1/L2/
  L3 lemmas do not carry), §6 inherits #414's `L^2`/`L-infinity` route-cuts, and §4/§7
  supply the caveat and falsifier #414 could only name. Non-conflicting: #414 claims
  `(STAR) <=> PR<=nu*` on the raw spectrum; we claim the identical algebra on `E_Q`,
  never `(STAR)_masked <=> atom`.
- **Object source — PR #413** — `cap25_v13_signed_em_masked_residual_audit.md`
  (integrated e83962ae) — *answers its masked-side question, affirmatively-with-caveat*.
  #413 proved the raw `(STAR)` is sufficient-but-overstrong and named `E_Q(t)` as the
  theorem-facing object; its repaired target
  `CAP25-V13-CHARACTER-PHASE-MASKED-SIGNED-EM-INVERSE` asks for support-side control.
  We answer: at #413's **own** counterexample row `(17,16,8,3)` support-side masking
  (`M_gen`) pulls the L1 triangle from `10.4728` (over budget) to `5.967` (under
  `8.4152`) — **viable exactly where raw is overstrong** (§1) — but the win is a
  raw-avg-units `tau` artifact (§4), the removal is the ledger's unpaid lift-class
  support cost (§8; the headline is conditional on that payment), and the
  frequency-quotient cell alone worsens it (§1). All three of #413's printed numbers (`2.672183`, `10.472846`, `8.4152079724`)
  replayed and gated (`verify` §3).
- **Floor inheritance — PR #412** — `cap25_v13_q_pw2_concentration_floor.md`
  (integrated e83962ae) — *inherited route-cut*. Its `p^{w/2}` concentration floor
  (`1,045,396.58` bits) survives masking: the masked floor is `p^{w/2}
  sqrt(Gamma2^Q-1)`, masking rescaling only the `sqrt` factor (`0.371 -> 0.274`, §6/
  `verify` §7). The masked `L^2`/`L-infinity` routes are dead by essentially the parent
  margins.
- **`rem:mass-aware-logmoment`** (grande_finale.tex, added e83962ae) — *instantiated*.
  The §4 caveat **is** this remark's concrete instance (`tau<1` in raw-avg units), and
  the §7 falsifier **is** its "prove a dense-heavy-fiber hypothesis ... or name
  sparse-heavy primitive fibers as an explicit residual cell" precondition. Both
  four-line clauses quoted verbatim and grep-verified against the tex.
- **`thm:fourier-flat-q`** (grande_finale.tex, added a5b7912) — *consistent-with,
  inherited margin*. The masked leaves inherit the **same finite-margin question**:
  the tex states the flat route "is not a deployed adjacent certificate unless the
  explicit Fourier error fits the row's finite margin" (Conclusion section, verbatim;
  the quoted sentence concerns thm:fourier-flat-q directly, not prop:q-exact-target).
  §6's masked floor/`nu*_masked` are precisely that finite margin, evaluated on `E_Q`
  — masking does not enlarge the affordable Fourier slack.
- **avdeev Route-D** — `rowsharp_q_prefix_atom_reductions_v1.md` (integrated e83962ae,
  was PR #397) — *consistent-with*. Route-D is the primitive full-rank support stratum;
  §5's measurement that the primitive Fourier share **survives masking** (`0.920 ->
  0.957`) is consistent with the mass sitting in Route-D's stratum — masking the paid
  quotient/collision cells leaves the primitive wall in place.
- **Hughes b2 Round (o)** — `b2_conjq_partial_results.md` (integrated e83962ae, was PR
  #398) — *unaffected*. His raw-identity convergence `Rhat(c)=e_m(v_c)` and the raw
  `(STAR)` target are the raw object; first-match masking is a separate support-side
  operation on `P_Q`, so his rounds are neither used nor obstructed here.

### One-line verdict
The PR #414 equivalence `(STAR) <=> PR <= nu*` transfers **verbatim** to the masked
residual `E_Q` (`REDUCED`, for `K_Q >= 1`); at #413's own counterexample row
support-side generated-field masking pulls the L1 triangle from `10.4728` (over
budget) to `5.967 / 6.071 < 8.4152` (`MEASURED`; `CONDITIONAL` — the removal is
exactly the ledger's unpaid lift-class support cost, §8) — viable **where raw is
overstrong** — while the
frequency-quotient cell alone worsens it to `11.89`; the mask is genuinely support-side
(`4880/4912` frequency-mixed, **not** a character projection), the `p^{w/2}` floor is
**inherited**, and the sole non-floor route `PR(E_Q) <= nu*_masked` stays `OPEN≡crux`
— **with the first-class caveat** (`rem:mass-aware-logmoment`) that the entire toy win
is the `tau<1` mass factor in raw-avg units: in intrinsic PR units masking *raises*
`PR` (`666 -> 2520`) and effective support (`0.14 -> 0.51`), and the toy-informative
object is the triangle constant, not the PR bound.

## 10. Replay
```
python3 experimental/scripts/verify_q_eq_masked_participation_ratio.py
#   RESULT: PASS (61/61 checks), exit 0 (~17 s) -- everything above, self-contained.
```
