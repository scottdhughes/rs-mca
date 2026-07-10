# Asymptotic RS-MCA lower side: collision-free reroute (gap A9 / B4)

**Date:** 2026-07-09
**Scope:** `experimental/asymptotic_rs_mca.tex`, lower-side step of the proof of
`thm:frontier` (identity-prefix construction, base tip `eb42b82`).
**Audit verdict on the collision-loss gap:** `FIXED` (rerouted to a collision-free
source), with one demoted route left `OPEN GAP` and one normalization corner
flagged.

---

## Claim

The lower side of `thm:frontier` can be sourced from the **collision-free**
identity-prefix floor `lem:capff1-identity-prefix-floor`
(`experimental/cap25_cap_v13_raw.tex:6909`) composed with the deep-point
list-to-CA conversion `thm:A` (`cap25_cap_v13_raw.tex:221`) and support-wise
monotonicity `fact:chain` (`cap25_cap_v13_raw.tex:191`). This replaces the
unproved assertion that the raw pole map's "collision loss ... is subexponential
in the standard pole-reservoir regime" (`asymptotic_rs_mca.tex:283`, base
`eb42b82`) with a **proved** collision bound, and matches the numerator the lower
side already uses.

## Status

`AUDIT` + `FIXED` for the collision-loss gap; the bridge composition is `LEMMA`
(proved from cited proved lemmas); the literal over-claim is `OPEN GAP`.

## Fit verdict: **BRIDGED** (exact numerator + proved 2-lemma object bridge)

Per-hypothesis fit of `lem:capff1-identity-prefix-floor` against what the lower
side of `thm:frontier` consumes. Denominators use the mandated separation
`q_gen = |B|` (prefix/entropy), `q_line = q_chal = |F|` (slope/challenge).

| # | Lower side consumes | Floor (+bridge) supplies | Verdict |
|---|---|---|---|
| 1 | Row class: smooth mult./circle RS seq, `B ⊆ F`, `D ⊆ B`, `|D|=n` | `B ⊆ F`, `D ⊆ B`, `|D|=n`, any `1≤K≤n` (strictly more general) | **exact** |
| 2 | Prefix numerator `binom(n,m)·|B|^{-w}`, `w = a_n − k_n − 1` | list floor `≥ ⌈binom(n,m)/|B|^w⌉`, `w = m − K` | **exact** (identical numerator) |
| 3 | Ledger separation `q_gen=|B|` vs `q_line=q_chal=|F|` | floor denom `|B|^w` (base); slopes in `F=q_line`; reservoir `F∖D` | **exact** (kept separate) |
| 4 | Window/scale `m = a_n = k_n + 1 + w_n` | `K=k+1`, `m=a_n` ⇒ `w = m−K = a_n−k−1 = w_n` | **exact** |
| 5 | Threshold for `C = RS_F(D,k)`, dimension `k` | floor at `K=k+1` → deep-point converts to the dim-`k` code `C` | **exact** |
| 6 | Endpoint: `δ*(ε)=sup{δ: ε_mca ≤ ε}`, integer ball | `def:dstar` identical + integer-ball convention (`cap25:189`) | **exact** |
| 7 | Object: MCA-bad **slope** count `B^MCA/q_line` | **list** size (list-decoding / CA precursor) | **needs-bridge** → `thm:A` + `fact:chain` |
| 8 | Collision control (asserted "subexponential in pole-reservoir regime") | injective `M ↦ c_M` (collision-**free**) + `thm:A` reservoir averaging | **needs-bridge** → **PROVED** |
| 9 | Target regime `log2(1/ε_n)=O(n)`, fixed challenge normalization | trigger `barN > 2·q_line·ε_n` and `ε_n < (1/2k)(1−n/q_line)` | **needs-bridge**; exact under fixed-challenge normalization, corner below |

Items 1–6 are **exact**. Items 7–9 are bridged by **proved** lemmas already in
the same v13-raw ledger; there is **no mismatch**. Overall: **BRIDGED**.

---

