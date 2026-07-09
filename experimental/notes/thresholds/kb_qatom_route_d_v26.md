# KB-MCA Route-D v26: free_core=1 M_pad packing + high-tag criterion

Status: `PARTIAL` — free_core=1 **M_pad packing** PROVED; residual **high-tag
payment criterion** PROVED; deployed M_pad / highs↪[K_max] still **OPEN**.

## free_core=1 M_pad packing (PROVED)

At free_core=1, multipad cores for fixed `(U,V)` are a free-1 CS clique of
`m_c`-sets (v23), hence pairwise disjoint and ⊆ `D \ (U∪V)` with
`|U∪V|=2e`:

```text
M_pad  ≤  ⌊(n − 2e) / m_c⌋
```

## Deployed arithmetic

```text
⌊n/e⌋              = 31
⌊n/m_c⌋            = 2
⌊(n−2e)/m_c⌋       = 2
K_max = ⌊e/⌊n/e⌋⌋  = 2176
K_max · ⌊n/e⌋      = 67456  ≤ e = 67472
free_core          = 846161  (≠ 1 ⇒ packing bound not applied)
```

If multipad cores were disjoint at deployed free_core, packing would give
`M_pad ≤ 2`. Toys show **core intersections when free_core≥2** — disjointness
fails in general.

## Residual high-tag payment (PROVED criterion)

```text
M_pad ≤ 1
and residual highs ↪ [K] with K · ⌊n/e⌋ ≤ e
    ⇒  (κ(H), ι(U), δ) injects pairs into ≤ e·p = t·p
    ⇒  |A_SP| ≤ t·p
```

Deployed budget allows **K ≤ 2176**.

Special case **K=1** (single residual high): `(ι,δ)` alone closes payment.

## Toys

| j | w | free_core | max M_pad | pack bound | max highs/fib | fc1 cores disj? | fc≥2 inter? | (ι,δ) inj? | full high inj? | high0 mod K inj? |
|---|---|---:|---:|---:|---:|---|---|---|---|---|
| 4 | 1 | 1 | 4 | 6 | 17 | True | None | False | True | False |
| 5 | 1 | 2 | 9 | 4 | 17 | None | True | False | True | False |
| 5 | 2 | 0 | 1 | 5 | 5 | None | None | False | True | False |
| 6 | 1 | 3 | 14 | 3 | 17 | None | True | False | True | False |
| 6 | 2 | 1 | 2 | 3 | 6 | True | None | False | True | False |
| 6 | 3 | -1 | 1 | 4 | 1 | None | None | False | True | False |
| 7 | 2 | 2 | 2 | 2 | 5 | None | True | False | True | False |
| 7 | 3 | 0 | 1 | 2 | 1 | None | None | False | True | False |
| 8 | 2 | 3 | 2 | 2 | 3 | None | True | False | True | False |
| 8 | 3 | 1 | 1 | 2 | 1 | True | None | False | True | False |
| 9 | 2 | 4 | 1 | 1 | 2 | None | False | True | True | True |
| 9 | 3 | 2 | 1 | 1 | 1 | None | False | True | True | True |

- free_core=1: M_pad respects packing; cores disjoint.
- free_core≥2: core intersections observed (4 rows).
- Multi-high fibers: 433/1002.
- `(ι,δ)` cross-high collides; full high tag injects (over budget);
  `high0 mod K_max` fails injectivity.

## OPEN

1. Residual highs ↪ `[2176]` (constructive κ from fiber/ledger), or
   single-high residual for A_SP
2. `M_pad≤1` (or packing M_pad≤2 via core disjointness) at free_core=`846161`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v26.py --check
```
