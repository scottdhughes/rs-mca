# Add-back profile decomposition: discharge / scope of gap A6 (`lem:addback`)

Status: `AUDIT` + `PARTIAL` proof. Headline finding: **`OPEN GAP` (materially
narrowed)** — the uncited "profile decomposition" inside
`experimental/asymptotic_rs_mca.tex` `lem:addback` (L246-252) is reduced to a
single named geometric condition, **proved unconditional in the full-mass
single-leaf frontier subregime**, given an explicit **falsifier**, and shown to
reduce (in the mass-carrying regime) to the already-isolated open atom
`prob:entropy-inverse-q` of `grande_finale.tex`. Not `FIXED` (general multi-leaf
case stays conditional); not `COUNTEREXAMPLE_NEW_FLOOR` (the condition is true in
the primary regime; the falsifier only shows it is load-bearing).

Base: `eb42b82` (upstream tip; PR #439 NOT integrated). Related open PRs:
**#435** (`thresholds-asymptotic-proof-audit-r2`, whose attack A6 is this gap's
headline), **#433** (`thresholds-asymptotic-ledger-audit`, joint B3
window-uniformity), **#439** (avdeev, B1 image-normalization; marks `lem:addback`
as an input but does not touch its math).

Verifier: `experimental/scripts/verify_addback_profile_decomposition.py`
(stdlib-only, zero-arg, `RLIMIT_AS` capped). 5 gates + 6 tamper self-tests.

---

## 1. The gap, precisely

`thm:primitive-q` (asymptotic L236-242, unconditional via the Sidon/BSG/quasicube
route) is a **per-leaf** bound at the **leaf's own scale**: for a frontier
primitive leaf (`def:primitive-leaf` L148-157, `\log\bar N=o(N)` with
`\bar N=M/L`, `L=|\operatorname{im}\Phi|`),

```
max_s |F_s|  <=  exp(o(N)) * barN_leaf,   barN_leaf = M/L.        (per-leaf Q)
```

`lem:addback` upgrades this to the **global** bound at the **row scale**

```
max_s N(s)   <=  exp(o(n)) * barN_global,  barN_global = C(n,a_n) |B_n|^{-w_n}.  (global)
```

