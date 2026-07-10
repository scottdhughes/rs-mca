# Q1 atom: breaking the R=w wall — the first toy firing of alternative (b), and what R>w opens up for prob:entropy-inverse-q

Status:
`REFERENCE` (§0 — the atom, its escape clause, the removal list, alternatives
(a)/(b), the frontier normalization, and `prop:vandermonde-kills-low-rank` quoted
with line refs) /
`CONVENTION` (§1 — the R/w/window/alphabet/normalization mapping table; the
image-normalized (B) and two-field (A) offset guards, all inherited from PR
#420/#422/#430 and pinned) /
`ANALYSIS` (§2 the construction is normalization-valid; §3 the differential-locator
mechanism `rank_K Span{v'_t}=R-1-floor((R-1)/p)` and the char-p Wronskian root
cause; §4 the printed-(b) blindness inherited from #422/#428) /
`PROVED-AT-TOYS` (§2 the moment curve is FULL rank_K at every swept R across five
extension fields and three prime fields, exhaustive; §3 the differential-locator
K-rank defect `1+floor((R-1)/p)` on every swept config; §6 the prime-field
`index=1` immunity, exact) /
`MEASURED` (§2 the extension index/defect R-sweeps; §4 the F_p-span census
occupancy `p^{-defect}`, `Gamma_2>=index*p^{defect}`, and excess; §5 the wall-vs-
break deltas; the #428 anchor cross-check) /
`OPEN` (§7 — what stays walled and what would unlock it).

**Verifier:** `experimental/scripts/verify_atom_toy_r_gt_w.py`
(zero-arg, stdlib-only, self-contained — no lane imports; `RESULT: PASS
(1640/1640 checks)`, exit 0; ~3.5 s and ~17 MB peak RSS **on the authoring box** —
environment-specific, not gated; best-effort `RLIMIT_AS` guard, default 2 GB, tune
or disable via `RGTW_AS_CAP_GB`, never fatal; `RGTW_DATA_DIR` overrides the data
location; `RGTW_DUMP` regenerates the committed JSONs from the run's own
recomputation). One script that **recomputes from scratch** — the finite-field
arithmetic (smallest-irreducible modulus), the moment columns `v_t` and their
formal derivatives `v'_t`, `dim_Fp V_T`, `rank_K`, the index/defect/occupancy, the
fiber census and `Gamma_2`, the `R+1` Vandermonde barrier, the low-support
dependencies, and the (B)/(A) normalization offsets — then gates every committed
number against the two data JSONs (exact on ints/strings/bools, `1e-9` on floats).
Dual path: field multiply table vs log/antilog on `F_27`, `F_32`, `F_125`. Ends
with **seven** tamper self-tests, each threading a corrupted value through a live
`geq`/`feq`/`want_true` gate (a faked moment K-rank defect, a faked
differential-locator formula, a faked occupancy off `p^{-defect}`, a faked
`index=1` at an extension field, a below-barrier moment support, a
non-collapsing differential map, a faked prime-field F_p-span defect).

**What this is / is not.** This packet **breaks the R=w wall** named as OPEN by PR
#421 §11 ("Build a true moment-curve toy with `R>w` so that alternative (b) and the
differential-locator cell become triggerable") and **instruments what opens up**.
It is **instrumentation and toy-exact structural analysis, consistent with the
atom, not a proof or refutation of `prob:entropy-inverse-q`.** It **does not**
produce a row-sharp Q, touch any deployed finite row, or claim the removal list is
complete or incomplete. **Asymptotic-lane only.** The construction's realizability
and the moment-curve full-rank fact are `PROVED-AT-TOYS`; the differential-locator
firing and the F_p-span census are `MEASURED`/`PROVED-AT-TOYS`; the (b)-blindness
and the char-p mechanism are `ANALYSIS`. Every claim carries a label (§8).

Lineage (credit by PR): `#414/#416` (masked/`e_m` participation ratio), `#417`
(lift-class cost model refuted), `#420` (toy dichotomy — the `R=w` wall named),
`#421` (missing-cell hunt — the wall named as OPEN, §11), `#422` (the F_p-span
cell), `#427` (twist span-codimension census), `#428` (the image-structure theorem:
occupancy `p^{-defect}`, `Gamma_2>=index*p^{defect}`, connectivity `Conn_a`), `#429`
(the Krawtchouk connectivity band), `#430` (residual controls: F_7 immunity, the
two-field reading (A)). This packet consumes no upper cell and instantiates no
`U(1116048)` certificate.

---

## 0. The atom, the wall, and alternative (b) `REFERENCE`

The Q1 atom is `prob:entropy-inverse-q` in `experimental/grande_finale.tex` (L827).
Its columns, removal list, normalization, and alternatives read verbatim (L828–867):

> Let \(\K=\K_N\) be a finite field, let \(T=T_N\subseteq\K\) have \(|T|=N\), let
> \(R=R_N\asymp N\) … \(v_t=\rho(t)(1,t,t^2,\ldots,t^{R-1})\in\K^R\) …
> and let \(\Omega^\circ\) be the primitive residual model after quotient
> pullbacks, Chebyshev/dihedral pullbacks, planted common blocks, tangent cells,
> extension cells, **differential-locator low-defect cells**, and saturation cells
> have been removed. Assume the frontier normalization
> \(\log|\Omega^\circ|-R\log|\K|=o(N)\). …
> (a) A positive-density restriction of the datum lies in one of the
> bounded-complexity algebraic cells already removed above.
> (b) There is a positive-density set \(U\subseteq T\) for which
> \(\operatorname{rank}_{\K}\Span\{v_t:t\in U\}<\min(|U|,R)\).

Alternative **(b)** demands a `K`-rank defect. `prop:vandermonde-kills-low-rank`
(L876) discharges it for the moment curve: *"any \(t\le R\) distinct columns are
independent."* Hence for distinct-point moment columns, `rank_K Span{v_t:t in U} =
min(|U|,R)` — **no defect, at any `R`.**

**The R=w wall (PR #420/#421).** In the pure Ψ subset-sum toy the moment depth `R`
is pinned to the deployed window `w` (`def:primitive-logmoment` uses `R=w`;
`def:fourier-flat-prefix-leaf` L896 records `Ψ(M)=(Σy,…,Σy^w)∈E^w`, `w<p`). There
(#421 §9): *"the differential-locator cell is untriggerable at `R=w` … Alternative
(b) is untestable until `R>w`."* This packet builds `R>w` and reports what
becomes testable.

---

## 1. Conventions — the R/w/window/alphabet/normalization mapping `CONVENTION`

Everything is pinned here and gated by the verifier. The toy is the **literal**
atom object over `K=F_{p^k}` with `ρ≡1` (the admissible `c=1` weight, L828), full
moment columns, and `R` swept freely.

**Mapping table (which atom quantity maps to what).**

| atom quantity | symbol | R=w wall (deployed Ψ-toy) | this packet's R>w break |
|---|---|---|---|
| point field / alphabet `K` | `K=F_{p^k}` | prime field `F_p` (`k=1`) | **extension** `F_{p^k}`, `k≥2` |
| base field (two-field reading (A)) | `B`, `|B|=p` | `=K` (`p`) | proper subfield `F_p⊊K` |
| domain | `T⊆K`, `|T|=N` | `μ_n⊂F_p^*` | `firstN`/`μ_d⊂K` (distinct) |
| **window** (deployed prefix depth) | `w` | `w` (rows `0..w-1`, `w≤p`) | `w` (small, `≤p`) |
| **moment depth / rank** | `R=R_N` | `R=w` (pinned) | **`R>w`** (extra rows `w..R-1`) |
| weights | `ρ(t)` | `ρ≡1` | `ρ≡1` |
| normalization | offset | `log|Ω|−R log|K|` | balance `R*`; (A)-reading `−R log p` |

Both `R` and `w` count **moment rows including the head** row `j=0` (`v_t`'s
constant `1`), so `R=w` and the barrier `R+1` are counted consistently with #422
(this differs from #420's head-excluding `w`, noted once). The deployed Ψ records
`w−1` power sums; the break appends rows `j=w,…,R-1`. Two thresholds matter:

- **`R>w`** — the atom's moment object `v_t∈K^R` now genuinely exceeds the window;
  alternative (b) and the differential-locator cell **exist** to test.
- **`R>p`** — the first Frobenius-reducible row `j=p` appears
  (`#red=floor((R-1)/p)`, gated); this is where the char-p structure fires. Since
  the Fourier-flat window has `w≤p`, the order is `w≤p<R`.

**Normalization guards (inherited #422/#430, pinned).** `offset_over_N =
(log₂|Ω| − R log₂ q)/N` (the **(B)** one-field reading) and `offset_A_over_N =
(log₂|Ω| − R log₂ p)/N` (the **(A)** two-field reading, columns in the point field
`E=K`, normalization over the `O(1)` base `B`, `|B|=p`). A break is
normalization-valid at `R` when the relevant offset straddles `0` (`> -0.25`
finite-balance guard). These are finite balance conventions; no finite toy claims
the printed asymptotic `o(N)` clause (gated `printed_oN_clause_claimed` discipline,
as #422/#430).

---

## 2. CONSTRUCTION — R>w is genuinely realized and normalization-valid `PROVED-AT-TOYS` / `MEASURED`

Three routes, all realized on the extension-field moment curve, all
normalization-checked. `Ω={-1,0,1}^T` signed (`p` odd) or `{0,1}^T` unsigned
(`p=2`), exactly `a=⌊N/2⌋` active; `Φ(x)=Σ x_t v_t`.

**Route 2 (extension-field prefix rows) + Route 3 (extra power-sum rows).** Over
`K=F_{p^k}` the moment map `v_t=(1,t,…,t^{R-1})∈K^R` is swept `R=2..7` at `T=firstN`,
`N=14`. The moment columns are **FULL `rank_K` at every `R`** (five extension fields
× six depths, exhaustive — `prop:vandermonde-kills-low-rank`), so the object is
admissible and the sweep is a genuine `R>w` extension of the window. `F16` (`p=2,
k=4`) and `F27` (`p=3,k=3`), verifier-gated:

| field | R | `#red` | `dim_Fp V_T` | flat | `index` | `fp_defect` | `offB/N` | `offA/N` | note |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--|
| F27 | 2 | 0 | 4 | 4 | 9 | 0 | `+0.660` | `+1.112` | |
| **F27** | **3** | 0 | 7 | 7 | **9** | 0 | `+0.320` | `+0.999` | **wall `R=w=3`** |
| **F27** | **4** | 1 | 7 | 7 | **243** | 0 | `-0.020` | `+0.886` | **break, `R>p`, (B)-balance** |
| F27 | 5 | 1 | 9 | 10 | 243 | 1 | `-0.359` | `+0.773` | (A)-valid; `defect=1` |
| F27 | 6 | 1 | 11 | 13 | 243 | **3** | `-0.699` | `+0.660` | (A)-valid; `defect=3` |
| **F16** | **2** | 0 | 5 | 5 | **16** | 0 | `+0.267` | `+0.696` | **wall `R=w=2`** |
| **F16** | **3** | 1 | 5 | 5 | **256** | 0 | `-0.018` | `+0.625` | **break, `R>p`, (B)-balance** |
| F16 | 6 | 2 | 11 | 13 | 4096 | **2** | `-0.875` | `+0.410` | (A)-valid; `defect=2` |

**Route 1 (deeper depth, two-field reading (A)).** Under the (A) reading the
offset is normalized by the `O(1)` base field `|B|=p`, so `R` can go **deep** at
balance. Recomputed here (`F16`, `N=15`, `a=8`, matching #430 M3), verifier-gated:

| R | `#red` | `index` | moment `rank_K` | `offB/N` | `offA/N` | (A)-balance |
|--:|--:|--:|--:|--:|--:|:--:|
| 11 | 5 | `16 777 216` | 11/11 full | `-2.090` | `+0.110` | |
| 12 | 5 | `16 777 216` | 12/12 full | `-2.357` | `+0.043` | ✓ |
| 13 | 6 | **`268 435 456` (`=2^28`)** | 13/13 full | `-2.623` | `-0.023` | ✓ |
| 14 | 6 | `268 435 456` | 14/14 full | `-2.890` | `-0.090` | |

The (A)-offset straddles `0` at `R∈{12,13}` (`+0.043`, `-0.023`) — a factor
`≈k=4` deeper than the (B)-balance at `R∈{2,3}` — where `R≫w`, the moment columns
stay **FULL `rank_K`** (13/13, 14/14), and the span-cell index reaches `2^28`
(reproducing #430 M3's `index=268 435 456` exactly, an independent cross-check of
the field/span machinery). A deep `R>w` break, normalization-valid under (A).

**Verdict — R>w REALIZED.** `PROVED-AT-TOYS` (full `rank_K`, exhaustive) that the
`R>w` moment object is admissible; `MEASURED` that it is normalization-valid at the
(B)-balance shallow break (`F27@R4` `offB/N=-0.020`; `F16@R3` `offB/N=-0.018`, both
inside the `-0.25` guard, both `R>w` and `R>p`) and at the (A)-reading deep break.
**The R=w wall is not a normalization obstruction — R>w is constructible.**

---

## 3. TRIGGERABILITY — the first toy firing of alternative (b) `PROVED-AT-TOYS` / `ANALYSIS`

This is the headline: the differential-locator mechanism, **never triggerable at
`R=w`**, fires cleanly at a toy for the first time.

**The moment curve never fires (b), at any R** (`PROVED-AT-TOYS`, exhaustive).
Across every swept config the moment columns `v_t` have `rank_K=min(N,R)`, defect
`0` — `prop:vandermonde-kills-low-rank` at `R=w` and at every `R>w` alike. Going to
`R>w` makes (b) **testable** (the object exists); the test result for the moment
curve is **still zero defect**. So within admissible moment-curve inputs, (b) is
**unconditionally untriggerable** — sharpening #421 §9 from "untestable" to
"testable and provably-null."

**The differential-locator cell fires (b)** (`MEASURED` firing, `ANALYSIS`
mechanism). The removed "differential-locator low-defect cell" (L839) is the
derivative geometry: replace each column by the formal differential of the moment
curve,

> `v'_t = d/dX (1,X,…,X^{R-1})|_{X=t} = (0, 1, 2t, 3t², …, (R-1)t^{R-2}) ∈ K^R`.

Over char `p` at **distinct** points, `U=T` (density `1`):

> **`rank_K Span{v'_t : t∈U} = R-1-floor((R-1)/p) < R = min(|U|,R)`**, so alternative
> (b)'s `K`-rank defect **FIRES**, with `defect_K = 1+floor((R-1)/p)`.

Verifier-gated on every swept config; representative rows (moment vs derivative):

| field | R | `rank_K(v_t)` | `rank_K(v'_t)` | `defect_K` (`=1+#red`) | min `K`-dep of `v'_t` | moment `R+1` barrier |
|---|--:|--:|--:|--:|--:|--:|
| F16 | 3 | **3** (full) | 1 | **2** | **2** | 4 |
| F16 | 4 | **4** (full) | 2 | **2** | **3** | 5 |
| F16 | 5 | **5** (full) | 2 | **3** | **3** | 6 |
| F27 | 4 | **4** (full) | 2 | **2** | **3** | 5 |
| F27 | 5 | **5** (full) | 3 | **2** | **3** | 6 |

Two parts of the defect: the **trivial** `+1` (the derivative annihilates the head
row, so `Span{v'_t}⊆{s_0=0}`), present at any `R≥2`; and the **char-p low-defect**
`floor((R-1)/p)`, present only past `R>p` — the substantive differential-locator
cell. **Root cause (`ANALYSIS`):** the char-p Wronskian `W(1,X,…,X^{R-1})=∏_{i<R}i!`
vanishes iff `R>p`, the algebraic source of the extra rank drop (`D^p X^{pj}=0`).

**Measured consequences (`MEASURED`, census).** The differential map carries a
`K`-exponential collision excess `Gamma_2 ≥ q^{defect_K}` (vs the F_p-span cell's
weaker `p^{defect}`), and its low-support `K`-dependencies (size `2–3`) sit **far
below** the `R+1` barrier that protects the moment curve — i.e. the differential
cell manufactures exactly the low-support primitive trades that
`rem:entropy-inverse-skeleton` step 3 / BCH removes. Census (F16 unsigned `N=12`,
`a=6`):

| geometry | R | `n_occ` | `Gamma_2` | reading |
|---|--:|--:|--:|--|
| moment `v_t` | 3 | 16 | `256.95` | F_p-span index excess (full `rank_K`) |
| **derivative `v'_t`** | 3 | **1** | **`4096.0`** | **entire slice collapses to one syndrome** (`=q^R`) |
| moment `v_t` | 5 | 254 | `4725.97` | |
| **derivative `v'_t`** | 5 | 16 | **`65780.40`** | `Gamma_2 ≥ q^{defect_K}=4096` |

At `F16@R3` the differential-locator map collapses the **entire** fixed-density
slice onto a **single** syndrome (`n_occ=1`, `Gamma_2=q^R=4096`) — the strongest
possible collision — while the moment curve at the same `(F,R,a)` has `n_occ=16`.

**Trigger verdict.** Alternative (b) is **TRIGGERED** (first toy firing), but only
for the differential (derivative) geometry — which **is** the removed
differential-locator cell (L839), not the moment curve `v_t`. The trigger therefore
lands in alternative **(a)**'s removed-cell branch, exactly as the atom's structure
predicts; it does **not** contradict `prop:vandermonde-kills-low-rank`, it exhibits
the "hypothesis-excluded degeneracy" #422 §4 anticipated. The char-p low-defect,
needing `R>p` (hence `N>p`, hence — for `T⊆K^*` — an extension field), is
unreachable at the deployed prime-field rows (§6).

---

## 4. ALTERNATIVE (b) AT R>w — printed (b) blind; restated (b) carries excess `ANALYSIS` / `MEASURED`

With `R>w` genuinely realized we can finally read the printed alternative (b) as
stated against the F_p-span cell. The verdict is that **printed (b) is structurally
blind at `R>w` exactly as at `R=w`**, while the **prime-field restatement of (b)**
(option 3 of #422 §2.4) is what carries the excess — reproducing and extending
#422/#428 with the `R`-vs-`w` reading and fresh, independently-gated data.

**Printed (b) — `rank_K` defect — stays blind (`ANALYSIS`).** On every F_p-span
census config the moment columns keep **full `rank_K`** (gated `rankK==kfull`) while
the collision excess is real. The excess lives in the `F_p`-span, not the `K`-span;
printed (b) asks for a `K`-rank defect and sees none. `R>w` does not change this.

**Restated (b) — `F_p`-span defect — fires and is measurable (`MEASURED`).** Reusing
the #428 image-structure primitives (audited before reuse; the surjection verifier
reproduces `253/253` here), F16/F27 census across the wall:

| config | wall? | R | `index` | `fp_defect` | `rank_K` | `Conn` | occupancy | `p^{-defect}` | `Gamma_2` | `≥index·p^{defect}`? |
|---|:--:|--:|--:|--:|--:|:--:|--:|--:|--:|:--:|
| F27s | ✓ | 3 | 9 | 0 | 3/3 full | no | `0.9936` | 1 | `10.58` | ✓ |
| F27s | | 4 | 243 | 0 | 4/4 full | no | `0.9936` | 1 | `285.63` | ✓ |
| F27s | | 6 | 243 | **3** | 6/6 full | no | `0.00506` | `0.0370` | `48043.2` | ✓ |
| F16u | ✓ | 2 | 16 | 0 | 2/2 full | yes | `1.0` | 1 | `16.06` | ✓ |
| F16u | | 3 | 256 | 0 | 3/3 full | yes | `1.0` | 1 | `256.95` | ✓ |
| F16u | | 5 | 4096 | 0 | 5/5 full | no | `0.9922` | 1 | `4725.97` | ✓ |

Every row: `rank_K` FULL (printed (b) blind), `Gamma_2 ≥ index·p^{defect}` (#428
Theorem D, unconditional). Where the connectivity hypothesis `Conn_a` holds
(`n_occ=p^{dim D}`), occupancy `= p^{-defect}` exactly (F16u@R2,R3); where it fails
(deep/small-kernel), the containment occupancy `≤ p^{-defect}` still holds (F27s@R6:
`0.00506 ≤ 0.037`) — the `Conn`-load-bearing split of #428/#429, reproduced here as
a live gate. **#428 anchor cross-check** (validates the census machinery):
`S27@R4` occ `1.0`, `G2=243.72≥243`; `U16o@R4` occ `1.0`, `G2=259.78≥256`;
`F64-firstN@R3` occ `0.5`, `defect 1`, `G2=8192.17≥8192` — all matching #428.

**Alternative-(b) verdict.** At `R>w`, **printed (b) as stated remains
structurally blind** (`ANALYSIS`, the excess is an `F_p`-span / differential
phenomenon at full `K`-rank). Low-rank/differential structure **does** carry excess
at `R>w`, but only under the **restatements** the program already has on the table:
the `F_p`-span defect (option 3, occupancy `p^{-defect}`, `MEASURED`) and the
differential-locator `K`-defect (§3, a removed cell, `MEASURED`). Printed (b) sees
neither.

---

## 5. BASELINE DELTAS — what changed crossing the wall `MEASURED`

Matched extension-field controls, `R=w` (wall) vs `R>w` (break):

| quantity | F27 wall `R=3` | F27 break `R=6` | F16 wall `R=2` | F16 break `R=6` |
|---|--:|--:|--:|--:|
| `#red = floor((R-1)/p)` | 0 | 1 | 0 | 2 |
| `index` `[K^R:W_c]` | 9 | 243 | 16 | 4096 |
| `fp_defect` | 0 | **3** | 0 | **2** |
| moment `rank_K` | 3/3 full | 6/6 **full** | 2/2 full | 6/6 **full** |
| min-support barrier `R+1` | 4 | 7 | 3 | 7 |
| differential `defect_K` | 1 (trivial) | **2** (char-p) | 1 (trivial) | **3** (char-p) |

Reading. (i) **Trade support.** The Vandermonde barrier rises `w+1 → R+1` (measured
min slice-support tracks it: `≥ R+1`, equal or `+1`, e.g. F16 `4→6` at `R=3→5`) —
the "min trade support `= R+1`" fact of #422 is the barrier, and it climbs with the
break. (ii) **Excess.** The head-collapse index (`p^{k-1}` signed / `q` unsigned)
is present already at the extension wall (`F27@R3` index `9`, `F16@R2` index `16`);
the **Frobenius** index `q^{#red}` turns on at `R=p+1` (`F27` `9→243`; `F16` `16→256`
at the wall-adjacent break) and the `excess_generic` jumps with it (`F16u` `0.50→
7.50` crossing `R=2→3`; noisy at deep/sparse `R`, as #422 flags). (iii) **Defect
band.** `fp_defect` runs `0` at the wall to `2–3` at the deep break (occupancy
`p^{-defect}` shrinks the image), and the differential `defect_K` runs `1` (trivial)
to `1+floor((R-1)/p)` (char-p). The wall is `defect 0` on both cells; the break is
where structure appears.

---

## 6. Prime-field immunity — the deployed corner stays walled `PROVED-AT-TOYS`

Over a prime field `K=F_p` (the deployed KoalaBear / Mersenne-31 corner), `T⊆F_p^*`
forces `N≤p-1`, so `R≤N<p`: **no Frobenius column ever** (`#red=0`), and the
`F_p`-span **is** the `K`-span. Exhaustively (F5, F7, F13, `R=2..q-1`), gated:

- `index = 1` and `fp_defect = 0` at **every** `R` — the F_p-span cell is
  definitionally absent (extends #430's F_7 immunity control across the whole
  `R`-sweep).
- moment `rank_K` FULL at every `R` — printed (b) null.
- the differential-locator map shows only the **trivial** `defect_K=1` (constant
  kill); the **char-p** low-defect needs `R>p`, unreachable at `N≤p-1<p`.

So the deployed prime-field rows are immune **twice over** — to the `F_p`-span cell
(prime field) and to the char-p differential-locator low-defect (`R<p`). The wall's
practical force survives at deployment; breaking it requires leaving the prime field
(an extension point field, `k≥2`). This is `PROVED-AT-TOYS` (exact finite
enumeration), consistent with the #422/#428/#429/#430 nonclaims.

---

## 7. Scope and obstruction — what stays walled `ANALYSIS` / `OPEN`

- **R>w is constructible; the deployed corner is not.** `R>w` is realized and
  normalization-valid over extension fields (§2), but is **inert over prime fields**
  (§6, index 1 at all R). The atom's `R=R_N≍N` with `T⊆K` prime and `N<p` cannot
  reach `R>p`; the deployed rows sit at `R<p`. So the wall-break is an
  extension-field / large-characteristic-depth phenomenon, not a prime-field one —
  a sharpening of the immunity, not a challenge to it. `OPEN`: whether a
  decoding-layer `u+zv` received-word toy (#421 §11) realizes an `R>w` differential
  defect on a genuinely deployed-shaped datum.
- **Printed (b) is not the operative alternative.** At `R>w` the excess is carried
  by the `F_p`-span defect and the differential-locator `K`-defect; printed (b)
  (`rank_K` on the moment curve) is blind to the former and fires only on the
  removed cell for the latter. Whether the program adopts option 1 (`ρ`/support
  genericity), option 2 (add the cell), or option 3 (restate (b) over `F_p`) is the
  standing #422 §2.4 question, `OPEN`, unmoved in kind by this packet.
- **Connectivity closed-form.** `Conn_a` is load-bearing (§4); a closed-form band
  is #429's OPEN item, untouched here.

---

## 8. Per-claim labels `AUDIT`

- **`PROVED-AT-TOYS`** — the moment curve is FULL `rank_K` at every swept `R`
  (five extension + three prime fields, exhaustive); the differential-locator
  `K`-rank defect equals `1+floor((R-1)/p)` on every swept config; the prime-field
  `index=1`/`fp_defect=0` immunity (exact enumeration, F5/F7/F13).
- **`ANALYSIS`** (complete arguments) — the differential defect formula and its
  char-p Wronskian root cause; the blindness of printed (b) to the `F_p`-span and
  differential cells (full `K`-rank); the containment `Gamma_2≥index·p^{defect}`
  and `occupancy≤p^{-defect}` (inherited #428).
- **`MEASURED`** (exact toy enumeration) — the extension index/defect R-sweeps; the
  F_p-span census occupancy / `Gamma_2` / excess and the `Conn` split; the
  differential-locator collision census (`n_occ`, `Gamma_2`); the wall-vs-break
  deltas; the #428 anchor cross-check.
- **`OPEN`** — the decoding-layer `R>w` realization; the #422 §2.4 ledger choice;
  the closed-form `Conn_a` band.

---

## 9. Weave and nonclaims `AUDIT`

- **`prob:entropy-inverse-q` (L827), escape clause (L828), removal list (L839),
  alternatives (a)/(b) (L862/863), `prop:vandermonde-kills-low-rank` (L876),
  `def:fourier-flat-prefix-leaf` (L896), `def:primitive-logmoment` (L756).** The
  atom and objects this note reads; every quote is line-provenanced and the labels
  are gated present in main.
- **PR #420 / #421 (toy dichotomy / missing-cell hunt).** #420 named the `R=w`
  wall; #421 §9/§11 named it as OPEN and asked exactly for the `R>w` moment-curve
  toy that makes alternative (b) and the differential-locator cell triggerable.
  This packet answers that OPEN item and inherits their `excess`/normalization
  discipline unchanged.
- **PR #422 / #427 / #428 / #429 (F_p-span cell / codim census / image-structure /
  connectivity).** The F_p-span mechanism, `defect`, occupancy `p^{-defect}`,
  `Gamma_2≥index·p^{defect}`, and the `Conn_a` split are inherited and reproduced
  (the #428 anchors `S27`/`U16o`/`F64-firstN` are cross-checked exactly). This
  packet adds the `R`-vs-`w` reading, the differential-locator `K`-rank trigger, and
  the prime-field `R<p` immunity refinement; it never contradicts them.
- **PR #430 (residual controls).** The F_7 prime-field immunity and the two-field
  reading (A) are extended here across the `R`-sweep (§2, §6).
- **PR #414/#416/#417 (participation ratio / lift-class refuted).** The
  coefficient-side structure this note reads is the same masked-residual language.

**Nonclaims.**

- This note does **not** prove or refute `prob:entropy-inverse-q`, does **not**
  resolve `prob:row-sharp-q` / `def:q-row-atom`, and does **not** claim the removal
  list is complete or incomplete — it breaks the `R=w` wall and instruments what
  opens up.
- **No finite claim of any kind:** nothing here certifies a **deployed finite safe
  row**, instantiates **no `U(a_0+1)≤B*` certificate**, and deploys **no finite
  safe row**. The deployed prime-field rows are immune twice over (§6).
  Asymptotic-lane only.
- The differential-locator trigger is a firing of alternative (b) for the **removed
  differential-locator cell** (the derivative geometry `v'_t`), **not** for the
  admissible moment curve `v_t` — it lands in alternative (a), consistent with
  `prop:vandermonde-kills-low-rank`, and validates the removal rather than
  challenging it.
- The window `w`, the `firstN` domain, the (B)/(A) balance guards, and the config
  grid are conventions; the structural facts (full `K`-rank, `defect_K=1+floor
  ((R-1)/p)`, `index=1` at prime fields, `Gamma_2≥index·p^{defect}`) are exact and
  robust to any `O(1)` choice.
