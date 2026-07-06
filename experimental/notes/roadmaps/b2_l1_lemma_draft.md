# Shared-core lemma draft (D1 literature + D3 structure), 2026-07-06

- **Status:** DRAFT / scoping. Two lemma statements, honest open/citeable labels. No proof.
- **Inputs:** D1 literature dive (BGK/Kowalski/Shkredov/Carlitz–McConnel/Xiong–Yip + CAP25 §16, all
  verified against local PDFs) and D3 saturator-structure computation (Codex-verified,
  `../scripts/b2_l1_saturator_structure.sage`).

## Headline: the two lanes share the BARRIER, not one dischargeable lemma

The earlier fold-in (`b2_l1_shared_core.md`) said "one core lemma discharges both lanes." **D1 corrects
this**: b2 and L1 share the `√p` Weil barrier and CAP25's "inverse theorem" *framing*, but their
resolutions diverge.

## D1 verdict (literature)

- **BGK / Heath-Brown–Konyagin / Kowalski** (single-sum cancellation over subgroups): require
  `|H| ≥ p^γ` for a fixed `γ>0`, savings `p^{-ν(γ)}` with `ν→0`. **In-regime for b2** (`|H|=2^41 ≥ q^{0.16}`);
  **vacuous for L1** (needs uniformity over *all* `ℓ|p−1`, including tiny `ℓ`), and only power-of-`p`
  precision — never the exact `ℓ−2`.
- **Shkredov** small-subgroup energy: right `|H|` range but bounds `H`'s own energy (wrong object) with
  log-power precision.
- **Carlitz–McConnel** (Xiong–Yip Thm 1.1): "all difference quotients in a proper subgroup `D` ⟹
  `f=ax^{p^j}+b`." The right *rigidity family*, but hypothesis far stronger than "many coincidences," and
  **collapses to linear over prime fields** (`n=1`); Xiong–Yip Thm 1.4 needs `n≥2` (vacuous mod p). It
  characterizes *extremizers*, does not prove the *bound*.
- **CAP25 v13** (verified: does NOT cite BGK): wants a *quantitative, explicit-constant* inverse theorem
  "large max-fiber ⇒ **quotient-stabilizer / block structure**," and flags that a **poly(n)-loss theorem
  is not a finite certificate** for the deployed adjacent rows, and that the needed moment order is `r~w`
  (high), not fixed.

**VERDICT:** L1's sharp `E_3≤ℓ−2` is **genuinely open** (no theorem in the right regime + precision).
b2's crude `extras≤n^3` is **essentially off-the-shelf** (BGK/HBK in-regime, cushion absorbs the loss).

## D3 corroboration (Codex-verified structure computation)

The extremal `E_3`-saturators show **no named combinatorial structure** beyond the coincidences:
- `M_2/M_3` coincidence moments separate extremal from random (excess 64–104 vs ~10) — but near-definitional.
- **Distinct value-set** multiplicative/additive energy does NOT separate (the earlier multiset signal was
  fiber multiplicity).
- **Directions / Carlitz–McConnel** concentration does NOT separate (top true `μ_ℓ`-class ~equal
  extremal vs random once zero quotients and the label bug are fixed).
- Heavy-fiber exponent sets are not APs.

So the extremal structure is **not** a high-energy set / directions-concentrated / monomial object at toy
scale — consistent with L1 being a **rank** statement, not a moment/energy inverse theorem.

## Draft lemma statements

### (a) b2 — CRUDE; reduces to an L¹-average character-sum bound (VERIFIED reduction, 2026-07-06)

The reduction is now pinned and numerically verified (`../scripts/b2_bound_mechanism.py`, **Codex-green**):

> **Reduction (verified).** For fixed giant `b` with `b ∤ M0` (so every t-null block of size `b` is an
> extra), the exact Fourier identity `extras_b = N_{t,b} = q^{−t} Σ_{c∈𝔽_q^t} S_b(c)`,
> `S_b(c) = [z^b] Π_{x∈μ_n}(1 + z·e_q(f_c(x)))`, gives by the triangle inequality
>   `extras_b ≤ q^{−t} Σ_c |S_b(c)| = C(n,b)/q^t` (first moment) `+ q^{−t} Σ_{c≠0}|S_b(c)|`.
> At (n,t,q)=(32,4,97): first moment ~4–6, the c≠0 L¹ average ~1810–2051, actual extras 32 — all
> `≪ n^3 = 32768`; the per-character max `|S_b(c)| ~1.4–1.8·10^6 ≫ n^3`. **Only the AVERAGE works, via the
> triangle inequality — no cancellation, no per-character bound.**