## The gap it fixes (A9 / B4), stated precisely

`asymptotic_rs_mca.tex:283` (base `eb42b82`) justifies
`B_C^MCA(m) ≥ exp(−o(n))·binom(n,m)·|B|^{−w}` by asserting the raw pole map

```
S ↦ ℓ_S(α) = ∏_{t∈S}(α − t),   α ∈ F∖D
```

has subexponential support-collision loss "in the standard pole-reservoir
regime." Prior audits established, and this packet re-confirms from the source
lemmas:

- **Algebra `NO ISSUE`** (r2 §A9): the pole-line identity
  `f_α + ζ g_α` code-explained on `S` ⟺ `ℓ_S(α) = U_z(α) − ζ` is correct
  (polynomial division; `g_α` genuinely not degree-`<k` on `k+1` points).
- **Collision loss `OPEN GAP` as written** (r2 §A9, ledger §B4 `FOUND-WEAKER`):
  the phrase "pole-reservoir regime" appears in **no source file**; Grande
  `prop:pole-line` only *flags* the loss; Grande `thm:simple-pole-list-floor`
  bounds a reservoir collision **among the `L` list codewords** (`P_i − P_j` has
  `≤ k` roots), **not among the `~binom(n,m)|B|^{−w}` supports** the pole map
  needs.

The fix both audits already recommended — and which this packet implements — is
to **redirect the lower bound to the collision-free injective identity-prefix
floor + deep-point conversion**, whose collision control is proved.

---

## Bridge lemma (LEMMA, proved from cited proved lemmas)

> **Lemma (collision-free lower construction).** Let `C = RS_F(D,k)`, `B ⊆ F`,
> `D ⊆ B`, `|D| = n`, `|F| = q > n`, and `m = k+1+w` with `1 ≤ m ≤ n`. Put
> `q_line = |F|` and let `ε ∈ (0,1)`. Then
> ```
>   ε_mca(C, 1−m/n)  ≥  min( (L−1)/(2 q_line),  (1/2k)(1 − n/q_line) ),
>   L := ⌈ binom(n,m) · |B|^{−w} ⌉.
> ```
> In particular `ε_mca(C,1−m/n) > ε` whenever
> `binom(n,m)|B|^{−w} > 2 q_line ε` **and** `ε < (1/2k)(1 − n/q_line)`. No
> support-collision hypothesis is used.

**Proof.**
1. **Collision-free list (`lem:capff1-identity-prefix-floor`, `K=k+1`).** There
   is a `B`-valued word `U` with a list of `C^+ = RS_F(D,k+1)` of size
   `≥ L = ⌈binom(n,m)|B|^{−w}⌉`. The count is over distinct **codewords**
   `c_M = U − Λ_M|_D`; injectivity is the locator identity (`c_M` fixes
   `e_j(M)` for `j>w`, the prefix fibre fixes `j≤w`, so `Λ_M` and hence `M` are
   determined). No pole is evaluated, so there is no support collision.
2. **Deep-point conversion (`thm:A`, `η = 1/2`).** Admissible since `q > n` and
   `m ≥ k+1` gives `f_δ = n−m ≤ n−k−1`. For any exhibited list of size `L` in
   `C^+`: either `eca(C,δ) > (1/2k)(1−n/q)`, or `eca ≤ (1/2k)(1−n/q)` and then
   `thm:A` forces `L ≤ ⌈2q·eca⌉`, i.e. `eca ≥ (L−1)/(2q)`. Hence
   `eca(C,1−m/n) ≥ min((L−1)/(2q_line), (1/2k)(1−n/q_line))`. The collisions of
   `thm:A`'s **own** pole live among list codewords: `P_i − P_j ≠ 0` has degree
   `≤ k`, so `≤ k` roots per pair, `≤ k·C(L,2)` over the `q−n` reservoir poles
   `Ω = F∖D`, and some pole realizes `M(α) ≥ L(q−n)/(q−n+kL)` distinct CA-bad
   slopes. **This is the proved replacement for the asserted loss.**
