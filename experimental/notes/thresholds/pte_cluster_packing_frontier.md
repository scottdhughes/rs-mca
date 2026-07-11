# The PTE-cluster packing frontier (image-normalized R=2)

## Status

`R1 PROBLEM FORMALIZED + AFFINE-INVARIANCE PROVED / R2 CENSUS EXTENDED
(COMPUTED) / R3 OPTIMIZER STRUCTURE MEASURED / R4 FINITE-b CAP IMPROVED
(PROVED) + FRONTIER-REDUCTION rho*<=phi* PROVED + CHAMPION IMPROVED
0.1317->0.1567 (PROVED family) / R5 HONEST BRACKET [0.1567, log2], sup OPEN`.

This packet consumes our open PR #623 (`pte_extremality_image_face.md`, HEAD
`c2027dc`) at its **named wall** — the `(fstar, L1)` PTE-cluster packing
frontier — and pushes it. One-line verdict: **the extremal rate is governed by
the max-fiber rate `phi* = sup (log fstar)/b` (proved: `rho <= phi`, and `rho`
sits within the small deficit rate `gamma` of `phi`); #623's champion `0.1317`
and its claimed "plateau ~0.14" are both superseded — a symmetric wide-diameter
interval-with-holes block at `b=14` reaches `rho = 0.156659` (PROVED infinite
family via tensoring), `phi(b)` climbs monotonically with no plateau through
`b=16`, and the true `sup rho` (equivalently `phi*`, the max exponential fiber
rate of the degree-2 moment map) remains the honest open wall, bracketed
`[0.156659, log 2 = 0.6931]`.**

Every number is recomputed by
`experimental/scripts/verify_pte_cluster_packing.py` (stdlib-only, zero-arg,
`RESULT: PASS`, runtime well under 5 min under `ulimit -v 2097152`). The heavy
searches that *find* the champions live in
`experimental/scripts/repro_pte_cluster_census.py` (documented runtime); the
verifier *re-checks* the reported blocks exactly and re-runs only the small
certified censuses.

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exhaustive
exact enumeration), **MEASURED** (exact finite objects, trend/limit read off but
not proved), **REFUTED**, **AUDIT** (cross-reference), **OPEN**.

**Credit.** Built directly on **our #623** (`pte_extremality_image_face.md`,
consumed at `c2027dc`: the `R=2` image face, the product/tensor rate machinery,
PTE-universality, the `(fstar,L1)` wall) and **scottdhughes #564**
(`w_a_star_pte_lemma.md`: the canonical star-PTE trade lemma / minimal support 6,
used in Lemma B). The `R=2` razor and image normalization trace to **Codex #615**
/ **LegaSage #585** / **holmbuar #614** via #623. **Codex's TEAM_BOARD
2026-07-11 12:42Z ledger line** (`F_17`, `V={1,2,3,4,5,6,7,8,10,16}`, fiber
`4^k`, normalized excess `(289/256)^k`) was tested here and is recorded in R6 as
a *different (span/ambient) normalization* that does not port to the
image-normalized rate. The AMBIENT/SIGNED `(LS)` corner is scottdhughes's and is
out of scope.

---

## R1 — the exact packing problem (PROVED / AUDIT extraction from #623)

