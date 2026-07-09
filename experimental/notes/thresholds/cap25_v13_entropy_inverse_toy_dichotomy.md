# CAP25 v13: toy instrumentation of the primitive entropic inverse atom — the L869 Sidon/free-energy dichotomy reads NEITHER at every trade-bearing level (four toys)

Status: `REFERENCE` (§0 — the atom's own trigger, dichotomy sentence, and
mass-aware remark quoted verbatim with line refs; §2 the anchor `(17,16,8,3)`
replay of shipped PR #416/#413 gates, `tau=5286/12870`, `Gamma2=1.13769`,
`PR(E)` raw`->`M_gen `666.52->2519.95`, reproduced by an independent census +
Parseval dual path) / `MEASURED` (§3 the per-level dichotomy verdicts — every
trade-bearing above-random level at every toy is `NEITHER`, triple-checked, with
the BCH-saturation / rank-defect-`0` corroboration; §4 the dense-heavy verdict and
the `M_gen -> ` #416 §7 full-support-delta degeneracy) / `CONVENTION` (§1 every
operationalization pinned: dyadic level, trade base-support rule, exact
finite-population entropies, `fe_slope` and its thresholds) / `SCALING` (§5 the
`Gamma_r` / `rho_max` / `tau` trends in `p`) / `OPEN` (§7 the next-measure list).

**Verifier:** `experimental/scripts/verify_entropy_inverse_toy_dichotomy.py`
(zero-arg, stdlib-only, `RESULT: PASS (234/234 checks)`, exit 0, ~20 s, 139 MB
RSS, `RLIMIT_AS` 2 GB): one self-contained script that **recomputes from
scratch** — fiber census, `Gamma_ell` by **two** code paths (power-sum census
and DFT/Parseval), the Newton power-sum-vs-locator multiset identity, the
signed-trade Vandermonde rank census, and the per-dyadic-level entropy /
free-energy dichotomy — then gates every recomputed number against the four
committed per-toy data JSONs (byte-exact on integers/rationals, `1e-9` on
floats). The full anchor `(17,16,8,3)` and `(13,12,6,2)` are recomputed in full;
`(19,18,9,3)` and `(23,22,11,3)` have their census + dense-heavy decomposition
recomputed (the p=23 `tau=39/2261` and `PR(E_Q)=p^w-1` degeneracy gates). Dual
paths (Newton, Parseval, both entropy paths, both free-energy paths) are explicit
gates, and the run ends with four tamper self-tests (perturb a stored constant,
fake a rank defect, flip a verdict threshold, falsify Parseval).

**What this is / is not.** This is **instrumentation**, consistent with the atom,
**not** a counterexample. It does **not** prove or refute
`prob:entropy-inverse-q`, exhibit a rank-defect, or produce an
entropy-small-doubling object at any scale. It **measures**, at four exact toy
scales `N <= 22`, where the atom's robust Sidon/free-energy proof route stands: it
finds that route's entropy-small-doubling **input is empirically absent** (the
level-typical trades are near-Sidon, so `H(Y-Y') ~ 2H(Y)`), while the same
above-random levels are exactly the popular ones whose `Gamma_ell` contribution
**grows**, so free-energy decay fails there too. The toy popular excess is instead
carried by paid algebraic cells — the atom's alternative **(a)**, exactly the
lift-class structure — which the two-branch test excludes by construction; the
`o(N)` frontier slack exceeds the measured signal at `N <= 22`. Every claim
carries a label.

---

## 0. The atom, its dichotomy sentence, and the mass-aware remark `REFERENCE`

The maintainer's Q1 atom is the standalone additive-combinatorics statement
`prob:entropy-inverse-q` in `experimental/grande_finale.tex` (L827). Its
collision-excess trigger and two alternatives read verbatim (L855–867):