3. **Monotonicity (`fact:chain`).** `eca ≤ emca`, so the same lower bound holds
   for `ε_mca = emca`. ∎

**Sharpness at `g*`.** With `m = a_n = (ρ+g)n+o(n)`, the numerator is
`barN_{n,a_n} = binom(n,a_n)|B|^{−w_n}`, `log2 barN = n(H2(ρ+g) − βg) + o(n)`.
For `g < g*(ρ,β)` by a fixed amount, `log2 barN = Ω(n)`. Under the fixed
challenge normalization (`log2(q_line ε_n) = o(n)`, i.e. the budget
`2 q_line ε_n` is subexponential — satisfied by the deployed rows, see below),
the trigger `barN > 2 q_line ε_n` fires and `ε_mca > ε_n`: the target fails at
radius `1−ρ−g+o(1)`, giving `δ*_{C_n}(ε_n) ≤ 1−ρ−g*+o(1)` as `g → g*`.

---

## Numeric anchor (deployed rows; exact-integer, from the verifier)

`experimental/scripts/verify_asymptotic_lowerside_collision_free_reroute.py`
(stdlib-only, zero-arg, best-effort `RLIMIT_AS` 2 GB, `630/630` checks, `6/6`
tamper self-tests, ~17 s). For `n=2^21`, `k=2^20`:

| Row | `|B|` | `q_line` | `w` | `ε_n` | floor `> 2 q ε` | `(1/2k)(1−n/q) ≥ 2^-86` | regime |
|---|---|---|---|---|---|---|---|
| KoalaBear list | `p=2^31−2^24+1` | `p^6` | `67470` | `2^-128` | yes (~9 bit margin) | yes (`≈2^-21`) | 1 (`barN<q`) |
| KoalaBear MCA | `p` | `p^6` | `67470` | `2^-128` | yes | yes | 1 |
| Mersenne-31 list | `p'=2^31−1` | `p'^4` | `67446` | `2^-100` | yes | yes | 1 |

The paper's exact edge inequalities `binom(n,m)·2^128 > p^{67470}·p^6` and
`binom(n,m)·2^100 > p'^{67446}·p'^4` (`prop:capff1-identity-frontier`) are
reproduced verbatim; the KoalaBear list margin recomputes to **9 bits**, matching
the printed `+9.2`. All deployed rows sit in **regime 1** (`barN < q_line`, so the
active bound is `(L−1)/2q_line`, not the saturated `1/2k`); `emca ≈ barN/2q ≈
2^-120 > 2^-128`, i.e. the `+9.2` bit margin. `cap25:93`'s universal
`emca > 1/2k ≥ 2^-86` is the **saturated** bound from the *quotient*-fiber floor
(`lem:fiber`, list `binom(N,ℓ)/|B|`), a different, larger list; both are `≤ 1`.

Gate E illustrates the mechanism exactly over `F_13`, `D={1..11}`, `K=3`, `m=5`:
the `462` subsets map to `462` distinct codewords (injective floor), while the raw
pole map `S ↦ ℓ_S(0)` collapses to only `12` distinct values — the collision loss
the reroute bypasses.

---

## What was edited in the tex

Surgical replacement of the collision-loss sentence + displayed bound at
`asymptotic_rs_mca.tex:283–287` only. The new text:
- cites `lem:capff1-identity-prefix-floor` by exact label for the collision-free
  list at `K=k+1`, `m=k+1+w`;
- cites `thm:A` by exact label for the deep-point conversion, stating that its
  reservoir averaging over `Ω=F∖D` **proves** the `≤ k·C(L,2)` collision bound;
- cites `eca ≤ eps_mca` (support-wise monotonicity) and prints the min-bound;
- **demotes** the direct pole bound `B_C^MCA(m) ≥ exp(−o(n))binom(n,m)|B|^{−w}`
  to an explicit `OPEN` alternative, noting it (a) presupposes the unproved
  support-collision control and (b) over-counts once `barN > q_line` (it would
  exceed the slope field).

