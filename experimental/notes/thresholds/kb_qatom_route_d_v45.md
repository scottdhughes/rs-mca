# KB-MCA Route-D v45: residual after SR + H_M

Status: `PARTIAL` — **double residual R2/H_R2** defined; Type D after SR
**PROVED**; residual card criteria **PROVED**; deployed R2/H_R2 gates **OPEN**.

## Residual definitions

```text
Type S multipad  →  paid by SR-cell (r_*)
Type D multipad  →  residual, M_pad ≤ pack_D = ⌊(n−2e)/m_c⌋
                    deployed pack_D = 2

R1 = free-1 CS pairs that are not Type-S multipad sides
R2 = R1 pairs with high ∉ H_M
H_R2 = highs of R2
```

```text
R2  ⊆  R1  ⊆  all free-1 pairs
H_M ≤ ⌊n/e⌋ = 31
```

## Residual card criteria (PROVED conditional)

| Gate | Condition | Pays |
|---|---|---|
| R1-enum | `|R2| ≤ e·p` | residual pairs by μ_all |
| H2-res | `|H_R2| ≤ H2` + M_pad≤2 | N_side≤930·H2 ≤ e·p/2 |
| R1-only | `|R1| ≤ e·p` | after SR, before H_M |

H2 = 77291948627; e·p = 143763024447376.

## Path

```text
1. SR-cell: Type S multipads
2. Type D residual multipads (M_pad ≤ 2 deployed)
3. Untyped free-1 (single-core multi-U pencils) stay in R1
4. H_M peels matching-supported pairs
5. Card-close R2 / H_R2
```

## Toys

| j | w | fc | #pairs | #S | #R1 | #R2 | #H_R2 | #H_M | frac S | frac R2 | max mpad D | D≤pack? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 4 | 1 | 1 | 400 | 286 | 114 | 62 | 7 | 7 | 0.71 | 0.15 | 1 | True |
| 5 | 1 | 2 | 286 | 200 | 86 | 54 | 8 | 6 | 0.70 | 0.19 | 1 | True |
| 5 | 2 | 0 | 260 | 146 | 114 | 110 | 49 | 4 | 0.56 | 0.42 | 1 | True |
| 6 | 1 | 3 | 200 | 132 | 68 | 36 | 6 | 6 | 0.66 | 0.18 | 1 | True |
| 6 | 2 | 1 | 146 | 80 | 66 | 62 | 29 | 4 | 0.55 | 0.42 | 1 | True |
| 6 | 3 | -1 | 60 | 26 | 34 | 30 | 15 | 2 | 0.43 | 0.50 | 1 | True |
| 7 | 1 | 4 | 132 | 86 | 46 | 28 | 6 | 5 | 0.65 | 0.21 | 1 | True |
| 7 | 2 | 2 | 80 | 42 | 38 | 36 | 17 | 3 | 0.53 | 0.45 | 1 | True |
| 7 | 3 | 0 | 26 | 10 | 16 | 14 | 7 | 2 | 0.38 | 0.54 | 1 | True |
| 8 | 1 | 5 | 86 | 52 | 34 | 24 | 6 | 5 | 0.60 | 0.28 | 1 | True |
| 8 | 2 | 3 | 42 | 16 | 26 | 18 | 9 | 3 | 0.38 | 0.43 | 1 | True |
| 9 | 2 | 4 | 16 | 6 | 10 | 8 | 4 | 2 | 0.38 | 0.50 | 1 | True |
| 5 | 1 | 2 | 484 | 354 | 130 | 82 | 9 | 7 | 0.73 | 0.17 | 1 | True |
| 5 | 2 | 0 | 568 | 354 | 214 | 204 | 73 | 5 | 0.62 | 0.36 | 1 | True |
| 6 | 2 | 1 | 354 | 214 | 140 | 132 | 52 | 5 | 0.60 | 0.37 | 1 | True |
| 7 | 2 | 2 | 214 | 126 | 88 | 82 | 34 | 4 | 0.59 | 0.38 | 1 | True |
| 8 | 2 | 3 | 126 | 74 | 52 | 50 | 22 | 4 | 0.59 | 0.40 | 1 | True |
| 4 | 2 | -1 | 11400 | 0 | 11400 | 11250 | 952 | 9 | 0.00 | 0.99 | 20 | True |

Census: max R2=11250; max H_R2=952;
avg frac S=0.537; avg frac R2=0.386;
max frac S=0.731.

Observation: **free_core≥1** often has large Type S fraction ⇒ SR cuts residual
sharply; R2 still the card wall but smaller than full N_pairs.

## OPEN

1. Deployed `|R2| ≤ e·p` or `|H_R2| ≤ H2`
2. Constructive SR e·p mark (separate)
3. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v45.py --check
```