Its proof (L251) performs the upgrade "by the first-match profile decomposition"
over "the subexponential profile family" — **two objects with no in-paper
definition and no citation**. These paraphrase `grande_finale.tex`
`lem:subexponential-addback-closure` (L2266-2275), which is explicitly a
**hypothesis**: it reads *"Suppose that, in every first-match leaf, the number of
paid quotient/profile cells is `exp(o(n))`, each paid cell contributes at most
`exp(o(n)) barN_n` supports to any prefix syndrome, ..."* and its combined
closure `thm:asymptotic-rs-mca-closure-combined` (L2298) re-supposes them, with
`rem:not-no-input-proof` (L2318) calling the equality *conditional*. So the
compact paper prints as a **proved** `\begin{proof}` lemma what the source
imports as an **assumption**. (This is the A6 = extends-B3 finding of #435.)

### Why the upgrade is nontrivial (`LEMMA`)

Write the global syndrome space `Y`, `|Y|=|B_n|^{w_n}`; leaves `Omega_j`
partition the residual supports; leaf `j` has mass `M_j=|Omega_j|`, image
`L_j=|Phi(Omega_j)| <= |Y|`, fiber counts `N_j(s)`. Then `N(s)=sum_j N_j(s)`
(a genuine partition, so a **sum**), and

```
max_s N(s)  <=  sum_j max_s N_j(s)        (union bound over leaves)
            <=  exp(o(n)) sum_j M_j/L_j   (per-leaf Q).
```

Dividing by `barN_global = (sum_j M_j_total)/|Y|` and writing mass fractions
`p_j = M_j / Mtot`,

```
(sum_j M_j/L_j) / barN_global  =  sum_j p_j (|Y|/L_j)   =  E_{j ~ mass}[ |Y|/L_j ].   (*)
```

`(*)` is the **mass-weighted image-collapse ratio**. It is `exp(o(n))` iff the
leaves carrying the mass have images of near-full density `L_j ~ |Y|`. A leaf
with collapsed image (`L_j << |Y|`) inflates `(*)` by up to `|Y|/L_j =
exp(Omega(n))`. This is the entire content of the "profile decomposition".

---

## 2. The named condition (`def:profile-nondegen`)

> **Profile non-degeneracy.** The closed-ledger primitive residual at `a_n` admits
> a first-match cover by leaves `Omega_j` that (a) partition the residual
> supports, (b) map into the global syndrome space `Y`, (c) have image
> `L_j >= exp(-o(n)) |Y|` (**image non-degeneracy**), and (d) satisfy `thm:primitive-q`
> with a rate uniform in `j`.

**Consumption sites (dependency map).**

```
def:profile-nondegen
   -> lem:addback           (asymptotic L246)   [the gap; now explicit hypothesis]
        -> thm:upper        (asymptotic L262)   "add back by lem:addback"
             -> thm:frontier(asymptotic L289)   safe side of the equality
mirror in grande_finale:
   lem:subexponential-addback-closure (L2266)
        -> thm:asymptotic-rs-mca-closure-combined (L2298)  ["Suppose ... add-back ..."]
```

Every downstream safe-side claim (`thm:upper`, `thm:frontier`, and the
`grande_finale` closure) inherits exactly this condition and nothing more from
the add-back step. #439 already re-labels `thm:frontier` to "assume ... the
add-back profile input in `lem:addback`"; `def:profile-nondegen` names that input.

---

## 3. Results

### Claim R1 — add-back sufficiency (`LEMMA`, PROVED)

*If the primitive residual is profile non-degenerate (`def:profile-nondegen`),
then `max_s N(s) <= exp(o(n)) barN_global`.*

Proof: with `L_j >= exp(-o(n))|Y|`, `M_j/L_j <= exp(o(n)) M_j/|Y|`, so the
union-bound line of section 1 gives

```
max_s N(s) <= exp(o(n)) sum_j M_j/L_j <= exp(o(n)) (sum_j M_j)/|Y|
            = exp(o(n)) M_res/|Y| <= exp(o(n)) barN_global,   M_res <= Mtot.
```

The mass partition `sum_j M_j = M_res` telescopes, so **no separate leaf-count
bound is needed** provided the per-leaf rate is uniform (which is
`def:cells`, "bounded-complexity family", asymptotic L77). This is slightly
cleaner than `grande_finale`, which assumed both `#cells = exp(o(n))` and the
per-cell global-scale bound; here (c)+(d) imply the grande per-cell hypothesis:
`max_s N_j(s) <= exp(o(n)) M_j/L_j <= exp(o(n)) M_j/|Y| <= exp(o(n)) barN_global`.
Gate G2 + G5.

### Claim R2 — unconditional in the full-mass single-leaf frontier subregime (`LEMMA`, PROVED)

*If the primitive residual is a single leaf carrying full mass
(`log(Mtot/M)=o(n)`) in a frontier row (`log barN_global = o(n)`) and the leaf is
frontier (`log(M/L)=o(n)`, the hypothesis `thm:primitive-q` already requires),
then image non-degeneracy `L >= exp(-o(n))|Y|` holds automatically; hence
`lem:addback` is unconditional there.*

Proof (log-arithmetic chain, base e):

```
log L - log|Y| = [log L - log M] + [log M - log Mtot] + [log Mtot - log|Y|]
```

each bracket is `o(n)` (frontier leaf, full mass, frontier row respectively), so
`|log L - log|Y|| <= o(n)`; with `L <= |Y|` this is `L >= exp(-o(n))|Y|`. Gate G4.

Remark (single in-place calibration): the frontier-leaf hypothesis of
`thm:primitive-q` (`log barN_leaf = o(N)`) **already excludes** image collapse in
the full-mass case, because a collapsed leaf has `barN_leaf = M/L` exponentially
large and is not frontier — so the paper's own primitive-Q hypothesis discharges
the add-back exactly when the residual is one full-mass frontier leaf.

### Claim R3 — the residual is the open atom, not a new one (`LEMMA`, PROVED)

*For the mass-carrying part, image non-degeneracy is equivalent to global-scale
primitive Q and hence sits at the same difficulty as the isolated open
`prob:entropy-inverse-q`.*

Proof: image collapse `L < exp(-eta n)|Y|` with full mass gives, in the global
normalization of `def:primitive-logmoment`,

```
M_prim = max_s N^prim(s)/barN >= (M/L)/barN = (M/Mtot)(|Y|/L) >= exp(-o(n)) exp(eta n) = exp(Omega(n)),
```

i.e. a positive-rate collision excess, which by
`thm:logmoment-equivalence` + `prob:entropy-inverse-q` forces a paid cell or a
Vandermonde rank defect; the latter is killed by
`prop:vandermonde-kills-low-rank` (`grande_finale` L876), the former contradicts
"primitive residual". So a full-mass collapsed leaf **cannot** survive first-match
removal *if* `prob:entropy-inverse-q` holds — the same input the Sidon/BSG route
was built to avoid. Net: the compact paper's unconditional `thm:primitive-q`
buys per-leaf/frontier flatness, but closing the add-back to global scale in the
mass-carrying regime re-imports `prob:entropy-inverse-q`-strength.

### Claim R4 — falsifier: image non-degeneracy is load-bearing (`NUMERIC`, exhibited)

*There is a leaf family with per-leaf Q satisfied and global add-back violated by
factor `|Y| = exp(Omega(n))`.*

Witness (Gate G3): `|Y|` leaves, each of mass `barN`, each with `L_j = 1`
(image = one syndrome), **all piled onto the same syndrome `s*`**. Then each leaf
trivially satisfies per-leaf Q (`max_s N_j = barN = M_j/L_j`), but
`N(s*) = sum_j barN = |Y| * barN`, a blow-up of `|Y|` over `barN_global`.
Repair by **spreading** the `L_j=1` images to distinct syndromes restores
`max_s N(s) = O(barN)` — confirming that pile-up (violation of
`def:profile-nondegen`(c)), not per-leaf Q, is the failure. Verified: 64 leaves,
`|Y|=64`, `barN=4` -> piled `max_s N = 256 = 64x`; spread `max_s N = 7 = 1.8x`.

---

## 4. Verdict and repair

- **Verdict:** `OPEN GAP` (materially narrowed). Ranked outcome **3 (AUDIT-scope)
  achieved with a genuine outcome-2 (PARTIAL) component** (R2 unconditional
  subregime). The general multi-leaf / partial-mass case remains conditional on
  `def:profile-nondegen`(c) (image non-degeneracy), which R3 shows is
  `prob:entropy-inverse-q`-hard in the mass-carrying regime and a
  syndrome-coincidence question in the small-mass regime.
- **Falsifier of the naive union-bound closure:** R4 (piled collapsed leaves).
- **TeX repair applied (minimal, #439-compatible):** `asymptotic_rs_mca.tex`
  gains `def:profile-nondegen`; `lem:addback` is restated as conditional on it,
  with the corrected union-bound+telescope proof (R1) and one calibration
  sentence recording the R2 subregime and the `grande_finale` import. No edit to
  the abstract, C9, or `thm:frontier` (those are #439's marking lane).

## 5. Nonclaims

- R1/R2/R3 are proofs of the **reduction/subregime**, not of image
  non-degeneracy in general.
- R4 is a synthetic profile witness; it refutes the *naive union-bound
  add-back*, not the RS-MCA frontier statement. No `COUNTEREXAMPLE_NEW_FLOOR`.
- Not re-audited here: the imported closed-ledger package, BSG/quasicube,
  `thm:primitive-q`'s internal Sidon/BSG steps (all `NO ISSUE` in #435), or the
  C9 image-normalization (#436/#439).
- Numeric gates are finite instantiations of the `exp(o(n))` bookkeeping, not
  proofs of the asymptotics.
