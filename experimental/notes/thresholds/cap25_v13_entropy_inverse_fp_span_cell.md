# CAP25 v13: the F_p-span cell for the primitive entropic inverse atom — a candidate answer to the L828 escape clause, invisible to alternative (b) as printed

Status: `REFERENCE` (§0 — the atom's escape clause, weight freedom, removal list,
frontier normalization, and alternatives (a)/(b) quoted verbatim with line refs) /
`CONVENTION` (§1 — the R-sweep regimes, balance `R*`, the `excess_generic` datum
extending PR #421's `excess_ratio`, the slice / weight definitions, and the
`gamma`-scaling equivalence honesty item, each tex-pinned) / `ANALYSIS` (§2 the
span-cell mechanism: `Phi` extends to an `F_p`-linear map on the ambient `F_p^T`
and the slice is a subset of it, so `image subset V_T`, a containment with a
complete argument; the two coordinate laws, in projective `c`-form, have a
one-line char-`p` proof; containment + Jensen already force `Gamma_2 >= index`;
and alternative (b) as printed is structurally blind to an
`F_p`-span defect at full `rank_K`) / `PROVED-AT-TOYS` (§2 the two laws verified
with zero violations on every slice point in all five projective-class
configs (`ones` + `proj`); `MEASURED` the exact `image = W_c`, `exc_cond`,
span-dim, and index numbers, toy-exact only) / `AUDIT` (§3 the
normalization wellformedness observation, scoped to one clause, framed as an
intended-semantics question with two neutral repairs) / `MEASURED` (§4 the
generic-`rho` null, the min-support Vandermonde barrier, the closed corners, the
support-invisibility, the bounded thin-alphabet residual, the plant-hunt null) /
`OPEN` (§6 next measures).

**Verifier:** `experimental/scripts/verify_entropy_inverse_fp_span_cell.py`
(zero-arg, stdlib-only, self-contained — no lane imports; `RESULT: PASS (197/197
checks)`, exit 0; ~11 s and ~63 MB peak RSS **on the authoring box** — timing and
RSS are environment-specific and deliberately not gated; best-effort `RLIMIT_AS`
guard, default 2 GB, tune or disable via `FP_SPAN_AS_CAP_GB`, never fatal on
platforms that refuse the cap; the data JSONs are resolved relative to the
script's own location — the in-tree `experimental/data/` layout — and
`FP_SPAN_DATA_DIR` overrides for out-of-tree runs). One script that
**recomputes from scratch** — the finite-field arithmetic (smallest-irreducible
modulus), the moment-curve census, the two exact coordinate laws in projective
`c`-form with their Frobenius `free`/`red` split, the red-count identity
`#red = floor((R-1)/p)` behind the sharp trigger criterion, the `image = W_c`
occupancies, the conditional excess on `W_c`, the containment-only Jensen bound
`Gamma_2 >= index`, the `F_p`-span dimension against the `K`-rank, the
baseline-relative `excess_generic`, the frontier-normalization offset table, the
`-Theta(N log N)` tension arithmetic, a generic-`rho` null row and a
large-subgroup row, and the exact Vandermonde min signed-dependency `R+1` — then
gates every recomputed number against the three committed data JSONs (exact on
ints / rationals / strings / bools, `1e-9` on floats). Dual paths: the field
multiply **table vs log/antilog** backend (full `F_27` and `F_16` sweeps), and
`Gamma_2` by **census vs additive-character Parseval**. It ends with seven
tamper self-tests including a **faked `K`-rank defect**, a **faked `F_p`-span
dimension**, and a **`c`-form load-bearing test** (the projective census must
break the `c = 1` laws).

