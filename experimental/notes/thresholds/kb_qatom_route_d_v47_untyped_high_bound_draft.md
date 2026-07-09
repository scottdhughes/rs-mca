# Untyped residual high bound — draft from free-1 + free_core geometry

Status: **DRAFT / PARTIAL** — reduction lemmas below are in good shape;
the terminal sublemma `H_*(A+e,e) ≤ H2` is **not** proved. This is the
intended primary-geometry attack on residual card (v45–v46), not a finished
theorem.

Companion verifier: `experimental/scripts/verify_kb_qatom_route_d_v47.py`.

---

## 0. Goal

Close residual card after SR + H_M by bounding **pure-untyped free-1 residual highs**

```text
H_unt  :=  free-1 highs whose A_SP free-1 CS pairs are all untyped
           (single-core multi-U pencils; not multi-core multipad sides)
```

and/or their residual after H_M. Target:

```text
|H_unt|  ≤  H2  ≈  7.73×10^10
```

(or `|R2_unt| ≤ e·p`). Under M_pad≤2 on any remaining Type D, this yields
`N_side ≤ 930|H|` and residual enum into e·p (v42–v46).

---

## 1. Primary dictionary (already proved)

| Symbol | Meaning | Source |
|---|---|---|
| `e = w+1` | free-1 side size | route-D |
| `m_c = j−e` | core size | |
| `free_core = m_c − w = j − 2w − 1` | free core coefficients | v22 |
| free-1 high `H` | monic coeffs of `X^{e−1},…,X^1` | v25 |
| `F_H` | fully split free-1 e-sets of high `H` | v25: **pairwise disjoint**, `\|F_H\|≤⌊n/e⌋` |
| top-seam | `S = C⊔U`, `T = C⊔V`, free-1 sides | v20 |
| multipad cores | several `C` with same free-1 sides `(U,V)` and `Φ_w(C)=Φ_w(C')` | v22 |
| Type S / D | multipad root mult ≥2 / ≤1 | v35 |
| untyped pair | free-1 CS pair in a multi-U pencil whose side key is **not** a multi-core multipad | v46 |

Deployed:

```text
n = 2^21,  e = 67472,  m_c = 913632,  free_core = 846161
n' := n − m_c = A + e = 1183520
⌊n'/e⌋ = 17 = pack_ceil
H2 = ⌊e·p / (2·31·30)⌋ ≈ 7.73e10
```

---

## 2. Lemma — unique core of an untyped pair (PROVED)

**Statement.** An untyped free-1 ordered pair `(U,V)` arises from a unique
multi-U pencil `(C,H)`, hence has a unique core `C`.

**Proof.** By definition, untyped means the free-1 side key is **not** realized
with two or more distinct cores (else it is a multipad side key, Type S or D).
The multi-U free-1 pencil that produces `(U,V)` is exactly one pair
`(C, high(U))` with `|pencil|≥2`. ∎

---

## 3. Lemma — unique core of a pure-untyped high (DRAFT / toys universal)

**Statement.** If every free-1 CS pair of a high `H` is untyped, then there is a
**unique** core `C(H)` such that all multi-U free-1 pencils of `H` use that core.

**Evidence.** On all A_SP-prefix toys checked (v47): no pure-untyped high has
two distinct cores.

**Draft proof sketch (gap marked ★).**

1. `F_H = {U_1,…,U_f}` is a free-1 family: same high, pairwise disjoint (v25).
2. Each multi-U pencil of `H` is a subset of `F_H` co-extended by a fixed core `C`
   (j-sets `C⊔U` for `U` in the pencil).
3. Each untyped pair `(U_i,U_j)` has a unique core by Lemma 2.
4. **★ Gap:** show all pairs of `F_H` share the **same** core, i.e. `F_H` does not
   split as two untyped sub-pencils on `C ≠ C'`.

   Heuristic: if `(U,V)` co-extends only with `C` and `(U,W)` only with `C'`, then
   `U` participates in two top-seam geometries; free-1 rigidity + monic recovery
   may force a multipad side key or identify `C=C'`. Not written as a complete
   argument yet.

**Status:** treat as **axiom/ conjecture C_unique** until ★ closed; toys support it
strongly (`multi_C_highs = 0` on full suite).

---

## 4. Lemma — reduction to per-core free-1 multipads (PROVED under C_unique)

**Statement.** Under C_unique,

```text
H_unt  =  ⊔_C  H_unt(C)
|H_unt|  =  sum_C |H_unt(C)|
```

where `H_unt(C)` is the set of pure-untyped highs with core `C`.

Each `H ∈ H_unt(C)` is a free-1 multipad high in the complement

```text
Ω_C  :=  D \ C ,   |Ω_C| = n − m_c = n' = A + e  (deployed).
```

**Proof.** Lemma 3 assigns each pure-untyped high a unique core; free-1 e-sets of
`H` lie in `Ω_C` because `S = C⊔U` is a partition. ∎

---

## 5. Lemma — free-1 geometry in a fixed complement (PROVED)

**Statement.** Fix `C` and `Ω = D\C` with `|Ω|=n'`. For free-1 multipad highs in `Ω`:

```text
|F_H|  ≤  ⌊n'/e⌋          (disjoint packing in Ω)
deg(U) ≤  ⌊n'/e⌋ − 1      (ordered free-1 mates of an e-set U ⊂ Ω)
```

Deployed: `⌊n'/e⌋ = 17`, `deg ≤ 16` (same as v19/v43 complement degree).

**Proof.** v25 family disjointness + v19 ambient CS degree on `Ω`. ∎

---

## 6. Lemma — crude per-core high bound (PROVED, not enough)

**Statement.**

```text
|H_unt(C)|  ≤  N_side(Ω_C) / 2  ≤  (1/2) · binom(n',e) · (⌊n'/e⌋ − 1)
```