The `thm:frontier` **statement** (135–142) and `lem:addback`/`sec:bsg` are **not**
touched — those belong to PRs #439 and #441 respectively.

---

## OPEN GAP (demoted route) and one normalization corner

- **`OPEN GAP`.** The literal `B_C^MCA(m) ≥ exp(−o(n))·binom(n,m)|B|^{−w}` (the
  *direct* pole route) remains unproved as a **slope**-count bound: it needs a
  subexponential bound on the fibres of `S ↦ ℓ_S(α)` at frontier scale, which no
  source supplies. As literally written it is moreover **unsound past
  `barN > q_line`** (a slope count cannot exceed `q_line`); it is kept only as an
  alternative. This is a `COUNTEREXAMPLE_NEW_FLOOR`-adjacent observation (a hard
  ceiling `B^MCA ≤ q_line` the direct over-claim ignores), but the *sound* lower
  side does not need it, so the frontier conclusion is unaffected.
- **Normalization corner (not the collision gap).** The reroute delivers the
  lower side for every `ε_n` with `log2(1/ε_n) = ω(log n)` (all cryptographic
  `ε_n = exp(−Θ(n))`, and the deployed targets). `ε_n` decaying slower than any
  inverse polynomial (e.g. constant `ε_n`) is not covered by the deep-point
  `1/2k` floor. This is a property of the "fixed challenge normalization"
  hypothesis of `thm:frontier` (the same normalization the B1/B3 audits and PR
  #439 address), **not** of the collision-loss gap fixed here.

---

## Nonclaims (AUDIT)

- **Not claimed:** that `thm:frontier` is now unconditional. Its `(C1)–(C9)` cell
  ledger, the C9 moduli/Fourier-Sidon source, `lem:addback`, and B3
  window-uniformity remain separate open items; this packet touches only the
  lower side.
- **Not claimed:** any bound on the raw pole fibres `S ↦ ℓ_S(α)`; the reroute
  *avoids* them.
- **Not claimed:** the deployed finite margins. Those need printed constants for
  every paid cell (`Remark [Finite adjacent rows]`); the asymptotic
  `exp(o(n))`/deep-point factors do not decide few-bit margins.
- **Not claimed:** improvement of the upper side, the entropy-frontier algebra,
  or the BSG/quasicube step.
- **Not claimed:** Lean certification; no Lean file was built.
- **Not a new floor:** the `B^MCA ≤ q_line` ceiling is standard, not a new
  obstruction; it is recorded only to justify demoting the direct pole bound.

---

## Interaction with open PRs

- **#439 (avdeevvadim), same block.** #439 reworded `thm:frontier`'s hypothesis
  to "... a lower-side identity-prefix input with subexponential collision loss,
  **or an equivalent collision-free identity-prefix floor**," and softened the
  `L283` sentence to that OR-branch **without instantiating it**. This packet is
  the **concrete instantiation of #439's second branch**: it names the
  collision-free floor (`lem:capff1-identity-prefix-floor`), the proved bridge
  (`thm:A` + `fact:chain`), and the resulting bound. Both edits touch the `L283`
  sentence, so a merge takes this concrete version in place of #439's abstract
  "or a replacement by a collision-free identity-prefix floor" clause; the
  `thm:frontier` statement edit of #439 is untouched here and composes.
- **#441 (holmbuar, A6), same file, different block.** #441 edits
  `lem:addback` / `sec:bsg` (upper side, ~`L243–265`) and adds files; disjoint
  from the lower-side block `L276–296`. No overlap.
- **Lineage.** This resolves the lower-side half of **#435 §A9** (proof-side
  collision caveat) and **#433 §B4** (`FOUND-WEAKER` citation joint), implementing
  the redirect both recommended.

## Reproducibility

```
python3 experimental/scripts/verify_asymptotic_lowerside_collision_free_reroute.py
# -> RESULT: PASS (630/630 checks, 6/6 tamper self-tests)   (~17 s, <2 GB)
```