**What this is / is not.** This is a **candidate answer to the atom's own escape
clause** (L828: "or identify the extra obstruction cell that must be added to the
first-match ledger"), plus a **wellformedness observation** on the printed frontier
normalization. It is **not** a proof or refutation of `prob:entropy-inverse-q`,
**not** a claim that the removal list is incomplete as intended, and **not** a
correction demand. **Merge framing: an experimental/audit note on an asymptotic
missing image-span cell plus a normalization repair proposal — no finite
adjacent-row progress is claimed (§7 nonclaims).** The span-cell **containment**
(`image(Phi) subset V_T`) and the
**blindness of alternative (b)** to it are a complete structural argument
(`ANALYSIS`); the **exact** `image = W_c`, the index-only excess, and the span-dims
are exact toy enumerations (`MEASURED` / `PROVED-AT-TOYS`) at six configs `N <= 21`.
The consequence for the ledger is stated as a **three-option question to the
program**, not as a verdict. Conventions are inherited from PR #420/#421 and
extended, never contradicted.

Lineage `#414 -> #416 -> #417 -> #420 -> #421 -> ` this packet. PR #420 measured
the robust Sidon/free-energy branch reads `NEITHER` on the natural `mu_n` family;
PR #421 planted structure against the escape clause and found zero candidates over
the **prime-field, `R=w`** toy, naming two corners it could not reach — the `R>w`
moment-curve reading and the large-subgroup normalization-valid excess. This
packet works the first corner (full moment columns `v_t in K^R`, `R` a free sweep
past `w`, over **extension** fields `K=F_{p^k}`) and closes the second, and there
the escape clause **does** return a candidate: the `F_p`-span cell.

---

## 0. The atom, its escape clause, weight freedom, and alternative (b) `REFERENCE`

The maintainer's Q1 atom is the standalone additive-combinatorics statement
`prob:entropy-inverse-q` in `experimental/grande_finale.tex` (L827). Its opening
sentence is the **escape clause** this packet answers (L828, verbatim):

> Prove the following standalone additive-combinatorics statement, or identify the
> extra obstruction cell that must be added to the first-match ledger.

The **weights are the chooser's** (L828, verbatim) — so every weight in a
projective prime-field class `rho(T) subset c F_p^times` is an admissible
instance, and `rho(t) == 1` (the `c = 1` representative) is the simplest one
that exhibits the cell:

> Let \(\K=\K_N\) be a finite field, let \(T=T_N\subseteq\K\) have \(|T|=N\), let
> \(R=R_N\asymp N\), and choose nonzero weights \(\rho(t)\in\K^\times\).

The **removal list** (L839, verbatim) — the cells `Omega^circ` is taken *after*:

> and let \(\Omega^\circ\subseteq\Omega\) be the primitive residual model after
> quotient pullbacks, Chebyshev/dihedral pullbacks, planted common blocks, tangent
> cells, extension cells, differential-locator low-defect cells, and saturation
> cells have been removed.

The **frontier normalization side condition** (L840–842, verbatim):

> Assume the frontier normalization \[ \log|\Omega^\circ|-R\log|\K|=o(N). \]

The collision trigger `Gamma_ell >= exp(eta N ell)` (L855–857) forces one of two
alternatives (L861–867, verbatim):

> \begin{enumerate}[label=\textup{(\alph*)}]
> \item A positive-density restriction of the datum lies in one of the
> bounded-complexity algebraic cells already removed above.
> \item There is a positive-density set \(U\subseteq T\) for which
> \[ \operatorname{rank}_{\K}\Span\{v_t:t\in U\}<\min(|U|,R). \]
> \end{enumerate}

Alternative **(b)** demands a `rank_K` defect. The proposition that discharges it,
`prop:vandermonde-kills-low-rank` (L876), proves the moment columns are `K`-linearly
independent, so no affine `K`-subspace of rank `o(n)` holds a positive-density
subset. **The observation of this packet is that a positive-density collision
excess can arise with `rank_K` staying full** — the excess lives in the `F_p`-span,
not the `K`-span — so alternative (b) as printed, and `prop:vandermonde-kills-low-rank`
with it, do not see it.

---

## 1. Conventions — regimes, balance, `excess_generic`, weights, `gamma`-scaling `CONVENTION`

Every operationalization is pinned here and gated by the verifier. The toy is the
**literal** atom object over `K=F_{p^k}` (an extension field, so the subfield /
Frobenius structure that was not instantiable in the prime-field Lanes 1–2 toys is
live), with the **full** moment-curve columns and `R` swept past the prefix depth.

- **The datum.** `K=F_{p^k}` with the deterministic modulus (smallest monic
  irreducible; `F_27=F_3[x]/(x^3+2x+1)`, `F_16=F_2[x]/(x^4+x+1)`,
  `F_64=F_2[x]/(x^6+x+1)`, gated by the field self-test). `T subset K`, `|T|=N`,
  `firstN` = the first `N` nonzero elements (or a subgroup `mu_d`). Columns
  `v_t = rho(t)(1,t,...,t^{R-1}) in K^R`. Profile slice `x in {-1,0,1}^T`
  (`signed`) or `{0,1}^T` (`unsigned`, `p=2`), exactly `a` active. `R` a free sweep
  variable (`R < , = , > a`), **not** pinned to `a` — this is the `R>w` break of
  #421's wall.
- **`Gamma_ell` normalization** is the atom's exact one (`= def:primitive-logmoment`):
  `Gamma_ell = |K|^{R(ell-1)} sum_s nu(s)^ell = size^{ell-1} sum_s N(s)^ell / C^ell`,
  `size = q^R`, `C = |Omega|`, exact via integer sums.
- **Balance `R*`.** `R* = log|Omega| / log q` (the `R` at which `log|Omega| - R log q`
  crosses `0`); a config is *at balance* at the integer `R` nearest `R*`. The atom's
  printed side condition is `offset := log|Omega| - R log|K| = o(N)` — an
  asymptotic clause a finite toy can neither satisfy nor falsify, and one §3
  shows is asymptotically incompatible with the one-field reading as printed.
  The toys sit at the **finite balance point** (per-config offsets straddling
  `0`), which realizes the repaired reading's intent (§3); no claim is made that
  the toys satisfy the printed `o(N)` clause itself (`AUDIT` §3, `MEASURED` §2).
- **`excess_generic` (the datum, extending #421's `excess_ratio`).** #421 divided
  `Gamma_2` by the exact multinomial `E[Gamma_2] = p^w/C + (C-1)/C` — a Poisson
  gauge. This packet divides instead by `Gamma_2` of a **generic random linear map
  of the same shape** (`N` uniform nonzero columns in `K^R`, same slice, seeds
  `11,23`): `excess_generic = Gamma_2(moment curve) / Gamma_2(generic map)`. This
  kills **both** Poisson sub-sampling **and** the "the affine image is not uniform
  on `K^R`" confound in one baseline. `excess_generic >> 1` is structure carried by
  the Vandermonde/moment geometry itself; `~ 1` is generic. It is the sharper
  reading of #421's discipline, and it is what isolates the `rho=ones` cell (huge)
  from the generic-`rho` null (`~ 1`).
- **Weights.** `ones` = `rho == 1` (the pure moment curve, `Phi_0 =` signed count);
  `proj` = `rho(t) = c a_t` with `c = g` the field generator (never in `F_p` for
  `k >= 2`, since its order `q-1` exceeds `p-1`) and deterministic
  `a_t in F_p^times` — a genuinely projective representative of the class
  `rho(T) subset c F_p^times`; `twist` = deterministic pseudo-random
  `rho(t) in K^times` (the atom's generic weight). The cell lives exactly on the
  projective classes `c F_p^times` (§2.1); `ones` is the admissible (L828)
  `c = 1` representative, and the `proj` configs verify the class-invariance
  exactly.
- **`gamma`-scaling equivalence (honesty item, `AUDIT`).** Two domains `T` are
  *census-equivalent* when related by `t -> gamma t`, which acts on the syndrome by
  `s_j -> gamma^j s_j` — a bijection of fibers, so identical `Gamma_ell`. The
  builder's first two discriminator `T`'s for the thin-alphabet residual were
  `gamma`-scaling-equivalent (`gamma = 42` over `F_49`), caught, and replaced with
  genuinely inequivalent generic-`T` trials. Recorded so the equivalence class of
  `T`'s is explicit.

---

## 2. THE F_p-SPAN CELL (headline) `ANALYSIS` / `PROVED-AT-TOYS` / `MEASURED`

### 2.1 The mechanism — a complete containment argument `ANALYSIS`

The map `Phi(x) = sum_t x_t v_t` extends to an **`F_p`-linear map on the ambient
`F_p^T`**; the profile slice (`{-1,0,1}^T`, exactly `a` active) is a *subset* of
`F_p^T`, not a subspace, so its `Phi`-image lies inside the image of the ambient
linear map. Hence, for *any* weight `rho`,

> `image(Phi) subset V_T := span_{F_p}{ rho(t) v_t : t in T } subset K^R`

viewed as an `F_p`-space (`ANALYSIS`, complete — the slice image sits inside the
image of the ambient `F_p`-linear map, which is contained in the `F_p`-span of
the columns). The excess is therefore forced by `[K^R : V_T]` whenever `V_T` is
`F_p`-deficient. Two **exact coordinate laws** make it deficient exactly on the
**projective classes** `rho(T) subset c F_p^times`, `c in K^times` — stated for
general `c`, with `rho == 1` the `c = 1` instance (each law a one-line char-`p`
proof, `ANALYSIS`; each verified with zero violations on every slice point in
all five projective-class configs (`ones` + `proj`), `PROVED-AT-TOYS`). Write
`rho(t) = c a_t`, `a_t in F_p^times`:

- **coord-0 collapse:** `s_0 = sum_t x_t rho(t) = c sum_t x_t a_t in c F_p`
  (`= c (a mod p)` for the unsigned slice at `p = 2`, where `a_t == 1`). The head
  lands in a fixed `F_p`-line of `K`.
- **Frobenius law:** `s_{pj} = c^{1-p} s_j^{p}` whenever `pj < R`, because
  `s_j^{p} = (c sum_t x_t a_t t^j)^{p} = c^{p} sum_t x_t a_t t^{pj} = c^{p-1} s_{pj}`
  (Frobenius is additive in char `p`, and `(x_t a_t)^{p} = x_t a_t` for
  `x_t a_t in F_p`). At `c = 1` this is `s_{pj} = Frob(s_j)`. Every
  `t^{pj}`-column is thus an `F_p`-linear image of the `t^j`-column and
  **adds zero new `F_p`-dimensions**. The verifier reports the split as
  `free = {j in [1,R): p nmid j}` and `red = {j: p | j}`.

So `V_T` collapses onto `W_c := {s in K^R : s_0 in c F_p, s_{pj} = c^{1-p} s_j^{p}}
= c W_1` (multiplication by `c` is an `F_p`-linear automorphism of `K^R`), whose
index is `c`-independent: `q^{1+#red} / p^{[s0 free]}` (the head contributes
`q/p` when free in `c F_p` (signed) and `q` when pinned to one residue
(unsigned); each reducible column contributes `q`) — `243`, `256`, `4096` for
the three rows below. Measured `F_p`-span dimensions (verifier-gated):

| config | `p^k` | `R` | `dim_Fp V_T` | ambient `Rk` | `rank_K {v_t}` | `min(N,R)` |
|---|---:|---:|---:|---:|---:|---:|
| F64-firstN, `rho=1` | `2^6` | 3 | **6** | 18 | **3** | 3 |
| S27, `rho=1` (signed) | `3^3` | 4 | **7** | 12 | **4** | 4 |
| U16o, `rho=1` (unsigned) | `2^4` | 4 | **9** | 16 | **4** | 4 |

**The structural point (`ANALYSIS`).** In every row `rank_K {v_t}` is **FULL**
(`3/3`, `4/4`) — `prop:vandermonde-kills-low-rank` holds, the columns are
`K`-independent — while the `F_p`-span is **deficient** (`6<18`, `7<12`, `9<16`).
Alternative (b) as printed asks for a `rank_K` defect (L863:
`rank_K Span{v_t} < min(|U|,R)`); there is none. **The `F_p`-span defect is exactly
the mechanism (b) is structurally blind to.** The cell is a **projective-class
phenomenon**: the `proj` configs (`c = g not in F_p`, deterministic
`a_t in F_p^times`) satisfy the `c`-laws with zero violations and reproduce
**every** census statistic of the `ones` instance exactly (span-dim, index,
`G2`, `exc_cond` bit-identical; verifier-gated) — as they must, since
mul-by-`c` is an `F_p`-automorphism carrying `W_1` to `W_c` and the `a_t`
factors act by slice symmetries. Under a generic `rho` (no single class
`c F_p^times` containing `rho(T)`) the twist scrambles the heads and the
Frobenius alignment, the laws break, and `V_T` fills to the full ambient
(S27 `dim_Fp` `7 -> 12`, verifier-gated).

### 2.2 The image is the subgroup `W_c` exactly at toys, and the excess is the index `MEASURED`

The containment `image subset V_T` is realized as `image = W_c` **exactly** at
the two surjective configs below (`S27`, `U16o`; occupancy `= 1.000`, with the
`proj` twins bit-identical); at `F64` the image is a half-`W` coset (occupancy
`0.5`, `exc_cond = 2`), so the general surjection stays `OPEN` (§2.3) and
`image = W_c` stays a **toy-measured** statement throughout. **The obstruction
does not need it (`ANALYSIS`):** containment alone gives, by Cauchy–Schwarz over
the `<= |W_c|` occupied fibers,
`Gamma_2 = q^R sum_s N(s)^2 / C^2 >= q^R / n_occ >= [K^R : W_c]`, and the
power-mean inequality lifts this to `Gamma_ell >= index^{ell-1}` — the verifier
gates `Gamma_2 >= index` on all five projective-class configs. The exact
`image = W_c` / equal-fiber rows below are **tightness evidence**, not
load-bearing. Conditioning on `W` removes all the excess:

| config | `R` | `law0`/`lawp` viol | `n_occ` | `|W|` = `pred_W` | index `[K^R:W]` | `exc_multi` (uncond.) | `exc_cond` on `W` |
|---|---:|---:|---:|---:|---:|---:|---:|
| S27, `rho=1` | 4 | `0`/`0` | 2187 | **2187** | 243 | 110.29 | **0.99798** |
| U16o, `rho=1` | 4 | `0`/`0` | 256 | **256** | 256 | 23.23 | **0.97610** |
| S27, `rho=twist` | 4 | `268570`/`291136` | 302456 | 2187 | 243 | 0.973 | 0.0088 |

For the signed S27 the head is free so `W = V_T` (`|W| = 3^7 = 2187`); for the
unsigned U16o the head is pinned `s_0 = a mod 2` so `W = V_T / p` (`|W| = 2^9/2 =
256`). In both, `n_occ = |W|` on the nose and `exc_cond ~ 1`: the **raw** Renyi moment
`Gamma_2` sits on the index `[K^R:W]` exactly (`243.72` vs `243`, `259.78` vs
`256`), and the `110x`–`120x` / `23x` figures are that index read against the
`~2` generic/Poisson baseline — the excess is **entirely** the `F_p`-span index,
uniform on `W`. The unconditional `excess_generic` at balance is `120.10` (S27,
`R=4`) — two orders of magnitude of structural excess, all of it the `F_p`-span
index. **Balance guard:** S27 `R=4` sits exactly at the finite balance `R*`
(`offset/N = -0.020` `> -0.25`), so this is **not** the small-family Poisson
trap #421's guard rejects. That is a statement about §1's finite balance
convention, **not** a claim that the toys satisfy the printed asymptotic `o(N)`
normalization — per §3 the printed one-field clause is asymptotically
incompatible as stated, and the toys realize the repaired reading (fixed `q`,
offsets straddling `0`).

### 2.3 The sharp trigger criterion, and the labeling `ANALYSIS`

The trigger arithmetic is the log-index closed form (verifier-gated per config,
with `#red = floor((R-1)/p)` exactly):

> `log index = floor((R-1)/p) log|K| + (head correction)`, head correction
> `in {log q - log p, log q}`,

so `Gamma_ell` is inflated by `index^{ell-1}`, hitting the atom's own trigger
`exp(eta N ell)` (L857) **iff `floor((R-1)/p) log|K| = Omega(N)`** (the head
correction is lower-order once `#red >= 1`). The **bounded-field regime**
(`|K| = O(1)`, `R asymp N`, so `#red = Theta(N)` and `index = exp(Theta(N))`) is
a *sufficient special case, not the sharp condition*: under the one-field repair
(B) of §3 (`R log|K| asymp N`) the index is `exp(Theta(N/p))`, so the cell still
fires at every **bounded characteristic** even with `|K| -> infinity`, and it
dies only when the characteristic outruns the depth — `R - 1 < p` gives
`floor((R-1)/p) = 0`, zero reducible columns, no cell. (The deployed CAP25 v13
rows sit in that dead corner twice over: prime field `K = F_p`, where the
`F_p`-span *is* the `K`-span, and active prefix depth below the large
characteristic — §7 nonclaims.) **Labels.** The containment `image subset V_T`,
the blindness of (b), the `c`-form laws, and the Jensen bound
`Gamma_ell >= index^{ell-1}` are `ANALYSIS` with complete arguments; the laws
are additionally `PROVED-AT-TOYS` (exhaustive zero-violation, `ones` + `proj`);
the exact `image = W_c`, `exc_cond`, span-dims, and index are `MEASURED` at toys
only. The **general surjection** `image = W_c` (that the weight-`a` slice covers
every `s_0`-correct coset of `ker Phi`, i.e. the `p in {2,3}` equal-fibers
claim) is left an **`OPEN` sketch**: the containment is proved, the equality is
only exact-enumerated at toys.

### 2.4 The consequence for the ledger — a question, not a correction `ANALYSIS`

State neutrally. The cell is admissible input to `prob:entropy-inverse-q` (a legal
projective-class weight `rho(T) subset c F_p^times`, at balance, `rank_K` full),
and it is not one of the L839 removals.
The nearest listed cells are the **extension** and **differential-locator
low-defect** cells, but both constrain the *support/locator* side (an
extension-valued slope, or a `rank_K` defect among the columns), whereas the
`F_p`-span cell constrains the *image subspace* at **full** `rank_K` and generic
support (§4: `98`–`100%` support-invisible, matching the `96.5%` random null);
alternative (a) fires only for a cell *already* on the list, and this one is
not. Three
options resolve it, any one sufficient; the choice is the program's:

1. add a **`rho`-genericity hypothesis** to the atom (restrict to weights for which
   `V_T` is `F_p`-full — equivalently, exclude the projective classes
   `rho(T) subset c F_p^times` and any residual `F_p`-deficient weights; the
   twist null of §4 shows generic `rho` already kills the cell); or
2. add the **`F_p`-span cell** to the L839 removal list (a bounded-complexity
   algebraic cell: "positive-density restriction lying in `Phi^{-1}(W_c)` for an
   `F_p`-deficient `V_T`"); or
3. restate alternative **(b) over the prime field** — replace
   `rank_K Span{v_t} < min(|U|,R)` by an `F_p`-span / `F_p`-rank defect, which the
   present column geometry *does* exhibit, so that (b) catches the cell it now
   misses.

Which option is asymptotically forced depends on the sharp criterion of §2.3
(`floor((R-1)/p) log|K| = Omega(N)`): under **either** §3 repair the cell fires
whenever the characteristic stays bounded (reading (A) trivially; reading (B)
with index `exp(Theta(N/p))`), and it is absent when the characteristic outruns
the depth. This packet does not choose among the three; it identifies the cell
and the question.

---

## 3. Normalization wellformedness — one clause, framed as intended-semantics `AUDIT`

A scoped observation on a single printed clause, offered as a question about intended
semantics, not a correction. `T subset K` with `|T| = N` forces `|K| >= N`. With
`R >= kappa N` and `Omega subset {-1,0,1}^T`,

> `log|Omega^circ| - R log|K| <= N log 3 - kappa N log N = -Theta(N log N) != o(N)`,

so the clause "`R asymp N` with `T subset K`" cannot satisfy the frontier
normalization `log|Omega^circ| - R log|K| = o(N)` asymptotically as printed — the
offset is `-omega(N)`, not `o(N)`. The recomputed table (`kappa = 1/4`, gated):

| `N` | `max_norm_over_N` |
|---:|---:|
| 100 | `-0.0527` |
| 1000 | `-0.6283` |
| 10000 | `-1.2040` |
| 100000 | `-1.7796` |

The per-`N` offset **grows** in magnitude (not `o(N)`). The finite toys, by
contrast, sit **on** the balance `R*` with per-config offsets straddling `0`
(`-0.27` S27, `+1.90` S49, `+0.65` U16, `-2.43` U64, `-1.83` S25 bits): extension
fields with `q = p^k` **fixed** realize the feasible reading (`log q = O(1)`, so
`R* = Theta(N)` and `offset(R*) = 0` exactly). Two repairs, stated neutrally:

- **(A) two-field reading.** The single symbol `K` conflates the **point field**
  `E` where the columns live (`|E| >= N`, growing; cf. `def:fourier-flat-prefix-leaf`,
  which has `T subset E`, `Psi(M) in E^w`, *not* in the base field) with an
  `O(1)`-size **base field** `B` in the normalization (bytes). The
  `thm:logmoment-equivalence` analog `log C(n,m) - w log|B| = o(n)` forces `w asymp n`
  only when `log|B| = O(1)`.
- **(B) one-field reading.** Keep one `K` but replace `R asymp N` by
  `R log|K| asymp N`, i.e. `R = Theta(N/log|K|) = o(N)`. Then
  `|Omega^circ| ~ |K|^R = exp(Theta(N)) <= 3^N` is achievable and the printed
  normalization holds; the over-strong clause is `R asymp N`.

**Which reading the span cell needs.** By the sharp criterion of §2.3
(`floor((R-1)/p) log|K| = Omega(N)`), the cell's asymptotic mandatoriness tracks
the **characteristic**, not the reading: under (A) it fires outright
(`log|B| = O(1)`, `R asymp N`); under (B) with `R log|K| asymp N` the index is
`exp(Theta(N/p))` — still trigger-scale for every bounded `p`, and
sub-exponential only if `p -> infinity` along the sequence (e.g. prime `K`,
where the cell is definitionally absent: the `F_p`-span *is* the `K`-span). So
the normalization repair and the span cell remain one question seen from two
sides, with the characteristic as the hinge.

---

## 4. Supporting instrumentation `MEASURED`

- **Generic-`rho` null (finite/toy evidence, not promoted) — no excess survives
  balance in any tested regime.** Dividing by the
  generic-map baseline, the balance-point `excess_generic` under a generic (twist)
  weight is `<= 1.08` across all eight swept regimes (four serialized in the gated JSON: S27t `1.060`, S49t `1.056`, U16
  `0.475`, U64 `0.479`; the sub-`1` values are additive-image effects, not deficits).
  The `rho=1` cell (S27 `120.10`, U16o `88.70`) is the sole structural excess, and it
  is exactly the `F_p`-span index. This is the twin of §2's mechanism seen through the
  sharper baseline: **structure is a weight phenomenon, not a domain one**.
- **Min signed-trade support = the exact Vandermonde barrier `R+1`.** A nonzero
  `{-1,0,1}` combination of the moment columns vanishing needs `>= R+1` support (any
  `R` columns are `K`-independent, `prop:vandermonde-kills-low-rank`), and the measured
  minimum saturates it: `R+1` for `R=3,4,5` and `R+2` at `R=6` (`min_supp` `5,5,6,8`
  vs `vdm_barrier` `4,5,6,7` on S27; `min_signed_dep(F16,R=3) = 4 = R+1`, recomputed).
  This is **sharper** than the `2(w+1)` prefix heuristic of #420/#421 — the full
  moment map has `R` equations, not `w`. Every trade-bearing level reads `NEITHER`
  (`rel_doubling 0.69–0.88`, `fe_slope > 0` everywhere), so #420's dichotomy verdict
  survives the `R>w` reading; the `U64` singleton-fiber configs are `NO-TRADE` at and
  past balance (`maxN = 1`).
- **Differential-locator defect `= 0`.** On every classified support and on synthetic
  `|U| gtrless R` distinct-point sets (F16/F27 at `R in {3,5}`), the `rank_K` defect is
  `0` exactly as `prop:vandermonde-kills-low-rank` guarantees; only
  hypothesis-excluded degeneracies would trigger it. The verifier recomputes four
  synthetic cases (defect `0`).
- **Large-subgroup corner (#421 residual) CLOSED.** Keeping a small-index subgroup
  `mu_d` exponentially large at balance, the retained excess vs the paired `firstN`
  control (both generic-`rho`) is `0.60x` (`mu_21 subset F_64`), `1.07x`
  (`mu_13 subset F_27`), `0.92x` (`mu_16 subset F_49`) — none. The one corner #421
  could not reach holds no genuine missing cell beyond the span cell.
- **The `rho=1` excess is support-invisible.** Classifying the `rho=1` popular
  supports, `98–100%` are `NOT-CAUGHT` (S27 `0.980`, S49 `1.000`), matching the
  `96.5%` random-support null — the excess is **not** in the support geometry (it is
  in the `F_p`-coefficient structure of `Phi`). The lone `U64` trace-cell hit
  (`ext:trace = 1.0`) is exposed as **domain-vacuous** by the null, which hits
  `ext:trace = 1.0` too (the whole domain sits in the trace cell).
- **Thin-alphabet residual BOUNDED.** The residual-above-`W` conditional excess has an
  intrinsic floor `~1.44` at balance; the `N`-sweep is `1.05 -> 1.16 -> 1.40 -> 1.44
  -> 1.37` (`N = 8..16`), peaking near balance and **falling** past it — not an
  `exp(eta N)` mechanism.
- **Plant hunt on the new cells.** Subfield-block, Frobenius-block/union,
  trace-balanced, a `mu_5`-coset positive control, and a random negative control yield
  `0` candidate cells beyond the span cell (each either caught or normalization-killed).

---

## 5. Guards and verification `AUDIT`

The verifier PASSES **197/197** checks (~11 s, ~63 MB peak RSS **on the
authoring box** — both environment-specific, neither gated), recomputing from
scratch and gating against the committed data. Reproducibility knobs for
out-of-tree audits: the `RLIMIT_AS` guard is best-effort (default 2 GB;
`FP_SPAN_AS_CAP_GB` tunes or disables it; never fatal on platforms that refuse
the cap), and `FP_SPAN_DATA_DIR` overrides the data location (default:
`experimental/data/` resolved relative to the script itself). Dual-path and
tamper guards:

- **Field multiply dual path.** The table multiply equals the log/antilog backend on
  the full `F_27` and `F_16` product tables (`0` mismatch).
- **Parseval dual path.** `Gamma_2` by census equals `Gamma_2` by additive-character
  Parseval on a small `F_9` moment census (`< 1e-7`).
- **Seven tamper self-tests** (each must be caught): a **faked `K`-rank defect** (distinct
  `<= R` columns are always independent, defect `0`); a **faked `F_p`-span dimension**
  (`p^{dim-1} != V_T`); the laws holding for `ones` and breaking for `twist`; the exact
  `image = W` (off-by-one would miss the census); a Parseval falsification (corrupt one
  fiber count); the conditional-excess guard (`exc_cond ~ 1` while `exc_multi >
  100`, so the claim is the index and not raw over-counting); and the **`c`-form
  load-bearing test** (the projective census must break the `c = 1` laws — its
  heads land in `c F_p`, not `F_p`).

---

## 6. OPEN — next-measure list `OPEN`

- **`q = 121 / 125` residual replication.** Replicate the thin-alphabet bounded floor
  at a third prime `p` to confirm the `~1.44` peak is intrinsic, not a `p in {2,3,7}`
  coincidence.
- **Full-alphabet `p = 7` control.** Push `T = F_7` (full prime field, not a subset)
  to check the coord-0 collapse against the large-characteristic Fourier-flat regime
  of `cor:large-characteristic-fourier-examples`.
- **Twist span-codimension census.** Measure `codim_{F_p} V_T` as a function of the
  twist entropy of `rho` — quantify how much genericity a `rho`-genericity hypothesis
  (option 1) would need to demand.
- **The `p in {2,3}` equal-fibers surjection.** Complete (or refute) the general
  `image = W_c` surjection so the `MEASURED` exact-equality becomes a theorem, not a toy
  enumeration.
- **Two-field-reading confirmation.** Instantiate the point-field `E` vs base-field
  `B` split of repair (A) directly (columns over `E >= N`, normalization over
  `|B| = O(1)`) and check the span cell's index there.

---

## 7. Weave and nonclaims `AUDIT`

- **`prob:entropy-inverse-q` (L827), escape clause (L828), weight freedom (L828),
  removal list (L839), frontier normalization (L840), alternatives (a)/(b) (L861–867),
  `prop:vandermonde-kills-low-rank` (L876), `def:fourier-flat-prefix-leaf` (L896),
  `thm:logmoment-equivalence`.** The atom and the objects this note reads; every quote
  is line-provenanced and the labels are gated present in the tex.
- **PR #421 `cap25_v13_entropy_inverse_missing_cell_hunt` (sibling, direct predecessor).**
  Found zero candidates over the prime-field, `R=w` toy and named the `R>w` and
  large-subgroup corners as residual. This packet works `R>w` over extension fields and
  finds the span cell there, and closes the large-subgroup corner. It **extends** #421's
  `excess_ratio` discipline (to `excess_generic`) and never contradicts it.
- **PR #420 `cap25_v13_entropy_inverse_toy_dichotomy`.** The `NEITHER` dichotomy on the
  natural family, which §4 confirms survives the `R>w` moment-curve reading (min support
  `= R+1`, `rel_doubling 0.69–0.88`, `fe_slope > 0`).
- **#417 / #416 (lift-class / masked-participation).** The `rho=1` support-invisibility
  (§4) is the coefficient-side complement of #417's support-side refutation.
- **The #422 review (DannyExperiments, 2026-07-08, on this PR).** The projective
  `c`-form of the laws (§2.1), the sharp `floor((R-1)/p) log|K| = Omega(N)`
  trigger criterion replacing the bounded-field sufficient condition (§2.3), and
  the containment+Jensen route that frees the obstruction from the `image = W_c`
  surjection (§2.2) were adopted from that review's repair list; the §1/§2.2/§3
  normalization demotions, the `MEASURED`-only labeling of `image = W_c` and the
  generic-`rho` nulls, and the §5 packaging knobs likewise. The review
  independently confirms the mechanism and the (b)-blindness, and concurs that
  the deployed finite rows are unaffected.
- **This packet consumes no upper cell and instantiates no `U(1116048)` certificate.**

**Nonclaims.**

- This note does **not** prove or refute `prob:entropy-inverse-q`, and does **not**
  claim the removal list is incomplete as intended — it identifies an admissible input
  (the projective class `c F_p^times`, at balance, `rank_K` full) not on the L839
  list and asks how the program wants it resolved.
- **No finite claim of any kind:** nothing here proves anything about
  `prob:row-sharp-q` / `def:q-row-atom`, certifies **no deployed finite safe
  row**, and instantiates **no `U(a_0+1) <= B*` certificate** at any deployed
  row. The deployed KoalaBear / Mersenne-31 rows are outside the mechanism twice
  over: they are prime-field (`K = F_p`, where the `F_p`-span *is* the `K`-span,
  so the cell is definitionally absent) and their active prefix depth sits below
  the large characteristic (`R - 1 < p`, so `floor((R-1)/p) = 0` — zero
  reducible columns). This packet is asymptotic-lane only.
- The span-cell **containment** (`image subset V_T`), the **blindness of (b)**, and
  the containment+Jensen bound `Gamma_ell >= index^{ell-1}` are complete
  arguments (`ANALYSIS`); the **exact** `image = W_c`, the equal fibers, and
  the span-dims are exact toy enumerations at the five projective-class
  configs `N <= 21` (`MEASURED` / `PROVED-AT-TOYS`), promoted by no theorem here.
  The **general** `image = W_c` surjection (the `p in {2,3}` equal-fibers claim)
  is an `OPEN` sketch.
- The normalization observation (§3) is scoped to one clause and framed as an
  intended-semantics question with two neutral repairs; it is **not** a correction
  demand, and both repairs keep the rest of the atom intact.
- `excess_generic`, the balance `R*`, `norm_ok` at `offset/N > -0.25`, and the
  regime grid are conventions; the cell is reported as robust to any `O(1)` choice,
  since `exc_cond ~ 1` and the index is exact.
