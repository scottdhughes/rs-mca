# KB-MCA Route-D v34: recursive multipad bound + multi-tier FM highs

Status: `PARTIAL` — **recursive M(m,f,N)** PROVED for all free_core; multi-tier
FM tags PROVED; deployed M_pad≤2 / |H|≤K_max / connectedness still **OPEN**.

## Recursive multipad bound (PROVED)

```text
M(m,0,N) ≤ 1
M(m,1,N) ≤ ⌊N/m⌋
M(m,f,N) ≤ ⌊ M(m−1,f−1,N−1) · N / m ⌋   (f≥2)
```

Lifts free_core=2 t-pack to **arbitrary free_core**, Helly or non-Helly.

### Deployed prefix (m=m_c, N=n−2e)

```text
f: M(m_c,f,n−2e) for f=0..9:
1, 2, 4, 8, 17, 36, 77, 165, 354, 760
```

f=1 → **2**, f=2 → **4** (v33). At free_core=`846161` the value is
finite but not useful for ≤2.

## Connectedness (PARTIAL)

Toys: all Type S connected. General proof OPEN. Bound does not need it.

## Multi-tier FM high tags (PROVED)

```text
tier τ: FM-match unmatched highs on fresh domain
κ(H) = (τ, local_idx) ∈ [R]×[⌊n/e⌋]
```

Deployed: `R ≤ 70` ⇒ capacity `2170` ≤ K_max=`2176`.

Every high with a U is eventually tagged if enough tiers. **Cardinality gate:**
full injection into [K_max] still needs `|H_A_SP| ≤ capacity`.

When all highs tagged, all A_SP pairs are covered (pair high ∈ tagged set).

## Toys

| j | w | free_core | #S | max M_pad | M_bound | ok? | connected? | #highs | tiers | full pair cover? |
|---|---|---:|---:|---:|---:|---|---|---:|---:|---|
| 4 | 1 | 1 | 0 | 1 | 6 | True | None | 17 | 3 | True |
| 5 | 1 | 2 | 908 | 9 | 20 | True | True | 17 | 4 | True |
| 5 | 2 | 0 | 0 | 1 | 1 | True | None | 110 | 30 | True |
| 6 | 1 | 3 | 904 | 14 | 54 | True | True | 17 | 4 | True |
| 6 | 2 | 1 | 0 | 1 | 3 | True | None | 65 | 18 | True |
| 6 | 3 | -1 | 0 | 1 | 1 | True | None | 30 | 14 | True |
| 7 | 1 | 4 | 620 | 17 | 84 | True | True | 17 | 5 | True |
| 7 | 2 | 2 | 4 | 2 | 7 | True | True | 36 | 13 | True |
| 7 | 3 | 0 | 0 | 1 | 1 | True | None | 13 | 6 | True |
| 8 | 1 | 5 | 364 | 14 | 132 | True | True | 16 | 5 | True |
| 8 | 2 | 3 | 2 | 2 | 8 | True | True | 19 | 8 | True |
| 8 | 3 | 1 | 0 | 1 | 2 | True | None | 5 | 3 | True |
| 9 | 2 | 4 | 0 | 1 | 11 | True | None | 8 | 4 | True |
| 9 | 3 | 2 | 0 | 1 | 1 | True | None | 1 | 1 | True |

Census: S=2802 bound OK; connected; all highs tagged;
full pair cover rows=14.

## OPEN

1. Deployed-useful M_pad (residual Type-S free / star); prove connectedness
2. `|H_A_SP| ≤ 2170` so multi-tier κ fits without overflow

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v34.py --check
```
