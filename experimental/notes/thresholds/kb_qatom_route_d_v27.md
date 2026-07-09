# KB-MCA Route-D v27: multipad intersections ≤ free_core−1

Status: `PARTIAL` — multipad **intersection bound** PROVED; constructive κ and
deployed M_pad≤2 still **OPEN**.

## Main theorem (PROVED)

If `C ≠ C'` are multipad cores, then

```text
|C ∩ C'|  ≤  free_core − 1
```

Proof: `Δ = Λ_C − Λ_{C'}` has `deg ≤ free_core−1` and is nonzero; every common
root is a root of `Δ`.

### Corollaries

| free_core | consequence |
|---:|---|
| = 1 | cores disjoint ⇒ `M_pad ≤ ⌊(n−2e)/m_c⌋` |
| ≥ 2 | pairwise inter ≤ free_core−1; simple disjoint packing may fail |

### Uniform packing (PROVED, weak deployed)

```text
M_pad  ≤  C(n−2e, free_core) / C(m_c, free_core)
```

Deployed `log10` estimate ≈ `478050.28` — **not** ≤ 2.

## Deployed

```text
free_core              = 846161
intersection bound     = 846160
⌊(n−2e)/m_c⌋ if disj.  = 2
K_max for high tags    = 2176
```

## Constructive κ census (BANKED NEGATIVE)

Payment still: `M_pad≤1` + residual highs↪`[K≤2176]` + `(ι,δ)`.

| κ tag | inj rows | coll rows |
|---|---:|---:|
| `const` | 2 | 12 |
| `high0_mod_K` | 2 | 12 |
| `sumh_mod_K` | 2 | 12 |
| `min_union_mod_K` | 2 | 12 |
| `canon_minU_mod_K` | 2 | 12 |
| `canon_c0_mod_K` | 2 | 12 |
| `pair_minU_mod_K` | 2 | 12 |
| `fiber_high_rank` | 3 | 11 |
| `full_high` | 14 | 0 |

Full high injects (over budget). Fiber-local high rank without fiber id collides.

## Toys

| j | w | free_core | max M_pad | max inter | bound | simple pack | exceeds pack? | max H/fib | fiber rank inj? | full high? |
|---|---|---:|---:|---:|---:|---:|---|---:|---|---|
| 4 | 1 | 1 | 4 | 0 | 0 | 6 | False | 17 | False | True |
| 5 | 1 | 2 | 9 | 1 | 1 | 4 | True | 17 | False | True |
| 5 | 2 | 0 | 1 | -1 | -1 | 5 | False | 5 | False | True |
| 6 | 1 | 3 | 14 | 2 | 2 | 3 | True | 17 | False | True |
| 6 | 2 | 1 | 2 | 0 | 0 | 3 | False | 6 | False | True |
| 6 | 3 | -1 | 1 | -1 | -2 | 4 | False | 1 | False | True |
| 7 | 1 | 4 | 17 | 3 | 3 | 2 | True | 16 | False | True |
| 7 | 2 | 2 | 2 | 1 | 1 | 2 | False | 5 | False | True |
| 7 | 3 | 0 | 1 | -1 | -1 | 2 | False | 1 | False | True |
| 8 | 1 | 5 | 14 | 4 | 4 | 2 | True | 12 | True | True |
| 8 | 2 | 3 | 2 | 2 | 2 | 2 | False | 3 | False | True |
| 8 | 3 | 1 | 1 | -1 | 0 | 2 | False | 1 | False | True |
| 9 | 2 | 4 | 1 | -1 | 3 | 1 | False | 2 | True | True |
| 9 | 3 | 2 | 1 | -1 | 1 | 1 | False | 1 | True | True |

Intersection checks: 34144/34144 OK; tight frac
0.62. free_core≥2 exceeds simple pack on
4 rows.

## OPEN

1. Constructive `κ`: residual highs → `[2176]` (ledger/fiber witness)
2. `M_pad≤1` or core-near-disjoint `M_pad≤2` at free_core=`846161`
   beyond the weak binomial packing

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v27.py --check
```
