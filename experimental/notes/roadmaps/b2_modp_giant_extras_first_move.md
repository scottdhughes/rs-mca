# b2_modp_giant_extras — first move: frame validated, analytic handle built, bound scoped

- **Status:** SCOPING + TOY-VERIFICATION (no bound proved yet). 2026-07-06.
- **DAG node:** `b2_modp_giant_extras` [TARGET] — a verified single point of failure into the MCA-safe
  grand challenge (`b2 --req--> u2c_boundary_scale_column --req--> x4b_moment_trade_exclusion --> ... -->
  mca_safe --> mca_grand`). Its char-0 sibling `b1_char0_giant_coset_theorem` is [PROVED] but enters
  `u2c` only as `ev` (support), NOT as an `alt` — the mod-p case has no Galois analogue, so **there is no
  bypass around b2** (verified against `prize_dag.json` edges).
- **Scripts (reproducible):** `../scripts/b2_toy_n16.py`, `b2_toy_sweep.py`, `b2_charsum_crosscheck.py`.
- **Lane check:** non-overlapping — disjoint from holmbuar (E_3/max-fiber), LegaSage (conj_f/XR),
  DannyExperiments (CAP25 Q-fin), and the M1 rank-2 slope terminal (scouted 2026-07-06).

## The object, re-derived (the reframing `b2` states but did not re-derive)

A **t-null block** is a subset `B ⊆ μ_n` (n = 2^s; `q ≡ 1 mod n` so `μ_n ⊆ F_q`) with vanishing power
sums `Σ_{x∈B} x^r = 0` in `F_q` for `r = 1..t`. By **Newton's identities**, vanishing power sums
`p_1..p_t` ⟺ vanishing elementary symmetric `e_1..e_t` ⟺ the monic divisor `L_B(X) = Π_{x∈B}(X−x)` of
`X^n − 1` has its **top t coefficients zero** (a "coefficient gap"). Hence:

> **b2's count = the number of monic degree-b divisors of `X^n − 1` over `F_q` with a top-t coefficient
> gap that are NOT coset-unions** — a Hayes/Carlitz "divisors with prescribed leading coefficients"
> count.

**Validated numerically** (`b2_toy_n16.py`): the Newton equivalence holds on every mod-p t-null block at
`(n,t,q) = (16,4,17)`.

## The Frobenius gap, made concrete

- **char 0 (b1):** `f_B` has integer coefficients, so `B̂(ζ^r)=0` propagates along Galois orbits ⟹ every
  0/1 t-null vector is a union of `μ_M`-cosets with `M > t`. **Confirmed:** at `(16,4)` the char-0 t-null
  blocks are *exactly* the 4 `μ_8`-coset unions (`b2_toy_n16.py`, exact `ℤ^8` arithmetic via `Φ_16=X^8+1`).
- **mod p (`q ≡ 1 mod n`):** Frobenius fixes `μ_n` pointwise, the forcing dies, and **"extras"
  (non-coset-union t-null blocks) genuinely appear** — e.g. **3600 extras** at `(16,1,17)` vs only 256
  structured (`b2_toy_sweep.py`). They vanish as the constraint cost approaches the entropy (t=3,4 at
  n=16 → 0 extras) and as `q` grows (`q=97` → 0 extras) — the char-0/finite-field gap is fundamental,
  not technical, exactly as the node states.

## The analytic handle (the concrete first move), cross-checked on two engines

Additive-character orthogonality gives the **exact first-moment identity**
```
N_t(n,q) = #{ B ⊆ μ_n : Σ_{x∈B} x^r = 0, r=1..t }
         = q^{-t} · Σ_{c ∈ F_q^t}  Π_{x∈μ_n} ( 1 + e_q( Σ_r c_r x^r ) ),   e_q(u)=exp(2πi u/q).
```
The `c=0` term is `2^n`; the giant-regime bound must control the rest. **`b2_charsum_crosscheck.py`
confirms `N_t` (character sum) equals the brute enumeration EXACTLY** on all of
`(8,1),(8,2),(16,1),(16,2),(16,3),(16,4),(16,2@q=97)` — the two-engine check (nt-stack rule) on the
Hayes/Carlitz handle we will bound.

