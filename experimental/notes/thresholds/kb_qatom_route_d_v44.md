# KB-MCA Route-D v44: CAS free-1 growth + residual R-cell bulk

Status: `PARTIAL` — **Sage free-1 census** (or python fallback) + **R-cell pair
bulk** after H_M; deployed N_ord/|H|≤H2 still **OPEN**.

## CAS (Sage) ambient free-1 on cyclic domains

Backend: `sage`
(PASS).

| n | e | #H | N_side | max f | max deg | bound | N_side/crude |
|---|---:|---:|---:|---:|---:|---:|---:|
| 16 | 2 | 17 | 728 | 8 | 7 | 7 | 0.867 |
| 16 | 3 | 224 | 704 | 3 | 2 | 4 | 0.314 |
| 30 | 2 | 31 | 5670 | 15 | 14 | 14 | 0.931 |
| 30 | 3 | 961 | 14250 | 10 | 9 | 9 | 0.390 |
| 60 | 2 | 61 | 49590 | 30 | 29 | 29 | 0.966 |
| 60 | 3 | 3721 | 288200 | 20 | 19 | 19 | 0.443 |
| 72 | 2 | 73 | 86940 | 36 | 35 | 35 | 0.972 |
| 72 | 3 | 5329 | 620688 | 24 | 23 | 23 | 0.452 |
| 96 | 2 | 97 | 209808 | 48 | 47 | 47 | 0.979 |
| 100 | 2 | 101 | 237650 | 50 | 49 | 49 | 0.980 |

Empirical:
- **e=2:** `|H|=p` on suite; degree near-tight (N_side/crude ≳ 0.87).
- **e=3:** `|H|/n² ∈ [0.875, 1.0677777777777777]` (Sage full suite).
- All scanned `|H| ≪ H2=77291948627`.

Not a deployed theorem for e=67472.

## PARI arithmetic

status=PASS: H2=77291948627, M_*=4792100814912, deg_comp=16,
n'=1183520, pack=17.

## Residual after H_M (A_SP-prefix toys)

| j | w | free_core | #H | #H_M | #H_R | pairs M | pairs R | frac R |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 5 | 2 | 0 | 110 | 4 | 106 | 8 | 252 | 0.969 |
| 6 | 2 | 1 | 65 | 4 | 61 | 8 | 138 | 0.945 |
| 7 | 2 | 2 | 36 | 3 | 33 | 6 | 74 | 0.925 |
| 8 | 2 | 3 | 19 | 3 | 16 | 10 | 32 | 0.762 |
| 4 | 2 | -1 | 164 | 5 | 159 | 10 | 430 | 0.977 |
| 5 | 2 | 0 | 179 | 5 | 174 | 20 | 548 | 0.965 |
| 6 | 2 | 1 | 127 | 5 | 122 | 14 | 340 | 0.960 |
| 7 | 2 | 2 | 85 | 4 | 81 | 8 | 206 | 0.963 |
| 4 | 2 | -1 | 961 | 9 | 952 | 150 | 11250 | 0.987 |
| 6 | 1 | 3 | 17 | 6 | 11 | 82 | 118 | 0.590 |
| 7 | 1 | 4 | 17 | 5 | 12 | 38 | 94 | 0.712 |
| 8 | 1 | 5 | 16 | 5 | 11 | 26 | 60 | 0.698 |

Census: max frac_R=0.987; avg=0.871;
max H_R=952.

**M-cell is pair-thin; R-cell is the A_SP mass.**

## Program path

```text
H_M ≤ 31          card OK (v43) but few pairs
H_R residual      need C1 max N_ord≤e·p or |H_R|≤H2
CAS e=2,3 growth  under H2 on n≤100 — confidence only
```

## OPEN

1. Residual `max N_ord ≤ e·p` or `|H_R| ≤ H2` at free_core=846161
2. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v44.py --check
# uses sage + gp when on PATH
```