**Setup (verbatim from #623's census, restated standalone).** A **block** is a
set `V` of `b` distinct integers (carried to a prime field via #615's no-carry
`Q^i` spacing, so per-block signatures are recovered). For a subset `S ⊆ V` its
**signature** is the pair of the first two power sums together with the
cardinality,
```
    sig(S) = ( w, s, q ) = ( |S|, sum_{x in S} x, sum_{x in S} x^2 ).
```
Fibers of `Phi = (sum, sum^2)` are taken **at fixed cardinality**, so `sig` is
the fiber label. Define
```
    fstar(V) = max_{w,s,q}  #{ S ⊆ V : sig(S) = (w,s,q) }     (the max fiber),
    L1(V)    = #{ distinct sig(S) : S ⊆ V }  = 2^b - c        (image size),
```
where `c = 2^b - L1` is the **collision deficit**. The **image-normalized
per-point rate** (the tensor limit; see R4 Prop E) is, for symmetric `V`,
```
    rho(V) = (1/b) log( fstar * L1 / 2^b ) = phi(V) + lambda(V) - log 2 ,
    phi(V) = (log fstar)/b ,   lambda(V) = (log L1)/b .
```
Tensoring `V` `k` times (no-carry) realizes `rho(V)` in the limit `k -> inf`.

> **The PTE-cluster packing problem.** Maximize `rho(V)` over all blocks `V`,
> i.e. compute `rho* = sup_b max_{|V|=b} rho(V)` and describe the optimizers.
> Equivalently maximize the per-point objective `G(V) = (fstar*L1)^{1/b} = 2 e^{rho}`.

Baselines recovered exactly (verifier BLOCK 0): 2-point Prouhet
`V={0,1,2,4,5,6}` gives `fstar=2, L1=63, rho = log(63/32)/6 = 0.112900`; #623's
census champion `V={0..13}\{4,9}` gives `fstar=6, L1=3315, rho = 0.131684`.

### Affine invariance (PROVED, verifier BLOCK 1) — new structural reduction

> **Lemma A.** For any invertible affine map `psi(x) = a x + b` (`a != 0`) over
> the rationals (or a field of char `> 2`), `fstar`, `L1`, `c`, and `rho` are
> unchanged: `fstar(psi V) = fstar(V)`, `L1(psi V) = L1(V)`.

*Proof.* At fixed weight `w`, `sum psi(x) = a·sum x + b w` and
`sum psi(x)^2 = a^2·sum x^2 + 2ab·sum x + b^2 w`. For fixed `w` the map
`(sum, sum^2) -> (a·sum + bw, a^2 sum^2 + 2ab sum + b^2 w)` is affine with
Jacobian `a·a^2 = a^3 != 0`, hence a bijection of the signature plane. So two
`w`-subsets collide on `V` iff they collide on `psi V`; `mu(w)` and `D_w` are
preserved weight-by-weight, and `fstar = max_w mu(w)`, `L1 = sum_w D_w` follow. ∎

Consequence: the packing problem lives on **affine-equivalence classes** of
blocks. Canonical form: translate `min V = 0`, divide by `gcd`, take the
lexicographically smaller of `V` and its reflection `max V - V`. This is the
search reduction used throughout, and it explains why absolute coordinates are
irrelevant — only the **combinatorial spacing type** matters (spreading points
apart is *not* an affine symmetry and *does* change `rho`; see R2).

---

## R2 — census extension (COMPUTED)

Two frontiers, both honest about their scope. `rho(V)` is the exact tensor rate
for **symmetric** `V` (R4 Prop E); the optimizers found are symmetric, so all
reported `rho` are genuine rates (verifier re-derives each block's `(fstar,L1)`
exactly and re-validates the champion by finite-`k` tensor).

### (a) Diameter-bounded exhaustive optimum (COMPUTED, certified)

Exhaustive over all affine-canonical blocks of bounded diameter (`b + 4` for
`b<=8`, `b + 3` for `9<=b<=12`, `b + 2` for `b=13,14`; exact per-`b` box in the
repro `exh` stage). Recomputed in verifier BLOCK 2 for `b in {6,9,10,11}`;
`b=12..14` in the repro script.

| b | OPT rho (diam-bounded) | fstar | L1 | optimizer V |
|---|-----------------------:|------:|----|-------------|
| 6  | 0.112900 | 2 | 63   | {0,1,2,4,5,6} |
| 9  | 0.117188 | 3 | 490  | {0,1,2,3,5,6,7,11,12} |
| 12 | 0.131684 | 6 | 3315 | {0..13}\{4,9}  (= #623 champion) |
| 14 | 0.150163 | 12| 11175| {0..16}\{2,8,14} |

### (b) Best known over wider diameter (COMPUTED lower bounds; symmetric search)

Widening the diameter strictly beats the tight-box optima — the tight box was a
#623 artifact. Symmetric interval-with-holes search (repro script; verifier
recomputes each listed block exactly, BLOCK 2/3):

| b | best rho (wide) | fstar | L1 | optimizer (deletions from {0..n-1}) |
|---|----------------:|------:|----|-------------------------------------|
| 12 | 0.140863 | 6  | 3701  | {0..20}\{1,3,8,9,10,11,12,17,19} |
| 13 | 0.139291 | 8  | 6262  | {0..16}\{1,7,9,15} |
| **14** | **0.156659** | 12 | 12239 | {0..22}\{1,6,7,10,11,12,15,16,21} |
| 15 | 0.144539 | 13 | 22034 | {0..22}\{2,3,4,5,17,18,19,20} |
| 16 | 0.148886 | 18 | 39425 | {0..22}\{2,3,4,11,18,19,20} |

The **`b=14` block `V = {0,2,3,4,5,8,9,13,14,17,18,19,20,22}`** (symmetric about
`11`, `fstar=12` at central weight `7`, `L1=12239`) is the **overall champion:
`rho = 0.156659`**, validated by exact finite-`k` tensor
`rho_k = 0.150228, 0.154001, 0.154981` for `k=1,2,3` (`MF_k = 12^k`, increasing
to `0.156659`; verifier BLOCK 3). Two *clean nameable* near-champions:
`{0..16}\{2,8,14}` (`rho=0.150163`, deletions in AP step 6) and
`{0..18}\{1,4,9,14,17}` (`rho=0.151643`).

**Verdict (COMPUTED, corrects #623).** #623 reported the structured family
"plateaus at `rho ~ 0.14`" and asserted `rho*` is "not climbing." Both are
**REFUTED as numerical claims**: the best rate climbs to `0.156659 > 0.14`, and
(R4) `phi(b)` rises monotonically through `b=16`. The weaker true statement —
`rho*` is a finite constant `<= log 2` — survives and is the open wall (R5).

### Pareto frontier in `(phi, lambda)` (COMPUTED, verifier BLOCK 2/5)

Champions trace a curve of *increasing* `phi` and *slowly decreasing* `lambda`;
the deficit rate `gamma = log2 - lambda` stays small, so `rho ~ phi`:

| b | phi = log fstar / b | lambda = log L1 / b | rho | gamma (deficit) |
|---|--------------------:|--------------------:|-----|-----------------|
| 6  | 0.1155 | 0.6905 | 0.112900 | 0.0026 |
| 9  | 0.1221 | 0.6883 | 0.117188 | 0.0049 |
| 12 | 0.1493 | 0.6755 | 0.131684 | 0.0176 |
| 14 | 0.1775 | 0.6723 | 0.156659 | 0.0208 |

---

## R3 — structure of optimizers (MEASURED + conjecture)

Measured across (a) and (b):

1. **Optimizers are affine-symmetric** (invariant under `x -> max V - x`). All
   listed champions are symmetric; `fstar` is attained at the **central weight
   `w = b/2`** (`mu` is a symmetric, unimodal profile — e.g. the `b=14` champion
   has `mu = [1,1,1,2,4,5,6,12,6,5,4,2,1,1,1]`). MEASURED.
2. **They are dense "interval-with-symmetric-holes"**, *not* the tight
   complement-of-2 blocks #623 highlighted. #623's `{0..13}\{4,9}` is the
   *diameter-`<=15`* optimum only; over wider diameter the `b=12` optimum is a
   9-hole block at diameter 20 (`rho=0.1409`). The number of holes and the
   diameter of the optimizer **grow with `b`** (no fixed deleted-set pattern
   stabilizes) — REFUTES "complement-of-few is optimal at every `b`" and the
   "stable deleted-set pattern" reading of #623's R3.
3. **Conjecture (MEASURED).** The rate-maximizer at each `b` is an indecomposable
   symmetric cluster (not a product of small trades), consistent with #623's
   "indecomposable near-AP cluster" stability read; here it is confirmed to be
   the *global* structure, not just near-extremal.

No symmetrization proof is claimed (symmetrizing a block need not preserve
`fstar*L1`), so optimizer-symmetry is MEASURED, not PROVED.

---

## R4 — bounds (PROVED lemmas; asymptotic cap OPEN)

### 4.1 Trade-deficit lemma (PROVED, verifier BLOCK 4)

> **Lemma B.** If `V` contains a degree-2 PTE trade of support `2r` (disjoint
> `P,Q ⊆ V`, `|P|=|Q|=r`, `sum P = sum Q`, `sum P^2 = sum Q^2`), then the
> collision deficit obeys `c = 2^b - L1 >= 2^{b-2r}`. Since the minimal degree-2
> trade has support 6 (hughes #564), any block with `fstar >= 2` has
> `c >= 2^{b - 2 r_min}` for its smallest trade support `2 r_min in [6, b]`.

*Proof.* Let `U = P ∪ Q`, `|U| = 2r`. For each `C' ⊆ V∖U` (there are `2^{b-2r}`),
the subsets `C'∪P` and `C'∪Q` are **distinct** (their `U`-parts are `P != Q`)
and share `(weight, sum, sum^2)` because `(P,Q)` is a trade. Among the
`2·2^{b-2r}` subsets `{C'∪P, C'∪Q : C'}`, each `C'∪Q` duplicates the signature
of `C'∪P`, so they occupy at most `2^{b-2r}` distinct signatures. The
multiplicity excess of this subfamily is therefore `>= 2·2^{b-2r} - 2^{b-2r} =
2^{b-2r}`, and since `c = sum_s (f_s - 1)` counts excess over all subsets
(`f_s >=` subfamily count at `s`), `c >= 2^{b-2r}`. ∎

This **quantifies why dense blocks are collision-rich** (a small-support trade
forces a *constant fraction* `2^{-2r}` of `2^b` into collisions), but note the
bound is `2^{b-2r}` with `r >= 3` fixed, so `(1/b) log(1 - 2^{-2r}) -> 0` and
**Lemma B does not move the asymptotic rate** — it sharpens the deficit, not the
exponent (verifier confirms `c >= 2^{b-2 r_min}` on every sample).

### 4.2 Codimension cap (PROVED, verifier BLOCK 4) — finite-b improvement

> **Lemma C.** `fstar(V) <= 2^{b-3}` for every block with `b >= 3`.

*Proof.* A max fiber lies in `{ x in {0,1}^b : 1·x = w, v·x = s, v^2·x = q }`.
The three functionals `1, v, v^2` are linearly independent (Vandermonde on any 3
distinct `v_i`), so this is a codimension-3 affine slice of the cube. Picking 3
coordinates whose `3x3` minor is invertible, those coordinates are affine
functions of the other `b-3`; each of the `2^{b-3}` free settings forces the 3
dependent coordinates to fixed reals, so at most `2^{b-3}` lie in `{0,1}^b`. ∎

With `L1 <= 2^b` this gives
```
    rho(V) <= (1/b) log( 2^{b-3} * 2^b / 2^b ) = (1 - 3/b) log 2 ,
```
**strictly tighter than #623's `(1 - 2/b) log 2`** at every finite `b` (`b=14`:
`0.5446` vs `0.5941`; combining with `fstar + L1 <= 2^b + 1` gives the marginally
better `(1-6/b)log2 + (log 7)/b = 0.535`). **Both still `-> log 2` asymptotically**
— the linear-algebra cap cannot beat `log 2` (only 3 moment constraints; the
improvement would need an arithmetic anticoncentration bound on the max fiber,
which resists — see 4.4).

### 4.3 Frontier reduction `rho* <= phi*` (PROVED, verifier BLOCK 4)

> **Proposition D.** `rho(V) <= phi(V) = (log fstar)/b`, with gap exactly the
> deficit rate `gamma = log2 - lambda >= 0`. Hence
> `rho* <= phi* := sup_b (log fstar(b))/b`, the **max exponential fiber-growth
> rate of the degree-2 moment map**; and `rho* >= phi* - sup gamma`.

*Proof.* `lambda = (log L1)/b <= (log 2^b)/b = log 2`, so
`rho = phi + lambda - log2 <= phi`. The sup statement follows; `phi*` is a
genuine sup because `fstar` is super-multiplicative under tensoring
(`fstar(b1+b2) >= fstar(b1) fstar(b2)`, Fekete). ∎

This is the packet's main structural contribution to the wall: **the PTE-cluster
packing rate equals the max-fiber rate up to the (small, Lemma-B-controlled)
deficit.** Measured `gamma` stays `~0.02` (table above), so `rho*` and `phi*`
differ by a small constant. Bounding `phi*` is now the clean open target.

### 4.4 The honest wall (OPEN)

`phi* <= log 2` (Lemma C). Is `phi* < log 2`? Measured `phi(b)` (max-fiber
rate, repro `sym` stage) is **increasing with shrinking increments**:
`0.0866, 0.1493, 0.1775, 0.1932` at `b=8,12,14,16` (these are *lower bounds* on
the true `max fstar(b)`, from a symmetric diameter-capped search). So
`phi* >= 0.1932` and the limit is unresolved. The fast verifier (BLOCK 4)
re-checks the `b=6,12,14` sub-sequence `0.1155 < 0.1493 < 0.1775` from the exact
named blocks. A sub-`log2` cap needs an exponential upper bound on
the max fiber `#{w-subsets with fixed (e_1,e_2)}` that beats the trivial
`fstar(b) <= 2·fstar(b-1)` (coordinate split) and `fstar <= C(b, b/2)`
(Littlewood-Offord) — both of which only give `-> log2`. This is #623's named
wall, now pinned as: **bound `phi*`, the degree-2 moment-map max-fiber rate.**

### 4.5 Champion / family improvement (PROVED family, headline)

Because `rho(V)` is the exact tensor limit for symmetric `V` (Prop E), the
`b=14` champion yields a **PROVED infinite family** (its `k`-fold tensor powers,
`b = 14k`) with `rho -> 0.156659`, improving #623's champion family `0.131684`
by **`+0.0250` (`+19%`)**. This is the concrete R4 deliverable: a structured
family with proved limit `> 0.1317`.

### Proposition E (tensor achievability; PROVED for symmetric V, verifier BLOCK 3)

For symmetric `V` the balanced-weight `k`-tensor rate is
`rho_k = (1/bk) log( MF_k * L_k / M_k )` with `MF_k = fstar^k` (max fiber tensors
at the balanced split, using `mu(w)=mu(b-w)`), `L_k = [x^{bk/2}] P_V(x)^k`
(central coefficient of the symmetric convolution power `= L1^k / poly(k)` by the
local CLT), `M_k = C(bk, bk/2) = 2^{bk}/poly(k)`. Thus
`rho_k -> (1/b)(log fstar + log L1) - log2 = rho(V)`. The `MF_k = fstar^k` and
`M_k`, `L_k` polynomial-factor steps are checked exactly for `k<=3`; the single
`log`-limit (`L_k = L1^k/poly`) is the local-CLT step, flagged for PI.

---

## R5 — closed form / honest bracket (OPEN)

No closed form for `rho*` is reachable here. The honest state:

```
    proved lower bound (family):   rho* >= 0.156659   (b=14 champion, tensored)
    proved upper bound (cap):      rho* <= phi* <= (1-3/b)log2 -> log 2 = 0.693147
    census-backed conjecture:      rho* = phi* - gamma*  with phi* a finite
                                   constant; measured phi(b) increasing, phi*
                                   >= 0.1932, no plateau -> rho* is a moderate
                                   finite constant, plausibly ~0.18-0.25, OPEN.
```

The bracket `[0.156659, 0.6931]` is wide because the wall (bounding `phi*`) is
genuinely unresolved. What is *new* vs #623: the upper side is reduced to a
single clean quantity (`phi*`), the lower side is improved `0.1317 -> 0.1567`,
and the "plateau at 0.14" is removed.

---

## R6 — Codex `F_17` lead (AUDIT, does not port)

Codex's TEAM_BOARD 2026-07-11 12:42Z ledger line offered
`V = {1,2,3,4,5,6,7,8,10,16}` over `F_17` (fiber `4^k`, normalized excess
`(289/256)^k`, energy `28^k`, projective locator-span dim 3, gcd 1). Computed in
the **image-normalized** metric of this packet (verifier BLOCK 6):
`b=10, fstar=2, L1=984, rho = 0.065330` — **below** even 2-point Prouhet
(`0.1129`) and far below the champion. Its `4^k` fiber and `(289/256)^k` excess
live in the **span/ambient (`M/|B|^R`) normalization**, a different scaling from
the image face `barN = M/L`; the mechanism does not transfer to improve the
image-normalized packing rate. Recorded as a negative AUDIT with credit; it does
not feed R4/R5 here.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/pte_cluster_packing_frontier.md` (this).
- Verifier: `experimental/scripts/verify_pte_cluster_packing.py` (fast; recomputes
  every headline number, re-checks each named block exactly, re-runs the
  certified small censuses; `RESULT: PASS`).
- Repro (heavy searches, documented runtime): `experimental/scripts/repro_pte_cluster_census.py`.
- Read-only inputs: our #623 `pte_extremality_image_face.md` (`c2027dc`);
  hughes #564 `w_a_star_pte_lemma.md`.

**Per-claim status.** Problem + Lemma A (affine invariance) = `PROVED`. Census
(both frontiers) + champion `0.156659` + refutation of the `0.14` plateau =
`COMPUTED`. Optimizer symmetry / central-weight / growing-hole structure =
`MEASURED`. Lemma B (trade-deficit `c>=2^{b-2r}`) = `PROVED`. Lemma C
(`fstar<=2^{b-3}` -> `(1-3/b)log2`) = `PROVED`. Prop D (`rho*<=phi*`) = `PROVED`.
Prop E (tensor achievability, symmetric) = `PROVED` modulo the flagged local-CLT
step. Champion family limit `0.156659` = `PROVED`. Value of `phi*` / `rho*`,
sub-`log2` cap = `OPEN`. R6 = `AUDIT` (negative).

**Flagged for PI re-derivation (least-certain, 3 steps).**
(a) **Lemma B counting** — the "subfamily excess `>= 2^{b-2r}` implies global
`c >= 2^{b-2r}`" step (uses `f_s >=` subfamily-count-at-`s` termwise); re-check
the excess is not double-subtracted.
(b) **Prop E local-CLT step** — `[x^{bk/2}]P_V^k = L1^k / poly(k)` for symmetric
`P_V` (central coefficient of a convolution power = maximal, `~ L1^k/sqrt(k)`);
verifier only checks `k<=3` exactly.
(c) **`phi(b)` monotonicity / `phi* >= 0.1932`** — measured over a
symmetric-deletion, diameter-capped search (a *lower bound* on the true
`max fstar(b)`); the true `phi*` (hence whether `rho* < log2`) is unproven and is
the wall.

**Exact vs heuristic.** All `fstar`, `L1`, `c`, finite-`k` tensor rates, and
census optima are exact integer / `Fraction` enumeration. The asymptotic `rho`,
the caps, and `phi*` trend are elementary limits / measured trends of the exact
finite objects. No `.tex`/`.pdf` touched; nothing promoted into the draft.
