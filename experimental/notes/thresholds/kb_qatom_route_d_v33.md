# KB-MCA Route-D v33: free_core=2 non-Helly bound + FM high matching

Status: `PARTIAL` — free_core=2 **non-Helly M_pad t-pack** PROVED; **FM high
matching ≤⌊n/e⌋** PROVED; full pair cover by FM **REFUTED**; connectedness proof OPEN.

## free_core=2 non-Helly M_pad (PROVED)

Through-sets are cliques with `|Cores_r| ≤ T₂ = ⌊(n−2e−1)/(m_c−1)⌋`.

```text
M_pad  ≤  ⌊ t (n−2e) / m_c ⌋  ≤  ⌊ T₂ (n−2e) / m_c ⌋
```

Works for **Helly and non-Helly** Type S at free_core=2.

Deployed-scale if free_core were 2: `T₂=2`, bound
`M_pad ≤ 4`. Actual free_core=`846161`.

## Connectedness (PARTIAL)

| case | status |
|---|---|
| mpad=2 | PROVED |
| all toys | UNIVERSAL (0 counterexamples) |
| general | OPEN |

## FM high matching (PROVED size; incomplete cover)

```text
FM-match: greedy domain order → H_FM
|H_FM| ≤ ⌊n/e⌋ = 31 ≤ K_max = 2176
```

Chosen representatives pairwise disjoint.

**Banked negative:** FM-match does **not** cover all A_SP pairs — many pairs use
unmatched highs. Two-tier payment required.

## Toys

| j | w | free_core | #S | max M_pad S | max t | fc2 bound | fc2 ok? | connected? | #highs | |H_FM| | frac pairs covered |
|---|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| 4 | 1 | 1 | 0 | 1 | 1 | 66 | None | None | 17 | 6 | 0.38 |
| 5 | 1 | 2 | 908 | 9 | 4 | 20 | True | True | 17 | 6 | 0.48 |
| 5 | 2 | 0 | 0 | 1 | 0 | 45 | None | None | 110 | 4 | 0.11 |
| 6 | 1 | 3 | 904 | 14 | 7 | 9 | None | True | 17 | 6 | 0.50 |
| 6 | 2 | 1 | 0 | 1 | 1 | 13 | None | None | 65 | 4 | 0.15 |
| 6 | 3 | -1 | 0 | 1 | 0 | 28 | None | None | 30 | 3 | 0.19 |
| 7 | 1 | 4 | 620 | 17 | 11 | 4 | None | True | 17 | 5 | 0.52 |
| 7 | 2 | 2 | 4 | 2 | 2 | 7 | True | True | 36 | 4 | 0.22 |
| 7 | 3 | 0 | 0 | 1 | 0 | 8 | None | None | 13 | 2 | 0.41 |
| 8 | 1 | 5 | 364 | 14 | 11 | 4 | None | True | 16 | 5 | 0.55 |
| 8 | 2 | 3 | 2 | 2 | 2 | 4 | None | True | 19 | 3 | 0.34 |
| 8 | 3 | 1 | 0 | 1 | 0 | 4 | None | None | 5 | 2 | 0.67 |
| 9 | 2 | 4 | 0 | 1 | 0 | 1 | None | None | 8 | 2 | 0.74 |
| 9 | 3 | 2 | 0 | 1 | 0 | 1 | None | None | 1 | 1 | 1.00 |

Census: Type S=2802 connected; fc2 bound OK=912/912;
nonstar=1328; rows with partial FM pair cover=13.

## OPEN

1. Type S connectedness theorem; non-Helly M_pad at free_core=`846161`
2. Pay unmatched-high A_SP pairs (or force residual into H_FM)

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v33.py --check
```