## Scoping the `n^3` cushion (what the bound is, and is NOT)

The `n^3 = 2^123` bound is **giant-regime-specific**, about the *extras* (deviation from the structured
coset-unions), NOT the total t-null count. At small t the total count follows the first moment
`N_t ≈ 2^n/q^t` and **vastly exceeds `n^3`** (verified by character sum, no enumeration needed):

| n | t | q | `N_t` (exact) | `2^n/q^t` | `n^3` | verdict |
|---|---|---|---|---|---|---|
| 16 | 1 | 17 | 3856 | 3855 | 4096 | `≤ n^3` (coincidence: `2^16/17 ≈ 2^12`) |
| 32 | 1 | 97 | 44,278,048 | 4.4e7 | 32,768 | `≫ n^3` (small-t, NOT a prize row) |
| 64 | 1 | 193 | 9.56e16 | 9.56e16 | 262,144 | `≫ n^3` (small-t, NOT a prize row) |

So the node's point (ii) is confirmed: **"pure counting can never close it"** — the *total* first moment
is enormous near the prize balance (`t log2 q ≈ n`), and the content of b2 is that the first moment is
almost entirely **structured** (coset unions, per b1) with only `≤ n^3` genuine extras. Full enumeration
lives in the wrong (small-t) regime to test this; the giant regime is analytic-only.

## Phase 0 — structural go/no-go (2026-07-06): the coset-union dichotomy FAILS below balance

Tested whether the extras confine to a coset scale (u2c's dichotomy conjecture: every t-null block is a
union of μ_M-cosets with `M ≥ t`), by classifying every t-null block by its symmetry scale `M_sym` =
largest power-of-2 `M | n` with `B` a union of μ_M-cosets (`../scripts/b2_phase0_dichotomy.py`;
meet-in-the-middle enumeration; **Codex-reviewed to GREEN over 2 rounds** — one float-precision bug in the
character count was fixed to an exact integer DP; MITM completeness, `M_sym`, Newton, and the char-0 `ℤ^8`
arithmetic were all independently re-verified).

**Result: the dichotomy FAILS below balance.** The extras are genuinely *unstructured* (`M_sym = 1`, not
even closed under `x → −x`), and their appearance is governed by the balance point `cost = t·log2 q`
vs `entropy ≈ log2 C(n, n/2)`:

| n=32, q=97 (entropy ≈ 29.2) | t=2 | t=3 | t=4 | t=5 | t=6 |
|---|---|---|---|---|---|
| cost = t·log2 q | 13.2 | 19.8 | 26.4 | 33.0 | 39.6 |
| extras | 455488 | 6336 | 160 | 0 | 0 |
| dichotomy | FAILS | FAILS | FAILS | HOLDS | HOLDS |

Codex-confirmed witness: at (16,2,17), block `{1,2,3,13,15}` (exponents `[0,1,4,6,14]`) has `Σx = Σx² = 0`
yet is not closed under `x → −x` — a genuine unstructured 2-null block.

**Consequence (route pruned).** The prize regime sits ~2% *below* balance, so unstructured extras
genuinely exist there — **b2's `≤ n^3` bound CANNOT rest on a coset-union dichotomy** (that route, the u2c
hope, is false below balance). This is *not* a refutation of u2c: their coset-only scans were at/above
balance or a narrower construction. Encouragingly, near balance the extras are modest (160 at t=4,
`≪ n^3`) and only balloon far below balance; the prize is *just* below balance.

## Step 2, fixed-b target + Prong 1 attempt (2026-07-06): pruned by the cancellation barrier