**Proof.** Each multipad high contributes ≥2 ordered free-1 pairs; each e-set has
≤⌊n'/e⌋−1 mates. ∎

Deployed: RHS has `log2 ~ 3.7×10^5 ≫ log2(H2)~36`. **Not a usable card bound.**

Toys also refute `|H_unt(C)| ≤ ⌊n'/e⌋` and `≤ 2⌊n'/e⌋` (e.g. 100 highs with
`⌊n'/e⌋=4`).

---

## 7. Conditional packing of cores (PROVED implication)

**Statement.** If the set `{C(H) : H ∈ H_unt}` is pairwise disjoint, then

```text
|H_unt|  ≤  ⌊n / m_c⌋ · max_C |H_unt(C)|
```

Deployed: `⌊n/m_c⌋ = 2`, so

```text
|H_unt|  ≤  2 · H_*(n', e)
```

where `H_*(n',e) := max |{free-1 multipad highs in a domain of size n'}|`.

**Toys:** often `n_C = 1` (all pure-untyped highs share one core), so
`|H_unt| = |H_unt(C_*)| ≤ H_*(n',e)` on those rows. Core-disjoint packing is
not always the story — sometimes a **single** core carries all untyped highs.

**Status of core packing as theorem:** not claimed. Single-core concentration is
empirical on small fields.

---

## 8. Master reduction (PROVED conditional)

Under C_unique (Lemma 3):

```text
|H_unt|  ≤  N_C · H_*(n', e)
```

with `N_C = # distinct cores of pure-untyped highs`, `n' = A+e`.

**Card close if:**

```text
N_C · H_*(A+e, e)  ≤  H2
```

Special cases:

| Extra input | Bound |
|---|---|
| `N_C = 1` (single core hosts all untyped) | need `H_*(A+e,e) ≤ H2` |
| cores pack, `N_C ≤ 2` | need `H_* ≤ H2/2` |
| free_core ≤ 0 + Φ_w unique core per fiber | may force small `N_C` (v22) |

---

## 9. Open sublemma ★ — refined after v48 attack

**Original unrestricted form (FALSE for e=3):**

```text
H_*(any domain of size A+e, e)  ≤  H2
```

v48 CAS: cyclic domains with e=3 attain `|H|=p² > H2`. So abstract-domain ★ fails.

**Refined ★_D (LIVE):**

```text
Ω = D \ C,  D = fixed KB n-point domain ⊂ F_p,  |C|=m_c
H_*^D = # free-1 multipad highs among e-subsets of Ω
Need H_*^D ≤ H2
(or co-extension-restricted count ≤ H2)
```

### Why this is the right residual problem

- Untyped residual (dominant after SR at free_core≥1, v46) reduces to free-1
  multipads in **one** complement of size `A+e`, not the full `n`-set high count.
- Complement free-1 **degree** is already 16 (sharp pack geometry).
- What remains is **how many** such multipad highs exist when
  `e / (A+e) ≈ 1/17`.

### Approaches that do **not** work (banked)

| Attempt | Why not |
|---|---|
| `H_* ≤ ⌊n'/e⌋ = 17` | REFUTED (toys: 100 > 4) |
| `H_* ≤ n'` | ambient e=3 has `\|H\|~n² > n` |
| `H_* ≤ binom(n',e)/2` | true, useless vs H2 |
| multi-tier capacity 2170 | only matched highs, not ambient free-1 |

### Approaches that might work (not drafted as proofs)

1. **Equal power-sum rigidity:** free-1 ⇔ agree on `p_1,…,p_{e−1}`; for
   `e ~ n'/17` in a cyclic subgroup of `F_p`, multipad families may be
   extremely rare (additive combinatorics / Prouhet–Tarry–Escott type).
2. **Field polynomial factorization:** monic `H(X)+c` fully splitting on a
   prescribed `n'`-set for two values of `c` — bound the number of such `H`.
3. **free_core linkage:** only those free-1 multipads that **co-extend** by a
   fixed `C` of size `m_c` with `Φ_w` constraints count; may be far fewer than
   ambient `H_*(n',e)`.

---

## 10. free_core’s role (honest)

| free_core | What it gives |
|---:|---|
| ≤ 0 | `Φ_w` determines monic core (v22); M_pad cores ≤1; helps uniqueness of `C` in a fiber |
| = 1 | multipad cores for fixed `(U,V)` are free-1 CS and pack (v26) |
| ≫ 1 (deployed) | core multi-mates exist; **does not** by itself bound free-1 **side** highs |

Deployed free_core helps the **SR / Type D** cut (multipads), which funnels mass
into **untyped free-1** (v46). It does **not** yet bound `|H_unt|` without ★.

---

## 11. What would finish residual card

```text
C_unique  (Lemma 3, almost toys-proved)
    +
N_C · H_*(A+e, e)  ≤  H2   (open ★, possibly N_C=1)
    +
v46: |R2| ≤ 930 |H_R2| and residual ≈ untyped
    ⇒
|R2| ≤ e·p   (or ≤ e·p/2 under M_pad≤2 bookkeeping)
    ⇒
residual free-1 card into e·p
```

SR + Type D + M-cell already structured (v35–v45). This draft is only the
**untyped high** step.

---

## 12. Recommended next mathematical work

1. **Close ★** for free-1 multipads on domains of size `A+e` with `|U|=e=⌊|Ω|/17⌋`,
   or prove the co-extension-restricted count ≪ ambient `H_*`.
2. **Close C_unique** (Lemma 3 ★ gap) with a short free-1 + top-seam argument.
3. Do **not** spend more PR packets on `|H|≤n` or `|H|≤⌊n/e⌋` envelopes (refuted).

---

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v47.py --check
```
