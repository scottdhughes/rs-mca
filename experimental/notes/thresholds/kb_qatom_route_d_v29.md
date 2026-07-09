# KB-MCA Route-D v29: residual multipad emptiness + Type D/S split

Status: `PARTIAL` — **residual multipads empty** after A_SP (PROVED); Type D
packing **M_pad≤2** deployed (PROVED); Type S at free_core≫1 still **OPEN**.

## Residual multipad emptiness (PROVED)

First-match partition (v17):

```text
Fib_w(z)  =  A_SP(z)  ⊔  R_sing(z)
```

- `A_SP` = multi-member top-seam core pencils
- `R_sing` = singleton pencils (matching-free residual)

Multipads need free-1 CS pairs from multi-member pencils ⇒ **only on A_SP**.

```text
R_sing:  N_ord = 0,  M_pad = 1 (vacuous)
```

After the A_SP cell is paid, **residual carries no multipad term**.

> The slogan “residual multipad t=1” is vacuously true: there are no residual
> multipads. The live problem is A_SP multipad geometry.

## A_SP multipad types (PROVED)

For each multipad side key `(U,V)` with core set `Cores`:

```text
t = max_r |{ C ∈ Cores : r ∈ C }|
Type D: t = 1   (pairwise disjoint cores)
Type S: t ≥ 2   (shared-root multipad)
```

| type | free_core | M_pad bound |
|---|---|---|
| D | any (all of free_core=1) | `≤ ⌊(n−2e)/m_c⌋` = **2** deployed |
| S | only ≥ 2 | OPEN at free_core=`846161` |

## Payment path (restated)

```text
first-match:
  pay A_SP  (needs Type D ≤ 2 + Type S control + side marks)
  residual ⊆ R_sing  (no multipad)
```

Side marks still: `(ι,δ)` within family + highs ↪ `[2176]` (v25–v28).

## Toys

| j | w | free_core | #R_sing | #A_SP | #Type D | #Type S | max M_pad D | max M_pad S | D pack | max t |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 1 | 0 | 17 | 540 | 0 | 4 | 1 | 6 | 1 |
| 5 | 1 | 2 | 0 | 17 | 64 | 908 | 2 | 9 | 4 | 4 |
| 5 | 2 | 0 | 28 | 261 | 0 | 0 | 1 | 1 | 5 | 0 |
| 6 | 1 | 3 | 0 | 17 | 0 | 904 | 1 | 14 | 3 | 7 |
| 6 | 2 | 1 | 54 | 235 | 2 | 0 | 2 | 1 | 3 | 1 |
| 6 | 3 | -1 | 4405 | 75 | 0 | 0 | 1 | 1 | 4 | 0 |
| 7 | 2 | 2 | 105 | 184 | 0 | 4 | 1 | 2 | 2 | 2 |
| 7 | 3 | 0 | 4782 | 34 | 0 | 0 | 1 | 1 | 2 | 0 |
| 8 | 2 | 3 | 181 | 108 | 0 | 2 | 1 | 2 | 2 | 2 |
| 8 | 3 | 1 | 4872 | 9 | 0 | 0 | 1 | 1 | 2 | 0 |
| 9 | 2 | 4 | 245 | 44 | 0 | 0 | 1 | 1 | 1 | 0 |
| 9 | 3 | 2 | 4815 | 1 | 0 | 0 | 1 | 1 | 1 | 0 |

Census: R_sing multipads=0 (must be 0);
Type D pack OK=606/606;
Type S events=1818; fc1 Type S=0.

## OPEN

1. **Type S** multipads at free_core=`846161` (shared-root A_SP)
2. High tag `κ → [2176]` for side injection under M_pad≤1 or ≤2

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v29.py --check
```
