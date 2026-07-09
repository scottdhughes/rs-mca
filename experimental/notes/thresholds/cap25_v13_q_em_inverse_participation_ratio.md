# CAP25 v13 raw: the signed-e_m inverse = a Fourier participation-ratio bound — the p^{w/2} floor is its trivial-support case (KB-MCA a=1116048)

Status: `REDUCED` (headline §1 — exact algebraic equivalence `(STAR) <=> PR(Rhat)
<= nu*`) / `OPEN≡crux` (the bound itself — the open input of the sufficient
`(STAR)` route to `prob:row-sharp-q` / `def:q-row-atom`; its tighter
masked-residual variant, §7) / `PROVED` (three structural lemmas + full-group
`w=1` collapse §4; §3 L∞ route-cut via the energy dichotomy) / `REFERENCE` (§2
parent-floor recovery, §6 four-row budget — exact computations) / `MEASURED` (§5
primitive-stratum mass + sparsity, exact toy enumeration).

**Verifier:** `experimental/scripts/verify_q_em_inverse_participation_ratio.py`
(zero-arg, stdlib-only, ~90 s, `RESULT: PASS (54/54 checks)`, exit 0): exact
big-int ledger, the `(STAR)`/`PR`/`nu*` arithmetic, the L-infinity margin,
floor recovery to the digit, the four-row table matched to `grande_finale.tex`
`prop:q-exact-target`, toy lemmas L1/L2/L3, faithful-toy Parseval + participation
ratio, the full-group `w=1` cyclotomic collapse, the whole §5 stratification table
including the primitive-only sup (witness-vs-lemma closure — every number
recomputed), the Parseval identity and the §3 energy floor gated on every shipped
row, an independent replay of the masked-residual audit's F_17 counterpacket, and
six tamper self-tests. Cross-validated against the integrated
`experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md` and the
integrated parent packet (was PR #412).

This is a focused follow-on to the concentration-floor packet
(`cap25_v13_q_pw2_concentration_floor.md`, integrated e83962ae, was PR #412): it
does **not** prove `U(1116048) <= B*`, the KB-MCA first-safe agreement, or the
row-sharp Q atom — it reformulates the one open L¹ input (`OPEN≡crux`), extends
the parent route-cut one norm up, proves three sub-lemmas, and measures where the
mass lives. Scope, per the masked-residual audit (was #413, weave §7): `(STAR)`
is a **sufficient — possibly overstrong — certificate** for the true L∞ atom
after first-match deletion; the equivalence claimed here is `(STAR) <=> PR <=
nu*`, never `(STAR) <=> atom`. Every claim carries a label.

---

## 0. Setup and the exact Fourier reduction  `REFERENCE` (imported-proved)

Over `F_p`, `p = 2^31-2^24+1 = 2130706433`, let `D = mu_n` be the multiplicative
subgroup of order `n = 2^21` (`p-1 = 2^24·127`, index 1016). Prefix map
`Phi_w(M) = (p_1(M),...,p_w(M))` (power sums; Newton-equivalent to the coefficient
prefix since `char = p > w`). `N(z) = |Phi_w^{-1}(z)|`, `Fbar = C(n,m) p^{-w}`.
Hughes / `prop:fourier-audit` (grande_finale.tex), Parseval-exact (parent packet
§6, was PR #412, and `verify` §6/§6c, relerr `< 1e-14`):

```
E(t) = sum_{|M|=m} e_p( t . Phi_w(M) ) = e_m(v_t),   v_t = ( e_p(f_t(a)) )_{a in mu_n},
       f_t(x) = sum_{i=1}^w t_i x^i,      e_p(x) = exp(2 pi i x / p),
max_z N(z) <= p^{-w} ( C(n,m) + sum_{t != 0} |e_m(v_t)| ).            (Fourier bound)
sum_{t!=0} |E(t)|^2 = p^w sum_z (N(z)-Fbar)^2.                        (Parseval)
```

Deployed constants, recomputed exactly (`verify` §1; matches the integrated
`rowsharp_q_prefix_atom_reductions_v1.md` (integrated e83962ae, was PR #397),
`cap25_v13_q_pw2_concentration_floor.md` (integrated e83962ae, was PR #412), and
the integrated `kb_mca_1116048_first_match_ledger_v1.md`):

```
n=2^21  m = n-a = 981104  w=67471   C=C(n,m): log2 C=2090873.279793
p^w: log2 = 2090837.544547     avg = C/p^w = 2^35.735246
avg_floor=57198030365   target_floor=274836936291722953   Krem=4805007   Kraw=4807520
```

`Krem=4805007` is the **integrated first-match ledger constant**
(`kb_mca_1116048_first_match_ledger_v1.md`: `K_rem = floor(B_rem·p^w/C(n,j)) =
4805007`, after reserving `t*p = 143763024447376` for the non-Q first-match cells;
`Kraw=4807520` is the pre-reservation ratio). The atom is `max_z N(z) <= Krem·avg`
after first-match payments (`R_prim <= N_w` pointwise). By (Fourier bound) it
**follows from** the exact L^1 target

```
(STAR)     sum_{t != 0} |e_m(v_t)|  <=  (Krem - 1) * C(n,m).
```

`(STAR)` is the L¹ certificate named by the parent packet (§7 of
`cap25_v13_q_pw2_concentration_floor.md`, was PR #412). Per the masked-residual
audit (`cap25_v13_signed_em_masked_residual_audit.md`, was #413; weave §7) it is
**sufficient for the atom but stronger than necessary** — the theorem-facing
object after first-match deletion is the masked residual `E_Q(t)` on the pruned
family `P_Q`, and the atom is an L∞ family of phase inequalities, not the raw L¹.
This packet treats `(STAR)` as the sufficient route it is. Its only
norm-inequality specialization (Cauchy–Schwarz on the `t`-sum) is the
second-moment route, floor-dead.

---

## 1. HEADLINE: (STAR) is exactly a Fourier participation-ratio bound  `REDUCED`

Write `Rhat(t) := e_m(v_t)` for `t != 0`. Set

```
||Rhat||_1 = sum_{t!=0} |e_m(v_t)|,     ||Rhat||_2^2 = sum_{t!=0} |e_m(v_t)|^2,
Gamma2 := p^w sum_z N(z)^2 / C^2  (>= 1),   so by Parseval  ||Rhat||_2^2 = C^2 (Gamma2 - 1),
PR(Rhat) := ||Rhat||_1^2 / ||Rhat||_2^2       (participation ratio = effective
                                               Fourier-support size of the spectrum).
```

**Reduction (exact algebraic equivalence).** Dividing `(STAR)^2` by the fixed number
`||Rhat||_2^2 = C^2(Gamma2-1)`:

```
(STAR)  <==>  PR(Rhat)  <=  nu* := (Krem - 1)^2 / (Gamma2 - 1).
```

Not a tautology: `PR` and `Gamma2` are two different scalar functionals of the
**same** spectrum, and the missing input is now named — an **effective-support /
large-spectrum bound** on `Rhat`, exactly the object of Chang's lemma and
inverse-Littlewood–Offord (`rem:standard-inverse-gap` cites this literature:
Tao–Vu inverse LO, Green–Ruzsa/PFR, GGMT). The equivalence holds for the true
(unknown) `Gamma2`; it is exact for **any** `Gamma2`. Reference budget at
`Gamma2-1 = 1` (`verify` §2):

```
nu*_ref = (Krem-1)^2 = 4805006^2 = 23088082660036 = 2^44.392214,
of  p^w - 1 = 2^2090837.544547  nonzero directions   (fraction 2^-2090793.15).
```

Reading: **row-sharp Q at KB-MCA follows once the signed-e_m spectrum has effective
support at most ~2^44.39** (calibrated by its own L^2 energy) — a `2^-2090793`
fraction of all directions must be Fourier-negligible. The toys (§5) measure
`Gamma2-1 = O(1)` small (`0.0137` in the most faithful toy), so `nu*_ref ~
(Krem-1)^2` is the operative budget (a **sufficient** target whenever the true
`Gamma2-1 <= 1`; the true budget is `1/(Gamma2-1)`× larger — ≈73× at the faithful
toy). This row's `nu*_ref` uses the integrated first-match `Krem`; §6's four-row
table evaluates the same quantity in the pre-reservation `Kraw` regime
(`K = B*/ceil(avg)`), giving `2^44.394` here — same object, budget conventions
differing only by the first-match reservation (§0). Self-consistency: if `Gamma2`
were the loose-ledger value `2^2090837.54` (parent packet route iii), `nu* < 1`
and the reduction is vacuous — but that `Gamma2` is exactly the floor-dead case,
i.e. the atom would then be false.

---

## 2. The parent packet's p^{w/2} floor is the trivial-support special case  `REFERENCE`

Cauchy–Schwarz on the support `Sigma = supp(Rhat)` gives `||Rhat||_1 <=
sqrt(|Sigma|) ||Rhat||_2`, so `(STAR)` follows from `|Sigma| <= nu*`. The **trivial**
support `|Sigma| = p^w - 1` recovers the parent packet's floor (integrated
e83962ae, was PR #412) to the digit (`verify` §4):

```
||Rhat||_1 / C  <=  sqrt( (p^w-1)(Gamma2-1) );  at Gamma2-1 = 1 (minimal):
||Rhat||_1 / C  <=  sqrt(p^w-1) = 2^1045418.7723 = 2^{(w/2) log2 p},
vs budget (Krem-1) = 2^22.196107   =>  SHORT by 1045396.58 bits.
```

`1045396.58` is **identical** to the parent packet's headline floor gap
(`1,045,396.58` bits, its §1). So the parent floor = this reduction at trivial
(full) support; the present packet isolates precisely the surplus needed beyond
`L^2`: a nontrivial effective-support bound. This is the exact sense in which it
extends the parent "one level up" (from `||Rhat||_2` to `||Rhat||_0`).

---

## 3. L-infinity per-direction route-cut  `PROVED` (route-cut)

Any argument that bounds each direction uniformly, `|e_m(v_t)| <= beta·C` for all
`t != 0`, and triangulates, gives `||Rhat||_1 <= beta·C·(p^w-1)`; this meets
`(STAR)` **iff**

```
beta <= beta* := (Krem-1)/(p^w-1) = 2^-2090815.3484.
```

`beta*` is unreachable by any per-direction bound. **Measured** (`verify` §6b,
toys §5): quotient directions (`f_t = g(x^c)`, `c|n`, `c>1`, §4 L2) have `|e_m|/C`
up to order 1 (toy global `max|e|/C` to `0.754`, quotient-attained); restricted to
the **primitive** stratum the per-direction sup is still macroscopic —
`max_{c(t)=1}|e_m|/C = 0.02914 / 0.12097 / 0.43413 / 0.25407` across the four §5
toys (gated per row), i.e. `>= 0.029 >> 2^-2090815` everywhere; the smallest
primitive spikes are the monomial/coset directions (§4 L3).

**Energy floor (PROVED) — the cut is unconditional, not just measured.** Since
`max >= RMS`, any spectrum satisfies `max_{t!=0} |e_m(v_t)|/C >=
sqrt((Gamma2-1)/(p^w-1))` (gated on every shipped row, `verify` §6c). Dichotomy:
either `Gamma2-1 <= nu*_ref/(p^w-1) = 2^-2090793.15`, in which case trivial-support
Cauchy–Schwarz (§2) already yields `(STAR)` outright — or `Gamma2-1 >
2^-2090793.15`, and the energy floor forces `max|e_m|/C > sqrt(2^-2090793.15 /
2^2090837.54) = beta*`, so no uniform per-direction estimate can close `(STAR)`.
**Either way the L-infinity route contributes nothing: dead by ~2,090,815 bits of
per-direction margin in the non-vacuous case.** The win must come from
**sparsity** (few large directions) plus **cancellation** (most directions
negligible) — the participation-ratio bound of §1, not any single-direction
inequality. This adds the `r=infinity` column to the parent packet's dead-route
table (which covered `r=2` / `L^2` / Cauchy–Schwarz / Plancherel).

Dead-route ladder (deployed row, exact margins):

| route | object | dead by | source |
|---|---|---:|---|
| L^2 / r=2 / Plancherel | `||Rhat||_2` floor | 1,045,396.58 bits | parent §1 (was #412; = §2 here) |
| L-infinity / uniform per-direction | `beta*` | 2,090,815.35 bits | §3 here |
| sparsity / PR <= nu* | `||Rhat||_0` (eff. support) | OPEN — the crux | §1 here |

---

## 4. Proved structural lemmas  `PROVED` (exactly verified, `verify` §6)

Let `N_t(s) = #{a in mu_n : f_t(a) = s}` be the level-set sizes of `f_t` on `mu_n`.

- **L1 (value-distribution reduction).** `e_m(v_t)` depends **only** on the multiset
  `{ f_t(a) }`, i.e. on `N_t(.)`: `e_m(v_t) = [T^m] prod_s (1 + T e_p(s))^{N_t(s)}`.
  So the entire signed-e_m inverse is a statement about **level-set concentration of
  degree-w polynomials on `mu_n`** — a finite combinatorial object. (max `|e_m|`
  difference within identical value-distribution `< 1e-14`.)

- **L2 (quotient-convolution self-similarity).** If `f_t(x) = g(x^c)` with `c|n`
  (coefficient-scale `s(t) = gcd(n, supp(t)) >= c`, `def:coefficient-scale`), then
  `x -> x^c` is `c`-to-1 from `mu_n` onto `mu_{n/c}`, and `e_m(v_t) = [T^m] ( sum_j
  e_j(w_g) T^j )^c`, `w_g = ( e_p(g(y)) )_{y in mu_{n/c}}` — the `c`-fold convolution
  power of the smaller system at depth `<= w/c`. The Fourier-side image of quotient
  pullback (`prop:sp-pullback`, `thm:coeff-quotient-extract`): quotient directions
  are exact self-similar copies of a lower row. (max err `< 1e-13` over all `c=2`
  directions.)

- **L3 (monomial collapse).** For `i` coprime to `n`, `x -> x^i` **permutes** `mu_n`,
  so the monomial direction `f_t = t_i x^i` has the **same** value-distribution
  (hence `|e_m|`) as the linear coset direction `t_i x`; its value-set is the coset
  `t_i mu_n`. The monomial primitive directions all reduce to the single "coset"
  building block. (all `i` coprime to `n` tested, `n in {8,16}`.)

- **Full-group `w=1` collapse (a proved inverse on a nonempty class).** For `D =
  F_p^*` (`n = p-1`) and any `w=1` direction `t_1 != 0`, the cyclotomic identity
  `prod_{b=1}^{p-1}(1 + T e_p(b)) = (1+T^p)/(1+T)` gives `|e_m(v_t)| = 1` **exactly**,
  for every `t_1 != 0` and every `m`. Hence on this class `sum_{t!=0}|e_m| = p-1 <<
  (Krem-1)C` — the inverse **holds with astronomical room, proved** (the single
  Fourier magnitude behind `prop:mode-null-false`). (`p in {13,17,23}`.) The extremal
  cancellation: for the most structured directions the coefficient collapses far
  **below** the `sqrt(C)` L^2-floor value, to `1`.

---

## 5. Near-extremizer structure + toy measurements  `MEASURED` (exact enumeration, `verify` §6b)

By L1, `|e_m(v_t)|` is large iff `N_t(.)` is concentrated, i.e. `f_t` has large
level sets — i.e. `f_t` is (approximately) a function of `x^c` for some `c|n`,
`c>1` (**approximately quotient-borne**, coefficient-scale `> 1`), the first-match
quotient-pullback stratum. The **primitive** spikes (coefficient-scale `1`) with the
largest `|e_m|` are the monomial/coset directions (L3).

Toy stratification (coefficient-scale `c(t) = gcd(n, supp(t))`; every cell recomputed
by `verify` §6b):

| p | n | m | w | avg | R_true | prim L^1/C | quot L^1/C | prim share | max\|e\|/C |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 97 | 16 | 8 | 1 | 132.68 | 1.4923 | 0.5302 | 0 (none) | 100% | 0.02914 |
| 97 | 16 | 8 | 2 | 1.368 | 5.8486 | 27.841 | 2.422 | 92.0% | 0.19631 |
| 41 | 8 | 4 | 2 | 0.042 | 48.03 | 122.62 | 9.543 | 92.8% | 0.75425 |
| 17 | 8 | 4 | 2 | 0.242 | 8.257 | 16.996 | 3.371 | 83.5% | 0.50406 |

(`max|e|/C` is the global maximum over all nonzero directions — for `w>=2` toys it
is attained on a quotient direction; the `w=1` toy has no quotient directions.)

Two measured facts:
1. **The primitive stratum carries the wall.** In every `w>=2` toy the primitive
   directions hold **83–93%** of the `L^1` mass (`verify` §6b: shares
   `0.920/0.928/0.834`). So "kill only the quotient (already-paid) directions" is
   **insufficient** — the reduction must control the primitive spectrum.
2. **In the deployment-faithful regime (avg `>> 1`) the inverse holds with room and
   the spectrum is genuinely sparse.** The most faithful toy (`p=97,n=16,m=8,w=1`,
   avg `132.7`, like deployment avg `2^35.7`) has `R_true=1.4923`, `L^1/C=0.5302`,
   `max|e|/C=0.02914`, triangle bound tight at `x1.025`, `Gamma2-1=0.0137`, and
   **participation ratio PR=20.5 of 96 directions** (`PR/#dirs=0.21`). Across toys
   PR grows slowly (`11 -> 13 -> 20 -> 27 -> 843`) while `#dirs` grows exponentially
   — the effective support is `<< #dirs`, consistent with `PR <= nu*` at deployment.

**Connection to `prob:entropy-inverse-q` (rewritten at a5b7912) / Vandermonde.**
By L1 + the Littlewood–Offord dictionary, `|e_m(v_t)|` is the `m`-subset-sum
concentration of the value-sequence `(f_t(a))_{a in mu_n}`; large only if that
sequence is additively structured. `prob:entropy-inverse-q` is now the standalone
**primitive entropic inverse theorem for Vandermonde slice sums**: fixed-density
profile slices on the **pruned** residual family `Omega^o` (first-match-type cells
removed — the same masking discipline as the residual audit, §7), normalized Renyi
collision excess `Gamma_ell >= exp(eta*N*ell)` with `ell -> infinity`, concluding
either (a) a positive-density restriction into a paid algebraic cell, or (b) a
positive-density Vandermonde rank defect — which `prop:vandermonde-kills-low-rank`
kills at moment-curve range; a robust Sidon/free-energy branch is admitted (either
entropy-small trade differences feed entropic-BSG/PFR, or free-energy decay bounds
that level's `Gamma_ell` contribution). The PR bound of §1 is its **finite-row,
moment-order-free (max-fiber) counterpart on the raw spectrum**: the open
structural content is steps 4–6 of `rem:entropy-inverse-skeleton` (entropy-BSG ->
PFR/Green–Ruzsa structuralization -> slice-derivative, or the free-energy decay
alternative; steps 5–6 remain the flagged nonstandard parts) — nothing here closes
them. The asymptotic side is now **conditionally closed given that atom**
(`thm:asymptotic-rs-mca-closure-combined` via `thm:primitive-q-closure-module` and
`lem:largest-fiber-to-excess-closure`, `sec:conditional-asymptotic-closure`); the
finite deployed rows — where this packet's budgets live — remain the open side.

---

## 6. Four-row parameter translation  `REFERENCE` (exact computation, `verify` §5)

`nu*(row) = (K-1)^2/(Gamma2-1)`, `K = B*/ceil(avg)` the exact rational budget of
`prop:q-exact-target`. Reference `nu*_ref = (K-1)^2` at `Gamma2-1=1` (avgceil and
`K`-ratio matched to `grande_finale.tex` for all four rows):

| row | a_+ | w | m | K = B*/avg | log2 nu*_ref | log2(#dir) |
|---|---:|---:|---:|---:|---:|---:|
| KoalaBear MCA  | 1116048 | 67471 | 981104 | 4807520.9295 | 44.394 | 2090837.54 |
| KoalaBear list | 1116047 | 67471 | 981105 | 4226236.5253 | 44.022 | 2090837.54 |
| Mersenne-31 MCA  | 1116024 | 67447 | 981128 | 9.5722 | 6.199 | 2090857.00 |
| Mersenne-31 list | 1116023 | 67447 | 981129 | 8.4152 | 5.781 | 2090857.00 |

(KB-MCA with the integrated first-match `Krem=4805007`: `nu*_ref = 2^44.3922`. The
four-row `K` is `B*/ceil(avg)` = the `Kraw` regime, giving KB-MCA `44.394`; the two
differ only by the first-match reservation, §0.)

**The binding row is Mersenne-31 list:** `nu*_ref = 2^5.781 ~ 55` — the reduction
there asks that the signed-e_m spectrum have effective support **at most ~55
directions** out of `2^2090857` (`Gamma2-1=1` reference). This is the sharpest,
most concrete standalone target the program has for the `(STAR)` route: *bound the
participation ratio of the M31-list prefix-fiber's nonzero-frequency Fourier
transform by ~55.* The finite, moment-order-free counterpart of
`prob:entropy-inverse-q` (itself now stated RS-free for isolated attack; §5) —
noting (masked-residual audit, §7) that at this row the raw-L1 route is
demonstrably overstrong in a full-group toy: `2.672 < 8.4152 < 10.473`
(`verify` §6c), so the masked-residual PR analog is the tight variant.

---

## 7. Weave  `AUDIT`

All previously-open cited PRs were integrated at e83962ae (2026-07-08 morning
sweep, byte-identical); citations below are by integrated repo path.

- **Parent packet** — `experimental/notes/thresholds/cap25_v13_q_pw2_concentration_floor.md`
  (integrated e83962ae, was PR #412) — *affected-downstream / extends*. This
  packet's §2 is its `p^{w/2}` floor as the trivial-support special case of §1's
  reduction (`1,045,396.58` bits, recomputed to the digit, `verify` §4); §3 adds
  the `L-infinity` column above its `L^2` floor. Non-conflicting: same open input,
  one norm up.
- **Masked-residual audit** — `experimental/notes/thresholds/cap25_v13_signed_em_masked_residual_audit.md`
  (integrated e83962ae, was PR #413) — *scope-clarifying, non-conflicting*. It
  proves the raw signed-e_m L¹ target `(STAR)` is a **sufficient but overstrong**
  certificate for the true L∞ row-sharp atom after first-match deletion: the
  theorem-facing object is the masked residual `E_Q(t) = Σ_{M in P_Q}
  psi(t·Phi_w(M))` on the pruned family `P_Q`, and its toy counterpacket
  (`p=17, D=F_17^*, n=16, m=8, w=3`) has true max-fiber ratio `2.672183` **below**
  the M31-list budget `8.4152` while the primitive signed-L1 triangle constant is
  `10.4728` **above** it — all three replayed and gated here (`verify` §6c). This
  packet is untouched: it claims only `(STAR) <=> PR(Rhat) <= nu*`, never `(STAR)
  <=> atom` (§0). Closing our PR bound re-establishes the (possibly overstrong)
  sufficient route; the **masked-residual PR analog** — the participation ratio of
  `E_Q` on `P_Q` against the same `nu*` ledger — is the tighter open variant that
  the audit's repaired target names. Moment-side face of the same masking point:
  `rem:mass-aware-logmoment` (tex, added e83962ae) — after first-match deletion
  the residual family has mass `tau < 1`, so full-mass lower bounds (`Gamma_r >=
  1`) may not be imported; the identical discipline applies to any `Gamma2`/PR
  ledger evaluated on `P_Q` instead of the full family.
- **Origin of the identity (attribution)** — the Fourier identity `E(t) =
  e_m(v_t)` of §0 is **Hughes's observation** (comment on the PR #397 thread,
  2026-07-07); recorded here as consumed provenance exactly as the parent packet
  records it — verified independently (Parseval-exact), not claimed as new.
- **Hughes partial-results package** — `experimental/notes/roadmaps/b2_conjq_partial_results.md`
  (integrated e83962ae, was PR #398) — *convergent-independent (same object,
  disjoint contributions)*. Its Round (o) (2026-07-07, same day) independently
  derives the identical object `Rhat(c) = e_m(v_c)` and the same `(STAR)` target
  `sum_{c!=0}|e_m| <= (L-1)C(n,m)`, and shows his freeze families inflate `pi_odd`
  but leave `e_m` negligible (corroborating the primal max-fiber form); his Round
  (b) explores large-spectrum methodology on the `pi_odd`/SP side
  (`b2_sp_large_spectrum.py`). Our content beyond his rounds = the `PR <= nu*`
  equivalence, the L1–L3 lemmas, and the stratified measurements — **not** the
  base identity or the `(STAR)` target. Non-conflation retained: his earlier
  `pi_odd` power-sum rounds and the x4b moment-column cap
  (`experimental/notes/roadmaps/x4b_moment_column_cap.md`, integrated e83962ae,
  was PR #402) are **different columns** from `e_m` — neither obstructs the PR
  bound.
- **Row-sharp Q-atom reductions** — `experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md`
  (+ `rowsharp_q_prefix_atom_routes_v1.md`; integrated e83962ae, was PR #397,
  avdeev) — *same-object, dual view (consistent-with, not-derived-from)*. Its
  Route-D large-signed-defect certificate (the primitive full-rank support
  stratum) is the **primal** side of the object §1 names on the Fourier side. Our
  §5 measurement — the primitive stratum carries 83–93% of the `L^1` mass — is
  **consistent with, not derived from**, it: the mass sits exactly in Route-D's
  stratum. (`E_ret <= binom(16,7) = 11440` imported-PROVED there.)
- **Binding-row calibration** — `experimental/notes/thresholds/cap25_v13_q_atom_binding_row_calibration.md`
  (integrated e83962ae, was PR #407, ours) — *consistent-with (unaffected)*. Its
  measured concentration constant `kappa <= 1.221` is consistent with the toy
  `R_true ~ 1`–`1.5` at avg `>> 1` (§5): the atom is almost certainly true; the
  wall is proof-method.
- **Moment-floor reconciliation** — `experimental/notes/thresholds/cap25_v13_q_moment_floor_reconciliation.md`
  (integrated e83962ae, was PR #392) — *provenance-consumed*. The
  precision/convention source behind the `Delta_Q`/order-floor constants the
  parent packet §5 reconciles; unaffected here (we use `Krem`/`Kraw` directly,
  §0).
- **Fourier-flat route (new tex, a5b7912)** — `thm:fourier-flat-q` +
  `def:fourier-flat-prefix-leaf` + `cor:large-characteristic-fourier-examples` —
  *consistent-with (complementary, asymptotic side)*. The maintainer's sufficient
  condition for asymptotic Q: a per-mode character-sum bound `L` fed through the
  Li–Wan distinct-coordinate sieve, with Weil-bound examples at `w = o(sqrt p)`.
  This packet is its **finite-row quantitative counterpart**: the tex's own
  conclusion states the flat route "is not a deployed adjacent certificate unless
  the explicit Fourier error fits the row's finite margin" — and §3's L∞
  dead-margin (`2,090,815.35` bits: a per-mode bound must beat `beta*`, which no
  Weil-scale `L` approaches) together with §1's `nu*` budgets **are** that finite
  margin, quantified at all four deployed rows. No conflict: his theorem lives
  where `exp(o(N))` slack is affordable; the deployed rows are exactly where it is
  not.
- **grande_finale.tex** — the reduction is the finite-row, moment-order-free
  counterpart of the rewritten `prob:entropy-inverse-q` (open structural steps =
  `rem:entropy-inverse-skeleton` 4–6, with 5–6 flagged nonstandard, or the
  Sidon/free-energy alternative; §5), and the finite-side complement of the new
  conditional asymptotic closure (`sec:conditional-asymptotic-closure`,
  `thm:asymptotic-rs-mca-closure-combined`). It consumes `prop:fourier-audit`
  (identity), `prop:q-exact-target` (four-row budget), `def:q-row-atom` /
  `prob:row-sharp-q` (the atom), `prop:sp-pullback` / `thm:coeff-quotient-extract`
  / `def:coefficient-scale` (L2), `prop:mode-null-false` (full-group collapse),
  `prop:vandermonde-kills-low-rank`, `rem:standard-inverse-gap`,
  `rem:mass-aware-logmoment` (masking). All labels verified present verbatim in
  the tex at this base tip (a5b7912).

### One-line verdict
The signed-e_m L¹ input `(STAR)` — the sufficient (per the masked-residual audit,
possibly overstrong) certificate for `prob:row-sharp-q` — is **exactly** a Fourier
participation-ratio / effective-support bound `PR(Rhat) <=
(Krem-1)^2/(Gamma2-1)`; the parent packet's `p^{w/2}` floor is its trivial-support
special case (`1,045,396.58` bits, to the digit) and the L-infinity per-direction
route is separately dead by `2,090,815` bits (now unconditional via the §3 energy
dichotomy); the primitive stratum carries 83–93% of the mass; the binding M31-list
target is an effective support of `~55` out of `2^2090857` directions.
Reformulation + route-cut + proved lemmas + measurements; the bound itself — and
its tighter masked-residual variant `PR(E_Q on P_Q)` — stays `OPEN≡crux`
(structural steps 4–6 of `prob:entropy-inverse-q`).

## 8. Replay
```
python3 experimental/scripts/verify_q_em_inverse_participation_ratio.py
#   RESULT: PASS (54/54 checks), exit 0 (~90 s) -- everything above, self-contained.
```