> For every fixed \(\alpha,\kappa,\eta>0\) and \(A<\infty\), with \(\kappa N\le
> R\le\kappa^{-1}N\), if \(\ell=\ell_N\to\infty\), \(\ell\le(\log N)^A\), and
> \[ \Gamma_\ell(\Omega^\circ,\Phi)\ge\exp(\eta N\ell), \]
> then at least one of the following alternatives holds.
> (a) A positive-density restriction of the datum lies in one of the
> bounded-complexity algebraic cells already removed above.
> (b) There is a positive-density set \(U\subseteq T\) for which
> \(\operatorname{rank}_{\K}\Span\{v_t:t\in U\}<\min(|U|,R)\).

The **robust proof route** is the two-branch dichotomy this note instruments
(L869, verbatim):

> The robust proof form may pass through an additional Sidon/free-energy branch:
> either level-typical star trades have entropy-small difference
> \(H(Y-Y')\le H(Y)+o(N)\), leading by entropic BSG/PFR and a slice-derivative
> lemma to the rank-defect alternative above, or else the free-energy decay of
> \(Y-Y'\) bounds that level's contribution to \(\Gamma_\ell\) by
> \(\exp(-\Omega(N\ell))\).

The mass-aware caveat we instrument in §4 is `rem:mass-aware-logmoment`
(L966–968, verbatim):

> After first-match deletion, the primitive residual family may have total mass
> \(\tau<1\) relative to all \(m\)-subsets. Consequently a proof of
> \cref{prob:entropy-inverse-q} may not import a full-mass lower bound such as
> \(\Gamma_r^{\rm prim}\ge1\) unless \(\tau=1\) is separately proved. The finite
> proof route should therefore use an off-diagonal or falling-factorial collision
> moment, prove a dense-heavy-fiber hypothesis before invoking ordinary moments,
> or name sparse-heavy primitive fibers as an explicit residual cell.

The skeleton `rem:entropy-inverse-skeleton` (L962) names the six proof steps; step
two (base-support trades), step three (the Tao cyclic-prime / BCH-Vandermonde
barrier), and step six (the slice-derivative back to `prop:vandermonde-kills-low-rank`,
L876) are the ones with a finite toy shadow, and are what §3 measures.

---

## 1. Conventions — every operationalization pinned `CONVENTION`

The atom is asymptotic in `N`; a finite toy sitting off both branches is an
instrumentation datum about sub-asymptotic scale, not a refutation (§6). To keep
the measurement honest, every choice is fixed here and gated by the verifier.

- **Toy family.** `E=F_p`, `T=mu_n < F_p^*` the order-`n` subgroup, `n=p-1`,
  `omega` a primitive `n`-th root of unity; a subset `S subset Z/n` labels
  `M={omega^e : e in S}`, `|M|=m`. Prefix syndrome `Psi(M)=(sum y, ..., sum y^w)`
  in `E^w` (power sums; `w<p`, so Newton-equivalent to the first `w` locator
  coefficients — **identical fibers**, gated as a dual path). Grid
  `(p,n,m,w) in {(17,16,8,3),(13,12,6,2),(19,18,9,3),(23,22,11,3)}`. Raw family =
  all `C(n,m)` `m`-subsets.
- **`M_gen` mask (#416 branch 7).** Per finite fiber keep only the largest **exact**
  `Z[zeta_n]=Z[x]/Phi_n(x)` lift class; charge the rest to generated-field.
  `tau=|P_Q|/C`. For the 2-power anchor `n=16`, `Phi_16=x^8+1`, so this is #416's
  own `x^{n/2}=-1` key exactly; the generic reducer extends it to `n=12,18,22` via
  the true `Q(zeta_n)` class.
- **Normalized collision moment.** `Gamma_ell = |K|^{R(ell-1)} sum_s N(s)^ell /
  C^ell` with `|K|=p`, `R=w` (`def:primitive-logmoment` normalization), exact via
  `Fraction`; computed by census (path A) and cross-checked against DFT/Parseval
  for `ell=2` (path B).
- **Dyadic level.** With `mean = C/p^w = E[N]`, the ratio `R(s)=N(s)/mean` and the
  level index `j = floor(log2 R(s))` (exact on the rational `R`). Level `j`
  above-random iff `j>=0`. A fiber is **popular** iff `N >= 2*mean` (`j>=1`).
- **Trade extraction (base-support rule).** Process the top `K=64` fibers by `N`
  (ties broken by increasing flat index). In each, the base `M0` is a member of
  the **largest exact lift class**; the star trade of `M` is
  `x(M)-x(M0) in {-1,0,1}^T`, which satisfies the first `w` moment equations
  (`sum_e sgn_e * omega^{e k} = 0`, `k=1..w`; asserted on a sample). `H(Y)` and
  `H(Y-Y')` are base-independent (translation / difference invariance); trade
  counts and support **histograms** are base-fixed by this rule.
- **Entropy estimators.** `Y` is uniform on a level's pooled trade population
  (exact finite population, capped at `P_CAP=1200`, highest-`N` fibers first; no
  sampling). `H(Y)` and `H(Y-Y')` are the **exact finite-population Shannon
  entropies** (bits) of the trade multiset and of the multiset of ordered
  differences `Y-Y'`. `H(Y)` is computed twice — sparse key and dense
  length-`n` signed vector — and asserted equal (`ok_HY`). Relative doubling
  `= (H(Y-Y')-H(Y))/H(Y)`; `>0.5` is the near-Sidon side.
- **Free-energy slope.** Level `j`'s contribution to `Gamma_ell` is
  `contrib_ell = |K|^{R(ell-1)} sum_{s in j} N(s)^ell / C^ell`, over **all**
  occupied fibers in the level, computed two ways (dyadic-fraction `*Gamma_ell`
  and direct sum; asserted equal, `ok_fe_2path`). `fe_slope = mean d/dell
  log2(contrib_ell)` over `ell=2..8`.
- **Branch thresholds.** ENTROPY-SMALL-DOUBLING iff doubling gap
  `H(Y-Y')-H(Y) <= DOUB_C * N` with `DOUB_C=0.10`. FREE-ENERGY-DECAY iff
  `fe_slope <= -DECAY_C * N` with `DECAY_C=0.05`. At the anchor `N=16` these are
  the gap threshold **`1.60`** and the slope threshold **`-0.80`**. The constants
  are arbitrary at toy scale; the verdicts below are robust to any `O(1)` choice
  because the measured gaps and slopes miss both thresholds by wide margins: the
  ES branch fires only at `DOUB_C >~ 0.40` (~4x the `0.10` convention; nearest
  at the anchor, `gap/N = 0.395`), and the FE branch is **sign-robust** — every
  trade-bearing `fe_slope` is positive, so no positive decay threshold fires at
  all.
- **Dense/sparse rule (inherited from #416 §7).** Over prime `F_p` there are no
  proper subfields, so every structured class is an exact `Z[zeta_n]` lift class.
  Per fiber, dominance `rho = largest_class / N`; a fiber is **dense-heavy** iff
  `rho <= 0.5`, else **sparse-heavy**. The #416 §7 falsifier extreme is `rho=1`
  (all mass on one class -> support-delta -> flat spectrum).

---

## 2. Validation — the anchor replays the shipped #416/#413 gates `REFERENCE`

At `(p,N,m,w)=(17,16,8,3)` the independent census reproduces every shipped
number, by fiber enumeration **and** by the Parseval dual path:

| quantity | measured | shipped #416/#413 |
|---|---:|---:|
| `M_gen` retained mass `tau = T_Q/C` | `5286/12870 = 0.41072` | `0.4107` |
| max fiber; `R_true = p^w*maxN/C` | `7`; `2.672183` | `2.672183` |
| `Gamma_2` (census **and** Parseval) | `1.137687` | `1.13769` |
| `PR(E)` raw `->` `M_gen` | `666.52 -> 2519.95` | `666.52 / 2519.95` |
| raw primitive triangle `(T+L1_prim)/C` | `10.472847` | `10.4728` |

The census `N`-multiset is identical under the power-sum and the locator (elementary
symmetric) conventions (Newton, `ok_newton`), and `Gamma_2` agrees between the
direct `sum N^2` and the DFT `L2^2` (`|census - Parseval| < 1e-9`, `parse_relerr
~ 1e-16`). The generic `Phi_n` reducer reproduces #416's 2-power `Cyc(16)` engine
exactly and extends the exact-lift classes to `n=12,18,22`.

---

## 3. FINDING 1 (headline): every trade-bearing above-random level is NEITHER `MEASURED`

Measuring the L869 dichotomy per dyadic level, at **every** toy, **every**
trade-bearing above-random level lands on **neither** branch. Anchor
`(17,16,8,3)`, `N=16`, gap threshold `1.60`, slope threshold `-0.80`:

| level `j` | fibers | trades | `H(Y)` | `H(Y-Y')` | rel-doub | `fe_slope` | ES? | FE? | verdict |
|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|:--|
| `-2` | 560 | — | — | — | — | `-1.389` | — | Y | **FE** |
| `-1` | 1600 | — | — | — | — | `-0.389` | — | N | near-FE |
| `0` | 2712 | 220 | `6.749` | `13.072` | `0.937` | `+0.541` | N | N | **NEITHER** |
| `1` | 9 | 53 | `5.473` | `10.644` | `0.945` | `+1.405` | N | N | **NEITHER** |

The other three toys (trade-bearing levels only; near-FE / FE rows from the
full-spectrum free-energy pass):

| toy | level `j` | fibers | trades | `H(Y)` | `H(Y-Y')` | rel-doub | `fe_slope` | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|:--|
| `(13,12,6,2)` `N=12` | `-1` | 78 | — | — | — | — | `-0.237` | near-FE |
| | `0` | 91 | 380 | `7.052` | `12.874` | `0.826` | `+0.313` | **NEITHER** |
| `(19,18,9,3)` `N=18` | `-2` | 541 | — | — | — | — | `-1.279` | **FE** |
| | `-1` | 3282 | — | — | — | — | `-0.186` | near-FE |
| | `0` | 3030 | 804 | `8.693` | `16.574` | `0.906` | `+0.599` | **NEITHER** |
| `(23,22,11,3)` `N=22` | `-1` | 5214 | — | — | — | — | `-0.095` | near-FE |
| | `0` | 6953 | 1200\* | `9.987` | `19.491` | `0.952` | `+0.105` | **NEITHER** |

\* pooled trade population capped at `P_CAP=1200`. The `(19,18,9,3)` /
`(23,22,11,3)` trade-geometry and dichotomy rows are byte-gated against the
committed data (their census + dense-heavy decomposition are recomputed from
scratch); the `(17,16,8,3)` and `(13,12,6,2)` trade/dichotomy rows are
recomputed in full — see §0.

**Why NEITHER.** The two branches fail for complementary reasons, at the **same**
levels:

- **Entropy-small-doubling has no input.** The trades are near-Sidon: relative
  doubling `(H(Y-Y')-H(Y))/H(Y)` is `0.82`–`0.95` grid-wide, i.e.
  `H(Y-Y') ~ 2H(Y)`, the maximal-doubling / Sidon regime. The gap `H(Y-Y')-H(Y)`
  is `5.2`–`9.5` bits, far above the `<= 0.10*N` threshold (`1.2`–`2.2` bits). No
  entropy-small-doubling population exists to feed BSG/PFR.
- **Free-energy decay fails on the same levels.** These above-random levels are
  the **popular** ones whose `Gamma_ell` contribution **grows**: `fe_slope`
  is `+0.10` to `+1.41` (anchor `+0.541` at `j=0`, `+1.405` at `j=1`), all above
  the `-0.05*N` decay threshold. Free-energy decay fires only on the **deep
  sub-random** level `j=-2` (`fe_slope -1.389` at p=17, `-1.279` at p=19), which
  carries no trades and no excess.

**Triple-check (all gated).** (i) `H(Y)` agrees across two estimators — sparse
trade key vs dense length-`n` signed vector — at every row (`ok_HY`). (ii) The
per-level free-energy contribution agrees across two code paths — dyadic-fraction
`*Gamma_ell` vs direct `sum_{s in j} N^ell`, a factoring identity, exact by
construction — to `<= 1e-6` relative (`ok_fe_2path`). (iii) The verdicts are robust across all four toys and to any
`O(1)` threshold, since every measured gap and slope misses its threshold by a
wide margin.

**Corroboration — the trades provably spread (skeleton steps 2,3,6).** The minimal
trade support **saturates the `2(w+1)` BCH/Vandermonde barrier** exactly, and the
Vandermonde rank defect is `0` everywhere:

| toy | `w` | `2(w+1)` | min trade supp | low-supp (`<=2w`) | `|U|` | vdm rank | rank-defect |
|---|---:|---:|---:|---:|---:|---:|---:|
| `(17,16,8,3)` | 3 | 8 | 8 | 0 | 16 | 16 | **0** |
| `(13,12,6,2)` | 2 | 6 | 6 | 0 | 12 | 12 | **0** |
| `(19,18,9,3)` | 3 | 8 | 8 | 0 | 18 | 18 | **0** |
| `(23,22,11,3)` | 3 | 8 | 8 | 0 | 22 | 22 | **0** |

No trade has support `<= 2w`; the minimum is exactly `2(w+1)`, the BCH bound for a
signed vector killed by the first `w` power sums (`rem:entropy-inverse-skeleton`
step 3, `Tao05`). With the trade supports spanning full-rank Vandermonde columns
(`prop:vandermonde-kills-low-rank`, defect `0`), the trades are forced to spread —
which is exactly why the doubling is high (near-Sidon) and the
entropy-small-doubling branch has no input. The two measurements are the same
phenomenon seen from the entropy side and the algebra side.

---

## 4. FINDING 2: dense-heavy holds; `M_gen` degenerates to the #416 §7 falsifier `MEASURED`

The mass-aware remark's **dense-heavy-fiber hypothesis** HOLDS on the popular /
top fibers at every toy, and strengthens with `p`:

| toy | top-`K` dense-mass frac | `rho_max` (top-`K`) | near-delta (`rho_max>0.9`) |
|---|---:|---:|:--:|
| `(17,16,8,3)` | `0.982` | `1.000` | yes |
| `(13,12,6,2)` | `0.986` | `1.000` | yes |
| `(19,18,9,3)` | `1.000` | `0.077` | no |
| `(23,22,11,3)` | `1.000` | `0.022` | no |

Dense-mass fraction rises `0.90 -> 1.00`; the sparse-heavy `rho=1` cells appear
only at the smallest toys (`p=13,17`, the single all-one-class fiber over
syndrome `0`), and vanish by `p=19` (`rho_max 0.077`) and `p=23` (`0.022`).

**The `M_gen -> ` #416 §7 falsifier linkage (one measurement).** The dense **raw**
fibers force `M_gen` to retain about one support per fiber, so the masked residual
degenerates to #416 §7's full-support-delta falsifier **exactly**. At `p=23`:

- `tau = T_Q/C = 12168/705432 = 39/2261 = 0.01725` (denominator-exact),
- masked `maxN = 2` (one support per fiber, plus a single doubled fiber),
- `PR(E_Q) = 12166 = p^w - 1 = 23^3 - 1` **on the nose**.

A constant-plus-single-delta mask has DFT of constant magnitude off the origin, so
its participation ratio is `p^w - 1` exactly — the #416 §7 "mask that isolates a
full-support delta falsifies the route." This single computation ties
`rem:mass-aware-logmoment` (`tau<1` after first-match deletion) `->` #416 §7
falsifier (`tau -> o(1)` gives the full-support delta) `->` #417's lift-class
refutation (the keep-largest residual is unpayable and sparse-heavy at deployment).
The masked off-diagonal blow-up the remark warns about is visible directly: anchor
`M_gen` `Gamma_8 = 202.5` versus raw `Gamma_8 = 13.1`.

---

## 5. Scaling — the toy regime approaches Fourier-flat `SCALING`

Raw `Gamma_8` flattens toward `1` as `p` grows: `13.14` (p=17), `10.00` (p=19),
`1.245` (p=23) — the `w=o(sqrt p)` Fourier-flat regime of
`thm:fourier-flat-q` / `cor:large-characteristic-fourier-examples` becoming
visible. `tau` collapses with `p` at fixed profile density
(`0.411 -> 0.312 -> 0.142 -> 0.017`), matching #417's monotone `tau`-vs-`w` trend:
coarser fibers, near-injective syndromes, sparse-heavy residual. The top-64 trade
population grows with `p` (level-`j=0` star trades `220, 804, 4631` at
p=`17,19,23`; `380` at p=13, `w=2`) and the doubling stays near-Sidon throughout,
so the NEITHER verdict is stable across the scan. The popular-level `fe_slope`
stays positive across the whole grid (`+0.541, +0.599, +0.105` for `w=3` at
p=`17,19,23`; `+0.313` for p=13), collapsing toward `0` at p=23 as the spectrum
flattens, but never reaching the `-0.05*N` decay threshold on any trade-bearing
level.

---

## 6. Scope — instrumentation, not a counterexample `ANALYSIS`

State carefully. This packet is **instrumentation, consistent with the atom, not a
counterexample.** The toy popular excess is carried by **paid algebraic cells** —
the atom's alternative **(a)**, exactly the lift-class (exactly-`Z[zeta_n]`)
structure — which the robust two-branch test **excludes by construction**, since
alternative (a) is the "already removed" cell. The Sidon/free-energy branch is the
route for the **primitive residual** after those cells are gone; at toy scale the
`o(N)` frontier slack `log|Omega^circ| - R log|K| = o(N)` **exceeds the measured
signal** (`N <= 22`, so `o(N)` is not yet small), and the two-branch test is being
read below the scale where it is asymptotically meaningful. The steering content is
therefore negative and precise: **the robust route's entropy-small-doubling input
is empirically absent at toy scale** (the trades are pseudorandom / near-Sidon, and
the free-energy branch fails on the same popular levels), so any finite structure
must come from **alternative-(a) bookkeeping** (the exact lift-class cells, priced
in #417) **or from regimes the toys do not reach** (`w -> p`, planted subgroup /
AP structure, the higher `ell` where the flat-spectrum limit has not set in). This
does not weaken the asymptotic route, whose input is a genuine `Gamma_r >=
exp(eta n r)` failure that toys at `N <= 22` do not exhibit.

---

## 7. OPEN — next-measure list `OPEN`

Instrumentation targets that would move the measurement, recorded as open:

- **Plant structure to realize the ES branch.** Seed subgroup-coset / AP structure
  into popular fibers and test whether entropy-small-doubling and a Vandermonde
  rank defect (`prop:vandermonde-kills-low-rank`'s negation) can be made to appear
  — the only way to exercise the (b) alternative on a toy.
- **Off-diagonal / falling-factorial collision moments.** The remark's first
  option. De-inflate the `M_gen` off-diagonal blow-up (anchor `Gamma_8 = 202`
  masked vs `13.1` raw) by switching to falling-factorial moments, and test
  whether the dense-heavy hypothesis lets an off-diagonal moment lower bound be
  imported at `tau<1`.
- **Push `w -> p` at fixed `p`.** Exit the Fourier-flat regime: p=23 is already
  near-flat (`Gamma_8 = 1.25` vs `13.1` at p=17). Higher `w` at fixed `p` should
  re-inflate the excess and stress the NEITHER verdict at the boundary of
  `thm:fourier-flat-q`.

---

## 8. Weave — lineage and current v13 PRs `AUDIT`

- **`prob:entropy-inverse-q` (`grande_finale.tex` L827), `rem:entropy-inverse-skeleton`
  (L962), `rem:mass-aware-logmoment` (L966), `prop:vandermonde-kills-low-rank`
  (L876).** The atom, its six-step skeleton, its mass caveat, and the rank
  proposition — the objects this note instruments. Every quote is
  line-provenanced and the labels are gated present in the tex.
- **#417 `cap25_v13_liftclass_cost_model_refuted` (sibling closure).** Prices the
  keep-largest `M_gen` removal and proves it unpayable at deployment
  (`tau -> o(1)`). This packet exhibits, at four toy scales, the **same** residual
  the moment `M_gen` degenerates to the #416 §7 full-support delta
  (`PR(E_Q)=p^w-1`), tying `rem:mass-aware-logmoment -> ` #416 §7 falsifier `-> `
  #417. Uses the identical `(17,16,8,3) tau=0.4107` anchor, gated exact.
- **#416 `cap25_v13_q_eq_masked_participation_ratio` (OPEN).** Source of the
  `M_gen` branch-7 mask, the §7 sparse-heavy falsifier, and the anchor gates
  replayed in §2. Non-correcting: this packet measures where #416's masked object
  sits per dyadic level.
- **#414 `cap25_v13_q_em_inverse_participation_ratio` / #413
  `cap25_v13_signed_em_masked_residual_audit` (integrated `e83962ae`).** The
  masked `PR <= nu*` equivalence and the signed-`E_Q` object; the trade / signed
  `{-1,0,1}^T` residual here is the same masked-residual language, read as an
  entropy population.
- **#412 `cap25_v13_q_pw2_concentration_floor` (integrated).** Route-cut sibling:
  #412 kills the `r=2` second-moment route per stratum; this packet measures the
  higher-`ell` free-energy contributions per level and finds them **growing** on
  the popular levels — same register, complementary (the toy excess is a
  high-`ell` effect, not a second-moment one).
- **Current v13 threshold PRs (BC-L4, LQ-seam, rung-audit families).** Unchanged;
  this packet consumes no upper cell and instantiates no `U(1116048)` certificate.
- **`def:q-row-atom` (L2043), `prob:row-sharp-q` (L2177), `cor:asymp-q-from-entropy-inverse`
  (L888).** The direct finite atom and the asymptotic corollary that
  `prob:entropy-inverse-q` feeds — untouched by this instrumentation.

---

## 9. Nonclaims

- This note does **not** prove or refute `prob:entropy-inverse-q`, nor exhibit a
  positive-density rank defect (alternative (b)), nor produce an
  entropy-small-doubling object at any scale.
- The NEITHER verdict is an **instrumentation datum at sub-asymptotic scale**
  (`N <= 22`, `o(N)` slack not small), **not** evidence against the asymptotic
  dichotomy; §6 states why.
- This note does **not** prove `U(1116048) <= B*`, the KB-MCA first-safe
  agreement, the row-sharp Q atom (`def:q-row-atom`), or any adjacent safe row.
- The dense-heavy verdict and the `M_gen` degeneracy are exact toy enumerations at
  `n <= 22`; they instantiate the deployed-scale behavior #417 proves, but this
  note interpolates nothing between the toys and the deployed row beyond the stated
  monotone trends.
- The branch thresholds `DOUB_C=0.10`, `DECAY_C=0.05` are conventions; the verdicts
  are reported as robust to any `O(1)` choice, not as threshold-free.