**Target corrected to FIXED degree-b.** b2 bounds non-coset-union t-null blocks of a *fixed* size `b`
in the giant regime `b > t` (the node's "monic degree-b divisors"), NOT the all-sizes count `N_t` (which
is `~2^{n − t log2 q} ≫ n^3` and is the wrong object). Fixed-b machinery built and **two-engine
cross-checked** (`../scripts/b2_prong1_fixed_b.py`, **Codex-GREEN**): a size-marked exact DP for
`N_{t,b}` vs the MITM/brute bucketing agree. Structural fact confirmed: at sizes `b` NOT divisible by
`M0`, structured `= 0` (every t-null block of that size is an extra — u2c's "weight not divisible by 16
⇒ primitive"). Near balance (32,4,97) the fixed-b extras are modest: `~32 = n` per size, total 160 `≪ n^3`.

**Prong 1 (per-character Hayes/Carlitz Weil) — ATTEMPTED and PRUNED.** For `b ∤ M0`,
`extras_b = N_{t,b} = q^{-t}[ C(n,b) + Σ_{c≠0} S_b(c) ]`, `S_b(c) = [z^b] Π_{x∈μ_n}(1 + z·e_q(f_c(x)))`,
`f_c = Σ_r c_r x^r`. Wolfram-verified reduction (`app-kernel`): `log Π = Σ_r (−1)^{r-1}/r·p_r z^r`, so
`S_b` is Newton-Girard in the power sums `p_r(c) = Σ_{x∈μ_n} e_q(r·f_c(x))` — which are **Weil character
sums**. Numerics (`gp`/Python, `q=97,n=32`): the `p_r(c)` ARE Weil-small (`|p_r| ≈ 3–6 ~ √q`). **But
the per-character bound is useless**: for giant `b=13`, individual `|S_b(c)|` has mean **2473** and max
**493394** (`≫ n=32`), while the true `extras_13 = 32`. The small count survives **only by signed
cancellation across the c-sum** (`Σ_c|S_b(c)|/q^t ≈ 2473 ≫ 32`). So bounding `S_b(c)` per character
cannot work — this is the **√p barrier** (CAP25 Rem 16.10), the **same "joint cancellation required"
wall as L1 route A** (the BGK inverse theorem). **Net: b2's giant-extras core and L1's E_3 core are the
same additive-combinatorics problem.**

## Step 3 (the surviving route): second moment / monodromy, not per-character

Bound `Σ_{c≠0} S_b(c)` via cancellation, not term-by-term. Two handles:
1. **Geometric monodromy / Katz equidistribution** of the family `{ Π_x(1 + z·e_q(f_c(x))) }_c` — a
   sheaf on `𝔸^t`; big monodromy ⇒ square-root cancellation in the c-sum. Tool: **Oscar**
   (function-field Galois / monodromy of the coincidence variety).
2. **BGK additive-combinatorics inverse theorem** (Bourgain–Glibichuk–Konyagin / Kowalski): large
   `Σ_c S_b(c)` ⇒ block/quotient-stabilizer structure — the CAP25 named-open route, shared with L1.
Because b2 ≡ L1 at this core, **progress on either transfers**; the 123-bit cushion (2^100-lossy OK) is
the reason b2 is the more tractable entry point. Tools: Oscar (monodromy), PARI/Arb (rigorous char-sum
enclosures), the research CPU box (MITM extras-vs-n scaling to n≈48–56), Aristotle for an isolated lemma.

## Honest scope

First move + Phase 0: reframing **re-derived and numerically validated**, b1 **confirmed**, Frobenius-gap
extras **exhibited**, character-sum handle **built and two-engine cross-checked**, and the coset-union
dichotomy **tested and refuted below balance** — all scripts **Codex-green**. **No bound on the extras is
proved yet** — that is Step 2 (the analytic route), the open crux of the node. Nothing here is a prize
threshold.