> **Lemma b2 (crude giant-extras bound) — target.** `extras_b ≤ n^3` for all deployed rows, reduced to the
> single analytic claim `q^{−t} Σ_{c≠0}|S_b(c)| ≤ n^3` — the L¹-Fourier mass of the size-b indicator against
> the power-sum characters.

- **Status:** the REDUCTION is verified (clean, no cancellation needed). The remaining crux is the
  **L¹-average bound** `mean_c|S_b(c)| ≤ n^3`. This is **NOT literally "cite BGK"** — BGK/HBK bound a
  *single linear* subgroup sum, whereas here the object is the elementary-symmetric `S_b` of the values
  `e_q(f_c(x))` of a *degree-t polynomial* `f_c`, averaged over `c` — a Bourgain–Chang-flavored *average*
  bound. The 123-bit cushion means a *very lossy* average bound suffices (`2^100`-lossy OK), which keeps
  b2 the tractable lane; but the deliverable is a genuine average-character-sum lemma, not a citation.
- **Two open pieces:** (i) prove/cite `mean_c|S_b(c)| ≤ n^3` — route: bound `S_b(c)` via Newton in the
  polynomial-subgroup power sums `p_r(c)=Σ_{x∈μ_n} e_q(r·f_c(x))` (Bourgain–Chang *on average over c*,
  not per-c, since per-c is useless), or a direct second-moment/energy bound absorbing the cushion;
  (ii) verify the arithmetic at the actual deployed `(n,b,t,q)` — CAP25's finite-certificate check.

### (b) L1 — SHARP, open; RANK statement, not a moment inequality
> **Lemma L1 (max-fiber ceiling).** Let `Γ ∈ 𝔽_p[X]`, `Γ(0)=0`, `deg Γ ≤ ℓ−1`, `ℓ` an odd prime with
> `ℓ | p−1`. Then `E_3 := Σ_C (μ_Γ(C)−2)_+ ≤ ℓ−2`, with equality only for `Γ` in the
> cyclotomic-coset-monomial rigidity class.
- **Route (per D1 + repo):** prove the inequality as the **rank statement** `dim Syz ≤ K` (⟺
  `dim(ΣV_k) ≥ E_3` ⟺ `E_3 ≤ ℓ−2`; upper half `dim(ΣV_k) ≤ ℓ−2` already proved, 4-CAS-verified). Do
  **not** pursue a BGK/moment proof of the inequality — provably not second-moment (pair-cap loses 2–3×),
  monodromy is blind, and no `M_r` inverse theorem of the needed uniformity+sharpness exists.
- **Extremal clause only:** the near-monomial/cyclotomic characterization via a Xiong–Yip-style
  char-sum + finite-geometry argument transferred to the *multiplicative (Kummer)* setting — a genuinely
  new transfer, not off-the-shelf. Numerology matches: `m*(ℓ)=(ℓ+3)/2 = (q+3)/2` directions bound
  (`Γ=X^{(ℓ+1)/2}`); refuted `⌈2ℓ/3⌉ = ` Gács gap.
- **Essential hypothesis:** single `Γ`, degree `≤ ℓ−1` (false for arbitrary coprime co-fibers).
- **Label: OPEN** (the sharp inequality; the rank crux `dim Syz ≤ K`, K≥3 chart, is the live L1 target).

## Net
b2 → draft (a), citeable, tractable NOW. L1 → the moment/BGK route (incl. Step-3 monodromy) is a **dead
end for the sharp bound**; refocus L1 on the **rank statement `dim Syz ≤ K`** (its pre-existing crux). The
"shared core" is the barrier and the extremal-rigidity *picture*, not a common proof.

Cross-refs: `b2_l1_shared_core.md` (corrected), `l1_e3_route_A_high_moment_scoping.md`,
`l1_e3_charsum_paircap.md`, `l1_e3_status_and_paper_connection.md`, `l1_e3_lacunary_directions_connection.md`.
