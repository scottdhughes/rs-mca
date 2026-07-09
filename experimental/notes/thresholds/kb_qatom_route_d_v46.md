# KB-MCA Route-D v46: R2 / H_R2 structure (untyped + Type D)

Status: `PARTIAL` — residual **decomposition + packing** PROVED; small H_R2
envelopes **REFUTED**; deployed `|H_R2|≤n` / H2 **OPEN**.

## Decomposition (PROVED)

```text
R2  =  R2_unt  ⊔  R2_D
```

- **R2_D:** Type D multipad residual pairs (cores pairwise **disjoint**, M_pad≤pack_D)
- **R2_unt:** untyped free-1 (single-core multi-U; not multi-core multipad)

Deployed pack_D = 2.

## Packing (PROVED)

```text
|R2|     ≤  930 · |H_R2|
|R2_D|   ≤  2 · n_mpad_D
```

## Sufficient residual card (PROVED implications)

| If | Then |
|---|---|
| `|H_R2| ≤ H2` | `|R2| ≤ e·p/2` | live OPEN |
| `|H_R2| ≤ n` | `|R2| ≤ 1950351360 ≪ e·p` | **premise REFUTED** (toys) |
| `|H_R2| ≤ A` | `|R2| ≤ 1037924640 ≪ e·p` | premise OPEN / unused |

## False envelopes (BANKED)

`|H_R2| ≤ ⌊n/e⌋`, `≤ 2⌊n/e⌋`, `≤ pack_D·⌊n/e⌋`, **`≤ n`** fail on A_SP residual
(e.g. n=30, `|H_R2|=952`).

## free_core trend (toys)

fc=-1:maxHR2=952, fc=0:maxHR2=73, fc=1:maxHR2=52, fc=2:maxHR2=34, fc=3:maxHR2=22, fc=4:maxHR2=18

free_core≥1: residual **almost pure untyped** (R2_D often 0).

## Toys

| j | w | fc | H_R2 | H_unt | H_D | R2 | R2_unt | R2_D | frac unt | ≤2floor? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 4 | 1 | 1 | 7 | 7 | 0 | 62 | 62 | 0 | 1.00 | True |
| 5 | 1 | 2 | 8 | 8 | 0 | 54 | 54 | 0 | 1.00 | True |
| 5 | 2 | 0 | 49 | 49 | 0 | 110 | 110 | 0 | 1.00 | False |
| 6 | 1 | 3 | 6 | 6 | 0 | 36 | 36 | 0 | 1.00 | True |
| 6 | 2 | 1 | 29 | 29 | 0 | 62 | 62 | 0 | 1.00 | False |
| 7 | 1 | 4 | 6 | 6 | 0 | 28 | 28 | 0 | 1.00 | True |
| 7 | 2 | 2 | 17 | 17 | 0 | 36 | 36 | 0 | 1.00 | False |
| 8 | 2 | 3 | 9 | 9 | 0 | 18 | 18 | 0 | 1.00 | True |
| 9 | 2 | 4 | 4 | 4 | 0 | 8 | 8 | 0 | 1.00 | True |
| 5 | 1 | 2 | 9 | 9 | 0 | 82 | 82 | 0 | 1.00 | True |
| 5 | 2 | 0 | 73 | 73 | 0 | 204 | 204 | 0 | 1.00 | False |
| 6 | 2 | 1 | 52 | 52 | 0 | 132 | 132 | 0 | 1.00 | False |
| 7 | 2 | 2 | 34 | 34 | 0 | 82 | 82 | 0 | 1.00 | False |
| 8 | 2 | 3 | 22 | 22 | 0 | 50 | 50 | 0 | 1.00 | False |
| 9 | 2 | 4 | 18 | 18 | 0 | 38 | 38 | 0 | 1.00 | False |
| 4 | 2 | -1 | 952 | 374 | 940 | 11250 | 2326 | 8924 | 0.21 | False |

Census: max H_R2=952; max R2=11250;
avg frac untyped=0.950.

## Path

```text
SR (Type S) → untyped free-1 + Type D
H_M peels matching
R2 card: need |H_R2|≤H2 or |R2|≤e·p  (not ≤n)
```

## OPEN

1. `|H_R2| ≤ H2` or `|R2| ≤ e·p` at free_core=846161
2. Especially **untyped free-1 residual** high / pair count
3. `A_SP ≤ t·p`

## Reproducibility

```bash
python3 experimental/scripts/verify_kb_qatom_route_d_v46.py --check
```
